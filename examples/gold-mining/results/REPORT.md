# Gold-mining → biodiversity corpus — accumulation run

**Run date:** 2026-05-19
**Protocol:** SAES v0.2.0-alpha
**Research question:** How do gold mining operations directly and indirectly affect biodiversity?
**Corpus:** 8 PDFs inherited from a 2022 Scopus-based literature search (`prior work gold mining/`).

This report summarises what was produced, what the consolidated evidence says, and the caveats a reader should hold in mind before treating the outputs as authoritative.

---

## What was run

| Stage | Output |
|---|---|
| 2022 Scopus search → screening (inherited) | 8 PDFs referenced in [`articles/README.md`](../articles/README.md); 5 PDFs from the prior corpus excluded as off-axis (see [`context/screening_decisions.md`](../context/screening_decisions.md)). PDFs are not shipped in this repo for copyright reasons. |
| Prior coding migration | 143 gold-related rows in the 2022 Scopus coding workbook (held outside the repo — see [`context/prior_work_translation.md`](../context/prior_work_translation.md)) were translated into the v0.2 row schema; 105 rows survived (rest had NA source/destination). 8 per-paper CSVs in [`extractions/`](extractions/). |
| Audit | [`audits/audit_report.md`](audits/audit_report.md) |
| Consolidation (01) | [`accumulation/consolidated_edges.json`](accumulation/consolidated_edges.json) — 43 edges |
| Disagreement surfacing (02) | [`accumulation/disagreement_report.md`](accumulation/disagreement_report.md) — 4 flagged edges |
| DAG construction (03) | [`accumulation/union_dag.svg`](accumulation/union_dag.svg) + [`dag_metadata.json`](accumulation/dag_metadata.json) — 43 edges, 33 nodes |

User-configured choices at the start of the run:

- **Relationship scope:** inherited from the 2022 coder's framing (causal-link extraction from gold-mining papers with biodiversity-adjacent endpoints).
- **Controlled vocabulary:** seeded verbatim from the 2022 manual coding ([`gold_mining_vocabulary.md`](gold_mining_vocabulary.md)). No novel `[UNVERIFIED]` codes were introduced because the migration did not add new codes.
- **DAG:** produced.

**Important methodological note.** Unlike the cocoa and VBAC test runs, this is **not** a fresh-from-PDF v0.2 extraction. It is a *migration* of a 2022 manual coding workbook into the v0.2 schema, with the v0.2 audit / consolidation / DAG stages applied on top. Implications throughout the caveats section.

---

## The 8 papers

| paper_id | type | location | rows |
|---|---|---|---|
| [asner2016](../articles/asner2016.pdf) | Remote sensing + statistical modelling | Peru / Madre de Dios | 24 |
| [castilhos2006](../articles/castilhos2006.pdf) | Observational (fish + sediment + hair sampling) | Indonesia / N Sulawesi | 25 |
| [fearnside2001](../articles/fearnside2001.pdf) | Review / synthesis (soy + gold) | Brazilian Amazon | 8 |
| [lacher1997](../articles/lacher1997.pdf) | Pantropical ecotoxicology review | Tropics | 10 |
| [regine2006](../articles/regine2006.pdf) | Observational (12 fish species, French Guiana) | French Guiana | 4 |
| [schwartzmann2005](../articles/schwartzmann2005.pdf) | Review (indigenous conservation alliances) | Brazil / Kayapó / Xingu | 11 |
| [soderquist2000](../articles/soderquist2000.pdf) | Observational (mammal trapping in mining-legacy forest) | SE Australia | 3 |
| [tarras-wahlberg2001](../articles/tarras-wahlberg2001.pdf) | Observational (river water + sediment + biota) | Ecuador / Puyango basin | 20 |

---

## Headline findings

### What the corpus says about gold mining → biodiversity

The corpus is internally very consistent: **every multi-row edge has unanimous valence within itself.** No real direction conflicts surface from the consolidation. The four `disagreement_flag = true` edges are all **vocabulary fragmentation** (sibling codes for the same construct), not substantive disagreements.

