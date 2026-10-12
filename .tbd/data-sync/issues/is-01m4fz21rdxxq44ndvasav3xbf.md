---
type: is
id: is-01m4fz21rdxxq44ndvasav3xbf
title: Maintained builder for the couzo-extended-ordinary-source-v1 preparation (OR-1)
kind: task
status: open
priority: 3
version: 3
delegate: null
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T09:14:12.109Z
updated_at: 2026-10-09T20:40:40.366Z
started_at: 2026-10-09T20:39:30.221Z
---
#466 review B5: no maintained code builds the preparation couzo_extended_reports --check-ordinary/--export consume. Builder would read a local bare fetch of the three pins (git ls-tree -r -l -z --full-tree, cat-file commit/blob; GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1, hooks off), write canonical JSON via canonical_custody/input_order as one XZ stream under MAX_COMPRESSED_BYTES, and run check_ordinary before writing. Needs a security pass (adds a git subprocess), integrity-ceremony note, synthetic git-repo test.
