# Lane rR1-lower: Findings as Frozen Before Any Program of the Source Was Opened

Frozen at the time in `frozen/findings-frozen-digests.txt`, which carries this file's
SHA-256. This is the text of the review's sections as they stood then; the review
document repeats them and marks what it changed afterwards.

**Two agents wrote this.** The lane's first agent froze the plan and the checker, ran the
premises, the search, the two-bin tier and the controls, and drafted the argument, the
decider's description and most of the findings below; it was cut off by a usage limit at
about 20:40Z on 20 November 2026, with the whole-certificate sample on its first
certificate. A second agent resumed the lane at 21:04Z from the pushed branch, the working
tree, the first agent's draft sections and logs in scratch space, and the bead; it checked
the drafts' numbers against the receipts, completed the sections the drafts left open (the
controls' outcomes, what was decided, the verdict), and froze this text. Neither agent had
opened a program of the source: the source checkout is sparse, and `proof/*.cpp`,
`proof/*.py` and every `verify.py` were never on this machine's disk before this freeze.

**The whole-certificate sample (control A0) was still running at this freeze.** Its first
run left no receipt (amendment A2). It was started again at 21:18:33Z under the resumed
lane's rule, one certificate per computation and at most 30 minutes each, by a driver
recorded in `frozen/checker-amendments.txt` before it ran (A2 to A4), and its receipts are
added after this freeze by that driver alone, with no change to any program. Its expected outcome is
stated here in advance: every bin it decides is accepted (`DECIDED` for a certificate it
completes, `NOT_COMPLETED_WALL_CAP` with every decided bin accepted otherwise). Any other
outcome is a finding added after the freeze and is marked so.

## Summary for the Author

