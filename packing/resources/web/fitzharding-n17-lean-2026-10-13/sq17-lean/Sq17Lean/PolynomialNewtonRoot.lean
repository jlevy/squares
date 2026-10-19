import Sq17Lean.PolynomialBoxContraction

namespace Sq17.PolynomialBox

/-- A nonsingular rational preconditioner introduces no spurious fixed points. -/
theorem linear_zero_iff (a b c d f g : ℝ) (hdet : a*d-b*c ≠ 0) :
    (a*f+b*g=0 ∧ c*f+d*g=0) ↔ (f=0 ∧ g=0) := by
  constructor
  · intro h
    have hf : (a*d-b*c)*f=0 := by linear_combination d*h.1-b*h.2
    have hg : (a*d-b*c)*g=0 := by linear_combination a*h.2-c*h.1
    exact ⟨(mul_eq_zero.mp hf).resolve_left hdet,(mul_eq_zero.mp hg).resolve_left hdet⟩
  · rintro ⟨rfl,rfl⟩; constructor <;> ring

def rootBox (m : ℝ × ℝ) (r : ℝ) : Set (ℝ × ℝ) :=
  {p | |p.1-m.1| ≤ r ∧ |p.2-m.2| ≤ r}

/-- Normalized finite coefficient certificates imply existence and uniqueness
of a simultaneous polynomial root in the original closed rational box. -/
theorem newton_unique_root (f g n0 n1 : List Term) (m : ℝ × ℝ) (r a b c d : ℝ)
    (hr : 0 < r) (hdet : a*d-b*c ≠ 0) (hc : check n0 n1 = true)
    (h0 : ∀ p : ℝ × ℝ, eval n0 p = p.1-
      (a*eval f (m.1+r*p.1,m.2+r*p.2)+b*eval g (m.1+r*p.1,m.2+r*p.2))/r)
    (h1 : ∀ p : ℝ × ℝ, eval n1 p = p.2-
      (c*eval f (m.1+r*p.1,m.2+r*p.2)+d*eval g (m.1+r*p.1,m.2+r*p.2))/r) :
    ∃! z : ℝ × ℝ, z ∈ rootBox m r ∧ eval f z=0 ∧ eval g z=0 := by
  let T : (ℝ × ℝ) → ℝ × ℝ := fun p => (m.1+r*p.1,m.2+r*p.2)
  let U : (ℝ × ℝ) → ℝ × ℝ := fun z => ((z.1-m.1)/r,(z.2-m.2)/r)
  have hTU (z : ℝ × ℝ) : T (U z) = z := by
    ext <;> dsimp [T,U] <;> field_simp [ne_of_gt hr] <;> ring
  have hUT (p : ℝ × ℝ) : U (T p) = p := by
    ext <;> dsimp [T,U] <;> field_simp [ne_of_gt hr] <;> ring
  have hbox (p : ℝ × ℝ) : T p ∈ rootBox m r ↔ p ∈ box := by
    simp only [rootBox,box,T,Set.mem_ofPred_eq,add_sub_cancel_left,abs_mul,abs_of_pos hr]
    constructor
    · intro h; constructor <;> nlinarith [h.1,h.2]
    · intro h; constructor <;> nlinarith [h.1,h.2]
  have hfix (p : ℝ × ℝ) : (eval n0 p,eval n1 p)=p ↔ eval f (T p)=0 ∧ eval g (T p)=0 := by
    rw [Prod.ext_iff,h0,h1]
    have hlin := linear_zero_iff a b c d (eval f (T p)) (eval g (T p)) hdet
    dsimp [T] at hlin
    rw [←hlin]
    constructor
    · intro h; constructor
      · have he : (a*eval f (m.1+r*p.1,m.2+r*p.2)+b*eval g (m.1+r*p.1,m.2+r*p.2))/r=0 := by linarith [h.1]
        exact (div_eq_zero_iff).mp he |>.resolve_right (ne_of_gt hr)
      · have he : (c*eval f (m.1+r*p.1,m.2+r*p.2)+d*eval g (m.1+r*p.1,m.2+r*p.2))/r=0 := by linarith [h.2]
        exact (div_eq_zero_iff).mp he |>.resolve_right (ne_of_gt hr)
    · intro h; simp [h.1,h.2]
  obtain ⟨p,hp,huniq⟩ := check_unique_fixed n0 n1 hc
  refine ⟨T p,⟨(hbox p).2 hp.1,(hfix p).1 hp.2⟩,?_⟩
  intro z hz
  have hzbox : U z ∈ box := (hbox (U z)).1 (by simpa only [hTU] using hz.1)
  have hzfix : (eval n0 (U z),eval n1 (U z))=U z :=
    (hfix (U z)).2 (by simpa only [hTU] using hz.2)
  have he := huniq (U z) ⟨hzbox,hzfix⟩
  simpa only [hTU] using congrArg T he

end Sq17.PolynomialBox
#print axioms Sq17.PolynomialBox.newton_unique_root
