import S12.Convex

namespace S12
open S12Pilot

structure HullConflictCertificate where
  leftSeeds : List (ℚ × ℚ)
  rightSeeds : List (ℚ × ℚ)
  left : TriangleCertificate
  right : TriangleCertificate

def HullConflictCertificate.Check (w : HullConflictCertificate) : Prop :=
  w.left.Check ∧ w.right.Check ∧ w.left.target = w.right.target ∧
  w.left.p0 ∈ w.leftSeeds ∧ w.left.p1 ∈ w.leftSeeds ∧ w.left.p2 ∈ w.leftSeeds ∧
  w.right.p0 ∈ w.rightSeeds ∧ w.right.p1 ∈ w.rightSeeds ∧ w.right.p2 ∈ w.rightSeeds
instance HullConflictCertificate.decidableCheck (w : HullConflictCertificate) : Decidable w.Check := inferInstanceAs (Decidable (_ ∧ _))

theorem hull_conflict_certificate_sound (w : HullConflictCertificate) (hw : w.Check)
    (q r : OpenSquare)
    (hl : ∀ p ∈ w.leftSeeds, q.Inside p.1 p.2)
    (hr : ∀ p ∈ w.rightSeeds, r.Inside p.1 p.2) :
    ∃ x y, q.Inside x y ∧ r.Inside x y := by
  obtain ⟨cl,cr,ht,l0,l1,l2,r0,r1,r2⟩ := hw
  have hq := triangle_certificate_sound w.left cl q
    (hl _ l0) (hl _ l1) (hl _ l2)
  have hr' := triangle_certificate_sound w.right cr r
    (hr _ r0) (hr _ r1) (hr _ r2)
  rw [← ht] at hr'
  exact ⟨w.left.target.1,w.left.target.2,hq,hr'⟩

#print axioms hull_conflict_certificate_sound
end S12
