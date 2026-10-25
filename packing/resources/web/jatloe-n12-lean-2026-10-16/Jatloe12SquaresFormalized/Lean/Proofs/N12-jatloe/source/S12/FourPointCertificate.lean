import S12.LinearCertificate
import S12.ShortCluster
import Mathlib.Algebra.BigOperators.Fin

namespace S12
open S12Pilot
set_option maxHeartbeats 0

def affine5 (c s u v a k : ℚ) : Affine 5 :=
  ⟨fun i => match i.val with | 0 => c | 1 => s | 2 => u | 3 => v | _ => a, k⟩
def squareEnv (q : OpenSquare) : Fin 5 → ℝ :=
  fun i => match i.val with | 0 => q.c | 1 => q.s | 2 => q.loU | 3 => q.loV | _ => q.side

theorem eval_affine5 (c s u v a k : ℚ) (q : OpenSquare) :
    (affine5 c s u v a k).eval (squareEnv q) =
    c*q.c+s*q.s+u*q.loU+v*q.loV+a*q.side+k := by
  simp [Affine.eval,affine5,squareEnv,Fin.sum_univ_succ]
  ring

def insideRows (p : ℚ × ℚ) : List (LinearConstraint 5) :=
  [⟨affine5 p.1 p.2 (-1) 0 0 0,true⟩,
   ⟨affine5 (-p.1) (-p.2) 1 0 1 0,true⟩,
   ⟨affine5 p.2 (-p.1) 0 (-1) 0 0,true⟩,
   ⟨affine5 (-p.2) p.1 0 1 1 0,true⟩]

def outsideRow (p : ℚ × ℚ) (face : Fin 4) : LinearConstraint 5 :=
  ⟨match face.val with
    | 0 => affine5 (-p.1) (-p.2) 1 0 0 0
    | 1 => affine5 p.1 p.2 (-1) 0 (-1) 0
    | 2 => affine5 (-p.2) p.1 0 1 0 0
    | _ => affine5 p.2 (-p.1) 0 (-1) (-1) 0, false⟩

def projectionRows (p e : ℚ × ℚ) : List (LinearConstraint 5) :=
  let dx := p.1-e.1
  let dy := p.2-e.2
  [⟨affine5 dx dy 0 0 0 1,false⟩,⟨affine5 (-dx) (-dy) 0 0 0 1,false⟩,
   ⟨affine5 dy (-dx) 0 0 0 1,false⟩,⟨affine5 (-dy) dx 0 0 0 1,false⟩]

def fourPointRows (a b p e : ℚ × ℚ) (f g : Fin 4) : List (LinearConstraint 5) :=
  [⟨affine5 0 0 0 0 0 1,true⟩,⟨affine5 0 0 0 0 1 (-1),true⟩] ++
  insideRows a ++ insideRows b ++ [outsideRow p f,outsideRow e g] ++ projectionRows p e

theorem inside_rows_hold (q : OpenSquare) (p : ℚ × ℚ) (h : q.Inside p.1 p.2) :
    ∀ r ∈ insideRows p, r.Holds (squareEnv q) := by
  obtain ⟨h0,h1,h2,h3⟩ := h
  intro r hr
  simp only [insideRows,List.mem_cons,List.not_mem_nil,or_false] at hr
  rcases hr with rfl | rfl | rfl | rfl <;>
    simp only [LinearConstraint.Holds,ite_true,eval_affine5] <;>
    push_cast <;> linarith

theorem outside_has_face (q : OpenSquare) (p : ℚ × ℚ) (h : ¬ q.Inside p.1 p.2) :
    ∃ f : Fin 4, (outsideRow p f).Holds (squareEnv q) := by
  simp only [OpenSquare.Inside,InBands,not_and_or,not_lt] at h
  rcases h with h | h | h | h
  · refine ⟨0,?_⟩
    simp [outsideRow,LinearConstraint.Holds,eval_affine5]
    linarith
  · refine ⟨1,?_⟩
    simp [outsideRow,LinearConstraint.Holds,eval_affine5]
    linarith
  · refine ⟨2,?_⟩
    simp [outsideRow,LinearConstraint.Holds,eval_affine5]
    linarith
  · refine ⟨3,?_⟩
    simp [outsideRow,LinearConstraint.Holds,eval_affine5]
    linarith

