import Sqpack.LemmaELeaf

/-!
# A compact encoding of the pair certificates

A leaf's pair certificates are large; as Lean literals of nested constructors they are slow to
elaborate.  Here a certificate is a short list of natural numbers (`chunks`): each holds `512`
digits base `2¹⁶`; the digits form a stream of variable-length numbers (`15` bits per digit, the top
bit marks a continuation), and the numbers are parsed into a `PairCert`.  Nothing here is trusted:
the decoded certificate is what `pairOk` checks.
-/

namespace SquarePacking

namespace LemmaELeaf

open LemmaEVert LemmaEPoly BernZ RatU

/-- `k` digits base `2¹⁶` of `n`, least significant first. -/
def digs : ℕ → ℕ → List ℕ
  | 0, _ => []
  | k + 1, n => n % 65536 :: digs k (n / 65536)

/-- Variable-length numbers: digits `< 2¹⁵` end a number, larger ones continue it. -/
def vnums : List ℕ → ℕ → ℕ → List ℕ
  | [], _, _ => []
  | d :: ds, acc, m =>
    if d < 32768 then (acc + d * m) :: vnums ds 0 1 else vnums ds (acc + (d - 32768) * m) (m * 32768)

def decNums (cs : List ℕ) : List ℕ := vnums (cs.flatMap (digs 512)) 0 1

/-! ### Parsers: `List ℕ → α × List ℕ` -/

def pN : List ℕ → ℕ × List ℕ
  | [] => (0, [])
  | a :: l => (a, l)

def pB (l : List ℕ) : Bool × List ℕ :=
  match pN l with | (a, l) => (a != 0, l)

/-- Zig-zag: `2z` for `z ≥ 0`, `−2z − 1` for `z < 0`. -/
def pZ (l : List ℕ) : ℤ × List ℕ :=
  match pN l with
  | (a, l) => (if a % 2 == 0 then ((a / 2 : ℕ) : ℤ) else -(((a + 1) / 2 : ℕ) : ℤ), l)

def pRep {α : Type} (p : List ℕ → α × List ℕ) : ℕ → List ℕ → List α × List ℕ
  | 0, l => ([], l)
  | n + 1, l =>
    match p l with
    | (a, l1) => match pRep p n l1 with | (as, l2) => (a :: as, l2)

/-- A list: its length, then its entries. -/
def pL {α : Type} (p : List ℕ → α × List ℕ) (l : List ℕ) : List α × List ℕ :=
  match pN l with | (n, l) => pRep p n l

def pPoly (l : List ℕ) : Poly × List ℕ := pL pZ l

def pPL (l : List ℕ) : PL × List ℕ :=
  match pPoly l with
  | (a, l) => match pPoly l with
    | (b, l) => match pPoly l with
      | (c, l) => ((a, b, c), l)

def pN4 (l : List ℕ) : (ℕ × ℕ × ℕ × ℕ) × List ℕ :=
  match pN l with
  | (a, l) => match pN l with
    | (b, l) => match pN l with
      | (c, l) => match pN l with
        | (d, l) => ((a, b, c, d), l)

def pSL (l : List ℕ) : SL × List ℕ :=
  match pPL l with
  | (P, l) => match pN4 l with
    | ((i, j, k, d), l) => (⟨P, i, j, k, d⟩, l)

def pSplit (l : List ℕ) : Split × List ℕ :=
  match pSL l with
  | (q, l) => match pN4 l with
    | ((a, b, c, d), l) => (⟨q, a, b, c, d⟩, l)

def pFC (l : List ℕ) : FCert × List ℕ :=
  match pN l with
  | (k, l) => match pPoly l with
    | (G, l) => match pPoly l with
      | (g, l) => match pN l with
        | (m, l) => (⟨k, G, g, m⟩, l)

def pSegC (l : List ℕ) : SegC × List ℕ :=
  match pN l with
  | (0, l) => (.drop, l)
  | (1, l) => (.box, l)
  | (_, l) => match pL pN l with
    | (U, l) => match pL pN l with
      | (L, l) => (.alt U L, l)

def pTag (l : List ℕ) : Tag × List ℕ :=
  match pN l with
  | (0, l) => (none, l)
  | (_, l) => match pN l with
    | (k, l) => match pB l with
      | (b, l) => (some (k, b), l)

def pSCT (l : List ℕ) : (SegC × Tag) × List ℕ :=
  match pSegC l with
  | (s, l) => match pTag l with
    | (t, l) => ((s, t), l)

def pCapA (l : List ℕ) : CapA × List ℕ :=
  match pN l with
  | (0, l) => (.zeroC, l)
  | (1, l) => match pN l with | (k, l) => (.zeroT k, l)
  | (2, l) => (.par, l)
  | (3, l) => match pN l with
    | (k, l) => match pB l with | (b, l) => (.parT k b, l)
  | (4, l) => (.linC, l)
  | (_, l) => match pN l with | (k, l) => (.linT k, l)

def pLC (l : List ℕ) : (List CapA × List CapA) × List ℕ :=
  match pL pCapA l with
  | (x, l) => match pL pCapA l with
    | (y, l) => ((x, y), l)

def pVCert (l : List ℕ) : VCert × List ℕ :=
  match pL pSplit l with
  | (s, l) => match pL pFC l with
    | (f, l) => match pL (pL pSCT) l with
      | (h, l) => match pL (pL pSCT) l with
        | (v, l) => match pL pLC l with
          | (c, l) => (⟨s, f, h, v, c⟩, l)

def pKind (l : List ℕ) : Kind × List ℕ :=
  match pN l with
  | (0, l) => match pN l with
    | (k, l) => match pN l with | (m, l) => (.out k m, l)
  | (_, l) => match pVCert l with | (c, l) => (.val c, l)

def pSubBin (l : List ℕ) : SubBin × List ℕ :=
  match pN l with
  | (b, l) => match pB l with
    | (s, l) => match pN l with
      | (m, l) => match pKind l with
        | (k, l) => (⟨b, s, m, k⟩, l)

def pPairCert (l : List ℕ) : PairCert × List ℕ :=
  match pN l with
  | (0, l) => (.par, l)
  | (_, l) => match pL pSubBin l with | (s, l) => (.bins s, l)

/-- **The decoder** of an encoded pair certificate. -/
def decPC (cs : List ℕ) : PairCert := (pPairCert (decNums cs)).1

end LemmaELeaf

end SquarePacking
