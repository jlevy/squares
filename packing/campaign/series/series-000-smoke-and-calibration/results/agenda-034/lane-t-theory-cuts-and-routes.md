# Agenda 034, lane T: what the certificate language can and cannot do past 3.82

Retained analysis-lane report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by a
Fable sub-agent at maximum effort on 2026-09-09 under the breadth survey the owner
requested. Read-only on the repository; its four scripts and their outputs ran from the
untracked scratchpad and are reproduced in the appendix so every number can be
recomputed. The report is reproduced as delivered, with its own status labels; X-023
carries the coordinator’s reading of it.
Nothing here is a registered round or a new bound.
The ceiling family this lane asked for (M0 of its plan) was produced by spike B and
replayed by the coordinator; see X-023.

Labels: PROVED (proof here), EXACT (rational decision by repository primitives), CHECKED
(float script retained), RECORD (retained file), PLAUSIBLE, SPECULATIVE, OPEN.

Notation. `L` side, `n = 11`, `U = 3.877083590`. `Λ_B^N(L)` = closed `B`-squares at the
`N`-step half-tangent net inside `[0,L]²`; `Λ°(L)` = open unit squares at *all* angles;
`Λ_1^N(L)` = closed unit squares at net angles.
`τ` = covering value, `ν` = fractional packing value (pointwise depth ≤ 1), `ν_int` =
max pairwise-disjoint members.
`D_N` = largest half-gap tangent, `D_N ≈ tan(π/8)/N`
(`D_180 = 207107/90000000 = 0.0023012`). A *k-fold packing* is a family with every point
in ≤ `k` members; `N_k(L)` its largest size.

## 0. Findings in one page

| # | Finding | Status |
| --- | --- | --- |
| F1 | **Sandwich.** `τ_1^N(L) ≤ τ°(L) ≤ τ_B^N(L) = τ_1^N(L/B)` for every `B(1+D_N) < 1`. Every sound one-body core rule (concentric, non-concentric, kernel, octagon, parent domain, open cores, continuum angles) has value `≥ τ°(L)`. So *all* core-choice ideas together are worth at most the growth of `τ_1^N` over the tax interval `[L, L/B]`, of length `L·D_N`: `0.0088` at 3.82 (`N=180`), `0.0022` (`N=720`), `0.0004` (`N=4000`). Net refinement dominates them all. | PROVED |
| F2 | **Direction-dependent atom weights never help**: `w_s(θ)` is dominated by `max_θ w_s(θ)` (same budget, weaker constraints). Only *count* conditioning (X-014 Lemma 3) can use angle, and the record shows it degenerates (`w₀ ≈ w₁`). | PROVED |
| F3 | **The plateau premise is unproved from the primal side.** Record: `10 ≤ ν_B(3.82) ≤ 11.0556`; the lower bound is the trivial ten-packing (`s(10) = 3.707 < 3.82·B`, cores at net directions by Condition 4); the retained families (`9.908` at 3.82, `10.384` unit at 3.84) are *below* it. Nothing exact says `ν* ≥ 11` anywhere below the cap `3.8690`. If `s(11) > 3.84` (conjectured) then `ν_1(3.84) − ν_int(3.84) ≥ 0.384` is a real integrality gap, witnessed by the retained unit family. | RECORD; PROVED (conditional) |
| F4 | **`ν* = sup_k N_k/k`.** A witness of `ν*(L) ≥ 11` is a `k`-fold packing of `11k` squares. A half-integral witness (`k=2`, 22 squares) with no 11 pairwise-disjoint members contains an odd cycle, and one rank-1 threshold atom `(S,2)` on that cycle cuts it. The threshold-atom spike is exactly the right tool for a 2-fold plateau; nothing guarantees it for `k ≥ 3`. | PROVED |
| F5 | **Clique cuts are rank-1 threshold atoms iff the clique’s fractional piercing number `τ*(C) < 2`.** Non-Helly triples: yes (`τ* ≤ 3/2`). Corner-triangle cliques and all Helly cliques are already point constraints (lane A: every square meeting `x+y ≤ d` contains `[d,1]²`), which is *why* corner boxing buys one integral unit and no more. Large non-Helly cliques: OPEN; test on Caoduro–Sebő’s 9-square clique (`τ = 3`). | PROVED / OPEN |
| F6 | The verified `10.384` family at `96/25` violates **no** clique, odd-hole (`C₅`), line-capacity or class-count cut; its heaviest non-Helly clique (17 placements at a corner) carries `0.920 < 1`; its heaviest wall line carries `2.85 < 3`. Structure: corners `0.71` each, wall slots `0.74` each, `1.75` slightly-tilted near-wall alternatives, four inner-corner clusters of `21°–42°` squares (`≈0.6` each, peak `29°`) at radius `0.76–0.80` from the centre, a `0.3` central pinwheel; no axis square near the centre. | CHECKED |
| F7 | **Sound `B = 1` formulation**: open cores, condition on `int Q`, decided per direction by the retained integer sweep with each atom’s cell-index box shrunk by one on the low side and the minimum taken over cells, edges and vertices; the direction continuum then needs either interval boxes in `θ` (the kernel) or, equivalently, net-plus-shrink. There is no separate continuum route; it is the `N → ∞` limit of the retained one and buys `≤ L·D_N`. `B = 1` exactly is needed only for the endpoint run (`σ < 6.6·10⁻⁶`, lane D). | PROVED |
| F8 | Fastest decisive measurements: fixed-support polisher (exact optimum on the 768 support at 96/25 and 191/50), a 2-fold packing search with exact `verify_ceiling` at weight 1/2, the `(S,k)` atom loop at 3.82, then row completion at 61/16 and `N = 720` at 3.82. Each has a stated kill (§6). | plan |

