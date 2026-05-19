# Gold-mining controlled vocabulary

Seeded from the 2022 manual coding (`prior work gold mining/Coding for mining review revision 2022(1).xlsx`, gold subset n=143). All codes carried over verbatim from the 2022 coding to preserve traceability with the prior work. Recommended renames and splits are documented in the audit report.

## subject_codes (drivers, pressures, mediators)

### Mining activity and inputs
| code | also covers |
|---|---|
| `gold_mining` | ASGM, alluvial gold mining, gold mining concession |
| `mercury_use` | amalgamation, mercury amalgam |
| `cyanide_use` | cyanide leaching |
| `soil_excavation_and_erosion` | open pit, surface stripping |
| `sediment_load_in_rivers` | sediment plume, turbidity (overlap with `turbidity` in cocoa vocab) |
| `mercury_contaminated_tailings` | tailings, amalgamation residue |

### Pollution / biogeochemistry (also serve as mediators)
| code | also covers |
|---|---|
| `aquatic_mercury_pollution` | water mercury, mercury in river water |
| `atmospheric_mercury_pollution` | mercury vapour, mercury emissions |
| `cyanide_pollution` | cyanide in water |
| `mercury_bio_accumulation` | methyl-mercury in fish, mercury in food web |
| `mercury_cyanide_compound_bio_accumulation` | combined Hg+CN compounds in fish |

### Governance and socio-economic drivers
| code | also covers |
|---|---|
| `gold_prices` | commodity price; demand |
| `economic_instability` | financial crisis, currency collapse |
| `economic_alternatives` | alternative livelihoods (absence/presence) |
| `need_for_economic_alternatives` | livelihood pressure |
| `informality` | informal / non-permit mining |
| `weak_governance_and_bad_policies` | state weakness, capture |
| `enforcement_and_other_barriers_to_entry` | enforcement, monitoring capacity |
| `effective_comprehensive_bottom_up_formalization` | formalisation programs |
| `legal_regulation` | mining law |
| `mining_lobbies` | industry lobbying |
| `miner_organization` | cooperatives, associations |
| `external_funding` | development assistance, donor support |
| `technical_alternatives_and_training` | cleaner technologies (e.g. retort), training programs |
| `indigenous_land_rights` | demarcation, titling |
| `protected_areas` | national parks, reserves |
| `social_inequality` | inequality of wealth/access |
| `social_vulnerability_of_miners` | miner poverty / health |
| `restoration_measures` | post-mining rehabilitation |
| `large_scale_commercial_agriculture` | soy expansion; not directly mining but indirect driver |

### Access and influx mediators
| code | also covers |
|---|---|
| `miner_influx` | inward migration of miners, population pressure |
| `road_creation` | also `road_construction`; routes opened |
| `infrastructure_construction` | broader (roads + ports + camps) |
| `boat_traffic` | river access (also used as ecological pressure) |
| `dry_season` | seasonal access window |
| `commerical_mine_closure` | industrial mine closure (release of labour pool to ASGM) — note 2022 spelling preserved |

## object_codes (outcomes / impacts)

| code | also covers |
|---|---|
| `deforestation_and_forest_degradation` | forest loss, primary forest conversion |
| `barren_land` | bare ground, denuded plots |
| `soil_excavation_and_erosion` | (also a mediator above) |
| `wildlife` | species abundance, fauna (broad) |
| `human_health` | morbidity, neuro-cognitive impact, mercury intoxication |
| `aquatic_mercury_pollution` | (also a mediator above) |
| `mercury_bio_accumulation` | (also a mediator above) |
| `sediment_load_in_rivers` | (also a mediator above) |

## Cross-domain / structural notes

The 2022 vocabulary uses several codes both as subject and object (mediators on a causal chain):
- `gold_mining` — caused by `gold_prices`, `miner_influx`, `weak_governance_and_bad_policies`; causes `deforestation_and_forest_degradation`, `mercury_use`, `cyanide_use`, `soil_excavation_and_erosion`, `sediment_load_in_rivers`, `indigenous_land_rights` (negative).
- `mercury_use` — caused by `gold_mining`; causes `aquatic_mercury_pollution`, `atmospheric_mercury_pollution`, `mercury_contaminated_tailings`.
- `aquatic_mercury_pollution` — caused by `mercury_use`, `mercury_contaminated_tailings`, `cyanide_use` (one row); causes `mercury_bio_accumulation`, `human_health`.
- `miner_influx` — caused by `road_creation`, `gold_prices`, `dry_season`, `commerical_mine_closure`, `social_inequality`; causes `gold_mining` (positive), `indigenous_land_rights` (negative).
- `enforcement_and_other_barriers_to_entry` — caused by `weak_governance`, `informality` (both negative); causes `gold_mining` (negative).
- `indigenous_land_rights` — caused by `gold_mining` (negative); causes `miner_influx`, `gold_mining`, `deforestation_and_forest_degradation` (all negative).

## Revision log

| date | change | rationale |
|---|---|---|
| 2022-08-29 | Initial coding by the original author over 10 papers. | Manual SAES-style extraction predating v0.2. |
| 2026-05-19 | Vocabulary migrated to v0.2 with code names underscored. Codes carried over verbatim; no merges or splits applied at migration time. | Preserve prior-work traceability; the audit recommends a vocab v2 with several splits/merges. |
