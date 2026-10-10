---
type: is
id: is-01m4hmxhc5s8btgpddky43pjhg
title: "PR477 B1: restrict retained SVG fill tokens"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4hm1cmpng01wvmzqh5dj415
hold: null
hold_until: null
created_at: 2026-10-10T00:55:27.360Z
updated_at: 2026-10-10T01:28:25.508Z
started_at: 2026-10-10T00:58:08.887Z
closed_at: 2026-10-10T01:28:25.507Z
close_reason: "B1 fixed and pushed at 9b9635a2ba59672837d79a492feea921de88c5fb. Illustration fills now require a full six-digit hexadecimal colour match; escaped URL regression failed before the fix and passes after it. Figure/renderer tests: 27 passed, 2 skipped; Ruff and BasedPyright zero findings. Coordinator native pre-push tier: all 66 selected steps passed, 4245 normal tests passed and 37 skipped. Fixed disposition: https://github.com/jlevy/squares/pull/477#issuecomment-6092180511. Root owns synchronization and final hosted all-107 checkpoint."
resolution: null
duplicate_of: null
---
Dedicated security review B reproduced an escaped CSS url() fill reaching Chromium as an external request. Restrict retained polygon fills to the inert color syntax required by the figures, add refusal regressions, and post a fixed disposition tied to the repair commit. Existing source colors and generated geometry must be preserved.
