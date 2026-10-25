import S12.MarkerCoverGeometry
import S12.WideWallRow
import S12.TwoHeightWall
namespace S12
open S12Pilot
set_option maxHeartbeats 0

def fPoint (i : Fin 10) : ℚ × ℚ :=
  match i.val with
  | 0 => (1,(87/50))
  | 1 => (1,(113/50))
  | 2 => ((8/5),1)
  | 3 => ((8/5),3)
  | 4 => (2,(87/50))
  | 5 => (2,(113/50))
  | 6 => ((12/5),1)
  | 7 => ((12/5),3)
  | 8 => (3,(87/50))
  | _ => (3,(113/50))
def AvoidsF (q : OpenSquare) : Prop := ∀ i : Fin 10, ¬q.Inside (fPoint i).1 (fPoint i).2

def fPermX (i : Fin 10) : Fin 10 :=
  match i.val with
  | 0 => 8
  | 1 => 9
  | 2 => 6
  | 3 => 7
  | 4 => 4
  | 5 => 5
  | 6 => 2
  | 7 => 3
  | 8 => 0
  | _ => 1
theorem f_owns_pullX (q : OpenSquare) (i : Fin 10) :
    (pullX q).Inside (fPoint i).1 (fPoint i).2 ↔ q.Inside (fPoint (fPermX i)).1 (fPoint (fPermX i)).2 := by
  fin_cases i <;> norm_num [fPoint,fPermX,inside_pullX]
theorem avoidsF_pullX (q : OpenSquare) (h : AvoidsF q) : AvoidsF (pullX q) := by
  intro i hi; exact h (fPermX i) ((f_owns_pullX q i).mp hi)

def fPermY (i : Fin 10) : Fin 10 :=
  match i.val with
  | 0 => 1
  | 1 => 0
  | 2 => 3
  | 3 => 2
  | 4 => 5
  | 5 => 4
  | 6 => 7
  | 7 => 6
  | 8 => 9
  | _ => 8
theorem f_owns_pullY (q : OpenSquare) (i : Fin 10) :
    (pullY q).Inside (fPoint i).1 (fPoint i).2 ↔ q.Inside (fPoint (fPermY i)).1 (fPoint (fPermY i)).2 := by
  fin_cases i <;> norm_num [fPoint,fPermY,inside_pullY]
theorem avoidsF_pullY (q : OpenSquare) (h : AvoidsF q) : AvoidsF (pullY q) := by
  intro i hi; exact h (fPermY i) ((f_owns_pullY q i).mp hi)

