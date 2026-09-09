---
title: "X-023 — three losses and a new atom: where the next stretch of s(11) comes from"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-023
  title: "Three Losses and a New Atom: Where the Next Stretch of s(11) Comes From"
  date: '2026-09-09'
  author: Claude coordinator (Fable), with two Opus agents for mechanical work and three Fable agents for measurement and mathematics
  campaign: packing.squares
  brief: >-
    The owner asked for every way to push the n = 11 lower bound aggressively beyond
    3.810025723614703, starting from a contributed research note (checked in as the
    dated review of 2026-09-08), and for breadth first: map the directions, spike the
    cheap ones, and leave each with a discriminating measurement. This report separates
    the certificate's three losses (the shrink tax, the site restriction, and the
    integrality gap of the point-covering relaxation), disposes of the note's seven
    proposals against the record, opens one new certificate language (threshold atoms,
    the rank-one Chvátal–Gomory cuts stated on the measure side), and records what the
    wave-one spikes measured.
  sources:
  - docs/project/reviews/review-2026-09-08-extending-s11-lower-bound-note.md
  - packing/frontier/n-011.md
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/covering-values.yaml
  - packing/campaign/explorations/X-014-closing-from-both-ends.md
  - packing/campaign/explorations/X-019-structural-restrictions-and-conditional-dots.md
  - packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md
  - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md
  - packing/cases/n11_fractional_certificate/certificate.json
  - packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md
  - packing/src/sqpack/fractional/certificate.py
  - packing/src/sqpack/fractional/sweep.py
  - packing/src/sqpack/fractional/ceiling.py
  proposes: []
---
# X-023 — Three Losses and a New Atom: Where the Next Stretch of s(11) Comes From

**The certificate that proved `s(11) >= 3.81` loses side in three separable places, and
each loss has its own remedy.** The shrink `B = 9977/10000` costs a fixed `0.23%` of
side, about `0.0088` at `3.82`, and a finer direction net recovers almost all of it at
no cost in soundness.
The finite site set on which every covering program is solved makes every reported
optimum an upper bound on the true covering value, and the retained `3.8125` state was
never solved to completion.
And the point-covering relaxation itself has an integrality gap: at `3.82` every site
set stops at or above eleven while the depth-one fractional packings that would certify
a plateau reach only `10.38`, and the dual that stops the instrument is a fractional
mixture of wall squares and `29°` intruders that no integral packing realises.
This report opens a certificate language for the third loss, threshold atoms, which are
the rank-one Chvátal–Gomory cuts of the point-depth system stated on the measure side
and decided by the same exact event-cell sweep; disposes of the contributed note’s seven
proposals against the record; and records the wave-one measurements.

The bracket at the start of this work is
`3.810025723614703 <= s(11) <= U = 3.877083590022814`. Nothing in this document is a new
bound unless a section says so with a decided certificate and its digest.

## The Contributed Note, Dispositioned

The owner supplied a research note written by another agent session against snapshot
`7ef80525`; it is checked in verbatim as the
[dated review of 2026-09-08](../../../docs/project/reviews/review-2026-09-08-extending-s11-lower-bound-note.md).
Its seven proposals, against what the record already holds:

