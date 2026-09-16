---
type: is
id: is-01m2mac3pw1btsww51ace8w2wf
title: "PR #175 follow-up: a local helper can return an unread script without classification"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T05:17:30.196Z
updated_at: 2026-09-16T05:54:32.705Z
closed_at: 2026-09-16T05:54:32.704Z
close_reason: Local helper returns now fail closed unless every possible return is loader-backed; negative and positive controls pass at pushed head d96f821c.
resolution: null
duplicate_of: null
---
The reconciled guard treats a call to a local function as opaque unless one returned expression is directly literal text. A local build function returning Path.read_text can therefore pass to page.evaluate even though a direct read_text call is refused. Classify all returns from locally defined functions: accept only an all-loader result; otherwise fail closed. Add a signature-free negative contract.
