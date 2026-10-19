import PackingCertMathlib.TopLevel

/-!
# -- OPEN: `stratum_kill` — the 162 non-Trump classes are empty on the window

**What it asserts.**  No packing at any side `s ∈ [3.82, ŝ]` has skeleton EXACTLY of a
non-Trump census class.  (Skeleton = the Young-form set of exactly-on-grid axis-aligned squares
at each corner; `InStratum i s z` = the skeleton is a D4-image of representative `i`.)

**Where the proof lives.**  Per class, a closed zone-tree at a rational side `s₀ > ŝ` with
(K)/(N) kill leaves (`checkCaseI` PASS files), (C) leaves, (D) tube leaves and (D′) atlas leaves,
plus slab kills below the tube's reach — `Composition.lean` proves `ClassKilledAt i m` from such
a tree (`classKilledAt_of_tree`, `classKilledAt_of_slabs`) and the class-blind crowd chain
(`classKilledAt_of_chain`).  The certificate campaigns: A57/A60/A61 (61 exact pin-set kills,
parametric window coverage), A86–A93 (the k0 route, Theorem N), and the shadow-tree campaigns
A180–A215 on the k5/k6 pages (`docs/residue_map/current/` lists what is alive).
Prose: `docs/proofs/k0_route.md`, `k0_blocked_side.md`, `instratum_bridge.md`,
`unique_transfer.md` (the quantifier caveat: at `s = ŝ` the K1-protected `k ≤ 4` classes must
be reached through the teleport-stuck route, `Statements/UniqueTransfer.lean`).

**Status (2026-09-14).**  OPEN.  The axiom is declared in `TopLevel.lean`; this file only
restates it so that `#print axioms` shows the dependence.
-/

namespace PackingCert.S11.OpenLemmas

/-- **[OPEN] Per-stratum kills, window form** — a restatement of the axiom `stratum_kill`. -/
theorem stratum_kill_open : ∀ i : StratumIdx, i ≠ trumpStratum → ∀ s ∈ wnd, ∀ z : Cfg,
    CfgPacking s z → ¬InStratum i s z :=
  stratum_kill

#print axioms stratum_kill_open

end PackingCert.S11.OpenLemmas