## 1. Three lemmas the rest rests on

**Lemma 1 (sandwich; core-choice cap).** Let `B(1+D_N) < 1`. Then
`τ_1^N(L) ≤ τ°(L) ≤ τ_B^N(L) = τ_1^N(L/B)`, and for any sound rule `Q ↦ core(Q) ⊂ int Q`
(any shape, position, angle dependence) the program “`μ(core(Q)) ≥ 1` for all admissible
unit `Q`” has value `τ_rule(L) ≥ τ°(L)`. All values are non-decreasing in `L`.

*Proof.* (i) A measure feasible for `Λ_B^N(L)` covers `int Q` for every admissible unit
`Q`: `int Q` contains a closed `B`-square at the nearest net angle (Condition 4,
`B(cos δ + sin δ) ≤ B(1+D) < 1`) whose centre is admissible because it lies in
`Q ⊂ [0,L]²`. So `τ° ≤ τ_B^N`. (ii) `μ(Q) ≥ μ(int Q)` and net angles are angles, so
`τ_1^N ≤ τ°`. (iii) Scaling by `1/B` maps `Λ_B^N(L)` onto `Λ_1^N(L/B)`, preserving `D4`
and the net. (iv) `core(Q) ⊂ int Q` gives `μ(int Q) ≥ μ(core(Q))`; soundness of a rule
needs `core(Q) ⊂ int Q` (else touching squares double count), so this covers every sound
rule, the note’s octagon and parent domain included.
(v) Monotonicity: a measure at `L' > L` restricted to the corner sub-container covers
everything inside it.
∎

*Consequence.* The retained method with net `N` proves `s(11) ≥ L` iff
`τ_1^N(L/B_N) < 11`. Any one-body improvement proves at most `s(11) ≥ L` with
`τ°(L) < 11`, and `τ°(L) ≥ τ_1^N(L)`. The whole family of core-choice ideas is bounded
by the mass growth of `τ_1^N` over `[L, L/B_N]`; in side terms `≤ L·D_N`, which net
refinement also delivers.

**Lemma 2 (direction-dependent weights).** If atom `s` charges `w_s(θ)` to cores at
direction `θ`, the counting budget is `Σ_s max_θ w_s(θ)` (each atom lies in at most one
of the disjoint cores, which has some direction).
Replacing `w_s(θ)` by `max_θ w_s(θ)` keeps the budget and raises every covered mass.
∎ (Q4c refuted.)

