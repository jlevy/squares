---
type: is
id: is-01m355gqecxjfj1yvcaabdedys
title: "PR 220 review R1: distinguish accepted proof from structural registration"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m3559hcm2gm7cfprehw5tzvk
hold: null
hold_until: null
created_at: 2026-09-22T18:19:43.946Z
updated_at: 2026-09-22T19:00:27.747Z
started_at: 2026-09-22T18:22:03.503Z
closed_at: 2026-09-22T19:00:27.737Z
close_reason: Fixed in e560571f2; documentation and record checks pass, 1681 reachable tests pass after parallel retry, and final-source hosted PR CI is green.
resolution: null
duplicate_of: null
---
packing/frontier/README.md:205-301 describes certificate metadata, novelty and C5 in terms that can overstate actual evidence. Require accepted replay receipts, whole-claim review, schema fields and bounded checker coverage.
