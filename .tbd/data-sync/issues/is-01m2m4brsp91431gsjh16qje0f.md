---
type: is
id: is-01m2m4brsp91431gsjh16qje0f
title: "PR #178 review R1: one new probe is clean only under the relaxed program"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2m4brc46s3a2pqbaqthnyz7
created_at: 2026-09-16T03:32:27.573Z
updated_at: 2026-09-16T06:17:01.132Z
closed_at: 2026-09-16T06:17:01.131Z
close_reason: "Fixed by c72b968e ancestry: scene-matches-snapshot.js binds nodes[index] and refuses undefined; strict TypeScript/browser floor is green."
resolution: null
duplicate_of: null
---
packages/workbench/probes/pack/scene-matches-snapshot.js:16 fails strict tsc with TS2532 under noUncheckedIndexedAccess. Fix: bind nodes[index] and refuse undefined. (PR #178, review 5218208269)
