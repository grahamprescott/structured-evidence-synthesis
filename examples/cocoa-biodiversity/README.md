# Cocoa-biodiversity example

**Research question:** how does biodiversity affect cocoa yields?

**Status:** end-to-end run complete (2026-05-19). Full pipeline from OpenAlex search → screening → download → extraction → audit → consolidation → disagreement surfacing → DAG.

This is the "intermediate-difficulty" example in the suite. It stress-tests vocabulary fragmentation on the predictor side (shade-tree density vs species richness vs cover percentage vs functional diversity vs `agroforestry_vs_monoculture` — five facets of "shade" that the literature uses interchangeably) and outcome-side conflation (yield magnitude vs yield stability under the same `cocoa_yield` code).

## Headline finding

The corpus does not support a single direction for "biodiversity → cocoa yield." It supports four distinct sub-claims: more shade reduces yield magnitude; functional diversity of shade-tree species recovers it; ambient pollinator service is the binding constraint (the only Intervention-level evidence); and agroforestry supports yield stability under climate stress, separately from magnitude. Full details in [`results/REPORT.md`](results/REPORT.md).

## What's here

| Path | What it is |
|---|---|
| [`context/`](context/) | Research question, OpenAlex search log, screening decisions. |
| [`articles/README.md`](articles/README.md) | List of the 8 included papers with DOIs. PDFs are not in the repo. |
| [`openalex_pdf_download.py`](openalex_pdf_download.py) | The helper script used to fetch OA PDFs for this run. |
| [`download_log.csv`](download_log.csv), [`openalex_works.jsonl`](openalex_works.jsonl) | What was actually downloaded, with timestamps and OpenAlex IDs. |
| [`results/extractions/`](results/extractions/) | 8 per-paper CSVs, 57 relationship rows total. |
| [`results/audits/audit_report.md`](results/audits/audit_report.md) | Audit pass over the 8 extractions. |
| [`results/accumulation/`](results/accumulation/) | Consolidated edges (31), disagreement report (3 flagged), union DAG (SVG + metadata). |
| [`results/cocoa_vocabulary.md`](results/cocoa_vocabulary.md) | Seeded controlled vocabulary as run. |
| [`results/REPORT.md`](results/REPORT.md) | Top-level report: headline findings, caveats, next steps. |

## Pipeline order

```
context/research_question.md
context/search_log.json + screening_decisions.md
  ↓
articles/ (PDFs — fetched per articles/README.md, not in repo)
  ↓
results/extractions/{paper_id}.csv                 (8 files)
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
