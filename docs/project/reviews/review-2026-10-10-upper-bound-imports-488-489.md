# Review: Two Rational Upper-Bound Imports of 10 October (#488, #489)

**Date:** 10 October 2026. **Verdict: accepted, for finite feasibility only.** All ten
certificates the two imports’ register entries would cite prove the upper bounds their
packets state: Francisco Couzo’s six (#488, at 132, 175, 209, 237, 270 and 305) and Evan
Daniel’s four from Hunt 3 (#489, at 132 and 308 in the case corpus and at 343 and 344
beyond it). Both retained receipts reproduce here job for job on the two maintained
routes; the third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md) agrees
with them at every number they share; and every retained byte is the upstream file at
its pin, fetched here, the 54 Couzo certificates the packet pins as unchanged included.
The four certificates of the two commits that no entry cites, Hunt 3’s 305 and Couzo’s
303, 338 and 340, were decided here on all three routes as well.
Ten findings are recorded, none blocking.
Each entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` when its
confirming evidence entry and this review are added; neither can take `V4`/`C4` from
this review alone.

This review was written by an AI agent (Claude, at maximum reasoning effort), the stage
4 review lane of the 2026-10-10 intake pass, under think-fvz4, prompted separately from
the import lanes that built the two packets, with no shared context: lane W2 of
[result-import.md](../../../packing/campaign/result-import.md#stage-4-validate).
Its relation to the results is `project`. It moves no rung, writes no register row and
adopts no house; the proposed record changes are listed at the end for the records lane.

## Claims Covered

| Entry | Source | Counts the entry would cite | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #488 | [Francisco Couzo, #488](https://github.com/jlevy/squares/issues/488), `franciscouzo/square-packing` at `3ef7634` | 132, 175, 209, 237, 270, 305 | 12 places, each the exact side rounded up |
| T-NNN, #489 | [Evan Daniel, #489](https://github.com/jlevy/squares/issues/489), `evand/square-packing` at `c013f43`, retained at `76a529b` | 132, 308; 343 and 344 beyond the case corpus | 30 places, each the exact side printed in full |

The exact sides are the fractions each packet’s README tabulates and its claim record
freezes: #488’s six
([README](../../../packing/resources/web/couzo-certificates-2026-10-10/README.md)) and
#489’s four
([README](../../../packing/resources/web/evand-record-hunt3-2026-10-10/README.md)). The
same two commits hold four certificates no entry cites: Couzo’s at 303, 338 and 340,
changed by the same commit, and Hunt 3’s at 305, which issue #489 does not name and
whose exact side is #488’s side at 305. Each packet replays its uncited certificates in
its receipt and compares them in its claim record; this review decided them on the third
route as well, so that every certificate of the two commits has three routes.
The 54 Couzo certificates the pin holds unchanged since `02f9690` are the issue-476
packet’s and are outside this review except for custody.
Construction credit stays as the issues ask (below).

**Read in full.** `devtools.upper_bound_reports` and its two test modules; issues #488
and #489 as fetched on this date; the kernel `evand_arrangement_reports` (`run_case`,
`job_input`, `validate_job`, `validate_receipt`, `replay_receipt`); the parser and
conversion in `evand_exact_certificates` (`parse`, `Pose.basis`, `Pose.corners`,
`basis_witness`, `ceiling_decimal`); `sqpack.verify` and the materialization and
`exact_verify` of `sqpack.witness`; `check_rational_witness_independent`;
`acquire_source` (`acquire`, `check`, the `identical_to` rule); the third route
`devtools/check_half_angle_area.py` and its tests; both packet READMEs, custody and
import declarations, acquisition records, claim records and the beyond-horizon record;
the source’s certificate-format README (`search/exact/README.md`), licence and credits
as retained; the five retained Hunt 3 solver reports; the packer log and the two Couzo
READMEs at their pins, fetched here; the two earlier imports reviews;
[epistemics.md](../../../epistemics.md) on review records and rungs.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host at
a load average of 0.5 to 2.5, at most two worker processes, in a worktree of
`claude/determined-rubin-yjfy2a` at `9d993677b`, with nothing of the importer or the
routes changed. A replay decides every job of the selected counts again through both
maintained routes, serially in one process, and compares every field of each fresh job
with its retained row except the measured times.
The two replays ran as two processes at once, both starting at 19:03:31Z.

| Command (`python -m devtools.…`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `upper_bound_reports couzo-certificates-2026-10-10 check --replay` | #488’s 27 jobs, all nine replayed counts | all 27 equal | 390.1 s |
| `upper_bound_reports evand-record-hunt3-2026-10-10 check --replay` | #489’s 15 jobs, all five | all 15 equal | 308.7 s |
| `upper_bound_reports PACKET check-claims`, for each | each frozen comparison rebuilt from the certificates and the houses’ own packets | both rebuilt equal | 1.9 s and 0.7 s |
| `acquire_source PACKET --check`, for each | custody of both packets, the 54 and two `identical_to` twins compared | `PACKET_MATCHES_ITS_CONTRACT` | about 1 s each |
| `check_half_angle_area decide-imports --workers 2 --imports '#488' '#489' --upstream couzo-certificates-2026-10-10 DIR --upstream evand-record-hunt3-2026-10-10 DIR` | the third route on the ten cited certificates and their 60 controls, every cross-check, and the ten retained files against their fetched upstream bytes | no disagreement; 329,821 pairs | 14.7 s (15.1 s with the interpreter’s start) |
| a scratch driver of the same route’s functions | the four uncited certificates with 24 controls, each held to its retained positive job, and the two 305s measured against each other | all accepted and agreeing | 20.0 s |
| `pytest -n 2` on `test_upper_bound_reports_488_489.py` and the two #488/#489 tests of `test_check_half_angle_area.py`, the slow 305 test included; then `test_upper_bound_reports.py` at the two packets | 7 tests; 4 tests | all passed | 6.2 s; 4.9 s |

Each wall includes the interpreter’s start.
`DIR` is a scratch directory holding the source’s files at the pin (below).
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #488 | 27 | 1,899,504 | 388.00 | 393.15 | 25.21 |
| #489 | 15 | 1,319,598 | 308.35 | 409.47 | 43.27 |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Every certificate of both commits is in Evan Daniel’s text format: a
header `n S` and then, for each square, a rational centre $(x, y)$ and
$t = \tan(\theta/2)$, each an integer or a fraction with a power-of-ten denominator.
The bound $s(n) \le S$ follows from four facts, each decided by every route:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$, and the corners
   $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ form a unit square.
   `sqpack.verify.check_unit_squares` holds every edge to length 1 and every corner to a
   right angle; the independent checker holds the edges to unit length, orthogonality
   and closure; the third route holds $(c, s)$ to the unit circle.
2. **There are exactly $n$ of them.** `legacy.parse` refuses a header count that differs
   from the file name’s, fewer or more rows than $n$, and any literal that is not an
   integer, a fraction or a plain decimal (no exponent, sign prefix or blank); the third
   route’s parser refuses the same.
   The kernel holds every job to $n(n-1)/2$ pairs tested, so no bucketing or early exit
   can have skipped a pair.
3. **Each lies in the closed box $[0, S]^2$**: every corner has $0 \le x \le S$ and
   $0 \le y \le S$ on the maintained routes, or equivalently $h \le x \le S - h$ and
   $h \le y \le S - h$ with $h = (|c| + |s|)/2$ on the third.
4. **Interiors are pairwise disjoint**, by an edge normal that separates the two squares
   (the maintained routes) or by an intersection of area zero (the third route).

Arithmetic is exact `Fraction` arithmetic throughout: `exact_verify` decides a rational
witness with `_rational_sign`, the independent checker and the third route compare
fractions, and nothing rounds, dilates or tolerates.
A touching pair or a corner on a wall is a zero sign and is accepted; an overlap is a
negative sign and refused; a duplicated square overlaps itself.
A half-turn has no finite $t$ and needs none, since it is the same square; every other
angle has one, and $t = 0$ is exact axis alignment, which most of these squares have.

**The box convention does not matter here.** No square of any of the 14 certificates
touches a wall: both maintained routes and the third route find the least wall clearance
exactly $1/(2 \cdot 10^{20})$ at every count, and the third route counts zero wall
contacts.
That is the source’s construction as its format README states it, read here and
not run: the exact KKT configuration is scaled about the origin corner by
$1 + 10^{-20}$, its centres rounded to $10^{-35}$, and $S$ rounded up, so a square that
touched the origin walls now clears them by $\varepsilon/2$; at #488’s 132, square 2 has
$y = 1/2 + 5 \cdot 10^{-21}$ exactly.
The least separating-axis gap is just under $10^{-20}$ at every count, as the issues
state, and the least Euclidean distance between squares is $1.000000 \times 10^{-20}$ on
the third route.
So the closed squares are pairwise disjoint and strictly inside the open
box $(0, S)^2$ the two issues name, and each bound holds under any of the usual
conventions.

## Adapters and Admission

Both packets declare one format, `evand-cert`, and no derived fact; every certificate is
read by `legacy.parse` from the retained bytes, and by the third route’s own parser.
Comment lines, one per file, are not believed.

**Admission.** A certificate is admitted only where its exact side equals the printed
side or, printed in decimals, rounds up to it at the printed places.
#488’s six sides round up at 12 places to the sides the issue prints, and its three
uncited sides to the prints of the source’s `certificates/README.md` at the pin
(17.917365675353, 18.907150436394 and 18.939701150684), held to the fetched file.
#489’s four sides are printed in full: each denominator is $10^{30}$, or
$5^7 \cdot 10^{23}$ at 344, so each side terminates within 30 places and the issue’s
30-place print equals it.
Its uncited 305 rounds up at 12 places to the print in the message of `c013f43`
(17.951139772207), which the packet names as the place it is printed and which was read
here from the commit; the importer’s upstream check reads blob URLs only, so that print
is attested here and not by the route.
The third route’s own integer ceiling admits all ten cited sides against their prints,
and every plan claim states the exact side.

**What the adapters decide, and what they do not.** Every route decides in full the
packing it is handed, so a misreading cannot make a false bound pass.
What a misreading would break is attribution; that rests on custody, which the fetched
upstream bytes close below.

## Derived-Fact Custody

Neither packet keeps a derived fact: #488’s nine changed certificates are retained as
factual data under the owner decision of 9 October, the source stating no licence, and
#489’s five are retained under the MIT licence.
So the custody is of bytes, and `acquire_source.check` binds each retained file to its
Git blob at the pin and each pinned-only file to its recorded digest, comparing the
`identical_to` twins: the 54 unchanged Couzo certificates against the issue-476 packet’s
copies, and Hunt 3’s two checkers against the issue-399 packet’s. Both packets pass.

For this review every file of both manifests was fetched again, by read-only requests to
the GitHub contents API at the pinned commits, into scratch directories outside the
repository and read as data; nothing fetched was run:

- **#488, 74 files at `3ef7634`** (2,610,667 bytes): all 74 have the manifest’s digests;
  the nine retained certificates equal their upstream bytes; the 54 unchanged ones equal
  the issue-476 packet’s copies, so the `identical_to` rule holds against upstream and
  not only against the packet; the nine `n*.txt` pose files and the two READMEs match
  their pins. Each of the 63 SHA-256 prefixes `certificates/README.md` prints is the
  prefix of its file’s digest.
- **#489, 26 files at `76a529b`** (782,804 bytes): all 26 match; the 23 retained equal
  their upstream bytes; `verify_cert.py` and `verify_cert2.py` equal the issue-399
  copies; and the five certificates fetched at `c013f43`, the commit the issue names,
  are byte-identical to those at `76a529b`, whose commit changes only `PACKER.md` and
  `pk/pending.yaml`.

The dates the packets state were read from the commits: `3ef7634` was committed at
2026-10-10T13:52:27Z on `9bf90e7` (22:34:41Z the day before, which removes 102, 103 and
272); it adds `n209.cert` and modifies the other eight, so every retained byte of #488
was first committed there.
`f7a2325` (09:15:50Z) added `hunt3_n132.cert` and `hunt3_n344.cert`, which no later
commit touches; `c013f43` (13:46:56Z) replaced 305 and 308 and added 343; `76a529b` was
committed at 14:48:25Z. Issue #488 was filed at 14:08:32Z and #489 at 14:47:57Z, and
neither has been edited since.
The third route’s `--upstream` check held the ten cited retained files to the fetched
bytes (6 and 4 checks); the scratch comparison above covers the other four and the
pinned-only files.

**Licences and credit.** The Couzo tree at the pin has no licence file, and neither
README states reuse terms; `certificates/README.md` names Evan Daniel’s MIT-licensed
format, which licenses nothing of this bundle.
The prose and the pose files are pinned by digest only.
The Daniel tree carries `LICENSE` (MIT, copyright 2026 Evan Daniel) and `CREDITS.md`,
both retained; the credits file says the repository’s work was produced by Claude under
human direction. Issue #488 asks that the starting packings be credited: Nate
Chaoweeraprasit’s SQUISH packings of #481 at 209, 237, 270 and 305, Mishapolk’s at 132
(#470) and Ryan Xu’s at 175 (#432), improved by Evan Daniel’s `fq` (132, 175, 209, 237,
305), the author’s basin hopping (175, 270) and David Ellsworth’s `refine_packing` (132,
175, 270), with Evan Daniel’s exact contact solver writing all six; it discloses that
the search code and the request were written with Claude (Claude Code) under the
author’s direction. Issue #489 asks that 308, 343 and 344 be credited to Kevin Fang’s
construction of #484 (the two-wedge family of Arslanov, Mustafin and Shangitbayev), 344
his packing polished and moved by a corner-to-corner descent, 308 his packing polished
and moved seven explorer steps, 343 his 344 less one square in a different basin; 132 is
the author’s own lineage from #465; it discloses the same assistance.
Both packets’ declarations carry these statements as the sources give them.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; at #488 the issue states its author also ran this `verify.py` | the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `json`, `hashlib` | `Fraction` and the format’s meaning only |

`upper_bound_reports` owns custody, the adapter, admission, the claim comparison and the
job layout; the kernel owns the two controls and `validate_job`, which both maintained
routes are held to. The custody of the bytes rests on each packet’s own admission
(`acquire_source.check`), which the third route calls before it reads anything and from
which it decides nothing.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the sources’ own programs ran: Daniel’s `verify_cert.py` and `verify_cert2.py`
(pinned, not retained), his `exactsolve` and `fq`, Couzo’s basin hopping and copy of
`verify.py`, Ellsworth’s `refine_packing`. The KKT, multiplier, reduced-Hessian and
jamming statements of both issues are source reports and are not decided; the five
retained Hunt 3 solver reports state them (`n_zero` 31, 44, 52, 19 and 71 flat motions
at 132, 305, 308, 343 and 344; `lambda_A_maxmin` at least $1.8 \times 10^{-7}$ at the
four cited counts; `vv_milp_dS` 0), which is what the issue prints, and they were read,
not replayed. That a published file is the one its author meant is attested by the pins
only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing it, so it is not a clean-room implementation; it imports none of
their parsing or deciding code.
Here it was run as retained, with no change, since both packets use the one format it
already reads. On the ten cited certificates it decided 329,821 pairs, clipping 5,535,
and on the four uncited ones 206,696 more, clipping 2,778; it found no overlap and no
square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RD-2 of the first
replay review, carried as RI-3 and RK-8). `validate_job` requires both routes to refuse
each control, on the complete pair count, with the negative diagnostic it was built for:
a pair gap below zero for the duplicated square, a wall clearance below zero for the
square moved by $S + 2$. In both receipts the duplicate’s gap is exactly $-1$ at all 14
counts, and the moved square lies 3.00 to 15.77 units outside the box (15.77 at #488’s
175, whose first square sits at $x = 13.27$; 3.00 to 4.23 elsewhere), refusals a
binary64 checker with a $10^{-9}$ tolerance would also make.
They show the routes can refuse, not that they decide at the $10^{-20}$ scale where
these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance, just above $5 \cdot 10^{-21}$ | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All 84 reached their required outcome: 60 on the ten cited certificates and 24 on the
four uncited ones.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all ten cited sides and every centre and rotation equal the maintained routes’
  retained checker inputs, and so do the four uncited ones;
- every cited side equals the exact side of its packet’s frozen claim record and the
  value its register plan’s claim states, and is admitted against its print by the
  route’s own integer ceiling; the two uncited beyond-horizon sides of #488 are claimed
  by no plan, as they must be;
- every least wall clearance equals both maintained routes’ to every digit, exactly
  $1/(2 \cdot 10^{20})$ at all 14 counts;
- every least Euclidean distance, $1.000000 \times 10^{-20}$ at all 14, is at least the
  separating-axis gap both maintained routes report;
- the two receipts’ totals are the numbers the packets print, and the ten retained files
  are the fetched upstream bytes.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes each certificate against the case record
as it stood at `main` `af17208c0` and against every other report pending there, each
case ceiling rebuilt from its holder’s own retained packet; `check-claims` rebuilt both
equal, and `live_problems` finds #488’s declaration still reading the live records (RL-1
for #489’s). Every relation the two records state was also decided here exactly, with
every pending report’s exact side read from its own packet where one is retained (#476,
#481, #484, T-130, T-131), and none changes:

| n | #488 or #489 certificate, exact side rounded up at 16 places | Below the case ceiling by | Against the other pending reports, exactly |
| --- | --- | --- | --- |
| 132, #489 | 11.9856801988458089 | $5.65 \times 10^{-3}$ (T-098) | below #488 by $1.27 \times 10^{-3}$, #476 by $1.27 \times 10^{-3}$, T-131 by $1.42 \times 10^{-3}$, #470’s print by $1.28 \times 10^{-3}$: the smallest |
| 132, #488 | 11.9869535872544210 | $4.37 \times 10^{-3}$ (T-098) | below #476 by $6.06 \times 10^{-7}$, T-131 by $1.46 \times 10^{-4}$, #470’s print by $2.64 \times 10^{-6}$; above #489 |
| 175, #488 | 13.7671207246923133 | $1.78 \times 10^{-3}$ (T-125) | below T-130 and #476, one certificate, by $3.44 \times 10^{-5}$ and #470’s print by $3.44 \times 10^{-5}$: the smallest |
| 209, #488 | 14.9462232264464511 | $3.39 \times 10^{-3}$ (T-127) | below #481’s exact side by $4.28 \times 10^{-7}$ and #470’s print by $3.39 \times 10^{-3}$: the smallest |
| 237, #488 | 15.9029496076778317 | $7.27 \times 10^{-4}$ (T-127) | below #481 by $3.96 \times 10^{-5}$, #476 by $7.21 \times 10^{-4}$, #470’s print by $7.27 \times 10^{-4}$: the smallest |
| 270, #488 | 16.9297753535413596 | $8.03 \times 10^{-3}$ (T-119) | below #481 by $4.77 \times 10^{-6}$, #476 by $6.94 \times 10^{-3}$, T-130 by $6.95 \times 10^{-3}$, #470’s print by $6.95 \times 10^{-3}$: the smallest |
| 305, #488 | 17.9511397722069976 | $1.82 \times 10^{-3}$ (T-098) | below #481 by $5.64 \times 10^{-5}$; #476 equals the case; Hunt 3’s uncited 305 is this exact side |
| 308, #489 | 17.9982698795262559 | $1.73 \times 10^{-3}$ (the grid’s 18) | below #484 by $1.04 \times 10^{-3}$: the smallest |
| 343, #489 | 18.9782325236356113 | no case; $2.18 \times 10^{-2}$ below the grid’s 19 | below #484 by $1.67 \times 10^{-2}$; #470’s print, 19.000000000007, is above the grid |
| 344, #489 | 18.9944505142774016 | no case; $5.55 \times 10^{-3}$ below the grid | below #484 by $1.04 \times 10^{-3}$; #470’s print, 19.002369297056, is above the grid |

The issues’ own differences are these numbers at two digits: #488’s $4.3$, $4.0$, $4.8$,
$5.6 \times 10^{-7..-5}$ against #481 at 209, 237, 270 and 305, $6.1 \times 10^{-7}$
against #476 at 132 and $3.4 \times 10^{-5}$ against #460 at 175; #489’s $1.27$, $1.04$,
$16.7$ and $1.04 \times 10^{-3}$. Issue #488 quotes Mishapolk’s 132 as 11.986956226077;
the record compares the 12-place print of his README, 11.986956226066, which T-138
registered, and the certificate is below either.
The three uncited Couzo certificates: 303 is below its case (T-113) by
$2.95 \times 10^{-3}$ and below #476 by $7.83 \times 10^{-5}$, but above #481’s exact
side by $4.30 \times 10^{-3}$, and the source marks it superseded; 338 and 340 are below
the record’s tracked beyond-horizon rows, Couzo’s own decimal reports, by
$1.48 \times 10^{-3}$ and $1.78 \times 10^{-4}$, and below #476’s certificates by
$1.48 \times 10^{-3}$ and $4.67 \times 10^{-5}$ (RL-9).

**Two comparisons rest on prints where exact sides are retained** (RL-2). #488’s
declaration names #481 at 209, 237, 270, 303 and 305 by its 15-digit displays with
rounding `unstated`, the model RI-1 found the data does not fit at 270; the exact
relations above hold by at least $4.28 \times 10^{-7}$ against a span of
$2 \times 10^{-15}$. #489’s names #488 at 132 and 305 by its 12-place print, rounded up;
at 305 that print cannot decide between two equal sides, so the frozen record reports
`undecided_among` where the exact relation is a tie.
#488 names #489 by its 30-place display with rounding `unstated`; the display is the
exact side, so the $10^{-30}$ span is harmless.

**Whose arrangements these are.** For credit, the third route’s `arrangement_gap`
matched each certificate to the packing its issue says it started from, square to
nearest centre under the box’s eight symmetries, kept only where one to one.
A measurement, deciding nothing; the issues’ RMS figures were not reproduced.

| Certificate | Against | Best symmetry | Squares moved beyond $10^{-9}$ (beyond $10^{-3}$) | Largest move | Largest turn (sine) |
| --- | --- | --- | --- | --- | --- |
| #489, 305 (uncited) | #488, 305 | a quarter turn | 34 of 305 (19) | $1.77 \times 10^{-2}$ | $8.26 \times 10^{-4}$, 3 squares beyond $10^{-6}$ |
| #488, 209 | SQUISH’s #481 | a reflection | 177 (24) | $3.37 \times 10^{-2}$ | $9.18 \times 10^{-2}$ |
| #488, 237 | SQUISH’s #481 | a reflection and turns | 237 (122) | $3.00 \times 10^{-1}$ | $7.05 \times 10^{-2}$ |
| #488, 270 | SQUISH’s #481 | a reflection | 225 (34) | $6.42 \times 10^{-2}$ | $2.21 \times 10^{-2}$ |
| #488, 305 | SQUISH’s #481 | three quarter turns | 262 (63) | $1.84 \times 10^{-1}$ | $1.42 \times 10^{-1}$ |
| #488, 132 | #476, 132 | identity | 116 (48) | $3.94 \times 10^{-2}$ | $3.25 \times 10^{-2}$ |
| #489, 132 | #488, 132 | identity | 119 (118) | $1.87 \times 10^{-1}$ | $3.47 \times 10^{-1}$ |
| #489, 132 | T-131, 132 | identity | 122 (121) | $2.40 \times 10^{-1}$ | $4.26 \times 10^{-1}$ |
| #489, 308 | Kevin Fang’s #484 | identity | 308 (278) | $2.08 \times 10^{-1}$ | $5.83 \times 10^{-1}$ |
| #489, 344 | Kevin Fang’s #484 | identity | 344 (321) | $8.18 \times 10^{-2}$ | $4.28 \times 10^{-2}$ |
| #489, 343 | Kevin Fang’s #484 | no one-to-one matching under any symmetry |  |  |  |

The measurements are consistent with what the issues say and decide nothing about
priority.
The two 305s are one arrangement up to a quarter turn, 271 squares to $10^{-9}$
and the rest within the flat motions the Hunt 3 report lists (3 free squares, 44 exact
flat motions), with one exact side; #488’s 209, 237, 270 and 305 match SQUISH’s packings
square for square under a symmetry, with real rearrangement at 237 and 305; #489’s 132
is a different local minimum from #488’s and from T-131’s, as the issue states; its 308
and 344 are Fang’s arrangements moved, and its 343 is not Fang’s, in a different basin
as the issue says. #488’s 175 and 270 have no one-to-one matching with #476’s
certificates at those counts, which the packet does not claim.

## Findings

**RL-1, non-blocking: #489’s declaration no longer reads the live coverage register.**
Its claim record was frozen at `af17208c0`, before the records lane registered #484’s
343 and 344 as `verified` beyond-horizon rows (T-135). `live_problems` now asks for
those rows to be declared under their source id,
`fang-two-wedge-certificates-2026-10-10`, and the declaration names them as `#484`, at
the same printed values.
`check-claims` passes, since it compares and does not consult the live records;
`check-claims --write` would refuse.
The relations are unaffected.
When #489’s rows are registered, #484’s must be marked superseded in the same change,
since `current_beyond_horizon` refuses two current rows at one count; a refrozen record,
if one is wanted, needs the two rows renamed in the declaration first.

