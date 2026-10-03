---
title: n17 Charge-Floor Pilot Review
date: 2026-10-02
status: planning-review
---
# n17 Charge-Floor Pilot Review

**Session:** 167, BC-406, lane B-review (independent adversarial reviewer).
**Reviewed:** `packing/devtools/pilot_n17_charge_floors.py` at commit `1a8a5e4a`
(SHA-256 `549ade62…`), its receipts under
`packing/campaign/explorations/X048-session-167-pilots/`, and lane B’s no-go for
[H-262](../../../packing/campaign/hypotheses/H-262-n17-conditional-charge-occupancy-census.md).
**Method:** every number below was recomputed in code that does not import the pilot,
retained with a `.txt` suffix and their logs under
[exp-243’s `audit/`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-243-n17-charge-floor-pilot/audit/)
(`recount.py.txt`, `spotcheck.py.txt`, `asymmetric.py.txt`, `verify_asym.py.txt`).
Nothing in the record was edited.

**Verdict.** The no-go stands.
The charge is valid at side $U$, the six floors and the endpoint control are reproduced
exactly by a direct rule evaluation, the cut-only census is reproduced exactly by two
independent methods, and the structural ceiling is a correct theorem for the class it
names. That class is narrower than the receipts’ prose reads: a *single, D4-symmetric,
linear* per-cell floor vector.
For that class, and so for H-262 as registered, confirmation is impossible and the exact
instrument is unnecessary.
Outside the class the ceiling gives nothing, and a short search shows one asymmetric
floor vector already beating it.

## Blocking Items

- **B1: the disposition must name the criterion band.** The ceiling, $30{,}966$, lies
  inside H-262’s own “inconclusive” band ($10^4$ to $10^5$), so the hypothesis’s
  pre-declared rule does not itself say “rejected”.
  What is established is stronger than the rule’s reject clause in one direction and
  weaker in the other: the confirm branch ($\le 10^4$) is impossible for every
  instrument in the registered class, by theorem; the engine-rejection clause ($> 10^5$)
  is reached only by the specific R068-at-$U$ charge ($7{,}703{,}312$), not by a rebuilt
  one, which was never measured.
  The record should close H-262 as *refuted by theorem for its registered class*, with
  the band stated, rather than as a count that crossed $10^5$.
- **B2: the ceiling’s scope must be stated wherever it is quoted.** The README’s “for
  *any* D4-symmetric per-cell floor vector, from any charge” is correct; the sentence
  after it, “per-cell floors cannot meet H-262’s $10^4$ threshold even with a charge
  designed for this test”, and the summary’s “charge-independent ceiling” are not, read
  alone. Asymmetric floors, families of charges, orientation-refined states, and
  nonlinear (pair or conditional) floors all escape the theorem, and a free asymmetric
  vector reaches $631$ orbits in fifteen hill-climb steps; see F4.

Neither item changes the verdict on H-262. Both change what the record may claim.

## Findings

### F1. The open-parent charge at $A_U$ is a valid packing charge at side $U$

R068’s budget is combinatorial and does not depend on the parent side.
I reconstructed it from the retained certificate (SHA-256 `cf70f74d…`): $M = \sum$ site
weights $+ \sum_{\text{rules}} w \times \text{images} \times \text{cap}$, with cap
$= \lfloor \sum c / \text{threshold} \rfloor$ for the 154 coefficient rules and the 481
plain rules (all coefficients positive, checked) and cap $= 1$ for the 254 mask rules
(every pair of winning masks intersects, checked: zero disjoint pairs).
No site weight is negative.
For any family of pairwise disjoint open regions, each site lies in at most one region
and each rule image fires for at most cap of them, so the charges sum to at most
$M = 17{,}000{,}448{,}944$. The parent side enters only through which sites a region
captures. R068’s strict cores belong to its *lower* bound ($\Gamma$ over legal parents),
which the pilot does not use.

The scaling is right: seventeen unit squares with disjoint interiors in $[0,U]^2$ become
seventeen open squares of side $A_U = L/U = 0.98653$ in $[0,L]^2$ with the sites fixed;
shrinking the squares rather than growing the container is the only choice that keeps
the sites where the certificate put them.
A packing at any side $\le U$ embeds.

The one-sided inequality holds in the claimed direction: the core of a pose lies inside
its open parent, coefficients and weights are nonnegative, so every rule is monotone in
the captured set and core charge $\le$ open-parent charge at every pose.
The exact instrument’s floor is at most the pilot’s sampled floor, so its survivors are
a superset of the pilot’s. The caveat is scope, not validity: the pilot evaluates R068’s
charge at a forced smaller parent, not the “rebuilt on $[0,U]^2$” charge H-262 names, so
F1 alone does not decide the hypothesis.
F4 does.

