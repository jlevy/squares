---
type: is
id: is-01m0p5tswc9s27gb5c1d3da27b
title: "Phase 5: compiled acceleration, where the profile says"
kind: epic
status: open
priority: 3
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
child_order_hints:
  - is-01m0p5tt80b0arp65y0z2ah9d3
  - is-01m0p5ttjs6qzwv1qhmszg5dbb
  - is-01m0p4bwrbqc4gvd227t3mgnxh
created_at: 2026-08-23T02:05:13.995Z
updated_at: 2026-08-23T02:05:29.841Z
---
Epic, deliberately late. By this point a real campaign has been profiled and the profile names what to accelerate. On the numbers taken before any of it was written the exact verifier is the candidate: 129ms per n=11 verification, 100x the LP quench and 5000x an annealer move. Verifying every basin in a 1e5-basin census would take hours; nothing else is close, and the annealer - the thing that looks slowest - already has a compiled implementation. Re-measure first, build only what the measurement names. Boundary is a native binary or a cdylib called with ctypes, not PyO3: the certificate's durable interface is JSON either way.
