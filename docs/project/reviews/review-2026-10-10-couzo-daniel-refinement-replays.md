# Review: Couzo’s and Daniel’s Rational Refinement Replays (T-128, T-130, T-131)

**Date:** 10 October 2026. **Verdict: accepted, for finite feasibility only.** All
fourteen certificates the three entries register, and the equal-side n = 155 certificate
recorded as an evidence update to T-128, prove the upper bounds their claims state.
Every retained receipt reproduces here job for job, a third exact route written for this
review agrees with the two maintained routes at every number they share, and no defect
blocks the claims. Six findings are recorded, none blocking.
Each entry can take `V3`/`C3` once its confirming evidence entry and this review are
added to the register; none can take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 2026-10-10 intake pass
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), under
`think-fvz4`, written by an AI agent (Claude, model Opus 5.5, `claude-opus-5-5`)
prompted separately from the import lanes that built the three packets, with no shared
context. Its relation to the results is `project`. It moves no rung, writes no register
row and adopts no house; the proposed record changes are listed at the end for the
adoption round.

## Claims Covered

| Entry | Source | Counts | Exact sides as the claims print them |
| --- | --- | --- | --- |
| T-128 | [Francisco Couzo, #451](https://github.com/jlevy/squares/issues/451), `franciscouzo/square-packing` at `ffd900d` | 105, 108, 127, 131, 155, 180, 228, 306 | 10.790618268107144505815379335866, 10.904821012320356429055628704222, 11.810878787589179839642367108002, 11.951105389414677460694240669403, 12.95249894401400738196585056694, 13.916993522477832483558124720393, 15.604601475729674284720634102188, 17.963433717491425739593840075522 |
| T-130 | [Couzo, PR #460 comment](https://github.com/jlevy/squares/pull/460#issuecomment-6070798890), `franciscouzo/square-packing` at `2d32a6e` | 84, 86, 105, 175, 270 | 9.697934799014921307163820128651, 9.820535407496742209971278280039, 10.789303783748158831034729697921, 13.767155163542549110085664417048, 16.9367230228761834072968722597 |
| T-131 | [Evan Daniel, #465](https://github.com/jlevy/squares/issues/465), `evand/square-packing` at `e008180` | 132 | 11.987099332245063227179742877435 |
| (T-128 update) | Daniel, #465, `hunt1_n155.cert` | 155 | 12.95249894401400738196585056694, equal to T-128’s |

Every side is a terminating decimal, and each claim’s decimal is the exact side, not a
rounding of it: the third route reads each claim from
[results.yaml](../../../packing/frontier/results.yaml) and holds it to the parsed
certificate as an exact rational.
The 12-decimal displays in #451 and in the #460 comment, read here against the exact
sides, all round upward.
Construction credit stays as the entries record it: Ryan Xu’s #432 packings at 84, 86,
105, 108, 127, 131 and 175, Nate Chaoweeraprasit’s SQUISH packings at 155 and 180 (180
through Siddharth Gupta’s #438), Evan Daniel’s #399 packing at 270 and Couzo’s own at
228 and 306, refined with David Ellsworth’s `refine_packing`, Couzo’s basin hopping and
Daniel’s `fq`; Daniel’s exact contact solver wrote every certificate.
At 132 Daniel reports a different local minimum reached from Couzo’s packing.

**Read in full.** The three register entries and their evidence atoms; the three packet
READMEs and acquisition records; issue #451’s body; the report modules
`couzo_refinement_reports.py`, `couzo_followup_reports.py` and `evand_hunt_reports.py`;
the kernel `evand_arrangement_reports.py`; the parser and conversion in
`evand_exact_certificates.py` (`parse`, `Pose`, `basis_witness`, `corner_squares`);
`check_rational_witness_independent.py`; `sqpack.witness` (`_materialize`,
`_square_from_pose`, `exact_verify`, `_margin_summary`) and `sqpack.verify` in full; the
[Gupta](review-2026-10-08-gupta-exact-refinements.md) and
[Ry-Xu](review-2026-10-08-ryxu-rational-radical-packets.md) precedents; T-125 and T-127;
[epistemics.md](../../../epistemics.md) on verification, confirmation and review
records.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on a four-core host
shared with other lanes, at most two worker processes, in a worktree of
`claude/determined-rubin-yjfy2a` at `b0486a547` with this review’s tool added.

| Command | What it decides | Outcome | Wall |
| --- | --- | --- | --- |
| `python -m devtools.check_half_angle_area replay-t128 --workers 2` | T-128’s 24 jobs through both maintained routes, each held to its retained row | all 24 equal | 339.0 s |
| `python -m devtools.couzo_followup_reports check --replay` | T-130’s 15 jobs, serial in-process | all 15 equal | 130.5 s |
| `python -m devtools.evand_hunt_reports check --replay` | T-131’s 6 jobs, n = 132 and 155 | all 6 equal | 38.5 s |
| `python -m devtools.evand_hunt_reports check-claims` | the frozen comparison with T-098, T-115 and T-128 | rebuilt equal | 0.5 s |
| `python -m devtools.couzo_refinement_reports check` | T-128 admission, no geometry | admitted | 0.6 s |
| `python -m devtools.check_half_angle_area decide --workers 2` | the third route on all fifteen certificates, 90 controls, every cross-check | no disagreement | 37.0 s |

T-128’s module has no replay command, so `replay-t128` drives the kernel’s own
`replay_receipt` with T-128’s namespace, as `check --replay` does for the other two
(RD-1). A replay compares every field of each fresh job with its retained row except the
measured times. The T-130 and T-131 replays ran concurrently, one process each.

The receipts’ own totals, recomputed by the third route, are the numbers the register
prints: 770,052 pair decisions and a longest job of 40.89 s for T-128; 384,846
decisions, 131.84 route CPU seconds, 132.22 job wall seconds and a longest job of 22.42
s for T-130; 123,486 decisions, 38.66, 38.79 and 7.72 s for T-131.

## From Certificate to Bound

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors. A certificate gives a rational side $S$ and, for each square, a rational
centre $(x, y)$ and $t = \tan(\theta/2)$. The bound $s(n) \le S$ follows from four
facts, each of which the routes decide or the format fixes:

1. **Every piece is a unit square.** $(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$
   satisfies $c^2 + s^2 = 1$ for every rational $t$, so the corners
   $(x, y) + R_\theta(\pm\tfrac12, \pm\tfrac12)$ form a unit square.
   `sqpack.verify.check_unit_squares` and the independent checker’s `square_failures`
   each re-check unit edges and right angles on the corners they receive.
2. **There are exactly $n$ of them.** The parser refuses a header that differs from the
   expected count and any row beyond the $n$-th; a square listed twice would overlap
   itself and be refused.
3. **Each lies in the closed box $[0, S]^2$.** A convex set lies in the box iff its
   corners do; equivalently, a square at angle $\theta$ reaches $h = (|c| + |s|)/2$
   either side of its centre along each axis.
4. **Interiors are pairwise disjoint.** For two convex polygons this holds iff some edge
   normal of either separates them (the separating-axis theorem), iff the area of their
   intersection is zero.

Arithmetic is exact `Fraction` arithmetic throughout; no route rounds, dilates or
tolerates. The solver’s dilation is already in the rational inputs.

**The box convention does not matter here.** Every positive clears its nearest wall by
exactly $1/(2 \cdot 10^{20})$ on all three routes and every pair by a least Euclidean
distance of $9.9999999999999865 \times 10^{-21}$ or more, so the closed squares are
pairwise disjoint and inside the open box.
The bound holds under an open or closed box and under disjoint interiors or disjoint
closed squares. The centres run up to about $S - 1/2$, so a centred box $[-S/2, S/2]^2$
would leave squares outside; the coordinates fit $[0, S]^2$, the box all three routes
use.

**What the parse decides, and what it does not.** A misreading of a literal shared by
both routes would decide a different packing.
If that packing passed, $s(n) \le S$ would still hold for it, so soundness does not rest
on the parse; attribution does.
The third route re-reads every source text with its own literal reader and matches all
fifteen sides and every centre and half-angle with the maintained routes’ inputs, which
closes it.

## Trust Boundaries

| Route | Decides | Code it trusts | Shares with the others |
| --- | --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | `sqpack.witness`, `sqpack.verify`; at T-128 and T-130 this is the `verify.py` the source author copied and ran | the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same three facts on rational corners | `check_rational_witness_independent.check_squares` | the same parse and map, and the corners `Pose.corners` builds; `Fraction`; the separating-axis method |
| third route (proposed V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area | `devtools.check_half_angle_area` | `Fraction` and the format’s half-angle meaning only |

The kernel also owns the job layout, the two controls and `validate_job`, which both
maintained routes are held to.
The custody of the bytes rests on each packet’s own admission: T-128’s complete
originals against the acquisition roster’s SHA-256, T-130’s rebuilt texts against the
pinned Git blob identities, T-131’s retained files through `acquire_source.check`. Those
are premise checks; the third route calls them and decides nothing from them.

**What stays unchecked.** CPython’s `fractions` and integer arithmetic are common to
every exact checker here.
The source’s own checkers (Daniel’s `verify_cert.py` and `verify_cert2.py`, and Couzo’s
copy of `verify.py`) were not run.
The KKT, no-descent, reduced-Hessian, jamming and local-minimum statements are numerical
source reports and are not decided.
That the published file is the one its author meant is attested by the pins only.

**The third route.** Its author read both maintained routes and their parser before
writing it, so it is not a clean-room implementation.
It imports none of their parsing or deciding code.
It reads literals without `Fraction`’s string parser, forms no corner to decide
containment, and decides a pair by the circumscribed-disc rule when the centres are at
least $\sqrt2$ apart and otherwise by clipping one square with the other’s four closed
half-planes and testing the exact shoelace area for zero.
It therefore uses a second pair-deciding procedure, not a second arithmetic.
On all fifteen certificates it decided 213,064 pairs, clipping 5,241, and found no
overlap and no square outside the box.
Its least wall clearance equals both maintained routes’ to every digit at all fifteen,
and its least Euclidean distance is at least their separating-axis gap at all fifteen.

## The Controls

**The kernel’s two controls cannot pass vacuously.** `validate_job` requires, on both
routes, `verification_passed` false, a non-empty failure list, the complete pair count
and the negative diagnostic each control is for: a pair gap below zero for the
duplicated square, a wall clearance below zero for the square moved by $S + 2$. A route
that accepted everything, or one that refused the control for some other reason, would
fail admission.

**They are gross, though (RD-2).** The duplicate’s gap is exactly $-1$ at all fifteen,
and the moved square lies 3.0 to 15.8 units outside the box; a binary64 checker with a
$10^{-9}$ tolerance would refuse both.
They show the routes can refuse, not that they decide at the $10^{-20}$ scale where
these certificates live.
The maintained routes’ exactness is shown instead by their margins, exact rationals that
a third, differently computed route reproduces.

The third route adds four sharp, two-sided controls to the same two, each a full
decision of the certificate, and all 90 reached their required outcome:

| Control | Required | Scale |
| --- | --- | --- |
| square 1 replaced by square 0 | refused | gross |
| square 0 moved by $S + 2$ | refused | gross |
| side reduced by the least far-wall clearance | accepted: the box is closed | exact contact |
| the same side less $10^{-40}$ | refused | $10^{-40}$ |
| the closest pair translated into contact | that pair accepted | exact contact |
| that square pushed $10^{-30}$ of the centre distance further | refused | $\sim 10^{-30}$ |

## Agreement to Every Digit

The third route held each certificate to the record and found no disagreement:

- all fifteen sides and every $(x, y, t)$ equal the maintained routes’ checker inputs;
- the register’s fourteen claimed decimals equal the exact sides, and T-128’s n = 155
  decimal equals Daniel’s equal-side certificate’s side as well;
- all fifteen least wall clearances are exactly $1/(2 \cdot 10^{20})$, at a near wall,
  on three routes and two formulas;
- every least Euclidean distance, between $9.9999999999999865 \times 10^{-21}$ and
  $9.9999999999999937 \times 10^{-21}$, is at least the separating-axis gap.

The record’s other numbers also check: T-130’s n = 105 lies below T-128’s by exactly
262896871797134956129927589/200000000000000000000000000000; T-131’s n = 132 lies below
T-098’s by exactly 84571108928763690161985083/20000000000000000000000000000, which is
$4.23 \times 10^{-3}$; the two n = 155 certificates share 152 of 155 exact poses and
differ exactly at the three squares the source report lists as free or flat
(`check-claims`).

## Findings

**RD-1, non-blocking: T-128 had no replay of its retained receipt.** The module admits
the receipt and can certify afresh, but `certify` writes the retained receipt in the
packet, as all three modules do, so no command decided T-128’s 24 jobs again and held
them to it. `check_half_angle_area replay-t128` does so now.
The confirming evidence can name that command, or the module can gain a `check --replay`
like the other two.

**RD-2, non-blocking: the kernel’s controls are not sharp.** As above.
The 2026-10-05 module carried sharper kinds (tightest pair overlapped, side shrunk past
its clearance, side shrunk one unit) that the arrangement kernel did not keep.
Carrying them into the kernel would make each packet’s own replay show exactness.

**RD-3, non-blocking: the maintained routes read each certificate once, together.** Both
take one parse and one half-angle map, and the independent checker’s corners are built
by the shared module rather than by the checker, as that module states.
The checker re-checks their shape, so no wrong conversion can pass a non-unit square,
but a misread literal would reach both routes alike.
The third route’s own reading closes it.

**RD-4, non-blocking: one maintained route is the producer’s checker.** Issue #451
states that the source ran this repository’s `verify.py`, copied, in exact rational
arithmetic, and the T-130 comment reports the same.
So at T-128 and T-130 V-sqpack-verify reproduces with the producer’s code, and the
independently re-implemented relation rests on V-check-rational-witness-independent and
the third route. With the third route, two deciding implementations independent of the
producer’s code decide every count, as both first-party routes did in Gupta’s precedent,
where they shared the same four premises.
At T-131 neither maintained route is the producer’s.

**RD-5, non-blocking for this claim: no private-worker custody at T-130 or T-131.**
T-128 has an actual private-worker transaction (8.91 s call); T-130 and T-131 have none.
The rung for finite feasibility does not need it.
Gupta’s and Ry-Xu’s house adoptions closed it first, so the adoption round should too
before any house moves.

**RD-6, non-blocking: two pending reports are smaller at three counts.** The
certificates at 131, 132 and 270 remain valid bounds but are no longer the smallest
known; see the adoption table below.

## Rungs

**T-128: `V3`/`C3`.** Machine-replayed here: all eight certificates and their sixteen
kernel controls on both maintained routes, and the eight with their 48 controls on the
third route, with a certificate, a replay command, a passing replay and retained
controls; reviewed adversarially here.

**T-130: `V3`/`C3`**, for the same reasons over five certificates, ten kernel controls
and 30 third-route controls.

**T-131: `V3`/`C3`**, for the same reasons over n = 132 and its controls.
Its evidence also confirms the n = 155 certificate, which T-128 may cite.

None reaches `V4`/`C4`: that needs a second accepted adversarial review by a distinct
reviewer and a retained human oversight record, and this is one AI review.
The register’s count of distinct machine methods is unchanged: every route is
`exact-algebraic`, the third using a second pair-deciding procedure within it.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

## Adoption per Count

The smallest exact certificate at each count, against the case’s current verified
ceiling and every report pending on 2026-10-10. Sides from #470, #476 and #481 are from
their packets and issues, as those lanes compared them; none is replayed here yet.
#470’s are decimal poses, interval-proved only after their declared dilation, with no
exact witness.

| n | Case ceiling, house | Reviewed here | Pending | Smallest | House to adopt |
| --- | --- | --- | --- | --- | --- |
| 84 | 9.6980520605096981, Ry-Xu | T-130, 9.6979347990149214 | #470, 9.697934799017 | T-130 | T-130 |
| 86 | 9.8205657300098206, Ry-Xu | T-130, 9.8205354074967423 | #470, 9.820535407499 | T-130 | T-130 |
| 105 | 10.7906765754107907, Ry-Xu | T-128, 10.7906182681071446; T-130, 10.7893037837481589 | #470, 10.789303783751 | T-130 | T-130; T-128’s stays verified, not selected |
| 108 | 10.9048247851109049, Ry-Xu | T-128, 10.9048210123203565 | #470, 10.904821012324 | T-128 | T-128 |
| 127 | 11.8109366475118110, Ry-Xu | T-128, 11.8108787875891799 | #470, 11.810878787590 | T-128 | T-128 |
| 131 | 11.9511500449119512, Ry-Xu | T-128, 11.9511053894146775 | #481, 11.9496595880358604; #470, 11.951105389418 | #481 | #481 once registered, replayed and reviewed; T-128 if it fails |
| 132 | 11.9913278876915015, T-098 | T-131, 11.9870993322450633 | #476, 11.9869541936403928; #470, 11.986956226066 | #476 | #476 once registered, replayed and reviewed; T-131 if it fails |
| 155 | 12.9525032026045129, SQUISH T-115 | T-128, 12.9524989440140074; Daniel’s equal side | none smaller | T-128 | T-128, Couzo’s certificate committed nine hours before Daniel’s; Daniel’s recorded as an equal-side confirmation |
| 175 | 13.7688992766137689, Ry-Xu | T-130, 13.7671551635425492 | #470, 13.767155163551 | T-130 | T-130 |
| 180 | 13.9176534174501843, Gupta T-127 | T-128, 13.9169935224778325 | #470, 13.916993522482 | T-128 | T-128 |
| 228 | 15.6046024545460570, Daniel’s exact optima | T-128, 15.6046014757296743 | none | T-128 | T-128 |
| 270 | 16.9378072284460292, Daniel #399 | T-130, 16.9367230228761835 | #481, 16.9297801262411717; #476, about 16.936720031122; #470, 16.936723155038 | #481 | #481 once registered, replayed and reviewed; then #476, then T-130 |
| 306 | 17.9634381397640029, Daniel’s exact optima | T-128, 17.9634337174914258 | #470, 17.963433717497 | T-128 | T-128 |

Displayed values are ceilings at sixteen places, or the 12-place values the issues print
for #470 and #476. #470 claims exactly those 12-place values, so comparing with them is
exact, though at every count but 270 they lie within $10^{-11}$ of Couzo’s sides.
#476 states its 12-place values as upward roundings of its exact sides, and at 132 and
270 they order against their neighbours by at least $2 \times 10^{-6}$. At 131, 132 and
270 this review recommends holding the current house until the smaller import has its
own two-route replay and mapped review, rather than adopting a T-entry certificate and
replacing it again; credit #476’s n = 132 to Mishapolk’s packing as its starting point.
At every count the earlier house stays retained as history, and the case’s reported and
verified ceilings move together, in coordination with
[#403](https://github.com/jlevy/squares/pull/403) and
[#435](https://github.com/jlevy/squares/pull/435), which own the exact-side case
records.

## Proposed Record Changes

For the adoption round; this review writes none of them.

- A confirming evidence entry per entry, `E-couzo-451-exact-feasibility` (the id T-128’s
  module already names), `E-couzo-460-followup-exact-feasibility` and
  `E-evand-465-record-hunt-exact-feasibility`: `assurance: verified`,
  `method: exact-algebraic`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`, the packet’s facts as
  `certificate`, the replay commands above, `replay_status: passed`, verifiers
  V-sqpack-verify, V-check-rational-witness-independent and V-check-half-angle-area,
  this review as `independence_record`, and limitations naming RD-3 and RD-4.
- A verifier entry V-check-half-angle-area for the new route, `role: decides`.
- On each of T-128, T-130 and T-131: the confirming evidence, `V3`/`C3`, a `reviews`
  entry for this document (`kind: adversarial`, `reviewer_kind: ai`,
  `relation: project`, `verdict: accepted`, covering all three), the new test file among
  the controls, and claim, notes and `next_rung` rewritten together.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty, priority or human
oversight. No replay of #470, #476 or #481. No run of the sources’ own checkers or
solvers. No house adoption, case-record change or private-worker custody for T-130 or
T-131.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
