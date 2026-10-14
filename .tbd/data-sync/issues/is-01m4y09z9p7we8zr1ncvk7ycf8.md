---
type: is
id: is-01m4y09z9p7we8zr1ncvk7ycf8
title: "PR604 F1: reveal percent-encoded News bookmarks fully"
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
created_at: 2026-10-14T20:05:22.347Z
updated_at: 2026-10-14T20:05:22.347Z
---
Final correctness review F1: encoded low-significance bookmark widened filters but did not expand its card. Fixed by guarded fragment decoding in17ead6a3902615a9fa8fc2abbcd22766e08ae4fa. Four retained browser cases passed; source confirmed at296c65c90fd5f25c0a674abb92e798e02bb721ee.
