# Subject controlled vocabulary

Controlled-vocabulary stub for the `subject_code` field (B2) in the extraction schema. The subject is the variable from which the causal arrow originates — typically a driver, cause, predictor, or independent variable.

> **Status: stub.** The terms below are illustrative, drawn from the gold-mining worked example. Production runs require domain-specific vocabulary populated against the included corpus. Treat the codes here as starting points to be extended via the audit-and-revise loop, not as a closed vocabulary.

## How to use this file

1. Before running `extraction/prompts/extraction.md`, paste the relevant subset of this file (or your own extended version) into the prompt's USER CONFIGURATION → CONTROLLED VOCABULARY section.
2. The extraction LLM uses these as preferred terms for `subject_code`. Novel terms encountered during extraction should be flagged `[UNVERIFIED]`.
3. The audit pass (Task 2) reports inconsistent usage and proposes harmonisations.
4. After audit, harmonised terms are added back to this file with a date stamp. The vocabulary grows.

The same discipline applies to `object_codes.md`.

## Convention

- **Codes are short, snake_case, English.** They are slugs, not prose.
- **Codes are domain-typed by prefix when ambiguity is likely.** e.g. `drv_gold_mining` vs `inv_gold_mining` if both a driver framing and an intervention framing are common in the literature. Prefixes are optional in single-domain syntheses.
- **Definitions are scoped.** The same English word can mean different things in different domains; the definition pins down the operational meaning for this synthesis.

## Stub vocabulary (gold-mining example)

| code | definition | also covers | first added |
|---|---|---|---|
| `gold_mining_artisanal` | Small-scale, low-mechanisation gold extraction, often informal. | ASGM, garimpo, garimpeiro mining, small-scale gold mining | v0.1.2 |
| `gold_mining_industrial` | Large-scale, mechanised gold extraction operated by a corporate entity, typically permitted. | LSGM, commercial gold mining, large-scale gold mining | v0.1.2 |
| `gold_price` | Market price of gold, typically USD/oz. Treat as a single subject regardless of currency. | gold price, gold market price | v0.1.2 |
| `economic_instability` | Macroeconomic conditions (recession, inflation, currency devaluation) framed as a driver of mining activity. | economic crisis, recession, inflation pressure | v0.1.2 |
| `enforcement_capacity` | State capacity to enforce mining or environmental regulations. | enforcement, regulatory capacity, governance capacity | v0.1.2 |
| `road_access` | Presence or expansion of roads enabling access to mining areas. | road creation, road network expansion | v0.1.2 |
| `mining_lobby_influence` | Organised political influence by mining interests on policy. | mining lobbies, industry capture | v0.1.2 |
| `protected_area_status` | Designation of an area as legally protected from extractive use. | protected area, reserve status | v0.1.2 |

## Ontology revision log

When the audit step (Task 2) recommends adding, splitting, merging, or retiring a term, log the decision here with a date and short rationale. This is a small file by design — if it grows past ~100 terms in a single domain, the synthesis question is probably under-scoped.

| date | change | rationale |
|---|---|---|
| 2026-05-15 | Migrated from `v1_code` to `subject_code` to match ontology v0.1.2. | Field rename only; vocabulary unchanged. |

## What's not here

- **Object-side vocabulary.** See `object_codes.md`.
- **Effect-size or method controlled vocabularies.** These are fixed in the schema enums, not extended per-synthesis.
- **Cross-paper alias dictionary.** When the same concept is named differently across papers, the alias is captured in the "also covers" column above, not in a separate file. Aliases are resolved at extraction time, not consolidation time.
