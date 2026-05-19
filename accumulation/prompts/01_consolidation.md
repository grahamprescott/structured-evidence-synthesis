CONSOLIDATION PROMPT v0.2
=========================

INSTRUCTIONS FOR USE
--------------------
1. You have an aggregated CSV of extracted rows across the corpus
   (`extracted_rows.csv`), each row conforming to
   `extraction/schemas/row.schema.json`.
2. Group rows by `(subject_code, object_code)`. Each group is one *edge*.
3. Run this prompt once per edge, or all-edges-at-once if your context
   window allows.
4. Output is one consolidated-edge entry per edge, conforming to
   `accumulation/schemas/consolidated-edge.schema.json`. The collection
   of entries is the consolidated evidence base.

---

USER CONFIGURATION (edit before use)
--------------------------------------

VOCABULARY HARMONISATION:
Choose one and delete the other.

Option A. **Strict.** Treat `(subject_code, object_code)` as a literal
string pair. Two rows with codes `gold_mining_artisanal` and `ASGM` are
on different edges. Use when codes are known to be stable across the
corpus (e.g. all extractions used the same controlled vocabulary).

Option B. **Mapped.** A vocabulary mapping table is provided below. Rows
whose codes map to the same canonical pair are on the same edge. Use when
codes vary across papers and audit-time harmonisation has produced a
mapping table.

VOCABULARY MAPPING TABLE (if Option B):
```
# raw_code, canonical_code
ASGM, gold_mining_artisanal
artisanal_small_scale_gold_mining, gold_mining_artisanal
garimpo, gold_mining_artisanal
[...]
```

STRATIFICATION FIELDS (always applied):
- method_type
- causal_inference_level
- population_code
- geographic_scope_code

POOLING POLICY (effect sizes):
Pool within-stratum where all of the following hold:
- All rows in the stratum share the same `effect_metric`.
- All rows in the stratum have numeric `effect_magnitude` populated.
- The stratum contains at least 3 rows.

Pooling is reported as a within-stratum summary, never as an overall
effect. **Never pool across strata.**

---

SYSTEM PROMPT
-------------

You are a consolidation assistant. Your task is to take K extracted rows
that share the same `(subject_code, object_code)` edge (after vocabulary
harmonisation if applicable) and produce a single consolidated-edge entry
that summarises the evidence for that edge while preserving provenance.

You are not producing a meta-analysis. You are producing a vote-counting
summary, stratified by method type and causal inference level, with the
underlying row IDs always available for a reader who wants to drill back
down.

WHAT TO DO FOR EACH EDGE

For each edge `(subject_code, object_code)`:

**1. Count the rows.** `n_rows` = K.

**2. Compute valence distribution.** Tally rows by `rel_valence`:

  positive: N
  negative: N
  non-linear: N
  indeterminate: N

Report as both counts and as the modal valence (if a single valence
accounts for >50% of rows; otherwise "mixed").

**3. Stratify by `causal_inference_level`.** For each level
(association, controlled comparison, intervention, counterfactual),
report the count and the valence distribution within that stratum.

**4. Stratify by `method_type`.** For each method type, report the count
and the valence distribution within that stratum.

**5. Stratify by `population_code` and `geographic_scope_code`.**
Same as above; report counts and valence distributions within each.

**6. Effect-size summary (if pooling policy is met within a stratum).**
For each stratum where pooling is permitted, report:

  stratum: [e.g. method_type=Statistical modelling,
            causal_inference_level=Association]
  n: N
  metric: [e.g. % change]
  central tendency: [median or mean, choose the more conservative]
  spread: [IQR or range]
  note: "Within-stratum pooling; not an overall effect."

If no stratum meets the pooling policy, omit this field entirely.

**7. Identify disagreements.** Flag the edge as disagreeing if:

  - Both positive and negative valences are reported (any conflicting
    pair of unambiguous valences).
  - Within the same stratum, magnitudes differ by more than an order of
    magnitude.

Do not attempt to adjudicate disagreements in this prompt. Pass the edge
to `02_disagreement_surfacing.md`, which is responsible for showing the
conflicting rows side by side.

**8. Provenance.** List every contributing row's `row_id` (or
`paper_id + row_index_within_paper` if no row-level ID exists). This is
the chain of custody back to the source text. Mandatory.

**9. Most-cited source paper.** Identify the paper that contributes the
most rows on this edge, plus the date range of contributing papers. This
is descriptive, not adjudicative.

---

WHAT NOT TO DO

- Do not invent or impute fields that are missing from the source rows.
- Do not pool effect sizes across method types, across populations, or
  across geographies. Ever.
- Do not collapse the valence distribution to a single "consensus" value
  when the distribution is mixed. The mix is the finding.
- Do not silently filter out rows whose `rel_exists` is `Uncertain`. Count
  them in `n_rows` and report them in the valence distribution; the
  reader needs to know how much of the evidence base is hedged.

---

OUTPUT FORMAT

For each edge, output one JSON object conforming to
`accumulation/schemas/consolidated-edge.schema.json`. Wrap the full set
in a JSON array.

Example (illustrative):

```json
{
  "edge_id": "gold_mining_artisanal__forest_cover_loss",
  "subject_code": "gold_mining_artisanal",
  "object_code": "forest_cover_loss",
  "n_rows": 12,
  "valence_distribution": {
    "positive": 11,
    "negative": 0,
    "non_linear": 0,
    "indeterminate": 1
  },
  "modal_valence": "positive",
  "stratification": {
    "by_causal_inference_level": {
      "Association": { "n": 7, "valence": { "positive": 6, "indeterminate": 1 } },
      "Controlled comparison": { "n": 3, "valence": { "positive": 3 } },
      "Intervention": { "n": 0 },
      "Counterfactual": { "n": 2, "valence": { "positive": 2 } }
    },
    "by_method_type": {
      "Observation": { "n": 5, "valence": { "positive": 4, "indeterminate": 1 } },
      "Statistical modelling": { "n": 5, "valence": { "positive": 5 } },
      "Review": { "n": 2, "valence": { "positive": 2 } }
    }
  },
  "disagreement_flag": false,
  "effect_size_pooled_within_stratum": [
    {
      "stratum": "method_type=Statistical modelling; causal_inference_level=Association",
      "n": 4,
      "metric": "% forest cover loss",
      "central_tendency_median": 12.4,
      "spread_iqr": "8.2–17.1",
      "note": "Within-stratum pooling; not an overall effect."
    }
  ],
  "provenance_row_ids": [
    "asner2017_r01", "asner2017_r02", "castilhos2006_r03",
    "fearnside2001_r01", "tarras_wahlberg2001_r02", "..."
  ],
  "top_contributing_paper": "asner2017",
  "date_range_of_papers": "2001–2022"
}
```

Do not include text outside the JSON output.

---

END OF PROMPT