| Note’s proposal | Record | Disposition here |
| --- | --- | --- |
| §2 complete the rows on the retained `3.8125` sites before adapting the dual support | BC-252 proposed exactly this; `devtools.run_fixed_site_completion` was built for it and never invoked on the target | Run as spike E, job 1 |
| §3 expand the container about the frozen centred measure until a bad cell is reachable | not in the record; distinct from T-022’s dilation | Run as spike C |
| §4 parent-feasible centre domains | not in the record; the sweep’s `centre_domain` uses the core-fit inset | Run as spike A part C |
| §5 a rational octagon kernel strictly dominating the square core | agenda 025 contemplated adaptive cores; nothing built | Priced, not run: it recovers exactly half the area the shrink loses at a fixed net, and a finer net drives that area to zero; dominated by spike A unless the fine net is LP-prohibitive |
| §6 compatibility cuts: cliques and odd cycles on placements | X-017/X-018/X-021 discuss compatibility as a conditional-certificate and resource question; no cut family was ever stated on the certificate side | The threshold atoms below are the exact, verifiable form of these cuts; spike B measures them |
| §7 branch-specific certificates with coupled geometry | Agenda 030’s lanes (corner pair, E.4 segments, anchors) and X-018’s coupled outer LP | Existing lanes; case splits without headroom so far (corner class bought `0.0005`); reserve until threshold atoms exist to condition |
| §8 the exact Trump value | X-014’s modulus lemma and X-021’s priced closing route | Unchanged: irrelevant until the ladder is within about `0.01` of `U` |

The note’s diagnosis that no reviewed failure proves the method exhausted is right, and
its warning against reading the `3.8171` interpolation as a target is adopted.
Its account of exp-116 is accurate: nineteen row solves at a two-round limit, a
numerical objective of `10.7176` that bounds nothing.

## Where the Gap Decomposes

Write the certificate at `(L, B, net)`. Scaling every length by `1/B` turns it into a
measure on `[0, L/B]^2` that covers every unit square at a net direction, so the
instrument at side `L` has exactly the reach of unit cores at side `L/B`: the shrink is
a tax of `L(1/B - 1)` in side, paid once, and it is what Condition 4 buys for a finite
net. The rest of the loss is in the covering value itself.

| Loss | Size | Remedy |
| --- | --- | --- |
| Shrink tax `L(1/B - 1)` | `0.0088` at `3.82`, `0.0089` at `U`; the packing cap is `U · B · max(cos δ + sin δ) = 3.868983` | A finer net: `1440` steps give `B = 0.99971` and a tax of `0.0011`; `4000` steps give `0.0004` and a cap of `3.8767` |
| Site restriction: a restricted optimum is an upper bound on `τ*` | unknown; the `3.8125` state is unconverged at `10.72` | Row completion at fixed sites; full-dual pricing (every generator so far priced only its 32 or 96 heaviest rows) |
| Integrality gap: `τ* >= ν*`, and `ν*` can pass eleven below `s(11)` | at `3.82`, `ν* ∈ [10.38, ?]` and every site set stops at or above eleven | Cuts valid for packings and not for fractional packings: threshold atoms |
| The last `0.008` below `U` | the shrink cap | `B → 1` by a fine net or the shrink-free route; then the exact-side tree |

The dual that stops the instrument at `3.82` has, read from the transported unit family
of weight `10.3842`: `5.82` units flush against a wall, `1.75` within `0.1` of one,
`2.82` in the interior; by angle, `6.54` within `2.5°` of the axes, `1.33` in
`[27.5°, 30°)`, `0.71` in `[7.5°, 12.5°)`, `0.22` in `[38.2°, 42.2°)`. Its heaviest
orbits are the axis corner cores at `(0.506, 0.506)` (`1.66` and `1.19` over two
orbits), the axis core one unit up the wall at `(0.506, 1.506)` (`0.95`), a core tilted
`0.53°` at `(0.551, 2.330)` (`0.82`), and the `29.4°` core at `(1.332, 2.445)` (`0.36`)
with a cloud of near copies.
That is a fractional mixture of the ring of eight wall squares with tilted squares that
intrude into the wall column where the ring’s middle square would sit: integrally a wall
holds three squares and the central hole one, and the mixture is worth more than eleven
only because the wall-middle square and the two intruders that compete for its slot
pairwise overlap without a common point, so the point-depth constraints let each carry
weight near one half.
That is the shape a clique cut removes.

## Threshold Atoms

Let a **threshold atom** be a finite point set `S` in the container with a threshold
`k`, `1 <= k <= |S|`, and a weight `w >= 0`. It charges `w` to every core `P` with
`|P ∩ S| >= k`. A point atom is the case `|S| = k = 1`.

