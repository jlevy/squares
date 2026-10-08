---
type: is
id: is-01m4evbpg3qb1f5xa9h4t4wa14
title: Measure atlas raster exports using resolved poster dimensions
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T22:50:19.522Z
updated_at: 2026-10-08T22:50:30.634Z
started_at: 2026-10-08T22:50:30.633Z
---
Independent poster review found that measure_release_assets._atlas_rasters reads unhydrated atlas.COMPOSITES and would force the new narrower SVG into the old8347x4766 raster size. Use resolved_composites for actual physical dimensions, and add a clone-free regression that captures requested export dimensions without invoking Cairo. Keep100-grid sizing and generic geometry semantics intact. This finding is part of the narrowed-poster variant review; verify the maintained cost measurement uses the same geometry as publication exports before PR validation.
