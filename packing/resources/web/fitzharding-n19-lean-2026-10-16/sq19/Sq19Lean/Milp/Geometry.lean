import Sq17Lean.SquareSeparationGeometry
import Sq17Lean.PropagationWall

/-!
# Geometry of the certificate rows

A square with centre `c` and angle `φ` is `Sq17.sq c.1 c.2 (cos φ) (sin φ)`. Its vertices are
`c + R(φ) o_j`, `o_j ∈ {(-1/2,-1/2), (1/2,-1/2), (1/2,1/2), (-1/2,1/2)}` (the order of milp_cert.c).
Face `k` of a square has outward normal `(cos (φ + kπ/2), sin (φ + kπ/2))`.

* `vertex_in_container`: a square inside `[0, L]^2` has all four vertices there (wall rows).
* `face_disjunction`: two squares with disjoint interiors are separated by a face of one of them,
  in the form of milp_cert's face rows: all four vertices of the other square lie on the far side.
  Derived from the 17 project's `square_disjoint_axis`.
* `sep_support`: a separating face forces `n.(c_B - c_A) ≥ 1/2 + (|n.u_B| + |n.u_B^⊥|)/2`
  (used by the face test).
-/
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

namespace Sq19.Milp

noncomputable def ox : Fin 4 → ℝ := fun j => if j.val = 1 ∨ j.val = 2 then 1/2 else -1/2
noncomputable def oy : Fin 4 → ℝ := fun j => if j.val = 2 ∨ j.val = 3 then 1/2 else -1/2

theorem abs_ox (j : Fin 4) : |ox j| = 1/2 := by
  unfold ox; split_ifs <;> norm_num
theorem abs_oy (j : Fin 4) : |oy j| = 1/2 := by
  unfold oy; split_ifs <;> norm_num

/-- Vertex offset `R(φ) o_j`. -/
noncomputable def vx (φ : ℝ) (j : Fin 4) : ℝ := Real.cos φ * ox j - Real.sin φ * oy j
noncomputable def vy (φ : ℝ) (j : Fin 4) : ℝ := Real.sin φ * ox j + Real.cos φ * oy j

theorem vertex_mem (c : ℝ × ℝ) (φ : ℝ) (j : Fin 4) :
    (c.1 + vx φ j, c.2 + vy φ j) ∈ Sq17.sq c.1 c.2 (Real.cos φ) (Real.sin φ) := by
  have h := Real.sin_sq_add_cos_sq φ
  have e1 : (c.1 + vx φ j - c.1) * Real.cos φ + (c.2 + vy φ j - c.2) * Real.sin φ = ox j := by
    simp only [vx, vy]; linear_combination (ox j) * h
  have e2 : (c.2 + vy φ j - c.2) * Real.cos φ - (c.1 + vx φ j - c.1) * Real.sin φ = oy j := by
    simp only [vx, vy]; linear_combination (oy j) * h
  refine ⟨?_, ?_⟩
  · simp only; rw [e1, abs_ox]
  · simp only; rw [e2, abs_oy]

theorem vertex_in_container (c : ℝ × ℝ) (φ L : ℝ)
    (hfit : Sq17.sq c.1 c.2 (Real.cos φ) (Real.sin φ) ⊆ Sq17.Propagation.containerBox L)
    (j : Fin 4) :
    0 ≤ c.1 + vx φ j ∧ c.1 + vx φ j ≤ L ∧ 0 ≤ c.2 + vy φ j ∧ c.2 + vy φ j ≤ L :=
  hfit (vertex_mem c φ j)

/-- Outward normal of face `k`. -/
noncomputable def nx (φ : ℝ) (k : ℕ) : ℝ := Real.cos (φ + k * (Real.pi / 2))
noncomputable def ny (φ : ℝ) (k : ℕ) : ℝ := Real.sin (φ + k * (Real.pi / 2))

/-- Face `k` of the square `(cA, φA)` separates the square `(cB, φB)`: every vertex of `B` is at
distance at least `1/2` beyond the face line through `A`'s centre. -/
def Sep (cA : ℝ × ℝ) (φA : ℝ) (cB : ℝ × ℝ) (φB : ℝ) (k : ℕ) : Prop :=
  ∀ j : Fin 4, nx φA k * (cB.1 + vx φB j - cA.1) + ny φA k * (cB.2 + vy φB j - cA.2) ≥ 1/2

private theorem vertex_dot_lb (n1 n2 φ : ℝ) (j : Fin 4) :
    -(|n1 * Real.cos φ + n2 * Real.sin φ| + |-n1 * Real.sin φ + n2 * Real.cos φ|) / 2 ≤
      n1 * vx φ j + n2 * vy φ j := by
  have e : n1 * vx φ j + n2 * vy φ j =
      ox j * (n1 * Real.cos φ + n2 * Real.sin φ) + oy j * (-n1 * Real.sin φ + n2 * Real.cos φ) := by
    simp only [vx, vy]; ring
  rw [e]
  have h1 : -(|n1 * Real.cos φ + n2 * Real.sin φ|) / 2 ≤ ox j * (n1 * Real.cos φ + n2 * Real.sin φ) := by
    have := neg_abs_le (ox j * (n1 * Real.cos φ + n2 * Real.sin φ))
    rw [abs_mul, abs_ox] at this; linarith
  have h2 : -(|-n1 * Real.sin φ + n2 * Real.cos φ|) / 2 ≤ oy j * (-n1 * Real.sin φ + n2 * Real.cos φ) := by
    have := neg_abs_le (oy j * (-n1 * Real.sin φ + n2 * Real.cos φ))
    rw [abs_mul, abs_oy] at this; linarith
  linarith

