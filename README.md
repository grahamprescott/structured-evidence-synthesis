# Structured AI-Assisted Evidence Synthesis (SAES)

**Version 0.1.1 — proof of concept.** A protocol, ontology, and extraction schema for AI-assisted evidence synthesis from scientific literature, with a paired audit step.

## The problem

Scientific knowledge accumulates only when prior work is synthesised. Unstructured literature reviews—whether produced by humans or by LLMs—are difficult to replicate and hard to evaluate. Without a defined extraction schema and ontology, outputs cannot be compared across users, sessions, or studies.

LLMs are highly capable at rapidly summarising information, but applying them to evidence synthesis without structure carries the same epistemic risks as unstructured human reviews.

This repository is an attempt to address that: a protocol that aims to make AI-assisted synthesis structured, transparent, auditable, and reproducible. The current release is a proof of concept, run end-to-end on a single paper.

## The workflow

The protocol has two steps:

1. **Extract.** An LLM reads a paper and codes every claimed relationship between variables against a pre-defined schema. Every coded field is paired with the verbatim text it was derived from.
2. **Audit.** A second LLM pass reviews the extraction against the schema and (optionally) the source paper, producing an audit report covering flag review, controlled vocabulary consistency, raw-to-code alignment, relationship completeness, and schema compliance. It also produces recommendations for revising the ontology itself.

The audit step is the part most missing from current LLM-based synthesis tooling. It separates *generating an extraction* from *evaluating an extraction*, which is the standard division of labour in human evidence synthesis (extractor and second reviewer) and which the design of the protocol depends on.

## What's here

- **`Ontology_specification.txt`** — full ontology and schema documentation
- **`Schema_for_ontology.csv`** — 34-field extraction schema with column definitions and controlled vocabularies, organised into eight groups (paper metadata, two variables, relationship, effect size, epistemic source, method, scope)
- **`Extraction_prompt.txt`** — generic LLM prompt template for the extraction step
- **`Extraction_prompt_Asner2016.txt`** — the extraction prompt configured for the worked example
- **`Audit_prompt.txt`** — generic LLM prompt template for the audit step
- **`Asner2016_extraction.csv`** — completed extraction against the worked example
- **`Asner2016_audit_report.txt`** — completed audit report on that extraction
- **`Asner2016.pdf`** — source paper for the worked example (Asner & Tupayachi 2017, *Environmental Research Letters*, on gold mining and forest loss in the Peruvian Amazon)

## Core design principles

**Variables and relationships as the unit of extraction.** Most synthesis questions reduce to: does a relationship between two variables exist, what is its direction, and what is its magnitude? The schema is built around extracting one directional relationship per row.

**Dual-layer architecture.** Every coded field is paired with the verbatim text it was derived from. This is the primary mechanism for transparency and auditability—a reviewer can always see what the LLM was looking at when it made a coding decision.

**PECO-style entity classification.** Variables are classified by role (Exposure / Intervention / Outcome / Context / Population) and by thematic domain (Environmental / Social / Economic / Governance), applied independently per relationship.

**Source and method as orthogonal axes.** Whether a claim is original to the paper or cited from elsewhere is recorded separately from how the claim was generated (observation, experiment, statistical modelling, simulation, review, expert elicitation). These should not be conflated.

**Three configurable scopes.** Users can specify target verbs, provide examples and prefer false negatives over false positives, or extract all relational language and filter afterwards.

## Worked example

The Asner & Tupayachi (2017) paper on gold mining in the Peruvian Amazon was chosen as the first worked example because it sits in a domain I know well (artisanal and small-scale gold mining) and because it makes a mix of original and cited causal claims, allowing the source/method distinction to be tested.

The full protocol—extraction followed by audit—has been run end-to-end. The extraction produced 30 relationships; the audit identified ~27 issues, ranging from minor coding inconsistencies to substantive ontology gaps. The audit report is included in full as `Asner2016_audit_report.txt`.

## What I tried and what broke

v0.1.1 has been run end-to-end on one paper and audited. The findings split into two groups, scoped to two different releases.

**Going into v0.1.2 — vocabulary and convention fixes:**

