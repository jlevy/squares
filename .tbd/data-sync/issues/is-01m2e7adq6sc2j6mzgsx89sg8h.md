---
type: is
id: is-01m2e7adq6sc2j6mzgsx89sg8h
title: Prevent PR156 validation from exhausting internal temp space
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
  - n11
dependencies: []
parent_id: is-01m2e0e4ct972w6eapcr8c3xjz
created_at: 2026-09-13T20:28:42.596Z
updated_at: 2026-09-13T20:39:48.041Z
---
The corrected PR156 --push gate ran with internal APFS Data at 101 MiB free and another exact-head pytest could not create a temporary directory; T2 Git commit also returned ENOSPC. After the gate exited, free space recovered to 838 MiB. Diagnose which gate or pytest temp artifacts caused the transient pressure and retain bounded output/cleanup so validation can complete on the host. Do not delete research records, agent sessions, worktrees, or active caches. Use the disk-recovery skill and distinguish logical candidate size from physical df change. No external export of private session metadata without explicit authorization; auto-review rejected that attempted receipt location.

## Notes

2026-09-13 20:39 UTC follow-up: internal APFS Data free space recovered without cleanup to 4.2 GiB while one bounded-output standalone reachable test rerun ran. No Trash staging/deletion occurred. The gate failure cause is still unproven; the rerun captures exact failure text and will distinguish a source/test failure from transient host pressure. Do not infer a pass from the disk recovery.
