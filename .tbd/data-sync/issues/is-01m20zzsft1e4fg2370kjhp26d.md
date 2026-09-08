---
type: is
id: is-01m20zzsft1e4fg2370kjhp26d
title: Build the inflation formulation as an ablatable sqsearch arm
kind: feature
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T17:10:26.553Z
updated_at: 2026-09-08T17:10:26.553Z
---
The 2026-09-08 survey's section 7 asks for the inflation formulation: fix the container to the unit square, carry a common square side s, maximise s, and report 1/s. It is the change the survey rates highest and it is a rewrite of packing/sqsearch/src/geom.rs rather than a flag.

Why it is worth building even though the cheap surrogate (H-126, geom::spread) is measured: the surrogate adds a dense term beside the sparse one, where inflation replaces the max over two to four extremes with a min over the active contact set, which at a jammed configuration has size on the order of 2n.

Note the caveat the round-1 record raises: a min over many constraints is still decided by its argmin, so inflation is not automatically dense either. Build it as an ablatable arm and measure it against the same subset, the same seeds and the same pair-test budget as exp-130 and exp-131, so the three are comparable.

The exact inflation factor is computable in closed form for squares: for a pair, the largest scale factor f keeping them disjoint is the max over the four edge normals a of |d . a| / (H_i(a) + H_j(a)); for a wall it is min(x, S - x, y, S - y) / E. Config-wide f is the min over pairs and walls, so it costs one O(n^2) scan, the same as total_overlap.
