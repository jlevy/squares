import Sq19Lean.Capture.ToHull

/-! The step into `Hull.prob` for a region whose targets are H through the anti-diagonal mirror (state 3435,
piece P0, `g = 5`). The family in `[a, a + L]^2` is translated by `-(a, a)` and reflected by
`R z = (L - z.2, L - z.1)`, which maps the square at angle `φ` to the square at angle `-φ`. The reflected
positions are `(L + a - y, L + a - x)`: two wall contacts bound `L + a` (`a <= A` from a square at the left wall,
`L + a >= Dlo` from a square at the top wall, `L + a <= Dhi` from `L <= side`), and a finite check places every
target, so moved, in its box of `Hull.prob`. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneInt
open Sq17.Propagation.HalfPlaneState.CaptureSummary Sq19.Milp

def rflL (L : ℝ) (z : ℝ × ℝ) : ℝ × ℝ := (L - z.2, L - z.1)

theorem rflL_invol (L : ℝ) (z : ℝ × ℝ) : rflL L (rflL L z) = z := by
  simp [rflL]

noncomputable def rflHomeo (L : ℝ) : (ℝ × ℝ) ≃ₜ (ℝ × ℝ) where
  toFun := rflL L
  invFun := rflL L
  left_inv := rflL_invol L
  right_inv := rflL_invol L
  continuous_toFun := by unfold rflL; fun_prop
  continuous_invFun := by unfold rflL; fun_prop

theorem rflL_sq (L cx cy φ : ℝ) :
    rflL L '' Sq17.sq cx cy (Real.cos φ) (Real.sin φ) =
      Sq17.sq (L - cy) (L - cx) (Real.cos (-φ)) (Real.sin (-φ)) := by
  ext z
  constructor
  · rintro ⟨w, hw, rfl⟩
    obtain ⟨h1, h2⟩ := hw
    simp only [Real.cos_neg, Real.sin_neg, rflL]
    constructor
    · have e : (L - w.2 - (L - cy)) * Real.cos φ + (L - w.1 - (L - cx)) * -Real.sin φ =
          -((w.2 - cy) * Real.cos φ - (w.1 - cx) * Real.sin φ) := by ring
      rw [e, abs_neg]; exact h2
    · have e : (L - w.1 - (L - cx)) * Real.cos φ - (L - w.2 - (L - cy)) * -Real.sin φ =
          -((w.1 - cx) * Real.cos φ + (w.2 - cy) * Real.sin φ) := by ring
      rw [e, abs_neg]; exact h1
  · intro hz
    refine ⟨rflL L z, ?_, rflL_invol L z⟩
    obtain ⟨h1, h2⟩ := hz
    simp only [Real.cos_neg, Real.sin_neg] at h1 h2
    simp only [rflL]
    constructor
    · have e : (L - z.2 - cx) * Real.cos φ + (L - z.1 - cy) * Real.sin φ =
          -((z.2 - (L - cx)) * Real.cos φ - (z.1 - (L - cy)) * -Real.sin φ) := by ring
      rw [e, abs_neg]; exact h2
    · have e : (L - z.1 - cy) * Real.cos φ - (L - z.2 - cx) * Real.sin φ =
          -((z.1 - (L - cy)) * Real.cos φ + (z.2 - (L - cx)) * -Real.sin φ) := by ring
      rw [e, abs_neg]; exact h1

theorem edge_top_mem (c : ℝ × ℝ) (φ : ℝ) :
    (c.1 - Real.sin φ / 2, c.2 + Real.cos φ / 2) ∈ Sq17.sq c.1 c.2 (Real.cos φ) (Real.sin φ) := by
  have h := Real.sin_sq_add_cos_sq φ
  constructor
  · have : (c.1 - Real.sin φ / 2 - c.1) * Real.cos φ + (c.2 + Real.cos φ / 2 - c.2) * Real.sin φ = 0 := by ring
    rw [this]; norm_num
  · have : (c.2 + Real.cos φ / 2 - c.2) * Real.cos φ - (c.1 - Real.sin φ / 2 - c.1) * Real.sin φ = 1/2 := by
      nlinarith
    rw [this]; norm_num

/-- Mirrored finite check for one square: angle `-φ + kπ/2 - mπ/4`, position `(D - y - rx, D - x - ry)`, `D ∈ [Dlo, Dhi]`. -/
def sqCheckM (t : Target) (k : ℕ) (q : Sq) (Dlo Dhi : ℚ) : Bool :=
  decide (q.a.lo ≤ -t.hi + k * piLo / 2 - q.m * piHi / 4 ∧ -t.lo + k * piHi / 2 - q.m * piLo / 4 ≤ q.a.hi) &&
  impliedOK t.cons (leY (Dlo - q.rx - q.x.lo)) && impliedOK t.cons (geY (Dhi - q.rx - q.x.hi)) &&
  impliedOK t.cons (leX (Dlo - q.ry - q.y.lo)) && impliedOK t.cons (geX (Dhi - q.ry - q.y.hi))

