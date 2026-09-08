---
type: is
id: is-01m1w1wzyq8b7cj2d0j3rykmft
title: "PR #98 review R4: validation_report frontmatter split raises bare IndexError"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:39.862Z
updated_at: 2026-09-06T19:16:34.083Z
closed_at: 2026-09-06T19:16:34.083Z
close_reason: "Fixed: render() raises ValueError naming the file when frontmatter is missing; test added."
resolution: null
duplicate_of: null
---
packing/benchmarks/validation_report.py:205 split('---',2)[1]. Fix: check parts and raise ValueError naming the file; add a test.
