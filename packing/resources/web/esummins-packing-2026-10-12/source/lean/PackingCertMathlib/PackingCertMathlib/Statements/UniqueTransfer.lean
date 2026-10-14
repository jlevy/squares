import PackingCertMathlib.UniqueChain

/-!
# Uniqueness transfer — how the uniqueness clause reaches the strata

**What it says.**  *`unique_transfer`:* every packing at side `ŝ` lies (with `f = id`, `e = 1`)
in some stratum — a corollary of census exhaustiveness once `InStratum` is a definition.
*`s_eleven_unique_of_chain`:* the uniqueness clause of the main theorem follows from two
hypotheses that do NOT quantify over all packings of the low-`k` classes: (H10-stuck) a
TELEPORT-STUCK packing at `ŝ` (no CC-2 move: every completable slot box inside the container
is interior-met by some other square for every non-simple square) is not in a non-Trump class;
and (Theorem U) a packing at `ŝ` that differs from a Trump image in ONE square is a Trump image.

**Why it matters.**  As stated, `stratum_kill` quantifies over ALL packings; for the
K1-protected classes (`k ≤ 4`) at `s = ŝ` that strength is a piece of the uniqueness theorem
itself and cannot come from certificates (A55 sharpness).  The chain route replaces it: teleport
non-simple squares onto completable slots (`k` rises by `card_lt_teleport`), reach a stuck
packing, kill or land it, and COLLAPSE back along the chain by Theorem U — one-square rigidity of
`ẑ`, an 11-certificate obligation (`docs/proofs/theorem_u.md`).

**How it is proved** (`UniqueChain.lean`, A78/A86; prose `docs/proofs/unique_transfer.md`
§1–§4): strong induction on the slack `11 − k`, using `teleport_packing`,
`card_lt_teleport`, `skeleton_card_le`, and the Trump-stratum endpoint `trump_residual` +
`basin`.
-/

namespace PackingCert.S11

open Set

/-- **Uniqueness transfer.**  Every packing at `ŝ` lies in some stratum. -/
theorem unique_transfer_stmt : ∀ z : Cfg, CfgPacking shat z →
    ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)) (i : StratumIdx),
      IsCtrSym shat f ∧ CfgPacking shat z' ∧ InStratum i shat z' ∧
        ∀ j, (z (e j)).set = f '' (z' j).set :=
  unique_transfer

/-- **The uniqueness clause via the CC-2 chain + Theorem U** — without `stratum_kill` and
without `unique_transfer`. -/
theorem uniqueness_of_chain
    (hstuck : ∀ z : Cfg, CfgPacking shat z → TeleportStuck shat z →
      ∀ i : StratumIdx, i ≠ trumpStratum → ¬InStratum i shat z)
    (hU : ∀ z z' : Cfg, CfgPacking shat z → CfgPacking shat z' → IsTrumpImage z' →
      (∃ i : Fin 11, ∀ j, j ≠ i → z j = z' j) → IsTrumpImage z) :
    ∀ Q : Fin 11 → Set RP, IsPacking 11 shat Q →
      ∃ (f : RP → RP) (e : Equiv.Perm (Fin 11)),
        IsCtrSym shat f ∧ ∀ i, Q i = f '' (zhat (e i)).set :=
  s_eleven_unique_of_chain hstuck hU

#print axioms unique_transfer_stmt
#print axioms uniqueness_of_chain

end PackingCert.S11
