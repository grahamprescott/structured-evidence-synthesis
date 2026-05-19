# VBAC example

**Research question:** what predicts vaginal birth after caesarean (VBAC)?

**Status:** end-to-end run complete (2026-05-19). Extraction → audit → consolidation → disagreement surfacing → DAG. The setup stage was skipped because the corpus was pre-supplied (13 clinical papers handed in at the start).

This is the "cross-domain" example in the suite. The SAES ontology was designed around environmental-causal claims; this example tests how it holds up against a clinical-predictive domain (binary outcome, regression-heavy literature, structured paper conventions).

## Headline finding

The corpus supports a clinically usable predictor set with several strongly-replicated edges (`prior_vaginal_birth`, `prior_caesarean_indication_recurring`, `macrosomia`, `induction_of_labour`, `maternal_age`). The DAG correctly distinguishes `vbac_success` from `tolac_failure` as complementary outcomes of the same TOLAC attempt — the safety-side edges (uterine rupture, maternal morbidity) originate from `tolac_failure`, not from `vbac_success`. Five edges carry disagreement flags; four are substantive, one is a coding artefact. Full details in [`results/REPORT.md`](results/REPORT.md).

## What's here

| Path | What it is |
|---|---|
| [`context/`](context/) | RTF notes that framed the search and the inclusion criteria. |
| [`articles/README.md`](articles/README.md) | List of the 13 included papers with DOIs. PDFs are not in the repo (mostly paywalled). |
| [`results/extractions/`](results/extractions/) | 13 per-paper CSVs, ~170 relationship rows total. |
| [`results/audits/audit_report.md`](results/audits/audit_report.md) | Audit pass — flagged ~20 novel `[UNVERIFIED]` codes and 5 in-paper conflict cases. |
| [`results/accumulation/`](results/accumulation/) | Consolidated edges (27), disagreement report (5 flagged), union DAG (SVG + metadata). The DAG layout was revised after a first-iteration version drew the safety edges confusingly close to `vbac_success`. |
| [`results/vbac_vocabulary.md`](results/vbac_vocabulary.md) | Seeded controlled vocabulary as run. |
| [`results/REPORT.md`](results/REPORT.md) | Top-level report: headline findings, caveats, next steps. |

## Pipeline order

```
context/Claude VBAC generic.rtf + Notes on OpenAlex search about VBAC 20260519.rtf
  ↓
articles/ (PDFs — pre-supplied, not in repo)
  ↓
results/extractions/{paper_id}.csv                 (13 files)
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
