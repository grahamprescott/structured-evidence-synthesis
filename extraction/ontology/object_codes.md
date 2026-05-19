# Object controlled vocabulary

Controlled-vocabulary stub for the `object_code` field (C2) in the extraction schema. The object is the variable the causal arrow points to — typically an outcome, effect, or dependent variable.

> **Status: stub.** The terms below are illustrative, drawn from the gold-mining worked example. Production runs require domain-specific vocabulary populated against the included corpus.

This is the vocabulary most prone to fragmentation across closely related papers — see [`examples/cocoa-biodiversity/`](../../examples/cocoa-biodiversity/) for an illustration. "Biodiversity" decomposes into species richness, community composition, functional diversity, phylogenetic diversity, and so on, and different papers measure different things. The accumulation stage's consolidation step is sensitive to how cleanly the object vocabulary lines up; tolerate fragmentation at extraction time, but harmonise aggressively at audit time.

## How to use this file

See [`subject_codes.md`](subject_codes.md). The lifecycle is identical: paste into the extraction prompt's controlled vocabulary slot; audit reports inconsistencies; harmonised terms are added back here with a date.

## Stub vocabulary (gold-mining example)

| code | definition | also covers | first added |
|---|---|---|---|
| `forest_cover_loss` | Reduction in forest cover area, measured as hectares or % change. | deforestation, forest loss, canopy loss | v0.1.2 |
| `soil_erosion` | Loss or displacement of soil material. | soil excavation, soil loss, erosion | v0.1.2 |
| `mercury_aquatic_pollution` | Mercury contamination of rivers, lakes, or other water bodies. | aquatic Hg pollution, river mercury, mercury in waterways | v0.1.2 |
| `mercury_atmospheric_pollution` | Mercury emitted to or transported in the atmosphere. | atmospheric Hg, Hg emissions | v0.1.2 |
| `mercury_bioaccumulation` | Accumulation of mercury in biological tissues, typically in fish or human consumers. | Hg bioaccumulation, fish mercury, mercury in tissue | v0.1.2 |
| `cyanide_pollution` | Cyanide contamination from gold leaching, in water or soil. | cyanide release, cyanide spill | v0.1.2 |
| `sediment_load` | Suspended sediment concentration in rivers, typically from mining-disturbed soil. | suspended sediment, turbidity from mining | v0.1.2 |
| `human_health_impact` | Adverse human health outcomes attributable to mining-related exposures. | health effects, disease burden, mercury health effects | v0.1.2 |
| `social_inequality` | Distributional outcomes that worsen existing social inequalities. | inequality, distributional impact | v0.1.2 |
| `indigenous_land_rights` | Recognition, erosion, or violation of indigenous land tenure. | indigenous tenure, land rights for indigenous communities | v0.1.2 |
| `miner_social_vulnerability` | Health, safety, or livelihood vulnerability of miners themselves. | miner welfare, miner vulnerability, ASGM livelihood | v0.1.2 |
| `local_employment` | Employment generated or displaced by mining activity. | jobs, employment effects | v0.1.2 |

## Ontology revision log

| date | change | rationale |
|---|---|---|
| 2026-05-15 | Migrated from `v2_code` to `object_code` to match ontology v0.1.2. | Field rename only; vocabulary unchanged. |

## When to split, when to merge

A persistent question at audit time. Heuristic:

- **Split** when two papers use the same surface term for materially different measurements (e.g. "biodiversity loss" measured as species richness in one paper and as functional diversity in another). Splitting preserves the distinction the accumulation stage needs to surface disagreement honestly.
- **Merge** when two papers use different surface terms for the same measurement under different naming conventions (e.g. "garimpo deforestation" and "artisanal mining forest loss"). Merging avoids spurious fragmentation that masks real signal.

When in doubt, split. The accumulation stage can re-merge with a vocabulary mapping; it cannot re-split codes that were prematurely collapsed.
