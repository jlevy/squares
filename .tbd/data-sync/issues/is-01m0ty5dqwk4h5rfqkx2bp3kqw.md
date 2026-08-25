---
type: is
id: is-01m0ty5dqwk4h5rfqkx2bp3kqw
title: Preserve final receipts from delegated long-running commands
kind: bug
status: open
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T22:27:25.563Z
updated_at: 2026-08-25T07:19:12.541Z
---
The serialized PACK_JOBS=1 deep-golden validation completed before its 180-second cap, but the delegated execution path returned neither stdout/stderr nor exit status. The run is inadmissible. Record as D-202; rerun once through a parent-owned durable session that preserves output, exit status, timing, and process cleanup. Update the portable runbook so long commands must retain a final receipt rather than infer completion from process disappearance.

## Notes

The first delegated PACK_JOBS=1 command finished before 180s but returned no stdout or exit status, so it was discarded. One parent-owned durable-session rerun retained full output, real/user/sys timing and exit=1 at 79.66s. Repository runbook policy still needs the same final-receipt requirement before this bead closes.
