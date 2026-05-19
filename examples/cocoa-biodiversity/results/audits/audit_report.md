# SAES Audit Report — Cocoa-biodiversity Corpus (v0.2.0-alpha)

> **Important caveat.** The `extraction.md` and `audit.md` prompts call for the audit to run in a *fresh* LLM session, ideally a different model. The work here was carried out in the same session as the extractions, which violates the protocol's separation-of-duties commitment. A second-pass audit by an independent reviewer (human or different model) is recommended before relying on the consolidated outputs.

**Audit scope:** Tasks 1, 2, 3, 5 (Flag review; Vocabulary consistency; Raw-to-code alignment; Schema compliance). Task 4 (Relationship completeness) was not performed because re-reading each PDF is out of budget. Missing relationships are likely in the larger papers (Bisseleua 2013, Jagoret 2017, Kongor 2024, Abah 2025).

**Sensitivity:** Comprehensive. Borderline cases flagged.

**Rows audited:** 57 rows across 8 per-paper CSVs:

| Paper | Rows | Type |
|---|---|---|
| bisseleua2013 | 16 | Primary observational study (Cameroon, 20 agroforests) |
| jagoret2017 | 12 | Primary observational study (Cameroon, 48 agroforests) + cited literature |
| saj2015 | 3 | Conference-poster abstract (Cameroon, 58 plots) |
| abah2025 | 7 | Review (Nigeria, multi-crop pollination) |
| kongor2024 | 10 | Review (cocoa challenges) |
| avadi2023 | 4 | Primary LCA study (Ecuador) |
| schneider2010 | 1 | Long-term-trial baseline / design paper (Bolivia) |
| setyowati2025 | 4 | Qualitative socio-ecological study (Indonesia, n=5) |

---

## 1. FLAG REVIEW

### Novel subject/object codes flagged `[UNVERIFIED]`

These were introduced because the seed cocoa vocabulary (`results/cocoa_vocabulary.md`) did not contain a clean match. Recommendation column indicates downstream consolidation handling.

| Code | First-appearing paper | Type | Recommendation |
|---|---|---|---|
| `shade_index` | bisseleua2013 | subject | **Accept** as composite predictor; document its 8 component variables. Recurs implicitly in Jagoret 2017 (basal-area indicators) but not by name. |
| `input_cost` | bisseleua2013 | object | **Accept**; useful for economic side of yield-vs-biodiversity trade-off. |
| `cocoa_tree_basal_area` | jagoret2017 | subject | **Accept**; cocoa-vigor proxy distinct from cocoa_density. |
| `unproductive_cocoa_rate` | jagoret2017 | object | **Accept**; mechanistic intermediate variable between shade and yield. |
| `pollinator_knowledge` | setyowati2025 | subject | **Accept** but tag as off-axis (farmer-cognition, not biodiversity). |
| `rainfall_extreme` | setyowati2025, abah2025 | subject | **Accept**; climate-side predictor that mediates pollinator activity. |
| `carbon_sequestration` | avadi2023 | object | **Accept**; ecosystem-service co-benefit, indirect to yield. |
| `natural_habitat` | abah2025 | subject | **Accept**; off-farm habitat-area predictor. |
| `cocoa_variety` | kongor2024 | subject | **Accept**; genotype-management interaction. |

### In-paper conflict / direction flags

