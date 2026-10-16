import Sq19Lean.Milp.Farkas
import Sq19Lean.Milp.Geometry
import Sq19Lean.Basic

/-!
# The certificate problem: data, pairs, rows

Mirrors `build()` in s19/tools/milp_cert.c (without midpoint rows, i.e. runs with `NOMIDROW=1`).

* A square `q` has record centre `(q.rx, q.ry)`, record angle `q.m π/4`, and box: relative angle
  `θ ∈ q.a`, offsets `dx ∈ q.x`, `dy ∈ q.y`. Its centre is `(q.rx + dx, q.ry + dy)` and its angle
  `q.m π/4 + θ`.
* Pairs: included when their centre boxes come within `√2` (`2.0000001` as in the C code);
  options: the faces that the interval face test cannot exclude on the root box, in C's order.
* Rows: four wall rows per vertex pair of axes, four face rows per option (relaxed by `M (1 - z)` when a
  pair has several options), and `Σ z ≥ 1`. Columns: `2i, 2i+1` the offsets of the `i`-th square,
  then one indicator per option of each multi-option pair.
-/
namespace Sq19.Milp

structure Sq where
  s : ℕ
  m : ℕ
  rx : ℚ
  ry : ℚ
  a : Iv
  x : Iv
  y : Iv

def Sq.default : Sq := ⟨0, 0, 0, 0, Iv.pt 0, Iv.pt 0, Iv.pt 0⟩

structure Opt where
  own : Bool
  k : ℕ
deriving DecidableEq

structure Pair where
  i : ℕ
  j : ℕ
  opts : List Opt
deriving DecidableEq

def Pair.default : Pair := ⟨0, 0, []⟩

/-! ## Expressions of the geometry -/

def oxq (j : Fin 4) : ℚ := if j.val = 1 ∨ j.val = 2 then 1/2 else -1/2
def oyq (j : Fin 4) : ℚ := if j.val = 2 ∨ j.val = 3 then 1/2 else -1/2

/-- Vertex offset `R(φ) o_j` of square `q`. -/
def vxE (q : Sq) (j : Fin 4) : Ex := .add (.mul (.c (oxq j)) (.cs q.s q.m)) (.neg (.mul (.c (oyq j)) (.sn q.s q.m)))
def vyE (q : Sq) (j : Fin 4) : Ex := .add (.mul (.c (oxq j)) (.sn q.s q.m)) (.mul (.c (oyq j)) (.cs q.s q.m))

/-- Face normal `k` of square `A`. -/
def nxE (A : Sq) (k : ℕ) : Ex := .cs A.s (A.m + 2*k)
def nyE (A : Sq) (k : ℕ) : Ex := .sn A.s (A.m + 2*k)

/-! ## Face test -/

/-- Exact interval of `c_B - c_A` along one axis. -/
def dIv (rA rB : ℚ) (IA IB : Iv) : Iv := ⟨rB + IB.lo - rA - IA.hi, rB + IB.hi - rA - IA.lo⟩

/-- Can face `k` of `A` separate `B` on the angle box `(T, H)`? (`false` only when it cannot.) -/
def facePossible (T : Trig) (H : ℕ → ℚ) (A B : Sq) (k : ℕ) : Bool :=
  let nx := nxE A k
  let ny := nyE A k
  let proj := (((nx.tf T H).range H).mul (dIv A.rx B.rx A.x B.x)).add
    (((ny.tf T H).range H).mul (dIv A.ry B.ry A.y B.y))
  let P : Ex := .add (.mul nx (.cs B.s B.m)) (.mul ny (.sn B.s B.m))
  let Q : Ex := .add (.neg (.mul nx (.sn B.s B.m))) (.mul ny (.cs B.s B.m))
  let σ1 : ℚ := if 0 ≤ ((P.tf T H).range H).mid then 1 else -1
  let σ2 : ℚ := if 0 ≤ ((Q.tf T H).range H).mid then 1 else -1
  let S : Ex := .add (.mul (.c σ1) P) (.mul (.c σ2) Q)
  let lb := max (1/2) ((((S.tf T H).range H).lo) / 2)
  !decide (proj.hi < 1/2 + lb)

/-- Owner and other square of an option. -/
def optSqs (sqs : List Sq) (pr : Pair) (o : Opt) : Sq × Sq :=
  if o.own then (sqs.getD pr.j Sq.default, sqs.getD pr.i Sq.default)
  else (sqs.getD pr.i Sq.default, sqs.getD pr.j Sq.default)

def optCols (pr : Pair) (o : Opt) : ℕ × ℕ := if o.own then (pr.j, pr.i) else (pr.i, pr.j)

def allOpts : List Opt := ([0,1,2,3].map (fun k => ⟨false, k⟩)) ++ ([0,1,2,3].map (fun k => ⟨true, k⟩))

/-! ## The problem -/

structure Prob where
  sqs : List Sq

def Prob.n (P : Prob) : ℕ := P.sqs.length
def Prob.sq (P : Prob) (i : ℕ) : Sq := P.sqs.getD i Sq.default

/-- Root angle box by square number (a point at `0` off the squares). -/
def Prob.rootAng (P : Prob) (k : ℕ) : Iv :=
  match P.sqs.find? (fun q => q.s = k) with
  | some q => q.a
  | none => Iv.pt 0

