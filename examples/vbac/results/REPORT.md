# VBAC corpus — extraction + accumulation run

**Run date:** 2026-05-19
**Protocol:** SAES v0.2.0-alpha
**Corpus:** 13 PDFs in `articles/` covering predictors of successful vaginal birth after caesarean.

This report summarises what was produced, what the consolidated evidence says, and the caveats a reader should hold in mind before treating the outputs as authoritative.

---

## What was run

The full SAES v0.2 pipeline was applied end-to-end:

| Stage | Prompt | Output |
|---|---|---|
| Extraction | [`extraction/prompts/extraction.md`](../../../extraction/prompts/extraction.md) | 13 per-paper CSVs in [`extractions/`](extractions/), ~150 relationship rows |
| Audit | [`extraction/prompts/audit.md`](../../../extraction/prompts/audit.md) | [`audits/audit_report.md`](audits/audit_report.md) |
| Consolidation (01) | [`accumulation/prompts/01_consolidation.md`](../../../accumulation/prompts/01_consolidation.md) | [`accumulation/consolidated_edges.json`](accumulation/consolidated_edges.json) — 27 edges |
| Disagreement surfacing (02) | [`accumulation/prompts/02_disagreement_surfacing.md`](../../../accumulation/prompts/02_disagreement_surfacing.md) | [`accumulation/disagreement_report.md`](accumulation/disagreement_report.md) — 5 flagged edges |
| DAG construction (03) | [`accumulation/prompts/03_dag_construction.md`](../../../accumulation/prompts/03_dag_construction.md) | [`accumulation/union_dag.svg`](accumulation/union_dag.svg) + [`dag_metadata.json`](accumulation/dag_metadata.json) |

User-configured choices at the start of the run:

- **Relationship scope:** Option B (guided) — VBAC success predictors, prefer false negatives over false positives.
- **Controlled vocabulary:** seeded VBAC vocab built from the context note in `context/Claude VBAC generic.rtf` ([`vbac_vocabulary.md`](vbac_vocabulary.md)); novel codes flagged `[UNVERIFIED]` at first appearance.
- **DAG:** produced (prompt 03 was opted in).

---

## Headline findings

### Strong, well-replicated predictors of VBAC success

| Predictor | Direction | n_rows | Notes |
|---|---|---|---|
| `prior_caesarean_indication_recurring` (FTP, CPD, macrosomia as prior indication) | Negative | 11 | Most-replicated negative predictor. Effect sizes large (OR ≈ 0.32-0.66 for success, or 6.4 for failure in Bhide 2016). |
| `macrosomia` (current birth weight >4000 g) | Negative | 9 | Consistent across 6+ papers; pooled median OR ≈ 0.56. |
| `prior_vaginal_birth` (any vaginal delivery before the index TOLAC) | Positive | 9 | Single best predictor in most papers, with OR ≈ 3-5. One outlier (Bhide 2016) found NS — flagged. |
| `maternal_age` (older → less success) | Negative | 9 | Small effect (OR ≈ 0.79-0.93 per ~5 years); NS in smaller studies. |
| `induction_of_labour` (current pregnancy) | Negative | 7 | OR ≈ 0.59-0.70 across well-powered studies. |
| `prior_successful_vbac` | Positive | 6 | Strong (OR 2.7-10.5). The most consistent positive predictor when present. |
| `ethnicity` (non-white vs white) | Negative | 6 | OR ≈ 0.37-0.76. Sustained across UK, US and multi-centre data. Mechanism contested. |

### Moderately replicated

- `prior_caesarean_indication_non_recurring` (breech, malpresentation as prior indication) → positive (n=4)
- `maternal_bmi` (higher BMI → less success) → negative (n=4)
- `parity` (higher parity → more success) → positive (n=4)
- `gestational_age` (later GA → less success) → negative (n=3)
- `gestational_diabetes` → negative (n=3)

### Safety-side edges

The edges into `maternal_morbidity` and `uterine_rupture` originate from **`tolac_failure`** — i.e., a trial of labor that ends in emergency repeat CS. Successful VBAC is the *safer* end-state for the mother. Read the safety edges as: failure raises these outcomes, not success.

