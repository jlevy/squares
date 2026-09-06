---
type: is
id: is-01m1vz4dvs8ng1e70vgzv9mfg7
title: Preserve distinct exact vertices that round to one float point in cutting separation
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:19:17.752Z
updated_at: 2026-09-06T18:20:01.920Z
---
At L=4 with epsilon=1e-20, three axis-aligned unit squares have y-range [1,2] and x-ranges [1-2epsilon,2-2epsilon] (weight0), [2-epsilon,3-epsilon] (weight1), [1+epsilon,2+epsilon] (weight1). Exact maximum is2 but screened_separation reports1 because float_vertices deduplicates distinct exact vertices by their identical float coordinates. Preserve these candidates or deduplicate exactly; regress the small-coordinate example. Final ceiling verifier enumerates independently.
