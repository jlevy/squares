# Review: Francisco Couzo’s Eleven Rational Upper-Bound Imports of 11 October (#506)

**Date:** 12 October 2026, for the intake pass of 11 October.
**Verdict: accepted, for finite feasibility only.** The eleven certificates the import’s
register entry and its nine beyond-horizon rows would cite prove the upper bounds its
packet states: Francisco Couzo’s exact optima at n = 304 and 305, inside the case
corpus, and at 338, 339, 344, 376, 378, 379, 380 and 381 beyond it, with the rational
witness at 375. The third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended to this packet, decided all eleven here and agrees with both maintained routes
at every number they share; the retained receipt reproduces here job for job at the four
counts replayed, and the import lane’s own complete replay stands for the rest; every
retained byte and every pinned file of the manifest is the upstream file at its pin,
fetched here. The comparison with SQUISH’s #500 at 304 and 305, which the import froze
against the issue’s 15-digit prints, was refrozen here against the #500 packet’s exact
sides, and no relation changed.
The lineage the issue states was measured where the record retains the parent.
Twelve findings are recorded, none blocking.
The entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` at 304
and 305 when its confirming evidence entry and this review are added, and the nine
beyond-horizon rows can take `assurance: verified` from the same evidence; neither can
take `V4`/`C4` from this review alone.
At 304 and 305 the house is this release, crediting #500’s packings as its starting
points.

This is the stage 4 review lane (W2, V4) of the 2026-10-11 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-720n`, written by an AI agent (Claude Fable 5.1 at extra-high reasoning effort, a
different model from the import lane’s) prompted separately from the import lane that
built the packet (`think-om5l`), with no shared context beyond its committed notes and
register plan. Its relation to the result is `project`. It moves no rung, writes no
register row and adopts no house; the proposed record changes are listed at the end for
the records lane.

## Claims Covered

| Entry | Source | Counts | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #506 | [Francisco Couzo, #506](https://github.com/jlevy/squares/issues/506), `franciscouzo/square-packing` at `337078c` | 304, 305 in the corpus; 338, 339, 344, 375, 376, 378, 379, 380, 381 beyond it | 12 places, each the exact side rounded up |

The exact sides are the fractions the packet’s README tabulates and its claim record
freezes
([README](../../../packing/resources/web/couzo-certificates-2026-10-11/README.md)); the
register plan’s claim states all eleven, each terminating side printed in full and the
375 as a fraction, and the third route holds each plan claim equal to the exact side.
The same two commits hold four certificates the issue does not name, at 175, 308, 340
and 343, each an import of its own: the packet replays and compares them, and this
review decided them on the third route in scratch (below) and registers none.
The 53 certificates the pin holds unchanged since `3ef7634` are the issue-476 and
issue-488 packets’ and are outside this review except for custody.

