# Review: Daniil Ostashev’s and Rio Calle’s Rational Upper-Bound Imports of 12 October (#528, #529)

**Date:** 12 October 2026. **Verdict: accepted, for finite feasibility only.** The four
certificates the two imports’ register entries would cite prove the upper bounds their
packets state: Daniil Ostashev’s n = 175, n = 232 and n = 264 (#528), retained byte for
byte at `a8db6ff`, and the exact certificate this repository derived from Rio Calle’s n
= 102 layout (#529) at `8313686`. Both retained receipts reproduce here job for job, the
third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended for Calle’s decimal format and for the credit measurements below, agrees with
both maintained routes at every number they share, and every file of both pinned scopes
was fetched here at its pin and found at the digest its packet records: each retained
file is its upstream file, and the derived fact is the packing the pinned layout states,
derived again by the route’s own reader and arithmetic.
Ostashev’s statement that his three packings are new arrangements was measured true:
none is a placement of the packing its case holds or of any report pending at its count,
and the pieces he names reappear by pose where the record retains them.
Calle’s statement that his packing is another arrangement of Ryan Xu’s design was
measured true: every square pairs with one of Xu’s under a half turn of the box, 40 to
the ninth decimal and 62 moved, 19 of them by more than a tenth of a unit.
Eleven findings are recorded, none blocking.
#528’s entry, once registered, can take `V3`/`C3` at all three counts when its
confirming evidence entry and this review are added, and its certificate is the smallest
side the record holds or has pending at each; #529’s is above the certificate the case
holds (T-146) by $2.43 \times 10^{-11}$, moves no case, and should be registered all the
same, at `V3`/`C3`, for the reasons under
[Whether #529 Is Registered](#whether-529-is-registered).
Neither can take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 2026-10-12 intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
the 2026-10-11 pass’s epic, written by an AI agent (Claude, at extra-high reasoning
effort) prompted separately from the import lane that built the two packets (lane U,
`think-em0b` and `think-s2i8`), with no shared context beyond their committed notes,
scratch measurements and register plans; the import lane and this reviewer are both
Claude, and the import lane decided no geometry.
Its relation to the results is `project`. It moves no rung, writes no register row and
changes no case record; it says what the records lane should write.

## Claims Covered

| Entry | Source | Count | How the side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #528 | [Daniil Ostashev, #528](https://github.com/jlevy/squares/issues/528), `dostashev/square-packing` at `a8db6ff`, the commit the issue names and the head when read | 175 | the issue prints `13.76417431748659662942782322004234282577`, 38 places rounded up; the exact side, $N/(2 \cdot 10^{117})$ with a 119-digit $N$, rounds up to it there, and to the README’s `13.764174317486597` at 15 |
| T-NNN, #528 | the same | 232 | `15.76417431748659662944782322004234282577`, likewise, $N/(2 \cdot 10^{117})$ |
| T-NNN, #528 | the same | 264 | `16.77473513238783284261026458732177098083`, likewise, $N/10^{118}$ |
| T-NNN, #529 | [Rio Calle, #529](https://github.com/jlevy/squares/issues/529), `riocalle/my-repo` at `8313686`, the repository’s only commit | 102 | the issue, the README and the file name print `10.605828696455852`; the derived certificate’s side is that decimal exactly, $2651457174113963/(25 \cdot 10^{13})$, admitted by equality |

The packets are
[dostashev-records-2026-10-12](../../../packing/resources/web/dostashev-records-2026-10-12/README.md)
and
[riocalle-n102-2026-10-12](../../../packing/resources/web/riocalle-n102-2026-10-12/README.md).
Ostashev’s tree is MIT-licensed and his packet retains the eight files `a8db6ff` adds or
changes with the licence, byte for byte, and pins the other 36 files of the tree at the
digests the #501 packet retains them at; Calle’s tree states no licence, so his packet
keeps a derived exact fact and pins all eleven files of the tree by SHA-256.

Four things the sources publish are outside the entries and are placed here.
Issue #528 restates #501’s three sides at the same commit; the certificates at 155, 156
and 211 are byte-identical to the ones the #501 packet retains and T-149 states, so
nothing is read again and the author’s wish that the record carry the `c3d17ab` sides is
already met (RW-1 of the
[#505/#501 review](review-2026-10-11-upper-bound-imports-505-501.md)). The same issue
reports a new packing of 38 unit squares in an $(h + 2) \times h$ rectangle,
$h = 5.76417431748659662929\ldots$, the shared piece of the three compositions: a
rectangle packing, no bound on $s(n)$, which stays in the packet.
Its statement that each side is the exact first-order optimum of its contact topology is
a local-optimality report, recorded and not decided.
Issue #529’s README reports a “valley bottom” at $s = 10.605828696431638$ with no layout
published: an author report, not certified here and not registrable; it is
$6.0 \times 10^{-14}$ above T-146’s side.
The same tree keeps the author’s earlier layout at $s = 10.605828708$ under `earlier/`,
first reported on 8 October in Davidebyzero’s tools repository; it is above every
ceiling and asks for no work.

**Read in full.** The import lane’s commit `fda34049d`: both packets’ READMEs,
declarations, acquisition records, manifests, claim records, the three retained
certificates, the derived fact and both receipts, with the `calle-txt` adapter and its
tests; the import lane’s bead notes, scratch lineage measurements and register plans;
issues #528 and #529, each with no comment yet; both pinned READMEs, fetched here, and
Calle’s `verify_exact.py`, read and not run; Ostashev’s `verify/` sources and
`tools/crosscheck_mpmath.py`, fetched at `a8db6ff` and found byte-identical to the #501
packet’s retained copies, not run; the #505/#501 review and its siblings for #503/#504,
#500 and #506; [epistemics.md](../../../epistemics.md) on the rungs, review records and
significance; and layer 5’s significance review
(`review-2026-10-11-significance-scores.md`, on branch `layer5`, not yet on this branch,
so not linked by the record here).

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 13 to 26, one worker process throughout, in a
worktree at the import lane’s `fda34049d` with this review’s change to the third route
added. A replay decides every job of the packet again through both maintained routes,
serially in one process, and compares every field of each fresh job with its retained
row except the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `riocalle-n102-2026-10-12 check --replay` | #529’s 3 jobs: the derived certificate with its two kernel controls | all 3 equal, “1 certificates and 3 jobs admitted”, exit 0 | 2 min 0 s |
| `dostashev-records-2026-10-12 check --replay` | #528’s 9 jobs: the three certificates, each with its two kernel controls | all 9 equal, “3 certificates and 9 jobs admitted”, exit 0 | 34 min 31 s |
| `PACKET check-claims`, for each | each frozen comparison rebuilt from the certificate and the holders’ own packets | both rebuilt equal as JSON (the printed layout differs from the frozen file’s) | 3 s and 7 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#528' '#529' --upstream dostashev-records-2026-10-12 DIR528 --upstream riocalle-n102-2026-10-12 DIR529 --json OUT` | the third route on the four certificates and 24 controls, every cross-check, the seven credit measurements and two lineage measurements, each #528 file against its upstream bytes, and the #529 fact against the layout derived again from the pinned file | no disagreement, exit 0 | 335.7 s (5 min 40 s with the interpreter’s start) |

The third route ran 10:03:37Z to 10:09:17Z, the #529 replay 10:11:34Z to 10:13:34Z and
the #528 replay 10:13:34Z to 10:48:05Z, the load having risen to 20 to 26 by then.
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #528 | 9 | 460,422 | 647.47 | 1,544.83 | 291.46 (the 264 positive) |
| #529 | 3 | 30,906 | 39.06 | 96.84 | 32.78 |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Each retained certificate gives a rational side $S$ and, for each
square, a rational centre $(x, y)$ in $[0, S]^2$ and $t = \tan(\theta/2)$; the derived
fact carries the exact rotation $(\cos\theta, \sin\theta)$ instead.
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
tolerates. Ostashev’s guards are already in his certificates: his 60-digit optima with
the load-bearing squares scaled by $1 + 10^{-20}$, then every centre and the side
multiplied by $1 + 10^{-60}$ and each $t$ rounded to 70 places, as the headers of the
files say and nothing here believes.

**Calle’s layout is not a certificate, and the certificate is this repository’s.** The
file prints each centre and each rotation in radians as a decimal of 18 significant
digits, and a rotation printed in radians has no rational cosine and sine.
The importer’s `calle-txt` adapter reads every decimal exactly as printed, takes the
printed side with no dilation, and replaces each angle by the rational
$t = \tan(\theta/2)$ rounded down at 40 places; the derived fact is that side, those
centres and those rotations.
The rounding turns each square by less than $2 \times 10^{-40}$ radians, which moves no
corner by as much as $10^{-39}$, against margins of $2 \times 10^{-12}$; whether the
result still packs is what the exact routes decide, and they do.
So the claim is $s(102) \le 10.605828696455852$, the printed side exactly, and its
certificate is the packet’s derived fact, as T-138’s witnesses are the record’s own
derivation from Mishapolk’s decimal poses.
Calle’s own exact certificate comes from an engine he does not publish; it is not
recoverable, and nothing here rests on it.

**Nothing touches, so the box convention does not matter.** Every positive clears every
wall and every pair by a positive amount, on all three routes, and the third route
counts no square-to-wall clearance of exactly zero at any count:

| Import | n | Least wall clearance | Least separating-axis gap (both maintained routes) | Least Euclidean distance (third route) |
| --- | --- | --- | --- | --- |
| #528 | 175 | $5.000000 \times 10^{-21}$, a tilted square’s, a 200-digit rational | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |
| #528 | 232 | exactly $(10^{60} + 10^{20} + 1)/(2 \cdot 10^{80})$, the corner square’s, as at #501’s 155 and 156 | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |
| #528 | 264 | $5.000000 \times 10^{-21}$, a tilted square’s, the near and far walls differing beyond the seventh digit | $5.000000 \times 10^{-21}$ | $5.000000 \times 10^{-21}$ |
| #529 | 102 | $2.002066 \times 10^{-12}$, the same at the near and the far walls | $1.932818 \times 10^{-12}$ | $1.932818 \times 10^{-12}$ |

At 232 the least wall clearance is the first corner square’s, whose centre is
$\tfrac12 + 5 \cdot 10^{-21} + 5 \cdot 10^{-61} + 5 \cdot 10^{-81}$: half the $10^{-20}$
scaling, half the $10^{-60}$ dilation, and their product, the number #501’s 155 and 156
showed. Calle’s margins are the ones his README describes, every centre scaled by
$1 + 2 \times 10^{-12}$ and lifted $2 \times 10^{-12}$ off the low walls with the box
set $2 \times 10^{-12}$ beyond the highest corner, and the ones his `verify_exact.py`
prints at three digits; here they are the routes’ own exact numbers, and the closest
pair is nearer than the walls.
So the closed squares are pairwise disjoint and inside the open box, and the bound holds
under any of the usual conventions.
All four certificates state their centres in $[0, S]^2$; no adapter moves anything.

## Adapters and Admission

Each format has one maintained adapter in `upper_bound_reports.ADAPTERS` and its own
reader in the third route.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `sqcert` | `records/n0175.sqcert`, `n0232.sqcert`, `n0264.sqcert`, retained | `n N`, `s S`, then `n` rows `x y t`; blank and `#` lines skipped | the `#` header labels: `claimed_s`, `delta`, `digits`, the source file name, the sqverify version line and the column legend |
| `calle-txt` (new on this import, both routes) | `n102_s10.605828696455852.txt` at derivation; here again at the pin | `# n = N` and `# s = S` once each among the comments, then `n` rows `x y theta`, every number a decimal, plain or in scientific notation, read exactly; `theta` in radians | the prose comment line; the JSON and SVG copies, which the import lane read in scratch and found to state the same 102 binary64 triples; the README |
| derived fact | #529 | a rational `center-basis` Witness/v2 in $[0, S]^2$ | its `claim` prose |

The maintained `calle-txt` adapter and the third route’s `read_calle_txt` with
`derive_calle_txt` were written separately, the adapter by the import lane and the
reader by this review: the adapter floors each half-angle tangent by an outward-rounded
mpmath interval enclosure at a rising working precision, the third route by Taylor
series of the sine and cosine of the exact half angle in `decimal` arithmetic with a
widening error bound and a rising guard, the method the route already used for
Ellsworth’s degrees (#470), without the $\pi$ that degrees need.
Both read the pinned file alike at every centre, every angle and the side, and
`decide-imports --upstream` found the fact the importer wrote equal, basis for basis, to
the packing the third route derived.
Its tests hold the two floors equal at the layout’s own angles and at 32 and 40 places,
and hold the floor at $\theta = 10^{-15}$ to $5 \times 10^{-16}$ exactly, where the
cubic term of the tangent lies below the fortieth place.
The third route refuses an angle of 3 radians or more rather than reduce it, since a
radian angle cannot be reduced exactly and the tangent’s pole is near; the layout’s
angles lie within $\pm\pi/2$.

**Admission.** Each #528 certificate is admitted by rounding up at the 38 places the
issue prints; the README at the pin prints the same three sides at 15 places, which the
third route’s `printed_table_side` does not check here since the declaration names the
issue, not the README, as where each side is printed.
The frozen claim records print each side rounded up at 16 places, $13.7641743174865967$,
$15.7641743174865967$ and $16.7747351323878329$, and the third route’s own integer
ceiling agrees. #529’s certificate is admitted by equality: the derived side is the
printed decimal, and the frozen record’s ceiling $10.6058286964558520$ is it.

## Custody

**#528, retained bytes.** All 44 files of the pinned tree were fetched over HTTPS from
`raw.githubusercontent.com` at `a8db6ff` into scratch space, outside the repository, and
read as data; all 44 have the SHA-256 the packet’s manifest pins, the eight retained
files among them.
`decide-imports --upstream` held each retained `.sqcert` to its fetched
bytes, byte for byte: three upstream checks.
The 25 files of `verify/` and the two of `tools/`, the author’s C++ GMP checker with its
tests and the mpmath cross-check, are byte-identical at `a8db6ff` to the copies the #501
packet retains, as the acquisition record says.

**#529, a derived fact.** The source states no licence and the packet keeps no upstream
byte. `derive` read the layout from a Git checkout at the pin once `acquire_source`
showed that the checkout yields the packet’s own acquisition record and manifest, and
wrote the certificate as a derived fact naming the pinned SHA-256. For this review all
eleven files of the pinned tree were fetched the same way at `8313686`; all eleven have
the SHA-256 the manifest pins.
`decide-imports --upstream` then read the pinned layout with the third route’s own
reader, derived the certificate again with its own arithmetic, and found it exactly the
packing the fact states, side, every centre and every rotation: one upstream check.
That binds the fact to its pinned layout as of this date (RX-7).

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the adapters, the parse and half-angle map of `evand_exact_certificates`, and for #529 the importer’s interval floor; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same adapters, parse, map and floor, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area; for #529 its own decimal reader and tangent floor | `devtools.check_half_angle_area`; `sqpack.yamlio` for the fact; `hashlib`; `decimal` | `Fraction` and the formats’ meaning only |

Neither source ran a route of this project.
Ostashev reports his own C++ GMP checker `sqverify` on the shipped certificates with no
dilation and no tolerance and on certificates rebuilt from the decimal packings, and an
80-digit mpmath cross-check, the first two sharing a parser and geometry and the third
sharing only the file format; all three are retained in the #501 packet and pinned here,
and none was built or run.
Calle reports `verify_exact.py`, a 60-digit `decimal` separating-axis check that rounds,
run by the import lane once outside the repository and reproducing the two gaps the
issue states, and his engine’s private exact rational-interval certificate, which cannot
be rerun by anyone but him; both, the issue says, were written with Claude and share no
code.
So at both imports every route here is independently re-implemented with respect to
the producers’ verification, and at #529 the certificate itself is the record’s.

`upper_bound_reports` owns custody, the adapters, admission, the claim comparison and
the job layout; the kernel owns the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on each packet’s own admission (`acquire_source.check`,
and for the fact `read_fact`), which the third route calls before it reads anything and
from which it decides nothing.

**What stays unchecked.** CPython’s `fractions`, `decimal` and integer arithmetic are
common to every exact checker here.
None of the sources’ programs ran.
Ostashev’s statement that each side is the exact optimum of its packing’s contact
topology, with nonnegative KKT multipliers, is a local-optimality report and is not
decided; nor is Calle’s valley bottom, nor the history of how either packing was found.
That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters, the `calle-txt` adapter included, before writing the extension, so it is not a
clean-room implementation; it imports none of their parsing, deriving or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It is a second pair-deciding procedure, not a second arithmetic.
On the four certificates it decided 81,888 pairs, clipping 1,665, and found no overlap
and no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3 of the first
imports review, carried as RX-6). `validate_job` requires both routes to refuse each
control, on the complete pair count, with the negative diagnostic it was built for.
In both receipts the duplicate’s gap is exactly $-1$ and the moved square lies exactly
3.0 units outside the box, refusals a binary64 checker with a $10^{-9}$ tolerance would
also make. They show the routes can refuse, not that they decide at the $10^{-12}$ and
$10^{-21}$ scale where these certificates live.

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

All 24 reached their required outcome.
At 232 the far-wall control shrinks the side by the same $5 \times 10^{-21}$ the near
wall shows, so the box is closed at both ends by the same guard; at 102 by the same
$2.002066 \times 10^{-12}$ lift.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all four sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- each side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against its print, #528’s by rounding up
  and #529’s by equality;
- each least wall clearance equals both maintained routes’ to every digit;
- each least Euclidean distance is at least the separating-axis gap both maintained
  routes report, and here equals it at seven places at every count;
- the two receipts’ totals are the numbers the packets print; each #528 file is its
  upstream file, and the #529 fact is the packing its pinned layout states.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes its certificates against the case record
as it stood at layer 4’s head `dead83f0e`, which carries `main` at `ad00d7f84` and the
open import and adoption layers, and against every register entry pending there, each
side rebuilt from its holder’s own retained packet; `check-claims` rebuilt both equal.
Every comparison is exact; the margins are shown at seven significant figures.

| n | Against | Exact side of the other | Relation | Margin |
| --- | --- | --- | --- | --- |
| 175 | the case ceiling on layer 4, T-140 (Francisco Couzo’s refinement of Ryan Xu’s packing, adopted on 11 October) | $860445045293269576081339809497 / (625 \cdot 10^{26})$ | below | $2.946407 \times 10^{-3}$ |
| 175 | Couzo’s certificate at `337078c`, not registered (`think-9fjl`), the issue’s “best public value” | $27534238048396728577781532581 / (2 \cdot 10^{27})$ | below | $2.944707 \times 10^{-3}$, the issue’s figure |
| 175 | T-125 (Ryan Xu’s certificate), the case ceiling on `main` | $68844496383068844496383 / (5 \cdot 10^{21})$ | below | $4.724959 \times 10^{-3}$ |
| 232 | the case ceiling on layer 4, T-136 (SQUISH’s third request, adopted on 11 October); on `main` the case holds the catalogue’s $8 + \tfrac{11}{2}\sqrt2$ with T-136 pending | an 82-digit numerator over an 80-digit denominator | below | $3.254032 \times 10^{-3}$, the issue’s figure |
| 264 | the case ceiling, T-101 (Evan Daniel’s exact certificate of the catalogue’s packing, Göbel’s $9 + \tfrac{11}{2}\sqrt2$ shared with 265), on `main` and layer 4 alike | $4194543648263005692144267432271 / (25 \cdot 10^{28})$ | below | $3.439461 \times 10^{-3}$, the issue’s figure |
| 102 | the case ceiling on layer 4, T-146 (Evan Daniel’s regularization of Ryan Xu’s packing, adopted on 11 October, `V3`/`C3` since 10 October) | $10605828696431578360490734944053 / 10^{30}$ | **above** | $2.427364 \times 10^{-11}$ |
| 102 | T-125 (Ryan Xu’s certificate), the case ceiling on `main`, the issue’s “current record” | $21211657393021211657393 / (2 \cdot 10^{21})$ | below | $5.475383 \times 10^{-11}$, the issue’s figure |
| 102 | T-120 (Evan Daniel’s degree-8 exact side of Francisco Couzo’s packing of 26 September, a different design), pending at `V0`/`C0` | $10.607174680176051125342523\ldots$, printed | below | $1.345984 \times 10^{-3}$ |

At 175 the reports T-130, T-138 and the #476 packet’s certificate are above T-140 and
not compared again. No pending entry exists at 232 or 264. No other report of 11 or 12
October states a side at any of the four counts.
At 175, 232 and 264 the certificate under review is the smallest exact side the record
holds or has pending; at 102 it is the second, between T-146 and T-125, which the issue
compares with alone, and its margin to T-125 is right.
T-120 says nothing about this arrangement: it is the exact side of the design this count
held before Ryan Xu’s, and no one has computed the exact side of Xu’s design or of
Calle’s arrangement of it.

## Credit and Lineage

**#528.** The issue says the three are compositions: two library rectangles in opposite
corners of the box and aligned squares around them, each using the new 38-square
$(h + 2) \times h$ block found by a GPU soft-to-rigid search after Yohei Nakajima’s
idea, at 175 in place of the 36-square pieces of Thomas Schadt’s s(50) in David
Ellsworth’s s(171) template ($2 \times 38 + 99$), at 232 beside a 76-square piece of
Erich Friedman’s s(85) ($38 + 76 + 118$), at 264 beside a 93-square piece of Evan
Daniel’s exact optimum of Joost de Winter’s s(126) ($38 + 93 + 133$), each then taken to
the exact optimum of its contact topology; “new arrangements, not refinements”.
`arrangement_gap`, the third route’s credit measurement, tries to match each certificate
to the packing its case holds, and to each report pending at its count, square for
square under the best of the box’s eight symmetries, and `patch_lineage` counts how many
of a named parent’s squares reappear in the child, centre within $10^{-9}$ and edge
direction within a sine of $10^{-6}$, under a symmetry of the parent’s box and a
translation:

| Certificate | Against | Result |
| --- | --- | --- |
| #528 n = 175 | T-140, Couzo’s `337078c` certificate, T-125 | no symmetry pairs the squares one to one with any of the three |
| #528 n = 232 | T-136 | no symmetry pairs the squares one to one |
| #528 n = 264 | T-101’s certificate of the catalogue packing | no symmetry pairs the squares one to one |
| #528 n = 175 | from T-101’s s(171) | 66 of the 171 squares reappear by pose under a half turn of the 171’s box, translated by the side difference $0.1927$ along both axes, none turned, 1 to the digit: the aligned squares the template keeps, those against two walls having moved with the walls |
| #528 n = 264 | from T-098’s s(126) | 88 of the 126 squares reappear by pose under a half turn, translated by $(5, -1)$, none turned: at most the 93 the issue says were cut |

None of the three is a placement of a packing the record holds or has pending, so the
issue’s statement that they are new arrangements is consistent with every pose the
record has; the credit the packet proposes, Daniil Ostashev for the packings and
certificates after the methods and pieces his issue names, is the measured one.
The 232’s piece, Friedman’s s(85), is retained as no exact certificate and was not
measured; nor was the 38-square block itself identified, since the squares were not
sorted into block and aligned squares.
The import lane’s scratch measurement that the whole 175 placed in the 232 moved by
$(0, 2)$ puts 122 of its squares on squares of the 232 is consistent with the shared
block and was not repeated here.

**#529.** The source credits ry-xu with finding the design and the width first (T-125,
published 8 October 2026 at 00:03 UTC) and Rio Calle with this arrangement, found by his
own engine from scratch about ten hours later without reading a published layout: the
same grid blocks and the same 43° diagonal band, “aligned (ry-xu’s rotated 180°), 40 of
the 102 squares coincide exactly, 39 differ by less than 0.05 of a square, and 23 differ
by more, 7 of them by up to half a square”.
The same measurement, against Ryan Xu’s certificate and Evan Daniel’s regularized view
of it, which the case holds:

| Certificate | Against | Symmetry | Largest move | Moved beyond $10^{-9}$ / $10^{-3}$ / $10^{-2}$ / $10^{-1}$ | Turned beyond a sine of $10^{-6}$ (largest sine) |
| --- | --- | --- | --- | --- | --- |
| #529 n = 102 | T-125, Ryan Xu’s certificate | a half turn | $4.941 \times 10^{-1}$ | 62 / 61 / 42 / 19 | 11 ($0.683$, about $43°$) |
| #529 n = 102 | T-146, Evan Daniel’s regularized view | a quarter turn | $4.941 \times 10^{-1}$ | 61 / 59 / 44 / 25 | 11 (the same) |

Every square of Calle’s packing pairs with one of Xu’s under a half turn of the box, and
40 land within $10^{-9}$ of their match, none turned: the issue’s 40, and the issue’s
half turn. The other 62 moved, 19 of them by more than a tenth of a unit and the largest
by $0.494$, half a square, and 11 turned by up to about $43°$: squares of the diagonal
band that sit at another angle in Calle’s arrangement.
The issue’s finer split, 39 within 0.05 and 23 beyond, was not reproduced at its scales,
which this measurement does not use; nothing rests on it.
So this is another arrangement of ry-xu’s design, as the issue says, and not a
refinement of ry-xu’s packing in the sense the record uses for re-equilibrated packings,
where no square moves beyond a tenth (T-150, T-152); nor is it a regularization in
T-146’s sense, so the entry lists no `regularizations` item and the packing is credited
to Rio Calle, with ry-xu credited for the design and width first, as the source asks.
Priority is stated, not defended: ry-xu’s publication time is the source’s own statement
and the record’s T-125 attribution, and Calle’s first report on 8 October at 17:34 UTC
is on Davidebyzero’s tools repository, which the import lane read through the API and
this review could not reach.

## AI Assistance

Ostashev states in the issue: “Yes.
I set up an AI-assisted research loop and drove it with my own ideas.
The rectangle library and composition was my idea; AI agents wrote and ran the search,
composition and verification code”; and of his three checkers, “All three were written
by the same author, with AI assistance.”
The README at `a8db6ff` states nothing about it.
Calle states in the issue: “I designed and directed the project and its experiments.
Claude wrote and ran the code: the GPU search, the exact finishing step, the refinement
search, and both checkers”, and in the README “Built with AI assistance (Claude)”. The
register should carry each disclosure as the source gives it, which both packets and
plans do.

**Against T-149.** T-149’s claim says “The source and the issue make no statement about
AI assistance, and the issue omits the template’s section on it”, and the #505/#501
review asked the author (RW-2, `think-e59i`). Both sentences stay true of #501’s source
and issue.
What #528 adds is the author’s statement about his loop, and two facts fix how
far it reaches: the verification code it names is the `verify/` and `tools/` of the one
repository, byte-identical at `a8db6ff` to the copies the #501 packet retains, so the
checkers that T-149’s source reports were, by the author’s own statement, written and
run by AI agents; and the README’s five-step method, the same at both pins, is what the
issue calls the search and composition code.
The record states AI assistance in the source’s own terms and infers nothing, so T-149
should not be rewritten as if the author had answered for #501; its claim and
`E-ostashev-501-certificate-report`’s limitations should gain one sentence, that on 12
October the author stated on #528 that AI agents wrote and ran his search, composition
and verification code, the verification code being the one retained there, and that
whether the statement covers the three packings’ search is still asked (RX-4). Nothing
in either verdict turns on it: the decisions are exact and do not depend on the authors’
assistants. The reviewer and Calle’s assistant are the same model family, and Ostashev
names none; the decisions here are the routes’, and the import lane decided no geometry.

## Whether #529 Is Registered

The import lane prepared #529’s plan either way and asked.
The rules are these.
[Stage 1’s table](../../../packing/campaign/result-import.md#stage-1-triage) registers
nothing for a claim “below the standing bound and asking for no work”, which stays in
the packet; [epistemics.md](../../../epistemics.md#results-by-others) holds in the
register “every result by others … that the record acts on: its bound is or was a case’s
reported or verified lower or upper bound, or it has been or is queued to be replayed or
reviewed here”, and leaves in their packets “results below the standing bound that ask
for no work”; and the
[frontier README](../../../packing/frontier/README.md#source-coverage-and-freshness)
accounts for every claim a retained source makes exactly once, as selected, superseded
or beyond the horizon, a report that a selected override beats staying listed as its
source printed it and marked superseded.
The standing is derived, never stored: an upper-bound entry whose case holds a bound at
least as good as the one it states reads *superseded by* that result
([epistemics.md](../../../epistemics.md#status)), and one better than its case’s bound
that the case records have not taken reads *pending adoption*.

**Register it**, as the coordinator’s T-155, for three reasons.
First, the scope clause is met on its face: the certificate has been replayed here, on
both maintained routes with controls and on the third, and reviewed here, and the record
holds no replayed packet whose receipt and review attach to no result.
Second, the exclusion is for a claim that asks for no work, and this one asked: the
author filed it through the registration form against `main`, where the case’s ceiling
was and is T-125 and his side is $5.48 \times 10^{-11}$ below it; only the adoption of
T-146, registered on 10 October and the house on layer 4 since 11 October, puts a
smaller certificate in front of it, and the replay was the right call either way.
Third, the standing takes care of itself: on `main` the entry reads *pending adoption*
until the adoption layer merges, and then *superseded by T-146*, with no field to
maintain, which is what the stage 3 rule describes for an entry whose case lanes are
left unchanged. The precedents cut the same way.
The record did not register Griffin Casson’s 39 packings, each larger than Couzo’s at
its count: none was replayed and none asked for work, and the case records state both
sources’ dates and values.
It did not register #505’s five superseded certificates: their author excluded them from
his request, so they are replayed in the packet, compared in its claim record and
registered nowhere (RW-5). And for Couzo’s `337078c` certificate at 175, the smallest
known when found and named by no issue, it asked the author whether he wants it
registered (`think-9fjl`). In each the author’s request, or its absence, decided; Calle
asks.
What registration gives is a row with its credit and its stated priority, its rungs
and derived standing, which every table lists like any other; what it costs is nothing
the case records carry, since the house at 102 stays T-146 and the reported and verified
lanes do not move. The case record at 102 should name the certificate as retained and
replayed, the house unchanged, and the answer to the author should say so.
If the owner prefers the lighter course, the alternative is coherent too: no row, the
packet and its receipt retained, a `priority_notes` item and a paragraph in `n-102.md`
with the value and the date, and the request record saying why; this review then stands
as the packet’s review and the rungs below apply to nothing.

## The Dates and the Plan’s Wording

**`attribution.published`.** Stage 3’s rule is “the date the source gives for it, or the
UTC date of the first commit that contains the certificate”.
For #528 the source gives no date for the three packings (the README is undated and the
issue names none), so the first commit decides: `a8db6ff` at 2026-10-12T03:05:21Z, and
the plan’s `2026-10-12` is right.
For #529 the source gives one: the README’s history and the issue’s lineage section both
date the certified $s = 10.605828696455852$ to 11 October (“11 Oct: pushed to the bottom
of its valley and certified with smaller safety gaps”), so `published` is `2026-10-11`,
not the plan’s `2026-10-12`, which is the first commit (2026-10-12T04:23:19Z) and the
rule’s fallback. The bibliography key keeps the pin’s date, `dated: '2026-10-12'`, by
stage 2’s rule. The import lane reports a comment on Davidebyzero’s issue 6 at
2026-10-11T23:06:09Z, read through the API; its content was not read here and the date
rests on nothing that needs it, since the source’s own date is what the rule takes
(RX-2).

**The generated plan.** Three things in #529’s plan are the template’s words for a
certificate that beats its case, and this one does not (RX-3):

- the claim’s first sentence, “reports a finite upper-bound improvement at the exact
  side it states”, and the register notes’ “the selected standing case is unchanged
  pending independent review and record review”: the side is above the case’s ceiling,
  and the case is unchanged because the record holds a smaller certificate;
- the significance rationale’s “a smaller finite construction side at n = 102, -2.43e-11
  below the case ceiling”: a negative margin below is a margin above;
- `E-calle-529-certificate-report`’s `reported_method: exact-algebraic`,
  `performed_by: source-author` and `certificate: …/facts/`: the exact certificate was
  derived here, so the reported atom should describe what the source reports, a 60-digit
  decimal check and a private exact certificate, as `E-mishapolk-470-pose-report` does
  for #470: `reported_method: numerical-multiprecision`, `performed_by: source-author`,
  `precision: {decimal_digits: 60, rounding: source-defined}`, its `certificate` the
  acquisition record that pins the layout, and the derived fact cited by the confirming
  entry alone, `performed_by: repository`, `origin: replayed-here`.

The corrected plan for both entries is written beside this review’s scratch outputs for
the records lane, with the coordinator’s planned ids as placeholders; the id is taken
last, in the commit that registers.

## Findings

**RX-1, non-blocking: #529 moves no case and should be registered all the same.** As
above; the entry’s claim says the case holds a smaller certificate, its standing is
derived, and the case record names it as retained with the house unchanged.

**RX-2, non-blocking: #529’s `attribution.published` is 11 October.** The date the
source gives, by stage 3’s rule; the plan’s 12 October is the first commit, the
fallback.

**RX-3, non-blocking: the generated plan’s wording and evidence fields for #529.** The
template’s “improvement”, a negative “below”, and a reported atom typed as the source
author’s exact-algebraic certificate for a certificate derived here; reworded above and
in the corrected plan.

**RX-4, non-blocking: #528’s AI-assistance statement reaches #501’s checkers.** T-149
and `E-ostashev-501-certificate-report` gain a sentence stating the 12 October statement
in the author’s terms and that its reach over the #501 search is still asked
(`think-e59i`); the question is not inferred away.

**RX-5, non-blocking: Couzo’s 175 at `337078c` is no longer the smallest.** #528’s 175
is $2.94 \times 10^{-3}$ below it; once T-154 is adopted the certificate is below the
standing bound and asks for no work, so by stage 1 it stays in the #506 packet, where it
is replayed and compared, and `think-9fjl` can close with that disposition unless the
author answers that he wants it registered; the #506 reply should say so, and T-154’s
claim should keep naming it, since the issue names it as the previous best.

**RX-6, non-blocking: the kernel’s controls are gross** (RI-3, RW-6, unchanged).

**RX-7, non-blocking: no retained check binds #529’s fact to upstream bytes.**
`read_fact` proves the fact well formed and self-consistent; `derive --check` needs a
checkout; this review closed the binding once, at this date, by `decide-imports
--upstream` with the third route’s own derivation (RI-2, RW-7, unchanged).
#528’s bytes are bound by `acquire_source --check` offline and were held here to the
fetched tree.

**RX-8, non-blocking: #528’s README still describes a $10^{-30}$ dilation its files do
not use.** The text at `a8db6ff` says “centres and side are scaled by $1 + \delta$
($\delta = 10^{-30}$)” while every certificate’s header says `delta: 1e-60` and is its
`claimed_s` times $1 + 10^{-60}$ exactly (RW-8, unchanged; the author may want to align
the prose with the files).

**RX-9, non-blocking: #529’s README says 17 significant digits; the file prints 18.**
Its files table describes the layout as “17 significant digits”, and every row prints a
mantissa of 18 (`2.50000000000700018e+00`). Every digit is read exactly, so nothing
rests on it.

**RX-10, non-blocking: #529’s stated margin is approximate.** The README’s “every gap is
at least about $2 \times 10^{-12}$” is right for the walls ($2.002066 \times 10^{-12}$)
and not quite for the closest pair ($1.932818 \times 10^{-12}$), as the author’s own
checker and the issue already print; the bound rests on the exact decisions, not on the
prose.

**RX-11, non-blocking: #528’s lineage is measured where the record retains the pieces,
and no further.** Friedman’s s(85) and the 38-square block are stated, not measured; the
entry’s claim should say which pieces were measured and which are the author’s
statement, and should not call the compositions “new” in the record’s own voice beyond
what was measured: no placement of any packing the record holds or has pending at the
count.

No private-worker custody exists at either import, which the adoption lane closes before
a house moves.

## Rungs

**#528: `V3`/`C3`** at 175, 232 and 264. Machine-replayed here: each certificate and its
two kernel controls on both maintained routes, and each certificate with its six
controls on the third route, with a certificate, a replay command, a passing replay and
retained controls; each retained file held to its upstream bytes here; reviewed
adversarially here.

**#529: `V3`/`C3`** at 102, for the same reasons over one certificate, its fact held to
the packing its pinned layout states by a second derivation here.
`V` is the strongest verification anywhere: the source’s own exact certificate is
asserted and not recoverable, which alone would be `V2`, but the record’s derived
certificate replays with a replay command and passing status, which is `V3`’s predicate
for exact-algebraic evidence of any origin, as T-138 holds `V3` on witnesses derived
from Mishapolk’s decimal poses.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

**Verdict lines for the records lane.**

| n | Import | Rungs | Confirming evidence | `relationship_to_generator` | Verifiers |
| --- | --- | --- | --- | --- | --- |
| 175 | #528 | `V3`/`C3` | `E-ostashev-528-exact-feasibility` | `independent-implementation`: the source’s checker is its own C++ GMP program and mpmath script, and the source ran no route here | V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area, V-evand-exact-certificates |
| 232 | #528 | `V3`/`C3` | the same entry | the same | the same six |
| 264 | #528 | `V3`/`C3` | the same entry | the same | the same six |
| 102 | #529 | `V3`/`C3` | `E-calle-529-exact-feasibility` | `independent-implementation`: the source’s checker is a 60-digit decimal script and a private engine, and the certificate is the record’s derivation | the same six |

This review is each confirming entry’s `independence_record` and each reported entry’s
`external_review`.

## Significance

The import lane drafted `S3` for #528 and `S2` for #529.

**#528: `S3` confirmed.** Three new packings, measured as no placement of the packings
their cases hold or have pending, $2.95 \times 10^{-3}$ to $3.44 \times 10^{-3}$ below
the case ceilings and the smallest known at all three counts: substantive case results,
as T-149 (`S3`, three packings built from scratch), T-136 and T-140 (`S3`, new packings
at seventeen and six counts) and T-151 (`S3`, nine arrangements composed from pieces of
earlier packings) are, and unlike T-150 and T-146 (`S2`, optimizations and
regularizations of packings already credited).
Not `S4`: the rectangle library and its composer are one author’s method at three counts
in one release, as SQUISH’s Mondrian composition was at nine (T-151) and PingYou’s
placed patches at one (T-147), and a reusable technique in the `S4` sense is shown by
its reuse, which layer 5’s significance review draws as the line between T-047, T-051
and T-052 and their single-count instances.
`by` should name this review.

**#529: `S2` confirmed.** The score is of the claim, $s(102) \le 10.605828696455852$, a
side the record already holds a smaller certificate below (T-146, $2.43 \times 10^{-11}$
smaller): a citable detail of the case that moves no bound and no theorem, as T-120
(`S2`, a reported exact form of a packing the record already credits), T-137 and T-150
(`S2`, refinements at the scale of $10^{-10}$ and $10^{-8}$) are.
That the arrangement is a different one of ry-xu’s design, independently found, is
credit and lineage, which the entry states and the score does not reward; a new
arrangement that moved a case ceiling would be `S3` (T-149), and this one moves none.
Not `S1`: the anchor fits an entry that establishes nothing the record did not hold, and
the record held no exact certificate of this arrangement.
`by` should name this review.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling on
layer 4 `dead83f0e` and every report pending on 12 October, each comparison exact.
Sides are shown rounded up at sixteen places.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | House to adopt |
| --- | --- | --- | --- |
| 175 | 13.7671207246923133, ry-xu improved by Francisco Couzo (T-140); on `main` 13.7688992766137689, ry-xu (T-125) | #528, 13.7641743174865967; Couzo’s `337078c` 13.7671190241983643, unregistered | #528, Daniil Ostashev; then T-140, then Couzo’s `337078c` certificate in its packet, then T-125 |
| 232 | 15.7674283499418417, Nate Chaoweeraprasit (T-136); on `main` the catalogue’s $8 + \tfrac{11}{2}\sqrt2$ with T-136 pending | #528, 15.7641743174865967 | #528, Daniil Ostashev; then T-136 |
| 264 | 16.77817459305203, the catalogue’s $9 + \tfrac{11}{2}\sqrt2$ verified by Evan Daniel’s exact ceiling (T-101) | #528, 16.7747351323878329 | #528, Daniil Ostashev; then T-101 |
| 102 | 10.6058286964315784, ry-xu regularized by Evan Daniel (T-146); on `main` 10.6058286965106059, ry-xu (T-125), with T-146 pending adoption | #529, 10.6058286964558520 | unchanged: T-146; #529 retained and not selected, then T-125 |

At every other count the earlier reviews’ tables stand; at 175, 232 and 264 the earlier
houses stay retained as history, and the case’s reported and verified ceilings move
together. Credit follows the packets: at 175, 232 and 264 Daniil Ostashev takes the
packings and certificates after the methods and pieces his issue names, with Ellsworth,
Schadt, Friedman, de Winter and Daniel acknowledged as the sources of the pieces; at 102
the house keeps its credit, and Rio Calle takes his arrangement and its certificate with
ry-xu named first for the design and width.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry per import**: `E-ostashev-528-exact-feasibility` and
  `E-calle-529-exact-feasibility`, each `assurance: verified`,
  `method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s retained
  certificates or derived fact as `certificate`, the replay commands above,
  `replay_status: passed`, the six verifiers named under Rungs, this review as
  `independence_record` and as `external_review` (`informally-verified`), and
  limitations naming the shared premises, RX-6 and RX-7.
- **On each reported entry** (`E-ostashev-528-certificate-report`,
  `E-calle-529-certificate-report`): `external_review` naming this review, which makes
  it `reviewed`; #529’s typed as the source’s numerical report (RX-3).
- **On each register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, covering both), both test files among the
  controls (`packing/tests/test_upper_bound_reports.py`,
  `packing/tests/test_check_half_angle_area.py`), the significance `by` naming this
  review, and claim, notes and `next_rung` rewritten together: for #528 the measured
  lineage (RX-11) and the AI-assistance statement; for #529 the case’s smaller
  certificate (RX-1, RX-3), the published date (RX-2) and the measured arrangement.
- **On T-149 and `E-ostashev-501-certificate-report`**: the sentence of RX-4.
- **On `think-9fjl`**: the disposition of RX-5.
- **In `source-coverage.yaml`**: the confirming evidence on each import’s source entry;
  #528’s three selected overrides when adopted; #529’s source entry with no override.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no run of
either source’s own checkers or solvers.
No reading of Calle’s private certificate or of his earlier layout, no reading of the
Davidebyzero comment, and no identification of the 38-square block or of Friedman’s
piece in #528’s packings.
No `derive --check` from a Git checkout.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
