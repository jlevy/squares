# unique_transfer: the uniqueness clause, routed honestly (A63, 2026-09-01)

Target: the Lean axiom `unique_transfer` (`TopLevel.lean`) and, behind it, the S1 uniqueness
clause `s_eleven_unique`: every packing at side ŝ is, up to a container symmetry and a
relabelling, Trump's packing. PI ruling: the clause STAYS in the theorem. A62 finding F3 called
this the largest hole ("the selection lemma produces a DIFFERENT minimiser"). This file
(1) corrects the diagnosis — the axiom **as stated** is nearly free, and the true load sits in
`stratum_kill`'s quantifier; (2) gives the complete proof architecture for the uniqueness
clause at drain-lemma-v3 rigor; (3) reduces the new mathematics to ONE new leaf (Theorem U,
one-square rigidity of ẑ) with an executable certificate spec. Labels: [T] proved,
[S] soundness statement whose proof is routine given cited items, [C] open obligation.

Setting: D1 (attainment, `drain_lemma.md`) and the composed lower bound give: packings at side
ŝ exist iff s(11) = ŝ, and they are exactly the minimisers. Census facts from A53 L1–L3
(window-stable, L2(iv)); exchange machinery from A58 CC-2/CC-2′.

## 1 [T] The axiom as stated is implied by census exhaustiveness (a re-diagnosis of F3)

A53 L3: EVERY packing P of 11 unit squares in [0, s]² (any s in the census window) has a
uniquely defined skeleton Simp(P), one of the 1110 Young 4-tuples = 163 D4 classes. Reading
`InStratum i s z` as "skeleton exactly of class i" with classes D4-reduced, every packing at ŝ
therefore lies in exactly one stratum after applying the D4 element g that carries its tuple to
the class representative: take f = g, e = the induced relabelling, z′ = the g-image of z. This
witnesses `unique_transfer` outright. **The axiom is NOT the hole.**

The hole moved, it did not close: `s_eleven_unique` then feeds z′ to `stratum_kill`, which
quantifies over **all packings** at ŝ. For the 61+2 certified classes that is what certificates
prove (they quantify over all families — via Lemma B of `closed_disjoint_bridge.md`). For the
K1-protected classes ({k4_03, k4_05, k4_06, k4_08, k4_11, corners4} and the ten k ≤ 3 classes)
NO certificate can ever exist (A55 K1 sharpness), and the planned H10 machinery (A58 clear-corner
/ crowd pricing) binds only SELECTED minimisers — K*-maximal / teleport-stuck ones — not all
packings. So under the current axiom split, H10 as being attacked would discharge `stratum_kill`
for the bound (where `stratify` supplies a selected minimiser) but NOT for the uniqueness
composition (where z′ is arbitrary). **A62's F3 gap is real but lives in `stratum_kill`'s
quantifier, not in `unique_transfer`.** Note the axiom is still TRUE as split — at sides < ŝ it
is vacuous (no packings exist, by the bound), and at ŝ it follows from full uniqueness — but a
discharge along that route through the bound would be circular for the low-k instances at ŝ.
The non-circular discharge is §2–§4.

## 2 [S] The selection chain at side ŝ

Fix a packing z at side ŝ (frame [0, ŝ]², the container given — no embedding freedom beyond D4).

**Chain construction.** While the current packing z_j has a completable slot box B_p
(Young-ready cell, box interior-disjoint from the slot squares) met by no square or by exactly
one non-simple square, apply the CC-2/CC-2′ **exchange**: teleport a non-simple square (the
single meeter, resp. any non-simple square) to p. Each step: stays inside [0, ŝ]² (B_p ⊆
container), preserves the packing property (the box interior was free after removing the moved
square), preserves the side (σ cannot drop below the minimum ŝ, cannot rise: nothing leaves the
container), and strictly increases k = |Simp| (completability + monotonicity of simplicity in
the occupied-slot pattern, A58 CC-2 proof verbatim). k ≤ 11 forces termination in ≤ 11 steps at
a **teleport-stuck** packing z* at side ŝ: every completable box is either simple-clipped
(CC-1(iii) geometry) or met by ≥ 2 non-simple squares.

Degenerate cases (the H1 list, resolved for THIS chain — teleports need no corridor):
* *slide creating a contact mid-path / blocked corridors*: not applicable — the exchange is a
  teleport (only the endpoint matters, A58 Rem. (a));
