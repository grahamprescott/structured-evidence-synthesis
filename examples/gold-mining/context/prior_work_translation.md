# Prior-work translation note

## Source

`prior work gold mining/Coding for mining review revision 2022(1).xlsx`, sheet `active_sheet`. 994 rows total; 143 rows where `commodity = "Gold"` were used as the input to this SAES v0.2 run.

The 2022 workbook captured causal links as **source → arrow → destination** with a quoted-text justification, in a style closely analogous to the SAES v0.2 row schema. This document describes the column mapping that converted those rows into the v0.2 row schema (33 columns).

## Column mapping

| 2022 column | v0.2 column | Notes |
|---|---|---|
| `article_code` | `paper_id` | Normalised to lowercase, underscore→nothing (e.g. `Asner_2016` → `asner2016`). |
| `section` | `paper_section` | Free text mapped to {Abstract, Introduction, Results, Discussion, Conclusion, Methods}. Non-canonical sections (e.g. "Future prospects: dynamics of soybean expansion") were collapsed to the nearest canonical section. Empty values default to `Introduction`. |
| — | `version` | Set to `v0.2.0-alpha`. |
| `uncoded_source` | `subject_raw` | Wrapped in double-quotes per schema. |
| `source` | `subject_code` | The canonical-form source. |
| `uncoded_destination` | `object_raw` | Wrapped in double-quotes. |
| `destination` | `object_code` | The canonical-form destination. |
| `quoted_text` | `rel_raw` | Wrapped in double-quotes. |
| `arrow` (positive/negative/bidirectional/NA) | `rel_valence` | Mapped: positive → Positive, negative → Negative, bidirectional → Indeterminate (direction set to Bidirectional), NA → Indeterminate. |
| `arrow` | `rel_direction` | Subject→Object unless `arrow=bidirectional`, in which case Bidirectional. |
| `arrow` | `rel_exists` | Yes when arrow is one of {positive, negative, bidirectional}; Uncertain when NA. |
| `context` | `rel_conditionality_raw` | Used to fill conditionality (e.g. "Informal / ASGM"). |
| — | `rel_conditionality_code` | Default Population-specific (e.g. ASGM-specific); Unconditional only where the source quote names no context. |
| `comments` | `rel_exists_note` | Where present, copied in. Otherwise marked with translation note "[2022-migration] no comment captured". |
| — | `rel_uncertainty_code` | Default Probable. Asserted where comments include phrases like "clear", "showed", "demonstrated". |
| — | `effect_raw`, `effect_metric`, `effect_magnitude`, `effect_error_metric`, `effect_error_magnitude` | All set to "Not reported". The 2022 coding did not systematically capture numeric effect sizes; downstream effect-size pooling is therefore impossible for this corpus. |
| — | `source_locus` | Set per row from the 2022 comments where they cite prior work; default `Original to this study`. |
| — | `method_raw` / `method_type` / `causal_inference_level` | Set at the paper level (see table below). |
| `location_1`, `location_2` | `geographic_scope_raw`, `geographic_scope_code` | Pair concatenated; scope set to Country (most rows) or Region (where Location_1 is a continent or "Tropics"). |
| — | `temporal_scope_raw`, `temporal_scope_code` | Set at the paper level from publication metadata. |
| `context` + `location` | `population_raw`, `population_code` | Population_code chosen from {Terrestrial ecosystem, Aquatic ecosystem, Human} based on whether the row's mechanism is forest-side, water-side, or health-side. |

## Paper-level metadata applied during translation

| paper_id | method_type | causal_inference_level | geographic_scope_code | temporal_scope_code | population_code (modal) |
|---|---|---|---|---|---|
| asner2016 | Statistical modelling | Association | Country | multi-year | Terrestrial ecosystem |
| castilhos2006 | Observation | Association | Country | snapshot | Aquatic ecosystem |
| fearnside2001 | Review | Association | Country | multi-year | Terrestrial ecosystem |
| lacher1997 | Review | Association | Region | snapshot | Aquatic ecosystem |
| regine2006 | Observation | Association | Country | snapshot | Aquatic ecosystem |
| schwartzmann2005 | Review | Association | Country | multi-year | Human |
| soderquist2000 | Observation | Association | Country | multi-year | Terrestrial ecosystem |
| tarras-wahlberg2001 | Observation | Association | Country | snapshot | Aquatic ecosystem |

Two papers in the 2022 workbook (`Festin_2019` n=1; `Prescott_2022` n=22) are **excluded from this v0.2 run**:

- `Festin_2019` has only one coded row in the workbook and the PDF is not present in `articles/`. Skipping.
- `Prescott_2022` is the author's own paper from the prior review and would create a circular dependency. Skipping.

A note on `Lacher_2009`: the 2022 workbook codes 10 rows under `Lacher_2009` but the PDF in the prior-work folder is `Lacher1997.pdf` ("Tropical ecotoxicology: status and needs", Environmental Toxicology and Chemistry, 1997). These are the same paper — the workbook label appears to be a typo. The 10 rows were re-labelled `lacher1997`.

## Known fidelity limitations of this migration

1. **No quantitative effect sizes.** The 2022 coding did not capture numeric effect sizes (regression coefficients, percent changes, dose-response numbers). All `effect_*` cells are `Not reported`. Re-extracting the PDFs from scratch would recover these — the audit recommends this.
2. **Method type is paper-level, not row-level.** Some rows within a paper cite prior work (Review-style rows); the migration could not always distinguish these from original-data rows without re-reading the PDFs. Default is the paper's modal method.
3. **The 2022 vocabulary was less granular than v0.2 in some places** (e.g. `wildlife` as a single destination; `protected areas` used as both subject and destination). The audit retains these as-is and flags candidates for splitting.
4. **`bidirectional` arrows (n=10 in gold subset) are flattened** to `rel_direction=Bidirectional`, `rel_valence=Indeterminate`. This loses information about which sign holds in which direction.
5. **rel_uncertainty_code was inferred, not extracted.** The 2022 workbook did not capture asserted-vs-probable explicitly; the v0.2 column was populated from text cues in the comments and quoted_text. Conservative default is Probable.

## What this run is and is not

- **It is** a translation of the 2022 coding into the v0.2 schema, with consolidation, disagreement surfacing, and DAG construction applied on top.
- **It is not** a fresh extraction from the PDFs. A v0.2-native re-extraction would yield more granular effect sizes, a cleaner method-type-per-row attribution, and possibly some additional rows the 2022 pass missed. That re-extraction is recommended as the next iteration.
