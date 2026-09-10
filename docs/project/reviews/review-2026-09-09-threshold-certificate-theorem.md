# Adversarial Review of the Threshold-Certificate Theorem and the 191/50 Candidate

**Verdict.** The threshold-certificate theorem is sound as stated in
[`threshold.py`](../../../packing/src/sqpack/fractional/threshold.py) and in spike B’s
report, and it needs nothing the point-atom theorem does not already need.
The exact event-cell decision of Condition 5' is correct on every instance I could
construct, and the candidate `threshold-candidate-191-50.json` (SHA-256
`3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, 673,639 bytes)
satisfies Conditions 1, 1', 2', 3 and 4 by my own recomputation from its bytes.
Condition 5' holds at the 23 of 181 net directions I decided with my own sweep, at the
logged witness by two containment predicates, and at 2,172,000 sampled centres; at the
other 158 directions it rests on the one route under review, which I replayed first-hand
to the same verdict and digest.
So `s(11) >= 191/50` is accepted by one exact route and is not yet a retained result.
What still stands between the two is listed under [Verdict](#verdict), item (d): the
independent second route, a stranger-facing statement of the theorem in the case
directory, controls that exercise a floored budget, and the candidate bytes themselves
in the repository.

Labels used throughout: **PROVED** (the argument is written out here), **CHECKED** (a
retained script, floating point), **EXACT** (rational or integer computation, by
repository primitives or by my own script), **OPEN** (not established).

## Findings

| # | What | Severity | Status |
| --- | --- | --- | --- |
| F1 | Lemma 1 (budget `w floor(|S|/k)`) needs the cores pairwise disjoint as closed sets, not merely interior-disjoint. The proof supplies exactly that, by the same step as for point atoms: `B(1 + D) < 1` puts each core strictly inside its own unit square’s interior. The threshold argument needs nothing more. | none | PROVED |
| F2 | The trace argument is valid for every `k` and `|S|`, including `k` not dividing `|S|`, for points shared between atoms (96 of the candidate’s 856 threshold points are), and would stay valid for repeated points, which the code refuses anyway. | none | PROVED |
| F3 | Condition 1' transfers to threshold atoms exactly: closure of the key set `(sorted S, k)` under the eight maps with orbit-constant weights makes the charge function invariant under every symmetry. The proof uses only the diagonal reflection (image index 4 of `d4_images`); the tool checks all eight. | none | PROVED; EXACT on the candidate with my own maps |
| F4 | Every unit square at an orientation in `[0, pi/4]` contains a concentric closed `B`-square at a net direction, strictly inside its interior. The last net interval straddles `pi/4`: `t_179` has slack `-52667931944591/8100000000000000 < 0` and `t_180` has slack `309449/250000000000 >= 0`. | none | PROVED; EXACT |
| F5 | The minimum charge at a net direction is attained on an open cell of the event grid built from every atom point (point atoms and threshold points both enter `_event_atoms`); a centre on a grid line carries at least the charge of an adjacent open cell that meets the centre domain; `reduce_to_spans` marks a superset of the open cells meeting the domain. | none | PROVED; EXACT on 175,315 cells |
| F6 | The identity `[m >= k] = sum_{j >= k} (-1)^(j-k) C(j-1, k-1) C(m, j)` and its implementation as signed rectangle terms in one `int64` difference array; the headroom bound `sum_j C(j-1, k-1) C(|S|, j)` is the largest magnitude any grid entry can reach; on the candidate the bound is `20141887792 < 2^35`, against the `2^60` limit. | none | PROVED; EXACT for all `|S| <= 12` and on random instances |
| F7 | Candidate Conditions 1, 1', 2', 3, 4 recomputed from the bytes without `sqpack`: 584 point atoms in 79 orbits (67 of size 8, 12 of size 4 on mirrors), 320 threshold atoms in 40 orbits of 8, all 2-of-3, every point inside the container, total budget `685457679/62500000 = 10.967322864 < 11`, margin `2042321/62500000`. | none | EXACT |
| F8 | Candidate Condition 5': the tool’s least charge `100000203/100000000 = 1.000002030` at direction 69 was reproduced by replaying the tool (216 s, one worker, same digest), by my own sweep at 23 directions (equal at every one), at the witness by two containment predicates, and by sampling; the remaining 158 directions rest on the reviewed route alone. | none found; retention needs the second route | EXACT (23 directions, witness); CHECKED (sampling); OPEN (158 directions by an independent route) |
| F9 | Two forgeries a wrong budget rule would admit are refused: every `k` changed to 1 fails Condition 2' (budget `15.554605328`); every `k` changed to 3 fails Condition 5' (least charge `0.794018124` at direction 69). Neither control is in the test suite. | low (test gap) | EXACT |
| F10 | Loader and tool gaps in the reviewed version: the `claim` label and `variant` are not checked (a record with `n = 1000` and `claim: "s(11) >= 3"` is ACCEPTED); a threshold point outside the container and `direction_steps = 0` end in tracebacks rather than a REFUSED line; the `symmetry` field is ignored but D4 is enforced regardless; symmetric point atoms outside the container are accepted, which the theorem permits. None admits a false certificate. | low | CHECKED (fixtures retained) |
| F11 | No positive control exercises a floored budget: the retained `n = 17` control is point-only, and every threshold test instance is random. | medium for retention | OPEN |
| F12 | The theorem’s full proof (Lemma 2(c), the identity’s proof, the signed-term argument) lives in a scratch report and a module docstring; X-023 carries the statement and a short proof; the case directory has no stranger-facing statement for threshold certificates. | medium for retention | OPEN |
| F13 | The candidate bytes and the decide log live under `/tmp`; the digest is bound only in scratch logs. | medium for retention | OPEN |
| F14 | `decide_threshold_certificate.py` changed on disk during this review (working tree `8d303dfc…`, adding an interval route); everything here concerns `HEAD`’s copy, `acf0e34dc2193fd69568351de0e6073fecf170b43d9fcb853df49bdf6a9ac2ba`, extracted to scratch for the fixture runs. `threshold.py` is unchanged (`c86b7d90…` in both). | informational | RECORD |
| F15 | `sweep_all_threshold_directions` forks unconditionally on Linux, without `certificate._pool_context`’s thread check. Robustness only. | low | RECORD |

## Scope

Reviewed, in order:
[`certificate.py`](../../../packing/src/sqpack/fractional/certificate.py) (the
point-atom theorem and its five conditions),
[`threshold.py`](../../../packing/src/sqpack/fractional/threshold.py) (the threshold
theorem, `rectangle_terms`, `charge_grid`, `sweep_slabs`, `charge_grid_direct`,
`minimum_charge`, the conditions),
[`sweep.py`](../../../packing/src/sqpack/fractional/sweep.py) (`centre_domain`,
`reduce_to_spans`, `_cell_witness`, which the threshold sweep builds on),
[`decide_threshold_certificate.py`](../../../packing/devtools/decide_threshold_certificate.py)
at `HEAD` (commit `526efabf`),
[`test_fractional_threshold.py`](../../../packing/tests/test_fractional_threshold.py),
the third-party statement of the point theorem in
[`thirdparty/README.md`](../../../packing/cases/n11_fractional_certificate/thirdparty/README.md),
the threshold section of
[X-023](../../../packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md),
spike B’s `REPORT.md` (sections 1, 3.3, 3.5) and its `resume/REPORT.md`, the candidate,
and `resume/decide-2.log`.

Every script named below is retained in the scratch directory
`scratchpad/threshold-review/` with its log: `recompute_conditions.py`,
`witness_check.py`, `xcheck_charge_grid.py`, `refusals.py`, `independent_sweep.py`,
`random_centres.py`, `quick_checks.py`, `decide_head.py` (the `HEAD` tool), and
`decide_replay.log`. All ran under the project interpreter with at most two worker
processes.

## The Theorem and the Attacks on It

**Setting.** Container `Q = [0, L]^2`, `n >= 1`, shrink `B > 0`, half-tangent net
`0 = t_0 < ... < t_K` with `t_K^2 + 2 t_K - 1 >= 0` (Condition 3), largest half-gap
tangent `D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1})`, and `B(1 + D) < 1` (Condition
4). An admissible core is a closed `B`-square at a net direction lying inside `Q`. A
point atom `(p, w)` charges `w` to every core containing `p`; a threshold atom
`(S, k, w)` with `S` a finite set of distinct points, `1 <= k <= |S|`, `w >= 0`, charges
`w` to every core `P` with `|P ∩ S| >= k`. The budget of the family is
`M = sum_p w_p + sum_A w_A floor(|S_A| / k_A)`. Condition 1' says the family, as a set
of keys `(sorted S, k)` with one weight per key, is closed under the eight symmetries of
`Q` with the weight constant on orbits (point atoms likewise, as today).
Condition 2' says `M < n`. Condition 5' says every admissible core is charged at least
1\.

**Claim.** Under Conditions 1', 2', 3, 4, 5', no `n` closed unit squares with pairwise
disjoint interiors fit in `Q`; hence `s(n) >= L`.

### Attack 1: Closed Disjointness and the Budget (F1)

Lemma 1 says: for pairwise disjoint closed sets `P_1, ..., P_m` and one threshold atom
`A = (S, k, w)`, `sum_i c_A(P_i) <= w floor(|S| / k)`. The proof: the traces `P_i ∩ S`
are pairwise disjoint subsets of `S` because the `P_i` are pairwise disjoint; each
charged trace has at least `k` points; so if `q` cores are charged then `q k <= |S|`,
`q <=
floor(|S| / k)`, and the total charge is `w q`. Only `w >= 0` is used (a negative `w`
reverses the inequality; that is the five-atom forgery recorded in `model.py`).

The attack: the packing gives interior-disjoint unit squares, not disjoint closed cores,
and a point of `S` on the shared boundary of two closed cores would lie in both traces.
It fails because the proof never uses interior-disjoint cores.
With `d` the angle between unit square `U_i` and the chosen net direction, `tan d <= D`,
and the core’s half-width across `U_i`’s edge normal is
`(B/2)(cos d + sin d) = (B/2) cos d (1 + tan d) <=
(B/2)(1 + D) < 1/2`, so the core `P_i` lies in `int(U_i)`. Then
`P_i ∩ P_j ⊂ int(U_i) ∩ int(U_j) = ∅` for `i != j`: the cores are pairwise disjoint as
closed sets. This is the one place `B(1 + D) < 1` enters, and it is the same place it
enters for point atoms (a point atom on a shared core boundary would be counted twice by
the point argument too).
The threshold theorem needs nothing beyond it.
PROVED.

### Attack 2: The Trace Argument at the Edges (F2)

For `k` not dividing `|S|` the bound `floor(|S| / k)` is what the counting gives and no
more is claimed: with `|S| = 5`, `k = 2`, two disjoint traces of size at least 2 use at
least four points and a third would need six.
For a point in several atoms, Lemma 1 is applied atom by atom and the bounds are summed;
nothing couples the atoms, so the 96 candidate points that belong to more than one
threshold atom are harmless.
For a repeated point (a multiset `S`), the traces would be sub-multisets, both copies of
a point going to the one core that contains it, and the count `q k <= |S|` survives with
multiplicity; `ThresholdAtom` refuses repeated points regardless.
The dual reading (clique and odd-cycle inequalities) plays no part in the proof and I
did not rely on it. PROVED.

### Attack 3: D4 Invariance (F3)

Let `g` be one of the eight maps of `d4_images` and `R` the diagonal reflection
`(x, y) -> (y, x)`, image index 4. For any closed set `P`,

`c(gP) = sum_A w_A [ |gP ∩ S_A| >= k_A ] = sum_A w_A [ |P ∩ g^{-1} S_A| >= k_A ]`,

since `g` is a bijection of the plane.
Condition 1' makes `A -> g^{-1} A` a bijection of the family onto itself preserving `k`
and `w`: it is injective because `g^{-1}` is, and it maps the finite key set into itself
because every image key is present with the same weight.
Reindexing the sum gives `c(gP) = c(P)`. The point-atom sum is invariant by Condition 1
in the same way. In the proof, a unit square `U_i` at orientation `phi >
pi/4` is reflected: `R U_i` has orientation `pi/2 - phi ∈ (0, pi/4)`, lies in `Q`, and
contains a core `P'_i` at a net direction with `P'_i ⊂ int(R U_i)`, so `P'_i` is
admissible and `c(P'_i) >= 1` by Condition 5'. Then `P_i = R P'_i ⊂ int(U_i)` and
`c(P_i) = c(R P'_i) = c(P'_i) >= 1`. The pulled-back core is at direction
`pi/2 - theta_k`, which is not a net direction, and it need not be: Condition 5' is
applied to `P'_i`, not to `P_i`.

