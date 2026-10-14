import PackingCertMathlib.ForcedCorners

/-!
# Lemma SLOT-CROWD — Theorem FC, Step 1 (the Lean half of forced corners)

**What it says.**  Take a packing at side `m` that contains the pins of a class `S`, and a cell
`p ∉ S` that is UNCLIPPED (the pins' squares miss the open slot box `int B_p(m)`), such that the
extension class `S ∪ {p}` is killed at side `m`.  Then at least TWO distinct non-pin squares
have interiors meeting `int B_p(m)`.  Step 2 (`fc_transfer`, bottom-left frame): an interior
point in the open slot box transfers under the dilation `scaleC λ` to an interior point of the
dilate inside the WIDENED box `(i, i + 1 + π_i) × (j, j + 1 + π_j)`,
`π_i = (λ_max − 1)(i + 1 + 1/√2)`.

**Why it matters.**  It is the forcing behind every shadow-tree page: a killed extension class
does not just say "no square sits exactly at `p`" — it says two non-pin squares CROWD the cell,
which is what the option table, the clip tree and the count (Theorem COUNT) consume.

**How it is proved** (`ForcedCorners.lean`, A192; prose `docs/proofs/forced_corners.md` §2,
`slot_crowds.md` §2): the teleport of `Selection.teleport_packing` — with at most one non-pin
meeter, replace it (or any non-pin square) by the slot square `B_p(m)` itself; the result is a
packing at side `m` containing the pins of `S ∪ {p}`, contradicting the kill.

**What is still prose** (`Statements/Open/TheoremFC.lean`): the other three corner frames
(D4 transport of Step 2) and Corollaries FC-corner / FC-count.

**For any `n`.**  The teleport argument uses only that a non-pin square exists; the same proof
works for every `n`.
-/

namespace PackingCert.S11

open Set ForcedCorners

/-- **Lemma SLOT-CROWD (Theorem FC, Step 1).** -/
theorem slot_crowd_stmt {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p : Slot)
    (hp : p ∉ S) (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbox : slotBox (slotCentre m p) ⊆ container m)
    (hunclip : ∀ a ∈ S,
      Disjoint (interior (slotBox (slotCentre m p))) (interior (z (f a)).set))
    (hnonpin : ∃ i, NonPin S f i)
    (hkill : ∀ z' : Cfg, CfgPacking m z' → ¬ ContainsPins (insert p S) m z') :
    ∃ i i', i ≠ i' ∧ NonPin S f i ∧ NonPin S f i' ∧
      ¬ Disjoint (interior (slotBox (slotCentre m p))) (interior (z i).set) ∧
      ¬ Disjoint (interior (slotBox (slotCentre m p))) (interior (z i').set) :=
  slot_crowd hz S p hp f hinj hocc hbox hunclip hnonpin hkill

/-- **Theorem FC, Step 2** (bottom-left frame): the transfer to the widened box. -/
theorem fc_transfer_stmt (q : PSq) (p : RP) (hp : p ∈ interior q.set) (i j lam lmax : ℝ)
    (hi0 : 0 ≤ i) (hj0 : 0 ≤ j) (h1 : 1 ≤ lam) (h2 : lam ≤ lmax)
    (hpx : i < p.1 ∧ p.1 < i + 1) (hpy : j < p.2 ∧ p.2 < j + 1) :
    (p.1 + (lam - 1) * q.cx, p.2 + (lam - 1) * q.cy) ∈ interior (scaleC lam q).set ∧
    p.1 + (lam - 1) * q.cx < i + 1 + (lmax - 1) * (i + 1 + 1 / Real.sqrt 2) ∧
    p.2 + (lam - 1) * q.cy < j + 1 + (lmax - 1) * (j + 1 + 1 / Real.sqrt 2) ∧
    (1 ≤ i → i < p.1 + (lam - 1) * q.cx) ∧ (1 ≤ j → j < p.2 + (lam - 1) * q.cy) :=
  fc_transfer q p hp i j lam lmax hi0 hj0 h1 h2 hpx hpy

#print axioms slot_crowd_stmt
#print axioms fc_transfer_stmt

end PackingCert.S11
