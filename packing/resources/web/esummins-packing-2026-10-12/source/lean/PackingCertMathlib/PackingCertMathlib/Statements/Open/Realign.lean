import PackingCertMathlib.Crowd
import PackingCertMathlib.Selection
import PackingCertMathlib.Statements.Open.LemmaCEIL
import PackingCertMathlib.Statements.Open.TwoGrains
import PackingCertMathlib.Statements.Open.OneFlush
import PackingCertMathlib.Statements.Open.LemmaEps

/-!
# -- OPEN: Lemma REALIGN (n-general), Lemma WALL-EXCESS, and what they close (A231)

`docs/proofs/realign.md`.  The PI (2026-09-15, 09:50 / 10:05): the only exclusion of a four-crowd is an
IMPROVEMENT -- settle one corner (CORNER-SWAP: the two meeters become the slot square `S` and one leftover),
then the grain in contact with `S` re-aligns toward `S`'s alignment and the side drops below the start; each
non-flush corner belongs to a grain, so some grain can be drained to flush at a profit, the profit being the
wall wastage the grain's tilted members leave along their wall.

**Conjecture REALIGN(n)** (`realign.md` §2, [C]).  Let `s < ⌈√n⌉`, `Q` a FOUR-CROWD at side `s` (every corner
box met by two squares, `FourCrowdN`) and `Q'` a CORNER-SWAP of `Q` (a packing at the same side agreeing with
`Q` off two indices and containing the slot square of a corner, `CornerSwapped`).  Then `n` squares pack at
some side `s' < s`.  The tested mechanism (`attempts/A231-realign/results/realign231.md`): the SHRINK
(fixed-tilt side minimum with `S` pinned) already lowers the side strictly on every corner-swapped witness
(193 four-crowds + the 40 window-over-met ones + A226's eight CROWD-ABOVE crowds), and the anchored
re-alignment of the grain touching `S` adds nothing on top of it -- that grain is empty or unloaded on the
witnesses.  The axiom is therefore the improvement statement, not the path: it is UNCROWD(n) restricted to
four-crowds that admit a swap.

**Theorem** `one_flush_of_realign`: REALIGN + STEP (every four-crowd below `⌈√n⌉` admits a corner swap,
`ring_swap.md` §2.1, [C] = RAISE(0 → 1) on four-crowds) ⇒ every optimal packing below `⌈√n⌉` has a singly-met
corner -- ONE-FLUSH(n) with its proof mechanism named.  **Theorem** `fourcrowd_dead_of_step_kill` (pure logic, no
axiom): at any side where no packing contains a corner slot square (the k1-a kill of the k1_00 tree at
`n = 11`, `m < ŝ`), a four-crowd with a corner swap cannot exist -- so at `n = 11` the k0_00 obligation on
`[3.82, ŝ)` needs STEP alone, not REALIGN; REALIGN is what ONE-FLUSH needs at general `n`.

**Lemma WALL-EXCESS** (`realign.md` §1, [T] in prose, `wall_budget.md` §1.1 Lemma WALL-F specialised).  The
squares touching a wall have interior chords `1 / max(cos θ_i, sin θ_i) ≥ 1` on the line at distance `1/√2`
from the wall, pairwise disjoint inside the container: their sum is `≤ s`, and each term is `1` only for a flush
square.  Stated here for the floor (`TouchesFloor`), tilts as `t = tan(θ/2) ∈ [0, 1]` (`cosT`, `sinT`); the
corollary `wall_count_le` (`k ≤ s` floor-touchers) is proved from it.  The sealed-pocket area statement of
`realign.md` §1.2 is prose only.

**Status (2026-09-15).**  `realign`, `lemma_WALL_EXCESS`: axioms; `one_flush_of_realign`,
`fourcrowd_dead_of_step_kill`, `chordT_ge_one`, `wall_count_le`: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- A FOUR-CROWD (n-general): no corner is singly met. -/
def FourCrowdN (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) : Prop :=
  ∀ c : Fin 4, ¬ SinglyMet s Q c

/-- CORNER-SWAP at corner `c`: `Q'` is a packing at the same side, agrees with `Q` off two indices (the
two meeters), and one of its squares is the corner's slot square `cornerBox s 1 c`. -/
def CornerSwapped (s : ℝ) {n : ℕ} (Q Q' : Fin n → Set RP) (c : Fin 4) : Prop :=
  IsPacking n s Q' ∧ (∃ i j : Fin n, i ≠ j ∧ ∀ k, k ≠ i → k ≠ j → Q' k = Q k) ∧
    ∃ k : Fin n, Q' k = cornerBox s 1 c

/-- **[OPEN] Conjecture REALIGN.**  A corner-swapped four-crowd below `⌈√n⌉` improves: `n` squares pack at a
strictly smaller side. -/
axiom realign (n : ℕ) (s : ℝ) (Q Q' : Fin n → Set RP)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ))
    (hP : IsPacking n s Q) (hcrowd : FourCrowdN s Q) (c : Fin 4) (hsw : CornerSwapped s Q Q' c) :
    ∃ s' : ℝ, s' < s ∧ Fits n s'

/-- **ONE-FLUSH from REALIGN + STEP.**  If every four-crowd below `⌈√n⌉` admits a corner swap (`step`), then
every optimal packing below `⌈√n⌉` has a singly-met corner. -/
theorem one_flush_of_realign (n : ℕ)
    (step : ∀ (s : ℝ) (Q : Fin n → Set RP), s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ) →
      IsPacking n s Q → FourCrowdN s Q → ∃ (Q' : Fin n → Set RP) (c : Fin 4), CornerSwapped s Q Q' c)
    (s : ℝ) (Q : Fin n → Set RP) (hopt : IsOptimalPacking n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ c : Fin 4, SinglyMet s Q c := by
  by_contra hno
  have hcrowd : FourCrowdN s Q := fun c hc => hno ⟨c, hc⟩
  obtain ⟨Q', c, hsw⟩ := step s Q hs hopt.1 hcrowd
  obtain ⟨s', hlt, hfit⟩ := realign n s Q Q' hs hopt.1 hcrowd c hsw
  exact absurd (hopt.2 s' hfit) (not_le.mpr hlt)

/-- **The n = 11 value route needs STEP only.**  At a side where no packing contains a corner slot square
(the k1-a kill), a four-crowd admitting a corner swap does not exist.  Pure logic. -/
theorem fourcrowd_dead_of_step_kill (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (_hP : IsPacking n s Q)
    (_hcrowd : FourCrowdN s Q)
    (step : ∃ (Q' : Fin n → Set RP) (c : Fin 4), CornerSwapped s Q Q' c)
    (kill : ∀ (Q' : Fin n → Set RP) (c : Fin 4), IsPacking n s Q' → ¬ ∃ k : Fin n, Q' k = cornerBox s 1 c) :
    False := by
  obtain ⟨Q', c, hP', _, hk⟩ := step
  exact kill Q' c hP' hk

/-! ## Lemma WALL-EXCESS -/

/-- A parametrised square TOUCHES THE FLOOR: some point of it has height `0`. -/
def TouchesFloor (q : PSq) : Prop := ∃ p ∈ q.set, p.2 = 0

/-- The interior chord of a floor-toucher of tilt `t = tan(θ/2)` on the line at height `1/√2`:
`1 / max(cos θ, sin θ)`. -/
noncomputable def chordT (t : ℝ) : ℝ := 1 / max (cosT t) (sinT t)

/-- **[OPEN] Lemma WALL-EXCESS** (Lemma WALL-F on the touchers).  The chords of the floor-touchers of a packing
sum to at most the side. -/
axiom lemma_WALL_EXCESS (n : ℕ) (s : ℝ) (z : Fin n → PSq) (ht : ∀ i, (z i).t ∈ Icc (0 : ℝ) 1)
    (hP : IsPacking n s fun i => (z i).set) (F : Finset (Fin n))
    (hF : ∀ i ∈ F, TouchesFloor (z i)) :
    ∑ i ∈ F, chordT (z i).t ≤ s

/-- Every chord is at least `1` (a flush square's is exactly `1`). -/
theorem chordT_ge_one {t : ℝ} (h0 : 0 ≤ t) (h1 : t ≤ 1) : 1 ≤ chordT t := by
  unfold chordT
  have hle : max (cosT t) (sinT t) ≤ 1 := max_le (cosT_le_one t) (sinT_le_one t)
  have hpos : 0 < max (cosT t) (sinT t) := by
    rcases lt_or_eq_of_le h1 with hlt | heq
    · exact lt_max_of_lt_left (cosT_pos_of_lt_one h0 hlt)
    · have hs : 0 < sinT t := by
        rw [heq, sinT]; norm_num
      exact lt_max_of_lt_right hs
  exact one_le_one_div hpos hle

/-- **Corollary.**  At most `s` squares touch a wall: `k ≤ s` floor-touchers. -/
theorem wall_count_le (n : ℕ) (s : ℝ) (z : Fin n → PSq) (ht : ∀ i, (z i).t ∈ Icc (0 : ℝ) 1)
    (hP : IsPacking n s fun i => (z i).set) (F : Finset (Fin n))
    (hF : ∀ i ∈ F, TouchesFloor (z i)) :
    (F.card : ℝ) ≤ s := by
  have h := lemma_WALL_EXCESS n s z ht hP F hF
  have hc : F.card • (1 : ℝ) ≤ ∑ i ∈ F, chordT (z i).t :=
    Finset.card_nsmul_le_sum F _ 1 (fun i _ => chordT_ge_one (ht i).1 (ht i).2)
  rw [nsmul_eq_mul, mul_one] at hc
  exact le_trans hc h

#print axioms realign
#print axioms one_flush_of_realign
#print axioms fourcrowd_dead_of_step_kill
#print axioms lemma_WALL_EXCESS
#print axioms chordT_ge_one
#print axioms wall_count_le

end PackingCert.S11.OpenLemmas
