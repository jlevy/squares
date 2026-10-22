# Review: Evan Daniel’s Regularized Views at 204, 227, 229 and 260 (T-225, evand/square-packing@0075967)

**Date:** 21 October 2026. **Verdict: accepted with findings at each of the four counts,
for finite feasibility only.** The four rational certificates that Evan Daniel committed
in `evand/square-packing@0075967` prove the upper bounds that pull request #716
registers as T-225. Each certificate is $n$ unit squares with pairwise disjoint
interiors inside the closed box of its header side, and that side is the one the entry’s
claim states, as a fraction and as a 30-place decimal.
They also hold in the strict sense: every wall is cleared by at least $5 \times
10^{-21}$ and every pair by just under $10^{-20}$, so the squares are disjoint as closed
sets inside the open box.
The packet’s replay reproduces here, and so does its frozen comparison.
A checker written for this review agrees with the packet’s two routes at every number
they share. It was written from the certificates’ format line and the mathematics and
shares no code with those routes or with the source.
Sharp controls at $10^{-30}$, which the packet lacks, are refused by all three, and
exact contact is accepted by all three.
Each side is exactly below the house best packing on `main` at its count, and below
every verified and reported upper bound at every later count through 324, so each bound
is new. Six findings are recorded, none blocking; one, the credit of the 227 view, is
major. The draft significance S2 is confirmed.

This is the Stage 4 mathematical review lane of the 21 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
`think-ql4v`, pull request #716 at `be6416a03`. It was written by an AI reviewer of the
Claude system family (Anthropic), strong sub-agent tier, at reasoning setting xhigh, as
lane `c-review-t225-math`. The lane was prompted separately from the import lane that
built the packet and the replay, and from the pull request’s senior reviewer.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row, adopts no house best packing and edits no bead.
The proposed record changes are listed at the end.
The register entry that #716 adds is T-225, which this review calls “the entry”.
Its programs and receipts are retained with the packet in
[`review/review-2026-10-21/`](../../../packing/resources/web/evand-regularized-2026-10-20/review/review-2026-10-21/README.md)
(RF-6).

**For the author.** All four of your bounds hold exactly at the sides your certificates
state. Three exact decision programs that are not your code decided them: the two
maintained routes of this repository’s replay, and a third written for this review that
decides each certificate twice, once in integers alone.
Your own checkers were not run here.
The findings are about this repository’s record, not about your certificates.
Three questions under Questions are about how the views turn squares relative to the
certificates they are credited to.
At 204 and 229, near-axis squares are made exactly axis-aligned, and at 227 one square
turns by 2.54°, while each JSON lists only kept free angles.

## Claims Covered

The entry’s claim, at the four counts of the record’s horizon (1 to 324): $s(n) \le
S_n$, with $S_n$ the header side of `search/regularize/lists/certs/n-NNN.cert.gz` at
`0075967`, equal to the `S_cert` its JSON prints.

