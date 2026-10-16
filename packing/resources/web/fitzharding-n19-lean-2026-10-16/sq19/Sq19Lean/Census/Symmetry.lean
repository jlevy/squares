import Sq19Lean.Census.Cells
import Sq17Lean.PropagationWall
import Sq17Lean.SquareBase

/-! The eight symmetries of the container `[0, 2443/500]^2` act on the 25 exact cells, on unit squares,
on disjointness of interiors and on containment. Adapted from the 17 project's `CellSymmetry` and
`WallSquareSymmetry` (pinned sq17-lean), with the 19 cover's side and 25 cells. -/
namespace Sq19.Census
open Sq17.Propagation

/-- Identity, x reflection, y reflection, half turn, diagonal reflection, quarter turn, inverse quarter
turn, other diagonal reflection, of the container `[0, U]^2`, `U = 2443/500`. -/
def action {K : Type*} [Field K] (g : Fin 8) (p : K × K) : K × K :=
  let U : K := 2443/500
  match g.val with
  | 0 => p
  | 1 => (U-p.1,p.2)
  | 2 => (p.1,U-p.2)
  | 3 => (U-p.1,U-p.2)
  | 4 => (p.2,p.1)
  | 5 => (U-p.2,p.1)
  | 6 => (p.2,U-p.1)
  | _ => (U-p.2,U-p.1)

def direction (g : Fin 8) (u : ℝ × ℝ) : ℝ × ℝ :=
  match g.val with
  | 0 => u
  | 1 => (-u.1,u.2)
  | 2 => (u.1,-u.2)
  | 3 => (-u.1,-u.2)
  | 4 => (u.2,u.1)
  | 5 => (-u.2,u.1)
  | 6 => (u.2,-u.1)
  | _ => (-u.2,-u.1)

theorem perm_inverse : ∀ g : Fin 8, ∀ i : Fin 25, perm (inv g) (perm g i) = i := by
  decide +kernel

theorem inverse_inverse : ∀ g : Fin 8, inv (inv g) = g := by decide +kernel

theorem perm_injective (g : Fin 8) : Function.Injective (perm g) := by
  intro i j h
  rw [← perm_inverse g i, ← perm_inverse g j, h]

/-- Every vertex of a cell maps to a vertex of the designated image cell. -/
theorem vertex_action_checked : ∀ g : Fin 8, ∀ i : Fin 25,
    (vertices i).all (fun p => decide (action g p ∈ vertices (perm g i))) = true := by
  decide +kernel

theorem action_cast (g : Fin 8) (p : ℚ × ℚ) :
    realPoint (action g p) = action g (realPoint p) := by
  fin_cases g <;> ext <;>
    simp [action,realPoint,Rat.cast_sub,Rat.cast_div,Rat.cast_ofNat]

theorem action_inverse (g : Fin 8) (p : ℝ × ℝ) : action (inv g) (action g p) = p := by
  fin_cases g <;> ext <;> simp [inv,action]

theorem action_affine (g : Fin 8) (p q : ℝ × ℝ) (a b : ℝ) (hab : a+b=1) :
    action g (a • p + b • q) = a • action g p + b • action g q := by
  fin_cases g <;> ext <;> simp [action] <;> nlinarith only [hab]

/-- Vertex checking lifts to the whole closed real cell. -/
theorem action_mem_cell (g : Fin 8) (i : Fin 25) {p : ℝ × ℝ}
    (hp : p ∈ cell i) : action g p ∈ cell (perm g i) := by
  let T := cell (perm g i)
  have ht : Convex ℝ T := convex_convexHull ℝ _
  have hpre : Convex ℝ {x | action g x ∈ T} := by
    intro x hx y hy a b ha hb hab
    change action g (a • x+b • y) ∈ T
    rw [action_affine g x y a b hab]
    exact ht hx hy ha hb hab
  apply convexHull_min (t := {x | action g x ∈ T}) ?_ hpre hp
  rintro _ ⟨q,hq,rfl⟩
  change action g (realPoint q) ∈ T
  rw [← action_cast]
  apply subset_convexHull ℝ _
  refine ⟨action g q,?_,rfl⟩
  exact of_decide_eq_true ((List.all_eq_true.mp (vertex_action_checked g i)) q hq)

