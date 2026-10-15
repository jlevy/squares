---
type: is
id: is-01m4znhtfbdwfewvssggm76b6q
title: Require a real writable task scratch directory before closure browser checks
kind: bug
status: in_progress
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zmmp3v11y25f6b8c6fjgvq
hold: null
hold_until: null
created_at: 2026-10-15T11:35:54.090Z
updated_at: 2026-10-15T11:36:27.774Z
started_at: 2026-10-15T11:36:27.773Z
---
Local News browser validation first skipped and then correctly failed when Chromium was required: TMPDIR pointed to a task tmp subdirectory that had not been created. Create dedicated external tutorial-closure scratch/tmp/Cargo/cache directories after verifying the mounted volume, verify TMPDIR exists and is writable before launch, rerun the four existing browser cases with pinned Chromium required, preserve skipped/error receipts and report only the final executed pass. Do not change assertions or browser availability refusal.
