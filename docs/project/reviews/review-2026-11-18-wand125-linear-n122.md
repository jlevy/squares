# wand125’s Linear Certificate for $s(122) \ge 563/50$: Mathematical Review

2026-11-18. Reviewer: Claude (Anthropic), `tbd-strong-max` tier at maximum reasoning,
lane r144-1118 (bead `think-rxs3`, under the import `think-nd7g`), and, after a
container restart stopped that lane at about 06:59Z, lane r144b-1118 at the same tier
and setting, which resumed from the pushed branch, finished the run and froze the
findings. Both were prompted separately from the replay lane and shared none of its
context beyond their briefs and the committed record.
Workflow:
[result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate),
“The review”. Scope: `mixed_n122_L1126`, wand125/square-packing at `a9f76c3`, with its
release asset `certificates__mixed_n122_L1126.tar.gz` at SHA-256 `6443eae0…5deb`, and
the register entry T-144 on `main`. On `main` the import packet
[`wand125-linear-n122-2026-10-10`](../../../packing/resources/web/wand125-linear-n122-2026-10-10/README.md)
holds the manifest but not the candidate or the certificate, so this lane fetched the
source at the pin and the asset at its digest itself.
The programs and receipts are in
[`wand125-linear-n122-review-2026-11-18`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md).
This review moves no bound and adopts nothing.

## Summary for the Author

**Decision: accept.** The argument from the certificate to the claim is correct and
complete, and every hypothesis it needs holds in exact arithmetic.
If 122 unit squares fitted in the closed square of side $563/50$, closed cores of side
$9977/10000$ at net angles, one inside each square, would be disjoint, each of measure
at least one, against a total mass of $122 - 1/100000$. So the certificate proves the
strict bound $s(122) > 563/50$, and the same holds at every $N \ge 122$, since $N$
squares would need mass at least $N$.

The computation the claim needs, a capture of at least one at every centre of every one
of the 201 net angles, was decided here **completely, by programs of this review’s
own**. They were written from the mathematics and the certificate’s documents, frozen
before any of them ran on the certificate and before your checker was opened, and they
share no code with it:

- node 0 by a vertex argument in exact integers: the infimum of the capture over the
  centre domain is exactly $1.0039577044080\ldots$;
- nodes 1 to 200 by a rigorous branch and bound of this review’s own, every one of them
  decided, in 71,418,450 boxes against your checker’s 71,476,052 nodes;
- every exact premise; that each of the 201 checker inputs encloses exactly the
  candidate’s 14,184 images; and the comparison with Green’s $G_{11}$, which your bound
  exceeds by more than $0.0307191$, as your README says (that comparison’s precision was
  raised after the freeze, as disclosed below).

Both deciders refuse two mutants with exact witnesses: every mass times 99/100, and the
heaviest segment orbit (mass $1.19$) removed.
The least capture found in a seeded search at 24 angles is $1.00176$ (angle 196); the
`lower` fields of your records, down to $1 + 4.1 \times 10^{-10}$, are where the branch
and bound stopped, not the margins.

Your checker, read as data after this review’s programs were frozen, decides what its
records say it decides, by sound interval arithmetic.
There is no blocking or major finding.
Two minor findings concern the bundle’s custody and wording: the release’s `SHA256SUMS`
does not list the asset (M-1), and the README’s statement of what was checked overstates
it and leaves the centre domain undefined (M-2). One minor finding is the record’s: at
$n = 126$ the reported lane is now T-180’s $a(126) = 11.3133\ldots$, above $563/50$, so
T-144 would raise the reported lane at four counts and the verified lane at five (R-1).

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
$11.2354552767$. The upper bounds run from $11.5355339059$ at $n = 122$ to
$11.7426406871$ at $n = 126$.

| $n$ | Reported lane on `main` | Verified lane on `main` | 563/50 raises |
| ---: | --- | --- | --- |
| 122 | Green, $11.22928\ldots$ | Karakuş, $11.04751\ldots$ (+0.21249) | both |
| 123 | Green, $11.22928\ldots$ | Karakuş, $11.09481\ldots$ (+0.16519) | both |
| 124 | Green, $11.22928\ldots$ | Karakuş, $11.14190\ldots$ (+0.11810) | both |
| 125 | Green, $11.22928\ldots$ | Karakuş, $11.18878\ldots$ (+0.07122) | both |
| 126 | T-180, $11.31332\ldots$ | Karakuş, $11.23546\ldots$ (+0.02454) | verified only |
| 127 | T-180, $11.37167\ldots$ | Karakuş, $11.28193\ldots$ | neither |

