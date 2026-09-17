---
type: is
id: is-01m2nf9ahn8sf67khhfcwqhxrc
title: Reject incoherent suite-file cost report sets
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:02:36.212Z
updated_at: 2026-09-17T02:06:21.351Z
---
PR #185 review suggestion: devtools.suite_files record should reject missing or duplicated shards and reports mixed across run id, attempt, SHA, or shard count before regenerating suite-file-costs.json. Add negative controls for partial and mixed report sets.

## Notes

2026-09-16 evidence audit at da2259fb: SATISFIED (suite_files.py:417-501; test_record_requires_one_complete_coherent_shard_cohort and neighbours in test_suite_files.py:147-245; commits 5ca38b03, 1fae8298). The wrong-shard-count refusal (441-445) lacked a test; one is being added on #188. Close after green exact-head hosted CI.
