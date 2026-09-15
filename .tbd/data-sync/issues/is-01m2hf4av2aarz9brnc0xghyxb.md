---
type: is
id: is-01m2hf4av2aarz9brnc0xghyxb
title: "capture_video cannot start: prepare sets Pack mode, then the page API refuses setRange"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:42:54.946Z
updated_at: 2026-09-15T03:32:54.626Z
closed_at: 2026-09-15T03:32:54.625Z
close_reason: "Fixed on PR #160 in fc8079df: the capture baseline (capture-control prepare) enters Animate first and stays there; check_animate_view runs prepare from the Pack tab, and squares-workbench-capture --from 2 --to 4 wrote 103 frames and its receipt against a freshly built page."
resolution: null
duplicate_of: null
---
Found 2026-09-14 by PR #160 review lane D-tools while fixing D50, and not fixed there (the files belong to lane D-page).

A real `capture_video` run cannot start at the #160 head, and the base version fails the same way. `prepare` in `packages/workbench/src/api/capture-control.ts:84-103` calls `setMode("pack")` and then `setRange`. While the Pack panel is visible, the `atlasTransitions` Proxy in `packages/workbench/src/application.js:5372` refuses every call, so `prepare=True` throws before the first frame is taken.

`capture_stills.py` and `smoke_capture.py` also call `prepare`, so they probably fail too; they were not run.

The capture path was verified with a scratch script that works around `prepare`, over n = 2 to 4: 103 frames, and ffprobe shows both metadata tags. Nothing in the repository relies on that workaround.

Done when `squares-workbench-capture --from 2 --to 4` produces a video and receipt against a freshly built page, and a check that runs `prepare` exists.