### F2. The floors are what the receipts say (spot check)

`spotcheck.py` evaluates the charge without a Möbius expansion: it expands the point
orbits as the checkers do, marks the sites strictly inside the open square, and fires
every rule directly.
All six witnesses agree to the unit: corner $63{,}045{,}956$, edge-near-corner
$377{,}790{,}059$, edge-middle $630{,}372{,}131$, interior-corner $747{,}616{,}217$,
interior-edge $930{,}431{,}172$, centre $920{,}859{,}332$. The 17 endpoint charges agree
to the unit and sum to $11{,}797{,}143{,}406 \le M$.

The corner collapse is real, not a units error.
At R068’s own side the same corner pose captures exactly $\Gamma = 1{,}000{,}026{,}844$
(also at three other corner poses).
At $A_U$ the corner-touching pose captures 62 sites against 355, all its charge from
rules; sliding the square along the diagonal, the charge is $63{,}045{,}956$ up to
$x = y = 0.5001$, $68{,}068{,}982$ at $0.501$, $189{,}448{,}782$ at $0.502$, and
$\Gamma$ from $0.505$ on.
The wall of sites that defeats R068’s corner pose sits in the band the $0.33\%$ smaller
square no longer reaches.
Random sampling of the corner cell at eight angles found nothing below the pilot’s
per-angle minima (its exact-in-position sweep is the stronger search, as it should be).

Note: the endpoint poses are five-decimal roundings; pose 9, $(0.70420, 2.70420,
39.805°)$, lies about $5 \times 10^{-6}$ outside the legal centre envelope.
Harmless for a sum $5.2 \times 10^9$ below $M$, but the control is not a strictly legal
packing as printed.

### F3. The cut-only census is exact (recount)

`recount.py` enumerates the $2^{16} \times 3^9$ occupancy vectors with its own cell
indexing and counts D4 orbits by Burnside: $161{,}100{,}756$ states and $20{,}155{,}518$
orbits before the cuts; $61{,}563{,}363$ states and $7{,}703{,}312$ orbits after, with
the identical fixed-point vector $(61563363, 16055, 16055, 2419, 14275, 27, 27,
14275)$. A row-by-row transfer DP over the five rows, a different algorithm, gives
$61{,}563{,}363$ cut-surviving states.
The endpoint’s own state survives the cuts.
Class-count table: $2{,}375$ vectors; $5{,}970$ orbits at the endpoint’s
$(4,4,3,2,4,0)$.

### F4. The ceiling: a theorem, and its exact class

**Statement.** Let $S$ be the D4 orbits of cut-surviving states, $N(n) \in \mathbb{Z}^6$
the class-count vector (D4-invariant, so defined on orbits), $c(v)$ the number of orbits
with $N = v$, and $N^* = (4,4,3,2,4,0)$. For every $\varphi \in \mathbb{R}^6$ and every
$M'$ with $N^* \cdot \varphi \le M'$,
$$\#\{[n] \in S : N(n)\cdot\varphi \le M'\} \;\ge\; c(N^*) + \sum_{\{N^*+d,\,N^*-d\}}
\min\big(c(N^*+d),\, c(N^*-d)\big) = 5{,}970 + 24{,}996 = 30{,}966,$$ the sum over the
49 unordered pairs with both members feasible.
*Proof:* if both members of a pair were excluded, adding the two inequalities gives
$2N^*\cdot\varphi > 2M'$. Nothing else is needed.
The three hypotheses that connect it to a charge: the test is linear in the occupancy
vector; the floors are constant on cell classes, which holds for every D4-invariant
charge, R068-type charges included; and the endpoint orbit passes, which holds for every
valid charge because floors are at most pose charges and the endpoint’s charges sum to
at most $M$. I recomputed all of it from my own table: 49 pairs, $30{,}966$; the largest
pair contributions are $3{,}864$ (one more near-corner, one fewer interior-edge) and
$2{,}210$. The pilot’s best random direction reproduces $34{,}690$ orbits in my counter,
so the symmetric optimum lies in $[30{,}966,\,34{,}690]$. Negative components are
harmless: $\sum N = 17$ on every survivor, so $\varphi$ is defined modulo the all-ones
vector.

