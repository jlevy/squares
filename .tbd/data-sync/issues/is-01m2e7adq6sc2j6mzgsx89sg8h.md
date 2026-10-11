---
type: is
id: is-01m2e7adq6sc2j6mzgsx89sg8h
title: Prevent PR156 validation from exhausting internal temp space
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
  - n11
dependencies: []
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
created_at: 2026-09-13T20:28:42.596Z
updated_at: 2026-10-06T08:35:48.664Z
closed_at: 2026-10-06T08:35:48.664Z
close_reason: "Obsolete: PR #156, whose --push gate exhausted temp space on one host on 2026-09-13, merged on 2026-09-14 (gh: MERGED 2026-09-14T04:24:55Z); the transient disk pressure was host-specific and the BC329 lane it served is superseded. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical."
resolution: canceled
duplicate_of: null
---
The corrected PR156 --push gate ran with internal APFS Data at 101 MiB free and another exact-head pytest could not create a temporary directory; T2 Git commit also returned ENOSPC. After the gate exited, free space recovered to 838 MiB. Diagnose which gate or pytest temp artifacts caused the transient pressure and retain bounded output/cleanup so validation can complete on the host. Do not delete research records, agent sessions, worktrees, or active caches. Use the disk-recovery skill and distinguish logical candidate size from physical df change. No external export of private session metadata without explicit authorization; auto-review rejected that attempted receipt location.

## Notes

2026-09-13 20:39 UTC follow-up: internal APFS Data free space recovered without cleanup to 4.2 GiB while one bounded-output standalone reachable test rerun ran. No Trash staging/deletion occurred. The gate failure cause is still unproven; the rerun captures exact failure text and will distinguish a source/test failure from transient host pressure. Do not infer a pass from the disk recovery.
