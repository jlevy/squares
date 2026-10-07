---
type: is
id: is-01m4c66fervqnev6wppvj1zk8f
title: Fix popover close accessibility state exposed by SQUISH import browser gate
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4bvqnk2d26b8ydnvt3h07n1
created_at: 2026-10-07T22:01:59.512Z
updated_at: 2026-10-07T22:01:59.512Z
---
PR421 final affected gate exposed reproducible Escape closure race: hidden case popover retains aria-expanded=true until asynchronous toggle. Unchanged complete browser replay1failed19passed; math fixtures passed. Sol engineering repair moves accessibility cleanup to synchronous noncancelable closing beforetoggle, leaves focus restoration on toggle, strict tests unchanged. Strong Astra scoped review accepted. Source b4c59000c3ba8ec4bc19fb89a4cc8b175ed6ef7d; complete repaired two-module replay20passed77.99s; required88-selector push since2a27 underway. Track actual source repair/review/CI/publication, keep prior broad failure receipt.
