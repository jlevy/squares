# Review: de Winter’s Exact Upper Bounds at 227, 229 and 260 (Issue #668, T-196)

**Date:** 20 October 2026. **Verdict: accepted with findings, for finite feasibility
only.** The three rational certificates of
[issue #668](https://github.com/jlevy/squares/issues/668) prove the upper bounds their
rows state: each is $n$ unit squares with pairwise disjoint interiors inside the closed
box of its exact side, and each printed bound is that side rounded upward at 12 places.
The replay of PR #704 reproduces here, a checker written for this review and sharing no
code with the replay’s two routes agrees with their receipt at every number they share,
and sharp controls at the $10^{-30}$ scale, which the packet lacks, are refused by both
routes. Four findings are recorded, none blocking.
T-196 can keep `V3`/`C3` and take this review as its accepted adversarial review; it
does not reach `V4`/`C4` from this review alone.
At 227 T-196 is the smallest registered side and the house best packing to adopt; at 260
it is the smallest registered side on `main` and on this branch, but Couzo’s #678
certificate, pending as T-223 in PR #701, lies $2.56 \times 10^{-5}$ below it; at 229
Evan Daniel’s T-199 is $1.32 \times 10^{-5}$ below it and the house best packing stays.

This is the Stage 4 review lane of the 20 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
`think-455r`, written by an AI reviewer of the Claude system family (Anthropic), strong
tier, maximum reasoning, as lane `c-review-704-fable`, prompted separately from the
replay lane (`think-8xr0`) that built the adapter and the receipt and from the records
lane that wrote PR #704. Its relation to the result is `project`. It is read-only: it
moves no rung, writes no register row, adopts no house best packing and edits no bead;
the proposed record changes are listed at the end.
Its three programs and their receipts are retained in the packet’s
[`review/review-2026-10-20/`](../../../packing/resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/review/review-2026-10-20/README.md)
(RF-4).

**For the author.** All three of your bounds hold exactly as stated, on three exact
decision procedures that are not your code: the two maintained routes of this
repository’s replay and a third written for this review, which also decides every pair
of centres within $\sqrt2$ a second way, by exact clipping area.
Your two separating-axis checkers were read in full and are sound as written; your
clipping checker was not run here.
The findings below are about this repository’s record and replay, not about your
certificates. Two things you may want to look at are under Questions.

## Claims Covered

T-196 on `main` (`f8d547728`, registered by #676 at `V0`/`C0`; this branch raises it to
`V3`/`C3`): $s(227) \le S_{227}$, $s(229) \le S_{229}$ and $s(260) \le S_{260}$, with
each $S_n$ the `certified_side_exact` of the retained `records.json` and the `side` of
the retained `n{n}_exact.json` (SHA-256 `5aa22dd0…`, `edb3ef2e…`, `56ddfa73…`,
decompressed here and matched).
The counts are inside the record’s horizon.

| n | Exact side | Rounded up at 16 | Printed | Below the case ceiling (T-155, the Kingbird closed form) by | Against the other sides registered or pending at n |
| ---: | --- | --- | --- | --- | --- |
| 227 | `194547458795865848854407472552117653131825098066089500568310019841668910818842825068644658133972443495777187230686109286929082683273291187074040913251499 / 12500000000000000000000000000001272204783003459957077568639425038233180795950995922365041743732086145591922059343477256613382050000000000000000000000000` | 15.5637967036692680 | 15.563796703670 | T-155 `19463834764831844055010554526310613/1250000000000000000000000000000000` by ≈ $7.2711 \times 10^{-3}$; below $17/2 + 5\sqrt2$, decided by $((S - 17/2)/5)^2 < 2$; below T-101 `486595869120796101380129821849/31250000000000000000000000000` by ≈ $7.2711 \times 10^{-3}$ | above Couzo’s #672 print 15.563625652343 (rounded up, exact side not retained) by $1.7105 \times 10^{-4}$: decided, since $S > $ the print |
| 229 | `156501747569482131747919637148801852719869637315233948984618327625011520667543259632677498716011131748832131668750692746335433269145213277034738380207139541 / 10000000000000000000000000000001737366297119815888250696550926607660931327350731575578989919015034082413286101971092035771621296900000000000000000000000000` | 15.6501747569482132 | 15.650174756949 | T-155 at 229 `391421356237309504880168872421/25000000000000000000000000000` by ≈ $6.6795 \times 10^{-3}$; below $10 + 4\sqrt2$; below T-101 by ≈ $6.6795 \times 10^{-3}$ | **above** T-199 `7825080756947776580756939951343/500000000000000000000000000000` (the house best packing) by `662152633000663904190609573313283554567729949543553117096920506958144693601643782695416358304522269823915536705586312469107090527463367767481678612137633 / 50000000000000000000000000000008686831485599079441253482754633038304656636753657877894949595075170412066430509855460178858106484500000000000000000000000000000` ≈ $1.3243 \times 10^{-5}$; above T-198 by ≈ $1.1502 \times 10^{-5}$; above Couzo’s #672 print 15.650174740273 by $1.6675 \times 10^{-8}$, decided |
| 260 | `16645778804181379786535601/1000000000000000000000000` | 16.6457788041813798 | 16.645778804182 | T-155 `416421356237309504880168872421/25000000000000000000000000000` by `276886132775010216778847421/25000000000000000000000000000` ≈ $1.1075 \times 10^{-2}$; below $11 + 4\sqrt2$, decided by $((S - 11)/4)^2 < 2$; below T-101 by ≈ $1.1075 \times 10^{-2}$ | **above** Couzo’s #678 side `146417594016514621500994169/8796093022208000000000000` (T-223, pending in PR #701) by `54876016367102771779176336823/2147483648000000000000000000000000` ≈ $2.5554 \times 10^{-5}$ |

Every side and margin was recomputed here from the certificate files, the `n-{n}.cert`
headers of the retained Daniel packet (T-101), the regularized sides T-155 reads, the
claims in `acquisition/claims.json`, and the #678 header; the program is
`programs/margins_704.py`, its receipt `outputs/out-margins.json`. The branch’s figures
(7.27e-3, 1.71e-4, 1.32e-5, 1.15e-5, 1.67e-8, 1.11e-2, 2.56e-5) are the same numbers.
The issue’s reductions against the catalogue’s closed forms, 0.007271108196,
0.006679492544 and 0.011075445311, are reproduced to the digits it prints.

**Smallest at each count.** At 227, T-196, among the registered sides (T-101, T-155,
T-196); Couzo’s #672 prints a smaller side but is at Stage 1, unregistered, with no
exact side retained.
At 229, T-199 (Daniel’s update), then T-198, then T-196; the ordering is exact and the
house best packing does not move.
At 260, T-196 among the sides registered on `main` and on this branch (T-101, T-155,
T-196), and T-223 once PR #701 lands: Couzo’s certificate is exactly below T-196, and
the #678 review of 20 October found it feasible on four exact routes.
The adoption question is in its own section.

**Read in full.** The issue body and its one comment; the packet README, the acquisition
declaration, report and claims, the three `records.json`, the three `SHA256SUMS`, the
source’s `verify_all.py`, `verify_exact.py` and `verify_polygon_exact.py` (one copy, the
three folders’ being byte-identical) and its audit summary and negative-control receipt;
`devtools.upper_bound_reports` (`center_basis_json`, `check_certification`, `certify`,
`decide_job`, `margins`, the HOUSES reader), `devtools.evand_arrangement_reports`
(`job_input`, `run_case`, `validate_job`, `validate_receipt`, `replay_receipt`),
`devtools.evand_exact_certificates` (`Pose`, `basis_witness`, `corner_squares`),
`devtools.check_rational_witness_independent` (`square_failures`, `axes`, `interval`,
`_separation`, `pair_gap`, `check_squares`), `sqpack.verify` (`edge_axes`, `project`,
`separated`, `check_unit_squares`, `verify_packing`), `sqpack.witness`
(`_square_from_pose`, `exact_verify`); the two test modules; the receipt, decompressed;
the branch’s diff of `results.yaml`, `evidence.yaml`, `verifiers.yaml`, `n-227.md`,
`n-260.md` and the citation deferral; Stage 4 of `result-import.md`; `epistemics.md` on
which code confirmed a result and the independence record; the 10 October review of
T-128, T-130 and T-131 and this reviewer’s own 20 October review of #678 as the form to
follow. The source’s `verify_polygon_clipping.py` was not read in full and was not run.

**Disclosure.** This reviewer wrote the 20 October review of Couzo’s #678, which ordered
#678’s n = 260 side against T-196’s and measured the seed’s geometry against T-196’s
witness; that review decided nothing about T-196’s certificates.
The PR says an earlier mathematical review of #668 exists on a branch that is not on
`origin` (`codex/review-668-math`, `think-455r`); its text was not available and was not
read. After the findings below were written, this reviewer read the two summaries of it
in the notes of `think-455r` and its parent bead; the comparison section at the end says
what they carry.

## Replays Reproduced Here

Run from `packing/` of a worktree of the PR head `efcd4ddac` with the project
interpreter (CPython 3.14.7), under `nice -n 10` on a four-core host shared with other
lanes.

| Command | What it decides | Outcome | CPU |
| --- | --- | --- | --- |
| `python -I programs/review_704_check.py` | this review’s checker on all three certificates: unit circle, half-extent containment, all $n(n-1)/2$ pairs by separating axes, every pair within $\sqrt2$ again by exact clipping area, the prints, and every number against the receipt’s two routes | 3 of 3 passed; every wall clearance, least gap, pair count and side equal to both routes’ to every digit | 4.8 s, 5.2 s, 2.7 s |
| `python sharp_controls_704.py 260 227` | six mutants per count through the adapter and both maintained routes (below) | every mutant decided as built | 227: 4 × (57 + 26) s; 260: 4 × (3 + 2.3) s |
| `python -I programs/margins_704.py` | the sides and margins above | as tabulated | 1 s |
| `pytest tests/test_upper_bound_reports_668.py tests/test_upper_bound_reports.py -k …` | the packet’s ten tests and the adapter’s read and seven refusals | passed (the log is `outputs/pytest.log`) | — |

The receipt (`receipts/exact-certification.json.xz`, format
`de-winter-668-exact-replay-v1`) says what the README and the evidence entry say: 9
jobs, each positive passing both routes with `pairs_tested` $= n(n-1)/2$ (25,651, 26,106
and 33,670, which is 512,562 decisions over 9 jobs and 2 routes), every wall clearance
exactly $10^{-9}$, least pair gaps $1.0030 \times 10^{-9}$, $1.0030 \times 10^{-9}$ and
$1.0300 \times 10^{-9}$ (the README’s 1.003, 1.002 and 1.030 are these floored at three
places), the duplicate-square control refused on gap $-1$ and the translated-square
control on a wall at every count on both routes.
`check --replay` was not run again here; the PR records it decided all nine jobs at
`7c801b596`, at the first merge and after the type fix, and `validate_receipt` holds
every retained row to the certificate it names (`checker_input` byte for byte) on every
`check`, which the tests run.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors. A certificate is `{n, side, squares}` with each square `{center: [x, y],
basis: [c, s]}`, every number a rational string.
The bound $s(n) \le S$ follows from six facts, each decided over $\mathbb{Q}$ or fixed
by the format:

1. **The basis is a rotation.** The certificate states $(c, s)$ directly, so the unit
   circle is a check, not a construction: $c^2 + s^2 = 1$ exactly.
   The adapter decides it indirectly: it takes $t = s/(1 + c)$ and requires
   `Pose.basis`, which is $\big((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2)\big)$, to equal
   $(c, s)$. For $c \ne -1$ that equality holds if and only if $c^2 + s^2 = 1$: with
   $t = s/(1+c)$, $(1 - t^2)/(1 + t^2) = ((1+c)^2 - s^2)/((1+c)^2 + s^2)$, which equals
   $c$ exactly when $(1 + c)(1 - c) = s^2$. So the adapter accepts exactly the
   unit-circle bases, and the two routes then see a pose $(x, y, t)$ whose basis is the
   certificate’s. This review’s checker tests $c^2 + s^2 = 1$ directly on every row; all
   716 pass. A basis with $c = -1$ (a rotation by $\pi$, the same square as $(1, 0)$) is
   refused as having no finite half-angle; none occurs here, and the refusal fails
   closed (RF-3).
2. **There are exactly $n$ of them.** The adapter refuses a top level that is not
   exactly `{n, side, squares}`, a count that differs from the declared one, and a
   square that is not exactly a centre and a basis of two rational strings
   (`upper_bound_reports.py:768–798`); JSON numbers are refused, so no float is read.
3. **Each lies in the closed box $[0, S]^2$.** Both routes build the four corners and
   test each against the four walls (`sqpack.verify.verify_packing`, `check_squares`’
   `containment`); this review’s checker tests the centre against each wall by the
   half-extent $h = (|c| + |s|)/2$, which is the same predicate, and also builds the
   corners once for the record.
   Every certificate clears its nearest wall by exactly $10^{-9}$: the author’s
   `rationalize` (`verify_exact.py`) adds that safety, so no corner is on a wall.
4. **Interiors are pairwise disjoint.** Two convex polygons have disjoint interiors iff
   one of their edge normals weakly separates their projections; a square has two
   distinct normals, so four axes decide a pair.
   Both routes take the four axes from the corners they build (`edge_axes`, `axes`) and
   compare projection intervals; the `independent` route records the largest one-sided
   separation over the four axes as the pair’s gap, and `sqpack` the same quantity
   through `_margin_summary`. This review’s checker computes the same maximum from the
   unit normals $(c, s)$ and $(-s, c)$ with half-extents
   $(|u c + v s| + |{-u s} + v c|)/2$, which is the author’s formula, and then decides
   every pair with $dx^2 + dy^2 < 2$ a second way: the area of one square clipped by the
   other’s four closed half-planes (Sutherland–Hodgman over `Fraction`), which must be
   exactly $0$. No pair touches: the least gaps are $\approx 10^{-9}$, again the
   author’s safety.
5. **Every pair is decided.** Neither route filters: `pairs_tested` $= n(n-1)/2$ is held
   by `validate_job`, so no distance lemma is needed.
   This review’s checker also decides every pair by separating axes and clips the 459,
   530 and 542 pairs within $\sqrt2$.
6. **The print is the side.** The frozen comparison holds `offered` to
   $\lceil S \cdot 10^{12} \rceil / 10^{12}$ (`test_each_print_is_its_side_rounded_up`);
   this review recomputed the 12-place ceiling and the 16-place ceiling of each side and
   found each equal to the record’s and to `claims.json`’s.

Arithmetic is CPython `Fraction` throughout every route, including the source’s checkers
and this review’s; no route rounds, dilates or tolerates.
The box convention is the closed box with disjoint interiors, the contract the issue
states; it does not matter here, since nothing touches.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqpack` (`V-sqpack-verify`) | unit shape on corners, corners in the box, all pairs by exact separating axes | `verify_packing`, `check_unit_squares`, `separated`; corners from `_square_from_pose` on the `(c, s)` literals `basis_witness` writes | with `independent`: the adapter (the only reader of the text), `Pose.basis` (the half-angle map), `Fraction` and the separating-axis method; with the producer: nothing of its code; the method and the centre-basis representation are the producer’s first checker’s |
| `independent` (`V-check-rational-witness-independent`) | the same three facts on corners `Pose.corners` builds | `square_failures`, `_separation`, `check_squares` | the same adapter, half-angle map, `Fraction` and method; its corners are built by a second formula and in a different corner order; none of its deciding code is the producer’s |
| the source’s `verify_exact.py` and `verify_polygon_exact.py` | unit circle (the first), unit shape on corners (the second), half-extent or corner containment, all pairs by separating axes with a bounding-box short cut | themselves; not run here, read in full | the producer’s own code; share the witness and `Fraction` |
| this review’s `review_704_check.py` | unit circle, half-extent containment, all pairs by separating axes on unit normals, every near pair again by exact clipping area, the prints | itself: its own reader, its own formulas, standard library only | `Fraction` and the format’s meaning; its author read every route above before writing it, so it is not clean-room |

Two readers of the certificate text therefore exist here (the adapter and this
review’s), and both read the same three sides, 716 centres and 716 bases: this review’s
sides equal the receipt’s at every row, and its least wall clearances and least pair
gaps, computed from half-extents and unit normals rather than corners, equal both
routes’ to every digit, with the least pair at (213, 214), (60, 150) and (199, 204).

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every route. The custody of the bytes rests on the packet’s admission
(`acquire_source --check`), which holds each file to the digest declared at acquisition;
that the retained revision `9bf5d9b` differs from the issue’s pin `c95c493` only in
`LICENSE` and two README lines is the acquisition’s statement, not re-fetched here.
The source’s clipping checker, its 12 corrupted-input controls and 7 analytic area tests
are the author’s runs.

## The Controls

The packet’s two kernel controls per count (`evand_arrangement_reports.job_input`, lines
234–244), decided by both routes and held to the receipt:

| Control | Built to fail on | Scale | Refused on that failure |
| --- | --- | --- | --- |
| square 2 replaced by square 1 | overlap | gross: gap $-1$ | 3 of 3, both routes |
| square 1 moved $S + 2$ right | wall | gross: $-18.6$ to $-30$ | 3 of 3, both routes |

Neither is sharp: nothing in the packet probes a wall or a pair at the $10^{-9}$ scale
where every margin lives, so a route with a tolerance of $10^{-8}$ would pass the packet
as it stands (RF-2). This review built six mutants per count and decided them through
the adapter and both maintained routes, at 227 and 260 (`sharp_controls_704.py`,
receipts `out-controls-n227.json` and `out-controls-n260.json`):

| Mutant | Expected | Both routes, at 227 and at 260 | This review’s checker |
| --- | --- | --- | --- |
| W1: side lowered by exactly the $10^{-9}$ clearance | passes, a corner on the far wall | passed, wall clearance exactly $0$, gaps unchanged | — |
| W2: side lowered by $10^{-9} + 10^{-30}$ | refused on a wall | refused, clearance exactly $-10^{-30}$ (`square 170 violates x<=s` at 227, `square 0` at 260; `container penetration -1/10^30`) | — |
| P1: the least-gap pair closed by exactly its gap along its best axis | passes, an exact contact | passed, least gap exactly $0$ | gap $0$, clipping area $0$ |
| P2: closed by its gap $+ 10^{-30}$ | refused on overlap | refused, `squares 213 and 214 overlap` and `199 and 204`, gap exactly $-10^{-30}$ | gap $-10^{-30}$, clipping area $> 0$ (≈ $4.9 \times 10^{-31}$ at 260, $1.6 \times 10^{-31}$ at 227) |
| B1: a basis with $c + 10^{-30}$ | refused by the adapter | `the basis is no rotation` | — |
| B2: a centre coordinate as a JSON number | refused by the adapter | `not a bounded rational string` | — |

Both routes decide exactly at the $10^{-30}$ scale in both directions, which is what
exact arithmetic promises; the source’s own `shrunken_box` and `invalid_unit_basis`
controls are W2 and B1 in other words.
These mutants are not in the packet and decide nothing for the record until retained
(RF-4).

## The Issue’s Assertions, Mapped

| Assertion | Where | Status |
| --- | --- | --- |
| $s(227) \le 15.563796703670$, $s(229) \le 15.650174756949$, $s(260) \le 16.645778804182$; the exact JSON witnesses authoritative | body, table; `records.json` | **computationally verified here**: three exact routes, every pair decided |
| each decimal is the exact side rounded upward at 12 places | body | **computationally verified here**, all three |
| reductions 0.007271108196, 0.006679492544, 0.011075445311 from the unrounded sides against the website-listed 15.57106781186547, 15.65685424949238, 16.65685424949238 | body | **computationally verified here** against the catalogue’s closed forms $17/2 + 5\sqrt2$, $10 + 4\sqrt2$, $11 + 4\sqrt2$, which T-155’s and T-101’s exact sides sit above; that those were the website’s values at `804eff369` is **asserted**, the pin not fetched |
| upper bounds only; no optimality or uniqueness | body | a scope statement, agreed: nothing here decides either |
| certificates at `c95c493`, one folder per count, with the listed files | body | custody **asserted**: the packet retains `9bf5d9b` and declares the witness blobs unchanged; the PDF, ZIP, SVG, PNG and `.cert` exports are pinned by digest only and not retained |
| `verify_all.py` runs three stdlib `Fraction` checkers; each checks count, unit geometry, containment and every pair with contact allowed: 25,651, 26,106 and 33,670 pairs | body | the pair counts are $n(n-1)/2$, **verified**; the two separating-axis checkers **read here** and sound as written; that all three accept the witnesses is **asserted** (`n{n}_checks.json` retained; not run here) |
| 0.6 to 1.2 s per count under Python 3.12.14 | body | **asserted but unverified**; this review’s checker takes 2.7 to 5.2 s per count under 3.14.7 |
| negative controls for wrong count, duplicated square, invalid basis and shrunken container in `audit/` | body | the receipt is retained and **read**; its verdicts are the author’s; the duplicated square, invalid basis and shrunken box are reproduced on this repository’s routes by the packet’s overlap control, B1 and W2 |
| the three checkers were implemented separately in one AI-assisted campaign and share the witness, `Fraction` and one witness producer; the first two share the separating-axis theorem; the clipping checker shares neither implementation | body | **asserted**; consistent with the two checkers read, which share no function |
| Claude replayed the supplied checkers; no independently authored external checker is claimed | body | **asserted**; this review and PR #704 now supply three such checkers |
| no Lean formalization, no independent human review, no exhaustive comparison with unpublished packings | body | agreed; none is claimed by the record either |
| the orange topology colours are descriptive, separate from the proof | body | not decided; nothing in the record rests on them |
| lineage: started from the catalogue at `804eff369`; asymmetric Young-corner fills around slipped tilted ribbons, centre LP and nonlinear restoration; one construction family; 229 descends from 260 | body | **asserted but unverified**; no identity or descent is measured here |
| AI assistance: OpenAI Codex agents under de Winter’s direction, 25 workers, at most six concurrent; Claude replayed and prepared publication | body | **asserted**; the record credits it as stated |

And T-196’s record on this branch:

| Assertion | Where | Status |
| --- | --- | --- |
| 9 jobs, 512,562 pair decisions, 425.22 route CPU s, 489.54 job wall s, longest 71.04 s | `evidence.yaml`, `results.yaml`, README | **verified from the receipt** (the times are the receipt’s own) |
| every wall cleared by $10^{-9}$ exactly, every pair by at least 1.003, 1.002 and 1.030 × $10^{-9}$ | the same | **computationally verified here**, to every digit |
| both routes refuse the duplicate-square and outside-container controls | the same | **verified from the receipt**, and the controls are gross (RF-2) |
| `relationship_to_generator: independent-implementation`; no route is the source’s code | `evidence.yaml:38315`, `n-227.md:180`, `n-260.md:172` | **verified by reading**: neither route reuses a function of the source; the shared parts between the two routes are this repository’s (adapter, half-angle map, `Fraction`), which `shares` rightly leaves empty, since it names the producer’s components |
| the adapter’s author is not clean-room, having read the source’s three checkers | `evidence.yaml:38356–38368` | consistent with `clean_room: false`; the `read` list omits `producer-code` (RF-1) |
| below the case by 7.27e-3 and 1.11e-2 at 227 and 260; above T-199 by 1.32e-5, T-198 by 1.15e-5, #672 by 1.67e-8 at 229; above #672 by 1.71e-4 at 227 and #678 by 2.56e-5 at 260; the smallest registered side at 227 and 260 | `results.yaml` notes, `claims.json` | **computationally verified here**, every margin exact |
| `V3`/`C3` on the replay, no review retained, no house best packing moved | `results.yaml`, deferral | a record rule, applied correctly: `check_results` derives `V3`/`C3` from a machine-shaped replay, and `select_houses.accepted_review` holds adoption to a review that `covers` the entry |
| draft significance S3 | `results.yaml` | **confirmed by this review**: two case ceilings move by $7 \times 10^{-3}$ and $1.1 \times 10^{-2}$, the first improvement at 260 below $11 + 4\sqrt2$, in a family whose counts Couzo and Daniel improved further within three days; not S4 |

No row claims optimality, local optimality, rigidity, novelty or priority, and none is
decided.

## Findings

**RF-1, minor, non-blocking: the independence record’s `read` list omits
`producer-code`.** `evidence.yaml:38345` says the authors read `specification`,
`certificate-format` and `earlier-review`; the same record’s note at 38356–38368 says
the import lane’s beads carried an earlier static read of the source’s three checkers,
which is why `clean_room` is `false`. `epistemics.md` defines `producer-code` as “the
producer’s own verification code”, which is what was read.
Add it; nothing else in the record changes, since `shares` is empty and the relation
stays `independent-implementation`.

**RF-2, minor, non-blocking: the packet’s controls are gross.** The duplicated square
has gap exactly $-1$ and the translated square clears its wall by $-18$ to $-30$
(`job_input`, lines 234–244), while every margin the certificates have is $10^{-9}$. A
binary64 checker with a tolerance of $10^{-8}$ would pass the packet as retained.
The six mutants above show both routes exact at $10^{-30}$ in both directions, and the
`evidence.yaml` `limitations` (38370) should say that the kernel’s controls are gross
and that the sharp ones are this review’s, once retained.
The kernel is shared by every import that drives it; a sharp contact-plus-$\varepsilon$
job in `JOBS` is the durable fix, and the 10 October review’s RD-2 and the 20 October
#678 review’s RF-2 asked for the same.

**RF-3, note: the adapter refuses a basis with $c = -1$.** A square rotated by $\pi$ is
the square rotated by $0$, and $(−1, 0)$ is on the unit circle, but it has no finite
half-angle and `center_basis_json` refuses it (`upper_bound_reports.py:794`). No
certificate here states one.
The refusal fails closed, so nothing wrong can be admitted through it; a future
certificate that states a basis that way would need the adapter to map $(−1, 0)$ to
$(1, 0)$, a two-line change the docstring should mention.

**RF-4, note, for the record: this review’s programs must be retained.**
`review_704_check.py`, `sharp_controls_704.py`, `margins_704.py` and their receipts
(`out-check.json`, `out-controls-n227.json`, `out-controls-n260.json`,
`out-margins.json`) are in this review’s scratch directory and decide nothing until they
sit under `packing/resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/review/`
with a README, as Stage 4 and `epistemics.md` (Every Run’s Code Is Kept) require, and
the two deciders are registered in `verifiers.yaml` with their independence records.

A further note on the pull request, not the mathematics: its Validation section still
says the hosted run is pending on `5ce183060`; the head `efcd4ddac` has
`packing-required` green.

## Questions for the Author

1. `records.json` keeps `validators_passed: 2` while the README and the audit say three
   checkers passed; the README explains the count, but a reader of the manifest alone
   will not see it.
2. The witness producer’s `rationalize` adds a $10^{-9}$ safety to every wall and scales
   the centres by $1 + 10^{-9}$, so no square touches a wall or another square.
   The numerical sides in `records.json` (15.563796687108 at 227) are
   $1.66 \times 10^{-8}$ below the certified sides; an exact re-solve of the contact
   graph would likely close most of that, as Daniel’s seed did at 260 for #678
   ($1.8 \times 10^{-8}$ below).

## Rungs

**T-196: `V3`/`C3`**, confirmed, independently re-implemented: a retained certificate, a
replay command (`certify`, `check --replay`), a passing replay reproduced here on a
third exact route, retained controls refused by every route that accepted the positive,
and sharp controls refused here; reviewed adversarially here.
This review is the accepted adversarial review that `select_houses.accepted_review`
needs, once mapped and entered in the register with `covers: [T-196]`. It does not reach
`V4`/`C4`: that needs a second accepted adversarial review by a distinct reviewer and a
retained human oversight record, and this is one AI review.
The register’s count of distinct machine methods is unchanged: every route is
`exact-algebraic`, this review’s using a second pair-deciding procedure within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Adoption per Count

The smallest exact certificate at each count, against the case’s verified ceiling and
every report registered or pending on 20 October 2026.

| n | Case ceiling, house best packing | T-196 | Pending or later | Smallest | House best packing to adopt |
| ---: | --- | --- | --- | --- | --- |
| 227 | 15.5710678118654753, T-155 (Kingbird’s $17/2 + 5\sqrt2$, regularized) | 15.5637967036692680 | Couzo #672, 15.563625652343 (Stage 1; no exact side retained) | #672 by its print | **T-196**, with both strong regularizers’ runs; #672 replaces it only once registered, replayed and reviewed |
| 229 | 15.6501615138955532, T-199 (Daniel) | 15.6501747569482132 | T-198, 15.6501632548585302; #672, 15.650174740273 | T-199 | **T-199 stays**; T-196 is recorded as the earlier report it descends from |
| 260 | 16.6568542494923802, T-155 (Kingbird’s $11 + 4\sqrt2$, regularized) | 16.6457788041813798 | Couzo #678, 16.6457532505449560, T-223 in PR #701 at `V0`/`C0`, feasible on four exact routes in the 20 October #678 review | T-223 | **the owner’s call**: T-196 now, by the house rule, since T-223 is not registered and its review is not mapped; or hold T-155 until #701 lands and T-223 takes `V3`/`C3` with its review, which the #678 review supports, and then adopt T-223 once, with T-196 recorded as the earlier report. Adopting T-196 and replacing it within days costs two regularization runs at 260; the 10 October review chose to hold at 131, 132 and 270 for the same reason |

Displayed values are ceilings at sixteen places, or the 12-place values the issues
print. At every count the earlier house best packing stays retained as history, and the
case’s reported and verified ceilings move together.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`evidence.yaml`, `E-de-winter-668-upper-exact-feasibility`.** Add `producer-code` to
  `independence.read` (RF-1); in `limitations`, say the kernel’s two controls are gross
  and name this review’s sharp controls once retained (RF-2); add this document as
  `external_review` with `kind: adversarial`, `reviewer_kind: ai`, `relation: project`,
  `verdict: accepted`, `date: '2026-10-20'`, which makes the entry `reviewed`. Add one
  entry for this review’s checker and sharp controls once retained: `assurance:
  verified`, `method: exact-algebraic`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, `coverage: full` over the
  three certificates, `clean_room: false`, `shares: []`, `read: [mathematics,
  certificate-format, producer-code, producer-output, earlier-review]`.
- **`verifiers.yaml`.** Register `review_704_check.py` and `sharp_controls_704.py` at
  their digests under the packet’s `review/` path, with `written_by` this lane (AI,
  Claude system family, strong tier, maximum reasoning) and the independence record
  above; the sharp-control program drives the two maintained routes and decides nothing
  itself beyond its clipping check.
- **`results.yaml`, T-196.** A `reviews` entry for this document (`kind: adversarial`,
  `reviewer_kind: ai`, `relation: project`, `verdict: accepted`, `covers: [T-196]`); the
  claim and `next_rung` rewritten together so that the claim says *confirmed,
  independently re-implemented* and `next_rung` names `V4`/`C4` and the adoption; the
  significance confirmed at S3.
- **Adoption.** At 227, T-196 as the house best packing over T-155, with both strong
  regularizers’ runs; at 229 nothing; at 260 as the owner decides above.
  The citation deferral `think-qdcc` closes with the adoption.
- **The packet.** A `review/` directory with the three programs, their four receipts and
  a README (RF-4); a sentence in the packet README pointing at this document once
  mapped.

## Comparison with the Earlier Review

Two earlier reads exist, both by an AI reviewer of the Astra (OpenAI) family at the
strong tier and maximum reasoning, and neither text is in Git.
The notes of the parent import bead carry the 18 October source-level review: it read
the source’s three checkers in full, found no blocker and no unsound acceptance path,
and argued the clipping checker’s soundness (counter-clockwise order from the
determinant $c^2 + s^2 = 1$, closed half-planes, exact crossing interpolation, shoelace
area), which this review did not read.
The note on `think-455r` carries the later review at `a70bc1979` on
`codex/review-668-math`: its own exact checker accepted the 716 squares and 85,427
pairs, refused 15 certificate mutants and passed five boundary examples, with no
blocking finding and `clean_room` conservatively false because the source’s checkers
were read after its initial findings.
This review agrees with both verdicts and reaches them by its own checker (85,427 pairs
by separating axes, 1,531 near pairs by clipping area), six sharp mutants per count run
through this repository’s two routes rather than through its own, and the exact ordering
against every registered and pending side.
Its mutants were decided by the routes the record cites, which the summaries do not say
the earlier checker’s were; whether the earlier review raised the gross-control point
(RF-2) or the `read` field (RF-1) cannot be known from the notes.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No fetch from the network: the pins `c95c493` and `9bf5d9b`, the catalogue at
`804eff369` and the omitted files were not checked.
No run of the author’s three checkers or of `check --replay` by this lane; the tests
that admit the receipt ran.
No measurement of the construction family, of 229’s descent from 260, or of any identity
with Couzo’s or Daniel’s later packings.
No house best packing adoption, case-record change or regularization run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
