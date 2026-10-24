import Sqpack.Rect3
import Sqpack.Rect4Core

/-!
# Four unit squares in a rectangle

`rect4_iff`: four unit squares (any angles) fit in `[0,w] × [0,h]` iff both sides are at least `1` and both are
at least `2`, or one is at least `4`, or the short side `H < 2` and the long side `L` satisfy
`L ≥ L(t, H) = 2 + (1 - 2(H - k - 1) sin t)/cos t + (1 - (H - 2k) cos t)/sin t`, `k = (cos t + sin t)/2`,
for some `t` (`Fried4`).  The boundary is Friedman's piece of `S₃` (Math Magic, June 2010; mostly Morandi),
given there by constructions; the lower bound `rect4_lower` is proved here.

Proof of the lower bound (`H < 2`), a chain as for `R₃` (`RectChain.lean`):
1. Sort the squares by centre `x`: `a, b, c, d`.  Left shelf on `b` (from `a`), right shelf on `c` (from `d`).
2. `separate_lr`: a line with unit direction `(C, S)` (`C ≥ 0`, `S > 0`, after a vertical mirror if needed)
   separates `b` from `c`: `b ⊆ {S x - C y ≤ s}`, `c ⊆ {S x - C y ≥ s}`.
3. `one_square` (`osl_set`): a square with a left shelf in `{S x - C y ≤ s}` has `s ≥ 2S - C(H - 1)` (an upright
   square at the top would do no better) or `C s ≥ C(S - C) + 1 + C + S - H` (the square at tilt `t` on the
   ceiling against the shelf's corner).  By witness case: the side vertex (`V`) and the edge above it (`U`) give
   the first; the edge below it (`D`) gives one of the two, through the two-angle inequalities `core_D1`,
   `core_D2` (`Rect4Core.lean`, half-angle factorisations).
4. The half turn about the rectangle's centre turns `c` into a square with a left shelf in
   `{S x - C y ≤ S L - C H - s}`; adding the two bounds (`combine4`) gives `L ≥ 4` or `L ≥ L(t, H)`.
   So the tilt of Friedman's packing is the direction of the line separating the two middle squares.

`rect4_friedman` builds Friedman's packing at any `t` with `L(t, H) < 4`.
-/

namespace SquarePacking

section one
variable {P Q x y lo H C S : ℝ}

/-- Case `U`, `σ ≤ 0`. -/
lemma os_U_neg (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 < S) (hlo' : lo ≤ H - 1)
    (hQ1 : Q ≤ 1) (l1 : y + (P - Q) / 2 < lo)
    (l3 : 0 ≤ Q * (x - 1 - (P + Q) / 2) + P * (lo - (y + (P - Q) / 2)))
    (hs : S * P + -C * Q ≤ 0)
    (rep : 2 * (S + C) ≤ (P + Q) * (S + C) + (-(S * P + -C * Q)) + (S * Q + C * P)) :
    0 ≤ Q * (S * x - C * y + (-(S * P + -C * Q) + (S * Q + C * P)) / 2 - (2 * S - C * (H - 1))) := by
  linarith [mul_nonneg hS.le l3, mul_nonneg (mul_nonneg hQ hC) (by linarith : 0 ≤ H - 1 - lo),
    mul_nonneg (by linarith : 0 ≤ lo - (y + (P - Q) / 2)) (by linarith : 0 ≤ -(S * P + -C * Q)),
    mul_nonneg hQ (by linarith : 0 ≤ (P + Q) * (S + C) + (-(S * P + -C * Q)) + (S * Q + C * P) - 2 * (S + C)),
    mul_nonneg (mul_nonneg hQ hC) (by linarith : 0 ≤ 1 - Q)]

/-- Case `U`, `σ ≥ 0`. -/
lemma os_U_pos (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 < S) (hPQ : P ^ 2 + Q ^ 2 = 1)
    (hy1 : (P + Q) / 2 ≤ y) (hlo' : lo ≤ H - 1) (hH : H < 2) (hP1 : P ≤ 1) (hQ1 : Q ≤ 1)
    (l3 : 0 ≤ Q * (x - 1 - (P + Q) / 2) + P * (lo - (y + (P - Q) / 2)))
    (hs : 0 ≤ S * P + -C * Q) :
    0 ≤ Q * (S * x - C * y + ((S * P + -C * Q) + (S * Q + C * P)) / 2 - (2 * S - C * (H - 1))) := by
  have e1 : S * P ^ 2 + S * Q ^ 2 = S := by linear_combination S * hPQ
  linarith [mul_nonneg hS.le l3, mul_nonneg hs (by linarith : 0 ≤ y - (P + Q) / 2),
    mul_nonneg (mul_nonneg hS.le hP) (by linarith : 0 ≤ H - 1 - lo),
    mul_nonneg hs (by linarith : 0 ≤ 2 - H),
    mul_nonneg (by linarith : 0 ≤ 1 - Q)
      (add_nonneg (mul_nonneg hC hQ) (mul_nonneg hS.le (by linarith : 0 ≤ 1 - P)))]

/-- Case `D`: `P T ≥ P (S - C) + P σ⁺ + γ (1 + P + Q - H)`, for `s = |σ|`. -/
lemma os_D_bound (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 < S) (hP : 0 ≤ P) (hlo : 0 ≤ lo)
    (hy2 : y ≤ H - (P + Q) / 2)
    (l3 : 0 ≤ P * (x - 1 - (P + Q) / 2) + Q * (y + (P - Q) / 2 - lo - 1)) (s : ℝ)
    (hs : s = S * P + -C * Q ∨ s = -(S * P + -C * Q)) :
    P * (S - C) + P * ((s + (S * P + -C * Q)) / 2) + (S * Q + C * P) * (1 + P + Q - H) ≤
      P * (S * x - C * y + (s + (S * Q + C * P)) / 2) := by
  have hγ0 : 0 ≤ S * Q + C * P := add_nonneg (mul_nonneg hS.le hQ) (mul_nonneg hC hP)
  rcases hs with rfl | rfl <;>
  linarith [mul_nonneg hS.le l3, mul_nonneg (mul_nonneg hS.le hQ) hlo,
    mul_nonneg hγ0 (by linarith : 0 ≤ H - (P + Q) / 2 - y)]

/-- Case `D`, `σ ≥ 0` (`core_D1`). -/
lemma os_D1 (hP0 : 0 < P) (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 < S) (hPQ : P ^ 2 + Q ^ 2 = 1)
    (hCS : C ^ 2 + S ^ 2 = 1) (hs : 0 ≤ S * P + -C * Q) {T : ℝ}
    (b : P * (S - C) + P * (((S * P + -C * Q) + (S * P + -C * Q)) / 2) +
      (S * Q + C * P) * (1 + P + Q - H) ≤ P * T) :
    2 * S - C * (H - 1) ≤ T ∨ C * (S - C) + (1 + C + S - H) ≤ C * T := by
  have core := core_D1 hP0.le hQ hC hS.le hPQ hCS (by linarith)
  have idD1 : S * (P * (S - C) + P * (S * P + -C * Q) + (S * Q + C * P) * (1 + P + Q - H)) =
      Q * (C * (S - C) + (1 + C + S - H)) + (S * P + -C * Q) * (2 * S - C * (H - 1)) +
        polyD1 P Q C S := by
    simp only [polyD1]; linear_combination S * (C + S) * hPQ + (-Q * (H - 2)) * hCS
  have hSP : 0 < S * P := mul_pos hS hP0
  have b' := mul_le_mul_of_nonneg_left b hS.le
  rcases le_total (C * (S - C) + (1 + C + S - H)) (C * (2 * S - C * (H - 1))) with hψ | hψ
  · right
    have h : 0 ≤ S * P * (C * T - (C * (S - C) + (1 + C + S - H))) := by
      nlinarith [mul_nonneg hs (sub_nonneg.2 hψ), mul_nonneg hC core]
    have := (mul_nonneg_iff_of_pos_left hSP).1 h; linarith
  · left
    have h : 0 ≤ S * P * (T - (2 * S - C * (H - 1))) := by
      nlinarith [mul_le_mul_of_nonneg_left hψ hQ]
    have := (mul_nonneg_iff_of_pos_left hSP).1 h; linarith

/-- Case `D`, `σ ≤ 0` (`core_D2`). -/
lemma os_D2 (hP0 : 0 < P) (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 < S) (hPQ : P ^ 2 + Q ^ 2 = 1)
    (hCS : C ^ 2 + S ^ 2 = 1) (hH : H < 2) (hs : S * P + -C * Q ≤ 0) {T : ℝ}
    (b : P * (S - C) + P * ((-(S * P + -C * Q) + (S * P + -C * Q)) / 2) +
      (S * Q + C * P) * (1 + P + Q - H) ≤ P * T) :
    C * (S - C) + (1 + C + S - H) ≤ C * T := by
  have core := core_D2 hP0.le hQ hC hS.le hPQ hCS (by linarith)
  have idD2 : C * (P * (S - C) + (S * Q + C * P) * (1 + P + Q - H)) - P * (C * (S - C) + (1 + C + S - H)) =
      polyD2 P Q C S + (2 - H) * (-S * (S * P + -C * Q)) := by
    simp only [polyD2]; linear_combination (-P * (H - 2)) * hCS
  have h : 0 ≤ P * (C * T - (C * (S - C) + (1 + C + S - H))) := by
    nlinarith [mul_le_mul_of_nonneg_left b hC, mul_nonneg (by linarith : 0 ≤ 2 - H)
      (mul_nonneg hS.le (by linarith : 0 ≤ -(S * P + -C * Q)))]
  have := (mul_nonneg_iff_of_pos_left hP0).1 h; linarith

end one

/-- The support of the framed square `(P, Q)`, centre `(x, y)`, in the direction `(S, -C)`. -/
noncomputable def suppT (C S P Q x y : ℝ) : ℝ :=
  S * x - C * y + (|S * P + -C * Q| + |-S * Q + -C * P|) / 2

/-- **One square.** -/
theorem one_square {P Q x y lo H C S : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hPQ : P ^ 2 + Q ^ 2 = 1)
    (hy1 : (P + Q) / 2 ≤ y) (hy2 : y ≤ H - (P + Q) / 2) (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hH : H < 2)
    (hw : Wit P Q y lo (x - 1 - (P + Q) / 2)) (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1) :
    2 * S - C * (H - 1) ≤ suppT C S P Q x y ∨
      C * (S - C) + (1 + C + S - H) ≤ C * suppT C S P Q x y := by
  unfold suppT
  have hγ : |-S * Q + -C * P| = S * Q + C * P := by
    rw [abs_of_nonpos (by nlinarith [mul_nonneg hS.le hQ, mul_nonneg hC hP])]; ring
  have rep := upright_repl P Q S (-C) hP hQ hPQ hS.le
  rw [hγ, abs_neg, abs_of_nonneg hC] at rep
  rw [hγ]
  have hk : 1 ≤ P + Q := by nlinarith
  have hP1 : P ≤ 1 := by nlinarith
  have hQ1 : Q ≤ 1 := by nlinarith
  rcases hw with hA | ⟨l1, l2, l3⟩ | ⟨l1, l2, l3⟩
  · -- V: the side vertex clears the wall square
    left
    linarith [mul_le_mul_of_nonneg_left hA hS.le, mul_le_mul_of_nonneg_left hy2 hC]
  · -- U: the edge above the side vertex meets the band's bottom
    left
    have hQ0 : 0 < Q := by linarith
    rcases le_total (S * P + -C * Q) 0 with hs | hs
    · rw [abs_of_nonpos hs] at rep ⊢
      have := (mul_nonneg_iff_of_pos_left hQ0).1 (os_U_neg hQ hC hS hlo' hQ1 l1 l3 hs rep)
      linarith
    · rw [abs_of_nonneg hs]
      have := (mul_nonneg_iff_of_pos_left hQ0).1 (os_U_pos hP hQ hC hS hPQ hy1 hlo' hH hP1 hQ1 l3 hs)
      linarith
  · -- D: the edge below the side vertex meets the band's top
    have hP0 : 0 < P := by linarith
    rcases le_total 0 (S * P + -C * Q) with hs | hs
    · rw [abs_of_nonneg hs]
      exact os_D1 hP0 hQ hC hS hPQ hCS hs (os_D_bound hQ hC hS hP hlo hy2 l3 _ (Or.inl rfl))
    · rw [abs_of_nonpos hs]
      exact Or.inr (os_D2 hP0 hQ hC hS hPQ hCS hH hs (os_D_bound hQ hC hS hP hlo hy2 l3 _ (Or.inr rfl)))

/-! ## Squares against a shelf, in the four orientations -/

/-- **One square, set form.**  A square with a left shelf in the half-plane `S x - C y ≤ s`. -/
theorem osl_set {c : ℝ × ℝ} {θ L H lo C S s : ℝ} (hin : sq c θ 1 ⊆ rbox L H) (hH : H < 2)
    (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hl : ∀ p ∈ sq c θ 1, lo ≤ p.2 → p.2 ≤ lo + 1 → 1 ≤ p.1)
    (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1)
    (hs : ∀ p ∈ sq c θ 1, S * p.1 + -C * p.2 ≤ s) :
    2 * S - C * (H - 1) ≤ s ∨ C * (S - C) + (1 + C + S - H) ≤ C * s := by
  obtain ⟨P, Q, hP, hQ, hPQ, -, -, hy1, hy2, hpt⟩ := framed hin
  have hk : 1 ≤ P + Q := by nlinarith
  have hw := witness (x := c.1) (by linarith) (by linarith)
    (fun u v hu hv h1 h2 => hl _ (hpt u v hu hv) h1 h2)
  have hT : suppT C S P Q c.1 c.2 ≤ s := by
    have := support_le hpt hs; unfold suppT; linarith
  rcases one_square hP hQ hPQ hy1 hy2 hlo hlo' hH hw hC hS hCS with h | h
  · left; linarith
  · right; nlinarith [mul_le_mul_of_nonneg_left hT hC]

/-- A square with a left shelf in the half-plane `S x + C y ≤ s` (vertical mirror). -/
theorem osl_set_up {c : ℝ × ℝ} {θ L H lo C S s : ℝ} (hin : sq c θ 1 ⊆ rbox L H) (hH : H < 2)
    (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hl : ∀ p ∈ sq c θ 1, lo ≤ p.2 → p.2 ≤ lo + 1 → 1 ≤ p.1)
    (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1)
    (hs : ∀ p ∈ sq c θ 1, S * p.1 + C * p.2 ≤ s) :
    2 * S - C * (H - 1) ≤ s - C * H ∨ C * (S - C) + (1 + C + S - H) ≤ C * (s - C * H) := by
  refine osl_set (sq_vmir_subset hin) hH (lo := H - 1 - lo) (by linarith) (by linarith)
    (fun q hq h1 h2 => ?_) hC hS hCS (fun q hq => ?_)
  · rw [← vmir_vmir H q, mem_sq_vmir] at hq
    have := hl (vmir H q) hq (by simp only [vmir]; linarith) (by simp only [vmir]; linarith)
    simpa only [vmir] using this
  · rw [← vmir_vmir H q, mem_sq_vmir] at hq
    have := hs _ hq; simp only [vmir] at this; linarith

/-- A square with a right shelf in the half-plane `S x - C y ≥ s` (half turn). -/
theorem osl_set_rot {c : ℝ × ℝ} {θ L H lo C S s : ℝ} (hin : sq c θ 1 ⊆ rbox L H) (hH : H < 2)
    (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hr : ∀ p ∈ sq c θ 1, lo ≤ p.2 → p.2 ≤ lo + 1 → p.1 ≤ L - 1)
    (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1)
    (hs : ∀ p ∈ sq c θ 1, s ≤ S * p.1 + -C * p.2) :
    2 * S - C * (H - 1) ≤ S * L - C * H - s ∨
      C * (S - C) + (1 + C + S - H) ≤ C * (S * L - C * H - s) := by
  refine osl_set (sq_rot_subset hin) hH (lo := H - 1 - lo) (by linarith) (by linarith)
    (fun q hq h1 h2 => ?_) hC hS hCS (fun q hq => ?_)
  · rw [← rot_rot L H q, mem_sq_rot] at hq
    have := hr _ hq (by simp only [rot]; linarith) (by simp only [rot]; linarith)
    simp only [rot] at this; linarith
  · rw [← rot_rot L H q, mem_sq_rot] at hq
    have := hs _ hq; simp only [rot] at this; linarith

/-- A square with a right shelf in the half-plane `S x + C y ≥ s` (horizontal mirror). -/
theorem osl_set_mir {c : ℝ × ℝ} {θ L H lo C S s : ℝ} (hin : sq c θ 1 ⊆ rbox L H) (hH : H < 2)
    (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hr : ∀ p ∈ sq c θ 1, lo ≤ p.2 → p.2 ≤ lo + 1 → p.1 ≤ L - 1)
    (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1)
    (hs : ∀ p ∈ sq c θ 1, s ≤ S * p.1 + C * p.2) :
    2 * S - C * (H - 1) ≤ S * L - s ∨ C * (S - C) + (1 + C + S - H) ≤ C * (S * L - s) := by
  refine osl_set (sq_mir_subset hin) hH (lo := lo) hlo hlo' (fun q hq h1 h2 => ?_) hC hS hCS
    (fun q hq => ?_)
  · rw [← mir_mir L q, mem_sq_mir] at hq
    have := hr _ hq h1 h2; simp only [mir] at this; linarith
  · rw [← mir_mir L q, mem_sq_mir] at hq
    have := hs _ hq; simp only [mir] at this; linarith

/-- Adding the two halves. -/
theorem combine4 {C S H L X Y : ℝ} (hC : 0 ≤ C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1) (hH : H < 2)
    (hXY : X + Y = S * L - C * H)
    (hX : 2 * S - C * (H - 1) ≤ X ∨ C * (S - C) + (1 + C + S - H) ≤ C * X)
    (hY : 2 * S - C * (H - 1) ≤ Y ∨ C * (S - C) + (1 + C + S - H) ≤ C * Y) :
    4 ≤ L ∨ (0 < C ∧ 2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L) := by
  have hS1 : S ≤ 1 := by nlinarith
  -- `C = 0` leaves only the upright branch
  rcases eq_or_lt_of_le hC with h0 | hC0
  · subst h0
    have hS1' : S = 1 := by nlinarith
    subst hS1'
    left
    rcases hX with hX | hX <;> rcases hY with hY | hY <;> nlinarith
  rcases le_total (C * (S - C) + (1 + C + S - H)) (C * (2 * S - C * (H - 1))) with hψ | hψ
  · right
    refine ⟨hC0, ?_⟩
    have hx : C * (S - C) + (1 + C + S - H) ≤ C * X := by
      rcases hX with hX | hX
      · nlinarith [mul_le_mul_of_nonneg_left hX hC]
      · exact hX
    have hy : C * (S - C) + (1 + C + S - H) ≤ C * Y := by
      rcases hY with hY | hY
      · nlinarith [mul_le_mul_of_nonneg_left hY hC]
      · exact hY
    nlinarith
  · left
    have hx : 2 * S - C * (H - 1) ≤ X := by
      rcases hX with hX | hX
      · exact hX
      · exact le_of_mul_le_mul_left (by linarith) hC0
    have hy : 2 * S - C * (H - 1) ≤ Y := by
      rcases hY with hY | hY
      · exact hY
      · exact le_of_mul_le_mul_left (by linarith) hC0
    have : 4 * S ≤ S * L := by nlinarith
    nlinarith

/-! ## Four squares -/

/-- **Four unit squares, lower bound.**  If four unit squares pack `[0,L] × [0,H]` with `H < 2`, then
`L ≥ 4`, or `S C L ≥ 2C(S - C) + 2(1 + C + S - H) + C² H` for some unit `(C, S)`, `C, S > 0`: that is,
`L ≥ L(t, H) = 2 + (1 - 2(H - k - 1) sin t)/cos t + (1 - (H - 2k) cos t)/sin t`, `k = (cos t + sin t)/2`,
Friedman's piece of `S₃` (mostly Morandi).  `(C, S)` is the direction of a line separating the middle two
squares. -/
theorem rect4_lower {L H : ℝ} (hp : RectPacks 4 L H) (hH : H < 2) :
    4 ≤ L ∨ ∃ C S : ℝ, 0 < C ∧ 0 < S ∧ C ^ 2 + S ^ 2 = 1 ∧
      2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L := by
  obtain ⟨ctr, ang, hin, hd⟩ := hp
  set σ := Tuple.sort (fun i => (ctr i).1)
  have hm := Tuple.monotone_sort (fun i => (ctr i).1)
  have hne : ∀ i j : Fin 4, i ≠ j → σ i ≠ σ j := fun i j h => σ.injective.ne h
  have h01 : (ctr (σ 0)).1 ≤ (ctr (σ 1)).1 := hm (by decide)
  have h12 : (ctr (σ 1)).1 ≤ (ctr (σ 2)).1 := hm (by decide)
  have h23 : (ctr (σ 2)).1 ≤ (ctr (σ 3)).1 := hm (by decide)
  obtain ⟨lo, l0, l1, hl⟩ := left_shelf (hin (σ 0)) (hin (σ 1)) (hd _ _ (hne 0 1 (by decide))) h01 hH
  obtain ⟨lo2, r0, r1, hr⟩ :=
    right_shelf (hin (σ 2)) (hin (σ 3)) (hd _ _ (hne 2 3 (by decide))) h23 hH
  obtain ⟨u1, u2, s, hu1, hb, hc⟩ :=
    separate_lr (hin (σ 1)) (hin (σ 2)) (hd _ _ (hne 1 2 (by decide))) h12 hH
  set r := Real.sqrt (u1 ^ 2 + u2 ^ 2)
  have hr0 : 0 < r := Real.sqrt_pos.2 (by positivity)
  have hr2 : r ^ 2 = u1 ^ 2 + u2 ^ 2 := Real.sq_sqrt (by positivity)
  have hS : 0 < u1 / r := div_pos hu1 hr0
  have hC : 0 ≤ |u2| / r := div_nonneg (abs_nonneg _) hr0.le
  have hCS : (|u2| / r) ^ 2 + (u1 / r) ^ 2 = 1 := by
    rw [div_pow, div_pow, sq_abs]; field_simp; linarith
  have scale : ∀ a b : ℝ, a ≤ b → a / r ≤ b / r := fun a b h => div_le_div_of_nonneg_right h hr0.le
  have fin := fun X Y hXY hX hY => combine4 (L := L) (X := X) (Y := Y) hC hS hCS hH hXY hX hY
  have out : ∀ C S : ℝ, (4 ≤ L ∨ (0 < C ∧ 2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L)) →
      0 < S → C ^ 2 + S ^ 2 = 1 → (4 ≤ L ∨ ∃ C S : ℝ, 0 < C ∧ 0 < S ∧ C ^ 2 + S ^ 2 = 1 ∧
        2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L) := by
    rintro C S (h | ⟨h1, h2⟩) hS hCS
    · exact Or.inl h
    · exact Or.inr ⟨C, S, h1, hS, hCS, h2⟩
  refine out _ _ ?_ hS hCS
  rcases le_total u2 0 with hu2 | hu2
  · have e : ∀ p : ℝ × ℝ, u1 / r * p.1 + -(|u2| / r) * p.2 = (u1 * p.1 + u2 * p.2) / r := by
      intro p; rw [abs_of_nonpos hu2]; field_simp
    have hX := osl_set (hin (σ 1)) hH l0 l1 hl hC hS hCS (s := s / r)
      (fun p hp => by rw [e]; exact scale _ _ (hb p hp))
    have hY := osl_set_rot (hin (σ 2)) hH r0 r1 hr hC hS hCS (s := s / r)
      (fun p hp => by rw [e]; exact scale _ _ (hc p hp))
    exact fin _ _ (by ring) hX hY
  · have e : ∀ p : ℝ × ℝ, u1 / r * p.1 + |u2| / r * p.2 = (u1 * p.1 + u2 * p.2) / r := by
      intro p; rw [abs_of_nonneg hu2]; field_simp
    have hX := osl_set_up (hin (σ 1)) hH l0 l1 hl hC hS hCS (s := s / r)
      (fun p hp => by rw [e]; exact scale _ _ (hb p hp))
    have hY := osl_set_mir (hin (σ 2)) hH r0 r1 hr hC hS hCS (s := s / r)
      (fun p hp => by rw [e]; exact scale _ _ (hc p hp))
    exact fin _ _ (by ring) hX hY

/-! ## Constructions -/

/-- Widening the box keeps a packing. -/
lemma RectPacks.mono {n : ℕ} {w h w' : ℝ} (hp : RectPacks n w h) (hw : w ≤ w') : RectPacks n w' h := by
  obtain ⟨ctr, ang, hin, hd⟩ := hp
  refine ⟨ctr, ang, fun i p hp => ?_, hd⟩
  have := hin i hp
  simp only [rbox, Set.mem_ofPred_eq] at this ⊢
  exact ⟨this.1, by linarith [this.2.1], this.2.2⟩

/-- Horizontal extent of an open tilted unit square: `|p₁ - c₁| < (C + S)/2`. -/
lemma sqInt_x {c p : ℝ × ℝ} {θ C S : ℝ} (hcos : Real.cos θ = C) (hsin : Real.sin θ = S)
    (hC : 0 < C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1) (h : p ∈ sqInt c θ 1) :
    c.1 - (C + S) / 2 < p.1 ∧ p.1 < c.1 + (C + S) / 2 := by
  obtain ⟨h1, h2⟩ := h
  simp only [coord, hcos, hsin] at h1 h2
  rw [abs_lt] at h1 h2
  have e : p.1 - c.1 = C * ((p.1 - c.1) * C + (p.2 - c.2) * S) - S * (-(p.1 - c.1) * S + (p.2 - c.2) * C) := by
    linear_combination (-(p.1 - c.1)) * hCS
  constructor <;> nlinarith [mul_lt_mul_of_pos_left h1.1 hC, mul_lt_mul_of_pos_left h1.2 hC,
    mul_lt_mul_of_pos_left h2.1 hS, mul_lt_mul_of_pos_left h2.2 hS]

/-- **Friedman's packing** (piece of `S₃`, mostly Morandi): uprights in two opposite corners, two squares at
tilt `t` (`(C, S) = (cos t, sin t)`) between them, one on the ceiling against the left upright's corner, one
on the floor against the right upright's corner, edge to edge.  It needs width
`L(t, H) = 2 + (1 - 2(H - k - 1)S)/C + (1 - (H - 2k)C)/S`; valid whenever that is below `4`. -/
theorem rect4_friedman {C S H L : ℝ} (hC : 0 < C) (hS : 0 < S) (hCS : C ^ 2 + S ^ 2 = 1) (hH : H < 2)
    (hL : 2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L) (hL4 : L < 4) :
    RectPacks 4 L H := by
  set k := (C + S) / 2 with hk
  set xb := 1 + (1 / 2 - (H - k - 1) * S) / C with hxb
  set L0 := 2 * xb + (1 - (H - 2 * k) * C) / S with hL0
  have hxbC : C * xb = C + 1 / 2 - (H - k - 1) * S := by simp only [hxb]; field_simp; ring
  have hL0S : S * L0 = 2 * S * xb + 1 - (H - 2 * k) * C := by simp only [hL0]; field_simp; ring
  have hSC : 0 < S * C := mul_pos hS hC
  have eL0 : S * C * L0 = 2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H := by
    linear_combination C * hL0S + 2 * S * hxbC + (C - 2 * H + S + 2) * hCS
  have hLL : L0 ≤ L := le_of_mul_le_mul_left (by linarith) hSC
  -- the height is at least `3/2`, so both tilted squares fit between floor and ceiling
  have hH32 : 3 / 2 ≤ H := by
    by_contra hc; push Not at hc
    have : S * C * L0 < 4 * (S * C) := by nlinarith
    nlinarith [sq_nonneg (C - S), sq_nonneg (C + S - 1), mul_pos hC hS]
  have hk2 : 2 * k ≤ H := by nlinarith [sq_nonneg (C - S)]
  have hk1 : 1 ≤ 2 * k := by nlinarith
  -- `x_b ≥ k` and `x_c - k ≥ 1` (`x_c = L0 - x_b`)
  have F2 : k ≤ xb := by
    have : 0 ≤ C * (xb - k) := by
      nlinarith [sq_nonneg (C - S), mul_pos hC hS, mul_nonneg hS.le (by linarith : (0 : ℝ) ≤ 2 - H),
        mul_nonneg (mul_nonneg hS.le hS.le) (by nlinarith : (0 : ℝ) ≤ 1 - S)]
    exact sub_nonneg.1 ((mul_nonneg_iff_of_pos_left hC).1 this)
  have F3 : 1 + k ≤ L0 - xb := by
    have g := core_g hC.le hS.le hCS
    have : 0 ≤ S * C * (L0 - xb - k - 1) := by
      have e : S * C * (L0 - xb - k - 1) = (S / 2 + C - S ^ 2 - 2 * C ^ 2 + (C + S) / 2 *
          (S ^ 2 - C * S + 2 * C ^ 2)) + (2 - H) := by
        linear_combination C * hL0S + S * hxbC + (2 - H) * hCS
      rw [e]; linarith
    have := (mul_nonneg_iff_of_pos_left hSC).1 this; linarith
  -- the angle
  set θ := Real.arccos C
  have hcos : Real.cos θ = C := Real.cos_arccos (by linarith) (by nlinarith)
  have hsin : Real.sin θ = S := by
    rw [Real.sin_arccos, show 1 - C ^ 2 = S ^ 2 by linarith]; exact Real.sqrt_sq hS.le
  have hkθ : (|Real.cos θ| + |Real.sin θ|) / 2 = k := by rw [hcos, hsin, abs_of_pos hC, abs_of_pos hS]
  refine RectPacks.mono ?_ hLL
  refine ⟨![(1 / 2, 1 / 2), (xb, H - k), (L0 - xb, k), (L0 - 1 / 2, H - 1 / 2)], ![0, θ, θ, 0], ?_, ?_⟩
  · intro i
    fin_cases i
    · exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
    · show sq (xb, H - k) θ 1 ⊆ rbox L0 H
      apply sq_subset_rbox <;> rw [hkθ] <;> simp only <;> linarith
    · show sq (L0 - xb, k) θ 1 ⊆ rbox L0 H
      apply sq_subset_rbox <;> rw [hkθ] <;> simp only <;> linarith
    · exact sq_zero_subset (by simp; linarith) (by simp) (by simp; linarith) (by simp)
  · -- interiors: each pair is split by a line
    have iA : ∀ p, p ∈ sqInt ((1 / 2, 1 / 2) : ℝ × ℝ) 0 1 → p.1 < 1 ∧ p.2 < 1 := by
      intro p hp; rw [sqInt_zero, abs_lt, abs_lt] at hp; simp only at hp; constructor <;> linarith
    have iD : ∀ p, p ∈ sqInt ((L0 - 1 / 2, H - 1 / 2) : ℝ × ℝ) 0 1 → L0 - 1 < p.1 ∧ H - 1 < p.2 := by
      intro p hp; rw [sqInt_zero, abs_lt, abs_lt] at hp; simp only at hp; constructor <;> linarith
    have iT : ∀ c p : ℝ × ℝ, p ∈ sqInt c θ 1 →
        -(1 / 2) < (p.1 - c.1) * C + (p.2 - c.2) * S ∧ (p.1 - c.1) * C + (p.2 - c.2) * S < 1 / 2 ∧
        -(1 / 2) < -(p.1 - c.1) * S + (p.2 - c.2) * C ∧ -(p.1 - c.1) * S + (p.2 - c.2) * C < 1 / 2 := by
      intro c p hp
      obtain ⟨h1, h2⟩ := hp
      simp only [coord, hcos, hsin] at h1 h2
      rw [abs_lt] at h1 h2
      exact ⟨h1.1, h1.2, h2.1, h2.2⟩
    have dAB : Disjoint (sqInt ((1 / 2, 1 / 2) : ℝ × ℝ) 0 1) (sqInt (xb, H - k) θ 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      obtain ⟨a1, a2⟩ := iA p h1; obtain ⟨b1, -, -, -⟩ := iT _ p h2
      simp only at b1
      linarith [mul_lt_mul_of_pos_left a1 hC, mul_lt_mul_of_pos_left a2 hS]
    have dCD : Disjoint (sqInt (L0 - xb, k) θ 1) (sqInt ((L0 - 1 / 2, H - 1 / 2) : ℝ × ℝ) 0 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      obtain ⟨-, c2, -, -⟩ := iT _ p h1; obtain ⟨d1, d2⟩ := iD p h2
      simp only at c2
      linarith [mul_lt_mul_of_pos_left d1 hC, mul_lt_mul_of_pos_left d2 hS]
    have dBC : Disjoint (sqInt (xb, H - k) θ 1) (sqInt (L0 - xb, k) θ 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      obtain ⟨-, -, b3, -⟩ := iT _ p h1; obtain ⟨-, -, -, c4⟩ := iT _ p h2
      simp only at b3 c4
      linarith
    have dAC : Disjoint (sqInt ((1 / 2, 1 / 2) : ℝ × ℝ) 0 1) (sqInt (L0 - xb, k) θ 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      have h3 := (sqInt_x hcos hsin hC hS hCS h2).1; have h4 := (iA p h1).1
      simp only at h3; linarith
    have dBD : Disjoint (sqInt (xb, H - k) θ 1) (sqInt ((L0 - 1 / 2, H - 1 / 2) : ℝ × ℝ) 0 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      have h3 := (sqInt_x hcos hsin hC hS hCS h1).2; have h4 := (iD p h2).1
      simp only at h3; linarith
    have dAD : Disjoint (sqInt ((1 / 2, 1 / 2) : ℝ × ℝ) 0 1) (sqInt ((L0 - 1 / 2, H - 1 / 2) : ℝ × ℝ) 0 1) := by
      rw [Set.disjoint_left]; intro p h1 h2
      have := (iA p h1).1; have := (iD p h2).1; linarith
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | exact absurd rfl hij | exact dAB | exact dAB.symm | exact dAC | exact dAC.symm | exact dAD | exact dAD.symm | exact dBC | exact dBC.symm | exact dBD | exact dBD.symm | exact dCD | exact dCD.symm

/-- Four in a row. -/
theorem rect4_row {w h : ℝ} (hw : 4 ≤ w) (hh : 1 ≤ h) : RectPacks 4 w h := by
  apply upright_pack ![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (5 / 2, 1 / 2), (7 / 2, 1 / 2)]
  · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
      (by norm_num) (by simp; linarith)
  · intro i j hij; left
    fin_cases i <;> fin_cases j <;> simp at hij ⊢ <;> norm_num [abs_of_pos, abs_of_neg]

/-- A `2 × 2` block. -/
theorem rect4_block {w h : ℝ} (hw : 2 ≤ w) (hh : 2 ≤ h) : RectPacks 4 w h := by
  apply upright_pack ![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (1 / 2, 3 / 2), (3 / 2, 3 / 2)]
  · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
      (by norm_num) (by simp; linarith)
  · intro i j hij
    fin_cases i <;> fin_cases j <;> simp at hij ⊢ <;> norm_num [abs_of_pos, abs_of_neg]

/-- The tilted piece of `R₄`'s boundary: some unit `(C, S)`, `C, S > 0`, with `L ≥ L(t, H)`. -/
def Fried4 (L H : ℝ) : Prop :=
  ∃ C S : ℝ, 0 < C ∧ 0 < S ∧ C ^ 2 + S ^ 2 = 1 ∧
    2 * C * (S - C) + 2 * (1 + C + S - H) + C ^ 2 * H ≤ S * C * L

/-- **`R₄` exactly.**  Four unit squares (any angles) fit in `[0,w] × [0,h]` iff both sides are at least
`1` and: both are at least `2`, or one is at least `4`, or the short side `s < 2` and the long side `ℓ`
satisfy `ℓ ≥ L(t, s)` for some `t ∈ (0°, 90°)` (`Fried4 ℓ s`; Friedman's piece of `S₃`, mostly Morandi). -/
theorem rect4_iff {w h : ℝ} : RectPacks 4 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧
    ((2 ≤ w ∧ 2 ≤ h) ∨ 4 ≤ w ∨ 4 ≤ h ∨ (h < 2 ∧ Fried4 w h) ∨ (w < 2 ∧ Fried4 h w)) := by
  constructor
  · intro hp
    obtain ⟨hw, hh⟩ := one_le_sides (hp.choose_spec.choose_spec.1 0)
    refine ⟨hw, hh, ?_⟩
    rcases lt_or_ge h 2 with hh2 | hh2
    · rcases rect4_lower hp hh2 with h4 | h4
      · exact Or.inr (Or.inl h4)
      · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨hh2, h4⟩)))
    rcases lt_or_ge w 2 with hw2 | hw2
    · rcases rect4_lower hp.swap hw2 with h4 | h4
      · exact Or.inr (Or.inr (Or.inl h4))
      · exact Or.inr (Or.inr (Or.inr (Or.inr ⟨hw2, h4⟩)))
    · exact Or.inl ⟨hw2, hh2⟩
  · rintro ⟨hw, hh, h2 | h4 | h4 | ⟨hh2, C, S, hC, hS, hCS, hF⟩ | ⟨hw2, C, S, hC, hS, hCS, hF⟩⟩
    · exact rect4_block h2.1 h2.2
    · exact rect4_row h4 hh
    · exact (rect4_row h4 hw).swap
    · rcases le_or_gt 4 w with h4 | h4
      · exact rect4_row h4 hh
      · exact rect4_friedman hC hS hCS hh2 hF h4
    · rcases le_or_gt 4 h with h4 | h4
      · exact (rect4_row h4 hw).swap
      · exact (rect4_friedman hC hS hCS hw2 hF h4).swap

end SquarePacking
