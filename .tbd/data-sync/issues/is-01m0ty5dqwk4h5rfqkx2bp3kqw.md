---
type: is
id: is-01m0ty5dqwk4h5rfqkx2bp3kqw
title: Preserve final receipts from delegated long-running commands
kind: bug
status: open
priority: 1
version: 9
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
child_order_hints:
  - is-01m0wcppfdp4hmb9g7gjwey1qr
  - is-01m0wcy2mq7vfj1adqjvn3jy27
created_at: 2026-08-24T22:27:25.563Z
updated_at: 2026-08-25T12:04:47.894Z
---
The serialized PACK_JOBS=1 deep-golden validation completed before its 180-second cap, but the delegated execution path returned neither stdout/stderr nor exit status. The run is inadmissible. Record as D-202; rerun once through a parent-owned durable session that preserves output, exit status, timing, and process cleanup. Update the portable runbook so long commands must retain a final receipt rather than infer completion from process disappearance.

## Notes

Session-011 order 12 added the portable parent-owned terminal-receipt rule and ran exactly one <=5s yielded command. Session 72108 and chunks 13aa02/4262fe retained both labeled streams, final exit 7, the 5s TERM/1s KILL policy, final polling and cleanup. D-300/think-jygr remains open because gdate rejected --iso-8601=milliseconds and emitted empty start/end fields; elapsed wall is not reconstructed. The phase stopped without retry, so D-202 and D-217 remain contained and this bead stays open.