**Read in full.** The import lane’s commits `80f4a3708` and `0df40a7db`: the packet’s
README, declaration, acquisition record, manifest and both claim records, the fifteen
retained certificates, the whole receipt as the kernel admits it, the `HOUSES` reader
and the tests; its bead notes and register plan; issue #506 as fetched here on
2026-10-12 at 01:13Z (filed 2026-10-11T18:06:50Z, not edited since, no comments); the
pinned `certificates/README.md`, `README.md` and the fifteen `nN.txt` pose files,
fetched here; the [#500 review](review-2026-10-11-upper-bound-imports-500.md), whose
RX-6 this review closes, and the
[#488/#489 review](review-2026-10-10-upper-bound-imports-488-489.md), the closest
precedent for a retained Evan Daniel-format release with beyond-horizon rows; the third
route and its tests; `check_source_coverage`’s beyond-horizon rules;
[epistemics.md](../../../epistemics.md) on review records and significance.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 3 to 8, one worker process throughout, in a
worktree of the V3 branch (`claude/wizardly-meitner-wqn4x3-imports` at `0ec1173c5` with
Lane A’s #500 packet and the #500 review) with the import lane’s `0df40a7db` merged and
this review’s changes to the declaration and the third route added.
A replay decides every job of the selected counts again through both maintained routes,
serially in one process, and compares every field of each fresh job with its retained
row except the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`, `PACKET` = `couzo-certificates-2026-10-11`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `PACKET check-claims --write`, after the declaration names #500 by its reader | the frozen comparison refrozen from the certificates and the holders’ own packets, #500’s included, then rebuilt and held equal | written, rebuilt equal, exit 0 | 9 s |
| `PACKET check --n 304 305 --replay` | 6 jobs at the two in-corpus counts: each positive, its duplicate-square and its outside-container control | all 6 equal, exit 0 | 305.1 s |
| `PACKET check --n 344 --replay` | 3 jobs at the count whose current row is verified | all 3 equal, exit 0 | 208.7 s |
| `PACKET check --n 381 --replay` | 3 jobs at the largest count | all 3 equal, exit 0 | 282.6 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#506' --upstream PACKET DIR` | the third route on all eleven requested certificates and 66 controls, every cross-check, four arrangement and three lineage measurements, and each retained certificate against its upstream bytes | no disagreement, exit 0 | 317.8 s (318.9 s with the interpreter’s start) |

The refreeze ran 01:17:14Z to 01:17:23Z, the replays 01:12:44Z to 01:26:00Z and the
third route 01:18:40Z to 01:23:59Z, all on 2026-10-12. Each wall includes the
interpreter’s start.
`DIR` is a scratch directory outside the repository holding the source’s files at the
pin (below).

**What was not replayed here, and why.** The 21 kernel jobs at 338, 339, 375, 376, 378,
379 and 380 and the 12 at the four unrequested counts were not decided again by this
review: the brief set the beyond-horizon replay, 75 minutes serially under load in the
import lane, aside and asked for 344 and 381 of the nine.
For those counts the record rests on the import lane’s two complete decisions of every
job, `certify --workers 1` (42 jobs from 20:39Z on 2026-10-11, the three at 381 by the
same `decide-job` command after the session’s background limit, assembled by
`certify --finished`) and its own serial `check --n N --replay` once per count (all 45
equal, 4,516 s summed), and on the third route here, which decided all eleven requested
certificates in full and held each one’s side, every pose and both margins to the
receipt’s rows. So every requested certificate was decided here by at least one exact
route, and every retained job was decided twice by the import lane; the confirming
evidence should cite both runs (RY-8).

The receipt’s own totals, recomputed by the third route, are the numbers the packet
prints:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #506 | 45 | 5,234,106 | 2,540.17 | 5,568.25 | 287.72 (the positive at 379) |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Every certificate of the commit is in Evan Daniel’s text format: a
header `n S` and then, for each square, a rational centre $(x, y)$ and
$t = \tan(\theta/2)$, each an integer or a fraction.
The bound $s(n) \le S$ follows from four facts, each decided by every route:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$, and the corners
   $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ form a unit square.
   `sqpack.verify.check_unit_squares` holds every edge to length 1 and every corner to a
   right angle; the independent checker holds the edges to unit length, orthogonality
   and closure; the third route holds $(c, s)$ to the unit circle.
2. **There are exactly $n$ of them.** `legacy.parse` refuses a header count that differs
   from the file name’s, fewer or more rows than $n$, and any literal that is not an
   integer, a fraction or a plain decimal; the third route’s parser refuses the same.
   The kernel holds every job to $n(n-1)/2$ pairs tested, so no bucketing or early exit
   can have skipped a pair.
3. **Each lies in the closed box $[0, S]^2$**: every corner has $0 \le x \le S$ and
   $0 \le y \le S$ on the maintained routes, or equivalently $h \le x \le S - h$ and
   $h \le y \le S - h$ with $h = (|c| + |s|)/2$ on the third.
4. **Interiors are pairwise disjoint**, by an edge normal that separates the two squares
   (the maintained routes) or by an intersection of area zero (the third route).

Arithmetic is exact `Fraction` arithmetic throughout; nothing rounds, dilates or
tolerates. A touching pair or a corner on a wall is a zero sign and is accepted; an
overlap is a negative sign and refused; a duplicated square overlaps itself.

**The box convention does not matter here.** No square of any of the eleven touches a
wall: both maintained routes and the third route find the least wall clearance exactly
$1/(2 \cdot 10^{20})$ at the ten exact optima and exactly $10^{-15}$ at the witness, and
the third route counts zero wall contacts at every count.
At the exact optima that is Evan Daniel’s construction as his format README states it,
read here and not run: the exact KKT configuration scaled about the origin corner by
$1 + 10^{-20}$, its centres rounded to $10^{-35}$ and $S$ rounded up, so the least
separating-axis gap is just under $10^{-20}$ and the least Euclidean distance
$1.000000 \times 10^{-20}$. At 375 the witness is the decimal packing dilated, measured
under The Rational Witness below.
So the closed squares are pairwise disjoint and strictly inside the open box $(0, S)^2$
the issue names, and each bound holds under any of the usual conventions.

| n | Least wall clearance (all three routes) | Least pair gap (both maintained routes) | Least Euclidean distance (third route) | Wall contacts (third route) |
| --- | --- | --- | --- | --- |
| 304, 305, 338, 339, 344, 376, 378, 379, 380, 381 | $1/(2 \cdot 10^{20})$ exactly | just under $10^{-20}$ | $1.000000 \times 10^{-20}$ | 0 |
| 375 | $10^{-15}$ exactly | $7.047 \times 10^{-12}$ | $7.047473 \times 10^{-12}$ | 0 |

## Adapters and Admission

The packet declares one format, `evand-cert`, and no derived fact; every certificate is
read by `legacy.parse` from the retained bytes, and by the third route’s own parser.
The one comment line of each file is not believed.

**Admission.** A certificate is admitted only where its exact side equals the printed
side or, printed in decimals, rounds up to it at the printed places.
All eleven requested sides round up at 12 places to the sides the issue prints, and the
four unrequested ones to the prints of the source’s `certificates/README.md` at the pin,
held here to the fetched file.
The third route’s own integer ceiling admits all eleven against their prints, and every
plan claim states the exact side; the frozen claim record prints each side rounded up at
16 places, and the third route’s ceiling agrees at all eleven.

**What the adapters decide, and what they do not.** Every route decides in full the
packing it is handed, so a misreading cannot make a false bound pass.
What a misreading would break is attribution; that rests on custody, which the fetched
upstream bytes close below.

## Custody

The source states no licence, so the fifteen changed certificates are retained as
factual data under the owner decision of 9 October, and the custody is of bytes:
`acquire_source.check` binds each retained file to its Git blob at the pin and each
pinned-only file to its recorded digest, comparing the 53 `identical_to` twins against
the issue-476 and issue-488 packets’ copies.
The packet passes.

For this review every file of the manifest was fetched again, by read-only requests to
`raw.githubusercontent.com` at `337078ca3e05153aceb099237b175cf64af5748a`, into a
scratch directory outside the repository and read as data at 01:14Z on 2026-10-12;
nothing fetched was run.
All 85 files, 3,066,594 bytes, have the manifest’s digests (`sha256sum -c`, 85 of 85):
the fifteen retained certificates equal their upstream bytes, the 53 unchanged ones
match the digests under which the earlier packets retain them, and the two READMEs and
fifteen pose files match their pins.
The third route’s `--upstream` check then held the eleven requested retained files to
the fetched bytes (11 checks).
Each of the 68 SHA-256 prefixes `certificates/README.md` prints is the prefix of its
file’s digest, as the import lane found; the eleven requested sides and twelve-place
prints in that table were read against the issue’s here.

The dates the packet states were read from the issue and the import lane’s record of the
commits: `337078c` was committed at 2026-10-11T17:29:19Z on `f311f08` (03:39:54Z); the
issue was filed at 18:06:50Z and has not been edited.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; the issue states its author also ran this `verify.py` | the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `json`, `hashlib` | `Fraction` and the format’s meaning only |

`upper_bound_reports` owns custody, the adapter, admission, the claim comparison and the
job layout; the kernel owns the two controls and `validate_job`, which both maintained
routes are held to. The custody of the bytes rests on the packet’s own admission
(`acquire_source.check`), which the third route calls before it reads anything and from
which it decides nothing.

**One maintained route is the producer’s checker** (RY-4, as RL-5 at #488). The issue
states that all eleven are valid under this repository’s `verify.py` and under Evan
Daniel’s `verify_cert.py`, so V-sqpack-verify reproduces with code the producer ran, and
the independently re-implemented relation rests on V-check-rational-witness-independent
and the third route, both of which the source did not run.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the sources’ own programs ran: Daniel’s `verify_cert.py`, `exactsolve` and `fq`,
Couzo’s basin hopping, LP and copy of `verify.py`, Ellsworth’s `refine_packing`. That
ten certificates are exact optima of their arrangements (KKT points to about $10^{-19}$,
the certificates README says) is a source report and is not decided; this review decides
feasibility only. That a published file is the one its author meant is attested by the
pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing it, so it is not a clean-room implementation; it imports none of
their parsing or deciding code.
Here it was run on the packet through a roster entry (`IMPORTS_506`) and its existing
parser of this format, with no change to any decision.
On the eleven certificates it decided 693,565 pairs, clipping 8,885, and found no
overlap and no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3, carried as
RY-5). `validate_job` requires both routes to refuse each control, on the complete pair
count, with the negative diagnostic it was built for.
In the receipt the duplicate’s gap is exactly $-1$ at all fifteen counts, and the moved
square, carried by $S + 2$, lies at least two units outside the box, refusals a binary64
checker with a $10^{-9}$ tolerance would also make.
They show the routes can refuse, not that they decide at the $10^{-20}$ scale where
these certificates live.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance, $5 \cdot 10^{-21}$ or, at 375, $10^{-15}$ | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All 66 reached their required outcome.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all eleven sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- every side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against the issue’s print by the route’s
  own integer ceiling;
- every least wall clearance equals both maintained routes’ to every digit;
- every least Euclidean distance is at least the separating-axis gap both maintained
  routes report;
- the receipt’s totals are the numbers the packet prints, and the eleven retained files
  are the fetched upstream bytes.

## The Rational Witness at 375

The issue says the 375 is “the decimal packing with centres dilated by 1 + 1e-11”; the
source’s `certificates/README.md`, describing every rational witness, says “centres
scaled apart by 1+1e-12”. The import lane noted the discrepancy and that the side excess
fits $10^{-11}$. Measured here, in scratch and not retained, from the retained
certificate and the pose file `n375.txt` fetched at the pin (377 rows of 17-digit
binary64 decimals, `# s = 19.906335144819391`):

- every centre of the certificate is the pose file’s scaled by $1 + 10^{-11}$ about the
  point $(\tfrac12, \tfrac12)$, to within $4.8 \times 10^{-15}$ at the worst coordinate
  (median $10^{-15}$, the pose file’s own print resolution); scaling about the origin
  leaves a residual of exactly $5 \times 10^{-12}$ at every coordinate, and
  $1 + 10^{-12}$ about either point leaves residuals up to $1.7 \times 10^{-10}$;
- the side exceeds the printed decimal by $1.890649 \times 10^{-10}$, which is
  $10^{-11}(S - 1)$ to seven digits, and the least far-wall clearance is exactly
  $10^{-15}$, so the side was rounded up at 15 places above the farthest edge;
- every rotation agrees with the pose file’s $\theta$ to $5.2 \times 10^{-11}$ radians,
  the conversion of a 17-digit decimal to $t$ and back.

So the certificate is what the issue says, with the scaling centred on the first
square’s centre rather than the origin, and the README’s general description does not
describe it (RY-2). None of this bears on the bound: every route decides the certificate
as written, and the dilation is why its pair gap, $7.047 \times 10^{-12}$, is far above
the $10^{-20}$ of the exact optima.

## The Claims Comparison

The packet’s `acquisition/claims.json` was frozen by the import lane against the case
record as it stood at `main` `3a5a91a90` and against every register entry and report
pending there, each side rebuilt from its holder’s own retained packet, except #500,
which had no packet when the lane read the issue and was compared at the 15 places its
issue prints with rounding `unstated`. The #500 review found those prints to be the
exact sides cut, so the comparison was a span (RX-6). For this review the declaration
names #500 at 304 and 305 by the reader of the `squish-500-fourth-request-2026-10-11`
packet (`[SQUISH fourth request 2026-10-11]`, on this branch since the import lanes
merged), and `check-claims --write` refroze the record after holding the declaration to
the live records (`live_problems` empty): the two #500 rows now carry #500’s exact
fractions and exact differences, and nothing else in either claim record changed (RY-1).
The register plan is byte-identical before and after, since it prints margins at two
digits. Every relation the record states was also decided here exactly, with every
pending report’s exact side read from its own packet, and the beyond-horizon rows at
their printed values.
Sides are shown rounded up at sixteen places; every margin is the other side less this
one, cut at four digits.

| n | Case ceiling, house | This certificate | Pending at the count, exact unless printed | Margin to each | Smallest |
| --- | --- | --- | --- | --- | --- |
| 304 | 17.9346500183906818, Couzo improved by Daniel (T-098) | 17.9295659468485010 | #500 17.9296570421708801; #476 equals the ceiling | case $5.084 \times 10^{-3}$; #500 $9.109 \times 10^{-5}$ | this |
| 305 | 17.9529594590155280 (T-098) | 17.9504664821377123 | #500 17.9505448539256365; T-140 17.9511397722069976 and #489’s tie of it; T-136 17.9511961441473858; #476 equals the ceiling | case $2.492 \times 10^{-3}$; #500 $7.837 \times 10^{-5}$; T-140 and #489 $6.732 \times 10^{-4}$; T-136 $7.296 \times 10^{-4}$ | this |

Beyond the corpus there is no case record; each side is compared with the grid, with the
beyond-horizon row the source register tracks as current, and with every retained
certificate there. The current rows are Couzo’s own decimal reports (`reported`) except
at 344, where it is Evan Daniel’s Hunt 3 side, `verified` and printed in full:

| n | This certificate | Current row, printed as the register holds it | Below it by | Other reports, below each by |
| --- | --- | --- | --- | --- |
| 338 | 18.9064365005518260 | 18.908632939046573, Couzo (`couzo-extended-range-reports-2026-10-08`) | $2.196 \times 10^{-3}$ | #488 $7.139 \times 10^{-4}$; #476 $2.196 \times 10^{-3}$ |
| 339 | 18.9294338838076622 | 18.930103647693699, Couzo (same) | $6.697 \times 10^{-4}$ | #476 $6.697 \times 10^{-4}$ |
| 344 | 18.9943532449434424 | 18.994450514277401521114135796864, Daniel, Hunt 3 (`evand-record-hunt3-2026-10-10`), verified | $9.726 \times 10^{-5}$ | #484 (Fang) $1.136 \times 10^{-3}$; #470’s print 19.002369297056, $8.016 \times 10^{-3}$ |
| 375 | 19.9063351450084560 | 19.907024692022954, Couzo (`couzo-extended-range-updates-2026-10-08`) | $6.895 \times 10^{-4}$ | #476 $6.466 \times 10^{-4}$ |
| 376 | 19.9102765868845442 | 19.920279652318701, Couzo (`couzo-extended-range-reports-2026-10-08`) | $1.000 \times 10^{-2}$ | #476 $1.000 \times 10^{-2}$ |
| 378 | 19.9425417773548106 | 19.946861170999796, Couzo (`couzo-extended-range-updates-2026-10-08`) | $4.319 \times 10^{-3}$ | #476 $3.919 \times 10^{-3}$ |
| 379 | 19.9535727095385746 | 19.957538882118669, Couzo (`couzo-extended-range-reports-2026-10-08`) | $3.966 \times 10^{-3}$ | #476 $3.966 \times 10^{-3}$ |
| 380 | 19.9874407665553876 | none | the grid’s 20, $1.255 \times 10^{-2}$ |  |
| 381 | 19.9926632884635649 | none | the grid’s 20, $7.336 \times 10^{-3}$ |  |

Each requested side is the smallest the record holds or has pending at its count.
The issue’s own “below it by” column is these numbers at two digits at 304, 305 and 344;
at the other seven it quotes the author’s own latest earlier certificate, which is not
the row the register tracks (RY-3): `3ef7634`’s at 338 (the issue-488 packet’s uncited
338, $7.14 \times 10^{-4}$ above), `02f9690`’s at 339 and 375 (the issue-476 packet’s),
and `f311f08`’s at 376, 378, 379 and 380, which no packet retains and whose prints the
certificates README at `f311f08` gives as 19.914264379786, 19.942703712927,
19.953573157088 and 19.988234448072. At 379 the release improves the author’s own
previous certificate by $4.5 \times 10^{-7}$ and the register’s row by
$3.966 \times 10^{-3}$.

**The four unrequested certificates** (RY-10), compared in the record and registered by
no entry. A scratch driver of the route’s functions, not retained, decided all four on
the third route in 33.4 s (178,786 pairs, 2,654 clipped): each passes with its six
controls, clears every wall by exactly $1/(2 \cdot 10^{20})$ and every pair by
$1.000000 \times 10^{-20}$, equals its retained positive job’s inputs and margins, and
is admitted against the certificates README’s print at the pin, so every certificate of
the two commits has three routes:

- **175**, 13.7671190241983643: below the case ceiling, Ryan Xu’s 13.7688992766137689
  (T-125), by $1.780 \times 10^{-3}$, and below T-140 (#488) by $1.700 \times 10^{-6}$,
  T-130, T-138 and #476 by $3.613 \times 10^{-5}$; the smallest side known at 175, and
  the source’s table calls it best known.
  Its own import is `think-9fjl`.
- **308**, 17.9984598310239785: below the grid and T-135 (#484) but above T-141 (#489)
  by $1.899 \times 10^{-4}$; the source marks it superseded.
- **340**, 18.9396496328910066, beyond the horizon: below the current tracked row,
  Couzo’s 18.939879629586962, by $2.299 \times 10^{-4}$, and below the issue-488 and
  issue-476 certificates by $5.151 \times 10^{-5}$ and $9.823 \times 10^{-5}$; the
  smallest side known at 340.
- **343**, 18.9938705897493327, beyond the horizon: below the grid and #484 but above
  Hunt 3’s verified row by $1.563 \times 10^{-2}$; the source marks it superseded.

## Credit and Lineage

The issue asks that the constructions each started from be credited: at 304 and 305 Nate
Chaoweeraprasit’s SQUISH Mondrian packings (#500), improved by Evan Daniel’s `fq` at 304
and by the author’s search cycle with David Ellsworth’s `refine_packing`, basin hopping
and LP at 305; at 344 Kevin Fang’s 344 (#484), improved by the author’s basin hopping;
and at 338, 339, 375, 376, 378, 379, 380 and 381 one of the author’s own smaller
packings with an L-shaped border row added and squares removed, then searched (338 and
375 from his 303, itself from SQUISH’s #401; 339 and 376 from his earlier 304; 378 from
306; 379 from 342; 380 from 343 and 381 from 344, both from Fang’s 344). Evan Daniel’s
exact contact solver wrote the ten exact optima.
The packet and the register plan carry that credit line, and the bibliography key’s
credit, “Couzo after Chaoweeraprasit, Fang, Daniel, Ellsworth, Levy”, follows the
record’s earlier Couzo entries.

**What was measured.** Where the record retains the parent as a certificate, the third
route’s two credit measurements were run: `arrangement_gap`, which matches each square
of the certificate to the nearest centre of the parent under the best of the box’s eight
symmetries, kept only where one to one, and reports the largest move, the largest turn
and how many squares moved beyond each scale; and `patch_lineage`, which finds the
placements of the parent under which most of its squares reappear in the child within
$10^{-9}$ (by pose) or, widened, within a tenth of a unit (to the eye).
For this the route gained credit pairs for #506 at 304 and 305 against #500 and at 344
against #484 and Hunt 3’s #489, and lineage entries for the same three counts; a credit
key that is an import rather than a register entry now reads that import’s certificate.
A measurement for credit; it decides nothing, and the issue’s own figures were not
reproduced.

| Certificate | Against | Best symmetry | Squares moved beyond $10^{-9}$ ($10^{-3}$, $10^{-2}$, $10^{-1}$) | Largest move | Largest turn (sine); turned beyond $10^{-6}$ |
| --- | --- | --- | --- | --- | --- |
| #506, 304 | #500, 304 | a reflection | 243 of 304 (65, 19, 0) | $5.03 \times 10^{-2}$ | $7.27 \times 10^{-2}$; 72 |
| #506, 305 | #500, 305 | a reflection | 257 of 305 (58, 24, 0) | $7.18 \times 10^{-2}$ | $6.18 \times 10^{-2}$; 92 |
| #506, 344 | Fang’s #484, 344 | a half turn | 344 of 344 (206, 79, 0) | $8.75 \times 10^{-2}$ | $4.48 \times 10^{-2}$; 254 |
| #506, 344 | Daniel’s Hunt 3 #489, 344 | a half turn | 214 of 344 (136, 63, 3) | $1.30 \times 10^{-1}$ | $3.40 \times 10^{-2}$; 125 |

| Parent, as the source names it | In | Placement found | Within $10^{-9}$ (turned; exact) | Within a tenth (turned) |
| --- | --- | --- | --- | --- |
| #500’s 304, whole | 304 | the 304’s box reflected in $x = L/2$, moved by $(-9.1 \times 10^{-5}, -9.1 \times 10^{-5})$ by pose and by $(0.0186, 0.0051)$ to the eye | 146 (0; 1) | 304 of 304 (72) |
| #500’s 305, whole | 305 | the same reflection, moved by $(-7.8 \times 10^{-5}, -7.8 \times 10^{-5})$ by pose and by $(0.0371, 0.0000)$ to the eye | 138 (0; 1) | 305 of 305 (92) |
| Fang’s #484 344, whole | 344 | no placement by pose; to the eye the 344’s box turned by a half turn, moved by $(0.0277, 0.0067)$ | none | 340 of 344 (250) |

**304 and 305 are #500’s arrangements re-equilibrated, and 344 is Fang’s moved.** At 304
and 305 every square of the certificate is matched one to one to a square of #500’s
packing under a reflection of the box, none moved beyond a tenth of a unit and at most
24 beyond a hundredth, and to the eye the whole parent reappears under that reflection;
by pose, under the reflection alone 243 and 257 squares moved beyond $10^{-9}$ and 72
and 92 turned, and under the reflection carried by the side difference 146 and 138
squares coincide, none of them turned, one of them exactly: upright squares against the
far walls, which moved with the walls.
That is the source’s account: a Mondrian packing re-solved by `fq` or by the author’s
search cycle and then taken to an exact optimum of the same contact graph, which moves
every square a little and no square far.
At 344 all 344 squares moved beyond $10^{-9}$ against Fang’s certificate and 329 beyond
$10^{-6}$, under a half turn of the box, with 254 turned by up to a sine of
$4.5 \times 10^{-2}$ and the largest move $8.7 \times 10^{-2}$; against Hunt 3’s 344,
itself Fang’s moved by $8.2 \times 10^{-2}$ at most under the identity in the #488/#489
review, the match is also one to one under a half turn with three squares moved beyond a
tenth. So the three 344s are one arrangement of Fang’s moved in different directions, as
the issue says of its own and the #489 review found of Hunt 3’s, and the verified row
this release supersedes at 344 is a sibling of it.
The credit is as the source asks and is not in question; the register entry’s claim
should state the relation as measured (RY-12).

**What was not measured.** The eight L-shaped constructions, whose parents are the
author’s own smaller packings at other counts (303, 304, 306, 342, 343, 344), which a
border row and removed squares relate to the child by no symmetry of one box; the record
retains the author’s 303, 306, 342 and 344 of `3ef7634`, and the measurement of a
sub-packing placed in a larger box is a tool this route does not have.
Their credit is the source’s account.

## AI Assistance

The issue states that the search code and the request were written with Claude (Claude
Code) and that the author directed and reviewed the work; the source’s commits name an
AI assistant as co-author, as the #488 review recorded.
The register plan carries that statement in the entry’s claim, as the record’s earlier
Couzo entries do. As at #488 (RL-8) and #500 (RX-7), the producer’s assistant and this
reviewer share a model family; the decisions are exact and do not depend on judgment,
both maintained routes predate the source, and the third route’s parser of this format
predates this release, but an error of method common to the family would not be
independent across them (RY-9).

## Findings

**RY-1, non-blocking, closed here: the comparison with #500 was frozen by print** (RX-6
of the #500 review).
The declaration now names #500 by the reader of its packet and the record is refrozen:
at 304 the exact margin is $9.109 \times 10^{-5}$ and at 305 $7.837 \times 10^{-5}$, the
lower bounds the #500 review stated to four digits, and every relation and every
`smallest` stands. No other row of either claim record changed, and the register plan is
unchanged.

**RY-2, non-blocking: the witness at 375 is dilated by $1 + 10^{-11}$ about
$(\tfrac12, \tfrac12)$, and the source’s README says $1 + 10^{-12}$.** As measured under
The Rational Witness.
The bound is unaffected; the author should be told that the README’s general description
does not describe this certificate, and the register entry’s claim should state the
dilation as the issue gives it, as the plan does.

**RY-3, non-blocking: the issue’s “before” column is the author’s own history, not the
register’s rows.** At seven of the nine beyond-horizon counts the issue compares with
the author’s latest earlier certificate, four of them at `f311f08` and retained by no
packet; the register’s margins, from the rows it tracks, are the ones in the table above
and are larger. The entry’s notes should state the register’s margins, as the plan does,
and may quote the issue’s separately.

**RY-4, non-blocking: one maintained route is the producer’s checker** (RL-5). The issue
states that all eleven pass this repository’s `verify.py`; the independently
re-implemented relation rests on V-check-rational-witness-independent and the third
route, neither of which the source ran.

**RY-5, non-blocking: the kernel’s controls are gross** (RI-3, unchanged).

**RY-6, non-blocking: no retained check binds a retained file to its upstream bytes**
(RI-2, unchanged). Closed once here, at this date, for all 85 files of the manifest and
by the third route’s `--upstream` for the eleven requested certificates; the confirming
evidence should cite this review for the binding.

**RY-7, non-blocking for this claim: no private-worker custody.** The rung for finite
feasibility does not need it; the adoption lane closes it before a house moves (RD-5,
RI-5).

**RY-8, non-blocking: this review replayed four of the eleven requested counts on the
kernel.** The other 21 requested jobs and the 12 unrequested ones rest on the import
lane’s `certify` and its own complete `check --replay`, both on 2026-10-11, and on the
third route here at all eleven requested counts; the confirming evidence’s `replay`
should name both runs and this one.

**RY-9, non-blocking: the reviewer and the producer’s assistant share a model family**
(RI-7, RL-8, RX-7, unchanged).
`V4`/`C4` needs a second adversarial review by a distinct reviewer in any case.

**RY-10, non-blocking, for the owner: the four unrequested certificates.** By the import
rules each is an import of its own and no entry registers it.
175 is the smallest side known at its count and its own bead, `think-9fjl`, asks the
author whether it should be registered and then registers it from this packet with the
third route and a review; this review decided it on the third route in scratch and that
decision is not retained, so that import adds it to a roster.
340 is the smallest side known at 340, replayed in the receipt and decided here in
scratch; the owner may adopt it as a verified beyond-horizon row once a roster retains
its third-route decision, as RL-9 offered for #488’s 338 and 340, or leave the row until
a request names it. 308 and 343 are beaten by T-141’s 308 and Hunt 3’s verified 343, the
source marks both superseded, and they stay replayed, compared and registered nowhere
(as RW-5).

**RY-11, non-blocking: the nine beyond-horizon rows supersede seven current rows, one of
them verified.** When the rows are registered, the current rows at 338, 339, 376 and 379
(`couzo-extended-range-reports-2026-10-08`), 375 and 378
(`couzo-extended-range-updates-2026-10-08`) and 344 (`evand-record-hunt3-2026-10-10`,
verified) must be marked `superseded` with
`superseded_by: couzo-certificates-2026-10-11` in the same change, since
`current_beyond_horizon` refuses two current rows at one count; each successor is
strictly smaller by exact comparison of the printed decimals and the source is dated no
earlier, as `_succession_errors` requires.
380 and 381 have no row and need no supersession.

**RY-12, non-blocking: 304 and 305 are #500’s arrangements re-equilibrated, and 344 is
Fang’s moved, as Hunt 3’s was.** As under Credit and Lineage.
The entry’s claim should say that the two in-corpus packings refine #500’s arrangements
(every square one to one under a reflection of the box, none moved beyond a tenth)
rather than that they are new, and its notes that the 344 and Hunt 3’s 344 are one
arrangement of Fang’s moved in different directions, so the verified row it supersedes
is a sibling of it.

## Rungs

**#506: `V3`/`C3` at 304 and 305.** Machine-replayed here: the six kernel jobs at both
counts on both maintained routes, equal to their retained rows; both certificates with
their twelve controls on the third route, held to the receipt’s inputs and margins; the
retained files held to their upstream bytes here; the import lane’s complete replay of
all 45 jobs retained; reviewed adversarially here.

**The nine beyond-horizon rows: `assurance: verified`** from the same confirming
evidence, as RL-7 decided for #489’s 343 and 344 and RI-6 for #484’s: each certificate
was decided twice by the import lane on both maintained routes, by the third route here,
and at 344 and 381 by the kernel here as well; the rows keep the issue’s twelve-place
prints byte for byte, each of which the exact side rounds up to, so each row is itself a
proved bound. At 344 the row replaces one that is itself verified, so a `reported` row
would step the register down.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

For the records lane: the entry can take `V3`/`C3` on a confirming evidence entry
(`E-couzo-506-exact-feasibility`, scope all eleven requested counts) with
`relationship_to_generator: independent-implementation`, as T-140’s records it under
RL-5, naming the verifiers V-sqpack-verify, V-check-rational-witness-independent,
V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area and
V-evand-exact-certificates, with this review as its `independence_record` and as the
reported entry’s `external_review`.

## Significance

The import lane drafted `S3`. The score is of the two in-corpus bounds; the nine
beyond-horizon rows carry none.
The measurement above says what the two packings are: #500’s arrangements, each square
one to one under a reflection of the box, re-equilibrated by `fq` at 304 and by the
author’s search cycle at 305 and then solved to an exact optimum, with 243 and 257
squares moved beyond $10^{-9}$, 65 and 58 beyond a thousandth, none beyond a tenth, and
72 and 92 turned by up to a sine of $7.3 \times 10^{-2}$. They are refinements of #500’s
packings, not new arrangements, by $9.109 \times 10^{-5}$ and $7.837 \times 10^{-5}$ in
side, and $5.084 \times 10^{-3}$ and $2.492 \times 10^{-3}$ below the case ceilings.
Compared with the entries nearest to them under the rubric the
[11 October final review of upper bounds](review-2026-10-11-final-upper-bounds.md#significance-and-novelty)
applied, `S3` for entries that moved a case’s best side by $10^{-6}$ to $10^{-2}$ when
published and `S2` for precision refinements and display views at $10^{-17}$ to
$10^{-10}$: T-140 (`S3`) is the same author’s refinements of SQUISH’s #481 packings by
the same tools, one to one under a symmetry with 177 to 262 squares moved and
$4.3 \times 10^{-7}$ to $5.6 \times 10^{-5}$ below them; T-128 (`S3`) is his exact
refinements of earlier packings at $9.8 \times 10^{-7}$ to $6.6 \times 10^{-4}$; T-137,
T-139 and T-146 (`S2`) are precision refinements and display views at $10^{-17}$ to
$10^{-10}$. These two sit with T-140, and `S3` is confirmed: substantive case results at
both counts, the smallest sides known there.
Under a reading that scores any refinement of a credited arrangement `S2` whatever its
size, which the record has not applied to T-140 or T-128, they would be `S2`; the
measurement is recorded so that the significance reviewers can apply whichever rule the
owner settles. Not `S4`: bounds, not a method.
`by` on the entry should name this review.

## Adoption per Count

The smallest exact certificate at each in-corpus count, against the case’s verified
ceiling at `main` `3a5a91a90` and every report pending on 2026-10-11, each comparison
exact. Sides are shown rounded up at sixteen places.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | House to adopt |
| --- | --- | --- | --- |
| 304 | 17.9346500183906818, T-098 | #506, 17.9295659468485010; #500, 17.9296570421708801 | #506, Francisco Couzo, crediting #500’s Mondrian packing as its start; then #500 |
| 305 | 17.9529594590155280, T-098 | #506, 17.9504664821377123; #500, 17.9505448539256365; T-140, 17.9511397722069976; T-136, 17.9511961441473858 | #506, crediting #500 as its start; then #500, T-140, T-136 |

This confirms the #500 review’s table at 304 and 305, which named #506 once reviewed; at
every other count that table and its predecessors stand.
Beyond the corpus there is no house: the register’s rows at 338, 339, 344, 375, 376, 378
and 379 move to this release’s sides and rows are created at 380 and 381 (RY-11); the
rows at 340 and 175’s case stay as they are unless the owner acts on RY-10. At every
count the earlier houses stay retained as history, and the case’s reported and verified
ceilings move together.
Credit follows the issue.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry**: `E-couzo-506-exact-feasibility`,
  `assurance: verified`, `method: exact-algebraic`, `performed_by: repository`,
  `origin: replayed-here`, `relationship_to_generator: independent-implementation`, the
  packet’s certificate directory as `certificate`, scope all eleven requested counts,
  the replay commands above with their walls and the import lane’s `certify` and
  `check --replay` runs, `replay_status: passed`, the six verifiers named under Rungs,
  this review as `independence_record` and as `external_review` (`informally-verified`),
  and limitations naming the shared premises, RY-4, RY-5, RY-7 and RY-8.
- **On the reported entry** (`E-couzo-506-certificate-report`): `external_review` naming
  this review, which makes it `reviewed`.
- **On the register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`), both test files among the controls
  (`packing/tests/test_upper_bound_reports.py`,
  `packing/tests/test_check_half_angle_area.py`), the significance `by` naming this
  review, and claim, notes and `next_rung` rewritten together: the exact margins to #500
  (RY-1), the dilation as the issue states it (RY-2), the register’s margins beyond the
  horizon (RY-3) and the lineage as measured (RY-12).
- **In `source-coverage.yaml`**: the source entry with the confirming evidence; nine
  rows at `assurance: verified`, `disposition: tracked-outside-case-corpus`, the values
  of the packet’s `beyond-horizon-claims.json` byte for byte; the seven current rows
  they beat marked `superseded`, `superseded_by: couzo-certificates-2026-10-11`, in the
  same change (RY-11).
- **Two verifier entries**: V-check-half-angle-area’s note gains this import, on which
  it ran through a roster entry with no change to any decision; V-upper-bound-reports’
  note gains this review.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the source’s or Evan Daniel’s checkers or solvers.
No kernel replay here of the 33 jobs at 338, 339, 375, 376, 378, 379, 380 and the four
unrequested counts. No retained third-route decision of the four unrequested
certificates: the scratch decision above is reported, not kept.
No measurement of the eight L-shaped lineages.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
