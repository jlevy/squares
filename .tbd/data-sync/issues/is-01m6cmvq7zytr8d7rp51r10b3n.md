---
type: is
id: is-01m6cmvq7zytr8d7rp51r10b3n
title: "Efficiency: DATA_REVISION pin in release.py conflicts on parallel records PRs (32 merges in 20 PRs since 24 Oct)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-01T22:49:39.327Z
updated_at: 2026-11-01T22:49:39.327Z
---
Measured by devtools.merge_conflicts in #873 (think-nrp6): after the no-public-change tuple, the DATA_REVISION pin in packing/src/sqpack/release.py is the next most frequent conflict, 32 merges in 20 PRs from 24 Oct to 1 Nov; the union driver 'parses' 9 of its sole-conflict merges but yields two pin assignments, silently wrong. Candidate fixes: derive the pin at check time from git (last data commit) instead of storing it, or store it outside release.py in a file whose merge is mechanical. Measure, pick the smallest sound fix (OR-12 efficiency block), red-first test that two data PRs merge cleanly.
