---
type: is
id: is-01m0r50mrppgcvsp2ewrac0x6z
title: Define basin identity for non-isolated terminal manifolds
kind: bug
status: open
priority: 0
version: 4
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
created_at: 2026-08-23T20:29:25.654Z
updated_at: 2026-08-23T20:29:52.886Z
---
PR #14 ambiguity 1. A basin must be defined for a fully specified deterministic quench on configuration space quotiented by square relabelling, each square's quarter-turn symmetry, and container D4. The current two-hash endpoint key assumes isolated minima and splits positive-dimensional terminal families. The exact n=3 family with centres (1/2,1/2), (3/2,1/2), (t,3/2), t in [1/2,3/2], has side 2 and one contact certificate but many geometric keys. Acceptance: distinguish observations, isolated terminal points, and connected terminal components; compute active-constraint rank/nullity after quotienting discrete symmetries; continue every detected null direction and identify connected stationary strata; preserve boundary strata where contact graphs change; make component-level attraction probability the counted object; and add the n=3 family as a regression that cannot inflate basin count with a finer quantum. Until this passes, small-n outputs are called endpoint clusters, not basin counts.
