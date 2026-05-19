# Gold-mining example

**Research question:** direct and indirect impacts of gold mining on biodiversity.

**Status:** end-to-end run complete (2026-05-19). This example demonstrates a **third input mode**: instead of fresh-from-PDF extraction, the rows were migrated from a 2022 manual coding workbook into the v0.2 schema. Audit → consolidation → disagreement surfacing → DAG were then applied on top.

This is the "legacy review translation" example. It tests whether SAES can ingest prior manually-coded evidence bases and produce useful v0.2 outputs without re-reading the PDFs.

## Headline finding

The corpus is internally very consistent (every multi-row edge has unanimous valence). Three pathways converge on biodiversity impact: direct biophysical (deforestation, soil disturbance), the toxic chain (mercury → bioaccumulation, the corpus's strongest sub-graph with `aquatic_mercury_pollution → mercury_bio_accumulation` at n=11), and a socio-economic loop (gold prices, miner influx, enforcement, indigenous land rights). All 4 disagreement flags are vocabulary fragmentation, not substantive.

**The biggest single audit observation:** the `wildlife` outcome code is in the vocabulary but used zero times. The corpus stops at proximate environmental endpoints; species-level biodiversity outcomes are implied, not coded. A v0.2 native re-extraction from the PDFs is the recommended next step. Full details in [`results/REPORT.md`](results/REPORT.md).

## What's here

| Path | What it is |
|---|---|
| [`context/research_question.md`](context/research_question.md) | The framing. |
| [`context/screening_decisions.md`](context/screening_decisions.md) | Why the 8 included papers were chosen from the 2022 Scopus search; why 5 prior PDFs were excluded. |
| [`context/prior_work_translation.md`](context/prior_work_translation.md) | **Required reading** — explains how the 2022 manual coding workbook was migrated into the v0.2 row schema, with column mapping and known fidelity limitations. |
| [`articles/README.md`](articles/README.md) | List of the 8 included papers with DOIs. PDFs are not in the repo; only Asner 2017 is open access. |
| [`results/extractions/`](results/extractions/) | 8 per-paper CSVs, 105 rows total (translated from 143 gold rows in the 2022 workbook). |
| [`results/audits/audit_report.md`](results/audits/audit_report.md) | Audit focused on the migration's limits (no effect sizes, paper-level method-type) and the missing biodiversity-outcome codes. |
| [`results/accumulation/`](results/accumulation/) | Consolidated edges (43), disagreement report (4 flagged, all vocabulary), union DAG (SVG + metadata). |
| [`results/gold_mining_vocabulary.md`](results/gold_mining_vocabulary.md) | Vocabulary as inherited from the 2022 coding. |
| [`results/REPORT.md`](results/REPORT.md) | Top-level report: pathways, where biodiversity sits in the DAG, full caveats. |

## Pipeline order

```
2022 Scopus search workbook (held outside repo)
  ↓
context/screening_decisions.md + research_question.md
  ↓
2022 manual coding workbook (held outside repo, 143 gold rows)
  ↓  [context/prior_work_translation.md — column mapping]
results/extractions/{paper_id}.csv                 (8 files, 105 rows)
  ↓
results/audits/audit_report.md
  ↓
results/accumulation/extracted_rows.csv            (concatenation)
  ↓
results/accumulation/consolidated_edges.json
  ↓
results/accumulation/disagreement_report.md
  ↓
results/accumulation/union_dag.svg + dag_metadata.json
  ↓
results/REPORT.md
```
