# wand125’s Linear Certificate for $s(122) \ge 563/50$: Mathematical Review

2026-11-18. Reviewer: Claude (Anthropic), `tbd-strong-max` tier at maximum reasoning,
lane r144-1118 (bead `think-rxs3`, under the import `think-nd7g`), prompted separately
from the replay lane and sharing none of its context beyond the brief and the committed
record. Workflow:
[result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate),
“The review”. Scope: `mixed_n122_L1126`, wand125/square-packing at `a9f76c3`, with its
release asset `certificates__mixed_n122_L1126.tar.gz` at SHA-256 `6443eae0…5deb`, and
the register entry T-144 on `main`. On `main` the import packet
[`wand125-linear-n122-2026-10-10`](../../../packing/resources/web/wand125-linear-n122-2026-10-10/README.md)
holds the manifest but not the candidate or the certificate, so this lane fetched the
source at the pin and the asset at its digest itself. The programs and receipts are in
[`wand125-linear-n122-review-2026-11-18`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md).
This review moves no bound and adopts nothing.

## Summary for the Author

**Decision: accept.** The argument from the certificate to the claim is correct and
complete, and every hypothesis it needs holds in exact arithmetic.
If 122 unit squares fitted in the closed square of side $563/50$, closed cores of side
$9977/10000$ at net angles, one inside each square, would be disjoint, each of measure
at least one, against a total mass of $122 - 1/100000$.
So the certificate proves the strict bound $s(122) > 563/50$, and the same holds at every
$N \ge 122$, since $N$ squares would need mass at least $N$.

The computation the claim needs, a capture of at least one at every centre of every one
of the 201 net angles, was decided here **completely, by programs of this review’s own**.
They were written from the mathematics and the certificate’s documents and frozen before
they read the certificate, and before your checker was opened, and they share no code
with it:

- node 0 by a vertex argument in exact integers: the least capture over the centre
  domain is exactly $1.0039577044080\ldots$;
- nodes 1 to 200 by a rigorous branch and bound of this review’s own, FULL_SUMMARY;
- every exact premise; that each of the 201 checker inputs encloses exactly the
  candidate’s 14,184 images; and the comparison with Green’s $G_{11}$, which your bound
  exceeds by more than $0.0307191$, as your README says.

Both deciders refuse the 99/100 mutant with exact witnesses. The least capture found in
a seeded search at 24 angles is $1.00176$ (angle 196); the `lower` fields of your
records, down to $1 + 4.1 \times 10^{-10}$, are where the branch and bound stopped, not
the margins.

Your checker, read as data after this review’s programs were frozen, decides what its
records say it decides, by sound interval arithmetic.
There is no blocking or major finding.
Two minor findings concern the bundle’s custody and wording: the release’s `SHA256SUMS`
does not list the asset (M-1), and the README’s statement of what was checked omits the
centre domain (M-2). One minor finding is the record’s: at $n = 126$ the reported lane is
now T-180’s $a(126) = 11.3133\ldots$, above $563/50$, so T-144 would raise the reported
lane at four counts and the verified lane at five (R-1).

## The Claims

| Item | Value |
| --- | --- |
| Certificate | `mixed_n122_L1126` at `a9f76c382d023b4095899c4eb7ea7483b8b87ecf` |
| Claim | $s(122) \ge 563/50 = 11.26$, hence $s(N) \ge 563/50$ for every $N \ge 122$ |
| Measure | 502 point, 1,268 segment and 3 rectangle orbits under $D_4$; 14,184 images, 13,948 distinct after merging |
| Total mass | $12199999/100000 = 122 - 1/100000$ |
| Net | core side $B = 9977/10000$; half-angle tangents $t_j = 83j/40000$, $j = 0, \ldots, 200$ |
| Candidate | file SHA-256 `cd427ddb…500c`; the source’s digest `c91a7509…9ed4` (SHA-256 of the JSON with sorted keys and compact separators, reproduced here) |
| Asset; proof bundle | 31,784,537 bytes, `6443eae0…5deb`; 38,912,523 bytes, `3986d902…55d0`, 810 files |
| Checker | `code/unified_linear_verify.cpp`, `0249726a…a06d` (`V-wand125-unified-linear-verify-cpp`) |

