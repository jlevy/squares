import Sqpack.FangGlue

/-!
# Fang's theorems from their pieces

K. Fang (note, draft v0.6, 2026-10-13; jlevy/squares#603):

* **Theorem 1.** `s(n² − n + 1) < n` for every `n ≥ 15`.
* **Theorem 2.** For `n ≥ 15` and `16p + 21q ≤ n − 15`, `n² − n + 1 + p + 2q` unit squares pack in side `< n`.

Both follow from the gluing lemma (`FangGlue.glue`) and finitely many packings.  This file proves the reduction:
`FangPieces.theorem2` takes the pieces as hypotheses (`FangPieces`), so it is a statement of the form "if these
packings exist, then so do these".  The pieces themselves are certificates (checked elsewhere).

`Squeezable N a b`: `N` unit squares pack in the `a × b` box shrunk by some `d > 0` in both directions.
`Excess m j`: `Squeezable (m² − m + j) m m`, i.e. `m² − m + j` squares in a square of side `< m`.
-/

namespace UnitSquarePacking.FangGlue

open Set UnitSquarePacking.Conjectures

/-- `N` unit squares pack in `[0, a − d] × [0, b − d]` for some `d > 0`. -/
def Squeezable (N a b : ℕ) : Prop := ∃ d : ℝ, 0 < d ∧ PacksIn N (rect (a - d) (b - d))

/-- `m² − m + j` unit squares pack in a square of side `< m` (with room to spare in both directions). -/
def Excess (m j : ℕ) : Prop := Squeezable (m * m - m + j) m m

/-- Dropping squares. -/
lemma _root_.UnitSquarePacking.Conjectures.PacksIn.drop {N N' : ℕ} {R : Set (ℝ × ℝ)} (h : PacksIn N R)
    (hN : N' ≤ N) : PacksIn N' R := by
  obtain ⟨c, θ, hin, hd⟩ := h
  refine ⟨fun i => c (Fin.castLE hN i), fun i => θ (Fin.castLE hN i), fun i => hin _, fun i j hij => ?_⟩
  exact hd fun h => hij (Fin.castLE_injective hN h)

lemma Squeezable.drop {N N' a b : ℕ} (h : Squeezable N a b) (hN : N' ≤ N) : Squeezable N' a b :=
  let ⟨d, hd, hp⟩ := h; ⟨d, hd, hp.drop hN⟩

lemma Squeezable.shrink {N a b : ℕ} {d : ℝ} (hp : PacksIn N (rect (a - d) (b - d))) {d' : ℝ} (h : d' ≤ d) :
    PacksIn N (rect (a - d') (b - d')) :=
  hp.mono (rect_mono (by linarith) (by linarith))

/-- A packing in a square of side `S < m` is squeezable in the `m × m` box. -/
lemma squeezable_of_packs {N m : ℕ} {S : ℝ} (h : Packs N S) (hS : S < m) : Squeezable N m m :=
  ⟨m - S, by linarith, by rw [show (m : ℝ) - (m - S) = S by ring]; exact h⟩

/-- A packing in `[0, W] × [0, H]` with `W < a`, `H < b` is squeezable in the `a × b` box. -/
lemma squeezable_of_packsIn {N a b : ℕ} {W H : ℝ} (h : PacksIn N (rect W H)) (hW : W < a) (hH : H < b) :
    Squeezable N a b := by
  refine ⟨min (a - W) (b - H), lt_min (by linarith) (by linarith), h.mono (rect_mono ?_ ?_)⟩
  · linarith [min_le_left ((a : ℝ) - W) (b - H)]
  · linarith [min_le_right ((a : ℝ) - W) (b - H)]

/-- `Squeezable N m m` gives `s(N) < m`. -/
lemma Squeezable.packs {N m : ℕ} (h : Squeezable N m m) : ∃ s < (m : ℝ), Packs N s :=
  let ⟨d, hd, hp⟩ := h; ⟨m - d, by linarith, hp⟩

/-- **The gluing step on squeezable pieces**: `A` (`a × b`) top left, `B` (`a' × b'`) bottom right. -/
theorem Squeezable.glue {nA nB a b a' b' : ℕ} (hA : Squeezable nA a b) (hB : Squeezable nB a' b')
    (ha : a ≤ b + b') (ha' : a' ≤ b + b') (hc : b + b' < a + a') (hb : 1 ≤ b) (hb' : 1 ≤ b') :
    Squeezable (nA + nB + (b + b' - a) * b + (b + b' - a') * b') (b + b') (b + b') := by
  obtain ⟨dA, hdA, pA⟩ := hA
  obtain ⟨dB, hdB, pB⟩ := hB
  set d := min (min dA dB) 1 with hd
  have d0 : 0 < d := lt_min (lt_min hdA hdB) one_pos
  have d1 : d ≤ dA := (min_le_left _ _).trans (min_le_left _ _)
  have d2 : d ≤ dB := (min_le_left _ _).trans (min_le_right _ _)
  have d3 : d ≤ 1 := min_le_right _ _
  have hb1 : (1 : ℝ) ≤ b := by exact_mod_cast hb
  have hb1' : (1 : ℝ) ≤ b' := by exact_mod_cast hb'
  have hcR : ((b + b' - a' : ℕ) : ℝ) + d ≤ a := by
    have : b + b' - a' + 1 ≤ a := by omega
    have : ((b + b' - a' : ℕ) : ℝ) + 1 ≤ a := by exact_mod_cast this
    linarith
  refine ⟨d, d0, ?_⟩
  have := UnitSquarePacking.FangGlue.glue d0.le (Squeezable.shrink pA d1) (Squeezable.shrink pB d2) ha ha' hcR (by linarith) (by linarith)
  exact this

/-- One step: glue the `a × b` rectangle `A` of waste `ab − nA` onto a square piece of side `m`. -/
theorem Squeezable.step {nA nB a b m : ℕ} (hA : Squeezable nA a b) (hB : Squeezable nB m m)
    (hab : b < a) (ha : a ≤ b + m) (hb : 1 ≤ b) (hm : 1 ≤ m) :
    Squeezable (nA + nB + (b + m - a) * b + b * m) (b + m) (b + m) := by
  have := hA.glue hB ha (by omega) (by omega) hb hm
  rwa [show b + m - m = b by omega] at this

/-- The pieces Fang's proof uses. -/
structure FangPieces : Prop where
  /-- `R`: 257 squares in the `17 × 16` box, squeezed. -/
  R : Squeezable 257 17 16
  /-- `R'`: 443 squares in the `22 × 21` box, squeezed. -/
  R' : Squeezable 443 22 21
  /-- `r² − r + 1` squares in side `< r` for `r = 15, …, 26`. -/
  base : ∀ r, 15 ≤ r → r ≤ 26 → Excess r 1
  /-- `m² − m` squares in side `< m` for `m = 11, …, 14`. -/
  base0 : ∀ m, 11 ≤ m → m ≤ 14 → Excess m 0

/-- Gluing `R` adds 16 to the side and 1 to the excess. -/
lemma Excess.stepR {m j : ℕ} (hR : Squeezable 257 17 16) (h : Excess m j) (hm : 1 ≤ m) :
    Excess (m + 16) (j + 1) := by
  rw [show m + 16 = 16 + m by ring]
  have := hR.step h (by norm_num) (by omega) (by norm_num) hm
  unfold Excess
  convert this using 1
  · have : m ≤ m * m := Nat.le_mul_self m
    have : 16 + m - 17 = m - 1 := by omega
    rw [this]
    cases m with
    | zero => omega
    | succ k => simp only [Nat.add_sub_cancel]; ring_nf; omega

/-- Gluing `R'` adds 21 to the side and 2 to the excess. -/
lemma Excess.stepR' {m j : ℕ} (hR' : Squeezable 443 22 21) (h : Excess m j) (hm : 1 ≤ m) :
    Excess (m + 21) (j + 2) := by
  rw [show m + 21 = 21 + m by ring]
  have := hR'.step h (by norm_num) (by omega) (by norm_num) hm
  unfold Excess
  convert this using 1
  · have : m ≤ m * m := Nat.le_mul_self m
    have : 21 + m - 22 = m - 1 := by omega
    rw [this]
    cases m with
    | zero => omega
    | succ k => simp only [Nat.add_sub_cancel]; ring_nf; omega

lemma Excess.drop {m j j' : ℕ} (h : Excess m j) (hj : j' ≤ j) : Excess m j' :=
  Squeezable.drop h (by omega)

/-- Excess 1 at every base side `r = 15, …, 30` (`r ≥ 27`: `R` glued to `m² − m`, `m = r − 16`). -/
lemma FangPieces.base' (P : FangPieces) (r : ℕ) (h1 : 15 ≤ r) (h2 : r ≤ 30) : Excess r 1 := by
  by_cases h : r ≤ 26
  · exact P.base r h1 h
  · obtain ⟨m, rfl⟩ : ∃ m, r = m + 16 := ⟨r - 16, by omega⟩
    exact Excess.stepR P.R (P.base0 m (by omega) (by omega)) (by omega)

/-- `p` copies of `R` and `q` of `R'` on a base side `r ∈ [15, 30]`. -/
lemma FangPieces.chain (P : FangPieces) (r : ℕ) (h1 : 15 ≤ r) (h2 : r ≤ 30) :
    ∀ p q : ℕ, Excess (r + 16 * p + 21 * q) (1 + p + 2 * q)
  | 0, 0 => by simpa using P.base' r h1 h2
  | p + 1, 0 => by
    have := Excess.stepR P.R (FangPieces.chain P r h1 h2 p 0) (by omega)
    convert this using 1 <;> ring
  | p, q + 1 => by
    have := Excess.stepR' P.R' (FangPieces.chain P r h1 h2 p q) (by omega)
    convert this using 1 <;> ring

/-- **Theorem 2 (Fang), from its pieces.** -/
theorem FangPieces.theorem2 (P : FangPieces) (n p q : ℕ) (hn : 15 ≤ n) (hpq : 16 * p + 21 * q ≤ n - 15) :
    Excess n (1 + p + 2 * q) := by
  -- n = r + 16 (p + p') + 21 q with r ∈ [15, 30]
  set t := n - 15 - 16 * p - 21 * q
  have h := P.chain (15 + t % 16) (by omega) (by omega) (p + t / 16) q
  have e : 15 + t % 16 + 16 * (p + t / 16) + 21 * q = n := by omega
  rw [e] at h
  exact h.drop (by omega)

/-- **Theorem 1 (Fang), from its pieces.** -/
theorem FangPieces.theorem1 (P : FangPieces) (n : ℕ) (hn : 15 ≤ n) : ∃ s < (n : ℝ), Packs (n * n - n + 1) s :=
  Squeezable.packs (P.theorem2 n 0 0 hn (by omega))

end UnitSquarePacking.FangGlue