**Theorem (threshold certificate).** Fix `(n, L, B, net)` with Conditions 3 and 4. Let
`μ` be a finite collection of threshold atoms `(S_j, k_j, w_j)` whose union is invariant
under the D4 group of `[0, L]^2` (an atom’s image is an atom of the same threshold and
weight), and write `charge(P) = Σ_j w_j [ |P ∩ S_j| >= k_j ]` and
`budget = Σ_j w_j ⌊|S_j| / k_j⌋`. If every closed `B`-square at a net direction inside
`[0, L]^2` has `charge(P) >= 1` and `budget < n`, then `n` unit squares with pairwise
disjoint interiors do not fit in `[0, L]^2`.

*Proof.* Each unit square contains, by Condition 4, a closed `B`-square at a net
direction (or a D4 image of one) strictly inside its interior; the `n` cores `P_i` are
pairwise disjoint closed sets, so their traces `P_i ∩ S_j` are pairwise disjoint subsets
of `S_j`. Atom `j` charges core `i` only when its trace has at least `k_j` points, and
at most `⌊|S_j| / k_j⌋` pairwise disjoint subsets of `S_j` can have that many points.
Hence `n <= Σ_i charge(P_i) = Σ_j w_j · #{i : |P_i ∩ S_j| >= k_j} <= budget < n`. D4
invariance handles cores at image directions exactly as Condition 1 does for point
atoms. ∎

When `k_j` divides `|S_j|` the atom’s inequality on the dual side,
`Σ_{P : |P ∩ S| >= k} y_P <= |S| / k`, is implied by the point constraints (sum the
constraints of the points of `S` and divide by `k`), so the atoms that add strength are
those with `k ∤ |S|`: `2`-of-`3`, `3`-of-`4`, `3`-of-`5`, `4`-of-`7` with budget one,
and `2`-of-`5`, `3`-of-`7` with budget two.
They are the rank-one Chvátal–Gomory cuts of the point-depth system, and on the
fractional-packing side they are clique cuts (three cores pairwise overlapping with no
common point may each carry `1/2` under the point constraints, `3/2` in all, and a
`2`-of-`3` atom with one point in each pairwise intersection charges all three, so they
must total at most one) and odd-cycle cuts (a `2`-of-`5` atom on five points that
consecutive cores contain in pairs allows two where the point constraints allow `5/2`).
Weighted thresholds (charge when `a(P ∩ S) >= t`, budget the largest number of pairwise
disjoint subsets of `S` of `a`-weight at least `t`, at most `⌊a(S) / t⌋`) are the same
theorem.

Two facts make the language cheap.
First, the exact sweep decides it unchanged: at a net direction the centres whose core
contains a point `s` form an axis-aligned rectangle `R_s` in the rotated frame, which is
what `sweep.py` already builds; `[ |P ∩ S| >= k ]` is a Boolean of rectangle indicators,
constant on the open cells of the same event grid, and by inclusion–exclusion it is a
signed sum of indicators of intersections of the `R_s`, each an axis-aligned rectangle
with corners on the existing grid, so the integer difference array takes the atom as a
few extra signed terms.
The minimum still sits in an open cell: on a cell boundary the closed core’s trace
contains the traces of the adjacent cells, and the charge is monotone in the trace.
The signed-weight refusal in `sweep.py` guards signed *point* weights, whose total is
not monotone; a threshold atom’s total is.
Second, the D4 averaging argument is unchanged, so the covering program may be solved
over atom orbits as today, with an atom orbit’s column carrying its budget times its
orbit size.

