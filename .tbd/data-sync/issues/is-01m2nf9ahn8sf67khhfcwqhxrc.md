---
type: is
id: is-01m2nf9ahn8sf67khhfcwqhxrc
title: Reject incoherent suite-file cost report sets
kind: task
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:02:36.212Z
updated_at: 2026-09-17T16:07:54.086Z
closed_at: 2026-09-17T16:07:54.083Z
close_reason: "Landed with PR #188 (merge 042e791c, 2026-09-17T15:54Z): hosted aggregates and the Deferred checkpoint passed on 7f387990; review dispositions in https://github.com/jlevy/squares/pull/188#issuecomment-5714064819. The first main push deployed GitHub Pages at 042e791c with verify-deployment passing."
resolution: null
duplicate_of: null
---
PR #185 review suggestion: devtools.suite_files record should reject missing or duplicated shards and reports mixed across run id, attempt, SHA, or shard count before regenerating suite-file-costs.json. Add negative controls for partial and mixed report sets.

## Notes

2026-09-16 evidence audit at da2259fb: SATISFIED (suite_files.py:417-501; test_record_requires_one_complete_coherent_shard_cohort and neighbours in test_suite_files.py:147-245; commits 5ca38b03, 1fae8298). The wrong-shard-count refusal (441-445) lacked a test; one is being added on #188. Close after green exact-head hosted CI.
