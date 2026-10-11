---
type: is
id: is-01m457wh74bmyny16eh5tshr0d
title: "Re-record suite-file-costs.json: main's shard 4 sits at the 10% unrecorded threshold"
kind: task
status: closed
priority: 2
version: 4
delegate: null
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-05T05:16:49.764Z
updated_at: 2026-10-06T08:43:36.042Z
started_at: 2026-10-05T07:21:15.340Z
closed_at: 2026-10-06T08:43:36.042Z
close_reason: "Done: the record was rebuilt from complete green four-shard hosted cohorts after this bead was filed: 56298168e (run 37283814485, 2026-10-05 16:35Z), b33376017 and a63005237 on origin/main (packing/devtools/suite-file-costs.json)."
resolution: null
duplicate_of: null
---
On main 6dbd6f69e, `python -m devtools.suite_files check` reports shard 4/4 at 13 of 130 files unrecorded (10.0%), exactly the UNRECORDED_SHARE_WARNING threshold that test_suite_files.py::test_check_passes_on_the_real_tree enforces. Any PR that adds one test file hashing to shard 4 fails suite-d. PR #336 hit it at 1fcb74fdf (run 37266380194, job 111623996216) and renamed its test to test_windows_supervision.py, which hashes to shard 2, rather than re-record: the session that found it could not download the hosted validation-timings-suite-* artifacts, because the egress proxy denies the Actions blob storage host. Remedy, as the check prints: rebuild the record from a complete green four-shard hosted cohort with `python -m devtools.suite_files record REPORT.json ...`, keeping target_ceiling_seconds, as eb8c15a35 did from run 37057794692.

## Notes

2026-10-05 07:23 UTC (bead bookkeeper). Stack 357's CI now fails on wall-time budget verdicts on every layer (tracked by think-umlx: on #347 suite-c 167.4 s vs its 154 s ceiling, recorded 132 s; suite-d 131.5 s vs 131 s). #347's lane is root-causing them; if the cause is a stale suite-file cost record, the re-record here is the fix, from a complete green four-shard hosted cohort. The Actions artifact blob host is still denied from the cloud session, so the cohort must be downloaded elsewhere or the egress allowlist widened.
