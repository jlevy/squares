---
type: is
id: is-01m169k6tppmcm63fw0gqa9cp0
title: "Close the round trip: rebuild the packing from the recovered field"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T08:18:50.326Z
updated_at: 2026-08-29T08:18:50.326Z
---
promote/solve.py's discharge() proves a recovered relation is irreducible and isolates the right root, but it stops at the side. The promotion spec's phase 4 asks for the full round trip: build a NumberField from the candidate, solve every pose unknown exactly, rebuild the packing, and call verify_packing with exact_sign — then compare the reconstructed side against the input pose, because a wrong contact structure can yield a valid but suboptimal packing that verification alone does not catch. This is now feasible at n=11: since BC-059 the contact system is full rank (34/34), so the pose is determined. Negative controls the spec names: a plausible wrong polynomial must fail back-substitution, and a perturbed contact structure must fail the side comparison.
