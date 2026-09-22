---
type: is
id: is-01m336y682k19wzvvppep4jh36
title: Resaturation shows other hues between grey and the settled color
kind: bug
status: closed
priority: 0
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T00:06:04.801Z
updated_at: 2026-09-22T01:18:11.678Z
closed_at: 2026-09-22T01:18:11.677Z
close_reason: "Fixed at 06029438e. Cause: the rest color switched from n's packing to n + 1's at moveEnd, after the hue had already come back, so a square returned from grey in its OLD hue and turned to the new one a few frames later (traced into 11, square 5: yellow, grey, yellow, pink; and a grey that climbed to the old shade then dropped one in a frame). The rest color now turns while the hue is gone (homeLevel, shared by both renderers). check_transitions' hue_turns and lightness_jumps rules hold it; --all passes."
resolution: null
duplicate_of: null
---
Owner's report: desaturating is smooth, saturated to grey. Resaturating is not: between grey and green other hues appear -- yellow again, and blue. The two directions are not mirror images.

Suspects, to be measured rather than assumed: hueLevel's return and chromaLevel's return are separate ramps, and the hue rotation is meant to finish INSIDE the grey before chroma returns. If the hue is still rotating while chroma comes back, every intermediate hue on the rotation's path shows. The drain-out side does not have this problem because chroma leaves before the hue does.

Reproduce with the transition contract checker; fix so the return is the mirror of the leave.
