import PackingCertMathlib.Composition

/-!
# Composition — what the two open leaf axioms reduce to

**What it says.**  *`ClassKilledAt i m`* is the per-class window obligation: every packing of
class `i` at side `m` has `m ≥ ŝ`, and at `m = ŝ` is a Trump image.  Both clauses of the main
theorem follow from these obligations alone (`lower_bound_of_classes`,
`uniqueness_of_classes`) — this is the shape in which the certificate campaigns discharge
`stratum_kill` and `trump_residual`, class by class (`classKilledAt_of_tree`,
`classKilledAt_of_slabs`, `classKilledAt_of_chain` in `Composition.lean`).
*Lemma SLIDE* (`slide_crowd`): under K0-O1 (k1_00's monotone kill of the corner pin on
`[lo, hi)`), EVERY packing at a side `m ∈ [lo, hi)` has, at every corner, two distinct squares
meeting the closed corner box `[0, 1 − (hi − m)]²` — the second intruder has depth `≥ hi − m`.

**Why it matters.**  It turns the three-axiom statement of `TopLevel.lean` into a finite list
of per-class, per-window certificate obligations with a known Lean shape (closed zone-tree,
tube certificate, slab kills, crowd chain), and Lemma SLIDE is the class-blind floor every
k0 argument starts from (`docs/proofs/k0_blocked_side.md` §3).

**How it is proved** (`Composition.lean`, `Slide.lean`, A86/A93): the composition glue of
`TopLevel.lean` re-based on `ClassKilledAt`; SLIDE by the teleport of a lone corner intruder
into the corner slot (`k0free_kill`).
-/

namespace PackingCert.S11

open Set

/-- **The lower bound from the per-class obligations on the window.** -/
theorem lower_bound_of_classes (hcls : ∀ i : StratumIdx, ∀ m ∈ wnd, ClassKilledAt i m) :
    ∀ s : ℝ, Fits 11 s → shat ≤ s :=
  s_eleven_ge_of_classes hcls

/-- **The uniqueness clause from the per-class obligations at `ŝ`.** -/
theorem uniqueness_of_classes (hcls : ∀ i : StratumIdx, ClassKilledAt i shat) :
    ∀ Q : Fin 11 → Set RP, IsPacking 11 shat Q →
      ∃ (f : RP → RP) (e : Equiv.Perm (Fin 11)),
        IsCtrSym shat f ∧ ∀ i, Q i = f '' (zhat (e i)).set :=
  s_eleven_unique_of_classes hcls

/-- **Lemma SLIDE.**  Under K0-O1 on `[lo, hi)`, every corner of every packing at
`m ∈ [lo, hi)` is met by two distinct squares at depth `≥ hi − m`. -/
theorem lemma_SLIDE {lo hi : ℝ} (hK1 : ∀ c : Fin 4, SlabKill {⟨c, 0, 0⟩} lo hi) (hlo1 : 1 ≤ lo)
    {m : ℝ} (hlo : lo ≤ m) (hhi : m < hi) {z : Cfg} (hz : CfgPacking m z) :
    CrowdBox m (1 - (hi - m)) z :=
  slide_crowd hK1 hlo1 hlo hhi hz

#print axioms lower_bound_of_classes
#print axioms uniqueness_of_classes
#print axioms lemma_SLIDE

end PackingCert.S11
