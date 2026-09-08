---
type: is
id: is-01m0nxq9sedycsz5hxfhbb2r84
title: "Lean: make the verifier emit a certificate, then formalize upward"
kind: epic
status: open
priority: 2
version: 7
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0nxqa3c286jz8mq1tv2ceme
  - is-01m0nxqaeghsmbn3crwefzrqy6
  - is-01m0nxqaw4vdz9psd5k42symvt
  - is-01m0nxqb6zj5ay2f22rar741ck
  - is-01m0nxqbhz1rszwhx745qq595f
  - is-01m1vvtxyvta4m04ybey4h0mhg
created_at: 2026-08-22T23:43:30.605Z
updated_at: 2026-09-06T17:21:40.826Z
---
From research-2026-08-22-lean-for-packing-proofs-and-validation.md. The requirement is a third-party-verifiable way to express and validate solutions: a Lean proof replaces 'trust our verifier' with 'run the kernel'. Lean sits in the agent tier (Flyspeck measured ~3000x slowdown on formal nonlinear inequality checking) and must never touch the search loop.
