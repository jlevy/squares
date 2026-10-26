import Sqpack.LemmaL

/-!
# L-blocks: the kernel form of Lemma L and Corollary L (joint bound over lines)

An **L-block** is a set of axis lines, each with

* an up end `a` and a down end `b` (`b ≤ a`, over `Q`), certified at every admissible pose of the box
  for the conditions typed at that end (`admK`), and the *untyped* conditions certified at the ends
  of the range `[b − Δ↓, a + Δ↑]` (the `roles`, two bits per condition: `0` untyped, `1` up, `2` down;
  each typed role must match the slope of the condition along the line, `kend`, and a type-`S`
  condition needs `u₀ > 0`, a type-`C` one `u₁ < 1`);
* pieces: the core `[b, a]`, the up zone `[a, a + Δ↑]` and the down zone `[b − Δ↓, b]`, each piece
  inside a claimed segment of the line (tag of the block), sorted;
* an affine minorant `s x + i` (`s ≥ 0`, `i` signed; *fine units* `1/(W Q)` per `Q`-unit of length)
  of the mass gained at each end, checked piece by piece (`gainOk`); `cap` = the zone's mass.

and, for each of the four corners of the box, a choice of option per end (`0` the cap, `k + 1` the
threshold of condition `k`) and a slack.  The kernel checks, at each corner and for every `u` of the
bin (degree-4 Bernstein, `ratOk`): the slacks (`chosen − other ≤ σ`) and the main inequality
`Σ (chosen − σ) ≥ lg`.  Soundness (`LBlockSound.lean`): at every admissible pose the block's segments
carry `≥ Σ cores + lg / Q` (units of `1/W`).
-/

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

/-- One line of an L-block. -/
structure LLine where
  dir : ℕ
  K : ℕ
  a : ℕ
  b : ℕ
  du : ℕ
  dd : ℕ
  roles : ℕ
  sU : ℕ
  iU : SP
  sD : ℕ
  iD : SP
  up : List (ℕ × ℕ × ℕ)
  core : List (ℕ × ℕ × ℕ)
  dn : List (ℕ × ℕ × ℕ)

/-- An L-block: lines, per-corner choices `(optU, σU, optD, σD)` for each line, the certified gain. -/
structure LBlk where
  lines : List LLine
  corners : List (List (ℕ × ℕ × ℕ × ℕ))
  lg : ℕ

/-- The role of condition `k`. -/
def role (roles k : ℕ) : ℕ := Nat.mod (Nat.div roles (Nat.pow 4 k)) 4

/-- The end at which condition `k` is typed along a line of direction `dir` (`1` up, `2` down),
and its type (`1`: slope `±4u`, `2`: slope `±2(1 − u²)`). -/
def kend (dir k : ℕ) : ℕ :=
  bif Nat.beq dir 0 then (bif Nat.beq (Nat.mod k 2) 0 then 1 else 2)
  else (bif Nat.beq k 0 || Nat.beq k 3 then 1 else 2)
def ktype (dir k : ℕ) : ℕ :=
  bif Nat.beq dir 0 then (bif Nat.blt k 2 then 1 else 2)
  else (bif Nat.blt k 2 then 2 else 1)

/-- The roles are consistent with the geometry. -/
def rolesOk (R U0 U1 dir roles : ℕ) : Bool :=
  (List.range 4).all fun k =>
    (Nat.beq (role roles k) 0 || Nat.beq (role roles k) (kend dir k)) &&
    (Nat.beq (role roles k) 0 ||
      (bif Nat.beq (ktype dir k) 1 then Nat.blt 0 U0 else Nat.blt U1 R))

/-- The line point of coordinate `t` (over `Q`). -/
def lpx (l : LLine) (t : ℕ) : ℕ := lx l.dir l.K t
def lpy (l : LLine) (t : ℕ) : ℕ := ly l.dir l.K t

