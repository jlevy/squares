---
type: is
id: is-01m4myc8vpg4t7wycn46x9tgp9
title: "PR #406 A3: gate runs only as a workflow step, outside packing-validate and the tier table"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:30.495Z
updated_at: 2026-10-11T18:58:28.216Z
started_at: 2026-10-11T07:39:09.343Z
closed_at: 2026-10-11T18:58:28.214Z
close_reason: "fixed in f18170d94 (packing-validate --push step) and 8811bd763 (tier table). Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Medium. .github/workflows/packing-validation.yml:74-81; development.md Validation Loops not updated; manual pre-commit instruction at development.md:1847. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
