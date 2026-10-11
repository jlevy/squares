---
type: is
id: is-01m3vbf7g19w4t32avqckzqszk
title: Replay evand finite family premise and reconcile the conditional Lean reduction
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
labels: []
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
created_at: 2026-10-01T09:07:03.806Z
updated_at: 2026-10-04T06:33:57.773Z
closed_at: 2026-10-04T06:33:57.773Z
close_reason: "Done on origin/main e5a48b310: T-064 V3/C3 (check_requests --report) with E-k2m3-evand-valid7-qx2-replay (full qx2 replay), E-k2m3-evand-bentz-lean-build (Lean reduction, standard axioms), and E-k2m3-wand125-valid7-independent (wand125 independent checker replayed in full with --guard-d1, replay_status passed, 156,800 roots; #329). #296 closed 2026-10-03 with follow-up reply."
resolution: null
duplicate_of: null
---
Oct1 source pin 08e8a5f reports s(k^2-3)=k for every k>=6. Register source assertions separately from acceptance. Acquire missing finite-cover inputs, audit exact zero-tilt and positive-tilt/area bounds, complete pose/root coverage and record-to-Lean mapping; replay Valid7 with a selected bounded gate or independent implementation. Lean reduction alone does not discharge Valid7. Scope and next commands in review-2026-10-01-evand-mathematical-transfer.md. Do not schedule the 81000 CPU-second source sweep blindly.

## To finish (validation backlog, 2026-10-02)

T-064 (Daniel's s(k^2 - 3) = k for k >= 6, V0/C1). Three things, before any case's verified bound moves: (1) a complete replay of one Valid7 checker on the retained cover resources/web/evand-square-packing-2026-10-01/source/s12/certificates/k2m3/L4_k02_box7.txt, either the source's qx2_zm.py (about 81,000 CPU-seconds at the source; schedule it deliberately) or wand125's independent checker (about 626 core-hours; packet resources/web/wand125-valid7-independent-check-2026-10-02/, audited by devtools.audit_valid7_independent); (2) a review of the independent checker's method (DESIGN.md and its module docstrings: closure at theta = 0, the core bound, the fixed-angle lemmas); (3) the Lean reduction built with an axiom receipt, after retaining the files it imports. Refutes: an uncertified root or a counterexample in a complete Valid7 sweep, or the reduction failing to build or resting on a non-standard axiom. Moves the rung: (1) recorded as an exact-algebraic replayed-here entry and (3) as proof-assistant-checked evidence derive V3/C3. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-02: a second, independently written exact checker for Valid7 (wand125/valid7-independent-check, #296) is retained in packing/resources/web/wand125-valid7-independent-check-2026-10-02/; its verify.sh (record check, 2,300 sampled leaves, three mutants) passes here, records-v1 pinned by digest. Remaining for T-064: a full replay of one Valid7 checker, a review of the independent checker's method, and the Lean reduction's build with its axiom receipt.
- 2026-10-03 ~05:30 T-064 at V3/C3 (pushed 19cb367ba): qx2 replay compare ok (9,800 roots, 32,079 leaves equal to the source's V3 record, none uncertified; E-k2m3-evand-valid7-qx2-replay, same-implementation) + Lean reduction built (E-k2m3-evand-bentz-lean-build, proof-assistant-checked, axioms propext/Classical.choice/Quot.sound). Nine more cases proved: n = 97, 118, 141, 166, 193, 222, 253, 286, 321; counts 77 proved / 247 open. Remaining on T-064: wand125's independent Valid7 checker replay with --guard-d1 (runners w1-w5, ~216 CPU-h), which would add an independent-implementation route and close D-1. The verifiers field waits for #311.
