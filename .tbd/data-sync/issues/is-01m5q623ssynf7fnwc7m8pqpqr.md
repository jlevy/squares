---
type: is
id: is-01m5q623ssynf7fnwc7m8pqpqr
title: "OR-1: move the pose-by-pose identity measurement and the sharp controls into devtools"
kind: task
status: in_progress
priority: 3
version: 5
delegate: c-or1-jv2s-1024
labels:
  - tooling
  - packing
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T14:46:57.081Z
updated_at: 2026-10-24T18:55:34.686Z
started_at: 2026-10-24T16:05:09.620Z
---
Five upper-bound packets now carry their own copy of the same two measurements: measure/identity.py (evand-regularized-2026-10-20 holds the measures; mishapolk-n204-2026-10-22, amundsk-n303-2026-10-23 and evand-kaggle-descents-2026-10-24 load them by file path, and the T-240 review wrote a clean-room one) and receipts/sharp_controls.py (mishapolk-n204-2026-10-22, amundsk-n303-2026-10-23/replay, and evand-kaggle-descents-2026-10-24, which takes --packet and --n). OR-1: build the tool once.

Done looks like: devtools.measure_identity (nearest centre under the eight symmetries via check_half_angle_area.arrangement_gap, plus the optimal assignment, over packets read through upper_bound_reports.read_facts and binary64 x-y-degrees inputs) and a sharp-controls subcommand of devtools.upper_bound_reports writing receipts/sharp-controls[-nNNN].json, each with tests; the retained per-packet programs stay as written (their receipts are bound to them), and later packets call the tools. The triage of think-6r5p proposed the same (devtools.measure_identity).

## Notes

2026-10-24, c-or1-jv2s-1024 (moderate tier): draft PR #796 (https://github.com/jlevy/squares/pull/796), branch claude/or1-2026-10-24-identity-and-sharp-controls, head 2251afe0f (main 3480b5fd3, #792, merged in), hosted CI green (31 passed, 28 skipped).
- devtools.measure_identity: specs packet:NAME, any upper_bound_reports adapter FORMAT:PATH, binary64-xyd:PATH; measures nearest_centre (arrangement_gap), assignment (Hungarian), tilts, bands, centred (T-240's box-centred variant). Reproduces amundsk-n303 #755 vs T-230 and evand-regularized 204/229 receipts key for key; centred block reproduces T-240's T230 vs T239 primary figures.
- upper_bound_reports PACKET sharp-controls [--n N] [--check] (devtools.upper_bound_sharp_controls): 11 rows (box at/below extent, tightest pair, near wall, enlarged pair, enlarged wall, duplicate); reproduces mishapolk-n204's retained receipt route for route (slow test, 134 s) and evand-kaggle-descents n268 the same way (scratch run, 223 s); refuses to overwrite another program's receipt.
- result-import.md stage 4 paragraph; release.py ReleaseNoPublicChange (four papers, 69 files byte-identical across four renders); slow-marker registry entry.
- Open: no packet converted to the tools (by design); local whole-repo basedpyright timed out under load and the browser floor cannot run in this worktree (stale shared node_modules lacks typescript-eslint); hosted CI is the gate.
- CI flake seen: wait_for_run_artifact treats GitHub HTTP 502 on the artifact join as fatal; four reruns at 803603eb8.
2026-10-24, review A round 1 (approve with changes, https://github.com/jlevy/squares/pull/796#issuecomment-6387891436): A1-A8 all fixed in 72f969cd0; main dd0061553 (#793) merged in 4147f3f96; release record re-measured at link revision dd006155 (451b39b3b). The reviewer's 12 mutants, run through his plugin, are all killed. Added tests for all five amundsk-n303 pairs and evand-regularized 227/260. Validation: 98 passed (two test files plus module boundaries, slow included); records tier 53/53. Dispositions reply: https://github.com/jlevy/squares/pull/796#issuecomment-6388074486. Hosted CI at 451b39b3b: one frontend rerun after a pytest-xdist worker crash in test_site_homepage (unrelated to the change).
