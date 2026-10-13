---
type: is
id: is-01m4vqkbtp0f8jhs1982xakb8v
title: Diagnose macOS full-suite font, glyph and proof-fixture failures
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T22:54:44.047Z
updated_at: 2026-10-13T22:56:40.304Z
started_at: 2026-10-13T22:56:40.303Z
---
The docs-only site-changelog plan push validation at d5e956cc5 passed 12 prerequisites and 5124 tests but had 12 failures. Complete workspace Node dependencies repaired the three type-floor failures; the exact walker case and isolated SQUISH n=129 rerun pass. Remaining full-suite failures involve macOS font negative control, overview glyph metrics/host font and duplicate proof-fixture move destinations. Compare unchanged baseline df9767225, diagnose suite interference and host controls, and fix/rerun in a separate code slice. Evidence: /Volumes/spud-ext1/agent-scratch/site-changelog-01a13732/tmp/final-push-validation.log. No runtime sources changed in plan PR590; do not represent the local full push gate as passing.
