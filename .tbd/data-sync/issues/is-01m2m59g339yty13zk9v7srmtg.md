---
type: is
id: is-01m2m59g339yty13zk9v7srmtg
title: "PR #180 review R2: TypeScript coverage ignores effective exclusions"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/180
    at: 2026-09-16T03:50:01.539Z
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-16T03:48:41.697Z
updated_at: 2026-09-16T03:50:01.540Z
closed_at: 2026-09-16T03:48:46.692Z
close_reason: "Fixed in 738f2c7c. Coverage now reads tsc --listFilesOnly and a negative control proves exclude removes a file. Full browser-floor contract: 38 passed."
resolution: null
duplicate_of: null
---
Formal review finding for PR #180. packing/tests/test_browser_floor_contract.py derived coverage from raw include globs, so exclude/files could remove tracked source from tsc while the contract stayed green. Coverage must use TypeScript's resolved program and carry a negative control.