The attack: does the decision tool check the symmetry the proof needs?
It checks more. `_condition_symmetric_threshold_atoms` loops over all eight images of
every atom and requires `weights[image.key] == weight`, with keys unique by
`ThresholdCertificate`’s constructor.
An atom lying on a mirror has coinciding images with the same key, which is present;
that is closure, not a gap.
Dropping one image from a small symmetric family is refused (`refusals.py`), and my own
eight maps, written out independently in `recompute_conditions.py`, find the candidate’s
320 atoms closed with weights constant on its 40 orbits.
PROVED; EXACT on the candidate.

### Attack 4: Condition 4 and the Last Gap (F4)

A unit square’s orientation can be taken in `[0, pi/2)`; after the reflection of Attack
3, in `[0, pi/4]`. The net angles `theta_k = 2 arctan t_k` run from `0` to
`theta_K >= pi/4` (Condition 3, decided as `t_K^2 + 2 t_K - 1 >= 0` because `tan(pi/8)`
is the positive root of that polynomial), so every `phi' ∈ [0, pi/4]` lies in some
`[theta_k, theta_{k+1}]` and the nearer endpoint is within half the gap, whose tangent
is `(t_{k+1} - t_k) / (1 + t_k t_{k+1}) <= D` by the half-angle formula.
The concentric `B`-square at that direction lies strictly inside by Attack 1. For the
candidate’s net, `t_k = 207107 k / 90000000`, the largest half-gap is the first,
`D = 207107/90000000`, and `pi/4` lies in the last interval: `t_179 = 37072153/90000000`
has `t^2 + 2t - 1 < 0` and `t_180 = 207107/500000` has it `>= 0`. Directions past `pi/4`
(here only `theta_180`) are decided too, which is a superset and harmless.
PROVED; EXACT.

