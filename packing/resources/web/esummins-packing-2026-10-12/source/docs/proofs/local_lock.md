# LOCAL-LOCK — the extremal route made exact for every n, the corner ARM, Lemma RADIAL, and what the local obligation is — A233, 2026-09-15

The PI (17:50): "an analytical reason for at least one simple square, since that would generalise up and allow us to ignore k0
for higher n without re-searching."  This file (i) states the extremal route in n-general form and says which of its pieces are
proved for every n, (ii) proves LOCALITY (the lock of a corner meeter is decided by its row partners, all inside a corner ARM of
n-independent size) and counts the local structure list, (iii) proves the n-general force facts behind the PI's gear rule —
Lemma RADIAL (a loaded arm is held in by a corner-ward push from OUTSIDE it), Corollary CHAIN (the loaded component of a crowd
reaches a far wall), Lemma NO-SELF-STRESS — and reads NOCRIT-SEL as the geometric gear rule, and (iv) says plainly what remains:
the residue is NOT a local problem, the brief's per-corner target is FALSE (Trump's own TL corner), and the exact obligation is
LOCKED-CROWD-FREE(n), a global frame statement at the optimum.  Tags: [T] proved, [S] routine given cited items, [M] measured,
[F] false (with the witness), [C] obligation.  Sources: `one_flush.md`, `ring_swap.md`, `realign.md`, `two_grains.md`,
`wall_torque.md`, `k0_count.md`, `k0_route.md` §3, `drain_flow_k0.md`, `theorem_u.md`, `nocrit_k0_blocked.md` (Lemma K,
CLUSTER, NOCRIT-SEL), `noroom.md` (ROT, RES-LOCK), `lockfree.md` (ROT-W, LOCKED, LINE), `drain_sel.md` (SUPPLY),
`sideband.md` (F1, F2, A2, B1).  Code `attempts/A233-local-lock/code/` (`arm233.py`, `summarise233.py`, `census233.py`,
`pages233.py`, `test233.py`), results `results/arm233.{jsonl,md}`, `census233.md`; pages
`docs/residue_map/campaigns/A233-local-lock/`; Lean `Statements/Open/LocalLock.lean`.

## 0. Verdict

