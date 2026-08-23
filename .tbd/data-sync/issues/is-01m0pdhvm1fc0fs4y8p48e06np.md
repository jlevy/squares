---
type: is
id: is-01m0pdhvm1fc0fs4y8p48e06np
title: "Postmortem: the soundness class, and why the perimeter let D-014 through"
kind: task
status: closed
priority: 0
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:20:09.472Z
updated_at: 2026-08-23T04:42:03.689Z
closed_at: 2026-08-23T04:42:03.689Z
close_reason: "docs/project/postmortems/postmortem-2026-08-23-soundness-class.md: timeline, why no detector existed, the shared root cause with D-019, and rules R1-R4."
---
Six of 21 defects are soundness failures; four flattered. D-014 (LP returned a packing violating its own constraints, claiming a side below the record) is the critical case. Write a postmortem covering: the timeline, how it was actually caught (a pre-registered rule, not a detector), why no detector existed, and the generalisable rules. Two candidate rules: every component that can assert a configuration is valid must be checked against the single validity oracle; and every numerical tolerance must be compared against the quantity it is meant to resolve, and declared.
