import Sq19Lean.Capture.CensusLink
import Sq19Lean.Endgame.HullData

/-! From captured poses to the local hull `Hull.prob` (Codex's `Good`, Sq19Lean/Milp/SoundRows.lean).

Input: poses `p` of 19 unit squares in a box `[a, a + L]^2`, pairwise disjoint, each owner in its capture target
(`targets`, the state's frame and owner order, `g = 0`). For every square of `Hull.prob` (record squares 1, 2, 5,
7, 8, 10, 11, 13, 14) a map gives its owner and a number of quarter turns. Output: `θ dx dy` with
`Good Hull.prob θ dx dy L`, for the family translated by `-(a, a)` into `[0, L]^2`.

The offset `a` is bounded above by wall contact: the owner of record square 1 has its centre at `x <= Xw` and angle
in `[-Φ, Φ]`; the midpoint `c - u/2` of its left edge lies in its square, so `a <= Xw - cos Φ / 2 <=
Xw - 1/2 + Φ^2/4 <= A`. Below, `a >= Amin` is a hypothesis (it comes from `L <= side`). The rest is a finite check:
each target, moved by any shift in `[-A, -Amin]`, lies in the matching box of `Hull.prob`. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneInt
open Sq17.Propagation.HalfPlaneState.CaptureSummary Sq19.Milp

def piLo : ℚ := 314159265358979323846 / 100000000000000000000 - 1 / 10 ^ 20
def piHi : ℚ := 314159265358979323847 / 100000000000000000000

theorem pi_lo : (piLo : ℝ) ≤ Real.pi := by
  have := Real.pi_gt_d20; simp only [piLo]; push_cast; linarith
theorem pi_hi : Real.pi ≤ (piHi : ℝ) := by
  have := Real.pi_lt_d20; simp only [piHi]; push_cast; linarith

/-- Half-planes `x ≥ r`, `x ≤ r`, `y ≥ r`, `y ≤ r` with integer coefficients. -/
def geX (r : ℚ) : IC := ⟨-(r.den : ℤ), 0, -r.num⟩
def leX (r : ℚ) : IC := ⟨(r.den : ℤ), 0, r.num⟩
def geY (r : ℚ) : IC := ⟨0, -(r.den : ℤ), -r.num⟩
def leY (r : ℚ) : IC := ⟨0, (r.den : ℤ), r.num⟩

theorem rat_eq (r : ℚ) : (r : ℝ) = (r.num : ℝ) / (r.den : ℝ) := by
  rw [← Rat.cast_intCast, ← Rat.cast_natCast, ← Rat.cast_div, Rat.num_div_den]

theorem den_pos (r : ℚ) : (0 : ℝ) < r.den := by exact_mod_cast r.den_pos

theorem geX_holds (r : ℚ) (z : ℝ × ℝ) (h : (geX r).Holds z) : (r : ℝ) ≤ z.1 := by
  simp only [geX, IC.Holds] at h; push_cast at h
  rw [rat_eq, div_le_iff₀ (den_pos r)]; linarith
theorem leX_holds (r : ℚ) (z : ℝ × ℝ) (h : (leX r).Holds z) : z.1 ≤ (r : ℝ) := by
  simp only [leX, IC.Holds] at h; push_cast at h
  rw [rat_eq, le_div_iff₀ (den_pos r)]; linarith
theorem geY_holds (r : ℚ) (z : ℝ × ℝ) (h : (geY r).Holds z) : (r : ℝ) ≤ z.2 := by
  simp only [geY, IC.Holds] at h; push_cast at h
  rw [rat_eq, div_le_iff₀ (den_pos r)]; linarith
theorem leY_holds (r : ℚ) (z : ℝ × ℝ) (h : (leY r).Holds z) : z.2 ≤ (r : ℝ) := by
  simp only [leY, IC.Holds] at h; push_cast at h
  rw [rat_eq, le_div_iff₀ (den_pos r)]; linarith

/-- The finite check for one square `q` of `Hull.prob` with owner target `t` and `k` quarter turns. -/
def sqCheck (t : Target) (k : ℕ) (q : Sq) (A Amin : ℚ) : Bool :=
  decide (q.a.lo ≤ t.lo + k * piLo / 2 - q.m * piHi / 4 ∧ t.hi + k * piHi / 2 - q.m * piLo / 4 ≤ q.a.hi) &&
  impliedOK t.cons (geX (q.rx + q.x.lo + A)) && impliedOK t.cons (leX (q.rx + q.x.hi + Amin)) &&
  impliedOK t.cons (geY (q.ry + q.y.lo + A)) && impliedOK t.cons (leY (q.ry + q.y.hi + Amin))

/-- The wall check on the owner `t` of record square 1. -/
def wallCheck (t : Target) (Xw Φ A : ℚ) : Bool :=
  impliedOK t.cons (leX Xw) && decide (-Φ ≤ t.lo ∧ t.hi ≤ Φ ∧ 0 ≤ Φ ∧ Xw - 1/2 + Φ ^ 2 / 4 ≤ A)

/-- Index in `Hull.prob` of each record square number. -/
def hullIdx : ℕ → Option (Fin 9)
  | 1 => some 0 | 2 => some 1 | 5 => some 2 | 7 => some 3 | 8 => some 4
  | 10 => some 5 | 11 => some 6 | 13 => some 7 | 14 => some 8 | _ => none

theorem hull_len : Endgame.Hull.prob.n = 9 := rfl

theorem hullIdx_s : ∀ i : Fin 9, hullIdx (Endgame.Hull.prob.sq i).s = some i := by decide

theorem hullIdx_some {k : ℕ} {i : Fin 9} (h : hullIdx k = some i) : (Endgame.Hull.prob.sq i).s = k := by
  unfold hullIdx at h; split at h <;> simp_all <;> subst h <;> rfl

theorem rootAng_idx {k : ℕ} {i : Fin 9} (h : hullIdx k = some i) :
    Endgame.Hull.prob.rootAng k = (Endgame.Hull.prob.sq i).a := by
  have hk := hullIdx_some h; subst hk
  fin_cases i <;> rfl

theorem rootAng_none {k : ℕ} (h : hullIdx k = none) : Endgame.Hull.prob.rootAng k = Iv.pt 0 := by
  unfold Prob.rootAng
  rw [List.find?_eq_none.mpr]
  intro q hq
  simp only [Endgame.Hull.prob, List.mem_cons, List.not_mem_nil, or_false] at hq
  rcases hq with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp only [decide_eq_true_eq] <;> intro e <;> subst e <;> simp [hullIdx] at h

theorem sq_of_mem {q : Sq} (hq : q ∈ Endgame.Hull.prob.sqs) : ∃ i : Fin 9, Endgame.Hull.prob.sq i = q := by
  obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp hq
  refine ⟨⟨i, hi⟩, ?_⟩
  simp [Prob.sq, List.getD_eq_getElem?_getD, hi]

theorem edge_mid_mem (c : ℝ × ℝ) (φ : ℝ) :
    (c.1 - Real.cos φ / 2, c.2 - Real.sin φ / 2) ∈ Sq17.sq c.1 c.2 (Real.cos φ) (Real.sin φ) := by
  have h := Real.sin_sq_add_cos_sq φ
  constructor
  · have : (c.1 - Real.cos φ / 2 - c.1) * Real.cos φ + (c.2 - Real.sin φ / 2 - c.2) * Real.sin φ = -1/2 := by
      nlinarith
    rw [this]; norm_num
  · have : (c.2 - Real.sin φ / 2 - c.2) * Real.cos φ - (c.1 - Real.cos φ / 2 - c.1) * Real.sin φ = 0 := by ring
    rw [this]; norm_num

theorem sq_turns (cx cy φ : ℝ) (k : ℕ) :
    Sq17.sq cx cy (Real.cos (φ + k * (Real.pi / 2))) (Real.sin (φ + k * (Real.pi / 2))) =
      Sq17.sq cx cy (Real.cos φ) (Real.sin φ) := by
  induction k with
  | zero => simp
  | succ k ih =>
    have e : φ + ((k + 1 : ℕ) : ℝ) * (Real.pi / 2) = (φ + (k : ℝ) * (Real.pi / 2)) + Real.pi / 2 := by
      push_cast; ring
    rw [e, square_angle_quarter_turn, ih]

/-- Captured poses give a `Good Hull.prob` configuration. -/
theorem good_of_targets (targets : Array Target) (own : Fin 9 → ℕ) (kq : Fin 9 → ℕ) (A Amin Xw Φ : ℚ)
    (hown : ∀ i, own i < 19) (hinj : Function.Injective own) (hw : own 0 = own 0)
    (hsq : ∀ i, sqCheck targets[own i]! (kq i) (Endgame.Hull.prob.sq i) A Amin = true)
    (hwall : wallCheck targets[own 0]! Xw Φ A = true) (hk0 : kq 0 = 0)
    (L a : ℝ) (ha : (Amin : ℝ) ≤ a) (p : ℕ → AnglePose)
    (hp : ∀ i : Fin 19, (targets[i.val]!).Holds (p i.val))
    (hbox : ∀ j : Fin 19, (p j.val).square ⊆ boxA a L)
    (hdis : ∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  have hpo : ∀ i : Fin 9, (targets[own i]!).Holds (p (own i)) := fun i => hp ⟨own i, hown i⟩
  -- wall contact: a ≤ A
  have haA : a ≤ (A : ℝ) := by
    obtain ⟨h1, h2⟩ := Bool.and_eq_true_iff.mp hwall
    obtain ⟨hl, hh, h0, hA⟩ := of_decide_eq_true h2
    have hx := leX_holds _ _ (impliedOK_sound _ _ h1 _ (hpo 0).2)
    have hang := (hpo 0).1
    set φ := (p (own 0)).angle
    have hφ1 : (-(Φ:ℝ)) ≤ φ := le_trans (by exact_mod_cast hl) hang.1
    have hφ2 : φ ≤ (Φ:ℝ) := le_trans hang.2 (by exact_mod_cast hh)
    have hcos := Real.one_sub_sq_div_two_le_cos (x := φ)
    have hm := hbox ⟨own 0, hown 0⟩ (edge_mid_mem (p (own 0)).center φ)
    have hA' : ((Xw - 1/2 + Φ ^ 2 / 4 : ℚ) : ℝ) ≤ (A : ℝ) := by exact_mod_cast hA
    push_cast at hA'
    have hsq2 : φ ^ 2 ≤ (Φ:ℝ) ^ 2 := by nlinarith
    exact le_trans hm.1 (by nlinarith [hm.1])
  let θ : ℕ → ℝ := fun k => match hullIdx k with
    | some i => (p (own i)).angle + kq i * (Real.pi / 2) - (Endgame.Hull.prob.sq i).m * Real.pi / 4
    | none => 0
  let dx : ℕ → ℝ := fun k => match hullIdx k with
    | some i => (p (own i)).center.1 - a - (Endgame.Hull.prob.sq i).rx
    | none => 0
  let dy : ℕ → ℝ := fun k => match hullIdx k with
    | some i => (p (own i)).center.2 - a - (Endgame.Hull.prob.sq i).ry
    | none => 0
  have hθ : ∀ i : Fin 9, θ (Endgame.Hull.prob.sq i).s =
      (p (own i)).angle + kq i * (Real.pi / 2) - (Endgame.Hull.prob.sq i).m * Real.pi / 4 := by
    intro i; simp only [θ, hullIdx_s]
  have hdx : ∀ i : Fin 9, dx (Endgame.Hull.prob.sq i).s = (p (own i)).center.1 - a - (Endgame.Hull.prob.sq i).rx := by
    intro i; simp only [dx, hullIdx_s]
  have hdy : ∀ i : Fin 9, dy (Endgame.Hull.prob.sq i).s = (p (own i)).center.2 - a - (Endgame.Hull.prob.sq i).ry := by
    intro i; simp only [dy, hullIdx_s]
  -- each square of the configuration is the translate of the captured square
  have hcen : ∀ i : Fin 9, cenOf dx dy (Endgame.Hull.prob.sq i) = (p (own i)).center + (-a, -a) := by
    intro i; simp only [cenOf, hdx, hdy]; ext <;> simp <;> ring
  have hang : ∀ i : Fin 9, angOf θ (Endgame.Hull.prob.sq i) = (p (own i)).angle + kq i * (Real.pi / 2) := by
    intro i; simp only [angOf, hθ]; ring
  have hsqr : ∀ i : Fin 9, Sq17.sq (cenOf dx dy (Endgame.Hull.prob.sq i)).1 (cenOf dx dy (Endgame.Hull.prob.sq i)).2
      (Real.cos (angOf θ (Endgame.Hull.prob.sq i))) (Real.sin (angOf θ (Endgame.Hull.prob.sq i))) =
      (fun z => z + (-a, -a)) '' (p (own i)).square := by
    intro i
    rw [hang, sq_turns, hcen]
    simp only [AnglePose.square, Prod.fst_add, Prod.snd_add]
    exact sq_translate _ _ _ _ _ _
  refine ⟨θ, dx, dy, ⟨?_, ?_, ?_, ?_⟩⟩
  · -- angles
    intro k
    cases hk : hullIdx k with
    | none => rw [rootAng_none hk]; simp only [θ, hk]; simp [Iv.mem, Iv.pt]
    | some i =>
      rw [rootAng_idx hk]
      have hs := hullIdx_some hk; rw [← hs, hθ]
      obtain ⟨h1, -⟩ := Bool.and_eq_true_iff.mp (hsq i)
      obtain ⟨h1, -⟩ := Bool.and_eq_true_iff.mp h1
      obtain ⟨h1, -⟩ := Bool.and_eq_true_iff.mp h1
      obtain ⟨h1, -⟩ := Bool.and_eq_true_iff.mp h1
      obtain ⟨hlo, hhi⟩ := of_decide_eq_true h1
      have ht := (hpo i).1
      have hpl := pi_lo; have hph := pi_hi
      have hlo' : (((Endgame.Hull.prob.sq i).a.lo : ℚ) : ℝ) ≤ ((targets[own i]!.lo + kq i * piLo / 2 -
          (Endgame.Hull.prob.sq i).m * piHi / 4 : ℚ) : ℝ) := by exact_mod_cast hlo
      have hhi' : ((targets[own i]!.hi + kq i * piHi / 2 - (Endgame.Hull.prob.sq i).m * piLo / 4 : ℚ) : ℝ) ≤
          (((Endgame.Hull.prob.sq i).a.hi : ℚ) : ℝ) := by exact_mod_cast hhi
      push_cast at hlo' hhi'
      have hk0 : (0 : ℝ) ≤ kq i := by positivity
      have hm0 : (0 : ℝ) ≤ (Endgame.Hull.prob.sq i).m := by positivity
      constructor <;> nlinarith [ht.1, ht.2]
  · -- positions
    intro q hq
    obtain ⟨i, rfl⟩ := sq_of_mem hq
    have hc := fun (c : IC) (h : impliedOK (targets[own i]!).cons c = true) => impliedOK_sound _ c h _ (hpo i).2
    simp only [sqCheck, Bool.and_eq_true] at hsq
    obtain ⟨⟨⟨⟨-, h2⟩, h3⟩, h4⟩, h5⟩ := hsq i
    have x1 := geX_holds _ _ (hc _ h2); have x2 := leX_holds _ _ (hc _ h3)
    have y1 := geY_holds _ _ (hc _ h4); have y2 := leY_holds _ _ (hc _ h5)
    push_cast at x1 x2 y1 y2
    refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩⟩ <;> simp only [hdx, hdy] <;> linarith
  · -- fit
    intro q hq
    obtain ⟨i, rfl⟩ := sq_of_mem hq
    rw [hsqr i]
    rintro _ ⟨z, hz, rfl⟩
    obtain ⟨h1, h2, h3, h4⟩ := hbox ⟨own i, hown i⟩ hz
    exact ⟨by simp; linarith, by simp; linarith, by simp; linarith, by simp; linarith⟩
  · -- disjoint
    intro i j hi hj hij
    rw [hull_len] at hi hj
    have e1 := hsqr ⟨i, hi⟩; have e2 := hsqr ⟨j, hj⟩
    simp only at e1 e2
    rw [e1, e2]
    apply translate_disjoint
    exact hdis ⟨own ⟨i, hi⟩, hown _⟩ ⟨own ⟨j, hj⟩, hown _⟩
      (fun he => hij (by simpa using congrArg Fin.val (hinj (by simpa using congrArg Fin.val he))))

end Sq19.Capture

#print axioms Sq19.Capture.good_of_targets
