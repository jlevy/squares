---
type: is
id: is-01m2nf9ahn8sf67khhfcwqhxrc
title: Reject incoherent suite-file cost report sets
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:02:36.212Z
updated_at: 2026-09-16T16:02:36.212Z
---
PR #185 review suggestion: devtools.suite_files record should reject missing or duplicated shards and reports mixed across run id, attempt, SHA, or shard count before regenerating suite-file-costs.json. Add negative controls for partial and mixed report sets.