**RL-2, non-blocking: RI-1 recurs, twice.** #488 compares #481 by its displays although
#481’s exact sides are retained and registered (T-136), and the first imports review
advised a `HOUSES` reader for the next claim record; #489 compares #488 by its print
although #488’s packet was retained 43 seconds earlier in the same pass.
Neither changes a relation, but the 305 tie is left undecided where it is exact.
The importer has no reader for either packet, so the lanes could not name them without a
code change; the patch is proposed below, text only, and the records lane can state the
exact relations from this review meanwhile.

**RL-3, non-blocking: the 305 tie and its credit.** Hunt 3’s uncited 305 and #488’s 305
have one exact side, $8975569886103498772971256586313 / (5 \cdot 10^{29})$, and are one
arrangement up to a quarter turn; both descend from SQUISH’s #481 packing through `fq`,
as the packer log says.
Issue #488 was filed at 14:08:32Z; `c013f43` was committed at 13:46:56Z but, by the
packer log at `76a529b`, pushed after #488 was filed, and #489 does not claim 305 and
its log gives it to Couzo.
The record should keep 305 under #488 and cite the Hunt 3 certificate nowhere, as the
packets do; if it is ever cited, it is an equal-side confirmation and no improvement.

**RL-4, non-blocking: the kernel’s controls are gross** (RD-2, RI-3, RK-8, unchanged).
Carrying the third route’s sharp kinds into the kernel would make each packet’s own
replay show exactness.

