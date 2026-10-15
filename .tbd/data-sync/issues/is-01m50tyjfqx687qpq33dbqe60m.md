---
type: is
id: is-01m50tyjfqx687qpq33dbqe60m
title: Synchronize the README edition during site release cuts
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
created_at: 2026-10-15T22:29:29.194Z
updated_at: 2026-10-15T22:29:29.194Z
---
The native v0.7.11 site cut updated release.py and generated claim links but left README.md at v0.7.10; the owning component checks omitted the existing README-version contract in test_n11_lower_bounds_explainer.py, so broad pre-push caught it later. Extend the existing site release-cut path to synchronize the single README website edition reference and include or relocate the existing contract into component-owned release tests. Preserve paper and infographic editions, and avoid a second full validation job or duplicate assertion. Current v0.7.11 source is manually corrected and the existing failing contract passes; this bead removes the repeat manual trap.
