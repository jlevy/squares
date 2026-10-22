# Review: Mykhailo Polkovskyi’s Certificates at 105 and 204 from Issue #719 (T-229)

**Date:** 22 October 2026. **Verdict: accepted at both certificates, for finite
feasibility only, with findings on the record.** The two rational certificates that
issue #719 names inside the case corpus, `certificates/n-105.cert` and
`certificates/n-204.cert` at `Mishapolk/square-packing-records@12fc4667`, prove the
upper bounds the register entry T-229 states: 105 and 204 unit squares with pairwise
disjoint interiors in the closed box of each header side, and each side is the one the
claim states. No square touches a wall and no two squares touch.
At 105 every wall clears by exactly $5 \times 10^{-21}$ and every pair by
$9.999999999999988 \times 10^{-21}$; at 204 every wall clears by
$4.9998207 \times 10^{-13}$ and every pair by $9.980857291582 \times 10^{-13}$. A
checker written for this review decides both on two routes, from the source’s
certificates and from the packet’s derived facts, which state exactly the same squares.
It shares no code with the maintained routes or with the source, and its author read
none of them before it ran.
It agrees with the packet’s receipt and with both maintained routes at every number they
share. Sharp controls at $10^{-30}$, which the packet lacks, are refused by all four
deciders, and exact contact is accepted by all four.
Each side is below every earlier report at its count, in report order and by exact
arithmetic wherever a retained file states the side, and below the house best packing
when it was reported: T-174 by $5.1834384423 \times 10^{-12}$ at 105 and T-225 by
exactly $1.0063597267311130871459 \times 10^{-8}$ at 204.

Nine findings are recorded, none blocking.
One is major: the issue names this repository’s `sqpack/verify.py` as one of its two
checkers. That file decides the maintained `exact_verify` route, so the packet’s replay
is not independent of the producer’s named checking on that route (RF-1). As the issue
writes the command, that file never reads the certificate: it has no command-line entry
point at any revision and exits 0 on anything, a duplicated square included (RF-2). At
204 the square the record calls “re-oriented” is released: it is held within
$1.2 \times 10^{-20}$ by four neighbours in T-225 and touches nothing within
$1.25 \times 10^{-2}$ in #719 (RF-3). The draft significance S2 is confirmed, but the
rationale’s 105 sentence, which scores that count as padding (S1), is changed.
105 is a refinement that is not padding, as T-190 is (RF-5).

This is the Stage 4 mathematical review lane of the 22 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
`think-4h23`, covering the one entry, T-229, that the records branch for #719
(`claude/intake-2026-10-22`, read at `56d6d0d6d`) registers at V0/C0, pending adoption
at both counts.
T-229 is not yet on `main`. This review names it as that branch registers
it, and is to land with or after that registration.
It was written by an AI reviewer of the Claude system family (Anthropic), strong
sub-agent tier (`tbd-strong-max`), at maximum reasoning, as lane `c-review-t229-math`.
The lane was prompted separately from the import lane that built the packet
(`c-lane-719-import`) and from any reviewer of the records pull request.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row, adopts no house best packing and edits no bead.
Its programs and receipts are proposed for retention in the #719 packet (RF-8), and the
proposed record changes are listed at the end.

**For the author.** Both of your bounds hold exactly at the sides your certificates
state. Three exact decision programs that are not your code decided them: the two
maintained routes of this repository’s replay, and a checker written for this review.
One of the maintained routes runs this repository’s `sqpack/verify.py`, which your issue
names as your second checker (RF-1). As your issue writes the command, that file reads
no certificate (RF-2), so we ask how you ran it (Question 1). Your sides were each the
smallest reported at their count when you reported them.
At 204 your certificate frees one square that the earlier packings hold fast, and we ask
how that came about (Question 2). The other findings concern this repository’s record,
not your certificates.

## Claims Covered

T-229 claims $s(n) \le S_n$ at 105 and 204, with $S_n$ the header side of the source
certificate its packet derives a fact from, within the record’s horizon (1 to 324).

| n | Exact side $S_n$ | Exact decimal | Issue’s print (binary64, 16 places) | Record’s ceiling (16 places) | Certificate at `12fc4667` | SHA-256, Git blob |
| ---: | --- | --- | --- | --- | --- | --- |
| 105 | `674331486483935962030285457609/62500000000000000000000000000` | 10.789303783742975392484567321744 | 10.7893037837429748, **below the side** | 10.7893037837429754 | `certificates/n-105.cert` | `15b8044a…`, `ef9c91b` |
| 204 | `882663895519250432/59604644775390625` | 14.808642830527896655757312 | 14.8086428305278961, **below the side** | 14.8086428305278967 | `certificates/n-204.cert` | `7c77ad00…`, `17e243a` |

Each side equals the claim’s fraction (`results.yaml:31399–31401` on the records
branch), `claims.json`’s exact side, and the importer’s `offered_side`, which is the
side’s exact decimal expansion.
The packet’s ceiling is the side rounded up at 16 places, and the ledger’s print is the
side rounded up at 12 (10.789303783743 and 14.808642830528). The issue’s “Certified Side
S (16 dec)” is each side’s binary64 value printed at 16 places, and at both counts it
lies below the exact side, so it is no upper bound as printed.
The record states the exact sides, so nothing in it depends on the print
(`margins_t229.py`, `out-margins.json`).

Each certificate’s Git blob is the same at the source’s first commit of it (`1851c2c`,
2026-10-22T05:29:48Z) and at the issue’s pin `12fc4667`. Its SHA-256 equals the packet
manifest’s and the derived fact’s `revision_sha256`. Each derived fact’s SHA-256 and Git
blob equal the packet README’s Compressed Files row (`out-check-*.json`,
`out-same.json`).

**Read in full.** The packet README; `acquisition/claims.json`’s rows at 105 and 204;
the declaration’s profile and replay roster; the issue body’s table rows at 105 and 204
and its lines on checkers; both derived facts; both pin certificates; the entry
(`results.yaml:31391–31543`); its report atom (`evidence.yaml:41642–41669`); and the
receipt’s six jobs. In the record: the rows at 105 and 204 of the 14, 16, 18, 19 and 21
October ledgers, the 22 October backlog ledger and #719’s own ledger, and the front
matter of `n-105.md` and `n-204.md` on `main`. The packet’s `earlier-publications.json`
rows at both counts, the significance rationales of 22 nearby entries, and the
`regularizations` schema text.
Stage 4 and the house rule of `result-import.md`, and `epistemics.md` on verification,
confirmation, the independence record, review records, significance and results by
others. From the source, read as data: its README’s verification lines.
After this review’s checker had run, it also read the first thirty lines of
`check_packing.py` and searched it for its arithmetic and tolerance.
Of the maintained routes, these were read after this review’s checker had run:

