---
type: is
id: is-01m1avr1fr94rt48yr999hvjyv
title: Non-smooth angle search generalised past one dimension (successor to H-002)
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-31T02:53:00.791Z
updated_at: 2026-08-31T02:53:00.791Z
---
exp-006 names this as 'the successor to H-002 and the spine's real angle half'. Nothing tracks it yet: think-imot (the LP-in-cell loop) is closed, think-vbk5 is the exploration problem, and think-opzu is H-001's angle-class proposer.

H-019 (confirmed by exp-010) says s(theta) has a corner at the optimal angles: one-sided slopes 0.1747 and 0.3841, ratio 2.198, stable over five decades on each side. No method assuming a smooth local model can converge there. Measured in exp-006: finite-difference descent stalls five orders short, and Powell and Nelder-Mead both do WORSE than descent.

quench_bracket already handles the one-dimensional case and reaches machine precision on both proved cells (exp-007: 2.22e-15 at n=5; exp-008: 1.33e-15 at n=10). What is missing is the general case: bisection on the sign of the one-sided derivative past 1-D, a subgradient or bundle method, or solving the active contact system algebraically.

Note this is orthogonal to the n=11 gap. exp-009 shows the bracketing quench does nothing at n=11 (6.999e-02 -> 6.2894e-02) because it is handed the wrong basin; that is think-vbk5. This bead is about the refiner being correct in general, not about reaching Trump's basin.

Watch for D-020's trap: the quench's answer must not depend on a merge tolerance, or basin identity inherits it.
