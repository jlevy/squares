import S12.WallRowCover
import S12.TriangleCover
namespace S12
open S12Pilot
set_option maxHeartbeats 0

def permX (i : Marker) : Marker :=
  match i.val with
  | 0 => 2
  | 1 => 3
  | 2 => 0
  | 3 => 1
  | 4 => 6
  | 5 => 7
  | 6 => 4
  | 7 => 5
  | 8 => 9
  | 9 => 8
  | 10 => 11
  | 11 => 10
  | 12 => 14
  | 13 => 13
  | 14 => 12
  | _ => 15
theorem owns_pullX (q : OpenSquare) (i : Marker) :
    Owns (pullX q) i ↔ Owns q (permX i) := by
  fin_cases i <;> norm_num [Owns,marker,permX,inside_pullX]

def permY (i : Marker) : Marker :=
  match i.val with
  | 0 => 6
  | 1 => 7
  | 2 => 4
  | 3 => 5
  | 4 => 2
  | 5 => 3
  | 6 => 0
  | 7 => 1
  | 8 => 11
  | 9 => 10
  | 10 => 9
  | 11 => 8
  | 12 => 12
  | 13 => 15
  | 14 => 14
  | _ => 13
theorem owns_pullY (q : OpenSquare) (i : Marker) :
    Owns (pullY q) i ↔ Owns q (permY i) := by
  fin_cases i <;> norm_num [Owns,marker,permY,inside_pullY]

def permSwap (i : Marker) : Marker :=
  match i.val with
  | 0 => 1
  | 1 => 0
  | 2 => 7
  | 3 => 6
  | 4 => 5
  | 5 => 4
  | 6 => 3
  | 7 => 2
  | 8 => 8
  | 9 => 11
  | 10 => 10
  | 11 => 9
  | 12 => 13
  | 13 => 12
  | 14 => 15
  | _ => 14
theorem owns_pullSwap (q : OpenSquare) (i : Marker) :
    Owns (pullSwap q) i ↔ Owns q (permSwap i) := by
  fin_cases i <;> norm_num [Owns,marker,permSwap,inside_pullSwap]

noncomputable def tri0w0 (X Y : ℝ) : ℝ := (162500/29799)*X+(-184000/29799)*Y+(25/21)
noncomputable def tri0w1 (X Y : ℝ) : ℝ := (-184000/29799)*X+(162500/29799)*Y+(25/21)
noncomputable def tri0w2 (X Y : ℝ) : ℝ := (500/693)*X+(500/693)*Y+(-29/21)
theorem triangle0_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤tri0w0 (centerX q) (centerY q))
    (h1 : 0≤tri0w1 (centerX q) (centerY q))
    (h2 : 0≤tri0w2 (centerX q) (centerY q)) :
    Owns q 0 ∨ Owns q 1 ∨ Owns q 8 := by
  have h := triangle_nonavoidance q ha 1 (457/500) (457/500) 1 (33/20) (33/20)
    (tri0w0 (centerX q) (centerY q)) (tri0w1 (centerX q) (centerY q)) (tri0w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [tri0w0,tri0w1,tri0w2]; ring)
    (by dsimp [tri0w0,tri0w1,tri0w2]; ring)
    (by dsimp [tri0w0,tri0w1,tri0w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)
  simpa [Owns,marker] using h

noncomputable def tri1w0 (X Y : ℝ) : ℝ := (-175/368)*X+-1*Y+(17919/7360)
noncomputable def tri1w1 (X Y : ℝ) : ℝ := (-325/368)*X+1*Y+(-1419/7360)
noncomputable def tri1w2 (X Y : ℝ) : ℝ := (125/92)*X+0*Y+(-457/368)
theorem triangle1_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤tri1w0 (centerX q) (centerY q))
    (h1 : 0≤tri1w1 (centerX q) (centerY q))
    (h2 : 0≤tri1w2 (centerX q) (centerY q)) :
    Owns q 1 ∨ Owns q 12 ∨ Owns q 8 := by
  have h := triangle_nonavoidance q ha (457/500) 1 (457/500) 2 (33/20) (33/20)
    (tri1w0 (centerX q) (centerY q)) (tri1w1 (centerX q) (centerY q)) (tri1w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [tri1w0,tri1w1,tri1w2]; ring)
    (by dsimp [tri1w0,tri1w1,tri1w2]; ring)
    (by dsimp [tri1w0,tri1w1,tri1w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)
  simpa [Owns,marker] using h

noncomputable def tri2w0 (X Y : ℝ) : ℝ := (-125/92)*X+0*Y+(825/368)
noncomputable def tri2w1 (X Y : ℝ) : ℝ := (125/184)*X+(-10/7)*Y+(11521/5152)
noncomputable def tri2w2 (X Y : ℝ) : ℝ := (125/184)*X+(10/7)*Y+(-17919/5152)
theorem triangle2_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤tri2w0 (centerX q) (centerY q))
    (h1 : 0≤tri2w1 (centerX q) (centerY q))
    (h2 : 0≤tri2w2 (centerX q) (centerY q)) :
    Owns q 12 ∨ Owns q 8 ∨ Owns q 11 := by
  have h := triangle_nonavoidance q ha (457/500) 2 (33/20) (33/20) (33/20) (47/20)
    (tri2w0 (centerX q) (centerY q)) (tri2w1 (centerX q) (centerY q)) (tri2w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [tri2w0,tri2w1,tri2w2]; ring)
    (by dsimp [tri2w0,tri2w1,tri2w2]; ring)
    (by dsimp [tri2w0,tri2w1,tri2w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)
  simpa [Owns,marker] using h

noncomputable def tri3w0 (X Y : ℝ) : ℝ := (-10/7)*X+(-10/7)*Y+(40/7)
noncomputable def tri3w1 (X Y : ℝ) : ℝ := (10/7)*X+0*Y+(-33/14)
noncomputable def tri3w2 (X Y : ℝ) : ℝ := 0*X+(10/7)*Y+(-33/14)
theorem triangle3_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤tri3w0 (centerX q) (centerY q))
    (h1 : 0≤tri3w1 (centerX q) (centerY q))
    (h2 : 0≤tri3w2 (centerX q) (centerY q)) :
    Owns q 8 ∨ Owns q 9 ∨ Owns q 11 := by
  have h := triangle_nonavoidance q ha (33/20) (33/20) (47/20) (33/20) (33/20) (47/20)
    (tri3w0 (centerX q) (centerY q)) (tri3w1 (centerX q) (centerY q)) (tri3w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [tri3w0,tri3w1,tri3w2]; ring)
    (by dsimp [tri3w0,tri3w1,tri3w2]; ring)
    (by dsimp [tri3w0,tri3w1,tri3w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)
  simpa [Owns,marker] using h


end S12
