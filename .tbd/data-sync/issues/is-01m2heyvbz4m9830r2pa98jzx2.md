---
type: is
id: is-01m2heyvbz4m9830r2pa98jzx2
title: "PR #160 review D50: capture_video misprices steps, repeats boundary frames and writes no D9 receipt"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:55.262Z
updated_at: 2026-09-15T02:40:55.064Z
closed_at: 2026-09-15T02:40:55.064Z
close_reason: "Fixed on #160 at a093ec7a: steps priced on the continuous beat and checked against range().duration; one clock with no boundary repeats; receipt has transitions_are_packings false with reason, intermediate_frames, commit, dirty, Playwright, browser and ffmpeg versions; +faststart and a metadata comment; no on-frame mark; atomic encode. Pure-function tests in test_capture_and_export.py."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

`capture_video` priced steps off the single-step beat, wrote none of plan D9's receipt fields or ffmpeg flags, repeated a frame at each step boundary, and nothing said its frames are not packings. Coordinator decision: no on-frame mark; the receipt records `transitions_are_packings: false` with the reason, and the MP4 comment says the same.

Source: #125 F14. Related: think-zvor, think-4yow.

Files: `packages/workbench/tools/workbench_tools/capture_video.py:104-135`, `:204-231`.