**RL-5, non-blocking: at #488 one maintained route is the producer’s checker.** The
issue states that all six are valid under this repository’s `verify.py`, so at #488
V-sqpack-verify reproduces with the producer’s code, as at T-128, T-130 and #476 (RD-4,
RI-4), and the independently re-implemented relation rests on
V-check-rational-witness-independent and the third route.
At #489 the producer’s checkers are `verify_cert.py` and `verify_cert2.py`, and no
maintained route is theirs.

**RL-6, non-blocking for this claim: no private-worker custody at either packet** (RI-5,
RK-10). The rung for finite feasibility does not need it; the adoption round should
close it before any house moves.

**RL-7, non-blocking: #489’s 343 and 344 lie beyond the case corpus.** Its register
entry can cite only 132 and 308. The two dated beyond-horizon rows its plan writes can
take `assurance: verified` from the same evidence, keeping their printed values byte for
byte, as RI-6 did for #484; they replace rows that are themselves verified, so a
`reported` row would step the register down.
Each print is the exact side, so each is itself a proved bound.

**RL-8, non-blocking: the reviewer and both producers share a model family.** Both
issues disclose that their search code and requests were written with Claude under the
authors’ direction, the two source repositories’ commits name an AI assistant as
co-author, and this review and the third route are Claude’s. The decisions are exact and
do not depend on judgment, and the two maintained routes predate these imports, but an
error of method common to the family would not be independent across them.
`V4`/`C4` needs a second adversarial review by a distinct reviewer in any case.

