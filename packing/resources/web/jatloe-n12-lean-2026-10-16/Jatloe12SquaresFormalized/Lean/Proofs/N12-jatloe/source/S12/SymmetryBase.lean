import S12.Diagonal

/-! Original container-coordinate symmetries, independent of point-cover templates. -/
namespace S12
open S12Pilot
set_option maxHeartbeats 0

def pullX (q : OpenSquare) : OpenSquare where
  c := -q.c
  s := q.s
  loU := q.loU-4*q.c
  loV := -q.loV-q.side-4*q.s
  side := q.side
  unit_normal := by nlinarith [q.unit_normal]
  side_pos := q.side_pos

def pullY (q : OpenSquare) : OpenSquare where
  c := q.c
  s := -q.s
  loU := q.loU-4*q.s
  loV := 4*q.c-q.loV-q.side
  side := q.side
  unit_normal := by nlinarith [q.unit_normal]
  side_pos := q.side_pos

def pullSwap (q : OpenSquare) : OpenSquare where
  c := q.s
  s := q.c
  loU := q.loU
  loV := -q.loV-q.side
  side := q.side
  unit_normal := by nlinarith [q.unit_normal]
  side_pos := q.side_pos

theorem inside_pullX (q : OpenSquare) (x y : ℝ) :
    (pullX q).Inside x y ↔ q.Inside (4-x) y := by
  dsimp [pullX, OpenSquare.Inside, InBands]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;>
    refine ⟨?_,?_,?_,?_⟩ <;> linarith

theorem inside_pullY (q : OpenSquare) (x y : ℝ) :
    (pullY q).Inside x y ↔ q.Inside x (4-y) := by
  dsimp [pullY, OpenSquare.Inside, InBands]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;>
    refine ⟨?_,?_,?_,?_⟩ <;> linarith

theorem inside_pullSwap (q : OpenSquare) (x y : ℝ) :
    (pullSwap q).Inside x y ↔ q.Inside y x := by
  dsimp [pullSwap, OpenSquare.Inside, InBands]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;>
    refine ⟨?_,?_,?_,?_⟩ <;> linarith

structure Transform where
  swap : Bool
  reflectX : Bool
  reflectY : Bool
  deriving DecidableEq, Repr

def Transform.apply (g : Transform) (x y : ℝ) : ℝ × ℝ :=
  let (u,v) := if g.swap then (y,x) else (x,y)
  (if g.reflectX then 4-u else u, if g.reflectY then 4-v else v)

def Transform.pull (g : Transform) (q : OpenSquare) : OpenSquare :=
  let q1 := if g.reflectX then pullX q else q
  let q2 := if g.reflectY then pullY q1 else q1
  if g.swap then pullSwap q2 else q2

@[simp] theorem pull_same_side (g : Transform) (q : OpenSquare) :
    (g.pull q).side = q.side := by
  rcases g with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem inside_pull (g : Transform) (q : OpenSquare) (x y : ℝ) :
    (g.pull q).Inside x y ↔ q.Inside (g.apply x y).1 (g.apply x y).2 := by
  rcases g with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;>
    simp [Transform.pull, Transform.apply, inside_pullX, inside_pullY, inside_pullSwap]

end S12
