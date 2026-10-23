# Review: Evan Daniel’s Certificate at 303 from Issue #728

**Date:** 22 October 2026. **Verdict: accepted, for finite feasibility only, with
findings on the record.** The rational certificate that Evan Daniel’s issue #728 names,
`search/packer/candidates/s303_r303w0.cert` at `evand/square-packing@f06521f`, proves
$s(303) \le S$ with
$S = 447744305431858194305431410441/25000000000000000000000000000 = 17.909772217274327772\ldots$:
303 unit squares with pairwise disjoint interiors in the closed box $[0, S]^2$, and $S$
is the side the issue claims.
No square touches a wall and no two squares touch.
The least wall clearance is exactly
$60480000000010479/10^{29} \approx 6.048 \times 10^{-13}$ (square 0 at the left wall and
square 62 at the bottom, numbered from 0), and the least pair gap is
$1.2045000000002 \times 10^{-12}$ (squares 284 and 296). A checker written for this
review decides the certificate on two exact routes that share only a reader, and agrees
with both maintained routes at every number they share.
It shares no code with them or with the source, and its author read none of them before
it decided. Sharp controls $10^{-30}$ past contact are refused by all four deciders, and
exact contact is accepted by all four.
$S$ is $1.860737955802 \times 10^{-4}$ below the house at 303, Mykhailo Polkovskyi’s
certificate of Daniil Ostashev’s packing (T-186), below every earlier report at 303 that
the record retains, and below every bound at the counts 304 to 324.

Seven findings are recorded, none blocking; two are minor.
The maintained replay reads the certificate through `devtools.evand_exact_certificates`,
whose corner construction and comment filter are the source’s checker code transcribed,
while the record says that module copies none of it (RF-1). The replay contract runs
only gross controls, against margins near $10^{-12}$ (RF-2). The packing is an
arrangement other than Ostashev’s: no symmetry of the box pairs nearest centres one to
one, 64 squares lie beyond a tenth of the house’s positions and 24 tilts are reversed.
It is also much closer to Ostashev’s packing than to T-146’s, the house before it: 180
of its 303 squares lie within $10^{-3}$ of the house’s positions, against 37 of T-146’s,
which agrees with the author’s account that the search started from Ostashev’s packing.
This review scores it S3, as T-197 at 155 is, and supports crediting the packing to Evan
Daniel, started from Ostashev’s packing.

This is the stage 4 mathematical review lane of the 22 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
issue #728, which no register entry on `main` yet records, so this review names the
result by its issue.
It was written by an AI reviewer of the Claude system family (Anthropic), strong
sub-agent tier (`tbd-strong-max`), at maximum reasoning, as lane `c-review-728-math` for
the intake coordinator `coord-intake-1021b`. The lane was prompted separately from the
triage lane and from the import lane that builds the packet, and read neither lane’s
notes.
Its relation to the result is `project`. It is read-only: it moves no rung, writes
no register row, adopts no house best packing and edits no bead.
Its programs and receipts are proposed for retention in the #728 packet’s
`review/review-2026-10-22/` (RF-6), and the proposed record changes are listed at the
end.

**For the author.** Your bound holds exactly at the side your certificate states.
Three exact decision programs that are not your code decided it: the two maintained
routes of this repository’s replay, and a checker written for this review.
Your side was the smallest reported at 303 when you reported it, $1.86 \times 10^{-4}$
below the house, and the issue’s prints of it are right.
Measured here, your packing is an arrangement other than Ostashev’s, and much closer to
it than to the house before it, as your account of the search suggests.
The findings concern this repository’s record, apart from two small points in the issue:
what “matching distance 0.266” measures (Question 1) and the citation of #501 (Question
2).

## Claim Covered

The claim is $s(303) \le S$, with $S$ the header side of the certificate, at a count
within the record’s horizon (1 to 324).

| n | Exact side $S$ | Issue’s print (rounded up at 12) | Certificate at its pin | SHA-256, Git blob |
| ---: | --- | --- | --- | --- |
| 303 | `447744305431858194305431410441/25000000000000000000000000000` | 17.909772217275 | `search/packer/candidates/s303_r303w0.cert` at `f06521f4` | `929c2acf…`, `c4bda0b` |

The side equals the issue’s fraction.
The issue’s 12-place print is $S$ rounded up, and its longer print,
17.909772217274327772…, is $S$ truncated at 18 places (`margins_728.py`,
`outputs/margins.json`). The file’s SHA-256 equals the issue’s, and its Git blob equals
the tree entry at the pin, read from a blobless clone (`outputs/custody.txt`). The
commit was authored by Evan Daniel at 17:09:55Z on 22 October, and the issue was opened
at 17:17:20Z.