**Verdict, frozen before any program of yours was read: the method is sound as
`proof/INTEGER_CHECKER.md` describes it, and nothing this review ran contradicts any of
the 77 certificates.** Each lemma the method needs was re-derived here and holds, with
one hypothesis that the implementation must respect (below); every exact premise of all
77 certificates holds; no unit square was found with a capture below 1; and this
review’s own exact decider, which shares neither your octagon nor your kernels, decided
155 bins across all 77 certificates, among them the bin of each certificate where
this review’s search found its least capture; its sample of nine whole certificates was
still running when this verdict was frozen. Whether the kernels
implement the lemmas soundly was read after this verdict was frozen, in
[After the Freeze](#after-the-freeze).

- **What is claimed.** For each certificate, $s(n) > L$, with $L$ the certificate’s side,
  equal to the claimed rational at all 75 claimed counts; the measure has total mass
  $n - 10^{-6}$ (76 certificates) and every closed unit square in $[0, L]^2$ is to
  capture at least 1.
- **The lemmas.** Exclusion (L1), the symmetry reduction with the domain set by the
  bin’s left end (L2), the octagon (L3), the angle error (L4), the Brunn–Minkowski
  interpolation (L6) and the quadratic step (L7) are proved below. L6 needs every
  corner set nonempty; a rectangle with a zero lower bound at any corner of a cell must
  count zero at all of them, and a counterexample shows the rule is necessary (F-2).
  L4’s bound needs a nonnegative centre and left end.
- **The premises, all 77, exactly.** Rows inside the board with positive extent and
  positive mass, no points, the same rows at every level, the stated totals, mass below
  the count, the eight-image expansion invariant, and the listed bins covering
  $[0, \sqrt 2 - 1]$ with no gap and no overlap; the side equals the claimed value.
- **The search.** At 462 poses (six per certificate) found by a float search over 33
  angles and 1,681 centres each, the exact captures are all at least 1: the least is
  $1.0005829$ (`1041/n105`), the median of the 77 least captures $1.00462$, and 11 of
  the 77 least captures sit at the axis-parallel square in the board’s corner.
- **The decider.** Two bins of each of the 77 certificates, the bin holding the least
  capture the search found and a seeded one, 154 bins, were each decided completely:
  every centre of the quadrant, for every angle of the bin, captures at least 1. None
  needed splitting; the least bound accepted on any box is $1 + 2.0 \times 10^{-8}$
  (`1042/n161`, the bin at $r = 0$ of its finest level). Pricing the cost decided one
  more bin (and one of the 154 again). The nine whole certificates of the frozen sample are
  reported in [What This Review Decided](#what-this-review-decided).
- **Controls.** The five premise controls and the three broken variants of the decider
  came out as planned. Of the 36 decider controls, 24 came out as planned and 12 did
  not, and none of the 12 is an unsound acceptance ([Controls](#controls)): the 99/100
  copy is refused with an exact witness at the six sampled certificates whose least
  capture found is below $100/99$ and accepted at the three above it; the threshold
  raised $10^{-4}$ above the least capture found is refused at eight and left undecided
  at one; and the plan’s expectation for the stretched copy was wrong for any
  certificate with more than about 0.2% of slack.

The findings are notes: an undocumented `fixed_mass` key (F-1); the zero-corner rule
L6 needs (F-2, to be confirmed in the code); the slack of eight certificates (F-3); the
weak negative control your README describes (F-4); the 64 certificates whose coordinates
no lattice finer than $2^{-37}$ holds exactly (F-5, for this review’s decider only); the
two standalone certificates under four-region claims (F-6); and the attachment of #1041
this review could not fetch (F-7). Questions are at the end.

## Scope

**Read.**

- The bodies of #1041 and #1042 through the REST API, fetched at 17:53:41Z on 20
  November, retained as `programs/issue-1041.json` and `programs/issue-1042.json`; the
  three replies on #1042, all by the author: the first in full (a follow-up at 161 by the
  four-region transfer), the second in full (an attribution correction), and the first
  4,000 characters of the third (a separate request for 155 counts with an encoded
  archive, not decoded and not in scope). #1041’s attachment
  `squaremath_continued_20261119.zip` was not fetched: the request returned 403 from
  this host.
- At the pin, as data: `README.md`, `CLAIM.md`, `FOLLOWUP.md`, `RESULTS.md`,
  `proof/INTEGER_CHECKER.md`, `constructions/README.md`, the three `PROOF.md` files of
  `followup/repeated/`, `followup/envelopes/` and `followup/corner_trim/`,
  `lower_bounds.csv`, `followup/best_by_count.csv`, `SHA256SUMS`, every certificate
  folder’s `manifest.json`, and, through this lane’s frozen programs, every measure file
  and the `r` field of every receipt line of the 77 certificates (617 files, each equal
  to its `SHA256SUMS` line). Before the plan, to learn the format: the keys and first
  three rows of `proof/n114/k80.json.gz`, three plus two lines of its receipts and two of
  `k240`’s.
- On `main`: `result-import.md` stage 4; the 18 November review of #1018 in full, as the
  model; `AGENTS.md`.
- By the agent that resumed the lane, before this freeze: the lane’s notes for
  sub-agents, `result-import.md` stage 4, the bead’s notes, the pushed branch, the working
  tree and the first agent’s draft sections and logs; for layout, the first 60 lines of
  the 20 November review of #1012, its packet’s findings digest list, and the heading
  lists of that review and of #1018’s; the manifests’ `nodes`, `directions` and
  `rectangles` fields; and `SHA256SUMS`, re-checked over the 617 certificate files.
  Nothing else of the source.

**Run.** Six Python programs and one C program of this lane’s, frozen before any of
them read a certificate, and one driver added by the resumed lane
([What I Ran](#what-i-ran)).

**Seen before the findings were frozen,** beyond the above: the lane’s brief, which named
the issues, the pin, the four source programs, the precedent, the stage, the freeze
protocol and the controls it wanted (a 99/100 measure, a widened interval, a flipped
rounding), and said where the record keeps the bounds; nothing of the bead `think-dhjz`
but its title.

**Not read before the findings were frozen:** any program of the source (`proof/gram.cpp`,
`proof/octagon.cpp`, `proof/check.py`, `proof/bm.py`, `proof/bmcheck.cpp`,
`proof/replay.py`, `proof/spot.py`, every `verify.py`), any receipt field but `r`, the
`verification.json`, `comparison.json` and replay records, the import lane’s draft pull
request, branch, packet and bead notes, and the record’s case files and register entries
for these counts.

**Not run:** any program of the source, and any program of this repository.

## The Claim

|  | #1041 | #1042 |
| --- | --- | --- |
| Certificates | 34 folders `proof/nNNN/`, one per row of `lower_bounds.csv` (50 to 137) | 43 folders `followup/lower/nNNN/` (50 to 162); 41 are the method “standalone certificate” of `followup/best_by_count.csv`, and `n138` (side 11.882) and `n162` (side 12.881) lie under the four-region claims at 138 and 162, which are out of scope |
| Kernels (manifest) | `octagon` 24, `octagon-gram` 10 | `octagon-gram` 43 |
| Claim | $s(n) \ge L$, $L$ the certificate’s side, equal to the claimed rational at every claimed count | the same |
| Measure | 34 files of rectangle rows, no points | 43 such files |
| Directions | 7,559 bins in two to four levels | 11,430 bins in one to six levels |
| Source’s centre boxes (manifests) | 135,207,431 | 212,838,728 |

All 77 have total mass $n - 10^{-6}$ except `1042/n162`, at $n - 0.3004$. Together
they hold 163,446 rows, 1,268,712 distinct rectangles after the eight-image expansion,
and 18,989 bins. Each folder holds one measure file per level (`kK.json.gz`, the same
rows at every level, format M keys `n`, `L`, `total_mass`, `points`, `rectangles`,
`proof_net`, `B`) and one receipt file per level, a JSON line per bin with its index
`r`; the bins of a level are read here as $t \in [(r - 1/2)D, (r + 1/2)D]$, $D$ the
level’s `proof_net.step`.

## The Argument, Re-Derived

Write $K = [0, L]^2$; $S(c, \theta)$ the closed unit square with centre $c$ and sides
along $e(\theta) = (\cos\theta, \sin\theta)$ and $e^\perp(\theta)$;
$t = \tan(\theta/2)$, so $e = ((1 - t^2), 2t)/(1 + t^2)$ is rational for rational $t$;
$w(t) = (1 + 2t - t^2)/(2(1 + t^2)) = (\cos\theta + \sin\theta)/2$, the least distance
from a wall at which a square of angle $\theta \in [0, \pi/2]$ can have its centre;
$\mu$ the certificate’s measure, each row’s mass spread evenly over its eight images
under the symmetry group of $K$.

1. **Exclusion (L1).** $\mu \ge 0$ has a bounded density on $K$ and
   $\mu(K) = M < n$. If every closed unit square $S \subseteq K$ has
   $\mu(S) \ge 1$, then $n$ unit squares with disjoint interiors in $K$ would carry
   $\sum_i \mu(S_i) = \mu(\bigcup_i S_i) \le M < n$, since their boundaries are
   null: a contradiction. A packing in a smaller square is one in $K$. So
   $s(n) > L$.
2. **Symmetry (L2).** $\mu$ is invariant under the eight symmetries of $K$. A
   reflection takes $S(c, \theta)$ to a square of angle $-\theta$ or
   $\pi/2 - \theta$, so the angles fold to $\theta \in [0, \pi/4]$,
   $t \in [0, \sqrt 2 - 1]$; the quarter turn about $(L/2, L/2)$ takes
   $S(c, \theta)$ to $S(c', \theta + \pi/2) = S(c', \theta)$, so the centres fold to
   the closed quadrant $c \in [L/2, L - w]^2$. Since
   $w'(t) = (1 - 2t - t^2)/(1 + t^2)^2 \ge 0$ on $[0, \sqrt 2 - 1]$, every square of
   a bin $t \in [l, h]$ that lies in $K$ has its centre in
   $[w(l), L - w(l)]^2$: the domain is set by the bin’s left end, $w(\max(l, 0))$,
   and must be rounded outward.
3. **The octagon (L3).** In the frame of $\theta_0$ the square at
   $\theta_0 + \delta$ is
   $\{\lvert u\cos\delta + v\sin\delta\rvert \le 1/2,\ \lvert -u\sin\delta +
   v\cos\delta\rvert \le 1/2\}$. If $\lvert u\rvert + \sigma\lvert v\rvert \le 1/2$
   and $\lvert v\rvert + \sigma\lvert u\rvert \le 1/2$ with
   $\sigma \ge \lvert\sin\delta\rvert$, then
   $\lvert u\cos\delta + v\sin\delta\rvert \le \lvert u\rvert +
   \lvert\sin\delta\rvert\lvert v\rvert \le 1/2$, and likewise the other. So
   $O_\sigma$ lies in every square of the bin when $\sigma$ bounds the bin’s angular
   deviation from $\theta_0$. Its area is $1/(1 + \sigma)$.
4. **The angle error (L4).** The derivative of $2\arctan s$ is $2/(1 + s^2)$, so for
   $t'' \in [l, l + h]$, $l \ge 0$, and a centre $t' \ge 0$,
   $\lvert 2\arctan t'' - 2\arctan t'\rvert \le 2\lvert t'' - t'\rvert/(1 +
   \min(t', l)^2) \le (h + 2\lvert t' - t\rvert)/(1 + \min(t', l)^2)$, with $t$ the
   bin’s centre. The exact largest deviation from $t$ is
   $2\arctan((t - l)/(1 + t l))$.
5. **Brunn–Minkowski (L6).** For convex $R$ and $O$ and $K(p) = R \cap (p + O)$:
   if $x_j \in K(p_j)$ and $p = \sum_j \lambda_j p_j$ with $\lambda$ in the simplex,
   then $\sum_j \lambda_j x_j \in R$ and $\sum_j \lambda_j x_j - p =
   \sum_j \lambda_j (x_j - p_j) \in O$, so $\sum_j \lambda_j K(p_j) \subseteq K(p)$.
   When every $K(p_j)$ is nonempty, the Brunn–Minkowski inequality for nonempty
   compact sets in the plane, with homogeneity and induction on the number of sets,
   gives $\lvert K(p)\rvert^{1/2} \ge \sum_j \lambda_j \lvert K(p_j)\rvert^{1/2}$,
   and the same for the mass under a constant density. The hypothesis is needed:
   with $R = [0, 1]^2$, $O = [-1/2, 1/2]^2$, $p_1 = (1/2, 1/2)$, $p_0 = (-5, 1/2)$ and
   $\lambda = (1/2, 1/2)$, $K(p)$ is empty while the right side is $1/2$.
6. **The quadratic step (L7).** For integers $v_j \le \sqrt{m_j}$ and any $a$,
   $(\sum_j \lambda_j v_j)^2 \ge \sum_j \lambda_j(2 a v_j - a^2)$, affine in
   $\lambda$, so its least value over a box is the least of the corner totals. For
   $H = \sum_R a_R a_R^{\mathsf T} \succeq 0$ and any $z$,
   $\lambda^{\mathsf T} H \lambda \ge 2\lambda^{\mathsf T} H z -
   z^{\mathsf T} H z \ge 2\min_i (Hz)_i - z^{\mathsf T} H z$ on the simplex. With
   $z = w/Z$ for integer weights summing to $Z$, the bound is
   $(2 Z \min_i (Hw)_i - w^{\mathsf T} H w)/Z^2$, rounded down. Either diagonal’s two
   triangles cover the box, and so do its four corners.
7. **Completeness (L8).** The certified bins must cover $t \in [0, \sqrt 2 - 1]$, and
   every centre box of every bin must pass, with no leaf passed by a budget stop.

## This Review’s Decider

`rr1_decide.py` with `rr1_decide.c` decides, for one bin $t \in [l, h]$ (clipped to
$[0, t^\ast]$, $t^\ast = 41421357/10^8 \ge \sqrt 2 - 1$), that every centre $c$ of the
quadrant $[L/2, L - w(l)]^2$ has $\mu(c + P) \ge 1$, where $P$ is a lattice polygon
inside every centred unit square of the bin. It does not use the octagon lemma (L3) or an
angle error (L4).

- **The polygon.** Let $I = \bigcap_{\theta \in [\theta_l, \theta_h]} S(0, \theta)$. For
  a point $p$ and $f(\theta) = p \cdot e(\theta) = \lvert p\rvert\cos(\theta -
  \varphi_p)$, the largest value on an interval shorter than $\pi$ is $\lvert p\rvert$
  if the direction $\varphi_p$ lies in it, else the larger end value. Since
  $S(0, \theta) = \{p : (R^{-k} p) \cdot e(\theta) \le 1/2,\ k = 0, \ldots, 3\}$, with
  $R$ the quarter turn, membership in $I$ is decided exactly from the rational end
  vectors $e(\theta_l)$, $e(\theta_h)$ and a sector test. $P$ is the hull of sixteen
  lattice points, each verified in $I$: near the tangent points $e(\theta_l)/2$,
  $e(\theta_h)/2$, the arc point $e(\theta_m)/2$ at $t_m = (l + h)/2$, and the corner
  where $p \cdot e(\theta_h) = 1/2$ meets $p \cdot e^\perp(\theta_l) = 1/2$, and their
  quarter turns. So $P \subseteq I$, and $P$ contains the source’s octagon centred at
  $t_m$ up to the lattice rounding, since the octagon’s edges leave its tip more steeply
  than the chords. $P$ misses $I$ only by the four circular segments, of area about
  $\Delta^3/48$ for an angular width $\Delta$.
- **Exact areas.** Lengths are integers on a lattice of $Q$ points per unit: the least
  common multiple of the coordinates’ denominators times a power of two when that is at
  most $2^{37}$ (exact), else $Q = 2^{35}$ with every rectangle rounded inward (64 of the
  77). The area of $R \cap (c + P)$ is bounded below by the hull of the lattice points
  that are verified, in signed 128-bit arithmetic, to lie in both: the polygon’s
  vertices in $R$, $R$’s corners in $c + P$, and each crossing of a polygon edge with a
  rectangle edge, rounded along that edge into the polygon. There is no floating point
  in any accepted bound. A density is $\lfloor \rho\, 2^G/(2Q^2) \rfloor$ and a mass
  $\lfloor d \cdot A_2 / 2^{G - 64}\rfloor$ in units of $2^{-64}$, $G \le 110$ chosen so
  that every product is below $2^{127}$.
- **The box bound.** For a box of centres with corners $c_1, \ldots, c_4$: rectangles
  inside $c_j + P$ at all four corners count their whole mass for every centre of the
  box (and leave the subtree); rectangles positive at all four corners enter
  $H = \sum_R s_R s_R^{\mathsf T}$, $s_{R,j} = \lfloor \sqrt{m_{R,j}}\rfloor$ (L6 over
  the four-corner simplex); the rest count zero. The term is bounded below by L7’s dual
  inequality at a test point nominated in floating point among the simplex’s faces,
  and at the four vertices, all evaluated exactly and rounded down. A box passes when the
  total reaches $2^{64}$; otherwise its longer side is halved. A box that cannot pass at
  width $2^{10}$ lattice units or within $10^6$ nodes stops the bin.
- **A stopped bin.** The driver evaluates true unit squares exactly at the stopped box’s
  corners and the bin’s end and middle angles, then searches the bin’s angles in floating
  point and evaluates the best poses exactly. A capture below the threshold is a
  refutation (`REFUSED_EXACT`); otherwise the bin is split in three and each part decided
  again, twice at most, else `UNDECIDED`.
- **Self-test.** On synthetic data only: 2,892 rectangle–polygon areas against exact
  rational areas (never above, within the lattice allowance); 40 random bins’ polygons
  against 401 sampled angles each; 40 box bounds against exact captures at points of the
  box; the domain against sampled angles; uniform and random measures accepted below
  their least capture and refused exactly above it; and the three broken variants T1 to
  T3 each caught. `PASS`, 5,933 checks.

## What This Review Decided

| Check | Population | Outcome | Receipt |
| --- | --- | --- | --- |
| Exact premises (L1, L2’s expansion, L8’s bins, L9) | all 77 | hold, every one | `out/premises.json` |
| Search for a unit square capturing less than 1 | all 77, 462 exact poses | none; least $1.0005829$ | `out/search.json` |
| The decider, two bins per certificate | 154 bins of all 77 | `DECIDED`, every bin, no bin split | `out/tier1/` |
| The decider, bins priced before the runs | `1041/n114` $K = 80$, $r = 40$ (one of the 154) and `1042/n136` $K = 324$, $r = 100$ | `DECIDED` | `out/decide-price-*.json` |
| The decider, whole certificates (A0) | nine, in the frozen order | running at the freeze | `out/sample/` |

**The premises.** For each certificate: the files parse under a strict reader; every row
is a rectangle of positive extent inside $[0, L]^2$ with positive mass; there are no
points; the rows are equal at every level; the exact sum of the masses equals the
file’s `total_mass` and the manifest’s target, and is below $n$ ($n - 10^{-6}$ at 76
certificates, $n - 0.3004$ at `1042/n162`); the eight-image expansion is invariant
under the eight symmetries, and its merged rectangle count equals the manifest’s
`rectangles` at all 77 (1,268,712 in all); the listed bins of all levels, read as
$t \in [(r - 1/2)D, (r + 1/2)D]$, cover $[0, \sqrt 2 - 1]$ with no gap and no overlap
(the least right end is $1909/4608 > \sqrt 2 - 1$); and the side equals the claimed
rational at the 75 certificates that have a claim.

**The search** is a diagnostic: it can refute a certificate and cannot confirm one. Per
certificate, a floating-point evaluation of true unit squares at 33 angles and
$41 \times 41$ centres of the quadrant, local refinement of the twelve lowest, and the
six lowest evaluated in exact rationals. The 77 least captures run from $1.0005829$
(`1041/n105`, $t \approx 0.2468$) to $1.0182492$ (`1041/n115`); 11 of them are the
axis-parallel square in the board’s corner.

**The two-bin tier.** For each certificate, the bin holding the angle of the least
capture found and one bin drawn by the frozen seed (no certificate drew the same bin
twice). The decider covered the whole quadrant of centres for each bin: 2,746,396
boxes and $3.67 \times 10^9$ polygon clips in all, tree depth at most 30, 1,424 CPU
seconds. Every bin was accepted without splitting. The least accepted box bounds are
$1 + 2.0 \times 10^{-8}$ (`1042/n161`, $K = 900$, $r = 0$), $1 + 2.6 \times 10^{-8}$
(`1042/n68`), $1 + 6.2 \times 10^{-8}$ (`1042/n104`): the branch and bound stops
splitting a box as soon as its bound reaches 1, so these are not the certificates’
margins. The least polygon area is $0.99508$. 64 of the 77 ran on the rounded lattice
(F-5).

So this review’s own decider has decided 155 of the 18,989 bins, 0.8%, chosen to
include each certificate’s worst angle found, and nothing below is a complete
independent verification of any certificate unless the sample completes one.

## Controls

Stated in `frozen/review-plan.md` and `programs/controls-plan.json` before any run, and
recorded as planned or not as planned; none was run again.

| Id | Change | Expected | Outcome |
| --- | --- | --- | --- |
| P0 | none, all 77 | premises hold | as planned |
| P1 | `1042/n136`: one row’s mass raised so the total is $n$ | refused | as planned |
| P2 | one row’s mass negated | refused | as planned |
| P3 | the middle bin of the finest level deleted | gap reported | as planned: gap $[46231/129600, 138859/388800]$ |
| P4 | one row’s $x_1$ set to $L + 1/1000$ | refused | as planned |
| P5 | a point mass added | refused | as planned |
| S0 | none, all 77 | no capture below 1 | as planned |
| S1 | every mass times 99/100, at the least pose found | below 1 at all 77 | **not as planned**: below 1 at 69; at the eight of F-3 the least capture found exceeds $100/99$ |
| A0 | the sample, every bin | `DECIDED` | running at the freeze |
| A1 | masses times 99/100, least-capture bin | `REFUSED_EXACT` | 6 as planned, **3 accepted** |
| A2 | threshold $10^{-4}$ above the least capture found | `REFUSED_EXACT` | 8 as planned, **1 undecided** |
| A3 | coordinates and side times $1001/1000$, masses kept | `REFUSED_EXACT` | 2 as planned, **7 accepted** |
| A4 | bin widened two steps each side, no splitting | not accepted | 8 as planned, **1 accepted** |
| T1 | broken variant: $P$ the square at the bin’s middle | caught | as planned |
| T2 | broken variant: zero corners kept in L6 | caught | as planned |
| T3 | broken variant: domain from $w(h)$ | caught | as planned |

The decider controls per sampled certificate, at its least-capture bin. A number after
`REFUSED` is the exact capture of the witness, a true unit square inside the board.

| Certificate | Bin ($K$, $r$) | Least capture found | A1, 99/100 | A2, threshold | A3, stretched | A4, widened |
| --- | --- | --- | --- | --- | --- | --- |
| `1042/n136` | 972, 0 | 1.00101 | REFUSED 0.99100 | REFUSED 1.00101 | REFUSED 0.99651 | undecided |
| `1041/n114` | 80, 80 | 1.00693 | REFUSED 0.99686 | REFUSED 1.00693 | **accepted** | undecided |
| `1042/n129` | 110, 0 | 1.01322 | **accepted** | REFUSED 1.01322 | **accepted** | undecided |
| `1042/n132` | 112, 0 | 1.00422 | REFUSED 0.99418 | REFUSED 1.00422 | **accepted** | undecided |
| `1042/n115` | 96, 96 | 1.01135 | **accepted** | REFUSED 1.01135 | **accepted** | **accepted** |
| `1041/n115` | 312, 0 | 1.01825 | **accepted** | REFUSED 1.01825 | **accepted** | undecided |
| `1041/n107` | 160, 60 | 1.00538 | REFUSED 0.99623 | **undecided** | **accepted** | undecided |
| `1042/n135` | 112, 103 | 1.00955 | REFUSED 0.99945 | REFUSED 1.00955 | **accepted** | undecided |
| `1041/n111` | 1188, 0 | 1.00414 | REFUSED 0.99409 | REFUSED 1.00414 | REFUSED 0.70193 | undecided |

What the twelve outcomes that were not as planned are, each read from its receipt:

- **A1, three accepted.** At `1042/n129`, `1042/n115` and `1041/n115` the least capture
  found is above $100/99$, so the 99/100 copy still covers at that bin, and the decider
  proved it does. The plan’s expectation was wrong for certificates with more than 1% of
  slack; the acceptances are consistent with the search and are not unsound. The control
  is sharp where it can be: all six certificates below $100/99$ are refused, each by an
  exact square capturing less than 1.
- **A2, one undecided.** At `1041/n107` the decider did not accept the raised threshold
  (the unsound outcome would be acceptance) and its witness step, which tries the
  stopped box’s corners and three angles of each part of the bin, found no exact square
  below the threshold, although the search’s least pose is one. The witness step is
  weaker than the search there; the decider is not shown unsound.
- **A3, seven accepted.** Stretching the coordinates by $1001/1000$ with the masses kept
  lowers every density by about 0.2%, so a certificate with more slack than that at the
  bin can still cover it, and the decider proved that these seven do. The plan’s
  expectation was wrong. The two refusals are the certificate with 0.10% of slack
  (`1042/n136`) and `1041/n111`, where an axis-parallel square near the wall captures
  only $0.7019$ of the stretched copy.
- **A4, one accepted.** `1042/n115`’s least-capture bin is the last of its level
  ($r = K$), and the decider clips every bin to $t \le \sqrt 2 - 1$, so the widened bin
  is $[15521/38400, t^\ast]$, about 2.3 steps wide and not five; with 1.1% of slack at
  that bin the acceptance is consistent. The control was not a widening on its right
  side there.

No control shows the decider accepting something false. What the controls do not show
is a refusal of every 99/100 copy: three sampled certificates, and by the search eight of
the 77, have room for one.

## What the Checkers Share

| Checker | Decides | Trusts |
| --- | --- | --- |
| The source’s kernels `gram.cpp` and `octagon.cpp`, through `check.py` and `bm.py`, on the author’s machines | Coverage at every bin of all 77 certificates, one run each, recorded as receipts | L2 to L8 as implemented; the octagon (L3) with the angle error (L4); 128-bit integer arithmetic with floating-point vertex proposals; the author’s compiler and machine; that the receipts are the runs’ |
| This review’s premises and search | Every exact premise of all 77; no capture below 1 at 462 searched poses | CPython 3.14.7 `fractions`; its own code |
| This review’s decider | The bins listed under [What This Review Decided](#what-this-review-decided) | L1, L2, L6 and L7’s inequality; the exact polygon membership test; signed 128-bit integer arithmetic in gcc 13.3.0 code; CPython `fractions` for the polygon and the witnesses; its own code |

This review’s programs share no code with the source; they were written from the
mathematics before any program of the source was opened. They share with the source the
reading of the format (rows as `[x0, y0, x1, y1]`, each mass shared over eight images
including duplicates, the bins centred at $r \cdot D$), the symmetry reduction (L2), the
Brunn–Minkowski interpolation (L6) and the dual inequality (L7), all three described in
`proof/INTEGER_CHECKER.md`, which this lane read first. They do not share the octagon or
its angle error: the decider’s polygon is the exact intersection of the bin’s squares,
rounded inward, and is decided vertex by vertex. Nor do they share the lattice, the
rounding of thresholds and densities, the floating-point vertex proposals or the
triangle split. An error in the shared mathematics would pass both; none was found, and
L6 and L7 are re-derived above with the counterexample that makes L6’s hypothesis
necessary.

Authorship overlaps at the system family only through this repository’s own programs,
which neither route ran: the issues say the search, the derivations and the certificate
construction were carried out by OpenAI GPT-6.2 Astra under the author’s direction; this
review is a Claude agent with its own prompt and files.

## Findings

No finding is blocking or major. Grades: blocking, major, minor, note.

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| F-1 | note (author) | `followup/lower/n161/k100.json.gz`, `k300`, `k900`; `followup/lower/n162/k100.json.gz`, `k300` | a key `fixed_mass`, equal to `total_mass`, that no document of the folder describes |
| F-2 | note, to be read in the code | `proof/INTEGER_CHECKER.md`, “From four corners” and “The triangular checker” | L6 needs every corner set of a rectangle nonempty; the rule “a row with a zero lower bound contributes zero” is sound only if it zeroes the rectangle at every corner of the cell |
| F-3 | note (author) | eight certificates | at the least captures this review found, `1041/n115`, `n130`, `n131`, `n135` and `1042/n115`, `n129`, `n130`, `n138` keep more than 1% of slack ($1.0104$ to $1.0183$); the 99/100 copy is accepted at their least-capture bins |
| F-4 | note (author) | `README.md`, “Reproduce” | the replay’s negative controls use quarter-strength weights, which any checker refuses; a 99/100 copy refused at every direction is the control that shows a kernel is sharp |
| F-5 | note | 64 of the 77 measures | coordinates whose least common denominator exceeds $2^{37}$ (up to $9 \times 10^{30}$, transplanted mixtures); harmless for the source, whose lattice rounds each rectangle both ways, and the reason this review’s decider rounds rectangles inward at $2^{-35}$ there |
| F-6 | note (record) | `followup/lower/n138`, `n162` | standalone certificates at 11.882 and 12.881, below the four-region claims at 138 and 162, which are out of scope; both hold as certificates |
| F-7 | note (record) | #1041’s attachment | `squaremath_continued_20261119.zip` (SHA-256 `d8d0d696…`) returned 403 here, so its identity with the folder’s `proof/` is not checked by this review; the folder’s 617 certificate files match its `SHA256SUMS` |

**F-1 — `fixed_mass`.** Five measure files carry `"fixed_mass"`, each equal to the
file’s `total_mass`: `160999999/1000000` at 161 and
`6195294667572573961101/38313604031114600000` at 162. This review’s frozen reader
refused the key, and was amended to accept it only when it equals `total_mass`
(`frozen/checker-amendments.txt`). If it means something else to your kernels, say so.

**F-2 — the zero-corner rule.** With $R = [0, 1]^2$, $O = [-1/2, 1/2]^2$,
$p_1 = (1/2, 1/2)$, $p_0 = (-5, 1/2)$ and $\lambda = (1/2, 1/2)$, $K(p) = \emptyset$
while $\lambda_1\lvert K(p_1)\rvert^{1/2} = 1/2$. So a kernel that kept the positive
corners of a rectangle with an empty corner set would overstate. A rectangle whose true
corner set is nonempty with a lower bound of zero is harmless either way. The documents
state the rule both ways (“A rectangle with a zero corner lower bound may be omitted”;
“A row with a zero lower bound contributes zero to this triangle”); see After the
Freeze for what the code does.

**F-3 — slack.** The exact least captures found are $1.01041$ (`1041/n135`), $1.01053$
(`1041/n131`), $1.01135$ (`1042/n115`), $1.01322$ (`1042/n129`), $1.01503$
(`1042/n138`), $1.01642$ (`1042/n130`), $1.01707$ (`1041/n130`) and $1.01825$
(`1041/n115`). A search finds upper bounds on a least capture, so this is slack the
search could not remove, not a proof of slack; but at the three of them that are in
the sample (`1041/n115`, `1042/n115`, `1042/n129`) the decider accepted the 99/100 copy
outright at the least-capture bin (A1), which proves that every square of that bin
captures more than $100/99$. Four of these counts are raised again in #1042 (115, 130,
131, 135), consistent with the slack.

**F-4 — the negative control.** `README.md` describes “negative controls with
quarter-strength weights”. A copy at a quarter of the mass captures about a quarter at
every pose; refusing it shows the kernel runs, not that it is sharp. This review’s
99/100 copies were refused with an exact witness at all six sampled certificates
whose least capture found is below $100/99$ (witness captures $0.9910$ to $0.9995$).

**F-5 — the lattice.** Not a defect of the certificates. The decider rounds a
rectangle inward only where its coordinates do not fit an exact lattice; the loss is at
most $2^{-35}$ per edge times the density, which for the densest rows (density
$72{,}421$ in `1041/n113`) is about $2 \times 10^{-6}$ per unit of edge.

**F-6 and F-7** are for the import lane.

## Questions for the Author

1. What is `fixed_mass` in `followup/lower/n161` and `n162`, and does any kernel read it
   (F-1)?
2. Do both kernels zero a rectangle at every corner of a cell when its lower bound is
   zero at any one (F-2)?
3. Would you run, or publish, a 99/100 control at every direction, as this repository’s
   census does, in place of quarter-strength weights (F-4)?
4. Do the eight certificates of F-3 support larger sides with the same measures?

## Verdict

Frozen before any program of the source was opened, and with the whole-certificate
sample still running:

1. **The method, as `proof/INTEGER_CHECKER.md` describes it, is sound**, on these
   hypotheses, each of which the implementation must meet and none of which this freeze
   has checked in the code: the centre domain of a bin is set by the bin’s left end and
   rounded outward (L2); the octagon’s $\sigma$ bounds the angular deviation of every
   angle of the bin from the octagon’s frame, including at a replaced or negative centre
   (L3, L4); every rounding goes toward less capture, the domain and the
   full-containment test outward (L5); a rectangle with a zero lower bound at any corner
   of a cell counts zero at every corner of that cell unless its corner sets are known
   nonempty (L6, F-2); the dual bound is scaled and rounded down (L7); and every leaf of
   every bin passes, with no budget stop counted as a pass (L8).
2. **Nothing this review ran contradicts any of the 77 certificates.** Their exact
   premises hold, no searched square captures less than 1, and this review’s decider
   accepted every bin it was given.
3. **The 77 bounds rest on the source’s kernels and receipts.** This review decided 155
   of 18,989 bins with a program of its own, which is a strong spot check of the worst
   angles found and not a replay. A complete replay of each certificate by the source’s
   kernels is the import lane’s, and this review has not seen it.
4. **No finding is blocking or major** at this freeze. F-2 becomes blocking if the code
   keeps the positive corners of a rectangle that has an empty corner set.

## What I Ran

All times are UTC on 20 November 2026. Host: 4 cores, Linux, gcc 13.3.0, CPython 3.14.7
run as `python -I`.

| When | What | Result | CPU |
| --- | --- | --- | --- |
| 17:53 | the two issues fetched through the REST API | retained under `programs/` | |
| 18:16 | the plan frozen, commit `a14dca6cde` | `frozen/plan-frozen-digests.txt` | |
| 18:33 | the checker and the controls plan frozen, commit `e324a433d9` | `frozen/checker-frozen-digests.txt` | |
| 18:38 | `rr1_selftest.py`, on the amended reader | `PASS`, 5,933 checks, T1 to T3 caught | |
| 18:41 | `rr1_premises.py`, first run | stopped at `1042/n161` on `fixed_mass`; amendment A1 | |
| 18:43 | `rr1_premises.py`, all 77, and P1 to P5 | `PREMISES_HOLD`; controls as planned | 82 s |
| 18:45 | `rr1_decide.py`, two bins, to price the runs | `DECIDED` | 45 s |
| 18:48 to about 20:40 | `rr1_runs.py sample`, on `1042/n136` | lost with the session, no receipt | about 5 CPU-hours, estimated |
| 18:58 | `rr1_search.py`, all 77 | `NO_COUNTEREXAMPLE_IN_SEARCH` | 438 s |
| 18:58 to 20:06 | `rr1_runs.py tier1`, all 77 | `DECIDED`, 154 bins | 1,424 s |
| 19:00 to 20:01 | `rr1_runs.py controls`, nine certificates | 24 of 36 as planned | 803 s |
| about 20:40 | the first agent cut off by a usage limit; the machine restarted at 20:53 | | |
| 21:04 | the lane resumed by a second agent | | |
| 21:10 to 21:17 | `rr1_sample_resumed.py`, first attempt, three processes in one session | stopped: about 0.1 of a core each, no batch finished (A3, A4) | 0.03 CPU-hours |
| 21:18 | `rr1_sample_resumed.py --own-sessions`, the nine certificates in the frozen order, 30 minutes each | running at the freeze | |

The lost run’s CPU is an estimate: three processes for an hour and fifty minutes on a
machine that two other runs of this lane and several other lanes shared. With it, the
lane had used about 6 of its 40 CPU-hours at this freeze.
