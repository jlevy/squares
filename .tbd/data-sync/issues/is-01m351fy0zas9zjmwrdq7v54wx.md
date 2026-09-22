---
type: is
id: is-01m351fy0zas9zjmwrdq7v54wx
title: "Make the color transition settings sensible: desaturate over 0.15 s, resaturate over 0.4 s"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T17:09:23.613Z
updated_at: 2026-09-22T17:36:39.623Z
---
The owner (2026-09-22): the four color settings (drain out, drain in, hue out, hue in; COLOR_FADE in packages/workbench/src/application.js, the colors group in assets/template.html) do not make sense to use. Whatever hue in is set to, the color coming back looks fast. Wanted: desaturation over about 0.15 s and resaturation over about 0.4 s, and settings a person can reason about. Likely cause, to be measured: at the default drain level 0 the hue turns while a square is grey, so the two hue settings change nothing visible, and what reads as the hue coming in is the drain in over the last 0.3 s of the step. Review the model with check_transitions --trace at level 0 and above, redesign the controls, and hold the result with the transition contract.

## Notes

Design (2026-09-22, by a read-only lane; waiting on the owner's two questions before implementation).

Findings, measured with check_transitions --trace at drain level 0:
- hue out / hue in never show a hue (chroma 0.000 through both windows); they only glide a square's grey lightness between its rest shade and its moving run's shade (up to dL 0.267, square 2 into 11).
- "The color coming in fast" is drain in: chroma returns over the last 0.3 s, 80% of it in 0.15 s (smootherstep's middle). Grid fills are still pairs: no hue setting runs at all, and drain in only caps the arriving square's crossing (0.105 s in play).
- Defects: the hue fields open blank (updateSegments writes only out/in); AtlasColorFade declares only out/in; assignGroups' restart key omits the fade.

Redesign: two numbers, desaturate (0.15 s) and resaturate (0.4 s), smootherstep ramps at [moveStart, moveStart + D] and [end - R, end]. Hue changes flip inside a ramp at the instant chroma is zero (a new fadeThroughGrey: linear lightness, signed chroma), so they are invisible at any drain level; the rest color turns from n's to n + 1's over [drained, returning] where it has no weight; moving-run merges stay inside that window. The arriving square: red hold (0.1 s floor), then the same two ramps, finishing at end. Too-short steps shrink both ramps proportionally (3:8). No step's length changes; the video's duration is unchanged.

Open questions for the owner:
1. Grid fills (0.46 s in play, 0.21 s after arrival): scale the ramps down (recommended), drop grid fills' unused resize wait and arrival delay (frees about 0.07 s), or lengthen grid fills (about +50 s of video).
2. A moving square's grey: its run's shade (today's look, recommended) or its own lightness (pure desaturation, runs invisible at level 0).

Change list: new src/animation/color-schedule.ts (colorWindows and level functions); colour.ts fadeThroughGrey and paintScene's moving and arriving branches; scene-types arrivalDrain; illustration.ts drops tintProgress for the windows; application.js replaces chromaLevel/hueLevel/homeLevel/tintUntil and the four controls with two; template.html two inputs; workbench-api AtlasColorFade {desaturate, resaturate} and colorWindows(); sweep.js returns the windows; transition_contract gains ramp-aware lightness, chroma-outside-ramps and ramp-timing rules; Node tests color-schedule.test.ts, colour.test.ts, illustration.test.ts; a round-trip check that duration() and schedule() do not move with the fade.
