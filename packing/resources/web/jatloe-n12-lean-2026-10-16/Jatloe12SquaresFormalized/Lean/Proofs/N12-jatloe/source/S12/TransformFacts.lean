import S12.SingletonForcing
import S12.WallBridge

namespace S12
open S12Pilot

theorem permX_injective : Function.Injective permX := by
  have h : Function.Involutive permX := by intro i; fin_cases i <;> decide
  exact h.injective
theorem permY_injective : Function.Injective permY := by
  have h : Function.Involutive permY := by intro i; fin_cases i <;> decide
  exact h.injective
theorem permSwap_injective : Function.Injective permSwap := by
  have h : Function.Involutive permSwap := by intro i; fin_cases i <;> decide
  exact h.injective

def Transform.markerAction (g : Transform) (i : Marker) : Marker :=
  let j := if g.swap then permSwap i else i
  let k := if g.reflectY then permY j else j
  if g.reflectX then permX k else k

theorem Transform.markerAction_injective (g : Transform) : Function.Injective g.markerAction := by
  have hx : Function.Injective (fun i => if g.reflectX then permX i else i) := by
    cases h : g.reflectX <;> simp only [h,Bool.false_eq_true,ite_false,ite_true]
    · exact Function.injective_id
    · exact permX_injective
  have hy : Function.Injective (fun i => if g.reflectY then permY i else i) := by
    cases h : g.reflectY <;> simp only [h,Bool.false_eq_true,ite_false,ite_true]
    · exact Function.injective_id
    · exact permY_injective
  have ht : Function.Injective (fun i => if g.swap then permSwap i else i) := by
    cases h : g.swap <;> simp only [h,Bool.false_eq_true,ite_false,ite_true]
    · exact Function.injective_id
    · exact permSwap_injective
  exact hx.comp (hy.comp ht)

theorem owns_transform (g : Transform) (q : OpenSquare) (i : Marker) :
    Owns (g.pull q) i ↔ Owns q (g.markerAction i) := by
  rcases g with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;>
    simp [Transform.pull,Transform.markerAction,owns_pullX,owns_pullY,owns_pullSwap]

theorem container_transform (g : Transform) (q : OpenSquare) (h : InsideContainer q) :
    InsideContainer (g.pull q) := by
  rcases g with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;> simp only [Transform.pull,Bool.false_eq_true,ite_false,ite_true]
  all_goals
    repeat' first | apply container_pullSwap | apply container_pullY | apply container_pullX | exact h

def Transform.applyRat (g : Transform) (p : ℚ × ℚ) : ℚ × ℚ :=
  let (u,v) := if g.swap then (p.2,p.1) else p
  (if g.reflectX then 4-u else u, if g.reflectY then 4-v else v)

theorem rat_inside_transform (g : Transform) (q : OpenSquare) (p : ℚ × ℚ) :
    (g.pull q).Inside p.1 p.2 ↔ q.Inside (g.applyRat p).1 (g.applyRat p).2 := by
  rw [inside_pull]
  rcases g with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;> simp [Transform.apply,Transform.applyRat]

def allTransforms : List Transform := [⟨false,false,false⟩,⟨false,false,true⟩,
  ⟨false,true,false⟩,⟨false,true,true⟩,⟨true,false,false⟩,⟨true,false,true⟩,
  ⟨true,true,false⟩,⟨true,true,true⟩]

def ExactMarkers (q : OpenSquare) (g : Finset Marker) : Prop :=
  ∀ i : Marker, Owns q i ↔ i∈g

#print axioms owns_transform
end S12
