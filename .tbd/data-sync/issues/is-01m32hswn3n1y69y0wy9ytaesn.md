---
type: is
id: is-01m32hswn3n1y69y0wy9ytaesn
title: Capture baseline forces tween and anneal 3, so a cut video has no shake
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md
labels: []
dependencies: []
created_at: 2026-09-21T17:56:43.809Z
updated_at: 2026-09-21T18:13:15.846Z
closed_at: 2026-09-21T18:13:15.844Z
close_reason: Capture reads style and anneal back from the page; n=49..51 under physics at shake 9 lands on all three records.
resolution: null
duplicate_of: null
---
The page's Animate view opens on SOLVER 'B · physics' with THE SHAKE annealing at 9 (ANNEAL.dflt). The capture baseline in `packages/workbench/src/api/capture-control.ts` `prepare()` overrides both: `api.setStyle('tween')` and `api.setAnneal(3)`.

Under `tween`, `annealSpan()` in `src/animation/timeline.ts` returns 1 whatever the level, so annealing is inert -- the cut video is a pure block tween with no shake at all, which is not what the page shows anyone who opens it.

The owner's call: a cut video should animate with the page's own defaults, including a light amount of annealing.

Also note the durations disagree: the Animate panel reports '323 steps, 7 min 48 s at this beat' (468 s) while a capture over the same range prices 382.7 s. Work out which is right before changing the baseline -- it may be the same class of defect as D-492.

Do not change `prepare()` blindly: it is the shared baseline for every capture tool (stills, check_animate_view, check_frontend and the rest), so a change to style or annealing may move what those checks assert. Audit the consumers first.