**RL-9, non-blocking, for the owner: #488’s three uncited certificates.** By the import
rules each is an import of its own and no entry registers it.
303 is superseded by T-136’s exact side and the source says so.
338 and 340 are exact certificates, replayed in the receipt and decided here on all
three routes, below the record’s tracked rows (Couzo’s own decimal reports, `reported`)
by $1.48 \times 10^{-3}$ and $1.78 \times 10^{-4}$. The owner may adopt them as verified
beyond-horizon rows from this evidence, which proves them, or leave the rows until a
request names them.

**RL-10, non-blocking, cosmetic: the register plan prints “1 further certificates” for
#489.** `register_plan` uses `_many` elsewhere but not in that sentence of the notes;
the records lane rewrites the notes in any case, and the four claim statements and every
number the plan prints are right.

## Rungs

**#488: `V3`/`C3`** at 132, 175, 209, 237, 270 and 305. Machine-replayed here: all nine
certificates of the replayed roster and their 18 kernel controls on both maintained
routes, and the six with their 36 controls on the third route, with a certificate, a
replay command, a passing replay and retained controls; reviewed adversarially here.

**#489: `V3`/`C3`** at 132 and 308, for the same reasons over five certificates, ten
kernel controls and 24 third-route controls; 343 and 344 are verified beyond-horizon
rows, not register scope.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Adoption per Count

