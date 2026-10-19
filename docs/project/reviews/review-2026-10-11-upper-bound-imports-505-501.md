# Review: Robert Barnett’s and Daniil Ostashev’s Rational Upper-Bound Imports of 11 October (#505, #501)

**Date:** 11 October 2026. **Verdict: accepted, for finite feasibility only.** The five
certificates the two imports’ register entries would cite prove the upper bounds their
packets state: Robert Barnett’s n = 146 and n = 261 (#505) and Daniil Ostashev’s n =
155, n = 156 and n = 211 (#501). Both retained receipts reproduce here job for job, the
third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended for Ostashev’s format and for the credit measurements below, agrees with both
maintained routes at every number they share, and every file of both pinned scopes was
fetched here at its pin and found at the digest its packet records, each certificate
read by the route’s own reader and found to be the packing the packet decides.
Barnett’s stated lineage, local refinements of Ryan Xu’s packings, was measured true
pose by pose against the exact certificates the record credits; Ostashev’s statement
that his packings were built from scratch was measured consistent, since none is a
placement of the packing its case holds or of the pending entry nearest it.
Eight findings are recorded, none blocking.
Each entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` when its
confirming evidence entry and this review are added; neither can take `V4`/`C4` from
this review alone.

This is the stage 4 review lane (W2) of the 2026-10-11 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-720n`, written by an AI agent (Claude, at extra-high reasoning effort, a
different model from the import lane’s) prompted separately from the import lane that
built the two packets (`think-dzre`, `think-e59i`), with no shared context beyond their
committed notes and register plans.
Its relation to the results is `project`. It moves no rung, writes no register row and
adopts no house; the proposed record changes are listed at the end for the records lane.

## Claims Covered

| Entry | Source | Count | How the side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #505 | [Robert Barnett, #505](https://github.com/jlevy/squares/issues/505), `RobertBarnettProjects/square-packing-research` at `2573ff5`, the issue’s pin | 146 | the issue and the README print `12.583782203951046204`; the exact side, a fraction with a 120-digit numerator, rounds up to it at 18 places |
| T-NNN, #505 | the same | 261 | `16.678779875343207747`, likewise, a 114-digit numerator |
| T-NNN, #501 | [Daniil Ostashev, #501](https://github.com/jlevy/squares/issues/501), `dostashev/square-packing` at its head `c3d17ab`, the issue naming no revision | 155 | the README at the pin prints `12.952425406958457`; the exact side, $N/(5 \cdot 10^{117})$ with a 119-digit $N$, rounds up to it at 15 places |
| T-NNN, #501 | the same | 156 | `12.979172613644427`, likewise, $N/(625 \cdot 10^{114})$ |
| T-NNN, #501 | the same | 211 | `14.996336721336316`, likewise, $N/(5 \cdot 10^{117})$ |

The packets are
[barnett-refinements-2026-10-11](../../../packing/resources/web/barnett-refinements-2026-10-11/README.md)
and
[dostashev-records-2026-10-11](../../../packing/resources/web/dostashev-records-2026-10-11/README.md).
Barnett’s tree states no licence, so his packet keeps a derived exact fact per
certificate and pins all eleven files of the tree by SHA-256; Ostashev’s is MIT-licensed
and his packet retains all 38 files of the tree byte for byte.

Three things the sources publish are outside the entries and are placed here.
The same pinned commit of #505 holds five certificates its README marks superseded, at
70, 103, 123, 237 and 295, each a refinement of a packing the record holds that a later
pending certificate beats; the author excludes them from the request, the packet replays
them beside the two requested, and they are compared below and registered nowhere.
It also holds a certificate at n = 2043, beyond the case corpus and beyond the record’s
beyond-horizon rows, which reach 379; it is pinned by digest, not requested, not
compared and not replayed, and the price of replaying it is recorded under RW-4. Issue
#501 prints the three sides of the README at `41019fb`, the head when it was filed; the
pinned head `c3d17ab` replaced all three certificates with smaller ones, and the
decision to claim the head’s sides is RW-1. The issue text of #505 speaks of “a
pre-submission refresh on 12 October” though it was filed at 14:24Z on 11 October; that
is the author’s local date or a slip, and nothing rests on it.

**Read in full.** The import lane’s commit `835dd7004`: the `sqcert` adapter and its
tests, both packets’ READMEs, declarations, acquisition records, manifests and claim
records, the seven facts, the three retained certificates and both receipts; the import
lane’s bead notes and register plans; issues #505 and #501 with their comments; both
pinned READMEs, Barnett’s `results/review-2026-10-11.json` and `quiet-2026-10-10.json`
and Ostashev’s `verify_all.sh`, `tools/crosscheck_mpmath.py` and the `verify/` sources,
fetched here and read, not run; the #503/#504 review and the first imports review with
its third route; [epistemics.md](../../../epistemics.md) on significance, and the
significance review of today
(`docs/project/reviews/review-2026-10-11-significance-scores.md`, lane S’s commit
`ca1439fca`, not yet on this branch, so not linked).

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 8 to 15, one worker process throughout, in a
worktree cut from the imports branch at `0ec1173c5` with the import lane’s `835dd7004`
merged and this review’s change to the third route added.
A replay decides every job of the packet again through both maintained routes, serially
in one process, and compares every field of each fresh job with its retained row except
the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `barnett-refinements-2026-10-11 check --replay` | #505’s 21 jobs: the seven certificates, the two requested and the five superseded, each with its two kernel controls | all 21 equal, “7 certificates and 21 jobs admitted”, exit 0 | 17 min 56 s |
| `dostashev-records-2026-10-11 check --replay` | #501’s 9 jobs | all 9 equal, “3 certificates and 9 jobs admitted”, exit 0 | 9 min 0 s |
| `PACKET check-claims`, for each | each frozen comparison rebuilt from the certificate and the holders’ own packets | both rebuilt equal as JSON (the printed layout differs from the frozen file’s) | 13 s and under 2 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#505' '#501' --upstream barnett-refinements-2026-10-11 DIR505 --upstream dostashev-records-2026-10-11 DIR501 --json OUT` | the third route on the five requested certificates and 30 controls, every cross-check, the seven credit measurements, each #505 fact against its upstream certificate, and each #501 file against its upstream bytes and the README print | no disagreement, exit 0 | 235.5 s (239 s with the interpreter’s start) |

The #505 replay ran 22:13:14Z to 22:31:10Z and the #501 replay 22:31:10Z to 22:40:10Z;
the third route ran 22:24:16Z to 22:28:15Z, beside the #505 replay.
The load was below the brief’s threshold when the replays started, so every job of both
receipts was re-run, the five superseded certificates included.
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #505 | 21 | 786,102 | 530.82 | 1,329.06 | 224.09 |
| #501 | 9 | 277,080 | 280.98 | 595.29 | 118.47 |

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
tolerates. The guards the sources speak of are already in the certificates.
Barnett’s come from an “exact rational contraction” after a floating-point solve and
state no dilation; their clearances are what the contraction left.
Ostashev’s are his 60-digit optima with the load-bearing squares scaled by
$1 + 10^{-20}$, then every centre and the side multiplied by $1 + 10^{-60}$ and each $t$
rounded to 70 places: read here and not believed, every retained side is exactly its
`claimed_s` label times $1 + 10^{-60}$, and every $t$ is a terminating decimal of at
most 70 places, some needing all 70.

**Nothing touches, so the box convention does not matter.** Every positive clears every
wall and every pair by a positive amount, on all three routes, and the third route
counts no square-to-wall clearance of exactly zero at any count:

| Import | n | Least wall clearance | Least separating-axis gap (both maintained routes) | Least Euclidean distance (third route) |
| --- | --- | --- | --- | --- |
| #505 | 146 | $3.925867 \times 10^{-14}$ | $1.206274 \times 10^{-16}$ | $1.206274 \times 10^{-16}$ |
| #505 | 261 | $4.688122 \times 10^{-14}$ | $1.206060 \times 10^{-16}$ | $1.206060 \times 10^{-16}$ |
| #501 | 155 | exactly $(10^{60} + 10^{20} + 1)/(2 \cdot 10^{80}) \approx 5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |
| #501 | 156 | the same fraction | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |
| #501 | 211 | $5.000000 \times 10^{-21}$, a tilted square’s | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |

At 155 and 156 the least wall clearance is the first corner square’s, whose centre is
$\tfrac12 + 5 \cdot 10^{-21} + 5 \cdot 10^{-61} + 5 \cdot 10^{-81}$: half the $10^{-20}$
scaling, half the $10^{-60}$ dilation, and their product.
Barnett’s margins at 146 and 261 are the ones his `results/review-2026-10-11.json`
reports as `min_wall_clearance_approx` and `min_detailed_pair_clearance_approx`, at the
same pairs, 71 and 72 at 146 and 36 and 149 at 261; here they are the routes’ own
numbers. So the closed squares are pairwise disjoint and inside the open box, and the
bound holds under any of the usual conventions.
All five certificates state their centres in $[0, S]^2$; no adapter moves anything.

## Adapters and Admission

Each format has one maintained adapter in `upper_bound_reports.ADAPTERS` and, for this
review, its own reader in the third route.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `evand-cert` | `n146.cert`, `n261.cert` at derivation; here at the pin again | the header `n S` and `n` rows `x y t`, every literal an integer, `p/q` or plain decimal | each file’s one `#` line, “Exact uniform contraction of SHA256 …”, naming a file the record does not hold; the source’s sides, differences and receipts are in `results/review-2026-10-11.json`, read as a report |
| `sqcert` (new, both routes) | `records/n0155.sqcert`, `n0156.sqcert`, `n0211.sqcert`, retained | `n N`, `s S`, then `n` rows `x y t`; blank and `#` lines skipped | the `#` header labels: `claimed_s`, `delta`, `digits`, the source file name, and the sqverify version line |
| derived fact | #505 | a rational `center-basis` Witness/v2 in $[0, S]^2$ | its `claim` prose |

The maintained `sqcert` adapter and the third route’s `parse_sqcert` are both new on
this import and were written separately: the adapter takes the labels in the order every
retained file uses and refuses the rest; the third route’s reader does the same from its
own `_data_rows` and `literal`, sharing no line with the adapter.
Both read every retained file alike, and `decide-imports` held the third route’s poses
to the maintained routes’ retained checker inputs at every count.

**Admission.** Each #505 certificate is admitted by rounding up at the 18 places the
issue prints, and the README at the pin prints the same two values, in bold cells; the
frozen claim records print each side rounded up at 16 places, $12.5837822039510463$ and
$16.6787798753432078$, and the third route’s own integer ceiling agrees.
Each #501 certificate is admitted by rounding up at the 15 places the README at the pin
prints, $12.9524254069584562$, $12.9791726136444261$ and $14.9963367213363157$ at 16;
the issue’s prints are the `41019fb` sides, above each by $2.80 \times 10^{-11}$,
$7.81 \times 10^{-11}$ and $1.57 \times 10^{-8}$, and are not the admitted ones (RW-1).

## Custody

**#505, derived facts.** The source states no licence and the packet keeps no upstream
byte. `derive` read each certificate from a Git checkout at the pin once
`acquire_source.acquire` showed that the checkout yields the packet’s own acquisition
record and manifest, and wrote it as a derived fact naming the pinned SHA-256. For this
review all eleven files of the pinned tree were fetched over HTTPS from
`raw.githubusercontent.com` at `2573ff5` into scratch space, outside the repository, and
read as data; all eleven have the SHA-256 the packet’s manifest pins.
`decide-imports --upstream` then read `n146.cert` and `n261.cert` with the third route’s
own text reader and found each exactly the packing its fact states, side, every centre
and every rotation: two upstream checks.
That binds each fact to its pinned certificate as of this date (RW-7); the five
superseded facts were not bound here, since no entry cites them.

**#501, retained bytes.** All 38 files of the pinned tree were fetched the same way at
`c3d17ab` and all 38 have the SHA-256 the manifest pins.
`decide-imports --upstream` held each retained `.sqcert` to its fetched bytes, byte for
byte, and held each offered side to the README fetched at the pin, which must equal the
retained README and print the side in the count’s row: six upstream checks, a check of
the printed table that the third route makes for retained certificates from this review
on (`printed_table_side`). The issue’s attachment of #505, `square-packing-results.zip`,
was read by the import lane and not retained; this review did not fetch it.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the adapters, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same adapters, parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `sqpack.yamlio` for the facts; `hashlib` | `Fraction` and the formats’ meaning only |

Neither source ran a route of this project.
Barnett reports four exact checks: two checkers “developed within this assisted research
project”, which the repository does not hold (“search code and run logs are currently
held outside this repository”), and Evan Daniel’s unchanged `verify_cert.py` and
`verify_cert2.py` at `268af52`, which are public and were not run here; Ellsworth’s
`check_packing.py` at tolerance $10^{-90}$ is his supplementary numerical evidence.
Ostashev reports his own C++ GMP checker `sqverify` on the shipped certificates with no
dilation and no tolerance and on certificates rebuilt from the decimal packings, and an
80-digit mpmath cross-check; both are retained in the packet and neither was built or
run here. So at both imports every route here is independently re-implemented with
respect to the producers’ verification, which is a stronger position than #503 and #504
held (RV-2).

`upper_bound_reports` owns custody, the adapters, admission, the claim comparison and
the job layout; the kernel owns the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on each packet’s own admission (`acquire_source.check`,
and for the facts `read_fact`), which the third route calls before it reads anything and
from which it decides nothing.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the sources’ programs ran.
Ostashev’s statement that each side is the exact optimum of its packing’s contact
topology, with nonnegative KKT multipliers, is a local-optimality report and is not
decided; nor is Barnett’s statement that the certificates came from a minimum-movement
sequential linear program.
That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing the extension, so it is not a clean-room implementation; it
imports none of their parsing or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It is a second pair-deciding procedure, not a second arithmetic.
On the five certificates it decided 90,695 pairs, clipping 2,035, and found no overlap
and no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3, carried as
RW-6). `validate_job` requires both routes to refuse each control, on the complete pair
count, with the negative diagnostic it was built for.
In both receipts the duplicate’s gap is exactly $-1$ and the moved square lies exactly
3.0 units outside the box, refusals a binary64 checker with a $10^{-9}$ tolerance would
also make. They show the routes can refuse, not that they decide at the $10^{-14}$,
$10^{-16}$ and $10^{-21}$ scale where these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All 30 reached their required outcome.
At 155, 156 and 211 the far-wall control shrinks the side by the same
$5 \times 10^{-21}$ the near wall shows, so the box is closed at both ends by the same
guard.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all five sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- each side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against its print by rounding up;
- each least wall clearance equals both maintained routes’ to every digit;
- each least Euclidean distance is at least the separating-axis gap both maintained
  routes report, and here equals it at six places at every count;
- the two receipts’ totals are the numbers the packets print; each #505 fact is the
  packing its pinned certificate states, and each #501 file is its upstream file and
  prints its side in the README at the pin.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes its certificates against the case record
as it stood at `main` `3a5a91a90` and against every register entry pending there, each
side rebuilt from its holder’s own retained packet; `check-claims` rebuilt both equal.
Every comparison is exact; the margins are shown at seven significant figures.

| n | Against | Exact side of the other | Relation | Margin |
| --- | --- | --- | --- | --- |
| 146 | the case ceiling, T-125 (Ryan Xu’s certificate) | $5033512911005033512911 / (4 \cdot 10^{20})$ | below | $7.356154 \times 10^{-8}$ |
| 146 | T-146 (Evan Daniel’s regularization of Ryan Xu’s packing), pending, $9.750690 \times 10^{-11}$ below T-125 | $6291891138707538440974154877957 / (5 \cdot 10^{29})$ | below | $7.346403 \times 10^{-8}$, the issue’s figure |
| 261 | the case ceiling, T-125, which is Ryan Xu’s printed $16.6787798754$ with every centre dilated by exactly $1 + 10^{-12}$ | $83393899377083393899377 / (5 \cdot 10^{21})$ | below | $7.347103 \times 10^{-11}$ |
| 261 | the undilated print $16.6787798754$, which no certificate carries |  | below | $5.679225 \times 10^{-11}$, the issue’s figure |
| 155 | the case ceiling, T-115 (SQUISH’s update) | $7291611074595605 / 562949953421312$ | below | $7.779565 \times 10^{-5}$ |
| 155 | T-128 (#451, Francisco Couzo’s refinement of SQUISH’s packing), pending | $647624947200700369098292528347 / (5 \cdot 10^{28})$ | below | $7.353706 \times 10^{-5}$, the issue’s figure |
| 156 | the case ceiling, T-098 (Evan Daniel’s exact optimum of Francisco Couzo’s packing) | $3245520674629223275519207125509 / (25 \cdot 10^{28})$ | below | $2.910085 \times 10^{-3}$, the issue’s figure |
| 211 | the case ceiling, T-098 (Evan Daniel’s exact optimum of Joost de Winter’s packing) | $7498980352483680782590502239189 / (5 \cdot 10^{29})$ | below | $1.623984 \times 10^{-3}$, the issue’s figure |

At 261 the margin below the dilated ceiling is more than the $1.67 \times 10^{-11}$ the
dilation adds, and the certificate is below the undilated print too, so it is not
padding removed; whether it is below Ryan Xu’s unpublished numerical optimum is not
decidable from anything the record holds.
No pending entry exists at 261, 156 or 211. No other report of 11 October states a side
at any of the five counts: #500 names 176, 181, 238, 239, 270 to 272, 304 and 305; #503
207; #504 153; #506 304, 305 and counts beyond the corpus.
At all five counts the certificate under review is the smallest exact side the record
holds or has pending.

**The five superseded certificates of #505**, each below its case’s ceiling and above a
pending entry, as the author says; they stay in the packet and are registered nowhere
(RW-5):

| n | Below the case ceiling by | Above the smallest pending entry by | Smallest at the count |
| --- | --- | --- | --- |
| 70 | $4.007896 \times 10^{-11}$ (T-125) | $1.132224 \times 10^{-10}$ (T-146); T-137 is $1.025510 \times 10^{-10}$ below too | T-146 |
| 103 | $1.526823 \times 10^{-11}$ (T-125) | $1.341046 \times 10^{-10}$ (T-146); T-138 $1.334110 \times 10^{-10}$ below | T-146 |
| 123 | $6.793038 \times 10^{-11}$ (T-125) | $1.459628 \times 10^{-10}$ (T-146) | T-146 |
| 237 | $5.329411 \times 10^{-6}$ (T-127) | $7.212981 \times 10^{-4}$ (T-140); T-136 $6.816849 \times 10^{-4}$ and T-134 $1.975140 \times 10^{-10}$ below | T-140 |
| 295 | $5.625622 \times 10^{-10}$ (T-125) | $2.191116 \times 10^{-10}$ (T-146) | T-146 |

The 237 was committed on 9 October at 12:49Z, before #476 (T-134) was filed; it is
$1.98 \times 10^{-10}$ above Couzo’s side there, and the author withdrew it rather than
contest it. None of the five changes a house.

## Which Sides #501 Claims

The issue prints the README’s sides at `41019fb` and names no revision; the record pins
a revision, and the import lane pinned the head, `c3d17ab`, whose three certificates are
the ones retained and decided.
**The register should claim the head’s sides**, for three reasons.
The claim of an upper-bound entry is the exact side of the certificate it cites, and the
only certificates the record holds are the head’s; the `41019fb` files were replaced and
are retained nowhere, so a claim at the issue’s sides would cite nothing the record
decided. Each issue side is above the head’s, by $2.80 \times 10^{-11}$,
$7.81 \times 10^{-11}$ and $1.57 \times 10^{-8}$, so $s(n) \le$ the head’s side implies
the issue’s bound, and claiming the smaller side loses nothing the issue stated.
And the author published the smaller sides himself, at the head the issue links, before
the record read it.
The entry’s notes should carry the issue’s three prints and the three
commits between (`662a13d`, `a31a747`, `c3d17ab`), so a reader of the issue finds the
register’s sides explained; the draft acknowledgement already asks the author to
confirm, and nothing in the verdict waits on the answer.

## Credit and Lineage

**#505.** The source credits Ryan Xu with both original layouts (#432), Evan Daniel with
the public regularization at 146 it compares with, and Robert Barnett with the
refinements, by minimum-movement sequential linear programming and exact rational
contraction, and it does not say whether the 146 started from Xu’s certificate or from
Daniel’s view. `arrangement_gap`, the third route’s credit measurement, matches each
certificate to the credited one square for square under the best of the box’s eight
symmetries and reports the largest centre move and the largest edge turn:

| Certificate | Against | Symmetry | Largest move | Moved beyond $10^{-3}$ / $10^{-2}$ / $10^{-1}$ | Turned beyond a sine of $10^{-6}$ (largest sine) |
| --- | --- | --- | --- | --- | --- |
| #505 n = 146 | T-125, Ryan Xu’s certificate | identity | $5.023 \times 10^{-2}$ | 51 / 31 / 0 | 24 ($2.089 \times 10^{-2}$, about $1.2°$) |
| #505 n = 146 | T-146, Evan Daniel’s regularized view | identity | $1.224 \times 10^{-1}$ | 40 / 29 / 3 | 24 (the same) |
| #505 n = 261 | T-125, Ryan Xu’s certificate | identity | $9.146 \times 10^{-6}$ | 0 / 0 / 0 | 62 ($2.442 \times 10^{-6}$) |

Both are Ryan Xu’s arrangements: every square pairs with its own under the identity, no
square moves beyond a tenth, and the 261 moves nothing beyond $10^{-5}$. At 146 the
certificate lies nearer Xu’s certificate than Daniel’s view, whose own regularization
slid 25 squares by up to 0.124 without turning any (T-146’s `regularizations` item); so
by pose the refinement is of Xu’s certificate, and the credit the packet proposes, Ryan
Xu for the packings and Robert Barnett for the refinements with Evan Daniel’s
regularization named at 146 as the comparison, is the measured one.
The 146 is not a precision refinement at the scale of rounding: 51 squares moved by more
than $10^{-3}$ and 24 turned by up to $1.2°$, and its side is $7.35 \times 10^{-8}$
below the side T-146’s source reports as the exact optimum of the same packing, so the
contact structure Barnett’s solver settled on is not the one Daniel solved (RW-3). The
261 is one: moves of at most $9.1 \times 10^{-6}$ and turns of at most
$2.4 \times 10^{-6}$, $5.7 \times 10^{-11}$ below the printed side.

**#501.** The README says each packing was constructed from scratch, an explicit
V-shaped tilted band at a chosen angle with aligned corner blocks chosen by an integer
program, “no existing record geometry is used”, then re-hardened on a GPU by Yohei
Nakajima’s soft-to-rigid method, polished by the fixed-angle linear program it credits
to this project, canonicalized, and solved to the exact optimum of its contact topology;
its certificates follow Ryan Xu’s construction.
The same measurement, against the case’s house and the pending entry nearest it:

| Certificate | Against | Result |
| --- | --- | --- |
| #501 n = 155 | T-115, SQUISH’s update | one to one at the identity, largest move $2.256 \times 10^{-1}$, 13 squares beyond a tenth, 50 turned, the largest by a sine of $0.457$ (about $27°$) |
| #501 n = 155 | T-128, Couzo’s refinement of the same packing | the same picture: $2.255 \times 10^{-1}$, 14 beyond a tenth, 50 turned by up to $27°$ |
| #501 n = 156 | T-098, Evan Daniel’s exact optimum of Couzo’s packing | no symmetry pairs the squares one to one |
| #501 n = 211 | T-098, Evan Daniel’s exact optimum of de Winter’s packing | no symmetry pairs the squares one to one |

None is a refinement of a credited packing.
At 155 the nearest-centre pairing exists only because every packing of this family has
aligned corner blocks at the same half-integer positions; the 24 squares that land
within $10^{-9}$ are those blocks, and the band between them is at another angle, 50
squares turned by up to $27°$. At 156 and 211 not even that holds.
The credit the packet proposes, Daniil Ostashev for the packings and certificates, is
consistent with the poses, and the author confirmed the name on the issue at 22:02Z
after the owner asked (“yea sure!”). What this review did not check about lineage: that
the band was built as the README says, and the KKT statement.

## AI Assistance

Barnett discloses OpenAI Codex assistance in the issue (“assisted the solver,
certificate/checker code, source review and preparation”) and in the README at the pin
(“with the assistance of codex”); the two project checkers he reports were “developed
within this assisted research project” and are not published.
The register should carry the disclosure as the source gives it, which the packet and
plan do. Ostashev states nothing about AI assistance anywhere in the repository or the
issue, and the issue omits the template’s section; the draft acknowledgement asks
(RW-2). Nothing in the finite-feasibility verdict turns on either: the decisions are
exact and do not depend on the authors’ assistants.
The reviewer and Barnett’s assistant are different model families; the import lane and
this reviewer are both Claude, and the import lane decided no geometry.

## Findings

**RW-1, non-blocking: #501’s issue prints the `41019fb` sides, and the register should
claim the head’s.** As above; the entry’s claim takes the three retained certificates’
sides and its notes carry the issue’s prints and the commits between.

**RW-2, non-blocking: no AI-assistance statement from #501.** The author was asked in
the draft acknowledgement; the entry says the source states nothing until he answers.

**RW-3, non-blocking: #505’s 146 is a local re-optimization, its 261 a precision
refinement.** The plan’s headline, “exact rational refinements of Ryan Xu’s packings”,
is right; the entry’s claim should state the measurement, that both match Xu’s
certificates square for square at the identity, the 261 within $9.1 \times 10^{-6}$ and
the 146 within $5.0 \times 10^{-2}$ with 24 squares turned by up to $1.2°$, nearer Xu’s
file than Daniel’s view, rather than call both precision refinements.

**RW-4, non-blocking: the n = 2043 certificate is unrequested, beyond the corpus and not
replayed.** The record’s beyond-horizon rows reach 379, so there is nothing to compare
it with; the import lane prices its three kernel jobs at about 1.7 CPU-hours from the
per-pair rate at 70, over the brief’s 30-minute single-job limit, and a derived fact
would have to be written first.
Whether a count that far outside the corpus is wanted at all is the owner’s call;
nothing here recommends it.

**RW-5, non-blocking: the five superseded certificates are no import of their own.** The
register plan’s notes call each “an import of its own”; each is beaten by a pending
entry and excluded by the author, so the records lane should say instead that they are
replayed in the packet, compared in its claim record and registered nowhere.

**RW-6, non-blocking: the kernel’s controls are gross** (RI-3, RV-4, unchanged).

**RW-7, non-blocking: no retained check binds #505’s facts to upstream bytes.**
`read_fact` proves each fact well formed and self-consistent; `derive --check` needs a
checkout; this review closed the binding once, at this date, by `decide-imports
--upstream` for the two requested certificates (RI-2, RV-3, unchanged).
#501’s bytes are bound by `acquire_source --check` offline and were held here to the
fetched tree.

**RW-8, non-blocking: #501’s README states a dilation its files do not use.** The
README’s description of `sqverify --precise --certify` says “centres and side are scaled
by $1 + \delta$ ($\delta = 10^{-30}$)”, while every shipped certificate’s header says
`delta: 1e-60` and is exactly its `claimed_s` times $1 + 10^{-60}$. Nothing here
believes either label; the author may want to align the prose with the files.
No private-worker custody exists at either import (RV-6), which the adoption lane closes
before a house moves.

## Rungs

**#505: `V3`/`C3`** at 146 and 261. Machine-replayed here: each certificate and its two
kernel controls on both maintained routes, and each certificate with its six controls on
the third route, with a certificate, a replay command, a passing replay and retained
controls; each fact held to its upstream certificate here; reviewed adversarially here.

**#501: `V3`/`C3`** at 155, 156 and 211, for the same reasons, each retained file held
to its upstream bytes and its README print here.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

**Verdict lines for the records lane.**

| n | Import | Rungs | Confirming evidence | `relationship_to_generator` | Verifiers |
| --- | --- | --- | --- | --- | --- |
| 146 | #505 | `V3`/`C3` | `E-barnett-505-exact-feasibility` | `independent-implementation`: no route here is the source’s code and the source ran none of them | V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area, V-evand-exact-certificates |
| 261 | #505 | `V3`/`C3` | the same entry | the same | the same |
| 155 | #501 | `V3`/`C3` | `E-ostashev-501-exact-feasibility` | `independent-implementation`: the source’s checker is its own C++ GMP program and mpmath script | the same six |
| 156 | #501 | `V3`/`C3` | the same entry | the same | the same |
| 211 | #501 | `V3`/`C3` | the same entry | the same | the same |

This review is each confirming entry’s `independence_record` and each reported entry’s
`external_review`.

## Significance

The import lane drafted `S2` for #505 and `S3` for #501.

**#505: `S2` confirmed.** Both certificates are optimizations of packings the record
already credits to Ryan Xu, measured above: the same arrangement at the identity, no
square moved beyond a tenth, the 261 moved by at most $9.1 \times 10^{-6}$. The record’s
line, as the significance review of today collected it and as its F-5 states it, is
drawn by kind: a packing refined or searched to a new arrangement or optimum is `S3`
(T-127, T-128, T-130), and an optimization of a packing already reported, a re-solve at
the scale of rounding or a regularization is `S2` (T-088 at $1.1 \times 10^{-5}$, T-137
at $1.4 \times 10^{-10}$, T-117, T-146). The 261 is on the `S2` side on both counts of
that line. The 146 is the closer call: $7.3 \times 10^{-8}$ is at the small end of
T-127’s band and the contact structure moved, but the arrangement did not, and T-088
holds a gain a hundred times larger at `S2` for the same reason; the entry takes one
score, and it is `S2`: a citable detail of each case, moving no theorem.
`by` should name this review.

**#501: `S3` confirmed.** Three new packings built from scratch, measured as no
placement of the packings their cases hold or have pending, $7.8 \times 10^{-5}$ to
$2.9 \times 10^{-3}$ below the case ceilings and $7.4 \times 10^{-5}$ below the pending
T-128 at 155: substantive case results at three counts, as T-136 (`S3`, new packings at
seventeen counts) and T-140 (`S3`, six) are, and unlike T-146 (`S2`, regularizations).
Not `S4`: the construction, an explicit band with integer-programmed corner blocks, is
one author’s method at three counts and its reuse is not shown.
`by` should name this review.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling at
`main` `3a5a91a90` and every report pending on 2026-10-11, each comparison exact.
Sides are shown rounded up at sixteen places.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | House to adopt |
| --- | --- | --- | --- |
| 146 | 12.5837822775125838, Ryan Xu (T-125) | #505, 12.5837822039510463; T-146, 12.5837822774150769 | #505, Robert Barnett’s refinement of Ryan Xu’s packing; then T-146, then T-125 |
| 261 | 16.6787798754166788, Ryan Xu (T-125) | #505, 16.6787798753432078 | #505, Robert Barnett’s refinement of Ryan Xu’s packing; then T-125 |
| 155 | 12.9525032026045129, SQUISH (T-115) | #501, 12.9524254069584562; T-128, 12.9524989440140074 | #501, Daniil Ostashev; then T-128, then T-115 |
| 156 | 12.9820826985168932, Couzo, improved by Evan Daniel (T-098) | #501, 12.9791726136444261 | #501, Daniil Ostashev; then T-098 |
| 211 | 14.9979607049673616, de Winter, improved by Evan Daniel (T-098) | #501, 14.9963367213363157 | #501, Daniil Ostashev; then T-098 |

At every other count the first imports review’s table and its successors stand; at the
five counts here the earlier houses stay retained as history, and the case’s reported
and verified ceilings move together.
Credit follows the packets: at 146 and 261 Ryan Xu keeps the packings and Robert Barnett
takes the refinements and certificates, with Evan Daniel’s regularization named at 146;
at 155, 156 and 211 Daniil Ostashev takes the packings and certificates, after the
methods his README credits.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry per import**: `E-barnett-505-exact-feasibility` and
  `E-ostashev-501-exact-feasibility`, each `assurance: verified`,
  `method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s facts or
  retained certificates as `certificate`, the replay commands above,
  `replay_status: passed`, the six verifiers named under Rungs, this review as
  `independence_record` and as `external_review` (`informally-verified`), and
  limitations naming the shared premises, RW-6 and RW-7.
- **On each reported entry** (`E-barnett-505-certificate-report`,
  `E-ostashev-501-certificate-report`): `external_review` naming this review, which
  makes it `reviewed`.
- **On each register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, covering both), both test files among the
  controls (`packing/tests/test_upper_bound_reports.py`,
  `packing/tests/test_check_half_angle_area.py`), the significance `by` naming this
  review, and claim, notes and `next_rung` rewritten together: for #505 the measured
  lineage (RW-3) and the five superseded certificates as retained and unregistered
  (RW-5); for #501 the head’s sides with the issue’s prints and the commits between
  (RW-1), the confirmed credit name, and the AI-assistance question (RW-2).
- **In `source-coverage.yaml`**: the confirming evidence on each import’s source entry.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of either source’s own checkers or solvers.
No decision of #505’s n = 2043 certificate, and no binding of its five superseded facts
to their upstream bytes.
No `derive --check` from a Git checkout.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
