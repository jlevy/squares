# de Winter’s Rescaled Measure for $s(109) \ge s(108) \ge 10.6300379408$ (#1018): Stage 4 Mathematical Review

**Date:** 2026-11-18 UTC. **Subject:** the lower bound of issue
[#1018](https://github.com/jlevy/squares/issues/1018) by Joost de Winter (Delft
University of Technology), the folder `lower_n108/` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/cc20a26845789c2502950041c26709eda8a71081/lower_n108)
at the commit the issue pins, `cc20a268`:
$s(109) \ge s(108) \ge S = 1700799526134255846599/159999384348528500000 = 10.6300379408297\ldots$

**Reviewed at:** `main` at `2980557a2` (the merge of #1016) and the pin above.

**Reviewer:** Claude (Anthropic), an AI reviewer at the strongest tier
(`tbd-strong-max`) and maximum reasoning, the blind stage 4 review lane r108-1118 of the
intake pass of 17 and 18 November 2026 (bead `think-i5en`), prompted separately from the
import lane and sharing none of its context beyond the brief and the committed record.
It read the source as data and ran only programs of its own, kept with their receipts in
[`packing/resources/web/de-winter-1018-review-2026-11-18/`](../../../packing/resources/web/de-winter-1018-review-2026-11-18/README.md).
It is not a human oversight record.
Workflow:
[result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate),
“The review”.

## Summary for the Author

**Verdict: accepted.** The argument from the certificate to the claim is correct and
complete, every exact premise holds, the measure is what the issue says it is, and the
coverage the argument needs holds at all 401 directions.
This review decided that coverage itself, with programs that share no code with yours or
with this repository’s verifier: direction 0 by an exact vertex argument, and directions
1 to 400 by a branch and bound of its own.
No finding is blocking or major.

- **What the proof claims.** No 108 unit squares pack in a square of side
  $S = 2h + (L - 2h)/u$, with $L = 10.63$, $h = 707107/10^6$ and
  $u = 2Bw(D/2) = 319998768697057/320000086112500$; so $s(108) > S$, and
  $s(109) \ge s(108)$ because a packing of 109 squares contains one of 108. $S$ is
  exactly the claimed fraction and prints as 10.630037940829 at 12 places.
- **The rescaling and the enlargement are valid.** The measure is T-216’s pushed forward
  by $x \mapsto (1063/1062)x$, which is again a $D_4$-invariant density on $[0, L]^2$ of
  mass $108 - 10^{-5}$; nothing is transferred from T-216’s certificate, which could not
  carry it (its core, scaled, no longer fits a unit square on its own net).
  The claim rests on the 401 new runs.
  The enlargement is a correct short lemma: shrink a packing in $[0, S]^2$ by $u$ about
  the point $(h, h)$; every centre keeps the clearance its unit square needs, every
  scaled square still holds the core of side $B$ at its nearest net angle, and the count
  goes through. Every step was checked in exact arithmetic.
- **The measure.** All 823 rows of `n108_measure.json.gz`, in file order, are T-216’s
  rows with every coordinate times $1063/1062$ exactly and every mass unchanged, as
  numbers and as strings.
  The merged expansion (6,524 rectangles) is T-216’s, scaled.
  Your copy `Hosono_n108.json.gz` is byte for byte the record’s retained candidate.
- **The archived runs.** Twelve logs hold 401 records, $r = 0, \ldots, 400$ once each,
  every one `verified` at threshold 1, on premises this review recomputed from the file
  (format M, per-bin domain, $D = 83/80000$, 401 angles, $B = 12487/12500$, the mass,
  the SHA-256 of the decompressed measure), from the crate source `d97758bb…` that this
  repository’s census accepts; 266,337,510 rotated nodes in complete trees.
  The bundled crate files of `sqverify_fast/` are byte for byte this repository’s at
  `910b6b12c`.
- **Decided here.** Direction 0: rigorous least capture $1.0074788332$, exact least
  $1.0074788336918702\ldots$ at your sweep’s argmin.
  Directions 1 to 400: all decided by this review’s branch and bound, 5,483,404 boxes in
  973 CPU-seconds. Exact captures at all 401 of your logged poses are at least your
  certified bounds. The least capture any search here found is $1.00468$ (direction 375);
  the same kind of search found $1.0003$ to $1.0008$ on the fine-net certificates of
  #446 and #953. Your certified bounds, $1 + 5 \times 10^{-11}$ to
  $1 + 5 \times 10^{-7}$, mark where your branch and bound stopped, not the margin.
- **Controls.** All 38 controls this review stated before it ran came out as planned,
  among them the 99/100 copy refused exactly at the axis and at $r = 1$, 200 and 399,
  and five wrong readings of the format refused at your logged poses.
  Run afterwards through the same decider, the 99/100 copy is refused with an exact
  witness at every one of the 400 rotated directions.
  Your runs carry no control: no run of a mutated measure.

The findings are notes: the README names a `SHA256SUMS` the folder lacks; the runs were
built with a compiler other than the one this repository pins and carry no binary
digest; the net’s last direction is needed by the verifier’s admission but not by the
argument; the PDF’s earlier figure of 10.622222909689 is not reproduced; and two notes
for the record on the gain at 109 and on how a replay here relates to your checker.
Questions are at the end.

## Scope

**Read.**

- Issue #1018’s body through the REST API, fetched at 01:34:16Z on 18 November, when it
  had no comment and the label `intake` (created at 22:27:34Z on 17 November); retained
  as `programs/issue-1018.json`. Not its comments.
- The source at the pin, as data: `README.md`, `proof_n108.pdf` (one page, typeset with
  Typst 0.15.1 on 17 November at 20:41:11 UTC, numbered 2), `lower_checks.txt` and
  `replay_lower.sh`; the structure of the run logs and of the measure files with `gzip`,
  `grep`, `head`, `tail` and one pretty-print; and, through this lane’s frozen programs,
  the measure, the run logs and the digests of all 35 files.
  The bundled `sqverify_fast/` was compared with this repository’s crate by SHA-256
  only, never opened.
- On `main`: `result-import.md` stage 4; the 11 November review of #953 and the #446
  review it cites, in full, as models; the #1009 review and the headings of the #1005 to
  #1007 review, for the house format and freeze protocol;
  [`packing/sqverify_fast/SOUNDNESS.md`](../../../packing/sqverify_fast/SOUNDNESS.md) to
  its Floating Point section (the theorem, lemma N0, lemma D and the direction lemmas);
  the `REVIEWED_SOURCES` constant of `devtools/sqverify_fast_census.py` and its comment;
  T-216’s register claim; the bound lanes of `n-108.md` and `n-109.md`; `epistemics.md`
  (rungs, which code confirmed it, significance).

**Run.** Eleven Python programs and one C program of this lane’s, frozen before any of
them read the certificate ([What I Ran](#what-i-ran)).

**Seen before the findings were written,** beyond the above: the lane’s brief, which
named the issue, the pin, the source’s files and T-216’s retained candidate, said the
measure was described as Hosono’s `mixed_n108_L1062` rescaled, and asked four questions
(what the proof claims; whether the rescaling argument is valid and $s(109) \ge s(108)$
follows; whether the measure is what it says; whether the runs cover every direction,
with controls); and nothing of the bead `think-i5en` but its id, to which this lane
appended its progress notes under its own heading without reading the others.

**Not read before the findings were frozen:** `check_lower.py` and `stretch_measure.py`
(to be read as data once the findings are frozen); any crate source, the source’s or
this repository’s; the census driver’s code; the reviews of T-216; the import lane’s
branch, packets, receipts and bead notes; the issue’s comments.

**Not run:** any program of the source’s, and any program of this repository’s on the
certificate.

## The Claim

|  | #1018 |
| --- | --- |
| Certificate | `lower_n108/evidence/n108_measure.json.gz` at `cc20a268`, SHA-256 `bd471f65…` (decompressed `d4d16090…`) |
| Claim | $s(109) \ge s(108) \ge S = 1700799526134255846599/159999384348528500000 = 10.6300379408297\ldots$ |
| Measure | 823 rows in $D_4$ orbits, no point; 6,584 images, 6,524 after merging; mass $10799999/100000$ |
| Side, core, net | $L = 1063/100$; $B = 12487/12500$; `proof_net {"step": "83/80000", "last": 400}` |
| Evidence | 401 direction records of `sqverify_fast`, source `d97758bb…`, in twelve logs |
| Lower lanes on `main` at 108 | 10.62 (T-216), reported and verified |
| Lower lanes on `main` at 109 | reported 10.551290369783 (T-180), verified 10.4624294225 (Karakuş) |
| Upper bounds on `main` | 10.90482101232 at 108; 10.94974746831 at 109 |

The issue states the gain as 0.0100 “for both counts”; at 109 that compares with T-216’s
monotone consequence $s(109) \ge 10.62$, which the record does not hold at 109 (N-6).

## The Argument, Re-Derived

Write $w(t) = (1 + 2t - t^2)/(2(1 + t^2))$, half the axis extent of a unit square at
angle $2\arctan t$ (that is, $(\cos\varphi + \sin\varphi)/2$); $w$ increases on
$[0, \tan(\pi/8)]$, since $w'(t) = (1 - 2t - t^2)/(1 + t^2)^2$. Let $t_r = rD$,
$\theta_r = 2\arctan t_r$, $a_r = \max(0, t_r - D/2)$, $U_r = L - w(a_r)$, and let $\mu$
be the file’s measure: each row’s mass spread evenly over its eight images under the
symmetry group of $K = [0, L]^2$, the field order `[x0, y0, x1, y1]`.

1. **The measure.** $\mu \ge 0$ is absolutely continuous, $D_4$-invariant and supported
   in $K$, with $\mu(K) = M = 108 - 10^{-5}$. It is T-216’s measure $\mu_0$ on
   $[0, 10.62]^2$ pushed forward by $x \mapsto \lambda x$, $\lambda = 1063/1062$: the
   map sends $[0, 10.62]^2$ onto $K$ and conjugates the two squares’ symmetry groups, so
   invariance carries over.
2. **What the runs decide.** For every $r = 0, \ldots, 400$ and every centre $c$ in
   $[w(a_r), U_r]^2$, the closed square $Q_r(c)$ of side $B$ at angle $\theta_r$
   satisfies $\mu(Q_r(c)) \ge 1$. A run decides the quadrant $[L/2, U_r]^2$; the quarter
   turn about $(L/2, L/2)$ maps $Q_r(c)$ to $Q_r$ at the turned centre and preserves
   $\mu$, so the quadrant suffices (lemma C1 of `SOUNDNESS.md`).
3. **The scaling.** Suppose 108 unit squares pack in $[0, S]^2$, with
   $S = 2h + (L - 2h)/u$. The map $x \mapsto ux + h(1 - u)$ sends $[0, S]$ onto
   $[h(1 - u), L - h(1 - u)]$, since $uS + h(1 - u) = L - h(1 - u)$, and the packing to
   108 squares of side $u$ with disjoint interiors in $K$.
4. **Clearance.** A unit square at folded half-angle tangent $t$ has its centre at least
   $v = w(t) \le \sqrt{1/2}$ from each wall of $[0, S]$. After the map that distance is
   at least $uv + h(1 - u)$, and $uv + h(1 - u) - v = (1 - u)(h - v) \ge 0$ because
   $u < 1$ and $h > \sqrt{1/2} \ge v$. So the scaled centre is at least $w(t)$ from each
   wall of $K$ although the scaled square is smaller than a unit square.
5. **Fold and node.** A symmetry $g$ of $K$ takes each scaled square to one at angle
   $\theta \in [0, \pi/4]$, $t = \tan(\theta/2) \le \tan(\pi/8)$, and keeps the
   clearance. Take the node with $|t - t_r| \le D/2$. Then $t \ge a_r$, so
   $w(a_r) \le w(t)$ and the centre lies in $[w(a_r), L - w(a_r)]^2$, where step 2
   applies.
6. **The core fits.** The core $Q_r(c)$ is turned by $\delta$ against the scaled square,
   $z = \tan(|\delta|/2) = |t - t_r|/(1 + t t_r) \le D/2$, and its extent along either
   of that square’s axes is $2Bw(z) \le 2Bw(D/2) = u$, the scaled square’s side.
   So the core lies in the closed scaled square, its interior in the square’s interior,
   and $g^{-1}$ maps it to a core of the same mass in the original scaled square.
7. **Count.** The 108 cores have disjoint interiors and $\mu$ has a density, so their
   masses add: $108 \le \mu(K) = 108 - 10^{-5}$, a contradiction.
   No packing fits in $[0, S]^2$, nor in a smaller square, so $s(108) > S$. And
   $s(109) \ge s(108)$: removing a square from a packing of 109 leaves a packing of 108.

Only step 2 needs a large computation.
Steps 1 and 3 to 7 are exact arithmetic on the file, which
[`rv1018_premises.py`](#what-i-ran) recomputed:

| Quantity | Value |
| --- | --- |
| $B(1 + D)$ (lemma N0 (b)) | $999996421/10^9$ |
| $B(1 + D/(1 - D^2/4))$ (N0 (e)) | $319998768697057/319999913887500$ |
| $u = 2Bw(D/2)$, the sharp extent | $319998768697057/320000086112500$, the PDF’s value; $1 - u = 4.1169 \times 10^{-6}$ |
| $t_{400}^2 + 2t_{400} - 1$ (N0 (c)), $t_{400} = 83/200$ | $89/40000 > 0$ |
| $2h^2 - 1$ | $309449/500000000000 > 0$ |
| $S$ | $1700799526134255846599/159999384348528500000$, the claimed fraction |
| $S$ to 40 places | $10.6300379408297263703123176570767509670882$ |
| $S - L$; the margin $h(1 - u)$ | $3.7941 \times 10^{-5}$; $2.9111 \times 10^{-6}$ |
| Least quadrant width $U_r - L/2$ | $4.6079$ (at $r = 400$) |

The enlargement is a general lemma.
For any coverage certificate with core $B$ on a net of step $D$, it turns the slack
between $2Bw(D/2)$ and 1 into the gain $(L - 2h)(1/u - 1)$: here $3.79 \times 10^{-5}$,
and at T-216’s own premises ($L = 10.62$, $B = 0.9977$, $D = 83/40000$) about
$2.14 \times 10^{-3}$. The gain of 0.01 comes from the rescaled measure on the finer
net: the new core is $12487/12500 = 0.99896$, which at T-216’s scale is $0.998020$,
$3.20 \times 10^{-4}$ more than T-216’s $0.9977$, and the half step allows it.
T-216’s core scaled by $1063/1062$ does not fit on T-216’s net
($B\lambda(1 + 83/40000) = 141700766911/141600000000 > 1$), so nothing of T-216’s
certificate carries over; its measure is the starting point and the credit.

## Hypotheses Each Checker Assumes

| Hypothesis | Where it enters | Status here |
| --- | --- | --- |
| H1. The format: `[x0, y0, x1, y1]`, mass $m/8$ per $D_4$ image, densities adding | every checker | read from the format; reproduces the source’s axis argmin and bound to $7 \times 10^{-11}$; wrong readings refused (W1 to W5) |
| H2. Every row inside $K$ with positive extents and mass | steps 1, 7 | holds: all 823 |
| H3. $M < n$ | step 7 | $n - M = 1/100000$ exactly |
| H4. Lemma N0 (a) to (e) on the declared net | the verifier’s admission | all hold, values above |
| H5. Every bin that holds a folded angle has $a_r < \tan(\pi/8)$ | step 5 | holds for $r = 0, \ldots, 399$; the bin of 400 holds none |
| H6. $D_4$-invariance | steps 2, 5, 6 | holds exactly on the merged expansion |
| H7. The capture on every quadrant | step 2 | decided here at all 401 directions, and by the source’s runs |
| H8. $h > 1/\sqrt 2$, $0 < u < 1$, $u = 2Bw(D/2)$ | steps 3, 4, 6 | hold exactly |

## The Measure Against T-216’s

`rv1018_measure.py` compared `n108_measure.json.gz` with T-216’s retained
`mixed_n108_L1062/candidate.json.gz` exactly.
Both have $n = 108$ and mass $10799999/100000$; the new side is
$531/50 \cdot 1063/1062 = 1063/100$; the 823 rows match one to one in file order, each
coordinate the old one times $1063/1062$ and each mass the same rational, written with
the same string.
The merged expansions have 6,524 rectangles each, and the new one is the
old one scaled, its densities divided by $(1063/1062)^2$. The two files differ otherwise
only in `B` (`0.9977` against `12487/12500`) and the net (`83/40000`, `last` 200,
against `83/80000`, `last` 400). The source’s `evidence/Hosono_n108.json.gz` is byte for
byte the retained candidate (SHA-256 `acaf2759…`). The run logs’ `input_sha256` is the
SHA-256 of the decompressed `n108_measure.json.gz` (`d4d16090…`).

Descriptive facts: the densest merged rectangle has density 37,568; 156 rows are thinner
than $1/500$.

## The Archived Runs

`rv1018_runs.py` read the twelve logs `directions_AAA_BBB.jsonl.gz` as data.

- **Coverage.** 401 direction records, $r = 0, \ldots, 400$ exactly once, each file
  exactly its named range; the last line of each file a summary.
- **Verdicts.** Every record `verified` at threshold `1`, least certified bound at least
  1: the least among rotated directions is $1 + 5.4 \times 10^{-11}$ at $r = 76$.
- **Methods.** The axis sweep at $r = 0$ only (5,542 by 5,542 events, 30,713,764
  vertices, argmin $(6893368290553469509/1062000000000000000)$ on the diagonal, inside
  $[L/2, L - 1/2]^2$); branch and bound elsewhere, every tree complete
  ($\text{nodes} = 2\,\text{leaves} - 1$), 367,017 to 1,010,517 nodes, depth at most 30,
  every least-bound box centred in its quadrant.
- **Premises.** Every summary states the premises recomputed here: format M, per-bin
  centre domain, $D = 83/80000$, 401 angles, last tangent $83/200$, net from
  `proof_net`, $B = 12487/12500$, $L = 1063/100$, $n = 108$, mass $10799999/100000$ and
  $1/100000$ below $n$, $B(1 + D) = 999996421/10^9$, 823 rows and 6,524 merged
  rectangles, no point or segment, and the input digest above.
- **Build.** Every summary names crate source `d97758bb…`, the digest `REVIEWED_SOURCES`
  lists for `910b6b12c` with declared nets accepted, and
  `rustc 1.100.0 (0ef1bc386 2026-11-09)`; no binary digest.
  Every summary has status `PARTIAL` (each covers its range), six threads, no refused
  direction and no injected fault; its node, direction and CPU totals equal its
  records’.
- **Totals.** 266,337,510 rotated nodes (the issue’s figure), 5,407.8 direction
  CPU-seconds (1.50 CPU-hours, 20.3 µs a node), 40,167 direction seconds of wall time.

So the runs cover every direction the argument needs, and one more: $r = 400$ is
required by the verifier’s admission premise (c), since $t_{399} = 0.4139625$ is below
$\tan(\pi/8)$, but its bin, $[0.41448125, 0.41551875]$, lies wholly above $\tan(\pi/8)$
and holds no folded angle (N-4).

## What This Review Decided

**Direction 0, completely.** `rv1018_axis.py` computes the events $x_k \pm B/2$ of every
merged rectangle in $[L/2, L - 1/2]$ exactly (5,542 in each coordinate, the source’s
counts), evaluates the bilinear capture at all 30,713,764 grid vertices as one float64
matrix product of nonnegative terms, and bounds each value below rigorously by the
product’s rounding ($\gamma_K$, $K = 6524$) and an a priori error of
$1.65 \times 10^{-13}$ per overlap.
The least of the 64 smallest vertices is evaluated exactly.

|  | Original | Every mass times 99/100 |
| --- | --- | --- |
| Rigorous least capture | $1.0074788332233897$ | $0.9974040448911559$ |
| Exact least vertex value | $1.0074788336918701996\ldots$ | $0.99740404535495149761\ldots$ |
| At | the source’s argmin, on the diagonal | the same vertex |
| Verdict | `AXIS_DIRECTION_DECIDED` | `REFUSED_EXACT` |

The source’s logged bound at its argmin is $6.97 \times 10^{-11}$ below the exact value
there, as an outward-rounded sweep’s should be; the exact values equal the issue’s
“1.007478833692” and “0.997404045355”.

**Directions 1 to 400, completely.** `rv1018_decide.py` runs `rv1018_bnb.c`, a branch
and bound written for this review.
For a box of centres with midpoint $p_0$ and half-widths $d_x, d_y$, the square at every
centre of the box contains the eroded square
$E = \{|u'| \le h' - b_u, |v'| \le h' - b_v\}$, where $u', v'$ are the coordinates along
the square’s sides from $p_0$, $b_u = c\,d_x + s\,d_y$ and $b_v = s\,d_x + c\,d_y$, and
$h' = B/2 - 10^{-12}$ absorbs the float frame.
It also contains four strips beside $E$ whose thickness depends on the centre; since
each strip’s mass grows with its thickness, a minimum over eight pieces of the shift
bounds their sum for every centre in the box.
Rectangles inside $E$ count their whole mass and pass to the children; the others count
lower bounds on their areas in $E$ and in the strips, from the concavity of chord
lengths (trapezoids at nodes, positive pieces only, an allowance for the float error of
each chord). A box is accepted when the bound, times $1 - 10^{-11}$, is at least 1. Any
box that cannot be accepted has its centre estimated, and a centre estimated below the
threshold is evaluated exactly.

|  | $r = 1$ to 200 | $r = 201$ to 400 | All |
| --- | ---: | ---: | ---: |
| Directions decided | 200 | 200 | 400 |
| Boxes | 1,829,790 | 3,653,614 | 5,483,404 |
| CPU-seconds | 286.2 | 686.7 | 973.0 |
| Least accepted bound (at $r$) | $1 + 4.4 \times 10^{-8}$ (11) | $1 + 4.5 \times 10^{-9}$ (390) | $1 + 4.5 \times 10^{-9}$ (390) |
| Most boxes (at $r$) | 27,841 (1) | 24,423 (397) | 27,841 (1) |
| Greatest depth | 22 | 20 | 22 |

No box reached the depth limit of 72 and no candidate arose.
The 19 sampled directions, decided first, took the same number of boxes again in the net
runs. The least accepted bound is where the search stopped, not the least capture.
The allowances: the chord error at most $3.6 \times 10^{-10}$ (at $r = 1$, where
$\sin\theta_1 = 0.0021$), the float frame within $1.1 \times 10^{-16}$ of the exact
cosine and sine, covered by the $10^{-12}$ taken off the half-side.
So every direction’s quadrant has capture at least 1: step 2 holds at all 401 directions
by this review’s programs alone.

**Poses at the source’s runs.** `rv1018_poses.py` evaluated the exact capture at the
centre of every rotated direction’s least-bound box and at the axis argmin: 401 poses,
each at least the source’s certified bound for that box and at least 1, every centre in
its quadrant. The least is $1.0081366$ ($r = 320$), the median $1.0305$; 16 of them were
evaluated again by the second exact method (vertical chords) and agree as rationals.

**A seeded search at 19 directions.** `rv1018_sample.py` fixed its sample by rules
written before it ran: $r = 1, 2, 3, 100, 200, 300, 399, 400$; the direction of least
certified bound (76), of most nodes (398) and of least exact pose (320); and one seeded
index in each eighth of the net (26, 52, 132, 187, 245, 293, 331, 375). A $41 \times 41$
grid, compass searches from the nine best starts, every end point exact.

| Least found | Where | Median of the per-direction least | 99/100 witness |
| --- | --- | --- | --- |
| $1.0046798276$ | $r = 375$, $(9.3507, 8.2004)$ | $1.00833$ | 17 of 19 directions |

At $r = 26$ and $52$ the least found is $1.01028$ and $1.01042$, above $100/99$; the
decider later found captures below $100/99$ at both (N-5), so this search, as it claims,
gives upper bounds on each direction’s least capture and nothing more.

## Controls

`programs/controls-plan.json` states 38 controls and their outcomes, frozen with the
checker.
Must-refuse controls fail on a checker that accepts everything, must-accept ones
on a checker that refuses everything.

| Id | Change | Expected | Outcome |
| --- | --- | --- | --- |
| P0 | none: the measure, and the PDF’s $h$ and $S$ | premises hold | as planned |
| P1 | total mass 108 (row 0 heavier by $10^{-5}$) | refused | as planned: $M < n$ fails |
| P2 | $B = 12488/12500$ | refused | as planned: $B(1 + D) > 1$ |
| P3 | `last` 399 | refused | as planned: the net stops short of $\tan(\pi/8)$ |
| P4 | step $83/79000$ | refused | as planned: $B(1 + D) > 1$ |
| P5 | $h = 7071/10000 < 1/\sqrt 2$ | refused | as planned |
| P6 | the claim $S + 10^{-30}$ | refused | as planned |
| M0 | none | scaled copy | as planned |
| M1 to M4 | row 400’s $x_0$ plus $10^{-30}$; row 0’s mass times $1 + 10^{-30}$; factor $1064/1062$; rows reversed | refused | as planned; the reversal is reported as a permutation of the scaled rows |
| R0 | none | the logs cover the net | as planned |
| R1 to R12 | a direction deleted; one duplicated; one `refused`; a bound 0.99999; a summary’s input digest, $B$, crate digest, node total, centre domain or angle count changed; a tree made incomplete; a least-bound centre moved past $U_r$ | refused | as planned, all twelve |
| W0 | the right reading, at $r = 0$ and every fourth rotated direction (101 poses) | no pose below its logged bound; the axis value within $[0, 10^{-6}]$ of the logged one | as planned: none below; $+6.97 \times 10^{-11}$ |
| W1 | rows without their $D_4$ images | refused | as planned: 101 of 101 poses below |
| W2 | T-216’s rows not rescaled, in the side 10.63 | refused | as planned: 1 pose below; the axis off by $+0.1213$ |
| W3 | T-216’s core $B = 0.9977$ | refused | as planned: 1 pose below; the axis off by $-0.0031$ |
| W4 | the standard step $83/40000$ for the angles | refused | as planned: 2 poses below |
| W5 | the field order read as `[x0, x1, y0, y1]` (49 rows degenerate) | refused | as planned: 56 poses below |
| A0 | direction 0 of the original | decided | as planned (rigorous least $1.0074788332$) |
| A1 | every mass times 99/100, direction 0 | refused exactly | as planned: $0.9974040453549515\ldots$ |
| D0 | the original at the rotated directions | decided | as planned: the 19 sampled, then all 400 |
| D1 to D3 | every mass times 99/100 at $r = 1$, 200, 399 | refused exactly | as planned: witnesses $0.9999347$, $0.9996144$, $0.9996777$ after 807, 19 and 9 boxes |
| D4 | the threshold $10^{-4}$ above the least capture the search found ($r = 375$) | refused exactly | as planned: a witness of $1.0047642 < 1.0047798$ after 38,221 boxes |

## What the Checkers Share

| Checker | Decides | Trusts |
| --- | --- | --- |
| The source’s runs: this repository’s `sqverify_fast`, crate source `d97758bb…`, built by the author with rustc 1.100.0, six threads | Coverage at all 401 directions, one run each | The reviewed crate; a compiler this repository does not pin; the author’s machine; that the logs are the runs’ |
| A census replay here (not run) | Coverage at all 401 directions with whole-net controls | The reviewed crate, census driver and controls; rustc 1.98.0; this host |
| This review’s programs | Every exact premise; the measure’s identity; the logs’ coverage; direction 0 completely; directions 1 to 400 completely; 401 poses and a 19-direction search | CPython 3.14.7 `fractions`, gmpy2 2.3.1 (GMP), numpy 2.5.2 with OpenBLAS at one thread; IEEE binary64 in gcc 13.3.0 code under the stated allowances; its own code |

This review’s programs share no code with `sqverify_fast` or with the source.
They were written from the mathematics: the PDF’s argument, the format’s stated meaning,
and the statements of `SOUNDNESS.md`, which this lane read before writing them.
The area bound for a straddling rectangle uses the concavity of chord lengths, the idea
of that document’s lemma R2; the box bound itself (an eroded square and a ring of
strips) is not the crate’s mean-value bound (R3 to R5), and the axis decision is this
lane’s own matrix form of the vertex argument.
All of them share the mathematics of steps 1 to 7 and the reading of the format; the
reading is checked against the source’s own logged values, and the mathematics was
re-derived above. An error in that shared mathematics would pass all of them; none was
found.

Authorship overlaps at the system family: the issue says the repository files and checks
were produced with Claude (Anthropic) and the rescaling, the computation and the proof
with GPT-6.2 Astra (OpenAI); the crate was written by a Claude agent of this project;
this review is a Claude agent with its own prompt and files.

## Findings

No finding is blocking or major.
Grades: blocking, major, minor, note.

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| N-1 | note | the claim | the certificate proves the strict bound $s(108) > S$, and $s(109) \ge s(108)$ |
| N-2 | note (author) | `README.md` line 24 | the README lists `SHA256SUMS`; the folder has none at the pin |
| N-3 | note (author, record) | the run summaries | built with rustc 1.100.0 where this repository pins 1.98.0; no binary digest; the bundle omits `rust-toolchain.toml` and the crate’s tests |
| N-4 | note | the net | direction 400 is required by the verifier’s premise (c) and holds no folded angle |
| N-5 | note (author) | the archived runs | no control: no run of a mutated measure; this review’s decider refuses the 99/100 copy at all 400 rotated directions |
| N-6 | note (record) | the issue’s gain at 109 | the record holds 10.551290369783 (reported) and 10.4624294225 (verified) at 109, not 10.62 |
| N-7 | note (record) | a replay here | a census replay runs the very crate the source ran |
| N-8 | note (author) | `proof_n108.pdf`, first paragraph | the earlier figure 10.622222909689 is not reproduced |

**N-1 — the strict bound.** No packing fits in $[0, S]^2$, so $s(108) > S$, and the
claim’s $\ge$ is what a lower-bound entry states.
The 12-place print 10.630037940829 is below $S$, so the bound holds as printed.

**N-2 — the missing checksum file.** `README.md` line 24 lists “`SHA256SUMS`:
checksums”; `git ls-tree` at the pin holds no such file in `lower_n108/` (other folders
of the repository have one).
Add it, or drop the line.

**N-3 — the build.** Every summary names `rustc 1.100.0 (0ef1bc386 2026-11-09)`. This
repository pins `1.98.0` in `packing/sqverify_fast/rust-toolchain.toml`, which the
bundle does not copy, nor `tests/adversarial.rs`, `tests/declared_net.rs`,
`clippy.toml`, `README.md`, `INDEPENDENCE.md` or `independence-record.yaml`;
`replay_lower.sh` therefore builds with whatever Rust is installed (“Rust 1.98 or
later”). The source digest `d97758bb…` identifies the crate the runs were built from,
and every bundled source file is byte for byte this repository’s at `910b6b12c` and
`f9ddfeeef`, but no summary records the binary’s digest.
Nothing in the mathematics depends on it; it is why the runs stand as reported until
replayed here with the pinned toolchain.

**N-4 — the last direction.** Lemma N0 (c) asks that the last tangent pass
$\tan(\pi/8)$, so the net needs $t_{400} = 83/200$: $t_{399}^2 + 2t_{399} - 1 < 0$. The
argument needs only that the bins cover $[0, \tan(\pi/8)]$, which those of $r \le 399$
already do ($t_{399} + D/2$ and $t_{400} - D/2 = 66317/160000$ both give
$19384489/25600000000 > 0$). So the run at $r = 400$ is required and unused; harmless.

**N-5 — no control.** The archived runs decide the original measure only.
`lower_checks.txt` reports that the axis capture at the argmin falls to $0.997404\ldots$
when every mass is reduced by 1%, a single exact integration at one pose; it is correct
(this review’s 99/100 axis decision refuses with that value), but it is not a run of the
verifier on a mutated certificate.
The census route runs the 99/100 copy at every direction
([result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate)).
What it should find: after its planned controls, this review ran the 99/100 copy through
its own decider at all 400 rotated directions (101 CPU-seconds), and every one was
refused with an exact witness in its quadrant, the axis too.
Witnesses run from $0.99629$ to $0.9999998$, since the decider stops at the first centre
it finds below 1; at $r = 26$ and 52, where the sampled search had found nothing below
$100/99$, they are $0.9999495$ and $0.9988058$. So a whole-net 99/100 control should
refuse everywhere, some directions narrowly.

**N-6 — the gain at 109.** The issue says the gain is 0.0100 for both counts.
At 108 it is $S - 10.62 = 0.0100379\ldots$ At 109, T-216’s $s(108) \ge 10.62$ implies
$s(109) \ge 10.62$, but `n-109.md` holds the reported 10.551290369783 (T-180) and the
verified 10.4624294225; against those the claim raises the lanes by 0.0787 and 0.1676.
How the record words the consequence at 109 is the import lane’s, under the runbook’s
row for “a consequence of another claim, such as monotonicity”.

**N-7 — what a replay here would be.** For T-216 the census replay was a
re-implementation sharing the producer’s components, since the producer’s checker was an
adapted copy of this repository’s crate.
Here the source ran this repository’s crate itself, at the reviewed source, so a census
replay reruns the producer’s own checker: in the record’s terms, reproduced with the
producer’s code.
This review’s complete decision of all 401 directions is the independent
route; it sets no rung by itself, since its decider’s soundness has not been
adversarially reviewed ([Rungs and Significance](#rungs-and-significance)).

**N-8 — the earlier figure.** The PDF’s first paragraph says that “an earlier
computation on the original orientation grid gave 10.622222909689… for both 108 and
109”. The PDF’s own enlargement at T-216’s premises ($L = 10.62$, $B = 0.9977$,
$D = 83/40000$, the same $h$) gives $10.622135524982\ldots$ That figure is no part of
the claim.

## Questions for the Author

1. Would you add the `SHA256SUMS` the README lists, or remove the line (N-2)?
2. Which binary produced the runs?
   Could the summaries, or a receipt beside them, record its digest, and would you build
   with the toolchain this repository pins (N-3)?
3. Did you run the verifier on a mutated measure?
   Do you know the least capture at each direction?
   This review’s searches found $1.0047$ at $r = 375$, and its decider found a capture
   below $100/99$ at every direction (N-5).
4. How was 10.622222909689 obtained (N-8)?

## Verdict

**Accepted.** The certificate proves $s(108) > S$ and hence $s(109) \ge s(108) > S$,
with $S$ the claimed fraction.

- Every hypothesis the argument needs holds exactly, and the enlargement lemma is
  correct.
- The measure is T-216’s, rescaled as the issue says.
- The coverage holds at all 401 directions: decided here by this review’s own programs,
  and by the source’s archived runs of this repository’s verifier.
- All 38 controls came out as planned.
- No defect of the certificate or its mathematics is open; every finding is a note.

## Rungs and Significance

**Now.** With this review recorded as the `external_review` of the reported entry (state
`informally-verified`) and listed in the entry’s `reviews` (kind `adversarial`, verdict
`accepted`), the entry derives `C1`, a read of a recorded claim, at `V0`.

**This review’s own runs** decide every load-bearing part: the premises exactly,
direction 0 by the vertex argument, and directions 1 to 400 by `rv1018_bnb.c`. They are
complete, independently re-implemented and clean room (by a Claude agent, a system
family the source also used).
The runbook’s replay is the source’s checker or a first-party implementation whose
soundness has been adversarially reviewed; `rv1018_bnb.c` has a self-test and controls
but no such review, so these runs set no rung.
They can be registered beside the replay, and would carry the result to *independently
re-implemented* once a soundness review accepts the decider.

**After a census replay.** A complete `sqverify-fast` census of the retained candidate
at all 401 directions, with the whole-net control receipt, held to the 6 October
declared-net checklist, of which items 1, 3 and 7 as the 11 November review of #953
lists them hold here (format M with no point, no `scaling_factor`, `proof_net` with
exactly `step` and `last`, no metadata; lemma N0 and the mass in exact arithmetic; this
review), supports `V3/C3`, reproduced with the producer’s code (N-7). `V4/C4` would need
a second accepting adversarial review by a distinct reviewer and a human oversight
record.

**Significance: S3, confirmed.** If correct, the claim is the strongest lower bound on
record at 108, $0.0100379$ above T-216, narrowing the gap to the upper bound from
$0.2848$ to $0.2748$; at 109 it raises the reported lane by $0.0787$ and the verified
lane by $0.1676$, the gap falling to $0.3197$. It is T-216’s measure on a declared net
of half T-216’s step, the certificate kind of T-142, T-143 and T-233, with a short
enlargement lemma: a substantive case result, as T-216 and those entries were scored.
The lemma is new to the record and reusable, but it adds $3.8 \times 10^{-5}$ here; a
reusable technique or bound family would be S4, and this result is neither; 108 and 109
are not central open cases (S5). Should the rescaling and the enlargement be applied
across the record’s measure certificates, that family would be scored on its own.

## The Price of a Full Replay

| Route | Basis | Capture (CPU-h) | Controls (CPU-h) | Total (CPU-h) |
| --- | --- | ---: | ---: | --- |
| `sqverify-fast` census, here | 266,337,510 nodes at the source’s 20.3 µs a node, or at the 18.6 µs a node of the n = 31 sample the #446 review priced with | 1.38 to 1.50 | 0.1 to 0.6 | 1.5 to 2.2 |
| This review’s `rv1018_bnb.c`, all 400 rotated directions | measured here, 5,483,404 boxes | 0.27 | — | 0.27 |

The census controls have cost 8 to 40 percent of the capture where the 99/100 copy
refuses early, as it should everywhere here (N-5). Both routes are far below the owner’s
cap of 40 CPU-hours an item; neither needs a decision.

## What I Ran

All with CPython 3.14.7 as `python -I`, at `nice -n 19`, `OPENBLAS_NUM_THREADS=1`, at
most two processes, from the packet’s `programs/`. The programs and the controls plan
were frozen in `frozen/checker-frozen-digests.txt` at 02:26:45Z and pushed at 02:27:16Z
(`87e79188b`), before any of them read the certificate.

| Program | Receipt (`out/`) | Result | CPU (s) |
| --- | --- | --- | ---: |
| `rv1018_selftest.py`, synthetic only | `selftest.json` | `PASS`: 39 checks, 2,016 box points | 9.0 |
| `rv1018_custody.py` | `custody.json` | crate identical at `910b6b12c` and `f9ddfeeef`; T-216 copy identical; `SHA256SUMS` missing | 0.1 |
| `rv1018_premises.py` | `premises.json` | `PREMISES_HOLD` | 0.5 |
| `rv1018_measure.py` | `measure.json` | `SCALED_COPY` | 0.5 |
| `rv1018_runs.py` | `runs.json` | `RUNS_COVER_THE_NET` | 0.3 |
| `rv1018_axis.py` | `axis.json` | `AXIS_DIRECTION_DECIDED` | 8.7 |
| `rv1018_axis.py --factor 99/100` | `axis-99_100.json` | `REFUSED_EXACT` | 8.2 |
| `rv1018_poses.py` | `poses.json` | `ALL_POSES_CONSISTENT` | 4.6 |
| `rv1018_sample.py` | `sample.json` | `NO_COUNTEREXAMPLE_IN_SAMPLE` | 10.4 |
| `rv1018_decide.py`, $r = 200$, the price | `decide-price-r200.json` | decided | 2.8 |
| `rv1018_decide.py`, the 19 sampled | `decide-sample.json` | 19 of 19 decided | 54.8 |
| `rv1018_decide.py`, $r = 1$ to 200 and 201 to 400, two processes | `decide-net-001-200.json`, `decide-net-201-400.json` | 400 of 400 decided | 1,021.4 |
| `rv1018_controls.py` | `controls.json` | `ALL_CONTROLS_AS_PLANNED` | 33.3 |
| `rv1018_decide.py --factor 99/100`, $r = 1$ to 400, outside the plan | `decide-net-99_100-001-200.json`, `decide-net-99_100-201-400.json` | 400 of 400 refused with an exact witness | 157.3 |

These runs took 1,312 CPU-seconds (0.36 CPU-hours); with the synthetic trials before the
freeze, about 0.5 CPU-hours in all, against the brief’s 10. The last row ran after the
planned controls and before the findings were frozen, with the frozen program and its
`--factor` option; it was not in the plan.
The decider’s runs report their own CPU (973 seconds for the net); the table gives the
process time. The summaries of the net runs carry the frozen program’s label
`ALL_SAMPLED_DIRECTIONS_DECIDED`, which there means every requested direction.

The run was priced before it started, as the plan required: the direction-200 run took
2.1 CPU-seconds and 11,613 nodes, so the 19-direction sample was priced at about a
CPU-minute, and the sample’s mean of 2.7 CPU-seconds a direction priced the full net at
about 0.3 CPU-hours, under the plan’s 4.

What went wrong along the way, before the freeze it precedes:

- The first version of the branch and bound bounded a box by its eroded square alone; on
  a uniform synthetic measure with 0.1% slack it needed about $10^8$ boxes.
  The ring of strips, and then a single cumulative integration per rectangle and side,
  brought that to about $4 \times 10^6$ boxes in 9 seconds.
- The self-test’s first two failures were the test’s own: a threshold $10^{-9}$ above an
  attained capture leaves only a sliver to find, and a small axis measure without its
  background captured nothing.
  Two later changes to the decider followed from them: a candidate is now any box centre
  estimated below the threshold by more than $10^{-12}$ (it was $10^{-9}$), and the
  child with the lower centre estimate is searched first.
  Neither changes which boxes are accepted.
- The decider’s control D4 was first planned at $10^{-6}$ above the least capture found;
  synthetic trials showed such a threshold leaves a set too small for the search to hit
  at sharp minima, so the plan states $10^{-4}$.
- A first `git push` of the freeze was refused for want of credentials and retried with
  `gh` as the credential helper; the commit was unchanged.

## Reproduction

The packet’s
[README](../../../packing/resources/web/de-winter-1018-review-2026-11-18/README.md)
gives every command, from the repository root with the source cloned at the pin.
Each program exits 0 on the retained inputs and prints its verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
