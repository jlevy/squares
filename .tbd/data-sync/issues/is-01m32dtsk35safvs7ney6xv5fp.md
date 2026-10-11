---
type: is
id: is-01m32dtsk35safvs7ney6xv5fp
title: Retain the Kleddamag n=17 artifact under the archive convention
kind: task
status: open
priority: 1
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
child_order_hints:
  - is-01m32f1hew684z85fk6c5d9g2x
hold: null
hold_until: null
created_at: 2026-09-21T16:47:19.139Z
updated_at: 2026-10-05T05:40:47.026Z
started_at: 2026-10-05T05:34:33.044Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Retain the external source following the convention the existing n=17 intake used (packing/resources/web/n17-weighted-certificates-2026-09-20/ with receipts), not an invented one: directory naming, receipts, hashing, the archive annotation census in packing/resources/README.md, and whatever .flowmarkignore requires for archived source.

Currently the clone lives only in the gitignored attic, so it is not retained at all and would not survive the container.

## Notes

Reopened: Reopened 2026-10-05: closing it left open children under a closed parent, which devtools.check_bead_tree refuses. The parent's own work is adopted (see the close reason), but its open children need their own disposition before it closes.
