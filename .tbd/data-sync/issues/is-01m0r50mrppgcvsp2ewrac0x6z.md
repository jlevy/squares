---
type: is
id: is-01m0r50mrppgcvsp2ewrac0x6z
title: Define basin identity for non-isolated terminal manifolds
kind: bug
status: open
priority: 0
version: 7
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - pr-14
  - ambiguity
  - basin-identity
dependencies:
  - type: blocks
    target: is-01m0r50x1ms53tfamwwmc5qw2z
  - type: blocks
    target: is-01m0r516kvkaaa5bbf9nm948qa
  - type: blocks
    target: is-01m0r51fbqgm0y4tb2d09fcb82
parent_id: is-01m0qxpb7634zbzt638d239jks
child_order_hints:
  - is-01m0tjpssmzsea6veac0znrtfs
created_at: 2026-08-23T20:29:25.654Z
updated_at: 2026-08-24T19:18:54.593Z
---
PR #14 ambiguity 1. A basin must be defined for a fully specified deterministic quench on configuration space quotiented by square relabelling, each square's quarter-turn symmetry, and container D4. The current two-hash endpoint key assumes isolated minima and splits positive-dimensional terminal families. The exact n=3 family with centres (1/2,1/2), (3/2,1/2), (t,3/2), t in [1/2,3/2], has side 2 and one contact certificate but many geometric keys. Acceptance: distinguish observations, isolated terminal points, and connected terminal components; compute active-constraint rank/nullity after quotienting discrete symmetries; continue every detected null direction and identify connected stationary strata; preserve boundary strata where contact graphs change; make component-level attraction probability the counted object; and add the n=3 family as a regression that cannot inflate basin count with a finer quantum. Until this passes, small-n outputs are called endpoint clusters, not basin counts.

## Notes

2026-08-24 correction after exp-014. The exact n=3 family does not have one contact certificate on the closed interval: the open stratum has one and both endpoint wall strata have a second. Exp-014 proves the full quotient is a closed interval and installs the regression.\n\n2026-08-24 exp-032 completes the narrow BC-009 known-answer child think-a2v6. The frozen policy assigns the complete exact n=3 interval and n=4 point, rejects eight key/stratum/sample/scope/f64 conflations, and leaves 16 unsupported numerical events unresolved. The general bead remains open for n=5 identity, ambiguity, continuation, angle clustering, and scalable classification; no component-level mass follows from hashes.
