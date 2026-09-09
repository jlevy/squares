# Agenda 034, lane B: threshold atoms at 191/50

Retained measurement-lane report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by
sub-agents on 2026-09-09 under the breadth survey: spike B, and after it the resume that
completed its rows and decided the candidate.
Both reports are reproduced as delivered, in order, each with its own findings table and
status labels; X-023 carries the coordinator’s reading.

**The candidate frozen in Part 2 is accepted by one exact route only and is not a
retained result.** `devtools.decide_threshold_certificate` decided its five conditions,
and the tool’s own verdict says as much: “ACCEPTED (one exact route; retention wants an
independent verifier)”. An independent verifier for threshold certificates, and a review
of the theorem of Part 1, are in progress.
Nothing here is a registered round or a new bound.

Retained beside this report:
[`lane-b-threshold-candidate-191-50.json`](lane-b-threshold-candidate-191-50.json), the
frozen candidate — 673,639 bytes, SHA-256
`3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, re-verified after
the copy — and [`lane-b-decide-191-50.log`](lane-b-decide-191-50.log), the decision log.
The ceiling family of Part 1 §3.3 was already retained in this directory as
[`ceiling-family-191-50.json`](ceiling-family-191-50.json); it is byte-identical to the
spike’s own copy (14,039 bytes, SHA-256
`95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427` on both), so it was
not copied again and both parts link to the retained one.
Every other file either part names is not retained (scratch only); [Files](#files) lists
them with the sizes that matter.

## Part 1 — Spike B: threshold atoms (rank-1 Chvátal–Gomory cuts) for the n = 11 certificate

Scratch: `spike-b/` in the untracked scratchpad, not retained (scratch only).
Branch `claude/n-11-stronger-result-d730ds` at `943f9cf`, nothing committed.
One core (`PACK_JOBS=1`), scipy HiGHS for every LP. Labels: EXACT (rational decision),
CHECKED (float computation, script retained), RECORD (retained file), OPEN.

### 0. Findings in one page

| # | Finding | Status |
| --- | --- | --- |
| F1 | Threshold-certificate theorem (Section 1): conditions C1'–C5' with budgets `w·floor(|S|/k)`; the event-cell sweep decides C5' on open cells; inclusion–exclusion puts a threshold atom into the same int64 difference array. | proved (Section 1) |
| F2 | Both retained depth-one families violate rank-1 2-of-3 cuts: 3,504 atoms in 438 D4 orbits at 191/50 (max charge 1.0785, total violation 55.0) and 52,088 in 6,471 orbits on the unit control (max 1.1848); 92 % of the violation mass is on mixed near-axis/tilted triples; no 2-of-5 cut is violated among 2 M chordless 5-cycles; the brief’s own-weight filter is vacuous (heaviest placement 0.148). | EXACT (charges), CHECKED (cycle cap) |
| F3 | Threshold columns lower the restricted covering value at 3.82 on the record’s 12,761 sites from `11.055617` to exactly `11.000000` in one round (600 orbits, 16 active, budget 1.38); more atom rounds (945, 1120 orbits) leave it at `11.000000`. | CHECKED (float LP), control RECORD |
| F4 | **Ceiling at 3.82.** After one exact site-separation round the LP dual is eleven rows at weight exactly 1; its D4-symmetrised family (88 closed `B`-squares at net angles, weight 1/8 each, total exactly 11) has exact maximum depth 1 over the 20,376 vertices of its arrangement. `verify_ceiling`: `proved=True`, regime `net`, `symmetric_only`. So **no D4-symmetric point-atom measure of mass below 11 exists at `L = 191/50`, `B = 9977/10000`, on this net or any net containing its six directions**, on any site set: the plateau at 3.82 is a theorem, not a search artefact. Frozen as [`ceiling-family-191-50.json`](ceiling-family-191-50.json), SHA-256 `95cf0647…6427`. | EXACT (`verify_ceiling`) |
| F5 | The ceiling transfers upward in `L` and (proof in 3.4) downward in `B` at the same net; it does not survive a rigid move to `B > 9977/10000` (max depth `7/4` after clamping at `B' = 0.998`), so the finer-net / larger-`B` regime stays open. | EXACT (depths), reasoning |
| F6 | **The ceiling family is separated by 2-of-3 cuts** once the atom points are placed near the vertices of the pairwise-intersection polygons (strictly inside, pulled 1/1000 to 1/10 towards the polygon centroid): maximum charge exactly `5/4` against budget 1, hundreds of violated triangles, zero ambiguous containments. Pair-centroid points (the loop’s generator) see nothing above 1. So the threshold method is not capped by the ceiling that caps the point method. | EXACT (charges) |
| F7 | Combined loop with the interior-vertex generator (run 3, 3 cycles, 50 min): cuts + sites take the restricted value to `10.927`, `10.949`, `10.956`; threshold-aware rows refill it to exactly `11.000000` each time on a new near-integral 9–14-row dual. No candidate below 11 with complete rows within the budget; convergence below 11 is OPEN. Task 4’s freeze/decide tooling is in place and exercised. | CHECKED |

### 1. Theorem: threshold certificates

**Setting.** `Q = [0, L]^2`, `n >= 1`, shrink `B > 0`, half-tangent net
`0 = t_0 < ... < t_K` reaching pi/4 (`t_K^2 + 2t_K - 1 >= 0`) with largest half-gap
tangent `D`, `B(1 + D) < 1`. An *admissible core* is a closed `B`-square at a net
direction inside `Q`; `𝒫` is their set; `G = D4` acts on `Q` by the eight maps of
`d4_images`.

**Atoms.** A *set-function atom* `A = (S, phi, w)`: `S` a finite set of distinct points
of `Q`, `phi : 2^S -> Q_{>=0}` monotone with `phi(∅) = 0`, `w >= 0`. Charge on a closed
set `P`: `c_A(P) = w phi(P ∩ S)`. Budget: `beta_A = w beta(phi)`,
`beta(phi) = max { sum_i phi(T_i) : T_i pairwise disjoint subsets of S }`. Instances:
point atom (`S = {p}`, `phi(T) = [p ∈ T]`, budget `w`); **threshold atom** `(S, k, w)`,
`1 <= k <= |S|`, `phi(T) = [|T| >= k]`, budget `w floor(|S|/k)` (at most `floor(|S|/k)`
disjoint subsets have size `>= k`, and a partition into `k`-blocks attains it); *floor
atom* `phi(T) = floor(|T|/k)`, same budget since `sum_i floor(|T_i|/k) <=
floor(|S|/k)`, charge dominating the threshold atom’s -- the rank-1 CG cut proper, which
a future implementation should carry (weighted form `floor(a(T)/t)`, budget at most
`floor(a(S)/t)`). This spike implements threshold atoms; everything below holds verbatim
for floor atoms.