noncomputable def aux0aw0 (X Y : ℝ) : ℝ := (-1850/1239)*X+(-500/413)*Y+(4460/1239)
noncomputable def aux0aw1 (X Y : ℝ) : ℝ := (5/3)*X+0*Y+(-5/3)
noncomputable def aux0aw2 (X Y : ℝ) : ℝ := (-215/1239)*X+(500/413)*Y+(-1156/1239)
theorem aux0a_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤aux0aw0 (centerX q) (centerY q))
    (h1 : 0≤aux0aw1 (centerX q) (centerY q))
    (h2 : 0≤aux0aw2 (centerX q) (centerY q)) :
    q.Inside 1 (457/500) ∨ q.Inside (8/5) 1 ∨ q.Inside 1 (87/50) := by
  exact triangle_nonavoidance q ha 1 (457/500) (8/5) 1 1 (87/50)
    (aux0aw0 (centerX q) (centerY q)) (aux0aw1 (centerX q) (centerY q)) (aux0aw2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [aux0aw0,aux0aw1,aux0aw2]; ring)
    (by dsimp [aux0aw0,aux0aw1,aux0aw2]; ring)
    (by dsimp [aux0aw0,aux0aw1,aux0aw2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def aux0bw0 (X Y : ℝ) : ℝ := (-500/343)*X+(-15000/12691)*Y+(44600/12691)
noncomputable def aux0bw1 (X Y : ℝ) : ℝ := (500/343)*X+(-2150/12691)*Y+(-14759/12691)
noncomputable def aux0bw2 (X Y : ℝ) : ℝ := 0*X+(50/37)*Y+(-50/37)
theorem aux0b_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤aux0bw0 (centerX q) (centerY q))
    (h1 : 0≤aux0bw1 (centerX q) (centerY q))
    (h2 : 0≤aux0bw2 (centerX q) (centerY q)) :
    q.Inside (457/500) 1 ∨ q.Inside (8/5) 1 ∨ q.Inside 1 (87/50) := by
  exact triangle_nonavoidance q ha (457/500) 1 (8/5) 1 1 (87/50)
    (aux0bw0 (centerX q) (centerY q)) (aux0bw1 (centerX q) (centerY q)) (aux0bw2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [aux0bw0,aux0bw1,aux0bw2]; ring)
    (by dsimp [aux0bw0,aux0bw1,aux0bw2]; ring)
    (by dsimp [aux0bw0,aux0bw1,aux0bw2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def aux1w0 (X Y : ℝ) : ℝ := -1*X+(20/37)*Y+(196/185)
noncomputable def aux1w1 (X Y : ℝ) : ℝ := 0*X+(-50/37)*Y+(87/37)
noncomputable def aux1w2 (X Y : ℝ) : ℝ := 1*X+(30/37)*Y+(-446/185)
theorem aux1_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤aux1w0 (centerX q) (centerY q))
    (h1 : 0≤aux1w1 (centerX q) (centerY q))
    (h2 : 0≤aux1w2 (centerX q) (centerY q)) :
    q.Inside 1 (87/50) ∨ q.Inside (8/5) 1 ∨ q.Inside 2 (87/50) := by
  exact triangle_nonavoidance q ha 1 (87/50) (8/5) 1 2 (87/50)
    (aux1w0 (centerX q) (centerY q)) (aux1w1 (centerX q) (centerY q)) (aux1w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [aux1w0,aux1w1,aux1w2]; ring)
    (by dsimp [aux1w0,aux1w1,aux1w2]; ring)
    (by dsimp [aux1w0,aux1w1,aux1w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def aux2w0 (X Y : ℝ) : ℝ := (-5/4)*X+(-25/37)*Y+(136/37)
noncomputable def aux2w1 (X Y : ℝ) : ℝ := (5/4)*X+(-25/37)*Y+(-49/37)
noncomputable def aux2w2 (X Y : ℝ) : ℝ := 0*X+(50/37)*Y+(-50/37)
theorem aux2_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤aux2w0 (centerX q) (centerY q))
    (h1 : 0≤aux2w1 (centerX q) (centerY q))
    (h2 : 0≤aux2w2 (centerX q) (centerY q)) :
    q.Inside (8/5) 1 ∨ q.Inside (12/5) 1 ∨ q.Inside 2 (87/50) := by
  exact triangle_nonavoidance q ha (8/5) 1 (12/5) 1 2 (87/50)
    (aux2w0 (centerX q) (centerY q)) (aux2w1 (centerX q) (centerY q)) (aux2w2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [aux2w0,aux2w1,aux2w2]; ring)
    (by dsimp [aux2w0,aux2w1,aux2w2]; ring)
    (by dsimp [aux2w0,aux2w1,aux2w2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def fanLw0 (X Y : ℝ) : ℝ := (20/13)*X+0*Y+(-20/13)
noncomputable def fanLw1 (X Y : ℝ) : ℝ := (-305/169)*X+(-25/13)*Y+(2079/338)
noncomputable def fanLw2 (X Y : ℝ) : ℝ := (45/169)*X+(25/13)*Y+(-1221/338)
theorem fanL_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤fanLw0 (centerX q) (centerY q))
    (h1 : 0≤fanLw1 (centerX q) (centerY q))
    (h2 : 0≤fanLw2 (centerX q) (centerY q)) :
    q.Inside (33/20) (33/20) ∨ q.Inside 1 (87/50) ∨ q.Inside 1 (113/50) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 1 (87/50) 1 (113/50)
    (fanLw0 (centerX q) (centerY q)) (fanLw1 (centerX q) (centerY q)) (fanLw2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [fanLw0,fanLw1,fanLw2]; ring)
    (by dsimp [fanLw0,fanLw1,fanLw2]; ring)
    (by dsimp [fanLw0,fanLw1,fanLw2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def fanTw0 (X Y : ℝ) : ℝ := 0*X+(-100/61)*Y+(226/61)
noncomputable def fanTw1 (X Y : ℝ) : ℝ := -1*X+(35/61)*Y+(429/610)
noncomputable def fanTw2 (X Y : ℝ) : ℝ := 1*X+(65/61)*Y+(-2079/610)
theorem fanT_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤fanTw0 (centerX q) (centerY q))
    (h1 : 0≤fanTw1 (centerX q) (centerY q))
    (h2 : 0≤fanTw2 (centerX q) (centerY q)) :
    q.Inside (33/20) (33/20) ∨ q.Inside 1 (113/50) ∨ q.Inside 2 (113/50) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 1 (113/50) 2 (113/50)
    (fanTw0 (centerX q) (centerY q)) (fanTw1 (centerX q) (centerY q)) (fanTw2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [fanTw0,fanTw1,fanTw2]; ring)
    (by dsimp [fanTw0,fanTw1,fanTw2]; ring)
    (by dsimp [fanTw0,fanTw1,fanTw2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

noncomputable def fanRw0 (X Y : ℝ) : ℝ := (-20/7)*X+0*Y+(40/7)
noncomputable def fanRw1 (X Y : ℝ) : ℝ := (305/91)*X+(-25/13)*Y+(-33/14)
noncomputable def fanRw2 (X Y : ℝ) : ℝ := (-45/91)*X+(25/13)*Y+(-33/14)
theorem fanR_hit (q : OpenSquare) (ha : 1<q.side)
    (h0 : 0≤fanRw0 (centerX q) (centerY q))
    (h1 : 0≤fanRw1 (centerX q) (centerY q))
    (h2 : 0≤fanRw2 (centerX q) (centerY q)) :
    q.Inside (33/20) (33/20) ∨ q.Inside 2 (87/50) ∨ q.Inside 2 (113/50) := by
  exact triangle_nonavoidance q ha (33/20) (33/20) 2 (87/50) 2 (113/50)
    (fanRw0 (centerX q) (centerY q)) (fanRw1 (centerX q) (centerY q)) (fanRw2 (centerX q) (centerY q))
    h0 h1 h2
    (by dsimp [fanRw0,fanRw1,fanRw2]; ring)
    (by dsimp [fanRw0,fanRw1,fanRw2]; ring)
    (by dsimp [fanRw0,fanRw1,fanRw2]; ring)
    (by norm_num) (by norm_num) (by norm_num)

end S12