**Lemma 3 (k-fold packings; half-integral witnesses).** (a) For the finite-net program
`ν(L) = max_k N_k(L)/k`; for the continuum, `sup`. (b) Let `F` be 22 placements with
`y ≡ 1/2` depth-feasible and no 11 members pairwise disjoint.
Then the intersection graph `G(F)` has an odd cycle `C`, and the atom `(S,2)` with `S` =
one point in each intersection of consecutive members of `C` charges every member of `C`
and has budget `⌊|C|/2⌋ < |C|/2 = Σ_C y`.

*Proof.* (a) A `k`-fold packing of size `N` gives `y = 1/k`; an LP optimum with rational
data has denominator `k` and is a `k`-fold multiset.
(b) A bipartite `G(F)` has a colour class of `≥ 11` pairwise disjoint members.
Each member of `C` contains its two incident points of `S`; disjoint cores contain
disjoint parts of `S`, so at most `⌊|S|/2⌋` of them contain two points.
∎

*Reading.* A 2-fold witness of the plateau is either an integral kill (11 disjoint
cores) or is cut by one rank-1 odd-cycle atom.
A `k`-fold witness with `k ≥ 3` can still violate `(S,2)` atoms (up to `⌊k|S|/2⌋`
members may contain two points of `S`) but need not; the CG rank required grows with the
denominator. **The denominator of the optimal dual at 3.82 is the single best predictor
of whether spike (ii) can close the plateau.**

## 2. Q1 — threshold atoms as Chvátal–Gomory cuts

**(a) Language.** An atom `(S,k)` with `S` a finite weighted point set (measure `λ`),
charge `⌊λ(P)/k⌋` (dominates the indicator `[λ(P) ≥ k]`, same soundness proof) and
budget `⌊λ(S)/k⌋` is exactly the rank-1 CG cut of the point-depth system with
multipliers `λ/k`: valid for every family of pairwise disjoint closed cores
(`Σ_i λ(P_i) ≤ λ(S)`, integrality).
PROVED. Verification is the retained integer sweep on `λ`’s prefix-sum grid, one grid
per `S`, thresholded per cell.

*Cliques.* For a clique `C` the inequality `Σ_C y_P ≤ 1` is a rank-1 atom iff some `λ`
has `λ(P) ≥ 1` on `C` and `λ(S) < 2`, i.e. iff `τ*(C) < 2`; then the rounded cut has
coefficient `≥ 1` on `C`, RHS `1`, and charges only cores containing a point of
`supp λ ⊂ ⋃` pairwise intersections, hence only cores meeting a member of `C`. Non-Helly
triples: `λ = 1/2` on the three pairwise points.
PROVED. General cliques of rotated unit squares: `τ(C) ≤ 6` (Caoduro–Sebő Lemma 1 at the
leftmost centre), and a 9-clique with `τ = 3` exists (their Theorem 2); whether
`τ*(C) < 2` always holds is OPEN. **Falsifier:** the LP `τ*` of that 9-clique; `≥ 2`
means some clique cuts need rank 2 (nested thresholds).
Infinite cliques: all cores containing a point are the point constraint; all cores
meeting the corner triangle `x+y ≤ d` contain `[d,1]²` (lane A), so that clique is the
point constraint at `(d,d)` — already in the LP, which is why lane D and the family here
find `0.96–1.02` of weight per corner.
PROVED.

**(b) Known gap results.** For axis-parallel rectangles the point LP *is* the clique LP
(Helly); the 2026 Wegner counterexamples (Ajwani–Gajjala–Raman–Ray: 64 triangle-free
rectangles, `ν = 16`, `τ ≥ 32`, LP gap `≥ 5/2 − ε`, `≤ 3` on triangle-free; Bal: 64
rectangles, gaps up to `5/2`) are therefore *odd-cycle* gaps of the point LP, not clique
gaps.
Axis-parallel unit squares: `τ ≤ 2ν−1`, so `ν*/ν ≤ 2`, and `C₅` gives `ν*/ν = 5/4`.
Rotated unit squares: only `ν ≤ ν* = τ* ≤ τ ≤ 6ν`, with the non-Helly triple giving a
local `3/2`; nothing bounds `ν*/ν` for the family “all unit squares in a square
container”.
Instance facts: the near-axis class `[0°, 6.45°]` at `q` has fractional value
`9.006` vs integral `9` (lane B) — no gap without tilt; the family’s `0.384` excess
appears only with the `21°–42°` inner-corner clusters.
RECORD/CHECKED.