Separation is where the work is: given the dual `y` of the current restricted program,
an atom is worth adding exactly when its charge `Σ_{P charged} y_P` exceeds its budget.
For `2`-of-`3` atoms the natural candidates are triangles of the overlap graph of the
dual’s support with empty triple intersection, with one point chosen in each pairwise
intersection; the charge is then evaluated over the whole support, so clusters of
near-copies aggregate.
What the language cannot express is a clique whose members are thin and pairwise cross
at distinct points (no point set gives every member more than half the weight once five
or more such members exist); cores are fat, and the pinwheel of five unit squares
pairwise overlapping about an uncovered centre is a `3`-of-`5` atom, so the limitation
is not expected to bind here.
Whether it closes `0.06` to `0.1` of covering value at `3.82` is the measurement of
spike B.

## The Direction Map

Breadth first, as asked.
Every direction carries the loss it attacks, what it could be worth, and the measurement
that kills it; the wave-one spikes are marked.

| # | Direction | Attacks | Worth, if it works | Kills it | Wave |
| --- | --- | --- | --- | --- | --- |
| D1 | Net refinement: more directions, larger `B` by the sharpened containment test | shrink tax | up to `0.19%` of side per rung, `0.007` at `3.82`; the cap rises to `3.876` | the least coverage on the fine net falls faster than `B` rises | A |
| D2 | Frozen-measure expansion: enlarge the container about the centred atoms until a cell at mass `M/11` is reachable | frozen certificate slack | probably `10^-4` or less | first bad cell within `10^-4` of `3.81` | C |
| D3 | Parent-feasible centre domains | wall strips of width `0.00115` where the tight cells sit | capped, with every other core-choice idea, by the shrink tax (lane T, Lemma 1) | no change in least coverage | A |
| D4 | Octagon or angle-cell kernels | shrink area | half the lost area at a fixed net | dominated by D1 | priced |
| D5 | Row completion at `3.8125`, then `3.815`, `3.8175` | site restriction | one rung of `0.0025` to `0.0075`, each multiplied by D1 | converged restricted value at or above eleven on the retained sites | E |
| D6 | The `3.82` discriminator: cutting loop with full-dual pricing | site restriction, and the plateau question | either a certificate at `3.82` or a depth-one family at eleven | neither within budget | E |
| D7 | Threshold atoms | integrality gap | unknown; the dual’s shape suggests up to a unit per wall slot | no violated `2`-of-`3` or `2`-of-`5` atom on the retained dual, or no drop on the fixed site set | B |
| D8 | Measure-majority atoms (segments, areas) | integrality gap | later rung of D7 | polygon-arrangement verification too costly | — |
| D9 | Pair certificates and the SDP hierarchy | integrality gap | the residual after D7 | no exact verifier | — |
| D10 | Structural conditioning (corner pair, E.4 segments, anchors) | case splits | case splits, `0.0005` measured | — | Agenda 030 |
| D11 | The shrink-free route, `B = 1` with open cores and interval-decided angles | shrink tax, the cap | the `N → ∞` limit of D1, at most `L · D_N` over it (lane T, F7); needed only for the endpoint run within `10^-5` of `U` | D1 reaches the same place cheaper | — |
| D12 | Class certificates by composition | angular integrality | none measured at `3.84` | already dead on grid 79 | — |
| D16 | Instrument: full-dual pricing, better separation | site restriction | the plateau at exactly eleven was a pricing stop | — | E |
| D18 | Saturation cuts from the `n = 12` bound: every unit probe meets a packed square’s interior below `3.96`, so `Σ_{P meets Q0} y_P >= 1` | integrality gap | none on the retained dual: the least met weight over sampled probes is `1.018`, at the corner probe | measured here, CHECKED | done |
| D19 | Direction-dependent atom weights | — | nothing: the budget is `Σ_s max_θ w_s(θ)`, so the maximum dominates (lane T, Lemma 2) | proved | rejected |
| D20 | `k`-fold packing witness search: `ν* ≥ 11` iff some `k`-fold packing has `11k` squares; anneal `22` unit squares with a triple-overlap penalty, verify hits exactly at weight `1/2` | the plateau question, from below | an exact kill of every one-body certificate at the hit side, with the odd cycles that name the cuts | no hit at `3.88`, where two Trump copies exist | 2 |
| D21 | Fixed-support polisher: the exact optimum of the fractional packing on the retained `768`-placement support against all arrangement vertices | the plateau question, from below | `ν_S ≥ 11` kills every one-body certificate at `3.82` for this `B` and net; otherwise the shadow prices say where the support is short | `ν_S` far below eleven | M0, running |
| D22 | Wall-line density atoms: charge cores with a chord of length `≥ 1` on a wall-parallel line, budget `⌊L⌋ = 3` per wall | integrality gap | whatever the optimum’s wall usage exceeds three (the retained family is at `2.85`) | the polished family keeps every wall line `≤ 3` | 2 |
| D28 | Disk cores: no net, no shrink | shrink tax | nothing: eleven unit-diameter disks fit at `3.82` | arithmetic | rejected |
| D17 | Asymmetric measures from the spanning premise | — | nothing unconditional: D4 averaging preserves validity | X-019’s argument | rejected |

