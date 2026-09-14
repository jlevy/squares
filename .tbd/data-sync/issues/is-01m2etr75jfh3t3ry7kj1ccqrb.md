---
type: is
id: is-01m2etr75jfh3t3ry7kj1ccqrb
title: "Land the n11 PR stack (#156, #161–#166) and sibling #157 on main"
kind: epic
status: open
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - pr
  - landing
dependencies:
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
child_order_hints:
  - is-01m2etrwa7dr81w3rwrzgm8cwq
  - is-01m2etrwrd527nqw0r62vg2gsw
  - is-01m2etsfvzb1rpqg15w6a8wyas
  - is-01m2ett16m2gz30tsat10zhshr
  - is-01m2ett207c0f76hc55gp435wz
  - is-01m2ettfz0drj6x542rqxghvqa
  - is-01m2ettwze138wbhg772ekt1d4
  - is-01m2evs21mvxf79h8jhnne4src
  - is-01m2evve1agpqv4m2s6jrcdseb
  - is-01m2evx728hwq95z70m0vz1878
  - is-01m2evx883khfqrmxg6fm6rqkg
  - is-01m2ey0emj7eakmbc3eyg1vj3f
created_at: 2026-09-14T02:08:17.585Z
updated_at: 2026-09-14T03:05:13.091Z
---
Land the unmerged n11 PR stack on main: #156 (BC329 runner, codex/n11-bc329-runner-publication-stack), the linear chain #161 → #162 → #163 → #164 → #165 → #166, and the sibling #157 (claude/n11-w7-weighted-atom-admission). #167 (H-162 preregistration, draft) stays above #166 as the next layer and retargets to main when the stack merges.

State at 2026-09-14 ~02:30 UTC: every PR is MERGEABLE/CLEAN with required hosted checks green (#156 2f8925b2, #157 382944dd, #161 ac6f39b8, #162 92320abf, #163 f70144fc, #164 be477f20, #165 93c5e217, #166 21d511f8); each branch contains its base; main is f2e24e07; `git merge-tree` of #166 with #157 is clean. No PR has a formal GitHub review decision. main has no branch protection (think-9tdn), so every gate below is policy, not enforcement.

Policy basis: development.md says a green fast surface is not full pre-merge evidence; the full checkpoint (fast surface plus deferred lane on the same source and base) must pass before merge and is void if main moves. The previous stack (#148/#149) landed by one full `Packing validation` dispatch on the top branch, PR bodies updated with the run, a stack merge of the top PR as one merge commit, a watched main push run, and a post-merge closeout section.

Children carry the decisions, stabilization, checkpoint, description refresh, merge, and #157 follow-on. The post-merge research checkpoint think-088v depends on this epic.
