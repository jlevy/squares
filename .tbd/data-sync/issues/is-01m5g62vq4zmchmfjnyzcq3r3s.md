---
type: is
id: is-01m5g62vq4zmchmfjnyzcq3r3s
title: adopt_houses never rewrites a case's '## The packing' section on adoption (stale finder text at 227, 229, 260)
kind: bug
status: in_progress
priority: 2
version: 2
delegate: coord-intake-1021b
labels:
  - tooling
  - packing
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T21:32:40.548Z
updated_at: 2026-10-21T21:32:42.213Z
started_at: 2026-10-21T21:32:42.213Z
---
Review B3 of #706 (https://github.com/jlevy/squares/pull/706#issuecomment-6327018031), pre-existing: devtools.adopt_houses rewrites the house paragraphs but not '## The packing', so n-260.md still says 'Found by David Ellsworth in 2024' after T-196 and T-223 were adopted; main has the same at 227 since #704 and at 229. Fix the writer so the section names the adopted house's finder and source (or derives it), add a test, and refresh the affected cases with adopt_houses --refresh.
blocked_on: none
