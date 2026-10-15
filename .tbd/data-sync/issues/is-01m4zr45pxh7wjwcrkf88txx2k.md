---
type: is
id: is-01m4zr45pxh7wjwcrkf88txx2k
title: Repair poster legend acceptance tests for the current admitted atlas export and numeric-only accents
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4me9gfnc1denbcj8v7veqnp
hold: null
hold_until: null
created_at: 2026-10-15T12:20:52.571Z
updated_at: 2026-10-15T12:21:11.708Z
started_at: 2026-10-15T12:21:11.707Z
---
Final closure pre-push at4dd found two stale assertions in test_known_best_atlas.py: descriptor still requires optimality proof as a red role, and retained poster expected307 exact/17 numeric despite admitted current export308/16. Preserve independent geometry/badge/count assertions; update description controls for gray case labels, numeric-only accents and unmodified badge styling. Record10,930 normalpasses/49skips/1xfail/twofailures and RuffRUF001 rather than calling broadrun green. Incremental final validation must not repeat unchanged corpus without need.
