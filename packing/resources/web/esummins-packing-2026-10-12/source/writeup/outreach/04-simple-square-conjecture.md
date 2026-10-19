# 04 — Conjecture ONE-FLUSH(n): the simple-square conjecture, stated in the Squares Project's vocabulary

**Abstract.** For every n with s(n) < ⌈√n⌉, some optimal packing has a corner box met by at most one square;
equivalently s(n) is attained by a packing with a flush (settled) corner square.  We give the equivalent forms we
have proved equivalent, the n-general theorems that reduce it to one residue (LOCKED-CROWD-FREE(n)), the refutations
that rule out every local or counting proof, the measurements that support it, the Lean statements, and the ask:
a threshold-type certificate conditioned on four doubly-met corners, as a family indexed by n.

Prepared from `writeup/outreach_simple_square_conjecture.md` (PI draft 2026-10-07) for jlevy/squares.  Repository
https://github.com/Esummins/packing; paths below are under `blob/master/`.  Tags [T]/[M]/[F]/[C].

## 1. Terms (yours in parentheses)

A packing of n unit squares in a container [0, s]² with independent rotations and disjoint interiors.  A **simple
square** (a parent settled in a lattice slot) is a unit square at an exact slot [a, a+1] × [b, b+1], a, b ∈ ℕ,
measured from a container corner; the **corner square** is the slot at a corner; the **corner box** is the open unit
square at a corner.  A corner is **flush** iff the corner square is in the packing (then it is the box's only
meeter, Cor. B1), **singly met** iff ≤ 1 square meets the box, **doubly met** iff ≥ 2 do.  A packing is
**teleport-stuck** (a **four-crowd**; lab: k0) iff every corner box is doubly met.  s(n) is the least side; an
**optimal** packing attains it (attainment: Lean `attainment`, compactness in 3n + 1 coordinates).

## 2. The conjecture and its equivalent forms

**Conjecture ONE-FLUSH(n) [C].**  If s(n) < ⌈√n⌉ then every optimal packing has a singly-met corner.
Lean: `Statements/Open/OneFlush.lean`, axiom `one_flush` over `IsPacking n s Q`; theorems `optimal_not_stuck`,
`no_optimal_of_kill`.

Forms proved equivalent [T] (`docs/proofs/one_flush.md` §1, `ring_swap.md`):
* (a) no optimal packing is a four-crowd;
* (b) every optimal packing exchanges, by K0-FREE (Lean `teleport_packing`), into an optimal packing with a flush
  corner — the VALUE form: s(n) = s_k1(n) := inf{side : a packing with a corner slot square};
* (c) **UNCROWD(n)**: every packing below ⌈√n⌉ with all four corner boxes doubly met admits a packing of the same n
  squares at a strictly smaller side;
* (d) **RAISE(0 → 1)** on the optimum (`ring_swap.md` §0; Lean `raise_zero_one`, `no_packing_of_raise`).

The VALUE form needs SOME optimal packing to be singly met somewhere; the UNIQUENESS form at n = 11 needs EVERY
packing at ŝ to be (`03` §1).

**Why it matters for scaling.**  With ONE-FLUSH(n) every exact-value search may start at k ≥ 1: the corner slot
square is a pin, the container minus the pin is the next stratum's container, and the k-strata inherit their
kills upward (Lemma K1, `01` §3).  The centre-cell method does not need it, but its case count grows with n,
while the stratification removes a corner per level.  [C] Scaling heuristic (PI): the optimum's slack s(n)² − n
is bounded by 2⌈√n⌉ − 2 while the occupied band of a four-crowd is fixed, so the conjecture should gain force with n.

## 3. What is known (n-general unless marked)

Proved [T]:
* K0-FREE, SWAP, CELLS (`03` §1; Lean `teleport_packing`, `swap_packing`, `cells_swap`).
* **Extremal reduction** (`local_lock.md` §1, A233; Lean `no_retreat_of_psiMin`, `exists_optimal_singly_met`,
  `optimal_psiMin_not_stuck`): among optimal packings take one minimal for the retreat potential Ψ; nothing
  retreats there; so ONE-FLUSH(n) holds UNLESS that optimum is a four-crowd all eight of whose corner meeters are
  locked.  **Residue: LOCKED-CROWD-FREE(n)** (Lean axiom `locked_crowd_free`;
  `one_flush_value_of_locked_crowd_free` is a theorem).  Implication chains in Lean: RING-CAPACITY(n) ⟹
  LOCKED-CROWD-FREE(n) ⟹ ONE-FLUSH(n) value form (`RingCapacity.lean`); POCKET-CAP ⟹ the same (`PocketWaste.lean`);
  REALIGN ⟹ ONE-FLUSH (`Realign.lean`) — each hypothesis an axiom, each implication a theorem.
