---
type: is
id: is-01m32nbaxqjae9kzmhzaxrxgm5
title: The records tier has an empty measured_seconds, switching off its drift, stale and headroom rules
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T18:58:41.207Z
updated_at: 2026-09-21T18:58:41.207Z
---
packing-validate --records now runs about 68s at 4 cpus / --jobs 1 and prints 'write measured_seconds: 67.9' on every run. The records tier's entry in gate-budgets.yaml has no recorded cost, and the file's own header says an empty record switches off the drift, stale and headroom rules together.

Its reference shape is 2 cpus / --jobs 2, so readings taken at 4/1 do not arm it -- which is why this has persisted. Same shape of hole as think-gsz0.

Under OR-17 this matters more than it did: a tier with no record cannot be judged against a ceiling at all, so it is exempt from the rule by omission rather than by decision.