* *σ-changing moves*: excluded above (σ pinned at the attained minimum);
* *ties between candidate moves*: any choice works; the chain is not required to be canonical;
* *simple-in-one-normalisation-only*: the frame at side ŝ is [0, ŝ]² itself; the only residual
  freedom is D4 × S₁₁, which the conclusion is stated modulo;
* *a teleported square landing on a slot of ANOTHER corner's diagram* (double-completion): k
  still strictly increases; harmless;
* *z_j with k = 11*: vacuous (no non-simple square to move — but then every box is occupied by
  simple squares and z_j is already stuck).

## 3 [S→C] The stuck endpoint is Trump: the kill layer for stuck packings

z* lies in exactly one stratum (L3). Three cases:
* class certified (all k = 6 and above via the cap, 19 + 2 k = 5, 8 k = 4, k3_00): excluded for
  every packing at ŝ by the certificate + Lemma B/B′ — PROVIDED the class's kill instantiates
  at side ŝ, i.e. has window coverage above ŝ (parametric; see closed_disjoint_bridge B.3 —
  the A57 pair k5_11/k5_16 currently does NOT instantiate at ŝ: obligation **U-O3** below);
* class = trump5: `trump_residual` + `basin` give z* = ẑ mod D4 × S₁₁ (their own open
  obligations D.TREE/D.SLAB/D.S6/E.COORD unchanged);
* class K1-protected (k ≤ 4 tier): the H10 obligation, in the form this file fixes as the
  target: **(H10-stuck) no teleport-stuck packing at side ŝ has skeleton in a K1-protected
  class** [C]. Note for A58: CC-2's proof mechanism derives the ≥ 2-meeter crowd facts directly
  from stuckness — K*-maximality is used only to GET a stuck packing — so A58's statements
  should be (and can be, with no new mathematics) re-based on "teleport-stuck", which is
  exactly what the chain of §2 delivers. H10-stuck is weaker than a ∀-packings kill and
  strictly sufficient here.

Conclusion of §2+§3: z* = g·(ẑ ∘ e) for some g ∈ D4, relabelling e. [modulo C-obligations]

## 4 The collapse: transferring uniqueness back along the chain

The chain moved squares, so z ≠ z* in general; F3's point. The transfer back is ONE lemma:

**Theorem U (one-square rigidity of ẑ) [C — the single new leaf].** Let P be a packing at side
ŝ consisting of 10 squares of ẑ (exact positions and orientations) together with one further
unit square Q. Then Q is the missing square of ẑ, i.e. P = ẑ.

