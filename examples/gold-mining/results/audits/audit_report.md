# SAES Audit Report — Gold-mining Corpus (v0.2.0-alpha)

> **Important caveat.** Two protocol-fidelity issues apply.
>
> 1. The `audit.md` prompt calls for a fresh LLM session, ideally a different model. The work here was carried out in the same session as the migration. A second-pass audit by an independent reviewer is recommended.
> 2. **The extraction stage here was not a v0.2 PDF extraction** — it was a programmatic migration of a 2022 manual coding workbook (`prior work gold mining/Coding for mining review revision 2022(1).xlsx`) into the v0.2 row schema. The audit accordingly focuses on *the prior coding* and *the migration* rather than on a fresh-from-PDF extraction. A native v0.2 re-extraction from the PDFs is recommended as the next iteration.

**Audit scope:** Tasks 1, 2, 3, 5 (Flag review; Vocabulary consistency; Raw-to-code alignment; Schema compliance). Task 4 (Relationship completeness) was not performed; missing relationships in the original 2022 coding are likely, particularly numeric effect sizes which were not captured at all.

**Sensitivity:** Comprehensive. Borderline cases flagged.

**Rows audited:** 105 rows across 8 per-paper CSVs:

| Paper | Rows | Type |
|---|---|---|
| asner2016 | 24 | Primary remote-sensing + cited literature (Peru) |
| castilhos2006 | 25 | Primary observational, mercury in fish (Indonesia) |
| fearnside2001 | 8 | Review of Amazonian land-use (Brazil) |
| lacher1997 | 10 | Pantropical ecotoxicology review |
| regine2006 | 4 | Primary observational, mercury bioaccumulation (French Guiana) |
| schwartzmann2005 | 11 | Review of indigenous-land conservation (Amazon) |
| soderquist2000 | 3 | Primary observational, mammals (Australia) |
| tarras-wahlberg2001 | 20 | Primary observational, river contamination (Ecuador) |

---

## 1. FLAG REVIEW

### Migration-derived defaults to confirm at re-extraction

These are defaults the migration applied that an independent auditor should verify against the source PDFs:

| Default field | Value applied | Recommendation |
|---|---|---|
| `effect_raw`, `effect_metric`, `effect_magnitude` | "Not reported" on **all 105 rows** | **Re-extract from PDFs.** The original 2022 coding made no attempt to capture numeric effect sizes (e.g. Asner's 4,437 ha yr⁻¹ deforestation rate; Tarras-Wahlberg's metal concentrations; Castilhos's hair-mercury μg g⁻¹; Régine's species-level Hg fold-differences). These are all available in the PDFs. |
| `method_type` | Paper-level, applied uniformly to all rows in a paper | Verify per-row; some rows within a primary paper are cited-from-prior-work and should be `Review`. |
| `causal_inference_level` | `Association` for all 105 rows | Review: Asner's protected-area-effect rows use an inside-vs-outside boundary contrast that could plausibly be `Controlled comparison`. Tarras-Wahlberg's upstream-downstream sampling design is also borderline. |
| `rel_uncertainty_code` | `Probable` default; `Possible` where comments suggested ambiguity (4 rows) | The 2022 workbook did not capture asserted-vs-probable explicitly. Defaults are conservative. |
| `population_code` | Heuristically chosen per-row from mention of water/mercury/health vs forest | Verify; the heuristic is text-based and may misclassify e.g. mercury-in-forest-soil rows. |

### Single-row anomalies

| Row | Issue | Recommendation |
|---|---|---|
| `fearnside2001:r6` — `gold_mining → indigenous_land_rights` Positive | A Positive arrow here is counter-intuitive given the rest of the corpus (Schwartzmann 2005: `gold_mining → indigenous_land_rights` is encoded only via `miner_influx → indigenous_land_rights` Negative). The 2022 comment notes the source sentence was "ambiguously worded"; could mean "gold mining increased the political *salience* of indigenous land rights," not "improved" them. | **Re-extract from PDF.** Likely a sign-error in the 2022 coding. |
| `asner2016:r9` — `road_creation → miner_influx` and several other `road_*` rows | The 2022 vocabulary uses both `road_creation` and `road_construction` for the same construct. | Merge in v2 vocabulary. |
| `lacher1997:r10` — `weak_governance → enforcement_and_other_barriers_to_entry` | The 2022 vocabulary uses `weak_governance` (one row) and `weak_governance_and_bad_policies` (more rows). | Merge in v2 vocabulary. |
| `asner2016:r17` — `gold_mining → mercury_use` (Positive) but accompanying comment "Maybe should be coded as 'enforcement efficacy' not 'enforcement'?" | The 2022 author already flagged this. Suggests `enforcement_and_other_barriers_to_entry` collapses two distinct constructs (capacity vs efficacy). | Split in v2 vocabulary. |
| `castilhos2006:r12` — `mercury_bio_accumulation → human_health` Negative | The 2022 comment notes "mixed evidence that levels sufficient for serious health risks have been reached" in this specific population. The valence is Negative (more accumulation → worse health) but the strength is qualified. | Accept; downgrade `rel_uncertainty_code` to Possible at re-extraction. |
| All Asner2016 protected-area rows | Comment notes the enforcement effect is "fleeting." Indicates a temporal-conditional finding. | Re-extract with `rel_conditionality_code = Temporal` for those rows. |

