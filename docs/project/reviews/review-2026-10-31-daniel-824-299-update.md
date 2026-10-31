# Review: Evan Daniel’s s(299) ≤ 17.801238549389 (Issue 824, Update of 29 October)

- **Date:** 31 October 2026
- **Reviewer:** Claude (Anthropic), strong tier (`tbd-strong`), at the xhigh reasoning
  setting its coordinator launched it with (the stage 4 mathematical review lane
  `bold-ritchie-rv-daniel`, for lane L2 of the 31 October intake pass; bead
  `think-8hjz`). See N-7 on the tier.
- **Subject:** the update’s certificate `search/packer/candidates/s299_1028.cert` at
  [evand/square-packing@0e76d9f](https://github.com/evand/square-packing/tree/0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d/search/packer/candidates),
  reported in
  [a comment on jlevy/squares#824](https://github.com/jlevy/squares/issues/824#issuecomment-6488202753)
  and retained in `packing/resources/web/evand-n299-update-2026-10-29/`. The records
  lane registers it as the \#824-update entry on draft PR \#852; it is not yet on
  `main`. Also decided here, as the packing it continues: T-248’s `s299-1025.cert`,
  retained in `packing/resources/web/evand-n299-2026-10-26/`.
- **Read at:** PR \#852 head `e2adcd8f7` (branch `claude/bold-ritchie-xo28us-upper`);
  `main` `ad84e0d2e`.
- **Verdict:** accepted, for finite feasibility.
  The bound holds at the exact side stated.
  No finding is blocking or major.
  Three are minor (M-1 on the update’s local-optimality sentence, M-2 on a truncated
  lineage in the ledger, M-3 on the bead), and seven are notes.

| Certificate | Verdict | Why |
| --- | --- | --- |
| \#824 update, `s299_1028.cert` | **accept for adoption** | Valid; 2.163711e-2 below the house (Kingbird, $33/2 + \sqrt7/2$, and T-101’s rational ceiling), 2.456886e-3 below T-248 and below every report at 299. |
| T-248, `s299-1025.cert` | **accept as recorded only** | Valid; recorded in report order on 26 October, but the update is smaller, so the house rule never adopts it. |

- **Code:** retained once, with the review of issue 845’s certificates
  ([README](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/README.md)),
  in `packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/`; it is
  the same code.

## Summary for the Author

Your update’s certificate is valid.
This review decided it again with a clean-room exact checker written for it, sharing no
code with your checkers or with this repository’s two exact routes, by two methods:
separating axes over all 44,551 pairs with no distance filter, and exact clipped areas.
The side is the certificate’s own header side, and the 12-place print rounds it up
correctly.

| Certificate | Exact side | Print, rounded up | Least wall clearance | Least pair gap |
| --- | --- | --- | --- | --- |
| Update, 299, `ccb323dd…` | 17801238549388584084680137655023 / 10^30 = 17.801238549388584084680137655023 | 17.801238549389 | 5e-21 exactly | 9.999999999999987e-21 |
| T-248, 299, `1ad65a49…` | 8901847717666168847717657266821 / (5 × 10^29) = 17.803695435332337695435314533642 | 17.803695435333 | 5e-13 | 1e-12 |

Ten sharp mutations of each came out as expected under both methods.

- **Against the house.** The side is 2.16e-2 below the catalogue’s $33/2 + \sqrt7/2$,
  decided exactly, and 2.46e-3 below your opening certificate.
- **A new packing, continuing yours.** No symmetry pairs it one to one with T-248; the
  optimal assignment moves 78 squares beyond 0.1. Your vocabulary and the measurement
  agree.
- **What the KKT certificate is.** It is your 80-digit KKT point dilated by
  $1 + 10^{-20}$, a valid packing at $S'$. It proves $s(299) \le S'$ and nothing about
  local optimality, which stays your numerical report (M-1).

## The Claim

$s(299) \le 17801238549388584084680137655023/10^{30}$, the bound of `s299_1028.cert`
(50,626 bytes, SHA-256 `ccb323dd6d69…`), printed as 17.801238549389, rounded up at 12
places (update, line 1). It is a finite packing, so the claim is an upper bound and
nothing more. A checker must establish five things: the parsed file is the pinned file;
each line is a unit square; the squares lie in the box; no two interiors meet; the print
is at least the side.

## Exact Verification

**Custody.** In a blobless clone of `evand/square-packing` taken on 31 October,
`s299_1028.cert` is absent at `d2d5dd9` and first appears at `0e76d9fe5e48…`, committed
2026-10-28T22:44:41−06:00 (04:44:41Z), which is also the repository’s head.
Its SHA-256 at `0e76d9f` and at the head is the update’s (line 7) and the retained
file’s; so are those of `.exact.txt` and `.input.txt`
([custody](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/custody.txt)).
The comment was posted at 04:46:49Z, 2 minutes 8 seconds after the commit.
T-248’s `s299-1025.cert` is unchanged at the head.

**The checker** is `exact_check.py`, described in full in the review of issue 845’s
certificates: a strict token reader, the frame $c = (1 - t^2)/(1 + t^2)$,
$s = 2t/(1 + t^2)$ asserted unit, then method A (corners in the box; the four edge
normals of every pair, no filter) and method B (each square clipped to the box keeps
area 1; every pair within $\sqrt2$ clipped to area 0; farther pairs disjoint by their
circumscribed discs).

**Results**
([update](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/check-s299_1028.json),
[T-248](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/check-s299-1025.json)):

|  | Update | T-248 |
| --- | --- | --- |
| SHA-256 as pinned | yes | yes |
| Valid, separating axes | yes (44,551 pairs) | yes (44,551) |
| Valid, clipped areas | yes (760 pairs clipped) | yes (667) |
| Tilted squares ($t \ne 0$) | 118 | 117 |
| Least near-wall clearance | 1/(2 × 10^20) exactly, square 0 | 5e-13, square 0 |
| Least far-wall clearance | 5.00000000083482e-21, square 30 | 5e-13, square 50 |
| Least pair gap (largest projected gap) | 9.999999999999987e-21, squares 124–134 | 1e-12, squares 3–4 |
| Pairs within 1e-15 | 561 | 0 |
| CPU, both methods | 4.7 s | 3.9 s |

**Controls**
([transcript](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/controls.txt)).
All ten mutations came out as expected for each certificate, and the two methods agreed
on every one: the box at the extent (accepted) and 1e-30 below it (refused); every
square onto the near walls (accepted) and 1e-30 further (refused); the closest pair
closed by its gap along its separating axis (accepted) and 1e-30 further (refused);
square 0 moved 1e-30 past its wall clearance (refused); square 0 duplicated (refused);
the rotation sense reversed (refused, 121 and 90 pairs); the mirror image (accepted).

**The maintained routes, re-run.** This review ran `devtools.upper_bound_reports
evand-n299-update-2026-10-29 decide-job --n 299 --control positive`, and the same for
`evand-n299-2026-10-26`, writing only to scratch
([receipts](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/maintained/)),
after its own checker had decided and reported.
Both routes passed on both certificates over 44,551 pairs.
Their least pair gap and least containment clearance equal this review’s as exact
fractions. The two jobs took 24.1 CPU seconds.

**Trust boundary.** As in the review of issue 845’s certificates: Python’s `fractions`,
the checker’s own reader and two geometric facts; nothing shared with the source’s
checkers or the maintained routes but the reading of `t` as $\tan(\theta/2)$ turning
counterclockwise.

## Sides and Prints

Exact arithmetic
([sides](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/sides.txt)):

- **The house.** $S' < 33/2 + \sqrt7/2$ exactly, since $2S' - 33 = 2.6025\ldots > 0$ and
  $(2S' - 33)^2 < 7$. The margin is 2.163711e-2, the same against T-101’s rational
  ceiling $142583005244258362363432293067/(8 \cdot 10^{27})$.
- **T-248.** $S_{248} - S' = 2.456886 \times 10^{-3}$. T-248 is itself below
  $33/2 + \sqrt7/2$.
- **\#846.** Polkovskyi’s 299, 17.80369543531573879…, lies 1.66e-11 below T-248 and
  2.456886e-3 above the update.
- **The print.** 17.801238549389 is the least 12-place decimal at or above $S'$.

## Report Order

The ledger’s walk at 299, checked against the exact sides and times:

1. T-248, the opening post of \#824 (26 October), recorded below the house.
2. The update (29 October, 04:46:49Z), 2.46e-3 below T-248: recorded.
3. \#846 (30 October, 05:46:42Z), above the update: not recorded.

The decision stands.
Under the house rule the house at 299 becomes the update’s certificate once this review
is mapped and its entry is at `V3`/`C3`. T-248 stays recorded and is never adopted.

## Identity and Lineage

`identity.py` (the review of issue 845’s certificates describes it) measured
([transcript](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/identity.jsonl)):

| First | Second | Best symmetry | One to one | Beyond 0.1 | Beyond 1e-2 | Largest move | Largest turn |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| Update | T-248 | identity | no | 78 | 166 | 0.8019 | 36.64° |
| Update | the house’s witness (Kingbird) | 2 | no | 134 | 246 | 1.281 | 30.75° |

So the update is a new packing at 299, not a refinement of T-248: the update’s four
refill generations and corner–corner kick (line 11) moved 78 squares beyond 0.1. It
continues T-248, which the update and the measurement both place as its start.
The tilt census has 105 squares tilted, 50 of them at 26.80°
([tilts](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/tilts.txt)).

## The KKT Certificate: What It Does and Does Not Establish

`kkt_consistency.py` read `s299_1028.exact.txt` at 100 digits
([transcript](../../../packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/out/kkt.jsonl)).

**What it establishes.**

- **The certificate is the KKT point, dilated.** The side ratio is
  $1 + 1.0 \times 10^{-20}$ and $S' - S^* = 1.78012 \times 10^{-19}$. The certificate’s
  centres divided by that ratio agree with the point to $8.1 \times 10^{-31}$, and its
  angles to $5.7 \times 10^{-34}$ degrees.
- **The certificate is a packing**, decided exactly above, so $s(299) \le S'$.
- **The contact structure** is the source’s: at the point, 46 walls and 561 pairs are
  active below 1e-60, the certificate’s 561 pairs within 1e-15, and 33 squares touch
  nothing, the update’s 33 rattlers (line 13).

**What it does not establish.**

- **That $S^*$ is a bound.** At $S^*$ the point overlaps by up to $6.4 \times 10^{-69}$
  in a pair and $1.3 \times 10^{-71}$ at a wall: a packing only to its precision.
  The bound is $S'$, $1.78 \times 10^{-19}$ above $S^*$ (N-2).
- **Local minimality.** The update’s statement (line 13) is numerical, at 80 digits,
  without interval enclosures, as it says.
  It is strict only modulo 119 flat motions, and the 33 rattlers mean the configuration
  is not isolated. The 64 corner–corner contacts make the feasible set non-smooth, so a
  second-order test on the active set plus a first-order MILP descent test do not cover
  every direction. The least inactive gaps are small, 2.4e-9 at a wall and 9.1e-10 for a
  pair, so the active set is decided by a margin of nine or ten orders of magnitude, not
  of sixty. This review replayed none of that computation.
- **That the question is settled.** So the certificate does not “settle the open
  local-optimality question for this packing” (line 1) (M-1).
- **Global optimality or a lower bound.** Nothing about $s(299)$ from below follows.

If the record carries the local-minimality statement, it carries it as the author’s
report. Registered as a result of its own, it would stand at `V1`, `C0` at most.
No rung of the upper bound depends on it.

## Credit Chain

**The packing** is Evan Daniel’s, found from his T-248 packing by refill and an exact
descent (update, line 11). The commit `0e76d9f` carries a Co-Authored-By trailer naming
Claude, and the source’s `CREDITS.md` says its work was produced by Claude under human
direction.

**The method and the start** keep T-248’s credit, as the update asks (line 11): Chris
Deotte for the method, his multi-gadget fault-line DP, and for the start, his public
Kaggle s(334) packing.
The chain is *Daniel, from his T-248 packing, after Deotte*.

## Significance

**S3, confirmed.** A new packing 2.16e-2 below the catalogue construction, which the
case records as its conjectured optimum, and 2.46e-3 below T-248. It is S3 as T-243 at
182 is. It proves no lower bound or optimum.

## Findings

No finding is blocking: the certificate decides its bound.
Lines are those of the update comment as fetched at 07:40Z on 31 October (15 lines,
SHA-256 `73348e30…`).

### M-1 (minor): “It also settles the open local-optimality question”

**Where.** Update, line 1.

**What.** The certificate is a rational dilation of the KKT point; it proves the upper
bound. The local-minimality evidence is the numerical statement of line 13, which the
same comment calls “not interval proofs”.
Strictness holds modulo 119 flat motions with 33 rattlers, and nothing encloses an exact
KKT point.

**Fix.** The record carries no “settles”, and the entry’s `claim` already does not; the
reply to the author should say why.
Question 1 asks about an enclosure.

### M-2 (minor): The ledger’s lineage for the update is truncated

**Where.** `packing/campaign/issue-intake/upper-bounds-843-846-20261031/ledger.yaml`,
line 390 (`continues: the source's own packing of`), and the rendered `README.md`’s 299
row (“new packing, continuing the source’s own packing of”).

**What.** The sentence stops before its object.

**Fix.** “the source’s own packing of \#824 (T-248)”, then render the README again.

### M-3 (minor): Bead `think-8hjz` still describes T-248’s certificate

**Where.** Bead `think-8hjz`, title and `## Validation` “Claim” line:
`s(299) <= 8901847717666168847717657266821/(5*10^29)`, `s299-1025.cert` at `1be69ca`.

**What.** Its note renumbers it to the update’s entry, but its Claim, packet and pins
are T-248’s.

**Fix.** Claim `s(299) <= 17801238549388584084680137655023/10^30`,
`search/packer/candidates/s299_1028.cert` at `0e76d9f`, packet
`evand-n299-update-2026-10-29`.

### N-1 (note): The update and the measurement agree that it is new

78 squares beyond 0.1 against T-248, 134 against the house.
The record should state the measurement beside the author’s vocabulary.

### N-2 (note): “Exact side $S^*$” is an 80-digit value, not a bound

Update, line 13. The record states $S'$.

### N-3 (note): A side-only Kaggle value lies below

Update, line 15. 17.793636991 (Cats and boxes) comes with no packing and is no report.
“The best publicly known packing”, the update’s words, is accurate as far as is known.

### N-4 (note): The regularized view is not committed

Commit `0e76d9f`, message: “The regularized view failed its checkers (presentation only)
and is not committed.”
The adoption’s regularization runs draw the record’s views; nothing here needs one.

### N-5 (note, for the record): Adoption withdraws the conjecture and stales the rigidity scope

`packing/frontier/n-299.md`: `conjectured_optimum: '17.82287565553229'` is withdrawn,
the new house lying 2.16e-2 below it.
The `rigidity` scope describes the Kingbird witness (square 254) and must be derived
again with `devtools.screen_translation_escape`; with 33 rattlers, “not rigid” stays.

### N-6 (note): T-248 is valid and stays recorded only

T-248’s certificate is a dilation by $1 + 10^{-12}$ with 5e-13 at the walls and 1e-12
between pairs, valid by both methods and both maintained routes, ten controls as
expected. This review may be mapped on T-248 too, which would let its entry take
`V3`/`C3`; the house rule never adopts it, since the update is smaller.

### N-7 (note, process): The review ran at the strong tier

The runbook asks for `tbd-strong-max` at maximum reasoning; this lane was launched as
`tbd-strong`. The coordinator decides whether that meets “strongest tier”.

## Questions for the Author

1. **An enclosure.** Do you plan an interval or exact enclosure of the 299 KKT point, or
   an argument along its 119 flat motions?
   Until then the record carries local minimality as your numerical report (M-1).
2. **The active set.** The least inactive gaps at your point are 2.4e-9 (wall) and
   9.1e-10 (pair). Did your second-order test treat any of them as near-active?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, for the \#824-update entry once
this review is mapped as accepted beside the records lane’s replay: *independently
re-implemented, clean-room, by a Claude agent, a system family the producer also used*.
By the house rule the entry then holds the smallest validated side at 299, and the
adoption moves the house to it.
No `V4`/`C4`, lower bound, optimum, local minimum or rigidity follows.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`verifiers.yaml`, `evidence.yaml`:** as in the review of issue 845’s certificates,
  with an exact-feasibility entry for 299 (both certificates), and this document as
  `external_review` on `E-evand-n299-update-certificate-report` (and, if T-248 takes it,
  on T-248’s report entry).
- **`results.yaml`:** the update’s entry gains this document under `reviews`
  (`adversarial`, `ai`, `accepted`); S3 stays.
- **`ledger.yaml`:** M-2. **Bead `think-8hjz`:** M-3.
- **The adoption:** N-5.

## Independence and Disclosure

The programs, what their author read, and what was seen first are as stated in the
review of issue 845’s certificates.
In addition, this review read bead `think-3xn9`, the \#824-update entry and T-248’s
entry headline and claim.
The \#824-update entry’s notes state the maintained identity figures against T-248 (78,
166, 0.801914), so the identity measurement was not blind to them.
No earlier review of either certificate exists.
The reviewer is a Claude agent, and the producer’s commit names Claude as co-author.

## Comparison with the Records Lane’s Measurements

Read after the findings: `measure/identity.json` in the update’s packet.
Against T-248 the counts and largest move agree exactly (78, 166, 0.801914). Against the
house they agree in count (134, 246); the largest moves differ (1.281 here, 1.133
there), because this tool minimises summed distance and that one summed squared
displacement.

## What This Review Does Not Establish

Any lower bound, optimum or local minimum at 299; that the update’s KKT point is exactly
stationary or a minimum; anything about the source’s search code.

## Files

The same `programs/` and `out/` as the review of issue 845’s certificates, in
`packing/resources/web/evand-issue845-2026-10-29/review/review-2026-10-31/`:
`out/check-s299_1028.json`, `out/check-s299-1025.json`, `out/controls.txt`,
`out/kkt.jsonl`, `out/identity.jsonl`, `out/tilts.txt`, `out/sides.txt`,
`out/custody.txt` and `out/maintained/n299u-positive.json`,
`out/maintained/n299-t248-positive.json`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
