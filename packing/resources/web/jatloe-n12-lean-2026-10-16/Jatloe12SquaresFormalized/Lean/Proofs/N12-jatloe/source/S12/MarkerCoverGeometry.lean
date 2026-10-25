import S12.Container
import S12.MarkerCoverGeometryBase
namespace S12
open S12Pilot
set_option maxHeartbeats 0

@[simp] theorem center_shiftOne_x (q : OpenSquare) : centerX (q.translated 1 0)=centerX q-1 := by
  dsimp [centerX,OpenSquare.translated]; nlinarith [q.unit_normal]
@[simp] theorem center_shiftOne_y (q : OpenSquare) : centerY (q.translated 1 0)=centerY q := by
  dsimp [centerY,OpenSquare.translated]; ring

theorem side_region_hit (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hX : centerX q≤457/500) (hY0 : 1≤centerY q) (hY1 : centerY q≤2) :
    Owns q 1 ∨ Owns q 12 := by
  let r := (pullSwap q).translated 1 0
  have hrside : 1<r.side := ha
  have hrwall : ∀ x y, r.Inside x y → 0≤y := by
    intro x y hi
    have hq : q.Inside y (1+x) := by
      simpa [r,inside_translated_iff,inside_pullSwap] using hi
    exact (hbox _ _ hq).1
  have hx0 : 0≤centerX r := by dsimp [r]; simp; linarith
  have hx1 : centerX r≤1 := by dsimp [r]; simp; linarith
  have hy : centerY r≤457/500 := by simpa [r] using hX
  have h := wall_row_nonavoidance r hrside hrwall hx0 hx1 hy
  simpa [r,inside_translated_iff,inside_pullSwap,Owns,marker,show (1:ℝ)+1=2 by norm_num] using h

/-- Four triangles, a unit corner, and a wall row cover this fundamental
region. The barycentric formulas are explicit rational affine expressions. -/
theorem fundamental_region_hit (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hxy : centerX q≤centerY q) (hy2 : centerY q≤2) : ∃ i : Marker, Owns q i := by
  by_cases hy1 : centerY q≤1
  · have h := corner_nonavoidance_horizontal q ha
      (fun x y hi => ⟨(hbox x y hi).1,(hbox x y hi).2.2.1⟩)
      (by linarith) hy1 (457/500) (by norm_num) (by norm_num)
    exact ⟨1,by simpa [Owns,marker] using h⟩
  by_cases hx : centerX q≤457/500
  · rcases side_region_hit q ha hbox hx (by linarith) hy2 with h | h
    · exact ⟨1,h⟩
    · exact ⟨12,h⟩
  by_cases hx3 : 33/20≤centerX q
  · have h := triangle3_hit q ha (by dsimp [tri3w0]; linarith)
      (by dsimp [tri3w1]; linarith) (by dsimp [tri3w2]; linarith)
    rcases h with h | h | h
    · exact ⟨8,h⟩
    · exact ⟨9,h⟩
    · exact ⟨11,h⟩
  by_cases h2 : 0≤tri2w2 (centerX q) (centerY q)
  · have h := triangle2_hit q ha (by dsimp [tri2w0]; linarith)
      (by dsimp [tri2w1]; linarith) h2
    rcases h with h | h | h
    · exact ⟨12,h⟩
    · exact ⟨8,h⟩
    · exact ⟨11,h⟩
  by_cases h1 : 0≤tri1w1 (centerX q) (centerY q)
  · have h := triangle1_hit q ha (by dsimp [tri1w0,tri2w2] at *; linarith) h1
      (by dsimp [tri1w2]; linarith)
    rcases h with h | h | h
    · exact ⟨1,h⟩
    · exact ⟨12,h⟩
    · exact ⟨8,h⟩
  · have h := triangle0_hit q ha (by dsimp [tri0w0,tri1w1] at *; linarith)
      (by dsimp [tri0w1]; linarith) (by dsimp [tri0w2]; linarith)
    rcases h with h | h | h
    · exact ⟨0,h⟩
    · exact ⟨1,h⟩
    · exact ⟨8,h⟩

theorem lower_left_region_hit (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hx2 : centerX q≤2) (hy2 : centerY q≤2) : ∃ i : Marker, Owns q i := by
  by_cases hxy : centerX q≤centerY q
  · exact fundamental_region_hit q ha hbox hxy hy2
  · obtain ⟨i,hi⟩ := fundamental_region_hit (pullSwap q) ha (container_pullSwap q hbox)
      (by simp; linarith) (by simpa using hx2)
    exact ⟨permSwap i,(owns_pullSwap q i).mp hi⟩

theorem lower_region_hit (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hy2 : centerY q≤2) : ∃ i : Marker, Owns q i := by
  by_cases hx2 : centerX q≤2
  · exact lower_left_region_hit q ha hbox hx2 hy2
  · obtain ⟨i,hi⟩ := lower_left_region_hit (pullX q) ha (container_pullX q hbox)
      (by simp; linarith) (by simpa using hy2)
    exact ⟨permX i,(owns_pullX q i).mp hi⟩

/-- The complete 16-marker non-avoidance statement, with no imported geometric
premise and no compiled arithmetic in its proof. -/
theorem marker_nonavoidance (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q) :
    ∃ i : Marker, Owns q i := by
  by_cases hy2 : centerY q≤2
  · exact lower_region_hit q ha hbox hy2
  · obtain ⟨i,hi⟩ := lower_region_hit (pullY q) ha (container_pullY q hbox)
      (by simp; linarith)
    exact ⟨permY i,(owns_pullY q i).mp hi⟩

#print axioms marker_nonavoidance
end S12