> **[T] The extremal route is n-general and gives ONE-FLUSH(n) in its VALUE form from ONE residue** (§1): for every n with
> s(n) < ⌈√n⌉ there is an optimal packing z* (Ψ-minimal among the packings at side s(n)) at which no square RETREATS; so
> either z* has a singly-met corner — and K0-FREE teleports it: **s(n) is attained by a packing with a flush corner, the
> census of n squares starts from a settled corner** — or z* is a FOUR-CROWD every meeter of which is retreat-free (hence
> LOCKED).  The residue **LOCKED-CROWD-FREE(n)** [C]: no optimal packing below ⌈√n⌉ is a retreat-free four-crowd.  Lean
> `locked_crowd_free` (axiom), `no_retreat_of_psiMin`, `exists_optimal_singly_met`, `optimal_psiMin_not_stuck` (theorems).
> Theorem U and the uniqueness clause are n = 11-only and are not needed for the value.
>
> **[F] The brief's target — "at a k-maximal minimiser below ⌈√n⌉ no corner box is doubly met by locked meeters" — is false
> at n = 11 by the canary itself:** Trump's TL corner is doubly met (the nick sq4, the 40.18° carrier sq6), both meeters are
> LOCKED and PUSHED (`lockfree.md` §5: 5/5 LOCKED), and Trump is k-maximal (three flush corners).  A locked 2-crowd at the
> optimum exists; what cannot exist is FOUR of them.  Nothing per corner can prove ONE-FLUSH.
>
> **[T] LOCALITY** (§2): every row partner of a corner meeter has its centre within √2 of the meeter's, hence inside the
> ARM A_c = [0, 1 + 2√2]² (centres in [½, 1 + 3/√2)²), n-independent; the Gordan certificate of a lock reads those rows only,
> so LOCKED is decided inside the arm; the four arms' row-partner sets are disjoint for s ≥ 2 + 3√2 = 6.243 (n ≥ 39).  [M]
> 1 227 / 1 227 doubly-met corners of A217's 486 witnesses + Trump: every holder inside the arm.  **[T] But the lock
> problem is not local:** NOCRIT-SEL's retreat cluster of every meeter is wall-anchored or anchored at another corner's
> crowd, and both anchors lie OUTSIDE the arm once s > 2 + 2√2 = 4.83 — the chain always leaves the arm.  [M] on the
> witnesses: 3 955 of 4 908 clusters anchored (3 892 at a far wall, 3 652 through another crowd's meeter — the ring); all but 8
> leave the arm, and the 8 are crowd-anchored inside it at n = 11, where s < 4.83 as the lemma allows; the 953 unanchored
> clusters are the witnesses' retreatable rattler meeters (772 retreat alone).
>
> **[T] Lemma RADIAL** (§3, any n, any FJ point): for any set U of squares, Σ over the rows joining U to the outside of
> λ ⟨force on the member, its position from the corner⟩ = −Σ over the internal rows of a POSITIVE quantity: a loaded arm is
> held in by a net corner-ward push from outside it.  **Corollary CHAIN:** the loaded component of a crowd reaches a far
> wall with load.  **Lemma NO-SELF-STRESS:** every FJ point of the side problem has λ₀ = 1.  [M] identity residual ≤ 5·10⁻⁷
> on 1 187 corners, internal term ≥ 0 on all, CHAIN 1 013 / 1 013 loaded crowds reach a far wall (A219's RING measured on
> 193, now a one-line theorem for all n).  This is the PI's gear rule exactly — and it is satisfied by Trump's TL crowd
> (its chain is the strip to the bottom and right walls), so it excludes nothing by itself.
>
> **[C] What the route reduces to** (§4): not a finite local obligation.  The arm's structure list is finite and small (§2.3:
> ≤ 10⁷ labelled row lists per corner at H ≤ 5 holders against A219's 2.6·10¹¹), but it decides only LOCKED, and locked
> corners exist at the optimum; the closing statement must couple the four chains through s < ⌈√n⌉, i.e. it is
> LOCKED-CROWD-FREE(n) = LOCK-FREE⁺ restricted to optimal packings, weaker than every form the lab has stated and still a
> global frame question.  At n = 11 it is the k0_00 obligation on [3.82, ŝ] exactly as `ring_swap.md`/`realign.md` left it.
> k0_00 unchanged.

## 1. The extremal route, n-general (task 1)

**Setting.**  n ≥ 2 unit squares in [0, s]², s ≥ 2 + √2 (so that a square meets or is tangent to at most one corner box,
CC-1(ii), and an intruder's far-wall rows have margin ≥ s − 1 − √2 > 0); corner frame (u, v); μ_c(Q) = min_{p∈Q} max(u, v),
d_c(Q) = max(0, 1 − μ_c(Q)); Q meets c iff d_c(Q) > 0; Ψ(z) = Σ_c Σ_i d_c(Q_i); M(s) = the packings at side s.

| piece | statement | n-general? | where |
|---|---|---|---|
| D1 attainment | s(n) = min side is attained; M(s(n)) compact | [T] any n (compactness in 3n + 1 coordinates) | `attained_thm` n = 11; [S] |
| K0-FREE / teleport | a corner met by ≤ 1 square exchanges, same side, into a flush corner | [T] any n, s ≥ 2 | `teleport_packing`, `swap_packing` (n = 11 Cfg); [S] over `IsPacking n s Q` |
| k-maximal minimiser | among the minimisers take one with the most flush corners; every non-flush corner is doubly met | [T] any n, s ≥ 2 (else a teleport adds a flush corner) | `fj_census_k0.md` K0-2 at n = 11; this file |
| Ψ-minimal minimiser | Ψ attains its minimum on M(s(n)); at it nothing RETREATS | [T] any n (compactness + Lean `no_retreat_of_psiMin`) | `nocrit_k0_blocked.md` SEL-Ψ; `LocalLock.lean` |
| NOCRIT-SEL | at the Ψ-minimiser every retreat cluster C_e(Q) is wall- or crowd-anchored | [T] any n, s ≥ 2 + √2 (Fact A, Lemma K, CLUSTER use nothing else) | A90 §3 (stated at n = 11) |
| ROT, ROT-W (LOCKED) | every intruder of the Ψ^(w)-minimiser is HELD and W-HELD | [T] any n, s ≥ 2 + √2 | A103 §2, A105 §1.2 (stated at n = 11) |
| PUSH, HOLD, TWO-CONTACT, ONE-TILTED, CEIL, FLUSH | corner-pair and load facts | [T] any n (already stated so) | `k0_count.md`, `wall_torque.md`, `two_grains.md` |
| RES-LOCK(m) | the residue: K0-BLOCKED, every intruder LOCKED, every cluster anchored | defined for any n; = ∅ is [C] | `noroom.md` §6 |
| Theorem U, basin, k1-b | one-square rigidity of Trump; every packing at ŝ is an image | n = 11 ONLY (uniqueness) | `theorem_u.md` |
| LOCK-FREE⁺(< 4), DRAIN-SEL(W) | no K0-BLOCKED packing at m < 4 is fully locked | n = 11 thresholds; the n-general form is §1.2 | `lockfree.md`, `drain_sel.md` |

**1.1 [T] Theorem EXTREMAL(n).**  Let s = s(n) < ⌈√n⌉ and let z* minimise Ψ on M(s).  Then (a) z* is optimal; (b) no square of
z* RETREATS — there is no packing z′ at side s agreeing with z* off one square i with d_c(Q′_i) < d_c(Q_i) and no depth larger
(Ψ(z′) < Ψ(z*)); (c) hence either some corner of z* is met by ≤ 1 square, or z* is a four-crowd all of whose meeters are
retreat-free.  Retreat-freedom implies LOCKED: a strictly opening first-order motion of one square (ROT / ROT-W) is a retreat
(it stays a packing, lowers d_c, and — s ≥ 2 + √2 — touches no other corner box), so ¬LOCKED ⇒ Retreats.  *Proof.* (a) M(s) is
the set of optimal packings.  (b) Lean `no_retreat_of_psiMin`.  (c) Definitions.  ∎  Consequences [T]: in case (i) K0-FREE
(any n) gives an optimal packing with a flush corner — **ONE-FLUSH(n), VALUE form**: s(n) = s_{k1}(n), the census starts
from a settled corner; k0 need not be searched at n once LOCKED-CROWD-FREE(n) is known.  The "every optimal packing" form of
`one_flush.md` §1 (uniqueness at n = 11) is not reached by any extremal argument: it needs Theorem U / the basin.

**1.2 [C] LOCKED-CROWD-FREE(n).**  No optimal packing below ⌈√n⌉ is a four-crowd all of whose meeters are retreat-free.  Lean
axiom `locked_crowd_free`; `exists_optimal_singly_met` derives ONE-FLUSH(n) (value) from it and the existence of a Ψ-minimal
optimal packing; `optimal_psiMin_not_stuck` is the n = 11 corollary (m < 4 via `ceil_sqrt_eleven`).  Relation to the lab's
statements: LOCK-FREE⁺(< 4) ⇒ LOCKED-CROWD-FREE(11) ⇒ ONE-FLUSH(11) value; DRAIN-SEL(W) is its window form at n = 11 with the
menu as the retreat.  It is consistent with every packing on disk: the fully locked frames (A104's 4.000237, 4.001525) are
above the optimum, and every four-crowd at side < 4 that A222/A231 tested raises.  Evidence at n ≠ 11: the 21 records (three
flush corners each) and CROWD-ABOVE's crowds, which are rattler crowds (§2.4, page (c)).

## 2. LOCALITY and the arm (task 2)

**2.1 [T] Lemma LOCALITY (any n).**  Frame the corner at the origin.  (i) A meeter Q of the open unit box has centre
z_Q ∈ [½, 1 + 1/√2)² (F2: ≥ ½ in the quadrant; F1: a point p ∈ Q with p < (1, 1) and |p − z_Q|_∞ ≤ 1/√2).  (ii) A square R
touching Q (a vertex-on-edge or edge-edge contact — every pair row of Q's certificate is one) has |z_R − z_Q|_∞ ≤ √2 (a common
point p: |z_R − p|_∞, |p − z_Q|_∞ ≤ 1/√2).  (iii) Hence every row partner of a meeter has centre in the ARM CENTRE BOX
[½, 1 + 3/√2)² = [0.5, 3.121)² and body in the ARM A_c = [0, 1 + 2√2)² = [0, 3.828)².  (iv) The Gordan certificate of LOCKED
(ROT's self-stress of Q's wall rows, pair rows and virtual corner rows; ROT-W's force cone) reads only Q's own rows, whose
data are the poses of Q and its row partners: **LOCKED at c is a property of the poses inside A_c**.  (v) For s ≥ 2 + 3√2 =
6.243 no square is a row partner of meeters of two different corners (its centre would be within 1 + 3/√2 of two opposite
walls), so the four locks are decided on four DISJOINT sets of squares; for s ≥ 2 + 4√2 = 7.657 the arms themselves are
disjoint.  Since s(n) ≥ √n, (v) holds for all n ≥ 39 (resp. n ≥ 59); at n = 11 the arm (3.83) is nearly the container
(3.88) and every square is in every arm.  ∎  [M] `arm233.md`: 1 227 / 1 227 corners have every holder within √2, inside the
centre box and inside the arm (`locality` fields).

**2.2 [T] The chain leaves the arm.**  NOCRIT-SEL: at the Ψ-minimiser every intruder Q and cardinal retreat e have C_e(Q)
wall-anchored (a member touches the far wall in direction e: its centre coordinate ≥ s − 1/√2) or crowd-anchored (a member
is a meeter or tangent square of another corner c′: its centre within 1 + 1/√2 of c′'s walls, i.e. coordinate ≥ s − 1 − 1/√2)
or a W-GEN rate tie.  Both anchors have a coordinate ≥ 1 + 3/√2 as soon as s ≥ 2 + 2√2 = 4.83 (wall) resp. s > 2 + 2√2
(crowd): **for s > 4.83 every retreat cluster of a locked meeter contains a square outside the arm's centre box.**  So the
gear rule of the brief — "a holder chain along a wall inside a convex corner ends at a wall row or leaves the arm" — is
NOCRIT-SEL read in the arm: the chain of pressers ends at a far wall (a wall-to-wall column through the crowd) or at the
next corner's crowd (a ring), never inside the arm.  [M] table in `arm233.md`: on HELD witnesses 1 774 / 1 836 clusters
anchored, all leaving the arm (1 528 through another crowd's meeter); the 62 unanchored single-square clusters are the
witnesses' rattler meeters (local optima of a bounded problem, not Ψ-minimisers).

**2.3 [T+M] The local structure list, counted (`census233.md`).**  What LOCKED reads at one corner with meeters A, B: their
cells (A2: distinct cells of the 2 × 2 grid at 1; B1: no meeter on both walls; NW can touch only the u-wall, SE only the
floor, NE neither), their wall rows (0 / vertex / flush edge), the partner rows (0 / 1 / 2), each meeter's depth type
(Lemma K: X, Y, D-vertex, D-edge, axis tie) and each meeter's holder rows (h holders, 1 or 2 rows each).  Labelled count
with h ≤ H per meeter: H = 3: 3.75·10⁵; H = 4: 8.4·10⁵; H = 5: 1.65·10⁶; H = 6: 2.9·10⁶ per corner — against 2.6·10¹¹ for
A219's four-corner structures with cross-corner holders.  [M] Realised on the witnesses: 75 distinct signatures (cells |
wall bits | partner | holders | cross-crowd holders) on 1 227 corners, max 3 holders and 13 rows per meeter; the {NW, SE}
cell pair with both meeters wall-touching and in contact is the common one (page `arm_census.svg`), Trump's TL among
them.  **The list is finite and small, and it does not close anything**: the per-structure question it decides is "are
both meeters locked?", and the answer YES is realised at the optimum (Trump TL).

**2.4 [F] The per-corner target.**  "No corner box is doubly met by locked meeters at a k-maximal σ-minimiser below ⌈√n⌉":
Trump (n = 11, side 3.877 < 4, three flush corners) has TL doubly met by sq4 (nick, depth 0.155, rows: the wall, sq6,
sq7) and sq6 (carrier, depth 0.168, rows: the top wall, sq4, sq9), both PUSHED
with explicit certificates (`lockfree.md` §5, §6), Lemma RADIAL's internal load 0.516 supplied by sq7 (0.199) and sq9 (0.317)
— page `arm_trump_ring_crowd.svg` (a).  A locked corner is the normal way a load path ENDS at a corner; ONE-FLUSH is about
there being a corner where no load path ends.

## 3. The force facts behind the gear rule (task 3)

Row model (A217/A219, any n): near-wall rows q_u(i) ≥ 0, q_v(i) ≥ 0 at corner c (q a vertex of Q_i), far-wall rows
s − q_u ≥ 0, s − q_v ≥ 0, pair rows n·(q_k(j) − c_i) − ½ ≥ 0 (owner i, outward edge normal n of i, q_k(j) the corner of j
minimising n·q), tilt-only rows (dominance, tilt bounds) with zero centre gradient.  FJ point: λ₀ ≥ 0, λ ≥ 0, λ₀ + Σλ = 1,
λ₀ e_s = Σ λ_k ∇g_k, complementary slackness.  The centre block reads: for every square i, Σ_k λ_k ∇_{c_i} g_k = 0.

**3.1 [T] Lemma RADIAL (any n, any FJ point, any corner frame, any set U of squares).**  Let y_U be the dilation of U's
centres about the corner (v_i = c_i for i ∈ U, ω = 0, outsiders fixed).  Then
  Σ_{k external} λ_k Σ_{i∈U} ⟨∇_{c_i} g_k, c_i⟩ = −Σ_{k internal} λ_k ⟨∇g_k, y_U⟩ ≤ 0,
where INTERNAL = pair rows with both squares in U and near-wall rows (c's two walls) of members, EXTERNAL = pair rows with
one square in U, far-wall rows of members, crowd rows; and every internal row has ⟨∇g_k, y_U⟩ ≥ 1 (pair) resp. ≥ ½ (wall).
So the right side is < 0 iff some internal row is loaded.  *Proof.*  Dot the centre balance of each i ∈ U with c_i and sum.
Pair row (owner i, other j, both in U): ∇_{c_j} g = n, ∇_{c_i} g = −n, contribution n·(c_j − c_i) = ½ + g_j(n) ≥ 1, using the
activity n·(q_k(j) − c_i) = ½ and n·(q_k(j) − c_j) = −g_j(n) ≤ −½ (the selected corner is j's extreme point against n).
Near-wall row of i: ∇_{c_i} g = e_u, contribution c_{i,u} ≥ ½ (F2).  Tilt-only rows contribute 0.  ∎  Reading: λ_k ∇_{c_i} g_k
is the force of row k on square i, so an external row with ⟨F, c_i⟩ < 0 pushes a member TOWARD the corner (its radial
component); a loaded arm needs such a push from outside.  With U = {A, B} this is Lemma HOLD with the case analysis
removed (the push is radial, not necessarily along the wall) and LOAD replaced by "any internal row loaded".

**3.2 [T] Corollary CHAIN.**  Let U* be the loaded component of the meeters of c (closure under loaded pair rows).  If any
row of U* ∪ {c's walls} is loaded — in particular if a meeter is loaded at all — some far-wall row of U* is loaded: **the
loaded component of a loaded crowd reaches a far wall.**  (External pair rows of U* are unloaded by construction; crowd
rows, if present, are the other external source.)  *Proof.* RADIAL with U = U*.  ∎  [M] 1 013 / 1 013 loaded crowds on the
witnesses (413 HELD, 583 CROWD, 17 genuine k0/settled FJ points, Trump); A219's "free FJ LP infeasible 193 / 193" is the
special case "walls + meeters alone cannot balance" (U = the eight meeters, whose external rows to non-meeters are absent by
hypothesis): now a theorem, for all n.

**3.3 [T] Lemma NO-SELF-STRESS.**  An FJ point of the side problem in this row model has λ₀ = 1.  *Proof.* λ₀ = 0 gives
Σ_{far-wall rows} λ = 0 (the s-component of stationarity); RADIAL with U = all squares in the BL frame then forces every
pair row and every BL-wall row unloaded, and the TR frame forces the TR-wall rows unloaded; only tilt-only rows could carry
λ, and a self-stress among dominance rows alone does not involve the side.  ∎  (A87 §5.4's "o012 self-stress" is of that
degenerate kind.)  Consequence: Σ_{far-wall rows} λ = 1 in every corner frame, and Σ_pairs λ_k (½ + g_j(n)) + Σ_{near} λ c ≤
s − ½ — the virial budget: the total compressive pair load is < s.

**3.4 [F] Why none of this closes.**  RADIAL / CHAIN hold at Trump (canary: TL's chain is the strip to the far walls, the
push 0.516 supplied by sq7, sq9), at the ring (BL's push supplied by the ADJACENT crowds' meeters 6 and 2 — the chain is the
ring, page (b)), and at every k ≥ 1 packing: they are the structure of a load path ending at a corner, not an obstruction.
The four-corner supply count (drain_sel SUPPLY (iv), k0_count's 12 > 11, the PUSH-LINE count of lockfree §3.6) is vacuous by
planarity and by the ring (nine squares balance a four-crowd at side 4.11).  What RADIAL adds to the PI's gear rule is the
exact bookkeeping: the chain from a loaded crowd is a compression path to a far wall whose pair loads are bounded by s;
what it lacks is any lower bound on the LENGTH such a path occupies along a wall — a pressed contact can carry load with an
arbitrarily small along-wall advance (noroom §3 F6), which is why no chord/extent count follows.

## 4. The exact remaining obligation, and whether it is finite

**n-general.**  LOCKED-CROWD-FREE(n) (§1.2): a statement about the OPTIMUM (as `one_flush.md` §3 requires), weaker than
LOCK-FREE⁺, whose hypothesis carries LOCKED + anchored clusters + RADIAL/CHAIN at every corner and whose proof must couple
the four chains through s < ⌈√n⌉.  It is NOT a finite local obligation: (a) the local list (§2.3) is finite but decides
LOCKED, which does not contradict optimality per corner (§2.4); (b) every anchored cluster leaves the arm (§2.2), so the
residue's hypothesis is about wall-to-wall columns and rings of length ~ s, whose configuration space has interior (K0-PAIR
(b)) — a tree, not a case list — unless a length lemma for pressed chains exists (§3.4).  For n ≥ 39 (s ≥ 6.243) the locks
are independent and the coupling is purely through the chains; at n = 11 nothing is local.  **Finite-n caveat:** for s <
6.243 a square can hold meeters of two corners (the ring's floor meeters hold each other at every s ≤ 4.83, `k0_count.md`
§4), and the local list must include cross-corner holders — the survey's cases n = 5 … 29.

**n = 11.**  LOCKED-CROWD-FREE(11) on [3.82, ŝ] is RAISE(0 → 1) / STEP in the extremal form: with k1-a it empties k0_00
for the value (`no_optimal_of_kill` with `optimal_psiMin_not_stuck` in place of `optimal_not_stuck`); uniqueness at ŝ stays
with Theorem U + SWAP-RIGIDITY.  Nothing here shortens the k0 row.

## 5. Lean, files

`Statements/Open/LocalLock.lean`: `muC`, `depthC`, `Psi`, `Retreats`, `PsiMin`; `no_retreat_of_psiMin` (theorem, std axioms);
`locked_crowd_free` (axiom [C], n-general); `one_flush_value_of_locked_crowd_free`, `exists_optimal_singly_met` (ONE-FLUSH(n)
value form from the axiom + the extremal hypothesis), `optimal_psiMin_not_stuck` (n = 11) — theorems; `lake build` +
`lean/audit.py` exit 0, no sorry.  Obligations: O-ATTAIN-Ψ (the Ψ-minimal optimal packing exists: compactness, [S]);
O-TELEPORT-N (`teleport_packing` over `IsPacking n s Q`, routine); O-RADIAL (Lemma RADIAL as a Lean statement over
rational rows: bookkeeping); LOCKED-CROWD-FREE(n) [C].  Code and results as in the header; `python arm233.py;
python summarise233.py; python census233.py; python pages233.py; python test233.py` (≈ 30 s in all).
