---
type: is
id: is-01m4y09z9p7we8zr1ncvk7ycf8
title: "PR604 F1: reveal percent-encoded News bookmarks fully"
kind: bug
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T20:05:22.347Z
updated_at: 2026-10-14T20:08:41.007Z
started_at: 2026-10-14T20:05:37.045Z
closed_at: 2026-10-14T20:08:40.997Z
close_reason: "Fixed in17ead6a3 and296c65c9; current-head correctness Review F5523939695 confirms both. Four chooser/bookmark and two tooltip desktop/mobile cases pass. Dispositions: https://github.com/jlevy/squares/pull/604#issuecomment-6177309801"
resolution: null
duplicate_of: null
---
Final correctness review F1: encoded low-significance bookmark widened filters but did not expand its card. Fixed by guarded fragment decoding in17ead6a3902615a9fa8fc2abbcd22766e08ae4fa. Four retained browser cases passed; source confirmed at296c65c90fd5f25c0a674abb92e798e02bb721ee.
