---
type: is
id: is-01m5nj7kqy546szevazpsvfckw
title: "Deep gate: the four whole fine-net sweeps put deferred-slow-lane over its 1250 s ceiling (1477 s); re-record, split or speed the evaluator"
kind: task
status: open
priority: 1
version: 3
labels:
  - decision
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T23:41:11.291Z
updated_at: 2026-10-23T23:41:39.107Z
---
Owner or coordinator decision, raised by A2 of PR #745's review A (https://github.com/jlevy/squares/pull/745#issuecomment-6372288301) and escalated by lane c-fix-745-1023 on 23 October.

The four whole fine-net census sweeps (`test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness` at mixed_n19_L48275, mixed_n20_L49125, mixed_n27_L5655 and mixed_n31_L59775, `packing/tests/test_sqverify_fast_census.py`) run under `slow` in the deep surface. On deep-gate dispatch 40033801674 at b39bd7cec:
- `deferred-slow-lane` job wall was 1477 s (step 1418.5 s at `-n 4`), against its 1250 s ceiling (`packing/devtools/gate-budgets.yaml`, recorded 921.7 s).
- Hosted call: n27 338.92 s, n19 256.43 s, n20 200.55 s, n31 157.35 s; 953.3 s in all.
- The lane's phase total was 4,980 s (1,245 s ideal at four workers). Without the four it is about 1,007 s ideal, about 1,180 s real on that runner class.
- So the four add about 240 s of wall however they are balanced. The slow lane becomes the deep gate's longest job, ahead of exhaustive-3 at about 1,074 s; the gate's own record is 1,133 s.
- They also run in packing-validation.yml's post-merge `slow-lane` job.

Profile (20 n27 refusals): `mixed_exact` in `packing/devtools/check_sqverify_fast.py` takes 5.03 s. Of that, `sqpack.rectangle_density.exact_intersection_area` is 3.20 s, about 700 exact clippings per direction behind a fixed ±0.71 float box. `mixed_rows` and `orbit_images`, rebuilt on every call, are 0.87 s.

Options:
- (a) Re-record `deferred-slow-lane` (and the post-merge lane) in gate-budgets.yaml with attribution to the four nodes, keeping earlier readings (OR-14). The ceiling rises to about 1,700 s, and every deep-gate run gets about 6 minutes longer on the slower runner class.
- (b) Split the four into a deep-gate job of their own: a marker or step in `packing/src/sqpack/cli/validate.py` (`SLOW_TESTS` and its complement rule), `.github/workflows/deep-gate.yml` and packing-validation.yml, `ci_gates` entries, development.md's Validation Loops, and the workflow contract tests. The gate's wall stays where it is.
- (c) Make the evaluator cheaper: a per-direction float prefilter that clips only boundary-crossing images and counts wholly inside images exactly, plus a per-candidate cache. That needs about 3.4x to fit 1250 s again, and it is a reviewed change to the evaluator that judges control receipts (result-import.md stage 4).

Never skip or sample away the whole sweeps (OR-13; review A's "Sampling is not skipping").

Done when one option is chosen and landed, and a deep-gate run reads `deferred-slow-lane` inside its declared ceiling, or over it with the selection recorded.
