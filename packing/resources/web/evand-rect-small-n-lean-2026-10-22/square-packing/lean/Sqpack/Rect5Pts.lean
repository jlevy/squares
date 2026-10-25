import Sqpack.RectChain
import Sqpack.Basic

/-!
# Five unit squares in a rectangle with both sides `≥ 2`: four unavoidable points

`rect5_pts_lower`: if `2 ≤ a, b < 2√2` and `a + b < 4 + √2`, five unit squares do not fit in `[0,a] × [0,b]`.
This is Friedman's piece 4.5 of `S₄` (`a + b = 4 + √2`) for `4 - √2 ≤ a ≤ 2 + 1/√2`; at `a = b` it is
`s(5) ≥ 2 + 1/√2` (Göbel 1979).

Proof: every closed unit square in the rectangle contains one of the four points `(1, 1)`, `(a - 1, 1)`,
`(1, b - 1)`, `(a - 1, b - 1)` (`rect5_cover`); a slightly scaled-up packing then puts five disjoint
squares on four points (`packing_le_weight`).  The cover splits the square's centre into 9 cells:
* corner cells: `In_corner` (the point is within `1 - k` of the centre in both coordinates);
* side cells: `In_side` (DS7 Lemma 2: a gap `≤ 2√2 - 2` between two points at distance 1 from a wall);
* the centre cell: `In_rect` (a centre in an `X × Y` cell with `X, Y ≤ 1`, `X + Y ≤ √2` forces a corner).
All three are real inequalities in a frame `(c, s)` of the square (`c, s ≥ 0`, `c² + s² = 1`); reflections of the
plane only swap `c` and `s` (`In_swap`, `In_negx`, `In_neg`), so each core lemma assumes `s ≤ c`.
Paper proofs and numerics: `search/rectfront/r5pts/R5PTS.md`.
-/

namespace SquarePacking

/-- The point at offset `(dx, dy)` from the centre lies in the closed unit square with frame `(c, s)`. -/
def In (dx dy c s : ℝ) : Prop := |dx * c + dy * s| ≤ 1 / 2 ∧ |-dx * s + dy * c| ≤ 1 / 2

lemma In_negx {dx dy c s : ℝ} : In (-dx) dy s c ↔ In dx dy c s := by
  unfold In
  rw [show -dx * s + dy * c = -dx * s + dy * c by ring, show - -dx * c + dy * s = dx * c + dy * s by ring]
  exact and_comm

lemma In_swap {dx dy c s : ℝ} : In dy dx s c ↔ In dx dy c s := by
  unfold In
  rw [show dy * s + dx * c = dx * c + dy * s by ring,
    show -dy * c + dx * s = -(-dx * s + dy * c) by ring, abs_neg]

lemma In_neg {dx dy c s : ℝ} : In (-dx) (-dy) c s ↔ In dx dy c s := by
  unfold In
  rw [show -dx * c + -dy * s = -(dx * c + dy * s) by ring,
    show - -dx * s + -dy * c = -(-dx * s + dy * c) by ring, abs_neg, abs_neg]

/-- Basic facts about a frame: `1 ≤ c + s ≤ √2`. -/
lemma frame_facts {c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1) :
    1 ≤ c + s ∧ c + s ≤ Real.sqrt 2 ∧ c ≤ 1 ∧ s ≤ 1 := by
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  refine ⟨by nlinarith [mul_nonneg hc hs], by nlinarith [sq_nonneg (c - s)], by nlinarith, by nlinarith⟩

/-! ## Corner cells -/

/-- **Corner lemma.**  A point within `1 - k` of the centre in both coordinates (`k = (c + s)/2`) is in the
square. -/
lemma In_corner {dx dy c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1)
    (hx : |dx| ≤ 1 - (c + s) / 2) (hy : |dy| ≤ 1 - (c + s) / 2) : In dx dy c s := by
  obtain ⟨p1, p2, -, -⟩ := frame_facts hc hs hcs
  have key : (1 - (c + s) / 2) * (c + s) ≤ 1 / 2 := by nlinarith [sq_nonneg (c + s - 1)]
  have bx := mul_le_mul_of_nonneg_right hx hc; have by' := mul_le_mul_of_nonneg_right hy hs
  have bx' := mul_le_mul_of_nonneg_right hx hs; have by'' := mul_le_mul_of_nonneg_right hy hc
  constructor
  · calc |dx * c + dy * s| ≤ |dx * c| + |dy * s| := abs_add_le _ _
      _ = |dx| * c + |dy| * s := by rw [abs_mul, abs_mul, abs_of_nonneg hc, abs_of_nonneg hs]
      _ ≤ 1 / 2 := by linarith
  · calc |-dx * s + dy * c| ≤ |-dx * s| + |dy * c| := abs_add_le _ _
      _ = |dx| * s + |dy| * c := by rw [abs_mul, abs_mul, abs_neg, abs_of_nonneg hc, abs_of_nonneg hs]
      _ ≤ 1 / 2 := by linarith

