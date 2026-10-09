---
type: is
id: is-01m4fdxw81pt2v4k29y9n58rn6
title: Stabilize stack 430 on main 3213 and qualify every layer
kind: task
status: in_progress
priority: 1
version: 11
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
child_order_hints:
  - is-01m4fdxwz8wxkhxwc1kpbene5s
  - is-01m4fdxxmb9djrbnegf3hrg48c
  - is-01m4fdxy7dbpfged7eh7j24bt9
  - is-01m4fdxysyxrsz86wnrpzt6sr4
  - is-01m4fdxzd5x9xh1q9nqqqwghay
  - is-01m4ffmmj2d5xhzg8axzntn67s
  - is-01m4ffmn5zpqw65ew6df3kxwh6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:49.601Z
updated_at: 2026-10-09T05:08:11.110Z
started_at: 2026-10-09T04:20:32.996Z
---
Cloud continuation of think-yij0 handoff (PR467). Normal-merge origin/main 3213d651b into #442, propagate to #468, fix the recorded failures without weakening limits, obtain exact-head required CI and full checkpoints, bind reviews. Merge only with owner confirmation (github-merge confirm-session).

## Notes

Owner asked (in session) to make all stack PRs ready to merge, fix CI and take them out of draft: all ten (#442-#468) marked ready via ccr/ready_for_review. Propagated #442 timing fix to every layer (#449 conflict in test_overview.py resolved keeping #449's indirect shared_html fixture; 4 affected tests pass, ruff clean): #443 191f2f3ba, #448 ee593f5dc, #449 73569a6e6, #450 ad11c35b0, #459 834b17090, #460 e017f455a, #463 8b8b6804d, #466 b5d689653, #468 c6bab8b25. Full checkpoint dispatch is impossible from this session: POST .../packing-validation.yml/dispatches returns 403 Resource not accessible by integration (gh and GitHub MCP). Full Packing validation runs only on workflow_dispatch, schedule and push to main; the deep-gate label runs the deferred surface on PRs.
