---
type: is
id: is-01m51ctd9c7w7fe3rjfpgsgjtx
title: "PR #636 C2: atlas README still states the house-sides admission guard that B3 replaced"
kind: bug
status: closed
priority: 3
version: 3
delegate: tbd-moderate-pr636-c
labels: []
dependencies: []
parent_id: is-01m51ct5f1m0k1swz8x23dkd7p
hold: null
hold_until: null
created_at: 2026-10-16T03:41:47.180Z
updated_at: 2026-10-16T04:01:33.010Z
started_at: 2026-10-16T03:41:51.691Z
closed_at: 2026-10-16T04:01:33.009Z
close_reason: "fixed in 89ef0da33: atlas README states the drawn-picture guard (worse on no goal than today's drawing; a tie admitted), and the guide says what today's drawing is and what layer keeps"
resolution: null
duplicate_of: null
---
Severity Low. PR #636 review C (https://github.com/jlevy/squares/pull/636#pullrequestreview-5542797505). File: packing/atlas/known-best/README.md:196-200 ('only where it shares at least as many full sides as the view it replaces'). admit_views now keeps the layer's view where the candidate is worse on any goal of the improvement rule and admits a tie. README is outside data_pathspec(), so DATA_REVISION does not move.
