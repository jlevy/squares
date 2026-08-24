---
type: is
id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
title: "H-010: reproduce the Stromquist falsifier triple"
kind: task
status: in_progress
priority: 1
version: 10
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxca8pjaj4v9jwww1kvg
child_order_hints:
  - is-01m0spchq2d2nh2n6m5y713t3r
  - is-01m0sqkws4xy2k3w33f5qepq5j
  - is-01m0sqkx2s29x73e34jkyszbn2
  - is-01m0sqkxbpmad9hq69qcb2rw4d
  - is-01m0sqkxmqxgbg5q29xmwcwhdc
  - is-01m0srbdq4h0zk1ngg3vckf03m
created_at: 2026-08-23T01:39:37.782Z
updated_at: 2026-08-24T11:26:36.247Z
---
Execute H-010 as a source-faithful known-answer reconstruction of Stromquist Theorem 2. The target is not a standalone 12-point unavoidable set. Acceptance: bind the exact Figure 13 ten-point set to the primary PDF; verify that its complement localizes an avoiding unit square to the top or bottom exceptional rectangle up to symmetry; certify with Lemmas 4 and 6 that that same square contains all three A-points from Figure 14; verify the nine remaining points and region partition make the 12-point set unavoidable; and replay the pigeonhole contradiction that 11 pairwise interior-disjoint squares cannot cover 12 points when three share one square. Every numerical search leg is only a falsifier and cannot pass without a separate exact or interval certificate. Include boundary and source-transcription mutation controls.

## Notes

2026-08-24 execution started after exp-014/015. Primary-page inspection found the cleaned transcription has the wrong four defining Figure 13 coordinates; think-abdh and D-146 own that correction. H-010 remains invalid until the point set, figure partition, conditional cohabitation, and final count are all reproduced from the corrected primary geometry.
