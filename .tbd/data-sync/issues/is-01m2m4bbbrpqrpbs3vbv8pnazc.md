---
type: is
id: is-01m2m4bbbrpqrpbs3vbv8pnazc
title: "PR #175 review R6: check_probes reads only positional literals"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:13.811Z
updated_at: 2026-09-16T04:10:13.930Z
closed_at: 2026-09-16T04:10:13.930Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
packing/devtools/check_probes.py:150. probe(ROOT, name="newgroup/absent") is reported by neither branch of name_faults. Fix: include node.keywords values in literal_calls. (PR #175, review 5218208204)
