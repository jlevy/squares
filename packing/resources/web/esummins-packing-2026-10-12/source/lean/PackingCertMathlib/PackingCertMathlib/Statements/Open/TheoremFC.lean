import PackingCertMathlib.ForcedCorners
import PackingCertMathlib.Crowd

/-!
# -- OPEN: Theorem FC — forced cells crowd the dilated page (all four corner frames)

**What it asserts** (`docs/proofs/forced_corners.md` §2, any `n`).  Let `P` be a packing at
side `m ∈ [3.82, s₀]` containing the pins of a class `S`, `p ∉ S` an UNCLIPPED cell (the pins'
squares miss the open slot box) whose extension class `S ∪ {p}` is killed at side `m`.  Then
the dilate `F = Δ_λ P`, `λ = s₀/m ≤ λ_max`, has TWO DISTINCT non-pin squares whose interiors
meet the WIDENED open box
`B_p⁺ = (i, i + 1 + π_i) × (j, j + 1 + π_j)`, `π_i = (λ_max − 1)(i + 1 + 1/√2)`,
in the corner frame of `p`'s corner at side `s₀`.

**What is Lean already** (`Statements/SlotCrowd.lean`): Step 1 (`slot_crowd`, two non-pin
meeters of `int B_p(m)` at side `m`) and Step 2 in the bottom-left frame (`fc_transfer`).
**What is prose**: Step 2 in the other three corner frames (the D4 transport — a coordinate
reflection `x ↦ s − x` per axis, `cframe`), and the corollaries FC-corner (Lemma A2
`Sideband.distinct_cells` once the meeters are in the quadrant) and FC-count.

**Status (2026-09-14).**  [T] in prose; the missing Lean is bookkeeping (frames + the
`i = 0` container-margin case).  Consumers: every shadow-tree page (A178–A215) — the forcing
that Theorem COUNT, Lemma CT and the clip tree read as "two distinct non-pin meeters of `B_p⁺`".
-/

namespace PackingCert.S11.OpenLemmas

open Set ForcedCorners

/-- The widened open slot box `B_p⁺` of cell `p` at side `s₀`, for dilation factors up to
`lmax`, in `p`'s corner frame (`cframe`). -/
def widenedSlotBox (s0 lmax : ℝ) (p : Slot) : Set RP :=
  {x | (p.cellx : ℝ) < (cframe s0 p.corner x).1 ∧
    (cframe s0 p.corner x).1 <
      (p.cellx : ℝ) + 1 + (lmax - 1) * ((p.cellx : ℝ) + 1 + 1 / Real.sqrt 2) ∧
    (p.celly : ℝ) < (cframe s0 p.corner x).2 ∧
    (cframe s0 p.corner x).2 <
      (p.celly : ℝ) + 1 + (lmax - 1) * ((p.celly : ℝ) + 1 + 1 / Real.sqrt 2)}

/-- **[OPEN] Theorem FC.**  Two distinct non-pin squares of the dilate meet the widened box. -/
axiom theorem_FC {m s0 lmax : ℝ} (hm : (191 / 50 : ℝ) ≤ m) (hms : m ≤ s0) (hl : s0 / m ≤ lmax)
    {z : Cfg} (hz : CfgPacking m z) (S : PinSet) (p : Slot) (hp : p ∉ S)
    (f : Slot → Fin 11) (hinj : Set.InjOn f ↑S)
    (hocc : ∀ a ∈ S, OccupiesSlot (z (f a)) (slotCentre m a))
    (hbox : slotBox (slotCentre m p) ⊆ container m)
    (hunclip : ∀ a ∈ S,
      Disjoint (interior (slotBox (slotCentre m p))) (interior (z (f a)).set))
    (hnonpin : ∃ i, NonPin S f i)
    (hkill : ∀ z' : Cfg, CfgPacking m z' → ¬ ContainsPins (insert p S) m z') :
    ∃ i i', i ≠ i' ∧ NonPin S f i ∧ NonPin S f i' ∧
      (interior (scaleC (s0 / m) (z i)).set ∩ widenedSlotBox s0 lmax p).Nonempty ∧
      (interior (scaleC (s0 / m) (z i')).set ∩ widenedSlotBox s0 lmax p).Nonempty

#print axioms theorem_FC

end PackingCert.S11.OpenLemmas
