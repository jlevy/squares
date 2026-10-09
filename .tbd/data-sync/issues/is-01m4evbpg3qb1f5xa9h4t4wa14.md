---
type: is
id: is-01m4evbpg3qb1f5xa9h4t4wa14
title: Measure atlas raster exports using resolved poster dimensions
kind: bug
status: closed
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T22:50:19.522Z
updated_at: 2026-10-09T13:44:10.698Z
started_at: 2026-10-08T22:50:30.633Z
closed_at: 2026-10-09T13:44:10.697Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Independent poster review found that measure_release_assets._atlas_rasters reads unhydrated atlas.COMPOSITES and would force the new narrower SVG into the old8347x4766 raster size. Use resolved_composites for actual physical dimensions, and add a clone-free regression that captures requested export dimensions without invoking Cairo. Keep100-grid sizing and generic geometry semantics intact. This finding is part of the narrowed-poster variant review; verify the maintained cost measurement uses the same geometry as publication exports before PR validation.

## Notes

Fixed resolved physical geometry in the retained raster measurement caller. Clone-free regression reproduced the old 8347 x 4766 dimensions and now passes at 6523 x 6090, preserving all 100-grid/custom export sizes. Four focused tests passed; independent senior source re-review is clear. Integrated validation remains in think-142l.
