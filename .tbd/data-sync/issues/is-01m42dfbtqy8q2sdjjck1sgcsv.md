---
type: is
id: is-01m42dfbtqy8q2sdjjck1sgcsv
title: Keep PR 305 and stacked PR 323 merge-ready until the owner merges them
kind: task
status: closed
priority: 1
version: 2
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-04T02:56:46.423Z
updated_at: 2026-10-06T08:23:41.434Z
closed_at: 2026-10-06T08:23:41.433Z
close_reason: "Done: PR 305 and stacked PR 323 both merged on 2026-10-04 (e19be6bb0)."
resolution: null
duplicate_of: null
---
The owner accepted the T-007 review and wants PR 305 merged, then PR 323 (relayed 2026-10-04 by the import coordinator session). Main merged #315, #330, #332 and #319 after session-169's close, so PR 305 conflicted. Fifth merge: 6f320b32c (#315, #330, #332; five conflicts), re-pin 58621d6fa, 498258a9f (#319, clean); --records, --edit, --sweeps and 1,157 tests passed. No new result ids, so this branch's results stay T-083..T-087. Then PR 323 catches up: main's measure-verifier census JSON files are new and large, so the layout check needs them re-laid or allowlisted. Do not merge either PR; report each head SHA when green and clean.
