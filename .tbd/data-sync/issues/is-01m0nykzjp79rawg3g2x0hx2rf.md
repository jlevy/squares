---
type: is
id: is-01m0nykzjp79rawg3g2x0hx2rf
title: "Minimal packing toolkit: search, verify, iterate"
kind: epic
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0nykzwb0b8kwndbvf27aefk
  - is-01m0nym0701fv1qq9fbqq9qz0w
  - is-01m0p1891hrpend196qc0444r2
created_at: 2026-08-22T23:59:10.422Z
updated_at: 2026-08-23T00:45:12.625Z
---
Implements the plan spec. Two phases: the verification core (Rust, generic over Scalar, certificate-emitting), then search plus the n=11/n=12 experiments. Kay's rule is the acceptance test: verify(packing) is one call in milliseconds, and the SAME predicate with a PoseBox scalar answers the unavoidable-set question for the proof lane. If a capability needs a second implementation of the separating-axis test, the design has failed.