On `main` the reported lower bounds are Green’s $11.22928087555$ (DS7 Theorem 9 with
$k = 11$) at 122 to 125, and Hosono’s closed form $a(126) = 11.313323850997$ (T-180) at
126; the verified lower bounds are Karakuş’s strip bounds, $11.0475115548$ to
$11.2354552767$. The upper bounds run from $11.5355339059$ at 122 to $11.7426406871$ at
126.

| $n$ | Reported lane on `main` | Verified lane on `main` | 563/50 raises |
| ---: | --- | --- | --- |
| 122 | Green, $11.22928\ldots$ | Karakuş, $11.04751\ldots$ (+0.21249) | both |
| 123 | Green, $11.22928\ldots$ | Karakuş, $11.09481\ldots$ (+0.16519) | both |
| 124 | Green, $11.22928\ldots$ | Karakuş, $11.14190\ldots$ (+0.11810) | both |
| 125 | Green, $11.22928\ldots$ | Karakuş, $11.18878\ldots$ (+0.07122) | both |
| 126 | T-180, $11.31332\ldots$ | Karakuş, $11.23546\ldots$ (+0.02454) | verified only |
| 127 | T-180, $11.37167\ldots$ | Karakuş, $11.28193\ldots$ | neither |

The comparisons are exact ([`out/lanes.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/lanes.json)):
$563/50 - G_{11} > 0.030719124449$, $563/50 - (1 + \sqrt{105}) > 0.013049234$, and
$(563/50 - 1/2)^2 > N - 11 + 1/4$ for $N \le 126$ but not at 127.

## What Was Read

**Before the checker froze (06:03:49Z), as data.** The lane’s briefs and the bead
`think-rxs3`; `result-import.md` stage 4; the house review of 11 November
(`review-2026-11-11-wand125-fine-net-n28-n30.md`) as the format model, and PRs #1013
and #1014’s structure; on `main`, the import packet’s README and `source-manifest.json`;
grep lines naming Green’s, Nagamochi’s and the closed form’s values in
`packing/frontier/`. From the source at `a9f76c3`: the commit, the tree, the
certificate’s `README.md`, `manifest.json`, `completion-audit.json`, `ASSET.json` and
`requirements.txt`, `mixed_n101_L1028/README.md`, and the first 250 lines of
`docs/lower-bounds.md`. From the asset and its bundle, to write the readers: the
listings, the shape of `candidate.json` and `input.txt`, the sum of the masses (which
showed that a primitive’s mass is its orbit’s), and a table of the 201 records’ status,
nodes, `lower`, seconds, $t$ and $E$. The `code/` files were hashed and not opened.

**After the checker froze, before the findings froze.** The source’s
`unified_linear_verify.cpp` in full, its driver `unified_linear_verify.py`,
`replay_linear_bundle.py`, the first 120 lines of `unified_measure.py`, `replay_angle` in
`unified_linear_full_verify.py` and `interval` in `mixed_rotated_verify.py`, all as data;
the register entries T-144 and T-180; the front matter of `n-122.md` to `n-127.md`; the
release’s current `SHA256SUMS`.

**Not read.** The other files of `code/` (hashed only); the replay lane’s branch, receipts
and notes; the import packet’s `receipts/` and `reported-n122.json`; this repository’s
`devtools.audit_wand125_linear` and `devtools.fine_net_followup`, which this review
neither read nor ran; and the earlier reviews of this certificate and its siblings, read
only after the findings were written
([Comparison With Earlier Reviews](#comparison-with-earlier-reviews)).

**Disclosed.** `tbd show think-rxs3` printed the parent bead `think-nd7g`’s notes of 10
to 12 October, which report that the intake’s readers held the premises and that two
angles replayed with the source’s checker; and the import packet’s README summarizes the
same. This review decided nothing from either.

## The Argument, Re-Derived

Write $L = 563/50$, $B = 9977/10000$, $b = B/2$, $D = 83/40000$, $t_j = jD$ for
$j = 0, \ldots, 200$, $\theta_j = 2\arctan t_j$, $c_j = (1 - t_j^2)/(1 + t_j^2)$,
$s_j = 2t_j/(1 + t_j^2)$, and $Q_j(c)$ for the closed square of side $B$, centre $c$ and
sides along $(c_j, s_j)$ and $(-s_j, c_j)$.

1. **The measure.** Each primitive of mass $m$ puts $m/8$ on each of its eight images
   under the symmetry group $D_4$ of $K = [0, L]^2$: a point mass, a mass spread
   uniformly by length on a segment, or uniformly by area on a rectangle. So $\mu \ge 0$
   is $D_4$-invariant, supported in $K$, and $\mu(K) = M = 122 - 1/100000$. A segment’s
   share in a core is its mass times the fraction of its parameter inside, so no square
   root enters.
2. **Fold.** A unit square’s orientation is defined modulo $\pi/2$, and a reflection of
   $K$ maps $\varphi$ to $-\varphi$, so each square $S$ of a packing has an image $gS$,
   $g \in D_4$, with orientation in $[0, \pi/4]$, half-angle tangent
   $t \in [0, \tan(\pi/8)]$. The fold is square by square.
3. **Reach.** Every $t \in [0, \tan(\pi/8)]$ lies within $D/2$ of some $t_j$, since
   $t_{200} = 83/200$ gives $t^2 + 2t - 1 = 89/40000 > 0$, so $t_{200} > \tan(\pi/8)$.
   The last node is needed: $t_{199} + D/2$ gives $-4544311/6400000000 < 0$.
4. **Containment.** The turn $\delta$ between $gS$ and $\theta_j$ has
   $z = \tan(|\delta|/2) = |t - t_j|/(1 + t t_j) \le D/2$. The concentric core turned by
   $\delta$ lies in the open unit square if $B(\cos\delta + \sin|\delta|) < 1$, and
   $\cos\delta + \sin|\delta| = (1 + 2z - z^2)/(1 + z^2) \le 1 + 2z \le 1 + D$, with
   $B(1 + D) = 399908091/400000000 < 1$, the manifest’s `rotated_side_upper`. The sharp
   value at $z = D/2$ is $63985225828447/64000068890000$, a clearance of about
   $2.3 \times 10^{-4}$.
5. **Centre domain.** The core lies in the open interior of $gS$, which lies in $K$, so
   the core lies in $K$ and its centre in $D_j = \{c : Q_j(c) \subseteq K\} =
   [L/2 - E_j, L/2 + E_j]^2$, $E_j = L/2 - b(c_j + s_j)$, since the core reaches
   $b(c_j + s_j)$ from its centre along each axis. $E_j$ runs from $4.92452$ (node 200)
   to $5.13115$ (node 0). The domain is the core’s own, so no bin-end estimate of the
   unit square’s reach is needed.
6. **Capture.** The certificate asserts $\mu(Q_j(c)) \ge 1$ for every $j$ and every
   $c \in D_j$. Then $g^{-1}Q_j(c)$, $c$ the centre of $gS$, is a closed square in the
   open interior of $S$ with the same measure, by invariance.
7. **Count.** The cores of distinct squares lie in disjoint open interiors, so
   $122 \le \sum_S \mu(\mathrm{core}(S)) \le \mu(K) = 122 - 1/100000$, a contradiction.
   A packing in a smaller square is one in $K$, so $s(122) > L$; and a packing of
   $N \ge 122$ squares contains one of 122, so $s(N) > L$.

**The quarter turn.** At a fixed angle the rotation by $\pi/2$ about $(L/2, L/2)$ maps
$Q_j(c)$ to $Q_j$ at the rotated centre and preserves $\mu$, and the four images of the
quadrant $[L/2, L/2 + E_j]^2$ cover $D_j$. Your checker decides the quadrant (its root
box, `unified_linear_verify.cpp` lines 175 and 182), and so do both deciders here.

**Point masses.** The core is closed, so a point on its boundary counts, and the capture
jumps where a point enters or leaves; it is upper semicontinuous in $c$. A decision must
hold at every centre, not only where the capture is continuous: the vertex argument here
takes one-sided limits, and both branch and bounds count a point only when it lies in
the core for every centre of the box.

**What is computed.** Steps 1 to 5 and 7 are exact arithmetic on the files, recomputed
here. Step 6 at 201 angles is the whole computational content.

## Hypotheses Each Checker Assumes

| Hypothesis | Where it enters | Status here |
| --- | --- | --- |
| H1. The format: kinds and field orders, $m/8$ per image, a segment uniform in its parameter, a rectangle by area | every checker | read from the files’ shape; confirmed by the exact enclosure of every input row, and by your driver (`unified_linear_verify.py` lines 25 to 29) and reader (`unified_linear_verify.cpp` lines 160 to 166): a rectangle’s weight is its density, a point’s and a segment’s their mass |
| H2. Every mass positive, every primitive in $K$, none degenerate | steps 1, 7 | holds at all 1,773 |
| H3. $M < n$, threshold one | step 7 | holds: $n - M = 1/100000$ |
| H4. Reach and containment | steps 3, 4 | hold, values above |
| H5. Every domain nonempty, $E_j$ as recomputed | step 5 | holds; every input’s $E$ interval encloses the exact $E_j$ |
| H6. $D_4$-invariance | steps 2, 6, quarter turn | holds on the merged measure, all eight symmetries |
| H7. The capture at every centre of every quadrant, at all 201 angles | step 6 | decided by your runs, and here by this review’s own programs at all 201 |
| H8. The inputs enclose the exact measure and constants | your checker only | holds for all 201: one shared body, each interval at most one unit in the last place |
| H9. IEEE binary64 with round to nearest and `nextafter`; no fast-math, no contraction; asserts on | your checker; this review’s binary64 parts | your compile command gives `-O2 -std=c++17 -ffp-contract=off -fno-fast-math` and no `-DNDEBUG` (driver line 15); this review’s numpy code relies on separately rounded elementwise binary64 operations and on its stated error bounds |

## What This Review Ran

Every program is this lane’s own, kept with its outputs in the packet’s
[`programs/`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md).
They use CPython 3.14.7 (`fractions`, `hashlib`, `json`, `tarfile`) and numpy 2.5.2 on
one OpenBLAS thread, and import nothing from this repository or the source.
The checker and the controls plan were frozen at 06:03:49Z
([`frozen/checker-frozen-digests.txt`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/frozen/checker-frozen-digests.txt)),
after the selftest had passed on synthetic measures and before any program read the
certificate.

| Program | Decides | Result | CPU (s) |
| --- | --- | --- | ---: |
| `r144_premises.py` | premises, custody, records, comparisons | `PREMISES_HOLD`, 79 checks | 3.1 |
| `r144_inputs.py` | the 201 inputs encode the candidate | `INPUTS_ENCODE_CANDIDATE` | 3.9 |
| `r144_axis.py` | node 0, completely | `AXIS_DECIDED` | 0.5 |
| `r144_axis.py --factor 99/100` | the mutant’s node 0 | `AXIS_REFUSED`, exact witness | 0.5 |
| `r144_bnb.py`, nodes 1 to 200 | nodes 1 to 200, completely | FULL_TABLE_RESULT | FULL_TABLE_CPU |
| `r144_bnb.py --factor 99/100`, nodes 37, 180 | the mutant | `NODE_REFUTED` at both, exact witnesses | 0.2 |
| `r144_poses.py` | poses | `NO_COUNTEREXAMPLE_FOUND`, 1,608 fixed poses, 24 searched angles | 53 |
| `r144_lanes.py`, `r144_release_sums.py` | the lanes; the release’s sums | above; M-1 | 0.2 |
| `r144_selftest.py` | nothing (controls) | `SELFTEST_PASS`, synthetic and real | 8.8 |

**Changes after the freeze, disclosed.** `r144_premises.py` first printed
`PREMISES_FAIL` on one check: its 60-digit enclosure of $G_{11}$ was $2 \times 10^{-60}$
wide, and your bound on $G_{11}$ lies inside it. At 200 digits your bound exceeds
$G_{11}$ by $1.42 \times 10^{-90}$, as 90-digit roots rounded up would give, and the
check holds; nothing else changed. `r144_poses.py` gained `--draw`, which draws the six
seeded search nodes. Three programs were added after the plan: `r144_lanes.py`,
`r144_release_sums.py`, and `r144_run_all.sh`, which runs the complete decision. The
plan priced the complete run without running it, and the coordinator approved it at
06:13Z, after the five-node sample had measured its cost (one process, `nice -n 19`, a
stop at 2 CPU-hours).

**Premises.** The reader is strict: no float token, no duplicate key, every number
`p`, `p/q` or (for `L` and `B`) a plain decimal, exactly the keys `schema`, `n`, `L`,
`B`, `net`, `primitives` and `total_mass`. The claim’s $n$, $L$, $B$, net and mass are
the file’s and the manifest’s; the masses sum exactly to `total_mass`; every primitive
lies in $K$ with positive mass and positive extent; the 1,773 primitives are 1,773
distinct $D_4$ orbits (59 of four images, 1,714 of eight), every segment representative
horizontal, lengths $0.0869$ to $0.0998$; the merged measure is invariant under all
eight symmetries. The net facts of step 3 and 4 equal `manifest.json`’s, and every
$E_j$ equals the record’s `E` at its node.
The 18 pinned documents have the manifest’s sizes, Git blobs and SHA-256, and the 13
`code/` files and `requirements.txt` equal the retained copies on `main`; the asset equals `ASSET.json` and the
release API; the bundle is the 810 files the README names, the 202 copies of the checker
are `0249726a…`, the 202 copies of the candidate are one file, and the extraction equals
the tarball byte for byte. All 201 records are `ANGLE_VERIFIED` with empty frontiers,
nodes $= 2 \times$ leaves $- 1$, and manifests whose $t$, $E$, $L$, $B$, $\gamma = 1$,
mass and digests are the recomputed ones; `certificate.json` and `summary.json` agree
with them: 73,694,735 nodes, at most 2,218,683 (node 0) under the limit of 3,000,000,
and 51,876.8 seconds.

**The inputs.** The 201 inputs share one body byte for byte, and differ only in the
header. Every header encloses $L$, $B$, $E_j$, $c_j$, $s_j$ and $1$ exactly; every body
row encloses one exact image of a primitive, each image used once: 24 rectangles
(weight their density), 4,016 points and 10,144 segments (weight their mass, $m/8$),
5,072 segment rows listing their end points in the other order. Every interval is at most
one unit in the last place wide.

**Node 0, decided.** At angle 0 the capture is $F(X, Y) = \sum_k w_k f_k(X) g_k(Y)$,
with indicator and overlap factors; between consecutive breakpoints (each coordinate
$\pm b$ in the quadrant) every factor is affine, so $F$ is bilinear on every cell and its
least value on a closed cell, with the indicators’ one-sided limits from inside the cell,
is at a corner. With every coordinate a multiple of $10^{-12}$, the breakpoints are exact
integers: 119 in each axis, 14,161 corners, four one-sided values at each.
The corner values are binary64 matrix products of nonnegative factors, so the true value
is at least the computed one over $(1 + u)^4 (1 + \gamma_k)$.

|  | Value |
| --- | --- |
| Rigorous least over the quadrant | $1.0039577044075541$ |
| Exact least corner value | $8164705441014341474078111754486671/8132519333400001178340724809600000 = 1.0039577044080\ldots$ |
| Where | $X = Y = 7.76834931$, limits from below in both |
| Exact capture at a pose inside that cell (methods A and B equal) | $1.0039577874\ldots$ |
| The 99/100 mutant | refused: rigorous least $0.99391812736$, exact witness $0.99391820956$ |

So node 0 is decided by an implementation that shares nothing with yours, and its margin
is $3.96 \times 10^{-3}$, where your record’s least leaf bound there is
$1 + 8.7 \times 10^{-8}$.

**Nodes 1 to 200, decided.** `r144_bnb.py` halves boxes of centres across their longer
side, from a $32 \times 32$ grid over the quadrant, and discharges a box when a rigorous
lower bound on the measure of its trimmed core $T$ (the intersection of all cores
centred in the box) is at least one. In the core’s own frame $T$ is the rectangle
$[c x_1 + s y_1 - b, c x_0 + s y_0 + b] \times [-s x_0 + c y_1 - b, -s x_1 + c y_0 + b]$.
Image coordinates are computed exactly and rounded to nearest; $T$ is computed in
binary64 and shrunk by $10^{-13}$ on every side, more than the error of any compared
quantity (below $2 \times 10^{-14}$ for numbers below 16). A point counts only inside the
shrunk $T$; a segment counts the parameter interval Liang–Barsky finds against the
shrunk $T$, which lies inside the exact interval against $T$, since each computed end
errs by less than the shrink divided by the direction component; a rectangle counts its
full mass only when its four corners are inside, and otherwise its exact share against
the exact $T$, by rational clipping. Masses are rounded down and the sum divided by
$1 + 2 \times 10^{-12}$, which covers $k u$ for the at most FULL_MAXTERMS terms a box
held. A box not discharged is also evaluated at its centre, exactly if a binary64
estimate there falls below $1 - 10^{-9}$, and a capture below one would refute the node.

FULL_RUN_PARAGRAPH

The 99/100 mutant is refuted at nodes 37 and 180, at the first box whose centre
estimate fell below one: exact captures $0.99953403$ and $0.99910313$ at
$(5.74367, 6.40593)$ and $(5.76951, 6.08703)$.

**Poses and a seeded search.** At every node the four corners of the quadrant and four
seeded poses were evaluated exactly by both methods: 1,608 poses, no disagreement, the
least $1.0040775$ (node 199). A seeded search at 24 nodes, fixed before it ran (0, 1, 2,
25, 36, 37, 83, 108, 150, 155, 157, 163, 164, 180, 185, 196, 199, 200 and six drawn by a
generator seeded from the candidate’s SHA-256: 8, 71, 79, 86, 94, 183), took a
$120 \times 120$ binary64 grid over each quadrant, a compass search from the six best
points, and the exact capture at every end point. It found nothing below one and nothing
below your record’s `lower` at its node; the least exact capture found is $1.0017586$ at
node 196, at $(6.0988, 6.0746)$, and the median of the per-node least is $1.00265$.

**Controls on this review’s programs.** The controls plan was frozen with the checker,
and each control fails an always-accept or an always-refuse checker:

- on synthetic measures before the freeze: the two exact evaluators agree at 200 seeded
  poses at five nodes; a point lattice of spacing $B/5$ and mass $(1 + 10^{-4})/25$ is
  decided at node 0 with least exactly $10001/10000$, and its 99/100 mutant refused; a
  segment grid with a point orbit and a rectangle orbit is decided at node 37 with no
  seeded capture below one, and refuted at factor $3/10$ with an exact witness;
- on the real data: the reader refuses a float token, a duplicate key and an unknown
  key; a total mass of 122, a negative mass, a point outside $K$ and a degenerate
  segment each fail their named premise, as do a net ending at index 199 and a step of
  $1/430$; an input written from the candidate is accepted, and its four mutations
  (a coordinate interval moved past its exact value, a dropped row, a duplicated row, the
  wrong node’s $E$) are refused, as is a copy of node 37’s real input with one coordinate
  moved;
- the mutants of the two deciders, above.

## The Source’s Checker and What the Checkers Share

**What `unified_linear_verify.cpp` decides.** One input, one net angle: that every box
of centres in the normalized quadrant, mapped to $[L/2, L/2 + E]^2$ with outward
rounding (lines 175, 182, 124), has a rigorous lower bound at least $\gamma$ on the
capture (line 183). Its interval type rounds every operation to nearest and widens it by
one unit in the last place (lines 17 to 23), which encloses the exact result under any
rounding mode; it asserts round to nearest anyway (line 158).

- Points are counted only when they lie in the core for every centre of the box, by
  interval tests (lines 109 to 110): the trimmed core.
- A segment’s parameter interval is proposed in floating point against the trimmed
  core, inset, and both its ends then checked in interval arithmetic to lie in every core
  of the box; convexity puts the whole interval in the trimmed core (lines 86 to 106).
- A rectangle’s share is a rigorous interval area at the box’s centre, from a polygon
  built approximately and then proved convex and inside both sets (lines 31 to 74), less
  a first-order term: interval bounds on the area’s partial derivatives over the box,
  the lengths of the rectangle’s edges inside the moving core (lines 76 to 79, 139 to
  151). The area is Lipschitz in the centre, so the mean value inequality makes this
  rigorous.
- Node 0 has its own branch (lines 125 to 138), with the same treatment of points and
  segments and an overlap-and-derivative bound for rectangles.
- A box that reaches $2^{-40}$ of the quadrant without discharge, or a node budget spent,
  leaves the stack nonempty and the status `ANGLE_UNRESOLVED` (lines 180 to 191).

This reading found no unsound step.

**What it trusts and does not check.** That its input encloses the intended measure and
constants; that the measure is $D_4$-invariant, which the quarter turn needs; that $E$ is
the right domain; the budget $M < n\gamma$; the net premises; and the meaning of the
weight fields. Its driver writes the inputs and checks the budget and the net
(`unified_measure.py` lines 40 to 72); this review recomputed every one of these apart
from both. It also trusts the compiler, the C++ library’s `stod` on hexadecimal floats,
IEEE binary64, and the compile command that keeps assertions on.

**What the replays share.** The source’s replay (`replay_linear_bundle.py`, through
`replay_angle`) regenerates each input, compares it byte for byte, reruns the same
binary at the stored node count, and compares status, nodes, leaves, `lower` and
frontier: re-execution of the same implementation, as the README says. A complete replay
by this repository’s T-080 route runs the same program, so it would confirm the
certificate as reproduced with the producer’s code.

| Checker | Decides | Trusts |
| --- | --- | --- |
| Your `unified_linear_verify.cpp` (`0249726a…`), your runs | the quadrant at each of the 201 angles, one run each, records retained | its inputs and the premises above; the compiler; your machine; that the records are the runs’ |
| A replay by the T-080 route (the replay lane) | the same, rerun here | the same program; this host |
| This review’s programs | every exact premise; the inputs; node 0 by the vertex argument; nodes 1 to 200 by the branch and bound; 1,608 poses and a search | CPython 3.14.7’s `fractions` and integers; numpy’s binary64 under the stated bounds; its own code |

This review’s programs share no code with your checker or its driver: they were written
from the mathematics and the certificate’s documents and frozen before any of your code
was opened. Both branch and bounds bound points and segments by the same trimmed core,
the natural bound, and found nearly the same trees: at node 37, 53,278 discharged boxes
here against your 53,272 leaves. The rectangles are handled differently (exact clipping
against the trimmed core here, a centre value and a derivative bound in yours), and node
0 here is decided by a different argument. All share the mathematics (steps 1 to 7 and
the quarter turn) and the reading of the format, which this review checked against the
inputs row by row. Authorship overlaps at the system family: the source’s commit names
Claude Opus 5.5 as co-author, and this review is a Claude agent with its own prompt and
files.

## Findings

No finding is blocking or major.
Grades: blocking, major, minor, note.
Paths are the source’s, under
`problems/square-lower-bounds/certificates/mixed_n122_L1126/` at `a9f76c3`, unless they
name the record.

**M-1 — minor, author. The release’s `SHA256SUMS` does not list the asset.** The
current `SHA256SUMS` of `square-lower-bounds-v1` (465 entries, updated 2026-10-18T07:10:19Z,
SHA-256 `29acc0c8…05e4`, the API’s digest) lists the sibling assets, `mixed_n101_L1028`,
`mixed_n106_L10503` to `mixed_n108_L1062` and `mixed_n145_L1224` among them, but neither
this asset’s name nor its digest
([`out/release-sums.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/release-sums.json)).
Custody rests on `ASSET.json` in the pinned commit and on the release API, which agree.
`ASSET.json` line 25 also gives `"commit": null`.