### Attack 5: Open Cells and Boundaries (F5)

At a net direction with rotated frame `(u, v)`, the core with centre `c` is
`P(c) = { q : |q_u - c_u| <= B/2, |q_v - c_v| <= B/2 }` and `s ∈ P(c)` iff `c ∈ R_s`,
the closed rectangle `[s_u - B/2, s_u + B/2] × [s_v - B/2, s_v + B/2]`. The event grid
takes every `s_u ± B/2` and `s_v ± B/2` over every atom point plus the extremes of the
centre domain `Ω`. `rectangle_terms` builds it through `_event_atoms`, which appends one
zero-weight atom per threshold point, so the grid is built from all points, not the
point atoms alone; I confirmed this by reading the code and by the cross-check below,
which fails on the first cell if any point is missing.
Write `T(c) = { s : c ∈ R_s }`. The charge depends on `T(c)` alone and is monotone in
it: point weights are nonnegative and `w [ |T ∩ S| >= k ]` is monotone in `T`.

(a) `T` is constant on each open cell: the cell’s open `u`-interval lies between
consecutive events and `R_s`’s `u`-edges are events, so the interval is inside or
disjoint from `R_s`’s `u`-span, and likewise in `v`. (b) If `c` is in the closure of an
open cell `C` then `T(c) ⊇ T(C)`, because `R_s` is closed.
(c) Every `c ∈ Ω` on a grid line is in the closure of an open cell meeting `Ω`: `Ω` is
convex with nonempty interior (the candidate has
`B(cos theta + sin theta) <= B sqrt 2 < 1.42 < L`), every neighbourhood of `c` contains
interior points of `Ω` off the finitely many grid lines, and infinitely many of a
sequence of such points converging to `c` lie in one of the finitely many open cells,
whose closure then contains `c`. So `min_Ω charge = min { charge(C) : C open, C ∩ Ω ≠
∅ }`. A centre on a grid line whose closed core holds a point exactly on its boundary is
the case (b) covers: the boundary point only enlarges the trace.

