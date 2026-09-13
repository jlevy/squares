---
type: is
id: is-01m2cv9dq93ydszsmkyhzjn1mf
title: "PR #157 review integration: reorder the stack to 148 -> 149 -> 156 -> 157"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:39:12.489Z
updated_at: 2026-09-13T07:39:12.489Z
---
Review directs placing PR157 above PR156; the merge of the reviewed PR156 head 52e4ab65 is textually clean. Preserve BOTH sets of threshold changes, update the handoff, and verify the integrated source before pushing. Target stack: PR148 -> PR149 -> PR156 -> PR157. PR156 is a codex branch and must not be pushed to; only PR157's base changes.
