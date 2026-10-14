# Review: Evan Daniel’s Rational Upper-Bound Import of 12 October (#552)

**Date:** 12 October 2026. **Verdict: accepted, for finite feasibility only.** The one
certificate the import’s register entry would cite proves the upper bound its packet
states, $s(154) \le 12922566401934059503377267965457/10^{30}$, Evan Daniel’s
`tt_n154.cert` retained byte for byte at `597e660`. The retained receipt reproduces here
job for job, the third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md), given
its roster line for this import and the credit measurements below, agrees with both
maintained routes at every number they share, and every file of the pinned scope was
fetched here at its pin and found at the digest its packet records: the retained
certificate is its upstream file.
The author’s statement that the packing is a different local minimum from SQUISH’s
(T-136) was measured true as far as arrangement goes: no symmetry of the box pairs the
two packings square for square, and under the best placement found 32 of SQUISH’s 154
squares land within $10^{-9}$ of one of these, one of them to the digit.
His statement that the packing descends from Francisco Couzo’s 5 October packing of 155
squares with one square removed is consistent with every measurement made here and
established by none of them: 43 of that packing’s squares reappear to the digit, but so
do 45 of Couzo’s 154, and the round-by-round trace the author names is not published.
Seven findings are recorded, none blocking.
Once registered, as the coordinator’s T-156, with its confirming evidence entry and this
review, the entry can take `V3`/`C3`; its side is the smallest the record holds or has
pending at 154, $5.04 \times 10^{-4}$ below the house (T-136), so the house should move
to it. It cannot take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 2026-10-12 intake continuation
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
the 2026-10-11 pass’s epic, written by an AI agent (Claude Fable 5.1, at extra-high
reasoning effort) prompted separately from the import lane that built the packet
(`think-6no5`, whose commits name Claude Opus 5.5), with no shared context beyond its
committed notes, scratch measurements and register plan; the import lane decided no
geometry. Its relation to the result is `project`. It moves no rung, writes no register
row and changes no case record; it says what the records lane should write.

## Claims Covered

| Entry | Source | Count | How the side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #552 | [Evan Daniel, #552](https://github.com/jlevy/squares/issues/552), `evand/square-packing` at `597e660`, the commit the issue names; the branch head when read, `31523f8`, adds one line to the packer’s log | 154 | the issue prints `12922566401934059503377267965457 / 10^30`, the exact side itself, admitted by equality; it rounds up at 16 places to $12.9225664019340596$ |

The packet is
[evand-n154-2026-10-12](../../../packing/resources/web/evand-n154-2026-10-12/README.md).
The tree is MIT-licensed and the packet retains nine of the thirteen files in its scope:
the certificate, its 80-digit KKT point (`tt_n154.exact.txt`), the binary64 packing it
was solved from, the solver’s report, the regularized drawing of the same packing with
the regularizer’s report, the licence, the credits and the certificate format’s README.
The source’s two checkers are pinned by digest and are byte-identical to the copies the
issue-399 packet retains; the packer’s working log `PACKER.md` and the time-travel
test’s report script are pinned by digest only.

