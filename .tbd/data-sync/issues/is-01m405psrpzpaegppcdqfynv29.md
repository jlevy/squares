---
type: is
id: is-01m405psrpzpaegppcdqfynv29
title: "H4: weighted-residual isolation lemma in the paper and the two-radius local box as a retained receipt (S1, S2)"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m405pqpja6nk3szf2hatajw0
created_at: 2026-10-03T06:02:32.597Z
updated_at: 2026-10-03T06:24:38.418Z
closed_at: 2026-10-03T06:24:38.418Z
close_reason: "check_n11_optimality_local_two_radius.py and receipts/local-isolation-two-radius/: the two-radius box (1/256, 1/128 for the angles of squares 9 and 10) passes the unchanged isolation audit with worst ratio 0.8667; six constants confirmed; paper Appendix C and the record describe it"
resolution: null
duplicate_of: null
---
Review S1/S2. Present the local argument as the lemma eta + M/2 < r_j with eta = sum_k r_k |e_k|, note the implemented unweighted form as a conservative instance, and name both ratio conventions. Run the repository's local checker and pose inclusion on the two-radius box (1/256 everywhere, 1/128 for the angular radii of local labels 9 and 10; every published radius is at most its replacement), retain the result as a new receipt with provenance and a portable replay, and report the exact worst ratio; the paper's appendix gets the box and the six curvature constants with the receipt cited.
