---
type: is
id: is-01m5att01xzbf0scps5z4rykw9
title: "validate.py: PYTHONUNBUFFERED is not set without an artifact directory, so a deadline kill can drop buffered output"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-19T19:39:23.580Z
updated_at: 2026-10-19T19:39:23.580Z
---
PR #685 Review D3 (Low). _run sets PYTHONUNBUFFERED=1 only when PACKING_VALIDATION_ARTIFACT_DIR is set (~:1179); the pipe path (~:1106) does not, so a local deadline kill can lose up to ~8 KB of buffered Playwright SEND/RECV lines. CI always sets the directory; local diagnosis only.