**(c) Where cuts bite at 3.82; is `0.06–0.1` plausible?** Ranked by the structures an
optimal dual would push over capacity: (1) odd cycles through {wall-slot square,
inner-corner tilted square (two mirror choices per corner), central pinwheel square,
adjacent wall’s inner-corner square} — the `(S,2)` atoms of Lemma 3 remove a
half-integral excess entirely; (2) non-Helly corner cliques {corner square, `5°–10°`
near-corner squares, `29°` inner-corner square, `45°` wall square}: 17 placements at
`0.920` of capacity `1`, no common point — rank-1 iff their `τ* < 2`; (3) wall-line
capacity (§2d), the line `y = 0.51` at `2.85` of `3`; (4) class-count resources — slack
(`7.5` in `[0°,12.5°)` vs `10`); (5) corner boxes/triangles: zero.
Prediction: PLAUSIBLE `≥ 0.05` if the optimal dual at 3.82 is half-integral or its
polished family has heavy odd cycles of length 3 or 5; PLAUSIBLE `≤ 0.01` if
denominators are `≥ 3` and every heavy clique is Helly.
No honest number without the witness (§6 M0–M2).

**(d) Rungs, priced.**

| Rung | Charge | Budget | Sound by | Verifiable by | Cost |
| --- | --- | --- | --- | --- | --- |
| `(S,k)` finite weighted | `⌊λ(P)/k⌋` | `⌊λ(S)/k⌋` | disjointness + integrality | retained integer sweep, one extra grid per `S` | trivial |
| odd cycle 2-of-`(2m+1)` | same, `S` = consecutive pair points | `m` | same | same; separation = shortest odd cycle in the weighted support graph | trivial |
| weighted majority `λ(P) > λ(S)/2` | indicator | `1` | same | same | trivial |
| rank-2 (thresholds of sums of rank-1 charges) | `⌊Σ_j a_j c_j(P)/k⌋` | `⌊Σ_j a_j b_j/k⌋` | iterate | same sweep, bookkeeping | trivial |
| density: chord `≥ c` on a segment `σ` | indicator | `⌊len(σ)/c⌋` | disjoint chords | chord is piecewise linear in the centre → sublevel polygons per direction, exact rational, **new engine** | days |
| area: `area(P ∩ R) ≥ a` | indicator | `⌊area(R)/a⌋` | disjoint areas | piecewise quadratic; interval route only | weeks; weak (`⌊1/(1/2)⌋ = 2` for a corner box of true capacity 1) |
| class counts (lane B) | `⌊μ_Θ(P)⌋` | `⌊M_Θ⌋` | CG on the class measure | sweep on `μ_Θ`’s atoms | free; PROVED here |
| pair resources / 2-point SDP | `r(P,Q)` on disjoint pairs | — | joint depth | a 4-parameter sweep per direction pair (`~10⁵² × 181²` cells) or an SDP with rigorous rounding | months; not exact-verifiable with current machinery |

## 3. Q2 — the shrink-free route

**Sound `B = 1` formulation.** Atoms `μ ≥ 0`, `D4`-invariant.
Condition 5°: for every `θ ∈ [0, π/4]` and centre `c ∈ [h(θ), L−h(θ)]²`,
`μ(int Q(c,θ)) ≥ 1`. Condition 2: `μ(total) < 11`. Proof: interiors of a packing’s
squares are pairwise disjoint open sets, so `11 ≤ Σ μ(int Q_i) ≤ μ(total)`. No shrink,
no net; touching is handled because interiors are disjoint.
Closed cores at `B = 1` are unsound (an atom on a shared edge counts twice).

