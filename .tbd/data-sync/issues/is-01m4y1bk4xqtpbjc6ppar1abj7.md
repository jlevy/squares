---
type: is
id: is-01m4y1bk4xqtpbjc6ppar1abj7
title: Keep ordinary pre-push validation in the reachable quick lane with explicit slow opt-in
kind: task
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
child_order_hints:
  - is-01m4zkv7xaws31vqay1f35rs0t
hold: null
hold_until: null
created_at: 2026-10-14T20:23:44.013Z
updated_at: 2026-10-15T11:19:17.634Z
started_at: 2026-10-14T20:24:38.989Z
---
Measured News pre-push selected608of791files, included slow behavior and ran serially700.49s before interruption at13%. Make default reachable validation use the existing QUICK_TESTS predicate for all selection kinds; preserve conservative path selection and normal/pool lane ownership. Add explicit deliberate slow coverage CLI and meaningful option/selection/control tests, document its required role at deep checkpoints. All fast checks stay automatic in CI; no timing ceilings or scientific obligations weakened. Follow Astra next-default-loop-slice report and active CI iteration plan.

## Notes

Quick defaults now cover every conservative selection kind, with explicit --include-reachable-slow and honest lane/exclusion/empty-selection receipts. PR618 (https://github.com/jlevy/squares/pull/618), head 3fe125696590cedc3ed3601dbbe098028948fd65, base f97bc0b199e2493b0d84ba51f512e2b406b73021. Three independent final-head reviews cover all 17 paths with no open findings. Site v0.7.6 is prepared. Broad e9cd pre-push had 67 prerequisite passes and 11,387 normal passes, 50 skips and one xfail, but one budget flag-contract failure; corrected by 3fe and the old run remains failed. Final incremental canonical gate passed nine checks in 430.55s, including 5,214 normal passes (36 skipped) and two pool cases. Separate quick pool complement passed nine cases in 40s. Maintained site cut passed 111 cases, 15 deselected; release-impact errors are empty. Hosted Packing 38726302496, Pages 38726302526 and one selected Deep checkpoint 38726327460 are running. Merge/publication remain pending; no three-minute claim or PR599 strict-gate waiver. Persistent evidence: primary .codex/regularization-closeout-evidence-2026-10-13/.