The corpus supports four well-connected causal pathways from gold mining to (proxy) biodiversity loss:

1. **Direct biophysical pathway.** `gold_mining → deforestation_and_forest_degradation` (n=7, all Positive). The Asner 2016 Peru/MdD remote-sensing primary source plus Soderquist 2000's Australian mining-legacy fragmentation comprise the bulk. The corpus does not directly code species-level outcomes from deforestation, but the proximate endpoint is unambiguous.

2. **Toxic chain (mercury).** The strongest sub-graph in the corpus, spanning every primary observational paper:
   - `gold_mining → mercury_use` (n=8, Positive)
   - `mercury_use → aquatic_mercury_pollution` (n=8, Positive)
   - `mercury_use → mercury_contaminated_tailings` (n=4, Positive) → `aquatic_mercury_pollution` (n=4, Positive)
   - `mercury_use → atmospheric_mercury_pollution` (n=2, Positive)
   - **`aquatic_mercury_pollution → mercury_bio_accumulation` (n=11, Positive) — the most-replicated edge in the entire corpus**
   - `mercury_bio_accumulation → human_health` (n=5, Negative)
   - `atmospheric_mercury_pollution → human_health` (n=2, Negative)

3. **Toxic chain (cyanide).** Smaller parallel sub-graph: `gold_mining → cyanide_use` (n=3) → `cyanide_pollution` (n=6). Both Positive. Only Castilhos 2006 and Tarras-Wahlberg 2001 contribute; cyanide leaching is a leading practice at Indonesian Talawanan and Ecuadorian Portovelo-Zaruma sites.

4. **Socio-economic and governance loop.** A complete causal chain runs:
   - `gold_prices → gold_mining` (n=3, Positive; Asner 2016 plus Schwartzman 2005)
   - `miner_influx → gold_mining` (n=4, Positive; 5 papers)
   - `road_construction / road_creation → miner_influx` (n=3, Positive; 3 papers)
   - `enforcement → gold_mining` (n=2, Negative)
   - `weak_governance_and_bad_policies → enforcement` (n=2, Negative; with the vocab-alias `weak_governance` adding another row)
   - `informality → enforcement` (n=2, Negative)
   - `effective_comprehensive_bottom_up_formalization → informality` (n=1, Negative)
   - `indigenous_land_rights → miner_influx` (n=3, Negative; Schwartzman 2005)
   - `indigenous_land_rights → gold_mining` (n=1, Negative)
   - `indigenous_land_rights → deforestation_and_forest_degradation` (n=1, Negative)
   - `gold_mining → protected_areas` (n=3, Negative; mining incursion into protected areas)

The socio-economic loop is the corpus's distinctive contribution. Most environmental-impact reviews focus only on the biophysical chain; the prior 2022 coder captured the institutional-economic causal pathways with care.

### Where the corpus stops short

**The strongest critical observation from this run:** the 2022 coding stops at proximate environmental endpoints (deforestation, mercury bioaccumulation, human health). It does not directly code species-level biodiversity outcomes despite the vocabulary file listing `wildlife` as an outcome code. **Zero rows in the entire 105-row corpus use `wildlife` or any other species-level outcome code.**

This means the headline question — "how does gold mining affect *biodiversity*?" — is answered only by inference:

- Deforestation is well-established as a driver of vertebrate species loss → so `gold_mining → deforestation` is treated as a proxy for `gold_mining → species_richness_loss`.
- Mercury bioaccumulation is well-established as a piscivore/raptor stressor → so `aquatic_mercury_pollution → mercury_bio_accumulation` is treated as a proxy for `aquatic_mercury_pollution → piscivore_population_decline`.
- Sediment loading is well-established as a benthic invertebrate stressor → so `gold_mining → sediment_load_in_rivers` is a proxy for `gold_mining → benthic_invertebrate_diversity_loss`.

