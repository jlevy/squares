import PackingCertMathlib.Statements.Open.PerimeterWalk

/-!
# -- OPEN: FAMILY-STUCK -- the stuck hypothesis Lemma CELLS actually needs (A250)

`attempts/A250-family-stuck/notes/family250.md`.  The PI (2026-09-17, 10:30), reading A248's
`twelve_stuck_fail.svg`: *"the 6/9 pair serves both TL00 and TL10 -- two meeters, two slots, so
they can teleport down."*

**The point.**  Lemma CELLS (`RingSwap.cells_swap`) exchanges a packing into a family `Π` of
pairwise interior-disjoint unit cells as soon as `|M(Π)| ≤ |Π|`, where `M(Π)` is the set of
squares whose interiors meet a cell of `Π`.  A244's TWELVE-STUCK is only the rows `|Π| = 1`
(every border cell doubly met), so it is NOT the hypothesis that blocks the exchange: a corner
DOMINO `{c00, c01}` met by exactly two squares in total is a legal `Π` with `|M(Π)| = 2 = |Π|`.
FAMILY-STUCK below asks `|Π| < |M(Π)|` for EVERY disjoint family of border cells; measured, no
twelve-stuck packing anywhere in the corpus satisfies it (0 of A244's 488 certified twelve-stuck
packings, 0 of A217's 486 witnesses; `attempts/A250-family-stuck/results/family250.md`).

**The count** [T] (`no_family_stuck_ge_four`).  At a side `m ≥ 4` the twelve border cells are
pairwise interior-disjoint (the two facing slots of a wall are the interval pair `(1,2)`,
`(m-2, m-1)`, disjoint exactly when `m ≥ 4`; every other pair is disjoint for `m ≥ 3`), so the
whole twelve is a legal family and family-stuck would need `13` squares.  With eleven there are
none: **the family hypothesis has no window at or above 4 at all**, where A244 certifies 488
twelve-stuck packings from `4.000010` to `4.5` and A247's UPPER-END only reaches down to
`4 + √2`.  Below 4 the count gives only `9` (exact, ILP over the PROJECTION catalogue with
NOT-SELF-SUFFICIENT and TWO-FAR, `count250.py`), so it does not close the window: the obligation
`family_stuck_exist_eleven` stays.  n-general: family-stuck at side `m` needs `n ≥ 4⌊m⌋ - 3`.

**What it buys** (`raise_of_ge_four`, `no_packing_of_family_ge_four`): at every side `m ≥ 4` the
twelve-cell family raises any eleven-square packing to one containing a corner pin, with no
hypothesis at all -- the count form of `ring_swap.md` §1.4's remark that RAISE is trivial above 4.
And `family_stuck_of_stuck_exist`: the new obligation is implied by the old one (FAMILY-STUCK
implies TWELVE-STUCK, `familyStuck_twelveStuck`), so A250 strictly weakens what must be killed.

**Status (2026-09-17).**  `twelve_cells_disjoint` (geometry, one line of prose) and `cells_raise`
(Lemma CELLS transported to the census cells) are axioms [T]; `family_stuck_exist_eleven` is the
axiom [C] that replaces STUCK-EXIST(11) on `[3.82, 4)`; everything else is a theorem.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The twelve BORDER CELLS as census slots: per corner the box `(c,0,0)`, the slot `(c,0,1)` up
its wall and the slot `(c,1,0)` along its floor (A244 `cells244`: `c00`, `c01`, `c10`). -/
def borderSlots : Finset Slot :=
  (Finset.univ : Finset (Fin 4)).biUnion fun c => {⟨c, 0, 0⟩, ⟨c, 0, 1⟩, ⟨c, 1, 0⟩}

/-- The cell of a slot at side `m`: the closed axis unit box centred at the slot's centre. -/
def cellOf (m : ℝ) (a : Slot) : Set RP := slotBox (slotCentre m a)

/-- Square `i` of `z` MEETS the border cell `a` (interiors overlap). -/
def MeetsBorder (m : ℝ) (z : Cfg) (a : Slot) (i : Fin 11) : Prop :=
  ¬ Disjoint (interior (cellOf m a)) (interior (z i).set)

/-- A family of border cells is admissible when its cells are pairwise interior-disjoint -- the
hypothesis of Lemma CELLS. -/
def DisjointFamily (m : ℝ) (F : Finset Slot) : Prop :=
  ∀ a ∈ F, ∀ b ∈ F, a ≠ b → Disjoint (interior (cellOf m a)) (interior (cellOf m b))

open scoped Classical in
/-- `M(Π)`: the squares meeting some cell of the family. -/
noncomputable def meeters (m : ℝ) (z : Cfg) (F : Finset Slot) : Finset (Fin 11) :=
  Finset.univ.filter fun i => ∃ a ∈ F, MeetsBorder m z a i

/-- **FAMILY-STUCK**: every admissible family of border cells is met by MORE squares than it has
cells -- exactly the negation of Lemma CELLS' hypothesis on every family at once.  `|Π| = 1` is
A244's TWELVE-STUCK; `|Π| = 2` on a corner domino is the PI's teleporting pair. -/
def FamilyStuck (m : ℝ) (z : Cfg) : Prop :=
  ∀ F : Finset Slot, F ⊆ borderSlots → DisjointFamily m F → F.card < (meeters m z F).card

theorem borderSlots_card : borderSlots.card = 12 := by decide

/-- **[T] The twelve cells are pairwise disjoint at every side `m ≥ 4`.**  On one wall the cells'
along-wall intervals are `(0,1)`, `(1,2)`, `(m-2,m-1)`, `(m-1,m)`: the only pair that can overlap
is the facing pair `(1,2)`, `(m-2,m-1)`, and it is interior-disjoint exactly when `4 ≤ m`; cells
of different walls differ by more than `1` in a coordinate for `m ≥ 3`.  (`fam250.conflicts`
computes the same four conflicting pairs below 4 and none at or above 4.) -/
axiom twelve_cells_disjoint (m : ℝ) (hm : 4 ≤ m) : DisjointFamily m borderSlots

/-- **[T] The count.**  No configuration of ELEVEN squares at a side `m ≥ 4` is family-stuck:
the twelve disjoint cells would need thirteen distinct meeters.  (No packing hypothesis is used
-- this is counting.)  n-general: `n ≥ 4⌊m⌋ - 3`. -/
theorem no_family_stuck_ge_four (m : ℝ) (hm : 4 ≤ m) (z : Cfg) (hfs : FamilyStuck m z) : False := by
  have h := hfs borderSlots (Finset.Subset.refl _) (twelve_cells_disjoint m hm)
  rw [borderSlots_card] at h
  have h2 : (meeters m z borderSlots).card ≤ 11 := by
    simpa using Finset.card_le_univ (meeters m z borderSlots)
  omega

/-- A family-stuck packing of eleven squares has side below 4 (the family window is `[3.82, 4)`,
against `[4, 4 + √2)` for TWELVE-STUCK). -/
theorem family_stuck_side_lt (m : ℝ) (z : Cfg) (hfs : FamilyStuck m z) : m < 4 := by
  by_contra h
  exact no_family_stuck_ge_four m (not_lt.mp h) z hfs

/-- **[T] Lemma CELLS on the census cells** (`cells_swap` with `F` the cells of `Π` as flat unit
squares and `ι` an injection onto `M(Π)`; the hypothesis `hmiss` is the definition of `M(Π)` and
`hdisj` is admissibility).  A family containing a corner box with `|M(Π)| ≤ |Π|` raises the
packing to one containing that corner pin. -/
axiom cells_raise (m : ℝ) (z : Cfg) (hz : CfgPacking m z) (F : Finset Slot)
    (hF : F ⊆ borderSlots) (hdis : DisjointFamily m F)
    (hcard : (meeters m z F).card ≤ F.card) (c : Fin 4) (hc : (⟨c, 0, 0⟩ : Slot) ∈ F) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z'

theorem corner_mem_borderSlots (c : Fin 4) : (⟨c, 0, 0⟩ : Slot) ∈ borderSlots := by
  refine Finset.mem_biUnion.mpr ⟨c, Finset.mem_univ c, ?_⟩
  simp

/-- **[T] RAISE is automatic at every side `m ≥ 4`**: the twelve-cell family has at most eleven
meeters, fewer than its twelve cells, so Lemma CELLS puts all twelve down -- in particular a
corner square.  (`ring_swap.md` §1.4's "trivially at `S ≥ 4`", as a theorem.) -/
theorem raise_of_ge_four (m : ℝ) (hm : 4 ≤ m) (z : Cfg) (hz : CfgPacking m z) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z' := by
  refine cells_raise m z hz borderSlots (Finset.Subset.refl _) (twelve_cells_disjoint m hm) ?_ 0
    (corner_mem_borderSlots 0)
  have h2 : (meeters m z borderSlots).card ≤ 11 := by
    simpa using Finset.card_le_univ (meeters m z borderSlots)
  rw [borderSlots_card]
  omega

/-- With the corner-pin kill at side `m` (k1-a), no packing of eleven squares exists at any side
`m ≥ 4` at which the kill holds.  Pure logic. -/
theorem no_packing_of_family_ge_four (m : ℝ) (hm : 4 ≤ m)
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z)
    (z : Cfg) (hz : CfgPacking m z) : False := by
  obtain ⟨z', hz', c, hc⟩ := raise_of_ge_four m hm z hz
  exact kill c z' hz' hc

/-- Singleton families: a family-stuck configuration has every border cell doubly met. -/
theorem doubly_met_of_familyStuck {m : ℝ} {z : Cfg} (hfs : FamilyStuck m z) {a : Slot}
    (ha : a ∈ borderSlots) : ∃ i j : Fin 11, i ≠ j ∧ MeetsBorder m z a i ∧ MeetsBorder m z a j := by
  have hsub : ({a} : Finset Slot) ⊆ borderSlots := Finset.singleton_subset_iff.mpr ha
  have hdis : DisjointFamily m {a} := by
    intro x hx y hy hxy
    rw [Finset.mem_singleton] at hx hy
    exact absurd (hx.trans hy.symm) hxy
  have h := hfs {a} hsub hdis
  rw [Finset.card_singleton] at h
  obtain ⟨i, hi, j, hj, hij⟩ := Finset.one_lt_card.mp h
  classical
  have hmi : ∃ b ∈ ({a} : Finset Slot), MeetsBorder m z b i := by
    simpa [meeters] using hi
  have hmj : ∃ b ∈ ({a} : Finset Slot), MeetsBorder m z b j := by
    simpa [meeters] using hj
  obtain ⟨b, hb, hbi⟩ := hmi
  obtain ⟨b', hb', hbj⟩ := hmj
  rw [Finset.mem_singleton] at hb hb'
  subst hb
  subst hb'
  exact ⟨i, j, hij, hbi, hbj⟩

theorem slot_mem_borderSlots (c : Fin 4) (k : Fin 2) :
    (⟨c, if k = 0 then 0 else 1, if k = 0 then 1 else 0⟩ : Slot) ∈ borderSlots := by
  refine Finset.mem_biUnion.mpr ⟨c, Finset.mem_univ c, ?_⟩
  fin_cases k <;> simp

/-- **FAMILY-STUCK implies TWELVE-STUCK** (the `|Π| = 1` rows), so A250's obligation is WEAKER
than A246's STUCK-EXIST(11): whatever kills the twelve-cell hypothesis kills this one. -/
theorem familyStuck_twelveStuck {m : ℝ} {z : Cfg} (hfs : FamilyStuck m z) : TwelveStuck m z := by
  constructor
  · intro c
    obtain ⟨i, j, hij, hi, hj⟩ := doubly_met_of_familyStuck hfs (corner_mem_borderSlots c)
    refine ⟨i, j, hij, ?_, ?_⟩ <;>
      simpa [MeetsCorner, cornerBox_one_eq_slotBox, cellOf, MeetsBorder] using ‹_›
  · intro c k
    obtain ⟨i, j, hij, hi, hj⟩ := doubly_met_of_familyStuck hfs (slot_mem_borderSlots c k)
    exact ⟨i, j, hij, hi, hj⟩

/-- **[OPEN] FAMILY-STUCK-EXIST(11)** [C]: no packing of eleven unit squares at a side below 4 is
family-stuck.  This is what the k0 route now has to kill; the count reaches only `9` below 4
(A250), the search finds no witness on `[3.82, 4.6]`, and the corpus contains none. -/
axiom family_stuck_exist_eleven (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) : False

/-- The weakening, as logic: STUCK-EXIST(11) implies FAMILY-STUCK-EXIST(11). -/
theorem family_stuck_of_stuck_exist (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) : False :=
  stuck_exist_eleven m hm z hz (familyStuck_twelveStuck hfs)

/-- No eleven-square packing is family-stuck at ANY side: below 4 by the obligation, at or above
4 by the count. -/
theorem no_family_stuck_anywhere (m : ℝ) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) : False := by
  by_cases h : m < 4
  · exact family_stuck_exist_eleven m h z hz hfs
  · exact no_family_stuck_ge_four m (not_lt.mp h) z hfs

#print axioms twelve_cells_disjoint
#print axioms cells_raise
#print axioms no_family_stuck_ge_four
#print axioms family_stuck_side_lt
#print axioms raise_of_ge_four
#print axioms no_packing_of_family_ge_four
#print axioms familyStuck_twelveStuck
#print axioms family_stuck_exist_eleven
#print axioms family_stuck_of_stuck_exist
#print axioms no_family_stuck_anywhere

end PackingCert.S11.OpenLemmas