The smallest exact certificate at each count these two imports touch, against the case’s
verified ceiling at `main` `af17208c0` and every report pending on 2026-10-10, merged
with the
[trio126 review’s table](review-2026-10-10-upper-bound-imports-470-and-trio126.md#adoption-per-count),
whose rows at 132, 175, 209, 237, 270, 303, 305 and 308 this table replaces; its other
rows stand. Every comparison is exact except with #470, whose 12-place values are
compared as the upward roundings they state.
Sides are shown rounded up at sixteen places, #470’s as printed.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | #470 | House to adopt |
| --- | --- | --- | --- | --- |
| 132 | 11.9913278876915015, T-098 | #489, 11.9856801988458089; #488, 11.9869535872544210; #476, 11.9869541936403928; T-131, 11.9870993322450633 | 11.986956226066 | #489, Evan Daniel’s own lineage from #465; #488’s stays verified, crediting Mishapolk’s packing as its start, then #476 and T-131 |
| 175 | 13.7688992766137689, Ryan Xu (T-125) | #488, 13.7671207246923133; T-130 and #476, one certificate, 13.7671551635425492 | 13.767155163551 | #488, crediting Ryan Xu’s packing as its start; T-130’s stays verified |
| 209 | 14.9496179522003981, Gupta (T-127) | #488, 14.9462232264464511; #481, 14.9462236544879195 | 14.949617952201 | #488, crediting SQUISH’s packing as its start; #481’s stays verified |
| 237 | 15.9036762351891381, Gupta (T-127) | #488, 15.9029496076778317; #481, 15.9029892208749656; #476, 15.9036709055806231 | 15.903676235190 | #488, crediting SQUISH’s packing as its start; then #481, then #476 |
| 270 | 16.9378072284460292, Daniel (T-119) | #488, 16.9297753535413596; #481, 16.9297801262411717; #476, 16.9367200311210158; T-130, 16.9367230228761835 | 16.936723155038 | #488, crediting SQUISH’s packing as its start; then #481, #476, T-130 |
| 303 | 17.9203123729203498, SQUISH (T-113) | #481, 17.9130654627385328; #488’s uncited 303, 17.9173656753523603; #476, 17.9174439254942359 | 17.920312372919 | #481, as before; the uncited 303 is cited by no entry |
| 305 | 17.9529594590155280, T-098 | #488, 17.9511397722069976, which Hunt 3’s uncited 305 equals; #481, 17.9511961441473858; #476 equals the case | none | #488, crediting SQUISH’s packing as its start; #481’s stays verified |
| 308 | 18, the grid (`E-basic-grid-upper`) | #489, 17.9982698795262559; #484, 17.9993098551627480 | none | #489, crediting Kevin Fang’s construction as the author asks; #484’s stays verified |

“Gupta (T-127)” is SQUISH’s packing refined by Siddharth Gupta, and T-098 Evan Daniel’s
exact optimum of Francisco Couzo’s packing.
Beyond the corpus there is no house: at 343 and 344 the record’s rows move from #484’s
18.9949035292204970 and 18.9954892754308151 to #489’s 18.9782325236356113 and
18.9944505142774016 (RL-7); at 338 and 340 the rows stay Couzo’s decimal reports unless
the owner adopts the uncited certificates (RL-9). Credit follows the issues.
At every count the earlier house stays retained as history, and the case’s reported and
verified ceilings move together.
House adoption waits for [#403](https://github.com/jlevy/squares/pull/403), which
rewrites every case record, as the coordinator recorded on `think-fvz4`, and for
private-worker custody (RL-6).

## Proposed Record Changes

For the records lane; this review writes none of them.
`T-NNN-488` and `T-NNN-489` stand for the ids it assigns.

- **A confirming evidence entry per import**: `E-couzo-488-exact-feasibility` and
  `E-evand-489-exact-feasibility`, each `assurance: verified`,
  `method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s certificate
  directory as `certificate`, the replay commands above with their walls (390.1 s and
  308.7 s; the third route 14.7 s), `replay_status: passed`, verifiers V-sqpack-verify,
  V-check-rational-witness-independent, V-evand-arrangement-receipts,
  V-upper-bound-reports and V-check-half-angle-area, this review as
  `independence_record` and as `external_review` (`informally-verified`), and
  limitations naming the shared premises, RL-4, RL-5 at #488, RL-6 and RL-8. The scope
  of #489’s is 132, 308, 343 and 344; its limitations should say that 305 is replayed in
  the receipt and cited by no entry (RL-3).

- **On each reported entry** (`E-couzo-488-certificate-report`,
  `E-evand-489-hunt3-report`): `external_review` naming this review, which makes it
  `reviewed`.

- **On each register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, `covers` both), both test files among the
  controls, and claim, notes and `next_rung` rewritten together as T-134’s were, each
  claim stating its bounds as the register plan writes them.
  #488’s notes should state the exact relations to #481 from the table above, and the
  305 tie; #489’s should say that 305 is Couzo’s by the source’s own account.

- **Two verifier entries**: V-check-half-angle-area’s note gains these two imports, on
  which it ran as retained; V-upper-bound-reports’ note gains this review.

- **In `source-coverage.yaml`**: #489’s rows at 343 and 344 at `assurance: verified`,
  #484’s two rows marked superseded in the same change (RL-1, RL-7), and the confirming
  evidence on each import’s source entry.

- **The `HOUSES` readers (RL-2), proposed and not made here.** In
  `devtools/upper_bound_reports.py`, beside `_couzo_476`:

  ```python
  def _squish_481(n: int) -> Fraction:
      return read_facts(packet_path("squish-481-third-request-2026-10-09"))[n].side


  def _couzo_488(n: int) -> Fraction:
      return read_facts(packet_path("couzo-certificates-2026-10-10"))[n].side
  ```

  registered in `HOUSES` as `"[SQUISH third request 2026-10-09]": _squish_481` and
  `"[Couzo certificates 2026-10-10]": _couzo_488`. Then #488’s declaration names #481 at
  209, 237, 270, 303 and 305 by `"reader": "[SQUISH third request 2026-10-09]"` with
  `"result": "T-136"` in place of `printed` and `rounding`, #489’s names #488 at 132 and
  305 by `"reader": "[Couzo certificates 2026-10-10]"`, and `check-claims --write`
  refreezes both records, after RL-1’s renaming; at 305 the record then reads `tied`.
  Every relation stays as this review decided it.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the sources’ own checkers or solvers.
No review of #488’s 54 unchanged certificates beyond their custody, of the pose files,
or of the packer log beyond its lines on 305. No house adoption, case-record change or
private-worker custody.

## Note of 10 October 2026: the Register Ids

Added by records lane R3 of the same intake pass (`think-fvz4`); the review above is
unchanged. The entries this review calls `T-NNN-488` and `T-NNN-489` are `T-140` and
`T-141`, each taken in the commit that first registered it at `V0`/`C0` and raised to
`V3`/`C3` with the confirming evidence this review proposes:
`E-couzo-488-exact-feasibility` and `E-evand-489-exact-feasibility`. `T-141` cites 132
and 308; 343 and 344 are verified beyond-horizon rows, and #484’s rows there are marked
superseded in the same change (RL-1, RL-7). The `HOUSES` readers of RL-2 cover the
issue-481, issue-484, issue-488 and issue-489 packets, both declarations name those
reports by `reader` and `result`, and both claim records were refrozen, so the 305
comparison reads as an exact tie.
Hunt 3’s 305 is cited by no entry (RL-3), and Couzo’s 338 and 340 stay compared and
uncited for the owner (RL-9). No case record changed: house adoption waits for
jlevy/squares#403, so each confirming entry is a recorded deferral of its case citation.
Ids are provisional until merged to `main`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
