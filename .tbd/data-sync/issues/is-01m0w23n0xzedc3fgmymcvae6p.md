---
type: is
id: is-01m0w23n0xzedc3fgmymcvae6p
title: Prevent under-scoped defect-status patches from closing the wrong defect
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T08:55:36.220Z
updated_at: 2026-08-25T08:56:45.122Z
closed_at: 2026-08-25T08:56:00.954Z
close_reason: D-039 restored to outstanding; D-256/D-257 corrected with id-scoped edits; D-258 records the transient uncommitted bookkeeping error.
resolution: null
duplicate_of: null
---
D-258. While fixing D-256/D-257, a patch whose context contained only 'status: outstanding' changed the first matching entry, D-034, to fixed; a similarly weak attempted repair then reopened fixed D-042. Coordinator diff inspection caught and restored both before validation, commit, or push. Acceptance: retain D-034 outstanding and D-042 fixed, set D-256/D-257 fixed with id-and-title-scoped patches, preserve this error in the defect log, and inspect exact diffs before committing logbook edits.

## Notes

Closed after restoring D-034 outstanding and D-042 fixed; the earlier close text's D-039 reference was itself corrected in the bead and D-258 before checkpoint.
