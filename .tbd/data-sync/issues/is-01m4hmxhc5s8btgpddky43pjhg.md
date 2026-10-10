---
type: is
id: is-01m4hmxhc5s8btgpddky43pjhg
title: "PR477 B1: restrict retained SVG fill tokens"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4hm1cmpng01wvmzqh5dj415
hold: null
hold_until: null
created_at: 2026-10-10T00:55:27.360Z
updated_at: 2026-10-10T00:58:08.888Z
started_at: 2026-10-10T00:58:08.887Z
---
Dedicated security review B reproduced an escaped CSS url() fill reaching Chromium as an external request. Restrict retained polygon fills to the inert color syntax required by the figures, add refusal regressions, and post a fixed disposition tied to the repair commit. Existing source colors and generated geometry must be preserved.
