---
type: is
id: is-01m5ac71fmmx0mc5qkt6d9jbmp
title: Audit and safely stage inactive Squares disk artifacts on internal drive
kind: chore
status: closed
priority: 1
version: 4
assignee: internal-disk-reclamation
delegate: internal-disk-reclamation
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T15:24:22.387Z
updated_at: 2026-10-19T15:42:06.114Z
started_at: 2026-10-19T15:24:43.102Z
closed_at: 2026-10-19T15:42:06.113Z
close_reason: null
resolution: null
duplicate_of: null
---
User requested thorough cleanup of disk space no longer needed from our Squares work, especially the nearly full internal drive. Audit existing metadata, all registered worktrees, and generated/temp artifacts; preserve source, unique research and logs, active environments and sessions. Trash-only staging with plan, dry-run, activity recheck and exact manifest. No whole active worktree removal or Trash emptying. Evidence: .codex/intake-resume-20261019/disk-audit-20261019 and external task scratch.

## Notes

Audit child completed and delivered; broader disk-space cleanup remains incomplete where source/app ownership or preservation requires follow-up. Verified Trash staging: only /Users/levy/.cache/fdu, 1,699,840 allocated bytes (2 derived .bin files) -> /Users/levy/.Trash/fdu. Dry-run and actual helper successful; exact manifest /private/tmp/disk-cleanup-squares-internal-20261019-fdu-cache-actual.tsv. Validated names, sizes, mtimes and source absence. Trash unemptied; no physical space reclaimed claimed. Receipt .codex/intake-resume-20261019/disk-audit-20261019/audit-receipt.json. Measured130.6GiB local work/cache,68 registered/nested worktree entries and bounded14 external Squares scratch roots plus internal generated/artifact/app-payload inventories. Partial gaps49 user-temp privacy errors and16 Library/Caches permissions; two abandoned cloud-blocked home scans excluded from totals. Protected all W44/live environments, all source and unique research/evidence/history/databases. Pending Codex update1,861,271,552B can clear after user relaunch at appropriate time; six internal app-managed Squares source worktrees7,132,512,256B require their own recoverable archive/owner context. Metaproc465,223,680B env ownership unresolved, preserved. Current intake evidence50,171,904B preserved by coordinating parent. No source edits, commits, pushes, PRs, merges, lifecycle changes or Trash emptying.
