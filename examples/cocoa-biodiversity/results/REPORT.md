# Cocoa-biodiversity-yield corpus — extraction + accumulation run

**Run date:** 2026-05-19
**Protocol:** SAES v0.2.0-alpha
**Research question:** How does biodiversity affect cocoa yields?
**Corpus:** 8 PDFs in `articles/`, downloaded from OpenAlex with the query `title_and_abstract.search:cocoa yield biodiversity`, restricted to open-access English-language articles 2010-present (4 originally returned papers were screened out — see [`context/screening_decisions.md`](../context/screening_decisions.md)).

This report summarises what was produced, what the consolidated evidence says, and the caveats a reader should hold in mind before treating the outputs as authoritative.

---

## What was run

The full SAES v0.2 pipeline was applied end-to-end, mirroring the VBAC test case:

| Stage | Output |
|---|---|
| OpenAlex search → screen → download | 8 OA PDFs referenced in [`articles/README.md`](../articles/README.md); 4 off-topic results excluded (see [`context/screening_decisions.md`](../context/screening_decisions.md)). PDFs are not shipped in this repo. |
| Extraction | 8 per-paper CSVs in [`extractions/`](extractions/), 57 relationship rows |
| Audit | [`audits/audit_report.md`](audits/audit_report.md) |
| Consolidation (01) | [`accumulation/consolidated_edges.json`](accumulation/consolidated_edges.json) — 31 edges |
| Disagreement surfacing (02) | [`accumulation/disagreement_report.md`](accumulation/disagreement_report.md) — 3 flagged edges |
| DAG construction (03) | [`accumulation/union_dag.svg`](accumulation/union_dag.svg) + [`dag_metadata.json`](accumulation/dag_metadata.json) |

User-configured choices at the start of the run:

- **Relationship scope:** Option B (guided) — biodiversity-side predictors of cocoa-yield outcomes; mediators (e.g. pollination, predator abundance) kept inline.
- **Controlled vocabulary:** seeded cocoa vocab from the research-question framing ([`cocoa_vocabulary.md`](cocoa_vocabulary.md)); novel codes flagged `[UNVERIFIED]` at first appearance.
- **DAG:** produced.

---

## The 8 papers

| paper_id | type | location | rows |
|---|---|---|---|
| [bisseleua2013](../articles/bisseleua2013.pdf) | Primary observational (20 agroforests) | Cameroon | 16 |
| [jagoret2017](../articles/jagoret2017.pdf) | Primary observational (48 agroforests) + cited literature | Cameroon | 12 |
| [saj2015](../articles/saj2015.pdf) | Conference-poster abstract | Cameroon | 3 |
| [abah2025](../articles/abah2025.pdf) | Review (multi-crop pollination) | Nigeria | 7 |
| [kongor2024](../articles/kongor2024.pdf) | Review (cocoa challenges) | West Africa / pantropical | 10 |
| [avadi2023](../articles/avadi2023.pdf) | LCA on 5,495 farm records | Ecuador | 4 |
| [schneider2010](../articles/schneider2010.pdf) | Long-term-trial design / baseline | Bolivia | 1 |
| [setyowati2025](../articles/setyowati2025.pdf) | Qualitative socio-ecological (n=5 farmers) | Indonesia | 4 |

The corpus is **structurally review-heavy** — 19 of 31 consolidated edges include at least one cited-from-prior-work row.

---

## Headline findings

### What the corpus says about biodiversity → cocoa yield

**Yes, but it depends on which facet of biodiversity and which facet of yield.** The corpus does not support a single direction for an "agroforestry-vs-monoculture → yield" headline. It supports four distinct sub-claims:

1. **More shade (cover or density) reduces per-area yield magnitude.** Multiple primary studies (Bisseleua 2013, Jagoret 2017) and classical cited experiments (Besse 1972 +253% from shade removal; Lachenaud 1985 +247% monocrop vs agroforest) point unambiguously in this direction. Avadí 2023's Ecuador LCA confirms the per-hectare gap.

