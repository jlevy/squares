---
type: is
id: is-01m0vnyt4qfetcp5cpyy30m2fq
title: Repair stale current reproducibility commands after packing module migration
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0vnq7t0x9ydha20bpdxmjzk
created_at: 2026-08-25T05:23:14.709Z
updated_at: 2026-08-25T05:37:41.725Z
closed_at: 2026-08-25T05:37:41.724Z
close_reason: Living synopsis, frontier, research reports, active spec and module docstring now use packing-validate or migrated cases/devtools paths; synopsis rejects removed command paths.
resolution: null
duplicate_of: null
---
PR23 removed test.sh, root verify_trump11.py, and root lp_cell.py but current synopsis/frontier/research reproducibility sections still direct readers to those deleted paths. Historical experiment/session provenance should remain verbatim; current operational claims and commands must point to packing-validate or the migrated cases modules, and the defect must be logged.
