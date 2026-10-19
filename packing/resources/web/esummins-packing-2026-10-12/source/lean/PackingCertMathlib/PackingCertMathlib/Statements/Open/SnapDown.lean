import PackingCertMathlib.Statements.Open.RingSwap
import PackingCertMathlib.Statements.Open.TwoGrains
import PackingCertMathlib.Statements.Open.OneFlush

/-!
# -- OPEN: SNAP-DOWN by directionality -- Lemma STACK, the wall click, Lemma REDUCE (A245)

`docs/proofs/snap_down.md`.  The PI (2026-09-16, 20:00): *"is there a way to show that ANY ring that
doubly meets all edge slots can be snapped down in some way -- something with the directionality of the
meeter tilts, to show a subset can always be reduced to simple."*

**12-STUCK** (`TwelveStuck`): every corner box and every wall slot (`wallSlot`: `[0,1] x [1,2]` up the
corner's wall and `[1,2] x [0,1]` along its floor, the census cells `(c, 0, 1)` and `(c, 1, 0)`) is met by
two distinct squares.  Below side 4 STUCK-4 may assume it (A243, Lemma WALL-SLOT + SLOT-MET).

**Lemma STACK** (`lemma_STACK`, n-general, [T] in prose, `snap_down.md` §1).  Two interior-disjoint unit
squares `B`, `B'` touching the wall `x = 0` of `[0, m]²`, `2 + √2 ≤ m < 4`, `B` meeting the corner box
`(0,1)²` and the far slot `(0,1) × (m-2, m-1)`, `B'` meeting the far box `(0,1) × (m-1, m)` and the near
slot `(0,1) × (1,2)` (the MUTUAL wall-grain supply of `wall_slot243.md`) satisfy: (a) ORDER -- every
wall point of `B` is below every wall point of `B'`; (b) CLEARANCE -- `B'` has a point at most `4 - m`
above some point of `B` (their vertical clearance is `< 4 - m`); the stack height of the pair is at
least the sum of their WALL-EXCESS chords, `≥ 2`.  What STACK does NOT give ([F], witnesses in the
note): contact (the pair may float with a gap `< 4 - m`), a handedness pairing (all nine occur), a
parallel contact (same-handed pairs rest vertex-on-edge unless the tilts are equal).

**Conjecture SNAP-DOWN(11)** (`snap_down`, [C]).  Every 12-stuck packing of eleven squares below side 4
exchanges, at a side no larger than its own, into a packing containing a corner slot square.  Its
proposed mechanism -- WALL-CLICK (the wall pair rotated jointly to flush, side re-minimised) followed by
REDUCE (Lemma CELLS on the wall column, or the 3-for-3 exchange `reduce_three_for_three` below) -- is
tested in `attempts/A245-snap-down/results/snapdown245.md`; the click's feasibility is the room
hypothesis of `wall_click`, not a theorem.

**Theorem** `reduce_three_for_three`: the 3-for-3 exchange IS Lemma CELLS -- three squares picked up,
the corner domino `{(c,0,0), (c,0,1)}` and one leftover put down, under exactly `cells_swap`'s
hypotheses -- and yields a packing at the same side containing the domino.  **Theorem**
`no_twelve_stuck_of_snap_down`: SNAP-DOWN + the corner-pin kill (k1-a) + the certified lower bound leave
no 12-stuck packing on the window.  Pure logic.

**Status (2026-09-16).**  `lemma_STACK`: axiom [T-prose]; `snap_down`: axiom [C];
`reduce_three_for_three`, `no_twelve_stuck_of_snap_down`, `twelve_stuck_teleport_stuck`: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The wall slot `k` of corner `c`: `k = 0` up the corner's wall (census cell `(c, 0, 1)`), `k = 1`
along its floor (cell `(c, 1, 0)`); a closed unit cell. -/
def wallSlot (m : ℝ) (c : Fin 4) (k : Fin 2) : Set RP :=
  slotBox (slotCentre m ⟨c, if k = 0 then 0 else 1, if k = 0 then 1 else 0⟩)

/-- Square `i` MEETS the open wall slot. -/
def MeetsSlot (m : ℝ) (z : Cfg) (c : Fin 4) (k : Fin 2) (i : Fin 11) : Prop :=
  ¬ Disjoint (interior (wallSlot m c k)) (interior (z i).set)

/-- 12-STUCK: teleport-stuck (all four corner boxes doubly met) and all eight wall slots doubly met. -/
def TwelveStuck (m : ℝ) (z : Cfg) : Prop :=
  TeleportStuck m z ∧
    ∀ (c : Fin 4) (k : Fin 2),
      ∃ i j : Fin 11, i ≠ j ∧ MeetsSlot m z c k i ∧ MeetsSlot m z c k j

theorem twelve_stuck_teleport_stuck {m : ℝ} {z : Cfg} (h : TwelveStuck m z) : TeleportStuck m z :=
  h.1

/-- A square (as a set) touches the wall `x = 0`. -/
def TouchesLeftWall (Q : Set RP) : Prop := ∃ p ∈ Q, p.1 = 0

/-- A body meets an open axis cell `(x0,x1) × (y0,y1)`. -/
def MeetsCell (Q : Set RP) (x0 x1 y0 y1 : ℝ) : Prop :=
  ¬ Disjoint (interior (Icc x0 x1 ×ˢ Icc y0 y1)) (interior Q)

/-- **[OPEN] Lemma STACK** (n-general, [T] in prose).  A mutual wall pair on the wall `x = 0` at a side
`2 + √2 ≤ m < 4` is ORDERED (every wall point of `B` below every wall point of `B'`) with vertical
CLEARANCE below `4 - m` (some point of `B'` is less than `4 - m` above some point of `B`). -/
axiom lemma_STACK (n : ℕ) (m : ℝ) (hm : 2 + Real.sqrt 2 ≤ m) (hm4 : m < 4) (Q : Fin n → Set RP)
    (hP : IsPacking n m Q) (i j : Fin n) (hij : i ≠ j)
    (hti : TouchesLeftWall (Q i)) (htj : TouchesLeftWall (Q j))
    (hi0 : MeetsCell (Q i) 0 1 0 1) (hi1 : MeetsCell (Q i) 0 1 (m - 2) (m - 1))
    (hj0 : MeetsCell (Q j) 0 1 (m - 1) m) (hj1 : MeetsCell (Q j) 0 1 1 2) :
    (∀ p ∈ Q i, p.1 = 0 → ∀ q ∈ Q j, q.1 = 0 → p.2 ≤ q.2) ∧
    (∃ p ∈ Q i, ∃ q ∈ Q j, q.2 - p.2 < 4 - m)

/-- **[OPEN] Conjecture SNAP-DOWN(11)** ([C]; mechanism WALL-CLICK + REDUCE, tested in A245).  A 12-stuck
packing below side 4 exchanges, at a side no larger than its own, into a packing containing a corner
slot square. -/
axiom snap_down (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z) (h12 : TwelveStuck m z) :
    ∃ m' : ℝ, m' ≤ m ∧
      ∃ z' : Cfg, CfgPacking m' z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m' z'

/-- **Lemma REDUCE, the 3-for-3 form** (a theorem: Lemma CELLS with `k = 3`).  Three distinct squares
`ι 0, ι 1, ι 2` of a packing are exchanged for the corner domino of `c` (`F 0` in the corner box,
`F 1` in the wall slot above it) and a leftover `F 2`, under `cells_swap`'s hypotheses -- the three new
squares are admissible, pairwise interior-disjoint, and interior-disjoint from every square NOT picked
up.  The result is a packing at the same side containing the domino. -/
theorem reduce_three_for_three {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (c : Fin 4)
    (ι : Fin 3 → Fin 11) (hι : Function.Injective ι) (F : Fin 3 → PSq)
    (hF0 : OccupiesSlot (F 0) (slotCentre m ⟨c, 0, 0⟩))
    (hF1 : OccupiesSlot (F 1) (slotCentre m ⟨c, 0, 1⟩))
    (htF : ∀ a, (F a).t ∈ Icc (0 : ℝ) 1) (hboxF : ∀ a, (F a).set ⊆ container m)
    (hdisj : ∀ a b, a ≠ b → Disjoint (interior (F a).set) (interior (F b).set))
    (hmiss : ∀ j, (∀ a, ι a ≠ j) →
      ∀ a, Disjoint (interior (F a).set) (interior (z j).set)) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ContainsPins {⟨c, 0, 0⟩, ⟨c, 0, 1⟩} m z' := by
  have h01 : ι 0 ≠ ι 1 := fun h => absurd (hι h) (by decide)
  have h02 : ι 0 ≠ ι 2 := fun h => absurd (hι h) (by decide)
  have h12 : ι 1 ≠ ι 2 := fun h => absurd (hι h) (by decide)
  let z' : Cfg :=
    Function.update (Function.update (Function.update z (ι 0) (F 0)) (ι 1) (F 1)) (ι 2) (F 2)
  have hF : ∀ a, z' (ι a) = F a := by
    intro a
    fin_cases a
    · change Function.update (Function.update (Function.update z (ι 0) (F 0)) (ι 1) (F 1)) (ι 2)
          (F 2) (ι 0) = F 0
      rw [Function.update_of_ne h02, Function.update_of_ne h01, Function.update_self]
    · change Function.update (Function.update (Function.update z (ι 0) (F 0)) (ι 1) (F 1)) (ι 2)
          (F 2) (ι 1) = F 1
      rw [Function.update_of_ne h12, Function.update_self]
    · change Function.update (Function.update (Function.update z (ι 0) (F 0)) (ι 1) (F 1)) (ι 2)
          (F 2) (ι 2) = F 2
      rw [Function.update_self]
  have hkeep : ∀ j, (∀ a, ι a ≠ j) → z' j = z j := by
    intro j hj
    change Function.update (Function.update (Function.update z (ι 0) (F 0)) (ι 1) (F 1)) (ι 2)
        (F 2) j = z j
    rw [Function.update_of_ne (hj 2).symm, Function.update_of_ne (hj 1).symm,
      Function.update_of_ne (hj 0).symm]
  refine ⟨z', cells_swap hz ι F z' hF hkeep htF hboxF hdisj hmiss, ?_⟩
  refine ⟨fun a => if a.celly = 0 then ι 0 else ι 1, ?_, ?_⟩
  · intro a ha b hb hab
    simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff,
      Set.mem_singleton_iff] at ha hb
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> simp_all
  · intro a ha
    simp only [Finset.mem_insert, Finset.mem_singleton] at ha
    rcases ha with rfl | rfl
    · simpa [hF 0] using hF0
    · simpa [hF 1] using hF1

/-- **The consequence.**  SNAP-DOWN(11) + the corner-pin kill on the window (k1-a) + the certified lower
bound `3.82` leave no 12-stuck packing at any side `m ∈ [3.82, 4)`.  Pure logic. -/
theorem no_twelve_stuck_of_snap_down (m : ℝ) (hm : m < 4)
    (kill : ∀ m' : ℝ, 191 / 50 ≤ m' → m' ≤ m →
      ∀ (c : Fin 4) (z : Cfg), CfgPacking m' z → ¬ ContainsPins {⟨c, 0, 0⟩} m' z)
    (lower : ∀ m' : ℝ, m' < 191 / 50 → ∀ z : Cfg, ¬ CfgPacking m' z)
    (z : Cfg) (hz : CfgPacking m z) : ¬ TwelveStuck m z := by
  intro h12
  obtain ⟨m', hm', z', hz', c, hc⟩ := snap_down m hm z hz h12
  by_cases hlow : m' < 191 / 50
  · exact lower m' hlow z' hz'
  · exact kill m' (not_lt.mp hlow) hm' c z' hz' hc

#print axioms lemma_STACK
#print axioms snap_down
#print axioms reduce_three_for_three
#print axioms no_twelve_stuck_of_snap_down
#print axioms twelve_stuck_teleport_stuck

end PackingCert.S11.OpenLemmas
