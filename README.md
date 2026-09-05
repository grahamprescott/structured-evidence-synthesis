# Structured AI-Assisted Evidence Synthesis (SAES)

**Version 0.2.0-alpha**

This is a research workflow for AI-assisted evidence synthesis from scientific literature.

This release expands the v0.1 prototype—a single extraction-and-audit pass on one paper—into an end-to-end workflow that runs from a research question to a consolidated, auditable evidence base. The underlying principle is that **every stage produces outputs traceable to its inputs.**

> **Scope.** SAES runs from research question to consolidated evidence base. Simulation, theory-building, and forward synthesis are out of scope.

---

## The pipeline

```
Research question
       ↓
   1. SETUP        →  Screened corpus + search log
       ↓
   2. EXTRACTION   →  Audited relationship rows
       ↓
   3. ACCUMULATION →  Consolidated evidence base with provenance
```

See [`docs/flowchart.svg`](docs/flowchart.svg) for the full pipeline diagram, including the documents produced at each stage. The argument for why this matters is in [`docs/covering-essay.md`](docs/covering-essay.md). A cross-trial reflection on the three worked examples is in [`docs/v0.2_trials_summary.md`](docs/v0.2_trials_summary.md).

| Stage | What it does | Traceable to | Status in v0.2.0-alpha |
|---|---|---|---|
| [setup/](setup/) | Question framing → OpenAlex search → title/abstract screening | a logged search string + screening decisions | proof of concept, exercised once at small scale (cocoa example) |
| [extraction/](extraction/) | Per-paper LLM extraction of variable–relationship rows, plus a second-pass LLM audit | verbatim text from the source paper | exercised on three corpora (8-13 papers each) |
| [accumulation/](accumulation/) | Consolidation across rows: count, valence distribution, disagreement surfacing, optional union DAG | the row-set being aggregated, with provenance back to source row IDs | exercised on three corpora; produced 27/31/43 consolidated edges and union DAGs |

Each stage has its own `README.md` describing inputs, outputs, prompts, and discipline.

---

## What's new in v0.2 vs v0.1

- **SETUP and ACCUMULATION** are new stages, framing the existing extraction work as the middle of a longer pipeline. Both have been exercised end-to-end on three corpora (see `examples/`); neither has been stress-tested at scale beyond ~13 papers.
- **EXTRACTION** is essentially the v0.1.2 SAES core, moved into `extraction/`. The ontology, schema, and prompts pass through with minor renaming (`v1`/`v2` → `subject`/`object` to match the v0.1.2 ontology specification).
- **Examples**: three worked runs at different difficulty levels. All three completed end-to-end on 2026-05-19. See [`docs/v0.2_trials_summary.md`](docs/v0.2_trials_summary.md) for a cross-trial reflection.
  - [`examples/cocoa-biodiversity/`](examples/cocoa-biodiversity/) — full pipeline from OpenAlex search through DAG. Stress-tests vocabulary fragmentation on the predictor side.
  - [`examples/vbac/`](examples/vbac/) — extraction onwards from a pre-supplied 13-paper corpus. Stress-tests cross-domain generalisation (the environmental-causal ontology applied to clinical prediction).
  - [`examples/gold-mining/`](examples/gold-mining/) — demonstrates a third input mode: migration of a 2022 manual coding workbook into the v0.2 schema, then audit / accumulation applied on top.

See [`CHANGELOG.md`](CHANGELOG.md) for full version history.

---

## Why this design

**AI-assisted evidence synthesis is easy to generate but challenging to evaluate.** SAES addresses this by:

1. Forcing every coded field to be paired with the verbatim text it came from.
2. Splitting generation from evaluation at every stage — extraction is followed by audit; consolidation is followed by disagreement surfacing.
3. Logging the inputs (search strings, screening decisions, source row IDs) so any consolidated claim can be traced back to the papers it draws on.

See examples: https://github.com/grahamprescott/structured-evidence-synthesis/tree/main/examples

---

## Quick start

The protocol is operated by hand for now — you copy prompts into an LLM session and feed it papers and schemas. Automation will follow once the prompts have stabilised.

1. **SETUP** — work through [`setup/prompts/01_question_framing.md`](setup/prompts/01_question_framing.md), then [`02_openalex_search.md`](setup/prompts/02_openalex_search.md), then [`03_screening.md`](setup/prompts/03_screening.md). For bulk PDF downloads from OpenAlex, see [`setup/scripts/openalex_pdf_download.py`](setup/scripts/openalex_pdf_download.py).
2. **EXTRACTION** — for each screened paper, run [`extraction/prompts/extraction.md`](extraction/prompts/extraction.md) followed by [`extraction/prompts/audit.md`](extraction/prompts/audit.md).
3. **ACCUMULATION** — over the row-set, run [`accumulation/prompts/01_consolidation.md`](accumulation/prompts/01_consolidation.md), then [`02_disagreement_surfacing.md`](accumulation/prompts/02_disagreement_surfacing.md), optionally [`03_dag_construction.md`](accumulation/prompts/03_dag_construction.md).

Worked examples live in [`examples/`](examples/).

---

## Citation and contact

If you use or build on this protocol, please cite the repository and get in touch. See [`CITATION.cff`](CITATION.cff). Bug reports, suggestions for ontology revisions, and benchmark contributions especially welcome.

Graham Prescott · graham.prescott@gmail.com · [grahamprescott.substack.com](https://grahamprescott.substack.com/)