**Deciding 5° at one rational direction, exactly.** `f(c) = μ(int Q(c,θ))` is a sum of
indicators of open boxes: lower semicontinuous, constant on the open cells, open edges
and vertices of the event arrangement, so its minimum over the closed domain is attained
on that stratification.
At vertex `v_{ij}` an atom counts iff its closed box contains all four adjacent cells,
i.e. its cell-index box `[a,b]×[a',b']` has `i ∈ [a+1,b]`, `j ∈ [a'+1,b']`: the retained
prefix-sum sweep with every atom’s index box shrunk by one on the low side, in one or
both axes (edges, vertices); domain edges and corners join the event coordinates.
Four sweeps per direction, same integer arithmetic.
PROVED.

**The direction continuum.** For an angle box `[θ−δ, θ+δ]`, `int Q(c,θ') ⊇ int K_δ` with
the kernel `K_δ = ⋂ Q(c,θ')` = intersection of the two extreme squares clipped by the
disc of radius `1/2` (the disc constraint is `O(δ²)`; numerically identical to six
digits, `tax_and_kernel.out`). `K_δ` contains the closed `1/(cos δ + sin δ)`-square at
the centre angle, so the interval decision over `θ` *is* the per-cell shrink
(`adaptive.py`). An exact decision over all `θ` would need algebraic event angles; the
practical one is interval boxes in `(c,θ)` (`interval.py`’s method), whose failure mode
is a stalled box at a tie.
There is no third route.

**Quantification.** Tax `L·D_N` at 3.82: `0.0088` (`N=180`), `0.0044` (360), `0.0022`
(720), `0.0011` (1440), `0.0004` (4000); the same within 1.5% near `U`; caps `U·B_N` =
`3.8682, 3.8726, 3.8749, 3.8760, 3.8767` (Trump’s angular offset adds `< 0.001`). The
kernel at `N=180` recovers `50.1%` of the lost *area* (`0.997709` vs `B² = 0.995413`),
so at best half the tax — what `N = 360` gives with existing code.
Verification is linear in `N`: the retained sweep took `3764 s` at 181 directions
(`net-coarsening-381-100.json`; the claim file quotes `~1 s/direction` for the minimal
verifier), so an exact decision costs `12 min – 4 h` at `N=720` and `1 – 23 h` at
`N=4000` on one core; LP row generation scales the same way.

**Does the continuum reach farther in practice?** No.
By Lemma 1 its advantage over the net-`N` shrink is at most the mass growth of `τ_1^N`
over `0.0004` of side at `N=4000`, and it adds a new soundness surface.
`B = 1` matters only at the endpoint: lane D’s equality run needs `L₁ − U < 6.6·10⁻⁶`,
below any finite net’s tax (`0.0002` at `N=8000`). Recommendation: refine the net
(`N=720` first); keep the open-core sweep for the endpoint.

**A prediction worth testing.** In unit terms the 3.82 plateau says
`τ_1^{180}(3.8288) ≈ 11` (site readings `11.00–11.07` are upper bounds) while
`τ_1^{180}(3.8188) ≤ 10.86` (T-018). If `τ_1` grows roughly linearly (slope `≥ 14` per
unit side), at `N=720` the certificate at 3.82 asks whether `τ_1^{720}(3.8222) < 11`,
interpolating to `≈ 10.91`, minus the finer net’s extra angular constraints (unknown
size). So refinement alone may certify 3.82 (PLAUSIBLE, coin flip); in general it
converts a plateau at unit side `L_u` into a bound `≈ B_N·L_u`, up to `+0.0084` over the
3.82 reading. Kill: the converged value at `N=720` on BC-200’s sites plus vertices stays
`≥ 11`.

## 4. Q3 — the integrality gap from the primal side

**What the record establishes.** `ν_B(3.82) ≥ 10` (the `s(10)` packing scaled into 3.82
contains ten disjoint `B`-cores at net directions by Condition 4), `ν_B(3.82) ≤ 11.0556`
(row-converged site measure, float tolerance), `ν_1(96/25) ≥ 10.3842` (EXACT). The
retained families are *below* the trivial integral ten.
The only exact gap statement is conditional: if `s(11) > 3.84` then
`ν_1(3.84) − ν_int(3.84) ≥ 0.384`. So the primal question is “is there any witness at
all”, and F4 says what it must look like.

**Structure of the 10.384 family** (`family_structure.out`, `clique_scan.out`; 768
placements, 93 `D4` orbits, top 40 carry `8.99`):

