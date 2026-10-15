---
type: is
id: is-01m4yc9h8wqsdkyzc7j4kggjh6
title: Keep module fixtures together in reachable xdist runs
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:34:50.895Z
updated_at: 2026-10-15T12:05:54.081Z
started_at: 2026-10-14T23:40:45.121Z
closed_at: 2026-10-15T12:05:54.081Z
close_reason: Delivered in PR618 merge fc2ceae79f462fe707ebbad1b94eb7cc306797b8 at2026-10-15T11:50:04Z. Exacthead3fe had three clear17path reviews and43passing hostedchecks, including full Deferred38726327460; ordinaryPacking38726302496 andPages38726302526 passed. Mainpublication38730161845 completed successfully including liveverify-deployment. Localcanonicalincremental9checks430.55s,5214normal/36skip+2pool, separatequickpool9pass; oldbroad1flagfailure preserved andfixed. Quickselection/loadfile andmodifierclassification shipped; no3minuteclaim orPR599strictgatewaiver. Parentcomponentcutfollow-up8iml/nkyg remains separatelytracked.
resolution: null
duplicate_of: null
---
Current broad prepush exposes a pre-existing main9b behavior: reachable_tests.py pytest_command uses -n10 with default load scheduling, while canonical quick shards use loadfile. Case-level distribution can repeat large module-scoped publication/atlas fixtures across workers. Inspect actual fixture construction counts and preserve every selected identity, normal/pool complement, native crash/requeue and deadlines. Prefer supported native loadfile distribution rather than a custom scheduler or shared transport; prove colocation with real workers and exact fixture-count/identity controls before any speed claim. Main9b and reviewed08d already contain this shape, so it is not introduced by PR599 and should follow current stabilization. Final prepush logs at7b802 record broad normal phase over400s; no attribution of that entire interval to this mechanism without measurement.

## Notes

Native --dist=loadfile preserves eight exact identities while the retained two-worker control reduces module fixture builds from two to one; no total-runtime speedup claim. Core runner/progress 164 passed; selected CLI 44 passed. PR618 (https://github.com/jlevy/squares/pull/618), head 3fe125696590cedc3ed3601dbbe098028948fd65, base f97bc0b199e2493b0d84ba51f512e2b406b73021. Three independent final-head reviews cover all 17 paths with no open findings. Site v0.7.6 is prepared. Broad e9cd pre-push had 67 prerequisite passes and 11,387 normal passes, 50 skips and one xfail, but one budget flag-contract failure; corrected by 3fe and the old run remains failed. Final incremental canonical gate passed nine checks in 430.55s, including 5,214 normal passes (36 skipped) and two pool cases. Separate quick pool complement passed nine cases in 40s. Maintained site cut passed 111 cases, 15 deselected; release-impact errors are empty. Hosted Packing 38726302496, Pages 38726302526 and one selected Deep checkpoint 38726327460 are running. Merge/publication remain pending; no three-minute claim or PR599 strict-gate waiver. Persistent evidence: primary .codex/regularization-closeout-evidence-2026-10-13/.
