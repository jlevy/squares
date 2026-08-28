---
type: is
id: is-01m12zhp8rh3dfdnyecaa0ezww
title: Witness sides carry no independent precision beyond the rounded published value
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T01:25:31.534Z
updated_at: 2026-08-28T01:26:22.438Z
---
The witness YAMLs write square centres and angles to ~100 significant digits, which looks like high-precision data but is not. Recomputing the container side from the coordinates at 400-digit working precision reproduces the recorded side string exactly for n=39, 70, 29, 55, 69, and to exactly the recorded digit count for n=11, 54, 71. The coordinates were generated FROM the rounded side, not from an independent solve, so the side field is the only carrier of precision and the coordinate digits are decorative.

Actual usable digits: n=29: 100, n=55: 50, n=71: 50, n=68: 46, n=69: 46, n=54: 30, n=11: 33, n=39: 50, n=70: 30.

Consequence: any numeric-to-symbolic recovery is bounded by these, not by the apparent 100+ digits. Minimal polynomials already recorded in this repo need digit budgets of 20 to 2247, median ~93, so at 30-50 digits most are simply out of reach. A failed search proves nothing about the mathematics.

Fix: re-refine the witnesses by Newton iteration on their own contact systems at 500-2000 digits. That would likely settle n=29, 55 and 71 outright and confirm n=54's quartic beyond doubt. n=68 and n=69 cannot be refined until their geometry is re-solved, since it is self-inconsistent at 1e-8 (see think-ecqk).

Also worth recording in the witness schema that decimal_digits under claim.precision is the CHECKING precision, not the data precision; that field was misread as the latter during this investigation.
