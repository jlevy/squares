import S12.SingletonTriangles
import S12.GeneralWallSegments

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- A replacement marker is forced once its two wall rows and two interior
triangle regions cover the possible center locations. -/
theorem singleton_forcing_template (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q) (hp : Owns q 0)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) (px py d : ℝ)
    (hwallL : 457/500≤centerX q → centerX q≤px → centerY q≤1 →
      q.Inside (457/500) 1 ∨ q.Inside px py)
    (hwallR : px≤centerX q → centerX q≤2 → centerY q≤d →
      q.Inside px py ∨ q.Inside 2 (457/500))
    (htriL : 457/500≤centerX q → centerX q≤px → 1≤centerY q → centerY q≤2 →
      q.Inside px py)
    (htriR : px≤centerX q → centerX q≤2 → d≤centerY q → centerY q≤2 →
      q.Inside px py) : q.Inside px py := by
  obtain ⟨hx2,hy2⟩ := corner_owner_center q hsize hp
  have hB : ¬q.Inside (457/500) 1 := by simpa [Owns,marker] using hout 1 (by decide)
  have hM : ¬q.Inside 2 (457/500) := by simpa [Owns,marker] using hout 13 (by decide)
  by_cases hx0 : centerX q≤457/500
  · by_cases hy0 : centerY q≤1
    · have h := corner_nonavoidance_horizontal q ha
        (fun x y hi => ⟨(hbox x y hi).1,(hbox x y hi).2.2.1⟩)
        (by linarith) hy0 (457/500) (by norm_num) (by norm_num)
      exact False.elim (hB h)
    · have h := side_region_hit q ha hbox hx0 (by linarith) hy2
      exact False.elim (h.elim (hout 1 (by decide)) (hout 12 (by decide)))
  by_cases hx : centerX q≤px
  · by_cases hy : centerY q≤1
    · exact (hwallL (by linarith) hx hy).resolve_left hB
    · exact htriL (by linarith) hx (by linarith) hy2
  · by_cases hy : centerY q≤d
    · exact (hwallR (by linarith) hx2 hy).resolve_right hM
    · exact htriR (by linarith) hx2 (by linarith) hy2

theorem singleton_forces_112 (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q) (hp : Owns q 0)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) : q.Inside (28/25) 1 := by
  have hw : ∀ x y, q.Inside x y → 0≤y := fun x y hi => (hbox x y hi).2.2.1
  apply singleton_forcing_template q ha hsize hbox hp hout (28/25) 1 1
  · intro hx0 hx1 hy
    exact bottom_segment_hit q ha hw (457/500) (28/25) 1 hx0 hx1 hy (by norm_num) (by norm_num)
  · intro hx0 hx1 hy
    apply general_segment_descending q ha hw (28/25) 2 1 (457/500) hx0 hx1 hy
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    intro c s hc hs hn
    nlinarith only [normal_bound_088 c s hc hs hn]
  · intro hx0 hx1 hy0 hy1
    exact replacement0_left q ha hx0 hx1 hy0 hy1 hout
  · intro hx0 hx1 hy0 hy1
    exact replacement0_right q ha hx0 hx1 hy0 hy1 hout

theorem singleton_forces_174 (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q) (hp : Owns q 0)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) : q.Inside (87/50) 1 := by
  have hw : ∀ x y, q.Inside x y → 0≤y := fun x y hi => (hbox x y hi).2.2.1
  apply singleton_forcing_template q ha hsize hbox hp hout (87/50) 1 1
  · intro hx0 hx1 hy
    exact bottom_segment_hit q ha hw (457/500) (87/50) 1 hx0 hx1 hy (by norm_num) (by norm_num)
  · intro hx0 hx1 hy
    apply general_segment_descending q ha hw (87/50) 2 1 (457/500) hx0 hx1 hy
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    intro c s hc hs hn
    exact normal_bound_small _ _ _ c s (by norm_num) (by norm_num) (by norm_num) hc hs hn
  · intro hx0 hx1 hy0 hy1
    exact replacement1_left q ha hx0 hx1 hy0 hy1 hout
  · intro hx0 hx1 hy0 hy1
    exact replacement1_right q ha hx0 hx1 hy0 hy1 hout

theorem singleton_forces_187 (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q) (hp : Owns q 0)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) : q.Inside (187/100) (19/25) := by
  have hw : ∀ x y, q.Inside x y → 0≤y := fun x y hi => (hbox x y hi).2.2.1
  apply singleton_forcing_template q ha hsize hbox hp hout (187/100) (19/25) (457/500)
  · intro hx0 hx1 hy
    apply general_segment_descending q ha hw (457/500) (187/100) 1 (19/25) hx0 hx1 hy
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    intro c s hc hs hn
    nlinarith only [normal_bound_0956 c s hc hs hn]
  · intro hx0 hx1 hy
    apply general_segment_hit q ha hw (187/100) 2 (19/25) (457/500) hx0 hx1 hy
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    intro c s hc hs hn
    exact normal_bound_small _ _ _ c s (by norm_num) (by norm_num) (by norm_num) hc hs hn
  · intro hx0 hx1 hy0 hy1
    exact replacement2_left q ha hx0 hx1 hy0 hy1 hout
  · intro hx0 hx1 hy0 hy1
    exact replacement2_right q ha hx0 hx1 hy0 hy1 hout

/-- All three singleton seeds used by the normalized classifier. This proves
the corrected horizontal (1.74,1) statement, not the paper's transposed typo. -/
theorem corner_singleton_forces (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q) (hp : Owns q 0)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (28/25) 1 ∧ q.Inside (87/50) 1 ∧ q.Inside (187/100) (19/25) :=
  ⟨singleton_forces_112 q ha hsize hbox hp hout,
    singleton_forces_174 q ha hsize hbox hp hout,
    singleton_forces_187 q ha hsize hbox hp hout⟩

#print axioms corner_singleton_forces
end S12