1. Resolve the schema field-count discrepancy. The extraction prompt instructs the LLM to populate "all 35 fields" but the schema CSV enumerates 34. The most plausible missing field is a `temporal_scope_code` paralleling `geographic_scope_code` (the schema currently has a raw temporal field with no paired controlled-vocabulary code).
2. Standardise the schema typo: `v1_entity_type` permits `Populations` (plural) while `v2_entity_type` permits `Population` (singular). Standardise on `Population`.
3. Tighten the `rel_conditionality_code` definition to distinguish genuine conditionality (e.g. "only during the dry season") from study scope (the time and place the study covered). The extraction systematically conflated the two: rows where `rel_conditionality_raw` was "Not reported" still received `Temporal` or `Spatial` codes because the extractor reached for the geographic/temporal scope of the study.
4. Tighten the `rel_uncertainty_code` definition to clarify that it captures *authorial hedging language*, not the structural complexity of the causal pathway. The extraction downgraded `Asserted` to `Probable` in places where the assertion was unhedged but described as one of multiple causes—that's not what the field is for.
5. Add a coding rule that `v1_code`/`v2_code` should be geographically neutral. The current extraction embeds geographic scope directly into the code (e.g. "Forest loss in Tambopata National Reserve" vs "Forest loss"). Spatial qualification belongs in the `geographic_scope_*` fields. This will materially improve cross-paper aggregability of any code vocabulary built up over time.
6. Add a "Reported without citation" or equivalent value to `source_locus`. The current options (`Original to this study`, `Cited from prior work`, `Synthesised from multiple sources`) do not handle uncited authorial assertions, and the extractor used `Synthesised from multiple sources` to fill the gap—overstating the evidentiary basis.

**Going into v0.2 — schema extensions:**

7. Resolve how `rel_valence` interacts with `rel_exists=No`. When the paper claims a relationship does *not* hold (e.g. "mining continued despite government decrees"), `rel_valence` is undefined but the schema currently forces a value. This produced a row where `effect_magnitude=40` reads like a positive intervention effect but actually quantifies the *failure* of the intervention. Either add `Not applicable` as a permitted value for `rel_valence` when `rel_exists=No`, or add a controlled-vocabulary field to flag asserted absences/failures distinct from asserted relationships.
8. Add a `Not reported / Unknown` value to `method_type` and `causal_inference_level`. Cited claims often arrive without information about the original method; the current schema forces the extractor to either invent a value or default to `Review`, which conflates synthesis with primary methodology.
9. Add `population_code` value(s) for purely economic systems. Relationships between economic variables (e.g. global recession → gold price) have no natural fit in the current `Human / Freshwater ecosystem / Terrestrial ecosystem / Mixed` vocabulary.
10. Support mediated and chained relationships via a `mediator_code` field or parent-row linking. Several relationships in the worked example involve clear mediating mechanisms (mercury mediating between mining and health; enforcement action → temporary reduction → rebound) that the current flat schema cannot represent. This is required for the longer-term aim of causal-network synthesis.
11. Tighten the decomposition rule for compound claims. The worked example contains an abstract sentence ("Gold mining... poses a major threat to biodiversity, water quality, forest carbon stocks, and human health") that the extractor decomposed into four pairwise rows, but other compound claims with similar structure were left as single rows with multi-domain V2s. The decomposition policy needs to be written into the prompt explicitly.

**Beyond the audit findings:**

- **No ground-truth benchmarking yet.** Extraction quality has not been compared against human coders working from the same prompt. Building a hand-coded gold-standard dataset and reporting inter-rater reliability is the priority for v0.3.
- **One worked example.** Generalisation across paper types, disciplines, and writing styles is unvalidated. A second extraction against a methodologically different paper (ideally one with substantial quantitative effect-size reporting, where the worked example has only one inferential statistic) is a near-term priority.
- **Controlled vocabularies for `v1_code` / `v2_code` are not yet populated.** Current extractions produce ad hoc codes derived by the LLM from each paper. A domain-specific vocabulary for biodiversity and nature-related risk applications is needed before extractions can be aggregated across papers.
- **Flag conventions are not enforced.** The extraction prompt instructs the LLM to mark uncertain entries with `[FLAG]` or `[UNVERIFIED]` tags inline. The completed extraction contained no such tags, despite the extractor noting several judgement calls in chat narrative. Inline flagging needs prompt-level reinforcement, or it will be skipped at scale.

## Roadmap

- **v0.1.2:** vocabulary and convention fixes from the audit (findings 1–6) and comparison with human-coded extraction. 


## Citation and contact

@software{prescott_saes_2026,
  author  = {Prescott, Graham},
  title   = {Structured AI-Assisted Evidence Synthesis (SAES)},
  version = {0.1.1},
  year    = {2026},
  url     = {https://github.com/<user>/<repo>}
}
Graham Prescott · graham.prescott@gmail.com · [grahamprescott.substack.com](https://grahamprescott.substack.com/)

If you use or build on this protocol, please cite the repository and get in touch. I'd particularly like to hear from anyone interested in benchmarking extraction quality or in domain-specific schema extensions.
