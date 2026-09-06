---
type: is
id: is-01m1t769sq46m6hkgfpj3j7z2c
title: Supersede final hashes and upstream observation
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1t71bf6rqbsd14afyvp2b7y
created_at: 2026-09-06T02:01:38.869Z
updated_at: 2026-09-06T02:46:37.474Z
closed_at: 2026-09-06T02:46:37.473Z
close_reason: "PR #87's exact green head fd7c9d94 was directly integrated, the final named inputs were re-hashed in agenda-024's pre-dispatch manifest, historical receipts were preserved, and campaign views were regenerated."
resolution: null
duplicate_of: null
---
After docs settle and PR 87 lands, append the actual sibling-head/landed observation and a superseding pre-T+0 manifest with final hashes. Regenerate campaign views; do not rewrite historical receipts.
