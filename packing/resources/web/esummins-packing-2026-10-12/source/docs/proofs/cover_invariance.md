# Cover invariance of the A57 shadow trees across the s-window (A63 follow-up, 2026-09-01)

Decision-gating question (advisor, via A57 T21): does A57's interior branch — the t-uniform
θ-cover × 12-column zone subdivision of `tree57` — remain a complete disjunction of the
stratum for every s ∈ W = [191/50, s0], with child-box s-dependence in exactly the
(α, β)-affine form `verify_param` consumes? **Answer: YES — proved below (CI-1..CI-3), with
ONE per-box obligation that is NOT invariant and must be checked mechanically (CI-4, the
601 logic kills), plus two named tool gaps.** Route (a) is therefore unblocked as
theory; its remaining cost is tooling + one 4-D pass + the CI-4 checks.

Deployed data, verified exact against the certificate corpus (this file's claims are about
THESE objects, not idealisations):
* zone at s0: Z = [11/10, 694271/250000]² and 694271/250000 = s0 − 11/10 **exactly** — so the
  zone is Z(s) = [c0, s − c0]², c0 = 11/10, instantiated at s0 (NO-child nofam field);
* cover: 12 × 12 equal columns/rows of Z(s) × 8 equal t-intervals of [0, 1] (1152 children);
  depth-2 refinement bisects boxes (dyadic sub-edges);
* sampled leaf cores sit at c0 + q·(s0 − 2c0) with q = 13/48, 11/48, 19/24 **exactly**
  (e.g. 6216841/4000000 = 11/10 + (13/48)·419271/250000) — every deployed box edge/centre is
  c0 + q·(s − 2c0)|_{s=s0} with q ∈ Q_dy := ({0, 1/12, …, 1} refined dyadically) ⊂ [0,1] ∩ ℚ;
* pins: slot coordinates in {1/2, 3/2, s0 − 1/2} (844271/250000 = s0 − 1/2 exactly) — affine
  α + β·s with **β ∈ {0, 1} confirmed**;
* t-intervals: [j/8, (j+1)/8], s-independent; core tilts tm constant rationals.

## The parametric family (P-aff)

For s ∈ W define: Z(s) = [c0, s−c0]²; column/row edges e_q(s) = c0 + q·(s − 2c0), q ∈ Q_dy;
box B(s) = [e_q1(s), e_q2(s)] × [e_q3(s), e_q4(s)] × [t0, t1]; core K_B(s) = centre at the box
centre (affine with q = (q1+q2)/2 etc.), half-side a and tilt tm frozen at their s0 values;
pins at slots_S(s). Every coordinate is α + β·s with

  edges/centres: β = q·1 ∈ [0,1] ∩ ℚ (from e_q(s) = (c0 − 2c0·q) + q·s);  pins: β ∈ {0,1};
  zone/nofam rectangle: x0 : (α, β) = (11/10, 0), x1 : (α, β) = (−11/10, 1).

This is exactly the widening form `verify_param` consumes ([α + β·a, α + β·b] per s-cell
[a, b]). At s = s0 the family reproduces the deployed tree identically (C1-canary by
construction, as in A56 P3).

## CI-1 [T] — completeness of the disjunction at every s ∈ W

