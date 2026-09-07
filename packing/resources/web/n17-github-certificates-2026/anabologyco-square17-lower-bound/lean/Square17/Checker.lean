/-
Exact checkers for the finite computation layer of the s(17) >= 4.5705 proof.

Everything is unbounded-integer arithmetic (`Int` is GMP-backed). Each checker
returns `Bool`; the theorems in `Theorems.lean` evaluate them by `native_decide`.

Geometry conventions (independently derived; see ../docs/PROOF.md):
- Container C = [0, 9141/2000]^2, atom grid 1/4000, so container = [0,18282]^2
  in grid units and the container center is (9141, 9141).
- Orientation t = tan(theta/2) = p/q gives d = p^2+q^2, cos = (q^2-p^2)/d,
  sin = 2pq/d, all exact rationals.
- In the rotated center frame u = R_{-theta} c, the centers capturing atom a
  form the closed axis-aligned unit square centered at R_{-theta} a; the
  feasible centers form the rotated square ("diamond") image of
  [h, 9141/2000-h]^2, h = (cos+sin)/2. Scaling by 8000000*d^2 makes every
  coordinate an integer.
-/

import Square17.Basic

namespace Square17

def massTarget : Int := 16994734834452
def coverTarget : Int := 1000000000000

/-! ## Certificate arithmetic -/

def weightAt (atoms : Array Atom) (x y : Int) : Int := Id.run do
  for a in atoms do
    if a.x == x && a.y == y then return a.w
  return -1

/-- 560 atoms on the [0,18282]^2 grid, nonnegative weights, no duplicate
coordinates, exact D4 symmetry of the weighted set, exact total mass, and
mass strictly below 17. -/
def certOK (atoms : Array Atom) : Bool := Id.run do
  if atoms.size != 560 then return false
  let mut mass : Int := 0
  for a in atoms do
    if a.w < 0 || a.x < 0 || a.x > 18282 || a.y < 0 || a.y > 18282 then
      return false
    mass := mass + a.w
  if mass != massTarget || mass >= 17 * coverTarget then return false
  -- no duplicate coordinates
  for i in [0:atoms.size] do
    for j in [i+1:atoms.size] do
      if atoms[i]!.x == atoms[j]!.x && atoms[i]!.y == atoms[j]!.y then
        return false
  -- D4 symmetry about the container center, weights constant on orbits
  let k : Int := 18282
  for a in atoms do
    let images := #[(k - a.x, a.y), (a.x, k - a.y), (k - a.x, k - a.y),
                    (a.y, a.x), (k - a.y, a.x), (a.y, k - a.x), (k - a.y, k - a.x)]
    for (gx, gy) in images do
      if weightAt atoms gx gy != a.w then return false
  return true

/-! ## theta = 0 endpoint

Feasible centers are [1/2, 9141/2000 - 1/2]^2 = [2000, 16282]^2 in grid units;
capture squares are atom +- 2000. Every open cell of the edge grid inside the
feasible box must have coverage >= coverTarget (the box itself is the feasible
region, so no separation test is needed). -/

def theta0OK (atoms : Array Atom) : Bool := Id.run do
  let lo : Int := 2000
  let hi : Int := 16282
  let mut xsR : Array Int := #[lo, hi]
  let mut ysR : Array Int := #[lo, hi]
  for a in atoms do
    for e in #[a.x - 2000, a.x + 2000] do
      if lo <= e && e <= hi then xsR := xsR.push e
    for e in #[a.y - 2000, a.y + 2000] do
      if lo <= e && e <= hi then ysR := ysR.push e
  let xs := sortedDedup xsR
  let ys := sortedDedup ysR
  let nx := xs.size - 1
  let ny := ys.size - 1
  for i in [0:nx] do
    -- 1D diff array over ys for this strip
    let mut diff : Array Int := .replicate (ny + 1) 0
    for a in atoms do
      if a.x - 2000 <= xs[i]! && xs[i+1]! <= a.x + 2000 then
        match (if a.y - 2000 <= lo then some 0 else exactIdx ys (a.y - 2000)),
              (if a.y + 2000 >= hi then some ny else exactIdx ys (a.y + 2000)) with
        | some bIdx, some tIdx =>
          if bIdx < tIdx then
            diff := diff.set! bIdx (diff[bIdx]! + a.w)
            diff := diff.set! tIdx (diff[tIdx]! - a.w)
        | _, _ => return false
    let mut cov : Int := 0
    for j in [0:ny] do
      cov := cov + diff[j]!
      if cov < coverTarget then return false
  return true

/-! ## theta = pi/4 endpoint, exact Z[sqrt 2] arithmetic

Frame U = 4000*sqrt(2)*u, V = 4000*sqrt(2)*v: atom capture squares become boxes
with centers (X+Y, Y-X) and half-width 2000*sqrt(2). The feasible diamond has
vertices (4000*sqrt2, 0), (36564-4000*sqrt2, 0), (18282, +-(18282-4000*sqrt2));
its edge normals are (1,+-1). -/

structure Quad where  -- a + b * sqrt 2
  a : Int
  b : Int
deriving Repr, Inhabited

namespace Quad

