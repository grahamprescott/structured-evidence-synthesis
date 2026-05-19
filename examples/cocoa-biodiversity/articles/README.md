# Cocoa-biodiversity corpus — articles

PDFs are not included in this repository. All 8 included papers are open-access; the 4 excluded papers are also OA. You can re-fetch them from OpenAlex using the search log + screening decisions below.

## Inputs needed to rebuild this folder

- [`../context/search_log.json`](../context/search_log.json) — the OpenAlex query and filters used (search ID `cocoa-biodiversity-yield-2026-05`).
- [`../context/screening_decisions.md`](../context/screening_decisions.md) — which 8 papers were included and which 4 were excluded.
- [`../openalex_pdf_download.py`](../openalex_pdf_download.py) — the helper script that retrieves OA PDFs from OpenAlex with httpx.
- [`../download_log.csv`](../download_log.csv) — what was actually downloaded in the original run, with timestamps and OpenAlex IDs.
- [`../openalex_works.jsonl`](../openalex_works.jsonl) — the raw OpenAlex JSONL response for the 48-result search.

## Included papers (target filenames)

After running the download script you should end up with:

```
articles/
├── abah2025.pdf          — Abah JC et al., Nigerian pollination review
├── avadi2023.pdf         — Avadí A et al., Ecuador cocoa LCA
├── bisseleua2013.pdf     — Bisseleua DHB et al., Cameroon 20-agroforest study
├── jagoret2017.pdf       — Jagoret P et al., Cameroon 48-agroforest study
├── kongor2024.pdf        — Kongor JE et al., cocoa-challenges review
├── saj2015.pdf           — Saj S et al., Cameroon poster abstract
├── schneider2010.pdf     — Schneider M et al., Bolivian FiBL long-term trial baseline
└── setyowati2025.pdf     — Setyowati N et al., Indonesian qualitative study
```

Excluded (kept in `articles/excluded/` in the original run):

```
articles/excluded/
├── bernet2019_palm_oil.pdf
├── kamath2024_biodiversity_at_risk.pdf
├── kouassi2023_adoption_only.pdf
└── rwigema2021_tea_coffee.pdf
```

DOIs and OpenAlex IDs are in `../openalex_works.jsonl`.