**Lemma 1 (packing bound).** For pairwise disjoint closed `P_1..P_m`,
`sum_i c_A(P_i) <= beta_A`: the traces `P_i ∩ S` are pairwise disjoint subsets of `S`. ∎
It needs `w >= 0` (a negative `w` reverses it: `model.py`’s five-atom forgery) and
nothing else; monotonicity of `phi` is for the decision procedure (Lemma 2).

**Certificate and conditions.** A finite list `𝒜` of point and threshold atoms, charge
`c(P) = sum_A c_A(P)`, budget `M = sum_A beta_A`.
- **C1'** for every `g ∈ G` and `(S, k, w) ∈ 𝒜`, `(gS, k, w) ∈ 𝒜`; operationally, merge
  equal `(S, k)` and require the weight function to be constant on `G`-orbits (point
  atoms checked as today).
  Then `c(gP) = c(P)`, since `c_{gA}(gP) = w[|gP ∩ gS| >= k] = c_A(P)` and `g` permutes
  `𝒜`.
- **C2'** `M < n`. **C3**, **C4** unchanged.
  **C5'** `c(P) >= 1` for every `P ∈ 𝒫`.

**Theorem.** C1'–C5' imply that `n` closed unit squares with pairwise disjoint interiors
do not fit in `Q`, hence `s(n) >= L`. *Proof.* Let `U_1..U_n` be such squares,
`theta_i ∈ [0, pi/2)` their angles.
If `theta_i <= pi/4`, C3 gives a net direction within half a gap and C4 puts the
concentric closed `B`-square `P_i` at that direction inside `int(U_i)`
(`B(cos d + sin d) <=
B(1 + D) < 1`, as in `certificate.py`); `g_i = id`. Otherwise let `g_i` be the
reflection of `Q` in its diagonal: `g_i U_i` has angle `pi/2 - theta_i < pi/4`, contains
such a core `P_i'`, and `P_i = g_i^{-1} P_i' ⊂ int(U_i)`. In both cases `g_i P_i ∈ 𝒫`,
so C5' and C1' give `c(P_i) = c(g_i P_i) >= 1`. The `P_i` are pairwise disjoint closed
sets, so Lemma 1 atom by atom gives `n <= sum_i c(P_i) <= M < n`. ∎

Remarks. (i) If `k | |S|` the threshold constraint is implied by the point constraints;
the useful shapes are `2-of-3`, `3-of-4`, `2-of-5`, `3-of-5`, `4-of-7`, ... -- clique
and odd-cycle inequalities on the dual side.
(ii) Helly: four convex placements meeting three at a time share a point, so `3-of-4`
with points in triple intersections never charges a whole 4-clique.
(iii) Every valid cut keeps every integer packing feasible: eleven pairwise disjoint
admissible cores would forbid any threshold certificate; at `191/50`, `9977/10000` that
is eleven unit squares in side `3.8288`, which the target denies.
The reach is the rank-1 closure, not the integer value.

**C5' is decided by the exact event-cell sweep.** At a net direction with rotated frame
`(u, v)` a core is `P(c) = { q : |q_u - c_u|, |q_v - c_v| <= B/2 }` and `s ∈ P(c)` iff
`c ∈ R_s := [s_u - B/2, s_u + B/2] × [s_v - B/2, s_v + B/2]`, the closed rectangle
`reduce_to_spans` builds.
The event grid is the sorted set of all `s_u ± B/2`, `s_v ± B/2` over *every* atom point
(point atoms and threshold points), plus the extremes of the centre domain `Ω`. Write
`T(c) = { s : c ∈ R_s }`; `c(P(c))` depends on `T(c)` alone and is monotone in it.