`reduce_to_spans` marks, in slab `i`, the cells `j0 .. j1` with `j0` the last event `<=`
the least `v` of `Ω ∩ [u_i, u_{i+1}]` and `j1` the last event `<` its greatest `v`. For
an open cell `(i, j)` meeting `Ω` at `c`, `u_{i+1} > u_low`, `u_i < u_high`, and
`v_j < c_v < v_{j+1}` with `low <= c_v <= high` give `j0 <= j <= j1`; so the marked set
is a superset of the open cells meeting `Ω`, its minimum is at most the true one, and a
marked minimum `>= 1` proves Condition 5'. The witness step (`_cell_witness`, which
raises unless the vertex average of the clipped cell is strictly inside the open cell)
turns “at most” into “equal”: the reported least charge is attained by a placement, and
the replay confirmed the membership count at that placement.
PROVED.

`xcheck_charge_grid.py` (EXACT): 40 random instances with shapes 1-of-1, 1-of-3, 2-of-3,
3-of-3, 2-of-4, 3-of-4, 2-of-5, 3-of-5, 4-of-5, 4-of-6, 3-of-7, points shared between
atoms and with point-atom sites, points on the container boundary, zero weights, over
seven directions including one at half-tangent `9/20 > tan(pi/8)`. For every one of the
175,315 marked cells, the `charge_grid` value equals the charge at the cell’s witness
computed by my own membership predicate in `Fraction` arithmetic; `charge_grid` equals
`charge_grid_direct` cell for cell; `minimum_charge` (dense and slab) equals the
brute-force minimum over the cells.
No marked cell lacked an interior witness on these instances.

