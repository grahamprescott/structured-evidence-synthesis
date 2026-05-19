# Disagreement report — schema and template

This file defines the structure of `disagreement_report.md`, the output of `accumulation/prompts/02_disagreement_surfacing.md`. It is itself a template: copy the structure below and populate one H2 section per flagged edge.

---

## Required structure

The report must contain, in order:

1. **A YAML or Markdown front-matter block** with the run metadata (date, corpus reference, consolidation run reference, total edges, flagged edges).
2. **A summary table** listing every flagged edge with its disagreement type(s) and the recommended next step.
3. **One H2 section per flagged edge**, following the per-edge template below.

The unflagged-edges section is optional — most disagreement reports do not include unflagged edges. If included, summarise them in a single appendix table at the end.

---

## Per-edge section template

Each H2 section has the form:

```markdown
## {subject_code} → {object_code}

**Disagreement type:** {valence | existence | magnitude | direction | conditionality} (comma-separated if multiple)

**N rows on edge:** {n_rows from consolidated_edges.json}
**Valence distribution:** {summary line, e.g. "3 negative, 2 positive"}

{Optional one-sentence framing of what's at stake on this edge — why a downstream reader should care about the conflict.}

**{Group label 1, e.g. "Negative-valence rows"}**:

- `{row_id}` ({paper_id}, {method_type}, {causal_inference_level}, {geographic_scope_raw or _code}, {population_code})
  > "{rel_raw verbatim text}"
- `{row_id}` (...)
  > "{rel_raw verbatim text}"

**{Group label 2, e.g. "Positive-valence rows"}**:

- `{row_id}` (...)
  > "{rel_raw verbatim text}"

**Triage:**

- **Pass 1 (stratification):** {One or two sentences. Does the disagreement track a method_type, population_code, or geographic_scope_code split? If yes, describe.}
- **Pass 2 (substantive):** {One or two sentences. If Pass 1 did not explain the disagreement, is it a substantive conflict in the literature?}

**Recommended next step:** {Stratify | Re-audit rows | Substantive disagreement; flag in synthesis | Insufficient evidence} — {short rationale}
```

---

## Field rules

- **Row identifiers** in backticks: `{row_id}`. If row IDs are not assigned, use `{paper_id}:r{row_index}`.
- **Verbatim quotes** as Markdown blockquotes (`> ...`). Quote `rel_raw` from the source row exactly. Do not paraphrase.
- **Method/level/population tags** in the parenthetical line, in the order: `paper_id, method_type, causal_inference_level, geographic_scope, population_code`. Use ASCII em-dashes (`—`) for missing values.
- **Triage** is mandatory. The two passes (stratification first, substantive second) reflect the protocol's commitment to checking the boring explanation before reaching for the interesting one.
- **Recommended next step** must be one of the four declared options. If none fit, the disagreement-surfacing prompt has missed a case — flag it.

---

## What this template enforces

- **The verbatim text is in the report.** The reader does not need to open the source paper to see what the conflicting claims actually said. They might still want to, but they should not have to.
- **The disagreement is named.** "Valence conflict" or "magnitude conflict" or "direction conflict" — not vague "discrepancies" or "heterogeneity" language that papers over what's actually different.
- **Both sides are shown.** Not "the literature is mixed" — here are the rows that say one thing, and here are the rows that say the other.
- **The triage is two-step.** Boring explanation (stratification) checked first, interesting explanation (substantive conflict) second. This avoids the common failure mode of treating an artefact of method as a substantive disagreement in the literature.
- **The next step is concrete.** Stratify, re-audit, flag, defer — one of four. Not "investigate further".

---

## Anti-patterns to avoid

- **A summary table without per-edge sections.** The summary table is for navigation; the per-edge sections are the actual report.
- **A consensus estimate per edge.** This document exists *because* the edge does not have a consensus estimate. Producing one defeats the purpose.
- **Hiding low-n disagreements.** "Only two papers" is not a reason to omit — it is grounds for the `Insufficient evidence` recommendation. Make the small-n state visible.
- **Quietly excluding `rel_exists=Uncertain` rows.** Uncertain rows count in the conflict; they are part of why the literature is unsettled.
