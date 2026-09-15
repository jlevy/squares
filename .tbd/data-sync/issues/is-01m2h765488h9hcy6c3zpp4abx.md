---
type: is
id: is-01m2h765488h9hcy6c3zpp4abx
title: Extract or retire JavaScript in the video spike tools
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:06.023Z
updated_at: 2026-09-15T00:24:19.609Z
---
Extract, or delete where obsolete, every JavaScript string in the video spike tools under `packing/atlas/known-best/video/spikes/`. About 600 lines:

- `v1-slideshow/build_candidate.py`: a 279-line page script held as a Python constant, which becomes a `.js` asset the build inlines;
- `v1-slideshow/render_review.py` (108);
- `v2-transitions/`: `grade_motion.py` (67), `measure_standardize.py` (33), `smoke_styles.py` (32), `measure_law.py` (20), `measure_stall.py` (20), `compare_palette.py` (19), `calibrate.py` (8) and `measure_optimize.py` (6).

Before extracting, check `think-cqfc`'s consumer inventory: a spike tool with no consumer can be deleted instead, but only after any unique assertion it carries is preserved. Acceptance: these files leave the allowlist, and the retained tools still run.