## What the Wave-One Spikes Measured

This section is filled as each spike reports; a row without a settled number is still
running. The lane reports are retained under
[`results/agenda-032/`](../series/series-000-smoke-and-calibration/results/agenda-032/)
with their scripts.

**The ceiling at `3.82` is a theorem.** Spike B’s combined loop, after one exact
site-separation round on BC-200’s sites, produced an LP dual of eleven rows at weight
exactly one whose D4 symmetrisation is a family of `88` closed `B`-squares at six net
directions, weight `1/8` each, total exactly `11`, with exact maximum depth `1` over the
`20,376` vertices of its arrangement.
`sqpack.fractional.ceiling.verify_ceiling` proves it (`net` regime, D4-symmetric
measures), and the coordinator replayed the frozen bytes (SHA-256 `95cf0647…6427`,
retained as
[`ceiling-family-191-50.json`](../series/series-000-smoke-and-calibration/results/agenda-032/ceiling-family-191-50.json)
with its
[replay receipt](../series/series-000-smoke-and-calibration/results/agenda-032/ceiling-family-191-50-replay.json)).
By weak duality no D4-symmetric point-atom measure of mass below eleven covers every
closed `9977/10000`-square at a net angle in `[0, 191/50]^2`, on this net or any net
containing those six directions; the statement transfers upward in `L` and downward in
`B` (a smaller concentric core is inside the larger one).
Scaled by `1/B` it is a family of unit squares at side `3.8288`: **the one-body
point-atom method, at any shrink and on any net containing those six directions, cannot
certify beyond unit side `3.8288`, that is beyond `L = 3.8288 · B`.** The two lost site
sets that stopped at exactly `11.000000` were reading this ceiling; BC-200’s `11.055617`
was above it because its site set was not at its optimum.
An independent reader written from the statement is being run.

**The frozen atoms transfer to every finer net and dilate to `3.8166` at `1440`
directions.** With the original shrink the least mass at every finer net is
`96377/100000` at an intermediate direction; with the sharpened-test shrink of each net
it is `4001/4000` at every net up to `2880` steps, so the certificate holds at
`(381/100, B_max(N), N)` for `N ∈ {360, 720, 1440, 2880}`. The crossing shrink, the
least `B` (to `10^-6`) whose least mass over the net exceeds `M/11`, is
`4989621/5000000` at `360` and `9979243/10000000` at `720` (the added directions never
bind there), and `2494953/2500000 = 0.9979812` at `1440`, where they do.
The dilation supremum `(381/100) · sqrt(1 + D_N^2) / (B_cross(N)(1 + D_N))` is then
`3.81353994` at `360`, `3.81573032` at `720` and `3.81660950` at `1440`, against T-022’s
`3.810025723614703`. The retention packet (a frozen certificate at the crossing shrink
on the finer net, decided through the two-route gate, and the dilation corollary) is in
progress; the `720` certificate has been accepted by both routes in its scratch run and
its formal report is pending.
The ceiling above says the same atoms can never be dilated past `3.8288 · B_max(N)`, and
the unit-equivalent side of these certificates, `3.8177` to `3.8179`, sits `0.011` below
that cap.

