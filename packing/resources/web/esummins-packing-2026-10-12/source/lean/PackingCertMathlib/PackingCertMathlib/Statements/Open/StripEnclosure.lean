import PackingCertMathlib.Statements.Open.LastTwo

/-!
# -- OPEN: STRIP₂ BY ENCLOSURE — the strip is walled in by the wall, C and X; the corner-box entry is closed by
# Lemma WEDGE-FLOAT, the C–X wedge by its width — A267

`docs/proofs/strip_enclosure.md`.  Corner frame: wall `x = 0`, floor `y = 0`; `C` the floater with lowest vertex
`(h_u + s, h_v)`, tilt `θ` (`c = cos θ, s = sin θ`), left vertex `L = (h_u, h_v + c)`; `S = T_u ∖ C` the strip.

**What is a theorem here (the algebraic cores of the hand proof).**
* `wedge_float_core` [T] (§1, case (iii) — the corner-box entry): a unit square `Q` of tilt `ψ` (`c', s'`) whose
  centre is at height `≤ 1` has exactly one vertex above height `1` (POKE in the slot `[0, ℓ_C(y))`, of width
  `≤ g < 1` there); its top vertex `T = (t_x, t_y)` has `t_x ≥ c'` (the wall), `t_y ≥ c' + s'` (the floor), and the
  chord of `Q` at height `1` ends at `t_x + (t_y − 1) tan ψ ≤ g` (left of C's lower-left edge).  Multiplying by
  `c' > 0`: `c' t_x + (t_y − 1) s' ≤ g c' < c'`, while `c' t_x + (t_y − 1) s' ≥ c'² + (c' + s' − 1) s' =
  1 + c' s' − s' ≥ c'` ⟺ `(1 − c')(1 − s') ≥ 0`.  Contradiction — no free square of the strip has its centre at
  or below height `1`; with the box condition `g < 1` this is A259's Lemma WEDGE for a FLOATING `C`.
* `sincos_le_half` [T]: `s' c' ≤ 1/2` — the chord of a unit square at distance `t` from an extreme vertex is
  `t / (s' c') ≥ 2 t`.
* `wedge_extent_core` [T] (§3, the C–X wedge): if every chord of `Q` on the `a`-interval `(a*, a₂)` (in C's frame:
  `a` along C's upper-left edge) has length `≤ w` while `Q` reaches past `a₂` and has a point before `a*`, then the
  tent-shaped chord function forces `(a₂ − a*) / (s' c') ≤ w`; with `a₂ − a* > w / 2` this is impossible: a poke
  into a slot of width `w` has depth `≤ w s' c' ≤ w / 2` (Lemma POKE, peel.md §2.3), and T_u's top edge lies deeper.
* `e_point_core` [T] (§3): the right end `E` of Q's centre chord (right of X, so `x_E ≥ r_X + 1` with
  `r_X > h_u + c − 1`) has `a_E > 1 ≥ a₂` — Q reaches past the wedge's mouth.
* `strip_in_ring_of_enclosure` [T from the axiom]: on the ring domain the BL sectors reduce to `pair3` exactly as
  `jam_sector_of_strip` (ThreeLemmas) does from `strip_lemma`.

**What is not.**
* `strip_two_in_ring` is the [T-prose] geometric theorem of strip_enclosure.md §1–§3 (the cores above are its
  arithmetic; the case analysis — LEFT, UPPER, FRAME, NO-STRADDLE, FAR-SIDE — is prose); `RingDomain` is opaque:
  the hypotheses (D1)–(D2), (U1)–(U9) of §3, measured with positive margin on the 43 JAM rings (`hyp267`).
  On the general STRIP₂ domain (A266) the UPPER case is not covered (§3.5).
-/

namespace PackingCert.S11.OpenLemmas.StripEnclosure

/-- **WEDGE-FLOAT, the arithmetic core** [T]: `c'² + s'² = 1`, `c' > 0`, `s' ≥ 0`, the slot width `g < 1`, the wall
`c' ≤ t_x`, the floor `c' + s' ≤ t_y`, and the chord at height `1` inside the slot, `c' t_x + (t_y − 1) s' ≤ g c'`
(the inequality `t_x + (t_y − 1) tan ψ ≤ g` multiplied by `c'`): impossible. -/
theorem wedge_float_core (c s g tx ty : ℝ) (h1 : c ^ 2 + s ^ 2 = 1) (hc : 0 < c) (hs : 0 ≤ s) (hg : g < 1)
    (hwall : c ≤ tx) (hfloor : c + s ≤ ty) (hchord : c * tx + (ty - 1) * s ≤ g * c) : False := by
  have hc1 : c ≤ 1 := by nlinarith
  have hs1 : s ≤ 1 := by nlinarith
  nlinarith [mul_le_mul_of_nonneg_left hwall hc.le, mul_le_mul_of_nonneg_right hfloor hs,
             mul_nonneg (sub_nonneg.2 hc1) (sub_nonneg.2 hs1)]

/-- `s' c' ≤ 1/2` for `s'² + c'² = 1` [T]. -/
theorem sincos_le_half (c s : ℝ) (h1 : c ^ 2 + s ^ 2 = 1) : s * c ≤ 1 / 2 := by
  nlinarith [sq_nonneg (s - c)]

/-- **The wedge is too shallow for a poke** [T]: a chord bound `d ≤ w · (s' c')` with `s' c' ≤ 1/2` and
`d > w / 2` is contradictory (`d = a₂ − a*`, the distance from the wedge's mouth to T_u's top edge). -/
theorem wedge_extent_core (d w sc : ℝ) (hsc : sc ≤ 1 / 2) (hw : 0 ≤ w) (hd : w / 2 < d) (hchord : d ≤ w * sc) :
    False := by
  nlinarith [mul_le_mul_of_nonneg_left hsc hw]

/-- **Q reaches past the mouth** [T]: with `r > h_u + c − 1`, `c > 0`, `c² + s² = 1`, the point
`E = (r + 1, ·)` of Q's centre chord has `a_E = c (r + 1 − h_u) + s · (q_y − L_h) > 1` once `q_y − L_h ≥ s`. -/
theorem e_point_core (c s hu r dy : ℝ) (h1 : c ^ 2 + s ^ 2 = 1) (hc : 0 < c) (hs : 0 ≤ s) (hr : hu + c - 1 < r)
    (hdy : s ≤ dy) : 1 < c * (r + 1 - hu) + s * dy := by
  nlinarith [mul_lt_mul_of_pos_left hr hc, mul_le_mul_of_nonneg_left hdy hs]

/-- The JAM-ring domain of strip_enclosure.md §3 ((D1)–(D2), (U1)–(U9)): opaque. -/
opaque RingDomain : Prop

/-- **STRIP₂-IN-RING** [T-prose] (strip_enclosure.md §1–§3): on the ring domain no unit square of the
quadrant interior-disjoint from `C` and `X` has an interior point in `T_u ∖ C`.  The cores
`wedge_float_core`, `wedge_extent_core`, `e_point_core` are its arithmetic; the case analysis is prose. -/
axiom strip_two_in_ring (hdom : RingDomain) (Q : Set RP)
    (h : PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q

/-- **The BL sectors of a JAM corner on the ring domain reduce to `pair3`** [T from `strip_two_in_ring`]:
as `jam_sector_of_strip` (ThreeLemmas), with STRIP₂ supplied on the ring domain instead of `strip_lemma`. -/
theorem strip_in_ring_of_enclosure (hdom : RingDomain)
    (hsub : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q)
    (hcover : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q →
      PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q)
    (hpair3 : ∀ Q, ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q) (Q : Set RP) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q :=
  fun h => hpair3 Q (hcover Q h (strip_two_in_ring hdom Q (hsub Q h)))

#print axioms wedge_float_core
#print axioms sincos_le_half
#print axioms wedge_extent_core
#print axioms e_point_core
#print axioms strip_in_ring_of_enclosure

end PackingCert.S11.OpenLemmas.StripEnclosure
