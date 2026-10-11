---
type: is
id: is-01m4m61h43ajxan7q3kn2b3n4n
title: Repair case math-face and result-dialog title browser oracles
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4m588mffw9ac4ssy5qa9hhd
hold: null
hold_until: null
created_at: 2026-10-11T00:33:12.834Z
updated_at: 2026-10-11T00:37:31.678Z
started_at: 2026-10-11T00:33:33.887Z
closed_at: 2026-10-11T00:37:31.677Z
close_reason: Five affected Chromium nodes passed in 35.10s (zzor-five-browser.log). Math-face tests and probes unchanged after neutral case-count fix. Popover test compares canonical text_content and separately asserts standalone uppercase/dialog none, preserving math and accessibility/focus assertions. Scoped Ruff lint/format, Biome, strict TypeScript and diff checks passed. No commit or push.
resolution: null
duplicate_of: null
---
Own test_site_math_faces.py, test_site_result_popover.py and their probes. Preserve serif case-count intent, panel-face checks, canonical title identity, accessible naming and math invariance while reconciling five current frontend failures. Run affected Chromium tests; no commit or push.