- `upper_bound_reports`: `replayed_facts`, `check_certification`, `receipt_parts`,
  `run_job`, `certify`, `decide_job`, `fact_witness`, `certificate_from_witness`,
  `read_fact`, `read_facts`, `evand_cert`, `parse_certificate`, `admit`, `check_claims`
  and `main`;
- `evand_arrangement_reports`: `checker_input`, `job_input`, `sharp_input`, `run_sharp`,
  `to_witness`, `run_case`, `stable_row`, `validate_receipt`, `replay_receipt` and
  `decide_job`;
- `evand_exact_certificates`: `Pose`, `parse`, `basis_witness`, `corner_squares`,
  `decide`, `tightest_pair`, `overlap_control`, `top_clearance` and `shrink_controls`;
- `sqpack/verify.py`’s import lines, and a search of every revision for an entry point.

Not read at any time: `sqpack/verify.py`’s deciding code,
`check_rational_witness_independent`’s code, `sqpack/witness.py`, the source’s named
checkers (which are not in its tree), and any earlier review’s programs.

**Disclosure.** Before writing its checker, this reviewer read the 22 October review of
T-226 to T-228 (`review-2026-10-22-couzo-670-672-675.md`, not yet on `main`) and its
README as the brief’s model.
Both describe that review’s checker: integer separating axes and a `Fraction` clipping
area, the pair of methods the brief also suggests, and the pair this checker uses.
That review decided other certificates, so this review’s independence record lists
`earlier-review` among what its author read.
The reviewer had also read the packet README, which reports the receipt’s margins, the
stage 1 triage’s in-corpus notes, which report the maintained routes’ margins and the
identity figures, and the entry, whose notes give the same figures.
It read the packet’s own identity measurement only after its own had run.
No earlier mathematical review of T-229 exists.

## Replays Reproduced Here

Run on 22 October 2026 against the records branch at `56d6d0d6d` (the worktree, on
`PYTHONPATH` ahead of the shared virtual environment, whose lockfile is the branch’s)
and `main` at `76496462b`. CPython 3.14.7, under `nice -n 10` on a shared host, at most
two processes.

| Command | What it decides | Outcome | CPU |
| --- | --- | --- | --- |
| `python -m devtools.acquire_source mishapolk-issue719-2026-10-22 --check` | the packet against its acquisition contract | `PACKET_MATCHES_ITS_CONTRACT` | 0.3 s |
| `python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 check-claims` | the frozen comparison rebuilt | equal to the retained `claims.json` | 22.2 s |
| `python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 check --replay` | all six jobs again on both maintained routes, each held to its retained row | `2 certificates and 6 jobs admitted` | 49.1 s |
| `python -I review_t229_check.py selftest`, under 3.14.7 and 3.13 | the checker on 21 hand-built packings and 6 reader cases | 27 of 27 as expected, both interpreters | under 1 s |
| `python -I review_t229_check.py check`, two processes | this review’s checker, both routes, each count’s certificate and fact | 4 of 4 accepted, the routes agreeing pair by pair | 3.0 s and 7.0 s |
| `python -I review_t229_check.py same` | that each fact states exactly its certificate | 105 of 105 and 204 of 204 rows equal | under 1 s |
| `python -I agree_t229.py` | the checker’s numbers against both receipt routes | every field equal | under 1 s |
| `python sharp_controls_t229.py`, two processes | eight mutants a certificate through all four deciders, and the kernel’s `run_sharp` | every mutant decided as required | 34 s and 90 s |
| `python -I margins_t229.py` | the sides in report order, against the house and every later count | as the entry claims | under 1 s |
| `python -I identity_t229.py`, three runs | each packing against its kin | as tabulated below | under 3 s |

The receipt’s positives pass both routes with `pairs_tested` $= n(n-1)/2$ (5,460 and
20,706). Its two controls at each count, a duplicated square and square 0 moved outside,
are refused on both routes.
`check --replay` decided every job again and found every stable field equal.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors. A certificate is a comment line, a header `n S` and $n$ rows `x y t`, each a
rational literal: a rational side, a rational centre and $t = \tan(\theta/2)$. Its own
format line states the reading, $(c, s) = ((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2))$. The
packet keeps no upstream byte; its derived fact is a Witness/v2 `center-basis` record of
the same squares, each a centre and the unit vector $(c, s)$. This review reads both.
The bound $s(n) \le S$ follows from six facts, each decided over $\mathbb{Q}$ or fixed
by the format:

1. **The fact is the certificate.** Row by row, the fact’s centre equals the
   certificate’s and its basis equals the half-angle map of the row’s $t$, as reduced
   fractions, and the two sides are equal (`same`, `out-same.json`). So deciding either
   decides the source’s file.
   The maintained adapter’s certificate also equals the packet’s fact, as `read_facts`
   admits it (`adapter_equals_packet_fact` in the controls receipts).
2. **Each rotation is on the unit circle.** For $t = p/q$ in lowest terms, the integers
   $a = q^2 - p^2$, $b = 2pq$ and $d = q^2 + p^2$ satisfy $a^2 + b^2 = d^2$. So
   $(a/d, b/d)$ is a unit vector, and the row states a unit square centred at $(x, y)$.
   Route Z checks the triple on every row of both forms, clearing the fact’s two
   denominators to one.
   Route C checks unit edges, right angles, positive orientation and the corner mean on
   the four corners it builds.
   Rows with $t = 0$ are axis-parallel: 62 of 105 and 127 of 204.
3. **There are exactly $n$ of them.** Both readers refuse a row count other than the
   header’s (mutant R1), and the fact reader refuses ids other than $1, \dots, n$ in
   order.
4. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box if and only
   if its corners do, equivalently if its centre clears each wall by its half-extent
   $(|a| + |b|)/(2d)$. Route Z decides the second form as four integer inequalities a
   square, route C the first.
   The least clearance is exactly $1/(2 \times 10^{20})$ at 105 (square 4, the left
   wall) and $37251567/74505805969238281250 \approx 4.9998207 \times 10^{-13}$ at 204
   (square 1, the right wall).
   No square touches a wall.
5. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors if
   and only if a line parallel to an edge of one of them weakly separates them.
   The Minkowski difference of the two squares is a convex polygon whose interior misses
   the origin exactly when the interiors are disjoint, and its edges are parallel to the
   squares’ edges, so four axes decide a pair.
   Route Z decides every one of the $n(n-1)/2$ pairs this way, with no distance filter,
   and records each pair’s exact gap, the largest separation over the four axes.
   Route C decides every pair, again with no filter, by the exact area that one square’s
   four closed half-planes clip from the other.
   That area is positive if and only if the interiors meet, and a clip that leaves only
   a point or a segment is a contact.
   For every pair whose centres are closer than 2 it also computes the exact squared
   Euclidean distance between the closed squares, the least over each vertex and each
   edge of the other. Every other pair is at least $2 - \sqrt 2$ apart.
   The two routes classify every pair the same (disjoint, touching or overlapping).
   Every pair is disjoint: no gap is 0 and no clip is non-empty.
   The least gaps are $9.999999999999988 \times 10^{-21}$ at 105 (squares 71 and 86,
   numbered from 1, on square 71’s edge normal) and $9.980857291582 \times 10^{-13}$ at
   204 (squares 11 and 17). The least Euclidean distances are at the same pairs and are
   no smaller, as they must be.
   Each least gap and clearance is the receipt’s `minimum_best_pair_gap` and
   `minimum_containment_clearance` as an equal rational.
6. **The side is the claim’s**, by the table above.

No route here rounds, dilates or tolerates.
Route Z uses no `fractions` at all: it clears every denominator and compares integers.
A pair’s gap is $(\max_k L_k - R)/(2 d_i d_j D_x D_y)$, with $D_x, D_y$ the products of
the two centres’ denominators, $L_k$ the four scaled projections and
$R = D_x D_y (d_i d_j + |C| + |S|)$, where $C$ and $S$ are the integer cosine and sine
of the angle between the squares.
Route Z counts 232 pairs at 105 and 498 at 204 whose centres lie within $\sqrt 2$. These
equal the candidate pairs of the triage’s filtered maintained run.

The margins are fine.
At 105 the least wall clearance and pair gap are about $2 \times 10^{5}$ to
$4 \times 10^{5}$ times smaller than the binary64 spacing of the coordinates there
($1.8 \times 10^{-15}$ at side 10.8). A binary64 checker, or one with a tolerance of
$10^{-15}$ or more, cannot decide this certificate either way.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (`legacy.exact_verify` on `kernel.to_witness`, `V-sqpack-verify`) | unit shape, corners in the box, every pair by exact separating axes | the fact reader (`certificate_from_witness`) or the `evand-cert` adapter (`legacy.parse`), the half-angle map `Pose.basis`, `basis_witness`, `sqpack.witness.exact_verify`, which calls `sqpack.verify.verify_packing` | with `independent`: the readers, the half-angle map, `Fraction` and the separating-axis method; **with the source: `sqpack/verify.py`**, which the issue names as its second checker (RF-1) |
| `independent` (`check_squares` on `corner_squares`, `V-check-rational-witness-independent`) | the same facts on corners built by `Pose.corners` | `check_rational_witness_independent` | the same readers, half-angle map, `Fraction` and method; with the source, nothing the source names |
| this review’s route Z (`review_t229_check.py`, integers) | Pythagorean triple per row, half-extent containment, every pair by four integer axis inequalities | its own readers and CPython integers | its readers with route C; with the maintained routes, CPython integers and the separating-axis method; no `fractions`, no code |
| this review’s route C (`review_t229_check.py`, `Fraction`) | unit edges, right angles, orientation and corner mean; corner containment; every pair by exact clipping area, and the exact distance of every pair within 2 | its own readers, corners, clipping and distances | `Fraction` with the maintained routes; clipping area and distance with no maintained route |

Two pairs of readers exist here: the maintained fact reader and `evand-cert` adapter,
and this review’s fact reader and certificate reader.
All four read the same sides and the same 309 poses (`agree_t229.py`, `same`, and the
controls’ adapter check).
The maintained certificate reader admits decimal literals and reads them exactly; this
review’s refuses them (mutant R2). No retained certificate has one.

**What stays unchecked.** CPython’s integers are common to every route, and `Fraction`
to all but route Z. The custody of the bytes rests on the packet’s admission, on the Git
blobs matched here against the source’s history, and on the pin.
The source’s own runs are the source’s: its statement that both certificates passed its
two named checkers with strictly positive clearance is consistent with what was measured
here and was not reproduced (RF-2).

## The Controls

Each count’s two receipt controls are gross: a duplicated square (gap $-1$) and square 0
moved outside.
The margins these certificates keep are $5 \times 10^{-21}$ and $10^{-20}$
at 105, and $5 \times 10^{-13}$ and $10^{-12}$ at 204. A route that rounded at binary64,
or tolerated $10^{-12}$, would pass the packet as retained (RF-7). This review built
eight mutants of each certificate (`sharp_controls_t229.py`, receipts
`out-controls-T-229-n105.json` and `out-controls-T-229-n204.json`). Each was built from
the packet’s derived fact written back in the certificate format, with the round trip
checked exactly, so the run needs no upstream byte.
An earlier run from the source’s own files gave the same verdicts.
It decided each by both of its own routes and by both maintained routes, reached through
the packet’s own `evand-cert` adapter as `run_case` calls them:

| Mutant | Expected | Both maintained routes, at both counts | This review’s checker |
| --- | --- | --- | --- |
| F0: side lowered by the least top-or-right clearance ($5.00000000035595 \times 10^{-21}$ at 105, $4.9998207 \times 10^{-13}$ at 204) | accepted, a corner on the far wall | accepted, wall clearance exactly 0 | accepted, 0 on both routes |
| F1: and by $10^{-30}$ more | refused on a wall | refused at exactly $-10^{-30}$ (`square 0 violates y<=s` at 105, `square 0 violates x<=s` at 204) | refused at $-10^{-30}$ on both routes |
| N0: every square moved toward the left wall by the least left-or-bottom clearance ($5 \times 10^{-21}$, $5.0005024 \times 10^{-13}$) | accepted, contact on the left wall | accepted, clearance exactly 0 | accepted, 0 |
| N1: by the clearance $+ 10^{-30}$ | refused on a wall | refused at exactly $-10^{-30}$ (`square 3 violates x>=0` at 105, `square 48 violates x>=0` at 204) | refused at $-10^{-30}$ |
| P0: the second square of the least-gap pair (86 at 105, 17 at 204) moved along the first’s edge normal toward it by exactly the gap | accepted, an exact contact | accepted, least gap exactly 0 | accepted, gap 0, one touching pair on both routes |
| P1: by the gap $+ 10^{-30}$ | refused on an overlap | refused at exactly $-10^{-30}$ (`squares 70 and 85 overlap`, `squares 10 and 16 overlap`, numbered from 0) | refused, gap $-10^{-30}$, one positive clipping area |
| R1: the last row dropped | refused by every reader | `104 square rows for n = 105`, `203 square rows for n = 204` | refused by the reader |
| R2: square 1’s $x$ written as its exact decimal | a reader difference, not a control | read exactly, then accepted as the certificate | refused by the reader |

