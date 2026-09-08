---
type: is
id: is-01m21c5wz2ymp6v369pjq3mrcz
title: "PR127 R2: preserve off-net cores in the deep-corner clip"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m21badm7ednkkxzwgcjmgaam
created_at: 2026-09-08T20:43:29.633Z
updated_at: 2026-09-08T23:03:18.405Z
closed_at: 2026-09-08T23:03:18.405Z
close_reason: Corrections are committed in ef8a2e72 and cbe9fd76 and documented in docs/project/reviews/review-2026-09-08-pr127-research-readiness.md. The completed checkpoint combines actual passing cbe9fd76 fast, negative-control, slow and exhaustive receipts with four unchanged geometry passes from the failed ef8a2e72 full run. Scientific limits and unrun complements remain explicit.
resolution: null
duplicate_of: null
---
Lane A 281-288 and 1479; X021 127: avoidance a+b>d+cos(theta_net) can discard the core of an off-net unit avoider. Exact counterexample d=7/10, half-tangent=1/1000, a=b=(d+1000000/1000001)/2. Safe elementary clip is a+b>d+B*cos(theta_net), or derive a sharper envelope over the entire angle cell. Route unrun; fix specification and add exact off-net control before execution.
