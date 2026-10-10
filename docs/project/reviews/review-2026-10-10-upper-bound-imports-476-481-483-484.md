# Review: Four Rational Upper-Bound Imports of 9 and 10 October (#476, #481, #483, #484)

**Date:** 10 October 2026. **Verdict: accepted, for finite feasibility only.** All 27
certificates the four imports’ register entries would cite prove the upper bounds their
packets state: Francisco Couzo’s six named counts (#476), Nate Chaoweeraprasit’s
seventeen (#481), Eric Deleeuw’s n = 70 (#483) and Kevin Fang’s three (#484). Every
retained receipt reproduces here job for job, the third exact route of the
[previous review](review-2026-10-10-couzo-daniel-refinement-replays.md), extended for
these formats, agrees with both maintained routes at every number they share, and the
two packets that keep no upstream byte were held here to the upstream files they were
derived from. Seven findings are recorded, none blocking.
Each entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` when its
confirming evidence entry and this review are added; none can take `V4`/`C4` from this
review alone.

This is the stage 4 review lane (W2) of the 2026-10-10 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-fvz4`, written by an AI agent (Claude, model Opus 5.5, `claude-opus-5-5`, at the
reasoning setting its harness gave it, which the agent cannot read) prompted separately
from the import lanes that built the four packets, with no shared context.
Its relation to the results is `project`. It moves no rung, writes no register row and
adopts no house; the proposed record changes are listed at the end for the adoption
round.

## Claims Covered

| Entry | Source | Counts the entry would cite | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #476 | [Francisco Couzo, #476](https://github.com/jlevy/squares/issues/476), `franciscouzo/square-packing` at `02f9690` | 132, 237, 263, 267, 270, 303 | 12 places, each the exact side rounded up |
| T-NNN, #481 | [Nate Chaoweeraprasit, #481](https://github.com/jlevy/squares/issues/481), `itsnaka/squish-certs` at `d45669b` | 131, 153, 154, 207, 209, 232, 236, 237, 259, 263, 269, 270, 292, 302, 303, 305, 307 | the exact fraction `summary.csv` prints; the issue’s 15-digit displays are not roundings |
| T-NNN, #483 | [Eric Deleeuw, #483](https://github.com/jlevy/squares/issues/483), `ebdeleeuw/square-packing-n70` at `24221d5` | 70 | the exact side, a terminating decimal |
| T-NNN, #484 | [Kevin Fang, #484](https://github.com/jlevy/squares/issues/484), `TheSnakeFang/squarepack-certs` at `c75bebd` | 308; 343 and 344 beyond the case corpus | 15 places, each the exact side rounded up |

The exact sides are the fractions each packet’s README tabulates and its claim record
freezes: #476’s six
([README](../../../packing/resources/web/couzo-exact-certificates-2026-10-09/README.md)),
#481’s seventeen
([README](../../../packing/resources/web/squish-481-third-request-2026-10-09/README.md)),
#483’s `888096037156625096037155737/10^26`
([README](../../../packing/resources/web/ebdeleeuw-n70-refinement-2026-10-10/README.md))
and #484’s three
([README](../../../packing/resources/web/fang-two-wedge-certificates-2026-10-10/README.md)).
#476’s other 59 certificates, #481’s three `sources/` packings and the 40- to 60-digit
decimal exports are outside this review.
Construction credit stays as the packets record it.
#476 started from Mishapolk’s packing at 132 (#470), SQUISH’s at 237, 263 and 303 (237
through Siddharth Gupta), Ryan Xu’s at 267 and Evan Daniel’s at 270; #481 composes
pieces of earlier records by SQUISH’s Mondrian method; #483 refines Ryan Xu’s
arrangement; #484 belongs to the two-wedge family of Arslanov, Mustafin and
Shangitbayev, grown from David Ellsworth’s and Tej Stead’s packings.

**Read in full.** `devtools.upper_bound_reports`, and the derived-fact tests of its test
module; issue #481’s body; the kernel `evand_arrangement_reports` (`run_case`,
`validate_job`, `validate_receipt`, `replay_receipt`); the parser and conversion in
`evand_exact_certificates` (`parse`, `Pose.basis`, `basis_witness`, `ceiling_decimal`);
`sqpack.verify`’s containment test; the four packet READMEs, import declarations,
acquisition records and claim records; the #470 to #484 rows of `result-requests.yaml`;
the previous review and its third route, `devtools/check_half_angle_area.py`;
[epistemics.md](../../../epistemics.md) on review records.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 9 to 25, at most two worker processes, in a
worktree of `claude/determined-rubin-yjfy2a` at `3884e9669` with this review’s change to
the third route added.
A replay decides every job of the selected counts again through both maintained routes,
serially in one process, and compares every field of each fresh job with its retained
row except the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `couzo-exact-certificates-2026-10-09 check --replay` | #476’s 51 jobs, all 17 replayed counts | all 51 equal | 546.5 s |
| `fang-two-wedge-certificates-2026-10-10 check --replay` | #484’s 9 jobs | all 9 equal | 514.2 s |
| `ebdeleeuw-n70-refinement-2026-10-10 check --replay` | #483’s 3 jobs | all 3 equal | 4.5 s |
| `squish-481-third-request-2026-10-09 check --n 154 207 232 237 259 292 302 303 --replay` | #481’s 24 jobs at eight counts | all 24 equal | 1,084.4 s |
| `squish-481-third-request-2026-10-09 check --n 131 153 209 236 263 269 270 305 307 --replay` | #481’s 27 jobs at the other nine | all 27 equal | 1,085.4 s |
| `PACKET check-claims`, for each of the four | each frozen comparison rebuilt from the certificates and the houses’ own packets | all four rebuilt equal | 0.5 to 2.6 s each |
| `python -m devtools.check_half_angle_area decide-imports --workers 2 --upstream …` | the third route on all 27 certificates and 162 controls, every cross-check, and the derived facts against their upstream files | no disagreement | 101.5 s |

