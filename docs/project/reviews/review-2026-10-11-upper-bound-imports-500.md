# Review: SQUISH’s Fourth Request, Nine Rational Upper-Bound Imports of 11 October (#500)

**Date:** 11 October 2026. **Verdict: accepted, for finite feasibility only.** The nine
certificates the import’s register entry would cite prove the upper bounds its packet
states: Nate Chaoweeraprasit’s SQUISH packings at n = 176, 181, 238, 239, 270, 271, 272,
304 and 305, composed by his Mondrian method from pieces of earlier packings.
The third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended to this packet, decided all nine here and agrees with both maintained routes at
every number they share; the retained receipt reproduces here job for job at the four
counts replayed, and the import lane’s own complete replay stands for the other five;
each derived fact was held here to the certificate it was derived from, fetched at the
pin. The lineage the source states was measured where the record retains the piece: each
piece reappears to the eye and not by pose.
Eight findings are recorded, none blocking.
The entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` at all
nine counts when its confirming evidence entry and this review are added; it cannot take
`V4`/`C4` from this review alone.
At 304 and 305 the bound stands and the house is Francisco Couzo’s #506, built from
these packings, once that import is reviewed.

This is the stage 4 review lane (W2) of the 2026-10-11 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-720n`, written by an AI agent (Claude, at extra-high reasoning effort, a
different model from the import lane’s) prompted separately from the import lane that
built the packet (`think-ga3m`), with no shared context beyond its committed notes and
register plan. Its relation to the result is `project`. It moves no rung, writes no
register row and adopts no house; the proposed record changes are listed at the end for
the records lane.

## Claims Covered

| Entry | Source | Counts | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #500 | [Nate Chaoweeraprasit, #500](https://github.com/jlevy/squares/issues/500), `itsnaka/squish-certs` at `aeacc6c` | 176, 181, 238, 239, 270, 271, 272, 304, 305 | the exact fraction `summary.csv` prints, admitted by equality; the issue’s 15-digit displays are the sides cut, not rounded |

The exact sides are the fractions the packet’s README tabulates and its claim record
freezes
([README](../../../packing/resources/web/squish-500-fourth-request-2026-10-11/README.md)).
Each numerator and denominator runs to about 80 digits; the register plan’s claim states
all nine as fractions, and the third route holds each plan claim equal to the exact
side. The five `sources/` certificates of the release, two of 154 and one each of 240,
272 and 305, ask for no entry and are outside this review: the packet compares each with
the case and with the filed certificate at its count, and imports none.

**What the register claim should print** (Lane A’s finding, confirmed here from the
fetched certificates): the issue’s 15-digit $S_n$ lie below `s_exact` at all nine
counts, by $3.87 \times 10^{-17}$ (304) to $9.73 \times 10^{-16}$ (271), so each is a
cut, and “$s(n) \le S_n$” with the display would be unproved; each certificate’s
`s_decimal` is not a rounding either, differing from `s_exact` by
$-1.57 \times 10^{-15}$ (305) to $+6.95 \times 10^{-16}$ (239) in both directions.
The claim must state the exact fractions, as the plan writes them, and any decimal
display must be the fraction rounded up, as the tables here show at sixteen places.
The third route’s own admission refuses each 15-digit display and admits each fraction.

