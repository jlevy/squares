---
type: is
id: is-01m2m6z46whctjsej6ba60pzkh
title: "PR #181 addendum A2: type the shared Node probe loader"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:59.003Z
updated_at: 2026-09-16T06:53:38.328Z
closed_at: 2026-09-16T06:53:38.327Z
close_reason: "Completed at PR #181 head 7f990cbb: the shared Node probe loader returns unknown, consumers narrow their actual contracts, and the browser/type floors reject an undeclared member."
resolution: null
duplicate_of: null
---
packing/tests/node/probe.mjs returns any to 28 converted scripts, bypassing the type floor. Replace the any boundary with a typed generic or precise JSDoc contract and remove the broad any index signatures where practical; prove a bad member is rejected.
