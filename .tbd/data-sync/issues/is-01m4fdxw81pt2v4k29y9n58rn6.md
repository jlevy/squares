---
type: is
id: is-01m4fdxw81pt2v4k29y9n58rn6
title: Stabilize stack 430 on main 3213 and qualify every layer
kind: task
status: in_progress
priority: 1
version: 20
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
  - is-01m4fh4xngwat02257fnj2f3dk
  - is-01m4fhtf47sdkk0ffx4b5x5jpx
  - is-01m4fhtfpzk93c99z2fj4pkb8y
  - is-01m4fhtg9da0y5514xbzg58cr6
  - is-01m4fk142s062w9aj65ptbas2d
  - is-01m4fkxpt2eacwcrz1sc25s00b
  - is-01m4fkxqcgp6xcf3e98azvvqj7
hold: null
hold_until: null
created_at: 2026-10-09T04:14:49.601Z
updated_at: 2026-10-09T06:05:17.186Z
started_at: 2026-10-09T04:20:32.996Z
---
Cloud continuation of think-yij0 handoff (PR467). Normal-merge origin/main 3213d651b into #442, propagate to #468, fix the recorded failures without weakening limits, obtain exact-head required CI and full checkpoints, bind reviews. Merge only with owner confirmation (github-merge confirm-session).

## Notes

2026-10-09 cloud coordinator: main 3213 integrated through #466 and pushed. Lanes running: think-x47r timing #442, think-cmjh CLS + #468 merge, think-xv8j T-129/survey URLs #459-#463, think-qtdo #466 integrity/records wall, think-88r0 five Couzo follow-ups on new branch codex/import-couzo-followup-five-2d32a6e. Owner asked (in session) for everything fully reviewed, clean and ready to merge, and PR descriptions organized as a gh stack with a titled clean top-of-stack description. gh-stack binary could not be installed (release API blocked, running downloaded binary denied); stack membership managed via REST POST /repos/jlevy/squares/stacks/430/add. Merge requires owner confirmation (confirm-session).

Owner asked (in session) to make all stack PRs ready to merge, fix CI and take them out of draft: all ten (#442-#468) marked ready via ccr/ready_for_review. Propagated #442 timing fix to every layer (#449 conflict in test_overview.py resolved keeping #449's indirect shared_html fixture; 4 affected tests pass, ruff clean): #443 191f2f3ba, #448 ee593f5dc, #449 73569a6e6, #450 ad11c35b0, #459 834b17090, #460 e017f455a, #463 8b8b6804d, #466 b5d689653, #468 c6bab8b25. Full checkpoint dispatch is impossible from this session: POST .../packing-validation.yml/dispatches returns 403 Resource not accessible by integration (gh and GitHub MCP). Full Packing validation runs only on workflow_dispatch, schedule and push to main; the deep-gate label runs the deferred surface on PRs.

Owner in session: 'Once everything is clean and ready to merge, you can merge the whole stack.' (github-merge confirm-session confirmation for stack 430, all layers). Owner asked to use proper gh stack methods and read GitHub's PR-stack instructions: read gh-stack v0.1.0 skills/gh-stack/SKILL.md and docs (stacked-prs guide, overview merging, merge-api, rest-api, FAQ). gh stack v0.1.0 installed (sha256 358552dd… verified) but its PR lookups and merge config use GraphQL, which this session blocks (gh stack link 430 468 -> 403 GraphQL). Using the documented REST equivalents it wraps: POST /stacks/430/add (link), GET /stacks?pull_request=N (membership), PUT /pulls/{top}/merge-async + poll (merge; merge_method merge, sha pinned). Stack must be linear (each branch contains parent head) before merge; new PRs append only on top of #468's head ref. Propagation stays normal merges per owner's first instruction (no rebase/force-push).
