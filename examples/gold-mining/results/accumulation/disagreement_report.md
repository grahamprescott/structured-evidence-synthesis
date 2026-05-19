---
run_date: 2026-05-19
corpus_reference: results/accumulation/extracted_rows.csv
consolidation_run_reference: results/accumulation/consolidated_edges.json
total_edges: 43
flagged_edges: 4
---

# Disagreement report — Gold-mining corpus (v0.2.0-alpha)

Four edges in the consolidated set carry `disagreement_flag = true`. **All four are vocabulary-artefact disagreements**, not substantive disagreements in the literature — they arise from the 2022 coding using two near-synonymous codes for the same construct. A fifth single-row anomaly is surfaced below the flag threshold.

The unanimity is itself a finding. After translation, every multi-row edge in this corpus has internally consistent valence. This is partly because the 2022 coding was carried out by a single author over a curated top-cited set, and partly because the gold-mining-on-biodiversity mechanisms are well-established: the direct biophysical pathway (deforestation, mercury bioaccumulation) is not contested in the literature, and the indirect socio-economic pathway has converging accounts across papers.

## Summary table

| Edge | Disagreement type | N rows | Recommended next step |
|---|---|---|---|
| `road_creation → miner_influx` | Vocabulary fragmentation (sibling code `road_construction` exists) | 2 | Merge with `road_construction → *` edges. |
| `road_construction → deforestation_and_forest_degradation` | Vocabulary fragmentation (sibling code `road_creation`) | 1 | Merge with `road_creation → *` edges. |
| `weak_governance → enforcement_and_other_barriers_to_entry` | Vocabulary fragmentation (sibling code `weak_governance_and_bad_policies`) | 1 | Merge with `weak_governance_and_bad_policies → *`. |
| `weak_governance_and_bad_policies → enforcement_and_other_barriers_to_entry` | Vocabulary fragmentation (sibling code `weak_governance`) | 1 | Merge with `weak_governance → *`. |

---

## road_creation / road_construction → (miner_influx, deforestation_and_forest_degradation)

**Disagreement type:** vocabulary fragmentation, not substantive.

**N rows:** 3 across two near-duplicate subject codes.

The 2022 coding used `road_creation` (Asner 2016 used the term for the Interoceanic Highway expansion in MdD; Schwartzmann 2005 used it for forest-frontier access) and `road_construction` (Schwartzmann 2005 and Fearnside 2001 used the term for industrial infrastructure builds in the Brazilian Amazon). The two are conceptually identical — the *opening of overland access into previously remote forest*.

**Rows on `road_creation → miner_influx`** (n=2, both Positive):

- `asner2016:r9` (asner2016, Introduction, Statistical modelling, Association, Peru/Madre de Dios)
  > "Second, paving of the Interoceanic Highway through Madre de Dios greatly increased roadway access to forests and prime gold mining sites (Asner et al 2010)."
- `schwartzmann2005:r4` (schwartzmann2005, Introduction, Review, Association, Brazil)
  > "Road creation increases access for miners and other land-grabbers into previously remote forest areas."

**Row on `road_construction → deforestation_and_forest_degradation`** (n=1, Positive):

- `schwartzmann2005:r3` (schwartzmann2005, Introduction, Review, Association, Brazil)
  > "Roads bring deforestation; road construction is the first stage of forest loss."

**Triage:** Direction is unambiguously Positive in all 3 rows. The disagreement flag is purely lexical.

**Recommended next step:** Merge the two codes into `road_construction` (more general) at the next vocabulary revision.

---

## weak_governance / weak_governance_and_bad_policies → enforcement_and_other_barriers_to_entry

**Disagreement type:** vocabulary fragmentation, not substantive.

**N rows:** 2 across two near-duplicate subject codes (and several additional rows where `weak_governance_and_bad_policies` connects to other targets such as `informality`, `effective_comprehensive_bottom_up_formalization`, `technical_alternatives_and_training`).

The 2022 coding inconsistently used `weak_governance` (Lacher 1997, n=1) and `weak_governance_and_bad_policies` (multi-paper, n=4 across the broader graph) for the same construct.

**Row on `weak_governance → enforcement_and_other_barriers_to_entry`** (n=1, Negative):

- `lacher1997:r7` (lacher1997, Heavy metals and mining → Discussion, Review, Association)
  > "Weak governance in tropical mining-producer states limits effective enforcement of environmental regulation."

**Row on `weak_governance_and_bad_policies → enforcement_and_other_barriers_to_entry`** (n=1, Negative):

- `tarras-wahlberg2001:r17` (tarras-wahlberg2001, Discussion, Observation, Association, Ecuador)
  > "Weak governance and ill-conceived mining policies in Ecuador have allowed unregulated discharge of mining effluents."

**Triage:** Direction is Negative in both. Lexical disagreement only.

**Recommended next step:** Merge to `weak_governance_and_bad_policies` at vocabulary revision.

---

## Sub-threshold tension: gold_mining → indigenous_land_rights

Not flagged by the algorithm (single row, no within-edge disagreement), but worth surfacing.

**`fearnside2001:r6`** codes `gold_mining → indigenous_land_rights` as **Positive**.

This sits awkwardly against:
- `miner_influx → indigenous_land_rights` (Schwartzmann 2005): **Negative** (miner influx degrades indigenous rights)
- `indigenous_land_rights → miner_influx` (Schwartzmann 2005, n=3): **Negative** (strong rights reduce miner influx — the reverse direction)
- `indigenous_land_rights → gold_mining` (Schwartzmann 2005): **Negative** (strong rights reduce mining)
- `indigenous_land_rights → deforestation_and_forest_degradation` (Schwartzmann 2005): **Negative** (strong rights reduce deforestation)

A Positive arrow on `gold_mining → indigenous_land_rights` is conceptually inconsistent with the rest of the indigenous-rights sub-graph. The 2022 comment on this row notes "ambiguously worded sentence — unclear if soybean cultivation hurting national interests because it promotes or competes with gold mining" (the comment refers to a Fearnside passage that conflates several drivers).

**Recommendation:** **Re-extract this row from the PDF.** The most likely correct reading is either:
- Negative (gold mining degrades indigenous land rights — consistent with the rest of the sub-graph), or
- Drop the row entirely (the source sentence is too ambiguous for a clean directional coding).

---

## Why so few substantive disagreements?

Three structural reasons:

1. **The 2022 coding was done by a single coder.** Inter-coder disagreement is absent by construction. A second coder (or v0.2 LLM re-extraction) would likely surface direction conflicts.
2. **The 2022 coding stops at proximate endpoints** rather than ultimate biodiversity outcomes (see audit report Section 2). Many of the disagreement-prone questions in the literature are at the ultimate-outcome stage (e.g., does ASGM-driven deforestation actually reduce vertebrate species richness in MdD, or does the regrowth scrub support a different community?). The corpus does not test those.
3. **The corpus is top-cited.** Top-cited papers tend to converge on dominant accounts; contrarian or controversial papers (e.g., those arguing ASGM has limited population-level mercury impact, or that protected-area enforcement is largely ineffective even when present) are under-represented.

**Recommended next step:** Re-extract from PDFs with the v0.2 prompts and add 2022–2025 papers to expose the corpus to contemporary controversies (Brazil Yanomami invasion 2023; mercury-Minamata implementation evaluations).

---

END OF DISAGREEMENT REPORT