Three things the source publishes are outside the entry and are placed here.
The regularized drawing, `tt_n154_regularized.cert`, is the same packing at the same
exact side, the source’s display view: it keeps 112 of the 154 poses, moves 42 by at
most $0.135$, every one of them a rattler or a flat square of the solver’s report, and
turns only the eight rattlers; it is retained, decided here as a diagnostic, and is no
separate claim. The statements that $S^\ast$ is a KKT point with positive multipliers on
the load-bearing contacts, that the reduced Hessian is positive semidefinite modulo 45
exact flat motions and that a first-order MILP finds the packing jammed in all 98
corner-to-corner branches are a local-optimality report, recorded and not decided.
The time-travel test the packing came from, a pre-registered run of the author’s
size-chaining explorer from the register as it stood on 5 October, is search
methodology; its result as the author’s log states it is quoted under
[Credit and Lineage](#credit-and-lineage), and nothing of it is imported.

**Read in full.** The import lane’s commits `f7c9b24ec` and `6a913c1c6`: the packet’s
README, declaration, acquisition record, manifest and claim record, the nine retained
files, the receipt, the `HOUSES` reader and the packet’s tests; the lane’s bead notes,
scratch lineage measurements, third-route run and register plan; issue #552 and its
comment of 14:13 UTC; the pinned `PACKER.md` (its time-travel entries) and
`timetravel.py`, fetched here and read as data, not run; the pinned commit’s message;
the #528/#529 review and the first imports review; the review of Evan Daniel’s exact
optima (T-098); [epistemics.md](../../../epistemics.md) on the rungs, review records,
credit and significance; the significance review of 11 October; and the case record
[n-154.md](../../../packing/frontier/n-154.md).

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 7 to 14, one worker process throughout, in a
worktree at the import lane’s `6a913c1c6` with this review’s change to the third route
added. A replay decides every job of the packet again through both maintained routes,
serially in one process, and compares every field of each fresh job with its retained
row except the measured times.

| Command (`python -m devtools.upper_bound_reports evand-n154-2026-10-12 …`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `check-claims` | the frozen comparison rebuilt from the certificate and the holders’ own packets | rebuilt equal as JSON | 7 s |
| `check --replay` | the 3 jobs: the certificate with its two kernel controls | all 3 equal, “1 certificates and 3 jobs admitted”, exit 0 | 51 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#552' --upstream evand-n154-2026-10-12 DIR --json OUT` | the third route on the certificate and its six controls, every cross-check, the two credit measurements and the lineage measurement, and the retained certificate against its upstream bytes | no disagreement, exit 0 | 25.05 s |

The replay ran 15:31:12Z to 15:32:03Z and the third route 15:35:18Z to 15:35:44Z. The
receipt’s own totals, recomputed by the third route, are the numbers the packet prints:
3 jobs, 70,686 pair decisions, 40.97 route CPU seconds, 80.68 job wall seconds, the
longest job 29.49 seconds.

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. The certificate gives a rational side $S$ and, for each square, a
rational centre $(x, y)$ in $[0, S]^2$ and $t = \tan(\theta/2)$. The bound
$s(154) \le S$ follows from four facts, each decided by every route:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$, so the corners
   $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ form a unit square.
2. **There are exactly 154 of them.** Every reader refuses a count that differs from the
   expected one and any row beyond the 154th; a square listed twice would overlap itself
   and be refused.
3. **Each lies in the closed box $[0, S]^2$**: $h \le x \le S - h$ and
   $h \le y \le S - h$ with $h = (|c| + |s|)/2$, or equivalently every corner in the
   box.
4. **Interiors are pairwise disjoint**, by an edge normal that separates the two squares
   (the maintained routes) or by an intersection of area zero (the third route).

Arithmetic is exact `Fraction` arithmetic throughout; no route rounds, dilates or
tolerates. The guard is in the certificate, as the issue says, and was checked here
without being believed: every centre is the KKT centre of `tt_n154.exact.txt` times
$1 + 10^{-20}$, to the 35 places the certificate prints (the largest deviation is
$5 \times 10^{-36}$), and the side is $\lceil S^\ast (1 + 10^{-20}) \rceil$ at 30
places, $7.45 \times 10^{-31}$ above the product and $1.29 \times 10^{-19}$ above
$S^\ast$. 103 of the squares are upright, their $t$ exactly $0$ where the KKT angles are
within $10^{-78}$ of a multiple of a quarter turn; the other 51 carry rationals $t$ of
up to 36 digits, at angles between $-44.82°$ and $44.75°$. The binary64 input the solver
started from has side $12.922566401936727$, $2.67 \times 10^{-12}$ above $S^\ast$. None
of this enters any decision: the routes decide the certificate as written.

**Nothing touches, so the box convention does not matter.** The source’s README says its
checker holds each square inside the open box; the record’s convention is the closed
box. Every clearance is positive on all three routes, and the third route counts no
square-to-wall clearance of exactly zero:

| Where | Both maintained routes | Third route |
| --- | --- | --- |
| Least wall clearance, the low walls | exactly $1/(2 \cdot 10^{20})$, half the $10^{-20}$ scaling | the same |
| Least far-wall clearance, both axes | not reported | $25000000003727 / (5 \cdot 10^{33}) = 5.0000000007454 \times 10^{-21}$, the scaling’s remainder once the side is rounded up |
| Closest pair | separating-axis gap $9.99999999999998961 \times 10^{-21}$ | Euclidean distance $9.99999999999998961 \times 10^{-21}$, the same rational exactly, between the route’s squares 141 and 145 counted from 0 |

The two measures of the closest pair coincide here because that pair’s nearest points
lie along a separating edge normal; `compare_import` holds only that the distance is at
least the gap. So the closed squares are pairwise disjoint and inside the open box, and
the bound holds under either convention.
The certificate states its centres in $[0, S]^2$; no adapter moves anything.

## Adapters and Admission

The format has one maintained adapter, `evand-cert` in `upper_bound_reports.ADAPTERS`,
and the third route’s own text reader, `parse_certificate`, which read #488’s, #489’s
and #506’s certificates before this one.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `evand-cert` | `search/packer/candidates/tt_n154.cert`, retained | `n S`, then `n` rows `x y t`; blank and `#` lines skipped | the `#` header line naming the checker; `tt_n154.exact.txt`, `tt_n154.input.txt`, the solver’s and the regularizer’s reports; the regularized drawing, decided apart |

**Admission.** The certificate is admitted by equality: the issue prints the exact
fraction, the declaration offers it, and the frozen claim record’s ceiling
$12.9225664019340596$ is its integer ceiling at 16 places, which the third route’s own
ceiling agrees with.
Nothing is printed in a README table or a JSON beside it, so the third route’s
`printed_table_side` and `printed_json_side` check nothing here.

## Custody

All 13 files of the pinned scope were fetched over HTTPS from
`raw.githubusercontent.com` at `597e660` into scratch space, outside the repository,
between 15:30:13Z and 15:30:19Z, and read as data; all 13 have the SHA-256 the packet’s
manifest pins, the nine retained files among them.
`decide-imports --upstream` held the retained certificate to its fetched bytes, byte for
byte: one upstream check.
The two checkers at the pin, `verify_cert.py` and `verify_cert2.py`, have the digests of
the copies the issue-399 packet retains, as the acquisition record says; neither was
run. The branch head was still `31523f8` when checked at 15:35Z, so nothing newer than
the packet’s reading exists upstream.

The two reports the packet retains name their inputs by paths in the author’s own
scratch space, so the binary64 input the certificate was solved from is identified by
`tt_n154.input.txt` alone; its header side, $12.922566401936727$, is the solver report’s
`S_input`.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the `evand-cert` adapter, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same adapter, parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area; its own text reader | `devtools.check_half_angle_area`; `hashlib` | `Fraction` and the format’s meaning only |

The source ran no route of this project.
It reports its own two exact rational checkers, `verify_cert.py` by separating axes and
`verify_cert2.py` by polygon intersection, which share, the issue says, an author and
the certificate format and not their geometry; both are pinned here and neither was run.
So every route here is independently re-implemented with respect to the producer’s
verification.

`upper_bound_reports` owns custody, the adapter, admission, the claim comparison and the
job layout; the kernel owns the two controls and `validate_job`, which both maintained
routes are held to. The custody of the bytes rests on the packet’s own admission
(`acquire_source.check`), which the third route calls before it reads anything and from
which it decides nothing.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the source’s programs ran: not its checkers, not the exact solver that produced
$S^\ast$, not the explorer that produced the packing.
The KKT, Hessian and jamming statements are not decided; nor is the history of the
chain. That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing the extension, so it is not a clean-room implementation; it
imports none of their parsing or deciding code.
On this certificate it decided 11,781 pairs, clipping 338, and found no overlap and no
square outside the box.
It is a second pair-deciding procedure, not a second arithmetic.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3 of the first
imports review, carried as RX-6 and here as RD-6). `validate_job` requires both routes
to refuse each control, on the complete pair count, with the negative diagnostic it was
built for. In the receipt the duplicate’s gap is exactly $-1$ and the moved square lies
$3 + 5 \times 10^{-21}$ outside the box, refusals a binary64 checker with a $10^{-9}$
tolerance would also make.
They show the routes can refuse, not that they decide at the $10^{-20}$ scale where this
certificate lives.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance, $5.0000000007454 \times 10^{-21}$ | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

All six reached their required outcome, on the certificate and, as a diagnostic, on the
regularized drawing.

## Agreement to Every Digit

The third route held the certificate to the record and found no disagreement:

- the side and every centre and rotation equal the maintained routes’ retained checker
  input;
- the side equals the exact side of the packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against the issue’s print by equality;
- the least wall clearance equals both maintained routes’ to every digit;
- the least Euclidean distance equals the separating-axis gap both maintained routes
  report, exactly;
- the receipt’s totals are the numbers the packet prints, and the retained certificate
  is its upstream file.

## The Claims Comparison

The packet’s `acquisition/claims.json` freezes the certificate against the case record
as it stood at the local branch `layer6` at `92649a2eb`, which carries the 2026-10-11
adoption layer and the records to T-155, and against every register entry pending there,
each side rebuilt from its holder’s own retained packet; `check-claims` rebuilt it
equal. Since pull request #518 merged at 15:11Z on 12 October, `main` holds the same
house at 154. Every comparison is exact; the margins are shown at seven significant
figures.

| Against | Holder | Exact side of the other | Relation | Margin |
| --- | --- | --- | --- | --- |
| T-136, the case ceiling on `layer6` and now on `main`, SQUISH’s third request, adopted on 11 October | Nate Chaoweeraprasit (itsnaka) | an 81-digit numerator over an 80-digit denominator, $12.9230702023011408$ at 16 places | below | $5.038004 \times 10^{-4}$, the issue’s $5.04 \times 10^{-4}$ |
| T-127 (#438), the ceiling `main` held until #518, the “12.9265622458523470” the issue says the register still showed | Nate Chaoweeraprasit, improved by Siddharth Gupta | $12926562245852346932527003441777 / 10^{30}$ | below | $3.995844 \times 10^{-3}$ |
| #470, pending, unregistered at this count | Mishapolk | $12926562245853 / 10^{12}$ | below | $3.995844 \times 10^{-3}$ |
| T-115 (#401) | Nate Chaoweeraprasit | $1819251903550235 / 2^{47}$ | below | $3.995844 \times 10^{-3}$ |
| T-113 (#401) | Nate Chaoweeraprasit | $7277982312406737 / 2^{49}$ | below | $5.727256 \times 10^{-3}$ |
| T-098 (#375), Couzo’s 154 solved exactly | Francisco Couzo, improved by Evan Daniel | $12931663721166847019324363825319 / 10^{30}$ | below | $9.097319 \times 10^{-3}$ |
| T-056, the print $12.931663721169976$, rounding up | Francisco Couzo | printed | below | $9.097319 \times 10^{-3}$ |

For the lineage only: Couzo’s 155 as T-098 solved it, the start the comment names, has
side $1295561959213445243801096476729 / 10^{29}$, $3.305319 \times 10^{-2}$ above this
certificate, and David Ellsworth’s catalogue side the issue quotes, $12.93166712962655$,
is $9.10 \times 10^{-3}$ above it.
The register holds six upper-bound entries whose scope includes 154, the six compared
above; no entry of the 2026-10-11 stack layers (T-147 to T-155) and no other open issue
through #552 reports this count.
The certificate is the smallest exact side the record holds or has pending at 154.

## Credit and Lineage

**What the source says.** The issue: the packing came from a test of the author’s
size-chaining explorer, the quality-diversity basin explorer of #465 and #489, restarted
from the register as of 5 October to see how much of the community’s later improvements
it would recover in nine hours; for 154 the starting packings were the register’s 5
October records at 154, 155 and 156, all credited to Francisco Couzo; the chain also
seeds $n$ from the best at $n + 1$ and $n + 2$ with squares removed; it never saw
T-136’s packing; after 26 rounds of four minutes on two cores it ended below T-136;
“please credit the start to Francisco Couzo’s packings”; RMS matching distance per
square 0.319 from T-136’s packing and 0.396 “from the 5 October register packing it
descends from”. The comment of 14:13 UTC: traced round by round with
`search/packer/chain_lineage.py`, the packing does not descend from the 154; it descends
from Couzo’s 5 October packing for 155 (12.9556195921) with one square removed, then 17
productive rounds at 154, 36 explorer moves, mostly angle swaps, plus crossovers and
kicks; “please credit the start to Couzo’s 155”.

The pinned log agrees with the issue and dates it.
`PACKER.md` pre-registers the test under its night plan of 11 October: 29 counts from 84
to 211 whose best improved after the frozen 5 October register, two arms, nine hours,
with the prediction that most counts would not move.
Its interim entry, at 06:50 in the log’s clock (12:50Z, the log’s times running six
hours behind UTC), records 154 below the best known at round 26 of the plain arm, the
certificate valid under both checkers, and “the chain started from the 10-05 packings
and never saw itsnaka’s packing”; its result entry at 07:47 records one full recovery in
29, the 154, which overshot, and that the scheduler spent 28 to 30 rounds on 153 and
154; its submission entry at 08:00 gives the two matching distances, 0.319 from
itsnaka’s packing and 0.396 “from the 10-05 start (Couzo)”, and the KKT, Hessian and
jamming figures the issue repeats.
`chain_lineage.py` is not in the tree at `597e660`, at `31523f8` or at the branch head
when checked at 15:35Z; `chain.py`, `lineage.py`, `lineage_reach.py` and
`parent_retro.py` are, pinned by the commit and neither retained nor read.

**What was measured.** The third route’s `arrangement_gap` tries to match the
certificate to a packing square for square under the best of the box’s eight symmetries,
and `patch_lineage` counts how many of a named parent’s squares reappear in it, centre
within $10^{-9}$ and edge direction within a sine of $10^{-6}$, under a symmetry of the
parent’s box and a translation, evaluating its three most-voted placements; at a coarser
nearness it counts to the eye.
Against the packings the record retains:

| Parent | One-to-one match | Reappear within $10^{-9}$ under the best placement found (to the digit) | Within a tenth of a unit (turned beyond a sine of $10^{-6}$) |
| --- | --- | --- | --- |
| SQUISH’s 154, T-136 | none | 32 of 154 (1) | 123 (32) |
| Couzo’s 154 as T-098 solved it | none | 45 of 154 (45), all upright, under a quarter turn translated by $(-0.0091, -1.0091)$ | 87 (10) |
| Couzo’s 155 as T-098 solved it, the start the comment names | not applicable | 43 of 155 (43), all upright, translated by $(0.9669, -1.0331)$; 40 and 37 under two other placements | 114 (24) |

The import lane also made a scratch measurement with no repository tool, a float optimal
matching over the eight symmetries by corner displacement, best of the four corner
labellings, reported as RMS per square: 0.318 from T-136’s packing (the author’s 0.319),
0.393 from Couzo’s 154 (the author’s 0.396), 0.181 from Couzo’s 155 with 154 of its
squares matched, and, for scale, 0.449 between T-136’s packing and Couzo’s 154. It was
not repeated here and nothing rests on it; it is reported because it is what the issue’s
figures measure.

**What the record can say.** Two things, in two voices.

1. *In its own voice, as measured:* the packing is another arrangement than T-136’s. No
   placement of SQUISH’s packing pairs with it square for square, one square reappears
   to the digit and 32 within $10^{-9}$ under the best placement found; that 123 land
   within a tenth of a unit says the two packings share most of a layout at the eye’s
   scale, as packings of 154 squares in boxes $5 \times 10^{-4}$ apart in side will, and
   says nothing about which came from which.
   So the credit the packet proposes, Evan Daniel for the packing and its certificate,
   is the measured one, and the entry lists no `regularizations` item: this is not a
   regularization, re-solve or refinement of a packing the record credits.
2. *As the author’s statement, with the measurements beside it:* the start is Couzo’s
   155 less one square.
   The measurement by pose cannot tell the 155 from the 154: both leave blocks of
   upright squares in the child to the digit, 43 and 45, which is what a chain that
   keeps untouched blocks from a Couzo start would leave from either, and T-136’s
   packing, which the chain did not see, leaves one.
   At a tenth of a unit the 155 is the nearer of Couzo’s two, 114 squares against 87,
   and the scratch matching says the same, 0.18 against 0.39. That is consistent with
   the comment and with the log; it does not establish descent, which only the trace
   could, and the trace is unpublished (RD-2). The issue’s 0.396 is the distance to
   Couzo’s 154, the packing the comment says is not the parent (RD-1).

So the record credits the start to Couzo’s 5 October packing of 155 squares, as the
author asks, and says in the entry that the identity of the start is the author’s
statement, measured here as consistent and not established.
Credit and lineage follow the source’s own words, never an inference from resemblance
([epistemics.md](../../../epistemics.md#parallel-projects-and-their-credit)), and the
bibliography key’s `credit`, `Daniel after Couzo`, and `lineage`, `builds-on-project`,
are what the issue states: the chain restarted from this project’s register and started
from Couzo’s packings.
One file at the pin says otherwise: the regularizer’s report,
`tt_n154_regularized.json`, lists the packing as `by: ["Francisco Couzo"]`, the credit
the regularizer carried from the start (RD-3); the record follows the issue and the
author may want to align the report.

## AI Assistance

The issue states: “The search code, the run and this request were done with Claude
(Claude Code). Evan Daniel directed and reviewed the work.”
The pinned commit carries Claude Opus 5.5 as co-author, and `CREDITS.md` at the pin says
of the repository’s work that it was “produced by Claude (Anthropic) in a single session
under human direction”.
Of the two checkers the issue says “an author (us) and the certificate format” is what
they share. The register should carry the disclosure as the source gives it, which the
packet and the plan do.
Nothing in the verdict turns on it: the decisions are exact and the routes’ own.
The reviewer, the import lane and the source’s assistant are one model family; the
import lane and the source’s assistant are the same model, and this reviewer a different
one.

## The Dates and the Plan’s Wording

**`attribution.published`.** Stage 3’s rule is “the date the source gives for it, or the
UTC date of the first commit that contains the certificate”.
The source gives none beyond the log’s entries of 12 October, and the first commit is
`597e660` at 2026-10-12T13:58:36Z; the plan’s `2026-10-12` is right, and so is the
bibliography key’s `dated`.

**The generated plan.** Two sentences need changing before the entry is written, and the
stage 4 exit rewrites the claim, notes and `next_rung` together in any case:

- the plan’s `next_rung` dates T-136’s adoption to 12 October; the case record and the
  coverage record date it 11 October, on the adoption layer, and #518 carried it to
  `main` on 12 October (RD-4);
- the plan’s claim says in the record’s voice that “the chain never saw SQUISH’s packing
  (T-136)”; that is the author’s statement, from the issue and the log, and should be
  attributed (RD-5), as the next clause attributes the local-minimum statement.

The template’s pre-review sentences, that the feasibility outcomes are retained
separately and the standing case is unchanged pending review, are right for the plan as
generated and are replaced by the review’s outcome in the reviewed plan, written beside
this review’s scratch outputs for the records lane with the coordinator’s planned id as
a placeholder; the id is taken last, in the commit that registers.

## Findings

**RD-1, non-blocking: the issue’s 0.396 is the distance to Couzo’s 154, not to the
parent the comment names.** The log’s submission entry gives it as the distance “from
the 10-05 start (Couzo)” and the issue as the distance from the packing it descends
from; the comment then names the 155. The lane’s scratch matching gives 0.393 to the 154
and 0.181 to the 155 less one square.
The reply should say so, and the entry should not quote 0.396 as the distance to the
start.

**RD-2, non-blocking: the lineage trace is not published.** `chain_lineage.py`, which
the comment names, is in no commit read here, and the round-by-round trace is nowhere in
the tree; the entry states the start as the author’s statement, and the reply asks for
the script or the trace, as the import lane’s draft already does.

**RD-3, non-blocking: the regularizer’s report credits the packing to Francisco Couzo.**
`tt_n154_regularized.json` at the pin lists `by: ["Francisco Couzo"]`, while the issue
credits the packing to Evan Daniel with the start to Couzo.
The record follows the issue, which is the author’s request; the reply may point the
author at the field.

**RD-4, non-blocking: the plan dates T-136’s adoption to 12 October.** It was adopted on
11 October on the adoption layer and reached `main` with #518 on 12 October; the entry
should say so.

**RD-5, non-blocking: the plan’s claim states in the record’s voice that the chain never
saw T-136’s packing.** Attribute it to the author; what the record measured is that the
packing is another arrangement than T-136’s.

**RD-6, non-blocking: the kernel’s controls are gross** (RI-3, RW-6, RX-6, unchanged).

**RD-7, non-blocking: the exact-reappearance measurement does not identify the start.**
The entry must not say in the record’s own voice that the packing descends from Couzo’s
155, or from any packing, beyond “the author states”; it may say that the measurements
here are consistent with the statement, with the numbers above.

No private-worker custody exists for this certificate; the adoption lane closes it, as
it did for T-154, before the house moves.

## Rungs

**#552: `V3`/`C3`** at 154, once registered with its confirming evidence entry and this
review. Machine-replayed here: the certificate and its two kernel controls on both
maintained routes, and the certificate with its six controls on the third route, with a
certificate, a replay command, a passing replay and retained controls; the retained file
held to its upstream bytes here; reviewed adversarially here.
`V` is the strongest verification anywhere: the source reports two exact checkers of its
own, and the record’s replay is `V3`’s predicate for exact-algebraic evidence of any
origin.

Not `V4`/`C4`: that needs a second accepted adversarial review by a distinct reviewer
and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

**Verdict line for the records lane.**

| n | Import | Rungs | Confirming evidence | `relationship_to_generator` | Verifiers |
| --- | --- | --- | --- | --- | --- |
| 154 | #552 | `V3`/`C3` | `E-evand-552-exact-feasibility` | `independent-implementation`: the source’s checkers are its own two Python scripts, pinned and not run, and the source ran no route here | V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area, V-evand-exact-certificates |

This review is the confirming entry’s `independence_record` and the reported entry’s
`external_review`.

## Significance

The import lane drafted `S3`.

**`S3` confirmed.** A new arrangement, measured as no placement of the packing the case
holds or of Couzo’s 154, $5.04 \times 10^{-4}$ below the case ceiling and the smallest
known at 154: a substantive case result, as T-149 (`S3`, three packings built from
scratch, $7.78 \times 10^{-5}$ to $2.91 \times 10^{-3}$ below their ceilings), T-136
(`S3`, seventeen packings, $1.68 \times 10^{-4}$ to $1.12 \times 10^{-2}$) and T-154
(`S3`, three compositions, $2.95 \times 10^{-3}$ to $3.44 \times 10^{-3}$) are, and as
the explorer’s earlier results T-131 (#465) and T-141 (#489) are.
Not `S2`: the re-solves, regularizations and refinements at `S2` (T-098, T-146, T-150)
keep every square of a packing the record credits, none moved beyond a tenth; here the
nearest credited packing by any measure, Couzo’s 155, leaves at most 114 of its 155
squares within a tenth under one placement and the side moves by $3.3 \times 10^{-2}$.
Not `S4`: one count, one run of a method the register has already scored at its first
instances, and no technique shown reusable by its reuse; the time-travel test is a
statement about the method, which the entry records and the score does not reward.
`by` should name this review.

## Adoption at 154

The smallest exact certificate at the count, against the case’s verified ceiling and
every report pending on 12 October, each comparison exact; sides rounded up at sixteen
places.

| n | Case ceiling, house | Exact certificate reviewed | House to adopt |
| --- | --- | --- | --- |
| 154 | 12.9230702023011408, Nate Chaoweeraprasit (T-136), adopted 11 October and on `main` since #518 | #552, 12.9225664019340596 | #552, Evan Daniel, the start credited to Francisco Couzo’s 155; then T-136, then T-127, T-115 and T-113 as history, verified and not selected |

The case’s reported and verified ceilings move together, and T-136 stays retained with
its replay as history, as T-127 did when T-136 replaced it.
Credit follows the packet: Evan Daniel for the packing and its certificate, after Couzo
for the start, in the source’s words.

## Proposed Record Changes

For the records lane; this review writes none of them.
The reviewed plan beside this review’s scratch outputs carries the text.

- **A confirming evidence entry**, `E-evand-552-exact-feasibility`: `assurance:
  verified`, `method: exact-algebraic`, `performed_by: repository`, `origin:
  replayed-here`, `relationship_to_generator: independent-implementation`, the retained
  certificate as `certificate`, the replay commands above, `replay_status: passed`, the
  six verifiers named under Rungs, this review as `independence_record` and as
  `external_review` (`informally-verified`), and limitations naming the shared premises,
  RD-6 and the unrun source programs.
- **On the reported entry** `E-evand-552-n154-report`: `external_review` naming this
  review, which makes it `reviewed`.
- **On the register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`), both test files among the controls
  (`packing/tests/test_upper_bound_reports.py`,
  `packing/tests/test_check_half_angle_area.py`),
  `packing/devtools/check_half_angle_area.py` and this review among the artifacts, the
  significance `by` naming this review, and claim, notes and `next_rung` rewritten
  together: the adoption date (RD-4), the author’s statements attributed (RD-5, RD-7),
  the measured arrangement and the consistent, unestablished start.
- **In `source-coverage.yaml`**: both evidence entries on the source entry; the selected
  override at 154 when adopted, with T-136’s row superseded by it; the notes naming this
  review.
- **In the case record** `n-154.md`: the house adoption paragraph with its date, the
  front matter’s reported and verified lanes on T-156’s side and evidence, a
  `priority_notes` item for T-136 as the earlier house, and the certificate’s own
  section stating the AI assistance in the source’s terms.
- **In the request record**, #552’s entry: `register: [T-156]`, the summary without the
  0.396 figure as a distance to the start (RD-1), and a reply that asks for the trace
  (RD-2) and points at the regularizer’s credit field (RD-3).

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no run of
the source’s checkers, solver or explorer.
No replay of the chain and no reading of its unpublished trace.
No identification of the start beyond consistency with the author’s statement.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