Fix s ∈ W. s − 2c0 ≥ 191/50 − 11/5 = 81/50 > 0, so Z(s) is a nonempty square inside the
admissible band ([1/2, s−1/2] ⊇ [c0, s−c0] since c0 > 1/2). The 12 columns
{[e_{i/12}(s), e_{(i+1)/12}(s)]} partition [c0, s−c0] for EVERY s (e_0(s) = c0,
e_1(s) = s−c0, edges affine in s with strictly increasing q ⇒ order preserved and widths
(s−2c0)/12 > 0); likewise rows; the 8 t-intervals partition [0,1]. Hence
{B_ijl(s)} is a closed cover of Z(s) × [0,1], and dyadic refinement of any box by
sub-edges (q ∈ Q_dy) preserves this. By A57 T1 (a tautology for any zone and any closed
cover of it), for every packing at side s:

  (NO: no square's centre in Z(s))  ∨  (∃ i,j,l: some square has (centre, t) ∈ B_ijl(s))

is a complete disjunction, at every s ∈ W separately. ∎
(Nothing here uses s0; completeness was never the s-fragile part.)

## CI-2 [T] — the frozen (a, tm) cores stay valid for every s ≤ s0

Obligation (tree-level soundness of a YES child): every square with (centre, t) ∈ B(s)
contains K_B(s). The caselp constructor's sufficient condition is
a·(1 + (t1 − t0)) ≤ 1/2 − hd, hd = half-diagonal of the centre box — monotone: it only
tightens as the centre box WIDENS. Under (P-aff) the centre-box half-widths are
(q2 − q1)·(s − 2c0)/2, strictly increasing in s, hence MAXIMAL at s = s0; the deviation of a
box point from the box centre is bounded by the s0 bound for every s ≤ s0, the t-window is
s-independent, and the core centre tracks the box centre exactly (same affine map). So the
containment verified at s0 (where a was computed) holds verbatim for every s ∈ W. ∎
Note the direction: this argument needs the window to sit BELOW s0 — true (W's top is s0).

## CI-3 [T] — pinguard across the window: no parent boxes, witnesses distinct, for every s

Pin centres of k5_11/k5_16 have a coordinate in {1/2, s−1/2}: 1/2 < 11/10, and
s − 1/2 > s − 11/10 (as 1/2 < 11/10). So NO pin placement has its centre in Z(s), for any
s ∈ W — the `parent` classification (T5) is empty on the interior zone at every side, the
YES witness is always distinct from the 5 pinned squares, and budget 11 − k − 1 = 5 stays
sound across the family. (The remaining pin coordinate values 3/2 do enter [c0, s−c0], but
zone membership requires both coordinates; every pin has an excluded coordinate.) ∎

## CI-4 [F + obligation] — the 601 logic kills are NOT cover-invariant and must be re-checked

The `contradictory` classification (T5: box core meets a pin core ⇒ empty by logic, no LP,
no certificate — 344 + 257 = 601 of the 2304 level-1 children) is a RELATIVE-POSITION fact.
Under (P-aff) interior cores move with β = q ∈ (0,1) while pin cores move with β ∈ {0,1}:
relative motion up to (1 − 1/24)·(s0 − s_lo) ≈ 0.0547 across W. A box whose core-vs-pin
overlap has less margin than its relative motion FLIPS to non-contradictory somewhere in the
window — and then carries NO kill there (it was never LP-solved). So the parametric route's
"no LP redo" holds only modulo:

  **(C-check)** for each of the 601 logic-killed boxes, an exact SAT overlap check of
  core K_B(s) vs the pin core with centres widened to their s-intervals over W (the same
  outward-interval predicate `verify_param` uses for (E)); boxes that fail on a sub-range
  get routed to LP + certificate on that sub-range (or depth-2).

This is bounded, cheap compute (601 exact 4-D SAT checks), but its flip count is unmeasured;
it is the honest asterisk on "one 4D re-verification pass". Mitigating expectation: the
recorded contradictions involve the NEAR pins ((1/2,1/2), (1/2,3/2), (3/2,1/2) — β = 0
coordinates), against which the relative motion is only the core's own q·δ_max; deep
overlaps (e.g. T6's inner-corner box) have margins ≫ 0.055; flips should concentrate on
grazing overlaps only.

*Alternative family (P-fix), recorded for completeness:* freezing zone, boxes and cores at
their s0 positions (β = 0 everywhere except pins) is ALSO a complete disjunction for every s
(CI-1 is tautological for any fixed zone; CI-2 becomes trivial; CI-3 still holds:
1/2 < 11/10 and s − 1/2 ≥ 191/50 − 1/2 = 166/50 > 694271/250000). Under (P-fix) every logic
kill against a β = 0 pin is EXACTLY s-invariant (no relative motion), and only kills against
the two far β = 1 pins could flip — plausibly none exist (the β = 1 pins are ≥ 0.5 from the
zone at s0). The trade-off: the zone loses its wall-clearance interpretation at small s and
the NO-child/YES certificates face different (not obviously worse) coverage geometry. If the
(C-check) under (P-aff) reports many flips, (P-fix) is the fallback that makes CI-4 nearly
vacuous — the choice of family is a completeness/cost decision, never soundness (A56 P3's
anchoring principle applies verbatim).

## Tool gaps (the actual blockers, now that the lemma exists)

1. `make_param.core_anchor()` rejects non-slot cores (T21 (i)) — relax to accept declared
   (α, β) with β ∈ [0,1] ∩ ℚ for non-pin cores (the verifier's widening is already general);
   pin cores must still validate against slots (β ∈ {0,1} — CONFIRMED above).
2. `verify_param` nofam support: the NO-children carry the zone as a NO-family with an
   s-anchored edge (x1 = s − 11/10, β = 1). A56's library had all-empty nofams, so the
   parametric (E)-style exemption for nofams with affine rectangles is likely unimplemented
   and in any case UNAUDITED. Sound direction: exemption must hold for ALL s in the cell ⇒
   use the INTERSECTION of the rectangles over the s-cell (x1 at the cell's LOWER end);
   conservative, never unsound.
3. The (C-check) driver of CI-4 (new, small; reuse the (E) SAT predicate).

## Verdict

The cover-invariance lemma **HOLDS** (CI-1 completeness for every s ∈ W; CI-2 frozen cores
valid on all of W; CI-3 pinguard-parent-freeness and witness distinctness on all of W), and
the affine form is exactly `verify_param`'s (α, β) with β = dyadic/12 rationals for boxes,
{0,1} for pins — both confirmed against the deployed corpus exactly. Route (a) for A57's
window form is therefore: two tool changes + the 601-box C-check (+ LP only on flippers) +
one 4-D re-verification pass over ~2300 leaves — against ~8 desktop-days for the δ = 1e-2
slack-core grid (T21 (b)). The un-priced items of route (a) are the 4-D per-leaf cost and
the C-check flip count; everything else is now theory-closed. The two routes compose: a
stratum is window-covered when EITHER succeeds per leaf, so (a) can run as a cheap first
pass with (b)'s grid as the mop-up for 4-D FAILs.
