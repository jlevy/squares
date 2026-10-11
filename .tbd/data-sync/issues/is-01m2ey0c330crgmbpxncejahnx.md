---
type: is
id: is-01m2ey0c330crgmbpxncejahnx
title: "Route B: test a pairwise SDP bound, starting with an n=6 control"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-14T03:05:10.489Z
updated_at: 2026-10-06T08:41:58.717Z
closed_at: 2026-10-06T08:41:58.717Z
close_reason: "Superseded: Route B's pairwise SDP was for an n=11 bound; the pose-cell theta route H-231 'stays retired' (packing/campaign/ideas.md row 202 on origin/main). s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical."
resolution: canceled
duplicate_of: null
---
Test a Lasserre level-2 or Schrijver theta-prime relaxation on a soundly discretized placement graph (de Laat–Vallentin 2015 style). This is one higher-order route to the fractional-versus-integer gap, alongside realizable-trace, geometric-budget, and mixed-resource approaches; compactness is a goal, not an established likelihood. The first n=6 near-side-3 run is a formulation control because the exact packing behavior is solved, not because point-certificate failure there has been proved. Require a sound conflict-edge guarantee, preserve legal n=6 and nine-square-grid controls, certify any numerical SDP verdict rigorously, and compare n=11 only against the strongest matched point-and-threshold baseline. Obstacles include complete pose coverage, symmetry, near-boundary conflict soundness, and independently checkable PSD dual certificates.

## Notes

BC-353 Astra Max correction, 2026-09-14: removed the stale 'only route' claim and the unproved n=6 point-LP-failure premise. Route B remains high-upside but paused behind a formulation/support screen; see review-2026-09-14-n11-post-w5-route-selection.md.
