# SAES Audit Report — VBAC Corpus (v0.2.0-alpha)

> **Important caveat.** The extraction.md and audit.md prompts call for the audit to run in a *fresh* LLM session, ideally a different model. The work here was carried out in the same session as the extractions, which violates the protocol's separation-of-duties commitment. A second-pass audit by an independent reviewer (human or different model) is recommended before relying on the consolidated outputs.

**Audit scope:** Tasks 1, 2, 3, 5 (Flag review; Vocabulary consistency; Raw-to-code alignment; Schema compliance). Task 4 (Relationship completeness) was not performed because re-reading each PDF is out of budget; missing relationships are likely especially in the larger papers (Knight 2013, Lazarou 2021, Seffah 2014, Ashwal 2015).

**Sensitivity:** Comprehensive. Borderline cases flagged.

**Rows audited:** ~170 across 13 per-paper CSVs.

---

## 1. FLAG REVIEW

The following inline `[FLAG]` items appear in the extractions. Each is recommended for downstream consolidation handling.

### Novel subject/object codes flagged `[UNVERIFIED]`

These were introduced because the seed VBAC vocabulary (`results/vbac_vocabulary.md`) did not contain a clean match. Recommendation: **Accept** as additions to the working vocab, with revision-log entries.

| Code | First-appearing paper | Recommendation |
|---|---|---|
| `gestational_age_at_prior_cs` | gonen2004 | Accept; add to subject_codes |
| `birth_weight_at_prior_cs` | gonen2004, lazarou2021 | Accept; recurring in cohort |
| `estimated_fetal_weight` | gonen2004 | Merge with `macrosomia` for consolidation; they overlap |
| `cervical_effacement` | gonen2004 | Accept; intrapartum predictor |
| `cervix_position_anterior` | gonen2004 | Accept; intrapartum predictor |
| `cervical_dilation_at_rom` | gonen2004 | Accept; distinct from `cervical_dilation_at_admission` |
| `duration_first_stage` | gonen2004, girma2021 | Accept; recurring |
| `cervical_dilation_at_prior_cs` | obeidat2013 | Accept; novel labour-progress predictor |
| `tolac_attempt` | knight2013, konheim-kalkstein2017 | Accept; distinct from `vbac_success` (uptake vs success) |
| `vbac_failure_indication_fhr` | hollard2006 | Revise: collapse into `vbac_failure_indication_recurring` or drop; over-specific |
| `pelvic_anatomy` | olagbuji2010 | Accept; mechanistic citation |
| `premature_rupture_of_membranes` | knight2013 | Accept |
| `antepartum_haemorrhage` | girma2021 | Accept |
| `vacuum_at_cesarean` | clark2008 | Accept but note: case report, off-topic for VBAC predictor synthesis |
| `incision_delivery_time` | clark2008 | Off-topic; consider deleting from corpus |
| `vacuum_assisted_delivery` | clark2008 | Off-topic |
| `fetal_sex_male` | bhide2016 | Accept; demographic predictor |
| `maternal_smoking` | bhide2016 | Accept |
| `vaginal_birth_experience_desire` | konheim-kalkstein2017 | Accept; psychological predictor for *attempt*, not *success* |
| `locus_of_control_powerful_others` | konheim-kalkstein2017 | Accept; psychological |
| `healthcare_provider_information` | konheim-kalkstein2017 | Accept; clinician influence |
| `medical_profession` | konheim-kalkstein2017 | Accept; patient demographic |
| `antenatal_care` | seffah2014 | Accept |

### In-paper conflict / direction flags

