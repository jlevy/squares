---
type: is
id: is-01m1z694scw2vnhs9rdetpmfe8
title: "Phase 2: capture tool and the first Version 1 video"
kind: feature
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z69by99pw12bxj1kf1p0g5
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:21:55.619Z
updated_at: 2026-09-09T04:10:08.854Z
---
devtools/capture_known_best_video.py: headless-shell launch as render_explainer_pdf does (SQPACK_CHROMIUM honoured), fixed viewport and device scale factor 1, seek(k/fps) loop with stateKey deduplication into an ffmpeg concat list, H.264 MP4 and VP9 WebM encodes with the host or runner ffmpeg (the bundled ffmpeg-1011 is VP8 only), <stem>.receipt.json (player sha256, commit, mode, timeline, viewport, Playwright version, browser revision, ffmpeg version and args, frame counts, intermediate_frames statement) and <stem>.timings.json (per-frame ms, encode wall, host shape); --stand-in (three frames) and --check (self-agreement in one browser). Measure per-frame cost at 1920x1080 and 3840x2160 and record both. .github/workflows/video.yml: stand-in on pull requests under CAPTURE_INPUTS with the filter test, full capture and release upload on workflow_dispatch. First full slideshow capture on the host for the owner's review. Decisions D8, D9, D14.

## Notes

Updated 2026-09-08 after Phase 0's drift was recorded.

This bead is the 'capture pipeline that turns Animate into a video file'. It is not a new bead: it is this plan's own Phase 2, and it stays here rather than moving to the workbench epic (think-qn6l), because capture, receipts and publication are video artefacts and the plan owns those.

What changed around it. Phase 0's Version 2 prototype became a solver workbench with three modes, and the one that renders a range of n at speed with nobody intervening -- this video -- is now called Animate (it was called Sweep until 2026-09-08; Calibrate is the mode that sweeps, over parameters). The prototype is the current best expression of what this bead will capture, but it is not the retained player: this bead captures from the deterministic player Phase 1 builds, under the CSP, the seek clock and the stateKey deduplication D8 specifies, and the prototype's own capture loop is reference rather than the thing.

Two facts measured on 2026-09-08 that bear on this bead. The page is not slow: 120 fps headless at n = 17 and n = 272, worst frame 10 ms, 358 DOM nodes, 10.7 MB heap, every API call under 2 ms -- apparent sluggishness during that session was a five-minute load average of 116 from another session, not the page, so nothing in the capture budget needs reopening for draw cost and the screenshot remains the cost, as D8 measures. And decision D16, new: snapping to the retained poses is production correctness for Animate and evidence of nothing, so no capture, receipt or caption may present a settled frame as a solver result.

Related: think-qn6l is the workbench epic; the solver, its modes and its research questions live there.