### Off-topic / borderline content

| Paper | Issue | Recommendation |
|---|---|---|
| fearnside2001 | Paper is primarily about **soybean** expansion in the Brazilian Amazon, not gold mining. Gold mining appears as a tangential land-use driver. 8 of 10 prior rows survived; some others were collapsed in migration because both source and destination were `NA`. | Retain but down-weight; better used for indirect-pathway rows than direct-impact rows. |
| schwartzmann2005 | Paper is about **indigenous-land conservation alliances**, not gold mining. Its 11 rows are entirely indirect-pathway (indigenous land rights, road creation, miner influx). | Retain; these are the corpus's main source of indirect-pathway evidence. |
| soderquist2000 | Paper is about **post-gold-rush legacy forests** in southeast Australia (1850s gold rush + a century of recovery). Only 3 rows survived migration; most prior coding rows on this paper had `NA` source/destination. | Retain but flag as legacy-context; not contemporary ASGM. |

---

## 2. CONTROLLED VOCABULARY CONSISTENCY

### Duplicate / near-duplicate codes (require merging in v2 vocab)

| Code A | Code B | Recommendation |
|---|---|---|
| `road_creation` (Asner 2016) | `road_construction` (Schwartzmann 2005, Fearnside 2001) | Merge to `road_construction` (more general). |
| `weak_governance` (Lacher 1997, n=1) | `weak_governance_and_bad_policies` (multiple papers, n=4 across edges) | Merge to `weak_governance_and_bad_policies`. |
| `commerical_mine_closure` (Tarras-Wahlberg) | (no other paper uses this) | Rename to fix spelling: `commercial_mine_closure`. Preserved in migration to match prior workbook. |
| `mercury_use` vs `mercury_contaminated_tailings` vs `aquatic_mercury_pollution` vs `atmospheric_mercury_pollution` vs `mercury_bio_accumulation` | Five distinct mercury codes carrying a clean transport chain (use → tailings → aquatic + atmospheric → bioaccumulation → human health). | **Keep all five.** They form the core mercury-pathway sub-graph and are mechanistically distinct. |

### Subject codes used in >1 paper

| Code | Papers | Note |
|---|---|---|
| `gold_mining` | asner2016, castilhos2006, fearnside2001, lacher1997, regine2006, tarras-wahlberg2001 | The hub node of the DAG. Used as both subject and object (when miner_influx, gold_prices, governance drives it). |
| `mercury_use` | asner2016, castilhos2006, lacher1997, regine2006, tarras-wahlberg2001 | Consistent. |
| `aquatic_mercury_pollution` | castilhos2006, lacher1997, regine2006, tarras-wahlberg2001 | Consistent. |
| `mercury_contaminated_tailings` | castilhos2006, regine2006, tarras-wahlberg2001 | Consistent. |
| `mercury_bio_accumulation` | castilhos2006, lacher1997, regine2006, tarras-wahlberg2001 | Consistent. |
| `miner_influx` | asner2016, fearnside2001, lacher1997, schwartzmann2005, tarras-wahlberg2001 | Consistent. |
| `indigenous_land_rights` | schwartzmann2005, fearnside2001 | Consistent (with one sign anomaly in fearnside2001 — see Flag Review). |
| `gold_prices` | asner2016, schwartzmann2005 | Consistent. |

### Critical vocabulary gap

**`wildlife` and biodiversity outcomes are not directly coded.** The vocabulary file lists `wildlife` as a valid object_code, but **zero rows in the 2022 coding** used it. The corpus instead stops at proximate environmental endpoints:

- Forest-side: `deforestation_and_forest_degradation`, `barren_land`, `soil_excavation_and_erosion`, `protected_areas`
- Water-side: `mercury_bio_accumulation`, `aquatic_mercury_pollution`, `cyanide_pollution`, `sediment_load_in_rivers`
- Health-side: `human_health`