The comparisons are exact.
The gain over $G_{11}$ is $0.0307191244486\ldots$, by 200-digit enclosures of $\sqrt 2$
and $\sqrt{22}$; the gain over $1 + \sqrt{105}$ is $0.0130492340404\ldots$, and its sign
is decided by squaring
([`out/premises.json.gz`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/premises.json.gz));
and $(563/50 - 1/2)^2 > N - 11 + 1/4$ for $N \le 126$ but not at 127, by squaring
([`out/lanes.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/lanes.json),
which reads the lanes from the case records).

## What Was Read

**Before the checker froze (06:03:40Z, commit `ee66533d0f`), as data.** The lane’s
briefs and the bead `think-rxs3`; `result-import.md` stage 4; the house review of 11
November (`review-2026-11-11-wand125-fine-net-n28-n30.md`) as the format model, and PRs
#1013 and #1014’s structure; on `main`, the import packet’s README and
`source-manifest.json`; grep lines naming Green’s, Nagamochi’s and the closed form’s
values in `packing/frontier/`. From the source at `a9f76c3`: the commit, the tree, the
certificate’s `README.md`, `manifest.json`, `completion-audit.json`, `ASSET.json` and
`requirements.txt`, `mixed_n101_L1028/README.md`, and the first 250 lines of
`docs/lower-bounds.md`. From the asset and its bundle, to write the readers: the
listings, the shape of `candidate.json` and `input.txt`, the sum of the masses (which
showed that a primitive’s mass is its orbit’s), and a table of the 201 records’ status,
nodes, `lower`, seconds, $t$ and $E$. The `code/` files were hashed and not opened.

**After the checker froze, before the findings froze.** The source’s
`unified_linear_verify.cpp` in full, its driver `unified_linear_verify.py`,
`replay_linear_bundle.py`, the first 120 lines of `unified_measure.py`, `replay_angle`
in `unified_linear_full_verify.py` and `interval` in `mixed_rotated_verify.py`, all as
data; the register entries T-144 and T-180; the front matter of `n-122.md` to
`n-127.md`; the release’s current `SHA256SUMS`.

**Lane r144b-1118, on resuming, before the findings froze.** Its two briefs and the bead
`think-rxs3`; this branch, its draft and its receipts, and the killed run’s partial
receipts; the source’s `unified_linear_verify.cpp` in full, and the lines of
`unified_linear_verify.py`, `unified_measure.py`, `README.md`, `manifest.json`,
`ASSET.json` and `completion-audit.json` that this review cites, to check each citation;
T-144’s register entry and `E-wand125-linear-n122-1126-report` on `main`; the front
matter of `n-122.md`, `n-126.md` and `n-127.md`; as format models, the file lists of PRs
#1013 and #1014, the freeze statements and closing note of the review of #1009, and the
headings of the review of 11 November; and, for the house conventions, the retained-data
rule, the flowmark and lint exclusions, `epistemics.md`’s rung tables, and the runbook’s
stage 4 and its pull-request label rule.

**A departure from the brief.** The coordinator’s brief allowed the source’s checker to
be read as data only after the findings froze.
Lane r144-1118 read it after this review’s checker froze and before its findings froze,
to give the checker’s trust boundary, which the bead asks for, and lane r144b-1118 read
it again before the freeze to check the line numbers cited here.
What rests on that reading is the section on the source’s checker, the citations in H1
and H9, and N-3 and N-5. No decision about the capture rests on it: every program that
decides was frozen before the checker was opened, and the two changes made to frozen
programs afterwards (below) touch the comparison with $G_{11}$ and the draw of six
search nodes.

**Not read.** The other files of `code/` (hashed only); the replay lane’s branch,
receipts and notes; the import packet’s `receipts/` and `reported-n122.json`; this
repository’s `devtools.audit_wand125_linear` and `devtools.fine_net_followup`, which
this review neither read nor ran; and the earlier reviews of this certificate and its
siblings, read only after the findings were written
([Comparison With Earlier Reviews](#comparison-with-earlier-reviews)).

**Disclosed.** For both lanes, `tbd show think-rxs3` printed the parent bead
`think-nd7g`’s notes of 10 to 12 October, which report that the intake’s readers held
the premises, that angles 37 and 108 replayed with the source’s checker, and that the
route’s control refused at angle 37 in a preparation smoke run; for lane r144b-1118 the
display cut the notes off after 12 October, and it read no later line.
The import packet’s README summarizes the same.
This review decided nothing from either.

## The Argument, Re-Derived

Write $L = 563/50$, $B = 9977/10000$, $b = B/2$, $D = 83/40000$, $t_j = jD$ for
$j = 0, \ldots, 200$, $\theta_j = 2\arctan t_j$, $c_j = (1 - t_j^2)/(1 + t_j^2)$,
$s_j = 2t_j/(1 + t_j^2)$, and $Q_j(c)$ for the closed square of side $B$, centre $c$ and
sides along $(c_j, s_j)$ and $(-s_j, c_j)$.

1. **The measure.** Each primitive of mass $m$ puts $m/8$ on each of its eight images
   under the symmetry group $D_4$ of $K = [0, L]^2$: a point mass, a mass spread
   uniformly by length on a segment, or uniformly by area on a rectangle.
   So $\mu \ge 0$ is $D_4$-invariant, supported in $K$, and
   $\mu(K) = M = 122 - 1/100000$. A segment’s share in a core is its mass times the
   fraction of its parameter inside, so no square root enters.
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
   the core lies in $K$ and its centre in the set $D_j$ of centres $c$ with
   $Q_j(c) \subseteq K$, which is $[L/2 - E_j, L/2 + E_j]^2$ with
   $E_j = L/2 - b(c_j + s_j)$, since the core reaches $b(c_j + s_j)$ from its centre
   along each axis. $E_j$ runs from $4.92452$ (node 200) to $5.13115$ (node 0). The
   domain is the core’s own, so no bin-end estimate of the unit square’s reach is
   needed.
6. **Capture.** The certificate asserts $\mu(Q_j(c)) \ge 1$ for every $j$ and every
   $c \in D_j$. Then $g^{-1}Q_j(c)$, $c$ the centre of $gS$, is a closed square in the
   open interior of $S$ with the same measure, by invariance.
7. **Count.** The cores of distinct squares lie in disjoint open interiors, so
   $122 \le \sum_S \mu(\mathrm{core}(S)) \le \mu(K) = 122 - 1/100000$, a contradiction.
   A packing in a smaller square is one in $K$, and the infimum defining $s(122)$ is
   attained (the packings in a closed square form a compact set), so $s(122) > L$; a
   packing of $N \ge 122$ squares contains one of 122, so $s(N) > L$.

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

Every program is the review’s own, lane r144-1118’s apart from lane r144b-1118’s
`r144b_compare_killed.py`, kept with its outputs in the packet’s
[`programs/`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md).
They use CPython 3.14.7 (`fractions`, `hashlib`, `json`, `tarfile`), numpy 2.5.2 on one
OpenBLAS thread and, in `r144_lanes.py`, PyYAML, and import nothing from this repository
or the source. The checker and the controls plan were frozen at 06:03:40Z (commit
`ee66533d0f`)
([`frozen/checker-frozen-digests.txt`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/frozen/checker-frozen-digests.txt)),
after the selftest had passed on synthetic measures and before any program read the
certificate.

| Program | Decides | Result | CPU (s) |
| --- | --- | --- | ---: |
| `r144_premises.py` | premises, custody, records, comparisons | `PREMISES_HOLD`, 79 checks | 3.1 |
| `r144_inputs.py` | the 201 inputs encode the candidate | `INPUTS_ENCODE_CANDIDATE` | 3.9 |
| `r144_axis.py` | node 0, completely | `AXIS_DECIDED` | 0.5 |
| `r144_axis.py --factor 99/100` | the mutant’s node 0 | `AXIS_REFUSED`, exact witness | 0.5 |
| `r144_bnb.py`, nodes 1 to 200, through `r144_run_all.sh` | nodes 1 to 200, completely | `NODE_DECIDED` at all 200 | 2,534, and about 600 in the run the restart killed |
| `r144_bnb.py --factor 99/100`, nodes 37, 180 | the mutant | `NODE_REFUTED` at both, exact witnesses | 0.2 |
| `r144_mutate.py`, then `r144_axis.py` and `r144_bnb.py` (nodes 37, 180) on its output | the second mutant | `AXIS_REFUSED`; `NODE_REFUTED` at both; exact witnesses | 30 |
| `r144_summarize.py`, `r144b_compare_killed.py` | nothing (receipts) | `ALL_201_NODES_DECIDED`; `KILLED_RUN_REPRODUCED` | 0.1 |
| `r144_poses.py` | poses | `NO_COUNTEREXAMPLE_FOUND`, 1,608 fixed poses, 24 searched angles | 53 |
| `r144_lanes.py`, `r144_release_sums.py` | the lanes; the release’s sums | above; M-1 | 0.2 |
| `r144_selftest.py` | nothing (controls) | `SELFTEST_PASS`, synthetic and real | 8.8 |

**Changes after the freeze, disclosed.** `r144_premises.py` first printed
`PREMISES_FAIL` on one check: its 60-digit enclosure of $G_{11}$ was $2 \times 10^{-60}$
wide, and your bound on $G_{11}$ lies inside it.
At 200 digits your bound exceeds $G_{11}$ by $1.42 \times 10^{-90}$, as 90-digit roots
rounded up would give, and the check holds; nothing else changed.
`r144_poses.py` gained `--draw`, which draws the six seeded search nodes.
Six programs were added after the plan, none of which decides a capture:
`r144_run_all.sh`, which runs the complete decision with the frozen `r144_bnb.py`;
`r144_summarize.py`, which gathers its receipts; `r144_mutate.py`, which writes the
second mutated certificate for the frozen deciders; `r144_lanes.py`;
`r144_release_sums.py`; and, by lane r144b-1118, `r144b_compare_killed.py`, which
compares the killed run’s printed lines with the rerun’s. The plan priced the complete
run without running it, and the coordinator approved it at 06:13Z, after the five-node
sample had measured its cost (one process, `nice -n 19`, a stop at 2 CPU-hours).

**The restart, disclosed.** A container restart at about 06:59Z killed the complete run
in its last range, 176 to 200, after it had printed node 193. That range had written no
`.done` file and its timer no time, and the driver runs such a range again from scratch,
so on the coordinator’s word lane r144b-1118 ran it again with the same driver, from
07:05:32Z to 07:29:15Z (one process, `nice -n 19`). The 18 nodes the killed run had
finished came out the same in verdict, boxes, least margin and witness
([`out/killed-range-comparison.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/killed-range-comparison.json),
from `out/bnb-all/killed-range-176-200.stdout.txt`), as a deterministic program’s
should. The killed run’s CPU, 569 seconds over those 18 nodes plus the part of node 194
it ran, about 600 in all by its per-node times (its timer died with it), is counted in
the totals.