- `tolac_failure` → `maternal_morbidity`: positive (n=5, cited from prior reviews — Landon 2004, McMahon 1996, Hibbard 2001 and others). Failed TOLAC carries higher morbidity than either elective repeat CS or successful VBAC.
- `tolac_failure` → `uterine_rupture`: positive (n=2). Within-cohort comparisons: Ashwal 2015 reports 0.6% rupture among successful VBACs vs 7.4% among failed TOLACs; Lazarou 2021 reports similar.
- `oxytocin_use` / `prostaglandin_use` → `uterine_rupture`: positive (n=3, all cited).
- `uterine_scar_thickness` → `uterine_rupture`: negative (n=1, single cited meta-analysis, Lazarou 2021).
- Uterine rupture rates across the cohort range from ~0.5% (Western settings, well-monitored) to 4.3% (Seffah 2014, Ghana). The high rate in low-resource settings is itself a finding.

> **Clinical synthesis the corpus supports.** Attempted TOLAC carries risk only if it fails. Patient selection (using the predictors on the left of the DAG) shifts the balance: well-selected candidates have high VBAC success probability and successful VBAC carries *lower* morbidity than elective repeat CS; poorly-selected candidates have high failure probability and failed TOLAC carries *higher* morbidity than elective repeat CS. This is the rationale for prediction tools like the Grobman/MFMU calculator (validated in Chaillet 2013, referenced in Bhide 2016, Ashwal 2015, Lazarou 2021).

### Flagged disagreements (see [`disagreement_report.md`](accumulation/disagreement_report.md))

1. **`prior_vaginal_birth → vbac_success`** — 8 positive vs 1 NS (Bhide 2016). Likely a methodological outlier; recommend re-audit.
2. **`prior_caesarean_indication_recurring → vbac_success`** — 9 negative vs 1 NS (Obeidat 2013). Likely explained by Obeidat's spontaneous-labour-only restriction.
3. **`maternal_age → vbac_success`** — 6 negative vs 3 NS (and 1 inverse). NS findings in smaller studies; likely under-powered.
4. **`inter_delivery_interval → vbac_success`** — direction conflict between Knight 2013 (negative for longer interval), Obeidat 2013 (positive), Ashwal 2015 (multivariate positive, bivariate negative). The cleanest signal here is on *rupture risk*, not success.
5. **`preeclampsia → vbac_success`** — 1 negative vs 1 NS (n=2 total). Insufficient evidence.

---

## What the visual DAG shows ([`union_dag.svg`](accumulation/union_dag.svg))

- **`vbac_success`** is the central outcome (degree 19); most predictors point to it.
- **`tolac_failure`** is shown as a separate node below `vbac_success`. The two are complementary outcomes of the same TOLAC attempt (every TOLAC ends in either VBAC success or repeat-CS failure). A definitional dotted line connects them.
- **The safety-side edges (→ `maternal_morbidity`, → `uterine_rupture`) originate from `tolac_failure`, not from `vbac_success`.** The DAG includes an inline note clarifying this — failure raises those outcomes, not success. An earlier iteration of the SVG drew these edges starting too close to `vbac_success` and was misleading; the layout has been fixed.
- Five edges carry a yellow halo and "!" marker indicating disagreement.
- Edge thickness encodes `n_rows`; all edges are at Association level so the inference-level encoding (which would otherwise vary line weight) is uniform.

---

## Caveats — read these before using the outputs

These are the limitations a reader should weigh when interpreting any of the consolidated outputs.

### Protocol fidelity

1. **The audit was run in the same LLM session as extraction.** The v0.2 protocol explicitly calls for audit to run in a *fresh* session, ideally with a different model, to keep generation and evaluation separated. Re-running the audit independently is strongly recommended before relying on the consolidated edges.
2. **Audit Task 4 (Relationship completeness) was not performed.** Each paper was read once and relationships were extracted; no second pass cross-checked against the full text for missing claims. Larger papers (Knight 2013, Lazarou 2021, Seffah 2014, Ashwal 2015) likely have additional uncoded relationships.

### Corpus composition

