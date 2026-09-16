---
type: is
id: is-01m2m4brsp91431gsjh16qje0f
title: "PR #178 review R1: one new probe is clean only under the relaxed program"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4brc46s3a2pqbaqthnyz7
created_at: 2026-09-16T03:32:27.573Z
updated_at: 2026-09-16T04:44:56.208Z
---
packages/workbench/probes/pack/scene-matches-snapshot.js:16 fails strict tsc with TS2532 under noUncheckedIndexedAccess. Fix: bind nodes[index] and refuse undefined. (PR #178, review 5218208269)
