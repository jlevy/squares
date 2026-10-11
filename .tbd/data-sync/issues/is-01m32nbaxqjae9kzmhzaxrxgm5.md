---
type: is
id: is-01m32nbaxqjae9kzmhzaxrxgm5
title: The records tier has an empty measured_seconds, switching off its drift, stale and headroom rules
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels: []
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-09-21T18:58:41.207Z
updated_at: 2026-10-10T22:55:54.779Z
---
packing-validate --records now runs about 68s at 4 cpus / --jobs 1 and prints 'write measured_seconds: 67.9' on every run. The records tier's entry in gate-budgets.yaml has no recorded cost, and the file's own header says an empty record switches off the drift, stale and headroom rules together.

Its reference shape is 2 cpus / --jobs 2, so readings taken at 4/1 do not arm it -- which is why this has persisted. Same shape of hole as think-gsz0.

Under OR-17 this matters more than it did: a tier with no record cannot be judged against a ceiling at all, so it is exempt from the rule by omission rather than by decision.
