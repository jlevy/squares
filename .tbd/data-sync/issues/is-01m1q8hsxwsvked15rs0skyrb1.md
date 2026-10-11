---
type: is
id: is-01m1q8hsxwsvked15rs0skyrb1
title: Harden the integer exact sweep after PR 78 integration
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1q78vv6ved9nhwhs4spdq2x
created_at: 2026-09-04T22:27:41.115Z
updated_at: 2026-10-06T08:27:13.078Z
closed_at: 2026-10-06T08:27:13.077Z
close_reason: "Superseded by PR 82 (bb65d8707): integer-sweep hardening ported as think-612b (masses in Python integers, refused at 2^62) and think-xyt1 (witness admissible on both routes; integer entry point checks its preconditions)."
resolution: null
duplicate_of: null
---
Correct the exact-sweep equivalence guard, int64 direct-call overflow boundary, parallel start-method/library safety, CPU and memory caps, and witness feasibility; add adversarial regression tests and distinguish retained correctness evidence from unretained timing reports.
