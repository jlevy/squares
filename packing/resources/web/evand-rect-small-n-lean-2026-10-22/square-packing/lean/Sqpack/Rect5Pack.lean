import Sqpack.Rect4

/-!
# Five unit squares in a rectangle: the constructions

The packings on the boundary of `R₅` (Friedman's Math Magic, June 2010, pieces 4.1–4.5 of `S₄`; closed
forms also in wand125 `problems/rectangles`).  Every tilted square is at `45°`, so each proof is linear
arithmetic in `√2`: every square gives four strict linear bounds on its interior points (`up_int`,
`dia_int`), and each pair of squares is split by an axis-parallel or a diagonal line, which `linarith`
finds from those bounds.

* `rect5_row`: five in a row, `5 ≤ w`.
* `rect5_grid`: a `2 × 3` grid minus one, `2 ≤ w`, `3 ≤ h`.
* `rect5_zigzag` (piece 4.2): uprights in both bottom corners, `45°` squares on the ceiling against their
  inner corners, a `45°` square on the floor between them, edge to edge: `L + 4H ≥ 4 + 6√2`, `√2 ≤ H ≤ 2`.
* `rect5_stretch` (piece 4.5, containing `s(5) = 2 + 1/√2`): four corner uprights and a central `45°` square
  touching their inner corners: `w + h ≥ 4 + √2`, `w, h ≥ 2`.
* `rect5_upper`: all of them, both orientations.
-/

namespace SquarePacking

/-- Interior of an upright unit square, as four linear bounds. -/
lemma up_int {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sqInt c θ 1) (hθ : θ = 0) :
    c.1 - 1 / 2 < p.1 ∧ p.1 < c.1 + 1 / 2 ∧ c.2 - 1 / 2 < p.2 ∧ p.2 < c.2 + 1 / 2 := by
  subst hθ
  rw [sqInt_zero, abs_lt, abs_lt] at hp
  obtain ⟨⟨a, b⟩, ⟨d, e⟩⟩ := hp
  exact ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- Interior of a `45°` unit square (a diamond of half-diagonal `√2/2`), as four linear bounds. -/
lemma dia_int {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sqInt c θ 1) (hθ : θ = Real.pi / 4) :
    c.1 + c.2 - Real.sqrt 2 / 2 < p.1 + p.2 ∧ p.1 + p.2 < c.1 + c.2 + Real.sqrt 2 / 2 ∧
      c.2 - c.1 - Real.sqrt 2 / 2 < p.2 - p.1 ∧ p.2 - p.1 < c.2 - c.1 + Real.sqrt 2 / 2 := by
  subst hθ
  have r2 : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  have r0 : 0 < Real.sqrt 2 := by positivity
  obtain ⟨h1, h2⟩ := hp
  simp only [coord, Real.cos_pi_div_four, Real.sin_pi_div_four, abs_lt] at h1 h2
  obtain ⟨a, b⟩ := h1; obtain ⟨d, e⟩ := h2
  -- multiply each bound by `√2` (`√2 · √2/2 = 1`)
  have m : ∀ z : ℝ, Real.sqrt 2 * (z * (Real.sqrt 2 / 2)) = z := fun z => by
    linear_combination (z / 2) * r2
  have ka := mul_lt_mul_of_pos_left a r0; have kb := mul_lt_mul_of_pos_left b r0
  have kd := mul_lt_mul_of_pos_left d r0; have ke := mul_lt_mul_of_pos_left e r0
  have e1 : Real.sqrt 2 * ((p.1 - c.1) * (Real.sqrt 2 / 2) + (p.2 - c.2) * (Real.sqrt 2 / 2)) =
      (p.1 + p.2) - (c.1 + c.2) := by rw [← add_mul, m]; ring
  have e2 : Real.sqrt 2 * (-(p.1 - c.1) * (Real.sqrt 2 / 2) + (p.2 - c.2) * (Real.sqrt 2 / 2)) =
      (p.2 - p.1) - (c.2 - c.1) := by rw [← add_mul, m]; ring
  rw [e1] at ka kb; rw [e2] at kd ke
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- The containment condition for a `45°` square: its centre keeps distance `√2/2` from every wall. -/
lemma dia_subset {c : ℝ × ℝ} {w h : ℝ} (h1 : Real.sqrt 2 / 2 ≤ c.1) (h2 : c.1 ≤ w - Real.sqrt 2 / 2)
    (h3 : Real.sqrt 2 / 2 ≤ c.2) (h4 : c.2 ≤ h - Real.sqrt 2 / 2) : sq c (Real.pi / 4) 1 ⊆ rbox w h := by
  have k : (|Real.cos (Real.pi / 4)| + |Real.sin (Real.pi / 4)|) / 2 = Real.sqrt 2 / 2 := by
    rw [Real.cos_pi_div_four, Real.sin_pi_div_four, abs_of_pos (by positivity)]; ring
  exact sq_subset_rbox (by rw [k]; exact h1) (by rw [k]; exact h2) (by rw [k]; exact h3) (by rw [k]; exact h4)