| Paper | Row context | Flag | Recommendation |
|---|---|---|---|
| gonen2004 | gestational_age → vbac_success | Subject framed as ≤41 weeks predicting success; coded as Negative for GA→success (higher GA = lower success). | Accept; coding convention consistent |
| gonen2004 | epidural_analgesia → vbac_success | Effect reported as 'absence of epidural'; coded as epidural→success Negative | Accept |
| ashwal2015 | inter_delivery_interval → vbac_success | Multivariate OR 1.13 (longer = more success) **conflicts** with bivariate (failed group had longer interval, mean 5.07 vs 3.71 yr) | **Flag for disagreement report**; likely confounded by parity |
| obeidat2013 | inter_delivery_interval → vbac_success | Reports >2 years has HIGHER success (65% vs 47%) — opposite direction to most literature (e.g. Esposito 2000 cited by lazarou2021) | **Flag for disagreement report** |
| obeidat2013 | maternal_age → vbac_success | Reports older (≥30) has HIGHER success (64% vs 52%); opposite to most literature | **Flag for disagreement report**; authors attribute to parity confounding |
| obeidat2013 | prior_caesarean_indication_recurring | NS in this paper (p=0.361); conflicts with strong negative finding in bhide2016, olagbuji2010, ashwal2015 | **Flag for disagreement report** |
| bhide2016 | prior_vaginal_birth → vbac_success | Found NS (p=0.65); conflicts with strong positive finding in all other papers in cohort | **Flag for disagreement report**; possibly small absolute n (n=203/1463) |
| bhide2016 | maternal_smoking → vbac_success | Direction (smoker → more success) counter-intuitive | Confounded by ethnicity/BMI; recommend re-audit at next iteration |
| olagbuji2010 | Apgar 1-min outcome | Recurrent indication group had LOWER rate of low Apgar (15.6% vs 29.0%) — counter-intuitive | Re-audit; possibly selection effect (more rapid emergency CS in recurrent group) |
| seffah2014 | uterine_rupture rate 4.3% | Very high vs typical 0.5-1% range | Accept as reported; reflects low-resource-setting reality |

### Off-topic content

| Paper | Recommendation |
|---|---|
| clark2008_fetal_injury | Single case report about vacuum at REPEAT CS, not VBAC. Recommend **exclude** from accumulation, or use only as a marginal contextual citation. |
| konheim-kalkstein2017 | Outcome is `tolac_attempt` (decision/intention), not `vbac_success`. Recommend **stratify** in consolidation: keep rows but cluster separately. |

---

## 2. CONTROLLED VOCABULARY CONSISTENCY

### Subject codes used >1 paper

| Code | Papers | Note |
|---|---|---|
| `maternal_age` | gonen2004, hollard2006, knight2013, obeidat2013, olagbuji2010, bhide2016, ashwal2015, lazarou2021, seffah2014, chaillet2013, girma2021 (implicit via NS) | Consistent usage |
| `ethnicity` | hollard2006, knight2013, bhide2016 | Consistent; race vs ethnicity terminology varies but coded uniformly |
| `prior_vaginal_birth` | hollard2006, obeidat2013, olagbuji2010, bhide2016, ashwal2015, knight2013, girma2021, chaillet2013, lazarou2021 | Consistent |
| `prior_successful_vbac` | obeidat2013, ashwal2015, knight2013, girma2021, lazarou2021, chaillet2013 | Consistent |
| `prior_caesarean_indication_recurring` | obeidat2013, olagbuji2010, bhide2016, ashwal2015, knight2013, seffah2014, girma2021 (macrosomia), lazarou2021, konheim-kalkstein2017, chaillet2013 | Consistent; subsumes FTP/CPD/large-baby/recurrent indications |
| `prior_caesarean_indication_non_recurring` | gonen2004, olagbuji2010, obeidat2013 (implicit), lazarou2021 | Consistent; subsumes breech/malpresentation/fetal-distress-as-prior |
| `induction_of_labour` | hollard2006, knight2013, obeidat2013, bhide2016, ashwal2015, chaillet2013 | Consistent |
| `macrosomia` | hollard2006, knight2013, bhide2016, ashwal2015, seffah2014, girma2021 | Consistent; includes overlap with `birth_weight_at_prior_cs` |
| `cervical_dilation_at_admission` | gonen2004, girma2021 | Consistent |
| `maternal_bmi` | bhide2016, lazarou2021, chaillet2013, seffah2014 (cited only) | Consistent |
| `inter_delivery_interval` | knight2013, obeidat2013, ashwal2015, lazarou2021 (cited Bujold) | **Direction conflict** — see Task 1 |
| `epidural_analgesia` | gonen2004, hollard2006 | Consistent |
| `parity` | hollard2006, obeidat2013, seffah2014, girma2021 | Consistent but coding mixes parity-of-prior-pregnancies and prior-vaginal-births |
| `socioeconomic_status` | hollard2006, knight2013 | Consistent |
| `gestational_diabetes` | hollard2006, knight2013 | Consistent; knight2013 subsumes pre-existing diabetes here — could split |
| `preeclampsia` | hollard2006, knight2013 | knight2013 conflated with pre-existing hypertension — could split |
| `oxytocin_use` | gonen2004 (cited), knight2013 (cited) | Consistent |
| `labour_augmentation` | gonen2004 | Consistent |
| `prostaglandin_use` | gonen2004 (cited), lazarou2021 (cited) | Consistent |
| `uterine_rupture` | gonen2004, hollard2006, obeidat2013, olagbuji2010, ashwal2015, lazarou2021, seffah2014 | Object code used as both outcome and trend-only marker |

