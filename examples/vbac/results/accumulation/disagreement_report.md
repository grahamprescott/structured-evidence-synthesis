---
run_date: 2026-05-19
corpus_reference: results/accumulation/extracted_rows.csv
consolidation_run_reference: results/accumulation/consolidated_edges.json
total_edges: 27
flagged_edges: 5
---

# Disagreement report — VBAC corpus (v0.2.0-alpha)

Five edges in the consolidated set carry `disagreement_flag = true`. Each is examined below.

## Summary table

| Edge | Disagreement type | N rows | Recommended next step |
|---|---|---|---|
| `prior_vaginal_birth → vbac_success` | Valence / magnitude conflict | 9 | Re-audit one row |
| `prior_caesarean_indication_recurring → vbac_success` | Existence conflict (single NS outlier) | 11 | Substantive disagreement; flag in synthesis |
| `maternal_age → vbac_success` | Existence / direction conflict | 9 | Stratify by population |
| `inter_delivery_interval → vbac_success` | Direction conflict | 4 | Substantive disagreement; flag in synthesis |
| `preeclampsia → vbac_success` | Existence conflict | 2 | Insufficient evidence |

---

## prior_vaginal_birth → vbac_success

**Disagreement type:** valence conflict (one indeterminate row), magnitude not pooled.

**N rows on edge:** 9
**Valence distribution:** 8 positive, 1 indeterminate

What's at stake: prior vaginal delivery is widely described as the single strongest positive predictor of VBAC success. One paper in the corpus (Bhide 2016) found no association, which contradicts the otherwise unanimous direction.

**Positive-valence rows** (prior vaginal birth → higher VBAC success):

- `hollard2006:r16` (hollard2006, Statistical modelling, Association, Southern California USA, Human)
  > "A history of no previous vaginal delivery was the strongest predictor of failure"
- `obeidat2013:r2-via-SVD` (obeidat2013, Statistical modelling, Association, North Jordan, Human)
  > "women with previous VBAC had higher odds to achieve VBAC success (OR = 3.8; 95% CI: 1.5, 9.5)"
- `olagbuji2010:r2` (olagbuji2010, Statistical modelling, Association, Benin City Nigeria, Human)
  > "previous vaginal delivery (p<0.0001, odds ratio (95% CI) 3.90 (2.1–7.4))"
- `ashwal2015:r2` (ashwal2015, Statistical modelling, Association, Israel, Human)
  > "prior vaginal delivery prior to the CS (3.05, 1.73-5.39, P<0.001)"
- `knight2013:r17-cited` (knight2013, Review, Association, UK, Human)
  > "all three studies included women with a prior vaginal delivery, which is the single best predictor of a successful VBAC"
- `girma2021:r3` (girma2021, Statistical modelling, Association, Ethiopia, Human)
  > "previous successful spontaneous vaginal delivery: AOR; 4, 95% CI (2.05, 7.83)"
- `chaillet2013:r3` (chaillet2013, Statistical modelling, Association, Quebec Canada, Human)
  > "+0.888 (any prior vaginal delivery [1 or 0])"
- `lazarou2021:r2` (lazarou2021, Statistical modelling, Association, Germany, Human)
  > "Any prior VB [...] OR 4.944 (1.798, 8.654), p=0.001"

**Indeterminate row** (no association detected):

- `bhide2016:r4` (bhide2016, Statistical modelling, Association, London UK, Human)
  > "Prior vaginal delivery did not affect the outcome of VBAC" (failed 14.5% vs successful 13.6%, p=0.65)

**Triage:**

- **Pass 1 (stratification):** The positive-valence rows span Israel, Jordan, Germany, Canada, USA, Nigeria, Ethiopia, UK (Knight cited). The single indeterminate row is also UK. No clean stratification by population, method, or geography distinguishes the discordant paper.
- **Pass 2 (substantive):** The most plausible explanation is methodological — Bhide 2016 has a low base rate of prior vaginal delivery in the cohort (≈14%), and the cohort already excluded women who underwent planned ERCS, so selection effects may suppress the effect. The other 8 rows are remarkably consistent in direction and magnitude.

**Recommended next step:** Re-audit rows — verify the Bhide 2016 extraction against the original paper. If correctly extracted, treat as a methodological outlier and retain the strong-positive consolidated finding. Note: this is **not** a substantive disagreement in the literature.

---

## prior_caesarean_indication_recurring → vbac_success

**Disagreement type:** existence conflict (one NS row against many strongly negative rows)

**N rows on edge:** 11
**Valence distribution:** 9 negative, 2 indeterminate

A recurring indication (dystocia / failure to progress / CPD / large baby) for the prior caesarean is the second-most-replicated negative predictor in this corpus.

**Negative-valence rows** (recurring indication → lower VBAC success):

