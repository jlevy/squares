# 03 — k = 0: the no-simple-square class, what is proved, what is refuted, what is measured

**Abstract.** k0_00 is the stratum with no simple square: every corner box is met by ≥ 2 squares ("teleport-
stuck", a four-crowd), since a corner met by ≤ 1 square teleports to flush (K0-FREE).  Its exclusion on the n = 11
window is the one piece of the stratification with no certificate route (Lemma K1(ii)), and the piece that
generalises: it is Conjecture ONE-FLUSH(n) restricted to the optimum (`04`).  This note lists the theorems (K0-FREE,
SWAP/CELLS, the extremal reduction to LOCKED-CROWD-FREE(n)), every refuted route with its witness, the measured
facts, the n = 11 form STEP on the eleven cells, and the current n = 11 chain with its open links.  Tags [T]/[M]/[F]/[C].

Repository https://github.com/Esummins/packing (paths under `blob/master/`; e.g. https://github.com/Esummins/packing/blob/master/docs/proofs/k0_route.md).  Sources: `docs/proofs/{k0_route,ring_swap,one_flush,local_lock,swap_leaf,k0_count,
wall_torque,two_grains,handedness,cross,no_vv,realign,ring_capacity,pocket_waste,drain_flow_k0,noroom}.md`,
`lean/PackingCertMathlib/PackingCertMathlib/Statements/Open/`, `attempts/A275-k0-knowledge/` (the compilation:
72 [T], 17 [T-computed], 21 [M], 38 [F], 18 [C] entries).

## 1. Theorems (n-general unless marked)

* [T] **K0-FREE / teleport** (`k0_route.md` §3; Lean `teleport_packing`): a corner box met by ≤ 1 square exchanges,
  at the same side, into the flush corner square — so a packing with a singly-met corner is in a k ≥ 1 class at the
  same side.  Hence k0_00 = the four-crowds.  [T] **K0-D4** (§2): the D4 quotient of the k0 tree; [T] **K0-WIDEN**
  (§4.1; Lean `k0_widen_stmt`): the corner-box statement at side m transfers to the s0 page with pad π₀.
* [T] **SWAP / STEP / CELLS** (`ring_swap.md`; Lean `swap_packing`, `cells_swap`, standard axioms): see `02` §1.
  **RAISE(0 → 1)** = "some admissible family Π with a corner cell has |M(Π)| ≤ |Π|"; with the k1 tree it empties
  k0_00 (Lean `no_packing_of_raise`, from the axiom `raise_zero_one`).  [F] RAISE is NOT a counting consequence:
  the perimeter sweep needs Σ|M_k| ≤ 8 cells while ≥ 9 squares meet the 8 window cells of a four-crowd — the count
  closes only for n ≤ 4 (`ring_swap.md` §0).
* [T] **The extremal reduction** (`local_lock.md` §1, A233; Lean `no_retreat_of_psiMin`, `exists_optimal_singly_met`,
  `optimal_psiMin_not_stuck`): for every n with s(n) < ⌈√n⌉ take an optimal packing minimal for the retreat
  potential Ψ = Σ_corners Σ_squares d_c(Q); nothing retreats there (compactness + Fritz-John); so either it has a
  singly-met corner — s(n) is attained with a flush corner — or it is a four-crowd all eight of whose meeters are
  retreat-free (LOCKED).  **Residue: LOCKED-CROWD-FREE(n)** [C] (Lean axiom `locked_crowd_free`): no optimal packing
  below ⌈√n⌉ is a retreat-free four-crowd.  [T] LOCALITY: a corner meeter's lock is decided inside the arm
  [0, 1 + 2√2]²; [T] but the retreat cluster leaves the arm (wall- or crowd-anchored), so the lock problem is global.
* [T] Local facts at a locked corner: PUSH, HOLD (`k0_count.md` §2–3, Lean axiom `lemma_PUSH`), TWO-CONTACT,
  ONE-TILTED (`wall_torque.md`), WEDGED-SEAL (`02` §5), RADIAL / CHAIN (a loaded arm is held in by a corner-ward
  push from outside; the loaded component reaches a far wall), NO-SELF-STRESS (every FJ point has λ₀ = 1), RING as
  a theorem (walls + meeters alone never balance a crowd), NO-VV (`no_vv.md`: the feasible set at a loaded vertex-
  on-vertex contact is a union of two half-spaces; two theorems, Lean `no_vv_pair`), CROSS-PLANAR (`cross.md` §4:
  two bracing chains across the container share a square), CEIL and FLUSH (`two_grains.md`: a packing of n flush
  squares has side ≥ ⌈√n⌉; Lean `flush_eleven_four`).
* [T] n = 11: `fourcrowd_dead_of_step_kill` (Lean, `realign.md` §5): STEP on the window + the k1 kill excludes
  four-crowds; so ONE-FLUSH(11) on [3.82, ŝ] ⟺ STEP there.

## 2. Refuted routes, each with its witness

| route | statement tried | verdict | witness / reason | source |
|---|---|---|---|---|
| torque sign rule | a signed corner torque separates four-crowds | [F] | every candidate is an identity at every FJ point or fails at Trump's TL corner (T = +0.035) | A217 `notes/torque.md` |
| 12 > 11 count | four doubly-met corners need 8 meeters + 4 holders | [F] | the true sharing bound is FOUR (a centre diamond holds two corners); a 9-square force-balanced ring exists at side 4.11 | A218 `k0_count.md` §5 |
| sweep count | settle corners one by one; the ring is not self-supporting | [F] as a count | ≥ 9 squares meet the 8 window cells; closes only for n ≤ 4 | A222 `ring_swap.md` §0 |
| click monotonicity | the chain formula decreases toward alignment | [F] | the corner-anchored ladder Λ(θ) = 2 + 4t/(t²+1) is minimal at 45° and rises to 4 at alignment; CLICK-DOWN ⟺ STUCK-4, the obligation itself | A223 `two_grains.md` |
| area / capacity counts | a stable ring needs side ≥ ⌈√n⌉ by capacity | [F] | Theorem NO-CLOSURE: band + core hold exactly m² − 3 squares, one for every n packing below m; no loaded tilt floor exists (A89) | A236 `ring_capacity.md` §3 |
| handedness sums | a convex container gives no net torque; count handedness | [F] | TORQUE-ID is an identity in all three forms; no scalar over 1,393 stressed witnesses separates four-crowds from ≤ 3-crowd optima | A234 `handedness.md` |
| CROSS / OPPOSE | corner jams need opposing torques; the X cannot close | [F] OPPOSE | locked corners are same-handed 215 : 11 (HELD 121 : 9, CROWD 50 : 1, free FJ 44 : 1); CROSS-PLANAR [T] but the shared square may be flush (realised at Trump) | A240 `cross.md` |
| lower tilt bounds | a locked meeter has tilt ≥ θ_min > 0 | [F] | θ_min(s) = 0 on [3.82, 4): the pinwheel common-tilt slice has positive margin down to 0.1°; CROWD-ABOVE tilts ε/2 | A253, A89, `one_flush.md` §3 |
| every LOCAL charge | corner waste / chord deficit / wall budget / per-corner side charge | [F] | CROWD-ABOVE: at every side S > s(n) a four-crowd exists (n = 26, 28, 29, 37, 40, 50, 51, 55 verified); a crowd costs O(ε) | A226 `one_flush.md` §3 |
| pocket waste | the ring's jagged pocket cannot hold n − ring | [F] analytic | waste is O(tilt), no tilt floor; specific pockets close by certificate (PIERCE, 0.1 s each) | A237 `pocket_waste.md` |
| drain-flow H1 | no k0 configuration below ŝ is FJ-critical, as a cover | [T] two lines, [M] not cheaper | DF-K0 holds in MinForm; H1 as a certificate is a configuration-space cover priced at ≥ the tree | A87 `drain_flow_k0.md` |

The lesson, in the PI's words after A226: the statement must be about the OPTIMUM, not about all packings, and
the proof must be a global improvement argument (an exchange or motion that lowers the side), not a local charge
and not a per-corner lemma — Trump's own TL corner is a locked 2-crowd at the optimum (`local_lock.md` §0 [F]).

## 3. Measured facts (all consistent with the conjecture)

* [M] **No free Fritz-John point has four doubly-met corners**: 0 of 883 genuine FJ points (sides 3.8867–5.0; at
  most three, once) — A217.  Every four-crowd forced by crowd rows needs an external pull at ≥ 1 corner.
* [M] **No valid teleport-stuck packing below side 4.0014**: every four-crowd local optimum found lives at
  S ≥ 4.0014; every witness below side 4 has a corner met by ≤ 1 square (A217, A222; `one_flush.md` §0).
* [M] **Every four-crowd witness has an improving corner swap**: on 792 corner-swapped cases (686 corners of the
  193 held four-crowds, 74 of the 40 window-shaped over-met crowds, A226's eight CROWD-ABOVE crowds) the corner
  swap is always possible and the shrink at fixed tilts is strictly side-lowering on 783 of 792, never blocked
  (A231 `realign.md` §2); the ring swaps at once at its own side 4.11 (A222).
* [M] **Crowd rings below 4 hold one square**: the eight-square crowd ring at S ∈ {3.90, 3.95, 3.99} leaves a
  pinwheel pocket that holds ONE further square, not three (A226 `ring11_226.jsonl`); the window family ring(S, θ),
  S ∈ [3.82, ŝ], θ ≤ 30°: capacity 1 by certificate (A237).  8 + 1 = 9 < 11.
* [M] Survey: all 21 record packings below ⌈√n⌉ (n = 5 … 55, re-verified by exact SAT from Ellsworth's coordinates)
  have ≥ 3 flush corners; 20 have four; Trump is the only one with a doubly-met corner (A226).

## 4. The n = 11 form: STEP on the eleven cells

The k0 residue at n = 11 is **eleven converged-alive cells** (`docs/shadows/k0v4/`, A115/A148: each an LP record at
τ = budget with one conditioned square H in a 0.105 × 0.105 centre box and tilt bin 30°–45°, budget 10).  [T] The
**swap leaf** (`swap_leaf.md`, A232; Lean `swap_leaf_dead`, standard axioms): a cell carrying an injection naming
the exchanged roles X, |X| fixed unit squares inside every container of the window, pairwise disjoint, one at the
corner slot, and an exact miss per (square, role outside X), is EMPTY wherever the k1 class is dead; |X| = 1 is
K0-FREE, |X| = 2 is the PI's STEP.  Verifier `verify_swap232.py` (stdlib), controls at n = 5 PASS, seven corruption
tests refused.  [M]/[F] On the eleven cells the leaf cannot fire: ten roles are unboxed, so |X| = 10 at every
corner — the leaf asks for ten disjoint unit squares in [0, 3.82]² missing H's reach set, an object barely weaker
than the theorem; the search places 6–9.  STEP is certifiable only at crowd-conditioned nodes (eight boxed roles,
|X| = 5), which is the k0 cascade priced at 3,200–7,000 CPU-h (`k0_route.md` §8).  [M] A191: the first frozen-
verifier node kills on cell l1_104 (17 of 64 S2 nodes, 23 S3 nodes); no cell closed.

## 5. The current n = 11 chain (`k0_route.md` §13, A258–A281) — the normal-ring route

A second route, independent of the LP cells, reduces k0 at n = 11 to a chain of ring statements: [T] NORMAL FORM
(Lean `exists_normalForm`: a lexicographic maximiser of touch / row / retreat potentials exists); [T] BAND-COUNT;
[T] MEETERS SPLIT (a doubly-met box has ≤ 1 toucher per wall, none touching both; the rest float); [T] COUNT + ROOM
⟹ n ≤ 9 per corner type (Lean `jam_count_core`); [T] BOX-MEETERS(11); row classification; window exclusions; locks
and open pairs; ROOM (every free square of the hybrid normal ring contains the centre); [T] 8 + 1 < 11
(`openPairs_excludes`, `k0_value_of_factors`).  **Open links** (as of A281): the per-corner sector certificates
`pair3` (not started), STRIP₂ off the ring domain (budgeted ~5·10³ CPU-h; closed by hand on the corner θ, φ ≤ 5°,
A276 `flat_x.md`), the FLOAT2 / indirect-jam CAP-2 statements (Lean axioms `bl_cap2_float2`, `float2_local`), the
gap statements of CAPACITY-2, and the [T-prose] Lean axioms (`meeters_split`, `rows_classified`, `band_count`).
Several [T-computed*] chains (A259–A266) were left running and are resumable; none is a theorem yet.

## What we ask

1. A field certificate for the n = 11 form: a measure on [0, s]², s ∈ [31/8, s0], conditioned on all four corner
   boxes being doubly met — owner sets the eight meeters' hulls (the arm [0, 1 + 2√2]² per corner), the other three
   squares charged as usual — whose total is < 11.  We supply the 193 held four-crowds and the 40 window-shaped
   crowds (`attempts/A217-torque-probe/results/witnesses217.jsonl`) as the adversaries it must beat.
2. Any angle from your charge machinery on LOCKED-CROWD-FREE(n) (the family indexed by n, `04` §4).
3. Compute: `pair3` and STRIP₂ (A262 `chain3`, A266 `strip266`: resumable, inputs in those directories).
