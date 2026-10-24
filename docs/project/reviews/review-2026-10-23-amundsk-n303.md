# Review: Amund Kristiansen’s Certificate at 303, from Issue #755

**Date:** 23 October 2026. **Verdict: accepted, for finite feasibility only, with
findings on the record.** Amund Kristiansen requested registration of `s303_amund.cert`
in the gist
[`amundsk/78f9f0e7b4669f2f509a281845081768`](https://gist.github.com/amundsk/78f9f0e7b4669f2f509a281845081768)
at revision `511f56bf6e6afb4eb22f12d31371c2a2fe7b4767`, on
[issue #755](https://github.com/jlevy/squares/issues/755). It proves $s(303) \le S$ with
$S = 223872029093440709529093216833/12500000000000000000000000000 =
17.90976232747525676232745734664$: 303 unit squares with pairwise disjoint interiors in
the closed box $[0, S]^2$. No square touches a wall and no two squares touch.
The least wall clearance is $6.020000000001029\ldots \times 10^{-13}$, at the top wall
(square 3, numbered from 0); it is $6.025\ldots \times 10^{-13}$ at the right (square
73\) and exactly $6.0300000000010299 \times 10^{-13}$ at the left (11 squares) and the
bottom (10). The least pair gap is exactly
$60250000000010249/(5 \times 10^{28}) = 1.20500000000020498 \times 10^{-12}$, at six
pairs, and the exact Euclidean distance of each of those pairs is the same number.
A checker written for this review decides the certificate on two exact routes that share
only a reader. It shares no code with the maintained routes or with the source, and it
decided before its author read any of them.
It agrees with both maintained routes at every number they share, 116 checks including
the records lane’s receipt and its derived fact.
Sharp controls $10^{-30}$ past contact at three walls and at five pairs are refused by
all four deciders, and exact contact is accepted by all four.
$S$ is $9.889799071009889799071 \times 10^{-6}$ below Evan Daniel’s certificate of 22
October (T-230), the house at 303. It is also below every earlier report at 303 that the
record holds, and below every bound at 304 to 320; from 321 on, area puts every bound
above it.

Nine findings are recorded, none blocking; one is minor.
The certificate is what Evan Daniel’s `dilate_cert.py`, written out here and not run,
computes from the float packing the gist publishes beside it: its side and all 303
centres to the last digit, and 267 of its 303 tangents.
Each of the other 36 tangents is the one that a `tan` one unit in the last place away
gives, as a machine whose `tan` rounds differently would compute it (RF-3). The packing
is T-230’s, rearranged.
It keeps T-230’s row order, and the best assignment is row for row, with 12 squares
moved beyond a tenth, at most 0.547, most of them in a column of squares beside the
upper tilted band. Five squares turn from the axes to tilts of 1.9° to 17.85°, and one
group of eleven tilted squares turns by 1.04°. Of about 860 contacts, 47 change: 38 of
T-230’s are released, 30 of them as one row of eleven aligned squares slides by up to
0.0097, and 9 are new.
The issue’s matching figures are reproduced exactly.
So the request’s account, a new packing found from T-230’s and not a refinement of it,
holds in the record’s sense of those words (RF-4). The least wall clearance the issue
quotes from `verify_cert.py`, $8.2 \times 10^{-13}$, is not this file’s (RF-1, minor),
and the side’s decimal it gives is the binary64 print of the side, not the side (RF-2).
This review scores the entry S2: a further arrangement of the house’s packing
$9.89 \times 10^{-6}$ below it, at the scale of T-188’s S2, where the draft had S3
(RF-5).

This is the stage 4 mathematical review lane of the 23 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
issue #755. The entry the records branch `claude/intake-2026-10-23-755` registers for it
is T-239, which `main` does not yet hold; this review names it as that entry.
The branch registered it as T-238 when this review was written and renumbered it T-239
on 24 October 2026, after the review, when #750 took T-237 and T-238. The renumbering
changed only the sentence before this one; the review’s programs keep the old id in
their names and docstrings, since their digests are bound.
It was written by an AI reviewer of the Claude system family (Anthropic), strong
sub-agent tier (`tbd-strong-max`), at maximum reasoning, as lane `c-review-t238-math`
for the intake coordinator `coord-intake-1023`. The lane was prompted separately from
the records lane (`c-lane-755-1023`) and read none of its notes.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row, adopts no house best packing, and changes no bead but its own
(`think-jdz0`). Its programs and receipts are proposed for retention in the packet’s
`review/review-2026-10-23/` (RF-9), and the proposed record changes are listed at the
end.

**For the author.** Your bound holds exactly at the side your certificate states,
$9.89 \times 10^{-6}$ below T-230’s, as you wrote.
Three exact decision programs decided it, none of them yours or Evan Daniel’s: the two
maintained routes of this repository’s replay, and a checker written for this review.
Your matching figures against T-230 (largest move 0.547, 12 squares beyond 0.1, 31
beyond 0.01, 96 tilted squares against 91) are reproduced exactly, under the identity
and with your rows in T-230’s order.
Two of the issue’s numbers need correcting.
`verify_cert.py` at `7982d7a` computes the least wall clearance as
$6.020 \times 10^{-13}$ here, not $8.2 \times 10^{-13}$. The decimal
$17.909762327475256427\ldots$ is how the checkers print the side as a binary64 float;
the side itself is $17.90976232747525676\ldots$. Neither changes the bound.
Question 1 asks where the $8.2 \times 10^{-13}$ came from, Question 2 which machine made
the certificate, and Question 3 whether the project may keep the certificate’s bytes.

## Claim Covered

The claim is $s(303) \le S$, with $S$ the header side of the certificate, at a count
within the record’s horizon (1 to 324).

| n | Exact side $S$ | Rounded up | Certificate at its pin | SHA-256, Git blob |
| ---: | --- | --- | --- | --- |
| 303 | `223872029093440709529093216833/12500000000000000000000000000` | 17.909762327476 (12 places); 17.9097623274752568 (16) | `s303_amund.cert` at `511f56b` | `9ec01059…511b`, `748da9a` |

$S$ terminates at 29 places, $17.90976232747525676232745734664$, so its 29-place print
is $S$ itself. The file’s SHA-256 equals the digest the issue, the gist README and the
records lane’s packet pin.
The gist holds one revision, `511f56b`, committed at 11:12:11Z on 23 October, 37 seconds
before the issue opened (11:12:48Z), with three files: `README.md` (`870ead51…`), the
certificate, and `s303_amund.input.txt`, whose SHA-256 is the issue’s `19fc5d17…4ba4`.
The gist states no licence.

**Read in full.** The issue’s body (it has no comments); the gist’s README, certificate
and input, as data. After this review’s checker had decided: Evan Daniel’s
`search/exact/verify_cert.py`, `search/exact/verify_cert2.py` and
`search/packer/dilate_cert.py` at `7982d7a`, fetched for this review, read and not run.

In the record, at `main` `c1115c095` (the commit the records lane read; `main` reached
`7335d0098` during this review with no change at 303 to 320): the result-import
process’s stage 4 and its significance rubric; `epistemics.md` on confirmation,
independence, kept code, review records and significance; the case record `n-303.md`;
T-230’s register entry, and the significance of T-181 to T-230; the source-coverage rows
at 303; the retained certificates or facts of every report at 303, as data; the house
witness `W-known-best-n303`; and the case records at 304 to 320. After its findings were
written: the Kingbird catalogue’s captures of 22 August and 30 September at 303, and,
untracked, of 23 October, and the list of issues opened since 22 October.

Of the maintained routes, after this review’s checker had decided: the module statements
of `upper_bound_reports`, `evand_arrangement_reports` and `evand_exact_certificates`;
`upper_bound_reports`’ `evand_cert`, `ADAPTERS`, `parse_certificate`, `admit`,
`run_job`, `certify` and `decide_job`; the kernel’s `checker_input`, `job_input`,
`SHARP_CONTROLS`, `sharp_input`, `run_sharp`, `to_witness`, `run_case`, `validate_job`
and `decide_job`; and `evand_exact_certificates`’ `Pose`, `parse`, `literal`,
`basis_witness`, `corner_squares`, `tightest_pair` and `top_clearance`. Also the
registry entries `V-evand-verify-cert-py` and `V-evand-verify-cert2-py`. Not read: the
code of `sqpack/verify.py`, `sqpack/witness.py` and
`check_rational_witness_independent`. On the records branch at `3003d81d5`, after this
review’s checker had decided: the packet’s `acquisition/report.json`, its replay receipt
and its derived fact `facts/n-303.yaml.gz`; not, before these findings were written, its
README, `measure/identity.py` or `replay/sharp_controls.py` (Comparison with the Earlier
Review says what was read after).

**Disclosure.** Before writing its checker, this reviewer read the model its brief named
for the document’s shape, the 23 October review of Mykhailo Polkovskyi’s second
certificate at 204 (`review-2026-10-23-mishapolk-n204.md`, on the intake branch).
That review describes its own checker’s two routes, an integer separating-axis gap with
every denominator cleared and the exact clipped area, and its table of sharp controls;
this review’s route Z decides by the same mathematics.
It is not a review of this result, and this reviewer read none of its programs.
Before writing its findings, this reviewer also read two summaries of the 22 October
review of T-230 that the record carries: T-230’s register entry (its claim, notes,
significance and review row, which name that review’s RF-1 to RF-4 and RF-7) and the
case record’s section on T-230. It read that review itself only after its own findings
were written (Comparison with the Earlier Review).
In the shared scratch directory it read one file, a brief for a pull-request review lane
that does not concern this result.

## Runs Here

Run on 23 October 2026 with CPython 3.14.7, under `nice -n 19` on a shared four-core
host, at most two processes at a time, against `main` at `c1115c095`.

| Command | What it decides | Outcome | CPU |
| --- | --- | --- | ---: |
| `review_t238_check.py --self-test` | the checker on 15 hand-built cases, 13 malformed texts and 2,000 random pairs | all as expected; the 2,000 pairs decided alike by both routes, 1,600 of them built to touch, 800 of those at a corner of the first square, and half of the 1,600 pushed $10^{-30}$ into overlap | 1.6 s |
| `review_t238_check.py`, routes Z and E as two processes | the certificate | accepted on both routes, 45,753 pairs each; every pair’s gap and every square’s four wall clearances equal between the routes | 0.31 and 8.7 s |
| `maintained_routes_t238.py`, the positive and the kernel’s two controls | the certificate on `exact_verify` and `independent`, as `certify`’s child decides it | positive accepted by both, `validate_job` passed; both controls refused by both | 9.9 s of route time |
| the same, `--sharp` | the kernel’s `run_sharp` | at contact accepted at exactly 0; past it refused at exactly $-10^{-30}$, on both routes | 85 s of wall |
| `sharp_controls_t238.py` | 21 mutants on four deciders | every mutant as expected (The Controls) | 724 s of wall |
| `agree_t238.py` | the checker’s numbers against the maintained routes’, the records lane’s receipt and its fact | 116 of 116 checks equal | under 1 s |
| `margins_t238.py` | the side and its prints; the margins against the record | as tabulated below | 1 s |
| `method_t238.py` | nothing: the certificate against the float packing it was made from, and T-230’s against its own | as described under How the Certificate Was Made | 2 s |
| `identity_t238.py`, and `--self-test` | nothing: poses against fourteen packings at 303, and contacts against T-230 | as tabulated below; the assignment and bottleneck code match scipy and brute force on 300 instances | 11 s |
| `identity_t238.py` on T-230’s certificate | nothing: T-230 against the same packings, for comparison | `outputs/identity-t230.json` (Comparison with the Earlier Review) | 10 s |

The checker ran a second time after its digest was recorded, and both receipts came out
identical apart from their timing (`outputs/second-run/`).

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors.
The certificate is one comment line, a header `n S` and $n$ rows `x y t`, each
a rational literal. The comment line names the generator and a checker, and it does not
state the format. This review read the format from the issue’s method statement (“each
angle to a rational half-angle tangent, so every square is exactly unit”), the gist
README and the data: row $k$ is the unit square with centre $(x, y)$ whose edges run
along $u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ and $v = (-u_y, u_x)$, so $t$ is the
tangent of half its rotation.
The first square’s centre lies half a unit and $6.03 \times 10^{-13}$ from the left
wall. The bound does not rest on that reading being the author’s. The 303 squares the
reading defines are one explicit packing, and if they have the five facts below,
$s(303) \le S$ follows whatever convention was intended.
The mirrored reading, every $t$ negated, is refused by all four deciders with 106
overlapping pairs (mutant M1), so the reading is not idle; it is also the one
`verify_cert.py`’s docstring states, read after deciding.
The bound follows from five facts, each decided over $\mathbb{Q}$ or fixed by the
format:

1. **The rotation is on the unit circle.** For $t = p/q$, the integers $a = q^2 - p^2$,
   $b = 2pq$ and $d = q^2 + p^2$ satisfy $a^2 + b^2 = d^2$, so $(a/d, b/d)$ is a unit
   vector. Route Z checks the triple on every row; route E builds the corners and checks
   unit edges, right angles, positive orientation and the corner mean.
   183 rows have $t = 0$ and 18 have $t = 1$, a quarter turn, so 201 squares are exactly
   aligned. Of the other 102, six lie within $10^{-9}$ degree of an axis, and 96 are
   turned, all the same way, by 1.93° to 26.14° from the nearest axis.
2. **There are exactly 303 of them.** The reader refuses any other row count (mutant
   R1).
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box exactly when
   its corners do, or equivalently when its centre clears each wall by the half-extent
   $(|a| + |b|)/(2d)$. Route Z decides the second form by four integer inequalities a
   square, route E the first.
   The least clearances are
   `60200000000010299100000000000060300000000010299/100000000000000000000000000000100000000000000000000000000000`
   $= 6.020000000001029\ldots \times 10^{-13}$ at the top wall (square 3, tilted by
   $1.1 \times 10^{-13}$ degree), $6.025000000001029\ldots \times 10^{-13}$ at the right
   (square 73), and $60300000000010299/10^{29}$ at the left (squares 0, 1, 2, 13, 15 and
   124 to 129) and at the bottom (62, 63, 64, 75, 77, 124, 136, 142, 148 and 154). Every
   square’s clearance of every wall is equal as a rational on the two routes, and no
   square touches a wall.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors
   exactly when a line parallel to an edge of one of them weakly separates them: the
   interiors meet exactly when the origin lies in the interior of their Minkowski
   difference, a convex polygon whose edges are parallel to the squares’ edges, so four
   axes decide a pair, and strictly separating ones decide that the closed squares are
   disjoint. Route Z decides every one of the 45,753 pairs this way, with no distance
   filter, and records each pair’s exact gap, the largest separation over the four axes.
   Route E decides every pair by another argument.
   A pair whose centres are more than $\sqrt{2}$ apart is disjoint, since each square
   lies in the closed disc of radius $\sqrt{2}/2$ about its centre; that decides 45,029
   pairs, by the exact comparison $|c_i - c_j|^2 > 2$. Two closed convex polygons meet
   exactly when an edge of one meets an edge of the other or a vertex of one lies in the
   other; route E decides each of the other 724 pairs so, by exact orientation tests,
   and finds that none meets.
   For each of those it computes the exact squared Euclidean distance as the least
   squared distance from a vertex of either square to an edge of the other, and the
   region the closed half-planes of one clip from the other, which is empty for all 724.
   Route E also recomputes every pair’s separating-axis gap from corner projections, as
   a comparison and not as its decision, and the two routes’ 45,753 gaps are equal pair
   by pair. The least gap, `60250000000010249/50000000000000000000000000000`, is at six
   pairs: squares 2 and 13, two aligned squares on square 2’s normal $v$, and (270,
   282), (273, 285), (275, 287), (281, 293) and (283, 295). Each of those six pairs’
   exact Euclidean distance is that gap.
   821 pairs lie below $10^{-11}$, every one of them at least $1.205 \times 10^{-12}$
   apart, and no other pair lies below $2.89 \times 10^{-4}$. 615 of the 821 are close
   pairs. The other 206 are corner-to-corner near-contacts whose centres lie just over
   $\sqrt{2}$ apart, which route E decides by their discs: two unit squares that meet
   have centres at most $\sqrt{2}$ apart, with equality only when they meet corner to
   corner. Of the 724 close pairs, the exact distance equals the gap at 721, and at every
   close pair whose gap is below $10^{-9}$.
5. **The side is the claim’s**, by the table above.

No route here rounds, dilates or tolerates.
Route Z never loads `fractions` (its receipt says so) and compares integers with every
denominator cleared: with $L$ the least common denominator of the side and the 606
centre coordinates (31 digits), a pair’s gap is
$(\max_k P_k - L(d_i d_j + |c_{ij}| + |s_{ij}|))/(2 L d_i d_j)$, where $P_k$ are the
four scaled projections of the centres’ difference and $c_{ij}$, $s_{ij}$ the integer
cosine and sine of the angle between the squares.

**Status.** That the five facts imply $s(303) \le S$ is proved by the argument above.
That this certificate has the five facts is computationally verified here, by exact
arithmetic on four routes.
Everything else the source states about the packing is asserted, and the mapped table
below says which parts were measured consistent.

The certificate is a dilation of a float packing, and its margins are the float
packing’s contacts opened by it.
The input’s squares at the left wall have centres at $x = 0.500000000000103$
(`s303_amund.input.txt`, line 2): $1.03 \times 10^{-13}$ clear.
Scaled about the box’s corner by $1 + 10^{-12}$, a square at the left or bottom wall
gains $5 \times 10^{-13}$, and two squares in contact gain $10^{-12}$ times their
centres’ distance along the contact normal.
So the left wall’s $6.03 \times 10^{-13}$ is $1.03 \times 10^{-13} + 5 \times 10^{-13}$,
and squares 2 and 13, whose centres the input puts $1 + 2.05 \times 10^{-13}$ apart
along their common normal (lines 4 and 15), end $1.205 \times 10^{-12}$ apart.
The dilation is how the certificate was made; the decision reads only the certificate.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`exact_verify` on `to_witness`, `V-sqpack-verify`) | unit shape, containment and every pair, by the exact separating-axis verifier | the `evand-cert` adapter (`upper_bound_reports.evand_cert`; `evand_exact_certificates.parse` and `basis_witness`), then `sqpack.witness.exact_verify` | with `independent`: the reader, the half-angle map and `Fraction`; with the source: the adapter’s line filter, transcribed from Evan Daniel’s two checkers, which the issue names as the author’s |
| `independent` (`check_squares` on `corner_squares`, `V-check-rational-witness-independent`) | the same facts, on corners | the same reader; corners from `evand_exact_certificates.Pose.corners`, which is `verify_cert2.py`’s `corners` term for term; `check_rational_witness_independent` | the reader and `Fraction`; the corner construction with the source |
| this review’s route Z (`review_t238_check.py`, integers) | the triple per row, half-extent containment, every pair by four integer inequalities | its own reader and CPython integers | its reader with route E; CPython integers with all; no code; the separating-axis method with `sqpack` and with `verify_cert.py` |
| this review’s route E (`review_t238_check.py`, `Fraction`) | unit edges, right angles, orientation and corner mean; corner containment; far pairs by discs, close pairs by edge and vertex tests, with exact distances and clipping | its own reader, corners, orientation tests and clipping | `Fraction` with the maintained routes; no code; its disc test and its edge and vertex tests are the mathematics of `verify_cert.py`’s filter and `verify_cert2.py`, which this reviewer read only after deciding |

Two readers read the certificate here, the maintained one and this review’s, and they
read the same side and the same 303 poses, literal by literal.
`agree_t238.py` holds this review’s reader to the `checker_input` of this lane’s
maintained run, which read the certificate’s bytes, and of the records lane’s, which
read its derived fact; it also holds the fact’s 303 centres and bases to the
certificate’s centres and the cosine and sine of its tangents.
The maintained reader admits decimal literals and skips blank and comment lines
anywhere; this review’s refuses decimals (mutant R2) and blank lines or comments after
the header (its self-test).
The certificate has none of these.

**What stays unchecked.** CPython’s integers are common to every route, and `Fraction`
to all but route Z. The custody of the bytes rests on the gist’s pin and on the digest,
matched here and in the records lane’s packet.

**The source’s checking.** The issue reports that Evan Daniel’s two checkers at
`7982d7a` accept the certificate, and that a third, unpublished check does.
At that pin, `search/exact/verify_cert.py` and `search/exact/verify_cert2.py` are
byte-identical to the registered `V-evand-verify-cert-py` (`3299ca0c…`) and
`V-evand-verify-cert2-py` (`55140a35…`). This review read them after its checker had
decided and ran neither.
The first decides containment by half-extents and pairs within $\sqrt{2}$ by separating
axes, the rest by discs.
On this file it would count 724 close pairs, as route E does and as the issue says, and
it computes the least wall clearance as this review does, which here is
$6.020 \times 10^{-13}$ (RF-1). The second decides close pairs by vertex containment and
closed-edge intersection, every corner strictly inside the open box, and prints the side
as `float(S)` to 20 digits (RF-2). No run of the author’s is retained.

## The Controls

The kernel’s two gross controls are refused by both maintained routes: a duplicated
square (gap $-1$), and square 0 moved right by $S + 2$ (clearance
$-3.000000000000603\ldots$). The margins are the ones this review’s routes give for the
same two mutants. This certificate keeps $6.02 \times 10^{-13}$ at the walls and
$1.205 \times 10^{-12}$ between pairs.
A route that rounded at binary64, or tolerated anything above $10^{-13}$, would accept
the certificate and still refuse both.
This review built 21 mutants (`sharp_controls_t238.py`, `outputs/sharp-controls.json`).
It decided each with both of its own routes and with both maintained routes, reached
through the `evand-cert` adapter as `certify`’s child reaches them:

| Mutant | Expected | Both maintained routes | This review’s checker |
| --- | --- | --- | --- |
| F0: the side lowered by the least top-or-right clearance, $6.020000000001 \times 10^{-13}$ at square 3’s top | accepted, a corner on the top wall | accepted, wall clearance exactly 0 | accepted, 0 on both routes; square 3 on the top wall |
| F1: and by $10^{-30}$ more | refused on a wall | refused at exactly $-10^{-30}$ | refused at $-10^{-30}$, square 3 |
| N0: every square moved left by the least left clearance, $6.030000000001 \times 10^{-13}$ | accepted | accepted, 0 | accepted, 0; eleven squares on the left wall |
| N1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused at $-10^{-30}$, the same eleven |
| B0: every square moved down by the least bottom clearance | accepted | accepted, 0 | accepted, 0; ten squares on the bottom wall |
| B1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused at $-10^{-30}$, the same ten |
| P0: square 13 moved toward square 2 along 2’s normal $v$ by the least gap, $1.205 \times 10^{-12}$ (two aligned squares) | accepted, an exact contact | accepted, least gap exactly 0 | accepted, gap 0; (2, 13) the one touching pair |
| P1: by the gap $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused, gap $-10^{-30}$; (2, 13) alone overlaps |
| Q0: square 177 moved toward square 165 along 177’s normal $u$ by their gap, $1.339 \times 10^{-12}$ (165 tilted by $-14.21°$, 177 aligned) | accepted | accepted, 0 | accepted, 0; (165, 177) touching |
| Q1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused; (165, 177) alone overlaps |
| T0: square 36 moved toward square 21 along 21’s normal $u$ by their gap, $1.2066 \times 10^{-12}$ (both tilted by $-23.26°$) | accepted | accepted, 0 | accepted, 0; (21, 36) touching |
| T1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused; (21, 36) alone overlaps |
| U0: square 116 moved toward square 92 along 92’s normal $v$ by their gap, $1.2114 \times 10^{-12}$ (tilted by $-25.11°$ and $-24.59°$) | accepted | accepted, 0 | accepted, 0; (92, 116) touching |
| U1: by that $+ 10^{-30}$ | refused | refused at $-10^{-30}$ | refused; (92, 116) alone overlaps |
| D0: square 202 moved onto square 191’s nearest corner, $1.207 \times 10^{-12}$ away on each axis (two aligned squares whose centres lie more than $\sqrt{2}$ apart) | accepted, a corner contact | accepted, 0 | accepted, 0; (191, 202) and (202, 203) touching, both decided by route E’s edge and vertex tests |
| D1: and $10^{-30}$ further on each axis | refused | refused at $-10^{-30}$ | refused; both pairs overlap, (191, 202) by an area of $10^{-60}$ |
| G1: square 1 replaced by a copy of square 0 | refused | refused, gap $-1$ | refused, gap $-1$ |
| G2: square 0 moved right by $S + 2$ | refused | refused, the same clearance | refused, clearance $-3.000000000000603\ldots$ |
| M1: every tangent negated, the mirrored reading | refused | refused, least gap $-0.2904$ | refused, 106 overlapping pairs, least gap $-0.2904$ |
| R1: the last row dropped | refused by both readers | `302 square rows for n = 303` | `302 square rows for n = 303` |
| R2: square 0’s $x$ written as its exact decimal | a reader difference, not a control | read exactly and accepted | refused by the reader |

D0 and D1 sit on the boundary of route E’s disc test, and of the kernel’s
`tightest_pair`, which skips pairs whose centres lie more than $\sqrt{2}$ apart.
Before the move the two centres lie just over $\sqrt{2}$ apart, at the corner contact
exactly $\sqrt{2}$, and past it closer.
All four deciders decide both correctly.

The kernel’s own `run_sharp` (`side-lowered-past-wall-contact` and
`tightest-pair-closed-past-contact`) was also run on the certificate.
At contact both maintained routes accept with the margin exactly 0, and past it both
refuse at exactly $-10^{-30}$. Its tightest pair, (2, 13), its gap, its closing normal
$(0, 1)$ and its top clearance equal this review’s (`agree_t238.py`). The records lane’s
own sharp-controls program in its packet was not run here.

## Identity, Measured

Whether two certificates are the same packing is not decided here.
What is measured is how far this packing lies from T-230’s and from the other packings
the record holds at 303, under the box’s eight symmetries applied to each reference in
its own box. Three things are measured.
First, whether nearest centres pair the squares one to one.
Second, under the assignment that minimizes the total squared centre displacement (this
review’s own Hungarian algorithm), how many squares lie within each distance, decided
exactly over the rationals, and how far squares turn modulo 90°. Third, the bottleneck,
the least largest move over all assignments (`identity_t238.py`,
`outputs/identity.json`).

| Against | Best symmetry | Nearest one to one | Within $10^{-9}$ | Within $10^{-3}$ | Beyond $10^{-2}$ | Beyond 0.1 | Beyond 0.5 | Largest move | RMS | Bottleneck | Turned beyond 1° | Tilts reversed |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T-230, `s303_r303w0.cert`, the house | the identity | yes | 37 | 231 | 31 | 12 | 1 | 0.547 | 0.0495 | 0.547 | 16 | 0 |
| `W-known-best-n303`, the house witness | the identity | yes | 37 | 231 | 31 | 12 | 1 | 0.547 | 0.0495 | 0.547 | 16 | 0 |
| T-186, Polkovskyi’s 14 October file, the house until 23 October | the identity | no | 36 | 166 | 108 | 70 | 9 | 0.910 | 0.197 | 0.910 | 68 | 44 |
| T-174 (PR #574) and #593, the same packing | the identity | no | 36 | 166 | 108 | 70 | 9 | 0.910 | 0.197 | 0.910 | 68 | 44 |
| T-162, Ostashev’s #562 | the identity | no | 36 | 167 | 107 | 68 | 7 | 0.910 | 0.183 | 0.910 | 68 | 44 |
| T-146, Daniel’s regularized lists | the transpose | no | 37 | 37 | 136 | 120 | 44 | 1.094 | 0.330 | 1.043 | 109 | 31 |
| T-136 (#481) and #573 | the mirror in $x$ | no | 37 | 37 | 138 | 119 | 44 | 1.094 | 0.329 | 1.043 | 110 | 31 |
| T-134 (#476) and #488, Couzo | the transpose | no | 36 | 36 | 264, 254 | 120, 121 | 53 | 1.094 | 0.329 | 1.000 | 105 | 29 |
| T-113 (#401) and T-138 (#470) | the identity | no | 37 | 37 | 266 | 113 | 53 | 1.094 | 0.325 | 1.005 | 100 | 29 |
| T-098, Daniel’s exact optima (#375) | the identity | no | 30 | 33 | 270 | 129 | 43 | 1.085 | 0.319 | 0.993 | 101 | 31 |

Against T-230 the assignment is the identity on row numbers, and it is also the
assignment that minimizes the total unsquared move.
The next symmetry, the transpose, has a total squared displacement of 22.29 against the
identity’s 0.743. The 37 squares within $10^{-9}$ of T-230’s lie within
$4.4 \times 10^{-15}$ of them, two within $10^{-20}$: they are squares the two float
packings place alike to their last digits.
231 squares lie within $10^{-3}$, 72 move beyond it, 31 beyond $10^{-2}$ (squares 5, 12,
16, 18, 23, 27, 32, 37, 39, 42, 46 to 49, 56, 57, 60, 67, 74, 130 to 133, 135 and 164 to
170\) and 12 beyond a tenth: squares 166 (0.547), 167 (0.419), 74 (0.266), 131, 168,
132, 5, 57, 67, 165, 130 and 169 (0.102). The column of squares at $x \approx 6.4$, 164
to 170, beside the upper-left band of tilted squares, slides down, by 0.53 at square 166
to 0.08 at square 170, while its three lowest squares turn and move left by about 0.1;
square 57, beside it at $(5.30, 14.26)$, turns and moves by 0.122. The column of aligned
squares at $x = 1.5$ above the bottom wall, 130 to 133, rises by up to 0.173. Square 74
moves left by 0.266 along the second row from the bottom, near the right wall, 67 right
by 0.117 and 5 down by 0.141. Thirteen squares of the upper band move by 0.010 to 0.059
(square 48), and squares 12, 47 and 135 by up to 0.017; every other square stays within
$10^{-2}$. Sixteen squares turn by more than 1°. Eleven of them, squares 16, 17, 19, 23,
26, 35, 37, 41, 46, 56 and 60, share one tilt, $-21.789°$ here against $-22.834°$ in
T-230. Square 164 turns from 0 to $-9.20°$, 165 from 0 to $-14.21°$, 166 from 0 to
$-17.85°$, and squares 57 and 167, T-230’s two near-axis squares at $-0.080°$ and
$-0.062°$, turn to $-17.84°$ and $-1.93°$. So five squares become tilted, and this
packing has 96 squares tilted beyond 0.1° against T-230’s 91. No tilt changes sign:
every tilted square in both packings is turned the same way.

**Contacts.** Both certificates are $10^{-12}$ dilations, so every contact of the float
packing appears as a gap or a wall clearance of about $10^{-12}$. In this certificate
every pair gap is either below $9.2 \times 10^{-12}$ or above $2.89 \times 10^{-4}$, and
every wall clearance is below $8.6 \times 10^{-11}$ or above $2.09 \times 10^{-4}$. In
T-230 the gaps are below $3.8 \times 10^{-12}$ or above $1.11 \times 10^{-4}$, and the
wall clearances below $2.8 \times 10^{-10}$ or above $2.55 \times 10^{-3}$. So a
threshold of $10^{-6}$ separates contacts from clearances in both.
Through the assignment, the two contact graphs share 812 of their pair contacts and 60
of their wall contacts.
T-230 has 850 pair contacts and 61 wall contacts; this packing has 821 and 60. Thirty of
T-230’s 38 lost contacts belong to one row of eleven aligned squares at height 11.41,
squares 176, 188, …, 284 and 296. In T-230 each lay against the next and touched the
squares diagonally beside it in the rows above and below.
Here the row slides left, by 0.0097 at square 176 down to 0.0002 at square 296, and
releases its ten contacts within the row and twenty corner contacts; square 296 also
leaves the right wall.
Four more are at squares 164 to 166, against 175 to 177, where the turned squares are,
and four are in the two tilted bands: (18, 39), (27, 48), (32, 38) and (86, 100). The 9
new contacts are (163, 164), (165, 166), (55, 164), (55, 165) and (27, 166), around the
turned squares, (22, 46), (39, 49) and (52, 55) in the upper band, and (105, 114) in the
lower. 52 squares’ contacts change, and the same five squares, 28, 57, 90, 119 and 167,
touch nothing in either packing (RF-6).

Against the older packings it measures as T-230 does, a little further off.
Against T-186, whose packing T-174 and #593 certify too and T-162 first reported, no
symmetry pairs the squares one to one: 70 squares move beyond a tenth, 166 lie within
$10^{-3}$, 68 turn beyond 1° and 44 tilts beyond 1° change sign.
Run on T-230’s certificate, the same program finds 64, 180, 52 and 44 for T-230 against
T-186 (`outputs/identity-t230.json`). Against the packings before Ostashev’s, from T-146
back to T-098, more than 110 squares move beyond a tenth under the best symmetry.

## How the Certificate Was Made

The issue says the certificate is a dilation certificate made with Evan Daniel’s
`search/packer/dilate_cert.py` at `7982d7a`: “the float64 packing’s centres and box
scaled by $1 + 10^{-12}$, coordinates rounded to rationals and each angle to a rational
half-angle tangent”.
The certificate’s comment line names the input file and the generator.
After its checker had decided, this review read `dilate_cert.py` at that pin (SHA-256
`a07082b7…`) and held the certificate to its formulas, written out in `method_t238.py`
and not run (`outputs/method.json`):

- The factor is $f = 1 + \mathrm{fl}(10^{-12})$: `Fraction(1e-12)`, the binary64 value
  of $10^{-12}$, so $f = 1 + 10^{-12} - 2.011335 \times 10^{-29}$.
- Each centre is the input’s decimal coordinate times $f$, rounded half to even at 30
  places. All 606 coordinates are reproduced exactly from `s303_amund.input.txt`.
- The side is the input’s side, $17.909762327457347$, times $f$, rounded up at 30
  places. It is reproduced exactly.
- Each tangent is `Fraction(tan(radians(deg % 90) / 2)).limit_denominator(10**15)` in
  binary64. On this host, CPython 3.14.7 on Linux, 267 of the 303 tangents are
  reproduced. Each of the other 36 is exactly the best approximation of the float one
  unit in the last place from this host’s `tan`: 25 above it and 11 below.
  Rows 4, 6 and 10, at $89.99999999999997°$ and $89.99999999999989°$, are among them;
  row 4’s $t = 1$ is the best approximation of the float one unit above this host’s
  tangent of half its angle.

The same formulas on this host reproduce T-230’s certificate from its retained input
(`s303_r303w0.input.txt`) in full: side, centres and all 303 tangents.
So both certificates are `dilate_cert.py`’s output from their published inputs, and this
one was computed where `tan` rounds some of these 36 arguments the other way.
The issue’s search ran on Apple hardware (“relaxed in a GPU batch (Apple Metal,
float32)”), whose mathematics library is not this host’s, which would account for it.
This measures how the file was made; it does not establish it (RF-3). Each certificate
tangent lies within $5.24 \times 10^{-16}$ of the exact half-angle tangent of the
input’s angle, and turns its square to within $5.7 \times 10^{-14}$ degree of it.

**The lineage statement.** The issue says the packing is “a new packing found from Evan
Daniel’s registered packing (#728, W-known-best-n303), not a refinement of it”, by a
search of random kicks, local melts, re-seated squares and rotated patches, and that
“the result differs in structure”.
What is measured agrees:

- **The start.** The rows are in T-230’s order, and the best assignment is row for row,
  as a search started from T-230’s certificate or from `W-known-best-n303` (the same
  squares in the same order) would leave them.
- **The step.** Twelve squares move beyond a tenth, so by the record’s word this is not
  a refinement of T-230’s packing, as the issue says.
  Most of the movement is in the column of squares 164 to 170 beside the upper tilted
  band, four of which turn (164 to 167), with square 57 beside them: where a rotated
  patch would be. The upper band’s eleven squares at one tilt turn together, and a column
  of aligned squares rises from the bottom wall.
- **The structure.** 47 of the contacts differ, and one row of eleven aligned squares is
  released.
- **The figures.** The issue’s largest move 0.547, 12 squares beyond 0.1, 31 beyond
  0.01, 96 tilted squares against 91 and sides $9.9 \times 10^{-6}$ apart are reproduced
  exactly.

## Newness in Report Order

Sides are each report’s exact side where the record retains it, and otherwise a print
(`margins_t238.py`, `outputs/margins.json`). Dates are those the record keys each report
by.

| Report | Reported | Side, rounded up at 16 places | $S$ below it by |
| --- | --- | --- | ---: |
| the basic grid | — | 18 | $9.023767252474 \times 10^{-2}$ |
| Kingbird, David Ellsworth’s catalogue, the record’s capture of 22 August (a print) | by 2026-08-22 | 17.9312789439468900 | $2.151661647163 \times 10^{-2}$ |
| the same catalogue, the capture of 30 September of its page of 24 September (a print; Ellsworth, refined by Tej Stead) | by 2026-09-24 | 17.9312550955619700 | $2.149276808671 \times 10^{-2}$ |
| Griffin Casson, `griffcass/square-packing` `82661bc` (a print) | 2026-09-24 | 17.9310563646295301 | $2.129403715427 \times 10^{-2}$ |
| Francisco Couzo’s first, `801915f` (the case record’s priority note, a print) | 2026-09-24 | 17.9285625410135480 | $1.880021353829 \times 10^{-2}$ |
| T-056, Couzo (a print) | 2026-09-27 | 17.9243492655479320 | $1.458693807268 \times 10^{-2}$ |
| T-092, Couzo (a print) | 2026-10-03 | 17.9243410098602500 | $1.457868238499 \times 10^{-2}$ |
| T-098, Daniel’s exact optima (#375) | 2026-10-05 | 17.9243410098511284 | $1.457868237587 \times 10^{-2}$ |
| T-113, Chaoweeraprasit’s SQUISH (#401) | 2026-10-07 | 17.9203123729203498 | $1.055004544509 \times 10^{-2}$ |
| T-134, Couzo (#476) | 2026-10-09 | 17.9174439254942359 | $7.681598018979 \times 10^{-3}$ |
| T-136, Chaoweeraprasit’s SQUISH (#481) | 2026-10-09 | 17.9130654627385328 | $3.303135263276 \times 10^{-3}$ |
| T-138, Polkovskyi’s decimal poses (#470) | 2026-10-09 | 17.9203123729190000 | $1.055004544374 \times 10^{-2}$ |
| T-146, Daniel’s regularized lists | 2026-10-10 | 17.9130654627385324 | $3.303135263276 \times 10^{-3}$ |
| #488, Couzo | 2026-10-10 | 17.9173656753523603 | $7.603347877103 \times 10^{-3}$ |
| T-162, Ostashev (#562) | 2026-10-12 | 17.9099582910699080 | $1.959635946512 \times 10^{-4}$ |
| #573, Polkovskyi | 2026-10-12 | 17.9130654627410000 | $3.303135265743 \times 10^{-3}$ |
| T-174, PingYou Ltd (PR #574) | 2026-10-13 | 17.9099582910699080 | $1.959635946512 \times 10^{-4}$ |
| #593, Polkovskyi | 2026-10-14 | 17.9099582910699080 | $1.959635946512 \times 10^{-4}$ |
| T-186, Polkovskyi’s KKT refinements (`70a033f`) | 2026-10-14 | 17.9099582910699080 | $1.959635946512 \times 10^{-4}$ |
| T-230, Daniel (#728), the house | 2026-10-22 | 17.9097722172743278 | $9.889799071009889799071 \times 10^{-6}$ exactly |

$S$ is below every one.
The margin below T-230 is the difference of the two float sides, times $f$: both files
are `dilate_cert.py` dilations, rounded up at 30 places.
The issue’s “9.89e-6” is that margin, rounded.
Of the issues opened since 22 October, #719, #732 and #734 make no claim at 303 (#732’s
rows start at 328), and the source-coverage register holds no other report there.
The issue’s list of issues that mention 303 includes #719, whose packet holds no file at
303\. The 23 October Kingbird capture (untracked, `attic/intake/`) still lists
17.93125509556197. This lane did not sweep the live heads of the watched repositories;
the records lane’s README reports that it did.

**Later counts.** Deleting squares from a packing of $m$ leaves a packing of any smaller
count in the same box, so $s(303) \le s(m)$ for $m > 303$, and a side is new only if it
is below every bound at every later count.
$S$ is below the verified and the reported upper bound at every count from 304 to 320 on
`main`; the least margin is $1.966543059992 \times 10^{-2}$, at 304. From 321 on, every
bound is at least $\sqrt{m} \ge \sqrt{321} > 17.916$ by area.

## Significance

The rubric is `epistemics.md`’s, and the score is of the claim.
The record’s line at this scale, read from its entries:

- **S2:** further arrangements and refinements of a packing already reported: T-188 at
  $9.29 \times 10^{-6}$, five squares beyond a tenth (“more than the exact re-solves …,
  less than T-172’s step”); T-198 at $1.15 \times 10^{-5}$ and T-199 at
  $1.32 \times 10^{-5}$, of de Winter’s design; T-228’s refinement at
  $5.05 \times 10^{-8}$.
- **S3:** new arrangements, from T-226 at $1.88 \times 10^{-5}$, which no symmetry pairs
  one to one with the house’s, “a substantive case result at the low end of S3, between
  T-198’s $1.15 \times 10^{-5}$ (S2) and T-223’s $2.04 \times 10^{-5}$”, to T-224 at
  $3.47 \times 10^{-5}$ and T-230 itself at $1.86 \times 10^{-4}$, each “well above
  T-188’s $9.29 \times 10^{-6}$ (S2)”, and T-219 at $4.46 \times 10^{-5}$, “above” it.

**S2.** A further arrangement of T-230’s packing at 303, $9.89 \times 10^{-6}$ below it
and below every report there: one to one with T-230’s packing under the identity, in its
row order, 12 squares beyond a tenth (at most 0.547), five squares newly tilted and a
group of eleven turned by 1.04°, 47 of about 860 contacts changed.
That is T-188’s case at T-188’s scale, a further arrangement of the house’s design with
a handful of squares beyond a tenth, and it lies below T-198’s $1.15 \times 10^{-5}$
(S2) and well below T-226’s $1.88 \times 10^{-5}$ at the low end of S3, an arrangement
no symmetry pairs one to one with the house’s. It moves the case’s 12-place print from
17.909772217275 to 17.909762327476, a citable detail of the case that moves no theorem.
It is not S3: it pairs one to one with the house’s packing, row for row, and no case
result beyond the side follows.
This score and rationale replace the records lane’s draft S3 (RF-5). An S2 result stays
out of News; the release records a coverage omission.

## Credit

The source says who did what.
The issue credits Amund Kristiansen (GitHub `amundsk`) and says the polish engine, the
certificate generator and the checkers are Evan Daniel’s; that the search started from
Evan Daniel’s registered packing at 303 (#728); and that “the search, the certificate
and this report were done by Claude (Anthropic), working in Claude Code at my direction,
using Evan Daniel’s open-source engine and checkers”.
The measurement supports crediting the certificate and the rearrangement to Amund
Kristiansen, and the packing as the record credits T-230’s: Evan Daniel’s arrangement of
Daniil Ostashev’s two-band design, found from Ostashev’s packing, here rearranged by
Kristiansen’s search.
Evan Daniel’s `dilate_cert.py` is measured as the certificate’s generator (RF-3), and
his `fq` quench is the issue’s, unmeasured.
That the search, the certificate and the report were done by Claude matters to the
independence record: this review is by the same system family (Rungs).

## The Source’s and the Record’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(303) \le 17.909762327476$, the side rounded up at 12 places | the issue’s claim; the gist README, lines 1 and 3 | **computationally verified here**: three exact programs, four exact routes, every pair decided |
| the side is `223872029093440709529093216833/12500000000000000000000000000` | the issue’s certificate table; README line 7 | **verified**: the header literal |
| “= 17.909762327475256427…” | the same places | **the binary64 print of the side**, not its expansion (RF-2) |
| $9.89 \times 10^{-6}$ below 17.909772217275, Evan Daniel’s #728 | the issue’s claim table | **verified**: $9.889799071009889799071 \times 10^{-6}$ below T-230’s exact side |
| a dilation certificate by `dilate_cert.py` at `7982d7a` of the float packing: centres and box scaled by $1 + 10^{-12}$, coordinates rounded, rational half-angle tangents, every square exactly unit | the issue; README lines 7, 8 and 11; the certificate’s line 1 | **measured consistent**, to the last digit for the side and centres, and for 267 tangents; 36 tangents one unit in the last place of `tan` apart; the factor is $1 + \mathrm{fl}(10^{-12})$ (RF-3) |
| `verify_cert.py`: VALID, least pair separation $1.2 \times 10^{-12}$, 724 close pairs | the issue, “Checking” | **consistent** with what this review measured; not run here |
| `verify_cert.py`: least wall clearance $8.2 \times 10^{-13}$ | the same | **not this file’s**: $6.020 \times 10^{-13}$ (RF-1) |
| `verify_cert2.py`: VALID, closed squares pairwise disjoint inside the open box, 724 close pairs | the same | **consistent**: no square touches a wall or another; not run here |
| a third, unpublished exact check accepts it | the same | **asserted**; not examined |
| the two public checkers share an author and the certificate format, and the certificate was made with the same author’s `dilate_cert.py` | the same | **true**; at the pin the checkers are byte-identical to `V-evand-verify-cert-py` and `V-evand-verify-cert2-py` |
| no exact KKT solve, local-optimality or rigidity analysis; only the upper bound is claimed | the issue, “Not done” | **agreed**; the packing is not rigid (RF-6) |
| a new packing found from #728’s (`W-known-best-n303`), not a refinement of it; it differs in structure | the issue, “Lineage and credit” | **measured consistent** (RF-4) |
| largest move 0.547; 12 squares beyond 0.1; 31 beyond 0.01; 96 tilted against 91; sides $9.9 \times 10^{-6}$ apart | the same | **reproduced exactly** |
| the search: 2,048 perturbed variants a round in float32 on Apple Metal, polished with Daniel’s `fq` quench, an iterated hill climb | the same | **asserted**; the 36 tangents are consistent with a host whose `tan` is not this one’s (RF-3) |

## Findings

Line numbers in the source are at `511f56b`, where square $k$, numbered from 0, is line
$k + 3$ of the certificate and line $k + 2$ of the input.

**RF-1, minor, non-blocking: the least wall clearance the issue quotes is not this
file’s.** The issue’s “Checking” section gives `verify_cert.py`’s output as “min wall
clearance 8.2e-13, min pair separation 1.2e-12”. The certificate’s least wall clearance
is $6.020000000001029 \times 10^{-13}$, at the top wall (square 3, line 6), decided
alike on four routes.
`verify_cert.py` at `7982d7a` (lines 38 to 43) takes the least of $x - e$, $S - x - e$,
$y - e$ and $S - y - e$ over the squares, the quantity this review computes, and prints
it to three digits (line 66), so on this file it reads “6.020e-13 (square #3)”. Its pair
figure and its count of 724 close pairs are this file’s. The records lane’s draft
`source_checks` repeats the author’s $8.2 \times 10^{-13}$ without the measured value.
No bound depends on it.
Proposed: the register states the measured clearances and says that the issue reports
$8.2 \times 10^{-13}$; Question 1 asks where it came from.

**RF-2, note: the side’s decimal in the issue and the README is its binary64 print.**
README line 7 and the issue’s certificate table give “S′ =
223872029093440709529093216833/12500000000000000000000000000 = 17.909762327475256427…”.
That decimal agrees with $S$ to 15 places and is the binary64 value nearest $S$,
$17.90976232747525642707842\ldots$, as both of Daniel’s checkers print it
(`float(S):.20g`, `verify_cert2.py` line 67). $S$ itself is
$17.90976232747525676232745734664$. The claimed bound, 17.909762327476, is $S$ rounded
up at 12 places, and is unaffected.
Proposed: the record prints $S$ exactly or rounded up, and quotes no 20-digit print.

**RF-3, note: the method statement, measured to the bit.** How the Certificate Was Made
gives the measurement: `dilate_cert.py`’s formulas reproduce the side and all 606 centre
coordinates from `s303_amund.input.txt`, and 267 of the 303 tangents on this host.
Each of the other 36 is the best approximation of a float one unit in the last place
from this host’s `tan`. The same formulas reproduce all of T-230’s certificate from its
input. The factor is $1 + \mathrm{fl}(10^{-12})$, $2.011335 \times 10^{-29}$ below
$1 + 10^{-12}$, which the issue rounds to $1 + 10^{-12}$. No bound depends on this.
Proposed: the record’s method line says “a dilation certificate, by Evan Daniel’s
`dilate_cert.py` at 7982d7a, of the binary64 packing the gist publishes beside it; its
side and centres are that program’s output from that input to the last digit, and its
tangents to within one unit in the last place of the platform’s tan (measured)”, citing
`outputs/method.json`.

**RF-4, note: the arrangement is T-230’s, rearranged.** Identity, Measured and the
lineage statement give the measurement: one to one with T-230 under the identity, row
for row in T-230’s order, 12 squares beyond a tenth and 31 beyond $10^{-2}$, most of
them in a column beside the upper tilted band, five squares newly tilted, one group of
eleven turned by 1.04°, and 47 contacts changed.
That is “not a refinement” in the record’s sense, as the issue says; and, unlike T-230
against T-186’s packing, it pairs one to one with the house’s packing under the
identity.
Proposed: the register’s claim and the case record call it “another arrangement
of T-230’s packing, found from it, not a refinement of it”, cite
`outputs/identity.json`, and give the issue’s figures as reproduced.

**RF-5, note: the significance is S2, not the draft S3.** The Significance section gives
the reasons: T-188’s scale and kind, below T-198’s $1.15 \times 10^{-5}$, both S2, and
well below T-226, the low end of S3. The records lane’s declaration drafts 3. Proposed:
score 2, with this review’s rationale and `by` naming this review.

**RF-6, note: the packing is not rigid, and no local-minimum claim follows.** The five
squares that touch nothing, 28, 57, 90, 119 and 167, keep clearances of at least
$4.67 \times 10^{-3}$ (square 28; 57 and 167 keep $1.20 \times 10^{-2}$) to every other
square and every wall, by the exact separating-axis gaps and wall clearances.
A square whose gaps all exceed $c$ can be translated by any vector shorter than $c$,
since the gap is a lower bound on the Euclidean distance.
So the packing admits non-trivial feasible motions at its side; that is computationally
verified by the exact clearances.
The issue makes no optimality, KKT or rigidity claim and calls the float packing “a
converged polish, not an exact stationary point”.
Proposed: the record carries no local-minimum, KKT or rigidity statement for this
certificate beyond “not rigid”.
Its rigidity block at 303 should be revisited when the house moves.

**RF-7, note: the maintained replay shares the producer’s components, as for T-230.**
The issue names Daniel’s two checkers as the author’s checks and his `dilate_cert.py` as
the generator. The maintained routes read the certificate through an adapter whose line
filter and corner construction are those checkers’, transcribed, as
`evand_exact_certificates`’ module statement says.
So the records lane’s replay is re-implemented sharing named components
(`shared-components`), as T-230’s is, and the independent re-implementation rests on
this review’s checker, which shares no code with either.
Its routes share mathematics with the source’s checkers, which this reviewer read only
after deciding: route Z’s separating axes are `verify_cert.py`’s, and route E’s discs
and its edge and vertex tests are `verify_cert.py`’s filter and `verify_cert2.py`’s
test. Proposed: the records lane’s replay entry records `shared-components` with those
two components, and this review’s entry records the shared methods in its independence
note.

**RF-8, note: custody.** The gist states no licence, holds one revision, `511f56b`, and
was committed 37 seconds before the issue opened.
The records lane keeps a derived fact and no upstream byte, and this review found the
fact to hold the certificate’s numbers exactly (`agree_t238.py`). The certificate’s line
1 names the input file, which the gist holds, and the generator.
Proposed: the record cites `511f56b` and the two digests; Question 3 asks whether the
bytes may be retained.

**RF-9, note, for the record: retain and register this review’s programs.** Until they
sit in the packet with their README they are scratch files the record cannot cite.
Proposed: the packet’s `review/review-2026-10-23/`, as laid out here.
`review_t238_check.py` decides, and `sharp_controls_t238.py` with
`maintained_routes_t238.py` are premise checks; all three belong in `verifiers.yaml`
with their independence records.
`margins_t238.py`, `method_t238.py`, `identity_t238.py` and `agree_t238.py` decide
nothing, and the README says so.

## Questions for the Author

1. The issue gives `verify_cert.py`’s least wall clearance as $8.2 \times 10^{-13}$. On
   `s303_amund.cert` at `511f56b` the checker computes $6.020 \times 10^{-13}$ (square
   3, at the top wall); its other figures, $1.2 \times 10^{-12}$ and 724 close pairs,
   are this file’s. Which run or file did $8.2 \times 10^{-13}$ come from?
2. 36 of the certificate’s tangents differ by one unit in the last place of `tan` from
   what `dilate_cert.py` computes from `s303_amund.input.txt` on Linux; its side and
   centres agree to the last digit.
   Was the certificate made with `dilate_cert.py` at `7982d7a` from that file on macOS,
   or elsewhere?
3. The gist states no licence, so the project keeps only facts derived from the
   certificate. May it retain the certificate file itself, and the input, in its packet?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, once the records lane’s replay
evidence and this review are entered.
That needs the derived fact the packet retains in place of the certificate (RF-8), a
replay command (`check --replay`), a passing replay, retained controls refused by every
route that accepted the positive, and sharp controls refused here.
The maintained replay is the records lane’s. It is re-implemented sharing named
components with the producer (RF-7). This review’s checker is a clean-room
re-implementation.
Before it decided, its author had read the certificate, the issue, the
gist README, the mathematics and the model review’s account of its checker (Disclosure),
and never the source’s, Evan Daniel’s or the maintained routes’ code.
The program has not changed since (SHA-256 `ba967921…8480`). It was written by a Claude
agent, and the issue says the search, the certificate and the report were done by
Claude, so the authorship overlaps the producer’s in system family: *independently
re-implemented, clean-room, by a Claude agent, a system family the producer also used*.

By the house rule, once the entry stands at `V3`/`C3` with this review mapped as its
accepted review, it holds the smallest validated side at 303. It is then adopted and
regularized in the same pull request, and T-230 stays retained as history.
It does not reach `V4`/`C4`, which need a second accepted adversarial review by a
distinct reviewer and a retained human oversight record.
No lower bound, optimum, local minimum or priority follows; no rigidity follows either,
beyond RF-6’s “not rigid”.

## Proposed Record Changes

For the records lane; this review writes none of them, and `record-changes.md` beside
this review’s output gives each in full.

- **`evidence.yaml`.** The records lane’s confirming replay entry, `shared-components`,
  with `limitations` citing this review’s controls receipts.
  An entry for this review’s checker: `independent-implementation`, `coverage: full`,
  `clean_room: true`, `shares: []`,
  `read: [mathematics, specification, certificate-format]`,
  `overlaps_producer: system-family`. This document is `external_review` on the reported
  entry.
- **`verifiers.yaml`.** Register `review_t238_check.py` (decides) and
  `sharp_controls_t238.py` with `maintained_routes_t238.py` (premise checks), with the
  digests in `outputs/program-digests.sha256`.
- **`results.yaml`.** The entry’s `reviews` gains this document (`kind: adversarial`,
  `reviewer_kind: ai`, `relation: project`, `verdict: accepted`). Its significance is S2
  with the rationale above, `by` naming this review (RF-5); its `source_checks` and
  method say what RF-1 to RF-3 propose; it calls the packing what RF-4 proposes; and it
  states no local-minimum claim (RF-6).
- **The case record.** Adopt the certificate at 303 and regularize it, by the house
  rule; T-230 stays retained as history.

## Comparison with the Earlier Review

No earlier review of this result exists.
The earlier review of the case is the 22 October review of T-230
([`review-2026-10-22-daniel-728.md`](review-2026-10-22-daniel-728.md)), which reviewed
T-230’s certificate, not this file.
This review read it only after its findings above were written (17:14Z on 23 October),
together with the records lane’s packet README and its `measure/identity.json`, and the
evidence and registry entries of that review’s programs, for the shape of the proposed
record changes. What it had seen of that review before is in the Disclosure: T-230’s
register entry and the case record’s section on T-230.

**Agreements.**

- **The method.** Both reviews decide the same five facts with a clean-room checker on
  two exact routes, route Z by the same mathematics, and hold the maintained routes to
  every shared number.
  Its second route decides pairs by clipped area; this review’s route E decides them by
  discs and by edge and vertex tests, with clipping as a check.
- **The side’s print.** Its RF-5, that `verify_cert2.py` prints the side as a binary64,
  is this review’s RF-2, for this file.
- **The adapter.** Its RF-1, that the maintained adapter transcribes the source
  checkers’ line filter and corner construction, is the basis of RF-7 here.
  `evand_exact_certificates`’ module statement now says so, and T-230’s register entry
  records the maintained replay as sharing those components, as RF-7 proposes here.
- **The controls.** Its RF-2, that the replay contract runs gross controls only, holds
  for this packet’s receipt too.
  The records lane added a sharp-controls program to the packet, and this review’s 21
  mutants and the kernel’s `run_sharp` pass on all four deciders.
- **The significance line.** Its line, refinements and further arrangements below about
  $1.4 \times 10^{-5}$ at S2 (T-188, T-199) and new arrangements from about
  $2 \times 10^{-5}$ at S3, is the line this review applied.
  Its S3 for T-230 rests on T-197’s case at $1.86 \times 10^{-4}$, nearly twenty times
  this margin.
- **The identity of T-230.** Its figures for T-230 against T-186 (64 squares beyond a
  tenth, 8 beyond half a unit, 180 within $10^{-3}$, 52 turned beyond 1°, largest move
  0.910, RMS 0.188) are reproduced by this review’s program run on T-230’s certificate.
  Its “tilt reversed”, 24, counts only reversals to the same angle within 1°; this
  review counts every tilt beyond 1° that changes sign, 44 for T-230 and 44 for this
  packing against T-186.
- **The tilt count.** Its RF-3 asked for a threshold with any tilt count, because
  T-230’s squares 57 and 167 lie at 0.080° and 0.062°. Here those two squares are turned
  by 17.84° and 1.93°, and the issue’s 96 holds at every threshold from $10^{-9}$ degree
  to 1.9°.
- **Local optimality.** Its RF-7 records that the source predicted a further descent of
  about $5 \times 10^{-7}$ for T-230’s arrangement and that a certificate of it that
  much lower would be a refinement.
  This certificate is about twenty times lower and is not a refinement of that
  arrangement, so it is not that descent.

**What this review adds about T-230.** That review found T-230’s side
$1 + 1.000025 \times 10^{-12}$ times the binary64 input side, and $4.5 \times 10^{-16}$
above the exactly dilated binary64 side.
Both certificates are `dilate_cert.py`’s output from the decimal text of their inputs,
with the factor $1 + \mathrm{fl}(10^{-12})$: T-230’s to the last digit of its side,
every centre and every tangent.
So the $4.5 \times 10^{-16}$ is the input’s decimal against its binary64 value, times
the factor (`outputs/method.json`, `reference`).

**The records lane’s packet.** Its README and identity receipt agree with this review at
every number they share: the side and its prints, the binary64 reading of the long
decimal, the replay’s margins, the identity figures against T-230 (one to one; 12, 31
and 72 beyond a tenth, $10^{-2}$ and $10^{-3}$; largest move 0.547 and largest turn
17.85°), the 96 tilted squares at 1.93° to 26.14°, the five newly tilted squares, and 68
to 70 squares beyond a tenth, with 44 opposite tilts, against Ostashev’s packing.
Its dilation check finds every centre within $4.9 \times 10^{-31}$ of the dilated input
and every angle within $5.7 \times 10^{-14}$ degree; this review reproduces the centres
exactly with `dilate_cert.py`’s rounding, and the tangents to one unit in the last place
(RF-3). It quotes the issue’s $8.2 \times 10^{-13}$ as the author’s report beside its
own measured $6.020 \times 10^{-13}$, and does not say that they differ (RF-1). Its
comparison table holds the registered and pending reports, without the Kingbird
catalogue, Casson’s packing or Couzo’s first; it calls the packing “a new arrangement”
and drafts S3, which RF-5 changes.

**Changed after reading.** The report-order table gained the Kingbird catalogue’s two
captures, 17.93127894394689 and 17.93125509556197, which the 22 October review lists and
which this review had wrongly taken to be absent at 303; `margins_t238.py` now reads
them from the record’s captures.
The comparison of tilt reversals with T-230’s now rests on this review’s own run on
T-230 (`outputs/identity-t230.json`) rather than on the 22 October review’s stricter
count. No finding changed.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, novelty or priority, and no rigidity beyond
RF-6; no human oversight.
No run of the source’s or Evan Daniel’s programs: `dilate_cert.py`’s formulas were
written out and compared, not run.
No decision of whether two certificates are the same packing.
No house adoption, case-record change or regularization at the new side, and no sweep of
the watched repositories’ live heads.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
