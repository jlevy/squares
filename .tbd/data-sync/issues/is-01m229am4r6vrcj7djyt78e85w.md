---
type: is
id: is-01m229am4r6vrcj7djyt78e85w
title: Split Pack and Animate cleanly in the workbench prototype
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:12:53.143Z
updated_at: 2026-09-09T05:12:53.143Z
---
The transitions prototype at packing/atlas/known-best/video/spikes/v2-transitions/ conflates two modes. Pack is one n and is a workbench for a single packing; Animate is many n and exists to show the flow end to end. Work: Pack shows all n squares from the first frame (measured: at n=17 the pool holds 17 and 16 are visible, because the previous-packing start withholds the arriving square, which is the transition model leaking in); drop the '16 to 17' step header in Pack; move the solver choice (physics, bodies) out of the step-animation group into the strategy group beside the force law; make the timing, motion-phasing and full-beat controls Animate-only; drop tween from Pack entirely, since tween is an animation technique and does not help pack anything. Rename Sweep to Animate in the internals as well as the label, keeping setMode('sweep') as a deprecated alias, because Calibrate is the mode that sweeps and two modes called sweep would be permanently ambiguous.
