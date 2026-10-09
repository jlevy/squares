---
type: is
id: is-01m4gzs7rbzw8mywvdfwfe652z
title: Add Fixed Row and Global scale controls to the web atlas
kind: feature
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T18:46:06.344Z
updated_at: 2026-10-09T18:51:39.298Z
started_at: 2026-10-09T18:51:39.294Z
---
Delegate and implement a three-valued web-only Scale option: Fixed retains current same displayed container-size behavior (default); Row scales each packing relative to its logical triangular-row grid side k, so k-by-k containers have equal display size across rows and shorter enclosing sides are smaller within their row; Global scales against the largest enclosing side among cases shown by the atlas instance. Keep PDFs unchanged. Preserve Triangle/Small defaults, Grid/Medium/Large options, logical segments and half-drawing gap, count/legend semantics, uniform row slots and image/caption alignment. Use canonical actual enclosing side data, accessible controls, validated URL/default/bootstrap/no-JS behavior and meaningful rendering/unit tests; avoid unexpected layout shift. Root sole tracker/committer, source web writer disjoint from print author. Publish to current PR474 and rebuild maintained manual preview with exact current-head qualification.
