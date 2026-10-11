---
type: is
id: is-01m0nxqaeghsmbn3crwefzrqy6
title: Formalize the nonavoidance lemma layer in Lean
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0nxq9sedycsz5hxfhbb2r84
created_at: 2026-08-22T23:43:31.280Z
updated_at: 2026-10-06T08:28:20.743Z
---
Friedman's Lemmas 1-3 and Stromquist's 1-6: single-variable calculus, self-contained, and load-bearing for EVERY proved value of s(n) -- yet machine-checked by nobody. Treat as diagnostic: the interesting outcome is a gap, not a green check. This repository already found one misreading in this layer (the two-stage structure of Stromquist's Theorems 2 and 3).

## Notes

2026-10-06 (bead review): think-xk35 was closed as a duplicate. It also proposed s(2) = s(3) = 2 as a first small Lean target beside Friedman's Lemmas 1-3; Stromquist's Theorem 1 is think-ix83.
