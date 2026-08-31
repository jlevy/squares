---
type: is
id: is-01m0p188jzhnz00j60evcr04dq
title: Unavoidable-set falsifier + the Stromquist triple (R-5/H-10)
kind: task
status: closed
priority: 1
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1b29qrvdzvmjb2n22n5826h
  - type: blocks
    target: is-01m1b29r4pe1vvj5vzp2kqpsxt
  - type: blocks
    target: is-01m1b297ydh4ahazqwk4mx6hqq
parent_id: is-01m0nym0701fv1qq9fbqq9qz0w
created_at: 2026-08-23T00:45:12.158Z
updated_at: 2026-08-31T06:04:08.253Z
closed_at: 2026-08-31T06:04:08.252Z
close_reason: "BC-094 discharged by session-050 phase 2: sqpack/falsify.py with the known-answer triple green as tests (Figure 13 escape found at margin 1.3e-2, 45-degree family; repaired twelve-point set saturates at -(L-1) with the fixed not-a-proof caveat; typed refusals name the defeating pose). Exact bridge certifies the retained Figure 13 escape over Q(sqrt2+sqrt5) through sqpack.cover predicates."
resolution: null
duplicate_of: null
---
Cheap direction of the proof lane: search (x,y,theta) for a box avoiding a point set. Known-answer triple: MUST find the escape on Stromquist's 10-point Figure-13 set at s=2+4/sqrt(5) (top/bottom rectangle), MUST saturate on his 12-point Figure-14 set, and PoseBox later must PROVE the latter. Machine-checks our own correction of Theorem 2's structure.

## Notes

Raised to P1 by X-010: rung A1's falsifier half and the CEGIS inner loop for think-0z9b; known-answer triple unchanged. agenda-010 BC-094 (block 1 second).