#481 was replayed in full, not sampled: its seventeen counts were split into two halves
of nearly equal recorded route CPU time (666 and 675 seconds) and run as two processes
at once. #476 ran beside #484 and then #483, and the two #481 halves after them, the
first starting six seconds before #476 ended.
Each wall includes the interpreter’s start.
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #476 | 51 | 1,486,686 | 338.07 | 958.00 | 99.13 |
| #481 | 51 | 3,148,314 | 1,340.82 | 2,487.87 | 208.94 |
| #483 | 3 | 14,490 | 3.31 | 3.34 | 1.12 |
| #484 | 9 | 989,562 | 307.82 | 680.92 | 87.93 |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Each certificate gives a rational side $S$ and, for each square, a
rational centre $(x, y)$ and either $t = \tan(\theta/2)$ (#476, #484, and #481 and #483
as their sources write them) or the exact rotation $(\cos\theta, \sin\theta)$ (the
derived facts of #481 and #483). The bound $s(n) \le S$ follows from four facts, each
decided by every route:

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
tolerates.

**The box is closed, and at #481 that is used.** At all seventeen #481 counts both
maintained routes and the third route find the least wall clearance exactly 0. The third
route counts 457 square-to-wall clearances that are exactly zero, from 3 to 44 at each
count, and the far wall is among those touched at every count; no clearance on any route
is negative. The record’s convention admits that contact.
`sqpack.verify` counts a corner on the wall as a container contact and passes it, and
the independent checker and the third route test containment with non-strict
inequalities. The frontier’s own grid bounds rest on it: the case ceiling #484 improves
at 308 is the $18 \times 18$ grid, whose outer squares lie on the wall, and T-060’s
$s(11)$ lower bound is stated for squares with boundary contact allowed.
The bound would also survive an open-box reading of the problem, provided $s(n)$ is read
as an infimum. The same packing lies in the open box $(-\varepsilon, S + \varepsilon)^2$
for every $\varepsilon > 0$, so the open-box infimum is at most $S$. Containment and
disjoint interiors are closed conditions on a compact set of poses, so the closed-box
minimum exists and equals that infimum.
Only a reading that demands strict containment and an attained least side together would
refuse a touching square, and under it no $s(n)$ would exist, since a packing strictly
inside a box fits a smaller one.
No two #481 squares meet: the least pair gap is $10^{-32}$, the clearance the source
states, at fifteen counts, and $3.16 \times 10^{-14}$ and $1.21 \times 10^{-14}$ at 263
and 292.

**At the other three imports the convention does not matter.** Every positive clears
every wall and every pair by a positive amount, on all three routes:

| Import | Least wall clearance | Least separating-axis gap | Least Euclidean distance (third route) |
| --- | --- | --- | --- |
| #476 | $1/(2 \cdot 10^{20})$ at 132, 237, 267, 270, 303; $10^{-15}$ at 263, the source’s rational witness | just under $10^{-20}$; $1.58 \times 10^{-12}$ at 263 | $1.000000 \times 10^{-20}$; $1.582645 \times 10^{-12}$ at 263 |
| #481 | exactly 0 at all seventeen | $10^{-32}$; $3.16 \times 10^{-14}$ at 263, $1.21 \times 10^{-14}$ at 292 | $1.000000 \times 10^{-32}$; $3.164060 \times 10^{-14}$ and $1.209007 \times 10^{-14}$ |
| #483 | $6.01 \times 10^{-13}$ | $1.20 \times 10^{-12}$ | $1.200573 \times 10^{-12}$ |
| #484 | $2^{-65} = 2.71 \times 10^{-20}$ at all three | $1.65 \times 10^{-20}$ (308), $5.03 \times 10^{-20}$ (343), $3.15 \times 10^{-20}$ (344) | $1.649991$, $5.029464$ and $3.146894 \times 10^{-20}$ |

So at #476, #483 and #484 the closed squares are pairwise disjoint and inside the open
box, and the bound holds under any of the usual conventions.
The centres of #476, #481 and #484 are stated in $[0, S]^2$; #483 states them in
$[-S/2, S/2]^2$, and its adapter moves every centre by exactly $S/2$, which the box
arithmetic needs: unmoved, every square with a negative centre coordinate would lie
outside $[0, S]^2$ and be refused.

## Adapters and Admission

Each format has one maintained adapter in `upper_bound_reports.ADAPTERS` and, for this
review, its own reader in the third route.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `evand-cert` | #476; #484’s `.cert` | header `n S`, exactly $n$ rows `x y t` of integer, fraction or plain decimal literals | comment lines |
| `squish-json` | #484’s `.cert.json`, held equal to its `.cert`; #481 at derivation | `n`, `s_exact` and `[x, y, t]` rational strings; no JSON number, duplicate key or unknown field | `s_decimal`, `note`, `phase`, `squeezed` |
| `centred-json` | #483 at derivation | `n`, `side`, `{x, y, t}` rational strings, `coordinate_system: centered`; each centre moved by $S/2$ | `schema`, `parent_side`, `dilation` |
| derived fact | #481, #483 | a rational `center-basis` Witness/v2 in $[0, S]^2$ | its `claim` prose |

The maintained routes read a derived fact through `certificate_from_witness`, which
recovers $t = s/(1 + c)$ and refuses a basis that is not that $t$’s rotation; the third
route reads the basis as stated and holds it to the unit circle.
#483’s unread labels are consistent with what is read:
$8.88096037155737 \times (1 + 10^{-12}) = 8.88096037156625096037155737$ exactly, so the
stated side already carries the stated dilation, and applying it again would decide a
different, larger packing.

**What the adapters decide, and what they do not.** Every route decides in full the
packing an adapter hands it, so a misreading cannot make a false bound pass: a misread
packing that passed would still bound $s(n)$ at its own side.
What a misreading would break is attribution, the claim that the packing is the
source’s. That rests on the adapters and on custody, and the third route’s own readers
and the upstream check below close it for every cited count.

**Admission.** A certificate is admitted only where its exact side equals the printed
side or, printed in decimals, rounds up to it at the printed places.
#476’s six sides round up to their 12-place prints and #484’s three to their 15-place
prints; #483 prints its side exactly.
#481 is admitted differently, and has to be: the issue’s 15-digit displays, and each
certificate’s `s_decimal`, are not roundings of the exact side.
They differ from it by up to $1.84 \times 10^{-15}$ in both directions, and at 131, 153,
154, 207, 263, 269, 305 and 307 the display lies below the exact side, so `s(n) <=` that
display would be unproved.
Each #481 side is admitted by equality to the exact fraction its source’s `summary.csv`
prints, and each register-plan claim states that fraction.
The third route holds every plan claim, at all 27 counts, to the exact side.

## Derived-Fact Custody

#481 and #483 state no licence, and their packets keep no upstream byte.
`derive` read each certificate from a Git checkout at the pin once
`acquire_source.acquire` showed that the checkout yields the packet’s own acquisition
record and manifest, and wrote the certificate as a derived fact naming the pinned
SHA-256. Offline, `read_fact` holds each fact to its own rebuild: a well-formed witness
that names the file the packet pins.
Nothing retained binds a fact to the bytes it was derived from, and `derive --check`
needs a checkout (RI-2).

For this review the 17 #481 certificates, #481’s `summary.csv` and #483’s
`certificate.json` were fetched over HTTPS from `raw.githubusercontent.com` at the
pinned commits into scratch space, outside the repository, and read as data.
All 19 files have the SHA-256 their packet pins.
`decide-imports --upstream` then read each certificate with the third route’s own SQUISH
or centred-JSON reader, moving #483’s centres by $S/2$, and found each exactly the
packing its fact states: side, every centre and every rotation.
Each of #481’s seventeen offered fractions is a cell of `summary.csv`’s row for its
count. That binds the facts to the pinned bytes, and #481’s admission to the file the
issue points to, as of this date; it is the 35 upstream checks in the command table, 17
certificates and 17 printed sides for #481 and one certificate for #483.

#476 also states no licence; its packet retains the certificates as factual data under
the owner decision of 9 October, and `acquire_source.check` binds each to its Git blob
at the pin. #484’s certificates are released under CC0 1.0 and retained.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; at #476 the issue states its author also ran this `verify.py` | the adapters, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same adapters, parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (proposed V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `sqpack.yamlio` for the facts; `json`, `csv`, `gzip`, `hashlib` | `Fraction` and the formats’ meaning only |

`upper_bound_reports` owns custody, the adapters, admission, the claim comparison and
the job layout; the kernel owns the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on each packet’s own admission (`acquire_source.check`,
and for the facts `read_fact`), which the third route calls before it reads anything and
from which it decides nothing.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the sources’ own checkers ran: Daniel’s `verify_cert.py` and Couzo’s copy of
`verify.py` (#476), SQUISH’s `Fraction` checker and Ellsworth’s `check_packing.py`
(#481), Deleeuw’s `verify_exact.py` (#483), Fang’s `verify.py` (#484). The KKT and
no-descent statements of #476, and every local-minimum, rigidity or optimality
statement, are source reports and are not decided.
That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the four
adapters before writing the extension, so it is not a clean-room implementation; it
imports none of their parsing or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It is a second pair-deciding procedure, not a second arithmetic.
On the 27 certificates it decided 880,705 pairs, clipping 15,359, and found no overlap
and no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RD-2 of the previous
review, carried as RI-3). `validate_job` requires both routes to refuse each control, on
the complete pair count, with the negative diagnostic it was built for: a pair gap below
zero for the duplicated square, a wall clearance below zero for the square moved by
$S + 2$. In all four receipts the duplicate’s gap is exactly $-1$ and the moved square
lies 3.0 to 11.95 units outside the box, refusals a binary64 checker with a $10^{-9}$
tolerance would also make.
They show the routes can refuse, not that they decide at the $10^{-32}$ to $10^{-12}$
scale where these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate.
At #481 the far-wall control is the positive itself, since its least far-wall clearance
is 0, and the next control moves that wall $10^{-40}$ inward:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All 162 reached their required outcome.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all 27 sides and every centre and rotation equal the maintained routes’ retained
  checker inputs, and at #484 each `.cert` equals its `.cert.json` under the route’s own
  two readers;
- every side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against its print by the route’s own
  integer ceiling;
- every least wall clearance equals both maintained routes’ to every digit: exactly
  $1/(2 \cdot 10^{20})$ at five #476 counts and $10^{-15}$ at its 263, exactly $2^{-65}$
  at all three #484 counts, $6.01 \times 10^{-13}$ at #483, and exactly 0 at all
  seventeen #481 counts;
- every least Euclidean distance, from $1.000000 \times 10^{-32}$ at #481 to
  $1.582645 \times 10^{-12}$ at #476’s 263, is at least the separating-axis gap both
  maintained routes report;
- the four receipts’ totals are the numbers the packets print, and the derived facts are
  the packings their pinned upstream files state.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes each certificate against the case record
as it stood at `main` `657cc4861` and against every other report pending there, each
case ceiling rebuilt from its holder’s own retained packet; `check-claims` rebuilt all
four equal. The comparisons the adoption table below needs are all in them: at 131 #481
against T-128 and #470; at 132 #476 against T-131 and #470; at 237, 263, 270 and 303
#481 and #476 against each other; at 267 #476 against #470; at 270 also T-130. At 343
and 344 there is no case record, and the certificates are compared with the grid’s 19
and with Mishapolk’s README prints, 19.000000000007 and 19.002369297056.

One comparison rests on a model the data does not fit (RI-1). #476’s declaration names
#481 by its printed 15-digit displays with rounding `unstated`, which the comparison
reads as within one unit in the last place of the exact side.
At 259, 263, 270, 292 and 307 the display lies $1.06$ to $1.84$ units from it.
No relation changes: the nearest pair of sides compared that way, at 307, differs by
$1.68 \times 10^{-4}$. #481’s own declaration names #476 by its retained packet and
compares exactly.

## Findings

**RI-1, non-blocking: #476 compares #481 by displays that are not within the span it
assumes.** As above.
When #476’s claim record is next written, its declaration should name #481 by a `HOUSES`
reader of its retained packet, as #481’s names #476, rather than by the displays.

**RI-2, non-blocking: no retained check binds a derived fact to its upstream bytes.**
`read_fact` proves each fact well formed and self-consistent; `derive --check` needs a
Git checkout at the pin.
This review closed it once, at this date, by
`check_half_angle_area decide-imports --upstream`; a later replay still rests on the
facts. The confirming evidence of #481 and #483 should cite this review for the binding.

**RI-3, non-blocking: the kernel’s controls are gross** (RD-2, unchanged).
Carrying the third route’s sharp kinds into the kernel would make each packet’s own
replay show exactness.

**RI-4, non-blocking: at #476 one maintained route is the producer’s checker.** The
issue states that the six certificates are valid under this repository’s `verify.py`. So
at #476 V-sqpack-verify reproduces with the producer’s code, as at T-128 and T-130
(RD-4), and the independently re-implemented relation rests on
V-check-rational-witness-independent and the third route.
At #481, #483 and #484 no maintained route is the producer’s.

**RI-5, non-blocking for this claim: no private-worker custody at any of the four.** The
rung for finite feasibility does not need it; the Gupta and Ry-Xu house adoptions closed
it first, so the adoption round should close it before any house moves (RD-5).

**RI-6, non-blocking: #484’s 343 and 344 lie beyond the case corpus.** Its register
entry can cite only 308. The two dated beyond-horizon rows in `source-coverage.yaml` can
take `assurance: verified` from the same evidence, keeping their printed values byte for
byte; each print is the exact side rounded up, so each is itself a proved bound.

**RI-7, non-blocking: the reviewer and three producers share a model family.** The
sources of #476, #481 and #484 disclose that their search, checking and submission code
was written with Claude, and this review and the third route are Claude’s. The decisions
are exact and do not depend on judgment, and the two maintained routes predate these
imports, but an error of method common to the family would not be independent across
them. `V4`/`C4` needs a second adversarial review by a distinct reviewer in any case.

## Rungs

**#476: `V3`/`C3`.** Machine-replayed here: all six cited certificates (and the eleven
others of the replayed roster) and their kernel controls on both maintained routes, and
the six with their 36 controls on the third route, with a certificate, a replay command,
a passing replay and retained controls; reviewed adversarially here.

**#481: `V3`/`C3`**, for the same reasons over seventeen certificates, 34 kernel
controls and 102 third-route controls, with the derived facts held to their upstream
files here.

**#483: `V3`/`C3`**, over n = 70, its two kernel controls and six third-route controls,
with its fact held to its upstream file here.

**#484: `V3`/`C3`** for 308, over three certificates, six kernel controls and 18
third-route controls; 343 and 344 are verified beyond-horizon rows, not register scope.

None reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling at
`main` `657cc4861` and every report pending on 2026-10-10, merged with the previous
review’s table, which this one replaces at 131, 132 and 270. Every comparison is exact
except with #470, whose 12-place values are compared as the upward roundings they state;
#470 has no exact witness.
Sides are shown rounded up at sixteen places, #470’s as printed.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | #470 | House to adopt |
| --- | --- | --- | --- | --- |
| 70 | 8.8809603717088810, Ryan Xu (T-125) | #483, 8.8809603715662510 | none | #483, Ryan Xu’s arrangement refined by Eric Deleeuw |
| 84 | 9.6980520605096981, Ryan Xu | T-130, 9.6979347990149214 | 9.697934799017 | T-130 |
| 86 | 9.8205657300098206, Ryan Xu | T-130, 9.8205354074967423 | 9.820535407499 | T-130 |
| 105 | 10.7906765754107907, Ryan Xu | T-130, 10.7893037837481589; T-128, 10.7906182681071446 | 10.789303783751 | T-130; T-128’s stays verified, not selected |
| 108 | 10.9048247851109049, Ryan Xu | T-128, 10.9048210123203565 | 10.904821012324 | T-128 |
| 127 | 11.8109366475118110, Ryan Xu | T-128, 11.8108787875891799 | 11.810878787590 | T-128 |
| 131 | 11.9511500449119512, Ryan Xu (T-125) | #481, 11.9496595880358604; T-128, 11.9511053894146775 | 11.951105389418 | #481; T-128’s stays verified, not selected |
| 132 | 11.9913278876915015, T-098 | #476, 11.9869541936403928; T-131, 11.9870993322450633 | 11.986956226066 | #476, crediting Mishapolk’s packing as its start; T-131’s stays verified |
| 153 | 12.8796793733293146, Gupta (T-127) | #481, 12.8720298490811809 | 12.879679373332 | #481 |
| 154 | 12.9265622458523470, Gupta (T-127) | #481, 12.9230702023011408 | 12.926562245853 | #481 |
| 155 | 12.9525032026045129, SQUISH (T-115) | T-128, 12.9524989440140074; Daniel’s equal side | none smaller | T-128, Daniel’s as an equal-side confirmation |
| 175 | 13.7688992766137689, Ryan Xu | T-130, 13.7671551635425492 | 13.767155163551 | T-130 |
| 180 | 13.9176534174501843, Gupta (T-127) | T-128, 13.9169935224778325 | 13.916993522482 | T-128 |
| 207 | 14.8879922583026574, Gupta (T-127) | #481, 14.8855063088416777 | 14.887992258303 | #481 |
| 209 | 14.9496179522003981, Gupta (T-127) | #481, 14.9462236544879195 | 14.949617952201 | #481 |
| 228 | 15.6046024545460570, Daniel’s exact optima | T-128, 15.6046014757296743 | none | T-128 |
| 232 | 15.7781745930520228, Daniel’s exact ceiling of the Kingbird packing (T-101) | #481, 15.7674283499418417 | none | #481; below the case’s reported Kingbird print, 15.77817459305202, too |
| 236 | 15.8678008394199166, Gupta (T-127) | #481, 15.8639557471592678 | 15.867800839421 | #481 |
| 237 | 15.9036762351891381, Gupta (T-127) | #481, 15.9029892208749656; #476, 15.9036709055806231 | 15.903676235190 | #481; then #476 |
| 259 | 16.6025684904933646, T-098 | #481, 16.5913781454976982 | none | #481 |
| 263 | 16.7404196795387766, SQUISH (T-116) | #481, 16.7331660078998839; #476, 16.7404126538191566 | 16.740419683047 | #481; then #476 |
| 267 | 16.8388319611168389, Ryan Xu (T-125) | #476, 16.8388152699482623 | 16.838828608296 | #476 |
| 269 | 16.9059670585838410, T-098 | #481, 16.9015135821891329 | none | #481 |
| 270 | 16.9378072284460292, Daniel (T-119) | #481, 16.9297801262411717; #476, 16.9367200311210158; T-130, 16.9367230228761835 | 16.936723155038 | #481; then #476, then T-130 |
| 292 | 17.5972493911564651, Rehwaldt (T-117) | #481, 17.5913781454979008 | none | #481 |
| 302 | 17.8813062180958085, SQUISH (T-116) | #481, 17.8720298490811800 | 17.881306218091 | #481 |
| 303 | 17.9203123729203498, SQUISH (T-113) | #481, 17.9130654627385328; #476, 17.9174439254942359 | 17.920312372919 | #481; then #476 |
| 305 | 17.9529594590155280, T-098 | #481, 17.9511961441473858 | none | #481 |
| 306 | 17.9634381397640029, Daniel’s exact optima | T-128, 17.9634337174914258 | 17.963433717497 | T-128 |
| 307 | 17.9810305486333107, T-098 | #481, 17.9808627840546911 | none | #481 |
| 308 | 18, the grid (`E-basic-grid-upper`; the Kingbird catalogue reports 18) | #484, 17.9993098551627480 | none | #484 |

T-098 is Evan Daniel’s exact optimum of Francisco Couzo’s packing, at 132, 259, 269, 305
and 307. #476’s certificates at 259, 269, 305 and 307, which the issue does not name,
equal the T-098 ceiling exactly and are not candidates; its certificate at 131 is
byte-identical to T-128’s. At 343 and 344 there is no case record and so no house:
#484’s sides, 18.9949035292204970 and 18.9954892754308151, are below the grid’s 19 and
below Mishapolk’s README prints, and the record keeps them as dated beyond-horizon rows
(RI-6).

Credit follows the packets.
At 153, 154, 207, 209, 236, 237, 263, 302 and 303 the case holds an earlier SQUISH
packing, directly or as refined by Siddharth Gupta, which #481 replaces, and #481
credits the earlier records its pieces came from.
At every count the earlier house stays retained as history, and the case’s reported and
verified ceilings move together.
House adoption waits for [#403](https://github.com/jlevy/squares/pull/403), which
rewrites every case record, as the coordinator recorded on `think-fvz4`, and for
private-worker custody (RI-5).

## Proposed Record Changes

For the adoption round; this review writes none of them.

- **A confirming evidence entry per import**: `E-couzo-476-exact-feasibility`,
  `E-squish-481-exact-feasibility`, `E-deleeuw-483-exact-feasibility` and
  `E-fang-484-exact-feasibility`, each `assurance: verified`, `method: exact-algebraic`,
  `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s certificates or
  facts as `certificate`, the replay commands above, `replay_status: passed`, verifiers
  V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts,
  V-upper-bound-reports and V-check-half-angle-area, this review as
  `independence_record` and as `external_review` (`informally-verified`), and
  limitations naming the shared premises, RI-3, RI-4 at #476 and RI-2 at #481 and #483.
  The scope of #484’s is 308, 343 and 344.
- **On each reported entry** (`E-couzo-476-certificate-report`,
  `E-squish-481-certificate-report`, `E-deleeuw-483-certificate-report`,
  `E-fang-484-certificate-report`): `external_review` naming this review, which makes it
  `reviewed`.
- **Two verifier entries.** V-check-half-angle-area, `role: decides`, for the third
  route as extended here; V-upper-bound-reports, `role: premises`, for the import
  module, which admits custody, adapters, admission and claim records and drives the
  kernel, and decides no geometry itself.
- **On each register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, covering all four), both test files among
  the controls, and claim, notes and `next_rung` rewritten together.
  Each claim states its bounds as the register plan writes them, the exact side as a
  fraction or terminating decimal, never #481’s displays.
- **In `source-coverage.yaml`**: the two #484 beyond-horizon rows at
  `assurance: verified`, and the confirming evidence on each import’s source entry.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the sources’ own checkers or solvers.
No review of #476’s 59 unnamed certificates, #481’s `sources/` packings or #470. No
`derive --check` from a Git checkout.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
