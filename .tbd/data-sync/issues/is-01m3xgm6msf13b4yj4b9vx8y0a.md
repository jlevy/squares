---
type: is
id: is-01m3xgm6msf13b4yj4b9vx8y0a
title: "Census: classify the 324 known-best witnesses into structural families"
kind: task
status: closed
priority: 2
version: 5
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m3xgm8td0cpy923bjvqb7c31
  - type: blocks
    target: is-01m3xgm9ccqv1h8p3j5x9ezjy0
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T05:15:38.521Z
updated_at: 2026-10-02T06:00:21.759Z
closed_at: 2026-10-02T06:00:21.759Z
close_reason: Lane exit reached and integrated into X-049 (packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md); coordinator verified the lane's claims, tests and checks; follow-ups are think-589i, think-hzv3, think-1n8w, think-bgkz and think-ptt7.
resolution: null
duplicate_of: null
---
W3 measurement lane, OR-1 tool. Build packing/devtools/classify_known_best_families.py with tests: for each n, k = nearest-square index and offset d = n - k^2, side excess over ceil(sqrt n), tilted-square count, angle classes (0, 45, other), largest axis-aligned grid component, symmetry (D4 subgroup within tolerance), source. Emit JSON and a summary keyed by d. Answer: do families keyed by d exist in the data, where do they break, and which consecutive pairs (232-233, 264-265, 268-269, 301-302) share structure.
