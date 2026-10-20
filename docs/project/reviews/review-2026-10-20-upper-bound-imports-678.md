# Review: Couzo’s 85 Exact Upper-Bound Certificates at 204–998 (Issue #678)

**Date:** 20 October 2026. **Verdict: accepted with findings, for finite feasibility
only.** All 85 rows of [issue #678](https://github.com/jlevy/squares/issues/678) prove
the upper bounds their claims state: each linked certificate, less the squares its row
deletes, is $n$ unit squares with pairwise disjoint interiors inside the closed box of
its exact header side, and each printed side is that header side rounded upward at 12
places. The packet’s receipts reproduce here, a checker written for this review and
sharing no code with the packet’s two routes agrees with them at every number they
share, and no defect blocks the claims.
Five findings are recorded, none blocking.
At 204 and 260, the two counts inside the record’s horizon, the entry that registers
them can take `V3`/`C3` once its confirming evidence and this review are added to the
register; neither can take `V4`/`C4` from this review alone.

This is the Stage 4 review lane of the 19 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
`think-xu4d`, written by an AI reviewer of the Claude system family (Anthropic), strong
tier, maximum reasoning, as lane `c-review-678-fable`, prompted separately from the
import lane that built the packet and the replay.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row, adopts no house best packing and edits no bead; the proposed record
changes are listed at the end for the records lane.
Its two programs and their receipts are retained with the packet, in
[`review/`](../../../packing/resources/web/couzo-issue678-2026-10-18/review/README.md)
(RF-5).

**For the author.** Every one of your 85 bounds holds, exactly as stated, on four exact
decision procedures: your own `verify_bound_certificate.py` run from its retained copy,
the two routes of this repository’s replay, and a fourth written for this review.
The findings below are about this repository’s replay and record, not about your
certificates. Two things you may want to look at are listed under Questions: the
manifest’s own `n545.cert` and `n641.cert` state sides above the ones your issue claims
at 545 and 641, and the n260 identity statement in your comment of 19 October holds at
$10^{-7}$ rather than $10^{-8}$.

## Claims Covered

No register entry on `main` carries these claims yet, so this review names no `T-NNN`.
It covers the issue’s 85 rows, read from the retained body
(`packing/campaign/issue-intake/intake-20261019/issue-678.json`): $s(n) \le P_n$ for
each listed $n$, with $P_n$ the 12-place print and the exact side the header of the
linked certificate at `franciscouzo/square-packing` commit
`7b6c87e129cf80b5ff9847b90b47fd30b4563c54`. Two of the 85 counts, 204 and 260, lie in
the record’s horizon (1 to 324); the other 83 are beyond it.
83 certificates carry the 85 rows: the rows at 545 and 641 are the 546 and 642
certificates with one square deleted.

| n | Exact side | Rounded up at 16 | Printed | Standing on `main` (`d588ad987`) | Below it by |
| ---: | --- | --- | --- | --- | --- |
| 204 | `141654921219558922887849/9565692327860000000000` | 14.8086428419812473 | 14.808642841982 | T-186, verified ceiling and house best packing, `740433161719347828316145172430104761481126338872178671530915993369069066972891707484286255665843382616078162213/5·10^110` = 14.80866323438695657…; T-193 (#639, pending adoption under `think-ot5c`), $S^*$ the root of a degree-35 integer polynomial in $[14.808663234387, 14.808663234387]$ at 12 places, $S^* = 14.808663234386956566322903448602…$, below T-186 by $1.48 \times 10^{-99}$ | below T-186 by `487668697101172702616924231495449803273497048500173320505928433730368651936044052618866540225047348468608149132957709/23914230819650000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000` ≈ $2.0392 \times 10^{-5}$; below T-193 by $S^* - S$ ≈ $2.0392 \times 10^{-5}$, the same to 60 digits, decided by $S < 14.8086632343865 \le S^*$ |
| 260 | `146417594016514621500994169/8796093022208000000000000` | 16.6457532505449560 | 16.645753250545 | every result registered at 260: T-083 (the Kingbird register, Ellsworth’s extension) $11 + 4\sqrt2$ = 16.65685424949238019…, the reported bound and house best packing; T-101 and T-155 (Daniel’s regularized exact points) `416421356237309504880168872421/25·10^27` = 16.65685424949238019520675489684, the verified ceiling, above $11 + 4\sqrt2$; T-196 (#668, pending adoption) `16645778804181379786535601/10^24` = 16.645778804181379… | below $11 + 4\sqrt2$, decided by $((S - 11)/4)^2 < 2$, by ≈ $1.1101 \times 10^{-2}$; below T-155 by `74497542862683609107498684663130851/6710886400000000000000000000000000000` ≈ $1.1101 \times 10^{-2}$; below T-196 by `54876016367102771779176336823/2147483648000000000000000000000000` ≈ $2.5554 \times 10^{-5}$ |

Couzo’s side is the smallest at both counts.
At 204 it lies below T-193’s algebraic side as well as T-186’s rational one; T-193’s
degree-35 polynomial at 204 is not retained on `main` (its packet keeps 19 of the 21
forms), so the ordering against it rests on the isolating interval and 60-digit value
the T-193 review retained
(`evand-exact-cur-2026-10-16/review/review-2026-10-16/outputs/claims.jsonl`), and the
two margins differ by T-193’s own $1.48 \times 10^{-99}$. At 260 it lies below the three
sides registered there, the exact $11 + 4\sqrt2$ included.
Every margin was recomputed here from the certificate headers and the exact forms in
`packing/frontier/n-204.md`, `n-260.md` and T-196’s claim on `main`. At 204 the issue’s
own prior column, #675’s print 14.808644367227, lies above this side by at least
$1.525 \times 10^{-6}$ (#675’s exact side is not retained; its print bounds it within
$10^{-12}$). The 19 October ledger’s verdicts at both counts (“recorded”, below by at
least $1.53 \times 10^{-6}$ and by $2.56 \times 10^{-5}$) are the same numbers.

**Read in full.** The issue body and its three comments; the packet README and the
acquisition declaration, record and manifest; `devtools/couzo_678_replay.py`,
`tests/test_couzo_678_replay.py`, `devtools/check_rational_witness_independent.py`,
`devtools/evand_exact_certificates.py` (`Pose`, `parse`, `basis_witness`,
`corner_squares`), `sqpack/verify.py` (`separated`, `project`, `edge_axes`,
`check_unit_squares`, `candidate_pairs`) and `sqpack/witness.py` (`_materialize`,
`_square_from_pose`, `_exact_materialize`, `materialize_exact_witness`); the source’s
`verify_bound_certificate.py` and licence; the four receipts; the 19 October ledger
README and the n260 seed custody receipt; T-186, T-155 and T-196 on `main`; Stage 4 of
`result-import.md`; `epistemics.md` on review records and on which code confirmed a
result; the [10 October review](review-2026-10-10-couzo-daniel-refinement-replays.md) of
T-128, T-130 and T-131 as the form to follow.
**Disclosure.** Before writing, this reviewer read the one-paragraph summary of the 19
October mathematical review in the notes of `think-xu4d` and the three sentences the
packet README added from it (`2c2c8032d`); the full text of that review is not retained.
The comparison is in its own section at the end.

## Replays Reproduced Here

Run from `packing/` of a worktree of `origin/claude/intake-678-replay` at `caef09ede`
with the project interpreter (CPython 3.14.7), under `nice -n 10` on a four-core host
shared with other lanes at a load average of 8 to 12.

| Command | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `python -m devtools.couzo_678_replay check --replay` | every row and every control again, in process, held field by field to the retained receipt | `OK: 85 rows verified, every control refused`, no row differs from its receipt | 686.9 s (549.5 CPU s) |
| `python -m pytest tests/test_couzo_678_replay.py` | the eight retained tests, the n = 204 row, its five controls and the source checker on a duplicate among them | 8 passed | 3.5 s |
| `python -m devtools.couzo_678_replay check` | the four receipts against the issue and the packet | `OK` | 4 s |
| `python -I review_678_check.py … --all-pairs 204 260 330 459 499 545 998 --workers 2` | this review’s checker on all 85 rows (below) | 85 of 85 passed, no disagreement with the receipt | 368.2 CPU s |
| `python -I identity_260.py …` | the n260 seed against T-196 and against #678’s certificate under the box’s eight symmetries | 240 of 260 within $10^{-7}$ (below) | 6 s |

The packet’s own receipts say what they said on 19 October: 85 of 85 rows verified,
140,866 candidate pairs of 21,393,271, 415 of 415 controls refused by both routes, each
on the failure it was built for (the receipt’s first failure string is an overlap at all
166 overlap controls, a wall crossing at all 166 wall controls and a non-unit edge at
all 83 shape controls); the source’s checker accepts 85 and refuses 332; the all-pairs
kernel agrees with the filtered decision at 204, 260, 343, 545 and 641 on every margin;
every side is below Göbel’s at its count.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors. A certificate is a header `n S` and $n$ rows `x y t`: a rational side, a
rational centre and $t = \tan(\theta/2)$. The bound $s(n) \le S$ follows from five
facts, each decided over $\mathbb{Q}$ or fixed by the format:

1. **The rotation is on the unit circle.** For every rational $t$,
   $(c, s) = \big((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2)\big)$ satisfies $c^2 + s^2 = 1$,
   since $(1 - t^2)^2 + (2t)^2 = (1 + t^2)^2$. The four points
   $(x, y) + \tfrac12(\pm c \mp s, \pm s \pm c)$ are therefore the corners of a unit
   square centred at $(x, y)$, counter-clockwise, and a certificate can state no other
   shape. Both routes nevertheless re-check the corners they build, unit edges and right
   angles (`sqpack.verify.check_unit_squares`, `square_failures`), and this review’s
   checker tests $c^2 + s^2 = 1$ on each row.
2. **There are exactly $n$ of them.** The parser refuses a header that differs from the
   file name’s count and any row beyond the $n$-th (`evand_exact_certificates.parse`,
   lines 209–239); a square listed twice overlaps itself and is refused.
   For the two deletion rows the first $n$ poses of the parent are kept
   (`couzo_678_replay.py:232`); any sub-multiset of a packing is a packing in the same
   box, so which square is deleted does not matter, and the derived packings were also
   written out and decided by the source’s checker.
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box iff its
   corners do (both routes), equivalently iff its centre clears each wall by its
   half-extent $h = (|c| + |s|)/2$ along that axis (the source’s checker and this
   review’s). The contract is the closed box: a corner exactly on a wall is accepted,
   and 62 of the 85 packings have one; the other 23 clear their nearest wall by exactly
   $10^{-15}$.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors iff
   one of their edge normals weakly separates their projections (the separating-axis
   theorem; a square has two distinct normals, so four axes decide a pair), equivalently
   iff the area of their intersection is zero.
   A gap of exactly $0$ is a contact and is accepted; 695 pairs touch, at nine counts.
5. **The pairs not decided cannot overlap.** Only pairs with $dx^2 + dy^2 < 2$, compared
   exactly from the certificate’s centres, are decided (`candidate_pairs`,
   `couzo_678_replay.py:272–290`). The interior of a unit square lies in the open disc
   of radius $\sqrt2/2$ about its centre, and two such open discs about centres at
   distance $\ge \sqrt2$ are disjoint by the triangle inequality, so the skipped pairs
   have disjoint interiors.
   The lemma needs each square to be a unit square centred where the filter read its
   centre: both routes check unit shape and that the corner mean equals that centre,
   exactly (`_centre_failures`, lines 293–298). The sweep sorts by $x$ and stops at the
   first later square with $dx^2 \ge 2$, which is sound since $dx \ge 0$ in sorted
   order. The source’s checker uses the same lemma after exact cells of side 2
   (`verify_bound_certificate.py:36–43`, `55`), keeping pairs with $dx^2 + dy^2 \le 2$.
6. **The print is the side.** `P − 10^{-12} < S \le P` with $P$ read as a 12-place
   decimal (`rounds_up_to`, lines 236–240); this review recomputed $\lceil S \cdot
   10^{12} \rceil / 10^{12}$ for all 85 rows and found every print equal to it.

Arithmetic is CPython `Fraction` throughout every route, including the source’s checker
and this review’s; no route rounds, dilates or tolerates.
The `sqpack.verify` bucket mode, which buckets float centres, is not used.
The box convention does not matter for the claim: every route decides the closed box and
disjoint interiors, which is the contract the issue states; under the open-box,
disjoint-closed-squares contract 62 rows would fail, as the source’s `--strict` verdict
says.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`V-sqpack-verify` predicates) | unit shape on corners, corners in the box, candidate pairs by exact separating axes | `sqpack.verify.check_unit_squares`, `separated`; corners from `sqpack.witness._square_from_pose` on the basis `basis_witness` writes | with `independent`: the parser, `Pose.basis` (the half-angle map, `evand_exact_certificates.py:176–179`), the pair filter, the centre check and `Fraction`; with the producer: the author reports running “the jlevy/squares corner verifier”, so these predicates are at or near the producer’s second checker |
| `independent` (`V-check-rational-witness-independent` predicates) | the same three facts on corners `Pose.corners` builds (lines 181–189) | `square_failures`, `pair_gap` | the same parser, half-angle map, filter, centre check and `Fraction`; its corners are built by a second formula on the same basis; none of its deciding code is the producer’s |
| the source’s checker (`verify_bound_certificate.py`, SHA-256 `1c8b89eb…`) | unit circle, half-extent containment, all pairs within $\sqrt2$ by separating axes with unit normals | itself, run with `python -I` from the retained copy | the producer’s own code: a reproduction, `same-implementation`; shares `Fraction` only |
| this review’s checker (`review_678_check.py`) | unit circle, half-extent containment, every pair at seven counts and every near pair at all 85 by separating axes with unit normals, and every near pair again by the exact area of one square clipped by the other’s four closed half-planes | itself: its own literal reader, conversion, filter and both pair procedures, standard library only | `Fraction` and the format’s meaning; its author read every route above before writing it, so it is not clean-room |

Three readers of the certificate text therefore exist (the shared `parse`, the source’s
`parse`, this review’s), and all three read the same 85 sides and the same centres and
half-angles: this review’s sides equal the receipt’s `exact_side` literal at every row,
and its least wall clearances and least pair gaps, computed from half-extents and unit
normals rather than corners, equal the `independent` route’s to every digit at the 78
rows where both decide the same pairs, and are no larger at the seven all-pairs rows.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every route. The custody of the bytes rests on the packet’s admission
(`acquire_source --check`, run by every command and by the test), which holds each file
to the digest declared at acquisition and the source’s `SHA256SUMS` to the pin; that the
published file is the one its author meant is attested by the pin alone.
The author’s own runs are the author’s. The all-pairs kernel of
`evand_arrangement_reports` has run on five counts only (`think-fpnd` holds the rest);
this review’s all-pairs checks at 204, 260, 330, 459, 499, 545 and 998 are a second
sample, not that replay.

## The Controls

Five mutants of each of the 83 certificates, decided by both routes
(`couzo_678_replay.py:434–486`), and four of them as certificates by the source’s
checker, which cannot state the fifth:

| Control | Built to fail on | Scale | Refused on that failure |
| --- | --- | --- | --- |
| square 2 replaced by square 1 | overlap | gross: gap $-1$ | 83 of 83, both routes, and the source |
| square 1 moved $S + 2$ right | wall | gross | 83 of 83, both routes, and the source |
| side lowered by the least top or right clearance, then by $10^{-18}$ | wall | $10^{-18}$ | 83 of 83, both routes, and the source |
| square 1 enlarged by $10^{-12}$ about its centre | shape | $10^{-12}$ | 83 of 83, both routes; not a certificate |
| the candidate pair with the least $\lvert dy\rvert$ given one $x$ | overlap | gross: the centres end within $7 \times 10^{-9}$ of each other at every count | 83 of 83, both routes, and the source; the first failure names the intended pair at all 83 (checked here) |

The two wall and shape controls are sharp.
The two overlap controls are not: at every count the chosen pair has
$\lvert dy\rvert \le 6.94 \times 10^{-9}$, so the one-coordinate mutant is a
near-duplicate, and no control probes overlap at the $10^{-11}$ to $10^{-13}$ scale
where the least gaps live (RF-2). `check --replay` holds every control to the receipt,
so a route that accepted everything would fail admission.

## Agreement to Every Digit

This review’s checker (`review_678_check.py`, run with `-I`, standard library only) read
all 83 certificates and the issue body with its own readers and decided all 85 rows:

- every print equals the header side rounded up at 12 places, and every 16-place ceiling
  in the receipt equals the one recomputed here;
- every rotation satisfies $c^2 + s^2 = 1$; every centre clears every wall by its
  half-extent, with a least clearance of exactly $0$ at 62 rows and $10^{-15}$ at 23,
  equal to the receipt’s at every row;
- the near-pair sets equal the receipt’s candidate sets in size at every row (140,866
  pairs in all), and every near pair has separating-axis gap $\ge 0$ and intersection
  area exactly $0$: no overlap under either procedure, 695 contacts;
- at 204, 260, 330, 459, 499, 545 and 998 every one of the 983,766 pairs was decided by
  separating axes with no filter; the least gap at each equals the receipt’s (at 204:
  `19393777832215110850002293904201121998896992458864930891047616814455259 /
  348725840364746259045903601310906709485310533577424592468948863701483520000000000` ≈
  $5.56 \times 10^{-11}$ between squares 115 and 124; at 260:
  `147556112062046079467311/119186041988467709397237450000000000` ≈ $1.24 \times
  10^{-12}$ between squares 56 and 62), so the filter skipped nothing that decides a
  margin at those counts;
- the 85 rows took 368.2 CPU seconds on two workers (48.1 s for the all-pairs decision
  at 998); the receipts are `outputs/out-all.json` and `outputs/out-204-260.json` in the
  packet’s `review/` directory, beside the program.

**At 260 the seed, T-196 and the certificate.** From the retained gzip
`issue-678-n260-seed-14a9af8.cert.gz`: 4,112 bytes, SHA-256 `e90993b1…4934e`;
decompressed 38,184 bytes, SHA-256 `34b203dd…c6d40`; header
`260 4161444696515435316429350771309/250000000000000000000000000000`, which rounds up at
12 places to the issue’s prior column 16.645778786062 and lies $1.812 \times 10^{-8}$
below T-196’s side. Against T-196’s retained `n260_exact.json.gz` under the box’s eight
symmetries, 240 of the seed’s 260 squares have a square of T-196 within $10^{-7}$ in
centre with the same axes (49 within $10^{-8}$, 226 within $2 \times 10^{-8}$; the side
difference alone displaces far-wall squares by $1.8 \times 10^{-8}$), and the other 20,
all axis-aligned, are displaced by 0.42 to 0.46. #678’s certificate is not a refinement
of the seed in place: under its best symmetry 162 of its 260 squares lie within
$10^{-4}$ of a seed square and 55 moved by more than $10^{-2}$; it has 199 axis-aligned
squares to the seed’s 194.

## The Issue’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(n) \le P_n$ at each of the 85 counts, the exact side authoritative | body, table | **computationally verified here**: four exact routes, every pair decided or excluded by a proved lemma |
| each print is the exact side rounded upward at 12 places | body | **computationally verified here**, all 85 |
| a row with surplus squares deletes them (545, 641) | body | **proved**: a subset of a packing is a packing; both derived packings decided |
| each bound is strictly smaller than the `c6da0fc` index and the earlier reports, pending submissions included | body | **computationally verified here** at 204 and 260 against `main` and T-196; at the 83 beyond-horizon counts the 19 October ledger records each claim against the record’s reports by their prints, which is report-order comparison, not verification of those reports; the `c6da0fc` index itself is pinned by digest and not compared here |
| below Göbel squares, ordinary and corner strips, with deletion | body | **computationally verified here** (the packet’s receipt, all 85 below by $\ge 4.31 \times 10^{-3}$, re-read here) |
| below Friedman off-centre constructions, square tilings and repeated L borders | body | **asserted but unverified** |
| new or changed witnesses passed the jlevy/squares corner verifier and the source’s centre/projection verifier; earlier receipts reused only for identical bytes | body | **asserted** (the author’s runs); the same checkers’ verdicts are reproduced here, the source’s from its retained copy |
| both checkers use exact half-angle rotations and separating axes; closed container, disjoint interiors, contact allowed | body | **computationally verified here** for the retained checker, by reading and by running it |
| construction and seed credits: de Winter, Fang, Polkovskyi, Daniel and others per the manifest | body, manifest | **asserted but unverified**; the credits are the source’s, read from the pinned manifest |
| `e90993…` is the gzip digest; the decompressed digest is `34b203dd…`; the seed is at evand `14a9af8`, path `search/regularize/lists/certs/n-260.cert.gz`, header as stated | comment 6269517369 | **computationally verified here** from the retained bytes (data custody; the fetch itself is the intake’s) |
| at evand `0f37f49` the path holds a different file of side $11 + 4\sqrt2$ | comment | **asserted but unverified**; not fetched here |
| the seed is Evan Daniel’s exact-form solve of de Winter’s #668 packing, $1.8 \times 10^{-8}$ below its posted side | comment | side difference **computationally verified here** ($1.812 \times 10^{-8}$); the attribution is the author’s and Daniel’s own statements, **asserted** |
| the seed is the analytic optimum of that packing | comment | **asserted but unverified**: optimality of a contact graph is not decided by any route here |
| after a 180° rotation 240 of 260 squares coincide with T-196 within $10^{-8}$; the other 20 are axis-aligned wall squares shifted along the wall | comment | **computationally checked here, holding at $10^{-7}$**: 240 within $10^{-7}$, 49 within $10^{-8}$; the 20 others are axis-aligned and displaced by 0.42 to 0.46 |
| the float conversion of the seed reproduces SHA-256 `9fdc6b41…` byte for byte | comment | **asserted but unverified**: the importer and the seed file are not retained |
| the search chain 109310 → 109500 → 109690 with the stated sides and digests produced `n260.cert` | comment | **asserted but unverified**: the intermediate files are not in the repository; the final job’s 16.645753250529 is $1.6 \times 10^{-11}$ below the certificate’s exact side, consistent with an exact re-solve or dilation of a float result, but nothing here decides that |
| #678’s n260 descends from the seed | comment | **asserted**; the geometry is consistent with a search that moved a fifth of the squares, which neither confirms nor refutes it |
| T-196 keeps its chronology; the seed does not rewrite it | comment 6270970266 | a record rule, applied: the 19 October ledger records #678 after T-196 |

No row claims optimality, local optimality, rigidity, novelty or priority, and none is
decided.

## Findings

**RF-1, minor, non-blocking: the two filtered routes read each certificate once,
together.** Both take `evand_exact_certificates.parse`, the half-angle map `Pose.basis`
and the filter of `couzo_678_replay.candidate_pairs`, and the `independent` route’s
corners are `Pose.corners`, built in the shared module rather than by the checker
(`couzo_678_replay.py:257–269`). A misread literal or a wrong map would reach both
alike; the shape and centre checks would catch a non-unit square but not a wrong centre
or tangent. The README says so (lines 379–383 at `caef09ede`). The source’s checker and
this review’s checker each read the text with their own readers and found the same
inputs, which closes it for these 85 rows.
The evidence entry should say `shared-components` and list the parser, the half-angle
map and the filter (Proposed Record Changes).

**RF-2, minor, non-blocking: the overlap controls are gross.** The duplicated square has
gap exactly $-1$ and the one-coordinate mutant puts two centres within
$6.94 \times 10^{-9}$ of each other at every count (`overlap_pair`, lines 421–431). The
wall and shape controls are sharp at $10^{-18}$ and $10^{-12}$, but nothing probes a
pair at the $10^{-11}$ to $10^{-13}$ scale of the least gaps, where a binary64 checker
with a tolerance would also pass.
Exactness is shown instead by the margins: three differently computed routes reproduce
the least gap at every count to every digit, and this review’s clipping route finds area
exactly zero at every near pair.
The contact-plus-$10^{-30}$ pair control of `check_half_angle_area` (the 10 October
review, RD-2) would make the packet show it itself.

**RF-3, note: the receipt’s `source_strict_valid` at 545 is the manifest’s verdict on
another file.** `source_manifest_rows` (`couzo_678_replay.py:517–541`, field at line
538\) reads `strict_verification.valid` from the manifest entry for the count, which at
545 and 641 names the source’s own `n545.cert` and `n641.cert`, not the issue’s rows.
The manifest says strict is false at 63 counts; the source’s checker run here says 62,
the derived 545 packing being strict-valid.
The README’s 62 (line 229) is the run’s and is right; the field should be dropped or
renamed so a reader does not take it for the row’s.

**RF-4, note: the issue’s prior column is read but not decided.** `Claim.prior` is
retained as `issue_prior` and compared with nothing; the README’s record-order
comparison is the ledger’s. At 260 the column is the seed’s print (verified above); at
204 it is #675’s. Nothing turns on it; the row-order verdicts rest on the ledger.

**RF-5, note, for the record: the 19 October review’s code and text were not retained,
and this review’s must be.** Stage 4 says a review’s code is kept in the packet with a
README and registered in `verifiers.yaml`; the earlier review survives as a note on the
bead and three sentences in the packet README. `review_678_check.py` and
`identity_260.py` are in this review’s scratch directory and decide nothing until they
sit under `packing/resources/web/couzo-issue678-2026-10-18/review/` with their receipts
(`out-all.json`, `out-204-260.json`).

## Questions for the Author

1. The manifest at the pin names `n545.cert` (bound 23.889010439313) and `n641.cert`
   (25.881306220599), each above the side your issue claims at that count from the 546
   and 642 certificates less one square.
   Is the manifest meant to carry the deletion rows, or the separate files?
2. The identity statement of 19 October holds at $10^{-7}$ (240 of 260) rather than
   $10^{-8}$ (49 of 260), the difference being T-196’s side itself; is $10^{-8}$ a
   per-coordinate figure after a side rescale?
3. The promised source patch (evand pin, hash kind, Daniel’s certificate credit) was not
   linked in the three retained comments.

## Rungs

**At 204 and 260, `V3`/`C3`** for the entry that registers them: a retained certificate,
a replay command (`check --replay`), a passing replay reproduced here, and retained
controls refused by every route that accepted the positive, reviewed adversarially here.
The confirmation is *re-implemented sharing named components* for the two filtered
routes (RF-1) and *reproduced with the producer’s code* for the source’s checker; this
review’s checker is a further re-implementation that shares none of the packet’s
deciding code and is not clean-room.
Neither count reaches `V4`/`C4`: that needs a second accepted adversarial review by a
distinct reviewer and a retained human oversight record, and this is one AI review.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.
The 83 beyond-horizon rows are verified to the same standard and take no rung, since no
register entry carries a count above 324.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`verifiers.yaml`.** Register `devtools.couzo_678_replay` with the digest that ran,
  `role: decides`, `methods: [exact-algebraic]`, and an `independence` record:
  `read: [mathematics, certificate-format, producer-code, producer-output]`,
  `clean_room: false`, `shares` naming `sqpack.verify` (`check_unit_squares`,
  `separated`), `devtools.check_rational_witness_independent` (`square_failures`,
  `pair_gap`), the parser and half-angle map of `devtools.evand_exact_certificates`, and
  CPython `Fraction`; `written_by` the import lane (AI, Claude system family).
  Add versions of `V-sqpack-verify` and `V-check-rational-witness-independent` at the
  digests that ran. Register this review’s `review_678_check.py` once retained, with
  `clean_room: false` and `shares: [Fraction]`, and the source’s checker as external,
  `same-implementation`, at SHA-256 `1c8b89eb…e98b`.
- **Evidence.** One confirming entry for the two in-horizon counts (and one report entry
  per the packet), `assurance: verified`, `method: exact-algebraic`,
  `origin: replayed-here`, `relationship_to_generator: shared-components`,
  `shared_components: ["sqpack.verify's unit-shape and separating-axis predicates, the corner verifier the author reports running", "the certificate parser and half-angle map of devtools.evand_exact_certificates", "the sqrt-2 centre filter of devtools.couzo_678_replay", "CPython Fraction arithmetic"]`,
  `replay: … couzo_678_replay check --replay`, `replay_status: passed`, verifiers as
  above, this document as `independence_record` and `external_review`, and `limitations`
  naming RF-1 and RF-2 and that the all-pairs kernel ran on five counts.
  The 83 beyond-horizon counts enter `source-coverage.yaml` as dated rows citing the
  same receipts.
- **Register.** The entry at {204, 260}: `V3`/`C3`, a `reviews` entry for this document
  (`kind: adversarial`, `reviewer_kind: ai`, `relation: project`, `verdict: accepted`),
  its claim saying *confirmed, re-implemented sharing named components*, and house best
  packings adopted at 204 over T-186 and at 260 over T-155 (T-196 stays recorded as the
  earlier report) with the regularization runs the adoption rule requires.
- **The packet.** A `review/` directory with the two programs, their receipts and a
  README; the receipt field of RF-3 dropped or renamed; the three sentences `2c2c8032d`
  added pointing at this document once mapped.

## Comparison with the Earlier Review

The 19 October review (Claude system family, summarized on `think-xu4d`) accepted with
findings, no blocker or high; it ran independent all-pairs checks at 204, 260, 330, 545,
641 and 998 and an independent separating-axis test on all 140,866 candidate pairs, and
its three low wording findings were applied in `2c2c8032d`. This review agrees with its
verdict and reaches it by an overlapping sample (204, 260, 330 and 998 in common; 459,
499 and 545 added, 641 not repeated) plus a second pair procedure, exact clipping area,
which the summary does not mention.
Its full text is not retained, so whether it raised RF-2 or RF-3 cannot be known; the
README sentence it added (“two implementations of the unit-shape, pair and wall
predicates, not two independent replays”) is RF-1 in other words.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No fetch from the network: the pins, the `0f37f49` file and the promised
source patch were not checked.
No run of the author’s importer or search; no decision of the float conversion or the
search chain. No replay of #670, #672 or #675, whose prints the ledger compares against.
No house best packing adoption, case-record change or regularization run.
No run of the all-pairs kernel beyond the packet’s five counts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