theorem projection_rows_hold (q : OpenSquare) (p e : ℚ × ℚ)
    (hd : distSq p e ≤ 1) : ∀ r ∈ projectionRows p e, r.Holds (squareEnv q) := by
  have hd' : ((p.1 : ℝ)-e.1)^2+((p.2 : ℝ)-e.2)^2 ≤ 1 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hd
    simpa [distSq, pow_two, Rat.cast_mul, Rat.cast_sub] using h
  obtain ⟨h0,h1,h2,h3⟩ := short_projections q _ _ hd'
  intro r hr
  simp only [projectionRows,List.mem_cons,List.not_mem_nil,or_false] at hr
  rcases hr with rfl | rfl | rfl | rfl <;>
    simp only [LinearConstraint.Holds,Bool.false_eq_true,ite_false,eval_affine5] <;>
    push_cast <;> linarith

/-- This is a verified replacement for the numerical uses of the four-point
rule. It checks all sixteen face choices through exact linear certificates,
without assuming that a Python convexity or acute-angle predicate is sound. -/
theorem four_point_certificate_sound (a b p e : ℚ × ℚ)
    (hd : distSq p e ≤ 1)
    (certs : Fin 4 → Fin 4 → List (ℚ × LinearConstraint 5))
    (hc : ∀ f g, LinearCertificateCheck (fourPointRows a b p e f g) (certs f g))
    (q : OpenSquare) (hs : 1 < q.side)
    (ha : q.Inside a.1 a.2) (hb : q.Inside b.1 b.2) :
    q.Inside p.1 p.2 ∨ q.Inside e.1 e.2 := by
  by_contra h
  obtain ⟨hp,he⟩ := not_or.mp h
  obtain ⟨f,hf⟩ := outside_has_face q p hp
  obtain ⟨g,hg⟩ := outside_has_face q e he
  apply linear_certificate_sound _ _ (hc f g)
  refine ⟨squareEnv q,?_⟩
  intro r hr
  simp only [fourPointRows,List.mem_append,List.mem_cons,List.not_mem_nil,or_false] at hr
  rcases hr with ((((h0 | h1) | h2) | h3) | (h4 | h5)) | h6
  · subst r; simp [LinearConstraint.Holds,eval_affine5]
  · subst r; simp [LinearConstraint.Holds,eval_affine5]; linarith
  · exact inside_rows_hold q a ha r h2
  · exact inside_rows_hold q b hb r h3
  · subst r; exact hf
  · subst r; exact hg
  · exact projection_rows_hold q p e hd r h6

#print axioms four_point_certificate_sound
end S12

namespace S12
open S12Pilot

structure FourPointDatum where
  a : ℚ × ℚ
  b : ℚ × ℚ
  p : ℚ × ℚ
  e : ℚ × ℚ
  weights : List (List (Nat × ℚ))

def FourPointDatum.terms (w : FourPointDatum) (f g : Fin 4) : List (ℚ × LinearConstraint 5) :=
  let inputs := fourPointRows w.a w.b w.p w.e f g
  let ws := w.weights[f.val*4+g.val]?.getD []
  ws.map fun t => (t.2,inputs[t.1]?.getD (LinearConstraint.zero 5))

def FourPointDatum.Check (w : FourPointDatum) : Prop :=
  distSq w.p w.e ≤ 1 ∧ ∀ f g, LinearCertificateCheck
    (fourPointRows w.a w.b w.p w.e f g) (w.terms f g)
instance FourPointDatum.decidableCheck (w : FourPointDatum) : Decidable w.Check := inferInstanceAs (Decidable (_ ∧ _))

theorem FourPointDatum.sound (w : FourPointDatum) (hw : w.Check)
    (q : OpenSquare) (ha : 1 < q.side)
    (hi0 : q.Inside w.a.1 w.a.2) (hi1 : q.Inside w.b.1 w.b.2) :
    q.Inside w.p.1 w.p.2 ∨ q.Inside w.e.1 w.e.2 :=
  four_point_certificate_sound w.a w.b w.p w.e hw.1 w.terms hw.2 q ha hi0 hi1

end S12