3. **Clark 2008 (`clark2008_fetal_injury.csv`) is off-topic.** It is a case report about routine vacuum use at *elective repeat cesarean*, not about TOLAC or VBAC predictors. Recommend excluding from any downstream analysis.
4. **Konheim-Kalkstein 2017 measures `tolac_attempt` (decision/intention), not `vbac_success`.** Rows are kept in the corpus but the outcome variable differs and should be stratified separately during synthesis.
5. **Geographic spread is narrow.** Studies cover USA, UK, Israel, Germany, Quebec, Nigeria, Ghana, Ethiopia, Jordan. No South Asian, East Asian, Latin American or Australian data in this 13-paper corpus.
6. **Selection bias varies by paper.** Obeidat 2013 included only spontaneous-labour TOLAC. Ashwal 2015 excluded estimated fetal weight >4000 g. Bhide 2016 excluded preterm and multiples. These restrictions affect which predictor signals each paper can detect.

### Causal inference

7. **All evidence is at `Association` or `Controlled comparison` level.** There are no Interventional or Counterfactual studies in this corpus (no RCTs, no IV or DiD analyses). Any consolidated direction should be interpreted as an *association* under observed confounding, not a causal effect. The pooled within-stratum effect sizes in [`consolidated_edges.json`](accumulation/consolidated_edges.json) are vote-counting summaries, not meta-analytic estimates.
8. **`tolac_failure → uterine_rupture` is direction-questionable.** Uterine rupture often *forces* the TOLAC to fail (emergency CS for suspected rupture), so the edge may be bidirectional or mis-oriented. Treat with care.

### Vocabulary stability

9. **The seed vocabulary was extended during extraction.** ~20 codes carry `[UNVERIFIED]` markers (see audit report Task 1). The consolidation grouped by string-identical codes; some of these `[UNVERIFIED]` codes may need merging during a future iteration (e.g. `estimated_fetal_weight` overlaps with `macrosomia`; `birth_weight_at_prior_cs` is distinct from current-pregnancy `macrosomia`).
10. **`prior_caesarean_indication_recurring` conflates several mechanisms** (FTP, CPD, prior macrosomia, failed induction in prior pregnancy). The audit recommends splitting these in a v2 of the vocabulary; current consolidation treats them as one edge.
11. **`induction_of_labour` is used for both current-pregnancy induction and the "failed induction of labour" prior-CS indication.** These are different mechanisms; the consolidation collapses them.

### Effect-size pooling

12. **Pooled effect sizes are NOT meta-analytic.** They are within-stratum vote-counting summaries (median + range) computed only where all rows shared the same metric and ≥3 numeric magnitudes were available. Reference frames vary between papers (Bhide reports OR for failure; others for success; magnitudes here are mapped to the success direction).
13. **Several effect-size cells contain ranges or "Not reported".** Standardisation is incomplete; downstream pooling would require a second cleaning pass.

### Reproducibility

14. **All work was done by a single LLM session.** A reproducibility check by re-running the same prompts on the same PDFs with a different model would be informative. The pipeline as specified is otherwise reproducible.

---

## Recommended next steps

1. **Independent audit pass.** Run [`audit.md`](../../../extraction/prompts/audit.md) on each per-paper CSV in a fresh session, ideally with a different LLM, and reconcile flagged items.
2. **Drop or relabel Clark 2008.** It belongs in a different review.
3. **Split the recurring-indication code** into `prior_caesarean_indication_dystocia`, `prior_caesarean_indication_macrosomia`, and `prior_caesarean_indication_fetal_distress` before next consolidation pass.
4. **Separate `induction_of_labour_current` from `induction_of_labour_prior`** in the vocabulary.
5. **Cross-check the Bhide 2016 prior-vaginal-birth row** — it's the only outlier on what is otherwise an unanimous edge.
6. **Add a uterine-rupture incidence appendix** rather than treating rupture rows as predictor edges.
7. **For a publication-quality synthesis**, expand the corpus beyond 13 papers and add the validated Grobman/MFMU calculator papers (Grobman 2007, Costantine 2009) as primary sources rather than only through citations.

---

END OF REPORT
