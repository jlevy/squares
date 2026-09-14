---
type: is
id: is-01m2gyp18kcxq2g8gq7hjacg3n
title: Express the workbench physics and every guidance use in the PackingStrategy format
kind: feature
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gyp41nh48d2kc155rrvzy7
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
  - type: blocks
    target: is-01m2gxkp2c5hk981zhv3aejfga
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:55:29.169Z
updated_at: 2026-09-14T21:55:51.387Z
---
Owner, 2026-09-14: "Each of these approaches to stitching things together should be a sort of strategy that we keep track of when we map out the way that we optimize and what level of guidance is given during the optimization process. We could then have code that tries these different paths. Ideally, each of the strategies for packing would be expressible in our format and could then be evaluated across a loop to see how the different strategies compare for a given n or across different n."

"Our format" is the PackingStrategy document (`packing/strategies/packing-strategy.schema.yaml`): phases, each with a mechanism, a `structure` rung with `source` and a rewired or thinned `control`, `constraints` as bands, `until`, `side`, `schedule` and `target`. The Python executor (`devtools/packing_strategy.py`, `MECHANISMS`) runs the projection lane. **The workbench's physics cannot be written in it today**, so blind, free and snap runs, the shake dial, bodies-style blocks and the overlap-tolerant contraction all live outside the format.

Extend the format so every approach is a document:
- **Physics mechanisms**: `drop` (the coarse-grid proposal for the new square), `simulate` (contacts, walls, a shake schedule, and walls closing toward a side with a declared overlap tolerance), and `resolve` (repair to a packing). Blind, free and snap become documents; snap stays a `guide`, illustration only.
- **Guidance uses**: say where a rung acts, not just which rung: `start` (construct from it), `weld` (rigid blocks, with a release step), `attract` (range and aligning torque), `shake` (amplitude per body), plus the existing `constraints` bands.
- **New rungs**: `blocks` (the transition's matched blocks, which is today's bodies style), `touching-partition`, `merged-near-flush` with its tolerance, and `partial-poses`.
- **Implementation capabilities**: each executor declares the mechanisms and uses it supports, and a document runs only where every phase is supported. An unsupported document is refused before it runs (the shared-language plan's Phase 1 rule).
- **Derived guidance summary**: computed from the phases (the most informative rung any phase uses, and whether any phase guides onto the record), recorded with every run, printed with every result.
- **Catalogue link**: each document names its `frontier/search-strategies.yaml` entry (`search:N`), so results roll up by family and hypotheses reference them through `strategy_refs`.

Related: think-karf (executable strategy semantics), think-rey9 (extraction the rungs read).