The implicit assumption is that these endpoints are reasonable proxies for biodiversity loss. **This is a major limitation for answering the framing question "how does gold mining affect biodiversity?"** The audit recommends adding the following object codes in a v2 vocabulary:

| Proposed v2 code | What it would capture | Found in PDFs (likely) |
|---|---|---|
| `species_richness_loss` | Loss of vertebrate/invertebrate/plant species richness | Soderquist 2000 (mammals), Régine 2006 (fish), Tarras-Wahlberg 2001 (benthic fauna) |
| `fish_community_composition` | Shifts in fish species mix downstream of ASGM | Tarras-Wahlberg 2001, Régine 2006 |
| `piscivorous_wildlife_mercury_exposure` | Hg burden in birds, otters, jaguars | Lacher 1997, Régine 2006 |
| `aquatic_invertebrate_diversity` | Benthic macroinvertebrate diversity | Tarras-Wahlberg 2001 |
| `mammal_abundance` | Population sizes of small/large mammals | Soderquist 2000 |
| `forest_carbon_loss` | Forest C stocks (proximate, but quoted in Asner 2016) | Asner 2016 |

A v0.2 PDF re-extraction would likely add 10–20 new biodiversity-side rows to the corpus by reading the Methods/Results sections more carefully.

### Conditionality coding

Of 105 rows, 78 carry `rel_conditionality_code = Population-specific` (typically because the 2022 `context` field said "Informal / ASGM" or "Mining company concession"). The corpus has effectively no Temporal or Spatial conditioning beyond the location stratification.

**Recommendation:** add `rel_conditionality_code = Temporal` to the Asner protected-area rows where the prior comment notes "the enforcement effect is fleeting."

---

## 3. RAW-TO-CODE ALIGNMENT

The migration is a 1:1 mapping from `(uncoded_source, uncoded_destination, arrow)` to `(subject_raw, object_raw, rel_valence)`. The 2022 raw-to-code alignment is largely faithful, but with these issues:

| Issue | Examples | Recommendation |
|---|---|---|
| Quote-spans cover claims that go to multiple destinations | `asner2016:r1-r4` all share the same Abstract sentence covering forest removal, soil excavation, mercury use, and threat-to-biodiversity. Each destination got a separate row with the same `rel_raw`. | Defensible; the multi-destination unpacking is faithful to the source's intent. |
| Single sentence interpreted as multiple links | `tarras-wahlberg2001` rows on cyanide + mercury + amalgamation share quoted spans. | Same as above; defensible. |
| `gold_mining → mercury_use` coded as Positive, but the relationship is *definitional* (ASGM by amalgamation uses mercury) rather than causal | Multiple papers | Accept as Positive; mechanism is definitional but direction is unambiguous. |
| `aquatic_mercury_pollution → mercury_bio_accumulation` (n=11) coded Positive | Multiple papers | Consistent and mechanistically clear. Strongest-replicated edge. |
| Some rows in `schwartzmann2005` collapse multi-sentence arguments into single rows | e.g. `indigenous_land_rights → deforestation_and_forest_degradation` | Accept; the consolidation step handles aggregation. |
| `castilhos2006` row on aquatic_mercury_pollution → human_health (n=1) overlaps with mercury_bio_accumulation → human_health (n=5) | Same paper, different mechanistic framings | Accept; the bioaccumulation chain is the more proximate link. Could be merged. |

---

## 5. SCHEMA COMPLIANCE

A column-by-column scan against `extraction/schemas/row.schema.json`.

### Permitted-value compliance

