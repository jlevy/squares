---
type: is
id: is-01m1v2yj8dabmp29e6cf1ejvqx
title: Resolve BC-242 to BC-243 precedence before dual-only pilot
kind: bug
status: closed
priority: 0
version: 5
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels:
  - mathematics
  - release-blocker
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:06:45.516Z
updated_at: 2026-09-06T17:57:54.053Z
closed_at: 2026-09-06T10:23:03.052Z
close_reason: "Integrated 0660f02b: only BC-242's obsolete combined future scheduling dependency is superseded; weak duality and all strong-duality, attainment, singular-primal, numerical, and primal-semantics limits remain frozen. Combined edit tier passed."
resolution: null
duplicate_of: null
---
The frozen BC-242 author packet says BC-243 is blocked on both an exact a.e.-depth verifier and continuum primal coverage, while the later reviewed agenda and continuation intentionally split BC-243 into a dual-only kill and defer primal coverage to BC-244. Because the current precedence clause puts frozen result packets first, explicitly supersede only the obsolete combined-pilot dependency or narrow precedence so the reviewed dual-only split is authoritative without rewriting frozen evidence. Preserve BC-242 weak duality and every strong-duality/attainment limitation.