The implicit chain is reasonable but not extracted. A v0.2 native re-extraction from the PDFs should add explicit species-level outcome codes — particularly:

- **Soderquist 2000** has direct mammal-trapping abundance data not currently in the rows.
- **Régine 2006** has 12 species-level fish-Hg measurements not currently in the rows.
- **Tarras-Wahlberg 2001** has benthic invertebrate diversity data not currently in the rows.

### Flagged disagreements (see [`disagreement_report.md`](accumulation/disagreement_report.md))

All four flagged edges are **vocabulary fragmentation**, not substantive:

1. `road_creation → miner_influx` and `road_construction → deforestation_and_forest_degradation` — same construct under two codes.
2. `weak_governance → enforcement_and_other_barriers_to_entry` and `weak_governance_and_bad_policies → enforcement_and_other_barriers_to_entry` — same construct under two codes.

A fifth sub-threshold tension is the single-row `fearnside2001:r6 — gold_mining → indigenous_land_rights Positive`, which conflicts conceptually with the rest of the indigenous-rights sub-graph (all Negative). The 2022 comment on this row already noted the source sentence was "ambiguously worded." Recommend re-extracting from the PDF; likely a sign-error.

---

## What the visual DAG shows ([`union_dag.svg`](accumulation/union_dag.svg))

- **Five tiers** left to right: distal drivers, access/influx/governance mediators, mining activity (with `gold_mining` as the central hub, degree=13), pollution mediators, outcomes.
- **`gold_mining`** is the visual hub. 5 incoming edges (gold_prices, miner_influx, enforcement-Negative, economic_alternatives-Negative, indigenous_land_rights-Negative) and 8 outgoing.
- **The mercury chain** is drawn with progressively thicker edges culminating in the `aquatic_mercury_pollution → mercury_bio_accumulation` line (n=11, the heaviest in the diagram).
- **Yellow halos** mark the 4 vocabulary-fragmentation flags.
- A **callout box (top-right)** explains where biodiversity sits in the DAG: implicit, not explicit.
- A **summary panel (bottom)** highlights the three named pathways (direct biophysical / toxic chain / socio-economic loop).

---

## Caveats — read these before using the outputs

These are the limitations a reader should weigh when interpreting any of the consolidated outputs.

### Protocol fidelity

