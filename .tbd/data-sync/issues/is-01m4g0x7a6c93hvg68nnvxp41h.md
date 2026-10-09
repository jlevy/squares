---
type: is
id: is-01m4g0x7a6c93hvg68nnvxp41h
title: "Follow-up to #464 prune: correct log sentences and cover every pruned file in the test"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-09T09:46:31.110Z
updated_at: 2026-10-09T11:51:09.549Z
started_at: 2026-10-09T10:17:43.517Z
closed_at: 2026-10-09T11:51:09.549Z
close_reason: "Review C corrections landed in #473 (6a0499ba4)"
resolution: null
duplicate_of: null
---
From Review C on #464 (pullrequestreview-5468437708), after #464 lands: (1) run_negative_controls.py comment log says check_gate_budgets opens 'the two workflows defects.md links' but it reads pages.yml and packing-validation.yml, and pages.yml is linked from a docs/ review — name both and their link sources; (2) the new UNREAD_WORKER_OUTPUTS test checks a hand-picked sample of the 130 files — reuse the 2026-10-06 precedent loop that checks every file under each pruned entry; (3) mark the 109.9 MB / 34.4 MB figures as measured before this selection. Also pre-existing worker reds: validate_schemas (resources/web paths not copied) and test_change_scoped_selection (vendor/kpress absent in workers).

## Notes

2026-10-09T10:17Z Commit df55081a7 on #473 (claude/modest-pascal-z3nisd): corrected check_gate_budgets sentence (pages.yml via 2026-09-12 workbench review; packing-validation.yml via defects.md), figures marked pre-selection, test now partitions every file under each UNREAD_WORKER_OUTPUTS entry. 132 tests pass; ruff/basedpyright clean; +668 bytes. Pre-existing worker reds (validate_schemas resources/web; test_change_scoped_selection vendor/kpress) not addressed here.



2026-10-09T11:51Z Landed with #473 at 6a0499ba4.