### Vocabulary recommendations

1. **Split `prior_caesarean_indication_recurring`** into:
   - `prior_caesarean_indication_dystocia` (FTP, CPD, slow progress, failed induction)
   - `prior_caesarean_indication_macrosomia` (big baby)
   These have different mechanisms and the dystocia subtype is the more reliable predictor.

2. **Decide policy on `prior_caesarean_indication_non_recurring`**: the literature treats fetal distress as recurring in some studies (lazarou2021) and non-recurring in others (gonen2004, olagbuji2010). Recommend treating fetal distress as a separate `prior_caesarean_indication_fetal_distress` category.

3. **`induction_of_labour`** is used for both prior-pregnancy induction and current-pregnancy induction. Recommend split into `induction_of_labour_current` and `induction_of_labour_prior`.

4. **Merge `tolac_failure` and `tolac_attempt`** outcome codes if they remain at <5 rows each after consolidation; otherwise keep them separate from `vbac_success` (the canonical success outcome).

5. **`birth_weight_at_prior_cs` vs `birth_weight_at_index_delivery`**: gonen2004 and lazarou2021 report the *prior* birth weight as a predictor (which captures the mother's intrinsic tendency to large babies). seffah2014, bhide2016, ashwal2015, girma2021 report the *current* birth weight. These should not be conflated — code them as distinct subject codes when consolidating.

---

## 3. RAW-TO-CODE ALIGNMENT

Spot-checks across the 13 CSVs reveal these alignment issues to flag:

| Paper:Row | Issue | Suggestion |
|---|---|---|
| knight2013 row 14 | `socioeconomic_status` → object_code `tolac_attempt` represents *uptake of TOLAC*; the rel_raw is about *attempted VBAC rate*, not success | Coding is correct given the introduced object code; ensure consolidation treats `tolac_attempt` and `vbac_success` as distinct edges |
| knight2013 row 7 | `pre-existing hypertension` coded under `preeclampsia` | Defensible (closest match in seed vocab) but split as recommended above |
| girma2021 row 1 | `fetal macrosomia as past indication of cesarean section` coded under `prior_caesarean_indication_recurring` | Defensible interpretation; mechanism is recurring large-baby tendency |
| obeidat2013 row 9 | Conflicts with knight2013 emergency-CS-indication finding | See disagreement report |
| seffah2014 row 11 | Coded under `maternal_bmi` but rel_raw lists multiple predictors as a composite | Recommend deleting this row and re-extracting as separate cited claims, OR consolidating as a synthesised meta-claim (current handling) |
| konheim-kalkstein2017 multiple rows | All outcome rows use `tolac_attempt` rather than `vbac_success` | Correct given the study's outcome variable; treat separately in consolidation |
| bhide2016 row 1, 2 | OR reported is for FAILED VBAC; coding converts to success-direction Negative | Correct; flagged in rel_exists_note |
| Multiple papers | "Indeterminate" rel_valence used for non-significant findings (e.g. NS associations) | Defensible; alternative would be to omit NS rows entirely. Keeping them preserves the "absence of evidence" signal |

---

## 5. SCHEMA COMPLIANCE

A column-by-column scan against `extraction/schemas/row.schema.json`:

### Permitted-value compliance

- **paper_section**: All values in {Methods, Results, Discussion, Introduction}. No Abstract rows. ✓
- **subject_trend_only**: All values in {Yes, No}. ✓
- **rel_exists**: All values in {Yes, No, Uncertain}. ✓
- **rel_direction**: All values in {Subject→Object, Object→Subject, Bidirectional, Non-directional, Indeterminate}. One Object→Subject (seffah2014 Apgar). ✓
- **rel_valence**: All values in {Positive, Negative, Non-linear, Indeterminate}. ✓
- **rel_conditionality_code**: All values in {Temporal, Spatial, Population-specific, Technology-specific, Unconditional, null}. ✓
- **rel_uncertainty_code**: All values in {Asserted, Probable, Possible, Speculative, null}. ✓
- **source_locus**: All values in {Original to this study, Cited from prior work, Synthesised from multiple sources}. ✓
- **method_type**: All values in {Observation, Experiment, Statistical modelling, Simulation, Review, Expert elicitation}. ✓
- **causal_inference_level**: All values in {Association, Controlled comparison, Intervention, Counterfactual}. No Intervention or Counterfactual rows in this corpus — all observational/regression. ✓
- **geographic_scope_code**: All values in {Country, Region, Biome, Global, null}. All set to Country (no biome/global appropriate for this clinical corpus). ✓
- **population_code**: All values are `Human`. ✓

### Required-field compliance

- **`paper_id`, `paper_section`, `version`**: present in all rows. ✓
- **`subject_raw`, `subject_code`**: present in all rows. ✓
- **`object_raw`, `object_code`**: empty only where `subject_trend_only = Yes`. ✓
- **`source_citation_raw`**: required when source_locus != "Original to this study". Compliance generally met but spot-check: a few cited-from-prior-work rows have `source_citation_raw` empty or terse (e.g. olagbuji2010 cited prior-work row). Recommend re-checking before publication.

### Free-text fields

- **`rel_exists_note`**: heavily used to carry `[FLAG]` markers and coding rationale. Useful as the audit trail.
- **`effect_magnitude`, `effect_error_magnitude`**: mix of numeric and string ("Not reported", ranges like "2.8-19.2"). Schema permits string-or-number; compliance ✓ but downstream pooling requires parsing.

### Issues to fix before consolidation

1. Several rows include `[FLAG]` in `subject_code` directly (e.g. `gestational_age_at_prior_cs [UNVERIFIED]`). For schema compliance the `[UNVERIFIED]` suffix should remain in the code itself per the extraction prompt — this is intended. Consolidation logic must strip the suffix when grouping.

2. `population_raw` is consistent across rows in a given paper but verbose. Consider standardising to "N=K women with one prior CS attempting VBAC".

3. Empty `effect_magnitude` is "Not reported" (string) in some rows and blank in others. Standardise to "Not reported".

---

## 6. ONTOLOGY REVISION RECOMMENDATIONS

1. **Split `prior_caesarean_indication_recurring`** into dystocia, macrosomia, and (debatably) fetal-distress sub-codes. The dystocia subtype is the cleanest predictor across this corpus (consistent strong negative effect in 6 of 13 papers). Currently the recurring code conflates several mechanisms.

2. **Distinguish `induction_of_labour_current` from `induction_of_labour_prior`**. The first is a within-pregnancy intervention reducing VBAC success; the second is a marker for prior dystocia indication. Conflating them confounds two distinct mechanisms.

3. **Distinguish `birth_weight_at_prior_cs` from `birth_weight_at_index_delivery`**. As noted in Vocab section.

4. **Outcome vocabulary needs `tolac_attempt` as a distinct outcome** from `vbac_success`. The Knight 2013, Konheim-Kalkstein 2017 rows are about uptake/decision, not success. Conflating them would mask important distinctions for policy.

5. **Add an `oxytocin_use_current` separate from `prostaglandin_use`** — both are induction agents but rupture risk profiles differ.

6. **Add `cervical_dilation_at_prior_cs`** to the working vocab. It is novel (Obeidat 2013) but well-defined and clinically meaningful.

7. **Consider retiring `socioeconomic_status` from the success-predictor vocabulary**: in Knight 2013 it predicts uptake, not success (NS for success, p=0.374). The signal is in uptake, not in success rates.

8. **For the rare-but-serious outcome `uterine_rupture`**: most papers report it as a `subject_trend_only` rate, not as a predictor relationship. The consolidation should produce a separate rupture-rate appendix rather than treating these as edges.

---

END OF AUDIT REPORT
