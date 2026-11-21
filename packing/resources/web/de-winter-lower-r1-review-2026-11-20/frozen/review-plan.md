# Review Plan, Lane rR1-lower (Frozen Before Any Checker Ran)

Blind stage 4 review R1 of the method behind the standalone lower-bound certificates of
jlevy/squares issues 1041 and 1042 (Joost de Winter, after Hiroaki Hosono), folder
`lower_bounds_2026_11_19` of JoostdeWinter/square-packing at
`21d944c43098e2261ab7d713cd10f02a5eb13f3d`. Bead `think-dhjz`. Written 2026-11-20 by the
lane, frozen before this lane wrote or ran any checker.

## What Was Read Before This Plan

- The bodies of issues 1041 and 1042 through the REST API (fetched 17:53:41Z), retained as
  `programs/issue-1041.json` and `programs/issue-1042.json`; the three comments on 1042,
  all by the author: the first in full (a follow-up at 161, `8036307/625000`, by the
  four-region transfer), the second in full (an attribution correction), and the first
  4,000 characters of the third (a separate request for 155 counts with an encoded
  archive; not decoded, not in scope).
- At the pin, as data: `README.md`, `CLAIM.md`, `FOLLOWUP.md`, `RESULTS.md`,
  `proof/INTEGER_CHECKER.md`, `constructions/README.md`, `followup/repeated/PROOF.md`,
  `followup/envelopes/PROOF.md`, `followup/corner_trim/PROOF.md`, `lower_bounds.csv`,
  `followup/best_by_count.csv`, the file list, every certificate folder’s
  `manifest.json` (fields `n`, `side`, `kernel`, `directions`, `levels`, `warp`), the
  four small JSON records of `proof/n114/`, the keys and first three rows of
  `proof/n114/k80.json.gz`, and, to learn the receipt format, the first three and last
  two lines of `proof/n114/k80_receipts.jsonl.gz`, the first two of
  `k240_receipts.jsonl.gz`, and the `r` lists of both. Those lines show per-direction
  fields `header`, `verdict`, `nodes`, `leaves`, `clips`, `depth`, `lower_units`,
  `seconds`; the five `lower_units` seen are within $2 \times 10^{-6}$ above
  $2^{48}$.
- Not read: any program of the source (`proof/gram.cpp`, `proof/octagon.cpp`,
  `proof/check.py`, `proof/bm.py`, `proof/bmcheck.cpp`, `proof/replay.py`,
  `proof/spot.py`, every `verify.py`), any other receipt, the import lane’s branch,
  packet, programs or bead notes, the issue’s other replies, and the record’s case files
  for these counts.

## The Population

The 77 standalone certificates are the 34 folders `proof/nNNN/` (issue 1041, one per
row of `lower_bounds.csv`) and the 43 folders `followup/lower/nNNN/` (issue 1042). Of the
43, 41 carry a row of `followup/best_by_count.csv` with method “standalone certificate”;
`n138` (side 11.882) and `n162` (side 12.881) are standalone certificates under the
claimed four-region bounds at 138 and 162, which are out of scope, as are the repeated
strips (188, 189, 218), the corner trim (217), the four-region bounds (137, 138, 162),
the follow-up at 161 and the corner families. Kernels by manifest: `octagon` 24 (all in
1041), `octagon-gram` 53.

## The Argument as Described, and the Lemmas It Needs

Notation: $K = [0, L]^2$; $\mu$ the certificate’s measure; a square $S(c, \theta)$ is
the closed unit square with centre $c$ and side direction $e(\theta) =
(\cos\theta, \sin\theta)$; $t = \tan(\theta/2)$ the half-angle tangent;
$w(t) = (1 + 2t - t^2)/(2(1 + t^2)) = (\cos\theta + \sin\theta)/2$.

**L1, exclusion.** If $\mu \ge 0$ is absolutely continuous on $K$, $\mu(K) < n$, and
$\mu(S) \ge 1$ for every closed unit square $S \subseteq K$, then $n$ unit squares with
disjoint interiors do not fit in $K$, nor in any smaller square; so $s(n) > L$. Needs:
no point masses (`points` empty), every row a rectangle of positive extent inside $K$
with nonnegative mass, and $\mu(K)$ computed exactly. Proof: interiors disjoint and
boundaries null give $\sum \mu(S_i) \le \mu(K)$. Status: standard; checked in exact
arithmetic on all 77.

