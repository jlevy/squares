---
type: is
id: is-01m12y4vf6c8t5mb3f268nm1kx
title: Algebraic degree is absent for all 84 cases that record an exact form, though it is derivable
kind: bug
status: open
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T01:01:02.299Z
updated_at: 2026-08-28T04:40:01.662Z
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

REFRAMED after PR #51 (merged 2026-08-28). My original framing was wrong in a way
that matters for scoping this.

I treated every empty exact_form as a fillable transcription gap. It is not. #51
establishes that "no exact form" has THREE distinct causes, and only the first is
a defect:

  1. NOT TRANSCRIBED - the source states it and we missed it. n=54 was this, and
     is fixed. This is the only defect class.
  2. IMPOSSIBLE - the side length is provably not expressible in radicals. n=28
     has Galois group S6 and n=39 has S5 over Q; neither is solvable. Verified
     independently with sympy.galois_group from the recorded polynomials. The
     empty exact_form is a PERMANENT mathematical property, not a gap.
  3. IMPRACTICAL - solvable but not worth writing. n=70 is degree 4 with Galois
     group S4, so a radical form exists in principle; #51 records that the
     expansion "runs to many lines and carries no insight the quartic does not
     already carry".

So this bead's remaining scope is narrower than written: derive and record the 84
missing DEGREES, which is still valid and unaffected, but do NOT treat the empty
exact_form fields as work to be done. Several of them are answers, not absences.

Note also the tooling limit: sympy.galois_group handles degree <= 6 only, so
n=11 (8), n=17 (18), n=41 (42), n=51 (12), n=83 (24), n=87 (44) and n=88 (20)
cannot be classified this way. #51 was careful not to claim otherwise; it made
factorization claims over Q(sqrt 2) instead, which I verified for n=37 (deg 8 ->
two quartics) and n=88 (deg 20 -> two degree-10 factors), each containing the
reported root.

This distinction belongs in think-18mu's provenance vocabulary: "absent" is too
coarse. An empty field needs to say WHICH of the three it is.
