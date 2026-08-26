---
type: is
id: is-01m0zn44dcthxvtacdm6d3hct4
title: Reject mixed angle classes in local contact realization or model their frames
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
  - pr-45-review
dependencies: []
created_at: 2026-08-26T18:25:38.219Z
updated_at: 2026-08-26T18:25:38.219Z
---
ContactScaffold preserves arbitrary vertex angle-class colors, but contact_realization validates only wall constraints and then solves every vertex in one shared u/v frame without reading vertex_colors. A two-vertex ('angle-a','angle-b') scaffold is reported locally-feasible. The current retained enumeration is uniform one-angle-class, so current atlas counts are unaffected, but the public bounded solver can silently certify an unsupported mixed-class input. Either require one uniform vertex color in this slice with a typed error/regression, or implement the relative frame semantics.