/-- The typed and untyped certificates of a line. -/
def lcertOk (Q R x0 x1 y0 y1 U0 U1 : ℕ) (l : LLine) : Bool :=
  Nat.ble l.b l.a && Nat.ble l.dd l.b && rolesOk R U0 U1 l.dir l.roles &&
  (List.range 4).all fun k =>
    bif Nat.beq (role l.roles k) 1 then admK Q R x0 x1 y0 y1 U0 U1 (lpx l l.a) (lpy l l.a) k
    else bif Nat.beq (role l.roles k) 2 then admK Q R x0 x1 y0 y1 U0 U1 (lpx l l.b) (lpy l l.b) k
    else admK Q R x0 x1 y0 y1 U0 U1 (lpx l (Nat.sub l.b l.dd)) (lpy l (Nat.sub l.b l.dd)) k &&
      admK Q R x0 x1 y0 y1 U0 U1 (lpx l (Nat.add l.a l.du)) (lpy l (Nat.add l.a l.du)) k

/-- A piece `(j+1, lo, hi)` of a line: inside its claimed segment (tag `tag`), within `[zlo, zhi]`. -/
def lpcOk (S tag : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (zlo zhi : ℕ) (p : ℕ × ℕ × ℕ) : Bool :=
  Nat.beq (cls.getD (Nat.sub p.1 1) ec0).2 tag &&
    onLine S l.dir l.K (cls.getD (Nat.sub p.1 1) ec0).1 &&
    Nat.ble (slo S l.dir (cls.getD (Nat.sub p.1 1) ec0).1) p.2.1 && Nat.ble p.2.1 p.2.2 &&
    Nat.ble p.2.2 (shi S l.dir (cls.getD (Nat.sub p.1 1) ec0).1) &&
    Nat.ble zlo p.2.1 && Nat.ble p.2.2 zhi

/-- Pieces sorted along the line. -/
def psorted : List (ℕ × ℕ × ℕ) → Bool
  | p :: q :: t => Nat.ble p.2.2 q.2.1 && psorted (q :: t)
  | _ => true

/-- The density of a piece's segment, fine units per `Q`-unit, rounded down. -/
def rho (S Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (p : ℕ × ℕ × ℕ) : ℕ :=
  Nat.div (Nat.mul (cls.getD (Nat.sub p.1 1) ec0).1.2.2.2.2 Q)
    (Nat.sub (shi S l.dir (cls.getD (Nat.sub p.1 1) ec0).1) (slo S l.dir (cls.getD (Nat.sub p.1 1) ec0).1))

/-- The mass of a core piece, units of `1/W`, rounded down. -/
def cmass (S : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (p : ℕ × ℕ × ℕ) : ℕ :=
  Nat.div (Nat.mul (cls.getD (Nat.sub p.1 1) ec0).1.2.2.2.2 (Nat.sub p.2.2 p.2.1))
    (Nat.sub (shi S l.dir (cls.getD (Nat.sub p.1 1) ec0).1) (slo S l.dir (cls.getD (Nat.sub p.1 1) ec0).1))

/-- `s X + i ≤ C` in signed integers. -/
def ellLe (s : ℕ) (i : SP) (X C : ℕ) : Bool := sle0 (ssub (sadd (Nat.mul s X, 0) i) (C, 0))

/-- **The gain check**: for pieces at distances `[o₀, o₁] ⊆ [0, Δ]` from the end (sorted), with
densities `ρ`, the minorant is below the gain at every breakpoint.  Returns the zone's mass (the cap)
if the check passes. -/
def gainOk (s : ℕ) (i : SP) (D : ℕ) : ℕ → List (ℕ × ℕ × ℕ) → Bool
  | C, [] => ellLe s i D C
  | C, (r, o0, o1) :: t => ellLe s i o0 C && ellLe s i o1 (Nat.add C (Nat.mul r (Nat.sub o1 o0))) &&
      gainOk s i D (Nat.add C (Nat.mul r (Nat.sub o1 o0))) t

def gainSum : ℕ → List (ℕ × ℕ × ℕ) → ℕ
  | C, [] => C
  | C, (r, o0, o1) :: t => gainSum (Nat.add C (Nat.mul r (Nat.sub o1 o0))) t

/-- The up zone at distances from `a`, the down zone (reversed) at distances from `b`. -/
def upOff (S Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : List (ℕ × ℕ × ℕ) :=
  l.up.map fun p => (rho S Q cls l p, Nat.sub p.2.1 l.a, Nat.sub p.2.2 l.a)
def dnOff (S Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : List (ℕ × ℕ × ℕ) :=
  (l.dn.map fun p => (rho S Q cls l p, Nat.sub l.b p.2.2, Nat.sub l.b p.2.1)).reverse

/-- The piece checks of a line. -/
def lpcsOk (S Q tag : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : Bool :=
  l.up.all (lpcOk S tag cls l l.a (Nat.add l.a l.du)) && psorted l.up &&
  l.core.all (lpcOk S tag cls l l.b l.a) && psorted l.core &&
  l.dn.all (lpcOk S tag cls l (Nat.sub l.b l.dd) l.b) && psorted l.dn &&
  gainOk l.sU l.iU l.du 0 (upOff S Q cls l) && gainOk l.sD l.iD l.dd 0 (dnOff S Q cls l)

def capU (S Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : ℕ := gainSum 0 (upOff S Q cls l)
def capD (S Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : ℕ := gainSum 0 (dnOff S Q cls l)
def coreVal (S : ℕ) (cls : List (SegE × ℕ)) (l : LLine) : ℕ := (l.core.map (cmass S cls l)).sum

/-! ### Options at a corner -/

/-- `σ̂` as a quadratic in `v`: `4Rv` (type 1), `2(R² − v²)` (type 2). -/
def sigq (R f : ℕ) : SP × SP × SP :=
  bif Nat.beq f 1 then ((0, 0), (Nat.mul 4 R, 0), (0, 0)) else ((Nat.mul 2 (Nat.mul R R), 0), (0, 0), (0, 2))

/-- The numerator `N = i σ̂ − s Ĝ_k` of the option `k` at the corner `(cx, cy)`, for the end point
`t` (over `Q`) of the line. -/
def optN (Q R : ℕ) (l : LLine) (s : ℕ) (i : SP) (t k cx cy : ℕ) : SP × SP × SP :=
  (ssub (smul i (sigq R (ktype l.dir k)).1)
      (sk s (gq Q R k (lpx l t, cx) (lpy l t, cy)).1),
    ssub (smul i (sigq R (ktype l.dir k)).2.1) (sk s (gq Q R k (lpx l t, cx) (lpy l t, cy)).2.1),
    ssub (smul i (sigq R (ktype l.dir k)).2.2) (sk s (gq Q R k (lpx l t, cx) (lpy l t, cy)).2.2))

/-- An option of an end, as `(type, N)` (type `0`: the cap, a constant). -/
def optT (Q R : ℕ) (l : LLine) (up : Bool) (cap o cx cy : ℕ) : ℕ × (SP × SP × SP) :=
  bif Nat.beq o 0 then (0, ((cap, 0), (0, 0), (0, 0)))
  else (ktype l.dir (Nat.sub o 1),
    bif up then optN Q R l l.sU l.iU l.a (Nat.sub o 1) cx cy
    else optN Q R l l.sD l.iD l.b (Nat.sub o 1) cx cy)

/-- Is `o` an option of the end (the cap, or a condition typed at that end)? -/
def isOpt (l : LLine) (up : Bool) (o : ℕ) : Bool :=
  Nat.beq o 0 || (Nat.ble o 4 && Nat.beq (role l.roles (Nat.sub o 1)) (bif up then 1 else 2))

/-- The term of an option in a sum over the common denominator `f` (`f ⊇` the option's type). -/
def term (R f : ℕ) (t : ℕ × (SP × SP × SP)) : P5 :=
  bif Nat.beq t.1 0 then cmul f R t.2.1 else tmul (Nat.sub f t.1) R t.2

/-- Type union on `{0, 1, 2, 3}` (bit sets: `1 ∪ 2 = 3`). -/
def tor (a b : ℕ) : ℕ :=
  bif Nat.beq a 0 then b else bif Nat.beq b 0 then a else bif Nat.beq a b then a else 3

/-- Slack check: `chosen − other − σ ≤ 0` for all `u` in the bin, at the corner. -/
def slackOk (Q R U0 U1 : ℕ) (l : LLine) (up : Bool) (cap ch σ cx cy : ℕ) (o : ℕ) : Bool :=
  bOk5 (p5add (p5add (term R (tor (optT Q R l up cap ch cx cy).1 (optT Q R l up cap o cx cy).1)
      (optT Q R l up cap ch cx cy))
    (p5neg (term R (tor (optT Q R l up cap ch cx cy).1 (optT Q R l up cap o cx cy).1)
      (optT Q R l up cap o cx cy))))
    (p5neg (cmul (tor (optT Q R l up cap ch cx cy).1 (optT Q R l up cap o cx cy).1) R (σ, 0)))) U0 U1

/-- The end's slacks, over all options. -/
def endOk (Q R U0 U1 : ℕ) (l : LLine) (up : Bool) (cap ch σ cx cy : ℕ) : Bool :=
  isOpt l up ch && (List.range 5).all fun o => !isOpt l up o || slackOk Q R U0 U1 l up cap ch σ cx cy o


/-- The common denominator of the chosen options at a corner. -/
def mainF (Q R S : ℕ) (cls : List (SegE × ℕ)) (cx cy : ℕ) :
    List (LLine × (ℕ × ℕ × ℕ × ℕ)) → ℕ
  | [] => 0
  | (l, c) :: t => tor (tor (optT Q R l true (capU S Q cls l) c.1 cx cy).1
      (optT Q R l false (capD S Q cls l) c.2.2.1 cx cy).1) (mainF Q R S cls cx cy t)

/-- The sum of the chosen options' terms and of the slacks. -/
def mainP (Q R S f : ℕ) (cls : List (SegE × ℕ)) (cx cy : ℕ) :
    List (LLine × (ℕ × ℕ × ℕ × ℕ)) → P5 × ℕ
  | [] => ((z0, z0, z0, z0, z0), 0)
  | (l, c) :: t =>
    (p5add (p5add (term R f (optT Q R l true (capU S Q cls l) c.1 cx cy))
        (term R f (optT Q R l false (capD S Q cls l) c.2.2.1 cx cy))) (mainP Q R S f cls cx cy t).1,
      Nat.add (Nat.add c.2.1 c.2.2.2) (mainP Q R S f cls cx cy t).2)

/-- **The corner check**: every end's slacks, and `Σ (chosen − σ) ≥ lg` for all `u` in the bin. -/
def cornerOk (Q R S U0 U1 : ℕ) (cls : List (SegE × ℕ)) (lg cx cy : ℕ)
    (lc : List (LLine × (ℕ × ℕ × ℕ × ℕ))) : Bool :=
  lc.all (fun lcx => endOk Q R U0 U1 lcx.1 true (capU S Q cls lcx.1) lcx.2.1 lcx.2.2.1 cx cy &&
    endOk Q R U0 U1 lcx.1 false (capD S Q cls lcx.1) lcx.2.2.2.1 lcx.2.2.2.2 cx cy) &&
  bOk5 (p5neg (p5add (mainP Q R S (mainF Q R S cls cx cy lc) cls cx cy lc).1
    (p5neg (cmul (mainF Q R S cls cx cy lc) R
      (Nat.add (mainP Q R S (mainF Q R S cls cx cy lc) cls cx cy lc).2 lg, 0))))) U0 U1

/-- Lines strictly increasing in `(dir, K)`: distinct lines. -/
def lsorted : List LLine → Bool
  | l :: m :: t => (Nat.blt l.dir m.dir || (Nat.beq l.dir m.dir && Nat.blt l.K m.K)) && lsorted (m :: t)
  | _ => true

/-- **The L-block check.** -/
def lblkOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (cls : List (SegE × ℕ)) (tag : ℕ) (B : LBlk) : Bool :=
  lsorted B.lines &&
  B.lines.all (fun l => Nat.ble l.dir 1 && lcertOk Q R x0 x1 y0 y1 U0 U1 l && lpcsOk S Q tag cls l) &&
  Nat.beq B.corners.length 4 &&
  B.corners.all (fun c => Nat.beq c.length B.lines.length) &&
  cornerOk Q R S U0 U1 cls B.lg x0 y0 (B.lines.zip (B.corners.getD 0 [])) &&
  cornerOk Q R S U0 U1 cls B.lg x0 y1 (B.lines.zip (B.corners.getD 1 [])) &&
  cornerOk Q R S U0 U1 cls B.lg x1 y0 (B.lines.zip (B.corners.getD 2 [])) &&
  cornerOk Q R S U0 U1 cls B.lg x1 y1 (B.lines.zip (B.corners.getD 3 []))

/-- **The L-block value** (units of `1/W`): the cores plus the certified gain. -/
def lblkVal (S Q : ℕ) (cls : List (SegE × ℕ)) (B : LBlk) : ℕ :=
  (B.lines.map (coreVal S cls)).sum + Nat.div B.lg Q

end ZMTreeM

end SquarePacking
