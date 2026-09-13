---
type: is
id: is-01m2chgbam9e6mvs59tkjpzw5j
title: "PR149: describe exact PDF prefixes without inferring truncation"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2cgrxbgn3kqyjh142w0cane
created_at: 2026-09-13T04:48:13.649Z
updated_at: 2026-09-13T04:53:45.054Z
closed_at: 2026-09-13T04:53:45.054Z
close_reason: "Reviewed repairs committed: PR148 e8baa8ff with81 focused tests; PR149 c699a7e3 with42 PDF/math tests and2 marker/corpus checks. Full integration validation continues under parent review."
resolution: null
duplicate_of: null
---
An exact byte prefix establishes a relationship, not whether bytes were truncated or appended. Repaired with neutral diagnostic and two-sided regression in c699a7e3.
