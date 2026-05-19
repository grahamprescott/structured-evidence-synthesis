# Screening decisions

The corpus for this v0.2 run is **inherited from a 2022 Scopus search** (see `prior work gold mining/All searches 2022-08-29.xlsx` and `Articles selected.xlsx`) rather than freshly downloaded from OpenAlex. The 2022 screening filtered the broader Scopus return set down to "top-cited articles" and "top-cited reviews" plus author-selected papers.

## Included (8 papers, 143 prior-coded rows)

| paper_id | citation | type | location | rows (2022) | reason |
|---|---|---|---|---|---|
| asner2016 | Asner GP, Tupayachi R. *Environ Res Lett* 2017;12:094004 | Article (remote sensing + modelling) | Peru / Madre de Dios | 24 | Top-cited; primary on gold-mining-driven forest loss in protected areas |
| castilhos2006 | Castilhos ZC et al. *Sci Total Environ* 2006;368:320-325 | Article (observational sampling) | Indonesia / N Sulawesi | 26 | Top-cited; primary on mercury in fish near ASGM sites |
| fearnside2001 | Fearnside PM. *Environ Conserv* 2001;28:23-38 | Article (review/synthesis) | Brazilian Amazon | 10 | Top-cited; mentions gold mining as driver alongside soy; indirect-pathway coverage |
| lacher1997 | Lacher TE Jr, Goldstein MI. *Environ Toxicol Chem* 1997;16:100-111 | Review | Tropics (pan) | 10 | Top-cited; tropical ecotoxicology including ASGM mercury |
| regine2006 | Régine MB et al. *Sci Total Environ* 2006;368:262-270 | Article (observational sampling) | France / French Guiana / Maroni River | 4 | Top-cited; primary on mercury bioaccumulation in 12 fish species |
| schwartzmann2005 | Schwartzman S, Zimmerman B. *Conserv Biol* 2005;19:721-727 | Review | Brazil / Kayapó / Xingu | 13 | Top-cited; indigenous land rights as a barrier to mining and other land-use change |
| soderquist2000 | Soderquist TR, Mac Nally R. *Biol Conserv* 2000;93:281-291 | Article (observational, mammal trapping) | Australia / box-ironbark | 6 | Top-cited; legacy of mining-driven forest fragmentation on small mammal communities |
| tarras-wahlberg2001 | Tarras-Wahlberg NH et al. *Sci Total Environ* 2001;278:239-261 | Article (observational, river sampling) | Ecuador / Puyango basin | 27 | Top-cited; primary on ASGM-driven river metal contamination |

## Excluded from this run

The following are present in the prior-work folder but **excluded** for this v0.2 run:

| File | Reason |
|---|---|
| Chivian2008.pdf | "Sustaining Life" book chapter; broad biodiversity-health volume; not in 2022 coding workbook. |
| Lin2006.pdf | Not in 2022 coding; topic unclear from prior-work metadata. |
| Monjezi2009.pdf | Not in 2022 coding; appears to be a mining engineering paper, not biodiversity-focused. |
| Rawlings2003.pdf | Not in 2022 coding; topic unclear. |
| VanDover2011.pdf | Not in 2022 coding; deep-sea mining context, off-axis for this question. |

Two further entries appear in the 2022 workbook but are excluded here:

| paper_id (workbook) | Reason |
|---|---|
| Festin_2019 (Africa post-mining restoration) | Only 1 row coded in the workbook; PDF not in folder. Insufficient evidence to include. |
| Prescott_2022 (the author's own paper) | Excluded to avoid circular dependency on the prior review. |

## Notes

- The 2022 Scopus search returned a much larger candidate set (`All searches 2022-08-29.xlsx`, ~hundreds of rows). The 8 included here are the "top-cited" cohort that the original author selected for coding. A fresh OpenAlex pass might add more recent (2022–2025) papers on Madre de Dios formalisation (Álvarez-Berríos et al. 2021 is in the candidate list but excluded here), Brazilian Yanomami invasion (2023–2024 literature), and mercury-Minamata-treaty implementation. Recommend expanding the corpus for a v0.2.1 run.
- The Schwartzman 2005 paper is **about indigenous conservation alliances** rather than gold mining per se. It is retained because the 2022 coding produced 13 indirect-pathway links involving indigenous land rights, road creation, and miner influx that are central to the question.
- The Soderquist 2000 paper is about Australian box-ironbark mammals in a **post-mining** landscape (historic gold rush); the link to ASGM-on-biodiversity is loose but the paper supplies cited evidence about persistence of mining legacy on biodiversity.
