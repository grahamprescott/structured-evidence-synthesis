# Screening decisions — cocoa-biodiversity-yield-2026-05

OpenAlex search returned 48 works. The download script obtained PDFs for 12 (open access + accessible publisher host). Of those 12, screening against the research question gave:

## Included (8 — in `articles/`)

| File | First author year | Why included |
|---|---|---|
| `bisseleua2013.pdf` | Bisseleua et al. 2013 | Directly on topic: shade tree diversity → cocoa pest damage / yield in West Africa. |
| `jagoret2017.pdf` | Jagoret et al. 2017 | Directly on topic: structural characteristics of cocoa agroforestry → productivity in Cameroon. |
| `saj2015.pdf` | Saj et al. 2015 | Functional traits of companion (shade) trees in cocoa agroforests; matches the diversity → yield framing. |
| `abah2025.pdf` | Abah et al. 2025 | Pollinator biodiversity → cocoa yield (Nigeria). One mechanistic pathway. |
| `kongor2024.pdf` | Kongor et al. 2024 | Review of cocoa production challenges/solutions — likely contains synthesised biodiversity-yield claims. |
| `avadi2023.pdf` | Avadí 2023 | Environmental LCA of Ecuadorian cocoa value chain — touches on biodiversity/yield trade-offs. Partial relevance. |
| `schneider2010.pdf` | Schneider et al. 2010 | Baseline + design paper for long-term cocoa farming systems comparison. Partial relevance; mostly methodological. |
| `setyowati2025.pdf` | Setyowati 2025 | Socio-ecological sustainable cocoa agroecosystems (Java, Indonesia). Partial relevance. |

## Excluded — moved to `articles/excluded/`

| File | Reason |
|---|---|
| `bernet2019_palm_oil.pdf` | Wrong crop (palm oil). OpenAlex hit it on "cocoa" because the comparison framing mentions cocoa. |
| `rwigema2021_tea_coffee.pdf` | Wrong crop (tea/coffee in East Africa). |
| `kamath2024_biodiversity_at_risk.pdf` | Reverse causal direction: cocoa expansion threatening biodiversity, not biodiversity affecting yield. Important question but different. |
| `kouassi2023_adoption_only.pdf` | Drivers of agroforestry *adoption*, not the agroforestry → yield link. |

## Caveats

- Several "included" papers are partial-relevance only (Avadí 2023, Schneider 2010, Setyowati 2025). They are included to demonstrate the extraction pipeline against the actual corpus the search returned; in a production synthesis run we would tighten screening, broaden the search, or both.
- **Major selection bias**: the `is_oa:true` filter restricted the corpus to ~9% of the 18,761-paper population of cocoa + biodiversity + yield literature. The downloaded subset is further biased toward publishers that allow direct PDF access (no 403). Several highly relevant titles in the result set (e.g. Niether 2020 meta-analysis "Cocoa agroforestry vs monocultures") were detected by the search but not downloaded due to PDF-host restrictions.
- The corpus is small (8 papers) and not representative; treat outputs as a pipeline demonstration, not a synthesis claim.