| n | Exact side $S_n$ | Rounded up at 16 | Packing per the source (`by`) | House best packing on `main` (`bb0c24e9f`) and margin | Verified bound at n + 1 and margin |
| ---: | --- | --- | --- | --- | --- |
| 204 | `14808642840591493923068442871459/10^30` | 14.8086428405914940 | Francisco Couzo (#678, T-223) | T-223, `141654921219558922887849/9565692327860000000000`; below by `664697624178869147740396776772613/478284616393000000000000000000000000000000` ≈ $1.389753 \times 10^{-9}$ | 205: `3706112786531022055915931516421/(2.5·10^29)`; below by `632332221303772023811327769/(4·10^28)` ≈ $1.580831 \times 10^{-2}$ |
| 227 | `7781812826162574542396221861851/(5·10^29)` | 15.5636256523251491 | Francisco Couzo (#672, unregistered) | T-196 (de Winter), the fraction of `n-227.md` with a 153-digit numerator; below by ≈ $1.710513 \times 10^{-4}$; below #672’s exact side `71427829379429597600111901507/4589408083628500000000000000` by `80671923699051704327371636387293/4589408083628500000000000000000000000000000` ≈ $1.757785 \times 10^{-11}$ | 228: PingYou Ltd’s fraction with a 473-digit numerator; below by ≈ $4.097582 \times 10^{-2}$ |
| 229 | `15650161513876431064009548865321/10^30` | 15.6501615138764311 | Evan Daniel (#674 update, T-199) | T-199, `7825080756947776580756939951343/(5·10^29)`; below by `3824419500866207473/(2·10^29)` ≈ $1.912210 \times 10^{-11}$ | 230: `7841463414634146341541829268293/(5·10^29)`; below by `6553063078372323814821934253/(2·10^29)` ≈ $3.276532 \times 10^{-2}$ |
| 260 | `4161438312629953048686574163329/(2.5·10^29)` | 16.6457532505198122 | Francisco Couzo (#678, T-223) | T-223, `146417594016514621500994169/8796093022208000000000000`; below by `843684791288921397849844113/33554432000000000000000000000000000000` ≈ $2.514377 \times 10^{-11}$ | 261: PingYou Ltd’s fraction with a 122-digit numerator; below by ≈ $3.302662 \times 10^{-2}$ |

Every side and margin was recomputed here from the certificate headers and from `main`’s
case records, read by `git show` at `bb0c24e9f` (`margins_t225.py`, `out-margins.json`).
Each side was compared with the verified and the reported upper bound at every count $m$
with $n < m \le 324$: 240, 194, 190 and 128 bounds.
The reported closed forms $a + b\sqrt{k}$ were decided exactly, and four null forms were
taken by their prints.
Each side is below all of them, and the least margin is at $n + 1$. Deleting $m - n$
squares from a packing of $m$ leaves a packing of $n$ in the same box, so no later count
gives a smaller bound at $n$ than these sides.
Each side equals the claim’s fraction, its 30-place decimal and the JSON’s `S_cert`. It
is also the JSON’s 60-digit `S_exact` times $1 + 10^{-20}$, rounded up at 30 places, and
lies above `S_exact` by $1.48$ to $1.66 \times 10^{-19}$. The packet’s README, the
entry’s notes and the ledger state the same margins.

**Read in full.** The packet README, the acquisition declaration and `claims.json`, and
the eight retained gzip files.
From the source, the method log `REGULARIZE.md` was read in its sections on the 10
October refresh, the angle policy, the path test and the levels (lines 140–236), and
`CREDITS.md` line 103 was read.
In the record: the entry’s register text at the PR head (`results.yaml:30752–30880`),
its evidence entry (`evidence.yaml:41183–41216`), its coverage row, the rendered lines
of `RESULTS.md` (498–501), the test module
`tests/test_upper_bound_reports_regularized_1020.py`, and the 21 October ledger README.
The import lane’s `measure/identity.py` was read in full, and so were Stage 4, the House
Rule and Label the PR of `result-import.md`, and `epistemics.md` on confirmation, the
independence record, significance and parallel credit.
Also read: the `regularizations` schema text, the regularization policy’s item 3, and
the two stage 4 reviews of 20 October (#668 and #678) as the form to follow.
Of the maintained routes, these were read after this review’s checker had run:
`upper_bound_reports` (`evand_cert`, `parse_certificate`, `check_certification`,
`decide_job`), `evand_arrangement_reports` (`job_input`, `sharp_input`, `run_sharp`,
`to_witness`, `run_case`, `replay_receipt`), `evand_exact_certificates.parse` and its
literal rule.
Also read then: the `result_credit`, `select_houses`, `render_announcement`
and `regularized_drawings` lines that read a regularization’s `of`. Not read: the
source’s checkers `verify_cert.py` and `verify_cert2.py`, its `refresh.py` and
`samepacking.py`, and the senior reviewer’s report of #716, until the findings were
written.

**Disclosure.** Before writing its checker, this reviewer read the two 20 October
reviews, which describe the maintained routes’ method and the design of their own
checkers (separating axes on unit normals, then clipping area).
It also read the packet README, which reports the receipt’s margins.
It read the import lane’s `identity.py` before writing its own identity program.
No earlier review of these four certificates was available to the lane.
The comparison with the pull request’s senior review is in its own section at the end.

## Replays Reproduced Here

Run on 21 October 2026 against the PR head `be6416a03`, with CPython 3.14.7, under
`nice -n 10` on a four-core host shared with other lanes, at most two processes.

| Command | What it decides | Outcome | Time |
| --- | --- | --- | --- |
| `python -m devtools.acquire_source evand-regularized-2026-10-20 --check` | the packet against its acquisition contract | `PACKET_MATCHES_ITS_CONTRACT` | 0.1 s |
| `python -m devtools.upper_bound_reports evand-regularized-2026-10-20 check-claims` | the frozen comparison rebuilt | equal to the retained `claims.json` | 0.7 s |
| `python -m devtools.upper_bound_reports evand-regularized-2026-10-20 check --replay` | all 12 jobs again on both maintained routes, serially, each held to its retained row | `4 certificates and 12 jobs admitted` | 62 s |
| `python -I review_t225_check.py` | this review’s checker, both of its routes, on all four certificates | 4 of 4 passed; strict at all four | 7.9 s and 9.1 s, two processes |
| `python -I agree_t225.py` | the checker’s numbers against the receipt’s two routes | every pose, side, least clearance, least gap and pair count equal | 1 s |
| `python sharp_controls_t225.py` | eight mutants per count through this review’s checker and both maintained routes, and the kernel’s `run_sharp` | every mutant decided as the contract requires | 194 s and 177 s, two processes |
| `python -I margins_t225.py` | the sides against `main` | as tabulated above | 1 s |
| `python -I identity_t225.py` | each view against the packing it is credited to | as tabulated below | 1 s |
| GitHub API, `contents` at `0075967`, its parent `bc0708f` and `88385ab` | custody of the eight retained gzip files | Git blobs equal to the packet’s at `0075967` and at `88385ab`; all eight differ at the parent | — |

The receipt (`receipts/exact-certification.json.xz`, format
`evand-regularized-1020-exact-replay-v1`) says what the README and the evidence entry
say. It holds 12 jobs, and each positive passes both routes with `pairs_tested` $=
n(n-1)/2$ (20,706, 25,651, 26,106 and 33,670). Every positive has a least wall clearance
of exactly $1/(2 \cdot 10^{20})$ and a least pair gap just under $10^{-20}$, and each
control is refused on both routes on the failure it was built for (an overlap of squares
0 and 1, square 0 outside the container).
`check --replay` decided all 12 jobs again and found every stable field equal.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors. A certificate is comment lines, a header `n S` and $n$ rows `x y t`, each a
rational literal: a rational side, a rational centre and $t = \tan(\theta/2)$. The bound
$s(n) \le S$ follows from five facts, each decided over $\mathbb{Q}$ or fixed by the
format:

1. **The rotation is on the unit circle.** For every rational $t = p/q$, the integers
   $a = q^2 - p^2$, $b = 2pq$ and $d = q^2 + p^2$ satisfy $a^2 + b^2 = d^2$. So
   $(c, s) = (a/d, b/d)$ is a unit vector, the four points $(x, y) + \tfrac12(\pm c \mp
   s, \pm s \pm c)$ are the corners of a unit square centred at $(x, y)$, and a
   certificate can state no other shape.
   This review’s integer route checks $a^2 + b^2 = d^2$ on every row, and its `Fraction`
   route checks unit edges and right angles on the corners it builds.
2. **There are exactly $n$ of them.** Both readers refuse a header that differs from the
   file’s count, and a row count other than $n$. Mutant R1 (one row dropped) is refused
   by both, and a duplicated square overlaps itself.
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box if and only
   if its corners do, equivalently if and only if its centre clears each wall by its
   half-extent $h = (|c| + |s|)/2$. The integer route decides the second form as four
   integer inequalities per square, the `Fraction` route the first.
   Every square clears every wall by at least exactly $1/(2 \cdot 10^{20})$; the far
   walls’ least clearances are $5.0000000004$ to $5.0000000009 \times 10^{-21}$.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors if
   and only if one of their edge normals weakly separates their projections.
   A square has two distinct normals, so four axes decide a pair; equivalently, the area
   of their intersection is zero.
   Both of this review’s routes decide every one of the $n(n-1)/2$ pairs by separating
   axes, with no distance filter, so no lemma about skipped pairs is needed.
   The `Fraction` route also decides every pair whose axis-aligned bounding boxes
   overlap with positive area (178, 149, 170 and 171) by the exact area that one
   square’s four closed half-planes clip from the other, which is exactly 0 at every
   one. A pair whose boxes do not overlap cannot overlap, since each square lies in its
   box. No pair touches: the least gaps are $9.999999999999989$, $9.99999999999999$,
   $9.999999999999992$ and $9.999999999999993 \times 10^{-21}$, between squares (60,
   82), (169, 180), (36, 129) and (178, 193), numbered from 0.
5. **The side is the claim’s.** The header equals the entry’s fraction and its 30-place
   decimal, the JSON’s `S_cert`, and `S_exact` scaled by $1 + 10^{-20}$ and rounded up
   at 30 places. The scaling about the origin corner is what the method log says it is
   (`REGULARIZE.md:175–176`): it opens every contact of the solved packing by about
   $10^{-20}$ and every wall contact by $5 \times 10^{-21}$, which is what the margins
   show.

No route here rounds, dilates or tolerates.
The integer route uses no `fractions` at all; it clears every denominator and compares
integers. Each pair’s exact gap is $(\max_k L_k - R)/(2 d_i d_j D_x D_y)$, with the four
axis tests sharing the positive factor, and the integer route’s least clearance and
least gap equal the `Fraction` route’s, compared by cross-multiplication, at all four
counts. The box convention does not matter here, since nothing touches.
The README’s “in an open square of the stated side” (README line 28) is true as
measured.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`exact_verify` on `to_witness`, `V-sqpack-verify`) | unit shape on corners, corners in the box, every pair by exact separating axes | the `evand-cert` adapter (`evand_exact_certificates.parse`), `Pose.basis`, `basis_witness`, `sqpack.verify` | with `independent`: the parser, the half-angle map, `Fraction` and the separating-axis method; with the source: none of its code (the source’s checkers are `verify_cert.py` and `verify_cert2.py`, pinned and not run) |
| `independent` (`check_squares` on `corner_squares`, `V-check-rational-witness-independent`) | the same three facts on corners built by a second formula | `square_failures`, `pair_gap`, `check_squares` | the same parser, half-angle map, `Fraction` and method |
| this review’s route I (`review_t225_check.py`, integers) | Pythagorean triple per row, half-extent containment, every pair by four integer axis inequalities | its own reader and CPython integers | its reader with route F; with the maintained routes, CPython integers and the separating-axis method; no `fractions`, no code |
| this review’s route F (`review_t225_check.py`, `Fraction`) | unit edges and right angles on corners, corner containment, every pair by corner projections, bounding-box-overlapping pairs again by exact clipping area | its own reader, corners and clipping | `Fraction` with the maintained routes; clipping area with no maintained route |

Two readers of the certificate text exist here, the shared `parse` of the maintained
routes and this review’s. They read the same sides and the same 920 poses: every
`checker_input` pose of the receipt equals, as rationals, the row this review’s reader
read (`agree_t225.py`). The two readers differ in one way that decides nothing here.
The maintained reader admits decimal literals (`evand_exact_certificates.py:158`,
`_RATIONAL`) and reads them exactly, and this review’s refuses them; no retained
certificate has one (mutant R2).

**What stays unchecked.** CPython’s integers are common to every route, and `Fraction`
to all but route I. The custody of the bytes rests on the packet’s admission, which
holds each file to its declared digest, on the Git blobs matched here against the pin,
and on the pin itself.
The source’s own runs are the source’s: its two checkers’ `VALID`, the 80-digit
verification and the path test.

## The Controls

The packet’s two kernel controls per count are gross: a duplicated square (gap $-1$) and
square 0 moved $S + 2$ outside.
Every margin these certificates keep is about $10^{-20}$, so a route rounding at
binary64 or tolerating $10^{-12}$ would pass the packet as retained (RF-3). This review
built eight mutants per count (`sharp_controls_t225.py`, receipts
`out-controls-nNNN.json`). It decided each by both of its own routes and by both
maintained routes, reached through the packet’s own `evand-cert` adapter:

| Mutant | Expected | Both maintained routes, at all four counts | This review’s checker |
| --- | --- | --- | --- |
| F0: side lowered by the least top-or-right clearance | accepted, a corner on the far wall | accepted, wall clearance exactly $0$ | accepted, $0$ on both routes |
| F1: and by $10^{-30}$ more | refused on a wall | refused, clearance exactly $-10^{-30}$ (`square 4 violates y<=s` at 204, square 0 at 227 and 260, square 8 at 229) | refused, $-10^{-30}$ |
| N0: every square moved toward the least-clearance near wall by that clearance | accepted, a corner on the near wall | accepted, clearance exactly $0$ | accepted, $0$ |
| N1: by the clearance $+ 10^{-30}$ (the near wall moved $10^{-30}$ inward) | refused on a wall | refused, exactly $-10^{-30}$ (`square 0 violates x>=0` at 204 and 260, square 56 at 227, square 13 at 229) | refused, $-10^{-30}$ |
| P0: the least-gap pair closed along its best separating axis by exactly its gap | accepted, an exact contact | accepted, least gap exactly $0$ | accepted, gap $0$, one contact |
| P1: closed by its gap $+ 10^{-30}$ | refused on an overlap | refused, least gap exactly $-10^{-30}$ (`squares 60 and 82 overlap`, `169 and 180`, `36 and 129`, `178 and 193`) | refused, gap $-10^{-30}$, clipping area positive |
| R1: one row dropped | refused by both readers | `203 square rows for n = 204` and the like | refused by the reader |
| R2: a coordinate written as a 25-place decimal | a reader difference, not a control | read exactly; then decided by its geometry (accepted at 204 and 260, where the decimal puts a square on the wall; refused at 227 and 229, where the binary64 conversion moved a square by about $10^{-16}$) | refused by the reader |

At 204, 229 and 260 the least-gap pair lies in an evenly spaced chain of equally tilted
squares, so either square’s move also closes a second pair at the same exact gap.
There P1 overlaps two pairs, each by at most $10^{-30}$, the named one by exactly that
(`diag_pair_t225.py`); at 227 the move isolates the pair.
The kernel’s own `run_sharp` (`side-lowered-past-wall-contact` and
`tightest-pair-closed-past-contact`, a construction of its own) was also run on all four
certificates. At contact both maintained routes accept with the margin exactly $0$, and
past it both refuse at exactly $-10^{-30}$. None of these runs is in the packet’s
receipt or its test (RF-3).

## Identity, Measured

The source credits each packing to its finder and says each view is the same packing at
level 2 (“traversable without expansion”), by a path test that samples angle moves.
Whether a view is the same packing is not decided here.
What is measured, under the box’s eight symmetries, is how far each view lies from the
certificate its credit names: by nearest centre, and by an optimal assignment of least
total squared displacement (`identity_t225.py`, its own Hungarian algorithm,
displacements compared with each bound exactly).
#672’s certificate was fetched for this at `franciscouzo/square-packing@af8cb79`:
`certificates/n227.cert`, Git blob `8172d92`, SHA-256
`65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17`, the bytes the import
lane named.

| n | View against | Nearest centres one to one under | Squares within $10^{-6}$ | Beyond $10^{-3}$ | Beyond $10^{-1}$ | Largest move | Largest turn | Turned beyond $10^{-3}$° |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 204 | T-223 (#678) | a half turn | 132 of 204 | 58 | 4 | 0.442 | 0.159° | 12 |
| 227 | #672 | a half turn | 194 of 227 | 16 | 3 | 0.168 | 2.54° | 4 |
| 227 | T-196 (#668) | the identity, the anti-transpose | 1 of 227 | 58 | 3 | 0.208 | 5.84° | 57 |
| 229 | T-199 (#674 update) | no symmetry | 95 of 229 | 112 | 13 | 0.650 | 0.055° | 31 |
| 260 | T-223 (#678) | no symmetry | 207 of 260 (all within $10^{-9}$) | 41 | 20 | 0.643 | $1.3 \times 10^{-7}$° | 0 |

#672’s own packing against T-196 has 1 of 227 squares within $10^{-6}$ and none beyond
$10^{-1}$ (largest 0.080), with 58 turned: #672 refines de Winter’s packing, and the 227
view is #672’s packing solved $1.76 \times 10^{-11}$ lower and regularized.
Rescaling the reference to the view’s side changes none of these counts against T-223,
#672 or T-199 (at 204 it brings 71 more squares within $10^{-9}$). Every displacement
count, largest move and largest turn above equals the packet’s `measure/identity.json`,
which was computed with SciPy and the record’s `arrangement_gap`. Its turned counts are
of turns whose sine exceeds $10^{-6}$, and this table’s are of turns above $10^{-3}$
degrees, so those differ by design.
So the lineage the source states is consistent with the geometry.
At 260 the view is T-223’s packing to $10^{-9}$ in 207 squares, with 53 slid and none
turned. At 204, 227 and 229 the views also turn squares relative to the credited
certificate:

- At 204, squares that T-223’s certificate tilts by 0.088°, 0.054° and 0.047° off the
  axis (view squares 120, 119 and 118) are exactly axis-aligned in the view, and others
  turn by up to 0.159°.
- At 229, the six most-turned squares go from 0.020°–0.055° to exactly axis-aligned.
- At 227, view square 71 is at 50.18° where #672’s certificate has 52.72°, and two
  near-axis squares are made axis-aligned.

Each JSON’s `angle_changes` lists only free angles kept.
The method log says the exact solve snaps near-axis tilts of Couzo’s float witnesses to
the axis (`REGULARIZE.md:140–143`), which would account for 204 if the refresh’s solve
made those turns. The record does not say which step made them (RF-2; Question 1). These
are lineage and credit facts, not bound facts.

## Significance

**S2, confirmed.** The claim is four finite upper bounds, each the solved exact side of
a packing already reported, $1.76 \times 10^{-11}$ to $1.39 \times 10^{-9}$ below that
packing’s certificate: a citable detail of each case that changes no theorem.

- The scale is T-146’s (S2), Daniel’s regularized views of 10 October at $2.21 \times
  10^{-17}$ to $7.82 \times 10^{-10}$ below the record.
- It is above the rounding-scale re-solves scored S1: T-186 at $10^{-94}$ to $1.8
  \times 10^{-19}$, and T-155 at $9.9 \times 10^{-15}$ at most.
- It is far below what scored S3. T-224 at 270 is a new arrangement $3.47 \times
  10^{-5}$ below with 15 squares beyond a tenth.
  T-223 is a new arrangement at 204 and 260, $2 \times 10^{-5}$ and more below.
- At 229 the side is a $1.9 \times 10^{-11}$ step on T-199, itself an S2 step of $1.32
  \times 10^{-5}$ in the same family.
- At 227 the $1.71 \times 10^{-4}$ drop below T-196 is #672’s, Couzo’s, not this
  entry’s; it is not inherited.

The regularization is display and adds nothing to the score of the claim.
Not S1: the margins are far above rounding, and each is a side the record did not hold.

## The Source’s and the Record’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(n) \le S_n$ at 204, 227, 229 and 260, at the header sides | the certificates; the entry’s claim | **computationally verified here**: three exact programs, four exact routes, every pair decided |
| each side is the JSON’s `S_cert` and `S_exact` scaled by $1 + 10^{-20}$, rounded up at 30 places | JSON; README; the test | **computationally verified here** |
| each certificate is VALID under the source’s two checkers and verified at 80 digits | JSON `cert_valid`, `verify_80` | **asserted**; the checkers are pinned and were not run |
| each side is the exact optimum of the store’s best packing at its count (at 229 after the slp2 polish) | commit message; method log | **asserted but unverified**: no optimality, local or global, is decided here |
| each view is the same packing at that side, level 2, by the path test | JSON `level`, `level_text` | **asserted but unverified**; the path test samples the path and is not a continuous proof (method log) |
| `angle_changes`: free angles kept, none turned or merged | JSON; README line 58 | **asserted** of the regularizer’s step; **contradicted as a statement about the view against the credited certificate** at 204, 227 and 229 (RF-2) |
| the packings are Couzo’s at 204, 227 and 260 and Daniel’s at 229 | JSON `by`; the commit | **asserted**; measured consistent (table above) |
| “not a new bound” | every JSON’s `note` | the author’s framing; each side is below every value on `main` and pending, decided here, which by the House Rule makes it a smaller packing |
| below every value the record holds or has pending, and below the verified bound at $n + 1$ | the entry’s claim and notes; `claims.json` | **computationally verified here** against `main` at `bb0c24e9f`, every later count through 324 included |
| the eight files are byte-identical at `88385ab`; `0075967` is the first commit to hold them | README | **verified here** by Git blob through the GitHub API, at the pin, its parent and `88385ab` |
| the two checkers are byte-identical to the n183 packet’s copies | README; declaration | **verified here** by SHA-256 (`3299ca0c…`, `55140a35…`) |
| the work was produced by Claude under human direction | `CREDITS.md` line 103 | read as stated |
| the identity measurement’s table | README; `measure/identity.json` | **reproduced here** on code that shares none of it |
| the replay: 12 jobs, 636,798 pair decisions, least clearance $5 \times 10^{-21}$, least gap just under $10^{-20}$ | README; evidence; notes | **reproduced here** (`check --replay`) and **computationally verified here** on a third program |

No row claims optimality, rigidity, novelty or priority, and none is decided.

## Findings

**RF-1, major, non-blocking: at 227 the item’s `of` names a packing the source does not
name, and the generated credit text follows it.** The 227 item says `of: T-196`,
`identity.basis: source-claim` (`results.yaml:30829–30841`). The schema defines `of` as
the result that holds the packing at $n$, through whose attribution “the packing’s
finder keeps its credit” (`results.schema.yaml:405–410`). T-196 holds de Winter’s #668
packing, but the source’s `by` names Couzo, and the view is #672’s packing.
194 of 227 squares lie within $10^{-6}$ of #672’s certificate and 1 of 227 within
$10^{-6}$ of T-196’s. The entry’s notes explain the choice: no entry registers #672 yet,
and think-2vjc imports it.
The generated text does not carry that explanation:

- `RESULTS.md:499` says “n = 227: a regularization of T-196’s packing by Daniel”.
- `render_announcement.py:890–902` names the finder of the packing from `of`’s own
  credit, which is de Winter.
- After adoption, `regularized_drawings.py:1144` would describe the house at 227 as “its
  source’s regularization of T-196’s packing”.

The item’s `moved: 58`, `max_move: 0.208` and `max_turn_deg: 5.84` measure #672’s
refinement and the regularization together, not the regularization.
Against #672 the figures are 16, 0.168 and 2.54. A `source-claim` basis on an `of` the
source never names reads as the source claiming identity with de Winter’s packing.
No bound depends on it.
Before the 227 adoption is published, register #672 (think-2vjc) and move `of` and the
identity figures to it.
If the adoption must go first, the case record’s and the drawing’s credit sentences at
227 should name Couzo’s #672 packing in hand-written prose until then.

**RF-2, minor, non-blocking: “no angle changed” sits beside measured turns.** Every item
records `changes: {merged_rotation_groups_deg: 0, straightened: 0, re_angled: 0}`
(`results.yaml:30821, 30834, 30847, 30860`). That is the source’s report of the
regularizer’s own step against the solved input, as the schema says
(`results.schema.yaml:416–419`). Against the credited certificate, the views turn
squares at three counts: 12 beyond $10^{-3}$° at 204, 4 at 227 (one by 2.54°) and 31 at
229, several of them exactly to the axis.
The generated line then reads “no angle changed; … turns up to 0.159°” at 204, “5.84°”
at 227 and “0.055°” at 229 (`RESULTS.md:498–500`). The wording comes from
`result_credit.py:145`, and T-146’s lines read the same way (`RESULTS.md:298–305`).
README line 58 says the angle changes are “free angles kept, none turned or merged”.
No number is wrong, but a reader comparing the view with the credited packing is told
nothing turned. In the README and the entry’s notes, say that the turns are measured
against the credited certificate and arise before the regularizer, as the method log’s
account of the exact solve suggests (pending Question 1). Separately, have the renderer
say “the regularizer changed no angle, as its source reports”.

**RF-3, minor, non-blocking: the packet’s controls are gross, and the kernel’s sharp
ones are not run on it.** The receipt’s controls are a duplicated square (gap $-1$) and
a square moved $S + 2$ outside, while every margin is about $10^{-20}$; the evidence
entry says so (`evidence.yaml:41206–41207`). The kernel has had sharp controls since the
20 October #668 review asked for them (`evand_arrangement_reports.SHARP_CONTROLS`,
`run_sharp`), and they pass on these four certificates here.
But neither the receipt nor `tests/test_upper_bound_reports_regularized_1020.py` runs
them, and the 10 October lists (T-146) had a third route with sharp controls that this
packet has not. Add a slow-marked test running `run_sharp` on one of these certificates
(each positive takes 2 to 4 CPU seconds a route in the receipt), or retain this review’s
controls receipts and name them in the evidence’s `limitations`.

**RF-4, note: `one_to_one: false` with moves and turns at 229 and 260.** The items at
229 and 260 record `one_to_one: false` with `moved`, `max_move` and `max_turn_deg`
(`results.yaml:30851–30854, 30864–30867`). Those figures come from an optimal
assignment, not from the nearest-centre pairing that `one_to_one` refers to.
The regularization policy’s clarification of 16 October says a view without the pairing
“records only that it has none … with no move or turn to state”
(`regularization-policy.md:91–94`). T-146’s items at 123 and 129 predate it and do the
same. Either drop the three figures at 229 and 260, or record that they are from the
assignment and that the clarification governs the drawing layer only.

**RF-5, note: the ledger’s own cross-check is open.** The 21 October ledger reports that
`claims.json` at 229 reads #672 as a pending report (print 15.650174740273), which the
ledger does not list at 229 (`upper-bounds-20261021/README.md:121`). #672 does print a
229 side, so either the ledger lists it there or the claim record drops it.
Nothing at 229 turns on it: the view is below #672’s print by $1.32 \times
10^{-5}$.

**RF-6, note, for the record: this review’s programs and receipts must be retained.**
They are in this lane’s scratch directory and decide nothing until they sit in
`packing/resources/web/evand-regularized-2026-10-20/review/review-2026-10-21/` with
their README. The deciding programs, `review_t225_check.py` and
`sharp_controls_t225.py`, must also be registered in `verifiers.yaml` with their
independence records, as Stage 4 and
[epistemics.md](../../../epistemics.md#every-runs-code-is-kept) require.

## Questions for the Author

1. At 204 and 229, squares that are 0.02° to 0.09° off the axis in the posted
   certificates (#678’s `n204.cert`; your `s229_v2.cert`) are exactly axis-aligned in
   the views. At 227, one square is at 50.18° where #672’s certificate has 52.72°. Yet
   each JSON’s `angle_changes` lists only free angles kept.
   Did `refresh.py`’s exact solve, or at 229 the slp2 polish, make these turns?
   And does the level-2 statement cover the path from the posted certificate, or only
   the regularizer’s moves from the solved input?
2. Was the store’s packing at 227 #672’s `certificates/n227.cert` at
   `franciscouzo/square-packing@af8cb79` (SHA-256 `65b03df8…`)? Was it #678’s
   certificates at 204 and 260, and `s229_v2.cert` at 229? 194 of 227, 132 of 204, 207
   of 260 and 95 of 229 squares lie within $10^{-6}$ of those certificates.
3. At 229, nearest centres pair the view with `s229_v2.cert` under no symmetry, and 13
   squares lie more than a tenth from their partners in an optimal assignment (largest
   0.650). Are these the slides that the method log says are connected “by
   construction”?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, at all four counts, once the
replay evidence and this review are entered: a retained certificate, a replay command
(`check --replay`), a passing replay reproduced here, retained controls refused by every
route that accepted the positive, and sharp controls refused here.
Neither maintained route is the source’s code, and this review’s checker is a further,
clean-room re-implementation: its author never read the source’s checkers.
It is by a Claude agent, a system family whose involvement the source’s credits also
state. This review is the accepted adversarial review that
`select_houses.accepted_review` needs once mapped and entered with `covers` naming the
entry.
It does not reach `V4`/`C4`, which needs a second accepted adversarial review by a
distinct reviewer and a retained human oversight record.
The register’s count of distinct machine methods is unchanged: every route is
`exact-algebraic`, and this review’s clipping area is a second pair procedure within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`evidence.yaml`.** Add a confirming entry for the replay at {204, 227, 229, 260}:
  - `assurance: verified`, `method: exact-algebraic`, `origin: replayed-here`,
    `relationship_to_generator: independent-implementation` (no route is the source’s
    code, as for T-146’s);
  - `verifiers` naming the five maintained programs;
  - the `check --replay` command and `replay_status: passed`;
  - an independence record with `coverage: full`, whose `read` says whether the import
    lane read the source’s pinned checkers;
  - `limitations` naming RF-3;
  - this document as `external_review`.

  Add one entry for this review’s checker and controls:
  - `independent-implementation`, `coverage: full` over the four certificates;
  - `clean_room: true`, `shares: []`;
  - `read: [mathematics, certificate-format, specification, producer-output]` (the
    format line, the method log and the JSON files; no producer code);
  - `written_by` this lane, with `overlaps_producer: system-family`,
    `separate_prompt: true` and `separate_code: true`.

- **`verifiers.yaml`.** Register `review_t225_check.py` (decides) and
  `sharp_controls_t225.py` (drives the maintained routes and this review’s checker on
  mutants), with their digests, retained paths and the independence record above.

- **`results.yaml`, the entry.**
  - Add a `reviews` entry for this document: `kind: adversarial`, `reviewer_kind: ai`,
    `relation: project`, `verdict: accepted`, `covers` the entry.
  - Rewrite the claim, `notes` and `next_rung` together, the claim saying *confirmed,
    independently re-implemented*, and remove `unfinished_confirmations`’ C3 item.
  - Keep the significance at S2, its `by` naming this review.
  - At 227, apply RF-1. In the notes, apply RF-2 and RF-4.
  - Print the verified bound at 228 rounded up, as 15.60460147572968, in the notes and
    the packet README (Review A’s A5, confirmed here).

- **Adoption.** At all four counts the entry’s views replace the houses (T-223 at 204
  and 260, T-196 at 227, T-199 at 229), with both strong generators’ runs on each
  re-housed count as the House Rule requires.
  Publish 227’s credit only after RF-1 is resolved.

- **The packet.** Add a `review/review-2026-10-21/` directory with this review’s
  programs, outputs and README (RF-6). Revise README line 58 per RF-2. Add a sentence
  pointing at this document once mapped.

- **Tests.** RF-3.

## Comparison with the Earlier Review

No earlier mathematical review of these certificates exists.
The pull request’s senior engineering review (Review A of #716, round 1, at `be6416a03`,
[issuecomment-6328806725](https://github.com/jlevy/squares/pull/716#issuecomment-6328806725))
covers the same entry among 58 changed files.
This reviewer read it only after the findings above were written, and changed none of
them for it.

**Where they agree.**

- Both find the bounds sound and new by exact arithmetic, at the same four margins.
  Both find the least later bound at $n + 1$, and both confirm S2 by T-146’s scale.
- Review A’s A2 is RF-1: `of: T-196` sends #672’s credit to de Winter.
  It grades it Medium where this review grades it major, and adds a second remedy:
  credit Couzo as improver through `adopt_houses.CREDITS` (`via=`), with a test, if the
  adoption is not to wait for #672’s registration.
- Its A12 asks the C3 item to name the sharp controls, which is RF-3’s substance.
- Its remark that the ledger omits #672 at 229 is RF-5.

Review A reproduced `check --replay` (61 s) and re-ran the import lane’s `identity.py`
on the same fetched bytes, with byte-identical output.
This review instead re-implemented the identity measurement.
Its own Hungarian algorithm and exact thresholds agree with every displacement count.

**What Review A found that this review did not.**

- **A5:** the verified bound at 228 is printed rounded down, as 15.60460147572967
  (`results.yaml:30907`; the packet README, line 149). That is confirmed here by exact
  arithmetic: the print lies $4.3 \times 10^{-15}$ below the exact form, while the
  prints at 205, 230 and 261 lie above theirs.
  Newness is unaffected.
- **A6:** `max_turn_deg: 0` at 260 records a measured $1.294 \times 10^{-7}$°. This
  review tabulated the value but raised no finding on it.
- **A7:** the wording of the 260 credit clause.
- **A11:** the credit line omits Polkovskyi, whom Couzo’s source credits at 204. This
  review had judged the omission defensible, since Daniel’s source names Couzo only.
  The 10 October lists’ line, which names every finder, favours adding him.
- A1, A3, A4 and A8, which concern other texts, replies, the release and dates, outside
  this review’s scope.

**What this review found that Review A did not.**

- RF-2: the turns of the views against the credited certificates, beside “no angle
  changed” and README line 58.
- RF-4: moves and turns recorded at 229 and 260 with `one_to_one: false`, against the
  policy’s 16 October clarification.
- The sharp controls actually run, on both maintained routes and on this review’s
  checker, and a clean-room checker whose integer route shares no arithmetic library
  with any other route.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight.
No run of the source’s checkers, solver, polish, regularizer or path test, and
no decision of the same-packing statements.
No house best packing adoption, case-record change or regularization run.
No decision of #672’s registration; its certificate was read and decided here only to
measure lineage (`out-check-672-n227.json`: feasible at its own side on both routes).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
