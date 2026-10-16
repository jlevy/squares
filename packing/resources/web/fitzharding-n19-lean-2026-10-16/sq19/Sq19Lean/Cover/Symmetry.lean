import Sq17Lean.SquareSupportSeparation
import Sq17Lean.PropagationWall

/-!
# Symmetries of the container `[0, U]^2`, `U = 2443/500`

`act sw fx fy` first swaps the coordinates (if `sw`), then reflects `x ↦ U - x` (if `fx`) and
`y ↦ U - y` (if `fy`). `dir sw fx fy` is its linear part, applied to square directions and to
separating normals. Disjointness is transferred through the support-gap characterisation of
the 17 project (`square_disjoint_unit_separator`, `support_gap_disjoint`), and containment
through the axis supports (`FitsU`), so no topology of the maps is needed.
-/
namespace Sq19.Cover
open Sq17.WallCapacity Sq17.Propagation

/-- The cover-frame container side. -/
def U : ℚ := 2443/500

noncomputable def act (sw fx fy : Bool) (z : ℝ × ℝ) : ℝ × ℝ :=
  let w : ℝ × ℝ := if sw then (z.2, z.1) else z
  (if fx then 2443/500 - w.1 else w.1, if fy then 2443/500 - w.2 else w.2)

def dir (sw fx fy : Bool) (z : ℝ × ℝ) : ℝ × ℝ :=
  let w : ℝ × ℝ := if sw then (z.2, z.1) else z
  (if fx then -w.1 else w.1, if fy then -w.2 else w.2)

theorem dir_unit (sw fx fy : Bool) (u : ℝ × ℝ) (hu : u.1^2+u.2^2=1) :
    (dir sw fx fy u).1^2+(dir sw fx fy u).2^2=1 := by
  cases sw <;> cases fx <;> cases fy <;> simp only [dir] <;> simp <;> linarith

private theorem abs_pair (A B A' B' : ℝ) (hA : A' = A ∨ A' = -A) (hB : B' = B ∨ B' = -B) :
    |A'|+|B'| = |A|+|B| := by
  rcases hA with h | h <;> rcases hB with h' | h' <;> simp [h, h', abs_neg]

theorem support_dir (sw fx fy : Bool) (u m : ℝ × ℝ) :
    squareSupport (dir sw fx fy u).1 (dir sw fx fy u).2 (dir sw fx fy m).1 (dir sw fx fy m).2 =
      squareSupport u.1 u.2 m.1 m.2 := by
  unfold squareSupport
  congr 1
  apply abs_pair <;>
  cases sw <;> cases fx <;> cases fy <;> simp only [dir] <;> simp <;>
    first | (left; ring1) | (right; ring1)

theorem dot_act (sw fx fy : Bool) (m p q : ℝ × ℝ) :
    (dir sw fx fy m).1*((act sw fx fy q).1-(act sw fx fy p).1) +
      (dir sw fx fy m).2*((act sw fx fy q).2-(act sw fx fy p).2) =
    m.1*(q.1-p.1)+m.2*(q.2-p.2) := by
  cases sw <;> cases fx <;> cases fy <;> simp only [act, dir] <;> simp <;> ring

/-- Disjoint interiors are preserved by the container symmetries. -/
theorem act_disjoint (sw fx fy : Bool) (p q u v : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hd : Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2))) :
    Disjoint
      (interior (Sq17.sq (act sw fx fy p).1 (act sw fx fy p).2
        (dir sw fx fy u).1 (dir sw fx fy u).2))
      (interior (Sq17.sq (act sw fx fy q).1 (act sw fx fy q).2
        (dir sw fx fy v).1 (dir sw fx fy v).2)) := by
  obtain ⟨a,b,hm,hgap⟩ := square_disjoint_unit_separator p q u.1 u.2 v.1 v.2 hu hv hd
  have hm' := dir_unit sw fx fy (a,b) hm
  apply support_gap_disjoint _ _ _ _ _ _ _ _ (dir_unit sw fx fy u hu) (dir_unit sw fx fy v hv) hm'
  rw [support_dir, support_dir, dot_act]
  exact hgap