**What it does not cover.** Orbits are D4 orbits, so an orbit is excluded as soon as
*one* image fails.
For a floor vector $f \in \mathbb{R}^{25}$ that is not class-constant,
the orbit test is $\max_g (gn)\cdot f \le \max_g (gn^*)\cdot f$: a maximum of eight
linear forms, convex and invariant, and the two members of an antipodal pair can be
killed by different images.
`asymmetric.py` hill-climbs over $f \in \mathbb{R}^{25}$ with exact Burnside counts,
starting from the pilot’s best symmetric direction ($34{,}690$): its second step left
$24{,}653$ orbits, below the symmetric ceiling; its fourth $3{,}614$, below H-262’s
threshold; its fifteenth $631$; its twenty-third $10$ orbits in $45$ states, close to
the hull floor (`asymmetric.log`; the run was still descending when this review closed,
and its final vector has not been recounted by canonicalisation).
*Coordinator’s note, 2026-10-02:* the run finished after 33 iterations at 6 orbits in 28
states. These are free vectors, not floors any charge has been shown to realise, and an
asymmetric charge costs an eightfold sweep; but as a structural matter the theorem is
specific to one symmetric linear floor vector and says nothing about asymmetric ones.
The same escape is open to a *family* of charges (an intersection of half-spaces; for
symmetric families the structural floor is the $N^*$ bucket, $5{,}970$), to
superadditive pair floors for doubly occupied cells (convex, the wrong direction for the
pair argument), and to an orientation-refined state space.
The only universal floor for a D4-invariant convex test that keeps the endpoint is the
lattice hull $\mathrm{conv}(D4 \cdot n^*)$: by LP over the $47{,}520$ candidate states
it holds exactly the 4 states of the endpoint orbit (the pattern has a stabiliser of
order 2). Beyond the registered class there is no structural obstruction, only cost.

**A strengthening left on the table.** Realisable floors obey far more than
$N^*\cdot\varphi \le M$: every packing of $k \le 17$ unit squares in $[0,U]^2$ gives
$m\cdot\varphi \le M$ for its occupancy vector $m$ (eight disjoint squares in the eight
near-corner cells force $\varphi_{\text{near}} \le M/8$, for instance).
Adding those constraints can only raise the ceiling.
It is not needed for the verdict.

### F5. Why this charge, and most charges, cannot bite at all

Every floor of the R068-at-$U$ charge is below $M/17$ (the best, interior-edge, is
$0.930\,M/17$), so the test is vacuous for every pattern, cut survivor or not.
That is not an accident of R068: at side $U$ a packing exists, so no charge is tight
globally, and the endpoint forces its seventeen floors to average at most $M/17$ (this
charge’s endpoint charges average $0.69\,M/17$). A per-cell test bites only where some
class floor exceeds $M/17$; the pilot’s orientation data shows this charge above $M/17$
at the centre for 46% of sampled angles and at the interior edge for 9%, nowhere else.

## Answers to the Review Questions

- **(a)** Valid, for the reasons in F1; the budget is independent of $A$; the inequality
  runs the right way. Scope caveat: not the rebuilt charge.
- **(b)** Reproduced to the unit; the collapse is geometric, not a scaling bug.
- **(c)** The antipodal argument is correct and I recount $30{,}966$ exactly.
  “Any D4-symmetric per-cell floor vector” is the right class for one R068-type charge
  and the wrong class for the phrase “any charge”: asymmetric floors do better (F4). The
  bound needs linearity (or concavity) in the occupancy vector.
- **(d)** Both counts reproduced exactly, by enumeration with Burnside and by a transfer
  DP.
- **(e)** H-262 is refuted for its registered class by theorem, with B1’s wording.
  The exact instrument is unnecessary: it could only place a count inside
  $[30{,}966,\,7{,}703{,}312]$, and no point of that interval confirms.
  The ceiling is a theorem with the statement in F4. For the next engine: a single
  symmetric linear floor is capped at $30{,}966$ orbits, about three to six times the
  affordable band; anything cheaper than geometric exclusion must therefore be
  asymmetric or multi-charge (free asymmetric vectors reach tens of orbits, so the
  obstruction there is realisability and the eightfold sweep, not structure), nonlinear
  (joint floors for the capacity-two cells, or floors conditional on neighbours), or
  orientation-refined.
  None of these has a structural ceiling above one orbit, and none has yet been shown to
  realise floors above $M/17$ anywhere but the centre.
  The subcontainer cuts are themselves asymmetric linear tests (a block indicator
  against a count), which is the natural place to look for a local charge that is tight.

## Evidence Status

Planning evidence. Nothing here is an admitted result; no bound or frontier field moves.
The recomputations are retained in the session scratchpad, not in the repository.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
