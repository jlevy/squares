---
type: is
id: is-01m405prq6vxb37g419dj1ct3p
title: "H2: corrected closed-interval cover kernel with singleton handling and the 12,180-case controls (C2)"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m405pqpja6nk3szf2hatajw0
created_at: 2026-10-03T06:02:31.526Z
updated_at: 2026-10-03T06:21:44.460Z
closed_at: 2026-10-03T06:21:44.456Z
close_reason: Corrected closed-interval cover kernel n11_closed_interval_cover.py with the 12,180-case control (616 historical false accepts, all singletons), caller audit in the docstring, frozen checkers unchanged
resolution: null
duplicate_of: null
---
Review C2. covers_vertical in the frozen field checker falsely accepts [1,1] covered by [0,0]. Add a new module with a correct exact closed-interval cover predicate (singleton covered iff some closed interval contains it; seams accepted; positive gaps refused; malformed refused), tests reproducing the 12,180-case enumeration (616 historical false accepts, all singleton targets; zero corrected errors), and a caller audit note naming each call site of the historical predicate and the contract (full-dimensional convex target with complete sweep; field callers clip covers to the domain; degenerate domains dispatch to the point/segment helper). Frozen checker bytes stay unchanged.
