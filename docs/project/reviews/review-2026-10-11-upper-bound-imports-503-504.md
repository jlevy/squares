# Review: PingYou Ltd’s Two Rational Upper-Bound Imports of 11 October (#503, #504)

**Date:** 11 October 2026. **Verdict: accepted, for finite feasibility only.** The two
certificates the imports’ register entries would cite prove the upper bounds their
packets state: PingYou Ltd’s n = 207 (#503) and n = 153 (#504). Both retained receipts
reproduce here job for job, the third exact route of the
[first imports review](review-2026-10-10-upper-bound-imports-476-481-483-484.md),
extended for this source’s two formats, agrees with both maintained routes at every
number they share, and each derived fact was held here to the certificate and to the
source’s own witness it was derived beside, fetched at the pin.
The n207’s stated lineage, two placed patches of Ryan Xu’s n70 construction, was
measured true pose by pose against the exact n70 certificate the record credits; the
n153’s was not measured true by pose and is the source’s account of its construction.
Seven findings are recorded, none blocking.
Each entry, once registered (its `T-NNN` is to be assigned), can take `V3`/`C3` when its
confirming evidence entry and this review are added; neither can take `V4`/`C4` from
this review alone.

This is the stage 4 review lane (W2) of the 2026-10-11 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-720n`, written by an AI agent (Claude, at extra-high reasoning effort, a
different model from the import lane’s) prompted separately from the import lane that
built the two packets (`think-0zd4`, `think-4znu`), with no shared context beyond their
committed notes. Its relation to the results is `project`. It moves no rung, writes no
register row and adopts no house; the proposed record changes are listed at the end for
the records lane.

## Claims Covered

| Entry | Source | Count | How the side is printed, and admitted |
| --- | --- | --- | --- |
| T-NNN, #503 | [PingYou Ltd, #503](https://github.com/jlevy/squares/issues/503), `BuddenPing/square-packing-certificates` at `9dc93b6` | 207 | the exact fraction the issue prints, `148809603730436756319360591381170501178639/10^40`, admitted by equality |
| T-NNN, #504 | [PingYou Ltd, #504](https://github.com/jlevy/squares/issues/504), the same repository at `bc328a7` | 153 | the exact fraction the issue prints, `6435006925203522001385040447/(5 · 10^26)`, admitted by equality |

Both sides are terminating decimals: $14.8809603730436756319360591381170501178639$ and
$12.870013850407044002770080894$, which is how each register plan’s claim states them,
and the third route holds each plan claim equal to the exact side.
The packets are
[pingyou-n207-certificate-2026-10-11](../../../packing/resources/web/pingyou-n207-certificate-2026-10-11/README.md)
and
[pingyou-n153-certificate-2026-10-11](../../../packing/resources/web/pingyou-n153-certificate-2026-10-11/README.md).
The source states no licence; each packet keeps a derived exact fact and pins every file
of its scope by SHA-256, the release packages among them.
The n153 package’s intermediate control `cycle-hit-153.cert.json`, at a side above the
case ceiling, and its n178 analysis files are outside this review: the source offers
neither.

**Read in full.** The import lane’s commit `7ad4fc95f`: the two `pingyou-json` and
`witness-corners` adapters and the `same_packing` comparison `derive` now makes, with
their tests; both packets’ READMEs, declarations, acquisition records and claim records;
the two facts; both receipts; the import lane’s bead notes and register plans; issues
#503 and #504 with their edit histories as the packets record them; the pinned
`n207.cert.json`, `n153.cert.json` and both witnesses, fetched here; the two release
packages’ `README.txt`, `evidence/README.txt`, `mechanism.txt`, `PROVENANCE.txt` and the
scripts, read and not run; the first imports review and its third route;
[epistemics.md](../../../epistemics.md) on review records and significance.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
that other lanes held at a load average of 14 to 18, one worker process throughout, in a
worktree cut from `main` at `3a5a91a90` with the import lane’s `7ad4fc95f` merged and
this review’s change to the third route added.
A replay decides every job of the packet again through both maintained routes, serially
in one process, and compares every field of each fresh job with its retained row except
the measured times.

| Command (`python -m devtools.upper_bound_reports PACKET …`) | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `pingyou-n207-certificate-2026-10-11 check --replay` | #503’s 3 jobs | all 3 equal, exit 0 | 134.8 s |
| `pingyou-n153-certificate-2026-10-11 check --replay` | #504’s 3 jobs | all 3 equal, exit 0 | 52.3 s |
| `PACKET check-claims`, for each | each frozen comparison rebuilt from the certificate and the holders’ own packets | both rebuilt equal | 7.4 s and 4.2 s |
| `python -m devtools.check_half_angle_area decide-imports --workers 1 --imports '#503' '#504' --upstream pingyou-n207-certificate-2026-10-11 DIR503 --upstream pingyou-n153-certificate-2026-10-11 DIR504` | the third route on both certificates and 12 controls, every cross-check, both lineage measurements, and each fact against its upstream certificate and witness | no disagreement, exit 0 | 59.4 s (65.4 s with the interpreter’s start) |

The replays ran 21:34:05Z to 21:37:24Z and the third route 21:46:12Z to 21:47:17Z. Each
wall includes the interpreter’s start.
The receipts’ own totals, recomputed by the third route, are the numbers the packets
print:

| Import | Jobs | Pair decisions | Route CPU s | Job wall s | Longest job s |
| --- | --- | --- | --- | --- | --- |
| #503 | 3 | 127,926 | 54.66 | 103.49 | 40.08 |
| #504 | 3 | 69,768 | 24.09 | 70.27 | 24.79 |

## From Certificate to Bound

$s(n)$ is the least side of a closed square containing $n$ unit squares with pairwise
disjoint interiors. Each certificate gives a rational side $S$ and, for each square, a
rational centre $(x, y)$ in $[0, S]^2$ and $t = \tan(\theta/2)$; each derived fact
carries the exact rotation $(\cos\theta, \sin\theta)$ instead.
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
tolerates. The dilations the source speaks of are already in the certificates: at 207
every centre and the box of the undilated assembly were multiplied by
$10000000001/10000000000$, at 153 by $5000000000001/5000000000000$, the squares keeping
side 1, and the routes decide the dilated packings as stated.
The certificates’ own metadata is consistent with that, read here and not believed:
$(14 + f) \cdot 10000000001/10000000000$ with the n207’s stated
$f = 880960371555579594780501178639/10^{30}$ is its `s_exact` exactly, and the n153’s
stated table side $1287001385040447/10^{14}$ times its guard is its `s_exact` exactly.

**Nothing touches, so the box convention does not matter.** Every positive clears every
wall and every pair by a positive amount, on all three routes, and the third route
counts no square-to-wall clearance of exactly zero at either count:

| Import | Least wall clearance | Least separating-axis gap (both maintained routes) | Least Euclidean distance (third route) |
| --- | --- | --- | --- |
| #503 | exactly $1/(2 \cdot 10^{10})$ | $19999999989999999999016010000001601/(2 \cdot 10^{44}) \approx 9.99999999500 \times 10^{-11}$ | $1.000000 \times 10^{-10}$ |
| #504 | exactly $1/10^{13}$ | $33179597140421157926909562845849204519671 / (175941977475349355327789470765625 \cdot 10^{21}) \approx 1.885826 \times 10^{-13}$ | $1.885826 \times 10^{-13}$ |

Each least wall clearance is half the guard’s increment.
At 153 it is the first square’s, whose centre is $\tfrac12(1 + 2 \cdot 10^{-13})$; at
207 it is attained at the right and top walls by 40 square-wall pairs, while the first
square sits $\tfrac12(10^{-10} + 10^{-20} + 10^{-30})$ from the near walls, the n70
parent’s own guard included.
So the closed squares are pairwise disjoint and inside the open box, and the bound holds
under any of the usual conventions.
The margins are the ones the sources’ own `native-replay.json` receipts record, which
the import lane noted; here they are the routes’ own numbers.
Both certificates state their centres in $[0, S]^2$; no adapter moves anything.

## Adapters and Admission

Each format has one maintained adapter in `upper_bound_reports.ADAPTERS` and, for this
review, its own reader in the third route.

| Format | Where | What is read | What is not believed |
| --- | --- | --- | --- |
| `pingyou-json` | `n207.cert.json`, `n153.cert.json` at derivation | `n`, `s_exact` and `[x, y, t]` rational strings, SQUISH’s rows; no JSON number, duplicate key or field beyond the four below | `note`, `dilation_exact`, `raw_side`, `provenance` (the construction record: owner lists, placements, the n70 parent’s digests, a degree-seven polynomial, a floating-point `numerical_screen_side`) |
| `witness-corners` | `pingyou-n207-rational.yaml`, `pingyou-n153-rational.yaml`, named by each row as the same packing | a rational `corners` Witness/v2 of `n` unit squares numbered in order in the lower-left frame; the maintained adapter recovers $t = s/(1 + c)$ from the first edge and holds all four corners to that pose; the third route takes the centre as the corners’ mean and the first edge as the rotation, held to the unit circle, and the other three edges to its quarter turns | the `claim`, `source` and `certificate` blocks, and the `softschema` envelope beyond its schema name |
| derived fact | both imports | a rational `center-basis` Witness/v2 in $[0, S]^2$ | its `claim` prose |

The maintained routes read a derived fact through `certificate_from_witness`, which
recovers $t = s/(1 + c)$ and refuses a basis that is not that $t$’s rotation; the third
route reads the basis as stated and holds it to the unit circle.
Both the maintained `witness-corners` adapter and the third route’s reader are new on
these imports, and they differ by design: the adapter refuses a square whose corners
start from another vertex, since it would be the same square at another $t$; the third
route reads such a square as the quarter-turned rotation, and a comparison of placements
then holds the witness to the convention the certificate’s bases use.
On both witnesses every square reads in the certificate’s convention, so the two readers
agree.

**What the adapters decide, and what they do not.** Every route decides in full the
packing an adapter hands it, so a misreading cannot make a false bound pass.
What a misreading would break is attribution, the claim that the packing is the
source’s; that rests on the adapters and on custody, and the upstream check below closes
it for both counts.

**Admission.** Each certificate is admitted by equality to the exact fraction its issue
prints; no rounding is involved.
The frozen claim records print each side rounded up at 16 places, $14.8809603730436757$
and $12.8700138504070441$, and the third route’s own integer ceiling agrees.

## Derived-Fact Custody

The source states no licence, and the packets keep no upstream byte.
`derive` read each certificate from a Git checkout at the pin once
`acquire_source.acquire` showed that the checkout yields the packet’s own acquisition
record and manifest, held the source’s witness from the same checkout to the
certificate’s poses and side, and wrote the certificate as a derived fact naming the
pinned SHA-256. Offline, `read_fact` holds each fact to its own rebuild, and `derive
--check` needs a checkout (RI-2 of the first imports review).

For this review all fifteen files of the two scopes were fetched over HTTPS from
`raw.githubusercontent.com` at the pinned commits into scratch space, outside the
repository, and read as data: the seven files of `9dc93b6` and the eight of `bc328a7`.
All fifteen have the SHA-256 their packet pins.
`decide-imports --upstream` then read each certificate with the third route’s own
`pingyou-json` reader and found it exactly the packing its fact states, side, every
centre and every rotation, and read each witness with the route’s own corner reader and
found it the same packing again.
That binds each fact to the pinned certificate and to the pinned witness, as of this
date; it is the four upstream checks in the command table, two per packet.

The two release packages, pinned by digest, were unpacked here into scratch space.
Every member has the digest its `manifest.json` and the packet README record; the
members read for this review are named under Credit and Lineage.
No program in either package ran.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; the source states it also ran this route, as `packing-witness verify`, on its own witness at `5b0eb012` | the adapters, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares`; the source states it ran this route too | the same adapters, parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area`; `sqpack.yamlio` for the facts and the witnesses; `json`, `hashlib` | `Fraction` and the formats’ meaning only; the source did not run it |

`upper_bound_reports` owns custody, the adapters, admission, the claim comparison and
the job layout; the kernel owns the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on each packet’s own admission (`acquire_source.check`,
and for the facts `read_fact`), which the third route calls before it reads anything and
from which it decides nothing.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
None of the source’s own programs ran: `VERIFY.py`, `reproduce.py`, the three checkers
`vertex_check.py`, `audit_all.py` and `polygon_check.py`, `convert_witness.py`,
`replay_upstream.py`, and at 153 `derive_half_return.py` (SymPy).
That `reproduce.py` rebuilds the n207 poses from the n70 parent and the n153 from its
rational table, that the degree-seven equation has the root the source names, and every
statement about returns, contacts and the undilated side are source reports and are not
decided. That a published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes, their parser and the
adapters before writing the extension, so it is not a clean-room implementation; it
imports none of their parsing or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It is a second pair-deciding procedure, not a second arithmetic.
On the two certificates it decided 32,949 pairs, clipping 699, and found no overlap and
no square outside the box.

## The Controls

**The kernel’s two controls cannot pass vacuously, and are gross** (RI-3, carried as
RV-4). `validate_job` requires both routes to refuse each control, on the complete pair
count, with the negative diagnostic it was built for.
In both receipts the duplicate’s gap is exactly $-1$ and the moved square lies exactly
3.0 units outside the box, refusals a binary64 checker with a $10^{-9}$ tolerance would
also make. They show the routes can refuse, not that they decide at the $10^{-10}$ and
$10^{-13}$ scale where these certificates live.

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

All 12 reached their required outcome.

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- both sides and every centre and rotation equal the maintained routes’ retained checker
  inputs;
- each side equals the exact side of its packet’s frozen claim record and the value its
  register plan’s claim states, and is admitted against the issue’s print by equality;
- each least wall clearance equals both maintained routes’ to every digit: exactly
  $1/(2 \cdot 10^{10})$ at 207 and exactly $1/10^{13}$ at 153;
- each least Euclidean distance is at least the separating-axis gap both maintained
  routes report;
- the two receipts’ totals are the numbers the packets print, and each derived fact is
  the packing its pinned certificate and its pinned witness state.

## The Claims Comparison

Each packet’s `acquisition/claims.json` freezes its certificate against the case record
as it stood at `main` `3a5a91a90` and against every register entry pending there, each
side rebuilt from its holder’s own retained packet; `check-claims` rebuilt both equal.
Every comparison is exact.

| n | Against | Exact side of the other | Relation | Margin |
| --- | --- | --- | --- | --- |
| 207 | the case ceiling, T-127 (SQUISH’s packing refined by Siddharth Gupta) | $14887992258302657381304248932763/10^{30}$ | below | $70318852589817493681897946459498821361/10^{40} \approx 7.03 \times 10^{-3}$ |
| 207 | T-136 (#481, SQUISH), pending | $735531374822863515605402999283143325118010869312518967079087271050773613271161277/49412586952851805135714733794522095254473298746909591292001747563872946931057236$ | below | $4.5459357980020505 \times 10^{-3}$, the issue’s figure |
| 153 | the case ceiling, T-127 (the same) | $2575935874665862918815262035657/(2 \cdot 10^{29})$ | below | $1933104584454118261245856857/(2 \cdot 10^{29}) \approx 9.67 \times 10^{-3}$ |
| 153 | T-146 (Evan Daniel’s regularization of SQUISH’s packing), pending | $402250932783786874180075932249/(3.125 \cdot 10^{28})$ | below | exactly $125999917133498187021808623/(6.25 \cdot 10^{28}) = 0.002015998674135970992348937968$, the issue’s figure |
| 153 | T-136 (#481, SQUISH), pending | $123797999524180008078530976954463155877532124256188212074430292658566758958161323/9617597300166052747813209874613658336103061290746859396882208758750786210512186$ | below | $2.0159986741368190 \times 10^{-3}$ |

T-146 at 153 lies $8.5 \times 10^{-16}$ below T-136, whose packing it regularizes, so
the two margins at 153 differ in the sixteenth place only.
No other report of 11 October states a side at 153 or 207: #500 names 176, 181, 238,
239, 270 to 272, 304 and 305; #501 155, 156 and 211; #505 146 and 261; #506 304, 305 and
counts beyond the corpus.
At both counts the certificate under review is the smallest exact side the record holds
or has pending.

## Credit and Lineage

The source asks that PingYou Ltd be credited with the n207 assembly and the n153
construction, Ryan Xu with the n70 construction both start from
([#432](https://github.com/jlevy/squares/issues/432)), and Evan Daniel with its exact
retention; it names SQUISH’s #481 certificates (T-136) and Evan Daniel’s regularized
n153 (T-146) as comparisons only, and claims neither the n70 packing nor patch
composition in general.
The packets and register plans record that; the commits are authored `BuddenPing` from a
`pingyou.com` address, and no individual is named anywhere.

**The n70 parent is the file the record credits.** Both release packages carry
`evidence/parents/n070.cert.json`, SHA-256 `d508ee05…`, the digest the n207
certificate’s `provenance` names for both its patches.
Its own `provenance` names Evan Daniel’s `search/regularize/lists/certs/n-070.cert.gz`
at `7dfca4e` with SHA-256 `65b1c469…`, which is the digest the
[T-146 packet](../../../packing/resources/web/evand-regularized-2026-10-10/README.md)
records for that file.
Read here with the third route’s own readers, the package’s JSON and T-146’s retained
certificate state the same side, $8880960371555579594785501178639/10^{30}$, and the same
70 poses, centre and rotation exactly.
That was read by hand from the unpacked package and is not a retained check (RV-3); the
lineage measurement below uses T-146’s retained file, which is what the record credits.

**The n207 is two placed patches of that n70, measured.** `patch_lineage`, added to the
third route for this review, undoes the certificate’s guard dilation and then, for each
of the eight symmetries of the n70’s box and every parent-to-child pairing, counts the
parent squares that reappear in the child under the translation the pairing names:
within $10^{-9}$ of a child centre, how many of those at another orientation, and how
many landing on a child square to the digit, centre equal and edge direction exactly a
multiple of a quarter turn away.
Against T-146’s n70 it finds:

| Placement of the n70 | Squares within $10^{-9}$ | Turned | Exact |
| --- | --- | --- | --- |
| the identity | 69 | 0 | 60 |
| $(x, y) \mapsto (L - y, L - x)$, $L$ the n70’s side, then moved by $(6, 6)$ | 69 | 0 | 69 |

That is the source’s account: patch A keeps 60 whole squares at the origin and patch B
69 under the map it calls “reflected in both axes, transposed, and translated by
$(6, 6)$”, the reflection being about the n70’s box; $60 + 69 = 129$, and the other 78
squares are the two upright grids of 42 and 36. The nine further squares that land
within $10^{-9}$ of the identity placement are grid squares at exact half-integers where
the parent’s own $10^{-20}$ guard makes its uprights inexact; the source does not count
them as retained owners, and neither does the exact column.
The exact counts equal the lengths of the certificate’s `A_retained_original_owners` and
`B_retained_original_owners` lists, read for this comparison only.

**The n153 is not a placement of the n70 by pose.** The same measurement finds no
placement landing more than 31 of the n70’s squares within $10^{-9}$ of a child centre,
and at most one exactly; the three best placements are the identity shifted along
upright lattice rows by about $0.989$ and $1.989$, and the $-1/(2 \cdot 10^{20})$ in
their vertical component is the parent’s own guard, which the n153’s construction table
restates at exact half-integers.
That agrees with the source’s own account: it kept a different set of surviving squares,
cut the n70’s long contact return and reclosed the survivors at a new angle from a
floating-point solve the release does not repeat, so the tilted population is at a new
$t$ and the uprights are re-registered.
The register’s credit line for #504, PingYou Ltd after Xu and Daniel, is therefore a
statement about the construction’s origin as the source gives it, not a measured
coincidence of poses, and the entry’s claim should say so (RV-5).

**What this review did not check about lineage.** That `reproduce.py` rebuilds the 207
poses from the parent by the stated transformations, which the measurement makes
plausible and does not prove; that the n153’s rational table came from the n70 at all,
beyond the source’s account; the degree-seven equation, its root and the SymPy
derivation; and the “PhiMath” and “Fibonacci Q operator” vocabulary of the n153
package’s `mechanism.txt`, which resembles that of the record’s undated “PINGYOU LTD”
abstract (`think-aj43`) and which neither the source nor the record links to it.
The company name is the same; nothing here rests on the connection.

## AI Assistance

The pinned source of #503 makes no statement about AI assistance.
Its first commit, `0d8b9c1`, published the README with the sentence “Verification,
comparison review and package preparation were assisted by OpenAI Codex”, and the
package’s `ISSUE_BODY.txt` spoke of “the same Codex-assisted workflow”; the issue as
first posted carried the same two passages.
The pinned commit `9dc93b6`, titled “Correct attribution in submission materials”,
changed only the package, the README and `SHA256SUMS`, removing that sentence and the
phrase; the issue, opened at 10:27:00Z citing `0d8b9c1`, was edited at 10:31:52Z to cite
the pin and to drop the same two passages.
No reason is given anywhere.
#504 and its commit `bc328a7` make no statement, and the issue omits the template’s
assistance section.

What the record should carry: the author’s first account, as the author gave it and as
the Git and issue histories retain it, and the fact of its removal, in the register
entry’s claim or notes for both counts, since #504 was published by the same author
eight minutes after the n207 pin under the same workflow; and the acknowledgement’s
question to the author, which the import lane drafted, asking which account the record
should carry. The import lane’s register plan for #503 already states the history; the
plan for #504 says only that the source makes no statement, and should add the
cross-reference (RV-1). Nothing in the finite-feasibility verdict turns on it: the
decisions are exact and do not depend on the author’s assistant.
Unlike the first imports review’s RI-7, the reviewer and the producer’s assistant are
different model families; the import lane and this reviewer are both Claude, and the
import lane decided no geometry.

## Findings

**RV-1, non-blocking: #503’s AI-assistance disclosure was removed at the pin, and #504
makes none.** As above.
The register should carry the first account and its removal on both entries, and the
author should be asked, as the draft acknowledgement does.

**RV-2, non-blocking: the source ran both maintained routes itself.** The source
reports, with receipts in its package, that `packing-witness verify` and
`check_rational_witness_independent` at `5b0eb012` accept its witnesses, and the import
lane reproduced that on the pinned bytes.
So at #503 and #504 both maintained routes are also the producer’s verification, as one
of them was at #476 (RI-4) and at T-128 and T-130 (RD-4). The independently
re-implemented relation rests on the routes’ authorship, which predates this source and
shares nothing with its generator or its three checkers, and on the third route, which
the source did not run.
The confirming evidence entries’ `limitations` should say so.

**RV-3, non-blocking: no retained check binds a derived fact to its upstream bytes, or
the n70 parent to T-146’s file.** `read_fact` proves each fact well formed and
self-consistent; `derive --check` needs a Git checkout.
This review closed the fact binding once, at this date, by `decide-imports --upstream`,
for the certificate and the witness of each packet, and held the packages’ n70 parent to
T-146’s retained certificate by hand.
A later replay still rests on the facts; the confirming evidence should cite this review
for the binding (RI-2 of the first imports review, unchanged).

**RV-4, non-blocking: the kernel’s controls are gross** (RI-3, unchanged).

**RV-5, non-blocking: #504’s lineage is by construction, not by pose.** The register
plan’s headline, “A packing of 153 squares from Ryan Xu’s packing of 70, its contacts
reclosed at a new angle”, and its credit line are the source’s account.
The measurement above shows the certificate is not a placement of the n70, and the
entry’s claim should state that the relation is the one the source describes and that no
pose was measured to coincide.
The credit itself is as the source asks and is not in question: the source claims the
construction and credits the n70 it started from.

**RV-6, non-blocking for this claim: no private-worker custody at either import.** The
rung for finite feasibility does not need it; the adoption lane closes it before a house
moves (RD-5, RI-5).

**RV-7, non-blocking: the n207 certificate’s unread metadata prints a comparison side
that is not SQUISH’s.** `provenance.numerical_screen_side` reads $14.885506208841678$;
SQUISH’s #481 side at 207 is $14.88550630884167768\ldots$, and the packages’
`public-comparison.json` and the issue print that one correctly.
The adapter does not read the field and nothing in the record believes it; the author
may want to correct it.

## Rungs

**#503: `V3`/`C3`.** Machine-replayed here: the certificate and its two kernel controls
on both maintained routes, and the certificate with its six controls on the third route,
with a certificate, a replay command, a passing replay and retained controls; the fact
held to its upstream certificate and witness here; reviewed adversarially here.

**#504: `V3`/`C3`**, for the same reasons over n = 153, its two kernel controls and six
third-route controls, with its fact held to its upstream certificate and witness here.

Neither reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
Every route is `exact-algebraic`, the third using a second pair-deciding procedure
within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

For the records lane: each entry can take `V3`/`C3` on a confirming evidence entry
(`E-pingyou-503-exact-feasibility`, `E-pingyou-504-exact-feasibility`) with
`relationship_to_generator: independent-implementation`, as the precedents record it,
naming the verifiers V-sqpack-verify, V-check-rational-witness-independent,
V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area and
V-evand-exact-certificates, with this review as its `independence_record` and as the
reported entry’s `external_review`.

## Significance

The import lane drafted `S3` for both.
Compared with the entries nearest to them: T-136 (`S3`, seventeen counts, $1.68 \times
10^{-4}$ to $1.12 \times 10^{-2}$ below the case ceilings) and T-140 (`S3`, six counts,
$7.27 \times 10^{-4}$ to $8.03 \times 10^{-3}$ below) are new constructions or
refinements that move a case ceiling by amounts of this order; T-146 (`S2`) regularizes
packings the record already credits and moves no ceiling by more than $7.82 \times
10^{-10}$ beyond what T-136 had moved.
These two are new constructions, one count each, $7.03 \times 10^{-3}$ and $9.67 \times
10^{-3}$ below the case ceilings and $4.55 \times 10^{-3}$ and $2.02 \times 10^{-3}$
below the smallest pending sides, by a method, placed boundary patches of an existing
packing, that the record has not seen before.
`S3` is confirmed for both: a substantive case result at each count, not a citable
detail, and not yet a reusable technique or bound family, since two instances by one
author do not show the method carries.
`by` on each entry should name this review.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling at
`main` `3a5a91a90` and every report pending on 2026-10-11, each comparison exact.
Sides are shown rounded up at sixteen places.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and the third route and reviewed with no blocking defect.

| n | Case ceiling, house | Exact certificates reviewed | House to adopt |
| --- | --- | --- | --- |
| 153 | 12.8796793733293146, Gupta (T-127) | #504, 12.8700138504070441; T-146, 12.8720298490811800; T-136, 12.8720298490811809 | #504, PingYou Ltd after Ryan Xu’s n70 and Evan Daniel’s exact certificate of it; then T-146, then T-136 |
| 207 | 14.8879922583026574, Gupta (T-127) | #503, 14.8809603730436757; T-136, 14.8855063088416777 | #503, PingYou Ltd, two placed patches of Ryan Xu’s n70 from Evan Daniel’s exact certificate; then T-136 |

This replaces the first imports review’s table at 153 and 207, where #481 was the house
to adopt; at every other count that table and its successors stand.
At both counts the earlier houses stay retained as history, and the case’s reported and
verified ceilings move together.
Credit follows the packets.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **A confirming evidence entry per import**: `E-pingyou-503-exact-feasibility` and
  `E-pingyou-504-exact-feasibility`, each `assurance: verified`,
  `method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s fact as
  `certificate`, the replay commands above, `replay_status: passed`, the six verifiers
  named under Rungs, this review as `independence_record` and as `external_review`
  (`informally-verified`), and limitations naming the shared premises, RV-2, RV-3 and
  RV-4.
- **On each reported entry** (`E-pingyou-503-certificate-report`,
  `E-pingyou-504-certificate-report`): `external_review` naming this review, which makes
  it `reviewed`.
- **On each register entry** once registered: the confirming evidence, `V3`/`C3`, a
  `reviews` entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, covering both), both test files among the
  controls (`packing/tests/test_upper_bound_reports_503_504.py`,
  `packing/tests/test_check_half_angle_area.py`), the significance `by` naming this
  review, and claim, notes and `next_rung` rewritten together: the AI-assistance history
  on both (RV-1), the lineage statement on #504 (RV-5), and the measured lineage on
  #503.
- **In `source-coverage.yaml`**: the confirming evidence on each import’s source entry.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No run of the source’s own checkers, reconstruction or derivation.
No decision of the n153 package’s intermediate control or n178 files.
No `derive --check` from a Git checkout.
No house adoption, case-record change or private-worker custody.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