/-- Either kind of square, as linear bounds. -/
lemma int_lin {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sqInt c θ 1) (hθ : θ = 0 ∨ θ = Real.pi / 4) :
    (θ = 0 ∧ c.1 - 1 / 2 < p.1 ∧ p.1 < c.1 + 1 / 2 ∧ c.2 - 1 / 2 < p.2 ∧ p.2 < c.2 + 1 / 2) ∨
    (θ = Real.pi / 4 ∧ c.1 + c.2 - Real.sqrt 2 / 2 < p.1 + p.2 ∧ p.1 + p.2 < c.1 + c.2 + Real.sqrt 2 / 2 ∧
      c.2 - c.1 - Real.sqrt 2 / 2 < p.2 - p.1 ∧ p.2 - p.1 < c.2 - c.1 + Real.sqrt 2 / 2) := by
  rcases hθ with h | h
  · exact Or.inl ⟨h, up_int hp h⟩
  · exact Or.inr ⟨h, dia_int hp h⟩

/-- Disjointness of every pair, for squares at angles `0` and `π/4`: the four bounds of each square,
then `linarith` with the side conditions in context (wrong-angle branches die on `π > 0`). -/
macro "pairs5" : tactic => `(tactic| (
  intro i j hij
  rw [Set.disjoint_left]
  intro p h1 h2
  fin_cases i <;> fin_cases j <;> simp at hij h1 h2 <;>
  (obtain ⟨e1, a1, a2, a3, a4⟩ | ⟨e1, a1, a2, a3, a4⟩ := int_lin h1 (by norm_num) <;>
   obtain ⟨e2, b1, b2, b3, b4⟩ | ⟨e2, b1, b2, b3, b4⟩ := int_lin h2 (by norm_num) <;>
   (try dsimp only at a1 a2 a3 a4 b1 b2 b3 b4) <;> linarith [Real.pi_pos])))

/-- Five in a row. -/
theorem rect5_row {w h : ℝ} (hw : 5 ≤ w) (hh : 1 ≤ h) : RectPacks 5 w h := by
  refine ⟨![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (5 / 2, 1 / 2), (7 / 2, 1 / 2), (9 / 2, 1 / 2)],
    ![0, 0, 0, 0, 0], ?_, ?_⟩
  · intro i
    fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
  · pairs5

/-- Five cells of a `2 × 3` grid. -/
theorem rect5_grid {w h : ℝ} (hw : 2 ≤ w) (hh : 3 ≤ h) : RectPacks 5 w h := by
  refine ⟨![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (1 / 2, 3 / 2), (3 / 2, 3 / 2), (1 / 2, 5 / 2)],
    ![0, 0, 0, 0, 0], ?_, ?_⟩
  · intro i
    fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
  · pairs5

set_option maxHeartbeats 1000000 in
/-- **The zigzag** (piece 4.2 of `S₄`): five unit squares fit in `[0,L] × [0,H]` when `√2 ≤ H ≤ 2` and
`L + 4H ≥ 4 + 6√2`.  Uprights in both bottom corners; `45°` squares on the ceiling with an edge through the
uprights' inner top corners; a `45°` square on the floor between them, edge to edge with both. -/
theorem rect5_zigzag {L H : ℝ} (hH1 : Real.sqrt 2 ≤ H) (hH2 : H ≤ 2)
    (hL : 4 + 6 * Real.sqrt 2 ≤ L + 4 * H) : RectPacks 5 L H := by
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2l : Real.sqrt 2 < 3 / 2 := by nlinarith [Real.sqrt_nonneg 2]
  have r2g : 7 / 5 < Real.sqrt 2 := by nlinarith [Real.sqrt_nonneg 2]
  refine RectPacks.mono (w := 4 + 6 * Real.sqrt 2 - 4 * H) ?_ (by linarith)
  refine ⟨![(1 / 2, 1 / 2), (2 - H + Real.sqrt 2, H - Real.sqrt 2 / 2), ((4 + 6 * Real.sqrt 2 - 4 * H) / 2,
    Real.sqrt 2 / 2), (4 + 6 * Real.sqrt 2 - 4 * H - (2 - H + Real.sqrt 2), H - Real.sqrt 2 / 2),
    (4 + 6 * Real.sqrt 2 - 4 * H - 1 / 2, 1 / 2)],
    ![0, Real.pi / 4, Real.pi / 4, Real.pi / 4, 0], ?_, ?_⟩
  · intro i
    fin_cases i
    · exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
    · exact dia_subset (by simp; linarith) (by simp; linarith) (by simp; linarith) (by simp)
    · exact dia_subset (by simp; linarith) (by simp; linarith) (by simp) (by simp; linarith)
    · exact dia_subset (by simp; linarith) (by simp; linarith) (by simp; linarith) (by simp)
    · exact sq_zero_subset (by simp; linarith) (by simp) (by norm_num) (by simp; linarith)
  · pairs5

/-- **The stretched `s(5)` packing** (piece 4.5 of `S₄`): four corner uprights and a central `45°` square
touching their inner corners fit in `[0,w] × [0,h]` when `w, h ≥ 2` and `w + h ≥ 4 + √2`. -/
theorem rect5_stretch {w h : ℝ} (hw : 2 ≤ w) (hh : 2 ≤ h) (hs : 4 + Real.sqrt 2 ≤ w + h) :
    RectPacks 5 w h := by
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2l : Real.sqrt 2 < 3 / 2 := by nlinarith [Real.sqrt_nonneg 2]
  have r2g : 7 / 5 < Real.sqrt 2 := by nlinarith [Real.sqrt_nonneg 2]
  refine ⟨![(1 / 2, 1 / 2), (w - 1 / 2, 1 / 2), (1 / 2, h - 1 / 2), (w - 1 / 2, h - 1 / 2), (w / 2, h / 2)],
    ![0, 0, 0, 0, Real.pi / 4], ?_, ?_⟩
  · intro i
    fin_cases i
    · exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
    · exact sq_zero_subset (by simp; linarith) (by simp) (by norm_num) (by simp; linarith)
    · exact sq_zero_subset (by norm_num) (by simp; linarith) (by simp; linarith) (by simp)
    · exact sq_zero_subset (by simp; linarith) (by simp) (by simp; linarith) (by simp)
    · exact dia_subset (by simp; linarith) (by simp; linarith) (by simp; linarith) (by simp; linarith)
  · pairs5

/-- **The upper half of `R₅`**: five unit squares fit in `[0,w] × [0,h]` in each of Friedman's cases. -/
theorem rect5_upper {w h : ℝ} (hw : 1 ≤ w) (hh : 1 ≤ h)
    (hc : 5 ≤ w ∨ 5 ≤ h ∨ (2 ≤ w ∧ 3 ≤ h) ∨ (3 ≤ w ∧ 2 ≤ h) ∨
      (2 ≤ w ∧ 2 ≤ h ∧ 4 + Real.sqrt 2 ≤ w + h) ∨
      (Real.sqrt 2 ≤ h ∧ h ≤ 2 ∧ 4 + 6 * Real.sqrt 2 ≤ w + 4 * h) ∨
      (Real.sqrt 2 ≤ w ∧ w ≤ 2 ∧ 4 + 6 * Real.sqrt 2 ≤ h + 4 * w)) : RectPacks 5 w h := by
  rcases hc with h5 | h5 | ⟨a, b⟩ | ⟨a, b⟩ | ⟨a, b, c⟩ | ⟨a, b, c⟩ | ⟨a, b, c⟩
  · exact rect5_row h5 hh
  · exact (rect5_row h5 hw).swap
  · exact rect5_grid a b
  · exact (rect5_grid b a).swap
  · exact rect5_stretch a b c
  · exact rect5_zigzag a b c
  · exact (rect5_zigzag a b c).swap

end SquarePacking