**Premises.** The reader is strict: no float token, no duplicate key, every number `p`,
`p/q` or (for `L` and `B`) a plain decimal, exactly the keys `schema`, `n`, `L`, `B`,
`net`, `primitives` and `total_mass`. The claim’s $n$, $L$, $B$, net and mass are the
file’s and the manifest’s; the masses sum exactly to `total_mass`; every primitive lies
in $K$ with positive mass and positive extent; the 1,773 primitives are 1,773 distinct
$D_4$ orbits (59 of four images, 1,714 of eight), every segment representative
horizontal, lengths $0.0869$ to $0.0998$; the merged measure is invariant under all
eight symmetries. The net facts of step 3 and 4 equal `manifest.json`’s, and every $E_j$
equals the record’s `E` at its node.
The 18 pinned documents have the manifest’s sizes, Git blobs and SHA-256, and the 13
`code/` files and `requirements.txt` equal the retained copies on `main`; the asset
equals `ASSET.json` and the release API; the bundle is the 810 files the README names,
the 202 copies of the checker are `0249726a…`, the 202 copies of the candidate are one
file, and the extraction equals the tarball byte for byte.
All 201 records are `ANGLE_VERIFIED` with empty frontiers, nodes $= 2 \times$ leaves
$- 1$, and manifests whose $t$, $E$, $L$, $B$, $\gamma = 1$, mass and digests are the
recomputed ones; `certificate.json` and `summary.json` agree with them: 73,694,735
nodes, at most 2,218,683 (node 0) under the limit of 3,000,000, and 51,876.8 seconds.

