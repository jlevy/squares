---
type: is
id: is-01m574bzhwhrhhxt6yddvjcee5
title: "PR #661: re-pin data after review D corrections"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573danqmx1gv9fe3vh2xsbe
hold: null
hold_until: null
created_at: 2026-10-18T09:09:32.345Z
updated_at: 2026-10-18T09:14:34.675Z
started_at: 2026-10-18T09:09:49.119Z
closed_at: 2026-10-18T09:14:34.674Z
close_reason: "Fixed the sole suite-b regression in one-line release re-pin a87de0cf735af2f84ce3ffaceb6d4d619bc64d80, pushed to PR #661. release_pin --check and failed release assertion plus five pin-tool tests pass (6 in 2.95s); exact failed atlas browser test passes (1 in33.12s), its source unchanged and previous frontend CI green. Formal CI followup https://github.com/jlevy/squares/pull/661#pullrequestreview-5562276935. Coordinator monitors new hosted CI."
resolution: null
duplicate_of: null
---
Run 39113550886 suite-b job 117634573500 fails only tests/test_release.py::test_the_pinned_data_revision_is_the_last_data_commit: data_revision is 9783a53a22d753c3997d2f2c0f435b9176c3925f while DATA_REVISION remains bcfe8aaa0196eb8adb2e80e72d7d6df0b9fc9676. Use release_pin --update, keep drawn asset provenance unchanged, test pin and release contract. Frontend job 117634573394 separately reports atlas no-script resize alignment.
