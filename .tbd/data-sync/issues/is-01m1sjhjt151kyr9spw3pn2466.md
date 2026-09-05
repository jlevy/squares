---
type: is
id: is-01m1sjhjt151kyr9spw3pn2466
title: Detect defect-id collisions at merge, not after
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T20:00:48.449Z
updated_at: 2026-09-05T20:00:48.449Z
---
D-462. Two branches allocated D-455/456/457 to different defects; the collision repeated one level down at D-458. Nothing inside one checkout can see it: the schema enforces uniqueness within a file, which is exactly the property that holds on both sides of a collision, and contiguity holds too. Detection needs a comparison against the merge base -- a check that reads git merge-base and refuses a defect id whose title differs on the two sides. conventions.md already rejects the alternatives (reserving ids, a second coordination ledger).