In P1 the move closes only the named pair, so exactly one pair overlaps, by exactly
$10^{-30}$. The kernel’s own `run_sharp` (`side-lowered-past-wall-contact` and
`tightest-pair-closed-past-contact`, its own construction) was also run on both.
At contact both maintained routes accept with the margin exactly 0, and past it both
refuse at exactly $-10^{-30}$. None of these runs is in the packet’s receipt or its
tests (RF-7).

## Identity, Measured

Whether two certificates are the same packing is not decided here.
What is measured, under the box’s eight symmetries, is how far each packing lies from
its kin (`identity_t229.py`, `out-identity-105.json`, `out-identity-204.json`,
`out-identity-204-couzo-copy.json`). The measures are: whether nearest centres pair the
squares one to one; and, for the symmetry with the least total squared displacement
under an optimal assignment (this review’s own Hungarian algorithm), how many squares
move beyond each threshold, compared exactly.
Also how far squares turn modulo 90° (a reflection negates the angle), and how many are
tilted in one packing and axis-parallel in the other.
Each packing is read from its retained file: the two house witnesses on `main`, T-174’s
and T-183’s facts, T-186’s facts, Couzo’s three 204 certificates and T-225’s source
certificate.

| n | Packing | Against | One to one under | Within $10^{-6}$ | Beyond $10^{-3}$ | Beyond $10^{-2}$ | Beyond $10^{-1}$ | Largest move | Largest turn | Turned beyond 1° | Tilted only in the first / only in the second |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 105 | #719 | T-174 (the house) | the identity | 63 | 42 | 27 | 0 | 0.0490 | 2.411° | 4 | 0 / 1 |
| 105 | #719 | T-183 (#593’s 105) | the identity | 63 | 42 | 27 | 0 | 0.0490 | 2.411° | 4 | 0 / 1 |
| 105 | T-174 | T-183 (#593’s 105) | the identity | 105 | 0 | 0 | 0 | $1.5 \times 10^{-19}$ | 0 | 0 | 0 / 0 |
| 204 | #719 | T-225 (the house) | a half turn | 117 | 67 | 39 | 6 | 0.273 | 25.64° | 1 | 10 / 0 |
| 204 | #719 | T-223 (#678) | the identity | 113 | 60 | 29 | 7 | 0.237 | 25.64° | 1 | 2 / 1 |
| 204 | #719 | T-228 (#675) | the identity | 35 | 66 | 39 | 6 | 0.199 | 25.66° | 4 | 5 / 1 |
| 204 | #719 | T-226 (#670) | the identity | 34 | 60 | 21 | 2 | 0.199 | 25.65° | 3 | 1 / 3 |
| 204 | #719 | T-186 | no symmetry | 35 | 98 | 45 | 14 | 0.716 | 25.90° | 5 | 17 / 0 |
| 204 | #719 | T-183 (#593’s 204) | no symmetry | 35 | 98 | 45 | 14 | 0.716 | 25.91° | 5 | 17 / 0 |
| 204 | T-225 | T-223 (#678) | a half turn | 132 | 58 | 27 | 4 | 0.442 | 0.159° | 0 | 0 / 9 |
| 204 | Couzo’s `5a299b4` copy | T-225 | the identity | 204 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 204 | #719’s other `n204.cert` | #719 | the identity | 204 | 0 | 0 | 0 | $2.0 \times 10^{-11}$ | 0 | 0 | 0 / 0 |

Every figure the entry and the packet record is reproduced.
That is 42, 0.049 and 2.411° at 105, and 67, 0.273 and 25.64° at 204, in the entry’s
regularization items.
The packet’s 6 beyond a tenth against T-225 and its 60, 29, 7 and 0.237 against T-223
are reproduced too, as are 14 beyond a tenth against T-183 and T-186, and T-225’s 4
beyond a tenth of T-223. The packet’s `measure/identity.json`, read after this table was
made, agrees at every figure both state.
The triage’s 66, 39, 6 and 60, 21, 2 against T-228 and T-226 are reproduced as well.

**At 105**, #719 is T-174’s arrangement re-solved: one to one under the identity, no
square beyond a tenth, 63 squares within $10^{-6}$. The most-turned square, 55 (2.41°),
is loose in both packings, with no neighbour within $10^{-9}$ in either: its nearest is
square 54, at $2.07 \times 10^{-4}$ in #719 and $3.29 \times 10^{-3}$ in T-174. One
square tilted in T-174 is axis-parallel in #719. Polkovskyi’s own #593 file at 105
(T-183) is the same packing as T-174 to $1.5 \times 10^{-19}$, at T-130’s exact side, so
#719 measures the same against both.

**At 204**, #719 pairs one to one with every packing of Couzo’s 204 line (#670, #675 and
#678, under the identity) and with T-225 (under a half turn).
It does not pair with Polkovskyi’s own 13 and 14 October packings (T-183, T-186), as the
entry says. Two things the record does not say were measured:

- **The re-oriented square is released, not merely turned (RF-3).** Square 38 (row 38 of
  #719’s certificate, id 38 of the house witness) is held in T-225 within
  $1.2 \times 10^{-20}$ by four neighbours: 151, 142, 16 and 29. It is held within
  $1.2 \times 10^{-10}$ by the same four in T-223 and T-226, and within
  $4.1 \times 10^{-12}$ by three of them in T-228. It sits at 89.40° modulo 90°, that is
  $-0.60°$. In #719 it is at 63.76°, turned by 25.64°. It touches nothing there: its
  nearest neighbours are 29 at $1.253 \times 10^{-2}$, 4 at $1.653 \times 10^{-2}$, 16
  at $2.117 \times 10^{-2}$ and 151 at $2.205 \times 10^{-2}$, with every wall 4.45
  away. So #719 turns a load-bearing square of the house arrangement into a free one.
  Square 38 itself moves 0.199. The other five squares beyond a tenth (18, 25, 62, 69
  and 167, up to 0.273) lie 2.2 to 11.5 away from it, so the larger moves are spread
  through the packing; its neighbours opened its cavity by moves under a tenth.
- **The certificate keeps Couzo’s frame and tilts, not T-225’s (RF-4).** #719 pairs with
  T-223 under the identity, with two squares tilted only in #719 and one only in T-223.
  It pairs with T-225 only under a half turn, with ten squares tilted that T-225’s
  regularization made axis-parallel.
  T-225 is #678’s packing half-turned with nine squares straightened, and Couzo’s
  `5a299b4` copy of T-225’s side is T-225’s file exactly.
  So the geometry is as close to T-223, the packing T-225 regularizes, as to the house
  the item names.

## Newness in Report Order

Sides are each certificate’s header and, for the reports compared, their retained exact
files: a certificate’s header, a fact’s `side`, or Ostashev’s `sqcert` `s` line.
Where only a print exists, the margin is taken from the print less one unit in its last
place (`margins_t229.py`, `out-margins.json`). Report times are the ledgers’, the
issues’ and the case records’.
#719’s certificates were first committed at 2026-10-22T05:29:48Z (`1851c2c`), and the
issue opened at 05:30:47Z. #718, which adopted T-225 at 204, merged at 04:28:54Z, so
T-225 was already the house at 204 when #719 was reported.

**At 105**, every earlier report, from the Kingbird catalogue on:

| Reported | Report | Side’s source | #719 below it by |
| --- | --- | --- | --- |
| catalogue | Kingbird catalogue, 10.80789399144854 | print | $1.86 \times 10^{-2}$ or more |
| 2026-09-24 to 2026-10-07 | Casson; Couzo (3bfc47e, 27 September); T-117 (Rehwaldt and Couzo) | prints | $1.68 \times 10^{-2}$ or more |
| 2026-10-08 and later | T-125 (Ryan Xu); T-128; T-138 at 10.789303783751 | prints | $1.37 \times 10^{-3}$, $1.31 \times 10^{-3}$, $7.0 \times 10^{-12}$ or more |
| 2026-10-08 | T-130, Couzo’s refinement of Xu’s packing | fact | $5.1834385502 \times 10^{-12}$ |
| 2026-10-12 | T-170, PingYou Ltd #568 | fact | $5.1834384423 \times 10^{-12}$ |
| 2026-10-13 | T-174, PingYou Ltd PR #574, **the house when #719 was reported** | fact, equal to `n-105.md`’s exact form | $5.1834384423 \times 10^{-12}$ |
| 2026-10-14T01:40Z | T-183, Polkovskyi #593 (T-130’s side) | fact | $5.1834385502 \times 10^{-12}$ |
| 2026-10-15, 2026-10-21 | Couzo `4e4c8ce` and `5a299b4` copies (T-174’s and T-130’s sides) | certificates, as data | the same two margins |

**At 204:**

| Reported | Report | Side’s source | #719 below it by |
| --- | --- | --- | --- |
| catalogue | Kingbird catalogue, 14.82287565553229 | print | $1.42 \times 10^{-2}$ or more |
| 2026-10-12 to 2026-10-15 | T-162 (Ostashev #562), PingYou Ltd PR #574, T-183 (#593), T-186 (`70a033f`), Couzo `4e4c8ce` (both files) | `sqcert`, facts, certificates | $2.0403859060 \times 10^{-5}$ to $2.0403875655 \times 10^{-5}$ |
| 2026-10-16T03:37Z | Evan Daniel #639, 14.808663234387 | the ledger’s print | $2.04 \times 10^{-5}$ or more |
| 2026-10-17T18:05Z | T-226, Couzo #670 | certificate | $1.5871620272 \times 10^{-6}$ |
| 2026-10-18T06:02Z | T-228, Couzo #675 | certificate | $1.5366988930 \times 10^{-6}$ |
| 2026-10-18T23:23Z | T-223, Couzo #678 | certificate | $1.1453350568 \times 10^{-8}$ |
| 2026-10-20T02:36Z | T-225, Evan Daniel `0075967`, **the house when #719 was reported** | certificate, equal to `n-204.md`’s exact form | exactly `10063597267311130871459/10^30` $\approx 1.0063597267 \times 10^{-8}$ |
| 2026-10-21T22:56Z (pushed) | Couzo `5a299b4` copy of T-225 | certificate, as data | the same |

Every exact difference here equals the one the packet’s `claims.json` records where it
records one. No earlier side equals #719’s, so `first_certified_in` does not apply, as
the entry says. The source’s own second files differ from the claimed ones.
`n105.cert` is $4.64 \times 10^{-12}$ above `n-105.cert`. `n204.cert` is
$1.48 \times 10^{-11}$ below `n-204.cert` and is the same packing (largest move
$2.0 \times 10^{-11}$). Neither is claimed.

**Later counts.** Deleting $m - n$ squares from a packing of $m$ leaves a packing of $n$
in the same box, so a side is new only if it is below every bound at every later count.
Each side is below the reported and the verified upper bound at every count $m$ with
$n < m \le 324$ on `main`: 438 bounds after 105 and 240 after 204, decided exactly where
the case record states a rational exact form and from the print less one unit in its
last place otherwise.
The least margin is at $n + 1$ both times: $3.36 \times 10^{-2}$ at 106 and
$1.58 \times 10^{-2}$ at 205.

**Status now.** At 105 and 204 the house best packings on `main` are T-174’s and
T-225’s. #719 is below both, so once the entry reaches V3/C3 the house rule adopts it at
both counts. This review adopts nothing.

## Significance

The rubric is `epistemics.md`’s (S1 “bookkeeping or a routine consequence”, S2 “a
citable detail that changes no theorem”, S3 “a substantive case result”). The score is
of the claim, and a later result that supersedes it does not lower it.
The record’s line, read from its entries:

- **Padding** is S1: T-170 at $1.08 \times 10^{-19}$, and T-174 and T-186 at $10^{-99}$
  to $10^{-19}$.

- **Refinements that are not padding**, and further arrangements below about
  $1.4 \times 10^{-5}$, are S2. These are T-190 at $2.40 \times 10^{-11}$ (“not
  padding”), T-165 at $2.54 \times 10^{-10}$, T-225 at $1.76 \times 10^{-11}$ to
  $1.39 \times 10^{-9}$, T-228 at $5.05 \times 10^{-8}$, T-185 at $1.70 \times 10^{-6}$,
  and T-188 at $9.29 \times 10^{-6}$ with five squares beyond a tenth.

- **New arrangements and refinements to new optima** from about $2 \times 10^{-5}$ up
  are S3: T-223, T-224, T-219, T-172 and T-152.

- **105: S2, not S1 (RF-5).** The draft calls it “a padding-scale re-solve of the
  packing T-174 refines, S1 as T-174’s and T-186’s are”.
  But $5.18 \times 10^{-12}$ is seven orders above their padding.
  42 squares move beyond $10^{-3}$ and 27 beyond $10^{-2}$, and the case’s 12-place
  print changes (10.789303783749 to 10.789303783743). It is a refinement to a new
  smallest side that is not padding, as T-190’s $2.40 \times 10^{-11}$ is, and that is
  S2.

- **204: S2, confirmed.** It is $1.006 \times 10^{-8}$ below T-225, with six squares
  beyond a tenth and one square released (RF-3). That is the scale of T-228’s
  $5.05 \times 10^{-8}$ step and of T-225’s own $1.39 \times 10^{-9}$ re-solve, well
  below T-188’s $9.29 \times 10^{-6}$ and the S3 line.

- **The entry: S2, confirmed**, by this review, with the 105 sentence changed.
  Neither count moves a theorem, and neither is a new arrangement.

## The Source’s and the Record’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(n) \le S_n$ at the two header sides | the certificates; the entry’s claim | **computationally verified here**: three exact programs, four exact routes, every pair decided, from the certificate and from the fact |
| “a valid non-overlapping packing … in an open square container” | issue, line 8 | **verified here**: no square touches a wall and no pair touches, so the open and the closed box both hold it |
| each side is the claim’s fraction; the record’s prints are its ceilings at 12 and 16 places | claim; `claims.json`; ledger | **computationally verified here** |
| “Certified Side S (16 dec)” | issue table | the binary64 value at 16 places, **below the exact side at both counts**; not an upper bound as printed, and not used by the record |
| “strictly improve upon the standing records … and all merged/open issues and pull requests” | issue, line 8 | **verified here at 105 and 204** against this record, in report order |
| 122/122 pass Evan Daniel’s `verify_cert.py` “(100% strictly positive clearance)” | issue, line 272; the README names `verify_cert.py` and `verify_cert2.py` | **asserted**; not in the pinned tree, not run or read here; consistent with the strictly positive clearances measured |
| 122/122 pass `sqpack/verify.py` “(100% exit code 0, zero mutual overlap)”, “Joshua Levy’s independent implementation” | issue, lines 273, 278 and 281 | **asserted, and the stated command decides nothing**: this repository’s file has no entry point at any revision and exits 0 without reading its argument (RF-2). It is the maintained `exact_verify` route’s decider, so it is not independent of that route (RF-1) |
| baseline holder “Catalogue Witness” at both counts | issue table | **measured consistent**: #719 re-solves the house packings |
| “no source program ran here” | claim (`results.yaml:31408–31409`), notes (31495), atom (41665–41666), README (38, 178, 219) | **literally true of the source’s scripts; misleading for the relation**: the replay’s `exact_verify` route is the source’s named second checker (RF-1) |
| the replay’s 156,996 pair decisions and its margins | notes; atom; README | **reproduced here** (`check --replay`) and **computationally verified here** on a third program; README’s “at 204 by $5.0 \times 10^{-13}$” is rounded up (RF-6) |
| the identity figures, “one square re-oriented by 25.64°” | notes (31474–31486); regularization items; README (97–106) | **reproduced here**; the square is released from four contacts, not only turned (RF-3) |
| “at 204 Francisco Couzo’s packing (#678, T-223) as Evan Daniel regularized it (T-225)” | claim, 31414–31416 | **measured consistent**, with two refinements: the arrangement was first reported in #670 (T-226), and the certificate keeps #678’s frame and tilts (RF-4) |

No row claims optimality, rigidity, a local minimum or priority, and none is decided.

## Findings

**RF-1, major, non-blocking: the issue names `sqpack/verify.py` as its second checker,
so the replay’s `exact_verify` route is not independent of the producer’s checking.**
The issue’s “Checks” section names `tools/jlevy_squares/packing/src/sqpack/verify.py`
(“Joshua Levy reference SQPACK verifier”, “Joshua Levy’s independent implementation”)
beside Evan Daniel’s `verify_cert.py` (issue body, lines 272–281; packet README lines
36–38). The maintained `exact_verify` route decides through it: `run_case` calls
`legacy.exact_verify`, which is `sqpack.witness.exact_verify`, which calls
`sqpack.verify.verify_packing`. The record does not say so.
The claim says “Those statements are the author’s; no source program ran here”
(`results.yaml:31408–31409`). The notes and atom say “The source’s own checkers were not
run here” (`results.yaml:31495`; `evidence.yaml:41665–41666`), and the README says “no
source program ran here” (lines 38, 178). That is literally true of the source’s
scripts. But the confirming replay entry that the exit writes must not record the
maintained routes as `independent-implementation`. The #678 precedent records the same
circumstance as `shared-components`, naming “sqpack.verify’s unit-shape and
separating-axis predicates …, the jlevy/squares corner verifier the source reports
running” (`E-couzo-678-filtered-exact-feasibility`, `evidence.yaml:40959–40972` on
`main`). The 22 October review of T-226 to T-228 found the same for Couzo’s manifests
(its RF-1). The `independent` route and this review’s checker are named by no source.
The result can still be stated as *confirmed, independently re-implemented*, since this
review’s checker is a clean-room re-implementation that decided both certificates in
full. No bound depends on this.

**RF-2, minor, non-blocking: as the issue states it, the `sqpack/verify.py` check
decides nothing, and the record repeats it without saying so.** The issue’s command is
`python3 tools/jlevy_squares/packing/src/sqpack/verify.py scratch/square-packing-records/certificates/n*.cert`
(line 278), reported as “122 / 122 passed (100% exit code 0, zero mutual overlap)”.
`packing/src/sqpack/verify.py` imports only the standard library, and none of its eight
revisions in this repository’s history, from `ab0cae9f7` to `7c2ba22fd`, has a
`__main__` block or reads `sys.argv` (`sqpack-verify-history.log`). Run as stated, this
repository’s file exits 0 with no output.
It does so on the real 105 certificate, on a 105 certificate whose square 2 duplicates
square 1, which this review refuses at gap $-1$, and on a path that does not exist
(`sqpack-verify-as-script.log`). So the statement is no evidence of a second check,
unless the author’s copy, which is not in the pinned tree, differed.
RF-1 stands either way, because the source names the file.
The source’s README names `verify_cert.py` and `verify_cert2.py` instead (README line 11
at the pin), which the record does not mention.
Suggested, in the claim’s second paragraph: “… run from the author’s own copies, which
are not in the pinned tree.
Run as the issue states it, this repository’s sqpack/verify.py reads no file and exits 0
whatever it is given, so that statement is no evidence of a check.
The source’s README names verify_cert.py and verify_cert2.py.”
Ask Question 1.

**RF-3, minor, non-blocking: at 204 the “re-oriented” square is released from four
contacts.** The notes say “every square turns less than 1 degree but one, re-oriented by
25.64 degrees” (`results.yaml:31479–31480`; README lines 100–102). Measured (Identity,
Measured): square 38 is held within $1.2 \times 10^{-20}$ by four neighbours in T-225,
and within $1.2 \times 10^{-10}$ in T-223 and T-226. In #719 it touches nothing within
$1.25 \times 10^{-2}$, after moving 0.199 itself.
The contact graph changed: a load-bearing square became a free one.
The regularization item’s schema reads a regularization as “rearranged for display
without changing what the packing is meant to be”.
The triage left the choice between that item and a ledger `new_packing` that
`continues: T-225` to the coordinator.
This review supports keeping the item.
The pairing is one to one, 117 squares lie within $10^{-6}$, the other 203 squares turn
less than 1°, and T-225’s own regularization of T-223 moved squares further (0.442). But
the record should say what changed.
Suggested, for the notes: “… and every square turns less than 1 degree but one, square
38, which T-223 and T-225 hold within 1.2e-10 and 1.2e-20 by four neighbours and which
#719 releases and turns by 25.64 degrees: in #719 nothing lies within 1.25e-2 of it.”
The README’s sentence should change to match.

**RF-4, note: at 204 the certificate keeps Couzo’s frame and tilts, and the arrangement
was first reported in #670.** The 204 item names `of: T-225` (`results.yaml:31533`), the
house, which is a half turn of #719 with ten squares axis-parallel that #719 tilts.
#719 pairs with Couzo’s #670, #675 and #678 under the identity, and with T-223 within
three tilts. Either `of` is defensible, since the record holds T-225 as T-223’s packing
regularized. Keeping `of: T-225` with a notes sentence (“the certificate keeps the frame
and tilt pattern of Couzo’s #678 certificate”) records the measurement.
The claim’s credit (`results.yaml:31414–31416`) names “Francisco Couzo’s packing (#678,
T-223)”. The arrangement was first reported in #670 (T-226), 29 hours before #678, and
#719 pairs one to one with all three.
The 22 October review of T-226 to T-228 asks the same of T-223’s rationale (its RF-4).
Suggested: “at 204 Francisco Couzo’s packing, first reported in #670 and refined in #675
and #678 (T-226, T-228, T-223), as Evan Daniel regularized it (T-225)”. Ask Question 2.

**RF-5, minor, non-blocking: the significance rationale scores 105 as padding.** The
rationale (`results.yaml:31426–31428`) says “a padding-scale re-solve … S1 as T-174’s
and T-186’s are”. See Significance: at $5.18 \times 10^{-12}$, with 42 squares beyond
$10^{-3}$, it is a refinement that is not padding, S2 by T-190’s precedent.
The entry’s score S2 is confirmed.
Its `by` should name this review.

**RF-6, note: lower bounds printed rounded up.** The README says “at 204 by
$5.0 \times 10^{-13}$” (lines 174–175), but every wall clears by at least
$4.9998207 \times 10^{-13}$, which is less.
The notes say “T-228 by 1.537e-6” (`results.yaml:31465`) and the README “T-228 by
$1.54 \times 10^{-6}$” (line 84); the exact margin is $1.5366989 \times 10^{-6}$. A
margin stated as “below by” or “at least” should be rounded down, as the ledgers’ “below
by at least” is: “4.99e-13”, “1.536e-6”, “1.53e-6”. The other printed margins are
truncations.

**RF-7, minor, non-blocking: the packet’s controls are gross, and no test runs sharp
ones.** The receipt’s controls are a duplicated square and a square moved outside.
The certificates keep margins of $5 \times 10^{-21}$ (105) and $5 \times 10^{-13}$
(204), and at 105 they are below binary64 resolution of the coordinates.
This review ran sharp controls through all four deciders and they pass (The Controls).
Neither the receipt nor `tests/test_upper_bound_reports.py` runs them, as the T-225
tests do with `run_sharp`. Add a slow-marked test running the kernel’s two sharp
controls on the 105 certificate, whose $5 \times 10^{-21}$ margins are the finest here
(each positive takes 1 to 3 CPU seconds a route).
Or cite this review’s controls receipts in the replay entry’s `limitations`.

**RF-8, note, for the record: retain and register this review’s programs.** They are in
this lane’s scratch directory and decide nothing until they sit in a packet with their
README. The proposal is
[`mishapolk-issue719-2026-10-22/review/review-2026-10-22/`](../../../packing/resources/web/mishapolk-issue719-2026-10-22/review/review-2026-10-22/README.md).
`review_t229_check.py` (decides) and `sharp_controls_t229.py` (premise check) belong in
`verifiers.yaml` with their independence records, as Stage 4 and `epistemics.md`
require.

**RF-9, note: the identity measurements read the houses’ source files, which equal the
house witnesses.** The 105 regularization item measures against T-174, and its
`measured_in` is the packet’s `measure/identity.json`, which read PR #574’s facts.
The house witness `W-known-best-n105` is the same geometry exactly (largest move 0), and
T-225’s source certificate equals `W-known-best-n204` exactly.
No figure depends on which was read.
This is recorded so that the adoption lane need not measure again.

## Questions for the Author

1. Your issue reports `sqpack/verify.py` as passing 122 of 122 with exit code 0, run as
   `python3 tools/jlevy_squares/packing/src/sqpack/verify.py …/n*.cert`. This
   repository’s file has no command-line entry point at any revision.
   Run that way, it reads no file and exits 0 even for a certificate with two identical
   squares. How did you call it: which function, with which conversion from your `.cert`
   rows to its input? Which revisions of Evan Daniel’s `verify_cert.py` and
   `verify_cert2.py`, which your README names, did you run?
2. At 204, square 38 of your certificate is turned by 25.64° and touches nothing: its
   nearest neighbour is $1.25 \times 10^{-2}$ away.
   In Couzo’s and Daniel’s packings the same square is held by four neighbours within
   $10^{-10}$ to $10^{-20}$. Did your solver release it deliberately?
   Which file did the 204 solve start from: this repository’s house witness (T-225), or
   Couzo’s #678 certificate, whose frame and tilts yours keeps?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, at both counts, once the replay
evidence and this review are entered.
That needs a retained certificate, a replay command (`check --replay`) and a passing
replay reproduced here.
It also needs retained controls refused by every route that accepted the positive, and
sharp controls refused here.
The maintained replay is recorded as `shared-components` (RF-1). This review’s checker
is a clean-room re-implementation: its author never read the source’s named checkers or
the maintained routes’ deciding code, and the checker was frozen (SHA-256 `b470c70b…`)
before its author read any maintained or source code at all.
It is by a Claude agent.
Agents of the Claude family also wrote this repository’s `sqpack.verify`, whose first
three revisions are Claude-authored commits, and the issue names that file as a checker.
The issue discloses Gemini assistance with the author’s scripting, a different family.
This review is the accepted adversarial review that `select_houses.accepted_review`
reads once mapped, with `covers: [T-229]`. With the replay entry it brings the entry to
the rungs the house rule needs, and the house moves to #719 at both counts in the
adopting pull request.
It does not reach `V4`/`C4`, which need a second accepted adversarial review by a
distinct reviewer and a retained human oversight record.
The count of distinct machine methods is unchanged: every route is `exact-algebraic`,
and the clipping area is a second pair procedure within it.
No lower bound, optimum, local minimum, rigidity or priority follows.

## Proposed Record Changes

For the records lane; this review writes none of them.
The line references are to the records branch at `56d6d0d6d`, and the companion
`proposed-record-changes.md` lists them change by change.

- **`evidence.yaml`.**
  - A confirming entry for the packet’s replay: `assurance: verified`,
    `method: exact-algebraic`, `origin: replayed-here`,
    `relationship_to_generator: shared-components`. `shared_components` names
    `sqpack.verify`’s predicates as the checker the issue names, the `evand-cert` and
    fact readers, the half-angle map and `Fraction`, as
    `E-couzo-678-filtered-exact-feasibility` does.
    Its `verifiers` are the maintained programs, its command `check --replay` and
    `replay_status: passed`. It carries an independence record with `coverage: full`,
    `limitations` naming RF-7 and this review’s controls receipts, and this document as
    `external_review`.
  - One entry for this review’s checker and controls: `independent-implementation`,
    `coverage: full` over both certificates and every pair, `clean_room: true` and
    `shares: []`. Its `read` is `[mathematics, certificate-format, producer-output,
    earlier-review]`: the certificates’ format line, the packet README and receipts, and
    the T-226 to T-228 review’s description of its checker; no producer code.
    `written_by` is this lane, with `overlaps_producer: system-family`,
    `separate_prompt: true`, `separate_code: true`, and the note that the issue names
    this repository’s `sqpack.verify`.
  - Correct the report atom’s “The source’s own checkers were not run here”
    (`41665–41666`, RF-1).
- **`verifiers.yaml`.** Register `review_t229_check.py` (decides) and
  `sharp_controls_t229.py` (premise check) with their digests
  (`outputs/program-digests.sha256`), retained paths and the record above.
- **`results.yaml`, T-229.**
  - Add a `reviews` entry for this document: `kind: adversarial`, `reviewer_kind: ai`,
    `relation: project`, `verdict: accepted`, `covers: [T-229]`.
  - Rewrite the claim, `notes` and `next_rung` together: say *confirmed, independently
    re-implemented*, state the source’s named checker (RF-1) and the vacuous command
    (RF-2), and remove the C3 item from `unfinished_confirmations` once the replay entry
    is cited.
  - Significance S2, `by` this review, with the 105 sentence of RF-5.
  - The credit at 204 (RF-4), the released square (RF-3), and the rounded-down margins
    (RF-6).
- **The packet.** Add `review/review-2026-10-22/` with this review’s programs, outputs
  and README (RF-8), and a pointer from the packet README once this document is mapped.
  Correct lines 36–38 and 177–178 (RF-1, RF-2), 100–102 (RF-3), and 84 and 174–175
  (RF-6).
- **Tests.** RF-7.
- **Adoption.** Once T-229 is at V3/C3 with this review mapped, the house rule adopts
  #719 at 105 (from T-174) and 204 (from T-225). The regularization layer then decides
  both, as the entry’s `next_rung` says.

## Comparison with the Earlier Reviews

No earlier mathematical review of T-229 exists.
The triage of 22 October (`c-triage-719`) and the packet’s own identity measurement are
the only earlier readings of these certificates, and this review read both before
writing this section.
The packet’s measurement was read only after this review’s identity measurement had run.
Every margin, near-pair count, least clearance and gap, and identity figure they state
that this review also measured is reproduced here.
Two things differ:

- **Significance at 105.** The triage drafted S1 at 105 “by the precedent of T-174 and
  T-186”, which the entry kept.
  This review compared it with T-190 and T-165 instead, which are refinements that are
  not padding (RF-5). The entry’s S2 is unchanged.
- **The 204 judgment.** The triage flagged the re-oriented square as a judgment between
  a regularization item and a new packing that continues T-225, and recommended the
  item. This review agrees with the recommendation.
  It adds that the square is released from four contacts rather than turned in place
  (RF-3), and that the certificate keeps #678’s frame (RF-4).

What this review found that the triage and the import did not: RF-1, RF-2, RF-3, RF-4,
RF-6 and RF-7. It also decided both certificates on a third program, from the source’s
files as well as the derived facts, and ran sharp controls through every decider.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no human
oversight. No run of the source’s checkers or searches, and no decision of whether any
two certificates are the same packing.
No house best packing adoption, case-record change or regularization run.
No review of the 120 counts beyond the corpus that the issue also claims, of the
source’s other files, or of the credit name, which the import’s reply already asks the
author about.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
