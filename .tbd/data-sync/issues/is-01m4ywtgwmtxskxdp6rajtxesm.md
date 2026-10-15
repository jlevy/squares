---
type: is
id: is-01m4ywtgwmtxskxdp6rajtxesm
title: "PR #612 A12: compare_lineage.py should be a devtools tool with a check"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m4ywspmt47ny1en5jnen7c09
created_at: 2026-10-15T04:23:44.787Z
updated_at: 2026-10-15T04:52:47.167Z
---
Suggestion. mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py backs 13 measured identities; OR-1. Review: https://github.com/jlevy/squares/pull/612#issuecomment-6184278979

## Notes

Deferred from PR #612 (review A12). compare_lineage.py in mishapolk-kkt-refinements-2026-10-14/review/ backs 13 measured identities in three packets (T-185, T-186) and runs by hand. Under OR-1 it belongs in devtools with a --check a tier runs, holding each retained compare_lineage-output.txt to a fresh run. Waits on a devtools slice of its own, outside this records PR.
