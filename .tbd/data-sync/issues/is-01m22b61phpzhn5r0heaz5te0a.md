---
type: is
id: is-01m22b61phpzhn5r0heaz5te0a
title: Make rigid contacts a constraint instead of a very stiff spring
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:45:20.336Z
updated_at: 2026-09-09T06:04:22.861Z
---
Pressing the rigid preset in the workbench makes the packing bounce violently. Cause, with numbers: the default law is a linear push of 2500 with the knee at 0.15; the rigid preset sets the knee to 0.01, the push to 4000, and the slope past the knee multiplies by about 7.5, so effective stiffness goes 2500 to roughly 30,000. An explicit integrator is stable only while dt is under about 2/omega; at that stiffness with unit mass omega is near 173 per second, giving a limit near 11.5 ms against the fixed step of 8.3 ms. That is already marginal for a single contact, and contact forces sum, so a square against four neighbours sees about four times the stiffness and a limit near 5.8 ms, well under the step being taken. It overshoots, is flung out, returns harder. It shows up exactly when squares are crowded, which is the case that matters.

The principled fix: a rigid contact is a constraint, not a force. Resolve overlaps by projecting the squares apart and iterating until none remain, which is unconditionally stable because nothing is integrated. This is the overlap-forbidden mode specified earlier and never built; it should report how many correction passes the last step needed, since that is the honest cost of the constraint.

Cheaper interim fix: substep when stiffness is high, taking several smaller steps per frame, which keeps the spring model and costs only time. Either way the slider should not reach settings the integrator cannot hold without saying so. Supersedes the 'rigidity slider reaches unstable settings' item noted in think-qluo. Owner reported 2026-09-08.

## Notes

Substepping landed in 3ba4bc97: the open-ended stepper derives its substep count from the law's stiffest slope, safety factor 4 for summed contacts, capped at 12. Defaults return 1 substep so the shipped trajectory is unchanged to the bit; rigid takes 2. Measured after, grid start at n=17 over 1200 steps: rigid 4.979, default 4.985, both about 0.005 penetration, neither flying apart. Still open: the principled fix, a projection constraint rather than a stiff spring, and the re-measurement of the rigid-versus-sticky comparison that the instability invalidated.
