import PackingCertMathlib.Statements.Open.RingDomain

/-!
# -- OPEN: STRIP₂ IN JAM under H1–H3 alone — the ring inequalities replaced by the DISC LEMMA — A272

`docs/proofs/strip_jam.md`.  Corner frame: wall `x = 0`, floor `y = 0`; `C` the floater (tilt `θ`, `c = cos θ`,
`s = sin θ`, left vertex at height `L_h = h_v + c`, top vertex `T = (h_u + c, C_top)`); `X` the wall toucher (tilt
`φ`, `cφ, sφ`, lowest point `X_low`, right vertex at height `Y_R = X_low + sφ`, wall vertex at `Y_W = X_low + cφ`);
`D = C_top − X_low` (how far X dips below C's top).

**What is a theorem here (the arithmetic cores of strip_jam.md §2–§4).**
* `d_low_core` [T] (§2 (D-low), the case `φ ≥ θ`): a point of `X` inside `T_u` at height `X_low + t` lies right of
  `T_u`'s upper-left edge and left of `X`'s lower-right edge, `(s − D + t) cot θ ≤ sφ + t cot φ`; with `cot φ ≤ cot θ`
  this gives `D cot θ ≥ c − sφ`: X's dip below C's top is at least `(c − sφ) tan θ`.
* `cl_core_i`, `cl_core_ii` [T] (§3, Lemma CL): `(D − cφ) cot φ ≤ c`, i.e. the region left of X's upper-left edge
  above X's wall vertex misses `T_u` — from X's lower boundary at `x = T_x` being above `C_top` (case i,
  `T_x ≤ cφ + sφ`) or from X's right vertex being above C's upper-left line (case ii).  This kills the case
  "Q's centre above X's top with Q LEFT of X" (case C-left) outright.
* `centre_right_core` [T] (§4): a centre right of X's right boundary by half a chord, at a height above `C_top`,
  has `a`-coordinate `> a* − 1/2`; so Q's `a`-range crosses `a* = 1 − h_u c` (T_u's top edge) — Q's body is
  right of T_u's top edge, only a poke reaches the strip.
* `strip_two_in_ring_of_disc` [T from the axiom]: the BL sectors of a JAM corner reduce to `pair3` under
  `JamCorner ∧ DiscLemma` — A271's `strip_two_in_ring_of_jam` with `RingIneq` replaced by `DiscLemma`.

**What is not.**
* `strip_two_in_jam_of_disc` [T-prose] is strip_jam.md §4–§5: every free strip square has its centre `q` above
  `L_h` (A267 WEDGE-FLOAT), its horizontal chords at X's heights on one side of X, its part below `C_top` left of
  C (LEFT); so its inscribed disc `D(q, 1/2)` misses the convex sets `Ξ` (left of X's right boundary at X's
  heights; `Ξ'` = right of X's left boundary when Q is left of X) and `Γ` (right of C's left boundary below
  `C_top`), and its strip point `p` is within `1/√2` of `q`.  `DiscLemma` is that these four conditions are
  inconsistent — a statement about a point and three convex sets, in the five parameters `(h_u, h_v, θ, X_low, φ)`;
  it is [M] on the H1–H3 set (`disc272`: sup of the slack `−0.005`, attained only as `h_v → 1`, the open boundary;
  the square statement itself has sup `−0.017`, `left272`) and NOT proved: the residual of A272.
* `JamCorner` is A271's opaque H1–H3.  A271's `strip_two_in_jam` (axiom under `RingIneq`) is untouched.
-/

namespace PackingCert.S11.OpenLemmas.StripJam

open PackingCert.S11.OpenLemmas.RingDomain