def add (x y : Quad) : Quad := ⟨x.a + y.a, x.b + y.b⟩
def sub (x y : Quad) : Quad := ⟨x.a - y.a, x.b - y.b⟩
def neg (x : Quad) : Quad := ⟨-x.a, -x.b⟩

def sign (x : Quad) : Int :=
  if x.a == 0 then (if x.b > 0 then 1 else if x.b < 0 then -1 else 0)
  else if x.b == 0 then (if x.a > 0 then 1 else -1)
  else if x.a > 0 && x.b > 0 then 1
  else if x.a < 0 && x.b < 0 then -1
  else
    let a2 := x.a * x.a
    let b2 := 2 * x.b * x.b
    if x.a > 0 then (if a2 > b2 then 1 else -1)
    else (if b2 > a2 then 1 else -1)

def lt (x y : Quad) : Bool := sign (sub x y) < 0
def le (x y : Quad) : Bool := sign (sub x y) <= 0
def qabs (x : Quad) : Quad := if sign x < 0 then neg x else x
def eq (x y : Quad) : Bool := x.a == y.a && x.b == y.b

end Quad

def sortedDedupQ (arr : Array Quad) : Array Quad :=
  let s := arr.qsort Quad.lt
  s.foldl (init := #[]) fun acc v =>
    if acc.isEmpty || !(Quad.eq acc.back! v) then acc.push v else acc

def exactIdxQ (xs : Array Quad) (v : Quad) : Option Nat := Id.run do
  let mut lo : Nat := 0
  let mut hi : Nat := xs.size
  for _ in [0:64] do
    if lo < hi then
      let mid := (lo + hi) / 2
      if Quad.lt xs[mid]! v then lo := mid + 1 else hi := mid
  if lo < xs.size && Quad.eq xs[lo]! v then return some lo
  return none

/-- Separating-axis test: does the closed box [xl,xr]x[yb,yt] meet the closed
endpoint diamond? Axes: U, V, and the diamond normals (1,-1), (1,1). -/
def quarterHits (xl xr yb yt : Quad) : Bool :=
  let ext : Quad := ⟨18282, -4000⟩
  let du := Quad.sub (Quad.add xl xr) ⟨36564, 0⟩   -- 2*(center - diamond center U)
  let dv := Quad.add yb yt                          -- diamond center V = 0
  let w := Quad.sub xr xl
  let h := Quad.sub yt yb
  let ext2 := Quad.add ext ext
  let g1 := Quad.sub (Quad.qabs du) (Quad.add w ext2)
  let g2 := Quad.sub (Quad.qabs dv) (Quad.add h ext2)
  let g3 := Quad.sub (Quad.qabs (Quad.sub du dv)) (Quad.add (Quad.add w h) ext2)
  let g4 := Quad.sub (Quad.qabs (Quad.add du dv)) (Quad.add (Quad.add w h) ext2)
  Quad.sign g1 <= 0 && Quad.sign g2 <= 0 && Quad.sign g3 <= 0 && Quad.sign g4 <= 0

def quarterOK (atoms : Array Atom) : Bool := Id.run do
  let ext : Quad := ⟨18282, -4000⟩
  let minU : Quad := ⟨0, 4000⟩
  let maxU : Quad := ⟨36564, -4000⟩
  let minV : Quad := Quad.neg ext
  let maxV : Quad := ext
  let half : Quad := ⟨0, 2000⟩
  let mut xsR : Array Quad := #[minU, maxU]
  let mut ysR : Array Quad := #[minV, maxV]
  for a in atoms do
    let uc : Quad := ⟨a.x + a.y, 0⟩
    let vc : Quad := ⟨a.y - a.x, 0⟩
    for e in #[Quad.sub uc half, Quad.add uc half] do
      if Quad.le minU e && Quad.le e maxU then xsR := xsR.push e
    for e in #[Quad.sub vc half, Quad.add vc half] do
      if Quad.le minV e && Quad.le e maxV then ysR := ysR.push e
  let xs := sortedDedupQ xsR
  let ys := sortedDedupQ ysR
  let nx := xs.size - 1
  let ny := ys.size - 1
  for i in [0:nx] do
    let mut diff : Array Int := .replicate (ny + 1) 0
    for a in atoms do
      let uc : Quad := ⟨a.x + a.y, 0⟩
      let vc : Quad := ⟨a.y - a.x, 0⟩
      if Quad.le (Quad.sub uc half) xs[i]! && Quad.le xs[i+1]! (Quad.add uc half) then
        let vb := Quad.sub vc half
        let vt := Quad.add vc half
        match (if Quad.le vb minV then some 0 else exactIdxQ ys vb),
              (if Quad.le maxV vt then some ny else exactIdxQ ys vt) with
        | some bIdx, some tIdx =>
          if bIdx < tIdx then
            diff := diff.set! bIdx (diff[bIdx]! + a.w)
            diff := diff.set! tIdx (diff[tIdx]! - a.w)
        | _, _ => return false
    -- walk cells, merge subthreshold runs, separation-test each run
    let mut cov : Int := 0
    let mut runStart : Int := -1
    for j in [0:ny] do
      cov := cov + diff[j]!
      if cov < coverTarget then
        if runStart < 0 then runStart := (j : Int)
      else
        if runStart >= 0 then
          if quarterHits xs[i]! xs[i+1]! ys[runStart.toNat]! ys[j]! then return false
          runStart := -1
    if runStart >= 0 then
      if quarterHits xs[i]! xs[i+1]! ys[runStart.toNat]! ys[ny]! then return false
  return true

/-! ## Interior rational orientations

All coordinates scaled by 8000000*d^2 (d = p^2+q^2), making every capture-square
edge and every diamond datum an exact integer. The diamond's separating axes
are the frame axes and its own edge normals (cos, -sin), (sin, cos). -/

structure Frame where
  c : Int        -- q^2 - p^2  (proportional to cos)
  s : Int        -- 2pq        (proportional to sin)
  cu : Int       -- diamond center u, scaled
  cv : Int
  extent : Int   -- half-extent of the diamond's bounding box, scaled
  proj : Int     -- diamond half-projection on its own edge normals, scaled

/-- Separating-axis test for a box against the rotated feasible square. -/
def sampleHits (f : Frame) (xl xr yb yt : Int) : Bool :=
  let w := xr - xl
  let h := yt - yb
  let du := xl + xr - 2 * f.cu
  let dv := yb + yt - 2 * f.cv
  intAbs du - w - 2 * f.extent <= 0 &&
  intAbs dv - h - 2 * f.extent <= 0 &&
  intAbs (du * f.c - dv * f.s) - (f.proj + w * f.c + h * f.s) <= 0 &&
  intAbs (du * f.s + dv * f.c) - (f.proj + w * f.s + h * f.c) <= 0

/-- The audited property at one exact rational orientation t = p/q:
every feasible center's closed unit square captures weight >= coverTarget.
Preconditions pin 0 < t < sqrt(2)-1. -/
def checkSample (atoms : Array Atom) (p q : Int) : Bool := Id.run do
  if !(0 < p && 0 < q && p * p + 2 * p * q - q * q < 0) then return false
  let d := p * p + q * q
  let c := q * q - p * p
  let s := 2 * p * q
  let sum := c + s
  let dif := c - s
  let tt := 9141 * d - 2000 * sum
  if !(0 < tt && 0 < c && 0 < s && 0 < dif) then return false
  let f : Frame := {
    c := c, s := s
    cu := 18282000 * d * sum
    cv := 18282000 * d * dif
    extent := 2000 * tt * sum
    proj := 4000 * d * d * tt }
  let minU := f.cu - f.extent
  let maxU := f.cu + f.extent
  let minV := f.cv - f.extent
  let maxV := f.cv + f.extent
  -- capture squares, scaled by 8000000*d^2
  let rects : Array (Int × Int × Int × Int × Int) := atoms.map fun a =>
    let au := a.x * c + a.y * s
    let av := -a.x * s + a.y * c
    (2000 * d * (au - 2000 * d), 2000 * d * (au + 2000 * d),
     2000 * d * (av - 2000 * d), 2000 * d * (av + 2000 * d), a.w)
  let mut xsR : Array Int := #[minU, maxU]
  let mut ysR : Array Int := #[minV, maxV]
  for (l, r, b, t, _) in rects do
    if minU <= l && l <= maxU then xsR := xsR.push l
    if minU <= r && r <= maxU then xsR := xsR.push r
    if minV <= b && b <= maxV then ysR := ysR.push b
    if minV <= t && t <= maxV then ysR := ysR.push t
  let xs := sortedDedup xsR
  let ys := sortedDedup ysR
  let nx := xs.size - 1
  let ny := ys.size - 1
  for i in [0:nx] do
    let mut diff : Array Int := .replicate (ny + 1) 0
    for (l, r, b, t, w) in rects do
      if l <= xs[i]! && xs[i+1]! <= r then
        match (if b <= minV then some 0 else exactIdx ys b),
              (if t >= maxV then some ny else exactIdx ys t) with
        | some bIdx, some tIdx =>
          if bIdx < tIdx then
            diff := diff.set! bIdx (diff[bIdx]! + w)
            diff := diff.set! tIdx (diff[tIdx]! - w)
        | _, _ => return false
    let mut cov : Int := 0
    let mut runStart : Int := -1
    for j in [0:ny] do
      cov := cov + diff[j]!
      if cov < coverTarget then
        if runStart < 0 then runStart := (j : Int)
      else
        if runStart >= 0 then
          if sampleHits f xs[i]! xs[i+1]! ys[runStart.toNat]! ys[j]! then return false
          runStart := -1
    if runStart >= 0 then
      if sampleHits f xs[i]! xs[i+1]! ys[runStart.toNat]! ys[ny]! then return false
  return true

/-- Check a batch of samples given as raw "p q" lines; requires the expected
count so a truncated data file cannot pass silently. -/
def checkSamples (atoms : Array Atom) (raw : String) (expected : Nat) : Bool := Id.run do
  let samples := parseSamples raw
  if samples.size != expected then return false
  for (p, q) in samples do
    if !checkSample atoms p q then return false
  return true

end Square17
