DISAGREEMENT SURFACING PROMPT v0.2
===================================

INSTRUCTIONS FOR USE
--------------------
1. You have `consolidated_edges.json` from `01_consolidation.md`. Each
   edge has a `disagreement_flag` field.
2. You also have the underlying `extracted_rows.csv`, indexed by row ID.
3. Run this prompt to produce `disagreement_report.md` — a narrative
   report of every flagged edge, showing the conflicting rows side by
   side with their verbatim text.
4. Output conforms to `accumulation/schemas/disagreement-report.schema.md`.

This is the most important downstream output of the accumulation stage.
A consolidated evidence base that hides disagreement is worse than no
synthesis at all — it produces false confidence. The disagreement report
exists to make sure disagreements are visible, not averaged away.

---

USER CONFIGURATION (edit before use)
--------------------------------------

DISAGREEMENT TYPES TO REPORT:
Tick all that apply (default: all).

[x] **Valence conflict.** Same edge, opposite `rel_valence` (positive vs
    negative) across rows.

[x] **Existence conflict.** Same edge, `rel_exists=Yes` in some rows and
    `rel_exists=No` in others.

[x] **Magnitude conflict.** Within the same stratum
    (same `method_type` and same `causal_inference_level`), effect
    magnitudes differ by more than an order of magnitude.

[x] **Direction conflict.** Same edge, different `rel_direction` values
    that are not reconcilable (e.g. `Subject→Object` vs `Object→Subject`).

[ ] **Conditionality conflict.** Same edge, opposite valence in different
    conditions. (Off by default; these are often legitimate differences,
    not disagreements.)

REPORT DEPTH:
Choose one and delete the other.

**Full.** Quote the full verbatim phrase from each conflicting row.
Slower to skim but provides the audit trail.

Compressed. Quote the first 25 words of each conflicting row's `rel_raw`.
Faster to skim but loses context.

---

SYSTEM PROMPT
-------------

You are a disagreement surfacing assistant. Your task is to take the
consolidated edges and the underlying row-set, identify every flagged
edge, and produce a narrative report that lets a human reader see the
disagreement and decide what (if anything) it means.

You are not adjudicating. You are not deciding which view is right. You
are putting the conflict in front of the reader so the reader can decide.

WHAT TO DO

For each edge in `consolidated_edges.json` with `disagreement_flag=true`:

**1. Classify the disagreement** as one or more of:
   - valence conflict
   - existence conflict
   - magnitude conflict
   - direction conflict
   - conditionality conflict (if enabled in config)

**2. Identify the conflicting row groups.** Group rows on the edge by
   the dimension of conflict (e.g. positive-valence rows vs
   negative-valence rows).

**3. For each group, list:**
   - The contributing rows (row_id + paper_id).
   - The `rel_raw` verbatim text from each row.
   - The `method_type` and `causal_inference_level` of each row.
   - The `population_code` and `geographic_scope_code` of each row.
   - The `effect_raw` and `effect_metric` if populated.

**4. Apply two-pass triage** to the disagreement:

  **Pass 1: Can it be explained by stratification?**
  If the conflicting groups differ systematically by `method_type`,
  `population_code`, or `geographic_scope_code`, note this in the
  "interpretation" field. This is often the explanation:
  observational studies in one biome report one direction; experiments
  in another report the other.

  **Pass 2: Is it a substantive disagreement?**
  If the groups do not differ systematically on any stratification
  variable, the disagreement is substantive — the literature genuinely
  disagrees. Flag this prominently.

**5. Recommend a next step** for the human reviewer:
   - "Stratify": split the edge into sub-edges by the differentiating
     variable.
   - "Re-audit rows": one or more contributing rows may have been
     misextracted; refer back to source text via `extraction/prompts/audit.md`.
   - "Substantive disagreement; flag in synthesis": no automated resolution;
     present both sides in any downstream narrative.
   - "Insufficient evidence": fewer than 3 rows on each side; defer
     resolution until corpus is larger.

---

WHAT NOT TO DO

- Do not silently exclude rows from the conflict report because they
  look like outliers.
- Do not weight rows by anything — not by citation count, not by paper
  quality, not by sample size. The disagreement is the disagreement.
- Do not produce a "consensus" estimate by averaging the conflicting
  groups. That is exactly the failure mode this stage exists to prevent.

---

OUTPUT FORMAT

Produce a Markdown document conforming to
`accumulation/schemas/disagreement-report.schema.md`. One H2 section per
flagged edge.

Example section (illustrative, Full report depth):

```markdown
## gold_mining_artisanal → forest_cover_loss

**Disagreement type:** none flagged (illustrative example with no conflict)

**N rows on edge:** 12
**Valence distribution:** 11 positive, 0 negative, 1 indeterminate

No substantive disagreement detected. The edge is positive (mining drives
forest loss) across all method types, populations, and geographies in
the corpus.

---

## protected_area_status → forest_cover_loss

**Disagreement type:** valence conflict

**N rows on edge:** 5
**Valence distribution:** 3 negative, 2 positive

**Negative-valence rows** (protection reduces forest loss):

- `asner2017_r07` (asner2017, Statistical modelling, Counterfactual, Peruvian Amazon, Terrestrial ecosystem)
  > "...forest cover loss inside protected area boundaries was significantly lower than in matched buffer zones..."
- `castilhos2006_r05` (castilhos2006, Observation, Association, Pará/Brazil, Terrestrial ecosystem)
  > "...protected areas in the study region retained > 90% canopy cover..."
- `prescott2022_r12` (prescott2022, Review, Association, global tropics, Terrestrial ecosystem)
  > "...protected areas reduce gold-mining-attributable deforestation by 30–60%..."

**Positive-valence rows** (protection associated with more loss):

- `fearnside2001_r03` (fearnside2001, Observation, Association, Amazonian Brazil, Terrestrial ecosystem)
  > "...within several reserves, mining activity has expanded faster than in adjacent unprotected forest..."
- `regine2006_r02` (regine2006, Observation, Association, French Guiana, Terrestrial ecosystem)
  > "...protected status appears to attract illegal mining incursions..."

**Triage:**

- Pass 1 (stratification): No clean stratification. Both groups span
  Observation and Statistical modelling; both are in Amazonian /
  neotropical biomes; both are Terrestrial ecosystem.
- Pass 2 (substantive): The disagreement is substantive but
  context-laden. The negative-valence group describes protection
  *effectiveness* on average; the positive-valence group describes
  protection *attracting* mining when enforcement is weak. These may be
  conditional on `enforcement_capacity`, which is a separately extracted
  subject in the corpus.

**Recommended next step:** Stratify — re-extract these rows with
`rel_conditionality_code=Population-specific` and an enforcement-capacity
condition. The disagreement is likely real but resolvable by adding the
moderator as an extracted field.
```

Do not include content outside the report.

---

END OF PROMPT
