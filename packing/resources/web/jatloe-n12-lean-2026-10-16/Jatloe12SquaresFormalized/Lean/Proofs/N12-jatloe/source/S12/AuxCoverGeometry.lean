import S12.AuxCoverBase

namespace S12
open S12Pilot
set_option maxHeartbeats 0

@[simp] theorem center_translate_x (q : OpenSquare) (x y : ℝ) :
    centerX (q.translated x y)=centerX q-x := by
  dsimp [centerX,OpenSquare.translated]
  nlinarith [congrArg (fun z : ℝ => z*x) q.unit_normal]
@[simp] theorem center_translate_y (q : OpenSquare) (x y : ℝ) :
    centerY (q.translated x y)=centerY q-y := by
  dsimp [centerY,OpenSquare.translated]
  nlinarith [congrArg (fun z : ℝ => z*y) q.unit_normal]

theorem bottom_segment_hit (q : OpenSquare) (ha : 1<q.side)
    (hw : ∀ x y, q.Inside x y → 0≤y) (x0 x1 b : ℝ)
    (hX0 : x0≤centerX q) (hX1 : centerX q≤x1) (hY : centerY q≤b)
    (hlen : x1-x0≤413/500) (hb : b≤1) :
    q.Inside x0 b ∨ q.Inside x1 b := by
  have h := wide_wall_row_nonavoidance (q.translated x0 0) ha
    (by intro x y hi; simpa using hw _ _ ((inside_translated_iff q x0 0 x y).mp hi))
    (x1-x0) b (by simp; linarith) (by simp; linarith) (by simpa using hY)
    (by linarith) hlen hb
  simpa only [inside_translated_iff,add_zero,zero_add,
    show x0+(x1-x0)=x1 by ring] using h

theorem bottom_twoheight_hit (q : OpenSquare) (ha : 1<q.side)
    (hw : ∀ x y, q.Inside x y → 0≤y) (x0 x1 b d : ℝ)
    (hX0 : x0≤centerX q) (hX1 : centerX q≤x1) (hY : centerY q≤d)
    (hlen : x1-x0≤4/5) (hb : 9/10≤b) (hbd : b≤d) (hd : d≤1) :
    q.Inside x0 b ∨ q.Inside x1 d := by
  have h := two_height_wall_nonavoidance (q.translated x0 0) ha
    (by intro x y hi; simpa using hw _ _ ((inside_translated_iff q x0 0 x y).mp hi))
    (x1-x0) b d (by simp; linarith) (by simp; linarith) (by simpa using hY)
    (by linarith) hlen hb hbd hd
  simpa only [inside_translated_iff,add_zero,zero_add,
    show x0+(x1-x0)=x1 by ring] using h