noncomputable def homeomorph (g : Fin 8) : (ℝ × ℝ) ≃ₜ (ℝ × ℝ) where
  toFun := action g
  invFun := action (inv g)
  left_inv := action_inverse g
  right_inv p := by simpa only [inverse_inverse] using action_inverse (inv g) p
  continuous_toFun := by
    change Continuous (fun p => action g p)
    fin_cases g <;> simp only [action] <;> fun_prop
  continuous_invFun := by
    change Continuous (fun p => action (inv g) p)
    fin_cases g <;> simp [inv,action] <;> constructor <;> fun_prop

theorem direction_unit (g : Fin 8) (u : ℝ × ℝ) (hu : u.1^2+u.2^2=1) :
    (direction g u).1^2+(direction g u).2^2=1 := by
  fin_cases g <;> simp [direction] <;> nlinarith only [hu]

theorem action_mem_square (g : Fin 8) (p u z : ℝ × ℝ) :
    action g z ∈ Sq17.sq (action g p).1 (action g p).2
      (direction g u).1 (direction g u).2 ↔ z ∈ Sq17.sq p.1 p.2 u.1 u.2 := by
  fin_cases g <;> simp only [action,direction,Sq17.sq,Set.mem_ofPred_eq,abs_le] <;>
    constructor <;> intro h <;> rcases h with ⟨⟨h1,h2⟩,⟨h3,h4⟩⟩ <;>
    constructor <;> constructor <;> nlinarith only [h1,h2,h3,h4]

theorem action_square_image (g : Fin 8) (p u : ℝ × ℝ) :
    action g '' Sq17.sq p.1 p.2 u.1 u.2 =
      Sq17.sq (action g p).1 (action g p).2 (direction g u).1 (direction g u).2 := by
  ext z
  constructor
  · rintro ⟨x,hx,rfl⟩
    exact (action_mem_square g p u x).2 hx
  · intro hz
    obtain ⟨x,rfl⟩ := (homeomorph g).surjective z
    exact ⟨x,(action_mem_square g p u x).1 hz,rfl⟩

theorem action_square_disjoint (g : Fin 8) (p q u v : ℝ × ℝ)
    (hd : Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2))
      (interior (Sq17.sq q.1 q.2 v.1 v.2))) :
    Disjoint (interior (Sq17.sq (action g p).1 (action g p).2
      (direction g u).1 (direction g u).2))
      (interior (Sq17.sq (action g q).1 (action g q).2
      (direction g v).1 (direction g v).2)) := by
  rw [← action_square_image,← action_square_image]
  change Disjoint (interior ((homeomorph g) '' _)) (interior ((homeomorph g) '' _))
  rw [← (homeomorph g).image_interior,← (homeomorph g).image_interior]
  apply Set.disjoint_left.mpr
  rintro z ⟨x,hx,rfl⟩ ⟨y,hy,he⟩
  have hxy : y = x := (homeomorph g).injective he
  exact Set.disjoint_left.mp hd hx (hxy ▸ hy)

theorem action_mem_container (g : Fin 8) (z : ℝ × ℝ)
    (hz : z ∈ containerBox (2443/500)) : action g z ∈ containerBox (2443/500) := by
  fin_cases g <;> simp only [action,containerBox,Set.mem_ofPred_eq] at * <;>
    rcases hz with ⟨h1,h2,h3,h4⟩ <;> exact ⟨by linarith,by linarith,by linarith,by linarith⟩

theorem action_square_fit (g : Fin 8) (p u : ℝ × ℝ)
    (hfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox (2443/500)) :
    Sq17.sq (action g p).1 (action g p).2 (direction g u).1 (direction g u).2 ⊆
      containerBox (2443/500) := by
  rw [← action_square_image]
  rintro _ ⟨z,hz,rfl⟩
  exact action_mem_container g z (hfit hz)

end Sq19.Census

#print axioms Sq19.Census.vertex_action_checked
#print axioms Sq19.Census.action_mem_cell
#print axioms Sq19.Census.action_square_disjoint
#print axioms Sq19.Census.action_square_fit
