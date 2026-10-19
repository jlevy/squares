import Sq19Lean.Endgame.PhiExpr
import Sq19Lean.Endgame.Farkas3

/-!
# The rows on H as angle expressions

Square angles: `angE θ s m` (`m = 0` axis, `m = 1` tilted). Index `0` is not a square, so on H its
angle offset is `0` and `Ex.cs 0 M`, `Ex.sn 0 M` are the fixed directions `cos (M π/4)`, `sin (M π/4)`.

`ProwB j Y`: the P half-plane in case b (13-14 separated by 14's face), with the 1-2 anchor owned by
square `j ∈ {1, 2}` and the offset bound `Y` for `c2y - c1y` (an end of its box chosen by the sign of
`sin g_j`), multiplied by `cos g_j > 0` so that no division remains:
`(cos g_j e2(φ14)) . c13 ≤ b0 + b1 L`.
-/
namespace Sq19.Endgame
open Sq19.Milp

structure RowE where
  ax : Ex
  ay : Ex
  b0 : Ex
  b1 : Ex

/-- The real row `ax x + ay y ≤ b0 + b1 L`. -/
def RowE.Holds (r : RowE) (θ : ℕ → ℝ) (x y L : ℝ) : Prop :=
  r.ax.real θ * x + r.ay.real θ * y ≤ r.b0.real θ + r.b1.real θ * L

/-- Signed wall/axis supports of P (case b), with an arbitrary anchor support lower bound.
The tilted-to-tilted support is exact and requires no sign choice. -/
structure PSigns where
  h1x : ℚ × ℚ
  h2y : ℚ × ℚ
  h2n : ℚ × ℚ
  anc : Ex

/-- `j` the owner of the 1-2 separation (1 or 2), `o` the other one. -/
def ProwB (j _o : ℕ) (Y : ℚ) (σ : PSigns) : RowE :=
  let cj := Ex.cs j 0
  let sj := Ex.sn j 0
  let h1x := suppE σ.h1x.1 σ.h1x.2 0 0 1 0
  let h2y := suppE σ.h2y.1 σ.h2y.2 0 2 2 0
  let h2n := suppE σ.h2n.1 σ.h2n.2 14 3 2 0
  let h13n := suppAbsE 14 3 13 1
  let anch := Ex.add (.c (1/2)) σ.anc
  ⟨.mul cj (.cs 14 3), .mul cj (.sn 14 3),
   .add (.mul (.cs 14 3) (.add (.add (.mul cj h1x) anch) (.neg (.mul sj (.c Y)))))
     (.mul cj (.add (.add (.add (.neg (.mul (.sn 14 3) h2y)) (.neg h2n)) (.c (-1))) (.neg h13n))),
   .mul cj (.sn 14 3)⟩

theorem angE_add (θ : ℕ → ℝ) (s M : ℕ) (k : ℕ) :
    angE θ s (M + 2 * k) = angE θ s M + k * (Real.pi / 2) := by
  unfold angE; push_cast; ring

/-- Soundness of `ProwB`: separations 2-14 (14's `+e2`), 13-14 (14's `-e2`), the 1-2 anchor of owner
`j`, the walls of 1 and 2, the offset bound and the signs give the row.
`σ.anc` may be the constant `1/2` (use `half_support_lb`) or any certified support lower bound. -/
theorem ProwB_holds {θ : ℕ → ℝ} {c1 c2 c13 c14 : ℝ × ℝ} {L : ℝ} {j o : ℕ} {Y : ℚ} {σ : PSigns}
    (hθ0 : θ 0 = 0)
    (h214 : Sep c14 (angE θ 14 1) c2 (angE θ 2 0) 1)
    (h1314 : Sep c14 (angE θ 14 1) c13 (angE θ 13 1) 3)
    (hanch : Real.cos (angE θ j 0) * (c2.1 - c1.1) + Real.sin (angE θ j 0) * (c2.2 - c1.2) ≥
      1/2 + supp (angE θ o 0) (angE θ j 0))
    (hw1 : supp (angE θ 1 0) 0 ≤ c1.1) (hw2 : c2.2 ≤ L - supp (angE θ 2 0) (Real.pi / 2))
    (hY : Real.sin (angE θ j 0) * (c2.2 - c1.2) ≤ Real.sin (angE θ j 0) * Y)
    (hcj : 0 < Real.cos (angE θ j 0)) (hs14 : 0 ≤ Real.sin (angE θ 14 1)) (hc14 : 0 ≤ Real.cos (angE θ 14 1))
    (e1 : (suppE σ.h1x.1 σ.h1x.2 0 0 1 0).real θ = supp (angE θ 1 0) (angE θ 0 0))
    (e2 : (suppE σ.h2y.1 σ.h2y.2 0 2 2 0).real θ = supp (angE θ 2 0) (angE θ 0 2))
    (e3 : (suppE σ.h2n.1 σ.h2n.2 14 3 2 0).real θ = supp (angE θ 2 0) (angE θ 14 3))
    (e5 : σ.anc.real θ ≤ supp (angE θ o 0) (angE θ j 0)) :
    (ProwB j o Y σ).Holds θ c13.1 c13.2 L := by
  have a00 : angE θ 0 0 = 0 := by simp [angE, hθ0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, hθ0]; ring
  have a143 : angE θ 14 3 = angE θ 14 1 + Real.pi / 2 := by
    have := angE_add θ 14 1 1; simpa using this
  have e4 := suppAbsE_real θ 14 3 13 1
  rw [a00] at e1; rw [a02] at e2; rw [a143] at e3 e4
  -- c2x lower bound X2
  set X2 := supp (angE θ 1 0) 0 + (1/2 + σ.anc.real θ - Real.sin (angE θ j 0) * Y) /
    Real.cos (angE θ j 0)
  have hX2 : X2 ≤ c2.1 := by
    have ha : Real.cos (angE θ j 0) * (c2.1 - c1.1) +
        Real.sin (angE θ j 0) * (c2.2 - c1.2) ≥ 1/2 + σ.anc.real θ := by linarith
    have h := shift_x_lb hcj ha (B := Real.sin (angE θ j 0) * Y) hY
    simp only [X2]; linarith
  have hrow := rowP_b h214 h1314 hX2 hw2 hs14 hc14
  have hm := mul_le_mul_of_nonneg_left hrow hcj.le
  unfold RowE.Holds ProwB
  simp only [Ex.real, e1, e2, e3, e4]
  have c3 : Real.cos (angE θ 14 3) = -Real.sin (angE θ 14 1) := by rw [a143, Real.cos_add_pi_div_two]
  have s3 : Real.sin (angE θ 14 3) = Real.cos (angE θ 14 1) := by rw [a143, Real.sin_add_pi_div_two]
  have cs3 : Real.cos ((3:ℕ) * Real.pi / 4 + θ 14) = -Real.sin (angE θ 14 1) := by
    rw [← c3]; rfl
  have sn3 : Real.sin ((3:ℕ) * Real.pi / 4 + θ 14) = Real.cos (angE θ 14 1) := by
    rw [← s3]; rfl
  have cj : Real.cos (((0:ℕ):ℝ) * Real.pi / 4 + θ j) = Real.cos (angE θ j 0) := rfl
  have sj : Real.sin (((0:ℕ):ℝ) * Real.pi / 4 + θ j) = Real.sin (angE θ j 0) := rfl
  rw [cs3, sn3, cj, sj]
  have ex : Real.cos (angE θ j 0) * X2 = Real.cos (angE θ j 0) * supp (angE θ 1 0) 0 +
      (1/2 + σ.anc.real θ - Real.sin (angE θ j 0) * Y) := by
    simp only [X2]; field_simp
  push_cast
  nlinarith [ex]

/-- Signed wall/axis supports of Q (case b). The tilted-to-tilted support is exact. -/
structure QSigns where
  h10x : ℚ × ℚ
  h10y : ℚ × ℚ
  h10n : ℚ × ℚ

/-- The Q half-plane in case b (13-11 separated by 11's face `-e1`), `n = e1(φ11)`:
`n . c13 ≤ cos f (L - h10x) + sin f (L - h10y) - h10(n) - 1 - h13(n)`. -/
def QrowB (σ : QSigns) : RowE :=
  let h10x := suppE σ.h10x.1 σ.h10x.2 0 0 10 0
  let h10y := suppE σ.h10y.1 σ.h10y.2 0 2 10 0
  let h10n := suppE σ.h10n.1 σ.h10n.2 11 1 10 0
  let h13n := suppAbsE 11 1 13 1
  ⟨.cs 11 1, .sn 11 1,
   .add (.add (.add (.neg (.mul (.cs 11 1) h10x)) (.neg (.mul (.sn 11 1) h10y))) (.neg h10n))
     (.add (.c (-1)) (.neg h13n)),
   .add (.cs 11 1) (.sn 11 1)⟩

theorem QrowB_holds {θ : ℕ → ℝ} {c10 c11 c13 : ℝ × ℝ} {L : ℝ} {σ : QSigns}
    (hθ0 : θ 0 = 0)
    (h1011 : Sep c11 (angE θ 11 1) c10 (angE θ 10 0) 0)
    (h1311 : Sep c11 (angE θ 11 1) c13 (angE θ 13 1) 2)
    (hx : c10.1 ≤ L - supp (angE θ 10 0) 0) (hy : c10.2 ≤ L - supp (angE θ 10 0) (Real.pi / 2))
    (hc : 0 ≤ Real.cos (angE θ 11 1)) (hs : 0 ≤ Real.sin (angE θ 11 1))
    (e1 : (suppE σ.h10x.1 σ.h10x.2 0 0 10 0).real θ = supp (angE θ 10 0) (angE θ 0 0))
    (e2 : (suppE σ.h10y.1 σ.h10y.2 0 2 10 0).real θ = supp (angE θ 10 0) (angE θ 0 2))
    (e3 : (suppE σ.h10n.1 σ.h10n.2 11 1 10 0).real θ = supp (angE θ 10 0) (angE θ 11 1)) :
    (QrowB σ).Holds θ c13.1 c13.2 L := by
  have a00 : angE θ 0 0 = 0 := by simp [angE, hθ0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, hθ0]; ring
  rw [a00] at e1; rw [a02] at e2
  have e4 := suppAbsE_real θ 11 1 13 1
  have hrow := rowQ_b h1011 h1311 hx hy hc hs
  unfold RowE.Holds QrowB
  simp only [Ex.real, e1, e2, e3, e4]
  have ca : Real.cos (((1:ℕ):ℝ) * Real.pi / 4 + θ 11) = Real.cos (angE θ 11 1) := rfl
  have sa : Real.sin (((1:ℕ):ℝ) * Real.pi / 4 + θ 11) = Real.sin (angE θ 11 1) := rfl
  rw [ca, sa]
  push_cast
  linarith

/-- F1 with `g8 ≥ 0` and the 5-8 separation owned by 8 (8's face `-e2`): `w = e2 φ8`,
`-w . c13 ≤ -(-sin φ8 X5 + cos φ8 h5y + 1/2 + h5(w) + 1/2 + h13(w))`, `X5 ≥ c5x` a box constant. The expression `s5w` may underapproximate `h5(w)`. -/
def F1rowPos8 (X5 : ℚ) (s5y s13w : ℚ × ℚ) (s5w : Ex) : RowE :=
  let h5y := suppE s5y.1 s5y.2 0 2 5 0
  let h5w := s5w
  let h13w := suppE s13w.1 s13w.2 8 2 13 1
  ⟨.neg (.cs 8 2), .neg (.sn 8 2),
   .neg (.add (.add (.add (.add (.mul (.cs 8 2) (.c X5)) (.mul (.sn 8 2) h5y)) (.c (1/2))) h5w)
     (.add (.c (1/2)) h13w)),
   .c 0⟩

theorem F1rowPos8_holds {θ : ℕ → ℝ} {c5 c8 c13 : ℝ × ℝ} {L : ℝ} {X5 : ℚ} {s5y s13w : ℚ × ℚ} {s5w : Ex}
    (hθ0 : θ 0 = 0)
    (h813 : Sep c8 (angE θ 8 0) c13 (angE θ 13 1) 1) (h58 : Sep c8 (angE θ 8 0) c5 (angE θ 5 0) 3)
    (hx : c5.1 ≤ X5) (hy : supp (angE θ 5 0) (Real.pi / 2) ≤ c5.2)
    (hs : 0 ≤ Real.sin (angE θ 8 0)) (hc : 0 ≤ Real.cos (angE θ 8 0))
    (e1 : (suppE s5y.1 s5y.2 0 2 5 0).real θ = supp (angE θ 5 0) (angE θ 0 2))
    (e2 : (s5w).real θ ≤ supp (angE θ 5 0) (angE θ 8 2))
    (e3 : (suppE s13w.1 s13w.2 8 2 13 1).real θ = supp (angE θ 13 1) (angE θ 8 2)) :
    (F1rowPos8 X5 s5y s13w s5w).Holds θ c13.1 c13.2 L := by
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, hθ0]; ring
  have a82 : angE θ 8 2 = angE θ 8 0 + Real.pi / 2 := by have := angE_add θ 8 0 1; simpa using this
  rw [a02] at e1; rw [a82] at e2 e3
  have hrow := rowF1_pos_owner8 h813 h58 hx hy hs hc
  unfold RowE.Holds F1rowPos8
  simp only [Ex.real, e1, e3]
  have c2 : Real.cos (((2:ℕ):ℝ) * Real.pi / 4 + θ 8) = -Real.sin (angE θ 8 0) := by
    rw [show ((2:ℕ):ℝ) * Real.pi / 4 + θ 8 = angE θ 8 2 by rfl, a82, Real.cos_add_pi_div_two]
  have s2 : Real.sin (((2:ℕ):ℝ) * Real.pi / 4 + θ 8) = Real.cos (angE θ 8 0) := by
    rw [show ((2:ℕ):ℝ) * Real.pi / 4 + θ 8 = angE θ 8 2 by rfl, a82, Real.sin_add_pi_div_two]
  rw [c2, s2]
  push_cast
  linarith

/-- F1 with `g8 < 0`: `-c13y ≤ -(c8y_lo + (1/2 + h13(w) - |sin φ8| Xh)/cos φ8)` with the 5-8 anchor
`c8y_lo = h5y + (anch58 + sin g_j X)/cos g_j` (owner `j ∈ {5, 8}`, `X` an end of the `c8x - c5x` box),
multiplied by `cos φ8 cos g_j > 0`. The expression `sanc` is a support lower bound. -/
def F1rowNeg (j _o : ℕ) (X Xh : ℚ) (s5y s13w : ℚ × ℚ) (sanc : Ex) : RowE :=
  let h5y := suppE s5y.1 s5y.2 0 2 5 0
  let h13w := suppE s13w.1 s13w.2 8 2 13 1
  let anch := Ex.add (.c (1/2)) sanc
  let c8 := Ex.cs 8 0
  let cj := Ex.cs j 0
  ⟨.c 0, .neg (.mul c8 cj),
   .neg (.add (.mul c8 (.add (.mul cj h5y) (.add anch (.mul (.sn j 0) (.c X)))))
     (.mul cj (.add (.add (.c (1/2)) h13w) (.mul (.sn 8 0) (.c Xh))))),
   .c 0⟩

theorem F1rowNeg_holds {θ : ℕ → ℝ} {c5 c8 c13 : ℝ × ℝ} {L : ℝ} {j o : ℕ} {X Xh : ℚ}
    {s5y s13w : ℚ × ℚ} {sanc : Ex}
    (hθ0 : θ 0 = 0)
    (h813 : Sep c8 (angE θ 8 0) c13 (angE θ 13 1) 1)
    (hanch : -Real.sin (angE θ j 0) * (c8.1 - c5.1) + Real.cos (angE θ j 0) * (c8.2 - c5.2) ≥
      1/2 + supp (angE θ o 0) (angE θ j 2))
    (hX : Real.sin (angE θ j 0) * X ≤ Real.sin (angE θ j 0) * (c8.1 - c5.1))
    (hw5 : supp (angE θ 5 0) (Real.pi / 2) ≤ c5.2)
    (hXh : c13.1 - c8.1 ≤ Xh)
    (hcj : 0 < Real.cos (angE θ j 0)) (hs8 : Real.sin (angE θ 8 0) ≤ 0) (hc8 : 0 < Real.cos (angE θ 8 0))
    (e1 : (suppE s5y.1 s5y.2 0 2 5 0).real θ = supp (angE θ 5 0) (angE θ 0 2))
    (e2 : (suppE s13w.1 s13w.2 8 2 13 1).real θ = supp (angE θ 13 1) (angE θ 8 2))
    (e3 : sanc.real θ ≤ supp (angE θ o 0) (angE θ j 2)) :
    (F1rowNeg j o X Xh s5y s13w sanc).Holds θ c13.1 c13.2 L := by
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, hθ0]; ring
  have a82 : angE θ 8 2 = angE θ 8 0 + Real.pi / 2 := by have := angE_add θ 8 0 1; simpa using this
  rw [a02] at e1; rw [a82] at e2
  -- c8y lower bound
  set Y8 := supp (angE θ 5 0) (Real.pi / 2) +
    (1/2 + sanc.real θ + Real.sin (angE θ j 0) * X) / Real.cos (angE θ j 0)
  have hY8 : Y8 ≤ c8.2 := by
    have : (1/2 + sanc.real θ + Real.sin (angE θ j 0) * X) / Real.cos (angE θ j 0) ≤
        c8.2 - c5.2 := by
      rw [div_le_iff₀ hcj]; nlinarith
    simp only [Y8]; linarith
  have hrow := rowF1_neg h813 hs8 hc8 hXh hY8
  rw [abs_of_nonpos hs8] at hrow
  have hpos : 0 < Real.cos (angE θ 8 0) * Real.cos (angE θ j 0) := mul_pos hc8 hcj
  have hm := mul_le_mul_of_nonneg_left hrow hpos.le
  unfold RowE.Holds F1rowNeg
  simp only [Ex.real, e1, e2]
  have c8e : Real.cos (((0:ℕ):ℝ) * Real.pi / 4 + θ 8) = Real.cos (angE θ 8 0) := rfl
  have s8e : Real.sin (((0:ℕ):ℝ) * Real.pi / 4 + θ 8) = Real.sin (angE θ 8 0) := rfl
  have cje : Real.cos (((0:ℕ):ℝ) * Real.pi / 4 + θ j) = Real.cos (angE θ j 0) := rfl
  have sje : Real.sin (((0:ℕ):ℝ) * Real.pi / 4 + θ j) = Real.sin (angE θ j 0) := rfl
  rw [c8e, s8e, cje, sje]
  have ex1 : Real.cos (angE θ j 0) * Y8 = Real.cos (angE θ j 0) * supp (angE θ 5 0) (Real.pi / 2) +
      (1/2 + sanc.real θ + Real.sin (angE θ j 0) * X) := by
    simp only [Y8]; field_simp
  have ex2 : Real.cos (angE θ 8 0) * ((1/2 + supp (angE θ 13 1) (angE θ 8 0 + Real.pi / 2) -
      -Real.sin (angE θ 8 0) * Xh) / Real.cos (angE θ 8 0)) =
      1/2 + supp (angE θ 13 1) (angE θ 8 0 + Real.pi / 2) + Real.sin (angE θ 8 0) * Xh := by
    field_simp; ring
  push_cast
  nlinarith [ex1, ex2]

/-- F1 with `g8 ≥ 0` and the 5-8 separation owned by 5 (5's face `+e2`): `m = e2 φ5`, `t = e1 φ5`,
`d = φ8 - φ5`, `w.c8 ≥ cos d (M0 + 1/2 + h8(m)) - sin d (cos φ5 Cx + sin φ5 Cy)` with
`M0 = -sin φ5 X5 + cos φ5 h5y`; box constants `X5` (for `c5x`) and `Cx, Cy` (for `c8`). The expression `s8m` is a support lower bound. -/
def F1rowPos5 (X5 Cx Cy : ℚ) (s5y s13w : ℚ × ℚ) (s8m : Ex) : RowE :=
  let h5y := suppE s5y.1 s5y.2 0 2 5 0
  let h8m := s8m
  let h13w := suppE s13w.1 s13w.2 8 2 13 1
  let M0 := Ex.add (.neg (.mul (.sn 5 0) (.c X5))) (.mul (.cs 5 0) h5y)
  let W8 := Ex.add (.mul (cosD 8 0 5 0) (.add (.add M0 (.c (1/2))) h8m))
    (.neg (.mul (sinD 8 0 5 0) (.add (.mul (.cs 5 0) (.c Cx)) (.mul (.sn 5 0) (.c Cy)))))
  ⟨.neg (.cs 8 2), .neg (.sn 8 2), .neg (.add (.add W8 (.c (1/2))) h13w), .c 0⟩

theorem F1rowPos5_holds {θ : ℕ → ℝ} {c5 c8 c13 : ℝ × ℝ} {L : ℝ} {X5 Cx Cy : ℚ} {s5y s13w : ℚ × ℚ} {s8m : Ex}
    (hθ0 : θ 0 = 0)
    (h813 : Sep c8 (angE θ 8 0) c13 (angE θ 13 1) 1) (h58 : Sep c5 (angE θ 5 0) c8 (angE θ 8 0) 1)
    (hX5 : Real.sin (angE θ 5 0) * c5.1 ≤ Real.sin (angE θ 5 0) * X5)
    (hc5 : 0 ≤ Real.cos (angE θ 5 0)) (hw5 : supp (angE θ 5 0) (Real.pi / 2) ≤ c5.2)
    (ht : Real.sin (angE θ 8 0 - angE θ 5 0) * (Real.cos (angE θ 5 0) * c8.1 + Real.sin (angE θ 5 0) * c8.2) ≤
      Real.sin (angE θ 8 0 - angE θ 5 0) * (Real.cos (angE θ 5 0) * Cx + Real.sin (angE θ 5 0) * Cy))
    (hcd : 0 ≤ Real.cos (angE θ 8 0 - angE θ 5 0))
    (e1 : (suppE s5y.1 s5y.2 0 2 5 0).real θ = supp (angE θ 5 0) (angE θ 0 2))
    (e2 : (s8m).real θ ≤ supp (angE θ 8 0) (angE θ 5 2))
    (e3 : (suppE s13w.1 s13w.2 8 2 13 1).real θ = supp (angE θ 13 1) (angE θ 8 2)) :
    (F1rowPos5 X5 Cx Cy s5y s13w s8m).Holds θ c13.1 c13.2 L := by
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, hθ0]; ring
  have a82 : angE θ 8 2 = angE θ 8 0 + Real.pi / 2 := by have := angE_add θ 8 0 1; simpa using this
  have a52 : angE θ 5 2 = angE θ 5 0 + Real.pi / 2 := by have := angE_add θ 5 0 1; simpa using this
  rw [a02] at e1; rw [a52] at e2; rw [a82] at e3
  have hm : -Real.sin (angE θ 5 0) * X5 + Real.cos (angE θ 5 0) * supp (angE θ 5 0) (Real.pi / 2) ≤
      -Real.sin (angE θ 5 0) * c5.1 + Real.cos (angE θ 5 0) * c5.2 := by
    have := mul_le_mul_of_nonneg_left hw5 hc5; linarith
  have hrow := rowF1_pos_owner5 h813 h58 hm ht hcd
  have he2 := mul_le_mul_of_nonneg_left e2 hcd
  unfold RowE.Holds F1rowPos5
  simp only [Ex.real, e1, e3, cosD_real, sinD_real]
  have c2 : Real.cos (((2:ℕ):ℝ) * Real.pi / 4 + θ 8) = -Real.sin (angE θ 8 0) := by
    rw [show ((2:ℕ):ℝ) * Real.pi / 4 + θ 8 = angE θ 8 2 by rfl, a82, Real.cos_add_pi_div_two]
  have s2 : Real.sin (((2:ℕ):ℝ) * Real.pi / 4 + θ 8) = Real.cos (angE θ 8 0) := by
    rw [show ((2:ℕ):ℝ) * Real.pi / 4 + θ 8 = angE θ 8 2 by rfl, a82, Real.sin_add_pi_div_two]
  have c5e : Real.cos (((0:ℕ):ℝ) * Real.pi / 4 + θ 5) = Real.cos (angE θ 5 0) := rfl
  have s5e : Real.sin (((0:ℕ):ℝ) * Real.pi / 4 + θ 5) = Real.sin (angE θ 5 0) := rfl
  rw [c2, s2, c5e, s5e]
  push_cast
  linarith

end Sq19.Endgame

#print axioms Sq19.Endgame.F1rowPos5_holds

#print axioms Sq19.Endgame.F1rowPos8_holds
#print axioms Sq19.Endgame.F1rowNeg_holds

#print axioms Sq19.Endgame.ProwB_holds
#print axioms Sq19.Endgame.QrowB_holds
