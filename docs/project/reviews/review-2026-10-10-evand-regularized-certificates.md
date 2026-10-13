# Review: Evan Daniel’s Regularized Certificates at Fifteen Counts (T-146)

**Date:** 11 October 2026. **Verdict: accepted, for finite feasibility only.** All
fifteen certificates T-146 cites prove the upper bounds the entry states: Evan Daniel’s
display-regularized record lists at 70, 102, 103, 123, 129, 146, 153, 236, 258, 263,
269, 292, 295, 302 and 303, which no issue reports.
The retained receipt reproduces here job for job on both maintained routes; the third
exact route agrees with it at every side, pose and margin and holds every retained byte
to the upstream file at its pin, fetched here; a checker written for this review from
the format and the mathematics accepts all fifteen and refuses their controls; and every
printed side in the claim is the certificate’s exact side.
Eleven findings are recorded, none blocking.
The credit question the import lane left open is decided below, count by count: the
record may state the source’s account of each certificate as the source’s, and may not
state as its own that any side is the exact optimum of the credited packing.
The entry can take `V3`/`C3` when its confirming evidence entry and this review are
added; it cannot take `V4`/`C4` from this review alone.

This review was written by an AI agent (Claude, at extra-high reasoning effort), the
stage 4 review lane (W2) of the 2026-10-10 intake pass under think-8k76, prompted
separately from the import lanes that built the packet, with no shared context: lane W2
of [result-import.md](../../../packing/campaign/result-import.md#stage-4-validate).
Its relation to the result is `project`. It moves no rung, writes no register row and
adopts no house; the proposed record changes are listed at the end for the records lane.

## Claims Covered

| Entry | Source | Counts | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-146 | Evan Daniel, `evand/square-packing` at `ea1a2f2`, `search/regularize/lists/certs/`, first committed in `346c6ed` (2026-10-10T18:05:38Z); no issue | 70, 102, 103, 123, 129, 146, 153, 236, 258, 263, 269, 292, 295, 302, 303 | 30 places, each the exact side in full, equal to the `S_cert` of the JSON beside it |

The exact sides are the fractions the packet’s README tabulates and its claim record
freezes
([README](../../../packing/resources/web/evand-regularized-2026-10-10/README.md)). Every
denominator divides $10^{30}$, so every side terminates within 30 places, and the
30-place print in the entry’s `claim` equals the exact side at all fifteen counts; this
review recomputed each expansion from the decompressed certificate and compared.
The lists hold 329 certificates in all; the other 314 are pinned by the commit, were not
retained, and are outside this review.

**Read in full.** `devtools.upper_bound_reports` (the declaration loader, the adapters,
`admit`, `_read`, `read_facts`, `HOUSES` and `house_side`, `check_certification`,
`receipt_parts`); the kernel `evand_arrangement_reports` (`job_input`, `run_case`,
`validate_job`, `validate_receipt`, `replay_receipt`); the parser and conversion in
`evand_exact_certificates` (`parse`, `Pose.basis`, `Pose.corners`, `basis_witness`,
`corner_squares`); `sqpack.witness` (`exact_verify`, `_exact_materialize`,
`_square_from_pose`, `_margin_summary`, `_rational_sign`) and `sqpack.verify`
(`edge_axes`, `project`, `separated`, `candidate_pairs`, `check_unit_squares`,
`verify_packing`); `check_rational_witness_independent`; the third route
`devtools/check_half_angle_area.py` (its parser, `rotation`, `corners`, `intersection`,
`overlaps`, `closest_points`, `decide_placed`, `controls_placed`, `verdict`, the import
readers, `admitted`, `printed_json_side`, `upstream_problems`, `symmetric`,
`arrangement_gap`, `credited_gaps`, `run_decide_imports`) and the regularized tests of
its test module and of `test_upper_bound_reports_regularized.py`; the packet’s README,
declaration, acquisition record, manifest and claim record; the method log
`REGULARIZE.md`, `LICENSE` and `CREDITS.md` as retained; `best.csv`, `best.json`,
`site/data/records2026.json` and the fifteen `n-NNN.json.gz` at the pin, fetched here;
the import lane’s notes on think-8k76; the three earlier imports reviews; the entries
T-098, T-125, T-136, T-137, T-138, T-139 and T-140;
[epistemics.md](../../../epistemics.md) on review records, confirmation and credit.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host at
a load average of 0.3 to 2.0, at most two worker processes, on
`claude/determined-rubin-yjfy2a` at `3ec95b418`, with nothing of the importer or the
routes changed. A replay decides every job of the roster again through both maintained
routes, serially in one process, and compares every field of each fresh job with its
retained row except the measured times.
The serial replay ran beside the third route and this review’s own checker, so its wall
overstates the work; the import lane’s serial replay, alone, took 476 s.

| Command (`python -m devtools.…`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `acquire_source evand-regularized-2026-10-10 --check` | custody of the 33 retained and 5 pinned files, the two checkers’ `identical_to` twins compared | `PACKET_MATCHES_ITS_CONTRACT` | 0.1 s |
| `upper_bound_reports evand-regularized-2026-10-10 check-claims` | the frozen comparison rebuilt from the certificates and the houses’ own packets | rebuilt equal | 3.0 s |
| `upper_bound_reports evand-regularized-2026-10-10 check` | the receipt admitted structurally against the retained certificates | 15 certificates and 45 jobs admitted | 0.5 s |
| `upper_bound_reports evand-regularized-2026-10-10 check --replay` | all 45 jobs, all fifteen counts, on both maintained routes | all 45 equal | 535.5 s (530.9 s CPU) |
| `check_half_angle_area decide-imports --workers 2 --imports regularized --upstream evand-regularized-2026-10-10 DIR` | the third route on the fifteen certificates and their 90 controls, every cross-check against the maintained routes and the record, and the 30 retained gzip files against their fetched upstream bytes and `S_cert` prints | no disagreement; 359,228 pairs | 137.7 s (121.7 s CPU) |
| a checker written for this review (`Fraction` arithmetic, no project code), at all fifteen counts, with three controls each | unit squares, closed-box containment, separating axes on every pair; the duplicate, the box shrunk $10^{-40}$ past the far-wall clearance, and the box at exact far-wall contact | all fifteen feasible; 30 refusals and 15 acceptances as required | 28.4 s in all, 0.1 to 2.0 s each |
| `pytest -n 2 -m "not slow"` on `test_upper_bound_reports_regularized.py`, `test_upper_bound_reports.py` and `test_check_half_angle_area.py` | 239 tests | all passed | 20.6 s |

`DIR` is a scratch directory holding the source’s files at the pin (below).
Each wall includes the interpreter’s start.
The receipt’s own totals, read here directly from the retained `json.xz` and recomputed
by the third route, are the numbers the packet prints: 45 jobs, 2,155,368 pair
decisions, 413.8 route CPU seconds, 566.29 job wall seconds, the longest job 39.16 s
(the outside-container control at 295).

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Each certificate is in Evan Daniel’s text format, stored as the
original gzip: one comment line, which no route believes, then a header `n S` and, for
each square, a rational centre $(x, y)$ and $t = \tan(\theta/2)$, each a fraction with a
power-of-ten denominator.
The bound $s(n) \le S$ follows from four facts, each decided by every route:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$, and the corners
   $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ form a unit square.
   `sqpack.verify.check_unit_squares` holds every edge to length 1 and every corner to a
   right angle; the independent checker holds the edges to unit length, orthogonality
   and closure; the third route holds $(c, s)$ to the unit circle; this review’s checker
   holds the edges and corners it builds.
2. **There are exactly $n$ of them.** `legacy.parse` refuses a header count that differs
   from the file name’s, fewer or more rows than $n$, and any literal that is not an
   integer, a fraction or a plain decimal; the third route’s parser refuses the same.
   The kernel holds every job to $n(n-1)/2$ pairs tested, so no bucketing or early exit
   can have skipped a pair; the receipt’s 45 jobs state that count at every route.
3. **Each lies in the closed box $[0, S]^2$**: every corner has $0 \le x \le S$ and
   $0 \le y \le S$ on the maintained routes, or equivalently $h \le x \le S - h$ and
   $h \le y \le S - h$ with $h = (|c| + |s|)/2$ on the third.
4. **Interiors are pairwise disjoint**, by an edge normal that separates the two squares
   (the maintained routes and this review’s checker) or by an intersection of area zero
   (the third route).

Arithmetic is exact `Fraction` arithmetic throughout, and nothing rounds, dilates or
tolerates. A touching pair or a corner on a wall is a zero sign and is accepted; an
overlap is a negative sign and refused; a duplicated square overlaps itself.

**The box convention does not matter here.** No square of any certificate touches a
wall: every route finds the least wall clearance exactly $1/(2 \cdot 10^{20})$ at every
count, the third route counts zero wall contacts, and the least far-wall clearance is
$5 \cdot 10^{-21}$ plus between $2.2 \cdot 10^{-33}$ (123 and 292) and
$9.1 \cdot 10^{-31}$ (236). That is the source’s construction as its method log states
it, read here and not run: the regularized packing is scaled about the origin corner by
$1 + 10^{-20}$ and the side rounded up, so a square that touched the origin walls now
clears them by $\varepsilon/2$. Each certificate’s side is the `S_exact` its JSON prints
times a factor that exceeds $1 + 10^{-20}$ by $1.3 \cdot 10^{-34}$ (292) to
$8.1 \cdot 10^{-32}$ (103), measured here, which is the rounding up at 30 places.
The least separating-axis gap is just under $10^{-20}$ at every count and the least
Euclidean distance between squares is $1.000000 \times 10^{-20}$ on the third route, so
the closed squares are pairwise disjoint and strictly inside the open box, and each
bound holds under any of the usual conventions.
The packet README’s “open square of the stated side” and the record’s closed box are the
same claim here.

## Adapters and Admission

The packet declares one format, `evand-cert`, and no derived fact.
Each certificate is read by `legacy.parse` from the retained gzip after `_read`
decompresses it (`read_retained_bytes`, which refuses a symlink, a file outside the
repository or one above the byte ceiling), and by the third route’s own parser after
`packet_bytes` decompresses it itself.
Each row of the declaration offers the exact fraction, so `admit` holds the parsed side
to it by equality, and `check-claims` compares nothing at a print.
The third route’s `admitted` holds the same.

**Where the side is printed.** Each row names the gzipped JSON beside the certificate as
`printed_in`, and `printed_json_side` holds the fetched copy to the retained bytes and
its `S_cert` to the offered side for the row’s count: 15 of the 30 upstream checks.
This review also read each JSON directly: `S_cert` equals the certificate’s header side
at all fifteen, and each `note` reads “regularized display view of a certified packing
at the same side; not a new bound”.

**What the adapters decide, and what they do not.** Every route decides in full the
packing it is handed, so a misreading cannot make a false bound pass.
What a misreading would break is attribution, which rests on custody.

## Custody

The packet keeps 33 of the manifest’s 38 files as bytes, under the source’s MIT licence,
and pins five by digest: the two checkers, `best.csv`, `best.json` and
`site/data/records2026.json`. `acquire_source.check` binds each retained file to its Git
blob at the pin and each pinned file to its digest, and compares the two checkers with
the issue-399 packet’s copies (`identical_to`).

For this review the source was fetched again at the pin, by a sparse blobless Git fetch
of `ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7` through the session’s read-only proxy into
a scratch directory outside the repository, and read as data; nothing fetched was run.
The commit’s tree is `ce00909386d0a1b4800a21d7d36436156a447a81`, committed
2026-10-10T20:37:25Z, as the acquisition record states.
All 38 manifest files have the manifest’s digests; the 33 retained ones equal their
upstream bytes, the thirty gzip files as stored; `verify_cert.py` and `verify_cert2.py`
equal the issue-399 copies (3,401 and 3,101 bytes).
The third route’s `--upstream` check held the fifteen certificates and fifteen JSON
files to the same fetched bytes, 30 checks, no disagreement.
`best.csv` at the pin names each of the fifteen as the list’s choice, with its variant,
its level (“2 same packing (traversable without expansion)” at all fifteen), its
orientation and the source’s finder; `records2026.json` at the pin credits each count’s
first posting as the packet README states.

**Licence and credit.** The tree carries `LICENSE` (MIT, copyright 2026 Evan Daniel) and
`CREDITS.md`, both retained; the credits file is the repository’s lower-bound credits
and says the work was produced by Claude (Anthropic) under human direction.
No issue asks for this import, so no author’s request fixes its credit; the source’s
attribution of the packings is read from `records2026.json` and `best.csv` at the pin
(below).

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the parse and half-angle map of `evand_exact_certificates` (`parse`, `Pose.basis`); `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `gzip`, `json`, `hashlib` | `Fraction` and the format’s meaning only |
| this review’s checker | unit shape from its own corners, closed-box corners, disc rule then separating axes | nothing of the repository; `gzip`, `fractions` | `Fraction` and the format’s meaning; the separating-axis method |

`upper_bound_reports` owns custody, the adapter, admission, the claim comparison and the
job layout; the kernel owns the two controls and `validate_job`, which both maintained
routes are held to. The two maintained routes are two implementations of one method with
a common front end: a defect in `legacy.parse` or in `Pose.basis` would reach both.
The third route and this review’s checker each read the gzip and the text themselves,
convert $t$ themselves and decide by a procedure of their own, so a false bound would
need four implementations of two pair-deciding procedures to agree on it.

**The relation each route would carry.** None of the sources’ programs ran: Daniel’s
`verify_cert.py` and `verify_cert2.py` (pinned, not retained), his `reg.py`, `atlas.py`,
`refresh.py`, `samepacking.py` and `exactsolve`. Nothing states that the source ran this
repository’s `sqpack` on these certificates.
So each route here is `independent-implementation` against the producer’s code, and the
confirming evidence entry takes that relation; the maintained routes’ shared parse and
map are shared with each other, not with the producer.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
The method log’s statements are source reports and are not decided: that every one of
the lists’ 324 certificates is VALID under both source checkers and verified at 80
digits; that each refreshed side is the exact optimum of the store’s best packing, below
the posted side only by rounding; that each of the fifteen views is the same packing as
the store’s best, traversable without expansion, by the path test (`samepacking.py`),
which the log says samples angle paths in steps of at most $0.01°$ and is not a
continuous proof; and that all 27 regularized packings with angle moves above $10^{-3}$
degrees are local minima at $S^*$ by `exactsolve`. The 80-digit KKT point each view was
made from (`runs/regularize/exact/n-N/`) is not published, so nothing here can compare
the view with the packing it was solved from; the JSON’s `S_exact` is a 60-digit
decimal, not that point’s exact side.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RD-2 of the first
replay review, carried as RI-3, RK-8 and RL-4). `validate_job` requires both routes to
refuse each control, on the complete pair count, with the negative diagnostic it was
built for. Read here directly from the retained receipt: the duplicate’s gap is exactly
$-1$ at all fifteen counts, and the moved square lies 3.00 to 17.00 units outside the
box (17.00 at 263, 13.59 at 123, 13.58 at 146, 12.61 at 102, 9.22 at 153, 9.02 at 236,
8.36 at 302, 4.00 at 103 and 3.00 at the other seven), refusals a binary64 checker with
a $10^{-9}$ tolerance would also make.
They show the routes can refuse, not that they decide at the $10^{-20}$ scale where
these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate, and this review’s checker two of its own:

| Control | Required | Scale | Where |
| --- | --- | --- | --- |
| square 1 replaced by square 0 | refused | gross | third route; this review |
| square 0 moved by $S + 2$ | refused | gross | third route |
| side reduced by the least far-wall clearance, just above $5 \cdot 10^{-21}$ | accepted: the box is closed | exact contact | third route; this review |
| the same side less $10^{-40}$ | refused | $10^{-40}$ | third route; this review |
| the closest pair translated into contact | that pair accepted | exact contact | third route |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ | third route |

All 90 of the third route’s and all 45 of this review’s reached their required outcome.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all fifteen sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- every side equals the exact side of the packet’s frozen claim record and the value the
  register plan’s claim states, and is admitted against its `S_cert` print;
- every least wall clearance equals both maintained routes’ to every digit, exactly
  $1/(2 \cdot 10^{20})$ at all fifteen;
- every least Euclidean distance, $1.000000 \times 10^{-20}$ at all fifteen, is at least
  the separating-axis gap both maintained routes report;
- the receipt’s totals are the numbers the packet prints, and the thirty retained files
  are the fetched upstream bytes.

This review’s checker found the same least wall clearance, the same least far-wall
clearance to every digit, and a least separating-axis gap of $1.000 \times 10^{-20}$ at
every count, and the pair count $n(n-1)/2$.

## The Claims Comparison

The packet’s `acquisition/claims.json` freezes each certificate against the case record
as it stood at `main` `af17208c0` and against every report pending there, each ceiling
rebuilt from its holder’s own retained packet; `check-claims` rebuilt it equal.
This review recomputed every relation from the decompressed certificates with
`Fraction`, and read the holders’ sides again by another path: Ryan Xu’s `s_exact` from
his packet’s `facts/complete-certificates.json.xz` at all seven of his counts, and the
derived facts of the issue-483, issue-470 and issue-481 packets at 70, 103, 258, 153,
292, 302 and 303. Every side equals the frozen record’s, and no relation changes:

| n | Certificate, exact side rounded up at 16 places | Below the case ceiling by | Against the pending reports, exactly |
| --- | --- | --- | --- |
| 70 | 8.8809603715555796 | $1.53 \times 10^{-10}$ (Ryan Xu, T-125) | below #483 (T-137, Eric Deleeuw) by $1.07 \times 10^{-11}$ |
| 102 | 10.6058286964315784 | $7.90 \times 10^{-11}$ (T-125) | none pending |
| 103 | 10.6792320473613065 | $1.49 \times 10^{-10}$ (T-125) | below #470 (T-138, Mishapolk) by $6.94 \times 10^{-13}$ |
| 123 | 11.5913781454976982 | $2.14 \times 10^{-10}$ (T-125) | none pending |
| 129 | 11.8720298490811800 | $1.31 \times 10^{-10}$ (T-125) | none pending |
| 146 | 12.5837822774150769 | $9.75 \times 10^{-11}$ (T-125) | none pending |
| 153 | 12.8720298490811800 | $7.65 \times 10^{-3}$ (SQUISH improved by Gupta, T-127) | below #481 (T-136) by $8.48 \times 10^{-16}$ |
| 236 | 15.8639557471592675 | $3.85 \times 10^{-3}$ (T-127) | below #481 by $3.29 \times 10^{-16}$ |
| 258 | 16.5634480021337894 | $5.36 \times 10^{-12}$ (SQUISH, T-115) | below #470 by $4.21 \times 10^{-12}$ |
| 263 | 16.7331660078993790 | $7.25 \times 10^{-3}$ (SQUISH, T-116) | below #481 by $5.05 \times 10^{-13}$, #476 (T-134) by $7.25 \times 10^{-3}$ |
| 269 | 16.9015135821891322 | $4.45 \times 10^{-3}$ (Couzo improved by Daniel, T-098) | below #481 by $6.73 \times 10^{-16}$, #476 by $4.45 \times 10^{-3}$ |
| 292 | 17.5913781454976982 | $5.87 \times 10^{-3}$ (Couzo improved by Rehwaldt, T-117) | below #481 by $2.03 \times 10^{-13}$ |
| 295 | 17.7042327907360304 | $7.82 \times 10^{-10}$ (T-125) | none pending |
| 302 | 17.8720298490811800 | $9.28 \times 10^{-3}$ (SQUISH, T-116) | below #481 by $2.21 \times 10^{-17}$, #470 by $9.28 \times 10^{-3}$ |
| 303 | 17.9130654627385324 | $7.25 \times 10^{-3}$ (SQUISH, T-113) | below #481 by $4.48 \times 10^{-16}$, #488’s uncited side by $4.30 \times 10^{-3}$, #476 by $4.38 \times 10^{-3}$, #470 by $7.25 \times 10^{-3}$ |

At every count the certificate is the smallest side the record holds or has pending.
The least margin is $2.21 \times 10^{-17}$ at 302 and the largest least margin
$7.82 \times 10^{-10}$ at 295, as the entry states; the gaps to the case ceilings run
from $5.36 \times 10^{-12}$ at 258 to $9.28 \times 10^{-3}$ at 302. Where the gap to the
case ceiling is large, at 153, 236, 263, 269, 292, 302 and 303, the improvement is
SQUISH’s of issue 481 (T-136), pending adoption, and this certificate’s own margin over
it is $2.21 \times 10^{-17}$ to $5.05 \times 10^{-13}$. That is the import lane’s
comparison and lane L26’s triage, rederived here.

## Whose Arrangements These Are

The question the import lane left open is what the record may say about each
certificate’s lineage.
The source says three things.
Each view was made from the store’s best packing at its count, refreshed and solved by
`exactsolve` to an 80-digit KKT point whose side, `S_exact`, the log calls “the exact
optimum of the same packing”, 2 to $8 \times 10^{-10}$ below the posted side.
The view is that packing regularized at fixed side: translated by an LP toward the
bottom-left corner and the walls, with symmetries and coincident faces imposed, and its
angles grouped; each of the fifteen is “level 2: same packing, different arrangement,
traversable without expansion”, by the path test.
And the orientation was refitted to this register’s witnesses and the finder read from
the catalogue, so `best.csv` names Joe DeVincentis, Francisco Couzo, David Ellsworth and
David W. Cantrell as finders of the arrangements the packings descend from, while
`records2026.json` credits each record’s first posting: issue 432 (Ryan Xu) at 70, 102,
103, 123, 129, 146 and 295, issue 401 (SQUISH) at 258 and issue 481 (SQUISH) at the
seven others, with issue 470 (Mishapolk) as a second posting at 103 and 258 and nothing
of issue 483 at 70.

The fifteen JSON files record what the regularization moved.
Eight views are the `conservative` variant, which moves only free squares’ angles: at
102, 103, 123, 146 and 295 no angle changed at all, at 258 free angles were kept, at 302
56 free squares were straightened and 26 free angles moved by up to $2.29°$, and at 303
one free square was straightened.
Seven views are the `fewest` variant, which also merges determined rotation groups, a
step the log of round 5 first called “a different packing at the same side” and the
policy of 10 October then admitted under the path test: at 70 (four squares, up to
$0.93°$), 129 (eight, up to $2.96°$, from a polished input, with sixteen free squares
straightened), 153 (two, $1.81°$), 236 (seven, up to $0.67°$), 263 (four, $1.06°$), 269
(two, $0.12°$) and 292 (three, up to $0.03°$). The log also says the translation moves
are “connected by construction”, each LP step staying in a convex region of valid
packings at fixed separating normals, which is sound mathematics for a path at fixed
angles; the angle moves are what the sampled path test covers.

For credit, this review measured each view against the certificate the entry credits,
square to square, as the third route does and by a stronger matching.
The third route’s `arrangement_gap` matches every square to the nearest centre of the
other packing under each of the box’s eight symmetries and keeps a symmetry only where
that is one to one; this review also solved the optimal assignment of squares under each
symmetry (Hungarian, in binary64) and took the symmetry with the least largest
displacement, so a view whose squares slid past their neighbours is still paired square
for square. A measurement, deciding nothing; the source’s path test was not reproduced.

| n | Against | Best symmetry | Squares within $10^{-9}$ | Moved beyond $10^{-3}$, $10^{-1}$ | Largest move | Turned beyond $10^{-6}$ (largest sine) | Nearest centres one to one |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 70 | T-125, Ryan Xu | identity | 60 of 70 | 10, 3 | 0.222 | 6 ($0.383$, a caged square through $22.5°$) | yes |
| 70 | T-137, Eric Deleeuw | identity | 50 | 10, 3 | 0.222 | 6 ($0.383$) | yes |
| 102 | T-125 | a quarter turn | 80 of 102 | 18, 6 | 0.169 | 1 ($7.6 \times 10^{-3}$) | yes |
| 103 | T-138, Mishapolk | three quarter turns | 87 of 103 | 15, 0 | 0.074 | 1 ($7.2 \times 10^{-3}$) | yes |
| 123 | T-125 | a reflection and a quarter turn | 78 of 123 | 45, 25 | 0.591 | 0 | no |
| 129 | T-125 | a half turn (the identity is as far) | 86 of 129 | 43, 31 | 0.834 | 26 ($0.635$, about $39°$) | no |
| 146 | T-125 | identity | 121 of 146 | 25, 3 | 0.124 | 0 | yes |
| 153 | T-136, SQUISH | a half turn | 44 of 153 | 80, 0 | 0.065 | 25 ($0.042$) | yes |
| 236 | T-136 | identity | 140 of 236 | 53, 0 | 0.068 | 15 ($0.012$) | yes |
| 258 | T-138 | identity | 186 of 258 | 48, 13 | 0.496 | 4 ($0.020$) | yes |
| 263 | T-136 | a reflection and a quarter turn | 101 of 263 | 132, 0 | 0.049 | 30 ($0.021$) | yes |
| 269 | T-136 | three quarter turns | 200 of 269 | 54, 0 | 0.088 | 18 ($0.020$) | yes |
| 292 | T-136 | three quarter turns | 53 of 292 | 239, 11 | 0.589 | 51 ($0.080$, about $4.6°$) | no |
| 295 | T-125 | identity | 105 of 295 | 122, 37 | 0.138 | 0 | yes |
| 302 | T-136 | identity | 46 of 302 | 198, 2 | 0.102 | 80 ($0.046$) | yes |
| 303 | T-136 | three quarter turns | 250 of 303 | 19, 1 | 0.135 | 7 ($0.021$) | yes |

Where nearest centres match one to one, the symmetry and the counts equal the third
route’s and the import lane’s. The best symmetry is in every case the re-orientation the
lists’ `orientation` column states.
At 103 and 258 the credited certificates are Mishapolk’s, which the review of issue 470
measured as Ryan Xu’s packing and SQUISH’s update refined in place, to $10^{-9}$, so the
measurement against them is the measurement against those packings.
At 70, Eric Deleeuw’s certificate is Ryan Xu’s refined in place, measured here: the
identity, every square within $1.9 \times 10^{-8}$ of Xu’s and none beyond $10^{-6}$.

**What the measurements show.** Every view differs from the credited certificate pose by
pose, as display regularization is meant to.
At twelve counts the squares still stand where they stood to within what the
regularization says it moved, and nearest centres pair them one to one.
At 123, 129 and 292 they do not: at 123 the slides are pure translations of a strip
packing at fixed angles, up to 0.59, and the assignment pairs 78 squares to $10^{-9}$;
at 292 slides up to 0.59 come with turns of up to about $4.6°$ on 51 squares; and at
129, the view made from a polished input, sixteen free squares were straightened, 26
squares turned by up to about $39°$ and 31 moved by more than a tenth, so that the
assignment under the half turn and under the identity are equally far.
Nothing here distinguishes a regularized view of the credited packing from a different
packing at the same side: the KKT point the view was solved from is not published, the
path test did not run here, and a measurement of poses cannot decide connectivity.

**The decision.** The bound each certificate proves is its own, and takes no lineage.
What the record may say about lineage is the source’s account, attributed, and it may
not say as its own that any side is the exact optimum of the credited packing: no exact
solve ran here, the solved point is not retained, and the certified object is, in the
source’s own scale, a different arrangement at the same side.
Count by count:

| n | Credit the packing to | The record may say | The record must add |
| --- | --- | --- | --- |
| 102, 103, 123, 146, 258, 295 | Ryan Xu (issue 432); at 103 as Mishapolk refined it (issue 470); at 258 SQUISH (issue 401) as Mishapolk refined it | Evan Daniel’s display-regularized arrangement of the packing, at the side he reports as its exact optimum; no angle changed, and the source says its translation steps are connected by construction | at 123, that its squares match Ryan Xu’s one to one only by optimal assignment, slid by up to 0.59 at fixed angles |
| 302, 303 | SQUISH (issue 481) | the same, with free squares re-angled | nothing further |
| 70, 153, 236, 263, 269 | Ryan Xu at 70; SQUISH (issue 481) at the others | the same, with determined rotation groups merged by up to $0.93°$, $1.81°$, $0.67°$, $1.06°$ and $0.12°$, which the source classes as the same packing by its sampled path test | at 70, that one caged square turned $22.5°$ |
| 129, 292 | Ryan Xu at 129; SQUISH (issue 481) at 292 | a certificate the source derives from the packing by display regularization that merged determined rotation groups ($2.96°$, $0.03°$) and, at 129, straightened sixteen free squares from a polished input; the source classes each as the same packing by its sampled path test | that no symmetry matches nearest centres one to one; by optimal assignment the squares slid by up to 0.83 and 0.59 and turned by up to about $39°$ and $4.6°$, so the lineage is the source’s statement alone |

In every row Evan Daniel is credited with the exact solve, the regularized arrangement
and the certificate, and the finder of the packing with the packing, as T-098 and T-139
credit. The bibliography key’s `credit` line should follow the source’s own attribution
files at the pin (`records2026.json`, `best.csv`), as
[epistemics.md](../../../epistemics.md#parallel-projects-and-their-credit) asks, and
those name issues 432, 401, 481 and 470 and the catalogue finders; they do not name Eric
Deleeuw (RG-2).

**Credit at 70, for the owner.** The source’s store holds Ryan Xu’s posting: the site’s
provenance credits issue 432 alone at 70, and the view’s sixty unmoved squares are Xu’s
poses to $10^{-9}$ and Deleeuw’s to $10^{-8}$ only, since Deleeuw’s refinement moved
nineteen of them by up to $1.9 \times 10^{-8}$. Eric Deleeuw’s T-137 is the smallest
side the record held at 70 and stays in the notes as that; it is not a link in this
certificate’s lineage.
The recommendation is to credit Ryan Xu, with Eric Deleeuw’s refinement named as the
record’s prior smallest side, and to drop Deleeuw from the bibliography credit line,
which the source does not support; keeping him there is defensible only as the record’s
own “nearest side above” convention, and the line should then say so.

## Findings

**RG-1, non-blocking: the draft states the source’s “exact optimum” and “same packing”
as the record’s own in two places.** The significance rationale calls the fifteen “the
exact optima of packings the record already credits”, and `next_rung` says “the credit
takes that packing to be the one whose side lies just above”; the claim and notes
attribute both statements to the source.
Nothing here decided either: the exact solve did not run, its point is not retained, and
the certified arrangements are, in the source’s own scale, different arrangements at the
same side. The rewritten claim, rationale and `next_rung` below state the source’s
account as the source’s and the measurement as the record’s.

**RG-2, non-blocking, for the owner: the credit line names Eric Deleeuw, whom the source
does not.** `[Daniel regularized lists 2026-10-10]` reads `Daniel after Xu,
Chaoweeraprasit, Mishapolk, Deleeuw, Levy`. The source’s attribution at the pin names
issues 432, 401, 481 and 470 and the catalogue finders, never issue 483; Deleeuw entered
by the lane’s rule that credit follows the side just above, and his certificate is Xu’s
refined in place. The recommendation above is Xu alone at 70 with T-137 noted; `Levy`
stands on the orientation fitted to this register’s witnesses and the poster the lists
were made for, which changes no packing, and the lineage `builds-on-project` is right
for that reason. At 103 and 258 the credit should name the finders first, Ryan Xu and
SQUISH, with Mishapolk’s refinement, as the source’s provenance orders them.

**RG-3, non-blocking: at 123, 129 and 292 the arrangement’s identity rests on the source
alone.** Measured above.
The record should say so where it credits them, and the headline’s “from Evan Daniel’s
regularized record lists” already names the right object.

**RG-4, non-blocking: seven views merged determined rotation groups.** The `fewest`
variant at 70, 129, 153, 236, 263, 269 and 292 changed angles the packing determines, by
$0.03°$ to $2.96°$, which the source’s own log first called a different packing at the
same side; its level-2 classification of those seven rests on the sampled path test.
The record should name the step where it describes the regularization, as the proposed
claim does.

**RG-5, non-blocking: the kernel’s controls are gross** (RD-2, RI-3, RK-8, RL-4,
unchanged). The third route’s sharp controls and this review’s checker show the routes
decide at the $10^{-20}$ scale; carrying sharp kinds into the kernel would make the
packet’s own replay show it.

**RG-6, non-blocking: the reviewer and the producer share a model family.** The source’s
`CREDITS.md` says its work was produced by Claude under human direction, and this
review, its checker and the third route are Claude’s. The decisions are exact and do not
depend on judgment, and both maintained routes predate the import, but an error of
method common to the family would not be independent across them.
`V4`/`C4` needs a second adversarial review by a distinct reviewer in any case.

**RG-7, non-blocking for this claim: no private-worker custody** (RI-5, RK-10, RL-6).
The rung for finite feasibility does not need it; adoption should close it before a
house moves.

**RG-8, non-blocking: fields that say the review is pending.** The coverage entry’s
notes say “T-146 records them at V0/C0”, the reported evidence entry’s limitations say
“Independent review and confirmation remain pending”, the entry carries an `activity`
block, and the notes of T-125, T-136, T-137 and T-138 route the house recommendation to
T-146 “pending its review”.
The stage 4 exit rewrites `claim`, `notes` and `next_rung` together and removes
`activity`; the coverage notes, the evidence limitations and the four entries’ notes
should move in the same change, so that no field says the review is pending while
another says it passed.

**RG-9, non-blocking: the premise programs.** The confirming entries of issues 488 and
489 list the kernel and the importer but not `V-evand-exact-certificates`, the parser
and half-angle conversion both maintained routes read through, which the issue-399
entries do list. The new entry should list it, as stage 4 asks for every program the
replay runs, and the records lane may add it to the two earlier entries.

**RG-10, non-blocking, cosmetic: the packet README says “in an open square of the stated
side”.** Every square clears every wall, the third route accepts the box at exact
far-wall contact, and the record’s convention is the closed box, so nothing turns on it;
the sentence could say “in the closed box of the stated side, clearing every wall”.

**RG-11, non-blocking: the source’s claim of local minimality is not part of the
import.** The log says all 27 regularized packings with angle moves are local minima at
$S^*$ by `exactsolve`; the declaration’s claims do not carry it and the entry does not
state it, which is right.
It is noted so that no later field adds it without a replay.

## Rungs

**T-146: `V3`/`C3`** at 70, 102, 103, 123, 129, 146, 153, 236, 258, 263, 269, 292, 295,
302 and 303. Machine-replayed here: all fifteen certificates and their 30 kernel
controls on both maintained routes, the fifteen with their 90 controls on the third
route and with 45 controls on a checker written for this review, with a certificate, a
replay command, a passing replay and retained controls; reviewed adversarially here.
It does not reach `V4`/`C4`: that needs a second accepted adversarial review by a
distinct reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it. No lower bound, optimum, local minimum, same-packing connectivity, rigidity,
novelty or priority follows.

## Significance and Novelty

**S2, confirmed.** The claim is fifteen finite construction sides $2.21 \times 10^{-17}$
to $7.82 \times 10^{-10}$ below the least side the record held or had pending, each
below its case ceiling by $5.36 \times 10^{-12}$ to $9.28 \times 10^{-3}$, where the
larger gaps are improvements SQUISH’s issue 481 (T-136) already made and this entry
sharpens by $10^{-17}$ to $10^{-13}$. It changes no theorem and resolves no disputed
value; it is a citable detail of each case, as T-098’s exact optima are (S2), and unlike
T-140’s six sides, which moved their cases by $7 \times 10^{-4}$ to $8 \times 10^{-3}$
on their own (S3). The `by` field should name this review.

**`previously-published`, confirmed.** The certificates are published in the source
repository at the pin, dated by their first commit; the source claims no record and no
priority, and the entry claims none for it.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry**, `E-evand-regularized-exact-feasibility`:

  ```yaml
  - id: E-evand-regularized-exact-feasibility
    claim: upper-bound
    scope:
      n_values: [70, 102, 103, 123, 129, 146, 153, 236, 258, 263, 269, 292, 295, 302, 303]
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Daniel regularized lists 2026-10-10]'
    certificate: packing/resources/web/evand-regularized-2026-10-10/source/search/regularize/lists/certs/
    replay: >-
      From packing/ with the project interpreter: python -m devtools.upper_bound_reports
      evand-regularized-2026-10-10 check --replay decides all 45 retained jobs of the
      fifteen-count roster again through both maintained routes, serially in one process,
      and holds each to its retained row (all equal, 535.5 s wall on 2026-10-11 beside two
      other runs, 476 s alone on 2026-10-10); check-claims rebuilds the frozen comparison
      (equal, 3.0 s); python -m devtools.check_half_angle_area decide-imports --workers 2
      --imports regularized decides the fifteen certificates by the third route with six
      controls each, decompressing each retained gzip itself, and holds every side, pose,
      margin, frozen claim and S_cert print to the record (no disagreement, 137.7 s on
      2026-10-11; with --upstream evand-regularized-2026-10-10 DIR, DIR a checkout at the
      pin, it holds each retained gzip to its upstream bytes, 30 checks).
    replay_status: passed
    verifiers:
      - V-sqpack-verify
      - V-check-rational-witness-independent
      - V-evand-exact-certificates
      - V-evand-arrangement-receipts
      - V-upper-bound-reports
      - V-check-half-angle-area
    independence_record: docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md
    external_review:
      state: informally-verified
      date: '2026-10-11'
      reviewed_by: >-
        AI agent (Claude), the stage 4 review lane of the 2026-10-10 intake pass under
        think-8k76, prompted separately from the import lane
      note: >-
        Accepted for finite feasibility only. All 45 retained jobs reproduced on both
        maintained routes, the frozen comparison rebuilt equal, and the third route agreed
        with them at every side, pose, wall clearance, frozen claim and print; its 90
        controls reached their required outcomes, as did 45 on a checker written for the
        review. Every file of the manifest was fetched again at the pin and matched.
        Findings RG-1 to RG-11, none blocking.
    limitations: >-
      All fifteen certificates pass both maintained routes and the third route; their 30
      kernel controls are refused by both maintained routes and the 90 third-route controls
      reach their required outcomes, four per certificate at exact contact or 10^-40 to
      10^-30 past it. The receipt's 45 jobs hold 2155368 pair decisions, 413.8 route CPU
      seconds and 566.29 job wall seconds; the longest job took 39.16 s. Every positive
      clears its nearest wall by exactly 1/(2*10^20), no square touches a wall, and every
      pair clears by a least Euclidean distance that rounds to 1.000000e-20. No route here
      is the source's code: its checkers verify_cert.py and verify_cert2.py are pinned and
      did not run, and neither did its solver, regularizer or path test. The maintained
      routes share one parse, half-angle conversion and the separating-axis method, and all
      three share Fraction arithmetic. The kernel's controls are gross (RG-5). The source's
      statements that each side is the exact optimum of the store's best packing and that
      each view is the same packing traversable without expansion are not decided here;
      measured pose by pose, every view differs from the certificate the entry credits,
      and at 123, 129 and 292 only an optimal assignment pairs the squares (RG-3, RG-4).
      No private-worker custody is on file (RG-7), and the reviewer and the producer share
      a model family (RG-6). Finite feasibility only: no lower bound, optimum, local
      minimum, same-packing connectivity, rigidity, novelty or human oversight.
    source_reviewed: '2026-10-11'
  ```

- **On the reported entry** `E-evand-regularized-certificate-report`: an
  `external_review` naming this review, which makes it `reviewed`, and limitations that
  no longer say the review is pending (RG-8):

  ```yaml
    external_review:
      state: informally-verified
      date: '2026-10-11'
      reviewed_by: >-
        AI agent (Claude), the stage 4 review lane of the 2026-10-10 intake pass under
        think-8k76, prompted separately from the import lane
      note: >-
        docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md accepted
        all fifteen certificates for finite feasibility only, with eleven non-blocking
        findings (RG-1 to RG-11); the replay it reproduced is
        E-evand-regularized-exact-feasibility. The source's exact-optimum and same-packing
        statements are the source's, and at 123, 129 and 292 the arrangement's identity
        rests on them alone.
  ```

- **On T-146**: the confirming evidence, `V3`/`C3`, `activity` removed, the `reviews`
  entry, and `claim`, `notes`, `next_rung` and `significance` rewritten together.

  `claim`:

  > Fifteen complete rational certificates from Evan Daniel’s display-regularized record
  > lists, which no issue reports, prove finite upper bounds at their exact sides: s(70)
  > <= 8.880960371555579594785501178639, s(102) <= 10.605828696431578360490734944053,
  > s(103) <= 10.679232047361306442680936279997, s(123) <=
  > 11.591378145497698159550863183468, s(129) <= 11.872029849081179973752429831968,
  > s(146) <= 12.583782277415076881948309755914, s(153) <=
  > 12.872029849081179973762429831968, s(236) <= 15.863955747159267422617702706295,
  > s(258) <= 16.563448002133789379765816191273, s(263) <=
  > 16.733166007899378970679613144039, s(269) <= 16.901513582189132198548012552701,
  > s(292) <= 17.591378145497698159610863183468, s(295) <=
  > 17.704232790736030358056092972112, s(302) <= 17.872029849081179973812429831968 and
  > s(303) <= 17.913065462738532305839753791206.
  > 
  > Each certificate gives a rational side and, for each unit square, a rational centre
  > and the tangent of its half-angle, in Evan Daniel’s format, retained as the original
  > gzip the source publishes beside a JSON that prints the same side as S_cert. Each is
  > below every value the record held or had pending at its count when read, by 2.21e-17
  > at 302 to 7.82e-10 at 295.
  > 
  > All 45 retained jobs, the fifteen positives with their duplicate-square and
  > outside-container controls, were decided again here on 11 October 2026 by both
  > maintained exact routes and equal their retained rows, and a third exact route,
  > half-extent containment and exact intersection area, decided the fifteen with six
  > controls each, decompressing each retained gzip itself, and held each retained file
  > to its upstream bytes at the pin.
  > No route here is the source’s code, so the replay is independently re-implemented.
  > The 11 October review found no blocking defect.
  > 
  > Each side is below the ceiling its case holds; the case records are unchanged until
  > a house is adopted, so each is pending adoption.
  > 
  > The source presents each certificate as a display view and not a new bound.
  > Its method log says every refreshed side is the exact optimum of the store’s best
  > packing at its count, below the posted side only by rounding, and classes each of
  > the fifteen views as the same packing in a different arrangement, traversable
  > without expansion, by a path test that samples angle paths in 0.01 degree steps and
  > that it says is not a continuous proof; it reports all 324 certificates of the lists
  > VALID under its two exact checkers and verified at 80 digits.
  > Those statements are the author’s: no source program ran here, and the solved point
  > each view was made from is not published.
  > Measured pose by pose, every view differs from the certificate the record credits;
  > at 123, 129 and 292 nearest centres match under no symmetry and only an optimal
  > assignment pairs the squares, slid by up to 0.59, 0.83 and 0.59.
  > 
  > Credit the packings to their finders, as the source’s provenance names them: Ryan
  > Xu’s (ry-xu, https://github.com/ry-xu/square_packing, issue 432) at 70, 102, 103,
  > 123, 129, 146 and 295, at 103 as Mishapolk refined it (issue 470, T-138); Nate
  > Chaoweeraprasit’s SQUISH packing of issue 401 at 258, as Mishapolk refined it; and
  > his SQUISH packings of issue 481 (T-136) at 153, 236, 263, 269, 292, 302 and 303,
  > composed from pieces of Francisco Couzo’s, Ryan Xu’s and earlier packings.
  > At 70 Eric Deleeuw’s refinement of Ryan Xu’s packing in place (issue 483, T-137) was
  > the smallest side the record held.
  > Evan Daniel (https://github.com/evand/square-packing) refreshed each packing from
  > his store, solved it to the side he reports as its exact optimum, regularized it for
  > display at that side, at 70, 129, 153, 236, 263, 269 and 292 also merging determined
  > rotation groups by up to 2.96 degrees, and wrote the certificate.
  > His lists name the finders of the arrangements the packings descend from: Joe
  > DeVincentis at 70, Francisco Couzo at 102, 103, 123, 236, 263, 269, 292, 302 and
  > 303, David Ellsworth at 129 and 153 and David W. Cantrell at 146, and no one at 258
  > and 295. The source claims no record, and its credits say the repository’s work was
  > produced by Claude (Anthropic) under human direction.

  `notes`: the replay paragraph and the margins paragraphs of the draft stand as
  written. Replace the pose-by-pose paragraph with the measurement above: the best
  symmetry, the squares within 1e-9, moved beyond 1e-3 and 1e-1, the largest move and
  the turns, at each count, and the sentence that at 123, 129 and 292 the arrangement’s
  identity is the source’s statement alone (RG-3, RG-4). Replace the credit paragraph
  with the decision above, naming Ryan Xu at 70 with T-137 as the prior smallest side,
  unless the owner decides otherwise (RG-2). Replace “Pending this entry’s review, the
  house recommendation at its fifteen counts goes to it” with “The 11 October review
  recommends this entry as the house at all fifteen counts, crediting each packing as
  above; no house moves until jlevy/squares#403 lands and private-worker custody is on
  file (RG-7)”. Add: “V3 and C3 rest on the 11 October review
  (docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md) and the
  replay it reproduced (E-evand-regularized-exact-feasibility).
  Its findings here are non-blocking: the kernel’s controls are gross (RG-5), the
  reviewer and the producer share a model family (RG-6), and no private-worker custody
  is on file (RG-7).” Keep the closing sentence on the source’s checkers and the shared
  parse.

  `next_rung`:

  > V4 and C4 need a second accepted adversarial review of this replay by a distinct
  > reviewer and a retained human oversight record; the 11 October review is one, by an
  > AI agent. Separately, once jlevy/squares#403 lands and private-worker custody is on
  > file (RG-7), adopt this entry as the house at all fifteen counts, each earlier house
  > kept as history and each packing credited as the review decided (RG-2). Final
  > exact-head CI remains required.

  `significance`:

  ```yaml
    significance:
      score: 2
      rationale: >-
        Smaller finite construction sides at fifteen counts from 70 to 303, 2.21e-17 to
        7.82e-10 below the least side the record held or had pending at each and 5.36e-12
        to 9.28e-03 below the case ceilings, where the larger gaps are improvements SQUISH's
        issue 481 (T-136) already made: display-regularized arrangements at the sides the
        source reports as the exact optima of packings the record already credits, a
        citable detail of each case that moves no theorem, S2 as T-098 is; no lower bound,
        optimum or priority.
      scored: '2026-10-11'
      by: the 11 October review (docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md)
  ```

  `reviews`:

  ```yaml
    reviews:
      - path: docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md
        kind: adversarial
        reviewer: >-
          AI agent (Claude, at extra-high reasoning effort), the stage 4 review lane (W2) of
          the 2026-10-10 intake pass under think-8k76, prompted separately from the import
          lanes, with no shared context
        reviewer_kind: ai
        relation: project
        date: '2026-10-11'
        scope: >-
          Finite feasibility of the fifteen certificates the entry cites, at 70, 102, 103,
          123, 129, 146, 153, 236, 258, 263, 269, 292, 295, 302 and 303. The retained receipt
          replayed on both maintained routes, the third exact route with its sharp controls
          and its upstream check, a checker written for the review, every retained and
          pinned file held to its bytes fetched at the pin, each claim print held to the
          exact side, the claim comparison re-derived with the holders' sides read again,
          each route's trust boundary, and the credit of each certificate measured against
          the packing it would be credited to.
        verdict: accepted
        covers: [T-146]
  ```

  `artifacts` gains this review’s path, as T-140’s does.

- **In `verifiers.yaml`**: V-check-half-angle-area’s note gains this import, on which it
  ran as retained with its `regularized` roster and `--upstream`; V-upper-bound-reports’
  note gains this review.

- **In `source-coverage.yaml`**: the confirming evidence on the source entry, and its
  notes rewritten from “T-146 records them at V0/C0” to the derived rung (RG-8).

- **In `bibliography.yaml`**: `credit` and `short_credit` of
  `[Daniel regularized lists 2026-10-10]` as the owner decides on RG-2; the
  recommendation is `Daniel after Xu, Chaoweeraprasit, Mishapolk, Levy`.

- **In `document-map.yaml`**: this review as a retained record review, as the three
  earlier imports reviews are mapped.

- **On T-125, T-136, T-137 and T-138**: their notes’ “pending the review of T-146”
  sentences rewritten to say the review accepted it (RG-8).

## What This Review Does Not Establish

No optimality, lower bound, local minimum, same-packing connectivity, rigidity, novelty,
priority or human oversight.
No run of the source’s own checkers, solver, regularizer or path test.
No review of the lists’ other 314 certificates beyond the commit pin, of the alternates,
or of the atlas images.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
