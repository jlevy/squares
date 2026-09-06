---
type: is
id: is-01m1sd4d4a37f6kf2hfb93xg0a
title: "BC-215: stop re-running expensive gate work whose inputs have not changed"
kind: task
status: open
priority: 0
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
created_at: 2026-09-05T18:26:13.770Z
updated_at: 2026-09-06T17:45:03.001Z
---

## Notes

W5 Phase 3 now includes explained exhaustive-family planning before any skip, complete input/node manifests, trusted reusable receipts, end-of-run source checks, and a complete fresh-plus-reused coverage union. See docs/project/reviews/review-2026-09-06-change-scoped-exhaustive-validation.md for PR94/95/96 timing evidence, focused contract obligations, exact files, invalidation fixtures, and project/upstream doc matrix. First slice fixes repository-relative configuration fallback but does not enable family reuse. Also retain the concrete n40 duplicate: exhaustive test_the_record_round_trips and named assessor --check both recompute assess(); preserve both until aggregate coverage and cheap CLI equality/drift/missing/read-only fixtures justify removing one execution.