2. **Better-selected shade-tree species recover or surpass monoculture yield.** Functional diversity of shade trees → cocoa yield is positive in all 4 rows where it appears (Jagoret 2017 citing Saj 2017; Saj 2015 directly; Kongor 2024 citing Utomo 2016 cocoa-coconut). The "shade is bad for yield" headline is too coarse.

3. **Cocoa yield is pollination-limited.** The strongest causal-inference rows in the corpus (Toledo-Hernández 2020, 2023, cited by Kongor 2024) show hand pollination increases yield 51-161% and triples fruit set. If ambient pollinator service can be doubled by intervention, then the biodiversity → yield link operates *primarily through pollination*, not through pest control or microclimate. Abah 2025 reports a ~300 kg/ha differential between high- and low-pollinator-diversity farms.

4. **Agroforestry supports yield *stability* under climate stress, separately from magnitude.** Setyowati 2025 and Kongor 2024 (citing Blaser-Hart 2021) describe agroforestry as a climate-resilience strategy. These are not magnitude claims and should not be averaged with the magnitude rows — they are a different outcome variable.

### Strongest individual edges

| Edge | Direction | n_rows | Note |
|---|---|---|---|
| `agroforestry_vs_monoculture → cocoa_yield` | Mixed (5 Neg / 3 Pos) | 8 | Mixture is largely artefactual — magnitude rows are 5-0 Negative; stability rows are 3-0 Positive. **Flagged.** |
| `agroforestry_vs_monoculture → natural_enemy_abundance` | Positive | 6 | Bundled biodiversity/ecosystem-services claim. 5 of 6 rows are review-style. |
| `functional_diversity_of_shade_trees → cocoa_yield` | Positive | 4 | The key nuance row. Yield-friendly shade is about *species selection*, not amount. |
| `agroforestry_vs_monoculture → natural_enemy_abundance` | Positive | 6 | (duplicate row in summary — already above) |
| `shade_index → pod_loss_to_pests` | Negative | 2 | Bisseleua 2013 only; more shade = less pest damage. |
| `shade_index → natural_enemy_abundance` | Positive | 2 | Bisseleua 2013 only; ants, spider webs, wasp nests all increase with shade. |
| `shade_cover_percentage → cocoa_yield` | Negative | 2 | Cited from Blaser 2017, Grant 2022. |
| `rainfall_extreme → cocoa_yield` | Negative | 2 | Climate-side predictor; mediated by pollinator inactivity in rain. |
| `pollinator_diversity → pollination_success` | Positive | 2 | Abah 2025 only. |
| `shade_tree_density → unproductive_cocoa_rate` | Positive | 2 | Jagoret 2017 mediator chain. |

### Strongest mechanistic story (mediator chains in the DAG)

The DAG carries three mediator chains worth tracking:

- **shade_tree_density → unproductive_cocoa_rate → cocoa_yield** (Jagoret 2017). Density of associated trees increases the share of unproductive cocoa trees (coef +0.787); unproductive-rate then reduces yield (coef −7.438; model r²=0.834). *But* — `shade_tree_species_richness → unproductive_cocoa_rate` is **Negative** (coef −7.269), meaning more diverse shade rescues the loss. Density penalises; diversity rescues.

- **pollinator_diversity → pollination_success → cocoa_yield/pod_count** (Abah 2025, Kongor 2024 citing Toledo-Hernández). The only Intervention-level evidence for biodiversity → yield in the corpus.