**Two of the note’s geometric refinements are inert on the frozen atoms.** Enlarging the
container about the centred measure reaches its first bad cell after
`δ* = 5.4926 × 10^-6` of side (at `L* = 176536859/46335000 = 3.81001099`, direction
`0`): the four corner atoms of weight `917/6250` sit on the far corner of the
corner-snug axis core, whose mass drops to `85353/100000` the moment the walls move, and
composing the expansion with T-022’s dilation gives `3.81003671`, a gain of `10^-5`.
Parent-feasible centre domains remove `541,048` of the `567,130,649` reachable cells at
the sharpened inset and improve the least mass at no direction; it stays `4001/4000`.

| Spike | Question | Reading | Status |
| --- | --- | --- | --- |
| A, net refinement | does a finer net cost coverage; does its larger shrink recover it? | see above: transfers at every net; crossings `0.9979242`, `0.9979243`, `0.9979812`; dilation suprema `3.81354`, `3.81573`, `3.81661` | EXACT (sweeps and crossings); retention packet running |
| C, frozen expansion and parent domains | at what side does a cell at mass `≤ M/11` become reachable; do parent-feasible domains raise the least mass? | first bad cell after `5.4926 × 10^-6`, composed supremum `3.81003671`; parent-feasible domains improve no direction | EXACT; both dead |
| B, threshold atoms | are two-of-three atoms violated by the retained dual; does adding them lower the restricted value? | `3504` violated atoms (`438` orbits) on the `191/50` family, maximum charge `1.078511`; `52088` (`6471` orbits) on the unit family, maximum `1.184795`; `92%` of the violation on mixed near-axis and tilted triples; no two-of-five violation. On BC-200’s sites the value falls from `11.055617` to exactly `11.000000` with pair-centroid atoms (the ceiling), and the ceiling family is separated by interior-vertex atoms at charge `5/4`; with those the restricted value reads `10.926982` with rows still incomplete | EXACT (charges, ceiling); LP running |
| E, `61/16` row completion; `3.82` cutting loop | does the unconverged `3.8125` state complete below eleven; does full-dual pricing move the `3.82` value? | the `3.82` loop read `11.055617`, `11.038636`, `11.024472`, `11.009981`, `11.009995` over five iterations with rows unconverged, consistent with the ceiling; the `61/16` completion is still running | running |
| T, theory | what can one-body core choices buy; where is the plateau evidence; what cuts fit the dual? | the sandwich lemma caps every core-choice idea by the shrink tax; direction-dependent weights never help; a half-integral witness is always cut by one odd-cycle atom | PROVED |
| M0, fixed-support polish | the exact optimum of the fractional packing on the retained `760`-placement support | `76/7 = 10.857` in floats with the working set closed, exact rebuild running; dominated by the ceiling family on its own support | running |
| D18, saturation cuts | does the retained dual violate the saturation inequality from the `n = 12` bound? | no: least met weight `1.018` at the corner probe | CHECKED |

## What This Document Does Not Establish

No bound changed. The threshold-atom theorem is proved here and in the module’s
docstring, and its module is tested against an independent per-atom route, but no
threshold certificate has been decided at any side, and the two-route retention gate
(`devtools.decide_certificate` and the interval route) does not yet accept the extended
object; a candidate would need the independent verifier the coordinator will commission.
Every LP value quoted is a restricted optimum on one site set, an upper bound on that
set’s covering value and a bound on nothing else.
The frozen-atom net readings are exact decisions about the retained atoms and say
nothing about the covering value on a finer net, which needs the re-optimised program.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