**The inputs.** The 201 inputs share one body byte for byte, and differ only in the
header. Every header encloses $L$, $B$, $E_j$, $c_j$, $s_j$ and $1$ exactly; every body
row encloses one exact image of a primitive, each image used once: 24 rectangles (weight
their density), 4,016 points and 10,144 segments (weight their mass, $m/8$), 5,072
segment rows listing their end points in the other order.
Every interval is at most one unit in the last place wide.

**Node 0, decided.** At angle 0 the capture is $F(X, Y) = \sum_k w_k f_k(X) g_k(Y)$,
with indicator and overlap factors; between consecutive breakpoints (each coordinate
$\pm b$ in the quadrant) every factor is affine, so $F$ is bilinear on every cell and
its least value on a closed cell, with the indicators’ one-sided limits from inside the
cell, is at a corner.
With every coordinate a multiple of $10^{-12}$, the breakpoints are exact integers: 119
in each axis, 14,161 corners, four one-sided values at each.
The corner values are binary64 matrix products of nonnegative factors, so the true value
is at least the computed one over $(1 + u)^4 (1 + \gamma_k)$. The 16 least corners were
evaluated again in exact rationals.
The next-least value, $1.0039992\ldots$, lies $4.2 \times 10^{-5}$ above the least, far
outside that error bound (about $5 \times 10^{-13}$ at the 4,432 terms of a block), so
the least exact corner value below is the infimum itself.

|  | Value |
| --- | --- |
| Rigorous least over the quadrant | $1.0039577044075541$ |
| Exact least corner value | $8164705441014341474078111754486671/8132519333400001178340724809600000 = 1.0039577044080\ldots$ |
| Where | $X = Y = 7.76834931$, limits from below in both |
| Exact capture at a pose inside that cell (methods A and B equal) | $1.0039577874\ldots$ |
| The 99/100 mutant | refused: rigorous least $0.99391812736$, exact witness $0.99391820956$ |
| The second mutant (the heaviest segment orbit removed) | refused: rigorous least $0.85744566944$, exact witness $0.85744567027$ |

So node 0 is decided by an implementation that shares nothing with yours, and its margin
is $3.96 \times 10^{-3}$, where your record’s least leaf bound there is
$1 + 8.7 \times 10^{-8}$.

**Nodes 1 to 200, decided.** `r144_bnb.py` halves boxes of centres across their longer
side, from a $32 \times 32$ grid over the quadrant, and discharges a box when a rigorous
lower bound on the measure of its trimmed core $T$ (the intersection of all cores
centred in the box) is at least one.
In the core’s own frame $T$ is the rectangle
$[c x_1 + s y_1 - b, c x_0 + s y_0 + b] \times [-s x_0 + c y_1 - b, -s x_1 + c y_0 + b]$.
Image coordinates are computed exactly and rounded to nearest; $T$ is computed in
binary64 and shrunk by $10^{-13}$ on every side, more than the error of any compared
quantity (below $2 \times 10^{-14}$ for numbers below 16). A point counts only inside
the shrunk $T$; a segment counts the parameter interval Liang–Barsky finds against the
shrunk $T$, which lies inside the exact interval against $T$, since each computed end
errs by less than the shrink divided by the direction component; a rectangle counts its
full mass only when its four corners are inside, and otherwise its exact share against
the exact $T$, by rational clipping.
Masses are rounded down and the sum divided by $1 + 2 \times 10^{-12}$, which covers
$k u$ for the at most 264 terms a box held.
A box not discharged is also evaluated at its centre, exactly if a binary64 estimate
there falls below $1 - 10^{-9}$, and a capture below one would refute the node.

