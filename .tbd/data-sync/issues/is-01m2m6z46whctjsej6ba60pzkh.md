---
type: is
id: is-01m2m6z46whctjsej6ba60pzkh
title: "PR #181 addendum A2: type the shared Node probe loader"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:59.003Z
updated_at: 2026-09-16T04:17:59.003Z
---
packing/tests/node/probe.mjs returns any to 28 converted scripts, bypassing the type floor. Replace the any boundary with a typed generic or precise JSDoc contract and remove the broad any index signatures where practical; prove a bad member is rejected.
