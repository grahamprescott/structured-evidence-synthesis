# Extraction — the SAES core

The middle stage of the SAES pipeline, and the one that has been run end-to-end and benchmarked against human coding (v0.1.2 release).

Per paper: an LLM reads the paper and codes every claimed relationship between variables against a defined schema, with every coded field paired with the verbatim text it was derived from. A second LLM pass then audits the extraction against the schema and the source paper, producing an issue list rather than a silently revised output.

## What this stage does

```
Screened paper (PDF + paper metadata)
       ↓
   extraction.md   — LLM extracts one directional relationship per row
       ↓
   audit.md        — second LLM pass checks against schema + verbatim text
       ↓
Audited relationship rows (CSV conforming to row.schema.json)
```

## Inputs and outputs

| Input | Output |
|---|---|
| Full text of one paper | One CSV of extracted rows per paper, conforming to `schemas/row.schema.json` |
| `schemas/row.schema.json` (or its CSV-header equivalent) | One audit report per extraction, identifying issues against the schema and the verbatim text |
| Optional: controlled vocabulary for subject/object codes (`ontology/`) | |

## The discipline

Two commitments, carried forward unchanged from v0.1.2:

1. **Variables and relationships are the unit of extraction.** Most synthesis questions reduce to: does a relationship between two variables exist, what is its direction, and what is its magnitude? The schema is built around extracting one directional relationship per row.

2. **Dual-layer architecture.** Every coded field is paired with the verbatim text it was derived from. This is the primary mechanism for transparency and auditability — a reviewer (or a future LLM auditor) can always see what the LLM was looking at when it made a coding decision.

A third commitment is the audit step itself:

3. **Generation and evaluation are separated.** The audit is run by a different LLM session (or, ideally, a different model) than the extraction. The audit produces an issue list; it does not silently revise the extraction. A human reviewer adjudicates.

## Files in this stage

### Prompts

- [`prompts/extraction.md`](prompts/extraction.md) — generic LLM prompt template for the extraction step.
- [`prompts/audit.md`](prompts/audit.md) — generic LLM prompt template for the audit step.

### Schema and ontology

- [`schemas/row.schema.json`](schemas/row.schema.json) — JSON schema for one extracted relationship row. Implements the ontology specification.
- [`ontology/subject_codes.md`](ontology/subject_codes.md) — controlled vocabulary stub for `subject_code` values.
- [`ontology/object_codes.md`](ontology/object_codes.md) — controlled vocabulary stub for `object_code` values.

> **Note on naming.** The checklist refers to these as `v1_codes.md` and `v2_codes.md`, matching the v0.1.1 ontology. The v0.1.2 ontology renamed `v1`/`v2` to `subject`/`object`; the files here use the v0.1.2 names. References elsewhere in the repo to `v1_code` / `v2_code` should be considered stale.

## What downstream stages expect

The accumulation stage operates on a *row-set* — the concatenation of per-paper extracted CSVs across the included corpus, with `paper_id` (column A1) preserved as the provenance key. Each row must validate against `row.schema.json`.

The accumulation stage will:

- Group rows by `(subject_code, object_code)` to form the edges of the consolidated DAG.
- Stratify within each edge by `method_type` and `causal_inference_level` — never naively averaging effect sizes across method types or populations.
- Surface disagreements (same edge, opposite `rel_valence` or conflicting magnitudes).

For these operations to work, the `subject_code` and `object_code` controlled vocabularies need to be reasonably stable across papers. This is the single largest source of friction in scaling SAES — see the cocoa-biodiversity example (`examples/cocoa-biodiversity/`) for an illustration of how `object_code` fragments across closely related papers when the vocabulary is not pre-specified.

## Worked example

The Asner & Tupayachi (2017) paper on gold mining in the Peruvian Amazon was the v0.1.1 worked example. Extraction and audit have been run end-to-end, and the LLM extraction has been compared against an independent human-coded extraction. See [`examples/gold-mining/`](../examples/gold-mining/) for the run.

## What's not yet here

- A `schema_for_ontology_v0.1.2.csv` companion table. The JSON schema is canonical for now.
- Populated controlled vocabularies. The ontology files are stubs with example entries; production runs require domain-specific population.
- An automated extraction-vs-human-coding diff tool. The comparison in v0.1.2 was done by hand.