### Attack 6: Inclusion-Exclusion and the Integer Grid (F6)

With `f_k(m) = sum_{j >= k} (-1)^(j-k) C(j-1, k-1) C(m, j)`, the identity
`C(j-1, k-1) = C(j, k) - C(j-1, k)` splits `f_k` into two sums.
The first is
`sum_j (-1)^(j-k) C(j, k) C(m, j) = C(m, k) sum_j (-1)^(j-k) C(m-k, j-k) = C(m, k) (1 - 1)^(m-k) = [m = k]`.
The second, after dropping the vanishing `j = k` term, is `-f_{k+1}(m)`. So
`f_k(m) = [m = k] + f_{k+1}(m)`, and `f_k(m) = 0` for `k > m`, giving
`f_k(m) = [m >= k]`. PROVED, and EXACT for every `1 <= k <= |S| <= 12` and every
`m <= |S|` in `quick_checks.py`.

In `rectangle_terms`, for each `j >= k` and each `j`-subset `T` of an atom’s points, the
intersection `∩_{t ∈ T} R_t` is a closed rectangle with event corners (a maximum of left
edges and a minimum of right edges), skipped when empty or degenerate, and entered with
coefficient `(-1)^(j-k) C(j-1, k-1) w` at its four corners.
An open cell `(i, j')` receives the term iff `left <= i < right` and
`bottom <= j' < top`, iff the cell lies inside the intersection, iff `T ⊆ T(C) ∩ S`.
Summing over `T` gives `C(m, j)` for `m = |T(C) ∩ S|`, and the identity turns the cell’s
total into `w [m >= k]`. A degenerate intersection contains no open cell, so skipping it
is exact. The signed intermediate values never reach the theorem: what the sweep
minimises is the cell total, which is the monotone charge of Attack 5; `sweep.py`’s
refusal of signed point weights guards a different thing, a signed measure, whose total
is not monotone.

