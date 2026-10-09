---
type: is
id: is-01m4f1dr9rjm9csyhx95q2pm7k
title: Collapse matching publication and revision dates in shared paper fronts
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T00:36:18.359Z
updated_at: 2026-10-09T00:46:44.441Z
started_at: 2026-10-09T00:36:38.536Z
---
PR #458 follow-up: shared HTML/Markdown/PDF paper date display should show Published Month D, YYYY when first publication and revision dates match, while retaining distinct date labels, original-proof dates, and metadata. Add focused regression coverage, update native paper design guidance, refresh preview, Astra review, push and confirm CI.

## Notes

Shared date follow-up committed/pushed 6cec096c2; targeted122passed12optinskips, Ruff/BasedPyright0; native affected HTML/MD/PDF refreshed. Astra ReviewD confirmed preliminaryLow auditfix, no sourcefindings. CI Packing37866116327 validate113613135404 fails only expired suite_d pending_measurement think-t7k5 at UTC9Oct, unrelated to paperdates. Moderate agent is admitting existing authoritative hosted timing into this branch without raising ceilings or extending deadline. Full new-head checkpoint will be rerun after fix; completed oldhead runs receive no finalhead credit.
