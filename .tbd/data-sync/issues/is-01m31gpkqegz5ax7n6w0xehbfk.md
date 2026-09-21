---
type: is
id: is-01m31gpkqegz5ax7n6w0xehbfk
title: File a D- entry for the side-6 distinctness unsoundness
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:13.356Z
updated_at: 2026-09-21T08:18:13.356Z
---
PR 205 re-review. F1 was a High soundness defect in the Bentz 2016 side-6 port - the distinctness predicate decided from colour labels rather than witness identity - and it was fixed by aed8638d, but no D- entry was filed. D-505, D-506 and D-507 register exactly this shape (detected_by: review, class: soundness, severity: high) for this same port. This one's direction would be optimistic, the opposite of those three, and the direction that pushes toward a false confirm on exp-217.