- **`paper_section`**: All migrated values mapped to {Abstract, Introduction, Results, Discussion, Methods}. Non-canonical sections from the 2022 workbook (e.g. "Future prospects: dynamics of soybean expansion") were collapsed to the nearest canonical value. ✓
- **`subject_trend_only`**: All values in {Yes, No}. No trend-only rows in this corpus (the 2022 coding required a source-destination pair). ✓
- **`rel_exists`**: All values in {Yes, Uncertain}. No "No" values — the 2022 coding did not capture null findings. ⚠ — re-extraction would likely surface these.
- **`rel_direction`**: All values in {Subject→Object, Bidirectional, Indeterminate}. ✓
- **`rel_valence`**: All values in {Positive, Negative, Indeterminate}. No Non-linear values (the 2022 coding scheme did not support Non-linear). ⚠ — re-extraction with v0.2 schema would surface dose-response findings (e.g. mercury concentration vs fish body size) as Non-linear.
- **`rel_conditionality_code`**: All values in {Population-specific, Unconditional}. ⚠ — re-extraction should add Temporal conditioning to the protected-area-enforcement rows.
- **`rel_uncertainty_code`**: All values in {Probable, Possible}. No Asserted or Speculative. Conservative default. ✓
- **`source_locus`**: Used Original to this study (primary papers) and Synthesised from multiple sources (review papers). No Cited from prior work — the 2022 coding did not distinguish original-data rows from cited-from-prior-work rows within a single paper. ⚠ — re-extraction would split these.
- **`method_type`**: All values in {Observation, Statistical modelling, Review}. No Experiment or Simulation. ✓
- **`causal_inference_level`**: All values are Association. ⚠ — re-extraction should examine whether any rows qualify as Controlled comparison (e.g. Asner's inside-vs-outside-protected-area design).
- **`geographic_scope_code`**: Used Country (most) and Region (Lacher pantropical). ✓
- **`population_code`**: Used Terrestrial ecosystem, Aquatic ecosystem, Human. ✓

### Required-field compliance

- **`paper_id`, `paper_section`, `version`**: present in all rows. ✓
- **`subject_raw`, `subject_code`**: present in all rows. ✓
- **`object_raw`, `object_code`**: present in all rows (no trend-only rows). ✓
- **`source_citation_raw`**: empty on all rows. ⚠ — re-extraction should fill where source_locus indicates a cited claim.

### Free-text fields

- **`rel_exists_note`**: every row carries the marker `[2022-migration] derived from prior manual coding workbook` plus the original 2022 comment where present. Good audit trail.
- **`effect_*` fields**: uniformly "Not reported". Re-extraction is the only fix.

### Issues to fix before re-running consolidation

1. Merge `road_creation` and `road_construction`.
2. Merge `weak_governance` and `weak_governance_and_bad_policies`.
3. Fix `commerical_mine_closure` → `commercial_mine_closure`.
4. Add Asserted uncertainty for primary-data rows that the source quote describes as conclusive (Asner: "regionally, gold mining-related losses of forest averaged 4437 ha yr⁻¹"; Castilhos: hair mercury measurements).

---

## 6. ONTOLOGY REVISION RECOMMENDATIONS

1. **Add biodiversity-outcome codes** as listed in section 2 above. The vocabulary's `wildlife` placeholder was never used; the corpus stops at proximate endpoints. Re-extraction should code species-level findings in Soderquist, Régine, Tarras-Wahlberg.

2. **Split `enforcement_and_other_barriers_to_entry`** into `enforcement_capacity` (presence of rangers, monitoring) and `enforcement_efficacy` (whether enforcement actually deters mining). The 2022 author already flagged this for Asner 2016.

3. **Split `gold_mining`** into:
   - `gold_mining_asgm` (artisanal / small-scale / informal)
   - `gold_mining_industrial` (mining-company concession)
   The 2022 `context` field already encodes this distinction; promote it to the subject_code.

4. **Add `mining_legacy_landscape`** as a distinct concept for post-mining recovery contexts (Soderquist 2000; Festin 2019). Currently `barren_land` and `restoration_measures` partially cover this but a unified code would help.

5. **Add `mercury_in_terrestrial_food_web`** alongside the existing aquatic chain. The 2022 coding only follows mercury through water; Lacher 1997 and other reviews note terrestrial pathways (soil → invertebrates → birds).

6. **Add `road_density`** distinct from `road_construction`. Density is a static landscape predictor; construction is a flow event. The Asner Interoceanic Highway story is about both.

7. **Re-encode `protected_areas`** as a subject_code with `protected_area_status` (binary) and as a context modifier for the spatial conditionality, not as an object_code (the current "gold_mining → protected_areas Negative" coding is awkward; the real claim is "protected_area_status reduces gold_mining incidence").

8. **The 2022 coding is one-pass and missed numeric effect sizes throughout.** The single most valuable v0.2 re-extraction would be to add `effect_magnitude` and `effect_metric` columns wherever the PDFs report them. Approximate audit estimates:
   - Asner 2016: ~10 numeric effects (regional deforestation rate, % inside/outside protected areas, hectare totals by year).
   - Castilhos 2006: ~15 numeric effects (mercury μg g⁻¹ in fish/sediment/hair by species and site).
   - Régine 2006: ~10 numeric effects (Hg fold-difference across 12 fish species, tissue partitioning).
   - Tarras-Wahlberg 2001: ~20 numeric effects (metal concentrations, sediment ratios).
   - Soderquist 2000: ~5 numeric effects (mammal capture rates by habitat).

---

END OF AUDIT REPORT