- Angle: `6.54` in `[0°,2.5°)` (`4.28` at exactly `0°`), `0.23` in `[2.5°,7.5°)`, `0.71`
  in `[7.5°,12.5°)` (`9.47°` squares at `(0.60, 3.20)` near corners), `0.40` in
  `[20°,25°)`, `1.62` in `[25°,30°)`, `0.28` in `[30°,32.5°)`, `0.22` in
  `[38.2°,42.2°)`, `0.19` in `[42.2°,45°]`.
- Position: flush (gap `< 0.01`) `5.82`; near (`< 0.1`) `1.75`; interior `2.82`. Corner
  squares `2.86` (`0.71` per corner); wall-slot squares at `y ∈ {1.51, 2.33}` `≈ 2.96`
  (`0.74` per wall) — *less than the integral 8 the ring holds*; the tilted weight sits
  in four inner-corner clusters at radius `0.76–0.80` from the centre (`29.4°` at
  `(1.33,1.40)` and its mirror `(1.40,1.33)`, `21°–42°` variants) and a `0.3` pinwheel
  at radius `0.30–0.36`; no axis square within `0.56` of the centre.
- Why `29°`: three squares at tilt `θ` stack vertically in height
  `2/cos θ + cos θ + sin θ` (offset `d` needs `d cos θ ≥ 1`); at 3.82 this fits for
  `θ ≤ 34.5°` (`3.646` at `29°`, slack `0.17`; `4.03` at `40.18°`). The dual’s `29°` is
  a sliding three-column between the wall slots — worth 3 integrally like an axis
  column, fractionally useful because the slack lets it overlap the slots and the
  pinwheel. CHECKED arithmetic; interpretation PLAUSIBLE.
- Cuts on this family: non-Helly triples among the heaviest 150: `3060`, max sum
  `0.2625` (all of the shape corner `0.149` + wall `0.084` + `1.05°` square dipping into
  both); chordless 5-cycles among the heaviest 120: `45200`, max sum `0.524` vs budget
  `2`; max-weight interior-overlap clique (heaviest 300): `0.9203`, 17 members at corner
  `(3.33,0.51)`, no common point; wall line `y=0.51`: chord-`≥1` weight `2.8505` vs `3`;
  diagonal and `±29°` lines `0.96` vs `1`; depth line-integrals never exceed length
  (sanity). Nothing is violated, as it must be for a family below 11.

**Resource families to cut a witness, ranked:** (1) odd-cycle `(S,2)` atoms on slot →
inner-corner tilted → pinwheel → adjacent inner-corner → slot, and corner → slot →
tilted-dip → corner; (2) non-Helly corner cliques (the 17-clique); (3) wall-line
chord-`≥1` atoms, budget 3 per wall; (4) class-count resources; (5) nothing from corner
boxes. This is also the separation order for spike (ii).

## 5. Q4 — candidates judged, and new directions

**(a) Non-concentric canonical cores.** REJECT: any sound rule is capped by Lemma 1 at
the tax; concretely it shrinks the admissible centre domain by at most
`(1−B)/2 = 0.00115` per side beyond the parent-feasible domain.
Kill already fired.

**(b) Angle-adaptive kernels.** REJECT as a side mechanism (same lemma; `50.1%` of lost
area ⇒ `≤ 0.0044` of side, free at `N=360`). The kernel is the right *object* for the
endpoint interval decision (F7).

**(c) Direction-dependent weights.** REFUTED (Lemma 2).

**(d) `D2` measures with a spanning case split.** REJECT for the square bound: `D4`
averaging preserves feasibility and mass of the unconditional program (X-019), so
asymmetry cannot lower its value; the robust spanning premise gives only “some square
within `0.0056` of each of two opposite walls”, whose Lemma-2 box has `I_b = ∅`, so by
Lemma D the conditional value equals the unconditional.
Rectangle no-fit theorems (lane D S1) are a `D2` problem and a new result type, but a
packing in `[0,L]²` also fits `L × L`, so they never feed the square bound.

