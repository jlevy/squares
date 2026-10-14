import PackingCertMathlib.Statements.Open.CommonSense

/-!
# -- OPEN: NORMAL-ROOM — the pocket of the normal ring holds ONE square — A259

`docs/proofs/normal_room.md`.  The NORMAL RING (A258, `family258.md`): four common-tilt PAIRS of one
sense, a pinwheel; parameters `(a_w, φ_w)` per wall and `s`; domain `D′`: `0 < φ_w < 45°`,
`a_w < 1`, `b_w < 1` (every corner box doubly met), the eight squares a packing.

**What is a theorem here.**
* `hole_one_tilt` [T]: HOLE-ONE in its tilt form — the algebra.  A unit square of tilt `θ`
  (`C = cos θ`, `S = sin θ`) whose centre is within `h` of a point `p` in both coordinates, with
  `h (C + S) ≤ 1/2`, has `p` within `1/2` of its centre along its edge direction: it contains `p`.
  (`h = (σ − w)/2` in a box of side `σ ≤ w + 1/w`; `σ ≤ 2` is A253's HOLE-ONE.)
* `tooth_flat` [T]: `cos φ (1 + sin φ) ≥ 1` on `[0°, 45°]` — a FLAT unit edge enters a tooth of a
  common-tilt pair by at most `sin φ (1 − cos φ)`, never below depth 1.
* `corner_frame_mono` [T]: in the corner frame the "misses the centre" form `(q − O).n ≥ 1/2` is
  monotone in `s` (the top of the side window is the worst case of the corner-PAIR lemma).
* `normalRoom_count` [T from the pierce]: if every non-ring square contains the container centre
  in its interior then `n ≤ 9`.
* `normalRoom_excludes` [T from `pair_pierce`]: no packing of 10 or more squares contains a normal
  ring on the window; with a NORMAL-RING hypothesis (A258) no row-normal packing of 11 is
  family-stuck.

**What is not.**
* `pair_pierce` [T-computed + C]: on the window every non-ring square of a packing containing a
  normal ring contains the centre.  Reduction to the four corner PAIRS: [T] (normal_room.md §2);
  the corner-PAIR lemma: [T-computed] by the box-valid certificate `certs/pair259_*` with its
  own verifier, EXCEPT the double-limit layer `e₀, δ₁ > 63/64` of each corner (obligation
  CORNER-NOTCH [C]; [M] on 6 177 sampled pairs and 0 counterexamples).
-/

namespace PackingCert.S11.OpenLemmas.NormalRoom

open Set

/-- **HOLE-ONE, tilt form** [T] (the algebra). -/
theorem hole_one_tilt (C S h a b : ℝ) (hC : 0 ≤ C) (hS : 0 ≤ S) (ha : |a| ≤ h) (hb : |b| ≤ h)
    (hw : h * (C + S) ≤ 1 / 2) : |C * a + S * b| ≤ 1 / 2 := by
  have h1 : |C * a + S * b| ≤ |C * a| + |S * b| := abs_add_le _ _
  have h2 : |C * a| = C * |a| := by rw [abs_mul, abs_of_nonneg hC]
  have h3 : |S * b| = S * |b| := by rw [abs_mul, abs_of_nonneg hS]
  have h4 : C * |a| ≤ C * h := mul_le_mul_of_nonneg_left ha hC
  have h5 : S * |b| ≤ S * h := mul_le_mul_of_nonneg_left hb hS
  nlinarith

/-- **TOOTH-FLAT** [T]: `c (1 + z) ≥ 1` for `c² + z² = 1`, `0 ≤ z ≤ c`. -/
theorem tooth_flat (c z : ℝ) (h1 : c ^ 2 + z ^ 2 = 1) (hz : 0 ≤ z) (hzc : z ≤ c) :
    1 ≤ c * (1 + z) := by
  have hc0 : 0 ≤ c := le_trans hz hzc
  have hc1 : c ≤ 1 := by nlinarith [sq_nonneg z]
  nlinarith [mul_nonneg hc0 (sub_nonneg.2 hc1), mul_nonneg hz (sub_nonneg.2 hzc)]

/-- **CORNER-FRAME MONOTONE** [T]: with the corner at the origin the centre is `(−s/2, s/2)`, and for
an outward normal `n` of the corner's quadrant (`n.1 − n.2 ≥ 0`) the form `(q − O).n` grows with `s`. -/
theorem corner_frame_mono (s t qx qy nx ny : ℝ) (hst : s ≤ t) (hn : 0 ≤ nx - ny) :
    (qx - (-(s / 2))) * nx + (qy - s / 2) * ny ≤ (qx - (-(t / 2))) * nx + (qy - t / 2) * ny := by
  nlinarith

/-- "`ι` enumerates a NORMAL RING of `Q`" (family258.md §2, domain `D′`; opaque). -/
opaque HasPairRing (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (ι : Fin 8 → Fin n) : Prop

/-- **PAIR-PIERCE** [T-computed + the CORNER-NOTCH layer C] (normal_room.md §2–3). -/
axiom pair_pierce (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (ι : Fin 8 → Fin n) (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (hring : HasPairRing n s Q ι) :
    ∀ j, j ∉ Set.range ι → ((s / 2, s / 2) : RP) ∈ interior (Q j)

/-- **NORMAL-ROOM, the count** [T]: a pierced pocket holds one square, so `n ≤ 8 + 1`. -/
theorem normalRoom_count (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (ι : Fin 8 → Fin n)
    (hpierce : ∀ j, j ∉ Set.range ι → ((s / 2, s / 2) : RP) ∈ interior (Q j)) : n ≤ 9 := by
  by_contra hn
  rw [not_le] at hn
  let T : Finset (Fin n) := (Finset.univ.image ι)ᶜ
  have himg : (Finset.univ.image ι).card ≤ 8 := by
    calc (Finset.univ.image ι).card ≤ (Finset.univ : Finset (Fin 8)).card := Finset.card_image_le
      _ = 8 := by simp
  have hT : 1 < T.card := by
    have : T.card = Fintype.card (Fin n) - (Finset.univ.image ι).card := Finset.card_compl _
    rw [this, Fintype.card_fin]
    omega
  obtain ⟨a, ha, b, hb, hab⟩ := Finset.one_lt_card.mp hT
  have hmem : ∀ x, x ∈ T → x ∉ Set.range ι := by
    intro x hx ⟨i, hi⟩
    have : x ∈ Finset.univ.image ι := Finset.mem_image.mpr ⟨i, Finset.mem_univ _, hi⟩
    exact (Finset.mem_compl.mp hx) this
  have hd := hP.interiorDisjoint a b hab
  exact Set.disjoint_left.mp hd (hpierce a (hmem a ha)) (hpierce b (hmem b hb))

/-- **NORMAL-ROOM(11) excludes** [T from `pair_pierce`]: on the window no packing of `n ≥ 10` unit
squares contains a normal ring. -/
theorem normalRoom_excludes (n : ℕ) (s : ℝ) (hn : 10 ≤ n) (hlo : (382 : ℝ) / 100 ≤ s)
    (hhi : s ≤ (38771 : ℝ) / 10000) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (ι : Fin 8 → Fin n) : ¬ HasPairRing n s Q ι := by
  intro hring
  have := normalRoom_count n s Q hP ι (pair_pierce n s Q hP ι hlo hhi hring)
  omega

/-- **The chain to FAMILY-STUCK-EXIST(11)** [T from `pair_pierce` and a NORMAL-RING hypothesis, which
is A258's conjecture]: if every row-normal family-stuck packing of 11 contains a normal ring, no
row-normal packing of 11 on the window is family-stuck. -/
theorem no_normal_family_stuck (s : ℝ) (hlo : (382 : ℝ) / 100 ≤ s)
    (hhi : s ≤ (38771 : ℝ) / 10000)
    (hNR : ∀ Q : Fin 11 → Set RP, IsPacking 11 s Q → FamilyStuckN 11 4 s Q → RowNormal 11 4 s Q →
      ∃ ι : Fin 8 → Fin 11, HasPairRing 11 s Q ι)
    (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q) (hN : RowNormal 11 4 s Q) :
    ¬ FamilyStuckN 11 4 s Q := by
  intro hfs
  obtain ⟨ι, hι⟩ := hNR Q hP hfs hN
  exact normalRoom_excludes 11 s (by norm_num) hlo hhi Q hP ι hι

#print axioms hole_one_tilt
#print axioms tooth_flat
#print axioms corner_frame_mono
#print axioms normalRoom_count
#print axioms normalRoom_excludes
#print axioms no_normal_family_stuck

end PackingCert.S11.OpenLemmas.NormalRoom