**M-2 — minor, author. The README does not say where the capture is checked.**
`README.md` line 15 says “every closed core of side `B` at that angle has measure `>= 1`”,
and `manifest.json` line 16 “every admissible centre”, without saying which centres. A
core that pokes out of $K$ can capture less than one. The checker decides the cores
inside $K$, by the quadrant $[L/2, L/2 + E_j]^2$ and the quarter turn, and step 5 above
shows that suffices. Say so, and give $E_j = L/2 - (B/2)(\cos\theta_j + \sin\theta_j)$.

**N-1 — note. The certificate proves the strict bound.** No packing fits at side $L$
(`README.md` line 3), so $s(122) > L$; line 1 and the record state $\ge$, which is what
a lower-bound entry means. Nothing to change.

**N-2 — note. The `lower` fields are not margins.** The records’ least `lower` is
$1 + 4.07 \times 10^{-10}$ (node 180). A branch and bound stops splitting as soon as a
box’s bound reaches one, so its least leaf bound can sit just above one whatever the
true margin: this review’s own tree at node 180 ended at $1 + 6.0 \times 10^{-9}$.
The least captures found here are $1.0039577$ at node 0 (exact, over the whole domain)
and $1.0017586$ over the search.

**N-3 — note. The checker’s cost is linear in the measure.** Every box evaluates every
image (`unified_linear_verify.cpp` lines 109 to 111, 128 and 141): 14,184 per box over
73.7 million boxes. A spatial cull leaves about 250 per box; this review’s numpy branch
and bound decided nodes 1 to 200 in FULL_CPU_HOURS CPU-hours, against 14.4 hours of
checker time in your records.