**Read in full.** The import lane’s commit `56bdfb51b`: the packet’s README,
declaration, acquisition record, manifest and claim record, the nine facts, the whole
receipt, the `HOUSES` reader and the two test modules; its bead notes and register plan;
issue #500 and issue #506 as fetched here; the pinned `nNNN.cert.json` at all nine
counts, `summary.csv` and both READMEs, fetched here; the first imports review (SQUISH’s
#481, the closest precedent) and the
[#503/#504 review](review-2026-10-11-upper-bound-imports-503-504.md); the third route
and its tests; [epistemics.md](../../../epistemics.md) on review records and
significance.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 8 to 16, one worker process throughout, in a
worktree of `claude/wizardly-meitner-wqn4x3-imports` at `0ec1173c5` with the import
lane’s `56bdfb51b` merged and this review’s change to the third route added.
A replay decides every job of the selected counts again through both maintained routes,
serially in one process, and compares every field of each fresh job with its retained
row except the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`, `PACKET` = `squish-500-fourth-request-2026-10-11`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `PACKET check-claims` | each frozen comparison rebuilt from the certificate and the holders’ own packets | rebuilt equal, exit 0 | 29 s |
| `PACKET check --n 176 270 271 272 --replay` | 12 jobs at four counts: each positive, its duplicate-square and its outside-container control | all 12 equal, exit 0 | 1,070 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#500' --upstream PACKET DIR` | the third route on all nine certificates and 54 controls, every cross-check, three lineage measurements, and each fact against its upstream certificate and printed side | no disagreement, exit 0 | 285.1 s (288 s with the interpreter’s start) |

The replay ran 22:22:56Z to 22:40:46Z and the third route 22:31:20Z to 22:36:08Z. Each
wall includes the interpreter’s start.

**What was not replayed here, and why.** The other fifteen kernel jobs, at 181, 238,
239, 304 and 305, were not decided again by this review: the import lane’s full
`check --replay` of all 27 jobs took 53 minutes 41 seconds serially under load, and the
lane brief set a rule that above a load average of 10 at the start (it was 11.3) only
the 176, 270, 271 and 272 jobs are re-run.
For those five counts the record rests on the import lane’s two complete decisions of
every job, `certify` (20:39:56Z to 21:20:06Z) and its own `check --replay` (21:20:20Z to
22:14:01Z, all 27 equal), and on the third route here, which decided all nine
certificates in full and held each one’s side, every pose and both margins to the
receipt’s rows. So every certificate was decided here by at least one exact route, and
every retained job was decided twice by the import lane; the confirming evidence should
cite both runs (RX-8).

The receipt’s own totals, recomputed by the third route, are the numbers the packet
prints:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #500 | 27 | 1,743,036 | 1,253.51 | 2,322.21 | 202.56 (the duplicate-square control at 304) |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Each certificate gives a rational side $S$ and, for each square, a
rational centre $(x, y)$ in $[0, S]^2$ and $t = \tan(\theta/2)$; each derived fact
carries the exact rotation $(\cos\theta, \sin\theta)$ instead.
The bound $s(n) \le S$ follows from four facts, each decided by every route:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$; a stated basis is held to
   $c^2 + s^2 = 1$ exactly.
   The corners $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ then form a unit square.
2. **There are exactly $n$ of them.** Every reader refuses a count that differs from the
   expected one and any square beyond the $n$-th; a square listed twice would overlap
   itself and be refused.
3. **Each lies in the closed box $[0, S]^2$**: $h \le x \le S - h$ and
   $h \le y \le S - h$ with $h = (|c| + |s|)/2$, or equivalently every corner in the
   box.
4. **Interiors are pairwise disjoint**, by an edge normal that separates the two squares
   (the maintained routes) or by an intersection of area zero (the third route).

Arithmetic is exact `Fraction` arithmetic throughout; no route rounds, dilates or
tolerates. The certificates carry no guard dilation: the source states that each was
drawn from a 60-digit contact solution with a clearance of $10^{-32}$, and that is the
pair gap every route finds.

**The box is closed, and at #500 that is used, as at #481.** At all nine counts both
maintained routes and the third route find the least wall clearance exactly 0, and the
third route’s least far-wall clearance is exactly 0 too, so the control that reduces the
side to the far-wall contact is the positive itself and the next control moves that wall
$10^{-40}$ inward. The third route counts 266 square-to-wall clearances that are exactly
zero, from 10 (304) to 43 (271) at each count; no clearance on any route is negative.
The record’s convention admits that contact, as the first imports review decided for
#481 and the 11 October final review of upper bounds confirmed for T-136 (“contact with
the closed box is the right notion”): `sqpack.verify` counts a corner on the wall as a
container contact and passes it, the independent checker and the third route test
containment with non-strict inequalities, and the frontier’s own grid bounds rest on it.
The bound also survives an open-box reading of the problem with $s(n)$ read as an
infimum, since the same packing lies in $(-\varepsilon, S + \varepsilon)^2$ for every
$\varepsilon > 0$ and the closed-box minimum exists and equals that infimum.

No two squares meet.
At all nine counts the least separating-axis gap on both maintained routes and the least
Euclidean distance on the third route are $10^{-32}$ to sixteen significant digits,
above it by about $5.6 \times 10^{-49}$:

| n | Least wall clearance (all three routes) | Least pair gap (both maintained routes) | Least Euclidean distance (third route) | Wall contacts (third route) |
| --- | --- | --- | --- | --- |
| 176, 181, 238, 239, 270, 271, 272, 304, 305 | exactly 0 | $1.000000 \times 10^{-32}$ | $1.000000 \times 10^{-32}$ | 30, 30, 18, 38, 37, 43, 41, 10, 19 |

## Adapters and Admission

Each format has one maintained adapter in `upper_bound_reports.ADAPTERS` and, for this
review, its own reader in the third route.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `squish-json` | `nNNN.cert.json` at derivation; the fetched copies here | `n`, `s_exact` and `[x, y, t]` rational strings, SQUISH’s rows; no JSON number or duplicate key | `s_decimal`, `note` |
| derived fact | all nine | a rational `center-basis` Witness/v2 in $[0, S]^2$ | its `claim` prose |

The maintained routes read a derived fact through `certificate_from_witness`, which
recovers $t = s/(1 + c)$ and refuses a basis that is not that $t$’s rotation; the third
route reads the basis as stated and holds it to the unit circle.
The route’s SQUISH reader is the one written for #481 in the first imports review; the
pinned certificates carry exactly the five fields that reader and the maintained adapter
know, `n`, `s_exact`, `s_decimal`, `note` and `squares`, and nothing else.

**What the adapters decide, and what they do not.** Every route decides in full the
packing an adapter hands it, so a misreading cannot make a false bound pass.
What a misreading would break is attribution, the claim that the packing is the
source’s; that rests on the adapters and on custody, and the upstream check below closes
it for all nine counts.

**Admission.** Each certificate is admitted by equality to the exact fraction
`summary.csv` prints in its row for the count; the issue’s 15-digit displays and the
certificates’ `s_decimal` are quotations, as above.
The frozen claim record prints each side rounded up at 16 places, and the third route’s
own integer ceiling agrees at all nine.

## Derived-Fact Custody

The source states no licence, and the packet keeps no upstream byte: digests of all 67
files of the pinned scope, and nine derived facts.
`derive` read each certificate from a Git checkout at the pin once
`acquire_source.acquire` showed that the checkout yields the packet’s own acquisition
record and manifest, and wrote each as a derived fact naming the pinned SHA-256.
Offline, `read_fact` holds each fact to its own rebuild, and `derive --check` needs a
checkout (RI-2 of the first imports review).

For this review the nine `nNNN.cert.json`, `summary.csv`, the submission README and the
root README, twelve files, were fetched over HTTPS from `raw.githubusercontent.com` at
`aeacc6c124df339074f7370e1e010bb6e8c1b5ca` into scratch space, outside the repository,
and read as data at 22:24:43Z. All twelve have the SHA-256 the packet pins.
`decide-imports --upstream` then read each certificate with the third route’s own SQUISH
reader and found it exactly the packing its fact states, side, every centre and every
rotation, and found each offered fraction to be a cell of `summary.csv`’s row for its
count: the 18 upstream checks in the command table, nine certificates and nine printed
sides. That binds each fact to the pinned bytes, and the admission to the file the issue
points to, as of this date.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the adapters, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same adapters, parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `sqpack.yamlio` for the facts; `json`, `csv`, `hashlib` | `Fraction` and the format’s meaning only |

`upper_bound_reports` owns custody, the adapters, admission, the claim comparison and
the job layout; the kernel owns the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on the packet’s own admission (`acquire_source.check`,
and for the facts `read_fact`), which the third route calls before it reads anything and
from which it decides nothing.

**No maintained route is the producer’s.** The source reports that SQUISH’s own exact
`Fraction` checker and David Ellsworth’s `check_packing.py` accept all nine; neither is
a route of this record, and the source does not say it ran any route of this record.
So the independently re-implemented relation rests on both maintained routes and on the
third, as at #481, and not as at #476, #503 and #504, where the source ran a maintained
route itself.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
Neither of the source’s checkers ran, nor its solver.
That each certificate came from a 60-digit contact solution, that an hour of nearby
search and a deep squeeze moved none by more than $7 \times 10^{-7}$, and every
statement about which packing each piece came from and how it was narrowed, are source
reports and are not decided; the lineage is measured below where the record retains the
piece. That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing the extension, so it is not a clean-room implementation; it
imports none of their parsing or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It is a second pair-deciding procedure, not a second arithmetic.
On the nine certificates it decided 290,506 pairs, clipping 5,032, and found no overlap
and no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3, carried as
RX-4). `validate_job` requires both routes to refuse each control, on the complete pair
count, with the negative diagnostic it was built for.
In the receipt the duplicate’s gap is exactly $-1$ at all nine counts, and the moved
square lies 3.0 units outside the box at 181, 239 and 272 and 4.49 to 12.82 units
outside at the others, refusals a binary64 checker with a $10^{-9}$ tolerance would also
make.
They show the routes can refuse, not that they decide at the $10^{-32}$ scale where
these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate.
At #500, as at #481, the far-wall control is the positive itself, since the least
far-wall clearance is 0, and the next control moves that wall $10^{-40}$ inward:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance, here by 0 | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All 54 reached their required outcome.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all nine sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- every side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against `summary.csv`’s print by
  equality;
