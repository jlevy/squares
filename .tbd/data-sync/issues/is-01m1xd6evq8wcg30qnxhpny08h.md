---
type: is
id: is-01m1xd6evq8wcg30qnxhpny08h
title: "Phase 1: frontier case generator for n > 100 with a golden test"
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6ffzyzddb7by875t49z4
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:18.806Z
updated_at: 2026-09-07T07:45:03.384Z
---
New devtools/generate_frontier_case.py drafting frontier/n-NNN.md under SquarePackingCase/v2 from the catalogue transcription and the bound rules in the spec: reported upper from the catalogue, verified upper ceil(sqrt n) (E-basic-grid-upper), lower bounds from Nagamochi (E-nagamochi-lower), status proved only where lower equals upper (k^2, k^2-1, k^2-2), Arslanov Table 4 cross-check as typed conflicts, de Winter claims as unreplayed notes, rigidity null until the screen writes it. Refuses to overwrite a hand-edited record. Golden test: regenerate n = 100 from the same inputs.
