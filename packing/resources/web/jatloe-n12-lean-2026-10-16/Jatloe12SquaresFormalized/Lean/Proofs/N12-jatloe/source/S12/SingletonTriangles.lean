import S12.CenterLocalization
import S12.WallNormalBounds
namespace S12
open S12Pilot
set_option maxHeartbeats 0
set_option Elab.async false

noncomputable def rep0tri0w0 (X Y : ℝ) : ℝ := (125/92)*X+0*Y+(-457/368)
noncomputable def rep0tri0w1 (X Y : ℝ) : ℝ := (-175/368)*X+-1*Y+(17919/7360)
noncomputable def rep0tri0w2 (X Y : ℝ) : ℝ := (-325/368)*X+1*Y+(-1419/7360)
theorem rep0tri0_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri0w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri0w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri0w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 1 ∨ q.Inside (457/500) 2 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (457/500) 1 (457/500) 2
    (rep0tri0w0 (centerX q) (centerY q)) (rep0tri0w1 (centerX q) (centerY q)) (rep0tri0w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri0w0,rep0tri0w1,rep0tri0w2]; ring)
    (by dsimp [rep0tri0w0,rep0tri0w1,rep0tri0w2]; ring)
    (by dsimp [rep0tri0w0,rep0tri0w1,rep0tri0w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep0tri1w0 (X Y : ℝ) : ℝ := (125/184)*X+(-10/7)*Y+(11521/5152)
noncomputable def rep0tri1w1 (X Y : ℝ) : ℝ := (-125/92)*X+0*Y+(825/368)
noncomputable def rep0tri1w2 (X Y : ℝ) : ℝ := (125/184)*X+(10/7)*Y+(-17919/5152)
theorem rep0tri1_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri1w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri1w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri1w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 2 ∨ q.Inside (33/20) (47/20) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (457/500) 2 (33/20) (47/20)
    (rep0tri1w0 (centerX q) (centerY q)) (rep0tri1w1 (centerX q) (centerY q)) (rep0tri1w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri1w0,rep0tri1w1,rep0tri1w2]; ring)
    (by dsimp [rep0tri1w0,rep0tri1w1,rep0tri1w2]; ring)
    (by dsimp [rep0tri1w0,rep0tri1w1,rep0tri1w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep0tri2w0 (X Y : ℝ) : ℝ := (-10/7)*X+(-10/7)*Y+(40/7)
noncomputable def rep0tri2w1 (X Y : ℝ) : ℝ := 0*X+(10/7)*Y+(-33/14)
noncomputable def rep0tri2w2 (X Y : ℝ) : ℝ := (10/7)*X+0*Y+(-33/14)
theorem rep0tri2_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri2w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri2w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri2w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (33/20) (47/20) ∨ q.Inside (47/20) (33/20) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (33/20) (47/20) (47/20) (33/20)
    (rep0tri2w0 (centerX q) (centerY q)) (rep0tri2w1 (centerX q) (centerY q)) (rep0tri2w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri2w0,rep0tri2w1,rep0tri2w2]; ring)
    (by dsimp [rep0tri2w0,rep0tri2w1,rep0tri2w2]; ring)
    (by dsimp [rep0tri2w0,rep0tri2w1,rep0tri2w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep0tri3w0 (X Y : ℝ) : ℝ := (-10/7)*X+(125/184)*Y+(11521/5152)
noncomputable def rep0tri3w1 (X Y : ℝ) : ℝ := (10/7)*X+(125/184)*Y+(-17919/5152)
noncomputable def rep0tri3w2 (X Y : ℝ) : ℝ := 0*X+(-125/92)*Y+(825/368)
theorem rep0tri3_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri3w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri3w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri3w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (47/20) (33/20) ∨ q.Inside 2 (457/500) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (47/20) (33/20) 2 (457/500)
    (rep0tri3w0 (centerX q) (centerY q)) (rep0tri3w1 (centerX q) (centerY q)) (rep0tri3w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri3w0,rep0tri3w1,rep0tri3w2]; ring)
    (by dsimp [rep0tri3w0,rep0tri3w1,rep0tri3w2]; ring)
    (by dsimp [rep0tri3w0,rep0tri3w1,rep0tri3w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep0tri4w0 (X Y : ℝ) : ℝ := (4300/30879)*X+(44000/30879)*Y+(-5424/3431)
noncomputable def rep0tri4w1 (X Y : ℝ) : ℝ := (32500/30879)*X+(-26500/30879)*Y+(-1100/3431)
noncomputable def rep0tri4w2 (X Y : ℝ) : ℝ := (-36800/30879)*X+(-17500/30879)*Y+(9955/3431)
theorem rep0tri4_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri4w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri4w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri4w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside 2 (457/500) ∨ q.Inside (28/25) 1 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 2 (457/500) (28/25) 1
    (rep0tri4w0 (centerX q) (centerY q)) (rep0tri4w1 (centerX q) (centerY q)) (rep0tri4w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri4w0,rep0tri4w1,rep0tri4w2]; ring)
    (by dsimp [rep0tri4w0,rep0tri4w1,rep0tri4w2]; ring)
    (by dsimp [rep0tri4w0,rep0tri4w1,rep0tri4w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep0tri5w0 (X Y : ℝ) : ℝ := 0*X+(20/13)*Y+(-20/13)
noncomputable def rep0tri5w1 (X Y : ℝ) : ℝ := (500/103)*X+(-7360/1339)*Y+(1419/1339)
noncomputable def rep0tri5w2 (X Y : ℝ) : ℝ := (-500/103)*X+(5300/1339)*Y+(1980/1339)
theorem rep0tri5_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep0tri5w0 (centerX q) (centerY q))
    (h1 : 0≤rep0tri5w1 (centerX q) (centerY q))
    (h2 : 0≤rep0tri5w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (28/25) 1 ∨ q.Inside (457/500) 1 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (28/25) 1 (457/500) 1
    (rep0tri5w0 (centerX q) (centerY q)) (rep0tri5w1 (centerX q) (centerY q)) (rep0tri5w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep0tri5w0,rep0tri5w1,rep0tri5w2]; ring)
    (by dsimp [rep0tri5w0,rep0tri5w1,rep0tri5w2]; ring)
    (by dsimp [rep0tri5w0,rep0tri5w1,rep0tri5w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

/-- Excluding the upper four triangles puts the center below both fan rays.
This uses six geometric regions, shared by all three replacement points. -/
private theorem singleton_lower_fan_bounds (q : OpenSquare) (ha : 1 < q.side)
    (hx0 : (457/500) ≤ centerX q) (hx1 : centerX q ≤ 2)
    (hy0 : (457/500) ≤ centerY q) (hy1 : centerY q ≤ 2)
    (hout : ∀ i : Marker, i ≠ 0 → ¬Owns q i) :
    rep0tri0w2 (centerX q) (centerY q) < 0 ∧
    rep0tri3w1 (centerX q) (centerY q) < 0 := by
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho9 : ¬q.Inside (47/20) (33/20) := by
    simpa [Owns, marker] using hout 9 (by decide)
  have ho11 : ¬q.Inside (33/20) (47/20) := by
    simpa [Owns, marker] using hout 11 (by decide)
  have ho12 : ¬q.Inside (457/500) 2 := by
    simpa [Owns, marker] using hout 12 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h0 (h₀ : 0 ≤ rep0tri0w0 (centerX q) (centerY q))
      (h₁ : 0 ≤ rep0tri0w1 (centerX q) (centerY q))
      (h₂ : 0 ≤ rep0tri0w2 (centerX q) (centerY q)) : False :=
    (rep0tri0_hit q ha h₀ h₁ h₂).elim ho8 (fun h => h.elim ho1 ho12)
  have h1 (h₀ : 0 ≤ rep0tri1w0 (centerX q) (centerY q))
      (h₁ : 0 ≤ rep0tri1w1 (centerX q) (centerY q))
      (h₂ : 0 ≤ rep0tri1w2 (centerX q) (centerY q)) : False :=
    (rep0tri1_hit q ha h₀ h₁ h₂).elim ho8 (fun h => h.elim ho12 ho11)
  have h2 (h₀ : 0 ≤ rep0tri2w0 (centerX q) (centerY q))
      (h₁ : 0 ≤ rep0tri2w1 (centerX q) (centerY q))
      (h₂ : 0 ≤ rep0tri2w2 (centerX q) (centerY q)) : False :=
    (rep0tri2_hit q ha h₀ h₁ h₂).elim ho8 (fun h => h.elim ho11 ho9)
  have h3 (h₀ : 0 ≤ rep0tri3w0 (centerX q) (centerY q))
      (h₁ : 0 ≤ rep0tri3w1 (centerX q) (centerY q))
      (h₂ : 0 ≤ rep0tri3w2 (centerX q) (centerY q)) : False :=
    (rep0tri3_hit q ha h₀ h₁ h₂).elim ho8 (fun h => h.elim ho9 ho13)
  dsimp [rep0tri0w0, rep0tri0w1, rep0tri0w2, rep0tri1w0,
    rep0tri1w1, rep0tri1w2, rep0tri2w0, rep0tri2w1, rep0tri2w2,
    rep0tri3w0, rep0tri3w1, rep0tri3w2] at h0 h1 h2 h3 ⊢
  constructor
  · by_contra hL
    have hL := le_of_not_gt hL
    by_cases hx : centerX q ≤ 33/20
    · by_cases hu : 0 ≤ (-175/368)*centerX q - centerY q + 17919/7360
      · exact h0 (by linarith only [hx0]) (by linarith only [hu]) hL
      · exact h1 (by linarith only [hx0, hy1])
          (by linarith only [hx]) (by linarith only [hu])
    · exact h2 (by linarith only [hx1, hy1])
        (by linarith only [hx, hL]) (by linarith only [hx])
  · by_contra hR
    have hR := le_of_not_gt hR
    by_cases hy : centerY q ≤ 33/20
    · exact h3 (by linarith only [hx1, hy0]) hR (by linarith only [hy])
    · by_cases hx : 33/20 ≤ centerX q
      · exact h2 (by linarith only [hx1, hy1])
          (by linarith only [hy]) (by linarith only [hx])
      · exact h1 (by linarith only [hx0, hy1])
          (by linarith only [hx]) (by linarith only [hx, hy, hR])

theorem replacement0_left (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (457/500)≤centerX q) (hx1 : centerX q≤(28/25))
    (hy0 : 1≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (28/25) 1 := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep0tri5w0 (centerX q) (centerY q) := by
    dsimp [rep0tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep0tri5w1 (centerX q) (centerY q) := by
    dsimp [rep0tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep0tri5w2 (centerX q) (centerY q)
  · exact ((rep0tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep0tri4w0 (centerX q) (centerY q) := by
      dsimp [rep0tri4w0, rep0tri5w2] at h5c ⊢
      linarith only [hy0, h5c]
    have h4b : 0 ≤ rep0tri4w1 (centerX q) (centerY q) := by
      dsimp [rep0tri4w1, rep0tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep0tri4w2 (centerX q) (centerY q) := by
      dsimp [rep0tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep0tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

theorem replacement0_right (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (28/25)≤centerX q) (hx1 : centerX q≤2)
    (hy0 : 1≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (28/25) 1 := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep0tri5w0 (centerX q) (centerY q) := by
    dsimp [rep0tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep0tri5w1 (centerX q) (centerY q) := by
    dsimp [rep0tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep0tri5w2 (centerX q) (centerY q)
  · exact ((rep0tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep0tri4w0 (centerX q) (centerY q) := by
      dsimp [rep0tri4w0, rep0tri5w2] at h5c ⊢
      linarith only [hy0, h5c]
    have h4b : 0 ≤ rep0tri4w1 (centerX q) (centerY q) := by
      dsimp [rep0tri4w1, rep0tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep0tri4w2 (centerX q) (centerY q) := by
      dsimp [rep0tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep0tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

noncomputable def rep1tri0w0 (X Y : ℝ) : ℝ := (125/92)*X+0*Y+(-457/368)
noncomputable def rep1tri0w1 (X Y : ℝ) : ℝ := (-175/368)*X+-1*Y+(17919/7360)
noncomputable def rep1tri0w2 (X Y : ℝ) : ℝ := (-325/368)*X+1*Y+(-1419/7360)
theorem rep1tri0_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri0w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri0w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri0w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 1 ∨ q.Inside (457/500) 2 := by
  exact rep0tri0_hit q ha h0 h1 h2

noncomputable def rep1tri1w0 (X Y : ℝ) : ℝ := (125/184)*X+(-10/7)*Y+(11521/5152)
noncomputable def rep1tri1w1 (X Y : ℝ) : ℝ := (-125/92)*X+0*Y+(825/368)
noncomputable def rep1tri1w2 (X Y : ℝ) : ℝ := (125/184)*X+(10/7)*Y+(-17919/5152)
theorem rep1tri1_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri1w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri1w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri1w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 2 ∨ q.Inside (33/20) (47/20) := by
  exact rep0tri1_hit q ha h0 h1 h2

noncomputable def rep1tri2w0 (X Y : ℝ) : ℝ := (-10/7)*X+(-10/7)*Y+(40/7)
noncomputable def rep1tri2w1 (X Y : ℝ) : ℝ := 0*X+(10/7)*Y+(-33/14)
noncomputable def rep1tri2w2 (X Y : ℝ) : ℝ := (10/7)*X+0*Y+(-33/14)
theorem rep1tri2_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri2w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri2w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri2w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (33/20) (47/20) ∨ q.Inside (47/20) (33/20) := by
  exact rep0tri2_hit q ha h0 h1 h2

noncomputable def rep1tri3w0 (X Y : ℝ) : ℝ := (-10/7)*X+(125/184)*Y+(11521/5152)
noncomputable def rep1tri3w1 (X Y : ℝ) : ℝ := (10/7)*X+(125/184)*Y+(-17919/5152)
noncomputable def rep1tri3w2 (X Y : ℝ) : ℝ := 0*X+(-125/92)*Y+(825/368)
theorem rep1tri3_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri3w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri3w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri3w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (47/20) (33/20) ∨ q.Inside 2 (457/500) := by
  exact rep0tri3_hit q ha h0 h1 h2

noncomputable def rep1tri4w0 (X Y : ℝ) : ℝ := (4300/8063)*X+(13000/8063)*Y+(-1862/733)
noncomputable def rep1tri4w1 (X Y : ℝ) : ℝ := (32500/8063)*X+(4500/8063)*Y+(-5550/733)
noncomputable def rep1tri4w2 (X Y : ℝ) : ℝ := (-36800/8063)*X+(-17500/8063)*Y+(8145/733)
theorem rep1tri4_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri4w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri4w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri4w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside 2 (457/500) ∨ q.Inside (87/50) 1 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 2 (457/500) (87/50) 1
    (rep1tri4w0 (centerX q) (centerY q)) (rep1tri4w1 (centerX q) (centerY q)) (rep1tri4w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep1tri4w0,rep1tri4w1,rep1tri4w2]; ring)
    (by dsimp [rep1tri4w0,rep1tri4w1,rep1tri4w2]; ring)
    (by dsimp [rep1tri4w0,rep1tri4w1,rep1tri4w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep1tri5w0 (X Y : ℝ) : ℝ := 0*X+(20/13)*Y+(-20/13)
noncomputable def rep1tri5w1 (X Y : ℝ) : ℝ := (500/413)*X+(-7360/5369)*Y+(1419/5369)
noncomputable def rep1tri5w2 (X Y : ℝ) : ℝ := (-500/413)*X+(-900/5369)*Y+(12210/5369)
theorem rep1tri5_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep1tri5w0 (centerX q) (centerY q))
    (h1 : 0≤rep1tri5w1 (centerX q) (centerY q))
    (h2 : 0≤rep1tri5w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (87/50) 1 ∨ q.Inside (457/500) 1 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (87/50) 1 (457/500) 1
    (rep1tri5w0 (centerX q) (centerY q)) (rep1tri5w1 (centerX q) (centerY q)) (rep1tri5w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep1tri5w0,rep1tri5w1,rep1tri5w2]; ring)
    (by dsimp [rep1tri5w0,rep1tri5w1,rep1tri5w2]; ring)
    (by dsimp [rep1tri5w0,rep1tri5w1,rep1tri5w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

theorem replacement1_left (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (457/500)≤centerX q) (hx1 : centerX q≤(87/50))
    (hy0 : 1≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (87/50) 1 := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep1tri5w0 (centerX q) (centerY q) := by
    dsimp [rep1tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep1tri5w1 (centerX q) (centerY q) := by
    dsimp [rep1tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep1tri5w2 (centerX q) (centerY q)
  · exact ((rep1tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep1tri4w0 (centerX q) (centerY q) := by
      dsimp [rep1tri4w0, rep1tri5w2] at h5c ⊢
      linarith only [hy0, h5c]
    have h4b : 0 ≤ rep1tri4w1 (centerX q) (centerY q) := by
      dsimp [rep1tri4w1, rep1tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep1tri4w2 (centerX q) (centerY q) := by
      dsimp [rep1tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep1tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

theorem replacement1_right (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (87/50)≤centerX q) (hx1 : centerX q≤2)
    (hy0 : 1≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (87/50) 1 := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep1tri5w0 (centerX q) (centerY q) := by
    dsimp [rep1tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep1tri5w1 (centerX q) (centerY q) := by
    dsimp [rep1tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep1tri5w2 (centerX q) (centerY q)
  · exact ((rep1tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep1tri4w0 (centerX q) (centerY q) := by
      dsimp [rep1tri4w0, rep1tri5w2] at h5c ⊢
      linarith only [hy0, h5c]
    have h4b : 0 ≤ rep1tri4w1 (centerX q) (centerY q) := by
      dsimp [rep1tri4w1, rep1tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep1tri4w2 (centerX q) (centerY q) := by
      dsimp [rep1tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep1tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

noncomputable def rep2tri0w0 (X Y : ℝ) : ℝ := (125/92)*X+0*Y+(-457/368)
noncomputable def rep2tri0w1 (X Y : ℝ) : ℝ := (-175/368)*X+-1*Y+(17919/7360)
noncomputable def rep2tri0w2 (X Y : ℝ) : ℝ := (-325/368)*X+1*Y+(-1419/7360)
theorem rep2tri0_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri0w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri0w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri0w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 1 ∨ q.Inside (457/500) 2 := by
  exact rep0tri0_hit q ha h0 h1 h2

noncomputable def rep2tri1w0 (X Y : ℝ) : ℝ := (125/184)*X+(-10/7)*Y+(11521/5152)
noncomputable def rep2tri1w1 (X Y : ℝ) : ℝ := (-125/92)*X+0*Y+(825/368)
noncomputable def rep2tri1w2 (X Y : ℝ) : ℝ := (125/184)*X+(10/7)*Y+(-17919/5152)
theorem rep2tri1_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri1w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri1w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri1w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (457/500) 2 ∨ q.Inside (33/20) (47/20) := by
  exact rep0tri1_hit q ha h0 h1 h2

noncomputable def rep2tri2w0 (X Y : ℝ) : ℝ := (-10/7)*X+(-10/7)*Y+(40/7)
noncomputable def rep2tri2w1 (X Y : ℝ) : ℝ := 0*X+(10/7)*Y+(-33/14)
noncomputable def rep2tri2w2 (X Y : ℝ) : ℝ := (10/7)*X+0*Y+(-33/14)
theorem rep2tri2_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri2w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri2w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri2w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (33/20) (47/20) ∨ q.Inside (47/20) (33/20) := by
  exact rep0tri2_hit q ha h0 h1 h2

noncomputable def rep2tri3w0 (X Y : ℝ) : ℝ := (-10/7)*X+(125/184)*Y+(11521/5152)
noncomputable def rep2tri3w1 (X Y : ℝ) : ℝ := (10/7)*X+(125/184)*Y+(-17919/5152)
noncomputable def rep2tri3w2 (X Y : ℝ) : ℝ := 0*X+(-125/92)*Y+(825/368)
theorem rep2tri3_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri3w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri3w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri3w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (47/20) (33/20) ∨ q.Inside 2 (457/500) := by
  exact rep0tri3_hit q ha h0 h1 h2

noncomputable def rep2tri4w0 (X Y : ℝ) : ℝ := (-7700/7479)*X+(6500/7479)*Y+(1051/831)
noncomputable def rep2tri4w1 (X Y : ℝ) : ℝ := (44500/7479)*X+(11000/7479)*Y+(-10175/831)
noncomputable def rep2tri4w2 (X Y : ℝ) : ℝ := (-36800/7479)*X+(-17500/7479)*Y+(9955/831)
theorem rep2tri4_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri4w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri4w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri4w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside 2 (457/500) ∨ q.Inside (187/100) (19/25) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 2 (457/500) (187/100) (19/25)
    (rep2tri4w0 (centerX q) (centerY q)) (rep2tri4w1 (centerX q) (centerY q)) (rep2tri4w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep2tri4w0,rep2tri4w1,rep2tri4w2]; ring)
    (by dsimp [rep2tri4w0,rep2tri4w1,rep2tri4w2]; ring)
    (by dsimp [rep2tri4w0,rep2tri4w1,rep2tri4w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def rep2tri5w0 (X Y : ℝ) : ℝ := (6000/19951)*X+(23900/19951)*Y+(-29384/19951)
noncomputable def rep2tri5w1 (X Y : ℝ) : ℝ := (16250/19951)*X+(-18400/19951)*Y+(7095/39902)
noncomputable def rep2tri5w2 (X Y : ℝ) : ℝ := (-22250/19951)*X+(-5500/19951)*Y+(91575/39902)
theorem rep2tri5_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤rep2tri5w0 (centerX q) (centerY q))
    (h1 : 0≤rep2tri5w1 (centerX q) (centerY q))
    (h2 : 0≤rep2tri5w2 (centerX q) (centerY q))
    : q.Inside (33/20) (33/20) ∨ q.Inside (187/100) (19/25) ∨ q.Inside (457/500) 1 := by
  exact triangle_nonavoidance q ha (33/20) (33/20) (187/100) (19/25) (457/500) 1
    (rep2tri5w0 (centerX q) (centerY q)) (rep2tri5w1 (centerX q) (centerY q)) (rep2tri5w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [rep2tri5w0,rep2tri5w1,rep2tri5w2]; ring)
    (by dsimp [rep2tri5w0,rep2tri5w1,rep2tri5w2]; ring)
    (by dsimp [rep2tri5w0,rep2tri5w1,rep2tri5w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

theorem replacement2_left (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (457/500)≤centerX q) (hx1 : centerX q≤(187/100))
    (hy0 : 1≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (187/100) (19/25) := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep2tri5w0 (centerX q) (centerY q) := by
    dsimp [rep2tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep2tri5w1 (centerX q) (centerY q) := by
    dsimp [rep2tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep2tri5w2 (centerX q) (centerY q)
  · exact ((rep2tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep2tri4w0 (centerX q) (centerY q) := by
      dsimp [rep2tri4w0, rep2tri5w2] at h5c ⊢
      linarith only [hx1', hy0']
    have h4b : 0 ≤ rep2tri4w1 (centerX q) (centerY q) := by
      dsimp [rep2tri4w1, rep2tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep2tri4w2 (centerX q) (centerY q) := by
      dsimp [rep2tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep2tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

theorem replacement2_right (q : OpenSquare) (ha : 1<q.side)
    (hx0 : (187/100)≤centerX q) (hx1 : centerX q≤2)
    (hy0 : (457/500)≤centerY q) (hy1 : centerY q≤2)
    (hout : ∀ i : Marker, i≠0 → ¬Owns q i) :
    q.Inside (187/100) (19/25) := by
  have hx0' : (457/500) ≤ centerX q := by linarith only [hx0]
  have hx1' : centerX q ≤ 2 := by linarith only [hx1]
  have hy0' : (457/500) ≤ centerY q := by linarith only [hy0]
  obtain ⟨hL, hR⟩ := singleton_lower_fan_bounds q ha hx0' hx1' hy0' hy1 hout
  have ho1 : ¬q.Inside (457/500) 1 := by
    simpa [Owns, marker] using hout 1 (by decide)
  have ho8 : ¬q.Inside (33/20) (33/20) := by
    simpa [Owns, marker] using hout 8 (by decide)
  have ho13 : ¬q.Inside 2 (457/500) := by
    simpa [Owns, marker] using hout 13 (by decide)
  have h5a : 0 ≤ rep2tri5w0 (centerX q) (centerY q) := by
    dsimp [rep2tri5w0]
    linarith only [hx0, hy0]
  have h5b : 0 ≤ rep2tri5w1 (centerX q) (centerY q) := by
    dsimp [rep2tri5w1, rep0tri0w2] at hL ⊢
    linarith only [hL]
  by_cases h5c : 0 ≤ rep2tri5w2 (centerX q) (centerY q)
  · exact ((rep2tri5_hit q ha h5a h5b h5c).resolve_left ho8).resolve_right ho1
  · have h4a : 0 ≤ rep2tri4w0 (centerX q) (centerY q) := by
      dsimp [rep2tri4w0, rep2tri5w2] at h5c ⊢
      linarith only [hx1', hy0']
    have h4b : 0 ≤ rep2tri4w1 (centerX q) (centerY q) := by
      dsimp [rep2tri4w1, rep2tri5w2] at h5c ⊢
      linarith only [h5c]
    have h4c : 0 ≤ rep2tri4w2 (centerX q) (centerY q) := by
      dsimp [rep2tri4w2, rep0tri3w1] at hR ⊢
      linarith only [hR]
    exact ((rep2tri4_hit q ha h4a h4b h4c).resolve_left ho8).resolve_left ho13

end S12