- `olagbuji2010:r1` (olagbuji2010, Statistical modelling, Association, Nigeria, Human)
  > "a non-recurrent indication for previous caesarean section (p<0.001, odds ratio (95% CI) 0.32 (0.2–0.6))" [direction inverted: recurrent reduces success]
- `bhide2016:r3` (bhide2016, Statistical modelling, Association, London UK, Human)
  > "previous cesarean for failure to progress (OR 6.39, 95% CI 4.81–8.49)" [OR for failure]
- `ashwal2015:r5` (ashwal2015, Statistical modelling, Association, Israel, Human)
  > "Previous CS for recurring reason 0.52 (0.35-0.80) 0.003"
- `knight2013:r5` (knight2013, Statistical modelling, Association, England, Human)
  > "emergency caesarean section in their first birth [...] Adjusted OR 0.66 (0.63, 0.69)"
- `knight2013:r6` (knight2013, Statistical modelling, Association, England, Human)
  > "history of failed induction of labour (OR, 0.59; 95% CI, 0.53–0.67)"
- `girma2021:r1` (girma2021, Statistical modelling, Association, Ethiopia, Human)
  > "macrosomia as past indication of cesarean section delivery: AOR; 0.31, 95% CI (0.15, 0.62)"
- `lazarou2021:r5` (lazarou2021, Statistical modelling, Association, Germany, Human)
  > "Fetal distress as indication of the previous CD was associated with a higher rate of unsuccessful TOLAC (p=0.012)"
- `konheim-kalkstein2017:r4` (konheim-kalkstein2017, Statistical modelling, Association, USA, Human; outcome is TOLAC attempt rather than success)
  > "Reason for Prior CSEC [...] Large Baby [...] OR 0.011, p=0.003"
- `chaillet2013:r5` (chaillet2013, Statistical modelling, Association, Quebec, Human)
  > "−0.632 (recurring indication for CS [1 or 0])"

**Indeterminate / NS rows**:

- `obeidat2013:r7-NS` (obeidat2013, Statistical modelling, Association, North Jordan, Human)
  > "Previous indications for caesarean [...] not significantly associated, p=0.361"
- `seffah2014:r10-r11` (seffah2014, Observation, Association, Ghana, Human; descriptive only — listing failure indications)
  > "major indications for emergency repeat CS [...] CPD (17.0%), failure to progress (16.0%)"

**Triage:**

- **Pass 1 (stratification):** The indeterminate finding (Obeidat 2013, n=207) is a smaller cohort than most negative-valence studies (Knight 75,086; Bhide 1,463; Ashwal 1,767). Population is North Jordan, where the cohort selected only women in *spontaneous* labour — i.e., excluded the inducted/augmented women most likely to fail TOLAC. This is a meaningful stratification.
- **Pass 2 (substantive):** After stratification, the negative finding is robust. The Obeidat result likely reflects a healthier subpopulation in which the recurring-indication signal is attenuated.

**Recommended next step:** Substantive disagreement; flag in synthesis. Recommend reporting the consolidated negative effect with a caveat that the signal weakens in cohorts restricted to spontaneous-labour TOLAC.

---

## maternal_age → vbac_success

**Disagreement type:** existence / direction conflict

**N rows on edge:** 9
**Valence distribution:** 6 negative, 3 indeterminate

Older maternal age is widely reported to reduce VBAC success. Three papers in this corpus report no significant association (Hollard 2006, Olagbuji 2010, Bhide 2016 univariate, Ashwal 2015 multivariate), and one (Obeidat 2013) reports the *opposite* direction (older = more success), attributed by authors to confounding with parity.

**Negative-valence rows** (older age → lower success):

- `knight2013:r1` (knight2013, Statistical modelling, Association, England, Human)
  > "Maternal age (years) >34 [...] Adjusted OR 0.79 (0.77, 0.82)"
- `knight2013:r2` (knight2013, Statistical modelling, Association, England, Human)
  > "Maternal age (years) <24 [...] Adjusted OR 1.23 (1.17, 1.29)" [younger = more success]
- `lazarou2021:r1` (lazarou2021, Statistical modelling, Association, Germany, Human)
  > "Maternal age OR 0.925 (0.879, 0.974) p=0.003"
- `seffah2014:r4` (seffah2014, Statistical modelling, Association, Ghana, Human)
  > "mean age 29.60 vs 30.89 yr, p<0.001 (successful VBAC vs failed)"
- `chaillet2013:r1` (chaillet2013, Statistical modelling, Association, Quebec, Human)
  > "w = 3.766 – 0.039 (maternal age)"

**Indeterminate / NS rows**:

- `hollard2006:r8` (univariate NS, p=0.088)
- `olagbuji2010:r3` (NS, OR 0.62 (0.3-1.3))
- `bhide2016:univariate-NS` (univariate p=0.20)
- `ashwal2015:r6` (multivariate NS, OR 0.98)
- `obeidat2013:r5-NS-inverse` (NS, direction inverted: older = more success in this cohort)