/-- Top-wall check: the owner's centre has `y ≥ Y0` and angle in `[-Φ, Φ]`, so `L + a ≥ Dlo`. -/
def topCheck (t : Target) (Y0 Φ Dlo : ℚ) : Bool :=
  impliedOK t.cons (geY Y0) && decide (-Φ ≤ t.lo ∧ t.hi ≤ Φ ∧ 0 ≤ Φ ∧ Dlo ≤ Y0 + 1/2 - Φ ^ 2 / 4)

theorem good_of_targets_mirror (targets : Array Target) (own : Fin 9 → ℕ) (kq : Fin 9 → ℕ)
    (A Xw Φ Y0 Φ2 Dlo Dhi : ℚ) (ow ot : ℕ) (hown : ∀ i, own i < 19) (hinj : Function.Injective own)
    (how : ow < 19) (hot : ot < 19)
    (hsq : ∀ i, sqCheckM targets[own i]! (kq i) (Endgame.Hull.prob.sq i) Dlo Dhi = true)
    (hwall : wallCheck targets[ow]! Xw Φ A = true) (htop : topCheck targets[ot]! Y0 Φ2 Dlo = true)
    (L a : ℝ) (hD : L + (A : ℝ) ≤ Dhi) (p : ℕ → AnglePose)
    (hp : ∀ i : Fin 19, (targets[i.val]!).Holds (p i.val))
    (hbox : ∀ j : Fin 19, (p j.val).square ⊆ boxA a L)
    (hdis : ∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  have hpo : ∀ i : Fin 9, (targets[own i]!).Holds (p (own i)) := fun i => hp ⟨own i, hown i⟩
  -- a ≤ A (left wall)
  have haA : a ≤ (A : ℝ) := by
    obtain ⟨h1, h2⟩ := Bool.and_eq_true_iff.mp hwall
    obtain ⟨hl, hh, h0, hA⟩ := of_decide_eq_true h2
    have hpw := hp ⟨ow, how⟩
    have hx := leX_holds _ _ (impliedOK_sound _ _ h1 _ hpw.2)
    set φ := (p ow).angle
    have hφ1 : (-(Φ:ℝ)) ≤ φ := le_trans (by exact_mod_cast hl) hpw.1.1
    have hφ2 : φ ≤ (Φ:ℝ) := le_trans hpw.1.2 (by exact_mod_cast hh)
    have hcos := Real.one_sub_sq_div_two_le_cos (x := φ)
    have hm := hbox ⟨ow, how⟩ (edge_mid_mem (p ow).center φ)
    have hA' : ((Xw - 1/2 + Φ ^ 2 / 4 : ℚ) : ℝ) ≤ (A : ℝ) := by exact_mod_cast hA
    push_cast at hA'
    have hsq2 : φ ^ 2 ≤ (Φ:ℝ) ^ 2 := by nlinarith
    exact le_trans hm.1 (by nlinarith [hm.1])
  -- L + a ≥ Dlo (top wall)
  have hDlo : (Dlo : ℝ) ≤ L + a := by
    obtain ⟨h1, h2⟩ := Bool.and_eq_true_iff.mp htop
    obtain ⟨hl, hh, h0, hD⟩ := of_decide_eq_true h2
    have hpt := hp ⟨ot, hot⟩
    have hy := geY_holds _ _ (impliedOK_sound _ _ h1 _ hpt.2)
    set φ := (p ot).angle
    have hφ1 : (-(Φ2:ℝ)) ≤ φ := le_trans (by exact_mod_cast hl) hpt.1.1
    have hφ2 : φ ≤ (Φ2:ℝ) := le_trans hpt.1.2 (by exact_mod_cast hh)
    have hcos := Real.one_sub_sq_div_two_le_cos (x := φ)
    have hm := hbox ⟨ot, hot⟩ (edge_top_mem (p ot).center φ)
    have hD' : (Dlo : ℝ) ≤ ((Y0 + 1/2 - Φ2 ^ 2 / 4 : ℚ) : ℝ) := by exact_mod_cast hD
    push_cast at hD'
    have hsq2 : φ ^ 2 ≤ (Φ2:ℝ) ^ 2 := by nlinarith
    have := hm.2.2.2
    nlinarith
  have hDhi : L + a ≤ (Dhi : ℝ) := by linarith
  let θ : ℕ → ℝ := fun k => match hullIdx k with
    | some i => -(p (own i)).angle + kq i * (Real.pi / 2) - (Endgame.Hull.prob.sq i).m * Real.pi / 4
    | none => 0
  let dx : ℕ → ℝ := fun k => match hullIdx k with
    | some i => L + a - (p (own i)).center.2 - (Endgame.Hull.prob.sq i).rx
    | none => 0
  let dy : ℕ → ℝ := fun k => match hullIdx k with
    | some i => L + a - (p (own i)).center.1 - (Endgame.Hull.prob.sq i).ry
    | none => 0
  have hθ : ∀ i : Fin 9, θ (Endgame.Hull.prob.sq i).s =
      -(p (own i)).angle + kq i * (Real.pi / 2) - (Endgame.Hull.prob.sq i).m * Real.pi / 4 := by
    intro i; simp only [θ, hullIdx_s]
  have hdx : ∀ i : Fin 9, dx (Endgame.Hull.prob.sq i).s = L + a - (p (own i)).center.2 - (Endgame.Hull.prob.sq i).rx := by
    intro i; simp only [dx, hullIdx_s]
  have hdy : ∀ i : Fin 9, dy (Endgame.Hull.prob.sq i).s = L + a - (p (own i)).center.1 - (Endgame.Hull.prob.sq i).ry := by
    intro i; simp only [dy, hullIdx_s]
  have hsqr : ∀ i : Fin 9, Sq17.sq (cenOf dx dy (Endgame.Hull.prob.sq i)).1 (cenOf dx dy (Endgame.Hull.prob.sq i)).2
      (Real.cos (angOf θ (Endgame.Hull.prob.sq i))) (Real.sin (angOf θ (Endgame.Hull.prob.sq i))) =
      rflL L '' ((fun z => z + (-a, -a)) '' (p (own i)).square) := by
    intro i
    have ha : angOf θ (Endgame.Hull.prob.sq i) = -(p (own i)).angle + kq i * (Real.pi / 2) := by
      simp only [angOf, hθ]; ring
    rw [ha, sq_turns]
    simp only [AnglePose.square]
    rw [← sq_translate, rflL_sq]
    simp only [cenOf, hdx, hdy, Prod.fst_add, Prod.snd_add]
    congr 1 <;> ring
  refine ⟨θ, dx, dy, ⟨?_, ?_, ?_, ?_⟩⟩
  · intro k
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
      have hlo' : (((Endgame.Hull.prob.sq i).a.lo : ℚ) : ℝ) ≤ ((-targets[own i]!.hi + kq i * piLo / 2 -
          (Endgame.Hull.prob.sq i).m * piHi / 4 : ℚ) : ℝ) := by exact_mod_cast hlo
      have hhi' : ((-targets[own i]!.lo + kq i * piHi / 2 - (Endgame.Hull.prob.sq i).m * piLo / 4 : ℚ) : ℝ) ≤
          (((Endgame.Hull.prob.sq i).a.hi : ℚ) : ℝ) := by exact_mod_cast hhi
      push_cast at hlo' hhi'
      have hk0 : (0 : ℝ) ≤ kq i := by positivity
      have hm0 : (0 : ℝ) ≤ (Endgame.Hull.prob.sq i).m := by positivity
      constructor <;> nlinarith [ht.1, ht.2]
  · intro q hq
    obtain ⟨i, rfl⟩ := sq_of_mem hq
    have hc := fun (c : IC) (h : impliedOK (targets[own i]!).cons c = true) => impliedOK_sound _ c h _ (hpo i).2
    simp only [sqCheckM, Bool.and_eq_true] at hsq
    obtain ⟨⟨⟨⟨-, h2⟩, h3⟩, h4⟩, h5⟩ := hsq i
    have y1 := leY_holds _ _ (hc _ h2); have y2 := geY_holds _ _ (hc _ h3)
    have x1 := leX_holds _ _ (hc _ h4); have x2 := geX_holds _ _ (hc _ h5)
    push_cast at x1 x2 y1 y2
    refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩⟩ <;> simp only [hdx, hdy] <;> linarith
  · intro q hq
    obtain ⟨i, rfl⟩ := sq_of_mem hq
    rw [hsqr i]
    rintro _ ⟨_, ⟨z, hz, rfl⟩, rfl⟩
    obtain ⟨h1, h2, h3, h4⟩ := hbox ⟨own i, hown i⟩ hz
    simp only [rflL, Prod.fst_add, Prod.snd_add]
    exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  · intro i j hi hj hij
    rw [hull_len] at hi hj
    have e1 := hsqr ⟨i, hi⟩; have e2 := hsqr ⟨j, hj⟩
    simp only at e1 e2
    rw [e1, e2]
    have hR : ∀ S : Set (ℝ × ℝ), rflL L '' interior S = interior (rflL L '' S) :=
      fun S => (rflHomeo L).image_interior S
    rw [← hR, ← hR]
    apply (Set.disjoint_image_iff (rflHomeo L).injective).mpr
    apply translate_disjoint
    exact hdis ⟨own ⟨i, hi⟩, hown _⟩ ⟨own ⟨j, hj⟩, hown _⟩
      (fun he => hij (by simpa using congrArg Fin.val (hinj (by simpa using congrArg Fin.val he))))

end Sq19.Capture

#print axioms Sq19.Capture.good_of_targets_mirror
