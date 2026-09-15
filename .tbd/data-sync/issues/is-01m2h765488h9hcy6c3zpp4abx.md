---
type: is
id: is-01m2h765488h9hcy6c3zpp4abx
title: Extract or retire JavaScript in the video spike tools
kind: task
status: closed
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:06.023Z
updated_at: 2026-09-15T16:09:06.069Z
closed_at: 2026-09-15T16:09:06.068Z
close_reason: "PR #179 (https://github.com/jlevy/squares/pull/179): the 13 video-spike files leave the allowlist; 12 were extracted to probes and a page asset, and calibrate.py was retired. The candidate page and each kept tool are identity-checked."
resolution: null
duplicate_of: null
---
Extract, or delete where obsolete, every JavaScript string in the video spike tools under `packing/atlas/known-best/video/spikes/`. About 600 lines:

- `v1-slideshow/build_candidate.py`: a 279-line page script held as a Python constant, which becomes a `.js` asset the build inlines;
- `v1-slideshow/render_review.py` (108);
- `v2-transitions/`: `grade_motion.py` (67), `measure_standardize.py` (33), `smoke_styles.py` (32), `measure_law.py` (20), `measure_stall.py` (20), `compare_palette.py` (19), `calibrate.py` (8) and `measure_optimize.py` (6).

Before extracting, check `think-cqfc`'s consumer inventory: a spike tool with no consumer can be deleted instead, but only after any unique assertion it carries is preserved. Acceptance: these files leave the allowlist, and the retained tools still run.

## Notes

2026-09-15, #175 merge-up of the reviewed stack (#171 at b7627cef) into 9f88e4a7: the guard's inventory counts 123 sites in 13 spike files for this bead, unchanged since #175 opened. The allowlist in packing/devtools/embedded-javascript.yaml is authoritative, and 'python -m devtools.check_no_embedded_js --inventory' lists every site. Beyond the files named above it includes dump_fills.py, measure_greens.py and measure_modes.py (v2-transitions). A spike's probes go in its own probes/ directory, which tsconfig.packing-probes.json and devtools.check_probes already cover.



2026-09-15, PR #179 (claude/no-js-spike-tools at 16c3fa34, base claude/no-js-in-python-guard): all 13 spike files have left the allowlist, and the guard reports 337 sites in 29 files. What happened to each:
- build_candidate.py's page script is now v1-slideshow/assets/slideshow.js. It is covered by Biome with no override and by tsc strict through tsconfig.packing-probes.json, and it is typed against probes/atlas-video.d.ts. assets/package.json declares it a classic script, so its "use strict" stays.
- render_review.py now loads 6 probes.
- The ten v2 instruments now load 61 probes.
- calibrate.py was deleted, not extracted. It had no consumer, it dies against today's page (atlasTransitions refuses Pack), and its results are recorded in NOTES Revision 16. The retirement is recorded in the spike README.
Evidence:
- Extraction alone left the candidate page byte-identical.
- After the floor, the page differs only inside its script element.
- render_review's survey of all 324 n and 7 PNGs is byte-identical: old tool on the old page, new tool on the old page, and new tool on the new page.
- test_candidate.py passes.
- Every kept v2 instrument is value-identical against a fixed page copy, with only wall-clock fields masked, and smoke_styles' PNGs are byte-identical.
Left over:
- The allowlist's shared header comment still counts think-53dt at 123 sites. That is shared text, left for the coordinator.
- smoke_styles' 9 stale expectations belong to think-lmf5.
