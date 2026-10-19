import Sq19Lean.Endgame.RowsH

/-!
# Combination of the three rows (LOCAL_THEOREM.md, Lean piece 3)

For rows `P, Q, F` (as `RowE`), `lam P Q F = -(a_Q × a_F, a_F × a_P, a_P × a_Q)` and
`S0 = Σ λ_i b0_i`, `S1 = Σ λ_i b1_i` are expressions in the angles. `combine`: if the three rows hold at
`c13`, the multipliers are nonnegative and `S1 > 0`, then `L ≥ -S0/S1` (this is `Phi` of endgame_cert.c,
up to the positive row scalings, which leave the quotient unchanged).
-/
namespace Sq19.Endgame
open Sq19.Milp

def crossE (ax ay bx by' : Ex) : Ex := .add (.mul ax by') (.neg (.mul ay bx))

def lam1 (P Q F : RowE) : Ex := .neg (crossE Q.ax Q.ay F.ax F.ay)
def lam2 (P Q F : RowE) : Ex := .neg (crossE F.ax F.ay P.ax P.ay)
def lam3 (P Q F : RowE) : Ex := .neg (crossE P.ax P.ay Q.ax Q.ay)

def S0E (P Q F : RowE) : Ex :=
  .add (.add (.mul (lam1 P Q F) P.b0) (.mul (lam2 P Q F) Q.b0)) (.mul (lam3 P Q F) F.b0)
def S1E (P Q F : RowE) : Ex :=
  .add (.add (.mul (lam1 P Q F) P.b1) (.mul (lam2 P Q F) Q.b1)) (.mul (lam3 P Q F) F.b1)

theorem combine {P Q F : RowE} {θ : ℕ → ℝ} {x y L : ℝ}
    (hP : P.Holds θ x y L) (hQ : Q.Holds θ x y L) (hF : F.Holds θ x y L)
    (l1 : 0 ≤ (lam1 P Q F).real θ) (l2 : 0 ≤ (lam2 P Q F).real θ) (l3 : 0 ≤ (lam3 P Q F).real θ)
    (hS : 0 < (S1E P Q F).real θ) :
    -(S0E P Q F).real θ / (S1E P Q F).real θ ≤ L := by
  simp only [lam1, lam2, lam3, crossE, Ex.real] at l1 l2 l3
  have h := farkas3 (x := x) (y := y) hP hQ hF (by unfold cross; linarith) (by unfold cross; linarith)
    (by unfold cross; linarith)
  have hS' : 0 < (S1E P Q F).real θ := hS
  simp only [S0E, S1E, lam1, lam2, lam3, crossE, Ex.real] at hS' ⊢
  rw [div_le_iff₀ hS']
  unfold cross at h
  nlinarith [h]

end Sq19.Endgame

#print axioms Sq19.Endgame.combine