/-! ## Side cells -/

/-- Not in the square: one of the four frame coordinates exceeds `1/2`. -/
lemma not_In {dx dy c s : ℝ} (h : ¬ In dx dy c s) :
    1 / 2 < dx * c + dy * s ∨ dx * c + dy * s < -(1 / 2) ∨ 1 / 2 < -dx * s + dy * c ∨
      -dx * s + dy * c < -(1 / 2) := by
  unfold In at h
  rw [not_and_or, not_le, not_le, lt_abs, lt_abs] at h
  rcases h with (h | h) | (h | h)
  · exact Or.inl h
  · exact Or.inr (Or.inl (by linarith))
  · exact Or.inr (Or.inr (Or.inl h))
  · exact Or.inr (Or.inr (Or.inr (by linarith)))

/-- Side lemma with `s ≤ c`. -/
lemma In_side_le {A A' B c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1) (hsc : s ≤ c)
    (hA : 0 ≤ A) (hA' : 0 ≤ A') (hB : 0 ≤ B) (hx : A + A' ≤ 2 * Real.sqrt 2 - 2)
    (hBk : B ≤ 1 - (c + s) / 2) : In A B c s ∨ In (-A') B c s := by
  obtain ⟨p1, p2, c1, s1⟩ := frame_facts hc hs hcs
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  by_contra hno
  rw [not_or] at hno
  obtain ⟨hQ, hP⟩ := hno
  have f1 := mul_nonneg hA hc; have f2 := mul_nonneg hA hs; have f3 := mul_nonneg hA' hc
  have f4 := mul_nonneg hA' hs; have f5 := mul_nonneg hB hc; have f6 := mul_nonneg hB hs
  have g1 : A * s ≤ A * c := mul_le_mul_of_nonneg_left hsc hA
  have r0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hx1 : A + A' < 1 := by nlinarith
  have g2 : B * c ≤ 1 / 2 := by nlinarith [mul_le_mul_of_nonneg_left c1 hB]
  have g3 : B * s ≤ 1 / 2 := by nlinarith [mul_le_mul_of_nonneg_left s1 hB]
  have g4 : A * c + A' * c < 1 := by nlinarith [mul_le_mul_of_nonneg_left c1 (by linarith : 0 ≤ A + A')]
  -- `Q` is witnessed by `u`
  have hu : 1 / 2 < A * c + B * s := by
    rcases not_In hQ with h | h | h | h
    · exact h
    · linarith
    · linarith
    · linarith
  rcases not_In hP with h | h | h | h
  · linarith
  · linarith
  · -- the 45° case: `s u_Q + c v_P = c s (A + A') + B > (c + s)/2`
    have hc0 : 0 < c := by nlinarith
    have k1 := mul_le_mul_of_nonneg_left hu.le hs
    have k2 := mul_lt_mul_of_pos_left h hc0
    have e1 : B * c ^ 2 + B * s ^ 2 = B := by linear_combination B * hcs
    have e2 : A * c ^ 2 + A * s ^ 2 = A := by linear_combination A * hcs
    have e3 : A' * c ^ 2 + A' * s ^ 2 = A' := by linear_combination A' * hcs
    have k3 := mul_le_mul hx (by linarith : c + s + 1 ≤ Real.sqrt 2 + 1) (by linarith) (by nlinarith)
    have k4 : 0 ≤ (c + s - 1) * (2 - (A + A') * (c + s + 1)) := mul_nonneg (by linarith) (by nlinarith)
    nlinarith
  · linarith

/-- **Side lemma** (DS7 Lemma 2, gap `x₀ = A + A' ≤ 2√2 - 2`, points at distance `1` from the wall): with
`B ≤ 1 - k` (the centre at least `k` from the wall), the square contains the point at offset `(A, B)` or the
point at offset `(-A', B)`. -/
lemma In_side {A A' B c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1)
    (hA : 0 ≤ A) (hA' : 0 ≤ A') (hB : 0 ≤ B) (hx : A + A' ≤ 2 * Real.sqrt 2 - 2)
    (hBk : B ≤ 1 - (c + s) / 2) : In A B c s ∨ In (-A') B c s := by
  rcases le_total s c with h | h
  · exact In_side_le hc hs hcs h hA hA' hB hx hBk
  · have := In_side_le hs hc (by linarith) h hA' hA hB (by linarith) (by linarith)
    have n : ∀ x y : ℝ, In (-x) y s c → In x y c s := fun x y h => In_negx.1 h
    have n' : ∀ x y : ℝ, In x y s c → In (-x) y c s := fun x y h => In_negx.1 (by rwa [neg_neg])
    rcases this with h1 | h1
    · exact Or.inr (n' _ _ h1)
    · exact Or.inl (n _ _ h1)

/-! ## The centre cell -/

lemma In_rect_le {A A' B B' c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1) (hsc : s ≤ c)
    (hA : 0 ≤ A) (hA' : 0 ≤ A') (hB : 0 ≤ B) (hB' : 0 ≤ B') (hX : A + A' ≤ 1) (hY : B + B' ≤ 1)
    (hXY : A + A' + (B + B') ≤ Real.sqrt 2) :
    In A B c s ∨ In (-A') B c s ∨ In (-A') (-B') c s ∨ In A (-B') c s := by
  obtain ⟨p1, p2, c1, s1⟩ := frame_facts hc hs hcs
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  by_contra hno
  simp only [not_or] at hno
  obtain ⟨h1, h2, h3, h4⟩ := hno
  have f1 := mul_nonneg hA hc; have f2 := mul_nonneg hA hs; have f3 := mul_nonneg hA' hc
  have f4 := mul_nonneg hA' hs; have f5 := mul_nonneg hB hc; have f6 := mul_nonneg hB hs
  have f7 := mul_nonneg hB' hc; have f8 := mul_nonneg hB' hs
  have g1 : A * s ≤ A * c := mul_le_mul_of_nonneg_left hsc hA
  have g2 : A' * s ≤ A' * c := mul_le_mul_of_nonneg_left hsc hA'
  have g3 : B * s ≤ B * c := mul_le_mul_of_nonneg_left hsc hB
  have g4 : B' * s ≤ B' * c := mul_le_mul_of_nonneg_left hsc hB'
  have gX := mul_le_mul hX c1 hc (by norm_num)
  have gY := mul_le_mul hY c1 hc (by norm_num)
  have gXY := mul_le_mul hXY p2 (by linarith) (Real.sqrt_nonneg 2)
  -- two possible witnesses per corner
  have w1 : 1 / 2 < A * c + B * s ∨ 1 / 2 < -A * s + B * c := by
    rcases not_In h1 with h | h | h | h
    · exact Or.inl h
    · linarith
    · exact Or.inr h
    · left; linarith
  have w2 : 1 / 2 < -(-A') * s + B * c ∨ (-A') * c + B * s < -(1 / 2) := by
    rcases not_In h2 with h | h | h | h
    · left; linarith
    · exact Or.inr h
    · exact Or.inl h
    · linarith
  have w3 : (-A') * c + (-B') * s < -(1 / 2) ∨ -(-A') * s + (-B') * c < -(1 / 2) := by
    rcases not_In h3 with h | h | h | h
    · linarith
    · exact Or.inl h
    · left; linarith
    · exact Or.inr h
  have w4 : 1 / 2 < A * c + (-B') * s ∨ -A * s + (-B') * c < -(1 / 2) := by
    rcases not_In h4 with h | h | h | h
    · exact Or.inl h
    · right; linarith
    · linarith
    · exact Or.inr h
  rcases w1 with a | a <;> rcases w2 with b | b <;> rcases w3 with d | d <;> rcases w4 with e | e <;>
    linarith

/-- **Centre-rectangle lemma.**  A centre in a cell `X × Y` (`X = A + A'`, `Y = B + B'`) with `X, Y ≤ 1` and
`X + Y ≤ √2`: the square contains one of the cell's corners, at offsets `(A, B)`, `(-A', B)`, `(-A', -B')`,
`(A, -B')`. -/
lemma In_rect {A A' B B' c s : ℝ} (hc : 0 ≤ c) (hs : 0 ≤ s) (hcs : c ^ 2 + s ^ 2 = 1)
    (hA : 0 ≤ A) (hA' : 0 ≤ A') (hB : 0 ≤ B) (hB' : 0 ≤ B') (hX : A + A' ≤ 1) (hY : B + B' ≤ 1)
    (hXY : A + A' + (B + B') ≤ Real.sqrt 2) :
    In A B c s ∨ In (-A') B c s ∨ In (-A') (-B') c s ∨ In A (-B') c s := by
  rcases le_total s c with h | h
  · exact In_rect_le hc hs hcs h hA hA' hB hB' hX hY hXY
  · have := In_rect_le hs hc (by linarith) h hA' hA hB hB' (by linarith) hY (by linarith)
    have n : ∀ x y : ℝ, In (-x) y s c → In x y c s := fun x y h => In_negx.1 h
    have n' : ∀ x y : ℝ, In x y s c → In (-x) y c s := fun x y h => In_negx.1 (by rwa [neg_neg])
    rcases this with h1 | h1 | h1 | h1
    · exact Or.inr (Or.inl (n' _ _ h1))
    · exact Or.inl (n _ _ h1)
    · exact Or.inr (Or.inr (Or.inr (n _ _ h1)))
    · exact Or.inr (Or.inr (Or.inl (n' _ _ h1)))

lemma In_congr {dx dy dx' dy' c s : ℝ} (h : In dx dy c s) (ex : dx = dx') (ey : dy = dy') :
    In dx' dy' c s := by subst ex; subst ey; exact h

/-! ## The cover -/

/-- From frame coordinates back to the square. -/
lemma mem_of_In {X : Set (ℝ × ℝ)} {m : ℝ × ℝ} {P Q x y : ℝ} (hf : FrameIn X m P Q) (hPQ : P ^ 2 + Q ^ 2 = 1)
    (h : In (x - m.1) (y - m.2) P Q) : (x, y) ∈ X := by
  have := hf _ _ h.1 h.2
  convert this using 1
  ext
  · simp only; linear_combination (-(x - m.1)) * hPQ
  · simp only; linear_combination (-(y - m.2)) * hPQ

/-- **The four unavoidable points.**  If `2 ≤ a, b ≤ 2√2` and `a + b ≤ 4 + √2`, every closed unit square in
`[0,a] × [0,b]` contains `(1, 1)`, `(a - 1, 1)`, `(1, b - 1)` or `(a - 1, b - 1)`. -/
theorem rect5_cover {a b : ℝ} (ha : 2 ≤ a) (ha' : a ≤ 2 * Real.sqrt 2)
    (hb' : b ≤ 2 * Real.sqrt 2) (hab : a + b ≤ 4 + Real.sqrt 2) {m : ℝ × ℝ} {θ : ℝ}
    (hin : sq m θ 1 ⊆ rbox a b) :
    (1, 1) ∈ sq m θ 1 ∨ (a - 1, 1) ∈ sq m θ 1 ∨ (1, b - 1) ∈ sq m θ 1 ∨ (a - 1, b - 1) ∈ sq m θ 1 := by
  obtain ⟨P, Q, hP, hQ, hPQ, h1, h2, h3, h4, hf⟩ := framed hin
  have hQP : Q ^ 2 + P ^ 2 = 1 := by linarith
  have M : ∀ x y : ℝ, In (x - m.1) (y - m.2) P Q → (x, y) ∈ sq m θ 1 := fun x y h => mem_of_In hf hPQ h
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2l : Real.sqrt 2 < 3 / 2 := by nlinarith [Real.sqrt_nonneg 2]
  have ab : ∀ {z : ℝ}, -(1 - (P + Q) / 2) ≤ z → z ≤ 1 - (P + Q) / 2 → |z| ≤ 1 - (P + Q) / 2 :=
    fun h h' => abs_le.2 ⟨h, h'⟩
  rcases le_total m.1 1 with x1 | x1 <;> rcases le_total m.2 1 with y1 | y1
  · exact Or.inl (M _ _ (In_corner hP hQ hPQ (ab (by linarith) (by linarith)) (ab (by linarith) (by linarith))))
  · rcases le_total m.2 (b - 1) with y2 | y2
    · -- left wall
      rcases In_side hQ hP hQP (A := b - 1 - m.2) (A' := m.2 - 1) (B := 1 - m.1) (by linarith) (by linarith)
        (by linarith) (by linarith) (by linarith) with h | h
      · exact Or.inr (Or.inr (Or.inl (M _ _ (In_swap.1 h))))
      · exact Or.inl (M _ _ (In_congr (In_swap.1 h) rfl (by ring)))
    · exact Or.inr (Or.inr (Or.inl (M _ _
        (In_corner hP hQ hPQ (ab (by linarith) (by linarith)) (ab (by linarith) (by linarith))))))
  · rcases le_total m.1 (a - 1) with x2 | x2
    · -- bottom wall
      rcases In_side hP hQ hPQ (A := a - 1 - m.1) (A' := m.1 - 1) (B := 1 - m.2) (by linarith) (by linarith)
        (by linarith) (by linarith) (by linarith) with h | h
      · exact Or.inr (Or.inl (M _ _ h))
      · exact Or.inl (M _ _ (In_congr h (by ring) rfl))
    · exact Or.inr (Or.inl (M _ _
        (In_corner hP hQ hPQ (ab (by linarith) (by linarith)) (ab (by linarith) (by linarith)))))
  · rcases le_total m.1 (a - 1) with x2 | x2 <;> rcases le_total m.2 (b - 1) with y2 | y2
    · -- the centre cell
      rcases In_rect hP hQ hPQ (A := a - 1 - m.1) (A' := m.1 - 1) (B := b - 1 - m.2) (B' := m.2 - 1)
        (by linarith) (by linarith) (by linarith) (by linarith) (by linarith) (by linarith) (by linarith)
        with h | h | h | h
      · exact Or.inr (Or.inr (Or.inr (M _ _ h)))
      · exact Or.inr (Or.inr (Or.inl (M _ _ (In_congr h (by ring) rfl))))
      · exact Or.inl (M _ _ (In_congr h (by ring) (by ring)))
      · exact Or.inr (Or.inl (M _ _ (In_congr h rfl (by ring))))
    · -- top wall
      rcases In_side hP hQ hPQ (A := m.1 - 1) (A' := a - 1 - m.1) (B := m.2 - (b - 1)) (by linarith)
        (by linarith) (by linarith) (by linarith) (by linarith) with h | h
      · exact Or.inr (Or.inr (Or.inl (M _ _ (In_neg.1 (In_congr h (by ring) (by ring))))))
      · exact Or.inr (Or.inr (Or.inr (M _ _ (In_neg.1 (In_congr h rfl (by ring))))))
    · -- right wall
      rcases In_side hQ hP hQP (A := m.2 - 1) (A' := b - 1 - m.2) (B := m.1 - (a - 1)) (by linarith)
        (by linarith) (by linarith) (by linarith) (by linarith) with h | h
      · exact Or.inr (Or.inl (M _ _ (In_neg.1 (In_congr (In_swap.1 h) (by ring) (by ring)))))
      · exact Or.inr (Or.inr (Or.inr (M _ _ (In_neg.1 (In_congr (In_swap.1 h) (by ring) rfl)))))
    · exact Or.inr (Or.inr (Or.inr (M _ _
        (In_corner hP hQ hPQ (ab (by linarith) (by linarith)) (ab (by linarith) (by linarith))))))

/-! ## Scaling and the count -/

lemma abs_scale {l x : ℝ} (hl : 0 < l) : |l * x| = l * |x| := by rw [abs_mul, abs_of_pos hl]

lemma coord_scale (c p : ℝ × ℝ) (θ l : ℝ) (hl : 0 < l) :
    coord (l * c.1, l * c.2) θ p = (l * (coord c θ (p.1 / l, p.2 / l)).1, l * (coord c θ (p.1 / l, p.2 / l)).2) := by
  simp only [coord]
  ext <;> simp only <;> field_simp

lemma mem_sq_scale {c p : ℝ × ℝ} {θ l : ℝ} (hl : 0 < l) :
    p ∈ sq (l * c.1, l * c.2) θ l ↔ (p.1 / l, p.2 / l) ∈ sq c θ 1 := by
  simp only [sq, Set.mem_ofPred_eq, coord_scale c p θ l hl, abs_scale hl]
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> nlinarith

lemma mem_sqInt_scale {c p : ℝ × ℝ} {θ l : ℝ} (hl : 0 < l) :
    p ∈ sqInt (l * c.1, l * c.2) θ l ↔ (p.1 / l, p.2 / l) ∈ sqInt c θ 1 := by
  simp only [sqInt, Set.mem_ofPred_eq, coord_scale c p θ l hl, abs_scale hl]
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> nlinarith

open scoped Classical in
/-- **Five unit squares need `a + b ≥ 4 + √2`** when `2 ≤ a, b < 2√2` (Friedman's piece 4.5 of `S₄` for
`4 - √2 ≤ a ≤ 2 + 1/√2`; at `a = b`, `s(5) ≥ 2 + 1/√2`, Göbel 1979). -/
theorem rect5_pts_lower {a b : ℝ} (ha : 2 ≤ a) (hb : 2 ≤ b) (ha' : a < 2 * Real.sqrt 2)
    (hb' : b < 2 * Real.sqrt 2) (hab : a + b < 4 + Real.sqrt 2) : ¬ RectPacks 5 a b := by
  rintro ⟨ctr, ang, hin, hd⟩
  have r0 : 0 < Real.sqrt 2 := by positivity
  -- the scale
  set l := min (2 * Real.sqrt 2 / a) (min (2 * Real.sqrt 2 / b) ((4 + Real.sqrt 2) / (a + b))) with hl
  have l1 : 1 < l := lt_min ((one_lt_div (by linarith)).2 ha') (lt_min ((one_lt_div (by linarith)).2 hb')
    ((one_lt_div (by linarith)).2 hab))
  have l0 : 0 < l := by linarith
  have la : l * a ≤ 2 * Real.sqrt 2 := (le_div_iff₀ (by linarith)).1 (min_le_left _ _)
  have lb : l * b ≤ 2 * Real.sqrt 2 :=
    (le_div_iff₀ (by linarith)).1 ((min_le_right _ _).trans (min_le_left _ _))
  have lab : l * (a + b) ≤ 4 + Real.sqrt 2 :=
    (le_div_iff₀ (by linarith)).1 ((min_le_right _ _).trans (min_le_right _ _))
  have la2 : 2 ≤ l * a := by nlinarith
  have lb2 : 2 ≤ l * b := by nlinarith
  -- the points
  let A : Finset (ℝ × ℝ) := {(1, 1), (l * a - 1, 1), (1, l * b - 1), (l * a - 1, l * b - 1)}
  have key := packing_le_weight A (fun _ => 1) (fun _ _ => zero_le_one) (rbox (l * a) (l * b))
    (fun c θ hc => by
      have hz : ∃ z ∈ A, z ∈ sq c θ 1 := by
        rcases rect5_cover la2 la lb (by linarith) hc with h | h | h | h
        · exact ⟨_, by simp [A], h⟩
        · exact ⟨_, by simp [A], h⟩
        · exact ⟨_, by simp [A], h⟩
        · exact ⟨_, by simp [A], h⟩
      obtain ⟨z, hzA, hz⟩ := hz
      exact Finset.single_le_sum (f := fun _ => (1 : ℝ)) (fun _ _ => zero_le_one)
        (Finset.mem_filter.2 ⟨hzA, hz⟩))
    5 l l1 (fun i => (l * (ctr i).1, l * (ctr i).2)) ang
    (fun i p hp => by
      have := hin i ((mem_sq_scale l0).1 hp)
      simp only [rbox, Set.mem_ofPred_eq] at this ⊢
      obtain ⟨e1, e2, e3, e4⟩ := this
      refine ⟨?_, ?_, ?_, ?_⟩
      · have := mul_nonneg l0.le e1; field_simp at this; linarith
      · have := mul_le_mul_of_nonneg_left e2 l0.le; field_simp at this; linarith
      · have := mul_nonneg l0.le e3; field_simp at this; linarith
      · have := mul_le_mul_of_nonneg_left e4 l0.le; field_simp at this; linarith)
    (fun i j hij => by
      rw [Set.disjoint_left]; intro p h1 h2
      exact Set.disjoint_left.1 (hd i j hij) ((mem_sqInt_scale l0).1 h1) ((mem_sqInt_scale l0).1 h2))
  have hcard : ∑ x ∈ A, (fun _ => (1 : ℝ)) x ≤ 4 := by
    simp only [Finset.sum_const, nsmul_eq_mul, mul_one]
    exact_mod_cast Finset.card_le_four
  norm_num at key hcard
  linarith

end SquarePacking