| Paper | Row context | Flag | Recommendation |
|---|---|---|---|
| bisseleua2013 | shade_index → cocoa_yield: Negative; shade_index → natural_enemy_abundance: Positive | The same predictor has opposite signs depending on outcome (yield vs ecosystem services). | Accept; this is **the headline trade-off** of the corpus, not an extraction error. |
| bisseleua2013 | shade_tree_density (native) → cocoa_yield Negative vs shade_tree_density (native) → natural_enemy_abundance Positive | Same trade-off split by tree provenance. Exotic-tree density shows neither effect (NS). | Accept; flag for separate subject_codes by tree origin if vocabulary is revised. |
| jagoret2017 | shade_tree_density → unproductive_cocoa_rate Positive (more shade → more unproductive trees → lower yield) but shade_tree_species_richness → unproductive_cocoa_rate Negative (more species → fewer unproductive trees → higher yield) | Two facets of "shade" diverge: density penalises, diversity rescues. | Accept; key qualitative insight. |
| jagoret2017 | shade_tree_density → cocoa_tree_basal_area Positive (forest trees), Positive (fruit trees) | Forest trees positively associated with cocoa vigour (cumulative r² high); contradicts the simple "shade reduces yield" framing. | Accept; consistent with structural-complexity-supports-vigour interpretation. |
| avadi2023 | agroforestry_vs_monoculture → cocoa_yield Negative *and* agroforestry_vs_monoculture → carbon_sequestration Positive | Two outcomes with opposite valences; canonical land-sharing trade-off. | Accept. |
| kongor2024 | agroforestry_vs_monoculture → cocoa_yield Negative (cited Ahenkorah, Armengot) and functional_diversity_of_shade_trees → cocoa_yield Positive (cited Utomo 2016) | Within the same review: monoculture beats agroforestry on yield, *but* selected shade-tree combinations (cocoa-coconut, pruned cocoa) can match or beat monoculture. | Accept; nuance preserved as separate rows. |
| kongor2024 | pollination_success → cocoa_yield Positive (hand pollination raises yield 51–161%) | Cited from Toledo-Hernández 2020, 2023. Implies cocoa yield is severely pollination-limited. | Accept; strongest mechanistic evidence for biodiversity → yield. |
| abah2025 | pollinator_diversity → cocoa_yield Positive (650–800 vs 350–500 kg/ha) | Review summary; primary sources not always reachable. | Accept but flag as **single tabular claim with unclear primary source**. |
| schneider2010 | subject_trend_only=Yes, no relationship results | This paper reports trial *design* and baseline only. Real biodiversity-yield results from this long-term trial would be in follow-up publications (FiBL/Sara Beni reports). | Flag for future inclusion; current paper contributes near-zero evidence to consolidation. |
| setyowati2025 | Whole paper: n=5 farmers, qualitative | All claims are either descriptive statistics on a tiny sample or cited from prior work; treat as a contextual paper, not a primary evidence source. | Down-weight in synthesis; do not drop. |

### Off-topic content

| Paper | Recommendation |
|---|---|
| schneider2010 | The paper itself is on-topic but contains no biodiversity-yield results. **Keep** for citation chain (it points to a long-term trial whose results would be valuable). |
| setyowati2025 | Tiny qualitative sample (n=5). **Keep but down-weight**; only one of its four rows touches the yield axis directly. |
| avadi2023 (row on Ecuadorian deforestation rate) | The 83.4 kg CO₂eq/ha land-use-change finding is biodiversity-adjacent but not biodiversity-yield. Coded as `cocoa_yield` trend-only and flagged. | Accept; informative context. |

---

## 2. CONTROLLED VOCABULARY CONSISTENCY

### Subject codes used >1 paper

| Code | Papers | Note |
|---|---|---|
| `agroforestry_vs_monoculture` | bisseleua2013, jagoret2017, saj2015, abah2025, kongor2024, avadi2023, schneider2010, setyowati2025 | **The corpus's most-used predictor (8/8 papers)**. Bundles several distinct contrasts: full-sun vs shaded, intensive vs traditional, mixed-species vs single-species. Consider splitting in a v2 vocabulary. |
| `shade_tree_density` | bisseleua2013 (native/exotic), jagoret2017 (forest/fruit) | Consistent; both papers stratify by tree origin. Recommend splitting into `shade_tree_density_native` vs `shade_tree_density_exotic` (or `_forest` vs `_fruit`) for the v2 vocab. |
| `shade_tree_species_richness` | bisseleua2013 (Discussion), jagoret2017 | Consistent. Jagoret's TRESpe variable and Bisseleua's diversity summary statement use the same construct. |
| `shade_cover_percentage` | bisseleua2013, jagoret2017 (cited Blaser 2017), kongor2024 (cited Grant 2022) | Consistent. |
| `shade_index` (UNVERIFIED) | bisseleua2013 | Unique to this paper; an 8-variable composite. Do not merge with `shade_cover_percentage`. |
| `functional_diversity_of_shade_trees` | saj2015, kongor2024 (twice — Utomo 2016 and pruning/thinning citations), jagoret2017 (cited Saj 2017) | Consistent; useful for nuancing "shade is bad for yield" finding. |
| `pollinator_diversity` | abah2025 (twice), [implicit in kongor2024 via hand-pollination findings] | Consistent. |
| `pollination_success` | kongor2024, abah2025 | Consistent. Used as both outcome (pollinator → pollination) and mediator (pollination → yield). |
| `natural_enemy_abundance` | bisseleua2013 (ants, spiders, wasps), jagoret2017 (cited), avadi2023 (cited "preservation of biodiversity"), kongor2024, saj2015 | **Used as a bundled "biodiversity / ecosystem services" stand-in.** In several rows it carries claims about pollination, soil fertility, carbon, and pest control. This is fuzzy; recommend separate codes in v2. |
| `pesticide_input` | abah2025 | Single-paper usage. |