All 200 nodes were decided, each `NODE_DECIDED`: `out/bnb-all/` holds the eight ranges,
and
[`out/complete-decision.json.gz`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/complete-decision.json.gz)
gathers them with node 0 (`ALL_201_NODES_DECIDED`). The trees hold 71,418,450 boxes,
35,811,625 of them discharged, against your checker’s 71,476,052 nodes over the same
angles: 0.973 to 1.034 times your record’s count at each node, median 0.996. They go at
most 22 halvings below a cell of the starting grid, clip 3,423,274 rectangle shares
exactly, and never have more than 264 images contributing to one box.
The least discharged margin is $2.8 \times 10^{-10}$, at node 113. At node 37 the tree
here discharged 53,278 boxes against your 53,272 leaves.
The run took 2,534 CPU-seconds by the driver’s timer, 2,457 of them inside the nodes,
one process at `nice -n 19`.

The 99/100 mutant is refuted at nodes 37 and 180, at the first box whose centre estimate
fell below $1 - 10^{-9}$: exact captures $0.99953403$ and $0.99910313$ at
$(5.74367, 6.40593)$ and $(5.76951, 6.08703)$. The second mutant removes the heaviest
segment orbit, primitive 627, a horizontal segment at height $1.9952$ of mass $1.1914$,
or $0.1489$ per image
([`out/mutant-segment.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/mutant-segment.json)).
The branch and bound refutes it at nodes 37 and 180, with exact captures $0.99494280$
and $0.97258041$ at $(8.78314, 10.36466)$ and $(8.82438, 10.05595)$
([`out/bnb-mutant-segment.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/bnb-mutant-segment.json)),
and the vertex argument refuses its node 0 (table above).

**Poses and a seeded search.** At every node the four corners of the quadrant and four
seeded poses were evaluated exactly by both methods: 1,608 poses, no disagreement, the
least $1.0040775$ (node 199). A seeded search at 24 nodes, fixed before it ran (0, 1, 2,
25, 36, 37, 83, 108, 150, 155, 157, 163, 164, 180, 185, 196, 199, 200 and six drawn by a
generator seeded from the candidate’s SHA-256: 8, 71, 79, 86, 94, 183), took a
$120 \times 120$ binary64 grid over each quadrant, a compass search from the six best
points, and the exact capture at every end point.
It found nothing below one and nothing below your record’s `lower` at its node; the
least exact capture found is $1.0017586$ at node 196, at $(6.0988, 6.0746)$, and the
median of the per-node least is $1.00265$.

**The full replay’s price.** This review did not run your checker, so it prices a
complete replay from your records and the record.
The 201 records sum to 51,876.8 checker-seconds, 14.4 CPU-hours on your machine.
The import packet’s two-angle sample ran your checker on this host at 0.776 of the
recorded times, which prices a complete replay at about 11.2 CPU-hours, plus about 170
CPU-seconds for the route’s control at angle 37; your own replay of 7 h 41 min at three
workers bounds it near 23 CPU-hours.
That replay is the replay lane’s. This review’s complete decision cost 0.70 CPU-hours on
one core (2,534 CPU-seconds; the run the restart killed spent about 600 more), because
each of its boxes evaluates only the images within reach of its cell of the
$32 \times 32$ starting grid, where your checker evaluates all 14,184 at every box
(N-3).

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
  $1/430$; an input written from the candidate is accepted, and its four mutations (a
  coordinate interval moved past its exact value, a dropped row, a duplicated row, the
  wrong node’s $E$) are refused, as is a copy of node 37’s real input with one
  coordinate moved;
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
- A segment’s parameter interval is proposed in floating point against the trimmed core,
  inset, and both its ends then checked in interval arithmetic to lie in every core of
  the box; convexity puts the whole interval in the trimmed core (lines 86 to 106).
- A rectangle’s share is a rigorous interval area at the box’s centre, from a polygon
  built approximately and then proved convex and inside both sets (lines 31 to 74), less
  a first-order term: interval bounds on the area’s partial derivatives over the box,
  the lengths of the rectangle’s edges inside the moving core (lines 76 to 79, 139 to
  151). The area is Lipschitz in the centre, so the mean value inequality makes this
  rigorous.
- Node 0 has its own branch (lines 125 to 138), with the same treatment of points and
  segments and an overlap-and-derivative bound for rectangles.
- A box that reaches $2^{-40}$ of the quadrant without discharge, or a node budget
  spent, leaves the stack nonempty and the status `ANGLE_UNRESOLVED` (lines 180 to 191).

This reading found no unsound step.

**What it trusts and does not check.** That its input encloses the intended measure and
constants; that the measure is $D_4$-invariant, which the quarter turn needs; that $E$
is the right domain; the budget $M < n\gamma$; the net premises; and the meaning of the
weight fields. Its driver writes the inputs and checks the budget and the net
(`unified_linear_verify.py` lines 18 to 35, calling `validate` and `net_check` in
`unified_measure.py` lines 40 to 72); this review recomputed every one of these apart
from both. It also trusts the compiler, the C++ library’s `stod` on hexadecimal floats,
IEEE binary64, and the compile command that keeps assertions on.

**What the replays share.** The source’s replay (`replay_linear_bundle.py`, through
`replay_angle`) regenerates each input, compares it byte for byte, reruns the same
binary at the stored node count, and compares status, nodes, leaves, `lower` and
frontier: re-execution of the same implementation, as the README says.
A complete replay by this repository’s T-080 route runs the same program, so it would
confirm the certificate as reproduced with the producer’s code.

