---
type: is
id: is-01m4x4c9wrx05gx4nsdsajh3ja
title: "#597 review A3: result-import.md misstates the registered case and per-result scope of reply due"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T11:57:18.616Z
updated_at: 2026-10-14T11:57:26.475Z
closed_at: 2026-10-14T11:57:26.475Z
close_reason: "fixed in 8db1905d5: result-import.md states the rule per result, without the impossible registered-since case, and the module docstring says that rung or status (#597 head 8db1905d5)"
resolution: null
duplicate_of: null
---
Review A of #597 (review 5517404240), finding A3 (Low): the rewritten reply-due sentence says an entry can be registered since the last reply that named it, which cannot occur, and omits that namings and statements count only under the same result; the module docstring said "a rung or status" for "that rung or status".