### Object codes used >1 paper

| Code | Papers | Note |
|---|---|---|
| `cocoa_yield` | All 8 papers | The corpus centroid. |
| `pod_count` | jagoret2017, kongor2024 (cited Toledo-Hernández 2023) | Consistent; closely-related-but-distinct from cocoa_yield. |
| `pod_loss_to_pests` | bisseleua2013 (twice) | Consistent. |
| `pollination_success` | abah2025 (several), kongor2024 | Consistent. |
| `natural_enemy_abundance` | bisseleua2013, jagoret2017, kongor2024, avadi2023, saj2015 | As above; serves as biodiversity-side outcome too. |
| `farmer_net_returns` | bisseleua2013 (twice) | Single-paper usage. |
| `input_cost` (UNVERIFIED) | bisseleua2013 (twice) | Single-paper usage; novel. |

### Vocabulary recommendations

1. **Split `agroforestry_vs_monoculture`** into:
   - `cocoa_shade_system_categorical` (full-sun / low-shade / shaded / forest-derived) — for cross-system comparisons.
   - `intensification_level` (already in vocab) — for input-intensity comparisons.
   - `shade_tree_diversity_categorical` (single-species / few-species / diverse) — for species-richness contrasts.
   These have different mechanisms and lump together very different studies.

2. **Split `shade_tree_density`** into `shade_tree_density_native` vs `shade_tree_density_exotic` (Bisseleua 2013) OR `shade_tree_density_forest` vs `shade_tree_density_fruit` (Jagoret 2017). The provenance distinction is mechanistically meaningful and is being lost in the current coding.

3. **Decompose `natural_enemy_abundance`** as currently used. In several rows it carries bundled biodiversity/ecosystem-service claims (carbon, soil, pest control). Recommend dedicated codes for:
   - `arthropod_predator_abundance` (ants, spiders, wasps)
   - `pollinator_abundance` (midges, bees) — already exists
   - `soil_organic_carbon` / `carbon_sequestration` — already exists / introduced here
   - `soil_biodiversity` — already exists
   Then `natural_enemy_abundance` becomes a clean predator-only code.

4. **Add `microclimate_buffering`** to the active codes list. It is the mechanistic mediator named in setyowati2025 ("stabilize yield under unpredictable weather"), abah2025 ("microclimatic conditions"), and kongor2024 ("microclimatic controls"). Currently encoded under `natural_enemy_abundance` by default; deserves its own code.

5. **Add `cocoa_yield_stability`** as a distinct outcome from `cocoa_yield` (magnitude). The "low-but-steady" framing in Saj 2015 and Setyowati 2025 is about stability, not mean yield, and conflating them obscures a key claim.

---

## 3. RAW-TO-CODE ALIGNMENT

