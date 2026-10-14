---
type: is
id: is-01m4t0sxy4j08amh5mdkwpms8y
title: "PR #579 C14: pinned_blobs recognizes only 40-hex blobs in packing/devtools/*.py; consider a pin manifest"
kind: bug
status: closed
priority: 4
version: 3
delegate: claude-address-pr579-0vpobe
labels: []
dependencies: []
parent_id: is-01m4t0rz9mprhgavf522e0cvcm
hold: null
hold_until: null
created_at: 2026-10-13T06:57:07.524Z
updated_at: 2026-10-13T07:45:27.773Z
started_at: 2026-10-13T06:57:11.611Z
closed_at: 2026-10-13T07:45:27.773Z
close_reason: "Declined on PR #579 (https://github.com/jlevy/squares/pull/579#issuecomment-6140818286): the 12-hex blob in independence-record.yaml is a historical note, not a binding; the one blob-binding tool names full hashes under packing/devtools/, which pinned_blobs reads; a declared pin manifest is a design change with no current consumer."
resolution: canceled
duplicate_of: null
---
Review C finding C14 (Suggestion) on PR #579 at head 2a8ce4aea. Refs: packing/devtools/move_documents.py:48-50,84-90. Review: https://github.com/jlevy/squares/pull/579#pullrequestreview-5499806599
