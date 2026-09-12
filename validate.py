#!/usr/bin/env python3
"""validate.py — check SAES worked examples against their own rows.

Three checks, all computed from the data rather than the prose:

1. SCHEMA   every per-paper CSV in results/extractions/ is checked against
            extraction/schemas/row.schema.json (required fields, enum values,
            conditional requirements).
2. EDGES    consolidated_edges.json is recomputed from the rows: which edges
            exist, n_rows, valence tallies, and whether every provenance ID
            (paper_id:rN) points at a real row.
3. QUOTES   every blockquote under a row reference in disagreement_report.md
            is checked against that row's rel_raw.

Also prints the row-level counts the docs quote (rows, controlled comparison,
trend-only, numeric effect sizes) so they never have to be typed from memory.

Usage:
    python3 validate.py                      # all examples
    python3 validate.py examples/vbac        # one example
    python3 validate.py --strict             # exit 1 on any failure

Row IDs are positional: paper_id:rN is the Nth data row (1-based) of
results/extractions/<paper_id>.csv. That is how the accumulation prompts
cite rows today; a stable row_id column is a planned improvement.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "extraction", "schemas", "row.schema.json")

VALENCE_KEY = {
    "Positive": "positive",
    "Negative": "negative",
    "Non-linear": "non_linear",
    "Indeterminate": "indeterminate",
}


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm(s: str) -> str:
    """Normalise text for quote comparison: collapse whitespace, unify quotes/dashes, lowercase."""
    s = s or ""
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("[...]", " ").replace("…", " ")
    s = re.sub(r"\s+", " ", s).strip().strip('"').strip()
    return s.lower()


def is_empty(v) -> bool:
    return v is None or str(v).strip() == ""


def code(v: str) -> str:
    """Edge key for a subject/object code: the consolidation stage drops the
    [UNVERIFIED] marker that extraction attaches to codes outside the seeded vocabulary."""
    return re.sub(r"\s*\[UNVERIFIED\]", "", (v or "").strip())


# ----------------------------------------------------------------------------
# 1. schema check
# ----------------------------------------------------------------------------

def check_schema(example_dir, schema, report):
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    enums = {k: set(v["enum"]) for k, v in props.items() if "enum" in v}
    # conditional requirements expressed as allOf/if-then in the schema
    conditionals = []
    for clause in schema.get("allOf", []):
        cond = clause.get("if", {}).get("properties", {})
        then_req = clause.get("then", {}).get("required", [])
        if cond and then_req:
            conditionals.append((cond, then_req))

    files = sorted(glob.glob(os.path.join(example_dir, "results", "extractions", "*.csv")))
    if not files:
        report.fail("schema", "no per-paper CSVs found in results/extractions/")
        return {}

    rows_by_paper = {}
    issues = Counter()
    examples = defaultdict(list)
    for path in files:
        paper = os.path.splitext(os.path.basename(path))[0]
        rows = read_csv(path)
        rows_by_paper[paper] = rows
        for i, row in enumerate(rows, start=1):
            rid = f"{paper}:r{i}"
            if row.get("paper_id", "").strip() != paper:
                issues["paper_id != filename"] += 1
                examples["paper_id != filename"].append(rid)
            for k in required:
                if is_empty(row.get(k)):
                    issues[f"missing required {k}"] += 1
                    examples[f"missing required {k}"].append(rid)
            for k, allowed in enums.items():
                v = row.get(k)
                if is_empty(v):
                    continue
                if v.strip() not in allowed:
                    key = f"non-enum {k}={v.strip()!r}"
                    issues[key] += 1
                    examples[key].append(rid)
            for cond, then_req in conditionals:
                matches = all((row.get(k) or "").strip() in set(v.get("enum", [v.get("const")])) for k, v in cond.items())
                if matches:
                    for k in then_req:
                        if is_empty(row.get(k)):
                            key = f"conditional: {k} required when {cond}"
                            issues[key] += 1
                            examples[key].append(rid)

    total = sum(len(r) for r in rows_by_paper.values())
    report.info("schema", f"{len(files)} papers, {total} rows")
    if issues:
        for key, n in issues.most_common():
            report.fail("schema", f"{n}× {key}  e.g. {', '.join(examples[key][:3])}")
    else:
        report.ok("schema", "all rows conform")

    # extracted_rows.csv, if present, must be the concatenation of the per-paper files
    concat = os.path.join(example_dir, "results", "accumulation", "extracted_rows.csv")
    if os.path.exists(concat):
        n = len(read_csv(concat))
        if n != total:
            report.fail("schema", f"extracted_rows.csv has {n} rows; per-paper CSVs total {total}")
        else:
            report.ok("schema", f"extracted_rows.csv matches per-paper CSVs ({n} rows)")
    return rows_by_paper


# ----------------------------------------------------------------------------
# 2. edge recompute
# ----------------------------------------------------------------------------

def recompute_edges(rows_by_paper):
    edges = defaultdict(lambda: {"n_rows": 0, "valence": Counter(), "rows": []})
    for paper, rows in rows_by_paper.items():
        for i, row in enumerate(rows, start=1):
            if (row.get("subject_trend_only") or "").strip() == "Yes":
                continue
            s, o = code(row.get("subject_code")), code(row.get("object_code"))
            if not s or not o:
                continue
            e = edges[(s, o)]
            e["n_rows"] += 1
            e["valence"][VALENCE_KEY.get((row.get("rel_valence") or "").strip(), "other")] += 1
            e["rows"].append(f"{paper}:r{i}")
    return edges


def check_edges(example_dir, rows_by_paper, report):
    path = os.path.join(example_dir, "results", "accumulation", "consolidated_edges.json")
    if not os.path.exists(path):
        report.info("edges", "no consolidated_edges.json; skipped")
        return
    with open(path) as f:
        data = json.load(f)
    json_edges = data if isinstance(data, list) else data.get("edges", [])
    computed = recompute_edges(rows_by_paper)

    json_keys = {(e.get("subject_code"), e.get("object_code")): e for e in json_edges}
    missing = [k for k in computed if k not in json_keys]
    extra = [k for k in json_keys if k not in computed]
    report.info("edges", f"rows imply {len(computed)} edges; consolidated_edges.json has {len(json_edges)}")
    if missing:
        report.fail("edges", f"{len(missing)} edges in rows but not in JSON  e.g. " +
                    ", ".join(f"{s} -> {o} (n={computed[(s,o)]['n_rows']})" for s, o in missing[:3]))
    if extra:
        report.fail("edges", f"{len(extra)} edges in JSON with no supporting rows  e.g. " +
                    ", ".join(f"{s} -> {o}" for s, o in extra[:3]))

    count_bad, val_bad = [], []
    for k, e in json_keys.items():
        if k not in computed:
            continue
        c = computed[k]
        if e.get("n_rows") != c["n_rows"]:
            count_bad.append(f"{k[0]} -> {k[1]}: JSON n_rows={e.get('n_rows')} rows={c['n_rows']}")
        vd = e.get("valence_distribution") or {}
        for key in ("positive", "negative", "non_linear", "indeterminate"):
            if int(vd.get(key, 0) or 0) != c["valence"].get(key, 0):
                val_bad.append(f"{k[0]} -> {k[1]}: {key} JSON={vd.get(key, 0)} rows={c['valence'].get(key, 0)}")
                break
    if count_bad:
        report.fail("edges", f"{len(count_bad)} edges with wrong n_rows  e.g. " + "; ".join(count_bad[:3]))
    if val_bad:
        report.fail("edges", f"{len(val_bad)} edges with wrong valence tallies  e.g. " + "; ".join(val_bad[:3]))

    # provenance resolution
    valid_ids = {rid for c in computed.values() for rid in c["rows"]}
    all_ids = {f"{p}:r{i}" for p, rows in rows_by_paper.items() for i in range(1, len(rows) + 1)}
    unresolved, total_ids = [], 0
    for e in json_edges:
        for rid in e.get("provenance_row_ids") or []:
            total_ids += 1
            if rid not in all_ids:
                unresolved.append(rid)
    if total_ids:
        if unresolved:
            report.fail("edges", f"{len(unresolved)}/{total_ids} provenance IDs do not resolve to a row  e.g. {', '.join(unresolved[:4])}")
        else:
            report.ok("edges", f"all {total_ids} provenance IDs resolve")
    if not (missing or extra or count_bad or val_bad or unresolved):
        report.ok("edges", "consolidation reconciles exactly with rows")


# ----------------------------------------------------------------------------
# 3. quote check
# ----------------------------------------------------------------------------

QUOTE_RE = re.compile(r"^- `([A-Za-z0-9_\-]+):r(\d+)[^`]*`.*?\n\s*> \"?(.+?)\"?\s*$", re.M)


def check_quotes(example_dir, rows_by_paper, report):
    path = os.path.join(example_dir, "results", "accumulation", "disagreement_report.md")
    if not os.path.exists(path):
        report.info("quotes", "no disagreement_report.md; skipped")
        return
    text = open(path, encoding="utf-8").read()
    found = QUOTE_RE.findall(text)
    if not found:
        report.info("quotes", "no row-referenced blockquotes found")
        return
    exact = approx = bad = 0
    bad_examples = []
    for paper, n, quote in found:
        rows = rows_by_paper.get(paper)
        n = int(n)
        if not rows or n > len(rows):
            bad += 1
            bad_examples.append(f"{paper}:r{n} (row does not exist)")
            continue
        raw = norm(rows[n - 1].get("rel_raw") or "")
        q = norm(quote)
        frags = [norm(f) for f in re.split(r"\[\.\.\.\]|\u2026", quote)]
        frags = [f for f in frags if len(f) > 3]
        if q and (q in raw or raw in q):
            exact += 1
        elif len(frags) > 1 and all(f in raw for f in frags):
            approx += 1
        else:
            bad += 1
            bad_examples.append(f"{paper}:r{n}")
    report.info("quotes", f"{len(found)} row-referenced quotes: {exact} verbatim, {approx} elided-but-consistent, {bad} not in the cited row")
    if bad:
        report.fail("quotes", f"{bad} quotes do not match their cited row  e.g. {', '.join(bad_examples[:4])}")
    else:
        report.ok("quotes", "every quote matches its cited row")


# ----------------------------------------------------------------------------
# counts the docs quote
# ----------------------------------------------------------------------------

def doc_counts(rows_by_paper, report):
    rows = [r for rs in rows_by_paper.values() for r in rs]
    n = len(rows)
    if not n:
        return
    cc = sum(1 for r in rows if (r.get("causal_inference_level") or "").strip() == "Controlled comparison")
    iv = sum(1 for r in rows if (r.get("causal_inference_level") or "").strip() == "Intervention")
    tr = sum(1 for r in rows if (r.get("subject_trend_only") or "").strip() == "Yes")
    strict = sum(1 for r in rows if re.fullmatch(r"-?\d+(\.\d+)?", (r.get("effect_magnitude") or "").strip().replace("−", "-")))
    anynum = sum(1 for r in rows if re.search(r"\d", r.get("effect_magnitude") or ""))
    report.info("counts", f"rows={n}  intervention={iv}  controlled_comparison={cc}  trend_only={tr}  "
                          f"effect_magnitude numeric={strict} ({strict/n:.0%}) any-number={anynum} ({anynum/n:.0%})")


# ----------------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------------

class Report:
    def __init__(self, name):
        self.name = name
        self.failures = 0
        print(f"\n== {name}")

    def ok(self, stage, msg):
        print(f"  PASS [{stage}] {msg}")

    def info(self, stage, msg):
        print(f"  info [{stage}] {msg}")

    def fail(self, stage, msg):
        self.failures += 1
        print(f"  FAIL [{stage}] {msg}")


def main(argv):
    strict = "--strict" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        targets = sorted(d for d in glob.glob(os.path.join(ROOT, "examples", "*")) if os.path.isdir(d))
    schema = load_schema()
    total_failures = 0
    for t in targets:
        t = os.path.abspath(t)
        rep = Report(os.path.relpath(t, ROOT))
        rows_by_paper = check_schema(t, schema, rep)
        if rows_by_paper:
            doc_counts(rows_by_paper, rep)
            check_edges(t, rows_by_paper, rep)
            check_quotes(t, rows_by_paper, rep)
        total_failures += rep.failures
    print(f"\n{total_failures} failure(s) across {len(targets)} example(s)")
    return 1 if (strict and total_failures) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