**N-4 — note. The README compares with $\sqrt N$.** Line 8 says the bound improves on
$\sqrt N$ at 122 to 126. True, but the record’s comparisons are Green’s report (122 to
125), Nagamochi’s $1 + \sqrt{105}$ and Hosono’s closed form at 126, and Karakuş’s strip
bound, which is stronger than $\sqrt N$ at every one of these counts.

**N-5 — note. Assertions carry some input checks.** Nonnegative weights, the stream’s
state and nonzero divisors are `assert`s (`unified_linear_verify.cpp` lines 23, 158, 162
to 166). The shipped compile command keeps them; a build with `-DNDEBUG` would drop
them. Not a defect as shipped.

**N-6 — note. The pre-publication replay left no receipt.** `README.md` lines 52 to 55
describe a replay from the tarball on a fresh machine, in 7 h 41 min. The bundle’s
`certificate.json`, `summary.json` and `replay-progress.json` record the verifying run
and its in-run replay, but no file records the fresh-machine run’s start, machine or
output.

**R-1 — minor, record. T-144’s text on $n = 126$ predates T-180.** T-144’s `claim`
compares 563/50 with “Nagamochi’s 11.2469507659... at n = 126”, its significance
rationale says it “raises the reported and verified lower bounds at five counts”, and
its `notes` say the entry is pending adoption “while Green’s or Nagamochi’s reported
value and the Karakus strip bound hold them”. Since 14 October the reported lane at 126
is T-180’s $a(126) = 11.313323850997\ldots$, above 563/50 (`packing/frontier/n-126.md`),
as T-180’s own entry says. So T-144 would raise the reported lane at 122 to 125 and the
verified lane at 122 to 126. The comparisons themselves are exact and correct.