| Checker | Decides | Trusts |
| --- | --- | --- |
| Your `unified_linear_verify.cpp` (`0249726a…`), your runs | the quadrant at each of the 201 angles, one run each, records retained | its inputs and the premises above; the compiler; your machine; that the records are the runs’ |
| A replay by the T-080 route (the replay lane) | the same, rerun here | the same program; this host |
| This review’s programs | every exact premise; the inputs; node 0 by the vertex argument; nodes 1 to 200 by the branch and bound; 1,608 poses and a search | CPython 3.14.7’s `fractions` and integers; numpy’s and OpenBLAS’s binary64 under the stated bounds, which hold in any summation order; its own code |

This review’s programs share no code with your checker or its driver: they were written
from the mathematics and the certificate’s documents and frozen before any of your code
was opened. Both branch and bounds bound points and segments by the same trimmed core,
the natural bound, and found nearly the same trees: at node 37, 53,278 discharged boxes
here against your 53,272 leaves, and over nodes 1 to 200, 0.973 to 1.034 times your node
counts. The rectangles are handled differently (exact clipping against the trimmed core
here, a centre value and a derivative bound in yours), and node 0 here is decided by a
different argument.
All share the mathematics (steps 1 to 7 and the quarter turn) and the
reading of the format, which this review checked against the inputs row by row.
Authorship overlaps at the system family: the source’s commit names Claude as co-author,
and this review is a Claude agent with its own prompt and files.

## Findings

No finding is blocking or major.
Grades: blocking, major, minor, note.
Paths are the source’s, under
`problems/square-lower-bounds/certificates/mixed_n122_L1126/` at `a9f76c3`, unless they
name the record.

**M-1 — minor, author.
The release’s `SHA256SUMS` does not list the asset.** The current `SHA256SUMS` of
`square-lower-bounds-v1` (465 entries, updated 2026-10-18T07:10:19Z, SHA-256
`29acc0c8…05e4`, the API’s digest) lists the sibling assets, `mixed_n101_L1028`,
`mixed_n106_L10503` to `mixed_n108_L1062` and `mixed_n145_L1224` among them, but neither
this asset’s name nor its digest
([`out/release-sums.json`](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/out/release-sums.json)).
Custody rests on `ASSET.json` in the pinned commit and on the release API, which agree.
`ASSET.json` line 25 also gives `"commit": null`.

**M-2 — minor, author.
The README does not define where the capture is checked.** `README.md` line 15 says
“every closed core of side `B` at that angle has measure `>= 1`”, which a core that
pokes out of $K$ need not satisfy; line 16 says the verifier proves the bound “over
every centre domain” without saying what the domain is, and `manifest.json` line 16 says
“every admissible centre”.
The checker decides the cores inside $K$, by the quadrant $[L/2, L/2 + E_j]^2$ and the
quarter turn, and step 5 above shows that suffices.
Say so in line 15, and give $E_j = L/2 - (B/2)(\cos\theta_j + \sin\theta_j)$.

**N-1 — note. The certificate proves the strict bound.** No packing fits at side $L$
(`README.md` line 3), so $s(122) > L$; line 1 and the record state $\ge$, which is what
a lower-bound entry means.
Nothing to change.

**N-2 — note. The `lower` fields are not margins.** The records’ least `lower` is
$1 + 4.07 \times 10^{-10}$ (node 180). A branch and bound stops splitting as soon as a
box’s bound reaches one, so its least leaf bound can sit just above one whatever the
true margin: this review’s own tree at node 180 ended at $1 + 6.0 \times 10^{-9}$, and
its least over nodes 1 to 200, at node 113, at $1 + 2.8 \times 10^{-10}$. The least
captures found here are $1.0039577$ at node 0 (exact, over the whole domain) and
$1.0017586$ over the search.

**N-3 — note. The checker’s cost is linear in the measure.** Every box evaluates every
image (`unified_linear_verify.cpp` lines 109 to 111, 128 and 141): 14,184 per box over
73.7 million boxes. A core of side about one meets only the images within its reach (at
most 264 contributed to any box here), so a spatial cull pays: this review’s numpy
branch and bound, which culls by its starting grid’s cells, decided nodes 1 to 200 in
0.70 CPU-hours, against 14.4 hours of checker time in your records.

**N-4 — note. The README compares with $\sqrt N$.** Line 8 says the bound improves on
$\sqrt N$ at 122 to 126. True, but the record’s comparisons are Green’s report (122 to
125), Nagamochi’s $1 + \sqrt{105}$ and Hosono’s closed form at 126, and Karakuş’s strip
bound, which is stronger than $\sqrt N$ at every one of these counts.

**N-5 — note. Assertions carry some input checks.** Nonnegative weights, the stream’s
state and nonzero divisors are `assert`s (`unified_linear_verify.cpp` lines 23, 158, 162
to 166). The shipped compile command keeps them; a build with `-DNDEBUG` would drop
them. Not a defect as shipped.

