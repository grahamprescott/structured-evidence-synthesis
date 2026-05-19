---
run_date: 2026-05-19
corpus_reference: results/accumulation/extracted_rows.csv
consolidation_run_reference: results/accumulation/consolidated_edges.json
total_edges: 31
flagged_edges: 3
---

# Disagreement report — Cocoa-biodiversity-yield corpus (v0.2.0-alpha)

Three edges in the consolidated set carry `disagreement_flag = true`. Each is examined below. A fourth edge (`agroforestry_vs_monoculture → cocoa_yield`) carries the bulk of the substantive disagreement in the corpus and is examined in detail.

## Summary table

| Edge | Disagreement type | N rows | Recommended next step |
|---|---|---|---|
| `agroforestry_vs_monoculture → cocoa_yield` | Mixed-valence / different outcome facets | 8 | **Stratify by outcome facet** (yield magnitude vs stability); the disagreement largely dissolves. |
| `shade_tree_density → natural_enemy_abundance` | Stratified disagreement by tree provenance | 2 | Split vocabulary into native vs exotic shade-tree codes. |
| `shade_tree_density → cocoa_yield` | Stratified disagreement by tree provenance | 2 | Split vocabulary into native vs exotic shade-tree codes. |

---

## agroforestry_vs_monoculture → cocoa_yield

**Disagreement type:** mixed valence (5 Negative, 3 Positive).

**N rows on edge:** 8
**Valence distribution:** 5 Negative, 3 Positive

What's at stake: this is **the central question of the synthesis**. Does cocoa agroforestry support yield, or does it cost yield? The mixed-valence consolidation hides a substantive distinction that, once surfaced, resolves much of the apparent conflict.

**Negative-valence rows** (agroforestry → lower yield magnitude):