Headroom: every entry of the difference array, and every entry after either prefix sum,
is a signed sum in which each term appears at most once, so its magnitude is at most
`sum_terms |coefficient| w`, at most `w sum_j C(j-1, k-1) C(|S|, j)` per atom, which is
`absolute_expansion_sum`. `_headroom` refuses at `2^60` on `int64`. On the candidate, at
direction 69 the 1,864 terms have `sum |weights| = 20141887792`, exactly the bound (no
pair or triple intersection of any 2-of-3 atom is empty), against `2^60`. EXACT.

### Attack 7: The Doubled Net (F3)

The interval route for point atoms decides Condition 5 on the doubled net `theta_k` and
`pi/2 - theta_k` and so never invokes Condition 1. The exact route decides Condition 5'
on the net alone and reaches the reflected orientations through Condition 1', which it
decides exactly, over all eight maps.
There is no gap: Attack 3 shows Condition 1' implies `c(RP) = c(P)` for every closed set
`P`, and `R` carries a core at `pi/2 -
theta_k` inside `Q` to a core at `theta_k` inside `Q`. The two routes rest on different
hypotheses (the doubled-net route on fewer), and for a D4-symmetric family both apply.
PROVED.

## The Implementation

The decision path is `minimum_charge`: `threshold_weight_scale` (the least common
denominator of every weight; `10^9` on the candidate), `rectangle_terms` (headroom
check, outside-point refusal, `reduce_to_spans` on the point atoms plus zero-weight
threshold points, one term per point atom and the signed terms of Attack 6), then either
the dense `int64` grid with two `cumsum`s or `sweep_slabs`, which maintains the
`v`-difference array across `u`-slabs (terms with `left <= i` added, `right <= i`
removed, so a term is active on `left <= i < right`) and reads one prefix sum per slab.
Both take the minimum over `reduction.spans`, first occurrence in span order winning,
and the decide tool requires the two to agree in value and witness at every direction.
`_placement_membership` re-evaluates the least cell by counting, with the same rotated
frame `u = ux x + uy y`, `v = vx x + vy y` that `reduce_to_spans` uses.
I read these against the argument of Attacks 5 and 6 and found them faithful; the
cross-check above exercises every path except the fork pool.

Forgeries (`quick_checks.py`, EXACT): the candidate with every threshold set to `k = 1`
keeps Condition 5' (a 1-of-3 charge dominates a 2-of-3 charge) and fails Condition 2'
with budget `972162833/62500000 = 15.554605328`; with every threshold set to `k = 3` the
budget is unchanged and the least charge at direction 69 falls to
`198504531/250000000 = 0.794018124`. A rule that budgeted `w |S| / k` without the floor,
or that charged without the threshold, would have accepted one of them.
Neither control exists in `test_fractional_threshold.py` (F9).

