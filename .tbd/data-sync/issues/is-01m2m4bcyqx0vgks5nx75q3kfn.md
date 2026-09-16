---
type: is
id: is-01m2m4bcyqx0vgks5nx75q3kfn
title: "PR #175 review R8: the new workbench probe needs the relaxed program"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:15.445Z
updated_at: 2026-09-16T04:10:13.986Z
closed_at: 2026-09-16T04:10:13.986Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
packages/workbench/probes/pack/stage-fits-viewport.js:5 fails strict tsc with TS2531. Fix: null-check the querySelector result. (PR #175, review 5218208204)
