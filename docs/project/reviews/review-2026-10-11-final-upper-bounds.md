# Review: Final Mathematical Review of the Upper-Bound Results of PR 487

**Date:** 11 October 2026. **Verdict: accepted, for finite feasibility only.** Every
certificate the twelve `V3`/`C3` upper-bound entries of the 2026-10-10 intake pass cite
(T-128, T-130, T-131, T-134, T-135, T-136, T-137, T-138, T-139, T-140, T-141 and T-146)
proves the bound its claim prints, and T-129’s three printed sides are the sides its
retained certificates state.
Each route’s acceptance of a certificate implies $s(n) \le S$, for the reasons
re-derived below; every one of the 86 printed sides in the thirteen claims is the exact
certificate side, or the witness’s side exactly; every comparison, scope list and
pending-adoption statement checked here holds against the case records at `aeb8a7219`,
where no case ceiling has moved; and the credit of each entry follows the bibliography
and, for T-146, the owner’s decision.
Four findings are recorded, none blocking.

This review was written by an AI agent (Claude, at maximum reasoning effort), lane F2 of
the final mathematical review of PR 487, prompted separately from the import, replay and
stage 4 review lanes, with no shared context.
Its relation to the results is `project`. It moves no rung, writes no record and adopts
no house; the proposed record changes are in the findings, for the coordinator.
It writes one file, this one.

## Claims Covered

| Entry | Source and counts | How each side is printed | Held here to |
| --- | --- | --- | --- |
| T-128 | Francisco Couzo, #451: 105, 108, 127, 131, 155, 180, 228, 306 | 29 or 30 places, the exact side | the complete originals in `facts/complete-certificates-and-decimal-poses.json.xz` |
| T-129 | Evan Daniel, #375 updates: 105, 130, 292 (`V0`/`C0`) | 30 places, the exact side | the retained `n-NNN.cert` files of the two dated packets |
| T-130 | Couzo, PR #460 comment: 84, 86, 105, 175, 270 | 28 or 30 places | the derived facts `facts/n-NNN.yaml` |
| T-131 | Daniel, #465: 132 | 30 places | `hunt1_n132.cert` |
| T-134 | Couzo, #476: 132, 237, 263, 267, 270, 303 | 30 places; a fraction at 263 | `source/certificates/nNNN.cert` |
| T-135 | Kevin Fang, #484: 308 (343 and 344 beyond the corpus) | fractions | `source/n0NNN/n0NNN.cert` |
| T-136 | Nate Chaoweeraprasit, SQUISH, #481: seventeen counts | fractions | the derived facts `facts/n-NNN.yaml.gz` |
| T-137 | Eric Deleeuw, #483: 70 | 26 places | the derived fact `facts/n-070.yaml.gz` |
| T-138 | Mishapolk, #470: sixteen counts | 12 places, the witness’s side exactly | the derived facts `facts/n-NNN.yaml.gz` |
| T-139 | Daniel, no issue: 126 | 30 places | `n126_xu.cert` |
| T-140 | Couzo, #488: 132, 175, 209, 237, 270, 305 | 29 or 30 places | `source/certificates/nNNN.cert` |
| T-141 | Daniel, #489: 132, 308 (343 and 344 beyond the corpus) | 30 places | `hunt3_nNNN.cert` |
| T-146 | Daniel’s regularized lists, no issue: fifteen counts | 30 places | the original gzip `n-NNN.cert.gz` |

**Read in full.** The thirteen register entries, their 26 evidence entries and the
bibliography keys they name; `results.schema.yaml` on `regularizations` and
`regularizations_problems` in `check_results.py`; the five stage 4 reviews of 10 and 11
October; the third route `devtools/check_half_angle_area.py` in full; the kernel
`evand_arrangement_reports` (`job_input`, `run_case`, `validate_job`,
`validate_receipt`, `replay_receipt`); the parser and conversion in
`evand_exact_certificates` (`Pose.basis`, `Pose.corners`, `parse`, `basis_witness`,
`corner_squares`, `ceiling_decimal`, `terminating_decimal`); `sqpack.verify` in full and
`sqpack.witness` (`_square_from_pose`, `_materialize`, `_exact_materialize`,
`_margin_summary`, `exact_verify`, `_rational_sign`);
`check_rational_witness_independent` in full; the adapters, `admit`,
`half_angle_tangent`, `decimal_dilation`, `certificate_from_witness`, `read_fact`,
`read_facts`, `HOUSES`, the spans and `compare` of `upper_bound_reports`;
`decimal_pose_margins` in full; the thirteen packet READMEs, declarations and frozen
claim records; the retained regularized JSON of each T-146 count and the method log; the
case records of every count in scope; the beyond-horizon rows of `source-coverage.yaml`;
and [epistemics.md](../../../epistemics.md) on review records, confirmation, credit,
regularizations and significance.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
shared with two other review lanes, at most two processes at once, on
`claude/determined-rubin-yjfy2a` at `aeb8a7219`, with nothing of the record or the
routes changed. The kernel replays and the third route sampled the receipts rather than
replaying all 270 retained jobs again, as the lane’s budget asked; the sample is named.

