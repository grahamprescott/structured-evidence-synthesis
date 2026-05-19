# Changelog

All notable changes to the SAES protocol are recorded in this file.

The protocol uses semantic-ish versioning: major versions for backwards-incompatible changes to the pipeline shape, minor versions for new stages or substantive ontology revisions, patch versions for vocabulary tweaks and bug fixes. `-alpha` indicates proof-of-concept that has not been tested at scale.

## [0.2.0-alpha] — 2026-05-19

Expands the v0.1 prototype (extraction + audit on one paper) into a three-stage end-to-end pipeline.

### Added

- **SETUP stage** (`setup/`) — question framing, OpenAlex search guidance, title/abstract screening. Includes a Python helper (`setup/scripts/openalex_pdf_download.py`) for bulk PDF retrieval from an OpenAlex query.
  - Exercised once end-to-end (cocoa example); not stress-tested at scale.
- **ACCUMULATION stage** (`accumulation/`) — consolidation across rows sharing the same `(subject_code, object_code)` edge, disagreement surfacing, optional union-DAG construction.
  - Exercised end-to-end on three corpora (cocoa 31 edges, VBAC 27 edges, gold-mining 43 edges); not stress-tested above ~13 papers.
  - Explicit "no naive averaging across methods/populations" rule.
- **Top-level pipeline framing** — new root `README.md` introducing the three stages; pipeline diagram at `docs/flowchart.svg`; covering essay at `docs/covering-essay.md`.
- **Worked examples completed** — three example folders (`examples/cocoa-biodiversity/`, `examples/vbac/`, `examples/gold-mining/`), each with a full pipeline run including REPORT.md, audit, consolidated edges, disagreement report, and union DAG.
  - Cocoa demonstrates the full setup→accumulation pipeline starting from a research question.
  - VBAC demonstrates the extraction→accumulation half on a pre-supplied corpus and stress-tests cross-domain ontology generalisation.
  - Gold-mining demonstrates a third input mode: migration of a 2022 manual coding workbook into the v0.2 schema.
- **Cross-trial reflection** — [`docs/v0.2_trials_summary.md`](docs/v0.2_trials_summary.md) covers what worked, what was hardest, and recommendations for v0.2.1.

### Changed

- **Existing SAES extraction core moved into `extraction/`.** The v0.1.2 ontology, schema, and prompts pass through with field renaming applied for internal consistency:
  - `v1_raw` / `v1_code` → `subject_raw` / `subject_code`
  - `v2_raw` / `v2_code` → `object_raw` / `object_code`
  - `rel_direction` values now reference Subject / Object rather than V1 / V2.
  - `subject_trend_only` added to capture cases where a subject's trajectory is reported without a paired object.
  - PECO-style entity typing and thematic domain fields removed (carried through from v0.1.2 ontology revision).
- **README rewritten** to lead with the pipeline rather than the extraction stage.

### Known issues / "honest notes"

- All three example trials were carried out by a single LLM session per trial. The audit step in each ran in the same session as the extraction, against the protocol's own separation-of-duties guidance. An independent second-pass audit is recommended for any consolidated output before treating it as authoritative.
- Cross-trial summary (`docs/v0.2_trials_summary.md`) records several patterns observed across the three runs: no Counterfactual evidence anywhere; uneven effect-size capture across domains; recurrent vocabulary fragmentation that the audit catches but the consolidation does not; the "stop short at proximate endpoint" trap (most acute in gold-mining, where the `wildlife` outcome code is in the vocabulary but used zero times).
- The extraction prompts in this draft were updated to use `subject`/`object` naming, but the v0.1.2 source files still contain stale `v1`/`v2` references in places. A systematic, human-led audit pass through the prompt and ontology files is planned (see SAES change log entry 15-05-2026).
- Ontology controlled vocabularies (`extraction/ontology/`) are minimal stubs in this draft; they require domain-specific population before extraction at scale. Each example folder ships its own seeded vocabulary as actually run.
- No automated tests of any pipeline stage. All discipline is enforced by prompts and manual audit.
- Article PDFs are not included in this repository (mostly paywalled). Each example's `articles/README.md` lists the DOIs needed to reconstruct the corpus.

## [0.1.2] — 2026-05-15

End-to-end run of extraction + audit on the Asner & Tupayachi (2017) gold-mining paper, compared against a human-coded benchmark.

### Changed

- Ontology fields renamed: `v1`/`v2` → `subject`/`object` throughout the schema specification.
- PECO-style entity type and thematic domain dropped from variable fields.
- `subject_trend_only` flag added.
- `temporal_scope_code` added; population fields renumbered.
- Extraction prompt updated to forbid duplicate-row recording for the same relationship in the same context.

### Known issues at v0.1.2

- Inconsistencies between `subject`/`object` (in ontology specification) and `v1`/`v2` (in prompt files) — flagged for systematic manual review.

## [0.1.1] — earlier

Initial proof of concept: extraction prompt + audit prompt + ontology specification, run once against one paper. No setup or accumulation stages.
