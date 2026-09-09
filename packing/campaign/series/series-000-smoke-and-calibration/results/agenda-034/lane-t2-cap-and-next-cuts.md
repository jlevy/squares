# Agenda 034, lane T2: the cap of the threshold method and the next cut families

Retained analysis-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a Fable
sub-agent at maximum effort on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds` (HEAD `30a1dbc6`). The report is reproduced as
delivered, with its own status labels; only its file references were rewritten to say
where each file now is.
X-024 carries the coordinator’s reading.
Nothing here is a bound and nothing here is a registered round.

The lane’s two scripts are not retained (scratch only) — scripts are not retained under
results — and what they measured is in the instrument this lane’s recommendation asked
for, promoted with it as `packing/devtools/plateau_reader.py` and reported in
[`lane-t2-plateau-reader.md`](lane-t2-plateau-reader.md).
`twothree_exact.py`, the exact two-of-three maximum of a family over vertex membership
sets (F3’s `5/4`), is the reader’s K4, which decides the same maximum by branch and
bound over the same sets and returns every maximiser.
The wall-chord half of `marks_and_lines.py` is the reader’s line search, exact over
every offset of four directions rather than horizontal lines alone.
Its other half has no counterpart in the reader: the mark-clique reading of F9 —
`y(K_c) = 1` at each corner on the ceiling family, `499999999/500000000` on lane M0’s
polished optimum, in both frames — reads a named clique’s weight, and the reader’s K5
enumerates maximal cliques without naming the corner marks.
The term table of B.2 was computed inline.

Labels: **PROVED** (argument written here), **EXACT** (rational computation, script
retained), **CHECKED** (float or record reading), **PLAUSIBLE** (argued, not proved),
**OPEN**.

Notation. `L` container side, `B = 9977/10000`, `D = 207107/90000000` the largest
half-gap tangent of the 181-direction net, `u = L/B` the *unit-equivalent side* (the
covering program at `(L, B, net)` is the program at `(u, 1, net)` by scaling, so `u` is
the coordinate in which every LP value lives).
`nu_0(u)` is the point-LP value (maximum fractional packing), `nu_1(u)` the value under
every rank-one threshold cut, `nu_{2/3}(u)` under the two-of-three cuts alone.
`K(S, k) = {P : |P ∩ S| >= k}` is the set an atom `(S, k)` charges;
`T(p) = {P : p in P}`. The accepted threshold certificate sits at
`u = 3.82/0.9977 = 3.828806`; the running measurement at `383/100` asks about
`u = 3.838829`; `96/25` would be `u = 3.848852`.

## Findings

| # | Finding | Q | Status |
| --- | --- | --- | --- |
| F1 | The rank-one threshold dual is the fractional packing polytope cut by `y(K(S,k)) <= floor(\|S\|/k)` for all finite `S`, `k`. Implied by point inequalities: every `(S, k)` with `k` dividing `\|S\|`, every `k = 1`, and every atom dominated by a sub-atom. Every atom is dominated by one of the canonical shapes `k`-of-`((b+1)k - 1)` with budget `b`: `2`-of-`3`, `3`-of-`5`, `4`-of-`7` (`b = 1`, cliques), `2`-of-`5`, `3`-of-`8` (`b = 2`), `2`-of-`7` (`b = 3`). In particular `3`-of-`4` is dominated by `2`-of-`3` and should not be built. | A, B | PROVED |
| F2 | For `2k > \|S\|` the charged set is a clique of the core intersection graph, and a clique inequality `y(C) <= 1` is a (weighted) rank-one atom iff the clique’s fractional piercing number `tau*(C) < 2` (lane T F5); with distinct points the same strength is reached by near-duplicate points. So the budget-one half of the language is exactly “clique cuts for cliques with `tau* < 2`”, and feasibility for all of them is decidable by enumerating a family’s maximal cliques above weight one and solving one small piercing LP each. | A | PROVED |
| F3 | The ceiling family at `191/50` (88 cores, weight `1/8`) has exact maximum two-of-three charge **`5/4`**, over *all* point triples, by a complete search over its 20,376 arrangement vertices (1,541 distinct membership sets, 152,288 candidate pairs, 19 s). Lane B’s sampled `5/4` was the true maximum. The witness triple has memberships `(4, 8, 8)`: a left-wall point at height `B` and two points `0.0005` apart near `(0.9977, 1.0)`, the corner square’s far corner, where images pile up. | A | EXACT |
| F4 | The same family is *tight, not violated*, on every other resource examined: the corner mark cliques carry exactly `1` at every corner (both marks), the wall lines `y in {0.10, 0.25, 0.50, 0.75}` carry exactly `3` of chord `>= 0.99` against budget `floor(3.82/0.99) = 3`, and its chordless five-cycles carry `5/8` against `2` (lane M0 F7). Its only rank-one violations are non-Helly clique cuts: `5/4` by two-of-three, `11/8` by a weighted three-of-five (the 11-entry corner clique with `tau* = 5/3`, lane M0 F7). The point-plateau family is a near-packing that fails only locally, at clusters of near-coincident images. | A, B, C | EXACT |
| F5 | Slope arithmetic (record numbers): `nu_0` rises from at most `10.863675` at `u = 3.8188` (T-018’s mass) to exactly `11` at `u = 3.8288`, at least `13.6` per unit of `u`. The two-of-three certificate sits at `10.967323` at `u = 3.8288`, `0.032677` below eleven with rows complete. If the cut LP’s slope is comparable, `nu_{2/3}` reaches eleven by `u ≈ 3.8312`, i.e. `L ≈ 3.8224` at this shrink, and the `383/100` run (`u = 3.8388`, 2.4 times farther) plateaus. Reaching `3.83` needs the cut LP’s slope to be under a quarter of the point LP’s. | A, D, E | PLAUSIBLE (arithmetic EXACT) |
| F6 | Proved bracket on the reach of every rank-one method at this `(B, net)`: `[3.82, 3.868983]` in `L` (`[3.8288, 3.8779]` in `u`); the upper end is Trump’s packing shrunk and snapped, feasible for every valid cut. Nothing sharper is proved. The cap of any *named* family is established exactly by one object: an exact D4-symmetric family of weight eleven at some side with depth at most one (`verify_ceiling`), plus a feasibility decision for that family: a vertex-set triple search for two-of-three (F3’s script), maximal-clique enumeration with piercing LPs for all budget-one atoms (F2), and the Fischetti-Lodi CG-separation MIP over vertex-set multipliers for the whole rank-one closure. | A | PROVED (bracket); tool specification |
| F7 | Every threshold atom, floor atom, odd-cycle atom and collinear (wall or line) atom is decided by the same event-cell sweep with the same counting budget `w floor(\|S\|/k)`; no family needs a different rule. Floor atoms (charge `w floor(m/k)`) are the exact rank-one CG cut, dominate threshold atoms at the same budget, and give the odd-wheel inequality that thresholds miss. A collinear atom with `m` points needs only `2(m - k) + 1` signed terms, not `sum_j C(m, j)`, by convexity: the wall-line family is cheap in the existing sweep. Headroom is a non-issue below `\|S\| ≈ 12` (table in B.2). | B | PROVED |
| F8 | Ranking of the next families by expected gain per cost: (1) weighted clique atoms (three-of-five with a doubled point, the piercing measure of any `tau* < 2` clique), which already cut both retained optima at `191/50` harder than two-of-three (`11/8` and `1.4107` against `5/4` and `1.0785`); (2) floor two-of-five; (3) the exact vertex-set separation for two-of-three, replacing the sampled generator; (4) wall-line atoms, tight at exactly `3` on the plateau family, expected gain zero; (5) three-of-four, provably zero. | B | PROVED (what is known), PLAUSIBLE (the gain) |
| F9 | Negative-weight *mark atoms* are sound: a proved lower bound on the number of packed cores in a clique `K_c` (the corner-pair theorem: one owner per corner at every side `<= 96/25`) lets an atom charge `-z` on `K_c` with budget `-z`; the dual constraint is `y(K_c) >= 1`. It is worth exactly nothing at `191/50`: `y(K_c) = 1` on the ceiling family and `499999999/500000000` on the polished fixed-support optimum, at every corner, in both frames. | C | PROVED (soundness), EXACT (value) |
| F10 | Patch deletion with a lowered threshold cannot be one rank-one certificate: it is a disjunction over owner classes, and its sound single object is a *class-indexed* threshold certificate (one atom family per class, or per internal node of a class tree), stated in C.2 with its conditions. A single unconditional certificate with `n` replaced by `n - 4` would have to charge every core that is residual in *some* class, and by the point-extension lemma that domain’s covering value is at least `tau(96/25) - 4 >= 7`, so its budget cannot fall below seven. | C | PROVED (given the point-extension lemma) |
| F11 | X-024’s `1.7` units per conditioned square compares a nine-direction restricted-site number (`11.884615`) with an exact full-net cover of one favourable class (`5`). The retained measure-free certificate at `96/25` (bc-293, mass `22524199/2000000 = 11.2620995`, Conditions 1, 3, 4, 5 hold) bounds the full-net covering value by `11.262`, so the gain is at most `(11.262 - 5)/4 = 1.566` per owner, of which the mark accounts for at most one; and it is measured on the one class that happened to be coverable. | D | PROVED (bound), CHECKED (reading) |
| F12 | X-024 does not price the plateau. By F5 the base case for the `383/100` run is a plateau at eleven; the memo’s route A ("`383/100` and `96/25`") reads as if `3.84` were within reach of two-of-three atoms, and its slice A3 measures the wrong thing for the base case (a value at one side rather than the cap and the cut that moves it). The finer-net figure `3.8266` is a fair expectation, but two-of-three charges are more angle-sensitive than point masses, so the crossing shrink may sit higher than the point certificate’s. | D | CHECKED |
| F13 | “The conditional engine scales toward pinning Trump’s structure” is overconfident: each layer of forced structure multiplies the leaf count (`16^4 = 65,536` raw at the first layer, unmeasured after pruning) while shrinking the residual by one square and a patch of area well below one; without bounding at internal nodes the tree, not the leaves, is the cost. The sound fix is branch-and-cut: threshold certificates at internal nodes (one patch, budget `< 10`) prune subtrees, and that, not the leaves, is where threshold atoms enter the conditional line. | D | PLAUSIBLE |
| F14 | Recommendation (E): in either outcome, build the exact plateau reader first (vertex sets, two-of-three search, maximal cliques with `tau*`, CG-separation MIP) and run it on the `383/100` dual; it turns a plateau into a theorem about the family in minutes and names the cut that moves it. Then build weighted clique atoms (allow repeated points in `ThresholdAtom`, or emit near-duplicate points with no code change) and re-solve at `383/100`. If `3.83` is reached, the same reader is run on the `96/25` dual instead, and the finer-net crossing shrink is measured on the new certificate. | E | plan |

## A. The cap of the threshold method

### A.1 The dual, exactly

The certificate LP at `(L, B, net)`: minimise `sum_p w_p + sum_A w_A floor(|S_A|/k_A)`
over nonnegative point and atom weights, subject to
`sum_p w_p [p in P] + sum_A w_A [|P ∩ S_A| >= k_A] >= 1` for every admissible core `P`.
Its dual is the fractional packing `y >= 0` on cores with

```text
(point)      y(T(p)) <= 1                     for every point p
(threshold)  y(K(S, k)) <= floor(|S| / k)     for every finite S and 1 <= k <= |S|
```

maximising `sum_P y_P`. Weak duality is one line (`sum y_P <= sum y_P charge(P) <=
budget`), so an exact `y` of weight at least `n` feasible for every threshold constraint
kills every threshold certificate at that `(L, B, net)`, on any site set, at any
weights. The theorem side is `threshold.py`’s; nothing changes.

**Implied inequalities (PROVED).** Summing the point inequalities over `S` gives
`sum_P |P ∩ S| y_P <= |S|`, hence `k y(K(S,k)) <= |S|`, so `y(K(S,k)) <= |S|/k` always;
the atom adds only the rounding to `floor(|S|/k)`, worth at most `(k-1)/k`. So:

- `k | |S|`: implied. `k = 1`: implied (`K(S,1) = ∪ T(s)`, budget `|S|`).
- Dominance: `K(S, k) ⊆ K(S', k - d)` for `S' ⊆ S`, `d = |S \ S'|` (a core holding `k`
  of `S` holds at least `k - d` of `S'`), so `(S, k)` is dominated by `(S', k - d)`
  whenever `floor(|S'|/(k-d)) <= floor(|S|/k)`. With `|S| <= 2k - 1` and `d = 2k - 1 -
  |S|` every budget-one atom reduces to a `j`-of-`(2j-1)`; in particular **`3`-of-`4` is
  dominated by `2`-of-`3`** (same budget, smaller charged set) and `4`-of-`6` by
  `3`-of-`5`. Conversely, adding a point never lowers the charge, and the budget stays
  while `floor` does, so the non-dominated shapes are `k`-of-`((b+1)k - 1)` with budget
  `b`. The language is two-parameter: `(k, b)`.
