import PackingCertMathlib.Statements.Open.NormalRing

/-!
# -- OPEN: BOX-MEETERS — who meets a corner box in normal form — A261

`docs/proofs/box_meeters.md`.  Setting: `n` unit squares in `[0, s]²`, `m = ⌈√n⌉`, `m − 1 < s < m`; the
corner statements are s-free (any `n`, any `s > 1 + √2`).

**What is a theorem here.**
* `same_wall_core` [T]: the arithmetic of SAME-WALL — Lemma PUSH (ii) applied both ways to two squares touching
  the same wall and meeting the open box asks `0 < n_u` and `0 < −n_u`.
* `blocker_side_core` [T]: the arithmetic of BLOCKER-SIDE — if the separating normal had both components
  positive, the blocker would sit in a right triangle with legs `β/n_u`, `β/n_v`, and a point `q` of the open
  box on the other side gives `1/u₀ + 1/v₀ > 1`: no unit square (SQUARE-IN-TRIANGLE).
* `strip_landing_core` [T]: for `ξ ≤ ψ ≤ α′` in `[0, π/2]` the direction `−(cos ψ, sin ψ)` has non-negative
  components along both wedge normals: `sin (α′ − ψ) ≥ 0`, `sin (ψ − ξ) ≥ 0`.
* `cert_core` [T]: weak duality, the soundness of a leaf certificate of `verify261.py` — non-negative
  multipliers on rows that are `≤ 0` on the feasible set give `S ≤ 0`; a positive lower bound of `S` refutes.
* `box_meeters`, `normal_ring_of_parts`, `only_ring_value_261` [T from the axioms below]: the chain.

**What is not.**
* `meeters_split` [T-prose] (box_meeters.md §0, §2): SAME-WALL + WEDGED-SEAL + TWO-CORNERS — in a family-stuck
  packing with no floating box meeter every box has exactly two meeters, touchers of its two walls, eight distinct.
* `touch_normal` [C] = NO-JAM(n): a normal-form family-stuck packing on the window has no floating box meeter.
  NOT a corner lemma: the JAMMED FLOATER (box_meeters.md §1.4) is a local counterexample with margin 0.009.
* `rows_classified` [C]: BOX-MEETERS + normal form + family-stuck ⟹ the hybrid normal ring (A258 §3, A260;
  its "pinwheel of rows" part is [T-computed] by the A261 certificates on tilts ≥ 0.703° and exactly flat walls).

**Status (2026-09-21).**  theorems: `same_wall_core`, `blocker_side_core`, `strip_landing_core`, `cert_core`,
`box_meeters`, `normal_ring_of_parts`, `only_ring_value_261`; axiom [T-prose]: `meeters_split`; axioms [C]:
`touch_normal`, `rows_classified`.
-/

namespace PackingCert.S11.OpenLemmas

/-- **SAME-WALL, arithmetic core** [T]. -/
theorem same_wall_core (nu : ℝ) (h1 : 0 < nu) (h2 : 0 < -nu) : False := by linarith

/-- **BLOCKER-SIDE, arithmetic core** [T]: legs `u₀ = β / n_u`, `v₀ = β / n_v`; `1/u₀ + 1/v₀ = n_u/β + n_v/β`. -/
theorem blocker_side_core (nx ny β qx qy : ℝ) (hx : 0 < nx) (hy : 0 < ny) (hβ : 0 < β)
    (hq : β ≤ nx * qx + ny * qy) (hqx : qx < 1) (hqy : qy < 1) : 1 < nx / β + ny / β := by
  have h1 : nx * qx < nx := by nlinarith
  have h2 : ny * qy < ny := by nlinarith
  have h : β < nx + ny := by linarith
  have h3 : 1 < (nx + ny) / β := (one_lt_div hβ).mpr h
  rwa [add_div] at h3

/-- **STRIP-LANDING, core** [T]. -/
theorem strip_landing_core (ξ ψ α : ℝ) (h0 : 0 ≤ ξ) (h1 : ξ ≤ ψ) (h2 : ψ ≤ α) (h3 : α ≤ Real.pi / 2) :
    0 ≤ Real.sin (α - ψ) ∧ 0 ≤ Real.sin (ψ - ξ) := by
  have hp := Real.pi_pos
  constructor
  · exact Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
  · exact Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)

/-- **Certificate soundness (weak duality)** [T]. -/
theorem cert_core {ι : Type} (t : Finset ι) (y r : ι → ℝ) (hy : ∀ i ∈ t, 0 ≤ y i)
    (hr : ∀ i ∈ t, r i ≤ 0) : Finset.sum t (fun i => y i * r i) ≤ 0 :=
  Finset.sum_nonpos (fun i hi => mul_nonpos_iff.mpr (Or.inl ⟨hy i hi, hr i hi⟩))

/-- Some doubly-met corner box has a meeter touching no wall (box_meeters.md §1; opaque). -/
opaque FloatingMeeter (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- BOX-MEETERS form (box_meeters.md §0; opaque): every corner box is met by exactly two squares, both wall
touchers, one on each of the box's walls, and the eight are distinct. -/
opaque BoxMeetersForm (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- [T-prose] SAME-WALL + WEDGED-SEAL + TWO-CORNERS (box_meeters.md §0, §2). -/
axiom meeters_split (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hfl : ¬ FloatingMeeter n m s Q) : BoxMeetersForm n m s Q

/-- **NO-JAM(n) = TOUCH-NORMAL** [C] (box_meeters.md §1.5), meant on the window `s ≤ ŝ`. -/
axiom touch_normal (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) : ¬ FloatingMeeter n m s Q

/-- **BOX-MEETERS(n)** [T from `touch_normal`, `meeters_split`]. -/
theorem box_meeters (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) : BoxMeetersForm n m s Q :=
  meeters_split n m s Q hP hlo hhi hfs (touch_normal n m s Q hP hlo hhi hfs hN)

/-- [C] the classification of the eight box meeters (A258 §3 + A260 + the A261 certificates). -/
axiom rows_classified (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) (hB : BoxMeetersForm n m s Q) : HasNormalRing n m s Q

/-- A258's `normal_ring`, split into its two obligations [T from the [C] axioms]. -/
theorem normal_ring_of_parts (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) : HasNormalRing n m s Q :=
  rows_classified n m s Q hP hlo hhi hfs hN (box_meeters n m s Q hP hlo hhi hfs hN)

/-- **ONLY-RING, value form, through BOX-MEETERS** [T from the axioms]. -/
theorem only_ring_value_261 (n m : ℕ) (s : ℝ) (hlo : (m : ℝ) - 1 < s) (hhi : s < m)
    (h : ∃ Q, IsPacking n s Q) :
    (∃ Q, IsPacking n s Q ∧ ¬ FamilyStuckN n m s Q) ∨
      (∃ Q, IsPacking n s Q ∧ HasNormalRing n m s Q) := by
  obtain ⟨Q, hQ, hN⟩ := exists_normalForm n m s h
  by_cases hfs : FamilyStuckN n m s Q
  · exact Or.inr ⟨Q, hQ, normal_ring_of_parts n m s Q hQ hlo hhi hfs hN⟩
  · exact Or.inl ⟨Q, hQ, hfs⟩

#print axioms same_wall_core
#print axioms blocker_side_core
#print axioms strip_landing_core
#print axioms cert_core
#print axioms box_meeters
#print axioms normal_ring_of_parts
#print axioms only_ring_value_261

end PackingCert.S11.OpenLemmas
