# Review: Mishapolk’s Decimal Poses (#470) and Evan Daniel’s n = 126 Certificate

**Date:** 10 October 2026. **Verdict: accepted, for finite feasibility only.** Every
exact witness the two entries would cite proves the upper bound its packet states: the
30 rational witnesses this repository derived from Mishapolk’s decimal centre-and-angle
poses (#470), 28 of them at the counts the issue names, and Evan Daniel’s
`n126_xu.cert`. Both retained receipts reproduce here job for job, the third exact route
of the [first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended for these packets, agrees with both maintained routes at every number they
share, and every #470 witness was derived again here from its pinned upstream file by
separate arithmetic and found to be exactly the witness the receipt decided.
Eleven findings are recorded.
One, RK-1, blocks registering #470 with the text its register plan prints, and not the
bounds: the plan calls the 28 sides improvements and the source’s files rational
certificates, and neither is true.
Each entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` when its
confirming evidence entry and this review are added, #470’s with RK-1’s rewrite; neither
can take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 2026-10-10 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-fvz4`, written by an AI agent (Claude, model Opus 5.5, `claude-opus-5-5`, at the
reasoning setting its harness gave it, which the agent cannot read) prompted separately
from the import lanes that built the two packets, with no shared context.
Its relation to the results is `project`. It moves no rung, writes no register row and
adopts no house; the proposed record changes are listed at the end for the adoption
round.

## Claims Covered

| Entry | Source | Counts | How each side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #470 | [Mishapolk, #470](https://github.com/jlevy/squares/issues/470), `Mishapolk/square-packing-records` at `dd3da5c` | 84, 86, 88, 103, 105, 108, 127, 130, 131, 153, 154, 175, 179, 180, 199, 207, 208, 209, 236, 237, 238, 239, 258, 263, 270, 302, 303, 306 cited; 132 and 267 decided, not cited | 12 places, each the file’s printed side rounded up; the witness’s side is that 12-place decimal exactly |
| T-NNN, trio126 | no issue; `evand/square-packing` at `268af52`, `search/trio126/n126_xu.cert` | 126 | the exact fraction the certificate states, `11742640687119285146522492579501/10^30` |

#470’s sides are tabulated in its
[README](../../../packing/resources/web/mishapolk-decimal-poses-2026-10-09/README.md)
and frozen in its claim record; 132 and 267 are printed in the source’s README, not the
issue, so they are compared and certified but are no part of the entry.
The 18 poses at 343 to 360 lie above the grid bound and are outside this review.
`n126_xu` is the one certificate of
[the trio126 packet](../../../packing/resources/web/evand-trio126-2026-10-09/README.md)
below the case ceiling; its two SQUISH reconstructions, at larger sides, are not
replayed or reviewed.

**Read in full.** The adapters, `decimal_dilation`, `half_angle_tangent`,
`certificate_from_witness`, `read_fact`, `read_facts`, `admit` and the register-plan
renderer of `devtools.upper_bound_reports`; `parse_pose` and the interval helpers of
`devtools.decimal_pose_margins`; the kernel’s `replay_receipt` and `to_witness`; both
packet READMEs, import declarations, acquisition records and claim records; the body of
issue #470 as fetched on this date (`updated_at` 2026-10-09T09:13:18Z); both register
plans; both earlier reviews of this pass and the third route they built,
`devtools/check_half_angle_area.py`; the evidence and verifier schemas.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host at
a load average of 2 to 3.5, at most two worker processes, in a worktree of
`claude/determined-rubin-yjfy2a` at `a3d47c00a` with this review’s change to the third
route added. A replay decides every job of the selected counts again through both
maintained routes, serially in one process, and compares every field of each fresh job
with its retained row except the measured times.

| Command (`python -m …`, `PACKET` the packet’s directory name) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `devtools.upper_bound_reports mishapolk-decimal-poses-2026-10-09 check --n 84 88 103 105 127 132 175 180 199 208 237 238 270 303 306 --replay` | #470’s 45 jobs at 15 counts | all 45 equal | 644.9 s |
| `devtools.upper_bound_reports mishapolk-decimal-poses-2026-10-09 check --n 86 108 130 131 153 154 179 207 209 236 239 258 263 267 302 --replay` | #470’s 45 jobs at the other 15 | all 45 equal | 641.0 s |
| `devtools.upper_bound_reports evand-trio126-2026-10-09 check --replay` | trio126’s 3 jobs | all 3 equal | 11.8 s |
| `devtools.upper_bound_reports PACKET check-claims`, for each | each frozen comparison rebuilt from the witnesses and the houses’ packets | both rebuilt equal | 2.7 s and 0.4 s |
| `devtools.acquire_source PACKET --check`, for each | custody of both packets | `PACKET_MATCHES_ITS_CONTRACT` | 0.1 s each |
| `devtools.decimal_pose_margins check …/receipts/decimal-pose-margins.json --root UPSTREAM` | the interval measurements of the 30 printed poses | `RECEIPT_REPRODUCED` | 4.6 s |
| the same for `decimal-pose-margins-4e1a601-control.json`, root the two `4e1a601` files | the replaced 199 and 263 | `RECEIPT_REPRODUCED` | 0.6 s |
| `devtools.check_half_angle_area decide-imports --workers 2 --imports '#470' trio126 --upstream …` | the third route on 31 witnesses and 186 controls, every cross-check, the 30 upstream derivations, and three arrangement measurements | no disagreement | 40.3 s |
| `devtools.check_half_angle_area decide-imports --workers 2` | the first review’s 27 certificates again, after this extension | no disagreement; the same 880,705 pairs | 51.7 s |

#470 was replayed in full: its 30 counts were split into two halves of nearly equal
recorded route CPU time (629.7 and 631.4 seconds) and run as two processes at once.
`UPSTREAM` is a scratch directory holding the source’s files at `dd3da5c` (below).
Each wall includes the interpreter’s start.
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #470 | 90 | 3,633,654 | 1,261.11 | 3,235.53 | 131.17 |
| trio126 | 3 | 47,250 | 11.48 | 26.27 | 10.76 |

## From Certificate to Bound

Each witness gives a rational side $S$ and, for each square, a rational centre $(x, y)$
in $[0, S]^2$ and a rational rotation: $t = \tan(\theta/2)$ in `n126_xu.cert`, the basis
$(\cos\theta, \sin\theta)$ in #470’s derived facts.
The bound $s(n) \le S$ follows from the four facts the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md#from-certificate-to-bound)
sets out: unit squares, exactly $n$ of them, each in the closed box, interiors pairwise
disjoint.
Every route decides all four in exact `Fraction` arithmetic and rounds, dilates
or tolerates nothing.

**The box convention does not matter here.** No square touches a wall on any route, and
every positive clears every wall and every pair by a positive amount:

| Import | Least wall clearance | Least separating-axis gap | Least Euclidean distance (third route) |
| --- | --- | --- | --- |
| #470 | $4.74 \times 10^{-16}$ at 84, $6.66 \times 10^{-16}$ at 238, $2.89 \times 10^{-15}$ at 131, at least $7.18 \times 10^{-15}$ elsewhere | $6.59 \times 10^{-16}$ at 238 | $6.591505 \times 10^{-16}$ at 238 |
| trio126 | exactly $1/(2 \cdot 10^{20})$ | $9.99999999999999 \times 10^{-21}$ | $1.000000 \times 10^{-20}$ |

So the closed squares are pairwise disjoint and inside the open box at every count, and
each bound holds under any of the usual conventions.

## The #470 Adapter

The source’s files are not certificates.
Each is David Ellsworth’s text format, `s: SIDE` and then `Square K: x=X, y=Y, deg=D`,
centres in $[-s/2, s/2]^2$ and angles in degrees, at 16 decimals or 36 at 132, 199, 263
and 267. The cosine and sine of a decimal angle are not rational, and the digits are
rounded. `upper_bound_reports.decimal_dilation` makes an exact witness by two declared
steps, reading only the two options each declaration row names:

1. **Dilation.** Every centre is scaled by $\lambda = S_n / s$ about the box centre, $s$
   the printed side and $S_n$ the issue’s 12-place ceiling, so the side becomes $S_n$
   exactly. $\lambda - 1$ runs from $1.33 \times 10^{-15}$ (238) to
   $7.89 \times 10^{-14}$ (108).
2. **Tangent rounding.** Each $t = \tan(\theta/2)$ is rounded down at 32 decimals,
   decided by an outward-rounded mpmath enclosure; at 0 and $\pm 90$ degrees it is
   exactly 0 or $\pm 1$.

The centres are then moved by $S_n/2$ into $[0, S_n]^2$.

**Soundness does not rest on either step.** Every route decides the exact witness in
full, so a wrong step could only yield a witness that fails, or one that passes and is a
packing at $S_n$ all the same.
What the steps bear on is attribution: whether the witness is Mishapolk’s pose.

**Dilation about the centre never harms a packing, and it repairs small defects.** Write
$d = c_j - c_i$ for two centres, and $K$ for the Minkowski sum of the two squares placed
at the origin: convex, centrally symmetric, with $0$ inside.
The interiors are disjoint iff $d \notin \operatorname{int} K$. If $\lambda d$ were in
$\operatorname{int} K$ for some $\lambda \ge 1$, then
$d = \lambda^{-1}(\lambda d) + (1 - \lambda^{-1}) \cdot 0$ would be too, by convexity;
so a disjoint pair stays disjoint.
Quantitatively, along any unit normal $u$ the separation $u \cdot d - w_i(u) - w_j(u)$
gains $(\lambda - 1)\, u \cdot d$, about $\lambda - 1$ for touching neighbours, whose
centres lie about 1 apart along their contact normal.
A square of half-extent $h = (|\cos\theta| + |\sin\theta|)/2 \ge 1/2$ has wall clearance
$\lambda(s/2 - |x| - h) + (\lambda - 1)h$ after dilation, a gain of at least
$(\lambda - 1)/2$. That is what the interval receipt shows: at 238 a printed overlap of
$-6.72 \times 10^{-16}$ becomes a gap of $6.59 \times 10^{-16}$ under
$\lambda - 1 = 1.33 \times 10^{-15}$, and at 84 a wall crossing of
$-2.48 \times 10^{-16}$ becomes a clearance of $4.74 \times 10^{-16}$ under
$1.44 \times 10^{-15}$. No centre moves by more than $10^{-12}$.

**The tangent rounding moves nothing that matters.** $\theta = 2\arctan t$ has
derivative at most 2, so rounding $t$ down by less than $10^{-32}$ turns a square by
less than $2 \times 10^{-32}$ radians and moves a corner, at distance $\sqrt2/2$ from
its centre, by less than $1.5 \times 10^{-32}$, against a least margin of
$4.7 \times 10^{-16}$. At 84 and 238, where the least margins lie, the routes’ margins
equal the interval receipt’s at $S_n$ to the three digits the README prints.

**The printed poses themselves are not packings at 19 counts** (RK-2). The interval
receipt, reproduced here from the fetched files, proves that at the printed side 12
poses have overlapping pairs, by at most $1.28 \times 10^{-15}$, and 17 have corners
outside the box, by at most $1.2 \times 10^{-15}$; 11 are packings.
Every one of the 30 is a packing after the dilation.
The issue calls each $S_n$ “the certified side length of each packing, rounded up”; the
bound $s(n) \le S_n$ holds, but through a step the source does not state.

**Every derived fact is exactly the witness the receipt decided, and exactly what its
upstream file yields.** The third route read each fact as its bases state them and found
it equal, side and every centre and rotation, to the positive job’s retained checker
input at all 30 counts.
It then derived each witness again from the pinned decimal file with its own parser, its
own dilation $S_n / s$ (equal to the declared option at all 30) and its own tangent
floor, computed in `decimal` arithmetic by Machin’s formula for $\pi$ and Taylor series
for sine and cosine at 72 working digits and above, with an explicit error bound, rather
than by mpmath intervals.
All 5,677 squares agree exactly.
The tests also hold the two floors to each other on five fixed angles, and this route’s
to the known expansions of $\tan 15^\circ$ and $\tan 30^\circ$.

## Derived-Fact Custody

The Mishapolk tree has no licence file and its README states no reuse terms.
The packet retains no upstream byte: every file is pinned by SHA-256 and Git blob, and
the facts are this repository’s derivation.
`read_fact` holds each fact to its own rebuild offline; nothing retained binds it to the
bytes it came from, and `derive --check` needs a checkout (RK-3, as RI-2 of the first
review).

For this review the 30 in-horizon pose files and the README were fetched over HTTPS from
`raw.githubusercontent.com` at `dd3da5c753c5ded6cb3b89476193b7b801005415` into scratch
space, outside the repository, and read as data; nothing fetched was run.
All 31 have the SHA-256 the packet pins.
`decide-imports --upstream` held each fact to its file as above, and found the two
README-printed sides, 11.986956226066 and 16.838828608296, in the README’s rows for 132
and 267: the 32 upstream checks the command reports.
Each offered side is the file’s printed side rounded up at 12 places, the issue’s
definition of $S_n$, at all 30. The issue body lists, beside each of its 28 file names,
exactly the SHA-256 that file has at `dd3da5c`, and its table prints the 28 offered
sides; the issue’s own pin string, `dd3da5c7b39f3796d19e0970bc2350ef9ea14ad`, has 39 hex
digits and names no commit, and the packet’s resolution to `dd3da5c753c5…` stands
(RK-5). The `4e1a601` files of 199 and 263, fetched the same way for the control
receipt, have the digests its README records.

`n126_xu.cert` is retained under the MIT licence, bound to its Git blob by
`acquire_source.check`. Fetched at `268af52`, it is byte-identical to the retained file,
and `SHA256SUMS` there lists its digest.

## Whose Arrangements These Are

Credit at the counts where these witnesses would become houses turns on whose packing
each is, and neither source says.
The third route measured each against the certificate its arrangement would be credited
to: under each of the box’s eight symmetries, every square matched to the nearest centre
of the other packing, kept only where the matching is one to one.

| Witness | Against | Best symmetry | Squares moved beyond $10^{-9}$ | Largest move | Largest turn (sine) |
| --- | --- | --- | --- | --- | --- |
| #470, n = 103 | Ryan Xu’s (T-125) | identity | 0 of 103 | $2.10 \times 10^{-10}$ | $2.49 \times 10^{-11}$ |
| #470, n = 258 | SQUISH’s update (T-115) | identity | 0 of 258 | $4.29 \times 10^{-10}$ | $1.43 \times 10^{-9}$ |
| `n126_xu` | Ryan Xu’s (T-125) | identity | 68 of 126 (61 beyond $10^{-3}$, 16 beyond $10^{-2}$) | $5.99 \times 10^{-2}$ | $5.87 \times 10^{-2}$, 13 squares beyond $10^{-6}$ |

So #470’s 103 is Ryan Xu’s packing and its 258 is SQUISH’s, each refined in precision by
$1.49 \times 10^{-10}$ and $1.15 \times 10^{-12}$ in side, and the houses should credit
them so (RK-6). `n126_xu` is a different packing of the same arrangement: 58 squares sit
where Ryan Xu’s do, to $10^{-9}$, and 68 others are displaced by up to 0.06 and turned
by up to about $3.4^\circ$, as the source’s reconstruction from a picture and its
statement that the local minimum is strict only modulo flat motions would allow (RK-7).
Its side is below Ryan Xu’s by $9.25 \times 10^{-11}$ because T-125 certifies a binary64
solution dilated by $10^{-12}$, while `n126_xu` lies $1.17 \times 10^{-19}$ above the
`exactsolve` side $15/2 + 3\sqrt2$, which is not itself certified.
These are measurements for credit and decide nothing.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify` | the facts read by `certificate_from_witness`, or the trio126 parse; the half-angle map; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same reading, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (proposed V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `sqpack.yamlio`; `json`, `csv`, `gzip`, `hashlib`, `decimal` | `Fraction` and the formats’ meaning only |
| the #470 adapter (proposed V-upper-bound-reports) | nothing; it generates the witness | `upper_bound_reports.decimal_dilation`, `decimal_pose_margins.parse_pose`, mpmath intervals | none with the third route’s re-derivation |
| interval margins (`devtools.decimal_pose_margins`) | the printed poses at $s$ and at $S_n$, by outward-rounded intervals at 60 digits | mpmath intervals | the parse with the adapter |

The custody of the bytes rests on each packet’s own admission (`acquire_source.check`,
and for the facts `read_facts`), which the third route calls before it reads anything
and from which it decides nothing.

**For #470 the generator of the exact witness is this repository** (RK-4). The routes
confirm the project’s own construction from the source’s numbers, not a certificate the
source wrote; the source’s checkers, Ellsworth’s `check_packing.py` at precision 40 with
$\varepsilon = 10^{-14}$ and an unnamed 60-digit separating-axis check, were not run,
and their tolerance is what accepted the 19 printed poses that are not packings.
Against the adapter, the third route’s re-derivation is the independent check.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the sources’ own programs ran: Mishapolk’s copy of `check_packing.py`, Daniel’s
`verify_cert.py` and `verify_cert2.py`, `fq`, `exactsolve` and `img2packing.py`. The KKT
statements of #470, and the local-minimum, jamming and closed-form statements of
trio126, are source reports and are not decided.
That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, the adapter and its parser
before extending it, so it is not a clean-room implementation; it imports none of their
parsing, deciding or deriving code.
On the 31 witnesses it decided 613,484 pairs, clipping 12,913, and found no overlap and
no square outside the box.

## The Controls

The kernel’s two controls, a duplicated square and a square moved by $S + 2$, are
required on both routes, on the complete pair count, with the negative diagnostic each
is built for; all 62 refused.
They are gross (RK-8, as RD-2 and RI-3). The third route adds its four sharp, two-sided
controls to the same two, each a full decision of the witness: the side reduced by the
least far-wall clearance (accepted) and by $10^{-40}$ more (refused), and the closest
pair translated into contact (that pair accepted) and then $10^{-30}$ of the centre
distance further (refused).
All 186 reached their required outcome, at #470 against margins from
$4.7 \times 10^{-16}$ up.

## Agreement to Every Digit

The third route held each witness to the record and found no disagreement:

- all 31 sides and every centre and rotation equal the maintained routes’ retained
  checker inputs;
- every side equals the exact side of its packet’s frozen claim record, is admitted
  against its print by the route’s own integer ceiling (here, by equality), and equals
  the value the register plan’s claim states at every cited count; the plan claims
  neither 132 nor 267;
- every least wall clearance equals both maintained routes’ exactly, from
  $4.7397 \times 10^{-16}$ at #470’s 84 to $1/(2 \cdot 10^{20})$ at 126;
- every least Euclidean distance, from $6.591505 \times 10^{-16}$ at #470’s 238 to
  $1.000000 \times 10^{-20}$ at 126, is at least the separating-axis gap both maintained
  routes report;
- both receipts’ totals are the numbers the packets print, and the #470 facts are the
  witnesses their pinned files yield.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes each witness against the case record as
it stood at `main` `af17208c0` and against every pending report, each case ceiling
rebuilt from its holder’s own retained packet; `check-claims` rebuilt both equal.
#470’s compares T-128, T-130, T-131 and #476 by their exact sides, and #481 by the
16-place upward ceilings of its claim record, a valid model; every relation with #481 is
decided by at least $6.87 \times 10^{-4}$ (RK-11). trio126 at 126 has no pending report.

The comparison decides the entry’s significance: $S_n$ is the smallest side known only
at 103 and 258. At 84, 86, 105, 108, 127, 131, 175, 180, 270 and 306 an earlier Couzo
certificate (T-128, T-130) is smaller; at 132, 267, 302 and 303 a later report (#476 or
#481) is. At 88, 130, 153, 154, 179, 199, 207, 208, 209, 236, 237, 238, 239 and 263 the
side lies above the case’s verified ceiling, by $2.17 \times 10^{-14}$ (238) to
$3.51 \times 10^{-9}$ (263).

## Findings

**RK-1, blocking for registration as the plan prints it; not for the bounds: #470’s
register plan misstates its evidence.** `register-plan` writes the claim “28 complete
rational source certificates report finite upper-bound improvements at the exact sides
they state”, but the source states decimal poses, the rational witnesses are this
repository’s, and 14 of the 28 sides are not improvements.
Its significance rationale says the sides are “-3.51e-09 to 1.74e-03 below the case
ceilings”, and its notes say “above the case’s ceiling … by -7.53e-13” at those 14:
`upper_bound_reports._comparison` prints the case’s signed difference where it prints a
pending report’s absolute value.
The reported atom `E-mishapolk-470-pose-report` “records the source author’s report of
28 exact rational certificates”, with `reported_method: exact-algebraic` and the derived
facts as its certificate; the source reports decimal poses accepted by a precision-40
check at $\varepsilon = 10^{-14}$. The records lane should write the proposed text below
instead, and the renderer should print an absolute difference and gain a claim form for
an import whose witnesses are derived; trio126’s plan is accurate.

**RK-2, non-blocking: the source’s printed poses are not packings at 19 counts.** As
above. The register must say that the bound rests on this repository’s dilation of the
source’s pose, not that the source’s files are valid; credit is unaffected, since the
dilation moves no centre by as much as $10^{-12}$.

**RK-3, non-blocking: no retained check binds a derived fact to its upstream bytes**
(RI-2, unchanged). Closed at this date for all 30 by `decide-imports --upstream`; the
confirming evidence should cite this review for the binding.

**RK-4, non-blocking: for #470 the witness’s generator is this repository.** The
confirming evidence is `independent-implementation` with respect to the source’s code
and decides the adapter’s output in full, but it must say that the certificate is the
project’s derivation and that no source checker ran.

**RK-5, non-blocking: the issue’s pin names no commit.** Resolved by digest, as the
packet did and as checked here against the issue body.

**RK-6, non-blocking: #470’s 103 and 258 are earlier packings refined.** Measured above.
The issue leaves credit with discoverers without saying which count started where;
adoption at 103 should credit Ryan Xu’s packing and at 258 SQUISH’s (Nate
Chaoweeraprasit), each refined by Mishapolk.

**RK-7, non-blocking: `n126_xu` is not Ryan Xu’s certificate refined in place.** It is
the same arrangement with 68 squares elsewhere, and its side improvement of
$9.25 \times 10^{-11}$ is one of certified precision.
Its packet’s phrase “a precision refinement of the same arrangement” holds for the side,
not the poses. Credit stays as the plan writes it: Ryan Xu’s arrangement, Evan Daniel’s
reconstruction and certificate.

**RK-8, non-blocking: the kernel’s controls are gross** (RD-2, RI-3, unchanged).

**RK-9, non-blocking: the reviewer and one producer share a model family.** The trio126
commit names Claude Opus 5.5 as co-author and its `CREDITS.md` says the repository’s
work was produced by Claude; this review and the third route are Claude’s. #470
discloses Gemini 3.8 assistance.
The decisions are exact, but `V4`/`C4` needs a distinct reviewer in any case.

**RK-10, non-blocking for this claim: no private-worker custody at either packet**
(RI-5). The adoption round should close it before any house moves.

**RK-11, non-blocking: #470 compares #481 by its 16-place ceilings.** No relation
changes; as RI-1 advised for #476, a `HOUSES` reader of #481’s packet would compare
exactly.

## Rungs

**#470: `V3`/`C3`** at its 28 cited counts, once RK-1’s text replaces the plan’s.
Machine-replayed here: all 30 witnesses and their 60 kernel controls on both maintained
routes, and the 30 with their 180 controls on the third route, with every witness
derived again from its pinned upstream file; a certificate, a replay command, a passing
replay and retained controls; reviewed adversarially here.
132 and 267 are confirmed by the same evidence and cited by no entry.

**trio126: `V3`/`C3`** at 126, for the same reasons over one certificate, two kernel
controls and six third-route controls.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling at
`main` `af17208c0` (unchanged since `657cc4861` at these counts) and every report
pending on 2026-10-10, merged with the first imports review’s table, which this one
replaces. #470’s sides are now exact witnesses, reviewed here, and every comparison is
exact. Sides are shown rounded up at sixteen places, #470’s as printed.

| n | Case ceiling, house | Other exact certificates reviewed | #470 | House to adopt |
| --- | --- | --- | --- | --- |
| 70 | 8.8809603717088810, Ryan Xu (T-125) | #483, 8.8809603715662510 | none | #483, Ryan Xu’s arrangement refined by Eric Deleeuw |
| 84 | 9.6980520605096981, Ryan Xu | T-130, 9.6979347990149214 | 9.697934799017 | T-130 |
| 86 | 9.8205657300098206, Ryan Xu | T-130, 9.8205354074967423 | 9.820535407499 | T-130 |
| 88 | 9.8824510304812469, Gupta (T-127) | none | 9.882451030482, above the case | the case’s, unchanged |
| 103 | 10.6792320475106793, Ryan Xu (T-125) | none | 10.679232047362 | #470, crediting Ryan Xu’s packing, refined by Mishapolk |
| 105 | 10.7906765754107907, Ryan Xu | T-130, 10.7893037837481589; T-128, 10.7906182681071446 | 10.789303783751 | T-130; T-128’s stays verified, not selected |
| 108 | 10.9048247851109049, Ryan Xu | T-128, 10.9048210123203565 | 10.904821012324 | T-128 |
| 126 | 11.7426406872117427, Ryan Xu (T-125) | `n126_xu`, 11.7426406871192852, this review | none | `n126_xu`, crediting Ryan Xu’s arrangement and Evan Daniel’s reconstruction |
| 127 | 11.8109366475118110, Ryan Xu | T-128, 11.8108787875891799 | 11.810878787590 | T-128 |
| 130 | 11.9044830325157865, Gupta (T-127) | none | 11.904483032516, above the case | the case’s, unchanged |
| 131 | 11.9511500449119512, Ryan Xu (T-125) | #481, 11.9496595880358604; T-128, 11.9511053894146775 | 11.951105389418 | #481; T-128’s stays verified, not selected |
| 132 | 11.9913278876915015, T-098 | #476, 11.9869541936403928; T-131, 11.9870993322450633 | 11.986956226066, not cited | #476, crediting Mishapolk’s packing as its start; T-131’s stays verified |
| 153 | 12.8796793733293146, Gupta (T-127) | #481, 12.8720298490811809 | 12.879679373332, above the case | #481 |
| 154 | 12.9265622458523470, Gupta (T-127) | #481, 12.9230702023011408 | 12.926562245853, above the case | #481 |
| 155 | 12.9525032026045129, SQUISH (T-115) | T-128, 12.9524989440140074; Daniel’s equal side | none | T-128, Daniel’s as an equal-side confirmation |
| 175 | 13.7688992766137689, Ryan Xu | T-130, 13.7671551635425492 | 13.767155163551 | T-130 |
| 179 | 13.8837954905108985, Gupta (T-127) | none | 13.883795490512, above the case | the case’s, unchanged |
| 180 | 13.9176534174501843, Gupta (T-127) | T-128, 13.9169935224778325 | 13.916993522482 | T-128 |
| 199 | 14.6175721735928069, Gupta (T-127) | none | 14.617572173597, above the case | the case’s, unchanged |
| 207 | 14.8879922583026574, Gupta (T-127) | #481, 14.8855063088416777 | 14.887992258303, above the case | #481 |
| 208 | 14.9245187720293559, Gupta (T-127) | none | 14.924518772030, above the case | the case’s, unchanged |
| 209 | 14.9496179522003981, Gupta (T-127) | #481, 14.9462236544879195 | 14.949617952201, above the case | #481 |
| 228 | 15.6046024545460570, Daniel’s exact optima | T-128, 15.6046014757296743 | none | T-128 |
| 232 | 15.7781745930520228, Daniel’s exact ceiling of the Kingbird packing (T-101) | #481, 15.7674283499418417 | none | #481 |
| 236 | 15.8678008394199166, Gupta (T-127) | #481, 15.8639557471592678 | 15.867800839421, above the case | #481 |
| 237 | 15.9036762351891381, Gupta (T-127) | #481, 15.9029892208749656; #476, 15.9036709055806231 | 15.903676235190, above the case | #481; then #476 |
| 238 | 15.9261468570109784, Gupta (T-127) | none | 15.926146857011, above the case | the case’s, unchanged |
| 239 | 15.9493131697276962, Gupta (T-127) | none | 15.949313169728, above the case | the case’s, unchanged |
| 258 | 16.5634480021391540, SQUISH (T-115) | none | 16.563448002138 | #470, crediting SQUISH’s packing, refined by Mishapolk |
| 259 | 16.6025684904933646, T-098 | #481, 16.5913781454976982 | none | #481 |
| 263 | 16.7404196795387766, SQUISH (T-116) | #481, 16.7331660078998839; #476, 16.7404126538191566 | 16.740419683047, above the case | #481; then #476 |
| 267 | 16.8388319611168389, Ryan Xu (T-125) | #476, 16.8388152699482623 | 16.838828608296, not cited | #476 |
| 269 | 16.9059670585838410, T-098 | #481, 16.9015135821891329 | none | #481 |
| 270 | 16.9378072284460292, Daniel (T-119) | #481, 16.9297801262411717; #476, 16.9367200311210158; T-130, 16.9367230228761835 | 16.936723155038 | #481; then #476, then T-130 |
| 292 | 17.5972493911564651, Rehwaldt (T-117) | #481, 17.5913781454979008 | none | #481 |
| 302 | 17.8813062180958085, SQUISH (T-116) | #481, 17.8720298490811800 | 17.881306218091 | #481 |
| 303 | 17.9203123729203498, SQUISH (T-113) | #481, 17.9130654627385328; #476, 17.9174439254942359 | 17.920312372919 | #481; then #476 |
| 305 | 17.9529594590155280, T-098 | #481, 17.9511961441473858 | none | #481 |
| 306 | 17.9634381397640029, Daniel’s exact optima | T-128, 17.9634337174914258 | 17.963433717497 | T-128 |
| 307 | 17.9810305486333107, T-098 | #481, 17.9808627840546911 | none | #481 |
| 308 | 18, the grid (`E-basic-grid-upper`) | #484, 17.9993098551627480 | none | #484 |

“Gupta (T-127)” is SQUISH’s packing refined by Siddharth Gupta, and T-098 Evan Daniel’s
exact optimum of Francisco Couzo’s packing.
As the first imports review recorded, #476’s certificates at 259, 269, 305 and 307 equal
the T-098 ceiling exactly and are not candidates, and #484’s 343 and 344 stay dated
beyond-horizon rows with no house.
Where #470 is below the case but not the smallest, its witness stays verified and is not
selected. At every count the earlier house stays retained as history, and the case’s
reported and verified ceilings move together.
House adoption waits for [#403](https://github.com/jlevy/squares/pull/403), as the
coordinator recorded on `think-fvz4`, and for private-worker custody (RK-10).

## Proposed Record Changes

For the adoption round; this review writes none of them.
`T-NNN-470` and `T-NNN-126` below stand for the ids the records lane assigns.

```yaml
# results.yaml, the #470 entry (fields that differ from its register plan)
- id: T-NNN-470
  headline: Exact witnesses at Mishapolk's printed ceilings, smallest known at 103 and 258
  claim: >-
    Exact rational witnesses derived here from Mishapolk's dd3da5c decimal centre-angle
    poses prove s(n) <= S_n at the 28 counts issue 470 names, S_n the printed side rounded
    up at 12 decimals: s(84) <= 9.697934799017, s(86) <= 9.820535407499,
    s(88) <= 9.882451030482, s(103) <= 10.679232047362, s(105) <= 10.789303783751,
    s(108) <= 10.904821012324, s(127) <= 11.810878787590, s(130) <= 11.904483032516,
    s(131) <= 11.951105389418, s(153) <= 12.879679373332, s(154) <= 12.926562245853,
    s(175) <= 13.767155163551, s(179) <= 13.883795490512, s(180) <= 13.916993522482,
    s(199) <= 14.617572173597, s(207) <= 14.887992258303, s(208) <= 14.924518772030,
    s(209) <= 14.949617952201, s(236) <= 15.867800839421, s(237) <= 15.903676235190,
    s(238) <= 15.926146857011, s(239) <= 15.949313169728, s(258) <= 16.563448002138,
    s(263) <= 16.740419683047, s(270) <= 16.936723155038, s(302) <= 17.881306218091,
    s(303) <= 17.920312372919 and s(306) <= 17.963433717497. Each witness dilates the
    printed centres about the box
    centre by S_n/s and rounds each half-angle tangent down at 32 decimals; at the printed
    side 19 of the 30 poses within the corpus are not packings, by up to 1.3e-15. S_n is
    the smallest known side only at 103 and 258; at 88, 130, 153, 154, 179, 199, 207, 208,
    209, 236, 237, 238, 239 and 263 it is not below the case's verified ceiling.
  verification: V3
  confirmation: C3
  significance:
    rationale: >-
      Smaller finite construction sides at n = 103 (1.49e-10 below the case ceiling) and
      258 (1.15e-12), each an earlier packing refined; at the other 26 counts a proved
      bound that a standing, earlier or later certificate betters. No lower bound or
      optimum.
  evidence: [E-mishapolk-470-pose-report, E-mishapolk-470-exact-feasibility]
  controls:
    - packing/tests/test_upper_bound_reports.py
    - packing/tests/test_check_half_angle_area.py
  reviews:
    - path: docs/project/reviews/review-2026-10-10-upper-bound-imports-470-and-trio126.md
      kind: adversarial
      reviewer: Claude (Opus 5.5, claude-opus-5-5), the W2 review lane of the 2026-10-10 intake pass
      reviewer_kind: ai
      relation: project
      date: '2026-10-10'
      scope: >-
        The 30 exact witnesses derived from Mishapolk's decimal poses at dd3da5c (#470) and
        Evan Daniel's n126_xu.cert: both receipts replayed, a third exact route, the
        witnesses derived again from their pinned upstream files.
      verdict: accepted
  next_rung: >-
    V4/C4 needs a second accepted adversarial review by a distinct reviewer and a
    retained human oversight record. Adopt houses at 103 and 258 only, crediting Ryan
    Xu's and SQUISH's packings, after #403 and private-worker custody.

# results.yaml, the trio126 entry (fields that differ from its register plan)
- id: T-NNN-126
  verification: V3
  confirmation: C3
  evidence: [E-evand-trio126-certificate-report, E-evand-trio126-exact-feasibility]
  controls:
    - packing/tests/test_upper_bound_reports.py
    - packing/tests/test_check_half_angle_area.py
  reviews: [the same review entry as above]
  next_rung: >-
    V4/C4 as above. Adopt n126_xu as the house at 126 after #403 and private-worker
    custody, crediting Ryan Xu's arrangement and Evan Daniel's reconstruction; its
    poses differ from T-125's at 68 squares.

# evidence.yaml
- id: E-mishapolk-470-pose-report        # replaces the plan's text
  claim: upper-bound
  scope: {n_values: [84, 86, 88, 103, 105, 108, 127, 130, 131, 153, 154, 175, 179, 180, 199,
                     207, 208, 209, 236, 237, 238, 239, 258, 263, 270, 302, 303, 306]}
  assurance: reported
  reported_method: numerical-multiprecision
  performed_by: source-author
  relationship_to_generator: same-implementation
  origin: external
  novelty: previously-published
  source_key: '[Mishapolk decimal poses 2026-10-09]'
  certificate: packing/resources/web/mishapolk-decimal-poses-2026-10-09/acquisition/sources.json
  replay_status: not-attempted
  verifiers: []
  source_reviewed: '2026-10-10'
  limitations: >-
    The author reports decimal centre-angle poses at dd3da5c, accepted by David
    Ellsworth's check_packing.py at precision 40 and epsilon 1e-14 and by an unnamed
    60-digit separating-axis check. No upstream byte is retained. At the printed side 19
    of the 30 in-horizon poses are interval-certified here not to be packings; the bound
    rests on the separate confirming entry's derived witnesses.
  external_review:
    state: informally-verified
    date: '2026-10-10'
    reviewed_by: Claude Opus 5.5, W2 review lane of the 2026-10-10 intake pass
    note: docs/project/reviews/review-2026-10-10-upper-bound-imports-470-and-trio126.md
- id: E-mishapolk-470-exact-feasibility
  claim: upper-bound
  scope: {n_values: [84, 86, 88, 103, 105, 108, 127, 130, 131, 132, 153, 154, 175, 179, 180,
                     199, 207, 208, 209, 236, 237, 238, 239, 258, 263, 267, 270, 302, 303, 306]}
  assurance: verified
  method: exact-algebraic
  performed_by: repository
  relationship_to_generator: independent-implementation
  origin: replayed-here
  novelty: previously-published
  source_key: '[Mishapolk decimal poses 2026-10-09]'
  certificate: packing/resources/web/mishapolk-decimal-poses-2026-10-09/facts/
  replay: >-
    From packing with project Python 3.14: python -m devtools.upper_bound_reports
    mishapolk-decimal-poses-2026-10-09 check --replay (all 90 jobs, both maintained
    routes), and python -m devtools.check_half_angle_area decide-imports --imports '#470'
    trio126, with --upstream mishapolk-decimal-poses-2026-10-09 DIR for the derivation
    from the pinned files.
  replay_status: passed
  verifiers: [V-sqpack-verify, V-check-rational-witness-independent,
              V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area]
  independence_record: docs/project/reviews/review-2026-10-10-upper-bound-imports-470-and-trio126.md
  source_reviewed: '2026-10-10'
  limitations: >-
    The 30 witnesses are this repository's derivation from the source's decimal poses: centres
    dilated about the box centre by S_n/s, half-angle tangents rounded down at 32 decimals.
    All 30 positives pass three exact routes and all 60 kernel and 180 sharp controls reach
    their required outcomes; the least wall clearance is 4.74e-16 and the least pair gap
    6.59e-16. Each fact was derived again from its pinned upstream file by separate
    arithmetic on 2026-10-10; no retained check binds it to those bytes. The kernel's
    controls are gross; the third route's are sharp. No source checker ran. 132 and 267
    are confirmed and cited by no entry. Finite feasibility only.
  external_review:
    state: informally-verified
    date: '2026-10-10'
    reviewed_by: Claude Opus 5.5, W2 review lane of the 2026-10-10 intake pass
    note: Accepted finite feasibility; see the review for RK-1 to RK-11.
- id: E-evand-trio126-exact-feasibility
  claim: upper-bound
  scope: {n_values: [126]}
  assurance: verified
  method: exact-algebraic
  performed_by: repository
  relationship_to_generator: independent-implementation
  origin: replayed-here
  novelty: previously-published
  source_key: '[Daniel trio126 2026-10-09]'
  certificate: packing/resources/web/evand-trio126-2026-10-09/source/search/trio126/n126_xu.cert
  replay: >-
    From packing with project Python 3.14: python -m devtools.upper_bound_reports
    evand-trio126-2026-10-09 check --replay, and python -m devtools.check_half_angle_area
    decide-imports --imports trio126.
  replay_status: passed
  verifiers: [V-sqpack-verify, V-check-rational-witness-independent,
              V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area]
  independence_record: docs/project/reviews/review-2026-10-10-upper-bound-imports-470-and-trio126.md
  source_reviewed: '2026-10-10'
  limitations: >-
    One certificate, its two kernel and six sharp controls, on three exact routes; least wall
    clearance 1/(2*10^20), least pair gap 9.99999999999999e-21. The retained file equals the
    upstream file at 268af52. The source's checkers, exactsolve and its local-minimum and
    closed-form statements were not run or decided. Its poses differ from T-125's at 68 of
    126 squares. Finite feasibility only.
  external_review:
    state: informally-verified
    date: '2026-10-10'
    reviewed_by: Claude Opus 5.5, W2 review lane of the 2026-10-10 intake pass
    note: Accepted finite feasibility; see the review.
# and on E-evand-trio126-certificate-report: the same external_review, which makes it reviewed.
```

The two verifier entries the first imports review proposed, V-check-half-angle-area
(`role: decides`) and V-upper-bound-reports (`role: premises`), cover these packets as
well; the third route’s entry should name its #470 re-derivation and arrangement
measurements, and the import module’s that `decimal_dilation` generates #470’s
witnesses. In `source-coverage.yaml`, each source entry gains its confirming evidence.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the sources’ own checkers or solvers, and no statement about the
printed decimal poses beyond the reproduced interval receipt.
No review of #470’s 18 poses beyond the corpus or of trio126’s two SQUISH
reconstructions. No `derive --check` from a Git checkout.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
