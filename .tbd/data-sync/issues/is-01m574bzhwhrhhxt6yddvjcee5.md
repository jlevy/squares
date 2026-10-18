---
type: is
id: is-01m574bzhwhrhhxt6yddvjcee5
title: "PR #661: re-pin data after review D corrections"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573danqmx1gv9fe3vh2xsbe
hold: null
hold_until: null
created_at: 2026-10-18T09:09:32.345Z
updated_at: 2026-10-18T09:09:49.120Z
started_at: 2026-10-18T09:09:49.119Z
---
Run 39113550886 suite-b job 117634573500 fails only tests/test_release.py::test_the_pinned_data_revision_is_the_last_data_commit: data_revision is 9783a53a22d753c3997d2f2c0f435b9176c3925f while DATA_REVISION remains bcfe8aaa0196eb8adb2e80e72d7d6df0b9fc9676. Use release_pin --update, keep drawn asset provenance unchanged, test pin and release contract. Frontend job 117634573394 separately reports atlas no-script resize alignment.
