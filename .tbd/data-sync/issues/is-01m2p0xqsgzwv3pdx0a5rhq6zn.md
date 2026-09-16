---
type: is
id: is-01m2p0xqsgzwv3pdx0a5rhq6zn
title: Visualize and control guidance tiers in the workbench
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench
  - animation
dependencies: []
parent_id: is-01m2p0wmnwn2dt3qnxwj4wwses
created_at: 2026-09-16T21:10:50.926Z
updated_at: 2026-09-16T21:24:15.047Z
closed_at: 2026-09-16T21:24:15.046Z
close_reason: Workbench control, overlay, replay-parity, and render-cost requirements moved to the existing Pack/Search product owner think-czav.
resolution: duplicate
duplicate_of: is-01m2gxkxbhyqesd394p4ezr66c
---
Expose the same backend guidance target and strength/schedule configuration in the workbench without a separate visual-only model. Provide controls for guidance tier, strength, schedule, and target source; overlay component membership, requested versus realized contacts, oriented face assignments, mismatches, and current guidance forces. Loading a retained CLI configuration must reproduce the same deterministic trajectory and metrics in the browser, with bounded rendering cost and truthful disabled states.