- Points shared between atoms, and repeated points, change nothing (review F2).

**Cliques versus cycles (PROVED).** Any two `k`-subsets of `S` meet when `2k > |S|`, so
`K(S, k)` is then a clique of the intersection graph and the atom is a clique inequality
with right-hand side one.
Lane T’s F5 characterises which cliques are reachable: `y(C) <=
1` is a rank-one atom iff `tau*(C) < 2`, where `tau*(C) = min { lambda(S) : lambda >= 0,
lambda(P) >= 1 for all P in C }` over finite point measures.
With integer multiplicities `a = t lambda`, `a(P) >= t` on `C` and `floor(a(S)/t) = 1`;
under the implementation’s distinct-point rule the multiplicity is realised by
near-duplicate points in the same membership cell (the review’s F2 says repeated points
would be valid anyway, so the rule can be dropped).
Helly cliques (a common point) are point constraints, and for axis-parallel squares
every clique is Helly, so **all of the language’s clique strength lives on
mixed-direction cliques**, which is what lane B measured (92 per cent of the violation
on mixed near-axis and tilted triples).
For `2k <= |S|` the charged set is not a clique and the constraint is of odd-cycle type:
`2`-of-`5` with the points in the consecutive intersections of a five-cycle is
`sum_C y <= 2`, and it charges every other core holding two of the points as well, at
the same budget.