| Command (`python -m devtools.…`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `upper_bound_reports PACKET check-claims`, all nine packets | each frozen comparison rebuilt from the certificates and the houses’ own packets | all nine rebuilt equal | 0.5 to 3.1 s each |
| `upper_bound_reports PACKET check`, all nine | each receipt admitted structurally: every job, both routes, the required control diagnostics | 98 certificates and 294 jobs admitted | 0.5 to 1.8 s each |
| `couzo_refinement_reports check`; `couzo_followup_reports check` and `check-packet`; `evand_hunt_reports check` and `check-claims` | T-128’s, T-130’s and T-131’s admissions, T-130’s blob rebuild, T-131’s frozen comparison | all admitted; 5 blobs rebuilt; rebuilt equal | 0.5 to 0.7 s each |
| `acquire_source PACKET --check` for #488, #489, the regularized and the #465 packets | custody of the retained bytes | `PACKET_MATCHES_ITS_CONTRACT` | 0.1 s each |
| `check_results` | the register’s structural contract, the typed `regularizations` included | 146 results pass; 132 confirmed | 1.9 s |
| `upper_bound_reports ebdeleeuw-n70-refinement-2026-10-10 check --replay` | T-137’s 3 jobs on both maintained routes | all equal | 4.7 s |
| `upper_bound_reports evand-trio126-2026-10-09 check --replay` | T-139’s 3 jobs | all equal | 15.5 s |
| `evand_hunt_reports check --replay` | T-131’s 6 jobs, n = 132 and 155 | all equal | 36.0 s |
| `upper_bound_reports couzo-certificates-2026-10-10 check --replay` | T-140’s 27 jobs, all nine replayed counts, serially in one process | all equal | 511 s (500 s CPU, beside the other lanes’ runs) |
| `check_half_angle_area decide-imports --workers 1 --imports '#476' '#483' '#484' trio126 '#488' '#489'` | the third route on the 21 certificates of six packets, 126 controls, every cross-check | no disagreement; 693,682 pairs | 66.6 s |
| `check_half_angle_area decide-imports --workers 1 --imports regularized` | T-146’s fifteen, 90 controls, the fifteen arrangement measurements | no disagreement; 359,228 pairs | 152.2 s |
| `check_half_angle_area decide-imports --workers 1 --imports '#470'` | all 30 of T-138’s witnesses, 180 controls, the two credit measurements | no disagreement; 605,609 pairs | 82.4 s |
| `check_half_angle_area decide --workers 1` | T-128’s, T-130’s and T-131’s fifteen certificates, 90 controls, the register decimals | no disagreement; 213,064 pairs | 24.6 s |
| this review’s own checker (`fractions` only, below), 18 certificates from thirteen packets, three controls each | unit squares, closed-box corners, separating axes on every near pair | all feasible; 54 controls as required | 58 s in all |
| the same, with every one of the 47,278 pairs of `hunt3_n308.cert` decided by the separating-axis test, no disc rule | the disc rule is not load-bearing | feasible, the same margins | 37.6 s |
| a diagnostic of the third route’s pushed-pair control on 36 certificates | whether the refusal is the pair’s | the pair overlaps in all 36; no square leaves the box | 48.8 s |
| an optimal-assignment measurement of T-146’s fifteen views against the packings the entry credits | the `identity` numbers of `regularizations` | all fifteen reproduced | 3.7 s |

Each wall includes the interpreter’s start; the third route ran with one worker, so its
wall is its CPU. The whole lane used about 18 CPU-minutes.
Not re-run here: `decide-imports --upstream` and `decimal_pose_margins check`, which
need the sources’ files fetched at their pins, and the full kernel replays of the other
eight receipts, which the admissions above hold to their rows and the third route to
their inputs and margins.

## From Certificate to Bound

The record defines $s(n)$ as the side of the smallest square holding $n$ closed unit
squares with pairwise disjoint interiors, boundary contact allowed (the frontier README;
T-014’s claim states the convention outright).
The minimum exists: at a fixed side $S$ the poses form a compact set, and containment in
$[0, S]^2$ and a non-negative separating-axis gap on every pair are closed conditions,
so the set of feasible $S$ is closed and bounded below.
Hence $s(n) \le S$ holds exactly when some packing of $n$ closed unit squares with
disjoint interiors lies in the closed box $[0, S]^2$, and that is what every route
decides. Under the other common reading, an open box with $s(n)$ an infimum, the same
number results: a closed-box packing at $S$ lies in the open box
$(-\varepsilon, S + \varepsilon)^2$ for every $\varepsilon > 0$, so the infimum is at
most $S$, and an open-box packing at $S$ is a closed-box packing at $S$. So a
certificate whose squares touch each other or the walls, as all seventeen of T-136 touch
the walls, proves $s(n) \le S$ in either reading; the touching-pair and wall-contact
acceptance of the routes is the right notion, and no route accepts an overlap of
positive area.

Each certificate gives a rational side $S$ and, for each square, a rational centre
$(x, y)$ and either $t = \tan(\theta/2)$ (the text certificates) or the rotation
$(c, s)$ (the derived facts).
The bound follows from four facts, and I re-derived why each route decides each:

1. **Every piece is a unit square.** For rational $t$,
   $(c, s) = ((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2))$ satisfies
   $c^2 + s^2 = ((1 - t^2)^2 + 4t^2)/(1 + t^2)^2 = 1$, so $(c, s)$ is a rotation by
   $\theta = 2\arctan t$, and every rotation but the half-turn, which is the same square
   as none, has such a $t$. The corners $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$
   are a unit square. `sqpack.verify.check_unit_squares` holds every edge to squared
   length 1 and every corner to a zero dot product; the independent checker holds the
   edges to unit length, orthogonality and closure; the third route holds $(c, s)$ to
   the unit circle and forms its corners from it; a stated basis of a derived fact is
   held to $c^2 + s^2 = 1$ by `certificate_from_witness` (which also recovers
   $t = s/(1 + c)$ and refuses a basis that is not that $t$’s rotation) and by the third
   route’s `unit_basis`.
2. **There are exactly $n$ of them.** `legacy.parse` refuses a header count that differs
   from the expected one, fewer or more rows than $n$, and any literal outside
   `-?\d+(?:/[1-9]\d*|\.\d+)?`; the SQUISH, centred and decimal adapters refuse a count
   or a square list that differs; the third route’s readers refuse the same; and
   `validate_job` holds every job to $n(n-1)/2$ pairs tested on both routes, so no pair
   was skipped. A square listed twice overlaps itself and is refused.
3. **Each lies in the closed box.** A convex polygon lies in a convex box iff its
   vertices do, so the maintained routes test every corner for $0 \le x \le S$ and
   $0 \le y \le S$ by exact sign, with zero counted as contact and accepted.
   The third route forms no corner: the corners of a unit square at rotation $(c, s)$
   lie at $x \pm (c \mp s)/2$, so its horizontal reach either side of the centre is
   $h = (|c| + |s|)/2$, and the same vertically; it lies in the box iff
   $h \le x \le S - h$ and $h \le y \le S - h$, tested with non-strict inequalities.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors iff
   a line separates them, and a separating line can be chosen parallel to an edge of one
   of them; for two squares the four edge normals suffice, two per square since opposite
   edges are parallel. `sqpack.verify.separated` and the independent checker’s `pair_gap`
   compute the exact projection gaps on those four axes and refuse a pair only when
   every axis shows overlapping projections; a zero gap is contact, accepted.
   The third route decides the same fact another way: two closed convex sets have
   disjoint interiors iff their intersection has zero area, since an intersection of
   positive area is convex and so has an interior point, which is interior to both, and
   conversely an open point common to both interiors gives the intersection positive
   area. It clips one square by the other’s four closed half-planes (Sutherland–Hodgman,
   exact for a convex clip polygon, in `Fraction`), takes the shoelace area, and refuses
   a pair whose area is positive.
   Pairs whose centres are at least $\sqrt2$ apart (squared distance at least 2) are
   skipped on the ground that each closed unit square lies in the closed disc of radius
   $\sqrt2/2$ about its centre and two such discs with centres $\sqrt2$ or more apart
   have disjoint interiors; my own run with that rule switched off decided all 47,278
   pairs of `hunt3_n308.cert` by separating axes and found the same verdict and margins.

Arithmetic is exact `Fraction` arithmetic on every route; nothing rounds, dilates or
tolerates.

**Printed sides.** A certificate is admitted only where the side it is printed at equals
the exact side, or is a decimal print that is the exact side rounded up at its places
(`admit`; the third route’s `admitted` by its own integer ceiling).
A print $p \ge S$ then states a true bound, $s(n) \le S \le p$. The thirteen claims
print either the exact side, as a terminating decimal of at most 30 places or a
fraction, or, for T-138, the 12-place ceiling that is the witness’s side exactly; my
audit found no claim that prints a rounded value as if it were exact (below).

**The decimal-pose route (T-138).** The source’s files are decimal centres and angles in
degrees; cosines and sines of decimal degrees are irrational and the digits are rounded.
`decimal_dilation` makes an exact witness from two declared options, read here from the
declaration at every count: a `dilation` $\lambda = S_n/s$, with $s$ the printed side
and $S_n$ its 12-place ceiling, applied to every centre about the box centre, so the
witness’s side is $S_n$ exactly; and `half_angle_places` 32, each $t = \tan(\theta/2)$
rounded down at 32 decimals, decided by an outward-rounded enclosure that the working
precision raises until both ends floor alike (the tangent of half a rational angle in
degrees is irrational except at $0$ and $\pm 90$, which are returned exactly, so the
floor is decided). Soundness of the bound rests on neither step: every route decides the
resulting exact witness in full, and a wrong step could only yield a witness that fails
or one that packs at $S_n$ all the same.
The steps bear on attribution, and there the arithmetic checks:
$\lambda - 1 \le 7.9 \times 10^{-14}$ and $|x|, |y| \le s/2 < 9.1$, so no centre moves
by as much as $10^{-12}$; and $\theta = 2\arctan t$ has derivative at most 2 in $t$, so
a rounding of $t$ below $10^{-32}$ turns a square by less than $2 \times 10^{-32}$ and
moves a corner, at distance $\sqrt2/2$, by less than $1.5 \times 10^{-32}$, which is the
claim’s “no corner by as much as 1e-31”. Dilation about the centre by $\lambda \ge 1$
never creates an overlap: with $d = c_j - c_i$ and $K$ the Minkowski difference of the
two squares, convex and centrally symmetric with $0$ in its interior, $\lambda d \in
\operatorname{int} K$ would put $d = \lambda^{-1}(\lambda d) + (1 - \lambda^{-1})0$ in
$\operatorname{int} K$ too.
That is why the printed near-packings become packings, and why the claim rightly says
the bound rests on the dilation (RK-2).

**Beyond the horizon.** T-135’s and T-141’s claims also print the release’s sides at 343
and 344, outside their scopes and the case corpus.
Each is proved by the same confirming entry, whose scope names 343 and 344 at
`assurance: verified`, and `source-coverage.yaml` carries them as beyond-horizon rows:
Kevin Fang’s two, now `superseded` by Evan Daniel’s, whose sides are smaller by
$1.667 \times 10^{-2}$ and $1.039 \times 10^{-3}$ (recomputed here), all four below the
grid’s 19. The printed row values are the exact sides (#489) and the 15-place ceilings
(#484), as recomputed.

**What the parse and the adapters decide.** A misread literal would reach both
maintained routes through the one parse they share; it could not make a false bound
pass, since whatever packing they decided would then be a packing at its own side, but
it could break attribution.
The third route’s own readers, and this review’s, close that: every side, centre and
rotation I read agrees with the retained checker inputs at the 18 certificates I
decided, and the third route found the same at all 81 it ran.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; at T-128, T-130, T-134 and T-140 the copy the source author ran | the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `gzip`, `json`, `hashlib`, `decimal`; `sqpack.yamlio` for a fact | `Fraction` and the formats’ meaning |
| this review’s checker | unit shape from its own corners, closed-box corners, disc rule then separating axes | nothing of the repository; `fractions`, `gzip`, `json`, `lzma`, PyYAML for a fact | `Fraction` and the formats’ meaning; the separating-axis method |

The kernel owns the job layout, the two controls and `validate_job`; the importer owns
custody, the adapters, admission and the claim comparison.
Which code decided what: at T-128, T-130, T-134 and T-140 the sources report passes from
a copy of this repository’s `sqpack` verifier, so V-sqpack-verify there reproduces with
the producer’s code, and the independently re-implemented relation each confirming entry
declares rests on the independent corner checker and the third route, which share
nothing with the producer’s code; at the other eight entries no route is the source’s,
and at T-138 the witness is this repository’s own derivation.
The record says so in each claim.

**What stays unchecked.** CPython’s integer and `fractions` arithmetic is common to
every exact checker here, this review’s included.
None of the sources’ programs ran: the checkers, solvers, regularizer and path test of
the sources are reports.
Every KKT, local-minimum, jamming, closed-form, exact-optimum and same-packing statement
is the source’s and is not decided; the record states each as the source’s. That a
published file is the one its author meant is attested by the pins and the stage 4
reviews’ fetches; this lane fetched nothing.

## The Controls

The kernel’s two controls (a duplicated square, a square moved by $S + 2$) are gross, as
every stage 4 review recorded (RD-2, RI-3, RK-8, RL-4, RG-5): `validate_job` requires
both routes to refuse each with its negative diagnostic on the full pair count, and the
retained receipts show a gap of exactly $-1$ and a square whole units outside.
The third route adds four sharp controls per certificate; all 486 that ran here reached
their required outcome.
One of them, the closest pair pushed $10^{-30}$ of the centre distance past contact, is
required only to be *refused*, and a square moved by its nearest-point shift could in
principle leave the box instead, so I checked, on all 36 certificates of the #476, #483,
#484, trio126, #488, #489 and regularized packets, which square the refusal came from:
in all 36 the pushed pair itself overlaps and no square is outside the box.
The control is sharp as described.
My checker ran the duplicate, the box at exact far-wall contact (accepted) and the box
$10^{-40}$ narrower (refused) on its 18 certificates.

## Agreement to Every Digit

My checker, written from the format and the mathematics with `fractions` only, decided
18 certificates from the thirteen packets: T-128 at 105, T-130 at 84, T-131 at 132,
T-134 at 132 and 263, T-135 at 344, T-136 at 131, T-137 at 70, T-138 at 103 and 258,
T-139 at 126, T-140 at 305, T-141 at 308, T-146 at 129 and 303, and T-129 at 105, 130
and 292. All are feasible, and the least margins equal the record’s to every digit where
the record prints them exactly: wall clearance $1/(2 \cdot 10^{20})$ and least
separating gap $10^{-20}$ at every Daniel-format certificate of Couzo’s, Daniel’s and
the regularized lists; $2^{-65}$ and $3.147 \times 10^{-20}$ at Fang’s 344; $10^{-15}$
and $1.583 \times 10^{-12}$ at Couzo’s rational witness of 263; exactly 0 and $10^{-32}$
at SQUISH’s 131; $6.011 \times 10^{-13}$ and $1.201 \times 10^{-12}$ at Deleeuw’s 70. At
every Daniel-format certificate the least far-wall clearance is $1/(2 \cdot 10^{20})$
plus a positive sliver, so the box at exact contact is $10^{-40}$ from refusal, as the
third route’s controls say.

My audit of the printed sides parsed every `s(n) <= v` of the thirteen claims, 86 in
all, and held each to the exact side from its packet by my readers: all 86 are the exact
side (at T-138, the witness’s side, which is the 12-place ceiling of the printed side by
construction).
Each claim prints every count of its scope and no other, except that T-135
and T-141 also print 343 and 344 as the release’s, which the text says.

Three exact identities the notes state hold: T-130’s 105 is below T-128’s by exactly
$262896871797134956129927589/(2 \cdot 10^{29})$; T-131’s 132 is below T-098’s by exactly
$84571108928763690161985083/(2 \cdot 10^{28})$; T-137’s 70 is below T-125’s by exactly
$14263000000014263/10^{26}$. T-139’s side exceeds $15/2 + 3\sqrt2$ by
$1.1743 \times 10^{-19}$ (claim: 1.17e-19). Hunt 3’s uncited 305 has exactly #488’s side
at 305 (RL-3), and the #476 packet’s retained `n175.cert` is pose for pose T-130’s 175,
so “T-130 and issue 476’s one certificate” at 175 is one certificate.

**T-146’s `regularizations`.** I recomputed each of the fifteen items from the retained
JSON beside its certificate and by my own measurement: `method` is the JSON’s `policy`
(fewest at 70, 129, 153, 236, 263, 269, 292; conservative at the other eight);
`changes.merged_rotation_groups_deg` is the largest `determined-merge` step (0.93, 2.96,
1.81, 0.67, 1.06, 0.12, 0.03 degrees; 0 where none), `straightened` the `free-angle
straighten` counts (16 at 129, 14 at 263, 4 at 269, 56 at 302, 1 at 303, else 0) and
`re_angled` the `free-angle` counts to a non-axis angle (3, 0, 0, 0, 5, 0, 8, 5, 0, 18,
11, 9, 0, 26, 0 in the entry’s order); `side: solved` at all fifteen, each JSON printing
an `S_exact` below its `S_cert`; and the `identity` measurements, by optimal assignment
under the box’s eight symmetries in binary64 and the sine of the least angle between
edge directions: `one_to_one` false exactly at 123, 129 and 292 (no symmetry pairs
nearest centres one to one), `moved` 10, 18, 15, 45, 43, 25, 80, 53, 48, 132, 54, 239,
122, 198, 19, `max_move` 0.222, 0.169, 0.074, 0.591, 0.834, 0.124, 0.065, 0.068, 0.496,
0.049, 0.088, 0.589, 0.138, 0.102, 0.135 and `max_turn_deg` 22.50, 0.43, 0.41, 0, 39.41,
0, 2.43, 0.71, 1.13, 1.22, 1.16, 4.57, 0, 2.62, 1.21, each equal to the register’s at
its printed precision.
The within-$10^{-9}$ and beyond-$10^{-1}$ counts in the notes agree too.
The third route’s nearest-centre measurement, run here, gives the same at the twelve
one-to-one counts and `unmatched` at the three others, as the entry records.
Every `identity.basis` is `source-claim`, and neither the claim nor the notes state in
the record’s own voice that a view is the same packing: the claim attributes the exact
optimum, the level-2 classification and the sampled path test to the source, and reports
the measurements as measurements.
The finders the JSONs name (Joe DeVincentis at 70; Francisco Couzo at 102, 103, 123,
236, 263, 269, 292, 302, 303; David Ellsworth at 129, 153; David W. Cantrell at 146;
none at 258, 295) are the ones the claim lists.
`check_results` holds every item to its scope, to a registered `of` no later on the
count, and to a `by` among the entry’s sources, and passes.

## Each Claim, Comparison and Scope

Every difference below was recomputed exactly from the certificates and the case
records’ `exact_form` and printed at three significant digits; the register’s figures
agree with all of them.

- **T-128.** Below its case at all eight: 105 by $5.831 \times 10^{-5}$, 108
  $3.773 \times 10^{-6}$, 127 $5.786 \times 10^{-5}$, 131 $4.466 \times 10^{-5}$, 155
  $4.259 \times 10^{-6}$, 180 $6.599 \times 10^{-4}$, 228 $9.788 \times 10^{-7}$, 306
  $4.422 \times 10^{-6}$. At 105 T-130 is smaller by $1.314 \times 10^{-3}$ and at 131
  T-136 by $1.446 \times 10^{-3}$, so the recommendation of T-128 at 108, 127, 155, 180,
  228 and 306 only is right; T-138’s witnesses lie above T-128 at 108, 127, 180 and 306
  by $8 \times 10^{-13}$ to $5.6 \times 10^{-12}$.
- **T-130.** Below its case at 84 by $1.173 \times 10^{-4}$, 86 $3.032 \times 10^{-5}$,
  105 $1.373 \times 10^{-3}$, 175 $1.744 \times 10^{-3}$, 270 $1.084 \times 10^{-3}$; at
  175 T-140 is smaller by $3.444 \times 10^{-5}$, at 270 T-140, T-136 and T-134 by
  $6.948 \times 10^{-3}$, $6.943 \times 10^{-3}$ and $2.992 \times 10^{-6}$; recommended
  at 84, 86 and 105 only, as the notes say.
- **T-131.** Below T-098 by $4.229 \times 10^{-3}$ (“4.23e-3”); T-134, T-140 and T-141
  are smaller by $1.451 \times 10^{-4}$, $1.457 \times 10^{-4}$ and
  $1.419 \times 10^{-3}$; no house move, as recorded.
- **T-134.** Below its cases by $4.374 \times 10^{-3}$ (132), $5.330 \times 10^{-6}$
  (237), $7.026 \times 10^{-6}$ (263), $1.669 \times 10^{-5}$ (267),
  $1.087 \times 10^{-3}$ (270), $2.868 \times 10^{-3}$ (303); below T-131 by
  $1.451 \times 10^{-4}$ and T-138’s print by $2.032 \times 10^{-6}$ at 132, T-138 by
  $1.334 \times 10^{-5}$ at 267, T-130 by $2.992 \times 10^{-6}$ at 270; T-140 and T-141
  smaller at 132 by $6.064 \times 10^{-7}$ and $1.274 \times 10^{-3}$; T-136 smaller at
  237, 263, 270, 303 by $6.817 \times 10^{-4}$, $7.247 \times 10^{-3}$,
  $6.940 \times 10^{-3}$, $4.378 \times 10^{-3}$; T-140 at 237 and 270 by
  $7.213 \times 10^{-4}$ and $6.945 \times 10^{-3}$; T-146 at 263 and 303 by
  $7.247 \times 10^{-3}$ and $4.378 \times 10^{-3}$. House at 267 only: right.
- **T-135.** Below the grid’s 18 at 308 by $6.901 \times 10^{-4}$; T-141 smaller by
  $1.040 \times 10^{-3}$; 343 and 344 below the grid’s 19 by $5.096 \times 10^{-3}$ and
  $4.511 \times 10^{-3}$, and below T-141’s by $1.667 \times 10^{-2}$ and
  $1.039 \times 10^{-3}$, as the notes say; not selected: right.
- **T-136.** Below its cases at all seventeen, from $1.678 \times 10^{-4}$ (307) to
  $1.119 \times 10^{-2}$ (259); below T-128 at 131 by $1.446 \times 10^{-3}$ and T-130
  at 270 by $6.943 \times 10^{-3}$; T-140 smaller at 209, 237, 270, 305 by
  $4.280 \times 10^{-7}$, $3.961 \times 10^{-5}$, $4.773 \times 10^{-6}$,
  $5.637 \times 10^{-5}$; T-146 smaller at 153, 236, 263, 269, 292, 302, 303 by
  $8.480 \times 10^{-16}$, $3.291 \times 10^{-16}$, $5.048 \times 10^{-13}$,
  $6.728 \times 10^{-16}$, $2.026 \times 10^{-13}$, $2.210 \times 10^{-17}$,
  $4.484 \times 10^{-16}$. The claim’s two exception lists are exactly those eleven
  counts, and the six recommended counts, 131, 154, 207, 232, 259 and 307, are the rest.
  The least wall clearance is exactly 0 at every count (my checker at 131; the third
  route at all seventeen), which the record’s convention admits.
- **T-137.** Below T-125 by $1.426 \times 10^{-10}$, exactly
  $14263000000014263/10^{26}$; T-146 smaller by $1.067 \times 10^{-11}$; house to T-146:
  right.
- **T-138.** The sixteen counts are exactly those where the 12-place ceiling lies below
  the case: 84, 86, 103, 105, 108, 127, 131, 132, 175, 180, 258, 267, 270, 302, 303 and
  306 (by $1.154 \times 10^{-12}$ at 258 to $4.372 \times 10^{-3}$ at 132), and the
  other fourteen in-horizon counts lie above their cases by $2.165 \times 10^{-14}$
  (238) to $3.508 \times 10^{-9}$ (263). Smallest only at 103 and 258 among the entries
  before T-146, by $1.487 \times 10^{-10}$ and $1.154 \times 10^{-12}$ below the case;
  T-146 smaller by $6.936 \times 10^{-13}$ and $4.211 \times 10^{-12}$. The 30 witnesses
  pass the third route here with 180 controls, and its nearest-centre measurements put
  the 103 witness within $2.1 \times 10^{-10}$ of Ryan Xu’s and the 258 within
  $4.3 \times 10^{-10}$ of SQUISH’s, as the credit says.
- **T-139.** Below T-125 by $9.246 \times 10^{-11}$; house at 126: right.
- **T-140.** Below its cases by $4.374 \times 10^{-3}$, $1.779 \times 10^{-3}$,
  $3.395 \times 10^{-3}$, $7.266 \times 10^{-4}$, $8.032 \times 10^{-3}$,
  $1.820 \times 10^{-3}$; the smallest at 175, 209, 237, 270, 305, with the margins the
  notes print; at 132 T-141 is smaller by $1.273 \times 10^{-3}$.
- **T-141.** Below T-098 at 132 by $5.648 \times 10^{-3}$ and below T-140, T-134, T-131
  and T-138’s print by $1.273 \times 10^{-3}$, $1.274 \times 10^{-3}$,
  $1.419 \times 10^{-3}$, $1.276 \times 10^{-3}$; at 308 below 18 by
  $1.730 \times 10^{-3}$ and T-135 by $1.040 \times 10^{-3}$; the smallest at both.
- **T-146.** The smallest at all fifteen: below the case by $5.365 \times 10^{-12}$
  (258) to $9.276 \times 10^{-3}$ (302), and below the least pending side by
  $2.210 \times 10^{-17}$ (302, T-136) to $7.817 \times 10^{-10}$ (295, the case), as
  the claim states.
- **T-129.** Its three printed sides are the certificates’ exact sides; each is above
  the case’s verified ceiling, by $1.540 \times 10^{-2}$ (105), $6.705 \times 10^{-3}$
  (130) and $1.760 \times 10^{-19}$ (292, Seth Rehwaldt’s side), so “superseded by
  smaller currently verified bounds” holds.
  For information: all three pass my checker at their stated sides, with the usual
  $1/(2 \cdot 10^{20})$ margins; the entry stays `V0`/`C0` because no replay is retained
  in the record, and its `next_rung` says so.

**No case ceiling moved.** Every case record in scope still carries its pre-pass house
(Ryan Xu’s at 70, 84, 86, 102, 103, 105, 108, 123, 126, 127, 129, 131, 146, 175, 267,
295; Gupta’s at 130, 153, 154, 180, 207, 209, 236, 237; T-098’s at 132, 259, 269, 305,
306, 307; the grid’s 18 at 308; and the rest as the entries name them), so every
“pending adoption” and every “no house moves until jlevy/squares#403 lands” statement is
right, and the superseded marks the register derives are unaffected.

## Credit

Each entry’s credit paragraph names the authors its bibliography key’s `credit` line
names, in the source’s terms: T-128 `Couzo after Xu, Chaoweeraprasit, Gupta, Ellsworth,
Daniel, Levy`; T-130 `Couzo after Xu, Daniel, Ellsworth, Levy`; T-131 `Daniel after
Couzo, Chaoweeraprasit, Levy` (Chaoweeraprasit for the n = 155 evidence update); T-134
`Couzo after Mishapolk, Chaoweeraprasit, Gupta, Xu, Daniel, Ellsworth, Levy`; T-135
`Fang after Arslanov, Mustafin, Shangitbayev, Ellsworth, Stead`, lineage `independent`;
T-136 `Chaoweeraprasit after Couzo, Xu, Goebel, Schadt, Ellsworth, Hajba, Levy`; T-137
`Deleeuw after Xu, Levy`; T-138 `Mishapolk after Stenlund, Friedman, Ellsworth,
Chaoweeraprasit, Couzo, Xu, Levy`; T-139 `Daniel after Xu, Chaoweeraprasit`, lineage
`independent`; T-140 `Couzo after Chaoweeraprasit, Mishapolk, Xu, Daniel, Ellsworth,
Levy`; T-141 `Daniel after Fang, Arslanov, Mustafin, Shangitbayev, Couzo, Levy`; T-129
`Daniel after Couzo, Levy`. Each AI-assistance disclosure is stated in the source’s own
terms, as the policy asks, and no agent is credited.

T-146 follows the owner’s decision: `Daniel after Xu, Chaoweeraprasit, Mishapolk, Levy`,
Eric Deleeuw dropped from the line and T-137 named only as the smallest side the record
held at 70; the packings are credited to their finders through `of` (T-125 at 70, 102,
123, 129, 146, 295; T-138 at 103 and 258; T-136 at the seven SQUISH counts), the
regularizer typed as `by`, which is the entry’s one source key; and epistemics.md’s own
example of the field describes exactly this entry.
The regularization at 70 is named `of: T-125` although T-137 is the nearer certificate
in side; that is the decision, measured by the stage 4 review (Deleeuw’s certificate is
Xu’s refined in place to $1.9 \times 10^{-8}$), and the notes say so.

## Significance and Novelty

The scores are of the claims and follow the rubric: `S3` for the entries that moved a
case’s best side by $10^{-6}$ to $10^{-2}$ at one or more counts when published (T-128,
T-130, T-131, T-134, T-135, T-136, T-140, T-141; and T-138, whose sides at 132, 267, 302
and 303 were the smallest known when published, by up to $4.37 \times 10^{-3}$, with
T-131 eight hours older); `S2` for precision refinements and display views at the
$10^{-17}$ to $10^{-10}$ scale (T-137, T-139, T-146, as T-098’s exact optima are); `S1`
for T-129’s custody.
Comparing each with its nearest neighbours, I keep all thirteen.
All are `previously-published` with `attribution`, each published in its source at the
pin; none claims novelty or priority, and T-139 and T-146 say the source claims none.

## Findings

**F2-1, non-blocking: T-138’s significance rationale is stale against its own claim.**
`packing/frontier/results.yaml`, T-138, `significance.rationale`, says the sides are
“still at 103 (1.49e-10 below the case) and 258 (1.15e-12)” the smallest known, while
the entry’s claim and notes record that T-146 is smaller at both (by
$6.94 \times 10^{-13}$ and $4.21 \times 10^{-12}$, recomputed here).
A reader of the rationale alone would take T-138 to hold the smallest side at 103 and
258\. The score is unaffected (a score follows the claim, not the frontier).
Fix: replace “and still at 103 (1.49e-10 below the case) and 258 (1.15e-12), each an
earlier packing refined” with “and, until Evan Daniel’s regularized certificates of 10
October (T-146), at 103 (1.49e-10 below the case) and 258 (1.15e-12), each an earlier
packing refined”.

**F2-2, non-blocking, already addressed in the working tree: the scores were drafts that
did not say so.** At `aeb8a7219` the `significance.by` of T-128, T-130, T-131, T-134,
T-135, T-136, T-137, T-139, T-140 and T-141 named the registering lane without saying
draft, and only T-138 said so and only T-146 named a review, although epistemics.md
(Significance and Novelty) says a score set at registration is a draft, `by` says so,
and the reviewing lane keeps or changes it and `by` then names that review.
While this review was being written, the grading lane (F3) rewrote all of them in the
working tree: `scored` is now `'2026-10-11'` and `by` names its review
(`review-2026-10-11-final-asymptotic-and-grading.md`) as confirming each draft, with
T-128’s and T-130’s rationales restated with their ranges below the case ceilings,
`9.79e-07 to 6.60e-04` and `3.03e-05 to 1.74e-03`, which this review’s own figures
reproduce. Having compared each score with its neighbours above, this review keeps all
thirteen; the coordinator may add this review’s path beside F3’s in `by`, and nothing
else is needed.

**F2-3, non-blocking: the premise programs the replays run are not all listed** (RG-9,
extended). `packing/frontier/evidence.yaml`: the confirming entries of T-128, T-130 and
T-131 (`E-couzo-451-exact-feasibility`, `E-couzo-460-followup-exact-feasibility`,
`E-evand-465-record-hunt-exact-feasibility`) list only the three deciding programs,
although their replay commands drive the kernel (`V-evand-arrangement-receipts`) and
both maintained routes read through the parser and half-angle conversion
(`V-evand-exact-certificates`); the eight later confirming entries
(`E-couzo-476-exact-feasibility`, `E-fang-484-exact-feasibility`,
`E-squish-481-exact-feasibility`, `E-deleeuw-483-exact-feasibility`,
`E-mishapolk-470-exact-feasibility`, `E-evand-trio126-exact-feasibility`,
`E-couzo-488-exact-feasibility`, `E-evand-489-exact-feasibility`) list the kernel and
the importer but not `V-evand-exact-certificates`, which only
`E-evand-regularized-exact-feasibility` lists.
The packet modules `couzo_refinement_reports`, `couzo_followup_reports` and
`evand_hunt_reports` are registered as no verifier.
Nothing of the mathematics turns on it; the record’s rule is that every entry that names
a replay lists its programs.
Fix: add `V-evand-exact-certificates` to the `verifiers` of those eleven entries and
`V-evand-arrangement-receipts` to the three of T-128, T-130 and T-131; optionally
register the three packet modules as `role: premises` verifiers and list each on its
entry.

**F2-4, non-blocking, for information: T-129’s certificates pack.** This review’s
checker accepts the three retained certificates of T-129 at their stated sides (walls
$1/(2 \cdot 10^{20})$, pairs $10^{-20}$, about 3 CPU-seconds in all).
No record change is proposed: the entry is `V0`/`C0` because no replay is retained,
every side is above its case’s ceiling, and its `next_rung` already calls such a replay
optional. If the owner ever wants the rung, the maintained kernel would do it for well
under a minute.

## Verdict per Result

| Result | Verdict | Grounds |
| --- | --- | --- |
| T-128 | accepted, `V3`/`C3` | eight certificates; the third route and my checker (105) agree with both maintained routes; claims, comparisons, credit right |
| T-129 | accepted as recorded, `V0`/`C0` | printed sides are the certificates’; custody only; F2-4 for information |
| T-130 | accepted, `V3`/`C3` | five; the third route and my checker (84) agree; claims, comparisons, credit right |
| T-131 | accepted, `V3`/`C3` | one; kernel replayed here (6 jobs equal), third route and my checker agree |
| T-134 | accepted, `V3`/`C3` | six; third route and my checker (132, 263) agree; claims, comparisons, credit right |
| T-135 | accepted, `V3`/`C3` at 308 | three; 343 and 344 verified beyond-horizon rows, superseded by T-141’s |
| T-136 | accepted, `V3`/`C3` | seventeen; contact with the closed box is the right notion; claims, exceptions, credit right |
| T-137 | accepted, `V3`/`C3` | one; kernel replayed here (3 jobs equal); exact identity holds |
| T-138 | accepted, `V3`/`C3` | thirty witnesses on the third route, my checker at 103 and 258; the bound rests on the exact witness; F2-1 wording |
| T-139 | accepted, `V3`/`C3` | one; kernel replayed here (3 jobs equal); closed-form offset holds |
| T-140 | accepted, `V3`/`C3` | six; kernel replayed here (27 jobs), third route and my checker (305) agree |
| T-141 | accepted, `V3`/`C3` at 132 and 308 | four; third route and my checker (308, every pair) agree; 343 and 344 verified rows |
| T-146 | accepted, `V3`/`C3` | fifteen; all fifteen `regularizations` items verified against the JSONs and by measurement; credit as the owner decided |

None reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record.
This review is a second adversarial AI review of each of the twelve `V3`/`C3` entries,
by a lane prompted separately from the stage 4 lanes; whether it counts as a distinct
reviewer under epistemics.md (“a different model family, or a separately prompted
independent lane with no shared context”) is for the owner, and the human oversight
record is still missing in any case.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, same-packing connectivity, novelty,
priority or human oversight.
No run of any source’s program.
No fetch of any source at its pin, so no re-derivation of T-138’s witnesses from the
upstream poses and no repetition of the interval receipts; the stage 4 reviews did both.
No full kernel replay of the eight receipts not named in the replay table.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