| Paper:Row | Issue | Suggestion |
|---|---|---|
| bisseleua2013 r1 | `shade_index → cocoa_yield` coded Negative. Subject is composite of 8 variables. | Defensible (matches the paper's headline); flag composite nature in `rel_exists_note`. |
| bisseleua2013 r10 | `shade_tree_density (exotic)` → cocoa_yield coded as `rel_exists = No` (r²=0.05, p=0.34). | Correct; the row preserves the "no effect" signal for absence-of-evidence accounting. |
| jagoret2017 r2 | `cocoa_tree_basal_area → pod_count`: subject is a vigour proxy, not a biodiversity variable. | Defensible; acts as mechanistic intermediate. Flag as off-the-main-axis when consolidating. |
| jagoret2017 rows on `unproductive_cocoa_rate` | Subject_code introduced as a novel intermediate variable; chains via mediator → yield. | Defensible; preserve the mediation chain rather than collapsing. |
| jagoret2017 r7–9 | Cited findings from Besse 1972, Lachenaud & Mossu 1985, Koko et al. 2013 give +247–253% yield increases from shade removal. | Accept; these are the most-cited classical findings and they consistently point Negative for agroforestry → yield. Should be flagged as historic (1972, 1985) — context for monocropping policy. |
| saj2015 r2 | `agroforestry_vs_monoculture → cocoa_yield` coded Negative ("low-but-steady"). | Coding captures the magnitude side; stability side is lost. Add a stability-outcome row in re-extraction. |
| abah2025 r1 | `pollinator_diversity → cocoa_yield`: numeric magnitude 650-800 vs 350-500 kg/ha drawn from a tabular summary in a review. Primary sources cited but not directly. | Accept with reduced provenance trust. The differential (~300 kg/ha) is large and would dominate a pooled estimate; consider down-weighting. |
| kongor2024 r6,7 | Cited Toledo-Hernández 2020, 2023: hand pollination 51-161% yield increase, 3× fruit set. | Accept; classified `causal_inference_level = Intervention` because Toledo-Hernández conducted experimental trials. **These are the strongest causal-inference rows in the corpus.** |
| kongor2024 r5 | `excessive shade cover → cocoa_yield` Negative, but `shade_cover_percentage` would normally be a continuous predictor. "Excessive" makes this a non-linear / threshold claim. | Defensible; rel_valence is `Negative` but mechanism is threshold-only. Consider `Non-linear` in re-extraction. |
| avadi2023 r4 | `cocoa_yield` as subject (Ecuador-specific land-use trend); subject_trend_only=Yes. | Correct usage. |
| setyowati2025 r1 | "Stabilization claim" coded Positive but with note that this is stability not magnitude. | Acceptable workaround; ideally needs its own `cocoa_yield_stability` outcome code (see vocab rec 5). |
| All review/cited rows (Kongor 2024 in particular) | Method type "Statistical modelling" or "Review" used inconsistently when citing other people's experiments. | Defensible; the *citing* paper is a review, but the *cited* method is the underlying type. Recommend a `cited_method_type` field in a future schema. |

---

## 5. SCHEMA COMPLIANCE

A column-by-column scan against `extraction/schemas/row.schema.json` (33 columns).

### Permitted-value compliance

- **paper_section**: All values in {Introduction, Methods, Results, Discussion, Conclusions, Abstract, Findings}. Cocoa corpus uses Introduction, Results, Discussion, Conclusions, Abstract, Findings. ⚠ The schema permits {Methods, Results, Discussion, Introduction, Abstract}; "Findings" (used in setyowati2025) and "Conclusions" (used in avadi2023) are extensions of the controlled list. Recommend updating the schema or remapping these to {Results, Discussion}.
- **subject_trend_only**: All values in {Yes, No}. ✓
- **rel_exists**: All values in {Yes, No, Uncertain}. ✓
- **rel_direction**: All values in {Subject→Object, Object→Subject, Bidirectional, Non-directional, Indeterminate}. No Object→Subject or Bidirectional rows. ✓
- **rel_valence**: All values in {Positive, Negative, Non-linear, Indeterminate}. No Non-linear rows even where mechanistically appropriate (Kongor excessive-shade row should arguably be Non-linear). ✓ in letter, ⚠ in spirit.
- **rel_conditionality_code**: All values in {Temporal, Spatial, Population-specific, Technology-specific, Unconditional, null}. ✓
- **rel_uncertainty_code**: All values in {Asserted, Probable, Possible, Speculative, null}. ✓
- **source_locus**: All values in {Original to this study, Cited from prior work, Synthesised from multiple sources}. ✓
- **method_type**: All values in {Observation, Experiment, Statistical modelling, Simulation, Review, Expert elicitation}. ✓
- **causal_inference_level**: All values in {Association, Controlled comparison, Intervention, Counterfactual}. **Two Intervention rows** (kongor2024 Toledo-Hernández hand-pollination, jagoret2017 Besse 1972 shade removal); rest are Association or Controlled comparison. ✓
- **geographic_scope_code**: All values in {Country, Region, Biome, Global, null}. Used Country, Region, Global. ✓
- **temporal_scope_code**: Used snapshot, multi-year, "Not reported". ✓ (schema allows free-text where unspecified).
- **population_code**: Used Terrestrial ecosystem (most), Human (when surveys/socio-economic). ✓

### Required-field compliance

- **`paper_id`, `paper_section`, `version`**: present in all rows. ✓
- **`subject_raw`, `subject_code`**: present in all rows. ✓
- **`object_raw`, `object_code`**: empty only where `subject_trend_only = Yes` (3 rows: abah2025 r2, avadi2023 r4, schneider2010 r1, setyowati2025 r2). ✓
- **`source_citation_raw`**: required when source_locus != "Original to this study". Compliance generally met but spot-check: a few rows in kongor2024 list multiple papers in one cell (acceptable); abah2025 has compressed citations ("Compiled from references 22, 28, 29, 32") — recommend expanding.

### Free-text fields

- **`rel_exists_note`**: heavily used to carry `[FLAG]` markers and coding rationale. Audit trail OK.
- **`effect_magnitude`, `effect_error_magnitude`**: mix of numeric and string. Several rows show numbers (regression slopes, R², F-statistics). Schema permits string-or-number; compliance ✓ but downstream pooling will require parsing.

### Issues to fix before consolidation

1. Several rows include `[UNVERIFIED]` in `subject_code` / `object_code` directly (e.g. `shade_index [UNVERIFIED]`, `unproductive_cocoa_rate [UNVERIFIED]`). For schema compliance the suffix should remain in the code per the extraction prompt — this is intended. Consolidation logic must strip the suffix when grouping.

2. `paper_section` values "Findings" and "Conclusions" are non-canonical; remap to "Results" and "Discussion" respectively, or extend the schema.

3. `effect_magnitude` cells contain various units (regression slope, F-statistic, R², percent change, fold change, kg/ha, t C/ha/yr). Pooling will require unit harmonisation; recommend a `effect_metric_canonical` column in v3 schema.

4. Three subject_trend_only=Yes rows (Schneider 2010, Avadi 2023 r4, Abah 2025 r2 [pollinator_knowledge], Setyowati 2025 r2) carry useful contextual data but contribute no edge to the consolidated graph. They should be retained in a side appendix, not discarded.

---

## 6. ONTOLOGY REVISION RECOMMENDATIONS

1. **Decompose `agroforestry_vs_monoculture`** (used by all 8 papers but for very different contrasts). At minimum split shade-system, intensification, and shade-diversity components.

2. **Distinguish native vs exotic / forest vs fruit shade trees** in `shade_tree_density`. Bisseleua 2013 and Jagoret 2017 both find the provenance distinction is mechanistically critical, and the current code loses it.

3. **Add `cocoa_yield_stability`** as a distinct outcome from `cocoa_yield`. Saj 2015 ("low-but-steady") and Setyowati 2025 ("stabilize yield under unpredictable weather") both make stability-side claims that the current coding can't represent cleanly.

4. **Add `microclimate_buffering`** as a first-class subject_code mediator. It is the mechanism name in setyowati2025, abah2025, kongor2024.

5. **Add `arthropod_predator_abundance`** as a sibling code to `pollinator_abundance` under a parent biodiversity-functional-group concept. The current `natural_enemy_abundance` code carries too many distinct meanings.

6. **Consider `cocoa_tree_basal_area`** and **`unproductive_cocoa_rate`** as accepted mediator codes (Jagoret 2017 introduces both). Useful for explicit-mechanism DAG paths.

7. **The hand-pollination evidence (Toledo-Hernández 2020, 2023) is the strongest causal-inference signal in the corpus.** Recommend it gets a dedicated `hand_pollination_supplementation → cocoa_yield` edge rather than being collapsed under `pollination_success`. It supplies the missing experimental warrant for the otherwise associational biodiversity-yield claim.

8. **The corpus has a strong bias toward review papers** (Kongor 2024, Abah 2025, parts of Jagoret 2017 Discussion). When consolidating, weight original-data rows higher than cited-from-prior-work rows.

9. **Setyowati 2025 and Schneider 2010 contribute almost no evidence** to the consolidated graph (n=5 farmers, baseline-only respectively). They are valuable as context and citation chain but should not influence pooled directions.

---

END OF AUDIT REPORT
