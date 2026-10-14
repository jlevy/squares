# The simple-square conjecture — a note for the Squares Project / 11SquaresOptimal group (draft, 2026-10-07)

Prepared for the PI's outreach.  Everything below is stated for general n; the n = 11 specialisation and what
this lab has proved or refuted about it are marked.  Lab sources in `docs/proofs/` (ring_swap.md, one_flush.md,
local_lock.md, ring_capacity.md, pocket_waste.md, cross.md, no_vv.md, wedged_seal.md) and Lean
`lean/PackingCertMathlib/PackingCertMathlib/Statements/Open/`.

## 1. Terms

A packing of n unit squares in a container [0, s]^2 (axis-parallel), independent rotations, disjoint interiors.
A **simple square** (the Squares Project would say an axis-aligned square settled in a corner slot) is a unit
square at an exact lattice slot [a, a+1] x [b, b+1] with a, b in {0, 1, ..., } measured from a container corner;
a **corner square** is the slot at a container corner.  A **corner box** is the open unit square at a corner.
A packing is **teleport-stuck** (lab: k0 and stuck) when every corner box is met by at least two squares.
s(n) is the least side; a packing attaining it is **optimal**.

## 2. The conjecture

**Conjecture ONE-FLUSH(n) (PI).**  For every n with s(n) < ceil(sqrt n), every optimal packing can be
transformed, with no increase of side, into a packing that contains a simple corner square.  Equivalently
(value form): s(n) is attained by a packing with a flush corner square.

Equivalent forms we have proved equivalent (ring_swap.md, one_flush.md):
* UNCROWD(n): every packing below ceil(sqrt n) with all four corner boxes doubly met admits a packing of the
  same n squares at a strictly smaller side.
* RAISE(0 -> 1) on the optimum: some optimal packing has a corner box met by at most one square (then the
  discrete teleport, Lean `teleport_packing`, exchanges that square for the corner slot square at the same side).

**Why it matters for scaling.**  A proof of ONE-FLUSH(n) lets any exact-value search stratify by the number k of
simple squares and START at k >= 1: the corner slot square is a pin, the container minus the pin is the next
stratum's container, and the k-strata trees inherit their kills upward (lab: Lemma K1, stratum_kill).  The
centre-cell method of 11SquaresOptimal does not need the conjecture, but its case count C(cells, n) grows with
n while the simple-square stratification removes a corner per level.  We believe the conjecture gains force as n
grows (the perimeter-to-area ratio of a four-crowd's waste falls, but the optimum's slack s(n)^2 - n is bounded by
2 ceil(sqrt n) - 2 while the four-crowd's occupied perimeter band is fixed).

## 3. What is known (lab, n-general unless marked)

Proved [T] (Lean where noted):
* Teleport (K0-FREE): a corner box met by <= 1 square exchanges for the corner slot square at the same side
  (`teleport_packing`).  Generalised exchange: any set X of squares exchanges for any packing of |X| squares inside
  union(X) u Free, interior-disjoint from the rest (`swap_packing`); a family of disjoint cells can be settled iff
  at most that many squares meet it (`cells_swap`).
* Survey: all 21 best-known packings with s < ceil(sqrt n) (n = 5 .. 55, Ellsworth's coordinates re-verified
  exactly) have >= 3 flush corners; 20 have four; Trump (n = 11) is the only one with a doubly-met corner.
* Extremal reduction (local_lock.md, Lean `no_retreat_of_psiMin`): among optimal packings take the one minimal
  for the retreat potential; nothing retreats there, so ONE-FLUSH(n) holds UNLESS that optimum is a four-crowd all
  of whose eight corner meeters are locked (loaded, retreat-free).  Residue: LOCKED-CROWD-FREE(n).
* Local facts at a locked corner: PUSH (the two meeters push each other out along their walls), HOLD (a pressed
  meeter has an along-wall holder), TWO-CONTACT, ONE-TILTED, WEDGED-SEAL (a square with a vertex on each wall of
  a corner admits no second meeter), RADIAL / CHAIN (a loaded corner arm is held in from outside; the loaded
  component reaches a far wall), RING as a theorem (walls + meeters alone never balance a crowd), the
  vertex-on-vertex zero-load lemma, Theorem CROSS-PLANAR (two bracing chains across the container share a square).
* At n = 11 (Lean `fourcrowd_dead_of_step_kill`): STEP -- every four-crowd in the window admits a corner swap --
  together with the certified k1 tree excludes four-crowds; so ONE-FLUSH(11) <=> STEP on [31/8, T].

Refuted [F] (with witnesses, so the proof cannot go these ways):
* Every LOCAL charge (area, chord, side, wall wastage): crowds exist at O(eps) above every record packing
  (CROWD-ABOVE), so the statement is about the optimum, not about all packings.
* Counting routes: "four doubly-met corners need 12 squares" (a 9-square force-balanced ring exists), the
  perimeter sweep count, the band/core capacity count (m^2 - 3 >= n for every n with s(n) < m).
* Torque / handedness invariants: no global sum separates (TORQUE-ID is an identity; locked corners are
  same-handed 215:11); container rotation is first-order stable at a four-crowd.
* Monotone grain re-alignment: chain formulas rise toward alignment near 45 degrees.
* Lower tilt bounds on locked meeters: none exist (CROWD-ABOVE tilts eps/2).

Measured [M], consistent with the conjecture everywhere: no free Fritz-John point has four doubly-met corners
(0 of 883); every valid packing found below side 4.0013 has a singly-met corner; every four-crowd witness
(193 held + 40 window-shaped) has a strictly improving corner swap; the n = 11 crowd rings below side 4 leave
room for one further square, not three.

## 4. The sharpest open form

**LOCKED-CROWD-FREE(n):** no optimal packing below ceil(sqrt n) is a four-crowd with all eight corner meeters
loaded and retreat-free.  Equivalently the pocket statement: the loaded component of such a crowd leaves a pocket
that cannot hold the remaining n - p squares.  What a proof needs, by elimination: a GLOBAL improvement argument at
the optimum (an explicit exchange or motion that lowers the side), not a local charge and not a per-corner lemma.
The witnesses say what it should do: swap one corner (always possible on every witness), then shrink at fixed
tilts (strictly side-lowering on 783 of 792 cases, never blocked).

## 5. The ask

Does the centre-cell / charge machinery give an angle on LOCKED-CROWD-FREE(n)?  In particular: a field
certificate conditioned on all four corner boxes being doubly met (owner sets = the eight meeters' hulls) would be
a direct attack on the n = 11 form, and a family of such certificates parametrised by n would be the n-general
statement.  We can supply the witnesses, the Lean statements of the equivalences, and the exact tools.
