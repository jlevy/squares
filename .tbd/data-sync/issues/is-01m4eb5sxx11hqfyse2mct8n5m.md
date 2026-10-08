---
type: is
id: is-01m4eb5sxx11hqfyse2mct8n5m
title: Reclaim large inactive generated builds with fdu and trash
kind: chore
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T18:07:29.212Z
updated_at: 2026-10-08T18:20:24.968Z
started_at: 2026-10-08T18:07:44.662Z
closed_at: 2026-10-08T18:20:24.965Z
close_reason: "Bounded audit complete: no eligible large build output; preserved active and unique data; zero staged."
resolution: null
duplicate_of: null
---
User requests disk-space cleanup of large expendable builds via fdu and trash. Verify generated ownership, inactive task/process state and recoverability; preserve all source, active environments and unique evidence. Record exact paths, measured bytes and df changes; never permanently empty Trash.

## Notes

Bounded user-authorized fdu/trash audit completed. No eligible generated build artifact >=1GiB in selected internal worktrees/temp or released old Cargo paths; zero bytes staged. ActiveQA with7930 open directoryhandles and active runtimes/evidence preserved. trash listings empty, never emptied. df internal420->329MiB/external4.6->3.4GiB, concurrent losses not attributable to audit. Partial usertemp scan documented. Other activecleanup owns packagecaches; avoid overlap. Receipt: attic/n17-six-hour-engineering/issue-followthrough-20261008/disk-cleanup-20261008.md. No source/Git/process changes by audit agent.
