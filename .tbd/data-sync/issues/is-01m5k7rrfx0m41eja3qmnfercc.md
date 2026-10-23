---
type: is
id: is-01m5k7rrfx0m41eja3qmnfercc
title: Records tier misses assess_frontier_rigidity --check, which an adoption can make stale (#731 went red in hosted validate after a green local records tier)
kind: bug
status: open
priority: 2
version: 2
labels:
  - validation
dependencies: []
created_at: 2026-10-23T01:59:50.013Z
updated_at: 2026-10-23T02:09:44.273Z
---
#731 adopted T-230 at 303 and passed packing-validate --records (52/52) locally, but hosted validate failed on 'frontier rigidity assessed here' (assess_frontier_rigidity --check: stale rigidity blocks for n = [303]), fixed by --update in 260a0cef0. A records change that moves a retained witness can stale a rigidity block, so the step belongs in the records tier (development.md validation tiers; OR-13). Add it, or make adopt_houses re-derive the block itself, with a test.

## Notes

2026-10-23 02:15Z coord-intake-1021b: the same chain then staled atlas/known-best/composite-figure.json (build_composite_figure_data --check, in hosted sweeps), fixed in e827907fe. So an adoption needs: adopt_houses, then assess_frontier_rigidity --update, then build_composite_figure_data --update. Either put both checks in the records tier or have the adoption tool run the derivations in order.
