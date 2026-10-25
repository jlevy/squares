import S12.TransformFacts

namespace S12
open S12Pilot
set_option maxHeartbeats 0

def baseSingletonSeeds : List (ℚ × ℚ) := [(28/25,1),(87/50,1),(187/100,19/25)]
def singletonExtras (t : Transform) (g : Finset Marker) : List (ℚ × ℚ) :=
  if g={t.markerAction 0} then baseSingletonSeeds.map t.applyRat else []
def cornerExtras (t : Transform) (g : Finset Marker) : List (ℚ × ℚ) :=
  if t.markerAction 0∈g ∧ t.markerAction 1∈g then [t.applyRat (1,1)] else []
def wallExtras (t : Transform) (g : Finset Marker) : List (ℚ × ℚ) :=
  if t.markerAction 1∈g ∧ t.markerAction 12∈g then
    [t.applyRat (1,5/4),t.applyRat (1,7/4)] else []

/-- A finite list of proved interior points. It deliberately contains the
original points, before any external convex-hull calculation. -/
def seedPoints (g : Finset Marker) : List (ℚ × ℚ) :=
  ((List.finRange 16).filter (fun i => decide (i∈g))).map marker ++
  allTransforms.flatMap (fun t => singletonExtras t g ++ cornerExtras t g ++ wallExtras t g)

theorem singleton_extras_sound (q : OpenSquare) (ha : 1<q.side) (hsize : q.side≤1001/1000)
    (hbox : InsideContainer q) (g : Finset Marker) (hg : ExactMarkers q g)
    (t : Transform) (p : ℚ × ℚ) (hp : p∈singletonExtras t g) : q.Inside p.1 p.2 := by
  by_cases he : g={t.markerAction 0}
  · simp only [singletonExtras,if_pos he] at hp
    obtain ⟨v,hv,rfl⟩ := List.mem_map.mp hp
    have h0 : Owns (t.pull q) 0 := (owns_transform t q 0).mpr ((hg _).mpr (by simp [he]))
    have hout : ∀ i : Marker, i≠0 → ¬Owns (t.pull q) i := by
      intro i hi ho
      have hm := (hg _).mp ((owns_transform t q i).mp ho)
      have hm' : t.markerAction i=t.markerAction 0 := by simpa [he] using hm
      exact hi (t.markerAction_injective hm')
    obtain ⟨h1,h2,h3⟩ := corner_singleton_forces (t.pull q) (by simpa using ha)
      (by simpa using hsize) (container_transform t q hbox) h0 hout
    apply (rat_inside_transform t q v).mp
    simp only [baseSingletonSeeds,List.mem_cons,List.not_mem_nil,or_false] at hv
    rcases hv with rfl | rfl | rfl
    · simpa using h1
    · simpa using h2
    · simpa using h3
  · simp [singletonExtras,he] at hp

theorem corner_extras_sound (q : OpenSquare) (ha : 1<q.side)
    (hbox : InsideContainer q) (g : Finset Marker) (hg : ExactMarkers q g)
    (t : Transform) (p : ℚ × ℚ) (hp : p∈cornerExtras t g) : q.Inside p.1 p.2 := by
  by_cases he : t.markerAction 0∈g ∧ t.markerAction 1∈g
  · simp only [cornerExtras,if_pos he,List.mem_singleton] at hp
    subst p
    have h0 := (owns_transform t q 0).mpr ((hg _).mpr he.1)
    have h1 := (owns_transform t q 1).mpr ((hg _).mpr he.2)
    have h := corner_pair_forces (t.pull q) (by simpa using ha)
      (fun x y hi => ⟨(container_transform t q hbox x y hi).1,
        (container_transform t q hbox x y hi).2.2.1⟩)
      (457/500) (by norm_num) (by simpa [Owns,marker] using h0) (by simpa [Owns,marker] using h1)
    apply (rat_inside_transform t q (1,1)).mp
    simpa using h
  · simp [cornerExtras,he] at hp

theorem wall_extras_sound (q : OpenSquare) (ha : 1<q.side)
    (hbox : InsideContainer q) (g : Finset Marker) (hg : ExactMarkers q g)
    (t : Transform) (p : ℚ × ℚ) (hp : p∈wallExtras t g) : q.Inside p.1 p.2 := by
  by_cases he : t.markerAction 1∈g ∧ t.markerAction 12∈g
  · simp only [wallExtras,if_pos he,List.mem_cons,List.not_mem_nil,or_false] at hp
    have h0 := (owns_transform t q 1).mpr ((hg _).mpr he.1)
    have h1 := (owns_transform t q 12).mpr ((hg _).mpr he.2)
    have hw : ∀ x y, (t.pull q).Inside x y → 0≤x :=
      fun x y hi => (container_transform t q hbox x y hi).1
    rcases hp with rfl | rfl
    · apply (rat_inside_transform t q (1,5/4)).mp
      have h := wall_bridge_forces (t.pull q) (by simpa using ha) hw
        (by simpa [Owns,marker] using h0) (by simpa [Owns,marker] using h1) (5/4) (by norm_num) (by norm_num)
      simpa using h
    · apply (rat_inside_transform t q (1,7/4)).mp
      have h := wall_bridge_forces (t.pull q) (by simpa using ha) hw
        (by simpa [Owns,marker] using h0) (by simpa [Owns,marker] using h1) (7/4) (by norm_num) (by norm_num)
      simpa using h
  · simp [wallExtras,he] at hp

theorem seed_points_sound (q : OpenSquare) (ha : 1<q.side) (hsize : q.side≤1001/1000)
    (hbox : InsideContainer q) (g : Finset Marker) (hg : ExactMarkers q g) :
    ∀ p∈seedPoints g, q.Inside p.1 p.2 := by
  intro p hp
  rcases List.mem_append.mp hp with hp | hp
  · obtain ⟨i,hi,rfl⟩ := List.mem_map.mp hp
    exact (hg i).mpr (of_decide_eq_true (List.mem_filter.mp hi).2)
  · obtain ⟨t,_,hp⟩ := List.mem_flatMap.mp hp
    rcases List.mem_append.mp hp with hp | hp
    · rcases List.mem_append.mp hp with hp | hp
      · exact singleton_extras_sound q ha hsize hbox g hg t p hp
      · exact corner_extras_sound q ha hbox g hg t p hp
    · exact wall_extras_sound q ha hbox g hg t p hp

#print axioms seed_points_sound
end S12
