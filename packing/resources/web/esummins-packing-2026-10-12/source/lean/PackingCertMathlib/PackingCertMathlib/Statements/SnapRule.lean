import PackingCertMathlib.ForcedCorners
import PackingCertMathlib.Statements.Open.RingSwap

/-!
# Rule SNAP — the teleport in slot form (A224)

**What the engine's certificate is.**  A node of the coarse tree (`attempts/A211-coarse-tree`) carries, for each
square of the packing, a set of allowed poses.  Rule SNAP (`docs/proofs/snap_rule.md`,
`attempts/A224-snap-rule/code/snap224.py`) emits, for one role `i` and one census cell `p`:

* an EXACT separating-axis certificate, per other role, that every allowed pose of that role gives a square whose
  interior misses the (widened) slot box — clause (a);
* the class's UNCLIPPED census for the pins, and either "no anonymous square is left" or an empty option-table row
  at `p` — clause (b);
* the target stratum `S ∪ {p}` and its closure record.

`snap_step` below says exactly that this data is the HYPOTHESIS of a theorem: the three clauses are precisely
`hfree : ∀ j ≠ i, Disjoint (interior (slotBox (slotCentre m p))) (interior (z j).set)`, and the conclusion is that
the teleported configuration is a packing at the SAME side containing the pins of `insert p S`.  `snap_dead` closes
the node against the stratum kill.  Nothing here is new mathematics: `snap_step` is
`Selection.teleport_packing` (itself `Open.RingSwap.teleport_of_swap`, Lemma SWAP with
`X = {i}`) plus the bookkeeping already inside `ForcedCorners.slot_crowd_key`, and SNAP-DIAG is
that step applied twice.

**Why the rule is not Lemma SLOT-CROWD.**  SLOT-CROWD consumes the kill of `S ∪ {p}` to DERIVE
two meeters at a FORCED cell; SNAP runs the same teleport forwards, at any cell the engine can
certify singly met — including cells where the node has already named two candidate meeters,
since a candidate that provably misses the box is not a meeter.  The two are the same theorem read in opposite directions (`snap_dead` is `slot_crowd_key`'s
contrapositive), which is why the engine may use either.

**SNAP-DIAG.**  `snap_diag_two`: two roles near two cells whose boxes are interior-disjoint,
each blocked only by the other, snap together — the first teleport makes the first slot square a
pin for the second.  This is Lemma SWAP with `|X| = 2`; the `k`-fold case is `swap_packing` /
`cells_swap` verbatim and is stated in `RingSwap.lean`.

**For any `n`.**  Every step is `n`-general: `swap_packing` is stated for an arbitrary index
set, and the census / scoreboard input is the only `n = 11` ingredient.

**Status (2026-09-14).**  `snap_step`, `snap_dead`, `snap_diag_two`: theorems, no new axiom.
-/

namespace PackingCert.S11

open Set ForcedCorners

