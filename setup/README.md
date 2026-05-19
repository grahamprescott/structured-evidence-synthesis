# Setup — corpus assembly

The first stage of the SAES pipeline. Turns a research question into a screened set of papers, with a logged search string and a screening-decisions record that downstream stages can trace inputs back to.

> **Status: proof of concept.** Not yet tested at scale. Prompts and schemas are drafts.

## What this stage does

```
Research question
       ↓
   01_question_framing   — declare scope and inclusion/exclusion criteria
       ↓
   02_openalex_search    — construct and run a reproducible boolean search
       ↓
   03_screening          — title/abstract screen against the pre-declared criteria
       ↓
Screened corpus + search log
```

## Inputs and outputs

| Input | Output |
|---|---|
| A research question, articulated in natural language | A populated `search-log.json` (one file per search) |
| | A populated `screening-decisions.csv` (one row per candidate paper) |
| | A folder of full-text PDFs for the included set (via `scripts/openalex_pdf_download.py`) |

## The discipline

The hard part of evidence synthesis is not running the search; it is **specifying the search well enough that the corpus is reproducible**, and **declaring inclusion/exclusion criteria before you see the results** so that screening decisions are auditable.

The same epistemic move that the extraction-and-audit pair makes at the row level, the question-framing-and-screening pair makes at the corpus level: separate generation (deciding what to look at) from evaluation (deciding what survives). If you frame the question after seeing the results, you can rationalise any corpus into existence.

Concretely, this stage commits to:

1. **Inclusion and exclusion criteria are written down before the search is run** — see `prompts/01_question_framing.md`. The output is checked into version control.
2. **The search string is captured verbatim**, with date, database, and result count, in `schemas/search-log.schema.json`. Re-running the same search a year later should return a knowably different corpus, not a mysteriously different one.
3. **Every screening decision has a reason** — see `schemas/screening-decisions.schema.csv`. "Excluded" is not a decision; "excluded because does not measure a biodiversity outcome" is. Reasons are auditable; outcomes alone are not.

## Files in this stage

### Prompts (scripts to run in an LLM session)

- [`prompts/01_question_framing.md`](prompts/01_question_framing.md) — forces the user to articulate the question, inclusion/exclusion criteria, and scope before seeing any results.
- [`prompts/02_openalex_search.md`](prompts/02_openalex_search.md) — guidance for constructing a reproducible boolean search against OpenAlex.
- [`prompts/03_screening.md`](prompts/03_screening.md) — title/abstract screening against the pre-declared criteria, with logged reasons for each exclusion.

### Schemas

- [`schemas/search-log.schema.json`](schemas/search-log.schema.json) — JSON schema for the search log.
- [`schemas/screening-decisions.schema.csv`](schemas/screening-decisions.schema.csv) — CSV header template for the screening-decisions table.

### Scripts

- [`scripts/openalex_pdf_download.py`](scripts/openalex_pdf_download.py) — pages through an OpenAlex search, downloads open-access PDFs, and writes a per-work log. Run after screening to fetch the included set.

## What downstream stages expect

- A `search-log.json` conforming to the schema.
- A `screening-decisions.csv` conforming to the schema.
- A folder of PDFs, one per `paper_id` marked `include` in the screening file.

The extraction stage operates one paper at a time and does not depend on the search log or the screening log being present. But the accumulation stage's provenance claims are weaker without them — they let a downstream reader check not only "what does this consolidated edge draw on" but also "what universe of papers was screened to produce that row-set."