**Floor atoms are the true rank-one cuts (PROVED).** Multipliers `lambda = a/t` on the
point system give the Chvátal-Gomory cut `sum_P floor(a(P)/t) y_P <= floor(a(S)/t)`. The
threshold atom is its weakening `[a(P) >= t] <= floor(a(P)/t)`; the floor atom, with the
same sweep (`floor(m/k) = sum_{j>=1} [m >= jk]`, a sum of threshold indicators, each
entering the difference array by the same identity) and the same budget (`sum_i
floor(|T_i|/k) <= floor(|S|/k)` for disjoint traces), dominates it.
The difference is real: on an odd wheel the hub holds all five rim points and the floor
atom charges it `floor(5/2) = 2`, giving `sum_rim y + 2 y_hub <= 2`, the odd-wheel
inequality, where the threshold atom charges the hub once.
Lane B’s Part 1 already recommended floor atoms; the theorem there is verbatim the one
here.

### A.2 What a maximal feasible dual looks like

A vertex of the closure polytope is rational with denominator `k`: a `k`-fold packing of
`11k` cores (lane T, Lemma 3) in which, additionally, every `K(S, t)` holds at most `k
floor(|S|/t)` members.
The record shows what the point-level vertices are:

- At `191/50` the point ceiling is the D4 average of eleven rows at weight one, six net
  directions (`0, 0.26°, 0.79°, 1.32°, 25.67°, 29.15°`), an 8-fold family whose base is
  a *near-packing*: two pairs of rows nearly coincide, the base double-covers there, and
  the average compensates with gaps elsewhere (lane B 3.3). Its structure on every
  global resource is integral (F4): exactly one unit on each corner mark clique, exactly
  three cores of chord `>= 0.99` on every wall line between `0.10` and `0.75`,
  five-cycles at `5/8`. It fails only locally: the exact maximum two-of-three charge is
  `5/4` (F3, `twothree_exact.py`), at a triple made of a left-wall point at height `B`
  and two points `0.0005` apart near `(0.9977, 1.0)`, with memberships `(4, 8, 8)`: two
  depth-eight clusters of near-coincident images at the corner square’s far corner,
  sharing members, plus a wall point that four of them hold.
  That is the sliver mechanism: the base family’s overlaps are unstraddled at the point
  level but straddled once eight images pile onto the same corner.