/-- A normal far enough from the other square's centre separates all its vertices. -/
private theorem sep_of_gap (n1 n2 : ℝ) (cA cB : ℝ × ℝ) (φB : ℝ)
    (h : n1 * (cB.1 - cA.1) + n2 * (cB.2 - cA.2) ≥
      1/2 + (|n1 * Real.cos φB + n2 * Real.sin φB| + |-n1 * Real.sin φB + n2 * Real.cos φB|) / 2)
    (j : Fin 4) : n1 * (cB.1 + vx φB j - cA.1) + n2 * (cB.2 + vy φB j - cA.2) ≥ 1/2 := by
  have := vertex_dot_lb n1 n2 φB j
  linarith

theorem nrm_k (φ : ℝ) :
    (nx φ 0 = Real.cos φ ∧ ny φ 0 = Real.sin φ) ∧
    (nx φ 1 = -Real.sin φ ∧ ny φ 1 = Real.cos φ) ∧
    (nx φ 2 = -Real.cos φ ∧ ny φ 2 = -Real.sin φ) ∧
    (nx φ 3 = Real.sin φ ∧ ny φ 3 = -Real.cos φ) := by
  have e2 : φ + (2:ℕ) * (Real.pi / 2) = φ + Real.pi := by push_cast; ring
  have e3 : φ + (3:ℕ) * (Real.pi / 2) = (φ + Real.pi) + Real.pi / 2 := by push_cast; ring
  simp only [nx, ny]
  refine ⟨⟨by simp, by simp⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
  · simp [Real.cos_add_pi_div_two]
  · simp [Real.sin_add_pi_div_two]
  · rw [e2, Real.cos_add_pi]
  · rw [e2, Real.sin_add_pi]
  · rw [e3, Real.cos_add_pi_div_two, Real.sin_add_pi]; ring
  · rw [e3, Real.sin_add_pi_div_two, Real.cos_add_pi]

private theorem abs_sum_eq {X Y A B : ℝ}
    (h : ((X = A ∨ X = -A) ∧ (Y = B ∨ Y = -B)) ∨ ((X = B ∨ X = -B) ∧ (Y = A ∨ Y = -A))) :
    |X| + |Y| = |A| + |B| := by
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;> rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2 <;>
    simp [h1, h2, abs_neg, add_comm]