* Local facts at a locked corner: PUSH, HOLD, TWO-CONTACT, ONE-TILTED, WEDGED-SEAL, RADIAL / CHAIN, RING, the
  vertex-on-vertex zero-load lemma (NO-VV), CROSS-PLANAR (`02` §5, `03` §1).
* n = 11 (Lean `fourcrowd_dead_of_step_kill`): STEP on the window + the k1 kill excludes four-crowds, so
  ONE-FLUSH(11) on [31/8, s0] ⟺ STEP there.

Refuted [F], with witnesses, so a proof cannot go these ways (`03` §2 has the table):
* every LOCAL charge — CROWD-ABOVE builds a four-crowd at O(ε) above every record packing (n = 26 … 55 verified);
* the counting routes — "four doubly-met corners need 12 squares" (a 9-square force-balanced ring exists), the
  perimeter sweep, the band/core capacity count (m² − 3 ≥ n for every n with s(n) < m, Theorem NO-CLOSURE);
* torque / handedness invariants — TORQUE-ID is an identity; locked corners are same-handed 215 : 11; container
  rotation is first-order stable at a four-crowd;
* monotone grain re-alignment — the corner-anchored ladder rises toward alignment near 45°;
* lower tilt bounds on locked meeters — none exist (θ_min = 0 on [3.82, 4); CROWD-ABOVE tilts ε/2);
* the PI's second conjecture "no non-trivial optimal packing has four flush corners" — false: n = 5 and n = 10 are
  proved optimal with four flush corners, as are 18 later records.

Measured [M], consistent everywhere: 0 of 883 free Fritz-John points have four doubly-met corners; no valid
teleport-stuck packing below side 4.0014; every four-crowd witness (193 held + 40 window-shaped) has an improving
corner swap (783 of 792 strictly side-lowering shrinks); the n = 11 crowd rings below side 4 leave room for one
square, not three; 21 of 21 records below ⌈√n⌉ have ≥ 3 flush corners (`03` §3).

## 4. The sharpest open form, and what a proof must do

**LOCKED-CROWD-FREE(n) [C]:** no optimal packing below ⌈√n⌉ is a four-crowd with all eight corner meeters loaded
and retreat-free.  Equivalently the pocket statement: the loaded component of such a crowd leaves a pocket that
cannot hold the remaining n − p squares.  By elimination, a proof needs a GLOBAL improvement argument at the
optimum — an explicit exchange or motion that lowers the side — not a local charge and not a per-corner lemma
(Trump's TL corner is a locked 2-crowd at the optimum).  The witnesses say what it should do: swap one corner
(always possible on every witness), then shrink at fixed tilts (strictly side-lowering on 783 of 792, never blocked).

Scaling argument, honestly tagged: [T] a four-crowd's eight meeters occupy the perimeter band and intrude into
the centre (TILT-BAND, `ring_capacity.md`); [F] that alone never closes (NO-CLOSURE); [C] what would close is a
bound on the pocket's capacity that grows slower than n − 8 — the n-indexed family of certificates of §5.

## 5. The ask

1. **A field certificate conditioned on four doubly-met corners** — in your terms a threshold certificate whose
   charges are placed on the eight meeters' owned hulls (the corner arms [0, 1 + 2√2]² in each corner's frame,
   `local_lock.md` §2) and on the pocket, with capture conditioned on "two distinct squares meet each corner box":
   at n = 11 on [31/8, s0] this is a direct attack on STEP and would close k0_00; the adversaries it must beat are
   supplied (`attempts/A217-torque-probe/results/witnesses217.jsonl`; the ring `ring_swap_rand_0_0569_t20`).
2. **A family indexed by n**: the same certificate shape parametrised by n (or by m = ⌈√n⌉ and the record side),
   which would be the n-general statement.  We can supply the Lean statements of the equivalences, the exact
   tools (`05-toolkit.md`) and the 21-record survey with exact coordinates (`attempts/A226-one-flush/`).
3. Does the centre-cell / charge machinery give an angle on LOCKED-CROWD-FREE(n) that the lab's routes (torque,
   handedness, capacity, re-alignment) missed?  Each is written up with the exact point of failure.

Sources (https://github.com/Esummins/packing/blob/master/): `docs/proofs/one_flush.md`, `ring_swap.md`,
`local_lock.md`, `ring_capacity.md`, `pocket_waste.md`, `cross.md`, `no_vv.md`, `wedged_seal.md`, `realign.md`,
`handedness.md`, `k0_count.md`, `wall_torque.md`; `lean/PackingCertMathlib/PackingCertMathlib/Statements/Open/{OneFlush,
LocalLock,RingSwap,RingCapacity,PocketWaste,Realign,Stuck4}.lean`; `writeup/outreach_simple_square_conjecture.md`.