**Read in full.** The issue (no comments when read) and the certificate.
After this review’s checker had decided: the source’s pipeline report `s303_r303w0.json`
and its f64 input `s303_r303w0.input.txt` at the pin (the input’s digest equals the
issue’s); the source’s two named checkers, `search/exact/verify_cert.py` and
`verify_cert2.py`; its `CREDITS.md` and `LICENSE` (MIT); and the commit message.
In the record, at `main` `cacdafc1f`: the case record `n-303.md` and the house witness
`n-303.yaml`; the claims, facts and certificates of every packet at 303; every intake
ledger; the retained Kingbird capture of 30 September and the intake sweep’s captures of
21 and 22 October (under the untracked `attic/intake/`); the case records at 304 to 324;
the significance of T-152, T-162, T-172, T-174, T-186, T-188, T-189, T-197 to T-199,
T-219 and T-221 to T-228; the registry entries `V-evand-verify-cert-py`,
`V-evand-verify-cert2-py`, `V-sqpack-verify`, `V-check-rational-witness-independent` and
`V-evand-exact-certificates`; and the replay entries of T-197, T-221, T-222 and T-224.
Of the maintained routes, after this review’s checker had decided: `upper_bound_reports`
(its module statement, `evand_cert`, `run_job`, `certify`, `decide_job`),
`evand_arrangement_reports` (`checker_input`, `job_input`, `SHARP_CONTROLS`,
`sharp_input`, `run_sharp`, `to_witness`, `run_case`, `decide_job`) and
`evand_exact_certificates` (its module statement, `Pose`, `parse`, `basis_witness`,
`corner_squares`, `decide`). Not read: the code of `sqpack/verify.py`,
`sqpack/witness.py` and `check_rational_witness_independent`.

