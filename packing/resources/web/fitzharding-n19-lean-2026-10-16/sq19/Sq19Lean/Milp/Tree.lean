import Sq19Lean.Milp.Problem

/-!
# Certificate trees

The search tree of milp_cert.c in preorder: `Z k` (indicator `k`, subtree `z_k = 1` then `z_k = 0`),
`S s m` (angle of square `s` split at `m`, lower half first), `E p` (pair `p` has no possible face),
`C y` (certified leaf with sparse multipliers), `F` (failed leaf).

`checkNode` replays it: at every node indicators of faces that cannot separate their pair on the
node's angle box are fixed to `0` (as in `node()`), then the node is checked.
-/
namespace Sq19.Milp

inductive Cert where
  | Z (k : ℕ) (one zero : Cert)
  | S (s : ℕ) (m : ℚ) (lo hi : Cert)
  | E (p : ℕ)
  | C (y : List (ℕ × ℚ))
  | F

def parseRat (t : String) : Option ℚ :=
  match t.splitOn "/" with
  | [a] => a.toInt?.map (fun z => (z : ℚ))
  | [a, b] => do
    let x ← a.toInt?
    let y ← b.toNat?
    if y = 0 then none else some ((x : ℚ) / (y : ℚ))
  | _ => none

def parseYs : ℕ → List String → Option (List (ℕ × ℚ) × List String)
  | 0, ts => some ([], ts)
  | n+1, i :: v :: ts => do
    let i ← i.toNat?
    let v ← parseRat v
    let (rest, ts) ← parseYs n ts
    some ((i, v) :: rest, ts)
  | _, _ => none

def parseCert : ℕ → List String → Option (Cert × List String)
  | 0, _ => none
  | fuel+1, t :: ts =>
    if t = "Z" then
      match ts with
      | k :: ts => do
        let k ← k.toNat?
        let (a, ts) ← parseCert fuel ts
        let (b, ts) ← parseCert fuel ts
        some (.Z k a b, ts)
      | _ => none
    else if t = "S" then
      match ts with
      | s :: m :: ts => do
        let s ← s.toNat?
        let m ← parseRat m
        let (a, ts) ← parseCert fuel ts
        let (b, ts) ← parseCert fuel ts
        some (.S s m a b, ts)
      | _ => none
    else if t = "E" then
      match ts with
      | p :: ts => do
        let p ← p.toNat?
        some (.E p, ts)
      | _ => none
    else if t = "C" then
      match ts with
      | n :: ts => do
        let n ← n.toNat?
        let (ys, ts) ← parseYs n ts
        some (.C ys, ts)
      | _ => none
    else if t = "F" then some (.F, ts)
    else none
  | _, [] => none

def tokens (s : String) : List String :=
  ((s.split (fun c => c = ' ' || c = '\n')).toList.map (fun w => w.toString)).filter (fun w => !w.isEmpty)

def Cert.ofText (s : String) : Option Cert :=
  let ts := tokens s
  match parseCert (ts.length + 1) ts with
  | some (c, []) => some c
  | _ => none

/-- Upper bound of `side19 = 3 + 4√2/3`. -/
def s19hi : ℚ := 4885618083164128/1000000000000000

/-- Everything a node needs that does not change along the tree. -/
structure Ctx where
  P : Prob
  pairs : List Pair
  zinfo : List (ℕ × ℕ)
  rows : List Row

def Ctx.ofProb (P : Prob) : Ctx :=
  let pairs := P.pairs
  ⟨P, pairs, zinfoOf pairs, P.rows⟩

def Ctx.ncol (c : Ctx) : ℕ := 2 * c.P.n + c.zinfo.length

/-- Can option `oi` of pair `p` separate on the angle box `(T, H)`? -/
def Ctx.possible (c : Ctx) (T : Trig) (H : ℕ → ℚ) (p oi : ℕ) : Bool :=
  let pr := c.pairs.getD p Pair.default
  let o := pr.opts.getD oi ⟨false, 0⟩
  let ab := optSqs c.P.sqs pr o
  facePossible T H ab.1 ab.2 o.k

