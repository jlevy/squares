import Sq17Lean.PropagationCoreCheck
import Sq17Lean.PropagationRational

/-! Wall exclusion from a checked inner core. These certificates may be weaker
than the trace checker's angle-specific wall rule; coverage and translation of
actual wall records remain separate obligations. All comparisons are strict
on the excluded side, so legal boundary contact is preserved. -/
namespace Sq17.Propagation

def containerBox (L : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 ≤ p.1 ∧ p.1 ≤ L ∧ 0 ≤ p.2 ∧ p.2 ≤ L}

/-- Four corners of an inner core supply necessary bounds on its center.
No normalization or sign assumption on the rational core direction is needed. -/
theorem core_center_bounds (cx cy c s h L : ℝ)
    (hf : core cx cy c s h ⊆ containerBox L) :
    h*(c+s)/2 ≤ cx ∧ cx ≤ L-h*(c+s)/2 ∧
    h*(c+s)/2 ≤ cy ∧ cy ≤ L-h*(c+s)/2 := by
  have hl := hf (show corePoint cx cy c s h (-1) 1 ∈ core cx cy c s h from
    ⟨-1, 1, by norm_num, by norm_num, rfl⟩)
  have hr := hf (show corePoint cx cy c s h 1 (-1) ∈ core cx cy c s h from
    ⟨1, -1, by norm_num, by norm_num, rfl⟩)
  have hb := hf (show corePoint cx cy c s h (-1) (-1) ∈ core cx cy c s h from
    ⟨-1, -1, by norm_num, by norm_num, rfl⟩)
  have ht := hf (show corePoint cx cy c s h 1 1 ∈ core cx cy c s h from
    ⟨1, 1, by norm_num, by norm_num, rfl⟩)
  change 0 ≤ (corePoint cx cy c s h (-1) 1).1 ∧ _ at hl
  change _ ∧ (corePoint cx cy c s h 1 (-1)).1 ≤ L ∧ _ at hr
  change _ ∧ _ ∧ 0 ≤ (corePoint cx cy c s h (-1) (-1)).2 ∧ _ at hb
  change _ ∧ _ ∧ _ ∧ (corePoint cx cy c s h 1 1).2 ≤ L at ht
  dsimp [corePoint] at hl hr hb ht
  exact ⟨by linarith [hl.1], by linarith [hr.2.1],
    by linarith [hb.2.2.1], by linarith [ht.2.2.2]⟩

def rationalWallCheck (V : List (ℚ × ℚ)) (r : CoreRowCertificate)
    (L : ℚ) (n : ℕ) : Bool :=
  let d := r.side*(r.c+r.s)/2
  r.check n && (rationalHalfPlane V (-1) 0 (-d) ||
    rationalHalfPlane V 1 0 (L-d) ||
    rationalHalfPlane V 0 (-1) (-d) || rationalHalfPlane V 0 1 (L-d))

theorem rationalWallCheck_sound (V : List (ℚ × ℚ)) (r : CoreRowCertificate)
    (L : ℚ) (n : ℕ) (hc : rationalWallCheck V r L n = true)
    (x : ℝ × ℝ) (hx : x ∈ convexHull ℝ (realPoint '' {p | p ∈ V}))
    (θ : ℝ) (hθ : θ ∈ Set.Icc (r.lo : ℝ) (r.hi : ℝ)) :
    ¬ Sq17.sq x.1 x.2 (Real.cos θ) (Real.sin θ) ⊆ containerBox L := by
  intro hfit
  have hb := Bool.and_eq_true_iff.mp hc
  have bounds := core_center_bounds x.1 x.2 r.c r.s r.side L
    (Set.Subset.trans (r.check_sound n hb.1 x.1 x.2 θ hθ) hfit)
  have hw : rationalHalfPlane V (-1) 0 (-(r.side*(r.c+r.s)/2)) = true ∨
      rationalHalfPlane V 1 0 (L-r.side*(r.c+r.s)/2) = true ∨
      rationalHalfPlane V 0 (-1) (-(r.side*(r.c+r.s)/2)) = true ∨
      rationalHalfPlane V 0 1 (L-r.side*(r.c+r.s)/2) = true := by
    simpa only [Bool.or_eq_true, or_assoc] using hb.2
  rcases hw with hw | hw | hw | hw
  all_goals
    have hv := rationalHalfPlane_sound _ _ _ _ hw x hx
    push_cast at hv
    norm_num at hv
    linarith

end Sq17.Propagation

#print axioms Sq17.Propagation.core_center_bounds
#print axioms Sq17.Propagation.rationalWallCheck_sound