**Collapse argument [T, given U].** Induct down the chain. z_{n} = z* = ẑ mod G; suppose
z_{j+1} = ẑ mod G. z_j differs from z_{j+1} by the position of ONE square (the teleported one):
in the normalising frame, z_j consists of 10 squares of ẑ plus one square elsewhere. By Theorem
U (D4 × S₁₁-covariant, since ẑ's symmetry class is what it applies to), z_j = ẑ mod G. Hence
z = z_0 = ẑ mod G. ∎  With §1 this proves `s_eleven_unique`'s content; the Lean split can keep
`unique_transfer` (discharged by §1) provided `stratum_kill` is re-read per §1's caveat, or —
RECOMMENDED at formalisation time — re-split into `stratum_kill_selected` (hypothesis: stuck)
plus this file's chain+collapse inside `unique_transfer`. Either split has exactly the same
leaves; do not change the axiom statements mid-campaign.

**Why Theorem U is true and how to certify it [S — executable spec].** If U failed there would
be a packing at ŝ with 10 ẑ-squares and Q elsewhere — in particular the uniqueness claim would
be false, so U is NECESSARY anyway; the point is that it is also SUFFICIENT for the whole
transfer, and it is certifiable by the existing machinery:

* *Certificate form* (11 instances, one per removed square i): a case-LP kill at a rational
  side s″ = ŝ(1 + ε) (any rational in the T1 isolating interval above ŝ works; ε ~ 1e-9 —
  e.g. s″ = 3877084/1000000), with r = 10 cores = rational under-approximations of the ten
  dilated ẑ-squares (half-side a = 1/2 − δ, tilt the rational t̂-approximation; containment
  margin δ minus the dilation offset (λ−1)·|ĉ|_∞ ≲ 3.4e-9 and the rational-rounding error —
  choose δ = 1e-4, comfortable), budget b = 1, and ONE `nofams` zone F_i = a rational box
  around the dilated missing square's (c, t) chosen with λ⁻¹F_i ⊆ the basin box
  (rBasin = 37/20000 per `theta_t_transfer.md`; any F_i of half-width ≤ 1e-3 around
  the dilated ẑ_i qualifies). PASS claim, via Lemma B run with the nofam case tracked: the
  dilated Q either meets a core — impossible: Q's interior is disjoint from the ten closed
  ẑ-squares, and a convex body with interior disjoint from a convex body cannot meet a compact
  subset of the latter's interior (separating line), cores are such subsets, and after Δ_λ the
  disjointness is strict — or is NO-exempt, i.e. (λc_Q, t_Q) ∈ F_i, i.e. z_j ∈ basin box
  (ten coordinates exactly ẑ, the eleventh within λ⁻¹F_i). Then `basin`'s equality clause
  forces z_j = ẑ. ∎ (modulo the certificates existing: they assert that the free space left by
  ten ẑ-squares supports no unit square clear of them except the true pocket — geometrically
  true with visible margins; LP cost expected small at budget 1.)
* *This is the only place in the composition where a `nofams` field is load-bearing*; the
  Lemma B analysis extends: exemption sends the dilated coordinates INTO F_i, which is the
  conclusion we want, not a leak.

## 5 Obligations ledger (what remains open for the uniqueness clause)

* **U-O1 [DISCHARGED — A65, 2026-09-01]** Theorem U's 11 re-insertion certificates: emitted
  and verified at s″ = 3877083591023/10¹² (all 11 PASS at depth 60, Σw = 0, plus a falsifier
  control whose only hole is Trump's own pocket); exact side-condition ledger and the
  Lemma B-NO + basin composition in `docs/proofs/theorem_u.md`
  (`attempts/A65-low-k-closure/certs/u_reinsert_*.json`, `results/u_ledger.json`).
* **U-O2 [C]** H10-stuck: A58's programme, re-based on teleport-stuck (no new mathematics in
  the re-base; the crowd-pricing residue is unchanged and remains THE largest open node).
* **U-O3 [C]** Window/at-ŝ instantiation of the k5_11/k5_16 kills (s0-only today — see
  closed_disjoint_bridge B.3; slack-core grid or parametric tree re-run).
* **U-O4 [C]** `trump_residual` + `basin` as already axiomatised (A60 campaign, D.SLAB, D.S6,
  E.COORD/rBasin re-emission).
* The chain and collapse arguments themselves: [T]/[S] here, Lean-formalisable against the
  census layer once `InStratum` is definitional (H2/F11).

Net effect on the ledger: A.UNIQ's content = {U-O1 (new, executable), U-O2 (= H10, re-based),
U-O3 (= F6 residue), U-O4 (= existing D/E nodes)}. No other new mathematics is required for
the uniqueness clause.

## 6 Formalisation (A78, 2026-09-02) — §1 and §2–§4 are Lean theorems

* **§1 is now literal Lean.** With the census a definition (`Census.lean`, F11/H2), the axiom
  `unique_transfer` of `TopLevel.lean` is a THEOREM (`f = id`, `e = 1`, `z' = z`: every packing
  at ŝ has a skeleton, `exists_stratum`), and so is `stratify`. The hole is therefore exactly
  where §1 put it: `stratum_kill`'s ∀-packings quantifier at the K1-protected classes.
* **§2–§4 are the Lean theorem `unique_via_chain`** (`UniqueChain.lean`): with the two open
  obligations as explicit hypotheses — `hstuck` (U-O2, H10-stuck: no TELEPORT-STUCK packing
  at ŝ lies in a non-Trump class; `TeleportStuck` = no CC-2/CC-2′ move available) and `hU`
  (U-O1, Theorem U as an interface: a packing at ŝ agreeing with a G-image of ẑ in all but
  one square is a G-image of ẑ) — every packing at ŝ is a G-image of ẑ, from `trump_residual`
  + `basin` at the stuck endpoint. The chain is a strong induction on `11 − k`
  (`skeleton_card_le`, `card_lt_teleport`: a CC-2 move raises `k` and changes one square;
  `teleport_packing`: it stays a packing at ŝ); the `k = 11` base case is stuck because an
  injective assignment of 11 skeleton slots to 11 squares is onto. `s_eleven_unique_of_chain`
  is the uniqueness clause obtained WITHOUT `stratum_kill` and WITHOUT `unique_transfer` —
  the recommended re-split of §4, realised without changing any axiom statement.
* The H1 degenerate cases are absent by the shape of the statements (A75); double completion
  is harmless (`Finset.card_lt_card` needs only `old ⊂ new`).
