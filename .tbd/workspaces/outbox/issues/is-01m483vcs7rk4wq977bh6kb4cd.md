---
type: is
id: is-01m483vcs7rk4wq977bh6kb4cd
title: Run exp-257's unrun draw u31 (mask 6015871, c4/i>=5/d>=8) under SW9's recipe, resuming BC-428
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m48zbcc8pzmh9njj74xyq4w7
hold: null
hold_until: null
created_at: 2026-10-06T08:04:01.446Z
updated_at: 2026-10-06T17:34:04.407Z
started_at: 2026-10-06T15:54:50.014Z
closed_at: 2026-10-06T17:34:04.406Z
close_reason: "u31 closed and admitted (s183-bc429-u31, exp-258 accepted); merged in jlevy/squares#385 (stack #386) on 2026-10-06. All 31 BC-428 draws have a verdict."
resolution: null
duplicate_of: null
---
exp-257 (H-275) stopped on its clock: new starts stopped at 06:17 UTC on 2026-10-06
under the coordinator’s session-lease rule, 57 minutes before the registered deadline.
Its verdict.resume_from names draw 31 of
packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt, under
exp-257’s recipe and command.
Needs a host with the run worktree’s kernel and, for admission, the standing verifier’s
full pass and the census.
u1/u15 saved nodes would at most certify round-cap stalls (W2 F7). Lands on #379’s
successor; the certificate objects should be hosted (think-jhgi) first so another host
can verify.

## Notes

Done on branch claude/n17-session-183-u31, draft PR #385: registration cbcf37697 (pushed
16:02:26Z, before the run), u31 PASS_CERTIFIED_CLOSED in 577 s wall / 547 s CPU,
standing verifier full PASS in 266 s, admitted as s183-bc429-u31 in 7ea2ee322 (census
36,784 states / 4,685 orbits, endpoint surviving), exp-258 accepted and Session 183
closed stopped in 152e37eae. Remaining: certification think-oanv (hosted fast run),
object upload think-jhgi, merge by the owner.
