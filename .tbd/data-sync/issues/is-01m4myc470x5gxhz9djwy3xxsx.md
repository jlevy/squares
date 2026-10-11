---
type: is
id: is-01m4myc470x5gxhz9djwy3xxsx
title: "PR #406 A2: no transition for files already over 5 MiB on main"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:25.857Z
updated_at: 2026-10-11T18:58:27.399Z
started_at: 2026-10-11T07:39:07.828Z
closed_at: 2026-10-11T18:58:27.395Z
close_reason: "fixed in 0a4a69d5e and f18170d94: paths over the per-blob ceiling at base.sha grandfathered and charged growth; new paths, copies and edited renames refused; migration tracked in think-xeav. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
High. check_added_blobs.py:174-186 and development.md:1854-1855. Owner decision: grandfather paths whose blob at base.sha exceeds the per-blob ceiling; new large blobs on new paths still refused; bead for moving those files to hosted data. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