- The polished fixed-support optimum (lane M0, `76/7`) is a 112-fold family; its
  heaviest non-Helly clique has 26 members at `1.4107` with `tau* = 5/3`.

The two-of-three analogue of the ceiling therefore has to be an `8k`-fold near-packing
whose D4 images do not stack more than `k` deep on any pair of straddled slivers, which
is a statement about where the base family’s overlaps sit relative to its corners and
walls. Whether such a family exists at `u = 3.8388` is exactly the running measurement,
and the plateau dual, if it comes, is the object to read; nothing short of it decides
the question (OPEN). What is decided: the dual will not be moved by mark cliques, wall
lines or five-cycles unless its structure differs from the `191/50` one in those
resources, and every violation it does have will be a non-Helly clique or, failing that,
an odd cycle through slivers.

### A.3 A bound on the two-of-three reach

**PROVED bracket.** The two-of-three method reaches `L = 191/50` (the accepted
certificate) and cannot reach `L >= 3.868983` at this `(B, net)`: Trump’s packing scaled
by `B` and snapped to the net gives eleven pairwise disjoint admissible cores (X-023’s
packing cap), whose indicator is feasible for every valid cut.
In unit side: `[3.8288, 3.8779]`.

**PLAUSIBLE estimate.** The point LP moved from at most `10.863675` (`u = 3.8188`) to
exactly `11` (`u = 3.8288`): slope at least `13.6` per unit of `u`. Two-of-three atoms
bought `0.0327` at `u = 3.8288` with the rows complete (the loop’s deeper dips,
`10.927`-`10.966`, were read with rows incomplete and bound nothing).
Three readings of the same arithmetic:

| assumption on the cut LP’s slope | `nu_{2/3} = 11` at `u` | at `L` (`B = 0.9977`) |
| --- | --- | --- |
| equal to the point LP’s (`13.6`) | `3.8312` | `3.8224` |
| half of it | `3.8336` | `3.8248` |
| a quarter of it | `3.8384` | `3.8296` |

The `383/100` run needs the last row.
The direction of the error is known: near-packings at larger sides have thinner slivers,
so a cut family whose strength is the sliver mechanism loses power as `L` rises and its
gain should *shrink* toward zero at `3.869`, not grow.
The prior for a plateau at `383/100` is therefore high, about three in four; the prior
for reaching `96/25` with two-of-three atoms alone is low.
This is the quantity X-024 left unpriced (F12).

**What establishes the cap exactly.** One frozen object per named family, decided by
tools that mostly exist:

1. An exact D4-symmetric family `y` of total weight `>= 11` at side `L'`, depth at most
   one at every arrangement vertex: `verify_ceiling`
   (`packing/src/sqpack/fractional/ceiling.py`), K0-K3.
2. **K4, two-of-three feasibility.** The maximum over triples of vertex membership sets
   of `y((T_1 ∩ T_2) ∪ (T_3 ∩ (T_1 Δ T_2)))` is at most one.
   The reduction to vertices is exact (a closed core containing an open face contains
   its closure, and the charge is monotone in each membership set), the search is
   `O(pairs × sets)` on bit masks, and `twothree_exact.py` is the prototype: 19 s on the
   88-core family, complete for every violating triple (a triple with nine or more
   charged members has a pair whose union holds them all and whose intersection is
   nonempty).
3. **K5, all budget-one atoms.** Every maximal clique of the interior-overlap graph with
   weight above one has `tau*(C) >= 2`, decided by Bron-Kerbosch on the family (lane
   M0’s `clique_scan` does the exact overlaps and a branch-and-bound clique) and one
   piercing LP per clique over the clique’s own arrangement vertices, rationalised and
   checked exactly. By F2 this covers every `k`-of-`(2k-1)` atom and everything they
   dominate.
4. **K6, the whole rank-one closure.** The CG-separation MIP (Fischetti-Lodi) with one
   multiplier `lambda_v in [0, 1)` per distinct vertex membership set, integer `f_P <=
   lambda(T ∋ P)`, integer `f_0 >= lambda(1) - 1 + eps`, maximising `sum f_P y_P - f_0`;
   a positive optimum is a violated floor atom (multiplicities from `lambda`’s
   denominators), verified exactly; zero certifies feasibility for every rank-one CG cut
   at once. HiGHS’s MIP handles 1,541 continuous multipliers and 88 integers.
   This is the one step that says “no threshold or floor atom of any size”, and it is
   the definition of the rank-one cap at that side.

With K1-K6 a plateau at `383/100` is a theorem in the sense the point ceiling is, and
the exact family carries the violation of every family that *does* cut it, which is B’s
ranking made exact for that side.

## B. The next cut families

### B.1 Budgets and the sweep

