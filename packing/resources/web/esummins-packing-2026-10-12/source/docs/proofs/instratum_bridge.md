# The monotone→exact InStratum bridge (F4/H10's logical half) — A63, 2026-09-01

Target: A62 finding F4. Certificates natively prove the MONOTONE form "no packing whose
skeleton CONTAINS pin-set S"; the composition's `InStratum i s z` means "skeleton EXACTLY of
class i". This file writes the two-paragraph bridge as a lemma with its exact inputs, states
K1 in one place, and fixes precisely which classes it covers. Census/notation: A53 L1–L3
(Young 4-tuples, window-stable by L2(iv)); containment = componentwise sub-diagram order ≤ on
4-tuples, acted on by D4.

## E.1 [T] Lemma K1 (kills climb containment, aliveness descends) — written home

Let S ≤ S′ be pin-sets (Young 4-tuples). (i) If a packing's skeleton contains S′ then it
contains S (transitivity of ≥ on occupied slots — slots_S(s) ⊆ slots_{S′}(s) at every side s,
since sub-diagram cells keep their (i, j) offsets and the slot map is per-cell). Hence a kill
of S (monotone form) empties the monotone class of every S′ ≥ S. (ii) Dually, if
τ*(S′) ≥ 11 − |S′| (the LP value cannot be certified: S′ is "alive", witnessed by a strictly
disjoint family per `alivewitness.py`), then τ*(S) ≥ 11 − |S|: adjoin the pin square at the
extra slot of S′ \ S to the witness family. So no certificate can ever exist for a subset of a
live class. ∎ (A55's registry statement, now in `docs/proofs/`; the witness-side uses the
strict-gap convention of A57's repaired canary.)

## E.2 [T] Lemma M→E (the bridge)

Let i be a Young class with representative tuple T, and suppose some pin-set S ≤ g·T (some
g ∈ D4) carries a kill valid at side s (in the Lemma B sense of
`closed_disjoint_bridge.md` — i.e. a certificate at a side s″ ∈ (s, s(1 + ρ/A)) with the
corpus margin ρ). Then no packing at side s has skeleton exactly of class i.

*Proof.* Suppose P at side s has skeleton exactly g′·T for some g′ ∈ D4 (class-i membership).
Then Simp(P) = g′·T ≥ g′g⁻¹·... — after applying the container symmetry h = g′·g⁻¹ ∈ D4 to P
(which permutes slots equivariantly and preserves the packing property and side), Simp(h⁻¹P) =
g·T ≥ S, so h⁻¹P **contains** axis-aligned unit squares at all slots of slots_S(s). Corollary
B′ (with the D4-image certificate, or equivalently the D4-transferred kill — L5's usual
symmetry action) forbids exactly this. ∎

Note the direction: "exactly" ⇒ "contains" is REFLEXIVITY plus D4 bookkeeping — the monotone
certificate form is strictly stronger than the per-stratum emptiness the composition needs.
There is no converse obligation for killed classes.

## E.3 [T+M] Coverage: which classes the bridge closes, exactly

By the ledger (A55 `results/cap.json`, rebuilt from PASS files; A55/k3_ext E4) and E.1–E.2:

* k ≥ 7: every tuple contains a certified k = 6 sub-tuple (A53 L5 combinatorial check, 0
  exceptions) → all strata empty wherever the 33 k = 6 kills instantiate (Lemma B window
  status per class);
* k = 6: 33/33 certified; k = 5: 19 certified + {k5_11, k5_16} via A57 trees (s0-only —
  instantiation hole per closed_disjoint_bridge B.3) + trump5 (never killed, by design);
* k = 4: 8 certified; k = 3: k3_00 certified;
* **the K1-protected remainder** — {k4_03, k4_05, k4_06, k4_08, k4_11, k4_13 = corners4} and
  the ten open k ≤ 3 classes, each ≤ some open k = 5 class — can NEVER be closed by E.2
  (E.1(ii) forbids any certificate). For these, "exactly" is the ONLY exclusion mechanism, and
  the mechanism is NOT a bridge but the H10 machinery (A58 crowd pricing), whose correct
  target form is fixed in `unique_transfer.md` §3 as **H10-stuck**. This file deliberately
  proves nothing about them — recording that fact IS the F4 discharge: the bridge lemma
  exists, its scope is exactly the certified part, and the residue is H10, not a missing
  lemma.

## E.4 Formalisation note — E.1(i) LEAN-PROVED, E.2 skeleton landed (A68, 2026-09-01)

`lean/PackingCertMathlib/PackingCertMathlib/Skeleton.lean`: slot model (`Slot` = container
corner + Young cell; `slotCentre` affine `α + β·s`, β ∈ {0,1}, matching A56 P1),
`ContainsPins` (injective slot assignment, the certificate-native monotone predicate), and
E.1(i) as `containsPins_mono` / `kill_mono` — in the indexed slot model the prose step
"sub-diagram cells keep their (i,j) offsets, so slots_S(s) ⊆ slots_{S′}(s)" IS the pin-set
inclusion, and K1(i) is restriction of the assignment. Finding: the residual mathematical
content of K1 lives entirely in the census's identification of slot indices with plane
positions, i.e. in F11/H2 — K1(i) itself carries none. E.2 is `monotone_to_exact`, with the
census interface as an explicit hypothesis `hface` ("exact class membership ⟹ ContainsPins of
the D4-normalised class tuple"); `hface` becomes a theorem only when the census is a Lean
definition (the D4 equivariance it needs is machine-checked computationally by A67 R8).
E.1(ii) (aliveness descends) is deliberately NOT formalised: it is a statement about LP values
τ* — which certificates CAN exist — i.e. completeness, never load-bearing in the composition.

`InStratum` stays opaque in `TopLevel.lean` until the Young-form census is a Lean definition
(F11/H2). When it lands, E.2 is the lemma that converts each certificate PASS into a
`stratum_kill` instance for its class; the Lean statement should take (class i, pin-set S,
D4 element g, side-window W) and the Lemma-B hypotheses as explicit arguments so that the
per-class instantiation is a table, not a proof search.

## E.5 Formalisation note — the census is a Lean DEFINITION; E.2 is LEAN-PROVED (A78, 2026-09-02)

`lean/PackingCertMathlib/PackingCertMathlib/Census.lean` pins the Young-form definition
(`skeleton s z` = per corner the cells whose whole down-set is occupied by exactly-on-grid
axis-aligned squares; all eight A72 binding choices B1–B8 are resolved at their definitions,
B1/B3/B6 as THEOREMS), enumerates the census (`censusL`, D4 action `d4Slot`/`d4Pins`,
canonical codes, class representatives `classRep`), and proves L3 as a statement about
packings — `skeleton_mem_census`: at every side `s ∈ (3,4)` the skeleton of a packing is a
census tuple (the B2 predicate is decided combinatorially and proved equal to the real
predicate on the whole window, `slotFar_iff`).  `CensusCheck.lean` verifies by `native_decide`:
1110 tuples, 163 classes, D4-closure, EXACT equality with A72's tuple set and orbit partition,
Trump in a `k = 5` class.  `TopLevel.lean`'s `StratumIdx / trumpStratum / InStratum` are now
definitions (`InStratum i s z` = "the skeleton is a D4-image of representative `i`").

* `hface` is discharged: `containsPins_skeleton` (exact ⟹ contains, by reflexivity of the slot
  assignment, injective on the skeleton at `s ∉ ℤ`).
* The D4 bookkeeping of E.2 is machine-checked: the action on points (`d4Apply`), squares
  (`d4Sq`, tilt `t ↦ (1−t)/(1+t)` for reflections, R5), slots (`d4Slot`; R8 is the theorem
  `d4Apply_slotCentre`), configurations (`d4Cfg`, preserves packings: `d4_packing`), and the
  equivariance `skeleton_d4 : Simp(g·P) = g·Simp(P)`.
* **Lemma M→E is the Lean theorem `class_kill`**: a monotone kill of some `S ≤ g·T` at side
  `s ∈ (3,4)` empties the exact class of `T` — the per-class instantiation table this section
  asked for is `class_kill T S g hS kill`.
* E.1(ii) stays deliberately unformalised (completeness); its arbiter `alivewitness` has its own
  Lean soundness statement (A78 T3, `AliveBridge.lean`).