/-- Containment in `[0, U]^2` read through the axis supports `h = (|ux|+|uy|)/2`. -/
def FitsU (p u : ℝ × ℝ) : Prop :=
  (|u.1|+|u.2|)/2 ≤ p.1 ∧ p.1 ≤ 2443/500-(|u.1|+|u.2|)/2 ∧
  (|u.1|+|u.2|)/2 ≤ p.2 ∧ p.2 ≤ 2443/500-(|u.1|+|u.2|)/2

private theorem support_x (ux uy : ℝ) : squareSupport ux uy 1 0 = (|ux|+|uy|)/2 := by
  unfold squareSupport; simp [abs_neg]

private theorem support_y (ux uy : ℝ) : squareSupport ux uy 0 1 = (|ux|+|uy|)/2 := by
  unfold squareSupport; simp [add_comm]

theorem fitsU_of_subset (p u : ℝ × ℝ) (hu : u.1^2+u.2^2=1)
    (hfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox (2443/500)) : FitsU p u := by
  have bound (a b : ℝ) : ∃ z ∈ Sq17.sq p.1 p.2 u.1 u.2,
      a*z.1+b*z.2 = a*p.1+b*p.2+squareSupport u.1 u.2 a b :=
    squareSupport_attained p.1 p.2 u.1 u.2 a b hu
  obtain ⟨z1,h1,e1⟩ := bound 1 0
  obtain ⟨z2,h2,e2⟩ := bound (-1) 0
  obtain ⟨z3,h3,e3⟩ := bound 0 1
  obtain ⟨z4,h4,e4⟩ := bound 0 (-1)
  have s2 : squareSupport u.1 u.2 (-1) 0 = squareSupport u.1 u.2 1 0 := by
    simpa using squareSupport_neg u.1 u.2 1 0
  have s4 : squareSupport u.1 u.2 0 (-1) = squareSupport u.1 u.2 0 1 := by
    simpa using squareSupport_neg u.1 u.2 0 1
  rw [s2] at e2
  rw [s4] at e4
  rw [support_x] at e1 e2
  rw [support_y] at e3 e4
  have c1 := hfit h1; have c2 := hfit h2; have c3 := hfit h3; have c4 := hfit h4
  simp only [containerBox, Set.mem_ofPred_eq] at c1 c2 c3 c4
  refine ⟨?_,?_,?_,?_⟩ <;> linarith [c1.1, c1.2.1, c2.1, c3.2.2.2, c4.2.2.1]

theorem subset_of_fitsU (p u : ℝ × ℝ) (hu : u.1^2+u.2^2=1) (h : FitsU p u) :
    Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox (2443/500) := by
  obtain ⟨h1,h2,h3,h4⟩ := h
  intro z hz
  have := support_walls_contained p u.1 u.2 (2443/500) hu
    (by rw [support_x]; exact h1) (by rw [support_x]; linarith)
    (by rw [support_y]; exact h3) (by rw [support_y]; linarith) hz
  exact this

theorem fitsU_act (sw fx fy : Bool) (p u : ℝ × ℝ) (h : FitsU p u) :
    FitsU (act sw fx fy p) (dir sw fx fy u) := by
  obtain ⟨h1,h2,h3,h4⟩ := h
  cases sw <;> cases fx <;> cases fy <;> simp only [FitsU, act, dir] <;> simp <;>
    refine ⟨?_,?_,?_,?_⟩ <;> linarith [abs_nonneg u.1, abs_nonneg u.2]

end Sq19.Cover

#print axioms Sq19.Cover.act_disjoint
#print axioms Sq19.Cover.fitsU_of_subset
#print axioms Sq19.Cover.fitsU_act