/-- **Face disjunction.** Two unit squares with disjoint interiors are separated by one of the
eight faces in the sense of `Sep`. -/
theorem face_disjunction (cA cB : ℝ × ℝ) (φA φB : ℝ)
    (hdis : Disjoint (interior (Sq17.sq cA.1 cA.2 (Real.cos φA) (Real.sin φA)))
      (interior (Sq17.sq cB.1 cB.2 (Real.cos φB) (Real.sin φB)))) :
    ∃ k < 4, Sep cA φA cB φB k ∨ Sep cB φB cA φA k := by
  have hu : Real.cos φA ^ 2 + Real.sin φA ^ 2 = 1 := Real.cos_sq_add_sin_sq φA
  have hv : Real.cos φB ^ 2 + Real.sin φB ^ 2 = 1 := Real.cos_sq_add_sin_sq φB
  have hax := Sq17.WallCapacity.square_disjoint_axis cA cB _ _ _ _ hu hv hdis
  obtain ⟨⟨a0, b0⟩, ⟨a1, b1⟩, ⟨a2, b2⟩, ⟨a3, b3⟩⟩ := nrm_k φA
  obtain ⟨⟨c0, d0⟩, ⟨c1, d1⟩, ⟨c2, d2⟩, ⟨c3, d3⟩⟩ := nrm_k φB
  set u1 := Real.cos φA; set u2 := Real.sin φA; set v1 := Real.cos φB; set v2 := Real.sin φB
  set D1 := cB.1 - cA.1; set D2 := cB.2 - cA.2
  have hH : (1 + |u1*v1+u2*v2| + |u1*v2-u2*v1|)/2 = 1/2 + (|u1*v1+u2*v2| + |u1*v2-u2*v1|)/2 := by ring
  have keyA : ∀ k, |nx φA k * v1 + ny φA k * v2| + |-nx φA k * v2 + ny φA k * v1| =
      |u1*v1+u2*v2| + |u1*v2-u2*v1| → nx φA k * D1 + ny φA k * D2 ≥
      (1 + |u1*v1+u2*v2| + |u1*v2-u2*v1|)/2 → Sep cA φA cB φB k := by
    intro k he hg j
    apply sep_of_gap
    rw [he]; linarith
  have keyB : ∀ k, |nx φB k * u1 + ny φB k * u2| + |-nx φB k * u2 + ny φB k * u1| =
      |u1*v1+u2*v2| + |u1*v2-u2*v1| → nx φB k * (-D1) + ny φB k * (-D2) ≥
      (1 + |u1*v1+u2*v2| + |u1*v2-u2*v1|)/2 → Sep cB φB cA φA k := by
    intro k he hg j
    apply sep_of_gap
    have e1 : cA.1 - cB.1 = -D1 := by simp only [D1]; ring
    have e2 : cA.2 - cB.2 = -D2 := by simp only [D2]; ring
    rw [e1, e2, he]; linarith
  rcases hax with h | h | h | h
  · rcases le_or_gt 0 (u1 * D1 + u2 * D2) with hs | hs
    · refine ⟨0, by norm_num, Or.inl (keyA 0 ?_ ?_)⟩
      · rw [a0, b0]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [a0, b0]; rw [abs_of_nonneg hs] at h; linarith
    · refine ⟨2, by norm_num, Or.inl (keyA 2 ?_ ?_)⟩
      · rw [a2, b2]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [a2, b2]; rw [abs_of_neg hs] at h; linarith
  · rcases le_or_gt 0 (u1 * D2 - u2 * D1) with hs | hs
    · refine ⟨1, by norm_num, Or.inl (keyA 1 ?_ ?_)⟩
      · rw [a1, b1]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [a1, b1]; rw [abs_of_nonneg hs] at h; linarith
    · refine ⟨3, by norm_num, Or.inl (keyA 3 ?_ ?_)⟩
      · rw [a3, b3]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [a3, b3]; rw [abs_of_neg hs] at h; linarith
  · rcases le_or_gt 0 (v1 * D1 + v2 * D2) with hs | hs
    · refine ⟨2, by norm_num, Or.inr (keyB 2 ?_ ?_)⟩
      · rw [c2, d2]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [c2, d2]; rw [abs_of_nonneg hs] at h; linarith
    · refine ⟨0, by norm_num, Or.inr (keyB 0 ?_ ?_)⟩
      · rw [c0, d0]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [c0, d0]; rw [abs_of_neg hs] at h; linarith
  · rcases le_or_gt 0 (v1 * D2 - v2 * D1) with hs | hs
    · refine ⟨3, by norm_num, Or.inr (keyB 3 ?_ ?_)⟩
      · rw [c3, d3]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [c3, d3]; rw [abs_of_nonneg hs] at h; linarith
    · refine ⟨1, by norm_num, Or.inr (keyB 1 ?_ ?_)⟩
      · rw [c1, d1]; apply abs_sum_eq; first | (left; constructor <;> first | (left; ring1) | (right; ring1)) | (right; constructor <;> first | (left; ring1) | (right; ring1))
      · rw [c1, d1]; rw [abs_of_neg hs] at h; linarith

/-- A separating face forces the centre gap to exceed `1/2` plus the support of the other square. -/
theorem sep_support (cA cB : ℝ × ℝ) (φA φB : ℝ) (k : ℕ) (h : Sep cA φA cB φB k) :
    nx φA k * (cB.1 - cA.1) + ny φA k * (cB.2 - cA.2) ≥
      1/2 + (|nx φA k * Real.cos φB + ny φA k * Real.sin φB| +
        |-nx φA k * Real.sin φB + ny φA k * Real.cos φB|) / 2 := by
  set n1 := nx φA k; set n2 := ny φA k
  set P := n1 * Real.cos φB + n2 * Real.sin φB
  set Q := -n1 * Real.sin φB + n2 * Real.cos φB
  have key : ∀ j : Fin 4, n1 * (cB.1 + vx φB j - cA.1) + n2 * (cB.2 + vy φB j - cA.2) =
      n1 * (cB.1 - cA.1) + n2 * (cB.2 - cA.2) + (ox j * P + oy j * Q) := by
    intro j; simp only [vx, vy, P, Q]; ring
  rcases le_or_gt 0 P with hP | hP <;> rcases le_or_gt 0 Q with hQ | hQ
  · have hj := h 0; rw [key] at hj
    have : ox 0 * P + oy 0 * Q = -(|P| + |Q|)/2 := by
      rw [abs_of_nonneg hP, abs_of_nonneg hQ]; norm_num [ox, oy]; ring
    linarith
  · have hj := h 3; rw [key] at hj
    have : ox 3 * P + oy 3 * Q = -(|P| + |Q|)/2 := by
      rw [abs_of_nonneg hP, abs_of_neg hQ]; norm_num [ox, oy]; ring
    linarith
  · have hj := h 1; rw [key] at hj
    have : ox 1 * P + oy 1 * Q = -(|P| + |Q|)/2 := by
      rw [abs_of_neg hP, abs_of_nonneg hQ]; norm_num [ox, oy]; ring
    linarith
  · have hj := h 2; rw [key] at hj
    have : ox 2 * P + oy 2 * Q = -(|P| + |Q|)/2 := by
      rw [abs_of_neg hP, abs_of_neg hQ]; norm_num [ox, oy]; ring
    linarith

end Sq19.Milp
