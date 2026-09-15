---
type: is
id: is-01m2gxxnjp4wp3zxzc759d9yxm
title: Display and export paths still show a side for unchecked arrangements
kind: bug
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:10.769Z
updated_at: 2026-09-15T03:33:22.115Z
---
The owner asked that no code still reports a run's arrangement without checking that it is a packing. The benchmark's ranking paths are fixed on PR #160, with tests (`test_sweep_cannot_rank_an_invalid_high_score`, `test_nonfinite_ranked_values_are_refused`). The 2026-09-14 audit found display and export paths that still show a side or excess for an unchecked state, on both BASE and #160:

- `workbench_tools/ascent.py:110-122` records `fair_side` and `excess_pct` from the settled phase with no geometry check, prints them (`:239-244`) and stores them in the animation document.
- `workbench_tools/strategy_execution.py:566` prints "reached side (excess %)" without validity; only `--json` carries `packing_valid`.
- The page optimiser's `growth().packing` is true at soft penetration up to `OPT.feasible` = 0.008 (BASE `workbench.js:4151`, verified), and `#grow-info` shows the side against the record with no validity.
- The gap bar's `valid` is the SUMMED overlap at most 1e-4 (BASE `workbench.js:3827`, verified), so a single pair overlapping by 9e-5 counts as valid, and `gapBar()` computes and exports `met`, `excess` and `side` whatever `valid` says; only the hand is hidden.
- The Pack panel prints "required side" for invalid states, labelled "not a valid packing" (`pack-panel.ts:162-177`).
- `historical_summary_audit.py:29-87` re-exports `closed_median`, excess and best-of prefixes for `resolved: false` cells, labelled but not filtered.

Fix: every one either requires the shared validity check first or labels the value as unchecked in the same field it prints. The gap bar moves to the deepest-pair rule under think-nals. Each fix carries a negative test with an overlapping arrangement.

## Notes

2026-09-14, PR #160 review lane D-tools (D61, bead think-qajp, closed at e90187c8): the tool paths are fixed. The ascent's `FairReach` carries `packing_valid` with a null side and excess when the settle fails the unit-square check (Python record, schema, browser decoder), and `ascent` and `strategy_execution` print "not a packing" instead of a side. The page paths (D11) and benchmark exports (D42) remain with lanes D-page and C.

2026-09-14, PR #160 review lane C (D42, #160 R12 audit item; #155 R22 Trial.row item), 6e0e7ffc: `historical_summary_audit` marks the 243 unresolved cells `void` and exports no metric for them; a written trial row carries `raw_valid` and `resolved_valid`. The page and Pack items are D11 (lane D-page); the ascent and strategy tool items are D61 (lane D-tools).

2026-09-14, lane D-page (PR #160 review D11): the page items are fixed on codex/review-workbench-stack in c0d9db2b. The gap bar assesses the drawn squares with PACKING_VALIDITY (assessCataloguePrecisionFrame, labelled `precision: catalogue-precision`, only where the frame draws a retained record as stored), measures at the drawn size, requires validity for `met` and reports `excess` only for a packing; growth().packing, the growth readout and optimizeState().excess follow the run's contract assessment; the Pack status and stage facts are worded from the assessment ("bounding side", "Not a packing: <clause>"); PackController.state() refuses a half-size import through the unit-size clause (Node test). Negative checks: check_animate_view `readouts_claim_only_packings` (5e-9 overlap, half size) and check_pack_panel (half-size and 5e-9 imports). The benchmark-side export items (D42, lane C) and the tool items (D61, lane D-tools) are not part of this note.