Every family below is a threshold or floor atom, so the counting proof is Lemma 1 of
`threshold.py` verbatim: disjoint closed cores have disjoint traces, a charged trace has
at least `k` points, so at most `floor(|S|/k)` cores are charged.
No family needs a different rule; the *graph* forms (an odd cycle over the cycle’s
members only, an odd wheel, a clique over a listed set) are weaker than the atom forms,
which charge every core holding the points, and the atom budget is the graph budget
(`floor((2m+1)/2) = m` for an odd cycle, `2` for a five-wheel by the floor atom).
The sweep decides all of them on the same event grid: the trace is constant on open
cells, the charge is monotone in the trace, the minimum is on an open cell, and each
atom enters the `int64` difference array either by the binomial identity (threshold;
floor as a sum of thresholds at `jk`) or by one count grid thresholded
(`charge_grid_direct`’s route), which is the right route once `|S|` is large.

**Collinear atoms are linear, not exponential (PROVED).** For `S = {s_1 < ... < s_m}` on
a line, a convex core meets the line in a segment, so `P ∩ S` is a run of consecutive
points and `[|P ∩ S| >= k] = [P holds some run of k]`. Let `Q_i = R_{s_i} ∩
R_{s_{i+k-1}}` (centres whose core holds both ends of run `i`, hence the run); the index
set `{i : P in Q_i}` is contiguous and `Q_i ∩ Q_j = R_{s_i} ∩ R_{s_{j+k-1}}`, so
`1_{∪ Q_i} = sum_i 1_{Q_i} - sum_i 1_{Q_i ∩ Q_{i+1}}` exactly: `2(m - k) + 1` signed
rectangle terms with coefficients `±1`. A wall-line atom with forty points and `k = 10`
costs 61 terms, where the binomial expansion would cost `2^40`.

### B.2 Cost table

Signed rectangle terms `sum_{j>=k} C(|S|, j)`, absolute coefficient sum `sum_j C(j-1,
k-1) C(|S|, j)` (`absolute_expansion_sum`, the headroom quantity), and the extra terms a
floor atom adds:

