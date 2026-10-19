import Sq19Lean.Cover.CoverBox
import Sq19Lean.Cover.Symmetry
import Sq19Lean.Cover.CornerCapacity
import Sq19Lean.Cover.SideCapacity
import Sq17Lean.InteriorCellCapacity

/-!
# Capacity one for all 25 cells

Two unit squares inside `[0, U]^2`, `U = 2443/500`, with pairwise disjoint interiors never have
both centres in the same cell.
* Interior cells 16-24: every vertex pair is at squared distance at most `15488/15625 < 1`,
  so the centres are closer than 1 and the inscribed disks overlap (17 project,
  `not_disjoint_of_distSq_lt_one`).
* Corner cells 0-3 and side cells 4-15: a container symmetry `act` maps the cell's bounding
  box into the canonical region of `corner_capacity` or `side_capacity`.
All data checks (bounding boxes, images of the boxes, diameters) are kernel reductions.
-/
namespace Sq19.Cover
open Sq17.WallCapacity Sq17.Propagation Sq17.InteriorCells

/-- A closed axis box `(xl, xh, yl, yh)`. -/
abbrev Box := ℚ × ℚ × ℚ × ℚ

def InBox (b : Box) (p : ℝ × ℝ) : Prop :=
  (b.1 : ℝ) ≤ p.1 ∧ p.1 ≤ (b.2.1 : ℝ) ∧ (b.2.2.1 : ℝ) ≤ p.2 ∧ p.2 ≤ (b.2.2.2 : ℝ)

/-- The image of a box under `act sw fx fy`. -/
def imgBox (sw fx fy : Bool) (b : Box) : Box :=
  let b1 : Box := if sw then (b.2.2.1, b.2.2.2, b.1, b.2.1) else b
  let b2 : Box := if fx then (2443/500 - b1.2.1, 2443/500 - b1.1, b1.2.2.1, b1.2.2.2) else b1
  if fy then (b2.1, b2.2.1, 2443/500 - b2.2.2.2, 2443/500 - b2.2.2.1) else b2

theorem act_inBox (sw fx fy : Bool) (b : Box) (p : ℝ × ℝ) (h : InBox b p) :
    InBox (imgBox sw fx fy b) (act sw fx fy p) := by
  obtain ⟨h1,h2,h3,h4⟩ := h
  cases sw <;> cases fx <;> cases fy <;> simp only [InBox, imgBox, act] <;> simp <;>
    refine ⟨?_,?_,?_,?_⟩ <;> linarith

/-- Bounding boxes of the 25 cells, in file order. -/
def bbox : Fin 25 → Box := ![
  (1/2, 27/20, 1/2, 27/20), (442/125, 2193/500, 1/2, 27/20),
  (1/2, 27/20, 442/125, 2193/500), (442/125, 2193/500, 442/125, 2193/500),
  (27/20, 20787/10000, 1/2, 1387/1000), (28073/10000, 442/125, 1/2, 1387/1000),
  (27/20, 20787/10000, 3499/1000, 2193/500), (28073/10000, 442/125, 3499/1000, 2193/500),
  (1/2, 1387/1000, 27/20, 20787/10000), (3499/1000, 2193/500, 27/20, 20787/10000),
  (1/2, 1387/1000, 28073/10000, 442/125), (3499/1000, 2193/500, 28073/10000, 442/125),
  (20787/10000, 28073/10000, 1/2, 1387/1000), (20787/10000, 28073/10000, 3499/1000, 2193/500),
  (1/2, 1387/1000, 20787/10000, 28073/10000), (3499/1000, 2193/500, 20787/10000, 28073/10000),
  (1387/1000, 2091/1000, 1387/1000, 2091/1000), (559/200, 3499/1000, 1387/1000, 2091/1000),
  (1387/1000, 2091/1000, 559/200, 3499/1000), (559/200, 3499/1000, 559/200, 3499/1000),
  (2091/1000, 559/200, 1387/1000, 2091/1000), (2091/1000, 559/200, 559/200, 3499/1000),
  (1387/1000, 2091/1000, 2091/1000, 559/200), (559/200, 3499/1000, 2091/1000, 559/200),
  (2091/1000, 559/200, 2091/1000, 559/200)]

def inBoxQ (b : Box) (v : ℚ × ℚ) : Bool :=
  decide (b.1 ≤ v.1 ∧ v.1 ≤ b.2.1 ∧ b.2.2.1 ≤ v.2 ∧ v.2 ≤ b.2.2.2)

theorem bbox_checked : ∀ i : Fin 25, (vertices i).all (inBoxQ (bbox i)) = true := by
  decide +kernel

