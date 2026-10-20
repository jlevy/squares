---
type: is
id: is-01m4zkv7xaws31vqay1f35rs0t
title: Classify the slow-test opt-in in the CLI budget contract
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4y1bk4xqtpbjc6ppar1abj7
hold: null
hold_until: null
created_at: 2026-10-15T11:06:05.609Z
updated_at: 2026-10-15T12:05:54.089Z
started_at: 2026-10-15T11:07:10.146Z
closed_at: 2026-10-15T12:05:54.089Z
close_reason: Delivered in PR618 merge fc2ceae79f462fe707ebbad1b94eb7cc306797b8 at2026-10-15T11:50:04Z. Exacthead3fe had three clear17path reviews and43passing hostedchecks, including full Deferred38726327460; ordinaryPacking38726302496 andPages38726302526 passed. Mainpublication38730161845 completed successfully including liveverify-deployment. Localcanonicalincremental9checks430.55s,5214normal/36skip+2pool, separatequickpool9pass; oldbroad1flagfailure preserved andfixed. Quickselection/loadfile andmodifierclassification shipped; no3minuteclaim orPR599strictgatewaiver. Parentcomponentcutfollow-up8iml/nkyg remains separatelytracked.
resolution: null
duplicate_of: null
---
Canonical e9cd pre-push caught one failure: test_gate_budgets.test_every_boolean_flag_is_classified_as_a_tier_or_not. New --include-reachable-slow is a push-selection option, not a new validation tier; explicitly classify it in the existing flag-audit contract and retain the check that unknown booleans fail. Run the focused budget contract and all affected option tests, preserve the failed canonical receipt and reuse its passing selected tests without repeating unchanged scientific work. No budget or assertion weakening.

## Notes

Fixed by 3fe: classify include_reachable_slow as a modifier and exercise --push --include-reachable-slow in declared-tier checks. Unknown-boolean refusal and all production tiers/budgets remain intact. PR618 (https://github.com/jlevy/squares/pull/618), head 3fe125696590cedc3ed3601dbbe098028948fd65, base f97bc0b199e2493b0d84ba51f512e2b406b73021. Three independent final-head reviews cover all 17 paths with no open findings. Site v0.7.6 is prepared. Broad e9cd pre-push had 67 prerequisite passes and 11,387 normal passes, 50 skips and one xfail, but one budget flag-contract failure; corrected by 3fe and the old run remains failed. Final incremental canonical gate passed nine checks in 430.55s, including 5,214 normal passes (36 skipped) and two pool cases. Separate quick pool complement passed nine cases in 40s. Maintained site cut passed 111 cases, 15 deselected; release-impact errors are empty. Hosted Packing 38726302496, Pages 38726302526 and one selected Deep checkpoint 38726327460 are running. Merge/publication remain pending; no three-minute claim or PR599 strict-gate waiver. Persistent evidence: primary .codex/regularization-closeout-evidence-2026-10-13/.
