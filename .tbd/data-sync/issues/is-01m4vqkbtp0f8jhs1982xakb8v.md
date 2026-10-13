---
type: is
id: is-01m4vqkbtp0f8jhs1982xakb8v
title: Diagnose macOS full-suite font, glyph and proof-fixture failures
kind: bug
status: open
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T22:54:44.047Z
updated_at: 2026-10-13T22:56:44.261Z
started_at: 2026-10-13T22:56:40.303Z
---
The docs-only site-changelog plan push validation at d5e956cc5 passed 12 prerequisites and 5124 tests but had 12 failures. Complete workspace Node dependencies repaired the three type-floor failures; the exact walker case and isolated SQUISH n=129 rerun pass. Remaining full-suite failures involve macOS font negative control, overview glyph metrics/host font and duplicate proof-fixture move destinations. Compare unchanged baseline df9767225, diagnose suite interference and host controls, and fix/rerun in a separate code slice. Evidence: /Volumes/spud-ext1/agent-scratch/site-changelog-01a13732/tmp/final-push-validation.log. No runtime sources changed in plan PR590; do not represent the local full push gate as passing.

## Notes

Bounded baseline evidence: df9767225 font negative control and index glyph test both fail (2 failed, 75.69s), matching plan run. Font CLS 0.002871777 vs required >0.1; glyph report includes Grid tab 15.2px vs15.7327px and host LucidaGrande. SQUISH129 individually and129+179 together pass (pair5.50s), duplicate destinations remain full-suite-only. All3 browser-floor tests plus exact walker alias pass in15.28s after complete workspace Node installation. No production edits. Follow-up should diagnose macOS controls and suite interference; planPR590 remains docs-only.