theorem cell_inBox (i : Fin 25) (p : ℝ × ℝ) (hp : p ∈ cell i) : InBox (bbox i) p := by
  have hc : Convex ℝ {p : ℝ × ℝ | InBox (bbox i) p} := by
    intro x hx y hy a b ha hb hab
    obtain ⟨x1,x2,x3,x4⟩ := hx
    obtain ⟨y1,y2,y3,y4⟩ := hy
    change ((bbox i).1 : ℝ) ≤ a*x.1+b*y.1 ∧ a*x.1+b*y.1 ≤ ((bbox i).2.1 : ℝ) ∧
      ((bbox i).2.2.1 : ℝ) ≤ a*x.2+b*y.2 ∧ a*x.2+b*y.2 ≤ ((bbox i).2.2.2 : ℝ)
    have he : b = 1-a := by linarith
    subst he
    refine ⟨?_,?_,?_,?_⟩ <;> nlinarith [mul_le_mul_of_nonneg_left x1 ha,
      mul_le_mul_of_nonneg_left x2 ha, mul_le_mul_of_nonneg_left x3 ha,
      mul_le_mul_of_nonneg_left x4 ha, mul_le_mul_of_nonneg_left y1 hb,
      mul_le_mul_of_nonneg_left y2 hb, mul_le_mul_of_nonneg_left y3 hb,
      mul_le_mul_of_nonneg_left y4 hb]
  apply convexHull_min (t := {p : ℝ × ℝ | InBox (bbox i) p}) ?_ hc hp
  rintro _ ⟨v,hv,rfl⟩
  have h := List.all_eq_true.mp (bbox_checked i) v hv
  simp only [inBoxQ, decide_eq_true_eq] at h
  obtain ⟨h1,h2,h3,h4⟩ := h
  simp only [InBox, Set.mem_ofPred_eq, realPoint]
  exact ⟨by exact_mod_cast h1, by exact_mod_cast h2, by exact_mod_cast h3, by exact_mod_cast h4⟩

/-! ## Wall and corner cells -/

/-- The symmetry taking wall cell `i` (index below 16) to the bottom wall or the corner at 0. -/
def trans : Fin 16 → Bool × Bool × Bool := ![
  (false,false,false), (false,true,false), (false,false,true), (false,true,true),
  (false,false,false), (false,false,false), (false,false,true), (false,false,true),
  (true,false,false), (true,false,true), (true,false,false), (true,false,true),
  (false,false,false), (false,false,true), (true,false,false), (true,false,true)]

/-- Left end of the canonical side window (unused for the corners 0-3). -/
def sideStart : Fin 16 → ℚ := ![0, 0, 0, 0,
  27/20, 28073/10000, 27/20, 28073/10000, 27/20, 27/20, 28073/10000, 28073/10000,
  20787/10000, 20787/10000, 20787/10000, 20787/10000]

def wallCheck (i : Fin 16) : Bool :=
  let B := imgBox (trans i).1 (trans i).2.1 (trans i).2.2 (bbox ⟨i.val, by omega⟩)
  if i.val < 4 then decide (B.2.1 ≤ 27/20 ∧ B.2.2.2 ≤ 27/20)
  else decide (sideStart i ≤ B.1 ∧ B.2.1 ≤ sideStart i + 7287/10000 ∧ B.2.2.2 ≤ 1387/1000)

theorem wall_checked : ∀ i : Fin 16, wallCheck i = true := by decide +kernel

private theorem corner_via (sw fx fy : Bool) (b : Box)
    (hb : (imgBox sw fx fy b).2.1 ≤ 27/20 ∧ (imgBox sw fx fy b).2.2.2 ≤ 27/20)
    (p q u v : ℝ × ℝ) (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hpf : FitsU p u) (hqf : FitsU q v) (hp : InBox b p) (hq : InBox b q) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2)) := by
  intro hd
  have hd' := act_disjoint sw fx fy p q u v hu hv hd
  have hps := subset_of_fitsU _ _ (dir_unit sw fx fy u hu) (fitsU_act sw fx fy p u hpf)
  have hqs := subset_of_fitsU _ _ (dir_unit sw fx fy v hv) (fitsU_act sw fx fy q v hqf)
  have hpb := act_inBox sw fx fy b p hp
  have hqb := act_inBox sw fx fy b q hq
  have h1 : ((imgBox sw fx fy b).2.1 : ℝ) ≤ 27/20 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb.1; push_cast at h; exact h
  have h2 : ((imgBox sw fx fy b).2.2.2 : ℝ) ≤ 27/20 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb.2; push_cast at h; exact h
  exact corner_capacity (act sw fx fy p) (act sw fx fy q) _ _ _ _
    (dir_unit sw fx fy u hu) (dir_unit sw fx fy v hv)
    (fun z hz => ⟨(hps hz).1, (hps hz).2.2.1⟩) (fun z hz => ⟨(hqs hz).1, (hqs hz).2.2.1⟩)
    (hpb.2.1.trans h1) (hpb.2.2.2.trans h2) (hqb.2.1.trans h1) (hqb.2.2.2.trans h2) hd'