**Disclosure.** Before writing its checker, this reviewer read the two models its brief
named: the review of Couzo’s #670, #672 and #675
(`review-2026-10-22-couzo-670-672-675.md`, pull request #725), which describes its own
checker’s design, the integer separating-axis gap and the clipping area, and the opening
of the review of Polkovskyi’s #719, for its structure.
Neither is a review of this result, and this reviewer read neither review’s programs.
The brief prescribed the same two-route design.
The issue describes the source’s two checkers in a phrase each (“separating axes”,
“polygon intersection”).

## Runs Here

Run on 22 October 2026 with CPython 3.14.7, under `nice -n 10` on a shared host, at most
two processes. The brief named `main` at `78dc902c1`. The shared checkout moved to
`cacdafc1f` (#722 merged) at 19:28Z, before every run that reads the repository.
Every file those runs read at 303 to 324, and every deciding program, is byte-identical
at the two revisions; the only inputs that differ are #719’s new claims and ledger,
neither of which has a claim at 303.

| Command | What it decides | Outcome | Time |
| --- | --- | --- | --- |
| `review_728_check.py --self-test` | the checker on 13 hand-built cases, 13 malformed inputs and 3,000 random pairs | all as expected; the 3,000 pairs, 628 of them built to touch, decided alike by both routes | 3 s |
| `run_checker.sh`, routes Z and C as two processes | the certificate | accepted on both routes, 45,753 pairs each, the decisions identical pair by pair | 0.34 and 4.81 CPU s |
| `run_maintained.sh`, the positive and the kernel’s two controls through `maintained_routes_728.py` | the certificate on `exact_verify` and `independent`, as `certify`’s child decides it | positive accepted by both, `validate_job` passed; both controls refused by both | 11.6 CPU s for the positive |
| the same, `--sharp` | the kernel’s `run_sharp` | at contact accepted at exactly 0; past it refused at exactly $-10^{-30}$, on both routes | within the above |
| `sharp_controls_728.py` | eight mutants on four deciders | every mutant as expected (The Controls) | 110 CPU s |
| `agree_728.py` | the checker’s numbers against the maintained routes and the source’s report | 13 of 13 checks equal | under 1 s |
| `margins_728.py` | the side and its prints; the margins against the record | as the issue states | 2 s |
| `identity_728.py`, and `--self-test` | poses against the house and T-146 | as tabulated below; the assignment code matches brute force on 300 instances | 2 s |

The checker ran a second time after its digest was recorded, and both receipts came out
identical apart from their timing.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors.
The certificate is one comment line, a header `n S` and $n$ rows `x y t`, each
a rational literal: a rational side, a rational centre and $t = \tan(\theta/2)$, the
issue’s “rational half-angle tangent”, so that the square’s edges run along
$u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ and $v = (-u_y, u_x)$. This review took the
format from the file and the issue.
The source’s checkers state the same map, and so does the header of the record’s earlier
Daniel certificate at 303 (T-098); both were read after the checker had decided.
The bound follows from five facts, each decided over $\mathbb{Q}$ or fixed by the
format:

1. **The rotation is on the unit circle.** For $t = p/q$, the integers $a = q^2 - p^2$,
   $b = 2pq$ and $d = q^2 + p^2$ satisfy $a^2 + b^2 = d^2$, so $(a/d, b/d)$ is a unit
   vector. Route Z checks the triple on every row; route C builds the four corners from
   the half-angle map and checks unit edges, right angles, positive orientation and
   corner mean. 171 rows have $t = 0$ and 26 have $t = 1$, a quarter turn: 197
   axis-aligned squares.
   Of the other 106, 13 lie within $10^{-10}$ degrees of an axis (eight rows have
   $t = 999999999999999/10^{15}$), two are turned by 0.062° and 0.080° (squares 167 and
   57), and 91 by more than 1°.
2. **There are exactly 303 of them.** The reader refuses any other row count (mutant
   R1).
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box if and only
   if its corners do, equivalently if its centre clears each wall by the half-extent
   $(|a| + |b|)/(2d)$. Route Z decides the second form by four integer inequalities a
   square, route C the first.
   Square 0 clears the left wall, and square 62 the bottom, by
   $6.048000000001 \times 10^{-13}$; square 69 clears the right by
   $6.075000000001 \times 10^{-13}$, and square 6 the top by
   $6.071673327316 \times 10^{-13}$. These least clearances are equal as rationals on
   the two routes, and no square touches a wall.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors if
   and only if a line parallel to an edge of one of them weakly separates them: the
   interiors meet exactly when the origin lies in the interior of their Minkowski
   difference, a convex polygon whose edges are parallel to the squares’ edges.
   So four axes decide a pair.
   Route Z decides every one of the 45,753 pairs this way, with no distance filter, and
   records each pair’s exact gap, the largest separation over the four axes.
   Route C decides every pair, again with no filter, by the exact area that one square’s
   four closed half-planes clip from the other, which is positive if and only if the
   interiors meet. Every area is 0 and every clipped polygon is empty, so no two squares
   touch, and every route Z gap is positive.
   The least gap,
   `120450000000020377549999999979562250000000010249/99999999999999900000000000000050000000000000000000000000000`
   $\approx 1.2045000000002 \times 10^{-12}$, is between squares 284 and 296, on an edge
   normal of square 284. The pair (4, 10) lies $5.0 \times 10^{-31}$ above it and the
   next, (105, 111), $3.8 \times 10^{-16}$ above.
   Route C’s exact squared Euclidean distance between squares 284 and 296 is the square
   of that gap, so their nearest points lie along that normal.
   On both routes, 695 pairs have centres within $\sqrt 2$.
5. **The side is the claim’s**, by the table above.

No route here rounds, dilates or tolerates.
Route Z never loads the `fractions` module (its run asserts so) and compares integers
with every denominator cleared: a pair’s gap is $(\max_k L_k - R)/(2 d_i d_j D_x D_y)$,
with $D_x$ and $D_y$ the products of the two centres’ denominators, $L_k$ the four
scaled projections and $R = D_x D_y (d_i d_j + |c_{ij}| + |s_{ij}|)$, where
$c_{ij} = a_i a_j + b_i b_j$ and $s_{ij} = a_i b_j - b_i a_j$ are the integer cosine and
sine of the angle between the squares.

**Status.** That the five facts imply $s(303) \le S$ is proved by the argument above.
That this certificate has the five facts is computationally verified here, by exact
arithmetic on four routes.
Everything else the source states about the packing is asserted, and the mapped table
below says which parts were measured consistent.

The certificate is, as the issue says, a dilation: its side is
$1 + 1.000025 \times 10^{-12}$ times the f64 input’s binary64 side, consistent with
scaling by $1 + 10^{-12}$ and rounding to rationals, and it exceeds the exactly dilated
binary64 side by $4.5 \times 10^{-16}$. The dilation is how the certificate was made;
the decision reads only the certificate.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`exact_verify` on `to_witness`, `V-sqpack-verify`) | unit shape, containment and every pair, by the exact separating-axis verifier the case record names | the `evand-cert` adapter (`upper_bound_reports.evand_cert`; `evand_exact_certificates.parse` and `basis_witness`), then `sqpack.witness.exact_verify` | with `independent`: the reader, the half-angle map and `Fraction`; with the source: the reader’s line filter, transcribed (RF-1) |
| `independent` (`check_squares` on `corner_squares`, `V-check-rational-witness-independent`) | the same facts, on corners | the same reader; corners from `evand_exact_certificates.Pose.corners`; `check_rational_witness_independent` | the reader and `Fraction`; with the source: the line filter and the corner construction, both transcribed (RF-1) |
| this review’s route Z (`review_728_check.py`, integers) | the triple per row, half-extent containment, every pair by four integer inequalities | its own reader and CPython integers | its reader with route C; CPython integers with all; the separating-axis method with `sqpack`; no code |
| this review’s route C (`review_728_check.py`, `Fraction`) | unit edges, right angles, orientation and corner mean; corner containment; every pair by clipped area | its own reader, corners and clipping | `Fraction` with the maintained routes; clipping area with no other route |

Two readers read the certificate here, the maintained one and this review’s, and they
read the same side and the same 303 poses: the digest of the maintained adapter’s
`checker_input`, rebuilt from this review’s reader, equals the one the maintained run
produced (`agree_728.py`). The maintained reader admits decimal literals and reads them
exactly, and skips blank and comment lines anywhere.
This review’s reader refuses decimals (mutant R2) and blank lines or comments after the
header (its self-test).
The certificate has none of these.

**What stays unchecked.** CPython’s integers are common to every route, and `Fraction`
to all but route Z. The custody of the bytes rests on the pin and on the digest the
issue states, matched here; the packet’s admission will add its own.
The source’s own runs are the source’s: its report’s `VALID` lines from `verify_cert.py`
and `verify_cert2.py`, which this review read and did not run.

**The source’s checkers.** Both are standalone, standard library only, and import
nothing. `verify_cert.py` requires each square strictly inside the open box, and each
pair whose centres lie within $\sqrt 2$ to be strictly separated along one of its four
face normals. `verify_cert2.py` decides the same pairs by vertex containment and
closed-segment intersection, with every corner strictly inside the open box.
In both, pairs with centres farther apart are separated by their circumscribed discs,
which is sound. Both are stricter than the claim needs: a contact, which the closed box
and disjoint interiors allow, fails them.
At the pin they are byte-identical to the versions the record registers as
`V-evand-verify-cert-py` and `V-evand-verify-cert2-py` (`3299ca0c…` and `55140a35…`), so
a replay of them needs no new registry version.
They share no code with this repository’s deciders.
The maintained adapter took two expressions from them (RF-1).

## The Controls

The kernel’s two controls, a duplicated square (gap $-1$) and square 0 moved outside
(clearance $-3.0000000000006048$), are refused by both maintained routes.
The margins this certificate keeps are $6.05 \times 10^{-13}$ at the walls and
$1.2045 \times 10^{-12}$ between pairs, so a route that rounded at binary64 or tolerated
$10^{-9}$ would accept the certificate and still refuse both (RF-2). This review built
eight mutants (`sharp_controls_728.py`, `outputs/sharp-controls.json`). It decided each
with both of its own routes and with both maintained routes, reached through the
`evand-cert` adapter and the kernel’s `run_case`, as `certify`’s child reaches them:

| Mutant | Expected | Both maintained routes | This review’s checker |
| --- | --- | --- | --- |
| F0: the side lowered by the least top-or-right clearance, $6.071673327316 \times 10^{-13}$ at square 6’s top | accepted, a corner on the top wall | accepted, wall clearance exactly 0 | accepted, 0 on both routes, one wall contact |
| F1: and by $10^{-30}$ more | refused on a wall | refused at exactly $-10^{-30}$ (`square 6 violates y<=s`) | refused at $-10^{-30}$ on both routes |
| N0: every square moved left by the least left clearance | accepted, contact on the left wall | accepted, clearance exactly 0 | accepted, 0, ten squares on the wall |
| N1: by that clearance $+ 10^{-30}$ | refused on a wall | refused at exactly $-10^{-30}$ (`square 0 violates x>=0`) | refused at $-10^{-30}$, ten squares |
| P0: square 296 moved along square 284’s edge normal toward it by the least gap | accepted, an exact contact | accepted, least gap exactly 0 | accepted, gap 0, the one touching pair (284, 296) on both routes |
| P1: by the gap $+ 10^{-30}$ | refused on an overlap | refused at exactly $-10^{-30}$ (`squares 284 and 296 overlap`) | refused, gap $-10^{-30}$; that pair alone has a positive clipped area |
| R1: the last row dropped | refused by both readers | `302 square rows for n = 303` | `302 square rows for n = 303` |
| R2: square 0’s $x$ written as its exact decimal | a reader difference, not a control | read exactly and accepted, the geometry unchanged | refused by the reader |

The kernel’s own `run_sharp` (`side-lowered-past-wall-contact` and
`tightest-pair-closed-past-contact`) was also run on the certificate: at contact both
maintained routes accept with the margin exactly 0, and past it both refuse at exactly
$-10^{-30}$. For F1, N1 and P1 the kernel’s `validate_job` refuses the row, because a
`positive` row must pass; the routes’ verdicts are the decision.

## Identity, Measured

Whether two certificates are the same packing is not decided here.
What is measured is how far this packing lies from the house’s and from T-146’s, the
house before Ostashev’s, under the box’s eight symmetries applied to the reference in
its own box. Three things are measured: whether nearest centres pair the squares one to
one; under the assignment that minimizes the total squared centre displacement (this
review’s own Hungarian algorithm), how many squares move beyond each threshold and how
far squares turn modulo 90°; and the bottleneck, the least largest displacement over all
one-to-one pairings (`identity_728.py`, `outputs/identity.json`). The house is read from
`witnesses/known-best/n-303.yaml`, and T-146 from its packet’s certificate.

| Against | Best symmetry | Nearest one to one | Within $10^{-6}$ | Within $10^{-3}$ | Beyond 0.1 | Beyond 0.5 | Largest move | Bottleneck | RMS | Turned beyond 1° | Tilt reversed |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| the house (T-186, Ostashev’s packing) | the identity | under no symmetry | 36 | 180 | 64 | 8 | 0.910 | 0.910 | 0.188 | 52 | 24 |
| T-146 | the transpose | under no symmetry | 37 | 37 | 114 | 45 | 1.093 | 1.042 | 0.326 | 104 | 0 |

“Tilt reversed” counts the squares that the reference tilts by more than 1° and this
packing tilts the other way, by the same angle within 1°. Against the house, the
transpose comes within $1.4 \times 10^{-4}$ of the identity’s RMS, and every other
symmetry is above 0.53. Rescaling the reference to this packing’s side about the origin
corner pairs nearest centres one to one under no symmetry either.
The largest turn against the house is 44.39°.

So the packing is not a refinement of Ostashev’s. A refinement pairs one to one with
small moves, as T-152 does with none beyond a tenth; here 64 squares move beyond a
tenth, eight beyond half a unit, and 24 tilts change sign.
It is much closer to Ostashev’s packing than to T-146’s, with 180 squares within
$10^{-3}$ of the house’s positions where only 37 are within that of T-146’s. That agrees
with the issue’s account: a search started from Ostashev’s packing, whose final move,
made on a descendant of it, reflected one of two tilted bands (“band flip”) and so
reversed that band’s tilt.
It agrees with the issue’s 91 tilted squares against 92, which hold at any threshold
from 0.1° up. The issue’s “matching distance 0.266” was not reproduced by any definition
tried here (RF-3).

## Newness in Report Order

Sides are each report’s exact side where the record retains it, and a print with a
$10^{-\text{places}}$ allowance otherwise (`margins_728.py`, `outputs/margins.json`).
The house at 303 has been T-186 since 16 October, on `main` today and when #728 was
reported: its witness side and the case record’s verified and reported exact forms are
one rational, and its print, 17.90995829106990799, is that side rounded up.

| Report | Reported | Side | $S$ below it by |
| --- | --- | --- | ---: |
| Griffin Casson, `griffcass/square-packing@82661bc` | 2026-09-24 | 17.93105636462953001 (print) | $2.128414 \times 10^{-2}$ |
| Francisco Couzo, `franciscouzo/square-packing@801915f` | 2026-09-24 | 17.928562541013548 (print) | $1.879032 \times 10^{-2}$ |
| Couzo, T-056 | 2026-09-27 | exact | $1.457704 \times 10^{-2}$ |
| Couzo, T-092 | 2026-10-03 | exact | $1.456879 \times 10^{-2}$ |
| Evan Daniel’s exact optimum, T-098 | 2026-10-05 | exact | $1.456879 \times 10^{-2}$ |
| Nate Chaoweeraprasit’s SQUISH #401, T-113 | 2026-10-07 | exact | $1.054015 \times 10^{-2}$ |
| Polkovskyi’s #470, T-138 | 2026-10-09 | exact | $1.054015 \times 10^{-2}$ |
| Couzo’s #476, T-134 | 2026-10-09 | exact | $7.671708 \times 10^{-3}$ |
| SQUISH #481, T-136 | 2026-10-09 | exact | $3.293245 \times 10^{-3}$ |
| Couzo’s #488 | 2026-10-10 | exact | $7.593458 \times 10^{-3}$ |
| Daniel’s regularized lists, T-146 | 2026-10-10 | exact | $3.293245 \times 10^{-3}$ |
| Ostashev’s #562, T-162 | 2026-10-12 | exact | $1.860737 \times 10^{-4}$ |
| Polkovskyi’s #573 | 2026-10-12 | exact | $3.293245 \times 10^{-3}$ |
| PingYou Ltd’s PR #574, T-174 | 2026-10-13 | exact | $1.860737 \times 10^{-4}$ |
| Polkovskyi’s #593 | 2026-10-14 | exact | $1.860737 \times 10^{-4}$ |
| Polkovskyi’s KKT refinements, T-186, the house | 2026-10-14 | exact | $1.860737955802 \times 10^{-4}$ |
| Kingbird, David Ellsworth’s catalogue | captures of 30 September, 21 and 22 October | 17.93125509556197 (print) | $2.148287 \times 10^{-2}$ |

No intake ledger through the 22 October passes holds a report at 303 after T-186, and
issues and pull requests #720 to #727 and #729 make no claim at 303. The 22 October
Kingbird capture, taken at 18:42Z, after the issue, still lists 17.93125509556197. This
lane did not sweep the live heads of the watched repositories.

**Later counts.** Deleting squares from a packing of $m$ leaves a packing of any smaller
count in the same box, so $s(303) \le s(m)$ for $m > 303$, and a side is new only if it
is below every bound at every later count.
$S$ is below the verified and the reported upper bound at every count from 304 to 324 on
`main`, all 42 decided exactly; the least margin is $1.965554 \times 10^{-2}$, at 304’s
verified bound. Beyond 324 every bound is at least $\sqrt m > 18$ by area.

**The issue’s comparison.** “Best public before it 17.909958291070” is the house side
rounded up at 12 places, and “Improvement 1.86e-4” is the margin above, rounded.
The issue’s source column, “Daniil Ostashev (#501 / #562; the register)”, credits the
packing as the record does, the house being Polkovskyi’s certificate of Ostashev’s
packing. But #501 reports 155, 156 and 211 and makes no claim at 303 (RF-4, Question 2).

## Significance

The rubric is `epistemics.md`’s (S3, “a substantive case result”), and the score is of
the claim. The record’s line, read from its entries: refinements and new arrangements
below about $1.4 \times 10^{-5}$ are S2 (T-188 at $9.29 \times 10^{-6}$, five squares
beyond a tenth; T-199 at $1.32 \times 10^{-5}$). New arrangements and refinements to new
optima from about $2 \times 10^{-5}$ up are S3: T-224 ($3.47 \times 10^{-5}$, 15 squares
beyond a tenth), T-222 ($1.06 \times 10^{-4}$, three), T-197 ($1.64 \times 10^{-4}$),
T-221 ($1.12 \times 10^{-3}$, 15) and T-162, Ostashev’s own 303 ($3.11 \times 10^{-3}$).

**S3.** A new arrangement at 303, $1.86 \times 10^{-4}$ below the case and every report
there, found by a search started from Ostashev’s packing.
That is T-197’s case at 155 (“A new arrangement at 155, 1.64e-04 below the case and
every report, found from Ostashev’s packing”), by the same author and method at a
slightly larger margin, with 64 squares beyond a tenth against T-197’s 29 and the 15 of
T-224 and T-221. It is not S4: it moves one case’s bound by a known method, with no
reusable technique, bound family or resolved dispute.
Nor is it S5, as 303 is not a central open case.
If the registering lane’s draft differs, this score and rationale replace it.
A later certificate of this arrangement up to about $5 \times 10^{-7}$ lower, which the
source expects (RF-7), would be a refinement, S2 as T-199 is.

## Credit

The source says who did what.
The issue credits “Evan Daniel (GitHub @evand)” and says the search started from
Ostashev’s packing, through generations of descendants, crossovers and a final band
flip. The commit names Claude Opus 5.5 as co-author and says Evan Daniel approved the
record claim (“Let’s post a new record claim, found by us”). The measurement supports
that account and decides none of it.
The packing is Evan Daniel’s, and Ostashev’s packing is where its search started, as in
T-197, whose headline reads “Daniel’s smaller n155 packing, started from Ostashev’s
packing”. The house’s credit chain, Polkovskyi’s certificate of Ostashev’s packing after
PingYou Ltd’s, does not pass to this packing, which is not a certificate of the house’s.

## The Source’s and the Record’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(303) \le S$ at the header side | the certificate; the issue | **computationally verified here**: three exact programs, four exact routes, every pair decided |
| the side, its 12-place print and its 18-place truncation | the issue | **computationally verified here** |
| a dilation certificate of the f64 packing, scaled by $1 + 10^{-12}$ and rounded to rationals | the issue | **consistent with what was measured**: the side is $1 + 1.000025 \times 10^{-12}$ times the binary64 input side, and the input’s digest equals the issue’s |
| both source checkers accept it; minimum pair separation 1.2e-12 | the issue; the report | **asserted**: the checkers were read, not run. The 695 close pairs and the $1.2 \times 10^{-12}$ equal what was measured here |
| the best public bound before it is 17.909958291070, Ostashev’s (#501 / #562; the register) | the issue | **verified here against the record**, except #501 (RF-4) |
| an improvement of 1.86e-4 | the issue | **verified here** |
| a new packing, not a refinement of Ostashev’s; 91 tilted squares against 92 | the issue | **measured consistent** (Identity); 91 holds at thresholds from 0.1° up |
| matching distance 0.266, the best of the 8 box symmetries | the issue; the report | **not reproduced**; not defined in the issue (RF-3) |
| the search started from Ostashev’s packing | the issue | **asserted**; measured consistent: much closer to Ostashev’s packing than to T-146’s |
| not first-order jammed; a further descent of about 4.8e-7 predicted; local optimality unresolved | the issue; the report | **asserted**; not examined here (RF-7) |

No row claims optimality, rigidity, a local minimum or priority, and none is decided.

## Findings

Line numbers in the repository are at `cacdafc1f`; in the source, at `f06521f`.

**RF-1, minor, non-blocking: the maintained adapter transcribes two pieces of the
source’s checker code, and the record says it copies none.** The `independent` route
decides on corners from `Pose.corners` in `devtools/evand_exact_certificates.py` (lines
181–188): `(self.x + c * a - s * b, self.y + s * a + c * b)` over
`((half, half), (-half, half), (-half, -half), (half, -half))`, noted
“counter-clockwise”.
That is `corners` in the source’s `verify_cert2.py` (lines 15–17),
`(x + c * a - s * b, y + s * a + c * b)` over `((h, h), (-h, h), (-h, -h), (h, -h))`,
noted “counter-clockwise”, term for term.
The reader’s line filter, `if line.strip() and not line.lstrip().startswith("#")` (line
220), is the source checkers’ (`verify_cert.py` line 24, `verify_cert2.py` line 42). The
module statement says the source’s checkers were read before it was written and that
“nothing of theirs … is imported or copied” (lines 28–31), and
`V-evand-exact-certificates` says it “copies none of their code” (`verifiers.yaml` line
2582). The evand replay entries record `read: [specification, certificate-format]` and
`shares: []` (for example `E-evand-703-n270-exact-feasibility`, `evidence.yaml` line
39348), while their own notes say the adapter’s author read the source’s checkers.
`epistemics.md`’s ladder says that “a transcription of the producer’s definitions shares
those definitions”. No bound depends on this.
The corner expression is the format’s definition, which this review’s checker derived
without reading it and which gives the same squares, and the `sqpack` route builds its
own corners from $(c, s)$. Proposed: the #728 replay entry lists `producer-code` in
`read` and names both transcribed expressions in its independence note.
Whether the corner construction is a shared component of the `independent` route, which
would make that route `shared-components`, is the records lane’s reading of the ladder;
either way the result’s level is set by this review’s clean-room checker.
Correct the module statement and the registry note, and let a records pass align the
other evand replay entries that carry the same note.

**RF-2, minor, non-blocking: the replay contract has gross controls only.** `certify`
runs a duplicated square and a square moved outside, while this certificate keeps
$6.05 \times 10^{-13}$ at its walls and $1.2045 \times 10^{-12}$ between pairs.
A route rounding at binary64, or tolerating $10^{-9}$, would accept the certificate and
refuse both controls.
This review’s eight mutants and the kernel’s `run_sharp` pass on all four deciders.
Proposed: cite `outputs/sharp-controls.json` and `outputs/maintained-positive.json` in
the replay entry’s `limitations`, or add a slow-marked test that runs `run_sharp` on
this certificate (about 12 CPU seconds a run on the two routes), as RF-6 of the Couzo
review asks for its packets.

**RF-3, note: the issue’s “matching distance 0.266” is not defined, and its tilt count
needs a threshold.** The issue gives 0.266 as the best over the box’s eight symmetries,
and the source’s report gives 0.26601933488520296 against “store best 17.909958291070”.
No definition tried here reproduces it.
Under the best symmetry the largest move is 0.910, the bottleneck 0.910, the RMS 0.188
and the mean 0.074, and an assignment with an angle term of $1/90$ per degree gives an
RMS of 0.2617. Of the 106 rows whose $t$ is neither 0 nor 1, 13 lie within $10^{-10}$
degrees of an axis, so “91 tilted squares” holds at thresholds from 0.1° up.
Proposed: the record states the measured identity (`basis: measured`, citing
`outputs/identity.json`) and gives the threshold with any tilt count; Question 1.

**RF-4, note: the issue cites #501 for the earlier bound at 303.** #501 (11 October)
reports 155, 156 and 211. The 303 report is #562 (12 October, T-162), and the house is
T-186, Polkovskyi’s certificate of that packing.
The source’s report lists “pending:#501” among the sources of its stored best.
Proposed: the record cites #562 and T-186 and does not repeat #501; Question 2.

**RF-5, note: `verify_cert2.py`’s VALID line prints the side as a binary64.** The line
reads “inside the open box of side 17.909772217274326778”, which is `float(S)` printed
to 20 significant digits (`verify_cert2.py` line 67), $9.95 \times 10^{-16}$ below $S$.
The checker itself compares at the exact side.
The record should quote the exact side or its 12-place ceiling, never that print.

**RF-6, note, for the record: retain and register this review’s programs.** Until they
sit in a packet with their README, they are scratch files that the record cannot cite.
Proposed: the #728 packet’s `review/review-2026-10-22/`. `review_728_check.py` (decides)
and `sharp_controls_728.py` with `maintained_routes_728.py` (premise checks) belong in
`verifiers.yaml` with their independence records; `margins_728.py`, `identity_728.py`
and `agree_728.py` decide nothing.

**RF-7, note: local optimality is open by the source’s own account.** The source says
the packing is not first-order jammed, and that its corner–corner MILP predicts a
further descent of $4.75 \times 10^{-7}$ (`vv_milp_dS` in the report) which its descent
step did not realize.
The record should carry no local-minimum, KKT or rigidity statement for this packing,
and a certificate of this arrangement up to about $5 \times 10^{-7}$ lower would be a
refinement of it (Significance).

## Questions for the Author

1. What does “matching distance 0.266” measure: an assignment of squares with an angle
   term, a root mean square, or a largest displacement, and against which certificate of
   Ostashev’s packing? Measured here under the best symmetry, against Polkovskyi’s
   certificate of it (T-186), the largest centre move is 0.910 and the RMS 0.188.
2. Your comparison column cites “#501 / #562”. #501 reports 155, 156 and 211; did you
   mean #562 alone at 303?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, once the replay evidence and
this review are entered.
That needs the retained certificate, a replay command (`check --replay`), a passing
replay, retained controls refused by every route that accepted the positive, and sharp
controls refused here.
The maintained replay is independently re-implemented after reading the producer’s code
(`clean_room: false`, as the record already says), and RF-1 asks the record to say what
it took. This review’s checker is a clean-room re-implementation: before it decided, its
author had read the issue and the certificate and never the source’s checkers or the
maintained routes, and the program has not changed since.
It was written by a Claude agent, a system family the producer also used (the commit’s
co-author).
By the house rule, once the entry stands at `V3`/`C3` with this review mapped
as its accepted review, the packing is adopted at 303 and regularized in the same pull
request. It does not reach `V4`/`C4`, which need a second accepted adversarial review by
a distinct reviewer and a retained human oversight record.
The count of distinct machine methods is unchanged: every route is `exact-algebraic`,
and the clipping area is a second pair procedure within it.
No lower bound, optimum, local minimum, rigidity or priority follows.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`evidence.yaml`.** A confirming replay entry: `exact-algebraic`, `replayed-here`,
  `independent-implementation` with `clean_room: false` and `producer-code` in `read`
  (RF-1), `limitations` naming RF-2 and this review’s controls receipts, and this
  document as `external_review`. An entry for this review’s checker:
  `independent-implementation`, `coverage: full`, `clean_room: true`, `shares: []`,
  `read: [mathematics, specification, certificate-format]`,
  `overlaps_producer: system-family`.
- **`verifiers.yaml`.** Register `review_728_check.py` (decides) and
  `sharp_controls_728.py` with `maintained_routes_728.py` (premise checks), with the
  digests in `outputs/program-digests.sha256`.
- **`results.yaml`.** The new entry’s `reviews` gains this document
  (`kind: adversarial`, `reviewer_kind: ai`, `relation: project`, `verdict: accepted`).
  Its significance is S3 with the rationale above, `by` naming this review; its identity
  is `measured` (RF-3); its claim cites #562 and T-186 (RF-4) and states no
  local-minimum claim (RF-7).
- **The case record.** Adopt the packing at 303 and regularize it, by the house rule;
  T-186 stays retained as history.
- **The adapter.** Correct `evand_exact_certificates`’s module statement and
  `V-evand-exact-certificates`’s note (RF-1).

## Comparison with the Earlier Reviews

No earlier review of this result exists.
This lane read neither the triage lane’s notes nor any discussion of #728 beyond the
issue itself.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no human
oversight. No run of the source’s checkers, search or descent step, and no decision of
whether two certificates are the same packing.
No house adoption, case-record change or regularization run, and no sweep of the watched
repositories’ live heads.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
