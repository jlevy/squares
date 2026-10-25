import S12.Seeds
import S12.Convex
import S12.FourPointData

namespace S12
open S12Pilot

inductive ShortKind | fiveLeft | fiveRight | six
  deriving DecidableEq, Repr

def ShortKind.insidePoints : ShortKind → List (ℚ × ℚ)
  | .fiveLeft => [(33/20,33/20),(1,113/50)]
  | .fiveRight => [(33/20,33/20),(2,113/50)]
  | .six => [(457/500,2),(1,87/50),(87/50,2)]
def ShortKind.outsidePoints : ShortKind → List (ℚ × ℚ)
  | .fiveLeft | .fiveRight => [(1,87/50),(33/20,47/20),(2,87/50)]
  | .six => [(1,8/5),(1,12/5),(33/20,33/20)]

theorem ShortKind.sound (k : ShortKind) (q : OpenSquare) (ha : 1<q.side)
    (hi : ∀ p∈k.insidePoints, q.Inside p.1 p.2) :
    ∃ p∈k.outsidePoints, q.Inside p.1 p.2 := by
  cases k with
  | fiveLeft =>
    have h := five_point_left q ha
      (by simpa using hi (33/20,33/20) (by simp [ShortKind.insidePoints]))
      (by simpa using hi (1,113/50) (by simp [ShortKind.insidePoints]))
    rcases h with h | h | h
    · exact ⟨(1,87/50),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(33/20,47/20),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(2,87/50),by simp [ShortKind.outsidePoints],by simpa using h⟩
  | fiveRight =>
    have h := five_point_right q ha
      (by simpa using hi (33/20,33/20) (by simp [ShortKind.insidePoints]))
      (by simpa using hi (2,113/50) (by simp [ShortKind.insidePoints]))
    rcases h with h | h | h
    · exact ⟨(1,87/50),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(33/20,47/20),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(2,87/50),by simp [ShortKind.outsidePoints],by simpa using h⟩
  | six =>
    have h := side_six_point q ha
      (by simpa using hi (457/500,2) (by simp [ShortKind.insidePoints]))
      (by simpa using hi (1,87/50) (by simp [ShortKind.insidePoints]))
      (by simpa using hi (87/50,2) (by simp [ShortKind.insidePoints]))
    rcases h with h | h | h
    · exact ⟨(1,8/5),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(1,12/5),by simp [ShortKind.outsidePoints],by simpa using h⟩
    · exact ⟨(33/20,33/20),by simp [ShortKind.outsidePoints],by simpa using h⟩

structure ShortTemplate where
  transform : Transform
  kind : ShortKind
  deriving DecidableEq, Repr

def ShortTemplate.insidePoints (k : ShortTemplate) : List (ℚ × ℚ) :=
  k.kind.insidePoints.map k.transform.applyRat
def ShortTemplate.outsidePoints (k : ShortTemplate) : List (ℚ × ℚ) :=
  k.kind.outsidePoints.map k.transform.applyRat

theorem ShortTemplate.sound (k : ShortTemplate) (q : OpenSquare) (ha : 1<q.side)
    (hi : ∀ p∈k.insidePoints, q.Inside p.1 p.2) :
    ∃ p∈k.outsidePoints, q.Inside p.1 p.2 := by
  have hbase : ∀ p∈k.kind.insidePoints, (k.transform.pull q).Inside p.1 p.2 := by
    intro p hp
    apply (rat_inside_transform k.transform q p).mpr
    exact hi _ (List.mem_map.mpr ⟨p,hp,rfl⟩)
  obtain ⟨p,hp,hi'⟩ := k.kind.sound (k.transform.pull q) (by simpa using ha) hbase
  exact ⟨k.transform.applyRat p,List.mem_map.mpr ⟨p,hp,rfl⟩,
    (rat_inside_transform k.transform q p).mp hi'⟩

def HullInCheck (inside : List (ℚ × ℚ)) (w : TriangleCertificate) : Prop :=
  w.Check ∧ w.p0∈inside ∧ w.p1∈inside ∧ w.p2∈inside
instance decidableHullInCheck (inside : List (ℚ × ℚ)) (w : TriangleCertificate) :
    Decidable (HullInCheck inside w) := inferInstanceAs (Decidable (_ ∧ _))

theorem hull_in_sound (inside : List (ℚ × ℚ)) (w : TriangleCertificate) (hw : HullInCheck inside w)
    (q : OpenSquare) (hi : ∀ p∈inside, q.Inside p.1 p.2) : q.Inside w.target.1 w.target.2 :=
  triangle_certificate_sound w hw.1 q (hi _ hw.2.1) (hi _ hw.2.2.1) (hi _ hw.2.2.2)

/-- Each certificate names the precise inside and outside points it uses.
The four-point proof is an actual checked proof field, never a Boolean claim
supplied by the Python generator. -/
inductive LocalRejection
  | hull (w : TriangleCertificate)
  | short (k : ShortTemplate) (witnesses : List TriangleCertificate)
  | four (t : Transform) (w : FourPointDatum) (checked : w.Check)

def LocalRejection.Check (c : LocalRejection) (inside outside : List (ℚ × ℚ)) : Prop :=
  match c with
  | .hull w => HullInCheck inside w ∧ w.target∈outside
  | .short k ws =>
    (∀ p∈k.insidePoints, ∃ w∈ws, w.target=p ∧ HullInCheck inside w) ∧
    (∀ p∈k.outsidePoints, p∈outside)
  | .four t w _ => t.applyRat w.a∈inside ∧ t.applyRat w.b∈inside ∧
    t.applyRat w.p∈outside ∧ t.applyRat w.e∈outside

instance LocalRejection.decidableCheck (c : LocalRejection) (inside outside : List (ℚ × ℚ)) :
    Decidable (c.Check inside outside) := by
  cases c <;> exact inferInstanceAs (Decidable (_ ∧ _))

theorem LocalRejection.sound (c : LocalRejection) (inside outside : List (ℚ × ℚ))
    (hc : c.Check inside outside) (q : OpenSquare) (ha : 1<q.side)
    (hi : ∀ p∈inside, q.Inside p.1 p.2) (ho : ∀ p∈outside, ¬q.Inside p.1 p.2) : False := by
  cases c with
  | hull w => exact ho _ hc.2 (hull_in_sound inside w hc.1 q hi)
  | short k ws =>
    have hinner : ∀ p∈k.insidePoints, q.Inside p.1 p.2 := by
      intro p hp
      obtain ⟨w,_,ht,hw⟩ := hc.1 p hp
      have h := hull_in_sound inside w hw q hi
      simpa only [ht] using h
    obtain ⟨p,hp,h⟩ := k.sound q ha hinner
    exact ho p (hc.2 p hp) h
  | four t w hw =>
    have h0 := (rat_inside_transform t q w.a).mpr (hi _ hc.1)
    have h1 := (rat_inside_transform t q w.b).mpr (hi _ hc.2.1)
    have h := w.sound hw (t.pull q) (by simpa using ha) h0 h1
    rcases h with h | h
    · exact ho _ hc.2.2.1 ((rat_inside_transform t q w.p).mp h)
    · exact ho _ hc.2.2.2 ((rat_inside_transform t q w.e).mp h)

#print axioms LocalRejection.sound
end S12
