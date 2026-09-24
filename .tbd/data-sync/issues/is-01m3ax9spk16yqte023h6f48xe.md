---
type: is
id: is-01m3ax9spk16yqte023h6f48xe
title: "BC-384: design a stronger per-node bound for the fixed-angle cell tree (rung 1 prerequisite)"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m3ackz509zmgq9cs6xew8hzw
created_at: 2026-09-24T23:51:34.866Z
updated_at: 2026-09-24T23:51:34.866Z
---
exp-234 shows rung-1 cost lives in the fixed-angle centre enumeration (~65% closed at 4M nodes per box regardless of width/tilt). Candidates from the record: second-order dual bounds from a fixed dual at the box centre (X-046), symmetry canonicalization, descent leaves (exp-228's filter), pruning tests from the verified-optimization literature. Benchmark: re-close a rung-0 subtree or a pilot box in orders of magnitude fewer nodes.
