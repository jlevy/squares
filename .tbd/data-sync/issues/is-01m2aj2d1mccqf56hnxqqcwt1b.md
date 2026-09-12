---
type: is
id: is-01m2aj2d1mccqf56hnxqqcwt1b
title: Make BC329 readback reconstruct every retained direction
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:36.360Z
updated_at: 2026-09-12T10:22:41.502Z
---
The WIP load_result validates raw, exact, and interval summary fields but does not reconstruct them from the retained per-direction JSON files. Missing, reordered, duplicated, or tampered direction evidence can therefore survive a claimed independent readback. Define a canonical per-direction manifest for all 2,881 raw, 2,881 normalized exact, and 5,761 reflected interval directions; reject omissions, duplicates, unexpected labels, digest changes, malformed witnesses, summary disagreement, and route reordering; recompute minima, argmins, disagreements, enclosures, stalls, and exhaustion counts from those bytes. Add adversarial mutations and a complete synthetic positive control before admission.
