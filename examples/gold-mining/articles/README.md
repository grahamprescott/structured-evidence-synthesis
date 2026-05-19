# Gold-mining corpus — articles

PDFs are not included in this repository. This corpus was inherited from a 2022 Scopus-based literature search; the original search workbook, screening decisions, and manual coding workbook are also held outside the repo (see [`../context/prior_work_translation.md`](../context/prior_work_translation.md)).

## Included papers (target filenames)

```
articles/
├── asner2016.pdf            — Asner GP, Tupayachi R. Environ Res Lett 2017;12:094004
├── castilhos2006.pdf        — Castilhos ZC et al. Sci Total Environ 2006;368:320-325
├── fearnside2001.pdf        — Fearnside PM. Environ Conserv 2001;28:23-38
├── lacher1997.pdf           — Lacher TE Jr, Goldstein MI. Environ Toxicol Chem 1997;16:100-111
├── regine2006.pdf           — Régine MB et al. Sci Total Environ 2006;368:262-270
├── schwartzmann2005.pdf     — Schwartzman S, Zimmerman B. Conserv Biol 2005;19:721-727
├── soderquist2000.pdf       — Soderquist TR, Mac Nally R. Biol Conserv 2000;93:281-291
└── tarras-wahlberg2001.pdf  — Tarras-Wahlberg NH et al. Sci Total Environ 2001;278:239-261
```

DOIs:

- Asner 2017: 10.1088/1748-9326/aa7dab (open access — IOP gold)
- Castilhos 2006: 10.1016/j.scitotenv.2006.01.039
- Fearnside 2001: 10.1017/S0376892901000030
- Lacher 1997: 10.1897/1551-5028(1997)016<0100:TESAN>2.3.CO;2
- Régine 2006: 10.1016/j.scitotenv.2005.09.077
- Schwartzman 2005: 10.1111/j.1523-1739.2005.00695.x
- Soderquist 2000: 10.1016/S0006-3207(99)00153-6
- Tarras-Wahlberg 2001: 10.1016/S0048-9697(01)00655-6

Of the 8, only Asner 2017 is unambiguously open access. The others are paywalled and should be obtained through institutional subscription or interlibrary loan.

## A note on the 2022 prior coding workbook

Most of this trial's output is *not* a fresh-from-PDF extraction. It is a programmatic migration of a 2022 manual coding workbook (143 gold-related rows) into the v0.2 schema. The workbook itself is held outside the repo. See [`../context/prior_work_translation.md`](../context/prior_work_translation.md) for the column mapping.

A v0.2 native re-extraction from the PDFs is recommended as the next iteration; the migration captured no numeric effect sizes.