- every least wall clearance equals both maintained routes’ to every digit, exactly 0;
- every least Euclidean distance, $1.000000 \times 10^{-32}$, is at least the
  separating-axis gap both maintained routes report;
- the receipt’s totals are the numbers the packet prints, and each derived fact is the
  packing its pinned certificate states.

## The Claims Comparison

The packet’s `acquisition/claims.json` freezes each certificate against the case record
as it stood at `main` `3a5a91a90` and against every register entry and report pending
there, each side rebuilt from its holder’s own retained packet, except #506, which has
no packet yet and is compared at its printed 12-place sides read as the upward roundings
the issue says they are; `check-claims` rebuilt it equal.
Sides are shown rounded up at sixteen places, #506’s as printed; every margin is the
other side less this one, cut at four digits.

| n | Case ceiling, house | This certificate | Pending at the count, exact | Margin to each | Smallest |
| --- | --- | --- | --- | --- | --- |
| 176 | 13.8228756555322953, the Kingbird catalogue’s packing at Evan Daniel’s exact ceiling (T-101) | 13.8128562532770564 | none | case $1.001 \times 10^{-2}$ | this |
| 181 | 13.9537488219544025, Couzo improved by Daniel (T-098) | 13.9508195310229241 | #476’s unrequested 181, equal to the ceiling | $2.929 \times 10^{-3}$ to both | this |
| 238 | 15.9261468570109784, SQUISH’s #401 refined by Gupta (T-127) | 15.9241067853214947 | #470’s 238, 15.9261468570110000, above the case | $2.040 \times 10^{-3}$ to both | this |
| 239 | 15.9493131697276962, the same (T-127) | 15.9484433273005000 | #470’s 239, 15.9493131697280000, above the case | $8.698 \times 10^{-4}$ to both | this |
| 270 | 16.9378072284460292, Daniel (T-119) | 16.9281969933290166 | T-140 16.9297753535413596; T-136 16.9297801262411717; T-134 16.9367200311210158; T-130 16.9367230228761835; T-138 16.9367231550380000 | case $9.610 \times 10^{-3}$; T-140 $1.578 \times 10^{-3}$; T-136 $1.583 \times 10^{-3}$; T-134 $8.523 \times 10^{-3}$; T-130 and T-138 $8.526 \times 10^{-3}$ | this |
| 271 | 16.9508207926249588 (T-098) | 16.9491166878150100 | #476’s 271, equal to the ceiling | $1.704 \times 10^{-3}$ | this |
| 272 | 16.9681101457696006, Daniel (T-119) | 16.9655864748376712 | #476’s 272, 16.9681658678521584, above the case | case $2.523 \times 10^{-3}$; #476 $2.579 \times 10^{-3}$ | this |
| 304 | 17.9346500183906818 (T-098) | 17.9296570421708801 | #476’s 304, equal to the ceiling; #506 prints 17.929565946849 | case $4.992 \times 10^{-3}$; #506 smaller by at least $9.109 \times 10^{-5}$ | #506 |
| 305 | 17.9529594590155280 (T-098) | 17.9505448539256365 | T-140 17.9511397722069976 and #489’s tie of it; T-136 17.9511961441473858; #476’s 305, equal to the ceiling; #506 prints 17.950466482138 | case $2.414 \times 10^{-3}$; T-140 and #489 $5.949 \times 10^{-4}$; T-136 $6.512 \times 10^{-4}$; #506 smaller by at least $7.837 \times 10^{-5}$ | #506 |