/-- **Rule SNAP, the step** (explicit assignment).  A packing at side `m` holding the pins of
`S` through `f`; a cell `p ∉ S` whose slot box lies in the container; a NON-pin square `i` such
that every OTHER square's interior misses the slot box.  Then teleporting `i` onto `p` is a
packing at side `m`, and `update f p i` assigns the pins of `insert p S` in it.  (The engine's
clause (a) is `hfree` restricted to the named roles, clause (b) is `hfree` for the anonymous
ones, and the pins are `hfree` by the class's unclipped census.) -/
theorem snap_assign {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p : Slot)
    (hp : p ∉ S) (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbox : slotBox (slotCentre m p) ⊆ container m)
    (i : Fin 11) (hi : NonPin S f i)
    (hfree : ∀ j, j ≠ i → Disjoint (interior (slotBox (slotCentre m p))) (interior (z j).set)) :
    CfgPacking m (teleport z i (slotCentre m p)) ∧
      Set.InjOn (Function.update f p i) ↑(insert p S) ∧
      ∀ a ∈ insert p S,
        OccupiesSlot (teleport z i (slotCentre m p) (Function.update f p i a))
          (slotCentre m a) := by
  refine ⟨teleport_packing hz i (slotCentre m p) hbox hfree, ?_, ?_⟩
  · intro a ha b hb hab
    rw [Finset.coe_insert, Set.mem_insert_iff] at ha hb
    rcases ha with ha | ha <;> rcases hb with hb | hb
    · rw [ha, hb]
    · have hbp : b ≠ p := fun h => hp (h ▸ hb)
      rw [ha, Function.update_self, Function.update_of_ne hbp] at hab
      exact absurd hab.symm (hi b hb)
    · have hap : a ≠ p := fun h => hp (h ▸ ha)
      rw [hb, Function.update_of_ne hap, Function.update_self] at hab
      exact absurd hab (hi a ha)
    · have hap : a ≠ p := fun h => hp (h ▸ ha)
      have hbp : b ≠ p := fun h => hp (h ▸ hb)
      rw [Function.update_of_ne hap, Function.update_of_ne hbp] at hab
      exact hinj ha hb hab
  · intro a ha
    rw [Finset.mem_insert] at ha
    rcases ha with ha | ha
    · rw [ha, Function.update_self, OccupiesSlot, teleport_self]
      rfl
    · have hap : a ≠ p := fun h => hp (h ▸ ha)
      rw [Function.update_of_ne hap, teleport_ne z i _ (hi a ha)]
      exact hocc a ha

/-- **Rule SNAP.**  The same step as `ContainsPins`: the node's hypothesis yields a packing at the
SAME side containing one more simple slot. -/
theorem snap_step {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p : Slot)
    (hp : p ∉ S) (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbox : slotBox (slotCentre m p) ⊆ container m)
    (i : Fin 11) (hi : NonPin S f i)
    (hfree : ∀ j, j ≠ i → Disjoint (interior (slotBox (slotCentre m p))) (interior (z j).set)) :
    CfgPacking m (teleport z i (slotCentre m p)) ∧
      ContainsPins (insert p S) m (teleport z i (slotCentre m p)) := by
  obtain ⟨h1, h2, h3⟩ := snap_assign hz S p hp f hinj hocc hbox i hi hfree
  exact ⟨h1, _, h2, h3⟩

/-- **Rule SNAP, the kill.**  With the target stratum `insert p S` closed at side `m` (a FULL
scoreboard row, transported to `m` by `Dilation.lemma_B` / K1), no packing satisfies the node's
hypothesis. -/
theorem snap_dead {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p : Slot)
    (hp : p ∉ S) (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbox : slotBox (slotCentre m p) ⊆ container m)
    (i : Fin 11) (hi : NonPin S f i)
    (hfree : ∀ j, j ≠ i → Disjoint (interior (slotBox (slotCentre m p))) (interior (z j).set))
    (hkill : ∀ z' : Cfg, CfgPacking m z' → ¬ ContainsPins (insert p S) m z') : False := by
  obtain ⟨h1, h2⟩ := snap_step hz S p hp f hinj hocc hbox i hi hfree
  exact hkill _ h1 h2

/-- **SNAP-DIAG, two slots at once.**  Roles `i ≠ i'` near cells `p`, `q`: every square OTHER than
`i` and `i'` misses both slot boxes (`hfp`, `hfq` — the engine's per-role exact miss certificates,
which do NOT have to exclude the partner: in the diagonal case each of the two blocks the other's
cell), and the two slot boxes are interior-disjoint (`hpq` — diagonal cells meet at a point only).
Then the two teleports TOGETHER give a packing at side `m` containing the pins of
`insert q (insert p S)`.  This is Lemma SWAP with `|X| = 2` (`Open.RingSwap.swap_packing`); the
`k`-fold form is that theorem verbatim. -/
theorem snap_diag_two {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p q : Slot)
    (hp : p ∉ S) (hq : q ∉ insert p S) (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbp : slotBox (slotCentre m p) ⊆ container m)
    (hbq : slotBox (slotCentre m q) ⊆ container m)
    (i i' : Fin 11) (hii : i ≠ i') (hi : NonPin S f i) (hi' : NonPin S f i')
    (hpq : Disjoint (interior (slotBox (slotCentre m p))) (interior (slotBox (slotCentre m q))))
    (hfp : ∀ j, j ≠ i → j ≠ i' →
      Disjoint (interior (slotBox (slotCentre m p))) (interior (z j).set))
    (hfq : ∀ j, j ≠ i → j ≠ i' →
      Disjoint (interior (slotBox (slotCentre m q))) (interior (z j).set)) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ContainsPins (insert q (insert p S)) m z' := by
  have hqp : q ≠ p := fun h => hq (by rw [h]; exact Finset.mem_insert_self p S)
  have hqS : q ∉ S := fun h => hq (Finset.mem_insert_of_mem h)
  set pc := slotCentre m p with hpc
  set qc := slotCentre m q with hqc
  set z2 : Cfg := teleport (teleport z i pc) i' qc with hz2
  have hzi : z2 i = ⟨pc.1, pc.2, 0⟩ := by
    rw [hz2, teleport_ne (teleport z i pc) i' qc hii]
    simp only [teleport, Function.update_self]
  have hzi' : z2 i' = ⟨qc.1, qc.2, 0⟩ := by
    simp only [hz2, teleport, Function.update_self]
  have hsi : (z2 i).set = slotBox pc := by rw [hzi, ← slotBox_eq_set]
  have hsi' : (z2 i').set = slotBox qc := by rw [hzi', ← slotBox_eq_set]
  have hzj : ∀ j, j ≠ i → j ≠ i' → z2 j = z j := by
    intro j h1 h2
    rw [hz2, teleport_ne (teleport z i pc) i' qc h2, teleport_ne z i pc h1]
  have hpack : CfgPacking m z2 := by
    refine OpenLemmas.swap_packing hz {i, i'} z2 ?_ ?_ ?_ ?_
    · intro j hj
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff, not_or] at hj
      exact hzj j hj.1 hj.2
    · rintro a (rfl | rfl)
      · rw [hzi]; exact ⟨le_refl _, by norm_num⟩
      · rw [hzi']; exact ⟨le_refl _, by norm_num⟩
    · rintro a (rfl | rfl)
      · rw [hsi]; exact hbp
      · rw [hsi']; exact hbq
    · rintro a (rfl | rfl) j hj
      · rw [hsi]
        by_cases hj' : j = i'
        · rw [hj', hsi']; exact hpq
        · rw [hzj j hj hj']; exact hfp j hj hj'
      · rw [hsi']
        by_cases hj' : j = i
        · rw [hj', hsi]; exact hpq.symm
        · rw [hzj j hj' hj]; exact hfq j hj' hj
  refine ⟨z2, hpack, Function.update (Function.update f p i) q i', ?_, ?_⟩
  · have hgq : Function.update (Function.update f p i) q i' q = i' := Function.update_self _ _ _
    have hgp : Function.update (Function.update f p i) q i' p = i := by
      rw [Function.update_of_ne (Ne.symm hqp), Function.update_self]
    have hgS : ∀ a ∈ S, Function.update (Function.update f p i) q i' a = f a := by
      intro a ha
      rw [Function.update_of_ne (fun h : a = q => hqS (h ▸ ha)),
          Function.update_of_ne (fun h : a = p => hp (h ▸ ha))]
    intro a ha b hb hab
    simp only [Finset.coe_insert, Set.mem_insert_iff] at ha hb
    rcases ha with rfl | rfl | ha
    · rcases hb with rfl | rfl | hb
      · rfl
      · rw [hgq, hgp] at hab; exact absurd hab.symm hii
      · rw [hgq, hgS _ hb] at hab; exact absurd hab.symm (hi' _ hb)
    · rcases hb with rfl | rfl | hb
      · rw [hgp, hgq] at hab; exact absurd hab hii
      · rfl
      · rw [hgp, hgS _ hb] at hab; exact absurd hab.symm (hi _ hb)
    · rcases hb with rfl | rfl | hb
      · rw [hgS _ ha, hgq] at hab; exact absurd hab (hi' _ ha)
      · rw [hgS _ ha, hgp] at hab; exact absurd hab (hi _ ha)
      · rw [hgS _ ha, hgS _ hb] at hab; exact hinj ha hb hab
  · intro a ha
    rw [Finset.mem_insert, Finset.mem_insert] at ha
    rcases ha with rfl | rfl | ha
    · rw [OccupiesSlot, Function.update_self, hsi']
      rfl
    · rw [OccupiesSlot, Function.update_of_ne (Ne.symm hqp), Function.update_self, hsi]
      rfl
    · have h1 : a ≠ q := fun h => hqS (h ▸ ha)
      have h2 : a ≠ p := fun h => hp (h ▸ ha)
      rw [Function.update_of_ne h1, Function.update_of_ne h2, hzj _ (hi a ha) (hi' a ha)]
      exact hocc a ha

#print axioms snap_assign
#print axioms snap_step
#print axioms snap_dead
#print axioms snap_diag_two

end PackingCert.S11