- `jagoret2017:r6` (jagoret2017, Discussion, Experiment, **Intervention**, Côte d'Ivoire, Terrestrial ecosystem)
  > "Besse (1972) [...] showed that the removal of shade tree led to a 253% increase in the mean cocoa yield per tree over a 5-year period"
- `jagoret2017:r7` (jagoret2017, Discussion, Experiment, Controlled comparison, Côte d'Ivoire)
  > "Lachenaud and Mossu (1985) showed that the yield of monocropped cocoa trees was 247% higher than that of a cocoa agroforest"
- `saj2015:r2` (saj2015, Abstract, Observation, Association, Central Cameroon)
  > "these c-AFS [...] providing farmers with sustainable low-but-steady cocoa yields"
- `kongor2024:r1` (kongor2024, Discussion, Statistical modelling, Controlled comparison, West Africa)
  > "some studies have reported higher cocoa yields under cocoa monoculture systems but with high inputs (fertilizers and agrochemicals)"
- `avadi2023:r1` (avadi2023, Results, Statistical modelling, Association, Ecuador)
  > "impacts per ha of monoculture are systematically higher than those of associated systems, despite lower yields, due to the lower input intensity of systems in cultural association"

**Positive-valence rows**:

- `kongor2024:r10` (kongor2024, Discussion, Statistical modelling, Association, Ghana)
  > "Blaser-Hart et al. (2021) emphasized that agroforestry is a climate-smart strategy used by agricultural stakeholders to combat climate change and improve agricultural production sustainability"
- `setyowati2025:r1` (setyowati2025, Discussion, Statistical modelling, Association, Yogyakarta Indonesia)
  > "shade trees and mixed cropping patterns improve farm microclimates, helping to stabilize cocoa yields despite unpredictable weather conditions"
- `setyowati2025:r4` (setyowati2025, Discussion, Review, Association, Tropical)
  > "agroforestry not only improves productivity but also strengthens cocoa farms' capacity to cope with climate change. The presence of shade trees helps maintain soil moisture, reduce heat stress, and provide habitats for pollinators"

**Triage:**

- **Pass 1 (stratification by outcome facet):** The 5 negative rows are about yield *magnitude* (kg/ha or pods/tree). All 3 positive rows are about yield *stability / resilience under climate stress* or *long-term productivity sustainability*. These are different outcome variables that have been collapsed under the same `cocoa_yield` code. When stratified, the magnitude-side is 5-0 negative, the stability/resilience side is 3-0 positive. The "disagreement" is largely **a vocabulary artefact**.
- **Pass 2 (substantive disagreement remaining):** The cited finding in `kongor2024:r3` (Utomo 2016 cocoa-coconut beating both monoculture and cocoa-rubber agroforestry on all environmental categories, including yield) is a genuine counterexample on the magnitude side. It is **already coded separately** under `functional_diversity_of_shade_trees → cocoa_yield` (n=4, unanimous positive) — so the corpus does represent this nuance, just on a different edge.
- **Pass 3 (causal-inference strength):** The two strongest-inference rows are both negative (jagoret2017:r6 Intervention, jagoret2017:r7 Controlled comparison). Both are cited classical experiments from the 1970s-80s. The two strongest-inference rows on the positive (stability) side come from a small qualitative study (n=5 farmers) and a literature synthesis.

**Recommended next step:** **Substantive disagreement is partial.** Split the edge in a v2 consolidation by introducing a new `cocoa_yield_stability` outcome code, separating the climate-resilience claims from the magnitude claims. After the split, the magnitude edge is unanimously Negative (with one cocoa-coconut nuance carried on the `functional_diversity_of_shade_trees` edge). Flag in the final synthesis that agroforestry reduces per-area yield magnitude but supports yield stability and ecosystem services.

---

## shade_tree_density → natural_enemy_abundance

**Disagreement type:** stratified disagreement (same study; native vs exotic tree provenance).

**N rows on edge:** 2
**Valence distribution:** 1 Positive, 1 Negative

This is a **within-study, by-strata** disagreement. Bisseleua 2013 reports both native-shade-tree density and exotic-shade-tree density separately, with opposite directions on the same outcome (spider webs and wasp nests).

**Positive-valence row** (native shade trees → more predators):

- `bisseleua2013:r6` (bisseleua2013, Results, Statistical modelling, Association, Cameroon, Terrestrial ecosystem)
  > "The number of spider webs and wasp nests significantly increased with increasing density of native shade trees" (F=11.5, r²=0.39, p<0.005)

**Negative-valence row** (exotic shade trees → fewer predators):

- `bisseleua2013:r7` (bisseleua2013, Results, Statistical modelling, Association, Cameroon)
  > "This number also tends to decrease with the density of exotic shade trees" (r²=0.01, p=0.64 — non-significant)

**Triage:**

- **Pass 1 (stratification):** The rows are stratified by tree provenance within a single study. They are not in real conflict; they describe two distinct strata of the same population. The negative row is itself non-significant (p=0.64), so the strongest reading is "native trees positively support predators; exotic trees show no effect."
- **Pass 2 (substantive):** There is no substantive disagreement in the literature. The disagreement is an artefact of the working vocabulary collapsing two ecologically distinct constructs.

**Recommended next step:** **Not a real disagreement.** Resolve at the vocabulary level: introduce `shade_tree_density_native` and `shade_tree_density_exotic` (or generic `_native` vs `_introduced`) as distinct subject_codes. Both rows would then sit on separate edges with consistent direction.

---

## shade_tree_density → cocoa_yield

**Disagreement type:** stratified disagreement (same study; native vs exotic tree provenance).

**N rows on edge:** 2
**Valence distribution:** 1 Negative, 1 Indeterminate

Same Bisseleua 2013 stratification, this time on the yield outcome.

**Negative-valence row** (native trees → lower yield):

- `bisseleua2013:r8` (bisseleua2013, Results, Statistical modelling, Association, Cameroon)
  > "Native shade trees negatively affected yield [...] y=2223.6-2.8x, F1,19=5.9, r²=0.25, p<0.05"

**Indeterminate row** (exotic trees → no detectable yield effect):

- `bisseleua2013:r9` (bisseleua2013, Results, Statistical modelling, Association, Cameroon)
  > "[exotic shade trees vs yield] r²=0.05, p=0.34" (NS)

**Triage:**

- **Pass 1 (stratification):** Same provenance stratification as the previous edge. The pattern is interpretable: **native trees both support predators AND reduce yield** (the land-sharing trade-off operates *via* native trees). Exotic trees support neither effect — they neither feed the predator community nor cost yield.
- **Pass 2 (substantive):** No substantive disagreement; this is also a vocabulary artefact.

**Recommended next step:** **Not a real disagreement.** Resolve at the vocabulary level (same fix as above edge). Note that the two stratified edges together support a mechanistic claim: the land-sharing trade-off in this corpus operates specifically through native (forest-derived) shade trees, not through exotic species.

---

## Additional substantive tensions (below `disagreement_flag` threshold)

These do not carry the flag because they are single-row or because the consolidation collapses them under one direction, but they are worth surfacing for the final synthesis.

1. **`functional_diversity_of_shade_trees → cocoa_yield` (n=4, unanimous Positive) vs. `shade_cover_percentage → cocoa_yield` and `shade_tree_density → cocoa_yield` (Negative).** All three are facets of "shade." The corpus consistently distinguishes: more cover/density of shade hurts yield, but better *selection* of shade-tree species can recover or improve yield. The conventional shade-vs-yield framing is too coarse.

2. **`pollination_success → cocoa_yield` (n=1, Intervention-level, +51%-+161%) and `pollinator_diversity → cocoa_yield` (n=1, Association, ~+300 kg/ha) are quantitatively very large.** If real, they imply that cocoa yield is severely pollination-limited and that ambient pollinator services in most cocoa systems are far below saturation. Yet only 2 papers in the corpus (Abah 2025, Kongor 2024) treat this; Bisseleua 2013 and Jagoret 2017 — the largest primary-data papers — do not measure pollinator abundance or fruit set. This is a **gap in the corpus**, not a disagreement: the strongest mechanistic biodiversity-yield link is also the most under-sampled.

3. **`bisseleua2013:r1` (shade_index → cocoa_yield, Negative) vs. `jagoret2017:r5` (shade_tree_density → cocoa_tree_basal_area, Positive — forest trees → larger cocoa trees).** Bisseleua's headline is "more shade = less yield." Jagoret's headline is "well-structured forest cover supports cocoa vigour, which positively predicts pod count." These are not contradictory once mediator variables are introduced (Jagoret's chain shade-tree-density → unproductive-rate → yield is Negative overall) but they emphasise different mechanisms.

---

## Disagreements involving review and cited-from-prior-work rows

A persistent concern: **31 of 54 rows** (57%) are cited from prior work or synthesised, not original-data. Among the flagged edges, only Bisseleua 2013 and Avadí 2023 contribute original-data rows. This corpus is structurally review-heavy. Recommendation: when ranking evidence for the final synthesis, weight original-data rows above cited rows; weight Intervention/Controlled-comparison rows above Association rows.

The two **Intervention-level rows** in the corpus (Jagoret 2017 citing Besse 1972; Kongor 2024 citing Toledo-Hernández 2020/2023) point in **opposite directions on the agroforestry-yield axis**: Besse's shade-removal trial shows monoculture wins on yield, while Toledo-Hernández's pollination-supplementation trial shows that ambient pollinator service (more abundant in agroforestry) is the binding constraint. Neither is a direct cocoa-agroforestry-vs-cocoa-monoculture RCT — that experiment is not in the corpus.

---

END OF DISAGREEMENT REPORT