**Triage:**

- **Pass 1 (stratification):** The papers reporting NS associations tend to have smaller sample sizes (Olagbuji 188, Obeidat 207, Bhide 1463). Knight (75,086) and Chaillet (3,113) and Seffah (2,472) all detect significant effects. This is consistent with a true small effect that requires large n to detect (Knight OR 0.79 per category is a small effect size).
- **Pass 2 (substantive):** Not a substantive disagreement — likely under-powered detection in smaller studies. Obeidat's inverse direction is acknowledged by the authors as parity confounding.

**Recommended next step:** Stratify by sample size or use age as a continuous variable. The signal is real but small; the consolidated weight should reflect the well-powered studies' effect estimates (OR ≈ 0.79-0.93 per ~5 years).

---

## inter_delivery_interval → vbac_success

**Disagreement type:** direction conflict (substantive)

**N rows on edge:** 4
**Valence distribution:** 1 positive, 2 negative, 1 indeterminate

Short inter-delivery interval is conventionally associated with higher rupture risk and lower VBAC success. The literature splits on whether the relationship to success itself is monotonic.

**Negative-valence rows** (longer interval → lower success):

- `knight2013:r13` (knight2013, Statistical modelling, Association, England, Human)
  > "Women who gave birth more than 3 years after the first baby were less likely to have a successful VBAC [Adj OR 0.95 (0.91-0.99), p=0.012]"

**Positive-valence row** (longer interval → higher success):

- `obeidat2013:r4` (obeidat2013, Statistical modelling, Association, North Jordan, Human)
  > "VBAC success rate was significantly associated with [...] inter-pregnancy interval [...] >2 years 65% vs ≤2 years 47%, p=0.018"
- `ashwal2015:r4` (ashwal2015, Statistical modelling, Association, Israel, Human; conflicts internally with bivariate)
  > "Interval from prior CS OR 1.13 (1.04-1.22), p=0.004 per year"

**Indeterminate row**:

- `lazarou2021:r8-NS` (NS, mean 3.0 vs 2.2 vs 2.7 years)

**Triage:**

- **Pass 1 (stratification):** The conflict does not track method or population cleanly. Knight (England, large administrative data), Obeidat (Jordan, single hospital), Ashwal (Israel, single hospital) all use multivariate regression. The Ashwal study explicitly notes its bivariate result is *opposite* to the multivariate. Knight uses ≥3 years as a categorical threshold; Obeidat uses >2 years; Ashwal uses a continuous variable. These are different operationalisations.
- **Pass 2 (substantive):** This appears to be a genuine substantive disagreement complicated by definition heterogeneity. Knight 2013 (n=75,086) is the most-powered, with effect estimate close to null (OR 0.95). Obeidat (n=207) and Ashwal (n=1,767) are smaller, and Ashwal's multivariate finding may be confounded by parity. The lazarou2021 cited Bujold finding suggests <24 months *raises rupture* risk specifically, separate from success-rate.

**Recommended next step:** Substantive disagreement; flag in synthesis. Recommend reporting that short intervals (<12-24 months) raise rupture risk and may modestly reduce success; longer intervals show inconsistent effects on success across studies. The cleanest separation is the *rupture* risk, not the success rate.

---

## preeclampsia → vbac_success

**Disagreement type:** existence conflict

**N rows on edge:** 2
**Valence distribution:** 1 negative, 1 indeterminate

**Negative-valence row**:

- `knight2013:r10` (knight2013, Statistical modelling, Association, England, Human)
  > "Pre-eclampsia/eclampsia [...] Adjusted OR 0.49 (0.42, 0.58)"

**Indeterminate row**:

- `hollard2006:r10-NS` (NS, OR 0.79 (0.47-1.49))

**Triage:**

- **Pass 1 (stratification):** Sample size difference (Knight n=75,086 vs Hollard n=2,575). Knight detects an effect Hollard cannot.
- **Pass 2 (substantive):** Not substantive — under-powered detection in Hollard.

**Recommended next step:** Insufficient evidence (only 2 rows). Defer until more studies are accumulated. The directionally consistent result favours Negative.

---

## Notes on edges NOT flagged but worth a second look

- **`maternal_bmi → vbac_success`** (n=4): all 4 rows are Negative but Lazarou's multivariate is NS while univariate is significant. Direction-consistent, magnitude-modest.
- **`socioeconomic_status → vbac_success`** (n=3): 2 positive (hollard) and 1 NS (knight). Different operationalisations (clinic service vs deprivation quintile). The "positive" hollard effect is on uptake more than success — review the coding.
- **`tolac_failure → uterine_rupture`** (n=2, both Positive): the direction-of-causation is questionable. Rupture *causes* the TOLAC to fail (forced emergency CS), so this is not a clean predictor relationship. Recommend re-coding as bidirectional or removing from the predictor DAG.

---

END OF REPORT