/-- Indicator fixings as data (a function value would be recomputed on every lookup in
compiled code): the first entry for `z` wins. -/
abbrev ZF := List (ℕ × Bool)

def zget (zf : ZF) (z : ℕ) : Option Bool := (zf.find? (fun e => e.1 = z)).map (·.2)

theorem zget_cons (k : ℕ) (b : Bool) (zf : ZF) (z : ℕ) :
    zget ((k, b) :: zf) z = if z = k then some b else zget zf z := by
  unfold zget
  by_cases h : z = k
  · subst h; simp
  · simp [List.find?_cons, Ne.symm h, h]

theorem zget_append_false (imp : List ℕ) (zf : ZF) (z : ℕ) :
    zget (imp.map (fun i => (i, false)) ++ zf) z = if imp.contains z then some false else zget zf z := by
  induction imp with
  | nil => simp
  | cons i imp ih =>
    rw [List.map_cons, List.cons_append, zget_cons, ih]
    by_cases h : z = i
    · subst h; simp
    · simp [h, List.contains_cons, Ne.symm h]

/-- Geometric fixings: free indicators of impossible faces become `0`. -/
def Ctx.fix (c : Ctx) (T : Trig) (H : ℕ → ℚ) (zf : ZF) : ZF :=
  ((List.range c.zinfo.length).filter (fun z =>
    zget zf z = none && !c.possible T H (c.zinfo.getD z (0, 0)).1 (c.zinfo.getD z (0, 0)).2)).map
    (fun i => (i, false)) ++ zf

/-- Column boxes of a node. -/
def Ctx.colBox (c : Ctx) (zfix : ℕ → Option Bool) (j : ℕ) : Iv :=
  if j < 2 * c.P.n then
    (if j % 2 = 0 then (c.P.sq (j / 2)).x else (c.P.sq (j / 2)).y)
  else match zfix (j - 2 * c.P.n) with
    | some true => Iv.pt 1
    | some false => Iv.pt 0
    | none => ⟨0, 1⟩

/-- Pair `p` has no option that is both allowed and possible. -/
def Ctx.emptyPair (c : Ctx) (T : Trig) (H : ℕ → ℚ) (zfix : ℕ → Option Bool) (p : ℕ) : Bool :=
  let pr := c.pairs.getD p Pair.default
  decide (p < c.pairs.length) && decide (1 < pr.opts.length) &&
  (List.range pr.opts.length).all (fun oi =>
    zfix (c.zinfo.idxOf (p, oi)) = some false || !c.possible T H p oi)

def splitLo (ang : ℕ → Iv) (s : ℕ) (m : ℚ) : ℕ → Iv := fun k => if k = s then ⟨(ang k).lo, m⟩ else ang k
def splitHi (ang : ℕ → Iv) (s : ℕ) (m : ℚ) : ℕ → Iv := fun k => if k = s then ⟨m, (ang k).hi⟩ else ang k
def Ctx.check (c : Ctx) (ang : ℕ → Iv) (zf : ZF) : Cert → Bool
  | .Z k one zero =>
    let fz := c.fix (boxTrig ang) (boxH ang) zf
    c.check ang ((k, true) :: fz) one && c.check ang ((k, false) :: fz) zero
  | .S s m lo hi =>
    let fz := c.fix (boxTrig ang) (boxH ang) zf
    c.check (splitLo ang s m) fz lo && c.check (splitHi ang s m) fz hi
  | .E p =>
    let T := boxTrig ang
    let H := boxH ang
    c.emptyPair T H (zget (c.fix T H zf)) p
  | .C y =>
    let T := boxTrig ang
    let H := boxH ang
    leafCheck T H c.rows c.ncol (c.colBox (zget (c.fix T H zf))) s19hi y
  | .F => false

/-- The whole check of a tree: `M` is valid and the tree checks from the root box. -/
def checkTree (P : Prob) (t : Cert) : Bool :=
  P.bigMOk && (Ctx.ofProb P).check P.rootAng [] t

/-- The same for a certificate given as text (milp_cert's CERTOUT format, rationals exact). -/
def checkCert (P : Prob) (text : String) : Bool :=
  match Cert.ofText text with
  | some t => checkTree P t
  | none => false

end Sq19.Milp
