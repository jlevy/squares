---
type: is
id: is-01m12y4vf6c8t5mb3f268nm1kx
title: Algebraic degree is absent for all 84 cases that record an exact form, though it is derivable
kind: bug
status: open
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T01:01:02.299Z
updated_at: 2026-08-28T01:32:33.439Z
---
exact_form and algebraic_degree have ZERO overlap across the 100 frontier records: 84 carry a radical, 11 carry a degree, none carry both. That mirrors the upstream catalogue's own convention -- Kingbird prints EITHER a radical (s = 4 + 2 sqrt 2) OR a locked degree (s = {}^{8}lock plus the polynomial) -- so the degree is missing from our records not because it is unknown but because the source did not print it and we never derived it.

It is cheap to derive and fully determined by the radical we already hold. Computed over all 84 with sympy minimal_polynomial in seconds:

  degree 1: 65 cases (integer sides)
  degree 2: 18 cases
  degree 4:  1 case (n=54)

Worked examples:
  n= 40  4 + 2 sqrt(2)                     -> s^2 - 8s + 8 = 0            degree 2
  n=  5  2 + (1/2)sqrt(2)                  -> 2s^2 - 8s + 7 = 0           degree 2
  n= 54  7 - (1/2)sqrt(2) + sqrt(1+sqrt 2) -> 4s^4 - 112s^3 + 1164s^2 - 5304s + 8897 = 0   degree 4

n=40 being degree 2 is evident from the structure by inspection, which is how this was noticed.

This is the same defect class as think-18mu: a null that means 'the source did not print it, and we did not compute it' is stored identically to one meaning 'nobody knows'. The composite figure prints 'deg d' for only 11 cases and is silent for 84 whose degree is a one-line computation.

DONE WHEN: algebraic_degree and minimal_polynomial are populated for all 84, marked as repo-derived rather than source-transcribed (see think-18mu for the provenance vocabulary), with a check that re-derives them from exact_form and fails on divergence. Note the derivation must record WHICH it is: transcribing a source claim and computing one ourselves are different epistemic acts and the records must say which happened.

## Notes

CONVENTION, settle this before populating anything.

Rationals have algebraic degree 1, not 0. The minimal polynomial of 2 is s - 2,
degree 1, and [Q(a):Q] = 1. A degree-0 polynomial is a nonzero constant and has
no root, so no number has algebraic degree 0. This came up because the integer
sides (n = 1, 2, 3, 4, 9, 12, ...) look degree-less; they are degree 1.

Verified with sympy:
  s(2)  = 2            -> s - 2          degree 1
  s(9)  = 3            -> s - 3          degree 1
  s(40) = 4 + 2sqrt(2) -> s^2 - 8s + 8   degree 2

Full derived distribution over the 84 records that carry an exact form:
  degree 1: 65   degree 2: 18   degree 4: 1 (n=54)

DISPLAY DECISION still open: the figure currently prints "deg d" only for the 11
records that carry the field, so 84 cards show nothing. Populating all 100 would
put "deg 1" on 65 cards, which is noise on an integer side. Suggest recording the
degree for every case in the data, and printing it in the figure only above some
threshold (deg >= 2, or only where no closed form is shown). That is a rendering
choice and should not drive what the records hold.