Loader fixtures (`refusals.py`, `quick_checks.py`, against `HEAD`’s tool): refused
before any condition runs are a duplicate `(S, k)` (also `S` in another order), a
negative threshold or point weight, `k = 0`, `k > |S|`, `k` as `true` or as a string, a
repeated point, a decimal or `1/0` weight, a float anywhere in the file (provenance
included), a duplicate JSON key, and a declared `total_budget` that differs from the
recomputed one. Rejected by a condition are a missing image, asymmetric weights, a net
short of `pi/4`, and `n` at or below the budget (`n = 361` with budget 361 rejected,
`n = 362` accepted).
A threshold point outside the container is refused by `rectangle_terms` with a traceback
rather than a REFUSED line, and `direction_steps = 0` ends in `ZeroDivisionError`; both
are rejections. Accepted, each correctly by the theorem: `k = |S|` (a conjunction atom
with budget `w`), zero weights, and symmetric point atoms outside the container (they
add mass and are never covered).
Not checked at all: the `claim` string and `variant`; a synthetic record with `n = 1000`
and `claim: "s(11) >= 3"` is ACCEPTED with `n = 1000` printed in its own log (F10). The
`symmetry` field is not read; D4 is enforced whatever it says, which is the safe
direction.

## The Candidate

### Conditions 1, 1', 2', 3, 4 (F7, EXACT)

`recompute_conditions.py` reads the bytes with a strict parser (rational strings only,
no duplicate keys, no floats), writes out the eight maps itself, and finds:

| Condition | Result |
| --- | --- |
| 1 | 584 distinct sites, all inside `[0, 191/50]^2`, closed under the eight maps with equal weights; orbit sizes 8 (536 sites) and 4 (48 sites on mirrors); point mass `271052551/31250000 = 8.673681632`, equal to the declared `point_mass` |
| 1' | 320 threshold atoms, all `(|S|, k) = (3, 2)`, distinct points within each atom, distinct keys, 856 distinct points all inside the container, closed under the eight maps with weights constant on 40 orbits of size 8; budget `143352577/62500000 = 2.293641232`, equal to the declared `threshold_budget` |
| 2' | total `685457679/62500000 = 10.967322864 < 11`, margin `2042321/62500000 = 0.032677136`, equal to the declared `total_budget` |
| 3 | `t_180 = 207107/500000`, `t^2 + 2t - 1 = 309449/250000000000 >= 0` |
| 4 | `D = 207107/90000000 = T / 180` (the first gap), `B(1 + D) = 899996306539/900000000000`, `1 - B(1 + D) = 3693461/900000000000 = 4.104e-6` |

Every weight is a multiple of `10^-9` (the freeze rounds up at that scale after a
`500001/500000` bump, which only raises charges); the common scale is `10^9` and the
headroom bound is `20141887792`. Condition 2' is decided on the recomputed total, and
the tool refuses a record whose declared total differs.

### Condition 5' (F8)

Replay of `HEAD`’s tool on the candidate bytes (`decide_replay.log`, one worker, 216 s):
every closed-form condition holds; least cell charge `100000203/100000000 =
1.000002030` at direction 69; dense and slab routes agree at all 181 directions; the
charge at the witness by membership counting agrees; verdict ACCEPTED; SHA-256
`3935651a…4bad5c`, the digest in `decide-2.log` and in the resume report.

`witness_check.py` (EXACT) parses the witness centre from `decide-2.log` and evaluates
the charge two ways: the rotated-frame box test, and a container-frame test that rotates
the centre back, builds the core’s four corners, and tests every atom point against the
four edge half-planes.
Both give point mass `59289327/62500000` plus threshold charge `25686399/500000000`,
total `100000203/100000000`; 50 point atoms and 4 threshold atoms are charged; no atom
point lies on the core’s boundary (nearest event line `1.9e-5` away in `v`), so the
witness is interior to its cell; the core’s corners lie inside the container.