- **shade_index → input_cost → farmer_net_returns** (Bisseleua 2013). More shade = lower spraying costs but also lower net returns (the input savings don't offset the yield loss in this dataset).

### Flagged disagreements (see [`disagreement_report.md`](accumulation/disagreement_report.md))

1. **`agroforestry_vs_monoculture → cocoa_yield`** — 5 Negative vs 3 Positive across 8 rows. Substantively, this is a *vocabulary collapse* (yield-magnitude vs yield-stability). Stratifying by outcome facet resolves most of the conflict.
2. **`shade_tree_density → natural_enemy_abundance`** — 1 Positive (native trees) vs 1 Negative (exotic, NS). Within-study stratification, not a real disagreement.
3. **`shade_tree_density → cocoa_yield`** — 1 Negative (native) vs 1 Indeterminate (exotic, NS). Same within-study stratification.

The shade-tree-density flags both resolve at the **vocabulary level** by introducing `shade_tree_density_native` and `shade_tree_density_exotic` codes.

---

## What the visual DAG shows ([`union_dag.svg`](accumulation/union_dag.svg))

- **`cocoa_yield`** is the central outcome (degree 9), drawn as the largest node.
- Three columns: **predictors** (left), **mediators** (centre, in yellow), **outcomes** (right). Mediator chains let the DAG carry mechanism, not just associations.
- **★** marks the two Intervention-level rows (Toledo-Hernández hand pollination via Kongor; Besse 1972 shade removal via Jagoret). These are the only causal-inference rows in the corpus.
- **Yellow halos and "!"** mark the 3 disagreement-flagged edges.
- **Co-benefit edge:** `agroforestry_vs_monoculture → carbon_sequestration` (Positive, Avadí 2023) is drawn separately at the bottom-right to show it is orthogonal to the yield axis.
- Edge thickness encodes `n_rows` (1.5 for n=1, 5 for n=8).

---

## Caveats — read these before using the outputs

These are the limitations a reader should weigh when interpreting any of the consolidated outputs.

### Protocol fidelity

1. **The audit was run in the same LLM session as extraction.** The v0.2 protocol explicitly calls for audit to run in a *fresh* session, ideally with a different model, to keep generation and evaluation separated. Re-running the audit independently is strongly recommended before relying on the consolidated edges.
2. **Audit Task 4 (Relationship completeness) was not performed.** Each paper was read once and relationships were extracted; no second pass cross-checked against the full text for missing claims. The larger papers (Bisseleua 2013, Jagoret 2017, Kongor 2024) likely have additional uncoded relationships, particularly in Methods and Supplementary sections that this pass did not enter.

### Corpus composition

3. **Only 8 papers in the corpus.** The OpenAlex search returned 48 results before screening; 36 were rejected at the abstract-screening step as off-topic (palm oil, tea/coffee, climate-projection rather than biodiversity, adoption-only rather than biodiversity-yield). A more inclusive search (e.g., adding "cacao", "shade", "agroforestry" individually) would likely produce a larger evidence base — including the well-cited Niether 2020 meta-analysis, Bisseleua 2009, Clough 2011, and the Schneider FiBL long-term trial follow-ups.
4. **The corpus is structurally review-heavy.** 19 of 31 consolidated edges include at least one cited-from-prior-work row. Kongor 2024 and Abah 2025 together contribute 17 rows, mostly citations of primary studies that are not themselves in the corpus. The Toledo-Hernández hand-pollination evidence and the Besse 1972 shade-removal evidence are the strongest in the corpus but **come to us via citation**, not directly from the source papers.
5. **Geographic spread is narrow at the primary-data level.** Cameroon (3 papers), Ecuador (1), Indonesia (1, n=5 only). Cited literature spans Côte d'Ivoire, Ghana, Brazil, Nigeria, Bolivia, but as third-hand evidence.
6. **Schneider 2010 contributes essentially zero evidence to the consolidation.** It is a long-term-trial design paper with no biodiversity-yield results yet. Setyowati 2025 has n=5 farmers and is qualitative. These two papers are best treated as context/citation chain rather than primary evidence.

### Causal inference

7. **49 of 54 contributing rows are at `Association` level.** Only 2 rows are `Intervention`-level (both cited from prior work, not original) and 3 are `Controlled comparison`. The pooled within-stratum effect sizes in [`consolidated_edges.json`](accumulation/consolidated_edges.json) are vote-counting summaries, not meta-analytic estimates.
8. **No primary cocoa-agroforestry vs cocoa-monoculture RCT is in this corpus.** The closest experimental evidence is from cited classical trials (Besse 1972, Lachenaud & Mossu 1985) and the FiBL Bolivian long-term trial baseline (Schneider 2010) whose results are not yet in the corpus.

### Vocabulary stability

9. **The seed vocabulary was extended during extraction.** ~9 novel codes carry `[UNVERIFIED]` markers (see audit report Task 1). The consolidation grouped by string-identical codes after stripping the suffix.
10. **`agroforestry_vs_monoculture` is over-broad.** It bundles full-sun-vs-shaded, intensive-vs-extensive, and single-species-vs-diverse contrasts. The mixed-valence flag on `agroforestry_vs_monoculture → cocoa_yield` is partly an artefact of this bundling. The audit recommends decomposing it for a v2 vocabulary.
11. **`natural_enemy_abundance` is also over-broad.** In several rows it carries bundled biodiversity / soil / carbon / pest-control claims. A separate `arthropod_predator_abundance` code and proper outcome codes for soil and carbon would clean this up.
12. **Yield magnitude and yield stability are coded under the same `cocoa_yield` outcome.** The audit recommends adding `cocoa_yield_stability` to separate the climate-resilience claims from the kg-per-hectare claims.

### Effect-size pooling

13. **Pooled effect sizes are NOT meta-analytic.** They are within-stratum vote-counting summaries computed only where rows shared a metric. Most edges have heterogeneous metrics (F-statistics, regression slopes, percent changes, kg/ha differentials, t C/ha/yr) and were not pooled.
14. **Many effect-size cells contain "Not reported" or "narrative only".** Where the extracted text was narrative without numbers, this is faithfully preserved.

### Reproducibility

15. **All work was done by a single LLM session.** A reproducibility check by re-running the same prompts on the same PDFs with a different model would be informative.

---

## Recommended next steps

1. **Independent audit pass.** Run [`audit.md`](../../../extraction/prompts/audit.md) on each per-paper CSV in a fresh session, ideally with a different LLM, and reconcile flagged items.
2. **Vocabulary v2.** Implement the audit's ontology recommendations: decompose `agroforestry_vs_monoculture` into shade-system / intensification / shade-diversity sub-codes; split `shade_tree_density` by tree provenance; add `cocoa_yield_stability` and `microclimate_buffering` as distinct codes; clean up `natural_enemy_abundance`.
3. **Expand the corpus.** Add Niether 2020 (meta-analysis of cocoa agroforestry yields), Clough 2011 (cocoa biodiversity-yield trade-offs in Indonesia), the FiBL Sara Beni long-term trial follow-up reports, Bisseleua's other primary studies (2009, 2017), Tscharntke 2011 reviews. The current 8-paper set is too small for confident synthesis.
4. **Get the Toledo-Hernández hand-pollination papers directly** (2020 Agric Ecosyst Environ; 2023 Agric Ecosyst Environ). These are the strongest mechanistic evidence in the corpus but currently enter only through Kongor 2024's citation. Extracting them as primary sources would convert the corpus's single best Intervention-level edge into a properly-supported primary-data finding.
5. **Add a stability-outcome appendix.** Setyowati 2025 and Kongor 2024 (citing Blaser-Hart 2021) make claims about yield stability under climate stress that are real but currently encoded awkwardly. A separate appendix or `cocoa_yield_stability` outcome would clean this up.
6. **For a publication-quality synthesis**, expand to ~30-50 papers including primary-data agroforestry yield experiments, pollination ecology, and pest-control biological-control trials. The current corpus is a useful proof-of-concept for the SAES protocol but is too narrow to settle the substantive question.

---

END OF REPORT