**(e) E.4 segments + corner-pair containment + atoms.** REJECT as a certificate
mechanism, ACCEPT only as a branching rule.
Each E.4 mark has capacity `≥ 4` (two axis squares touching a segment’s endpoints from
each side), so the pigeonhole cut `Σ_{P meets mark_i} y_P ≤ cap_i` is slack, and “every
square meets a mark” constrains placements, not `y`. Corner-pair containment is Lemma 1
(tight cores) read on four atoms; conditioning on “some core contains atom `a`” has
`I_b = {a}`, which the measure already weights, so Lemma 2 returns the unconditional
program. PROVED.

**(f) Certify the plateau from below.** ACCEPT, in two forms cheaper than a hand
construction: the fixed-support polisher (M0) and the 2-fold packing search (N1).

**(g) Upper-bound side.** SPECULATIVE, low (`< 5%`): the fractional structure is a
`k`-fold packing that cannot be unfolded (its overlap graph has an odd cycle by Lemma
3b, else 11 disjoint unit squares would sit at side `L/B`), so it is not evidence of a
packing below `U`; the `29°` signal is the sliding three-column arithmetic, worth 3
integrally; Trump’s pose is locally isolated (exp-013) and every search lands on it.
One cheap test: if a 2-fold witness at `L ∈ [3.84, U)` has an approximate 2-colouring
whose classes overlap only slightly, scale each class up — an “unfolding” packing search
seeded by the LP.

**New directions (not in the note, not restating a lane):**

- **N1. `k`-fold packing witness search.** `ν* ≥ 11 ⟺ N_k ≥ 11k` for some `k`; anneal 22
  unit squares in `[0, L/B]²` with a triple-overlap penalty; verify hits with
  `verify_ceiling` at weights `1/2` (`unit` regime).
  A hit at `L` proves, EXACT, that no one-body certificate exists at `L` for any
  `(B, net)`, and its odd cycles name the cuts.
  Cost: hours, one core.
  Kill: no hit at `3.88` (two Trump copies exist there) ⇒ tool inadequate; hits only
  above the plateau side ⇒ plateau still open.
- **N2. Wall-line density atoms.** Charge cores with chord `≥ 1` on `y = ε`; budget
  `⌊L⌋ = 3` per wall; sound by disjoint chords; exact via sublevel polygons.
  Worth whatever the optimum’s wall usage exceeds 3 (family at `95%`). Kill: the
  polished optimal family keeps every wall line `≤ 3`.
- **N3. Lane B’s counts as CG resources** (§2d): free, zero soundness risk, same sweep.
  Kill: the optimal family’s class weights stay below the counts (the current one: `7.5`
  vs `10`).
- **N4. Denominator diagnostic.** Read the denominator and odd girth of the optimal dual
  at 3.82 (BC-200 state re-solved with vertex constraints): half-integral with heavy
  triangles/5-cycles ⇒ spike (ii) closes it (Lemma 3b); denominators `≥ 3` with Helly
  cliques ⇒ rank-1 will not; budget rank-2 or stop.
- **N5. Net refinement as plateau-to-bound converter** (§3): a plateau at unit side
  `L_u` becomes a bound `B_N·L_u`; `N=720` quarters the tax at `4×` LP cost.
  Kill: value `≥ 11` at `N=720` on the same sites.
- **N6. Open-core index-shrunk sweep** (F7): build only when a cut-strengthened ladder
  reaches `3.87`.

## 6. Q5 — a day of four cores, in order

