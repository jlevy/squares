---
type: is
id: is-01m1hbxbsxavmqd8zmp4v6gyjb
title: Make declared-bound evidence module-aware under duplicate MAX_ names
kind: bug
status: closed
priority: 0
version: 2
spec_path: packing/campaign/agendas/agenda-015-ten-hour-earned-routes-and-guard-repairs.md
labels: []
dependencies: []
parent_id: is-01m1g7btz9tbnfvpxdtkc0rqd1
created_at: 2026-09-02T15:30:59.004Z
updated_at: 2026-09-02T16:34:33.547Z
closed_at: 2026-09-02T16:34:33.546Z
close_reason: Module-aware declared-bound evidence and duplicate-name negative control pass the exact-tree full gate.
resolution: null
duplicate_of: null
---
BC-146 final XHigh audit found devtools.check_declared_bounds flattens attribute references to bare names, so author and independent n54 tests cross-satisfy duplicate MAX_INPUT_BYTES/MAX_COMMENTS/MAX_COMMENT_BYTES/MAX_ASSIGNMENTS/MAX_INTEGER_DIGITS declarations. Add a two-module collision negative control and require qualified/module-resolved evidence so each of all 14 n54 caps is defended by its own implementation's refusal test before publication.
