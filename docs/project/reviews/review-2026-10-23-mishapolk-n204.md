# Review: Mykhailo Polkovskyi’s Second Certificate at 204, from Issue #719

**Date:** 23 October 2026. **Verdict: accepted, for finite feasibility only, with
findings on the record.** Mykhailo Polkovskyi claimed this rational certificate on issue
#719 (answer 3 of
[his comment of 22 October](https://github.com/jlevy/squares/issues/719#issuecomment-6350348588)):
`certificates/n204.cert` at `Mishapolk/square-packing-records@12fc4667`. It proves
$s(204) \le S$ with
$S = 14808642830513087197802415708703/10^{30} = 14.808642830513087197802415708703$: 204
unit squares with pairwise disjoint interiors in the closed box $[0, S]^2$. No square
touches a wall and no two squares touch.
The least wall clearance is exactly $5 \times 10^{-21}$, at the left wall (10 squares)
and the bottom (9), and $5.00000000068827 \times 10^{-21}$ at the right (13) and the top
(10). The least pair gap is $9.99999999999998720936\ldots \times 10^{-21}$, between
squares 63 and 84 (numbered from 0), whose exact Euclidean distance is the same number.
A checker written for this review decides the certificate on two exact routes that share
only a reader. It shares no code with the maintained routes or with the source, and it
decided before its author read any of them.
It agrees with both maintained routes at every number they share, 63 checks including
the records lane’s receipt.
Sharp controls $10^{-30}$ past contact at all four walls and at three pairs are refused
by all four deciders, and exact contact is accepted by all four.
$S$ is $1.4809457954896291297 \times 10^{-11}$ below T-229, the house at 204, which was
published in the same commit.
It is also below every earlier report at 204 that the record holds, and below every
bound at 205 to 224.

Seven findings are recorded, none blocking; one is minor.
The certificate and T-229 are one solved packing at two paddings.
T-229 is this certificate dilated about the box’s corner by
$1 + 1.000055 \times 10^{-12}$, to within $2.9 \times 10^{-15}$ at every centre, with
the same tilts; this file is padded by $10^{-20}$ of its side.
So the step from T-229 is padding alone, and every square moves by about $10^{-12}$ of
its distance from the corner, at most $2.02 \times 10^{-11}$. The solved point is the
one Evan Daniel’s exact solver finds for T-229’s arrangement.
The side is, byte for byte, the solver’s for T-229’s witness, as the project’s run of 22
October reported, and 119 of the 204 rows are byte-identical to the certificate that
solver writes from T-229. The other 85 rows are exactly the 21 squares the solver finds
free and the 64 squares holding the flat variables it freezes, where its solution is not
determined.
The author’s account of the search does not mention the solver (RF-1, minor).
His statement that the search started from Francisco Couzo’s #678 certificate, in
Couzo’s frame, agrees with the frame and the arrangement, as it does for T-229. The
source states the side nowhere but in the file (RF-2), and the file left the author’s
tree at `3285fac` (RF-3). This review scores the entry S2: the solved side of a packing
already reported, below that packing’s certificate at the scale of T-225’s solved sides,
which are S2.

This is the stage 4 mathematical review lane of the 23 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
the second 204 file of issue #719. The entry the records branch
`claude/intake-2026-10-23` registers for it is T-231, which `main` does not yet hold;
this review names it as that entry.
It was written by an AI reviewer of the Claude system family (Anthropic), strong
sub-agent tier (`tbd-strong-max`), at maximum reasoning, as lane `c-review-t231-math`
for the intake coordinator `coord-intake-1023`. The lane was prompted separately from
the records lane (`c-lane-719-records-1023`) and read none of its notes.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row, adopts no house best packing, and changes no bead but its own
(`think-tetq`). Its programs and receipts are proposed for retention in the packet’s
`review/review-2026-10-23/` (RF-7), and the proposed record changes are listed at the
end.

**For the author.** Your bound holds exactly at the side your certificate states,
$1.48 \times 10^{-11}$ below `n-204.cert`’s, as you wrote.
Three exact decision programs that are not your code decided it: the two maintained
routes of this repository’s replay, and a checker written for this review.
Measured here, `n-204.cert` is this certificate dilated by $1 + 10^{-12}$, to within
$2.9 \times 10^{-15}$: the same packing with a larger padding.
Its side and 119 of its rows are exactly what Evan Daniel’s exact solver
(`exactsolve.py`, MIT) writes for that packing, and the other rows are the ones that
solver leaves undetermined.
Question 1 asks which program wrote the file.
Question 2 asks whether the licence covers it now that your tree no longer holds it.

## Claim Covered

The claim is $s(204) \le S$, with $S$ the header side of the certificate, at a count
within the record’s horizon (1 to 324).

| n | Exact side $S$ | Rounded up | Certificate at its pin | SHA-256, Git blob |
| ---: | --- | --- | --- | --- |
| 204 | `14808642830513087197802415708703/1000000000000000000000000000000` | 14.808642830514 (12 places); 14.8086428305130872 (16) | `certificates/n204.cert` at `12fc4667` | `9c5dabc8…3e7d`, `4117e9d` |

$S$ terminates at 30 places, so its 30-place print is $S$ itself.
The file’s SHA-256 equals the digest the brief and the #719 packet pin.
Its Git blob equals the tree entry at the pin, read from a blobless clone.
The path first holds this blob at `1851c2c7` (22 October, 05:29:48Z), the commit that
also first holds `certificates/n-204.cert` (T-229), one minute before the issue opened
at 05:30:47Z. The path held other sides from 13 October: `8bb41af`, then `70a033f` on 14
October, T-186’s file, which at the pin is `certificates/square-204.cert`. The author
claimed the file at 20:15:57Z on 22 October.

**Read in full.** The issue’s body and the author’s comments of 22 October and
[23 October](https://github.com/jlevy/squares/issues/719#issuecomment-6355484781); the
certificate; as data, `n-204.cert` at the pin and `n204.cert` at `70a033f`; at the pin,
the source’s `README.md`, `ISSUE_REGISTRATION.md`, `LEGAL_VICTORIES.jsonl`,
`SIGNIFICANT_VICTORIES.jsonl` and `certificates/census.json`, at 204; and the commit log
of the 204 paths. After this review’s checker had decided: the source’s one program,
`check_packing.py`, read and not run.

In the record, at `main` `31584003e`: the result-import process’s stage 4 and its
significance rubric; `epistemics.md` on confirmation, independence, kept code and review
records; the case record `n-204.md`; the significance of T-146, T-155, T-162, T-174,
T-186, T-188, T-190, T-193, T-199 and T-223 to T-229; the source-coverage rows, evidence
entries and intake-ledger rows at 204; the retained certificates or facts of every
report at 204, as data; the T-229 packet’s declaration and derived fact at 204; the
adoption regularization README of 23 October and its 204 report
(`packing/cases/regularized_drawings/think-4h23-2026-10-23/`); the case records at 205
to 224; and, for layout, the README of the T-225 review’s programs.

Of the maintained routes, after this review’s checker had decided: `upper_bound_reports`
(its module statement, `evand_cert`, `ADAPTERS`, `run_job`, `certify`, `decide_job`),
`evand_arrangement_reports` (`checker_input`, `job_input`, `SHARP_CONTROLS`,
`sharp_input`, `run_sharp`, `to_witness`, `run_case`, `validate_job`, `decide_job`) and
`evand_exact_certificates` (`Pose`, `parse`, `literal`, `basis_witness`,
`corner_squares`, `decide`, `tightest_pair`, `top_clearance`). Also the module
statements of `beyond_horizon_replay` and `regularize_evand`, and of the vendored
`search/exact/exactsolve.py`, with its lines on free squares.
Not read: the code of `sqpack/verify.py`, `sqpack/witness.py` and
`check_rational_witness_independent`. On the records branch at `15ecb0a68`, after this
review’s checker had decided: the message of `f308d3f5a`, the packet’s
`acquisition/report.json` and its replay receipt; not its README or its
`measure/identity.py`.

**Disclosure.** Before writing its checker, this reviewer read the model its brief named
for the document’s shape, the review of Evan Daniel’s #728
(`review-2026-10-22-daniel-728.md`). That review describes its own checker’s two routes,
the integer separating-axis gap and the clipping area.
It is not a review of this result, and this reviewer read none of its programs.
Before writing its findings, this reviewer also read three summaries of the 22 October
review of T-229 that the record carries: the case record’s paragraph on T-229’s identity
(`n-204.md` lines 679–688), T-229’s significance rationale in `results.yaml`, and the
adoption README of 23 October, which reports the regularizer’s solved side.
It read that review itself only after its own findings were written (Comparison with the
Earlier Review).

## Runs Here

Run on 23 October 2026 with CPython 3.14.7, under `nice -n 10` on a shared four-core
host, one process at a time, against `main` at `31584003e`.

| Command | What it decides | Outcome | CPU |
| --- | --- | --- | ---: |
| `review_t231_check.py --self-test` | the checker on 13 hand-built cases, 12 malformed texts and 1,500 random pairs | all as expected; the 1,500 pairs decided alike by both routes, 500 of them built to touch and half of those pushed $10^{-30}$ into overlap | 1.1 s |
| `review_t231_check.py`, routes Z and C as two processes | the certificate | accepted on both routes, 20,706 pairs each; every pair’s gap and every square’s four wall clearances equal between the routes | 0.25 and 6.8 s |
| `maintained_routes_t231.py`, the positive and the kernel’s two controls | the certificate on `exact_verify` and `independent`, as `certify`’s child decides it | positive accepted by both, `validate_job` passed; both controls refused by both | 16.4 s |
| the same, `--sharp` | the kernel’s `run_sharp` | at contact accepted at exactly 0; past it refused at exactly $-10^{-30}$, on both routes | 22.3 s |
| `sharp_controls_t231.py` | sixteen mutants on four deciders | every mutant as expected (The Controls) | 181 s |
| `agree_t231.py` | the checker’s numbers against the maintained routes’, and against the records lane’s receipt | 63 of 63 checks equal | under 1 s |
| `margins_t231.py` | the side and its prints; the margins against the record; the solver’s side | as tabulated below | 1 s |
| `identity_t231.py`, and `--self-test` | poses against T-229, T-225, T-223, T-228, T-226 and T-186 | as tabulated below; the assignment and bottleneck code match brute force on 300 instances | 2.7 s |
| `regularize_evand run --n 204`, the project’s generator | nothing: Evan Daniel’s regularizer driver on T-229’s witness, rerun | the 22 October run reproduced: the same input digest and the same two view blobs | 113 s of wall |
| `lineage_t231.py` | nothing: the certificate against the rerun’s outputs | as described under Lineage | 0.4 s |

The checker ran a second time after its digest was recorded, and both receipts came out
identical apart from their timing.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors.
The certificate is one comment line, a header `n S` and $n$ rows `x y t`, each
a rational literal: a rational side, a rational centre and $t = \tan(\theta/2)$, so that
the square’s edges run along $u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ and
$v = (-u_y, u_x)$, as the comment line states.
This review took the format from that line.
The bound follows from five facts, each decided over $\mathbb{Q}$ or fixed by the
format:

1. **The rotation is on the unit circle.** For $t = p/q$, the integers $a = q^2 - p^2$,
   $b = 2pq$ and $d = q^2 + p^2$ satisfy $a^2 + b^2 = d^2$, so $(a/d, b/d)$ is a unit
   vector. Route Z checks the triple on every row; route C builds the corners and checks
   unit edges, right angles, positive orientation and the corner mean.
   127 rows have $t = 0$, and none is a quarter turn.
   Of the 77 tilted rows, 16 lie within 1° of an axis, two of them within $10^{-10}$
   degrees, and 61 are turned by 20.05° to 27.96°, 32 one way and 29 the other.
2. **There are exactly 204 of them.** The reader refuses any other row count (mutant
   R1).
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box exactly when
   its corners do, or equivalently when its centre clears each wall by the half-extent
   $(|a| + |b|)/(2d)$. Route Z decides the second form by four integer inequalities a
   square, route C the first.
   The least clearances are $1/(2 \times 10^{20})$ at the left wall (squares 48 to 51
   and 198 to 203) and at the bottom (4, 5, 6, 173, 179, 185, 191, 197 and 203). They
   are $500000000068827/10^{35}$ at the right (0, 4, 11, 41 and 88 to 96) and at the top
   (48, 55, 85, 88, 106, 124, 133, 142, 151 and 160). Every square’s clearance of every
   wall is equal as a rational on the two routes, and no square touches a wall.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors
   exactly when a line parallel to an edge of one of them weakly separates them.
   The interiors meet exactly when the origin lies in the interior of their Minkowski
   difference, a convex polygon whose edges are parallel to the squares’ edges, so four
   axes decide a pair. Route Z decides every one of the 20,706 pairs this way, with no
   distance filter, and records each pair’s exact gap, the largest separation over the
   four axes. Route C decides every pair, again with no filter, by the exact area that
   one square’s four closed half-planes clip from the other, which is positive exactly
   when the interiors meet.
   It also computes every pair’s gap again from corner projections.
   Every area is 0 and every clipped polygon is empty, so no two squares touch; every
   gap is positive, and the two routes’ gaps are equal pair by pair.
   The least gap,
   `82541895235790714182044220504141977834799093428446189704607867361866276872708954451/8254189523579081975837371701336187856304747589645757681624187247640050000000000000000000000000000000000`
   $= 9.99999999999998720936\ldots \times 10^{-21}$, is between squares 63 and 84, two
   squares tilted alike by 26.75°, on square 63’s normal $v$. 395 pairs lie below
   $10^{-15}$: 283 between aligned squares, 91 between tilted squares and 21 mixed.
   40 of them lie below $10^{-20}$. Route C’s exact squared Euclidean distance between
   squares 63 and 84 is the square of that gap, so their nearest points lie along that
   normal.
5. **The side is the claim’s**, by the table above.

No route here rounds, dilates or tolerates.
Route Z never loads `fractions` (its receipt says so) and compares integers with every
denominator cleared.
A pair’s gap is $(\max_k L_k - R)/(2 d_i d_j D_x D_y)$. Here $D_x$ and $D_y$ are the
products of the two centres’ denominators, $L_k$ the four scaled projections, and
$R = D_x D_y (d_i d_j + |c_{ij}| + |s_{ij}|)$, where $c_{ij}$ and $s_{ij}$ are the
integer cosine and sine of the angle between the squares.

**Status.** That the five facts imply $s(204) \le S$ is proved by the argument above.
That this certificate has the five facts is computationally verified here, by exact
arithmetic on four routes.
Everything else the source states about the packing is asserted, and the mapped table
below says which parts were measured consistent.

The certificate is a dilation of a contact packing.
90 of its centre coordinates are exactly a half-integer times $1 + 10^{-20}$. Dilating
about the box’s corner by $1 + 10^{-20}$ opens each contact by $10^{-20}$ times the
centres’ distance along its normal: $10^{-20}$ between aligned squares and
$5 \times 10^{-21}$ at the left and bottom walls, which are the margins found.
$S$ equals $\lceil 10^{30} (1 + 10^{-20}) S^* \rceil / 10^{30}$, with $S^*$ the exact
side Evan Daniel’s solver reports for this arrangement (Lineage).
The dilation is how the certificate was made; the decision reads only the certificate.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`exact_verify` on `to_witness`, `V-sqpack-verify`) | unit shape, containment and every pair, by the exact separating-axis verifier | the `evand-cert` adapter (`upper_bound_reports.evand_cert`; `evand_exact_certificates.parse` and `basis_witness`), then `sqpack.witness.exact_verify` | with `independent`: the reader, the half-angle map and `Fraction`; with the source: `sqpack/verify.py`, which the issue names among the author’s checkers |
| `independent` (`check_squares` on `corner_squares`, `V-check-rational-witness-independent`) | the same facts, on corners | the same reader; corners from `evand_exact_certificates.Pose.corners`; `check_rational_witness_independent` | the reader and `Fraction` |
| this review’s route Z (`review_t231_check.py`, integers) | the triple per row, half-extent containment, every pair by four integer inequalities | its own reader and CPython integers | its reader with route C; CPython integers with all; the separating-axis method with `sqpack`; no code |
| this review’s route C (`review_t231_check.py`, `Fraction`) | unit edges, right angles, orientation and corner mean; corner containment; every pair by clipped area and by corner projections | its own reader, corners and clipping | `Fraction` with the maintained routes; clipping area with no other route |

Two readers read the certificate here, the maintained one and this review’s, and they
read the same side and the same 204 poses, literal by literal.
`agree_t231.py` holds this review’s reader to the `checker_input` of this lane’s
maintained run and of the records lane’s. The maintained reader admits decimal literals
and skips blank and comment lines anywhere; this review’s refuses decimals (mutant R2)
and blank lines or comments after the header (its self-test).
The certificate has none of these.

**What stays unchecked.** CPython’s integers are common to every route, and `Fraction`
to all but route Z. The custody of the bytes rests on the pin and on the digest, matched
here and in the records lane’s packet.

**The source’s checking.** The source keeps one program at the pin, `check_packing.py`,
from its first commit (`4e1a601`, 9 October).
It reads another format, `s:` and `Square i: x=, y=, deg=` rows in a box centred at the
origin. It converts degrees by its own decimal series, and it passes a square that
crosses a wall, or a pair that overlaps, by up to $10^{-p}$, with $p$ at least 7 and set
by the length of the side’s print.
It cannot read this certificate.
This review read it after its checker had decided and ran nothing of the source.
The certificate’s comment line names `verify_cert.py`, Evan Daniel’s checker, which the
source does not keep.
The issue names that checker and `sqpack/verify.py` for its 122 files.
For this file the author’s statement is that it “passed both of your exact routes”
(RF-6), and no run of his is retained.

## The Controls

The kernel’s two gross controls are refused by both maintained routes: a duplicated
square (gap $-1$), and square 0 moved right by $S + 2$ (clearance
$-16.808642830513087\ldots$). The margins are the ones this review’s routes give for the
same two mutants. This certificate keeps $5 \times 10^{-21}$ at the walls and $10^{-20}$
between pairs. A route that rounded at binary64, or tolerated anything above $10^{-21}$,
would accept the certificate and still refuse both.
This review built sixteen mutants (`sharp_controls_t231.py`,
`outputs/sharp-controls.json`). It decided each with both of its own routes and with
both maintained routes, reached through the `evand-cert` adapter as `certify`’s child
reaches them:

| Mutant | Expected | Both maintained routes | This review’s checker |
| --- | --- | --- | --- |
| F0: the side lowered by the least top-or-right clearance, $5.00000000068827 \times 10^{-21}$ | accepted, corners on the top and right walls | accepted, wall clearance exactly 0 | accepted, 0 on both routes; 13 squares on the right wall and 10 on the top |
| F1: and by $10^{-30}$ more | refused on a wall | refused at exactly $-10^{-30}$ | refused at $-10^{-30}$, 23 squares |
| N0: every square moved left by the least left clearance | accepted | accepted, 0 | accepted, 0, ten squares on the wall |
| N1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused at $-10^{-30}$, ten squares |
| B0: every square moved down by the least bottom clearance | accepted | accepted, 0 | accepted, 0, nine squares on the wall |
| B1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused at $-10^{-30}$, nine squares |
| P0: square 84 moved toward square 63 along 63’s normal $v$ by the least gap (two squares tilted alike) | accepted, an exact contact | accepted, least gap exactly 0 | accepted, gap 0; (63, 84) the one touching pair |
| P1: by the gap $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused, gap $-10^{-30}$; (63, 84) and (80, 84) overlap, 80 lying beside 63 on that line |
| Q0: square 130 moved toward square 121 along 121’s normal $u$ by their gap, $1.0021 \times 10^{-20}$ (a tilted and an aligned square) | accepted | accepted, 0 | accepted, 0; (121, 130) touching |
| Q1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused; (121, 130) alone overlaps |
| A0: square 41 moved toward square 0 along 0’s normal $v$ by their gap (two aligned squares) | accepted | accepted, 0 | accepted, 0; (0, 41) touching |
| A1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused; (0, 41) alone overlaps |
| G1: square 1 replaced by a copy of square 0 | refused | refused, gap $-1$ | refused, gap $-1$ |
| G2: square 0 moved right by $S + 2$ | refused | refused, the same clearance | refused, the same clearance |
| R1: the last row dropped | refused by both readers | `203 square rows for n = 204` | `203 square rows for n = 204` |
| R2: square 0’s $x$ written as its exact 35-place decimal | a reader difference, not a control | read exactly and accepted | refused by the reader |

The kernel’s own `run_sharp` (`side-lowered-past-wall-contact` and
`tightest-pair-closed-past-contact`) was also run on the certificate.
At contact both maintained routes accept with the margin exactly 0, and past it both
refuse at exactly $-10^{-30}$. Its tightest pair, gap, closing normal and top clearance
equal this review’s (`agree_t231.py`). The records lane’s own sharp-controls program in
its packet was not run here.

## Identity, Measured

Whether two certificates are the same packing is not decided here.
What is measured is how far this packing lies from T-229’s and from the packings in
T-229’s lineage, under the box’s eight symmetries applied to the reference in its own
box. Three things are measured.
First, whether nearest centres pair the squares one to one.
Second, under the assignment that minimizes the total squared centre displacement (this
review’s own Hungarian algorithm), how many squares lie within each distance, decided
exactly over the rationals, and how far squares turn modulo 90°. Third, the bottleneck,
which here equals the largest move in every row (`identity_t231.py`,
`outputs/identity.json`).

| Against | Best symmetry | Nearest one to one | Within $10^{-9}$ | Within $10^{-6}$ | Within $10^{-3}$ | Beyond 0.1 | Largest move | RMS | Turned beyond 1° |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T-229, `n-204.cert`, the house | the identity | yes | 204 | 204 | 204 | 0 | $2.02 \times 10^{-11}$ | $1.21 \times 10^{-11}$ | 0 |
| T-225, Daniel’s view, the house until 23 October | the half turn | yes | 35 | 117 | 137 | 6 | 0.273 | 0.0403 | 1 |
| T-223, Couzo’s #678 | the identity | yes | 32 | 113 | 144 | 7 | 0.237 | 0.0341 | 1 |
| T-228, Couzo’s #675 | the identity | yes | 35 | 35 | 138 | 6 | 0.199 | 0.0305 | 4 |
| T-226, Couzo’s #670 | the identity | yes | 31 | 34 | 144 | 2 | 0.199 | 0.0204 | 3 |
| T-186, Polkovskyi’s 14 October file | the identity | no | 35 | 35 | 106 | 14 | 0.716 | 0.0865 | 5 |

Against T-229 the assignment is the identity on row numbers.
Every square moves by between $7.1 \times 10^{-13}$ and $2.02 \times 10^{-11}$ (square
88), 131 of them by more than $10^{-11}$. The 127 aligned squares are aligned in both,
and the 77 tilts agree to $5.2 \times 10^{-15}$ degrees: the tangents are rounded
differently, T-229’s with powers of 5 in the denominators and these at 35 decimal
places.
The transpose, the next symmetry, has an RMS of 0.113. Divided by $1 + 10^{-20}$,
the certificate measures the same against T-229. The moves are a dilation.
Scaled about the box’s corner by the ratio of the two sides,
$1 + 1.000055043828 \times 10^{-12}$, this certificate’s centres land on T-229’s to
within $2.87 \times 10^{-15}$, the largest residual at square 118. Every square’s move
is between $0.99991 \times 10^{-12}$ and $1.00025 \times 10^{-12}$ times its distance
from the corner, which is why square 88, at the far corner, moves most
(`outputs/lineage.json`, `t229_as_a_dilation`). So this is T-229’s packing at a smaller
padding: no square moves against another beyond T-229’s rounding.

Against the packings of the lineage it measures as T-229 does.
Against T-225, under the half turn, 117 squares lie within $10^{-6}$, 67 move beyond
$10^{-3}$ and 6 beyond a tenth, at most 0.273. These are the counts the case record
gives for T-229. The 35 squares within $10^{-9}$ of T-225 lie within $10^{-20}$: they
sit at half-integer positions times $1 + 10^{-20}$ in both dilated files, measured from
opposite corners, which the half turn maps onto each other.
Against T-223 and T-225 one square turns beyond 1°: square 37 (row 40 of the file), at
$-26.2375°$ here and in T-229, against $-0.5952°$ in both, a turn of $25.64°$. Against
T-186 no symmetry pairs the squares one to one, and the identity and the transpose are
within $10^{-4}$ in RMS. Under the identity, square 37’s counterpart in T-186 is turned
$-26.0028°$, within $0.24°$ of this packing’s and $0.034$ away; squares 18, 164 and 165
differ there by up to $25.9°$. Squares 81 and 165 hold the tilts that T-223 and T-225
hold, 26.455° and 20.052°, where T-226 and T-228 differ by 2.5° to 3.4°.

## Lineage: Evan Daniel’s Exact Solver

The project ran Evan Daniel’s regularizer driver on T-229’s witness on 22 October, from
14:06Z to 14:10Z, in the stage 4 branch of the adoption pass (`think-4h23`). Its report
is retained at
`packing/cases/regularized_drawings/think-4h23-2026-10-23/adopt-2026-10-23-n105-204-evand/n-204/report.json.gz`.
It gives the solve’s exact side to 63 places,
$S^* = 14.808642830513087197654329280397180858229902327763609140301316364\ldots$, and
its certificate side, `S_cert`, as
`14808642830513087197802415708703/1000000000000000000000000000000`.

The brief asks whether that output equals this side, as reported.
It does: `S_cert` is the certificate’s header literal, character for character.
It is also $(1 + 10^{-20}) S^*$ rounded up at 30 places, from either end of the 63-place
print (`margins_t231.py`), and the run’s README says so (line 74).

This review reran the driver at 204 (113 s of wall).
The rerun read the same input (`input.txt`, SHA-256 `4fa2b348…344e`) and wrote views
with the same Git blobs (`5ee06383…` solved, `1937dcf6…` same side), so the 22 October
run reproduces.

The run’s solved view is the display view.
The driver imports `regularize.cert`, which its regularize step writes from the solve’s
point after moving squares (step 4 of `devtools/regularize_evand.py`’s module
statement), and that view differs from this certificate by up to 0.242. The solve’s own
certificate, `solve/witness.cert`, is much closer.
The run keeps it in its scratch directory; this review keeps a copy in
`outputs/regularizer-rerun/solve/`.

| Rows | Count | Against the solve’s certificate | Against T-229 |
| --- | ---: | --- | --- |
| byte-identical to the solve’s | 119 | equal as text | within $2.02 \times 10^{-11}$ |
| the solve’s free squares (rattlers) | 21 | the solve moves them by up to $1.41 \times 10^{-3}$ and turns seven by up to 0.057°; here they stay in place | within $1.68 \times 10^{-11}$, with T-229’s tilts |
| the squares holding the solve’s 64 frozen flat variables, one each | 64 | $1.5 \times 10^{-12}$ to $1.43 \times 10^{-11}$ apart in the frozen coordinate, and in 26 of them in the other too; tilts equal | within $1.95 \times 10^{-11}$ |

The comment line and the header are identical too.
So every row that the solver’s KKT system determines is the solver’s, to the last of its
35 places. The rows that differ are exactly those it places itself or takes from its
input.
Free squares are placed by its `place_free` step, which seeks a clearance of up to
$10^{-6}$. From T-229 the least such clearance it reaches is $5.769 \times 10^{-9}$;
here it is $5.774 \times 10^{-9}$, and in T-229 $5.775 \times 10^{-9}$. Square 37, the
square T-229 turned by 25.64°, is one of the free squares: here it is
$1.25 \times 10^{-2}$ clear, the most of any.
Squares 7 and 31 are $10^{-6}$ clear to within $1.1 \times 10^{-12}$ here, in T-229 and
in the solve’s certificate alike, the clearance that placement seeks.
That suggests T-229’s free squares had passed through such a placement too.
Flat directions are frozen.
In the rerun the frozen coordinates lie within $4.7 \times 10^{-12}$ of T-229’s; here
they lie within $1.43 \times 10^{-11}$, and within $2.9 \times 10^{-15}$ of T-229’s
divided by T-229’s dilation.
So the certificate is not that solver’s output from T-229 as the project ran it.
Its undetermined part is T-229’s, without T-229’s padding: both files come from one
solve of this arrangement, which placed the free squares and froze the flat variables
differently from the project’s run, and T-229 is that solve’s point dilated by
$1 + 10^{-12}$. T-229’s side lies $1.48 \times 10^{-11}$ above $S^*$ for that reason.
This measures how the files were made; it does not establish it.

**The lineage statements.** On 22 October the author wrote, of the 25.64° turn: “Started
from Couzo #678 / Evan Daniel (T-225)… an intentional relaxed local reorientation
identified during continuous SQP/Newton relaxation”.
On 23 October he wrote that the optimization “was initialized directly from Francisco
Couzo’s #678 certificate… in Couzo’s native unrotated coordinate frame”.
Both statements answered questions about T-229, and he gave none for this file.
They agree with what is measured:

- **The frame.** Like T-229, the certificate is in #678’s frame: the identity pairs it
  one to one with T-223, and T-225 only under a half turn.
- **The arrangement.** It is T-229’s, and it keeps every feature of T-229 that neither
  T-223 nor T-225 has.
  Square 37 is turned to $-26.24°$. The free squares 1, 18, 45, 101, 118, 119, 120 and
  163 carry small tilts: T-225 holds all of them at 0, and T-223 tilts 18 and 119 the
  other way. Squares 130 to 132 and 139 to 141 share one angle, 0.237060°. T-223 and
  T-225 hold 130 to 132 at 0.236923° and 139 to 141 at three angles from 0.1998° to
  0.2015°.

What neither statement says is the last step, which the measurement shows: the side and
the determined rows are Evan Daniel’s exact solver’s for T-229’s arrangement (RF-1).

## Newness in Report Order

Sides are each report’s exact side where the record retains it, and otherwise a print
with an allowance of one unit in its last place (`margins_t231.py`,
`outputs/margins.json`).

| Report | Reported | Side, rounded up at 16 places | $S$ below it by |
| --- | --- | --- | ---: |
| Kingbird, David Ellsworth’s catalogue | before 30 September | 14.82287565553229 (print) | at least $1.423282501919 \times 10^{-2}$ |
| T-101, Daniel’s exact certificate of the catalogue’s packing | 2026-10-05 | 14.8228756555322953 | $1.423282501921 \times 10^{-2}$ |
| T-155, the project’s regularized certificate of it | 2026-10-12 | the same side | the same |
| T-162, Ostashev’s #562 | 2026-10-12 | 14.8086632343869566 | $2.040387386937 \times 10^{-5}$ |
| T-174, PingYou Ltd’s PR #574 | 2026-10-13 | 14.8086632343869566 | $2.040387386937 \times 10^{-5}$ |
| Polkovskyi’s file of 13 October (`8bb41af`, #593) | 2026-10-13 | 14.8086632343869566 | $2.040387386937 \times 10^{-5}$ |
| T-186, Polkovskyi’s KKT refinements (`70a033f`) | 2026-10-14 | 14.8086632343869566 | $2.040387386937 \times 10^{-5}$ |
| T-193, Daniel’s exact algebraic side (#639) | 2026-10-16 | a root of a degree-35 polynomial, $1.48 \times 10^{-99}$ below T-186 | $2.040387386937 \times 10^{-5}$ (at least $2.040387291 \times 10^{-5}$ from the receipt’s 12-place interval) |
| T-226, Couzo’s #670 | 2026-10-17 | 14.8086444176899239 | $1.587176836610 \times 10^{-6}$ |
| T-228, Couzo’s #675 | 2026-10-18 | 14.8086443672267897 | $1.536713702499 \times 10^{-6}$ |
| T-223, Couzo’s #678 | 2026-10-18 | 14.8086428419812473 | $1.146816002570 \times 10^{-8}$ |
| T-225, Daniel’s regularized lists | 2026-10-20 | 14.8086428405914940 | $1.007840672527 \times 10^{-8}$ |
| T-229, Polkovskyi’s `n-204.cert`, the house | 2026-10-22, `1851c2c7` | 14.8086428305278967 | $1.4809457954896291297 \times 10^{-11}$ |

$S$ is below every one.
T-229’s side and $S$ were published in the same commit, so neither comes before the
other in report order; $S$ is the smaller.
The author’s “$1.48 \times 10^{-11}$ lower” is that margin, rounded.
The project’s run reached the same side at 14:06Z on 22 October, after the commit, as
its README says. That run is not a report.
The intake ledgers through the 22 October passes and the source-coverage register hold
no other report at 204. This lane did not sweep the live heads of the watched
repositories.

**Later counts.** Deleting squares from a packing of $m$ leaves a packing of any smaller
count in the same box, so $s(204) \le s(m)$ for $m > 204$, and a side is new only if it
is below every bound at every later count.
$S$ is below the verified and the reported upper bound at every count from 205 to 224 on
`main`; the least margin is $1.580831561098 \times 10^{-2}$, at 205’s reported bound.
From 225 on, every bound is at least $\sqrt{m} \ge 15$ by area.

## Significance

The rubric is `epistemics.md`’s, and the score is of the claim.
The record’s line at this scale, read from its entries:

- **S1:** padding and exact re-solves at rounding scale: T-174 and T-186 at up to
  $1.8 \times 10^{-19}$, and T-155 at up to $9.9 \times 10^{-15}$.
- **S2:** a refinement of a packing to a new smallest side, or the solved side of a
  packing already reported: T-190 at $2.40 \times 10^{-11}$, T-229’s row at 105 at
  $5.18 \times 10^{-12}$, its row at 204 at $1.006 \times 10^{-8}$, T-225’s solved sides
  at $1.76 \times 10^{-11}$ to $1.39 \times 10^{-9}$, and T-228 at
  $5.05 \times 10^{-8}$.
- **S3:** new arrangements, starting at about $2 \times 10^{-5}$ here (T-226).

**S2.** The solved side of T-229’s packing at 204, at the solver’s padding of
$10^{-20}$, $1.48 \times 10^{-11}$ below T-229, which certifies the same point padded by
$10^{-12}$. That is T-225’s case: “the solved exact side of a packing already reported”,
$1.76 \times 10^{-11}$ to $1.39 \times 10^{-9}$ below that packing’s certificate, S2.
The step is padding alone, and the record scores padding S1 when it is at rounding
scale: T-170, T-174 and T-186 at up to $1.8 \times 10^{-19}$. This step is eight orders
of magnitude above those, and it moves the case’s 12-place print from 14.808642830528 to
14.808642830514. That is what the 22 October review weighed in scoring T-229’s row at
105 S2 rather than S1. Read by kind alone, as a padding change, it would be S1. This
review keeps S2 by scale and by T-225’s precedent.
It is not S3: no arrangement changes, and no case result beyond the side follows.
If the records lane’s draft differs, this score and rationale replace it.

## Credit

The source says who did what.
The issue credits “Mishapolk (Mykhailo Polkovskyi)” and says Gemini assisted with solver
scripting, precision checks and formatting.
It also says its packings “build upon and refine” the work of named contributors, and
the comments name Couzo’s #678 as the seed.
The measurement supports crediting the certificate to Mykhailo Polkovskyi and the
packing as the record credits T-229’s: Francisco Couzo’s arrangement, first reported in
#670 and refined in #675 and #678, re-solved by Polkovskyi.
The record’s line for T-229 also names Evan Daniel’s regularization (T-225) as an
antecedent at 204. The triage bead plans to reconsider that on the author’s answer
(Comparison with the Earlier Review), and what is decided there applies here too.
Daniel’s exact solver is a separate matter.
RF-1 asks the record to name it as the measured method until the author says which
program wrote the file.

## The Source’s and the Record’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(204) \le S$ at the header side | the certificate; the author’s comment of 22 October (answer 3) | **computationally verified here**: three exact programs, four exact routes, every pair decided |
| the side is $1.48 \times 10^{-11}$ below `n-204.cert`’s | the same comment | **verified here**: $1.4809457954896291297 \times 10^{-11}$ |
| it “passed both of your exact routes” | the same comment | **true now**: both maintained routes accept it, in this lane’s run and in the records lane’s; see RF-6 for when |
| the optimization started from Couzo’s #678 in Couzo’s frame | the author’s comment of 23 October, about T-229 | **measured consistent** for the frame and the arrangement; the last step is the solver’s (RF-1) |
| “Started from Couzo #678 / Evan Daniel (T-225)” | the comment of 22 October, about T-229 | **measured consistent**; the frame points to #678 |
| strictly positive wall clearances and separating-axis gaps | the issue, of its 122 files | **verified here** for this file too: at least $5 \times 10^{-21}$ and $9.99999999999998 \times 10^{-21}$ |
| the regularizer solved T-229’s witness to this side | the adoption README of 23 October, line 74 | **verified here**: the report’s `S_cert` is the header literal, and the rerun reproduces it |
| “the view reproduces his own publication” | the same README, line 82 | **the side only** (RF-4) |
| no global optimality, rigidity or KKT second-order claim | the issue | **agreed**; the packing is not rigid (RF-5) |

## Findings

Line numbers in the repository are at `31584003e`; in the source, at `12fc4667`, where
square $k$, numbered from 0, is line $k + 3$ of the certificate.

**RF-1, minor, non-blocking: the certificate’s determined rows are Evan Daniel’s exact
solver’s, and the source does not say so.** Lineage gives the measurement: the side, the
comment line and 119 of the 204 rows (lines 3 to 206) are byte-identical to the
certificate `exactsolve.py` writes from T-229’s witness, including 183 of the 204 tilts.
The other 85 rows are exactly the solver’s 21 free squares and the 64 squares holding
its frozen flat variables.
At 35 decimal places, with the solver’s dilation and rounding, that agreement does not
arise from another procedure unless it computes the same KKT point and rounds it the
same way.
The issue’s method statement (“Gemini assisted with solver scripting, precision
checks, and formatting”) and the comments (“continuous SQP/Newton relaxation”) do not
mention Daniel’s solver, which is MIT-licensed and which its author says was written
with Claude.
T-229 is this certificate dilated by $1 + 10^{-12}$ (Identity, Measured), so
the measurement bears on both files.
No bound depends on this.
The record’s method and credit lines do.
Proposed: until the author answers Question 1, the entry’s method says “the exact solved
side of T-229’s packing, whose determined rows equal Evan Daniel’s exact solver’s
(`exactsolve.py`) row for row, at that solver’s padding of 1e-20; T-229 is the same
point padded by 1e-12 (measured)”, citing `outputs/lineage.json`. The packing keeps
T-229’s credit line, and the certificate is Polkovskyi’s.

**RF-2, note: the source states the side only in the certificate.** At the pin,
`certificates/census.json` (line 309) still describes the 14 October file at 204: side
`740433161719347828…/5·10^{109}`, SHA-256 `f0885fa8…`, which is `square-204.cert`.
`LEGAL_VICTORIES.jsonl` (line 163) and `SIGNIFICANT_VICTORIES.jsonl` (line 6) list only
`n-204.cert`. The issue’s tables name only `n-204.cert`, and the claim gives
“$1.48 \times 10^{-11}$ lower” and no side.
So the header is the only statement of $S$. The records lane already admits it as
offered by the file itself.
Proposed: the record prints $S$ exactly or rounded up, 14.808642830514 at 12 places or
14.8086428305130872 at 16, and quotes no source print for it.

**RF-3, note: the file has left the author’s tree, and the licence commit does not hold
it.** `3285fac` (19:29:30Z on 22 October) dropped the path.
Its sharded successor, `certificates/0000-0999/n204.cert`, holds `n-204.cert`’s bytes
(blob `17e243a`) through the head, `7b6366f`. The MIT licence arrived at `17cc220`
(20:15:36Z), whose tree holds T-229’s bytes under that name and not this file.
The author’s comment grants retention of “the raw certificate files in your packets”
(answer 5) and claims this file in the same comment, 21 seconds after the licence
commit. The records lane retains it under that grant.
Proposed: the record cites `12fc4667` and the digest, never the head’s path, which now
names another certificate; Question 2 asks the author to confirm the grant.

**RF-4, note: the adoption README says the solved view reproduces the publication; it
reproduces the side.**
`packing/cases/regularized_drawings/think-4h23-2026-10-23/README.md` lines 81–82 read
“the view reproduces his own publication, in the same commit as T-229’s certificate”.
The view the run keeps (`view-solved.yaml`, blob `5ee06383…`) is the display
regularization at the solved side.
It differs from this certificate by up to 0.242, and the solve’s own certificate differs
from it at 85 rows. What reproduces is the side, byte for byte, as line 74 says.
Proposed: reword to “the run reproduces his side”, and cite this review’s lineage
receipt for the rows.

**RF-5, note: the packing is not rigid, and no local-minimum claim follows.** The 21
free squares keep clearances from $5.774 \times 10^{-9}$ to $1.25 \times 10^{-2}$, by
the exact separating-axis gap to every other square and to every wall.
A square whose gaps all exceed $c$ can be translated by any vector shorter than $c$,
since the gap is a lower bound on the Euclidean distance.
So the packing admits non-trivial feasible motions at its side; that is computationally
verified by the exact clearances.
The solver’s own second-order check is “inconclusive: negative curvature blocked (first
order) by weakly active contacts”.
Proposed: the record carries no local-minimum, KKT or rigidity statement for this
certificate beyond “not rigid”.
Its rigidity block at 204 describes an earlier witness and should be revisited when the
house moves.

**RF-6, note: “passed both of your exact routes” rests on a run the record does not
keep.** The author wrote this at 20:15:57Z on 22 October.
The #719 packet README says the file “passed both routes in triage” (lines 237–238), and
the project’s reply of 20:03Z on 22 October repeats it, which is presumably what the
author quotes. That packet pins the file by digest only and keeps no receipt of the
triage’s run. The 22 October review measured the file’s identity and did not decide it
(Comparison). The statement is true now, with receipts: the records lane’s replay and
this review’s runs. Proposed: the record cites those, and not the triage, for the file’s
feasibility.

**RF-7, note, for the record: retain and register this review’s programs.** Until they
sit in the packet with their README they are scratch files the record cannot cite.
Proposed: the packet’s `review/review-2026-10-23/`, as laid out here.
`review_t231_check.py` decides, and `sharp_controls_t231.py` with
`maintained_routes_t231.py` are premise checks; all three belong in `verifiers.yaml`
with their independence records.
`margins_t231.py`, `identity_t231.py`, `agree_t231.py` and `lineage_t231.py` decide
nothing, and the README says so.

## Questions for the Author

1. Which program wrote `n204.cert`, and from which input?
   Its side and 119 of its rows are exactly what Evan Daniel’s `exactsolve.py` writes
   for `n-204.cert`’s packing.
   Its free squares and flat coordinates lie within $2 \times 10^{-11}$ of
   `n-204.cert`’s, but not where that solver places them when it starts from
   `n-204.cert`. Was it Daniel’s solver, at which revision, run on the optimization
   result that `n-204.cert` also comes from?
2. Your tree has not held this file since `3285fac`, and
   `certificates/0000-0999/n204.cert` now holds `n-204.cert`’s bytes.
   Do you confirm that the MIT licence of `17cc220` and your grant on #719 cover
   `certificates/n204.cert` at `12fc4667` (blob `4117e9d`)?
3. Both files first appear in `1851c2c`, and `n-204.cert` is `n204.cert` dilated by
   $1 + 10^{-12}$ and rounded to within $2.9 \times 10^{-15}$. Which did you write
   first, and why does `n-204.cert` carry the larger padding?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, once the records lane’s replay
evidence and this review are entered.
That needs the retained certificate, a replay command (`check --replay`), a passing
replay, retained controls refused by every route that accepted the positive, and sharp
controls refused here.
The maintained replay is the records lane’s. By T-229’s precedent it shares the
producer’s components, since the issue names `sqpack/verify.py` among the author’s
checkers. This review’s checker is a clean-room re-implementation.
Before it decided, its author had read the certificate, the issue, the comments, the
mathematics and the #728 review’s account of its checker (Disclosure), and never the
source’s code or the maintained routes.
The program has not changed since.
It was written by a Claude agent.
The author discloses Gemini assistance, but RF-1 measures the certificate’s numbers as
Evan Daniel’s solver’s, and its source says it was written with Claude, so the
authorship may overlap the producer’s in system family.

By the house rule, once the entry stands at `V3`/`C3` with this review mapped as its
accepted review, it holds the smallest validated side at 204. It is then adopted and
regularized in the same pull request, and T-229 stays retained as history.
It does not reach `V4`/`C4`, which need a second accepted adversarial review by a
distinct reviewer and a retained human oversight record.
No lower bound, optimum, local minimum or priority follows; no rigidity follows either,
beyond RF-5’s “not rigid”.

## Proposed Record Changes

For the records lane; this review writes none of them, and `record-changes.md` beside
this review’s output gives each in full.

- **`evidence.yaml`.** The records lane’s confirming replay entry, with `limitations`
  citing this review’s controls receipts.
  An entry for this review’s checker: `independent-implementation`, `coverage: full`,
  `clean_room: true`, `shares: []`,
  `read: [mathematics, specification, certificate-format]`,
  `overlaps_producer: system-family`. This document is `external_review` on the reported
  entry.
- **`verifiers.yaml`.** Register `review_t231_check.py` (decides) and
  `sharp_controls_t231.py` with `maintained_routes_t231.py` (premise checks), with the
  digests in `outputs/program-digests.sha256`.
- **`results.yaml`.** The entry’s `reviews` gains this document (`kind: adversarial`,
  `reviewer_kind: ai`, `relation: project`, `verdict: accepted`). Its significance is S2
  with the rationale above, `by` naming this review; its identity is `measured`; its
  method is as RF-1 proposes; and it states no local-minimum claim (RF-5).
- **The case record.** Adopt the certificate at 204 and regularize it, by the house
  rule; T-229 stays retained as history.
- **The adoption README of 23 October.** Reword lines 81–82 (RF-4).

## Comparison with the Earlier Review

The earlier review of the closely related result is the 22 October review of T-229
([`review-2026-10-22-mishapolk-719.md`](review-2026-10-22-mishapolk-719.md)). It
reviewed `n-204.cert`, not this file.
This review read it, the #719 packet README’s lines on this file, the triage bead’s
notes (`think-xyhn`) and the project’s two replies on #719 only after its findings above
were written. What it had seen before is in the Disclosure: three summaries of that
review’s identity findings and significance, in the case record, the register and the
adoption README.

**What the earlier review says of this file.** It measured it once: “`n204.cert` is
$1.48 \times 10^{-11}$ below `n-204.cert` and is the same packing (largest move
$2.0 \times 10^{-11}$). Neither is claimed” (its Newness section), with a row in its
identity table. It did not decide the file.
This review’s identity row against T-229 agrees with that row.

**Agreements.** Every identity figure that review gives for T-229 is this review’s for
this certificate, as it must be for a dilation of T-229. In that review’s columns
(within $10^{-6}$; beyond $10^{-3}$, $10^{-2}$ and a tenth; the largest move; squares
turned beyond 1°):

- against T-225 under the half turn: 117, 67, 39 and 6, and 0.273;
- against T-223 under the identity: 113, 60, 29 and 7, and 0.237;
- against T-228: 35, 66, 39 and 6, 0.199, four turned;
- against T-226: 34, 60, 21 and 2, 0.199, three turned;
- against T-186, which no symmetry pairs one to one: 35, 98, 45 and 14, 0.716, five
  turned.

Its released square, “square 38” numbered from 1 (row 38 of the certificate’s squares),
is this review’s square 37, numbered from 0. Here too it is turned by 25.64° with
nothing within $1.25 \times 10^{-2}$. This review adds that Daniel’s solver lists it
among its free squares, and that under the identity it lies within 0.034 and 0.24° of
T-186’s square 37. Its RF-4, that the certificate keeps Couzo’s frame and tilts, holds
here, and the author’s later answer, that the solve started from #678 in Couzo’s frame,
agrees with both reviews.
Its RF-1 precedent, that the maintained replay shares the producer’s components because
the issue names `sqpack/verify.py`, is carried here unchanged.
Both reviews score S2 against the same comparators: T-190, T-225 and T-228, and T-229’s
row at 105.

**What this review adds.**

- **The two 204 files are one point at two paddings.** That review measured T-229’s
  margins at 204, walls $4.9998207 \times 10^{-13}$ and pairs
  $9.980857291582 \times 10^{-13}$, and did not say why they are about $10^{-12}$. T-229
  is this certificate dilated by $1 + 1.000055 \times 10^{-12}$, to within
  $2.9 \times 10^{-15}$, so its margins are the solved point’s contacts opened by that
  dilation. Its side is $1.48 \times 10^{-11}$ above the solved side of its own packing.
- **Daniel’s solver (RF-1).** That review ran before the project’s run of Daniel’s
  regularizer on T-229, and did not compare either file with the solver’s output.
  The triage bead’s note of 23 October (04:05Z) proposes that T-229’s credit at 204 drop
  Daniel’s regularization as an antecedent, on the author’s answer.
  RF-1 bears on that change: the solver measured here is a method, not a packing
  antecedent, and the record can drop T-225 from the lineage while naming the solver as
  the measured method.
- **Custody (RF-3).** The file left the source’s tree at `3285fac`. The project’s reply
  of 22 October noted it, and the record should cite the pin.

**Changed after reading.** RF-6 was written before this review read the #719 packet
README. It now cites that README’s line on the triage’s run, and a question asking which
run the author meant is withdrawn.
No other finding changed.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, novelty or priority, and no rigidity beyond
RF-5; no human oversight.
No run of the source’s program or search: the one solver run here was the project’s own
generator, as a measurement (Lineage).
No decision of whether two certificates are the same packing.
No house adoption, case-record change or regularization at the new side, and no sweep of
the watched repositories’ live heads.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
