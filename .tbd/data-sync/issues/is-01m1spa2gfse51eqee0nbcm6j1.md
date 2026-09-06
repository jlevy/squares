---
type: is
id: is-01m1spa2gfse51eqee0nbcm6j1
title: Exactify and independently replay a fractional candidate
kind: task
status: open
priority: 1
version: 3
labels:
  - research
dependencies: []
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
created_at: 2026-09-05T21:06:36.686Z
updated_at: 2026-09-06T17:57:54.520Z
---
BC-238: independently decide any frozen adaptive fractional candidate with the project exact sweep, interval route, and BC-231's standard-library standalone verifier. Re-run falsifying mutations, preserve the candidate hash, and report shared assumptions; only the coordinator may retain or promote it.

## Notes

BC-238 accepts scalar candidates from BC-251/H-093 as well as legacy BC-232/233; adaptive BC-234/H-095 and kernel BC-236 retain object-specific routes. Commit candidate bytes and identify Git revision/path under OR-16, no duplicate local hash manifest. All exact decision routes and required refusals remain; a new typed proof boundary needs source-distinct review.
