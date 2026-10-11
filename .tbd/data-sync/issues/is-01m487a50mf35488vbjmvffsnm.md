---
type: is
id: is-01m487a50mf35488vbjmvffsnm
title: "Stage-4 review of check_karakus_strip_measure (T-083, T-084, #295), then merge R6's staged exit"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-06T09:04:30.740Z
updated_at: 2026-10-06T17:02:05.871Z
started_at: 2026-10-06T11:00:14.339Z
closed_at: 2026-10-06T17:02:05.870Z
close_reason: "Done and on main via #382 (d087422ed); reply posted 2026-10-06 and recorded"
resolution: null
duplicate_of: null
---
Stage 4's review lane for the machine check of Karakuş's Proposition 5.1 (T-083, T-084, #295). Lane R6 could not run it: launching `claude -p` as the separately prompted reviewer was refused by its session's permission classifier ("Create Unsafe Agents"), so the replay lane is done and the exit is staged, not merged.

What exists (lane R6, branch claude/ecstatic-pascal-pothtx-r6, not pushed):
- d7f2c6186 on the lane branch: packing/devtools/check_karakus_strip_measure.py, packing/tests/test_karakus_strip_measure.py, and the receipt packing/campaign/series/series-000-smoke-and-calibration/results/karakus-strip-measure/receipt.json (5,939-leaf exact Fraction cover, depth 34, 4 corner leaves; 3 mutated measures refused with counterexamples).
- The staged exit on branch claude/ecstatic-pascal-pothtx-r6-exit: 28ffccc7c (E-karakus-strip-measure-interval, V-check-karakus-strip-measure, T-083 and T-084 to V3/C3, 203 case records, the case generator, the stage's citation lines, rendered views) and b5778dbbe (re-pin).

How to finish:
1. Run the review as the brief describes: `claude -p --agent tbd-strong --model claude-opus-5-5` in its own detached worktree at d7f2c6186, blind to the exit commit. It reads Section 5 of packing/resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma.md and the checker; checks that the decided statement plus the hand reductions in the module docstring imply Proposition 5.1 as stated (open versus closed, orientations, the point-row argument, the case split by which strip lines cut, reflection and central symmetry, b near 3, what 101/100 is used for); checks every enclosure and rule (tau monotonicity, per-cell bounds, the row rule, margin, area and corner rules with lambda = 1 in a box, the tree replay, the sympy identities); runs the checker and its test; decides something independently with its own code; says what rung the evidence supports for T-083 and T-084 under epistemics.md; lists findings blocking or not.
2. Store its output byte-identical under docs/project/reviews/ (with a .flowmarkignore entry, as the other byte-identical reviews have), map it in docs/project/document-map.yaml, and list it in T-083's and T-084's `reviews` (kind adversarial, relation project).
3. If it has no blocking finding: merge the exit branch (or cherry-pick 28ffccc7c and b5778dbbe), re-render, re-pin. If it has one: fix the checker, rerun `--update`, and redo the exit.
4. #295 is then closeable (check_requests --report on the exit branch: "Closeable: yes, with a final comment").

Expected CPU: the checker's replay is about 4 s; the review lane, its own budget.
What refutes: a box the checker closes by an unsound rule, or a gap in the hand reduction.

## Notes

2026-10-06: done on the lane branch claude/ecstatic-pascal-pothtx-r6. The coordinator ran the review as a fresh-context subagent with no permission bypass, from the lane's prompt; its verdict is accept with non-blocking findings. The exit commits 28ffccc7c and b5778dbbe were fast-forwarded onto the lane branch.
- c77b29307 stores the review (SHA-256 55ba50b2..., with a .flowmarkignore entry and a document-map entry) and lists it in T-083's and T-084's reviews.
- c77b29307 also dispositions the findings:
  - 1: a quick soundness-sampling test, a slow full-leaf sweep, and an unsound point-row control that the sampling rejects.
  - 2: the trust boundary as an enumerated list.
  - 3: decides and premises fields in the receipt.
  - 4: the independent-decomposition sentence, with Lemma 5.2 stated as read.
  - 5: the full replay test marked slow.
  - 6: the corollary checks labelled as restatements, and the vacuous T-084 line dropped.
- 396f9beb8 re-pins.
Validation: packing-validate --records fails only campaign record (the n = 17 ledger). Close at R6's merge.