At seven counts this certificate is the smallest exact side the record holds or has
pending, below the author’s own #481 packings at 270 and 305 and below Francisco Couzo’s
#488 refinements of them (T-140) by $1.578 \times 10^{-3}$ and $5.949 \times 10^{-4}$,
as the issue states to the digit.
At 304 and 305 Francisco Couzo’s #506 (`337078c`), imported in parallel by another lane,
prints smaller sides built from these very packings; the comparison with #506 is by its
prints rounded up, and the exact one waits for its packet (RX-6). T-146 has no row at
any of the nine counts; #501 (155, 156, 211), #503 (207), #504 (153) and #505 (146, 261)
name none of them.

## Credit and Lineage

The source asks that Nate Chaoweeraprasit be credited, using SQUISH and its Mondrian
composition method, and names the packings its pieces came from: Francisco Couzo’s
$s(127)$ (#451, T-128) and the Kingbird catalogue’s $s(5)$ in the 176; the catalogue’s
former $s(11)$, $s(19)$ and $s(182)$ in the 304, 270 and 272; SQUISH’s #401 $s(209)$ as
refined by Siddharth Gupta (T-127) in the 239; SQUISH’s #481 $s(209)$ (T-136) whole in
the 270 and the 304; and SQUISH’s own unfiled packings of 154, 240, 272 and 305 in the
rest, whose certificates the release carries in `sources/`. The packet and the register
plan record that credit line, and the bibliography key’s credit follows the record’s
earlier SQUISH entries.

**What was measured.** `patch_lineage`, added to the third route for the #503/#504
review, was run on the three pieces the record retains as whole or nearly whole
packings: for each of the eight symmetries of the parent’s box and every parent-to-child
pairing it counts the parent squares that reappear in the child under the translation
named most often, within $10^{-9}$ of a child centre (by pose) and, with the nearness
widened to a tenth of a unit for this review, to the eye.
For this it gained a reader of T-128’s retained certificates and a `near` setting.

| Piece, as the source names it | In | Placement found | Within $10^{-9}$ (exact) | Within a tenth (turned beyond a sine of $10^{-6}$) |
| --- | --- | --- | --- | --- |
| Couzo’s $s(127)$, 121 squares, a $2 \times 3$ corner of cells taken out | 176 | the 127’s box reflected in $x = L/2$, moved by $(0.0213, -0.0072)$ | 20 (1) | 115 (59) |
| SQUISH’s #481 $s(209)$, whole | 270 | the identity, moved by $(0.0482, 0.0052)$ | 99 (1) | 180 (36) |
| the same | 304 | the identity, moved by $(0.0441, 0.0178)$ | 98 (1) | 188 (43) |

**Each piece reappears to the eye and not by pose.** Within a tenth of a unit, 115 of
the 127 and 180 and 188 of the 209 land on squares of the composed packing under one
placement, which is the source’s account: 121 of the 127 used, and the 209 whole with
its seam repaired and the arrangement searched nearby.
By pose the picture is different.
The squares that land within $10^{-9}$ are upright squares at lattice positions, which
coincide under many translations (the $10^{-9}$ placements of the 209 are offset by
$0.982$ and $0.983$ along a lattice row, not by the placement the coarse count finds),
and not one tilted square of either piece keeps its pose: at a nearness of $10^{-6}$ the
209’s 61 tilted squares all miss in the 270 and the 304, and 25 of the 127’s squares in
the 176 are turned by more than a sine of $10^{-2}$. That is consistent with the
source’s method: the certificates are drawn from a 60-digit contact solution of the
composed packing, which re-equilibrates every tilted cluster against its new neighbours,
so a piece keeps its arrangement and not its coordinates.
The credit is as the source asks and is not in question; the register entry’s claim
should say that the lineage is the one the source describes and that the pieces were
measured to reappear to the eye, not by pose (RX-2).

**What was not measured.** The Kingbird catalogue’s $s(5)$ in the 176: the record holds
it as a decimal centre-angle witness of Göbel’s packing (`W-known-best-n005`), and a
scratch placement of it, not retained, found at most one of its five squares within
$10^{-2}$ of a square of the 176 and four within a tenth, three of them turned, so the
interlock is the source’s account.
The narrowed pieces, which the source says were searched toward smaller rectangles
before composition and so cannot reappear by pose: Gupta’s 209 in the 239 (89 of 209
within $10^{-9}$ in a scratch run, lattice coincidences again), the catalogue’s former
11, 19 and 182, and the unfiled 154, 240, 272 and 305 of `sources/`, which no packet
retains as facts. That the `sources/` 272 is the filed 272 before its squeeze, as the
source says, and that the 305 is two pieces of it, were not checked.

## AI Assistance

The issue states that SQUISH’s solver, its verification and the issue itself were
written with Claude Opus 5.5 for coding and research, that the Mondrian composition
method was planned, ideated and formulated by the author and then implemented with
Claude Opus 5.5, and that the SQUISH project is directed, managed, reviewed and steered
by Nate Chaoweeraprasit.
The register plan carries that statement in the entry’s claim, and #481’s entry carries
the same source’s earlier one.
As at #481 (RI-7), the producer’s assistant and this reviewer share a model family; the
decisions are exact and do not depend on judgment, the maintained routes predate the
source, and the third route’s reader of this format predates this release, but an error
of method common to the family would not be independent across them (RX-7).

## Findings

**RX-1, non-blocking: the issue’s 15-digit sides are cuts, and `s_decimal` is not a
rounding.** As under Claims Covered.
The register claim states the exact fractions; any display is the fraction rounded up.
The draft acknowledgement already tells the author.

**RX-2, non-blocking: the lineage holds to the eye and not by pose.** As under Credit
and Lineage. The entry’s claim should state the relation as the source describes it and
what was measured; “whole” at 270 and 304 is the arrangement, not the coordinates.

**RX-3, non-blocking: no retained check binds a derived fact to its upstream bytes**
(RI-2, unchanged). Closed once here, at this date, for all nine certificates and their
printed sides by `decide-imports --upstream`; a later replay still rests on the facts,
and the confirming evidence should cite this review for the binding.

**RX-4, non-blocking: the kernel’s controls are gross** (RI-3, unchanged).

**RX-5, non-blocking for this claim: no private-worker custody.** The rung for finite
feasibility does not need it; the adoption lane closes it before a house moves (RD-5,
RI-5).

**RX-6, non-blocking: at 304 and 305 the smaller sides are #506’s, compared by print.**
#506 has no packet at this date, so the packet compares its 12-place prints rounded up,
and the margins of $9.109 \times 10^{-5}$ and $7.837 \times 10^{-5}$ are lower bounds on
the true ones. The #500 entry’s scope keeps both counts: its bounds hold, #506 credits
these packings as its starting points, and the exact comparison and the house belong to
#506’s own import and review.

**RX-7, non-blocking: the reviewer and the producer’s assistant share a model family**
(RI-7, unchanged). `V4`/`C4` needs a second adversarial review by a distinct reviewer in
any case.

**RX-8, non-blocking: this review replayed four of the nine counts on the kernel.** The
other fifteen jobs rest on the import lane’s `certify` and its own complete
`check --replay`, both on 2026-10-11, and on the third route here at all nine; the
confirming evidence’s `replay` should name both runs and this one.

## Rungs

**#500: `V3`/`C3` at all nine counts.** Machine-replayed here: 12 kernel jobs at four
counts on both maintained routes, equal to their retained rows; all nine certificates
with their 54 controls on the third route, held to the receipt’s inputs and margins at
every count; the facts held to their upstream certificates and printed sides here; the
import lane’s complete replay of all 27 jobs retained; reviewed adversarially here.
At 304 and 305 the rung is of the bound, which holds; the house is #506’s once reviewed.

It does not reach `V4`/`C4`: that needs a second accepted adversarial review by a
distinct reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

For the records lane: the entry can take `V3`/`C3` on a confirming evidence entry
(`E-squish-500-exact-feasibility`) with
`relationship_to_generator: independent-implementation`, as T-136’s records it, naming
the verifiers V-sqpack-verify, V-check-rational-witness-independent,
V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area and
V-evand-exact-certificates, with this review as its `independence_record` and as the
reported entry’s `external_review`.

## Significance

The import lane drafted `S3`. Compared with the entries nearest to it: T-136 (`S3`, the
same author’s seventeen Mondrian packings, $1.68 \times 10^{-4}$ to
$1.12 \times 10^{-2}$ below the case ceilings, scored by the 11 October final reviews)
and T-140 (`S3`, six refinements, $7.27 \times 10^{-4}$ to $8.03 \times 10^{-3}$ below)
are constructions or refinements that move a case ceiling by amounts of this order; the
#503/#504 review confirmed `S3` for two single-count constructions at
$7.03 \times 10^{-3}$ and $9.67 \times 10^{-3}$. This entry is nine new arrangements,
$8.698 \times 10^{-4}$ to $1.001 \times 10^{-2}$ below the case ceilings, the smallest
pending side at seven counts, below the author’s own earlier packings at four, and the
starting point of #506 at two.
`S3` is confirmed: substantive case results at nine counts, not a citable detail.
It is not `S4`: the entry records bounds, not the method, and the method is the author’s
own, already in T-136; whether Mondrian composition, now carrying 26 record sides over
two releases and feeding #506, merits a note of its own as a reusable technique is a
question for the significance reviewers, not a reason to score the nine bounds higher.
`by` on the entry should name this review.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling at
`main` `3a5a91a90` and every report pending on 2026-10-11, each comparison exact except
with #506, compared at its prints rounded up.
Sides are shown rounded up at sixteen places.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | House to adopt |
| --- | --- | --- | --- |
| 176 | 13.8228756555322953, the Kingbird catalogue (T-101) | #500, 13.8128562532770564 | #500, Nate Chaoweeraprasit, from Couzo’s 127 and the catalogue’s 5 |
| 181 | 13.9537488219544025, T-098 | #500, 13.9508195310229241 | #500 |
| 238 | 15.9261468570109784, Gupta (T-127) | #500, 15.9241067853214947 | #500, replacing the author’s own #401 packing as refined by Gupta; T-127’s stays verified |
| 239 | 15.9493131697276962, Gupta (T-127) | #500, 15.9484433273005000 | #500, the same |
| 270 | 16.9378072284460292, Daniel (T-119) | #500, 16.9281969933290166; T-140, 16.9297753535413596; T-136, 16.9297801262411717; T-134, T-130 | #500; then T-140, then T-136 |
| 271 | 16.9508207926249588, T-098 | #500, 16.9491166878150100 | #500 |
| 272 | 16.9681101457696006, Daniel (T-119) | #500, 16.9655864748376712 | #500 |
| 304 | 17.9346500183906818, T-098 | #500, 17.9296570421708801; #506 prints 17.929565946849 | #506, Francisco Couzo from this packing, once its import is reviewed; #500 until then |
| 305 | 17.9529594590155280, T-098 | #500, 17.9505448539256365; T-140, 17.9511397722069976; T-136, 17.9511961441473858; #506 prints 17.950466482138 | #506 once reviewed, crediting #500 as its start; #500 until then; then T-140, then T-136 |

This replaces the first imports review’s table at 270 and 305, where #481 was the house
to adopt, and the #488/#489 review’s at those counts; at every other count those tables
and their successors stand.
At every count the earlier houses stay retained as history, and the case’s reported and
verified ceilings move together.
Credit follows the packet.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry**: `E-squish-500-exact-feasibility`,
  `assurance: verified`, `method: exact-algebraic`, `performed_by: repository`,
  `origin: replayed-here`, `relationship_to_generator: independent-implementation`, the
  packet’s facts as `certificate`, the replay commands above and the import lane’s
  `certify` and `check --replay` runs, `replay_status: passed`, the six verifiers named
  under Rungs, this review as `independence_record` and as `external_review`
  (`informally-verified`), and limitations naming the shared premises, RX-3, RX-4 and
  RX-8.
- **On the reported entry** (`E-squish-500-certificate-report`): `external_review`
  naming this review, which makes it `reviewed`.
- **On the register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`), both test files among the controls
  (`packing/tests/test_upper_bound_reports_500.py`,
  `packing/tests/test_check_half_angle_area.py`), the significance `by` naming this
  review, and claim, notes and `next_rung` rewritten together: the exact fractions as
  the claim (RX-1), the lineage as measured (RX-2), and the #506 relation at 304 and 305
  (RX-6).
- **In `source-coverage.yaml`**: the confirming evidence on the import’s source entry.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the source’s checkers or solver.
No decision of the five `sources/` certificates, and no measurement of the pieces the
record does not retain.
No `derive --check` from a Git checkout.
No kernel replay here of the 181, 238, 239, 304 and 305 jobs.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