/-- Trig table and radii of an angle box (indices `0 .. 19`). -/
def boxTrig (ang : ℕ → Iv) : Trig := Trig.ofCentres (fun k => (ang k).mid) 20
def boxH (ang : ℕ → Iv) : ℕ → ℚ := fun k => (ang k).rad

/-- Minimal distance of an interval from `0`. -/
def ivGap (I : Iv) : ℚ := if 0 < I.lo then I.lo else if I.hi < 0 then -I.hi else 0

def pairNear (A B : Sq) : Bool :=
  let gx := ivGap (dIv A.rx B.rx A.x B.x)
  let gy := ivGap (dIv A.ry B.ry A.y B.y)
  decide (gx^2 + gy^2 < 20000001/10000000)

def Prob.pairs (P : Prob) : List Pair :=
  let T := boxTrig P.rootAng
  let H := boxH P.rootAng
  ((List.range P.n).flatMap (fun i => ((List.range P.n).filter (fun j => i < j)).map (fun j => (i, j)))).filterMap
    (fun ij =>
      let A := P.sq ij.1
      let B := P.sq ij.2
      if pairNear A B then
        some ⟨ij.1, ij.2, allOpts.filter (fun o =>
          let ab := optSqs P.sqs ⟨ij.1, ij.2, []⟩ o
          facePossible T H ab.1 ab.2 o.k)⟩
      else none)

/-- Indicators: one per option of a multi-option pair, in pair order. -/
def zinfoOf (pairs : List Pair) : List (ℕ × ℕ) :=
  (pairs.zipIdx.filter (fun pp => 1 < pp.1.opts.length)).flatMap
    (fun pp => (List.range pp.1.opts.length).map (fun o => (pp.2, o)))

/-- The big M of milp_cert.c. -/
def Prob.bigM (P : Prob) : ℚ :=
  let R := P.sqs.foldl (fun r q => max r (max (max (-q.x.lo) q.x.hi) (max (-q.y.lo) q.y.hi))) 0
  max 4 (282/100 + 283/100 * R)

def wallRowsOf (q : Sq) (i : ℕ) : List Row :=
  (List.finRange 4).flatMap (fun j =>
    [⟨[(2*i, .c (-1))], .add (.c q.rx) (vxE q j), 0⟩,
     ⟨[(2*i, .c 1)], .neg (.add (.c q.rx) (vxE q j)), 1⟩,
     ⟨[(2*i+1, .c (-1))], .add (.c q.ry) (vyE q j), 0⟩,
     ⟨[(2*i+1, .c 1)], .neg (.add (.c q.ry) (vyE q j)), 1⟩])

def optRow (P : Prob) (zinfo : List (ℕ × ℕ)) (M : ℚ) (pr : Pair) (p : ℕ) (o : Opt) (oi : ℕ)
    (j : Fin 4) : Row :=
  let A := (optSqs P.sqs pr o).1
  let B := (optSqs P.sqs pr o).2
  let ca := (optCols pr o).1
  let cb := (optCols pr o).2
  let nx := nxE A o.k
  let ny := nyE A o.k
  let base : List (ℕ × Ex) := [(2*cb, .neg nx), (2*cb+1, .neg ny), (2*ca, nx), (2*ca+1, ny)]
  let b0 : Ex := .add (.add (.add (.mul nx (.c (B.rx - A.rx))) (.mul ny (.c (B.ry - A.ry))))
    (.add (.mul nx (vxE B j)) (.mul ny (vyE B j)))) (.c (-1/2))
  if 1 < pr.opts.length then
    ⟨base ++ [(2*P.n + zinfo.idxOf (p, oi), .c M)], .add b0 (.c M), 0⟩
  else ⟨base, b0, 0⟩

def pairRowsOf (P : Prob) (zinfo : List (ℕ × ℕ)) (M : ℚ) (pr : Pair) (p : ℕ) : List Row :=
  (pr.opts.zipIdx.flatMap (fun oo => (List.finRange 4).map (fun j => optRow P zinfo M pr p oo.1 oo.2 j))) ++
  (if 1 < pr.opts.length then
    [⟨(List.range pr.opts.length).map (fun oi => (2*P.n + zinfo.idxOf (p, oi), Ex.c (-1))), .c (-1), 0⟩]
   else [])

def Prob.rows (P : Prob) : List Row :=
  let pairs := P.pairs
  let zinfo := zinfoOf pairs
  (P.sqs.zipIdx.flatMap (fun qi => wallRowsOf qi.1 qi.2)) ++
  (pairs.zipIdx.flatMap (fun pp => pairRowsOf P zinfo P.bigM pp.1 pp.2))

/-- Check that `M` relaxes every face row of a multi-option pair on the root box. -/
def Prob.bigMOk (P : Prob) : Bool :=
  P.pairs.all (fun pr =>
    let A := P.sq pr.i
    let B := P.sq pr.j
    let gx := (dIv A.rx B.rx A.x B.x).mag
    let gy := (dIv A.ry B.ry A.y B.y).mag
    decide (121/100 ≤ P.bigM ∧ gx^2 + gy^2 ≤ (P.bigM - 121/100)^2))

end Sq19.Milp