private theorem side_via (sw fx fy : Bool) (b : Box) (x0 : ℚ)
    (hb : x0 ≤ (imgBox sw fx fy b).1 ∧ (imgBox sw fx fy b).2.1 ≤ x0 + 7287/10000 ∧
      (imgBox sw fx fy b).2.2.2 ≤ 1387/1000)
    (p q u v : ℝ × ℝ) (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hpf : FitsU p u) (hqf : FitsU q v) (hp : InBox b p) (hq : InBox b q) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2)) := by
  intro hd
  have hd' := act_disjoint sw fx fy p q u v hu hv hd
  have hps := subset_of_fitsU _ _ (dir_unit sw fx fy u hu) (fitsU_act sw fx fy p u hpf)
  have hqs := subset_of_fitsU _ _ (dir_unit sw fx fy v hv) (fitsU_act sw fx fy q v hqf)
  have hpb := act_inBox sw fx fy b p hp
  have hqb := act_inBox sw fx fy b q hq
  have h0 : (x0 : ℝ) ≤ (imgBox sw fx fy b).1 := by exact_mod_cast hb.1
  have h1 : ((imgBox sw fx fy b).2.1 : ℝ) ≤ x0 + 7287/10000 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb.2.1; push_cast at h; exact h
  have h2 : ((imgBox sw fx fy b).2.2.2 : ℝ) ≤ 1387/1000 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb.2.2; push_cast at h; exact h
  exact side_capacity x0 (act sw fx fy p) (act sw fx fy q) _ _ _ _
    (dir_unit sw fx fy u hu) (dir_unit sw fx fy v hv)
    (fun z hz => (hps hz).2.2.1) (fun z hz => (hqs hz).2.2.1)
    ⟨h0.trans hpb.1, hpb.2.1.trans h1⟩ ⟨h0.trans hqb.1, hqb.2.1.trans h1⟩
    (hpb.2.2.2.trans h2) (hqb.2.2.2.trans h2) hd'

theorem wall_cell_capacity (i : Fin 16) (p q u v : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1) (hpf : FitsU p u) (hqf : FitsU q v)
    (hp : p ∈ cell ⟨i.val, by omega⟩) (hq : q ∈ cell ⟨i.val, by omega⟩) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2)) := by
  have hc := wall_checked i
  have hpb := cell_inBox _ p hp
  have hqb := cell_inBox _ q hq
  unfold wallCheck at hc
  split_ifs at hc with h4
  · exact corner_via _ _ _ _ (of_decide_eq_true hc) p q u v hu hv hpf hqf hpb hqb
  · exact side_via _ _ _ _ _ (of_decide_eq_true hc) p q u v hu hv hpf hqf hpb hqb

/-! ## Interior cells -/

def diamCheck (vs : List (ℚ × ℚ)) : Bool :=
  vs.all (fun p => vs.all (fun q => decide ((p.1-q.1)^2+(p.2-q.2)^2 ≤ (15488/15625 : ℚ))))

theorem interior_diam_checked : ∀ i : Fin 9, diamCheck (vertices ⟨16+i.val, by omega⟩) = true := by
  decide +kernel

theorem interior_cell_capacity (i : Fin 9) (p q u v : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hp : p ∈ cell ⟨16+i.val, by omega⟩) (hq : q ∈ cell ⟨16+i.val, by omega⟩) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2)) := by
  apply not_disjoint_of_distSq_lt_one p q u.1 u.2 v.1 v.2 hu hv
  have h : distSq p q ≤ 15488/15625 := by
    apply hull_distSq_le _ _ ?_ hp hq
    rintro _ ⟨a,ha,rfl⟩ _ ⟨b,hb,rfl⟩
    have hc := interior_diam_checked i
    simp only [diamCheck, List.all_eq_true, decide_eq_true_eq] at hc
    have h := hc a ha b hb
    dsimp [distSq, realPoint]
    have hr := (Rat.cast_le (K := ℝ)).mpr h
    norm_num only [Rat.cast_add, Rat.cast_sub, Rat.cast_pow, Rat.cast_div, Rat.cast_ofNat] at hr
    exact hr
  linarith

/-! ## All cells -/

/-- **Capacity one.** Two unit squares inside `[0, U]^2` with centres in the same cell do not
have disjoint interiors. -/
theorem cell_capacity_one (i : Fin 25) (p q u v : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hpfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox (2443/500))
    (hqfit : Sq17.sq q.1 q.2 v.1 v.2 ⊆ containerBox (2443/500))
    (hp : p ∈ cell i) (hq : q ∈ cell i) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2)) := by
  by_cases hi : i.val < 16
  · have he : i = ⟨(⟨i.val, hi⟩ : Fin 16).val, by omega⟩ := rfl
    rw [he] at hp hq
    exact wall_cell_capacity ⟨i.val, hi⟩ p q u v hu hv (fitsU_of_subset p u hu hpfit)
      (fitsU_of_subset q v hv hqfit) hp hq
  · have he : i = ⟨16+(⟨i.val-16, by omega⟩ : Fin 9).val, by omega⟩ := by
      apply Fin.ext; simp; omega
    rw [he] at hp hq
    exact interior_cell_capacity _ p q u v hu hv hp hq

end Sq19.Cover

#print axioms Sq19.Cover.bbox_checked
#print axioms Sq19.Cover.wall_checked
#print axioms Sq19.Cover.interior_diam_checked
#print axioms Sq19.Cover.cell_capacity_one
