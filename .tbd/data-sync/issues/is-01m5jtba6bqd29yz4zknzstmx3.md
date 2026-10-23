---
type: is
id: is-01m5jtba6bqd29yz4zknzstmx3
title: Keep shared navigation stable before first paint
kind: bug
status: closed
priority: 1
version: 3
delegate: navigation-components
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T22:05:17.897Z
updated_at: 2026-10-22T22:30:28.314Z
started_at: 2026-10-22T22:05:25.525Z
closed_at: 2026-10-22T22:30:28.314Z
close_reason: Unified category label-and-chevron controls and prepaint navigation geometry implemented and reviewed. Navigation/Workbench 21 tests, seven-alias redirect regression, five paper-shell checks, typography check and 19 bootstrap Node tests pass. No open senior-review findings; integrated CI and local rebuild tracked separately under think-kmpp.
resolution: null
duplicate_of: null
---
PR737 final-head Pages validation reports CLS 0.508 desktop and 0.692 mobile in the standalone explainer. Diagnose navigation/bootstrap initial geometry and fix at source while preserving no-script destinations; retain the existing CLS ceiling and validate desktop/mobile in both themes.
