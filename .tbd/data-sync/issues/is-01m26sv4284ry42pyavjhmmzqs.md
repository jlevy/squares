---
type: is
id: is-01m26sv4284ry42pyavjhmmzqs
title: Clarify T-026 as a proved lower bound across the explainer and reader docs
kind: task
status: closed
priority: 1
version: 19
labels: []
dependencies: []
child_order_hints:
  - is-01m27258dy9wympsk083fspbm0
  - is-01m2729rgwe9tf9kk6m8hv5242
  - is-01m27341tgrm865t7htkcacdf5
  - is-01m27hc9136cfzbb0gcq3b90pm
  - is-01m27kjxj4g8z0vyckt3x8xp2w
  - is-01m27m4teg5w29vh0d03ddp9tg
  - is-01m27myg3v2zhr8dnzy6fg82vm
created_at: 2026-09-10T23:18:28.662Z
updated_at: 2026-09-12T08:42:29.981Z
closed_at: 2026-09-12T08:42:29.980Z
close_reason: PR148 head 989fd544 states and verifies the ordinary lower bound s(11) >= C, includes self-contained T025 and T026 claim packets and mapped review, reconciles all reader and research terminology, passes exact-head pre-push and full checkpoints, and has every hosted check green. Ready for review.
resolution: null
duplicate_of: null
---
Revise PR148 on current main so the headline states s(11) >= C directly, publishes the v0.4.0 explainer, gives T025 and T026 self-contained verifiable claims, records T026 at V4/C5 under epistemics.md, reconciles reader and research terminology, and passes local and hosted validation.

## Notes

PR148 final candidate head 989fd544 is pushed and clean. All hosted checks pass, including packing validation, Certificate page, Firefox, WebKit, and mergeability. Exact-head pre-push passed 46 of 74 steps with 5,037 tests, Ruff over 1,781 files, and BasedPyright with zero findings in 967.56 seconds. The full merge and research checkpoint passed in 7,628.28 seconds; four local Rust and sqsearch checks skipped because this host lacks Cargo and the binary, while their hosted jobs passed. The PR body records the exact status and the branch is ready for review.