**N-6 — note. The pre-publication replay left no receipt.** `README.md` lines 52 to 55
describe a replay from the tarball on a fresh machine, in 7 h 41 min.
The bundle’s `certificate.json`, `summary.json` and `replay-progress.json` record the
verifying run and its in-run replay, but no file records the fresh-machine run’s start,
machine or output.

**R-1 — minor, record.
T-144’s text on $n = 126$ predates T-180.** T-144’s `claim` compares 563/50 with
Nagamochi’s $1 + \sqrt{105} = 11.2469507659\ldots$ at $n = 126$, its significance
rationale says it “raises the reported and verified lower bounds at five counts”, and
its `notes` say the entry is pending adoption “while Green’s or Nagamochi’s reported
value and the Karakus strip bound hold them”; the limitations of
`E-wand125-linear-n122-1126-report` call the value “the strongest report at those
counts”, 123 to 126. Since 14 October the reported lane at 126 is T-180’s
$a(126) = 11.313323850997\ldots$, above 563/50 (`packing/frontier/n-126.md`), as T-180’s
own entry says. So T-144 would raise the reported lane at $n = 122$ to $125$, and the
verified lane at $n = 122$ to $126$. The comparisons themselves are exact and correct.

**R-2 — note, record.
The pending-review clauses.** T-144’s `next_rung`, `unfinished_confirmations` and
`composition` say that a review that reads the certificate is pending and that “no
second implementation stands beside” the source’s checker.
The change that maps this review should rewrite them: the review is retained, and its
programs decided all 201 angles apart from the source’s code
([Rungs and Significance](#rungs-and-significance)).

## Questions for the Author

1. Would you add the asset to the release’s `SHA256SUMS`, and name the commit in
   `ASSET.json` (M-1)?
2. Could the README say that the capture is checked at every centre whose core lies in
   $K$, by the quadrant and the quarter turn (M-2)?
3. `completion-audit.json` says that “Green’s published proof has gaps for k>=4”. Which
   publication is meant?
   Friedman’s survey reports Green’s values from a private communication, and this
   record has not recovered a proof.
4. Did the fresh-machine replay keep its log or receipt (N-6)?
5. The least capture this review found is about $1.0018$ (node 196). Was that the margin
   your repair aimed at, and is the least capture over the net recorded anywhere?

## Rungs and Significance

**Now.** T-144 stands at `V0/C0`. With this review recorded as the `external_review` of
its reported entry (state `informally-verified`) and listed in the entry’s `reviews`
(kind `adversarial`, verdict `accepted`), it derives `V0/C1`, a read of a recorded
claim, as the change that maps this review records.

**This review’s complete decision.** Its programs decided all 201 angles of the net, the
whole of step 6, apart from the source’s code.
The runbook counts a first-party implementation as the replay when its soundness has
been adversarially reviewed and its independence recorded, and asks that two mutated
certificates be refused by every checker that accepted the original, with a test that
holds them (stage 4, “The replay”). Here both deciders refused two, each with exact
witnesses: every mass times 99/100, and the candidate without its heaviest segment
orbit. What the decision still needs is the review of its soundness, its registration in
[`verifiers.yaml`](../../../packing/frontier/verifiers.yaml) with its independence
record, and the test; with those it supports `V3/C3`: confirmed, independently
re-implemented (clean-room), by a Claude agent, a system family the producer also used.
Until then it sets no rung.
The replay lane’s complete replay by the T-080 route would support `V3/C3` as reproduced
with the producer’s code; the two together would stand beside each other, as the runbook
records a second route.
`V4/C4` would further need a second adversarial review by a distinct reviewer and a
human oversight record.

**Significance: S3, as drafted.** If adopted, the certificate raises the verified lower
bound at five counts, by $0.2125$ at 122 down to $0.0245$ at 126, and the reported one
at four, by $0.0307$ over Green’s unproved report at 122 to 125. It turns an unproved
report into a certificate-backed bound there, narrowing the reported gap at 122 from
$0.3063$ to $0.2755$. It uses T-080’s certificate kind, net and checker at a new size,
with no new technique: a substantive case result, as T-080 is.
It is not a reusable technique or bound family (S4), and 122 to 126 are not central open
cases (S5). The rationale’s “five counts” for the reported lane should read four (R-1).

## Reproduction

The packet’s
[README](../../../packing/resources/web/wand125-linear-n122-review-2026-11-18/README.md)
gives every command, what each printed and the digests of the three compressed receipts.
The programs need the source at `a9f76c3` and the asset at its digest, fetched as above.
The review’s compute was about 0.93 CPU-hours, at `nice -n 19` and one process at a
time: about 195 CPU-seconds for the plan’s controls and samples, 2,534 for the complete
decision, about 600 lost to the restart, and 30 for the second mutant.

## Comparison With Earlier Reviews

This section is written after the findings freeze, from earlier reviews read only then,
as the runbook asks; the frozen copy ends here.

Lane r144b-1118 wrote it after the findings froze at 07:35:35Z (commit `80405c86fe`),
from four reviews read only then: the
[2 October review](review-2026-10-02-wand125-linear-certificates-and-n76.md) of T-080,
which read the same checker for `mixed_n101_L1028` and `mixed_n83_L935`; the
[14 October review](review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md) of
T-179 and its siblings, which re-derived the argument for the sibling certificate
`mixed_n145_L1224`; and the two final reviews of 11 October,
[of the lower bounds](review-2026-10-11-final-lower-bounds.md) and
[of the asymptotics and the grading](review-2026-10-11-final-asymptotic-and-grading.md),
which read T-144’s record and premises only.
Nothing above this section changed after the freeze.

**Where they agree.**

- *The argument.* The 2 October review derived the chain this review re-derived: the
  orbit expansion, the containment identities, the quarter turn and the reflection,
  which need only the $D_4$ invariance, the count, and the transfer by mass.
  The 14 October review repeated it at $n = 145$. All three find it sound.
- *The checker.* The 2 October review read `0249726a…` line by line, as this review did
  without it. Both find the same things at the same lines: a point charged only when it
  lies in the closed core for every centre of the box; a segment proposed in floating
  point, proved at both ends and closed by convexity; the axis branch’s overlap less the
  `axis_slice` derivative bound; and the oblique rectangle kernel.
- *Termination margins.* The 14 October review calls the stored lower bounds “the branch
  and bound’s termination margin, not the measure’s slack”, which is N-2 here; the 2
  October review’s LC-3 makes the matching point about refusals.
- *The README’s comparison with $\sqrt N$* is F-8 of 14 October and N-4 here, both
  notes. *The fresh-machine replay without a receipt* is in §3 and question 3 of 14
  October, and in N-6 and question 4 here.
- *The README’s statement of the fold.* LC-2 of 2 October says the READMEs state the
  conclusion (“every closed core …”, “every admissible centre”) and not the quadrant and
  the quarter turn. M-2 here is the same wording at $n = 122$. That review graded it a
  note and this one minor, because line 15 read literally is false of a core that leaves
  $K$. The frozen grade stands; the fix asked of the author is the same.
- *Green’s margin.* The 11 October final review computed
  $563/50 - 11.22928087555\ldots = 0.0307191\ldots$, as this review does to more places.
- *The transfer.* That review found the derivation of 123 to 126 valid by either route
  the record gives, containment of 122 squares in $N$ or the mass below $N$; step 7 here
  uses the first.
- *Significance.* The grading review confirmed `S3` “as T-080, five counts by
  monotonicity”, and the 14 October review confirmed $n = 145$’s `S3` by pointing to
  T-144’s five counts at $k = 11$. This review confirms `S3`, with four counts on the
  reported lane (R-1).

**What this review adds.**

- *A complete decision apart from the source’s code.* The 2 October review’s list of
  what the replay must show says that “the point and segment paths have no second
  implementation anywhere”.
  The 14 October review says the same for $n = 145$ and names “an independent
  implementation of the linear bounds” as a possible second route.
  This review’s branch and bound and vertex argument are such an implementation, and
  they decided every angle of this certificate, and only this certificate, with two
  mutants refused.
- *R-1,* which neither earlier review could raise: T-180 landed on 14 October, after the
  final reviews of 11 October compared $563/50$ with Nagamochi’s value at 126, then the
  reported lane there.
- *M-1.* T-144’s `notes` and its evidence entry’s `limitations` already say that the
  release’s `SHA256SUMS` omits the asset; no earlier review took it up, and the sibling
  assets are listed.

**What the earlier reviews raised that this one did not.**

- *The records carry no per-angle bound.* LC-4 of 2 October and F-5 of 14 October
  (minor) say that `certificate.json`’s records hold the index, status, input digest and
  node count, and each angle’s `lower` lives only in the proof bundle.
  The same holds here (`out/premises.json.gz`: the records list digests and node
  counts), and this review did not raise it.
  It stands for this certificate as F-5 states it, and question 3 of 14 October applies
  here too.
- *Exit status.* The 2 October review’s hypothesis 10: every acceptance check in the
  source’s drivers is an `assert`, and the C++ exits zero on an unresolved angle, so a
  run of the source’s command must keep assertions on and read the status.
  N-5 here covers the C++’s asserts only.
- *Dependencies.* The 2 October review noted that the READMEs ask for NumPy, SciPy,
  Numba and HiGHS while the replay path imports the standard library and needs a C++17
  compiler. This README asks for the same (line 48), and this review did not check what
  the replay imports.
- *The case records.* The 11 October final review’s F1-4 found that `n-122.md` to
  `n-126.md` listed nothing of T-144’s evidence.
  That has since been fixed: all five now list `E-wand125-linear-n122-1126-report`.

**Where they differ.** The 11 October grading review groups T-144 with T-132, T-142 and
T-143 as entries that “say that a replay would be re-implemented sharing the producer’s
components”. T-144’s `composition` said then, on PR #487’s branch at `aeb8a7219`, the
commit the companion review of the lower bounds names, and says now that a replay here
“would run the source’s checker unchanged”, which is a confirmation reproduced with the
producer’s code, as this review and the 14 October review’s §9 put it.
The grouping fits the three check2 entries, whose replays run this repository’s crate as
the producer adapted it, and not T-144.

## Note on This Copy

This copy differs from the frozen text
(`frozen/review-2026-11-18-wand125-linear-n122.frozen.md`, bound by
`frozen/findings-frozen-digest.txt`) in two places, both written after the freeze by
lane r144b-1118: the body of Comparison With Earlier Reviews, and this note.
No finding, verdict or number above changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
