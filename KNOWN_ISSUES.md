# Known issues — v0.2.1-alpha (audit of 11 September 2026)

Before submitting this protocol for external review I ran an adversarial audit of every worked example: recomputing all consolidation counts from the extracted rows, resolving every DOI, and checking quoted spans against open-access source text. This file records what it found. Items are open until struck through here and in CHANGELOG.

## Holds up
- Extraction quoting, where it could be checked against source text: 15 of 16 sampled `rel_raw` spans are verbatim (cocoa: Bisseleua 2013, Jagoret 2017; gold-mining: Asner & Tupayachi 2017). Only the cocoa rows are LLM-extracted (11 of 12 verbatim); the gold-mining rows are migrated human coding, and the VBAC rows could not be checked because their DOIs do not resolve (item 4).
- `paper_section` is populated in the fresh-extraction examples.
- The cocoa and gold-mining consolidations recompute exactly from their row-sets (31/31 and 43/43 edges; provenance resolves). VBAC does not (item 2).
- The row schema generalised across three domains without field changes.

## Does not hold up
1. **No LLM-vs-human comparison exists.** The gold-mining example is a migration of a prior *human* coding into the schema, not a comparison against LLM extraction. Earlier wording ("benchmarked against human coding") was wrong and has been removed. No agreement figure exists for any stage.
2. **VBAC consolidation does not reconcile with its rows.** 63 distinct edges exist in `extracted_rows.csv`; `consolidated_edges.json` has 27. Ten of the 26 overlapping edges have wrong `n_rows` or valence tallies (e.g. `parity → vbac_success` hides a Negative row; the sign of the `inter_delivery_interval` disagreement is inverted). One edge, `uterine_scar_thickness → uterine_rupture`, appears in no row. 41 of 111 provenance IDs are not real row references. The consolidation was evidently generated from the model's reading of the papers rather than from the row-set — the failure this protocol exists to prevent. The VBAC DAG, disagreement report and REPORT are preliminary and should not be cited.
3. **"Verbatim" quotes in disagreement reports are not always verbatim.** Gold-mining: 4 of 5 blockquotes do not match any `rel_raw`. VBAC: 9 of 29 have appended statistics not present in the row. One extracted effect size (`bisseleua2013:r8`, "y=2223.6-2.8x") does not appear in the source paper.
4. **VBAC corpus identifiers are unreliable.** None of the 13 listed DOIs resolves to the intended paper; `knight2013` is Knight et al., BJOG 2014 (10.1111/1471-0528.12508); `girma2021` could not be identified and may be misattributed.
5. **Setup was not run per its own schemas.** In the cocoa example, 36 of 48 hits were excluded by PDF availability, not by screening; the REPORT previously said otherwise. No `screening_decisions.csv` exists.
6. **Audits ran in the same session as extraction**, contrary to `extraction/prompts/audit.md`; audit Task 4 (completeness) was skipped in all three examples. The same-session audit passed a non-enum `population_code` on 60 rows and missed item 2.
7. **Counts in docs were wrong** (`docs/v0.2_trials_summary.md`, `examples/vbac/README.md`, `examples/vbac/results/audits/audit_report.md`): VBAC has 153 extracted rows (docs say ~170); 8 controlled-comparison rows (docs say 0); 9 trend-only rows (docs say 6). The "~80% numeric effect sizes" claim depends on definition: 63% of rows carry a bare number in `effect_magnitude`, 76% carry some numeric value (including percentages and ranges).
8. Vocabulary for VBAC was seeded from a model answer to the research question, so the extraction target list carries the model's prior.
9. Schema/output mismatches: extra properties on consolidated edges; effect-size summaries populated below the n≥3 rule; no `row_id`, so provenance is positional.

## Fix plan
- [x] `validate.py`: schema-check every CSV and recompute edge counts from rows (target: 14 Sept)
- [ ] Regenerate VBAC consolidation from rows, audit in a separate session/model
- [ ] Correct VBAC DOIs; identify or drop `girma2021`
- [ ] Add `screening_decisions.csv` for cocoa; fix REPORT wording
- [ ] Log model, date and prompt hash per run
- [ ] Benchmark extraction against human coders (Evidence Inference, one Cochrane review, one CEE review) — the v0.3 milestone
