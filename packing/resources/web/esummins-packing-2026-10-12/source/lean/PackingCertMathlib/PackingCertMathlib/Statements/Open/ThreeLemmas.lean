import PackingCertMathlib.Statements.Open.OpenPairs

/-!
# -- OPEN: THREE LEMMAS — the near-flat cube (a theorem), the jammed sector (reduced to pair3 + STRIP), the
# non-serving gap (pieces) — A264

`docs/proofs/three_lemmas.md`.

**What is a theorem here.**
* `cube_pppm`, `cube_pmpm`, `cube_ppmm` [T]: the three mixed-sense rings of pairs with every tilt in `[0, ε₀]`,
  `ε₀ = π/256`, are infeasible for `s ≤ 3.8771` (in fact for `s < 3.981`).  Inputs: the wall identity
  `a_w + b_w ≤ s − 2` and the three CORNER LEMMAS of three_lemmas.md §3.2, stated as axioms on opaque corner
  predicates with the explicit constants `λ = 0.0062112`, `μ = 0.0124984`, `ν(A) = 0.0000753 + 0.0122724·A`
  (upper bounds of `ε₀/2 + ε₀²/2`, `ε₀²/2 + tan ε₀ (1 + sin ε₀)`, `ε₀²/2 + A tan ε₀`).  The proofs are `linarith`
  over the chain of §3.3; `slab_cube_264` packages them (A263's axiom `slab_cube` is discharged for rings of pairs).
* `jam_sector_of_strip` [T from `strip_lemma`]: given STRIP, the BL sectors of a JAM corner reduce to A262's `pair3`
  statement at that corner (three_lemmas.md §4.3) — `pair3` is carried as a hypothesis (its certificate runs).

**What is not.**
* `mixed_corner_pm`, `mixed_corner_mp`, `pinwheel_corner_pp` [T-prose]: the corner lemmas — exact SAT forms of
  §1.2 plus `1 − cos x ≤ x²/2`, `sin x ≤ x ≤ tan x` on `[0, ε₀]`; checked against exact SAT on 20 000 corners.
* `strip_lemma` [C]: a low free square of a JAM corner never enters the strip between the wall and C's left flank
  (`cmp264`: 0 of 323 rings violate it).
-/

namespace PackingCert.S11.OpenLemmas.ThreeLemmas

/-- A corner of type (σ_A, σ_B) with wall START offset `a`, floor END offset `b`, tilts in `[0, ε₀]`, both squares
meeting the open box and interior-disjoint: an opaque predicate (three_lemmas.md §1). -/
opaque CornerPM (a b : ℝ) : Prop
opaque CornerMP (a b : ℝ) : Prop
opaque CornerPP (a b : ℝ) : Prop

/-- **MC(+,−)** [T-prose] (§3.2): both offsets exceed `1 − λ`, `λ = ε₀/2 + ε₀²/2 ≤ 0.0062112`. -/
axiom mixed_corner_pm (a b : ℝ) (h : CornerPM a b) :
    1 - (62112 : ℝ) / 10000000 < a ∧ 1 - (62112 : ℝ) / 10000000 < b

/-- **MC(−,+)** [T-prose] (§3.2): one offset exceeds `1 − μ`, `μ = ε₀²/2 + tan ε₀ (1 + sin ε₀) ≤ 0.0124984`. -/
axiom mixed_corner_mp (a b : ℝ) (h : CornerMP a b) :
    1 - (124984 : ℝ) / 10000000 < a ∨ 1 - (124984 : ℝ) / 10000000 < b

/-- **PC(+,+)** [T-prose] (§3.2): the END offset `b` exceeds `1 − ε₀²/2 − a tan ε₀`, with `ε₀²/2 ≤ 0.0000753`,
`tan ε₀ ≤ 0.0122724`. -/
axiom pinwheel_corner_pp (a b : ℝ) (h : CornerPP a b) :
    1 - (753 : ℝ) / 10000000 - (122724 : ℝ) / 10000000 * a < b

/-- A ring of pairs with senses + + + − at side `s`, all tilts in `[0, ε₀]`: offsets in `[0, 1)`, wall identity
`a_w + b_w ≤ s − 2`, corner 0 of type (+,−) (A = wall 0, B = wall 3), corner 3 of type (−,+) (A = wall 3, B = wall 2),
corners 1, 2 of type (+,+). -/
theorem cube_pppm (s a0 a1 a2 a3 b0 b1 b2 b3 : ℝ) (hs : s ≤ (38771 : ℝ) / 10000)
    (ha : ∀ x ∈ ({a0, a1, a2, a3, b0, b1, b2, b3} : Set ℝ), 0 ≤ x ∧ x < 1)
    (w0 : a0 + b0 ≤ s - 2) (w1 : a1 + b1 ≤ s - 2) (w2 : a2 + b2 ≤ s - 2) (w3 : a3 + b3 ≤ s - 2)
    (c0 : CornerPM a0 b3) (c1 : CornerPP a1 b0) (c2 : CornerPP a2 b1) (c3 : CornerMP a3 b2) : False := by
  have h0 := mixed_corner_pm a0 b3 c0
  have h3 := mixed_corner_mp a3 b2 c3
  have h2 := pinwheel_corner_pp a2 b1 c2
  have h1 := pinwheel_corner_pp a1 b0 c1
  have ha0 := ha a0 (by simp); have ha1 := ha a1 (by simp); have ha2 := ha a2 (by simp)
  have ha3 := ha a3 (by simp); have hb0 := ha b0 (by simp); have hb1 := ha b1 (by simp)
  have hb2 := ha b2 (by simp); have hb3 := ha b3 (by simp)
  rcases h3 with h3 | h3
  · linarith [h0.2]
  · linarith [h0.1, h0.2, h3, h2, h1, ha0.1, ha1.1, ha2.1, ha3.1, hb0.1, hb1.1, hb2.1, hb3.1]

/-- + − + −: corners 0, 2 of type (+,−), corners 1, 3 of type (−,+). -/
theorem cube_pmpm (s a0 a1 a2 a3 b0 b1 b2 b3 : ℝ) (hs : s ≤ (38771 : ℝ) / 10000)
    (ha : ∀ x ∈ ({a0, a1, a2, a3, b0, b1, b2, b3} : Set ℝ), 0 ≤ x ∧ x < 1)
    (w0 : a0 + b0 ≤ s - 2) (w1 : a1 + b1 ≤ s - 2) (w2 : a2 + b2 ≤ s - 2) (w3 : a3 + b3 ≤ s - 2)
    (c0 : CornerPM a0 b3) (c1 : CornerMP a1 b0) (c2 : CornerPM a2 b1) (c3 : CornerMP a3 b2) : False := by
  have h0 := mixed_corner_pm a0 b3 c0
  have h2 := mixed_corner_pm a2 b1 c2
  have h1 := mixed_corner_mp a1 b0 c1
  have ha0 := ha a0 (by simp); have ha1 := ha a1 (by simp); have hb0 := ha b0 (by simp)
  rcases h1 with h1 | h1
  · linarith [h2.2]
  · linarith [h0.1]

/-- + + − −: corner 0 of type (+,−), corner 1 of type (+,+) suffice. -/
theorem cube_ppmm (s a0 a1 b0 b3 : ℝ) (hs : s ≤ (38771 : ℝ) / 10000)
    (ha0 : 0 ≤ a0 ∧ a0 < 1) (ha1 : 0 ≤ a1 ∧ a1 < 1) (hb0 : 0 ≤ b0 ∧ b0 < 1) (hb3 : 0 ≤ b3 ∧ b3 < 1)
    (w0 : a0 + b0 ≤ s - 2) (c0 : CornerPM a0 b3) (c1 : CornerPP a1 b0) : False := by
  have h0 := mixed_corner_pm a0 b3 c0
  have h1 := pinwheel_corner_pp a1 b0 c1
  linarith [h0.1, h1, ha1.1, ha1.2]

/-- **SLAB-CUBE for rings of pairs** [T]: the three mixed patterns in the cube are excluded at every `s ≤ 3.8771`
(three_lemmas.md §3.3).  A263's `slab_cube` covered + + + − and + − + −; + + − − is included for completeness. -/
theorem slab_cube_264 (s a0 a1 a2 a3 b0 b1 b2 b3 : ℝ) (hs : s ≤ (38771 : ℝ) / 10000)
    (ha : ∀ x ∈ ({a0, a1, a2, a3, b0, b1, b2, b3} : Set ℝ), 0 ≤ x ∧ x < 1)
    (w0 : a0 + b0 ≤ s - 2) (w1 : a1 + b1 ≤ s - 2) (w2 : a2 + b2 ≤ s - 2) (w3 : a3 + b3 ≤ s - 2) :
    ¬ ((CornerPM a0 b3 ∧ CornerPP a1 b0 ∧ CornerPP a2 b1 ∧ CornerMP a3 b2) ∨
       (CornerPM a0 b3 ∧ CornerMP a1 b0 ∧ CornerPM a2 b1 ∧ CornerMP a3 b2) ∨
       (CornerPM a0 b3 ∧ CornerPP a1 b0)) := by
  rintro (⟨c0, c1, c2, c3⟩ | ⟨c0, c1, c2, c3⟩ | ⟨c0, c1⟩)
  · exact cube_pppm s a0 a1 a2 a3 b0 b1 b2 b3 hs ha w0 w1 w2 w3 c0 c1 c2 c3
  · exact cube_pmpm s a0 a1 a2 a3 b0 b1 b2 b3 hs ha w0 w1 w2 w3 c0 c1 c2 c3
  · exact cube_ppmm s a0 a1 b0 b3 hs (ha a0 (by simp)) (ha a1 (by simp)) (ha b0 (by simp)) (ha b3 (by simp)) w0 c0 c1

/-- The BL-sector statements of a JAM corner (A262 §2.4), the STRIP property, and A262's `pair3` statement at the
corner with the floater's wall drop `T_u` as the wall square: opaque (three_lemmas.md §4.3). -/
opaque JamSectorFree (Q : Set RP) : Prop      -- Q is a unit square of the BL sectors avoiding A, A₂, X, C
opaque InStrip (Q : Set RP) : Prop            -- Q has an interior point in T_u ∖ C
opaque Pair3Free (Q : Set RP) : Prop          -- Q is a unit square of the BL sectors avoiding A, A₂, T_u

/-- **STRIP** [C] (§4.3): a low free square of a JAM corner never enters the strip between the wall and C's left
flank.  [M] 0 of 323 rings violate it (`cmp264`). -/
axiom strip_lemma (Q : Set RP) (h : JamSectorFree Q) : ¬ InStrip Q

/-- **The reduction** [T from `strip_lemma`]: avoiding `C` and not entering `T_u ∖ C` is avoiding `T_u` — stated as
the implication that the sector pocket of {A, A₂, X, C} lies in the pair3 pocket of {A, A₂, T_u} (the geometric
content `avoid C ∧ ¬ InStrip → avoid T_u` is the hypothesis `hcover`). -/
theorem jam_sector_of_strip (hcover : ∀ Q, JamSectorFree Q → ¬ InStrip Q → Pair3Free Q)
    (hpair3 : ∀ Q, ¬ Pair3Free Q) (Q : Set RP) : ¬ JamSectorFree Q :=
  fun h => hpair3 Q (hcover Q h (strip_lemma Q h))

#print axioms cube_pppm
#print axioms cube_pmpm
#print axioms cube_ppmm
#print axioms slab_cube_264
#print axioms jam_sector_of_strip

end PackingCert.S11.OpenLemmas.ThreeLemmas
