---
type: is
id: is-01m2hct1ehavcc1vtj0t1vsbqd
title: "PR #125 review D74: motion lab reduced motion regressed"
kind: bug
status: closed
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:20.497Z
updated_at: 2026-09-15T02:13:11.000Z
closed_at: 2026-09-15T02:13:11.000Z
close_reason: "Fixed in a50f986e: !important restored in motion-lab.css's reduced-motion block with reasoned Biome suppressions; test_reduced_motion_outranks_every_transition_in_the_stylesheet fails on the old stylesheet; retained n5-motion-lab.html regenerated."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F34 (Low); triage row D74.

Reduced motion regressed in the motion lab: lint-floor commit c8e852ca removed !important from the reduced-motion block (packing/src/sqpack/motion_lab/assets/motion-lab.css :680-686), and `select, button { transition: ... }` (:112-123) outranks `*`, so those transitions still animate for users who ask for reduced motion.
