---
type: is
id: is-01m2m4bcyqx0vgks5nx75q3kfn
title: "PR #175 review R8: the new workbench probe needs the relaxed program"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:15.445Z
updated_at: 2026-09-16T03:32:15.445Z
---
packages/workbench/probes/pack/stage-fits-viewport.js:5 fails strict tsc with TS2531. Fix: null-check the querySelector result. (PR #175, review 5218208204)