theorem aux_avoid_walls (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hf : AvoidsF q) (hm : ¬Owns q 0 ∨ ¬Owns q 1)
    (hX : centerX q≤2) (hY : centerY q≤2) :
    1<centerX q ∧ 1<centerY q := by
  have hL : ¬q.Inside 1 (87/50) := by simpa [fPoint] using hf 0
  have hL' : ¬q.Inside 1 (113/50) := by simpa [fPoint] using hf 1
  have hB : ¬q.Inside (8/5) 1 := by simpa [fPoint] using hf 2
  have hB' : ¬q.Inside (12/5) 1 := by simpa [fPoint] using hf 6
  have hw : ∀ x y, q.Inside x y → 0≤y := fun x y hi => (hbox x y hi).2.2.1
  have hws : ∀ x y, (pullSwap q).Inside x y → 0≤y := by
    intro x y hi; exact (hbox _ _ ((inside_pullSwap q x y).mp hi)).1
  have hm' : ¬q.Inside 1 (457/500) ∨ ¬q.Inside (457/500) 1 := by
    simpa [Owns,marker] using hm
  have hx1 : 1<centerX q := by
    by_contra he
    have hx : centerX q≤1 := le_of_not_gt he
    by_cases hy : centerY q≤1
    · have h0 := corner_nonavoidance_horizontal q ha
        (fun x y hi => ⟨(hbox x y hi).1,(hbox x y hi).2.2.1⟩)
        hx hy (457/500) (by norm_num) (by norm_num)
      have h1 := corner_nonavoidance_horizontal (pullSwap q) ha
        (fun x y hi => ⟨(container_pullSwap q hbox x y hi).1,
          (container_pullSwap q hbox x y hi).2.2.1⟩)
        (by simpa using hy) (by simpa using hx) (457/500) (by norm_num) (by norm_num)
      have h1' : q.Inside 1 (457/500) := by simpa [inside_pullSwap] using h1
      exact hm'.elim (fun h => h h1') (fun h => h h0)
    by_cases hy' : centerY q≤87/50
    · rcases hm' with hm' | hm'
      · have h := bottom_segment_hit (pullSwap q) ha hws (457/500) (87/50) 1
          (by simp; linarith) (by simpa using hy') (by simpa using hx) (by norm_num) (by norm_num)
        simp only [inside_pullSwap] at h
        exact h.elim hm' hL
      · have h := bottom_twoheight_hit (pullSwap q) ha hws 1 (87/50) (457/500) 1
          (by simp; linarith) (by simpa using hy') (by simpa using hx)
          (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        simp only [inside_pullSwap] at h
        exact h.elim hm' hL
    · have h := bottom_segment_hit (pullSwap q) ha hws (87/50) (113/50) 1
        (by simp; linarith) (by simp; linarith) (by simpa using hx) (by norm_num) (by norm_num)
      simp only [inside_pullSwap] at h
      exact h.elim hL hL'
  refine ⟨hx1,?_⟩
  by_contra he
  have hy : centerY q≤1 := le_of_not_gt he
  by_cases hx : centerX q≤8/5
  · rcases hm' with hm' | hm'
    · have h := bottom_twoheight_hit q ha hw 1 (8/5) (457/500) 1
        (by linarith) hx hy (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      exact h.elim hm' hB
    · have h := bottom_segment_hit q ha hw (457/500) (8/5) 1
        (by linarith) hx hy (by norm_num) (by norm_num)
      exact h.elim hm' hB
  · have h := bottom_segment_hit q ha hw (8/5) (12/5) 1
      (by linarith) (by linarith) hy (by norm_num) (by norm_num)
    exact h.elim hB hB'

theorem aux_lower_interior_hit (q : OpenSquare) (ha : 1<q.side) (hf : AvoidsF q)
    (hm : ¬Owns q 0 ∨ ¬Owns q 1) (hx0 : 1≤centerX q) (hx1 : centerX q≤2)
    (hy0 : 1≤centerY q) (hy1 : centerY q≤87/50) : False := by
  have hL : ¬q.Inside 1 (87/50) := by simpa [fPoint] using hf 0
  have hB : ¬q.Inside (8/5) 1 := by simpa [fPoint] using hf 2
  have hM : ¬q.Inside 2 (87/50) := by simpa [fPoint] using hf 4
  have hB' : ¬q.Inside (12/5) 1 := by simpa [fPoint] using hf 6
  by_cases h2 : 0≤aux1w2 (centerX q) (centerY q)
  · by_cases h0 : 0≤aux1w0 (centerX q) (centerY q)
    · have h := aux1_hit q ha h0 (by dsimp [aux1w1]; linarith) h2
      exact h.elim hL (fun h => h.elim hB hM)
    · have h := aux2_hit q ha (by dsimp [aux2w0]; linarith)
        (by dsimp [aux2w1,aux1w0] at *; linarith) (by dsimp [aux2w2]; linarith)
      exact h.elim hB (fun h => h.elim hB' hM)
  · rcases hm with hm | hm
    · have h := aux0a_hit q ha (by dsimp [aux0aw0,aux1w2] at *; linarith)
        (by dsimp [aux0aw1]; linarith) (by dsimp [aux0aw2,aux1w2] at *; linarith)
      have hm' : ¬q.Inside 1 (457/500) := by simpa [Owns,marker] using hm
      exact h.elim hm' (fun h => h.elim hB hL)
    · have h := aux0b_hit q ha (by dsimp [aux0bw0,aux1w2] at *; linarith)
        (by dsimp [aux0bw1]; linarith) (by dsimp [aux0bw2]; linarith)
      have hm' : ¬q.Inside (457/500) 1 := by simpa [Owns,marker] using hm
      exact h.elim hm' (fun h => h.elim hB hL)

theorem aux_lower_localization (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hf : AvoidsF q) (hm : ¬Owns q 0 ∨ ¬Owns q 1)
    (hX : centerX q≤2) (hY : centerY q≤2) :
    1<centerX q ∧ 87/50<centerY q := by
  obtain ⟨hx,hy⟩ := aux_avoid_walls q ha hbox hf hm hX hY
  refine ⟨hx,?_⟩
  by_contra he
  exact aux_lower_interior_hit q ha hf hm hx.le hX hy.le (le_of_not_gt he)

theorem aux_central_fan (q : OpenSquare) (ha : 1<q.side) (hf : AvoidsF q)
    (hx0 : 1≤centerX q) (hx1 : centerX q≤2)
    (hy0 : 87/50≤centerY q) (hy1 : centerY q≤113/50) : Owns q 8 := by
  have hL0 : ¬q.Inside 1 (87/50) := by simpa [fPoint] using hf 0
  have hL1 : ¬q.Inside 1 (113/50) := by simpa [fPoint] using hf 1
  have hR0 : ¬q.Inside 2 (87/50) := by simpa [fPoint] using hf 4
  have hR1 : ¬q.Inside 2 (113/50) := by simpa [fPoint] using hf 5
  have hp : q.Inside (33/20) (33/20) := by
    by_cases h1 : 0≤fanTw1 (centerX q) (centerY q)
    · by_cases h2 : 0≤fanTw2 (centerX q) (centerY q)
      · have h := fanT_hit q ha (by dsimp [fanTw0]; linarith) h1 h2
        exact h.resolve_right (not_or.mpr ⟨hL1,hR1⟩)
      · have h := fanL_hit q ha (by dsimp [fanLw0]; linarith)
          (by dsimp [fanLw1,fanTw2] at *; linarith) (by dsimp [fanLw2]; linarith)
        exact h.resolve_right (not_or.mpr ⟨hL0,hL1⟩)
    · have h := fanR_hit q ha (by dsimp [fanRw0]; linarith)
        (by dsimp [fanRw1,fanTw1] at *; linarith) (by dsimp [fanRw2]; linarith)
      exact h.resolve_right (not_or.mpr ⟨hR0,hR1⟩)
  simpa [Owns,marker] using hp

#print axioms aux_lower_localization
#print axioms aux_central_fan
end S12
