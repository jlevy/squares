---
type: is
id: is-01m41crc9rnphq77swdexdmgtx
title: "Merge #292, #298, #311 into main bottom-up once each is green and mergeable"
kind: task
status: closed
priority: 1
version: 24
labels:
  - merge
dependencies:
  - type: blocks
    target: is-01m3wyajwc1tbyq4f2rbhjhqdh
  - type: blocks
    target: is-01m3ys19bfzkjp4yrp53ndbc8j
  - type: blocks
    target: is-01m3ys1amqty0xqzyhx0avfssz
  - type: blocks
    target: is-01m3ys1by49bhke0fd8twcff5m
  - type: blocks
    target: is-01m3ys1ddgc8ydwg9vk5bpfrkp
  - type: blocks
    target: is-01m3ys1eyvhd71mxr5nec8w8rs
  - type: blocks
    target: is-01m3ys1fz0a6qc5j6vny00wb2p
  - type: blocks
    target: is-01m3ys10dq5xc2gjw4m5dn086t
  - type: blocks
    target: is-01m3ys11k8svw9337p3gsj48rf
  - type: blocks
    target: is-01m3ys13d4m4f3nsy0mq964m19
  - type: blocks
    target: is-01m3ys14zf9kaxrjz44ksfrhmd
  - type: blocks
    target: is-01m41e1tqg81pgz89snb0whnv4
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:24:58.807Z
updated_at: 2026-10-05T03:23:08.176Z
closed_at: 2026-10-03T18:13:03.565Z
close_reason: null
resolution: null
duplicate_of: null
---
Merge commits, not squash or rebase (think-fqut: GitHub's stacked merge rebases children). After each merge, retarget and check the next PR is still mergeable; refresh its CI.

## Notes

2026-10-03 18:00 Owner: stabilize and land now; new imports after. Scope freeze sent to the records lane (#298), SP2 (#311) and the stack-merge lane (#292).
Merge procedure (main is unprotected; delete_branch_on_merge is true, and GitHub restack-rebases children when a base branch is deleted, think-fqut):
1. #292 green → retarget #298's base to main FIRST (gh pr edit 298 --base main), then merge #292 with a merge commit.
2. #298 green against main → retarget #311's base to main FIRST, then merge #298 with a merge commit. Our designated branch is deleted on merge; restart it from main for follow-ups.
3. #311 green → merge with a merge commit.
4. Then final issue replies from main with check_requests --draft N (think-hen3), evand's #316, #256 and #238 first, then close the closeable ones.
Follow-up branch after landing: n82 (T-076), n83 (T-073), T-077, T-046 leftovers, Valid7 w-shards, census evidence (think-3ok2), #316 import (IM316 branch claude/import-316-k2m4), and any newer issues.
2026-10-03 18:20 Revised: #290, #292 and #298 are a native GitHub PR stack (stack 293). 'gh pr edit 298 --base main' is refused ("part of a stack"), and the GraphQL API has no unstack mutation. Merging #292 first would make GitHub restack-rebase #298 (as it did #292 after #290), rewriting a branch full of merge commits under the records lane's unpushed work. Plan without any rewrite: (1) the records lane pushes the restacked #298, which contains #292's head c307f646f, so #298 is a clean fast-forward of its base; (2) merge #298 into its base claude/import-2026-10-01-requests with a merge commit (top of stack; nothing above it in the native stack); (3) #292 then carries everything; CI on #292's new head; merge #292 into main with a merge commit. #311 (not in the native stack) gets retargeted by GitHub as its base branch is deleted; SP2 follows. #292 green and CLEAN at c307f646f (run 37140957988) before step 2.
2026-10-03 18:40 GitHub's stack mergeability kept #298 'dirty' though its base was an ancestor, so I fast-forwarded claude/import-2026-10-01-requests c307f646f..944d2d39f (no rewrite). GitHub marked #298 MERGED and deleted claude/zealous-gauss-jem7l9; #311 retargeted to #292's branch. #292 (base main) now carries #292 + #298, MERGEABLE, CI running; merge it into main with a merge commit when green.
2026-10-03 18:13 LANDED. #292 (carrying #298 by fast-forward) merged into main via the stacked async merge API (PUT pulls/292/merge-async, merge_method=merge, direct_merge): merge commit 47569ad50. #311 retargeted to main, CLEAN, marked ready from draft and merged: 4043d863e. CI green beforehand: #292 run 37142741383, #311 run 37142992325. Next: deploy verification (think-ovwb), final issue replies (think-hen3), follow-up PRs (homepage think-nlyc; n101 + acks think-xex7/think-t2mu).