| atom | budget | signed terms | `sum abs(coef)` | floor extra terms | 2,000 atoms at weight `0.03`, scale `10^9` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2`-of-`3` | 1 | 4 | 5 | 0 | `3.0e11` |
| `3`-of-`4` (dominated) | 1 | 5 | 7 | 0 | -- |
| `2`-of-`5` | 2 | 26 | 49 | 6 | `2.9e12` |
| `3`-of-`5` | 1 | 16 | 31 | 0 | `1.9e12` |
| `4`-of-`7` | 1 | 64 | 209 | 0 | `1.3e13` |
| `2`-of-`7` | 3 | 120 | 321 | 72 | `1.9e13` |
| `3`-of-`8` | 2 | 219 | 1,023 | 37 | `6.1e13` |
| `5`-of-`9` | 1 | 256 | 1,471 | 0 | `8.8e13` |
| `6`-of-`11` | 1 | 1,024 | 10,625 | 0 | `6.4e14` |
| `8`-of-`15` | 1 | 16,384 | 580,865 | 0 | `3.5e16` |
| collinear `10`-of-`40` | 3 | 61 | 61 | -- | `3.7e12` |

The `int64` refusal is at `2^60 = 1.15e18`; the candidate at `191/50` used `2.0e10`.
Headroom binds nowhere below `|S| ≈ 15` and never for collinear atoms; the term count,
not the headroom, is the cost, linear in atoms times terms per atom against a grid of a
few thousand events per side.
Nothing in this table changes the sweep’s asymptotics for `|S| <= 9`.

### B.3 Separation from the LP dual

Given the symmetrised dual `y` of a plateau (nine to fourteen rows, 72 to 112 cores),
the exact oracles are those of A.3, in order of cost: arrangement vertices and
membership sets (`ceiling.py` and `cutting.float_vertices` enumerate them; seconds);
two-of-three by the pair-then-third search (seconds); budget-one weighted cliques by
maximal-clique enumeration plus piercing LPs (minutes); two-of-five and three-of-eight
by a five- or eight-set search seeded from the best triple, or by the CG MIP (minutes);
collinear atoms by scanning lines at a grid of offsets and directions
(`marks_and_lines.py` does horizontal lines in two seconds).
The loop’s present generator (pair-polygon vertices pulled inward, cap 24 per pair)
found the exact two-of-three maximum on the ceiling family, so it is adequate for that
shape; it generates no other shape, which is the gap.

### B.4 Ranking

| rank | family | what it captures | evidence at `191/50` | cost | verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | weighted clique atoms: `3`-of-`5` with one point doubled (`a = (2,1,1,1)`, `t = 3`), and generally the piercing measure of any clique with `tau* < 2` | non-Helly cliques of four or more cores that two-of-three sees only pairwise | the ceiling family’s heaviest clique `11/8` (`tau* = 5/3`) beats its two-of-three `5/4`; the polished optimum’s 26-clique `1.4107` (`tau* = 5/3`) beats its heaviest triangle `0.75` | 16 terms; no sweep change; `ThresholdAtom` needs repeated points allowed or near-duplicates emitted; generator = maximal cliques + piercing LP | **build first** |
| 2 | floor `2`-of-`5` (and `3`-of-`8`) | odd cycles through slivers, odd wheels | five-cycles at `5/8` and `0.848` against `2`: nothing at `191/50`; lane T predicts them for half-integral duals, and the record’s duals are quarter- or eighth-integral | 32 terms; generator = five-set search from the best triple, or the CG MIP | second, after the plateau dual is read |
| 3 | exact two-of-three separation on vertex sets | the same shape, exhaustively | reproduces `5/4` exactly in 19 s | script exists | promote into the loop and the ceiling verifier |
| 4 | wall-line and interior-line atoms (collinear, budget `floor(len/c)`) | wall usage above three | exactly `3.0000` on the plateau family, `2.96`-`3.00` on the polished optimum: tight, never violated | 61 terms each | measure on each plateau dual (two seconds); do not build a loop around it |
| 5 | `3`-of-`4`, `4`-of-`6` | nothing beyond `2`-of-`3`, `3`-of-`5` | dominated (A.1) | -- | do not build |
| 6 | rank-two atoms (thresholds of sums of rank-one charges) | whatever survives K6 | none yet | bookkeeping only | only after a K6-certified plateau |

## C. Where conditioning enters the fractional certificate

PR 137’s object at `q = 96/25`: four distinct owners (one per corner, each holding one
of two marks; proved from the measure-free certificate bc-293 of mass `11.262` and the
cross-corner distance `1.8545 > B sqrt 2`), sixteen classes per corner, each class
guaranteeing a closed patch `F` inside the owner’s core; residual cores avoid the union
of the four patches; budget below seven.
Three ways to put that inside one certificate:

**C.1 Mark atoms with negative weight (PROVED sound, EXACT worthless at 3.82).** Let
`K_c` be the cores holding a mark of corner `c`. The Owner Lemma says every
eleven-packing at `L <= 96/25` has at least one core in each `K_c` (the marks are
absolute points, so the lemma reads unchanged in a smaller container).
Then for `z_c >= 0` the atom “charge `-z_c` to every core in `K_c`” has budget `-z_c`:
`sum_i (-z_c [P_i in K_c]) = -z_c
#{i : P_i in K_c} <= -z_c`. The certificate condition becomes `charge(P) >= 1 + z_c [P
in K_c]` with budget `< 11 + sum_c z_c`, equivalently an owner-aware count.
This is the only sound use of a negative weight: `model.py` refuses signed point weights
because no lower bound on a point’s occupancy exists; here the Owner Lemma supplies one.
Its dual reading is `y(K_c) >= 1`. On the ceiling family `y(K_c) = 1` exactly at all
four corners and for each mark separately; on lane M0’s polished optimum
`499999999/500000000` (`marks_and_lines.py`, both in the `191/50` frame and in the
`96/25` frame).
The constraint is already tight at the optimum, so the atom moves nothing
at `191/50`; the retained duals are owner-saturated, as the corner-pair proof itself
predicts (the pair’s mass `0.2656` exceeds the slack `0.2621` by `0.0035`, so the duals
had no room to avoid the marks).

**C.2 Patch deletion is a disjunction (PROVED).** In class `j` the residual cores avoid
`F_j` because `F_j` lies inside the owner’s core and cores are pairwise disjoint closed
sets; that is an *edge* fact `x_P + x_O <= 1` for each owner `O ⊇ F_j` and each `P`
meeting `F_j`, and aggregated over owners it is the clique `K_{c,j} ∪ {P}`, which is
Helly (a common point in `P ∩ F_j`) and hence already a point constraint.
The LP gains nothing from the patch as an inequality; what PR 137 uses is integrality,
“the owner is one core”, which a fractional packing spreads over sixteen classes.
That is a lift-and-project step on the class disjunction, of Chvátal rank at least two
in general, and no single rank-one certificate expresses it.
The sound single object is:

> **Class-indexed threshold certificate.** Fix `(n, L, B, net)` with Conditions 3 and 4.
> Let `J` be a finite set of classes with, for each `j`, a closed set `F_j ⊂ [0, L]^2`
> and an integer `m_j >= 0`, and a *Class Lemma*, proved outside the sweep: every
> packing of `n` unit squares in `[0, L]^2` belongs to some class `j`, meaning that
> `m_j` of its selected cores are pairwise distinct and their union contains `F_j`. For
> each `j` let `A_j` be a finite family of point and threshold atoms with charge `c_j`
> and budget `M_j` such that
> 
> - **C2_j** `M_j < n - m_j`;
> - **C5_j** every closed `B`-square at a direction of the *doubled* net, inside the
>   container and disjoint from `F_j`, has `c_j(P) >= 1` (or: `A_j` and `F_j` are
>   D4-invariant and the folded net suffices, exactly as Condition 1' allows).
> 
> Then no such packing exists.
> *Proof.* Take the packing’s class `j`; its `n - m_j` non-owner cores are pairwise
> disjoint closed sets, admissible at doubled-net directions by Condition 4, and
> disjoint from `F_j` since `F_j` lies in the union of the other cores; C5_j charges
> each at least one, Lemma 1 bounds the sum by `M_j`, and C2_j contradicts.
> ∎
> 
> The residual domain `{c : P(c) ∩ F_j = ∅}` is open; the sweep still decides its
> infimum on open cells because boundary centres carry at least the charge of an
> adjacent open cell (Lemma 2 of the docstring), and the strict clearance `B(1 + D) < 1`
> is what puts the physical residual cores in the open domain.
> The point-only, unit-dot case with `m_j = 4` and `M_j = 5` is T-023.

Where it fails: the Class Lemma is the one input the sweep cannot check (V3 until
mechanised); the symmetry of the folded net is lost unless `F_j` is symmetric, so a
generic class costs the doubled net and eight times the columns; and a single family
`A_j` serves several classes only if their forbidden sets *contain* a common `F` (PR
137’s reuse rule), which is set containment, not area.

**C.3 A single certificate with `n - 4` is impossible (PROVED given the point-extension
lemma).** A certificate valid for every class at once must charge every core that is
residual in *some* class, i.e. every core avoiding at least one patch of each corner;
that domain contains every core avoiding the marks (each patch contains its mark).
PR 137’s point-extension lemma says one unit dot at an owned mark turns a cover of the
cores avoiding the mark into a global cover, so the covering value of that domain is at
least `tau(96/25) - 4 >= 11 - 4 = 7` (the `11` is the ceiling transferred upward).
Budget below seven is unattainable; the disjunction is essential.

**C.4 The right hybrid.** Not “one certificate” but “one tree with certificates at
internal nodes”: the root is the unconditional threshold certificate (`m = 0`, budget
`< 11`); a child fixes one corner’s class (`m = 1`, one patch, budget `< 10`); and so
on. A node whose certificate is accepted prunes every leaf below it.
This is branch-and-cut, and it is where the two lines meet: the internal-node programs
have the same integrality gap as the root, and threshold and floor atoms are what close
it. It also answers the class-count question without a census: the tree’s size is the
number of nodes whose relaxation could not be certified, not `65,536`.

## D. Adversarial read of X-024

**“Each conditioned square bought about 1.7 units for a price of 1.”** Two artefacts and
one selection effect.
The `11.88` is exp-142’s *nine-direction, restricted-site* covering value; fewer
directions lower a covering value and restricted sites raise it, so it is neither a
bound nor comparable to the exact 361-direction `5`. The exact comparison at `96/25`:
the retained measure-free certificate bc-293 has mass `11.2620995` and satisfies
Conditions 1, 3, 4, 5 on the full net, so `tau(96/25) <= 11.262`; the gain is at most
`(11.262 - 5)/4 = 1.566` per owner, and the point-extension lemma caps the mark part at
one, leaving at most `0.566` per owner for the patch.
That is measured on the one class of `65,536` that was covered; the deletion screens say
nothing about the others (they bound nothing, as PR 137 states).
So the figure is optimistic by at least a quarter and is an upper-tail sample.
Not a nine-direction artefact only: the frame is wrong as well as the sample.

**“The conditional engine scales toward pinning Trump’s structure.”** Forced structure
does accumulate: the measure-free argument works whenever a mark set’s mass exceeds the
slack `M - 11`, and at `96/25` the slack is `0.262` against a pair mass of `0.266`, a
margin of `0.0035`, so every further layer at the same side competes for the same
`11.26` of mass.
But the residual per leaf shrinks by one square and a patch of area well
under one while the leaf count multiplies by the class count per layer: `65,536` raw at
the first layer, perhaps `8,192` after D4, unmeasured after compatibility pruning, and a
second layer of wall-segment owners multiplies again.
Trump’s packing must survive in its own leaf at `3.877`, so at `3.84` every leaf is
excluded only by the side margin `0.037`; the leaves are easy, the tree is the cost.
Without internal-node bounding (C.4) the engine is exhaustive enumeration, and “it
scales in the direction the endgame needs” describes the leaf difficulty, not the tree.
The class census (slice B1) is the right measurement, but it should count the nodes the
bounding fails to prune, which needs the internal-node certificate first.

**“The unconditional route is the highest value per certificate.”** True per success,
and the memo names the risk ("a second plateau") without pricing it.
Priced (F5): the point LP’s slope is at least `13.6` per unit of `u`; the two-of-three
margin at `u =
3.8288` is `0.033`; `383/100` asks for `u = 3.8388`, a step of `0.010`. Unless the cut
LP’s slope is under a quarter of the point LP’s, the run plateaus, and then route A’s
value per certificate is zero until the next family exists.
The memo’s own H-156 notes say “whether the threshold LP’s slope is gentler is the whole
question” and then plan `383/100` followed by `96/25`; the plan should have been “read
the plateau, name the cut, build it”, which is E. The `3.8266` dilation figure is the
point-atom transfer ratio applied to the threshold certificate; two-of-three charges
flip when a core loses one of two points, so their coverage at intermediate directions
is less robust than a point mass’s, and the crossing shrink may sit above the point
certificate’s `0.99798`. OPEN, being measured.

**“Threshold atoms are the tool the conditional line needs.”** Half right.
The class that was covered needed no LP at all: five unit dots, an integral piercing
set. Where a class resists, PR 137 itself names two causes, “the relaxation is too weak”
(residual cores that could never coexist) and “the search is incomplete”; threshold
atoms address a third, the integrality gap of the residual LP, which nobody has yet
shown to be the binding one on any class.
What the conditional line needs first is bounding at internal nodes (C.4), and there
threshold atoms are the tool.
Two costs the memo omits: a class has no D4 symmetry, so the threshold sweep loses
Condition 1' and runs on the doubled net with eight times the columns; and
`sweep.centre_domain` is the inset square, so the residual domain needs PR 137’s
polygons joined to the sweep (E1), a build, not a switch.

**What the memo gets right.** The two lines share cores, sweep and obstruction; the
finer-net gain is free and real; the ceiling family is the right object; and the
division of labour is sensible.
The corrections are the pricing of route A and where threshold atoms enter route B.

## E. One recommendation

Both outcomes share a first hour: **build the exact plateau reader** (A.3, K4-K6) as one
devtool on top of `ceiling.py`, `cutting.float_vertices` and lane M0’s `clique_scan`:
vertex membership sets, the two-of-three triple search (`twothree_exact.py`, 19 s on 88
cores), maximal cliques above weight one with exact piercing LPs, wall and diagonal line
chords (`marks_and_lines.py`), and the CG-separation MIP through HiGHS with exact
re-verification of any cut it returns.
Its output on a family is a ranked list of violated atoms with exact violations, or a
certificate that none exists, per family.
Two to three hours for one Fable agent; the two searches already exist as scripts.

**Outcome 1: the `383/100` run reaches a rows-complete value below eleven.**

| step | instrument | measurement | discriminator |
| --- | --- | --- | --- |
| 1 | `decide_threshold_certificate`, both routes | the frozen `383/100` bytes | both routes agree; `s(11) >= 383/100` |
| 2 | the finer-net crossing-shrink measurement now running on the `191/50` certificate, re-pointed at the new bytes | `B_cross(720)`, `B_cross(1440)` | the dilation record; about `3.8366` if the transfer ratio holds |
| 3 | the plateau reader on the `383/100` dual at the last plateau before the drop (the loop logs it) | which atoms carried the drop | whether the gain was two-of-three alone or the site separation |
| 4 | the loop at `96/25` (`u = 3.8489`) from the `383/100` site and atom set, with weighted clique atoms already in the generator | rows-complete value | below eleven: freeze; at eleven: outcome 2 at `96/25` |

The slope reading from step 1, `(11 - value)/0.010`, replaces F5’s assumption and prices
step 4 before it runs.

**Outcome 2: the run plateaus at eleven.**

| step | instrument | measurement | discriminator |
| --- | --- | --- | --- |
| 1 | `verify_ceiling` on the symmetrised plateau dual | exact depth | depth `<= 1` and weight `>= 11`: a point-ceiling family at `383/100` (expected) |
| 2 | the plateau reader, K4 | exact maximum two-of-three charge | `<= 1`: the two-of-three method is capped at `383/100`, a theorem; `> 1`: the loop’s generator missed it, so add the exact triple as an atom orbit and re-solve (one round, minutes) |
| 3 | the plateau reader, K5 and K6 | heaviest `tau* < 2` clique; heaviest five-cycle; line chords; the CG MIP’s best cut | names the family that moves the value, with its exact violation; if K6 finds nothing, the rank-one cap is at `383/100` and only rank two or the class tree remain |
| 4 | weighted clique atoms in the loop (allow repeated points in `ThresholdAtom`, or emit near-duplicate points; generator = maximal cliques + piercing LP) | one atom round plus rows-only completion at `383/100` | rows-complete value below eleven: freeze and gate; at eleven: step 3’s next family (floor two-of-five) |
| 5 | if steps 3-4 leave the value at eleven | the loop at `L = 3.825` from the same columns | locates the two-of-three cap to `0.0025`; a certificate there still dilates by about `+0.0066` on the finer net |

The measurement that discriminates everything is step 2 of outcome 2: whether the
plateau family is two-of-three-feasible.
If it is, the plateau is a theorem and step 3 names the cut; if it is not, the loop’s
generator, not the language, was the limit.
Either way the branch spends its next four hours on the plateau family, not on the next
side.

What not to do in the next four hours: bisect the side with the present loop (each point
is ninety minutes and locates a cap that step 3 names directly); build three-of-four
(dominated); build wall atoms as a family (tight, never violated, on every plateau
family seen); or start the class census before an internal-node certificate exists.

## Files

- `twothree_exact.py`, `twothree-ceiling.log`, `twothree-ceiling.json`: the exact
  two-of-three maximum of [`ceiling-family-191-50.json`](ceiling-family-191-50.json) (88
  cores, 304 distinct lines, 20,376 vertices, 1,541 membership sets, maximum `5/4` at a
  triple with memberships `(4, 8, 8)`; 19 s). Not retained (scratch only); the
  measurement is K4 of `packing/devtools/plateau_reader.py`, which reports the same
  `5/4` in 2.5 s.
- `marks_and_lines.py`, `marks-and-lines.log`: mark-clique weights and horizontal-line
  chord weights on [`ceiling-family-191-50.json`](ceiling-family-191-50.json),
  [`lane-m0-bc200-polished-191-50.json`](lane-m0-bc200-polished-191-50.json) and
  [`lane-e-cutting-191-50-family.json`](lane-e-cutting-191-50-family.json).
  Not retained (scratch only); the chord half is the reader’s line search, the mark half
  is not in the reader.
- Repository inputs: `packing/src/sqpack/fractional/certificate.py`,
  `packing/src/sqpack/fractional/threshold.py`,
  `packing/src/sqpack/fractional/ceiling.py`, `packing/src/sqpack/fractional/sweep.py`,
  `packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md`,
  `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-b-threshold-atoms-at-191-50.md`,
  `.../agenda-034/lane-t-theory-cuts-and-routes.md`,
  `.../agenda-034/lane-m0-fixed-support-polish-191-50.md`,
  `.../agenda-034/lane-e-lp-runs-61-16-and-191-50.md`,
  `.../agenda-034/lane-a-net-refinement-and-shrink-tax.md`,
  `.../agenda-032/gaps-to-global-bound.md`, `.../agenda-032/sprint-report.md`,
  `.../agenda-032/proofs/point-extension-lemma.md`,
  `.../agenda-030/bc-303-first-wave-selection.md` (the corner-pair theorem and bc-293’s
  mass), `packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md`,
  `docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md`,
  `packing/frontier/n-011.md`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