1. **This run is a migration, not a fresh extraction.** The 105 rows come from a 2022 manual coding workbook (single coder, paper-level method-type assignment, no numeric effect sizes captured). A v0.2 native re-extraction from the PDFs would yield more granular rows.
2. **The audit was run in the same LLM session as the migration.** Independent re-audit recommended.
3. **No quantitative effect sizes anywhere in the corpus.** All 105 `effect_*` cells are "Not reported." The PDFs themselves contain dozens of usable numbers (Asner's hectare/year deforestation rates, Castilhos's μg g⁻¹ hair-Hg measurements, Régine's species-level Hg fold-differences, Tarras-Wahlberg's metal concentrations, Soderquist's mammal capture rates) — none of these survive the migration. **This is the single biggest re-extraction gain available.**

### Corpus composition

4. **Small and old corpus.** 8 papers, publication range 1997–2016. The corpus predates the major 2016–2025 wave of Madre de Dios formalisation research (Álvarez-Berríos 2021 candidate excluded), the Yanomami/Venezuela ASGM-invasion literature (2020–2024), and Minamata-treaty implementation evaluations.
5. **Heavy lean toward Latin American Amazon.** 5 of 8 papers cover Amazonian or Andean sites; 1 each for Indonesia, French Guiana, Australia, and pantropical review. African ASGM (Ghana, Burkina Faso, DRC, Sudan), South-East Asian ASGM (Philippines, Myanmar), and Pacific small-island mining are under-represented.
6. **Schwartzmann 2005 and Fearnside 2001 are not primarily gold-mining papers** (they are on indigenous conservation and soy expansion respectively). They contribute valuable indirect-pathway rows but should be down-weighted for direct-impact synthesis.
7. **Soderquist 2000 is a post-mining legacy study** (1850s Australian gold rush), not contemporary ASGM. Its 3 surviving rows are off-pathway for ASGM-on-biodiversity but inform the legacy-impact question.

### Causal inference

8. **All 105 rows are at `Association` level.** No Intervention, Counterfactual, or even Controlled comparison rows. The Asner 2016 inside-vs-outside-protected-area design could plausibly be Controlled comparison; re-extract.
9. **`source_locus` is uniformly `Original to this study` (for primary papers) or `Synthesised from multiple sources` (for reviews).** The migration could not distinguish original-data rows from cited-from-prior-work rows within a single paper. Re-extraction would split these.
10. **Direction is sometimes ambiguous in the source PDFs but committed to one arrow in the 2022 coding.** The `fearnside2001:r6 gold_mining → indigenous_land_rights Positive` row is the clearest example.

### Vocabulary stability

11. **Vocabulary fragmentation in 2 cases** (road_creation/road_construction, weak_governance/weak_governance_and_bad_policies) — merge in v2.
12. **The `gold_mining` code conflates ASGM and industrial mining.** The 2022 `context` field already encodes this distinction; promote it to subject_code in v2 (`gold_mining_asgm` vs `gold_mining_industrial`).
13. **The `enforcement_and_other_barriers_to_entry` code conflates enforcement capacity and enforcement efficacy.** The 2022 author already flagged this. Split in v2.
14. **The `wildlife` code is in the vocabulary but never used in the rows.** See "Where the corpus stops short" above.

### Reproducibility

15. **Single-coder corpus, single-session migration.** The 2022 coding was done by one person; the v0.2 migration was done by one LLM in one session. Inter-coder / inter-model agreement has not been tested.

---

## Recommended next steps

1. **v0.2 native re-extraction from the 8 PDFs.** Highest-priority follow-up. Use [`extraction.md`](../../../extraction/prompts/extraction.md) with the seeded vocabulary plus the proposed biodiversity-outcome additions (see audit report §6). Expected gains: ~50 numeric effect sizes, ~15 species-level outcome rows, per-row method_type and source_locus, refined causal_inference_level.

2. **Independent audit pass.** Run [`audit.md`](../../../extraction/prompts/audit.md) on the freshly re-extracted CSVs in a separate session, ideally with a different model.

3. **Vocabulary v2:**
   - Merge `road_creation` ← `road_construction`.
   - Merge `weak_governance` ← `weak_governance_and_bad_policies`.
   - Fix `commerical_mine_closure` spelling.
   - Split `gold_mining` into ASGM vs industrial.
   - Split `enforcement_and_other_barriers_to_entry` into capacity vs efficacy.
   - Add: `species_richness_loss`, `fish_community_composition`, `piscivorous_wildlife_mercury_exposure`, `aquatic_invertebrate_diversity`, `mammal_abundance`, `forest_carbon_loss`, `mercury_in_terrestrial_food_web`.

4. **Expand the corpus.** Add 2017–2025 papers, especially:
   - Álvarez-Berríos et al. 2021 (Peru formalisation) — in 2022 candidate set; was author-selected but not coded.
   - Recent Brazil Yanomami / Venezuela Arco Minero literature (Roraima, Tapajós invasion studies).
   - Minamata-treaty implementation evaluations (UNEP, AMAP).
   - African ASGM studies (Ghana, Burkina Faso, Sudan).
   - The Niether-style cocoa-equivalent for mining: a recent meta-analysis if one exists.

5. **Cross-check the Fearnside 2001 sign-error.** The `gold_mining → indigenous_land_rights Positive` row is the only conceptual outlier; verify or drop.

6. **For a publication-quality synthesis**, the corpus needs at least 25–40 primary studies with biodiversity-outcome metrics, not 8 papers stopping at proximate endpoints. The current pipeline is a useful prior-work translation but not a publication-grade evidence base on its own.

---

END OF REPORT
