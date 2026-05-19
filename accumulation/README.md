# Accumulation — consolidation across rows

The third stage of the SAES pipeline. Aggregates the per-paper extracted rows from the [extraction stage](../extraction/) into a consolidated evidence base, edge by edge, with provenance back to the source row IDs.

> **Status: proof of concept.** This is the new frontier of v0.2 — the stage that has not been run end-to-end at scale. Prompts and schemas are drafts; the discipline they encode is more important than the specifics.

## What this stage does

```
Audited relationship rows (the row-set across the included corpus)
       ↓
   01_consolidation         — collapse K rows on the same edge into one summary row,
                              stratified by method_type and causal_inference_level
       ↓
   02_disagreement_surfacing — surface edges where rows conflict; show side by side
       ↓
   03_dag_construction (opt) — build the union DAG of all extracted edges,
                              colour by evidence strength, flag disagreements
       ↓
Consolidated evidence base with end-to-end provenance
```

## Inputs and outputs

| Input | Output |
|---|---|
| The concatenated row-set across the included corpus (`extracted_rows.csv`, conforming to `extraction/schemas/row.schema.json`) | `consolidated_edges.json` — one entry per `(subject_code, object_code)` edge, conforming to `schemas/consolidated-edge.schema.json` |
| | `disagreement_report.md` — narrative report of edges where extracted rows conflict |
| | Optional: `union_dag.svg` and `dag_metadata.json` from `03_dag_construction.md` |
| | Optional: `accumulation_curve.csv` — new edges contributed per paper added (saturation analysis; see "Saturation curve" below) |

## The discipline

Three rules. None are technically enforced; all are enforced by prompt design and by audit.

### 1. Stratify before you summarise.

For any edge with K extracted rows, the consolidation does *not* produce a single "average effect" or a single "consensus valence". It produces a stratified summary:

- Count of rows.
- Distribution of `rel_valence` (positive / negative / non-linear / indeterminate).
- Distribution of `causal_inference_level` (association / controlled comparison / intervention / counterfactual).
- Distribution of `method_type`.
- Distribution of `population_code` and `geographic_scope_code`.

The reader sees the shape of the evidence base for that edge. They can draw their own conclusion about whether it's a robust finding or an artefact of one methodology.

### 2. No naive averaging across methods or populations.

Effect sizes are reported per row. The consolidation does not pool effect sizes across rows from different `method_type` or different `population_code`. Where a within-stratum pooling is informative, it is reported separately and labelled as such — never as the "overall" effect.

This is the rule that distinguishes accumulation from meta-analysis. Meta-analysis assumes exchangeability of the things being pooled; SAES does not, by design.

### 3. Provenance is mandatory.

Every consolidated edge carries the list of source row IDs it draws on. A reader who wants to check a claim can follow the chain: consolidated edge → source rows → verbatim text in source papers. This is not optional; it is the contract the protocol makes with the reader.

## Files in this stage

### Prompts

- [`prompts/01_consolidation.md`](prompts/01_consolidation.md) — given K rows sharing `(subject_code, object_code)`, produce a summary entry with count, distributions, stratifications, and source row IDs.
- [`prompts/02_disagreement_surfacing.md`](prompts/02_disagreement_surfacing.md) — for edges with conflicting valences or magnitudes, show rows side by side with their verbatim text. This is where the most evidence-synthesis-relevant questions live.
- [`prompts/03_dag_construction.md`](prompts/03_dag_construction.md) *(optional)* — build the union graph of all extracted edges, colour by evidence strength, flag disagreements visually.

### Schemas

- [`schemas/consolidated-edge.schema.json`](schemas/consolidated-edge.schema.json) — JSON schema for one consolidated edge.
- [`schemas/disagreement-report.schema.md`](schemas/disagreement-report.schema.md) — Markdown template for the disagreement-surfacing output.

## Saturation curve

A separate, optional, but useful analysis: as papers are added to the corpus one at a time, how many *new* edges does each paper contribute to the consolidated DAG?

```
paper_1 → 16 new edges → cumulative 16
paper_2 → 10 new edges → cumulative 26
paper_3 →  5 new edges → cumulative 31
paper_4 →  2 new edges → cumulative 33
paper_5 →  6 new edges → cumulative 39
paper_6 →  0 new edges → cumulative 39   ← saturation begins
paper_7 →  0 new edges → cumulative 39
...
```

When the new-edges-per-paper curve flattens, the corpus has saturated with respect to the consolidated DAG: each additional paper is replicating known edges rather than introducing new ones. This is a useful corpus-completeness signal and a candidate stopping rule for the SETUP stage (see `setup/prompts/01_question_framing.md`, question 7).

The curve does *not* tell you the corpus has saturated with respect to the **evidence strength** of individual edges — additional papers continue to refine effect sizes and stratification even after no new edges appear.

## What's not here yet

- A reference implementation of the saturation curve (it's currently produced by hand from the consolidated row-set).
- Vocabulary-mapping logic for harmonising `subject_code`/`object_code` across papers. The consolidation prompt currently treats string-identical codes as the same edge; a real implementation would apply a mapping table.
- Automation. All three prompts are run by hand against the LLM.

## Pointers

- The inspiration for the saturation curve is the link-accumulation analysis in the user's mining-review coding spreadsheet (`Coding for mining review revision 2022.xlsx`, tab `link_accumulation_info`).
- The inspiration for the DAG visualisation is the Causal Networks slide deck — annotated DAGs with +/− edges, evidence-strength colour, and policy-solution overlays.
