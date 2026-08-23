---
type: is
id: is-01m0nym0hvhtp7kvr9n0j1ejjk
title: "sqpack-core: Scalar trait, SAT predicate, containment, grid bucketing"
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:11.419Z
updated_at: 2026-08-23T05:26:44.162Z
---
Generic over a Scalar trait giving + - * and a sign decision. No allocation on the hot path, no I/O. The predicate is four axes and eight dot products with no divisions and no square roots, which is why one implementation is correct over every scalar type.