**R-2 — note, record. The pending-review clauses.** T-144’s `next_rung`,
`unfinished_confirmations` and `composition` say that a review that reads the
certificate is pending and that “no second implementation stands beside” the source’s
checker. The change that maps this review should rewrite them: the review is retained,
and its programs decided all 201 angles apart from the source’s code
([Rungs and Significance](#rungs-and-significance)).

## Questions for the Author

1. Would you add the asset to the release’s `SHA256SUMS`, and name the commit in
   `ASSET.json` (M-1)?
2. Could the README say that the capture is checked at every centre whose core lies in
   $K$, by the quadrant and the quarter turn (M-2)?
3. `completion-audit.json` says that “Green’s published proof has gaps for k>=4”.
   Which publication is meant? Friedman’s survey reports Green’s values from a private
   communication, and this record has not recovered a proof.
4. Did the fresh-machine replay keep its log or receipt (N-6)?
5. The least capture this review found is about $1.0018$ (node 196). Was that the margin
   your repair aimed at, and is the least capture over the net recorded anywhere?

## Rungs and Significance

**Now.** T-144 stands at `V0/C0`. With this review recorded as the `external_review` of
its reported entry (state `informally-verified`) and listed in the entry’s `reviews`
(kind `adversarial`, verdict `accepted`), it derives `V0/C1`, a read of a recorded claim,
as the change that maps this review records.

**This review’s complete decision.** Its programs decided all 201 angles of the net, the
whole of step 6, apart from the source’s code. The runbook counts a first-party
implementation as the replay when its soundness has been adversarially reviewed and its
independence recorded (stage 4, “The replay”). Registered in
[`verifiers.yaml`](../../../packing/frontier/verifiers.yaml) with that record, and once
a review of its soundness is recorded, the decision supports `V3/C3`: confirmed,
independently re-implemented (clean-room), by a Claude agent, a system family the
producer also used. Until then it sets no rung. The replay lane’s complete replay by the
T-080 route would support `V3/C3` as reproduced with the producer’s code; the two
together would stand beside each other, as the runbook records a second route.
`V4/C4` would further need a second adversarial review by a distinct reviewer and a human
oversight record.

**Significance: S3, as drafted.** If adopted, the certificate raises the verified lower
bound at five counts, by $0.2125$ at 122 down to $0.0245$ at 126, and the reported one at
four, by $0.0307$ over Green’s unproved report at 122 to 125. It turns an unproved report
into a certificate-backed bound there, narrowing the reported gap at 122 from $0.3063$ to
$0.2755$. It uses T-080’s certificate kind, net and checker at a new size, with no new
technique: a substantive case result, as T-080 is. It is not a reusable technique or
bound family (S4), and 122 to 126 are not central open cases (S5). The rationale’s
“five counts” for the reported lane should read four (R-1).

## Reproduction

The packet’s
[README](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md)
gives every command, what each printed and the digests of the two compressed receipts.
The programs need the source at `a9f76c3` and the asset at its digest, fetched as above.
The review’s compute, the complete decision included, was FULL_TOTAL_CPU CPU-hours, at
`nice -n 19` and one process at a time.

## Comparison With Earlier Reviews

COMPARISON_PLACEHOLDER

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