| # | Measurement | Cores × h | Lets us claim | Kills |
| --- | --- | --- | --- | --- |
| M0 | Fixed-support polisher: max `Σy` on the 768 support at `96/25` (unit) and `191/50` (`B`-cores), exact depth `≤ 1` at all arrangement vertices, by working-set LP (768 vars, `~10⁴` near-tight rows) + exact recheck until no vertex exceeds 1 | 1 × 2 | the exact fixed-support optimum `ν_S ∈ [10.384, 11]`; if `ν_S ≥ 11`: **no unconditional one-body certificate at that side for any `(B,net)`** (EXACT, `ceiling.py` unit regime); capture designs also die if outside weight `≥ 1` (D2) | `ν_S < 10.6`: support too small; nothing about the plateau |
| M1 | `τ*` LPs of the 17-clique found here and of Caoduro–Sebő’s 9-clique (Fig. 14: three squares on a triangle’s sides plus six small shifts) | 1 × 1 | whether every clique cut needed at 3.82 is rank-1 (`τ* < 2`) | `τ* ≥ 2`: rank-2 atoms needed for cliques |
| M2 | 2-fold packing search (N1) at unit sides `3.8288, 3.84, 3.86, 3.88`, seeded from the 40 heaviest orbits and from two Trump copies; exact `verify_ceiling` on hits | 1 × 3 | a hit at `L`: `ν_1(L) ≥ 11` EXACT, plateau real at `L`, odd cycles listed; smallest hit side vs `3.8690` | no hit at `3.88`: tool inadequate; hits only `≥ 3.86`: 3.82 still open |
| M3 | `(S,k)` atom loop at `191/50` from BC-200’s state: polish (M0), separate odd cycles and non-Helly cliques on the support graph, add resource columns (cost `⌊λ(S)/k⌋`), re-solve with row generation; exact integer sweep with atom grids on any candidate `< 11` (interval route stays sound: the charge is monotone in the atom set) | 2 × 6 | a certificate at 3.82 (`s(11) ≥ 3.82` after the two-route gate) or “rank-1 atoms leave BC-200’s sites at `X`” | converged value `≥ 11` after all `(S,2)` atoms with `|S| ≤ 7` and all cliques of M1’s kind |
| M4 | Row completion at `61/16` (exp-116 state, `N=180`); then `N=720` at `191/50` from BC-200’s state with rows remapped to nearest new directions | 2 × 8 | a frozen certificate at `3.8125`/`3.815` (`+0.0025–0.005`); the mass value of the tax `τ_180 − τ_720` on one site set; possibly 3.82 by refinement alone | `61/16` converges `≥ 11`; `N=720` value `≥ 11`: the plateau is not tax |

Order by information per hour: M0 and M1 first (reads of retained objects; they fix M3’s
design), M2 in parallel, M3 once M0 has a polished family, M4 on the remaining cores.
If M0 or M2 returns `≥ 11` at 3.82, drop M4’s `N=720` leg and move its cores to M3; if
M3 fails its kill, the verdict is that the one-body language with rank-1 cuts is closed
at 3.82 on this site set, and the next spend is rank-2 atoms or N1 at `3.84–3.86` to
locate the true plateau.

## 7. Method, numbers, what failed

Reads (light, `packing/.venv` Python 3.14): `family_structure.py` folds the 768
placements of `pr127-unit-control.json`, bins weight by angle and wall gap, builds `D4`
orbits, the closed-intersection graph of the heaviest 300 (float SAT, margin `1e-9`),
non-Helly triples (polygon clipping) and chordless 5-cycles; `clique_scan.py` does the
interior-overlap graph, a weighted branch-and-bound clique, the Helly test and the
centre census; `line_capacity.py` scans horizontal, diagonal and `±29.4°` lines at
`0.01–0.02` offsets for chord-`≥c` weight against `⌊len/c⌋`; `tax_and_kernel.py`
tabulates `D_N, B_N, L·D_N, U·B_N` and clips the kernel.
Every number in §3–§4 is in the `.out` files.
Floats only; nothing here is a decision.

Exact record inputs: `B = 9977/10000`, `D_180 = 207107/90000000`, T-018 mass
`434547/40000`, least cell `4001/4000`; family weight `21342289572/2055263195`; site
values `11.0556` (converged), `11.000` (two lost sets), `11.0724` (strip-seeded).

What failed: the family-level tests found no violated cut (expected at `10.38`), so
§2c’s prediction is qualitative; Caoduro–Sebő’s `τ*` was not computed (their figure is
not in the archive text; M1 must reconstruct it); no lemma bounds `τ*` of a general
clique of rotated unit squares; the slope of `τ_1(L)` is unknown, so §3’s “refinement
may certify 3.82” is a coin flip; whether `ν_B(3.82) ≥ 11` at all is OPEN, which M0/M2
exist to decide.

Next discriminating measurement: M0.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