**L2, symmetry.** The certificate’s rows are expanded into eight images under the
symmetry group of $K$, each with one eighth of the row’s mass (duplicate images kept);
the expanded $\mu$ is then $D_4$-invariant by construction. Consequences: (a) every
orientation folds to $\theta \in [0, \pi/4]$, $t \in [0, \sqrt 2 - 1]$, by a reflection;
(b) a quarter turn about the board centre maps $S(c, \theta)$ to $S(c', \theta)$, so
centres reduce to the closed quadrant $[L/2, L - w]^2$; (c) for a bin
$t \in [l, h] \cap [0, \sqrt 2 - 1]$, every admissible centre lies in
$[w(l), L - w(l)]^2$ because $w$ increases on $[0, \sqrt 2 - 1]$
($w'(t) = (1 - 2t - t^2)/(1 + t^2)^2 \ge 0$ there). So the domain must use the bin’s
left end, $v(\text{left}) = w(\max(l, 0))$, and be rounded outward. Status: proved here;
the source’s rounding is to be read in the code.

**L3, the octagon.** For $\lvert\delta\rvert \le \sigma$, the octagon
$O_\sigma = \{\lvert u\rvert + \sigma\lvert v\rvert \le 1/2,\ \lvert v\rvert +
\sigma\lvert u\rvert \le 1/2\}$ in the frame of $\theta_0$ lies in $S(0, \theta_0 +
\delta)$. Proof: in that frame the square is
$\{\lvert u\cos\delta + v\sin\delta\rvert \le 1/2,\ \lvert -u\sin\delta +
v\cos\delta\rvert \le 1/2\}$, and $\lvert u\cos\delta + v\sin\delta\rvert \le
\lvert u\rvert + \lvert\sin\delta\rvert\lvert v\rvert \le \lvert u\rvert +
\sigma\lvert v\rvert$; the other likewise. So it needs only
$\sigma \ge \sup_{\text{bin}} \lvert\sin\delta\rvert$, and $\sigma \ge$ the largest
angular deviation of the bin from $\theta_0$ suffices. Status: proved here. Its area is
$1/(1 + \sigma)$, which this plan uses to judge slack: a bin of angular half-width
$\sigma$ costs about $\sigma$ of area, so $\sigma$ must be close to exact and rounded
up, never down.

**L4, the angle error.** With bin $[l, l + h]$, $l \ge 0$, centre $t$ and a replacement
centre $t'$, every $\theta$ of the bin is within $(h + 2\lvert t' - t\rvert)/(1 +
\min(t', l)^2)$ of $2\arctan t'$ (mean value theorem; the derivative of $2\arctan$ is
$2/(1 + s^2)$, and every $s$ between $t'$ and a point of the bin is at least
$\min(t', l) \ge 0$). Status: proved here for $t' \ge 0$; for $t' < 0$ the bound is not
justified as written (check the code for negative centres, and for the bin at
$r = 0$, whose left end is $-h/2$). The exact deviation is
$2\arctan((t - l)/(1 + t l))$ to the left end, which is the larger one when $t \ge 0$.

**L5, rounding.** The lattice is $2^{-30}$, densities are rounded down to multiples of
$2^{-32}$, masses to multiples of $M^{-1}$, $M = 2^{48}$; the domain outward; each
rectangle has inward and outward forms; the octagon’s half-plane thresholds inward; a
corner mass is the exact area of the hull of lattice vertices verified (exact signed
128-bit tests) to lie in the inward rectangle and the octagon. Every one of these must
round toward less capture, except the domain (outward) and the full-containment test
(outward rectangle). Status: the stated directions are the sound ones; the code is to
be read for each, and for 128-bit overflow.

**L6, Brunn–Minkowski interpolation.** For convex $R$ and $O$ and
$K(p) = R \cap (p + O)$: if $p = \sum_j \lambda_j p_j$ with $\lambda$ in the simplex,
then $\sum_j \lambda_j K(p_j) \subseteq K(p)$, and, when every $K(p_j)$ is nonempty,
$\lvert K(p)\rvert^{1/2} \ge \sum_j \lambda_j \lvert K(p_j)\rvert^{1/2}$. Status:
proved here (convexity for the inclusion; Brunn–Minkowski for nonempty compact sets,
homogeneity and induction). The hypothesis that every corner set is nonempty is
necessary: with $R = [0, 1]^2$, $O = [-1/2, 1/2]^2$, $p_1 = (1/2, 1/2)$,
$p_0 = (-5, 1/2)$ and $\lambda = (1/2, 1/2)$, $K(p) = \emptyset$ while the right side is
$1/2$. So a rectangle whose lower bound is zero at any corner of the cell must
contribute zero at every corner of that cell, unless its true corner set is known to be
nonempty. To be checked in both kernels.

**L7, the quadratic step.** Four corners: with $v_j$ the floor of the square root of
the certified corner mass (units $M^{-1}$) and any real $a$,
$(\sum_j \lambda_j v_j)^2 \ge \sum_j \lambda_j (2 a v_j - a^2)$, affine in $\lambda$,
so the box bound is the least of four totals. Triangles: with
$H = \sum_R a_R a_R^{\mathsf T}$ (positive semidefinite) and any $z$,
$\lambda^{\mathsf T} H \lambda \ge 2\lambda^{\mathsf T} H z - z^{\mathsf T} H z \ge
2\min_i (Hz)_i - z^{\mathsf T} H z$ for $\lambda$ in the simplex; $z$ is any vector, so
its integer rounding (weights summing to 65,536) only weakens the bound; the bound must
be divided by the right powers of 65,536 and rounded down. Two triangles of either
diagonal cover the box. Status: proved here; the scaling, the rounding, the sign of a
negative total and the full-mass bookkeeping (“added once”) are to be read in the code.

**L8, completeness.** Every leaf of the subdivision passes; the leaves cover the closed
domain; a budget stop or an unproved leaf cannot pass; per level, the bins listed cover
their share of $[0, \sqrt 2 - 1]$, and the levels together cover it with no gap (a finer
level replaces whole coarser bins). Status: the bins are checked here from the
certificate files; the tree coverage is to be read in the code (receipts carry counts,
not trees).

**L9, the claim.** The side is the certificate’s exact `L`, the total mass is below the
count, and the claimed rational equals the side. Out of scope: whether the measure was
built from Hosono’s measures as described (`constructions/`); the bound needs only the
measure as given.

## Independent Checks

All programs are this lane’s own, written from the mathematics above, and run as
`python -I` (CPython 3.14.7) and a C program built with the host’s gcc 13.3.0. Before
the checker’s freeze they run on synthetic data only.

1. **Premises, all 77** (`rr1_premises.py`): format; every row inside $K$ with positive
   extent and nonnegative mass; no points; the exact total against the count and the
   stated total; the eight-image expansion and merging; equal rows across a
   certificate’s levels; the bins of every level and their union over
   $[0, \sqrt 2 - 1]$, assuming bins centred at $r \cdot$`step` of half-width
   `step`/2 (the format M convention) and reporting any gap or overlap.
2. **Seeded search, all 77** (`rr1_search.py`): a float search for low captures of true
   unit squares (a grid of centres in the quadrant at fixed angles, then local
   refinement), each end point evaluated exactly in rational arithmetic. It decides
   nothing unless it finds a capture below 1, which would refute the certificate. The
   same poses with every mass times 99/100 give the 99/100 witnesses.
3. **The decider** (`rr1_decide.py` with `rr1_decide.c`), clean room. For a bin
   $[l, h]$ it does not use the octagon lemma: it builds a lattice polygon $P$ inside
   $I = \bigcap_{\theta \in [2\arctan l,\, 2\arctan h]} S(0, \theta)$, vertex by vertex,
   with an exact membership test (at the bin’s rational end points
   $e = ((1 - t^2), 2t)/(1 + t^2)$, plus the radius test where a vertex’s direction
   falls inside the bin’s sector), and so $\mu(S(c, \theta)) \ge \mu(c + P)$ for every
   $\theta$ in the bin. It covers the quadrant $[L/2, L - w(l)]^2$, rounded outward, by
   a branch and bound whose box bound is: full masses of rectangles inside $c_j + P$ at
   all four corners, plus a Brunn–Minkowski term (L6) over rectangles positive at all
   four corners, minimized over the four-corner simplex by an exact dual test point
   (L7’s inequality; the test point is chosen in floating point and only nominates).
   Areas are exact integer hull areas of lattice points verified exactly inside the
   rectangle and the polygon, computed without floating point; densities are floored
   to multiples of $2^{-110}$ relative to the lattice area; masses are in units of
   $2^{-64}$. The threshold is 1. A box that cannot pass at the smallest size or within
   the node budget is a failure; the driver then evaluates true unit squares exactly at
   that box’s corners at the bin’s end and middle angles, and reports `REFUSED_EXACT`
   on a capture below 1, else splits the bin in three and retries, twice at most, else
   `UNDECIDED`. A certificate is `DECIDED` when every bin of its partition is.
4. **Self-test** (`rr1_selftest.py`, synthetic only): the clip routine against exact
   rational areas; box bounds against exact captures of $c + P$ at random points of the
   box; the polygon test against dense angle sampling; acceptance and refusal on
   synthetic $D_4$ measures with known least captures; and three deliberately broken
   variants of the decider (no angular widening, zero corners kept, domain from the
   right end of the bin) each caught.
5. **After the findings freeze**: read `gram.cpp`, `octagon.cpp`, `check.py`, `bm.py`
   and the other source programs as data; map L2 to L8 to their lines; compare the
   receipts with this lane’s results on the sample; and compare the bounds with the
   record in `packing/frontier/n-NNN.md`.

## The Sample, Fixed Here

The decider runs on whole certificates in this order, stopping when its cumulative CPU
reaches 24 CPU-hours or before a certificate whose cost, projected from the mean CPU per
bin so far, would pass that:

1. `1042/n136`, the largest stated gain of issue 1042 (0.1765);
2. `1041/n114`, the largest stated gain of issue 1041 (0.0672);
3. `1042/n129`, seeded pick 1;
4. `1042/n132`, the second of issue 1042 (0.1066);
5. `1042/n115`, seeded pick 2;
6. `1041/n115`, the second of issue 1041 (0.0200);
7. `1041/n107`, seeded pick 3;
8. `1042/n135`, the third of issue 1042 (0.1043);
9. `1041/n111`, seeded pick 4.

Seeded picks: `random.Random(int(SHA, 16)).sample(rest, 4)` in CPython 3.14.7, with
`SHA = 7a3b186a2e65c7f277c20770eb6727420f895862` (`origin/main` when this lane branched)
and `rest` the 72 labels other than the five deterministic picks, sorted as strings. The
stated gains are the issues’ own columns.

Besides the whole certificates, for each of the 77 the decider runs two bins: the bin
holding the angle of the least exact capture the seeded search found, and one bin drawn
by `random.Random(int(SHA, 16) + i)` for the certificate at index `i` of the sorted
labels.

## Controls, With Expected Outcomes

Must-refuse controls fail on a checker that accepts everything; must-accept controls on
one that refuses everything.

| Id | Change | Checker | Expected |
| --- | --- | --- | --- |
| P0 | none, all 77 | premises | hold |
| P1 | one row’s mass raised so the total is $n$ | premises | refused |
| P2 | one row’s mass negative | premises | refused |
| P3 | one bin of the finest level deleted | premises | coverage gap reported |
| P4 | one row’s $x_1$ set to $L + 1/1000$ | premises | refused |
| P5 | a point mass added | premises | refused |
| S0 | none, all 77 | seeded search | no capture below 1 |
| S1 | every mass times 99/100, all 77 | exact capture at the least pose found | below 1 |
| A0 | none, the sample, every bin | decider | `DECIDED` |
| A1 | every mass times 99/100, the least-capture bin of each sampled certificate | decider | `REFUSED_EXACT` |
| A2 | threshold $10^{-4}$ above the least exact capture found, at that bin | decider | `REFUSED_EXACT` |
| A3 | coordinates and side times $1001/1000$, masses kept, the least-capture bin | decider | `REFUSED_EXACT` |
| A4 | the least-capture bin widened by two steps on each side, no bin splitting | decider | not accepted |
| T1 | broken variant: $P$ = the square at the bin centre | self-test | caught |
| T2 | broken variant: zero corners kept in the Brunn–Minkowski term | self-test | caught |
| T3 | broken variant: domain from $w(h)$ | self-test | caught |

## After the Freeze, What Will Be Reported

A verdict per lemma (sound, gap or unverified), which certificates this lane’s checks
decide and which rest on the source kernels, the controls, the compute used (cap 40
CPU-hours for the lane, 24 for the whole-certificate runs), the comparison with the
receipts and the record, significance, and questions for the author.
