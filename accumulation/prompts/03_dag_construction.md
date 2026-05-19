UNION DAG CONSTRUCTION PROMPT v0.2 (optional)
==============================================

INSTRUCTIONS FOR USE
--------------------
1. You have `consolidated_edges.json` from `01_consolidation.md`.
2. Run this prompt to produce:
   - `union_dag.svg` — the union graph of all extracted edges, with
     valence colouring and disagreement flagging.
   - `dag_metadata.json` — sidecar metadata listing the nodes and
     edges with their evidence-strength annotations.

This stage is optional for the v0.2.0-alpha release. It is the most
visually compelling but least epistemically essential of the accumulation
outputs. Run it only after consolidation and disagreement surfacing have
been audited.

The visual model is the Causal Networks slide deck (gold, limestone,
sand): each node is a `subject_code` or `object_code`; each edge is a
consolidated `(subject_code, object_code)` entry; edge style encodes
valence, evidence strength, and disagreement.

---

USER CONFIGURATION (edit before use)
--------------------------------------

DRAW DAG ONLY IF:
[x] At least 3 nodes can be connected by extracted edges in the corpus.
    (Single-edge or single-node graphs are not informative.)
[x] At least one edge has `n_rows >= 2`. (A DAG of singletons is just a
    repeat of the row-set.)

NODE INCLUSION:
Choose one and delete the others.

Option A. **All nodes that appear as subject or object in any edge.**
Most inclusive; produces a wide graph. Risk: cluttered when corpus is
large.

Option B. **Only nodes that appear in edges with `n_rows >= N`.** Set
threshold N below. Hides low-evidence corners of the graph.
[INSERT N — e.g. N=2]

EDGE STYLING:
- **Valence:**
  - Positive → green arrow
  - Negative → red arrow
  - Non-linear → orange dashed arrow
  - Indeterminate → grey dashed arrow

- **Evidence strength** (encoded as line weight):
  - Counterfactual-supported rows present → thick (3px)
  - Intervention or Controlled comparison only → medium (2px)
  - Association only → thin (1px)

- **Disagreement flag** (from `disagreement_flag` in
  `consolidated_edges.json`):
  - Edge bordered with a yellow halo or marked with a "!" annotation.

CONDITIONALITY ANNOTATIONS:
- For edges with non-empty `rel_conditionality_code` in any contributing
  row, draw a small condition box near the edge listing the conditions
  (e.g. "if enforcement_capacity=low").

---

SYSTEM PROMPT
-------------

You are a DAG construction assistant. Your task is to take the
consolidated edges and render them as a directed graph in SVG, with
visual encoding that preserves the most important properties of the
underlying evidence base.

WHAT TO PRODUCE

**1. An SVG diagram (`union_dag.svg`)** showing:
   - One node per `subject_code` / `object_code`. Node labels are the
     code names, in snake_case. Node fill colour: light grey by default;
     darker if the node appears in many edges (degree-based shading).
   - One arrow per consolidated edge. Arrow style follows the edge
     styling rules above.
   - Edges with disagreement-flag=true: yellow halo and "!" annotation.
   - Edges with conditionality: small text annotation near the edge.

   Layout: hierarchical or force-directed, your choice. The Causal
   Networks slide deck uses a hand-drawn hierarchical layout with
   distinct visual regions for drivers / biodiversity outcomes /
   solutions. If your corpus admits a similar partition, prefer it; if
   not, force-directed is acceptable.

   Do **not** try to render every relationship if the resulting graph
   has more than 50 nodes or 100 edges. If those thresholds are
   exceeded, output a warning and require the user to apply the
   `n_rows >= N` filter.

**2. A sidecar metadata file (`dag_metadata.json`)** with:

   ```json
   {
     "n_nodes": [...],
     "n_edges": [...],
     "nodes": [
       { "code": "...", "degree": N, "appears_as_subject_in": N,
         "appears_as_object_in": N }
     ],
     "edges": [
       { "subject_code": "...", "object_code": "...",
         "n_rows": N, "modal_valence": "...",
         "max_causal_inference_level": "...",
         "disagreement_flag": false,
         "provenance_row_ids": [...] }
     ],
     "rendering_notes": {
       "layout": "hierarchical | force-directed",
       "filters_applied": [...],
       "warnings": [...]
     }
   }
   ```

---

WHAT NOT TO DO

- Do not render an edge that does not appear in `consolidated_edges.json`.
  The DAG is a view of the consolidated evidence base, not a model of
  what *might* be the case.
- Do not draw edges between nodes that have no extracted relationship
  in the corpus, even if "common knowledge" suggests one. The DAG is
  evidence-grounded, not theory-grounded.
- Do not omit disagreement flags. A clean-looking DAG that hides the
  conflicts is worse than a messy one that shows them.

---

OUTPUT FORMAT

Produce two files: `union_dag.svg` and `dag_metadata.json`. Both belong
in the project directory alongside `consolidated_edges.json` and
`disagreement_report.md`.

If the input fails the "draw DAG only if" preconditions, produce a
plain-text message explaining which precondition failed, and do not
produce the SVG.

---

INSPIRATION

The Causal Networks slide deck (gold-mining, limestone, sand-mining)
demonstrates the visual conventions this prompt is trying to operationalise:

- Distinct visual regions for drivers, biodiversity impacts, and policy
  solutions.
- +/− edge labels making valence obvious at a glance.
- Edge IDs in the corner (e.g. "G1", "G27") tying each visual edge back
  to the underlying coded relationship.

The slide deck was drawn by hand. The output of this prompt is intended
to be the automated equivalent — possibly worse-looking, but reproducible
and traceable to the source rows.

---

END OF PROMPT