**Lemma 2.** (a) `T` is constant on each open cell `C`. (b) If `c ∈ closure(C)` then
`T(c) ⊇ T(C)`, so `c(P(c)) >= c(P(C))`. (c) Every point of `Ω` on a cell boundary lies
in the closure of an open cell meeting `Ω`. Hence
`min_{c ∈ Ω} c(P(c)) = min { c(P(C)) : C open, C ∩ Ω ≠ ∅ }` and the sweep may omit the
boundaries. *Proof.* (a) a cell’s `u`-interval lies between consecutive events and the
edges of `R_s` are events, so it is inside or disjoint; likewise in `v`. (b) `R_s` is
closed. (c) `Ω` is convex with nonempty interior (C5' presupposes an admissible core),
any neighbourhood of `c ∈ Ω` contains interior points of `Ω` off the nowhere-dense grid
lines, and such a point lies in an open cell whose closure contains `c`. ∎
`reduce_to_spans` marks a superset of the cells meeting `Ω`; a minimum over a superset
is at most the true one, so `>= 1` on the marked cells implies C5'.

**Threshold atoms in the integer prefix-sum grid.** For an open cell with
`m = |T(C) ∩ S|`, `[m >= k] = sum_{j=k}^{m} (-1)^{j-k} C(j-1, k-1) C(m, j)`. *Proof.*
With `f_k(m)` the right side, `C(j-1, k-1) = C(j, k) - C(j-1, k)` and
`C(j, k) C(m, j) = C(m, k) C(m-k, j-k)` give `f_k(m) = C(m, k)(1-1)^{m-k} + f_{k+1}(m) =
[m = k] + f_{k+1}(m)`, and `f_k = 0` for `k > m`, so `f_k(m) = [m >= k]`. ∎ Since
`C(m, j)` counts the `j`-subsets `T ⊆ S` with `C ⊆ ⋂_{t∈T} R_t`,

```
[|P(C) ∩ S| >= k] = sum_{j>=k} (-1)^{j-k} C(j-1, k-1) sum_{|T|=j} [C ⊆ ⋂_{t∈T} R_t],
```

each `⋂ R_t` a closed axis-aligned rectangle with event-coordinate corners (empty:
skipped; degenerate: its four corner entries cancel on every open cell).
So a threshold atom is `sum_{j>=k} C(|S|, j)` signed rectangle terms in the *same*
difference array (`2-of-3`: 4 terms, `3-of-4`: 5, `2-of-5`: 26, `3-of-5`: 16), and after
the two prefix sums every open cell holds
`scale · (sum_p w_p [p ∈ P(C)] + sum_A w_A [|P(C) ∩ S_A| >=
k_A])` exactly.

*Why this does not conflict with `sweep.py`’s refusal of signed weights.* That refusal
guards a precondition of the theorem (a signed point weight makes the charge
non-monotone and Lemma 1 false).
Here every signed term is an exact expansion of the nonnegative monotone `w[|T| >= k]`
on the open cells, where the identity holds; the function whose minimum is decided is
`c(P(C))`, monotone in the trace, and Lemma 2(b) speaks about that function, not about
how its cell values were obtained.
In code `ThresholdAtom` refuses `w < 0`, `k < 1`, `k > |S|`, repeated points; the
expansion is internal to the grid builder, whose int64 headroom check uses
`scale · sum_A w_A sum_{j>=k} C(j-1, k-1) C(|S|, j)` (the largest intermediate entry);
`charge_grid_direct` (one count grid per atom, thresholded) is the independent route.

**Dual side.** Minimise `sum_p w_p |O_p| + sum_A w_A |O_A| floor(|S_A|/k_A)` subject to
`sum_p a_{P,p} w_p + sum_A t_{P,A} w_A >= 1` per row (`t_{P,A}` = images `S' ∈ O_A` with
`|P ∩ S'| >= k_A`). The dual adds `sum_P y_P t_{P,A} <= |O_A| floor(|S_A|/k_A)` to the
fractional packing, i.e. for the D4-symmetrised dual
`sum_{P' : |P' ∩ S_A| >= k_A} y_{P'}
<= floor(|S_A|/k_A)`: clique (`2-of-3`) and odd-cycle (`2-of-5`) inequalities.
An atom prices in iff its charge against the symmetrised dual exceeds its budget.

### 2. Separation on the retained depth-one families

Scripts `sep_family.py` (stage A graph, representatives, triangles, 2-of-3; stage B
chordless 5-cycles, 2-of-5); logs/outputs `sep-b19150.*`, `sep-unit127.*`; 243 s and 239
s on one core. **Inputs (RECORD):** `bc-200-family-191-50.json`, 760 placements at
`L = 191/50`, `B = 9977/10000`, total `9.907905595`, max depth 1 over 2,769,100
vertices; `agenda-030/pr127-unit-control.json`, 768 unit placements declared at `96/25`,
total `10.384212408`, max depth 1 over 2,702,488 vertices (a different family, BC-232
leg 01).

**Method.** Weights rounded *down* to `10^-9` (`cutting.tidy_family`, loss `3.6e-7`,
`3.8e-7`), so every charge is a lower bound on the retained-weight charge.
Overlap graph by float prescreen plus the exact separating-axis test; pairwise
intersection polygons by Sutherland–Hodgman in `Fraction`s, representative = vertex
average (every edge has positive area, median `0.081` / `0.091`); containment with a
`1e-9` float screen and `Placement.contains` on ambiguous pairs (8 and 0); 2-of-3 charge
= sum of `y_P` over the *whole* family for placements containing `>= 2` of the points,
`int8` for every triangle (CHECKED), every atom reaching `1 - 1e-7` re-summed exactly
(EXACT).

| Quantity | 191/50 family | unit control | status |
| --- | --- | --- | --- |
| overlapping pairs / all pairs (mean degree) | 121,144 / 288,420 (318.8) | 122,064 / 294,528 (317.9) | EXACT |
| heaviest placement / pair / triangle own weight | `0.1484` / `0.2967` / `0.3943` | `0.1599` / `0.3198` / `0.4692` | EXACT |
| triangles | 10,043,912 | 10,349,056 | EXACT |
| 2-of-3 charges in `[0.95,1)` / `[1,1.05)` / `[1.05,1.1)` / `[1.1,1.2)` | 148,152 / 3,376 / 128 / 0 | 212,272 / 48,160 / 3,464 / 464 | CHECKED |
| violated atoms (charge `> 1`) / distinct D4 orbits | 3,504 / 438 | 52,088 / 6,471 | EXACT |
| maximum charge | `1.078511` | `1.184795` | EXACT |
| total violation, all atoms / one per orbit | `55.025` / `6.878` | `850.173` / `104.307` | EXACT |
| orbits with violation `>= 0.02` / `0.05` / `0.1` | 106 / 16 / 0 | 798 / 478 / 58 | EXACT |
| top-300 atoms with empty triple intersection | 268 | 0 | EXACT |
| chordless 5-cycles examined (cap) / max 2-of-5 charge (budget 2) | 2,000,000 / `1.907361` | 2,000,000 / `1.889828` | CHECKED |

The brief’s filter “triangle weight sum `> 1`” is vacuous on these smeared duals
(heaviest triangle `0.39` / `0.47`; heaviest 5-cycle `0.36` / `0.43`): a violated cut
collects from tens of small placements that each contain two of its points.
No 2-of-5 cut is violated on cycle-edge representatives; `3-of-4` was not run (Remark
ii).

**Where the violation lives** (191/50 family; orbits / violation mass by angle class,
axis `<= 2.5°`, `29` in `[25°, 35°]`, other): `axis-axis-other` 63 / 1.99,
`29-axis-other` 122 / 1.61, `29-axis-axis` 129 / 1.34, `axis-other-other` 47 / 1.15,
`29-29-29` 23 / 0.27, `29-29-other` 15 / 0.24, `29-29-axis` 28 / 0.19, `29-other-other`
10 / 0.08, `axis-axis-axis` 1 / 0.004 (a `0.26°` triple).
92 % of the mass is on triangles mixing a near-axis and a tilted placement, as on the
unit control; by region 316 interior, 118 wall, 4 corner orbits.
The worst 191/50 atom (violation `0.078511`, 74 placements charged) joins two `0.26°`
placements and one at `44.32°`: points `(3.3945, 3.3945)`, `(2.8162, 2.8237)`,
`(2.8236, 2.8162)`, a pair `0.0105` apart straddling the diagonal and a third `0.81` up
it, a near-45° edge along the diagonal separating the pair.
Unit worst: `0.184795`, angles `42.04°, 1.58°, 1.32°`.

**Reading.** Both retained fractional packings violate hundreds of rank-1 clique cuts,
each by little (`<= 0.08`, `<= 0.19`), on mixed near-axis / tilted triples -- the
brief’s prediction. Whether they move the LP value is Section 3.

### 3. The restricted LP at 3.82 with threshold columns

Scripts `lp_threshold.py` (run 1), `lp_threshold2.py` (runs 2, 3); logs `lp-run*.log`,
checkpoints `lp-run*/`. State `bc-200-state-191-50.json` (RECORD): 12,761 sites in 1,657
D4 orbits, 9,868 snapped rows (`cutting.rows_from_exact`, 7,750,442 nonzeros); every LP
is scipy HiGHS, sparse.
**Control (CHECKED):** point-only optimum `11.055616943` against the record’s
`11.055617`; primal support 47 site orbits; dual support 117 rows = 936 placements after
D4 (total `11.055617`, the unscaled parent of the retained 760-family).

#### 3.1 Run 1: atom columns only, fixed rows and sites (CHECKED)

Separation against that dual (166,100 overlapping pairs, mean degree 355 -- denser than
the scaled family because the unscaled dual is 1.116 deep at vertices) found more than
the 600-orbit cap of violated 2-of-3 orbits (pair-centroid points).

| stage | atom orbits | objective | atom budget carried | active orbits | site support | LP s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 0 | `11.055616943` | -- | -- | 47 | 31 |
| atoms-0 | 600 | `10.999999999999968` | `1.382681` | 16 | 89 | 135 |
| atoms-1 | 945 | `11.000000000000025` | `1.690631` | 24 | 96 | 157 |

The cuts move the restricted value by `0.055617`, to `11.000000` -- an integer, to the
LP’s precision -- and stop there (a further 345 violated orbits, max charge `1.25`,
change nothing; the 24 active atoms are light, largest image weight `0.0264`). An
integer plateau on a fixed site set is the brief’s own signature (two lost site sets at
exactly `11.000000`), so the run was stopped for the record’s site separation.

**Anatomy of the exactly-11 dual** (`dual-anatomy-run2-start.txt`; EXACT depths): 18
support rows with quarter-integral weights (`1.5` ×1, `1` ×3, `0.75` ×2, `0.5` ×8,
`0.25` ×4), wall-middle and corner axis placements plus one `29.15°` and one `23.65°`
placement.
Symmetrised (144 placements, total 11) its exact maximum depth is `1.125` at a
vertex of its arrangement but `<= 1.000` at all 12,761 sites, and 120 of its 1,644 heavy
overlapping pairs meet in a sliver containing no site (largest area `0.00507`): lane F’s
unsampled-double-coverage mechanism, reached *because* the atoms removed the fractional
near-axis dual that used to hide it.

#### 3.2 Run 2: sites + atoms (+ rows when below 11), CHECKED unless marked

Each iteration: solve; symmetrise the dual; add its deepest arrangement vertices with
exact depth `> 1 + 1e-6` (`cutting.screened_separation`, cap 120 orbits) as site
columns; add violated 2-of-3 orbits (cap 400); sweep for rows only below 11 (rows only
raise the value). Seeded with run 1’s 945 orbits.

| stage | sites (orbits) | atom orbits | objective | dual support | LP s |
| --- | ---: | ---: | ---: | ---: | ---: |
| start | 12,761 (1,657) | 945 | `11.000000000` | 18, quarter-integral | 161 |
| site sep. 0: 1,672 vertices above 1, max `1.125`, +120 orbits; atoms +175 (max charge 1.125) |  |  |  |  |  |
| iter-0 | 13,721 (1,777) | 1,120 | `11.000000000` | **11 rows, all at weight 1** | 271 |
| site sep. 1: exact max depth **1** over 20,376 vertices, 0 above 1; no violated 2-of-3 on centroids: stopped |  |  |  |  |  |

#### 3.3 The ceiling (EXACT)

`ceiling-verdict-run2-iter0.txt`,
[`ceiling-family-191-50.json`](ceiling-family-191-50.json) (SHA-256
`95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427`). The eleven support
rows (float duals within `1.2e-12` of 1, exact value 1): nine near-axis placements at
directions 0, 1, 3, 5 -- five wall-middle/corner ones at direction 0 such as
`(3.3211, 0.4989)` and `(0.4994, 3.3206)`, `(3.3188, 3.3159)`, `(1.5143, 1.5231)`,
`(1.5079, 0.5161)`, `(1.5326, 3.3038)` -- and two tilted ones, `(2.4952, 1.3869)` at
`29.15°` (dir. 113) and `(2.4760, 1.3907)` at `25.67°` (dir.
99); the file lists all eleven exactly.
Two pairs are near-coincident: the integral family double-covers there and its D4
average compensates with gaps elsewhere.
Symmetrised: 88 distinct placements at `1/8`, total `11`. `verify_ceiling` (2.1 s): K0
admissible (`net` regime, mirrored angles, D4-symmetric measures only); K1 inside; K2
maximum depth exactly `1` at
`(264972971069099593854641303/10050443262954450608772780000, 191/100)` over 20,376
vertices, 3,675 decided exactly; K3 total `11 >= 11`. **`proved = True`.** Statement:
*no D4-symmetric measure of mass below 11 captures mass 1 in every closed `B`-square at
a net angle in the container, for this `B` and every net containing the angles used; the
fractional method cannot certify this `n` at this side or any larger side.*
Cross-readings: depth `<= 1` at all 13,721 sites; screened separation: 0 vertices above
1\.

This answers the brief’s OPEN item -- “whether `tau*(3.82) < 11`” -- in the negative for
this `B` and net: `tau*(191/50; 9977/10000, net) >= 11` over D4-symmetric measures, the
only measures Condition 1 admits.
The lost site sets that stopped at exactly `11.000000` were right; BC-200’s `11.055617`
was a site set short of its optimum.

#### 3.4 What the ceiling covers

- Upward in `L` (`ceiling.py`): no point certificate at any `L >= 191/50`, this `B`,
  net.
- Downward in `B` (proof, not in `ceiling.py`): for `mu` D4-symmetric with mass 1 on
  every closed `B''`-square at a net angle, `B'' < B`, let `P''` be each placement’s
  concentric `B''`-square; `1_{P''} <= 1_P`, so `11 = sum y_P <= sum y_P mu(P'') =
  ∫ (sum y_P 1_{P''}) dmu <= ∫ depth dmu <= mu(Q)`. So the ceiling holds for **every
  `B <= 9977/10000`** on any net containing `t = T k/180`, `k ∈ {0, 1, 3, 5, 99, 113}`
  -- every uniform refinement of the retained net included.
- Not to larger `B`: with the centres clamped into the `B'`-domain the exact maximum
  depth is `7/4` already at `B' = 998/1000` (`ceiling-depth-vs-B.txt`): the family is
  wall-tight. Net caps `B < 1/(1 + D)`: `0.997704` (180 steps), `0.998851` (360),
  `0.999425` (720); `B ∈ (0.9977, 0.99885]` on a 360-step net is open.
- Not to smaller `L`: the retained certificate at `381/100` exists; the least side `L*`
  with a total-11 ceiling family lies in `(3.81, 3.82]`.

#### 3.5 Does any threshold cut separate the ceiling family?

- Pair centroids (the loop’s generator): nothing above 1, which is why run 2 stopped.
- Points at **arrangement vertices** (`sep_ceiling.py`; 21,200 candidates, 15,136
  containments decided exactly, all combinations at cap 40): 3,280 triangles, maximum
  charge `10/8 = 1.25`, 1,428 violated.
  Best: triangle `(0, 40, 45)` (`0°, 29.15°,
  29.15°`), points `(2.81518, 1.83654)`, `(2.40905, 1.91)`, `(2.81518, 1.98346)`; exact
  recheck (`top-atom-exact.txt`): `5/4`, ten images, the whole orbit at `5/4`.
- **Interior points** (`sep_ceiling_interior.py`): the same candidates pulled towards
  their pair polygon’s centroid by `1/1000`, `1/100`, `1/10` (strictly inside both
  placements, 0 ambiguous containments), deepest 24 per pair plus the centroid: maximum
  charge **`10/8 = 1.25` at every pull**, 857 / 647 / 318 violated triangles; at `1/10`
  the best is `(32, 33, 43)` (`0.79°, 0.79°, 29.15°`), points `(1.8215, 1.87087)`,
  `(1.81457, 1.53613)`, `(1.34699, 1.80728)`. (Pulling towards the *triangle’s* centroid
  drops the charge to 1: that direction leaves the pair polygons.)
  The 5-cycle stage was stopped (522,848 cycles at `8^5` combinations).

So the ceiling family is **not** in the rank-1 closure: interior 2-of-3 cuts of
violation `1/4` separate it (EXACT charges); the threshold method is not capped by the
family that caps the point method.
The centroid is the worst place for an atom point: the images that lift the charge past
1 have edges near the *vertices* of the pair polygon.

#### 3.6 Run 3: the combined loop with interior-vertex atoms (`lp-run3`, CHECKED)

Resumed from run 2’s checkpoint with the generator of 3.5 (interior vertex candidates,
cap 24 per pair, every triangle refined for families of `<= 400` placements), 75 min.

| stage | sites (orbits) | atom orbits (active, budget) | rows | objective | dual support | s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| start | 13,721 (1,777) | 1,120 (28, 2.12) | 9,868 | `11.000000000` | 11 | 256 |
| separation: 0 vertices above 1; **450 violated 2-of-3 orbits at charge 1.25**, 400 added (`29-axis-axis` 309, `axis-axis-axis` 66, `29-29-axis` 25) |  |  |  |  |  | 8 |
| iter-0 | 13,721 | 1,520 (26, 2.87) | 9,868 | **`10.926981816`** | 114 | 84 |
| sweep 0: 384 sites + 204 atoms, least charge `0.9248` at direction 131, 543 violated cells |  |  |  |  |  | 76 |
| rows-0-0 |  | 1,520 (28, 2.72) | 10,411 | `10.936984287` | 131 | 98 |
| sweep 1: least charge `0.9521` at direction 173, 543 violated cells |  |  |  |  |  | 59 |
| rows-0-1 |  | 1,520 (24, 2.33) | 10,954 | `11.000000000` | 12 | 72 |
| site separation 1: max depth `1.25` over 28,308 vertices, 152 above 1, +20 orbits; atoms: **1,295 violated orbits, max charge 1.5**, 400 added |  |  |  |  |  | 12 |
| iter-1 | 13,873 (1,797) | 1,920 (31, 2.81) | 10,954 | `10.948525770` | 119 | 80 |
| sweeps 2–4: least charge `0.9345` (dir. 144), `0.9318` (dir. 0), `0.9617` (dir. 125); 486, 432, 543 violated cells |  |  |  |  |  | 73, 107, 128 |
| rows-1-0 / -1 / -2 |  | (35, 2.42) / (35, 2.47) / (45, 2.16) | 11,440 / 11,872 / 12,415 | `10.974868125` / `10.990502229` / `11.000000000` | 139 / 117 / 14 | 120, 133, 237 |
| site separation 2: max depth `1.1875` over 37,512 vertices, 1,132 above 1, +108 orbits; atoms: 3,040 violated orbits (max 1.375), 400 added |  |  |  |  |  | 37 |
| iter-2 | 14,725 (1,905) | 2,320 (28, 2.57) | 12,415 | `10.956243518` | 151 | 131 |
| rows-2-0 / -1 / -2 / -3 (sweeps: least `0.9244`, `0.9682`, `0.9694`, `0.9729`; 537, 444, 249, 267 cells) |  |  | 12,952 / 13,396 / 13,645 / 13,912 | `10.960754578` / `10.965242304` / `10.966348911` / `11.000000000` | 156 / 137 / 157 / **9** | 137, 117, 129, 149 |
| site sep. 3: max depth **`1.5`** over 9,056 vertices, 2,460 above 1, +45 orbits; atoms 246 violated (max 1.5), all added |  |  |  |  |  |  |
| iter-3 | 15,085 (1,950) | 2,566 (44, 2.51) | 13,912 | `10.965931732` | 169 | 119 |

**Reading (shadow prices).** Three full cycles and a fourth dip.
Cuts and sites push the value below 11 (`10.927`, `10.949`, `10.956`, `10.966`); the
rows refill it, slowly at first (`+0.0045`, `+0.0011` per round in cycle 2) and then in
one jump to exactly `11.000000000`, where the dual collapses onto a near-integral family
-- 11, 12, 14, then 9 support rows of total 11, `1.19`–`1.25` deep at vertices no site
samples -- and the cycle restarts with ~100 site orbits, 400 atom orbits and ~1,500 rows
more. The shadow prices at every complete-rows plateau are therefore integral or
quarter-integral on a handful of rows and zero elsewhere: the program is pinned by
*near-packings of eleven cores* whose overlaps are unsampled slivers, each excluded only
after its own slivers get sites and atom points.
Every such family violates interior 2-of-3 cuts by `1/4` to `1/2`, so the threshold
method keeps making progress the point method cannot make (Section 3.3); whether the
dips ever fail to refill -- a threshold certificate -- is OPEN at this budget.
Per cycle: ~15 min on one core.

### 4. Candidate and decision

No threshold-certificate candidate exists yet: the restricted value never went below 11
with complete rows (Section 3). The step is tooled: `freeze_candidate.py` writes the
extended record (`atoms` as today plus `threshold_atoms: [{points, threshold, weight}]`,
weights bumped by `1 + 2e-6` and rounded up at scale `10^9`, orbits expanded,
`total_budget` declared) from a loop checkpoint; `devtools.decide_threshold_certificate`
decides such a file (strict rational parsing; Conditions 1', 2', 3, 4 in closed form;
Condition 5' by the dense grid and the slab sweep, required to agree at every direction;
the least charge re-evaluated at its witness by membership counting; SHA-256). Exercised
on a fixture (rejected at Condition 5', both routes agreeing) and two refusals.
What *was* frozen and decided is the ceiling family of 3.3, which the coordinator should
have verified independently: 88 rational placements, 20,376 rational vertices, exact
membership, one exact sum.

### 5. Deliverables, timings, what failed, next measurement

#### 5.1 Files (repository additions uncommitted; no existing file edited)

- `packing/src/sqpack/fractional/threshold.py`: `ThresholdAtom`, `ThresholdCertificate`,
  `rectangle_terms` (inclusion–exclusion terms on `reduce_to_spans`’s event grid),
  `charge_grid` (dense int64), `sweep_slabs` (same terms slab by slab, `O(V)` memory),
  `charge_grid_direct` (independent count-and-threshold reference), `minimum_charge`,
  `least_charged_cells` / `least_charged_slabs` (row generation), `exact_charge`,
  `closed_form_threshold_conditions`, `verify_threshold`. Ruff and BasedPyright at zero.
- `packing/tests/test_fractional_threshold.py`: 14 tests, 1.7 s -- the expansion
  identity for every `(|S|, k)` up to 7; inclusion–exclusion grid = direct count grid
  cell for cell on random instances (`2-of-3` … `4-of-6`, seven directions); `1-of-1`
  threshold atoms reproduce `sweep.minimum_covered_mass` value and witness; slab sweep =
  dense grid slab for slab; the minimum agrees with membership counting at its witness;
  budgets, refusals, symmetry check, zero-weight atoms leave the point verdict
  unchanged. On the record (`check_retained.py`, EXACT): dense, slab and retained sweep
  agree at all 181 directions of the 1121-atom certificate, least `4001/4000`, 0
  mismatches.
- `packing/devtools/decide_threshold_certificate.py`: decides a frozen threshold
  certificate (Section 4). One exact route, not the retention gate.
- Scratch `spike-b/`: scripts `sep_family.py`, `sepcore.py`, `lp_threshold.py`,
  `lp_threshold2.py`, `dual_anatomy.py`, `sep_ceiling*.py`, `freeze_candidate.py`,
  `check_retained.py`; every log, checkpoint directory and `.txt` reading named above;
  **[`ceiling-family-191-50.json`](ceiling-family-191-50.json)**.

#### 5.2 Timings (one core)

Retained 1121-atom sweep: `0.03`–`0.34` s per direction.
Task 2: 243 / 239 s per family (graph 21, representatives 55, 10 M triangles 110, 2 M
cycles 17–32). Run 1: control LP 31 s, dual geometry 112 s, separation ~250 s, LPs with
600 / 945 atom columns 135 / 157 s. Run 2: 448 s. `verify_ceiling`: 2.1 s.
`sep_ceiling.py`: 22 s; interior variant 11 s per pull.
Retained check: 161 s. Run 3: per-stage seconds in the table of 3.6.

#### 5.3 What failed, and what the numbers do not say

- Run 1 crashed once on a degenerate triangle (two identical mirror images of one
  placement); fixed by merging identical placements.
  Nothing here bounds `s(11)`.
- The brief’s own-weight filter is vacuous on smeared duals, and its pair-centroid point
  choice (Sections 2, 3.1, 3.2) is weak: vertex-near interior points find violations of
  `1/4` to `1/2` where centroids find none.
  The 2-of-5 exhaustive search was not finished.
- `verify_ceiling` is the retained route (float screen, exact arithmetic on 3,675
  vertices near the maximum), not an independent one; the downward-in-`B` transfer (3.4)
  is this report’s three-line proof.

#### 5.4 The next discriminating measurement

1. **Continue run 3’s loop** at 3.82 with more wall-clock (3–15 min per iteration on one
   core); the question is a value below 11 *with complete rows*, which
   `freeze_candidate.py` + `decide_threshold_certificate` then freeze and decide.
2. **Locate `L*`** in `(381/100, 191/50)`, the least side with a total-11 ceiling family
   at `B = 9977/10000`: the exact reach of the point method at this `B`, a one-parameter
   search with the combined loop.
3. **Finer net**: at 360 steps `B` may reach `0.99885`, where the rigid ceiling family
   fails; run the loop with threshold atoms from the start at `(191/50, 0.9985, 360)`.
   **Floor atoms** and shapes beyond `2-of-3` dominate threshold atoms at no extra cost.

## Part 2 — Resume of spike B run 3: rows-only completion at 191/50 and the decision

Scratch: `spike-b/resume/` in the untracked scratchpad, not retained (scratch only).
Scripts beside that report: `rows_only.py` (the rows-only driver), `freeze_candidate.py`
(spike B’s freeze script with one line changed, Section 5), `freeze_and_decide.sh`.
Logs: `lp-run4.log`, `decide-1.log`,
[`lane-b-decide-191-50.log`](lane-b-decide-191-50.log).
State: `lp-run4/` (sites.json, atoms.json, rows.json, x.npy, duals.npy,
trajectory.json). Candidate:
[`lane-b-threshold-candidate-191-50.json`](lane-b-threshold-candidate-191-50.json).
No git state was changed.

### 1. Findings

| # | Finding | Status |
| --- | --- | --- |
| F1 | Run 3’s “ROWS COMPLETE at objective 10.967300462” was declared by a sweep that its own log says was cut “inside row sweep at direction 79”: directions 80-180 were never swept for that measure. | RECORD (`lp-run3.log`) |
| F2 | The full 181-direction sweep of the saved rows-3-4 measure (540 point atoms + 328 threshold atoms, budget 68545631/6250000 = 10.967300960) has least charge 31232339/31250000 = 0.999434848 at direction 114 (about 29.4 deg); 20 cells below 1 - 1e-6, in directions 105, 106 and 114. The record’s completeness claim was false. | CHECKED (`lp-run4.log`, sweep-0) |
| F3 | Two row rounds (+20, then +240 rows; 15,021 rows) leave the LP objective at 10.967300461957 to twelve decimals and reach rows complete: sweep-2 finds no cell below 1 - 1e-6 at any of the 181 directions, least charge 40000001/40000000 = 1.000000025 at direction 0. The rows were absorbed inside the optimal face (9 simplex iterations for the last 240 rows). | CHECKED (`lp-run4.log`, `lp-run4/trajectory.json`) |
| F4 | Frozen candidate (every positive weight times 1 + 2e-6, rounded up at scale 1e9, D4-expanded): 584 point atoms of mass 271052551/31250000 = 8.673681632 and 320 threshold atoms, all 2-of-3, of budget 143352577/62500000 = 2.293641232; total budget 685457679/62500000 = 10.967322864, margin 2042321/62500000 = 0.032677136 below 11. SHA-256 `3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, 673,639 bytes. | EXACT (recomputed by the decide tool from the frozen bytes) |
| F5 | `devtools.decide_threshold_certificate`: Conditions 1, 1', 2', 3 and 4 hold in closed form. | EXACT |
| F6 | Condition 5' holds: least cell charge 100000203/100000000 = 1.000002030 at direction 69 (about 18.0 deg); dense grid and slab sweep agree at every one of the 181 directions (0 disagreements); the charge re-evaluated at the witness placement by membership counting is 100000203/100000000 (agrees). Verdict: **ACCEPTED** (the tool’s wording: one exact route; retention wants an independent verifier). 72.9 s at PACK_JOBS=3. | EXACT ([`lane-b-decide-191-50.log`](lane-b-decide-191-50.log)) |
| F7 | Hence a threshold certificate exists at L = 191/50, B = 9977/10000 on the 181-direction net with total budget 10.967322864 < 11. By spike B’s theorem (its REPORT section 1, restated in the `sqpack.fractional.threshold` docstring) this gives s(11) >= 191/50 = 3.82, past the point-method ceiling `tau*(191/50) >= 11` (EXACT, spike B section 3.3): the 2.29 of threshold budget is what the point method cannot have. The five conditions are decided; the inference and the tool are not yet independently verified, so this is not a retained result. | EXACT conditions; retention OPEN (independent verifier outstanding) |
| F8 | Spike B’s `freeze_candidate.py` writes `provenance.lp_objective` as a JSON float, which the decide tool’s strict parser refuses (`inexact JSON number '10.96730046195726'`) before any condition is checked. Cycle 1 was lost to it; the `resume/` copy writes the field as a string, the only change. The freeze pipeline had never been exercised end to end on a loop checkpoint. | CHECKED (`decide-1.log`); defect |
| F9 | Keeping one HiGHS handle (scipy’s bundled `_Highs`: `passModel` once, `addRows`, re-`run` from the old basis) makes a row round cost 3.5 s and 9 simplex iterations for 240 added rows, against 167 s and 12,658 iterations cold. The sweep (about 35 s on three workers) is now the whole cost of a round. | CHECKED (`lp-run4.log`) |

Timings (wall): reload 1.6 s; matrices 26.6 s (14,761 x 4,516, 31.9 M nonzeros); HiGHS
model pass 8.2 s; sweeps 36.1 / 34.3 / 36.3 s (181 directions, 3 forked workers); LP
167.3 s cold, 3.5 s warm; driver total 319 s of the 90-minute budget.
Freeze 1 s. Decide 72.9 s. From the first read of the brief to the verdict: 13 minutes.

### 2. What was resumed, and how

Run 3 (`lp-run3/`, `lp-run3.log`) stopped at its deadline with 15,085 sites (1,950 D4
orbits), 2,566 threshold-atom orbits (41 active, budget 2.311043), 14,761 rows and
objective 10.967300462. The saved `x.npy` is the rows-3-4 solution: the deadline fell
inside the following sweep, which added no rows, and the “rows-complete” and “final”
checkpoints wrote the same `x`. Reloading the checkpoint (sites regrouped into orbits as
`lp_threshold2.py --resume` does, rows as snapped exact placements, atom orbits in
`atoms.json` order) and rebuilding the coefficient matrix with `cutting.coverage_matrix`
and `sepcore.atom_columns` reproduces the objective 10.967300462 on the saved `x`, so
the reload is consistent (`lp-run4.log`, line “saved x”).

`rows_only.py` then runs only row rounds: no site separation, no atom separation.

1. Round 0 sweeps the saved measure directly: weights rounded up at scale 1e9,
   `threshold.rectangle_terms` and `sweep_slabs` for the least charge of every
   direction, `least_charged_slabs(keep=40, below=1 - 1e-6)` for the violated slab
   minima, each rotated back to a snapped exact row `(direction, x, y)`. These are the
   script’s calls, with `keep` raised from 3 to 40 so that every violated slab minimum
   becomes a row (the largest count seen was 240, so the cap never bound).
2. Each later round appends the rows to the matrix and to the HiGHS handle (`addRows`),
   re-solves from the previous basis, and sweeps again.
3. It stops when a full sweep finds no violated cell, when the objective reaches 11 -
   1e-9, or at the deadline (set to 88 minutes; 5.3 were used).
   A sweep is never interrupted, so the driver cannot repeat F1.

The sweep is the decision-grade primitive; the solver only proposes weights.
The warm-started handle and `scipy.optimize.linprog` (the script’s cold solve) optimise
the same LP; only the re-solve cost differs (F9). Three forked workers sweep the 181
directions and the LP runs on one core; the two phases do not overlap, so the load
stayed within the three-core budget.

### 3. Trajectory

| stage | rows | objective | site / atom support (atom budget) | dual support | least charge (direction) | violated cells (directions) | LP | sweep |
| --- | ---: | ---: | --- | ---: | --- | --- | ---: | ---: |
| saved x (rows-3-4) | 14,761 | 10.967300462 | 74 / 41 (2.311043) | 161 |  |  |  |  |
| sweep-0 |  |  | 540 points + 328 threshold, budget 10.967300960 |  | 31232339/31250000 = 0.999434848 (114) | 20 (105, 106, 114) |  | 36.1 s |
| rows-1 | 14,781 | 10.967300461957 | 78 / 38 (2.287490) | 185 |  |  | 167.3 s, 12,658 it, cold |  |
| sweep-1 |  |  | 576 points + 304 threshold, budget 10.967300952 |  | 496067051/500000000 = 0.992134102 (88) | 240 (1, 88-93, 116-118) |  | 34.3 s |
| rows-2 | 15,021 | 10.967300461957 | 79 / 40 (2.293636) | 185 |  |  | 3.5 s, 9 it, warm |  |
| sweep-2 |  |  | 584 points + 320 threshold, budget 10.967300952 |  | 40000001/40000000 = 1.000000025 (0) | **0** |  | 36.3 s |

The per-direction least charge of every sweep is in `lp-run4/trajectory.json`
(`per_direction`, exact rationals).
Reading: the objective never moved.
The twenty cells of sweep-0 were charged 0.99943-0.99988; satisfying them cost nothing,
but the alternative optimum the solver moved to opened 240 cells in ten directions
(least 0.9921 at direction 88, about 22.9 deg); satisfying those, again at no cost,
closed everything. The optimal face at 10.9673 is wide enough to hold a rows-complete
point, which is why the value stayed below 11, unlike run 3’s three earlier cycles,
where the rows refilled the value to exactly 11.000000000 and collapsed the dual onto a
near-integral family.

### 4. Candidate and decision

Freeze (`freeze_candidate.py` logic: `x.npy` site orbits first, then atom orbits in
`atoms.json` order; every positive weight times 1000002/1000000, rounded up to a
multiple of 1e-9; zero weights dropped; orbits expanded to D4-closed lists;
`total_budget` declared):

- 584 point atoms (79 site orbits), point mass 271052551/31250000 = 8.673681632, largest
  weight 0.074195;
- 320 threshold atoms (40 orbits, every one 2-of-3), threshold budget 143352577/62500000
  = 2.293641232, largest weight 25534197/1000000000 = 0.025534;
- total budget **685457679/62500000 = 10.967322864**, margin 2042321/62500000 =
  0.032677136 below 11; ratio to the LP measure’s budget 1.0000019979 (the bump);
- `id` C-n011-threshold-191-50, L = 191/50, B = 9977/10000, angle limit 207107/500000,
  180 steps (181 directions), symmetry D4; SHA-256
  `3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, 673,639 bytes.

Decision (`uv run --frozen --all-extras --group dev python -m
devtools.decide_threshold_certificate`, `PACK_JOBS=3`;
[`lane-b-decide-191-50.log`](lane-b-decide-191-50.log)):

- holds: Condition 1, 584 point atoms closed under D4;
- holds: Condition 1', 320 threshold atoms closed under D4 (every image present, same
  weight);
- holds: Condition 2', 271052551/31250000 + 143352577/62500000 = 685457679/62500000
  against n = 11;
- holds: Condition 3, final half-tangent 207107/500000, t^2 + 2t - 1 =
  309449/250000000000;
- holds: Condition 4, B(1 + D) = 899996306539/900000000000 with D = 207107/90000000;
- holds: Condition 5', least cell charge 100000203/100000000 = 1.000002030 at direction
  69, dense/slab disagreements 0, witness membership charge 100000203/100000000
  (agrees). The witness centre is printed in
  [`lane-b-decide-191-50.log`](lane-b-decide-191-50.log) as an exact rational in the
  rotated frame (a 400-digit numerator: the cell midpoint of an event grid built from
  1,544 atom points).

Verdict: **ACCEPTED (one exact route; retention wants an independent verifier)**; 72.9
s.

Cycles used: two of the three allowed.
Cycle 1 (`decide-1.log`; that record’s SHA-256 was
`f10d0897eb2851ca885e553a6c334c7a5bc1924cfbd94495c9651175c832de9d`) was refused at
parsing (F8) and decided nothing; cycle 2 is the first mathematical decision of a
candidate from the loop, and it needed no further row round.

Consistency with the ceiling: spike B’s section 3.3 proves (EXACT) that no D4-symmetric
point measure of mass below 11 satisfies Condition 5 at this L, B and net.
The accepted candidate carries 2.29 of threshold budget in 2-of-3 atoms, which the
ceiling’s weak duality does not bound (section 3.5 showed the ceiling family violates
such cuts by 1/4). The two facts are compatible and together locate the gain in the
threshold atoms.

### 5. What failed

- Run 3’s completeness claim (F1, F2). `lp_threshold2.py` checks its deadline inside the
  direction loop and then reports the partial sweep’s `least` and `new_rows` as if they
  were complete; with no violated cell among directions 0-79 it printed “ROWS COMPLETE”.
  The fix is one line (a sweep that breaks on the deadline must not declare
  completeness); `rows_only.py` never breaks inside a sweep.
- The freeze record was unreadable by the decide tool (F8). `freeze_candidate.py` wrote
  `provenance.lp_objective` as a JSON float; `decide_threshold_certificate.load` refuses
  every inexact number in the file, provenance included.
  The `resume/` copy writes `lp_objective_float` as a string;
  `diff ../freeze_candidate.py freeze_candidate.py` is that line plus the `tool` label.
  Spike B’s REPORT section 4 said the tool had been “exercised on a fixture”; the
  fixture carried no provenance.
- Nothing else: no LP failure, no route disagreement, no memory pressure.
  A pipeline check that froze the run-3 (rows-3-4) measure before the loop ran was
  deleted after use; it was never decided and is superseded by the accepted record.

### 6. Next discriminating measurement

1. An independent verifier for threshold certificates, the retention gate the decide
   tool itself names. `charge_grid_direct` (one count grid per atom, thresholded) exists
   as the test-level route; a standalone verifier in the style of
   `packing/cases/n11_fractional_certificate/`, reading the frozen bytes and deciding
   Condition 5' by exact membership on the event cells without `sweep.py`, closes the
   gap between “ACCEPTED (one exact route)” and a retained entry for s(11) >= 3.82. The
   theorem itself (spike B section 1) should be reviewed alongside.
2. Push the side. A rows-only round now costs about 40 s. Spike B’s combined loop at
   383/100 or 385/100 from this site and atom set, with a deadline-safe completeness
   check, measures whether the threshold method reaches past 3.82; the method’s cap is
   3.869 (brief) and the ceiling family is wall-tight, so B and the net can be pushed as
   well.
3. Record the two defects (F1’s premature “ROWS COMPLETE”, F8’s float provenance) in
   `packing/defects.yaml` when the coordinator integrates, with these logs as evidence.

## Files

Retained in this directory:

- [`lane-b-threshold-candidate-191-50.json`](lane-b-threshold-candidate-191-50.json) —
  673,639 bytes, SHA-256
  `3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, re-hashed after
  the copy from the spike’s `resume/threshold-candidate-191-50.json` and matching the
  hash Part 2 F4 records.
  The frozen candidate: 584 point atoms of mass `271052551/31250000`, 320 `2-of-3`
  threshold atoms of budget `143352577/62500000`, total budget
  `685457679/62500000 = 10.967322864` at `L = 191/50`, `B = 9977/10000`, 181 directions,
  `D4`.
- [`lane-b-decide-191-50.log`](lane-b-decide-191-50.log) — 3,858 bytes, the spike’s
  `resume/decide-2.log`: `devtools.decide_threshold_certificate` over those bytes, its
  verdicts for Conditions 1, 1', 2', 3, 4 and 5', the Condition 5' witness centre as an
  exact rational, and the ACCEPTED verdict with its one-exact-route wording.
- [`ceiling-family-191-50.json`](ceiling-family-191-50.json) — retained here before this
  lane and byte-identical to the spike’s `spike-b-ceiling-family-191-50.json` (14,039
  bytes, SHA-256 `95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427` on
  both), so no second copy was made.

Not retained (scratch only).
The large ones, by size:

- `sep-unit127.json`, 75,020,589 B — the separation output on the unit control family
  behind Part 1 §2 (52,088 violated `2-of-3` atoms in 6,471 orbits, plus the 5-cycle
  stage).
- `resume/lp-run4/`, 16,397,983 B, and `lp-run3/`, 16,295,283 B — loop checkpoints
  (`sites.json`, `atoms.json`, `rows.json`, `x.npy`, `duals.npy`, `trajectory.json`);
  `lp-run4/trajectory.json` carries the per-direction least charge of every sweep in
  Part 2 §3.
- `sep-b19150.json`, 5,153,703 B — the same separation output on the `191/50` family
  (3,504 violated atoms in 438 orbits).
- `lp-run2/`, 3,945,652 B, and `lp-run1/`, 1,645,715 B — the earlier checkpoints.
- `lp-run1-atoms-seed.json`, 1,215,538 B — run 1’s atom columns.

And the rest: the scripts `sep_family.py`, `sepcore.py`, `sep_ceiling.py`,
`sep_ceiling_interior.py`, `lp_threshold.py`, `lp_threshold2.py`, `dual_anatomy.py`,
`freeze_candidate.py`, `check_retained.py`, and in `resume/` `rows_only.py`, its
one-line-changed `freeze_candidate.py` and `freeze_and_decide.sh`; the logs and readings
`sep-b19150.log`, `sep-unit127.log`, `lp-run1.log`, `lp-run1-crashed.log`,
`lp-run2.log`, `lp-run3.log`, `lp-run4.log`, `decide-1.log`, `check-retained.log`,
`sep-ceiling.log`, `sep-ceiling-interior.log`, `ceiling-depth-vs-B.txt`,
`ceiling-verdict-run2-iter0.txt`, `dual-anatomy-run2-start.txt`,
`dual-anatomy-run2-iter0.txt`, `top-atom-exact.txt`; and the three parser fixtures
`fixture-threshold.json`, `fixture-bad-dup.json`, `fixture-bad-float.json`.

The library and tools the two parts describe are in the repository rather than in
scratch: `packing/src/sqpack/fractional/threshold.py`,
`packing/tests/test_fractional_threshold.py` and
`packing/devtools/decide_threshold_certificate.py`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