`independent_sweep.py` (EXACT) decides Condition 5' at a direction with nothing from
`sweep.py` or `threshold.py`: its own event grid in `Fraction`s, its own centre domain,
per-atom count grids thresholded directly (never the inclusion-exclusion expansion), and
its own reachable-cell test (a closed cell is kept when it meets the closed rotated
domain, decided by separating axes with a slack of `10^-9` that can only add cells), and
compares its minimum with `minimum_charge` at the same direction.

| Directions | My minimum | Tool minimum | Equal |
| --- | --- | --- | --- |
| 0, 10, 20, 30, 40, 50, 60, 100, 110, 114, 120, 140, 150, 160, 170, 180 | `1000002031/1000000000` | same | yes, all sixteen |
| 69, 70, 80, 88, 90, 130, 136 | `100000203/100000000` | same | yes, all seven |

The minimum at every direction sits at `1 + 2.03e-6`, the bump above the LP measure’s
tight cells, as an LP optimum with rows at every direction predicts.

`random_centres.py` (CHECKED, with EXACT re-evaluation): 12,000 centres per direction
over all 181 directions, 3,000 uniform in the centre domain plus three jittered copies
of each at `10^-7`; the least float charge at every direction is `1.000002`, no centre
falls below `1 + 10^-6`, and the least sampled centre re-evaluated exactly is
`100000203/100000000` at direction 136.

## Verdict

**(a) The theorem as stated.** Sound.
Conditions 1', 2', 3, 4, 5' imply `s(n) >= L`, by the argument of Attacks 1 to 4, and
the reduction of Condition 5' to open event cells with the inclusion-exclusion terms is
correct by Attacks 5 and 6. The threshold argument needs the cores pairwise disjoint as
closed sets and gets them where the point argument does.
PROVED.

**(b) The implementation’s decision of Condition 5'.** Correct on every instance
constructed: the grid value equals exact membership on 175,315 cells across eleven
threshold shapes, dense and slab routes agree, the minimum is attained at a witness the
tool re-counts, and forged budgets and thresholds are refused.
The tool’s residual gaps (F10) cannot admit a false certificate; the `claim` and
`variant` checks the working-tree revision declares were not reviewed.
EXACT where labelled; the implementation is not proved correct in general, and no
cross-check of this kind can do that.

**(c) The candidate’s Conditions 1', 2', 3, 4.** Hold, by recomputation from the bytes
with no repository code, with the numbers in the table above.
Condition 1 for the point atoms holds the same way.
EXACT.

**(d) Between “accepted by one route” and a retained result.** In order of weight:

1. The second route must decide Condition 5' at all 181 directions by a method that
   shares nothing with `reduce_to_spans` and the signed-term grid, and agree on the
   number `100000203/100000000`, not only on the verdict; the margin is `2.03e-6`, so an
   enclosure route must resolve to that width.
   The interval route now in the working tree is that lane’s deliverable and is
   unreviewed here. Until it lands, 158 of 181 directions rest on one method (F8).
2. A stranger-facing statement of the threshold theorem with the proof in the case
   directory, in the shape of `thirdparty/README.md`: Lemma 1, Attack 3’s invariance,
   Lemma 2 with part (c), the identity’s proof, and the signed-term argument now live in
   scratch and in a docstring (F12).
3. Controls: a positive control whose floored budget is essential (a synthetic small
   instance or the candidate itself once frozen) and the two forgeries of F9 as negative
   controls, in `test_fractional_threshold.py` and in the case directory’s falsification
   table.
4. The candidate bytes, the decide log and the digest into
   `packing/cases/n11_fractional_certificate/`, with the frontier entry bound to the
   digest (F13); the two process defects the resume report names (a partial sweep
   reported as complete, a float in provenance) into `defects.yaml`.
5. Small tool fixes: check `claim` and `variant`, turn the two tracebacks into REFUSED
   lines, and route the fork pool through `_pool_context` (F10, F15).

Nothing found here weakens the accepted verdict; what is missing is the independence and
the record that retention requires.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
