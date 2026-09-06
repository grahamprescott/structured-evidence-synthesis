# Structured AI-Assisted Evidence Synthesis (SAES)

**Version 0.2.1-alpha**

When we ask an LLM a question, the LLM searches and screens the available evidence, extracts claims, weighs conflicting evidence, and consolidates what it finds into a fluent narrative to answer the question. We currently receive the LLM's answer, but the process behind arriving at that answer is opaque. We don't know what the LLM searched or extracted, or what conflicts it had to resolve. 

SAES is an open protocol that makes each of those steps explicit and auditable, tracing every claim to its source text, logging every search and screening decision, surfacing disagreements between sources, and building a map of how the evidence connects across the whole corpus.

This protocol has been tested on three questions spanning medicine, agriculture and environmental impact. It is applicable to any literature that makes causal claims. The intention is to develop and test it until it can be used wherever people ask an LLM "what does the evidence say about x?"

> **Scope.** SAES runs from research question to consolidated evidence base. It is not intended for use in simulation, theory-building, or forward synthesis.

---

## Why this design

**AI-assisted evidence synthesis is easy to generate but challenging to evaluate.** SAES addresses this by:

1. Forcing every coded field to be paired with the verbatim text it came from.
2. Splitting generation from evaluation at every stage. Extraction is followed by audit and consolidation is followed by disagreement surfacing. (in the v0.2 trials the audit ran in the same LLM session as the extraction; they will separated in the next release). 
3. Logging the inputs (search strings, screening decisions, source row IDs) so any consolidated claim can be traced back to the papers it draws on.

See examples: https://github.com/grahamprescott/structured-evidence-synthesis/tree/main/examples

---

## Further development needed 

- Benchmark against human coding
- Run the audit independently of extraction (different session or model)
- Specify a meta-analytic step. The current effect-size field is a vote count, rather than a pooled estimate. 
- Automation 

---
## Evaluation plan 
- Find labelled datasets to test against (Conservation Evidence, CEE, Cochrane)
- Human-human then human-LLM agreement
- Test structured against unstructured extraction
  

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

See [`docs/flowchart.svg`](docs/flowchart.svg) for the full pipeline diagram, including the documents produced at each stage. A cross-trial reflection on the three worked examples is in [`docs/v0.2_trials_summary.md`](docs/v0.2_trials_summary.md).

| Stage | What it does | Traceable to | Status in v0.2.0-alpha |
|---|---|---|---|
| [setup/](setup/) | Question framing → OpenAlex search → title/abstract screening | a logged search string + screening decisions | proof of concept, exercised once at small scale (cocoa example) |
| [extraction/](extraction/) | Per-paper LLM extraction of variable–relationship rows, plus a second-pass LLM audit | verbatim text from the source paper | exercised on three corpora (8-13 papers each) |
| [accumulation/](accumulation/) | Consolidation across rows: count, valence distribution, disagreement surfacing, optional union DAG | the row-set being aggregated, with provenance back to source row IDs | exercised on three corpora; produced 27/31/43 consolidated edges and union DAGs |

Each stage has its own `README.md` describing inputs, outputs, prompts, and discipline.

---

## What's new in v0.2 vs v0.1

New stages (SETUP and ACCUMULATION) added and description of worked examples on three corpora.

See [`CHANGELOG.md`](CHANGELOG.md) for full version history.


---

## Quick start

This protocol is currently operated by hand, with users copying prompts, papers, and schemas into LLM sessions. Future development will tackle automation when the prompts and protocol have stabilised. 

1. **SETUP**

Work through [`setup/prompts/01_question_framing.md`](setup/prompts/01_question_framing.md), then [`02_openalex_search.md`](setup/prompts/02_openalex_search.md), then [`03_screening.md`](setup/prompts/03_screening.md). For bulk PDF downloads from OpenAlex, see [`setup/scripts/openalex_pdf_download.py`](setup/scripts/openalex_pdf_download.py).

2. **EXTRACTION**
   
For each screened paper, run [`extraction/prompts/extraction.md`](extraction/prompts/extraction.md) followed by [`extraction/prompts/audit.md`](extraction/prompts/audit.md).

3. **ACCUMULATION**
   
Over the row-set, run [`accumulation/prompts/01_consolidation.md`](accumulation/prompts/01_consolidation.md), then [`02_disagreement_surfacing.md`](accumulation/prompts/02_disagreement_surfacing.md), optionally [`03_dag_construction.md`](accumulation/prompts/03_dag_construction.md).

Worked examples live in [`examples/`](examples/).

---

## Citation and contact

If you use or build on this protocol, please cite the repository and get in touch. See [`CITATION.cff`](CITATION.cff). Bug reports, suggestions for ontology revisions, and benchmark contributions especially welcome.

Graham Prescott · graham.prescott@gmail.com · [grahamprescott.substack.com](https://grahamprescott.substack.com/)

Tara Mei · taramei.mf@gmail.com
