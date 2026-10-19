import PackingCertMathlib.Crowd
import PackingCertMathlib.Statements.Open.LemmaCEIL

/-!
# -- OPEN: Lemma FLUSH (n-general), Conjecture CLICK-DOWN and Theorem FOUR-WALL (A223)

`docs/proofs/two_grains.md`.  The PI's picture (2026-09-14, 21:10): a self-supporting k0 structure is
two opposite-handed grains with boundaries on all four walls; the grain-level CLICK-DOWN (every grain
rotating toward its axis alignment) beats it, because a FLUSH packing of `n` unit squares has side
`≥ ⌈√n⌉`.

**Lemma FLUSH** (`two_grains.md` §3.1, any `n`, [T] in prose).  A packing of `n` AXIS-ALIGNED unit
squares in `[0, s]²` has `s ≥ ⌈√n⌉`.  Proof: with `k = ⌈√n⌉` and `s < k`, the bottom edges `b_i ∈ [0, s−1]
⊂ [0, k−1)` fall into the `k − 1` classes `[j, j+1)`, `j < k − 1`; squares of one class overlap in `y`,
so their `x`-intervals are interior-disjoint unit intervals in `[0, s]`, at most `⌊s⌋ ≤ k − 1` of them;
hence `n ≤ (k − 1)² < n`.  Stated here as the axiom `lemma_FLUSH`; the `n = 11` corollary
`flush_eleven_four` (`4 ≤ s`) is proved from it with `ceil_sqrt_eleven` (`LemmaCEIL.lean`).

**Conjecture CLICK-DOWN** (`two_grains.md` §3.2, [C]).  Every TELEPORT-STUCK packing (every corner's
open unit box met by ≥ 2 squares — the hypothesis under which no K0-FREE teleport settles a corner)
clicks down to a flush packing at a side no larger than its own: there is a flush packing at some
`m' ≤ m`.  Measured on the ring `rand_0_0569|t20` and on all 193 four-crowd witnesses of A217
(`attempts/A223-two-grains/results/click223.md`): the joint tilt path with the fixed-tilt side
minimised at every step reaches the flush side 4.000 from every witness, monotonically in the free
variant; it is NOT a theorem — the chain formula of a grain need not decrease toward alignment
(the corner-anchored ladder `Λ(θ) = 2 + 4t/(t² + 1)` INCREASES from 45° to 0°, `two_grains.md` §2.3),
and the path's monotonicity is what would have to be proved.

**Theorem FOUR-WALL** (`two_grains.md` §3.3): CLICK-DOWN + FLUSH ⇒ every teleport-stuck packing of 11
squares has side `≥ 4`; in particular none exists in the window `[3.82, ŝ]` (`no_stuck_in_window`).
Pure logic over the two statements above.  Lemma TWO-GRAIN and Conjecture SEAM are prose over the
Fritz-John multipliers (`two_grains.md` §1, §4) and have no object in the readable layer.

**Status (2026-09-14).**  `lemma_FLUSH`: axiom [T-prose]; `flush_eleven_four`, `four_wall`,
`no_stuck_in_window`: theorems; `click_down`: axiom [C].
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- An axis-aligned closed unit square (a slot box at some centre). -/
def IsFlatSquare (Q : Set RP) : Prop := ∃ c : RP, Q = slotBox c

/-- Square `i` of `z` MEETS the open unit corner box of corner `c` at side `m`. -/
def MeetsCorner (m : ℝ) (z : Cfg) (c : Fin 4) (i : Fin 11) : Prop :=
  ¬ Disjoint (interior (cornerBox m 1 c)) (interior (z i).set)

/-- TELEPORT-STUCK: every corner box is met by two distinct squares (K0-FREE′). -/
def TeleportStuck (m : ℝ) (z : Cfg) : Prop :=
  ∀ c : Fin 4, ∃ i j : Fin 11, i ≠ j ∧ MeetsCorner m z c i ∧ MeetsCorner m z c j

/-- **[OPEN] Lemma FLUSH.**  A packing of `n` axis-aligned unit squares has side `≥ ⌈√n⌉`. -/
axiom lemma_FLUSH (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hflat : ∀ i, IsFlatSquare (Q i)) :
    ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ) ≤ s

/-- **Corollary (n = 11).**  Eleven flat unit squares need side `4`. -/
theorem flush_eleven_four (s : ℝ) (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q)
    (hflat : ∀ i, IsFlatSquare (Q i)) : (4 : ℝ) ≤ s := by
  have h := lemma_FLUSH 11 s Q hP hflat
  rw [ceil_sqrt_eleven] at h
  exact_mod_cast h

/-- **[OPEN] Conjecture CLICK-DOWN.**  A teleport-stuck packing clicks down to a flush packing at a
side no larger than its own. -/
axiom click_down (m : ℝ) (z : Cfg) (hz : CfgPacking m z) (hstuck : TeleportStuck m z) :
    ∃ m' : ℝ, m' ≤ m ∧ ∃ Q : Fin 11 → Set RP, IsPacking 11 m' Q ∧ ∀ i, IsFlatSquare (Q i)

/-- **Theorem FOUR-WALL** (conditional on CLICK-DOWN): a teleport-stuck packing of eleven squares
has side `≥ 4`. -/
theorem four_wall (m : ℝ) (z : Cfg) (hz : CfgPacking m z) (hstuck : TeleportStuck m z) :
    (4 : ℝ) ≤ m := by
  obtain ⟨m', hm', Q, hQ, hflat⟩ := click_down m z hz hstuck
  exact le_trans (flush_eleven_four m' Q hQ hflat) hm'

/-- No teleport-stuck packing below side 4 — in particular none in the window `[3.82, ŝ]`. -/
theorem no_stuck_in_window (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z) :
    ¬ TeleportStuck m z :=
  fun h => absurd (four_wall m z hz h) (not_le.mpr hm)

#print axioms lemma_FLUSH
#print axioms flush_eleven_four
#print axioms click_down
#print axioms four_wall
#print axioms no_stuck_in_window

end PackingCert.S11.OpenLemmas
