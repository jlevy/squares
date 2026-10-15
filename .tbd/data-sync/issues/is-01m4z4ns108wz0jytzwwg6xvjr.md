---
type: is
id: is-01m4z4ns108wz0jytzwwg6xvjr
title: "Main red: check_results in a worker cannot find T-185/T-186 identity.measured_in (PR #612)"
kind: bug
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-15T06:40:57.888Z
updated_at: 2026-10-15T08:35:15.231Z
started_at: 2026-10-15T06:41:04.612Z
closed_at: 2026-10-15T08:35:15.230Z
close_reason: "Fixed by jlevy/squares#615 (merged): run_negative_controls declares identity.measured_in; fast guard test added."
resolution: null
duplicate_of: null
---
The slow test tests/test_negative_controls.py::test_unmutated_results_checker_is_green_inside_a_worker fails on main c4c690a3e at 13 rows (T-185 at 175, T-186 at its twelve counts): identity.measured_in does not name a file. Both files are compare_lineage-output.txt under packing/resources/web, which the snapshot prunes; since #611 (think-b6ir) the copy-back declares the register's artifacts, controls and reviews but not measured_in, which check_results.regularizations_problems stats. Fix: declare measured_in (results and regularized_drawings) in run_negative_controls._result_paths, and add a fast guard that every path check_results stats reaches a worker.

## Notes

Reproduced on c4c690a3e: 13 problems (T-185 at 175, T-186 at its 12 counts). PR #615 (https://github.com/jlevy/squares/pull/615), head 119852eac: run_negative_controls.result_paths declares identity.measured_in (results and regularized_drawings). Guard: tests/test_snapshot_link_consumers.py::test_every_file_the_results_checker_stats_reaches_a_worker (fails without the fix). Snapshot 212,861,306 bytes, 13,631,110 under the cap (main 212,848,544). Hosted CI on 119852eac: 31 pass, 27 skipped, 0 fail. Not declared: open_review.retained (may be a directory; no entry carries one). Close on merge.