/-- **(D-low), the core** [T]: `k = cot θ`, `k' = cot φ ≤ k`, `s k = c`, a point of X in `T_u` at height
`X_low + t` (`0 ≤ t`): `(s − D + t) k ≤ sφ + t k'`.  Then `c − sφ ≤ D k`. -/
theorem d_low_core (s c k k' sphi D t : ℝ) (hsk : s * k = c) (hkk : k' ≤ k) (ht : 0 ≤ t)
    (h : (s - D + t) * k ≤ sphi + t * k') : c - sphi ≤ D * k := by
  nlinarith [mul_le_mul_of_nonneg_left hkk ht]

/-- **Lemma CL, case (i)** [T]: X's lower-right edge spans `x = T_x = h_u + c` and passes above `C_top`:
`D cφ ≤ (h_u + c − sφ) sφ`; with `h_u ≤ 1`, `sφ ≤ 1`, `cφ² + sφ² = 1`: `D cφ ≤ cφ² + c sφ`, i.e.
`(D − cφ) cot φ ≤ c`. -/
theorem cl_core_i (hu c cphi sphi D : ℝ) (hphi : cphi ^ 2 + sphi ^ 2 = 1) (hs0 : 0 ≤ sphi)
    (hs1 : sphi ≤ 1) (hhu : hu ≤ 1) (h : D * cphi ≤ (hu + c - sphi) * sphi) :
    D * cphi ≤ cphi ^ 2 + c * sphi := by
  nlinarith [mul_le_mul_of_nonneg_right hhu hs0]

/-- **Lemma CL, case (ii)** [T]: X's right vertex `(cφ + sφ, X_low + sφ)` is above C's upper-left line,
`D ≤ s + sφ − (cφ + sφ − h_u) s / c`, written with `k = s / c = tan θ ≤ 1`: `D ≤ s + sφ − (cφ + sφ − h_u) k`,
`s = c k`, `h_u ≤ 1`, `0 ≤ sφ ≤ cφ`, `cφ² + sφ² = 1`, `c ≤ 1`, `0 ≤ k ≤ 1`: `D cφ ≤ cφ² + c sφ`. -/
theorem cl_core_ii (hu c s k cphi sphi D : ℝ) (hphi : cphi ^ 2 + sphi ^ 2 = 1) (hs0 : 0 ≤ sphi)
    (hsc : sphi ≤ cphi) (hc1 : c ≤ 1) (hc0 : 0 ≤ c) (hk0 : 0 ≤ k) (hk1 : k ≤ 1) (hsk : s = c * k)
    (hhu : hu ≤ 1) (h : D ≤ s + sphi - (cphi + sphi - hu) * k) :
    D * cphi ≤ cphi ^ 2 + c * sphi := by
  have hcphi0 : 0 ≤ cphi := by nlinarith
  have hw : 1 ≤ cphi + sphi := by nlinarith
  subst hsk
  nlinarith [mul_le_mul_of_nonneg_right h hcphi0, mul_nonneg hk0 hcphi0, mul_nonneg hc0 hcphi0,
             mul_nonneg (sub_nonneg.2 hsc) hcphi0,
             mul_nonneg (sub_nonneg.2 hhu) (mul_nonneg hk0 hcphi0),
             mul_nonneg (sub_nonneg.2 hc1) hcphi0,
             mul_nonneg (sub_nonneg.2 hk1) (mul_nonneg hcphi0 hcphi0),
             mul_nonneg (sub_nonneg.2 hw) (mul_nonneg hk0 hcphi0), mul_nonneg hs0 hcphi0,
             mul_nonneg (sub_nonneg.2 hk1) (mul_nonneg hs0 hcphi0),
             mul_nonneg (sub_nonneg.2 hc1) (mul_nonneg hk0 hcphi0)]

/-- **The centre is right of T_u's top edge, up to half a unit** [T]: `q_x ≥ r + 1/2` with `r > 0` (X's right
boundary), `q_y − L_h ≥ s`, `c² + s² = 1`, `0 < c ≤ 1`: `a_q = c (q_x − h_u) + s (q_y − L_h) > (1 − h_u c) − 1/2`. -/
theorem centre_right_core (c s hu r qx dy : ℝ) (h1 : c ^ 2 + s ^ 2 = 1) (hc : 0 < c) (hc1 : c ≤ 1)
    (hr : 0 < r) (hq : r + 1 / 2 ≤ qx) (hdy : s ≤ dy) (hs : 0 ≤ s) :
    1 - hu * c - 1 / 2 < c * (qx - hu) + s * dy := by
  nlinarith [mul_lt_mul_of_pos_left hr hc, mul_le_mul_of_nonneg_left hq hc.le,
             mul_le_mul_of_nonneg_left hdy hs, mul_nonneg (sub_nonneg.2 hc1) (by linarith : (0:ℝ) ≤ 1 / 2 + c)]

/-- The DISC LEMMA of strip_jam.md §5 (a point and three convex sets in the corner, five parameters):
[M] on the H1–H3 set, not proved: opaque. -/
opaque DiscLemma : Prop

/-- **STRIP₂-IN-JAM from the disc lemma** [T-prose] (strip_jam.md §4–§5): under H1–H3 and `DiscLemma` no unit
square of the quadrant interior-disjoint from `C` and `X` has an interior point in `T_u ∖ C`.  The ring
inequalities (U3)–(U6), (U8) of A271 are NOT assumed. -/
axiom strip_two_in_jam_of_disc (hjam : JamCorner) (hdisc : DiscLemma) (Q : Set RP)
    (h : PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q

/-- **The BL sectors of a JAM corner reduce to `pair3`** [T from `strip_two_in_jam_of_disc`]: A271's
`strip_two_in_ring_of_jam` with `RingIneq` replaced by `DiscLemma`. -/
theorem strip_two_in_ring_of_disc (hjam : JamCorner) (hdisc : DiscLemma)
    (hsub : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q)
    (hcover : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q →
      PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q)
    (hpair3 : ∀ Q, ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q) (Q : Set RP) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q :=
  fun h => hpair3 Q (hcover Q h (strip_two_in_jam_of_disc hjam hdisc Q (hsub Q h)))

#print axioms d_low_core
#print axioms cl_core_i
#print axioms cl_core_ii
#print axioms centre_right_core
#print axioms strip_two_in_ring_of_disc

end PackingCert.S11.OpenLemmas.StripJam
