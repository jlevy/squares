# Review Plan for Issue 1042's Derived Lower Bounds (Lane rR2), Frozen Before Any Check Ran

Lane rR2-lower, bead `think-bgi2`, 2026-11-20. Scope: the derived arguments of issue 1042
(with 1039 and 1041) in `JoostdeWinter/square-packing` at
`21d944c43098e2261ab7d713cd10f02a5eb13f3d`, folder `lower_bounds_2026_11_19/`: the
repeated central strips at 188, 189 and 218, the four translated regions at 137, 138 and
162 with the 161 follow-up (issue comment 7020627554), and the corner reweighting at 217.
The integer octagon kernels and the standalone certificates are review R1's (bead
`think-dhjz`); here an anchor's coverage receipts are an input.

## Read Before This Plan

As data, no program of the source opened or run (`*.py`, `*.cpp` unread): the bodies of
issues 1039, 1041 and 1042 and the author's three comments on 1042 (the third, a separate
155-count request carrying a base85 archive, read only in its prose and outside this
scope); `CLAIM.md`, `README.md`, `FOLLOWUP.md`, `RESULTS.md`, `proof/INTEGER_CHECKER.md`
and the three `PROOF.md` of `followup/repeated`, `followup/envelopes` and
`followup/corner_trim`; the data files `claims.json`, `family.json`, `claim.json`,
`bounds.json`, `multipliers.json`, the `proof/manifest.json` and `verification.json` of
each anchor, the keys, totals and first records of the measure and receipt files,
`native-audits.json` and the rows of `followup/best_by_count.csv` in scope. For form only:
the blind review of issue 1050 on branch `claude/intake-2026-11-20-review-1050` (review,
plan, README, frozen digest files). Also seen: the parent epic bead's notes, whose last
entry says the import lane's phase 1 replays of #1051 all match; nothing there concerns
the derived arguments. Not read: PR 1051, its branch and packet, the import lane's notes,
review R1's branch and notes, and the record at these counts.

Observations made while reading the data, before this plan (each is re-decided by a
frozen checker below): the four anchor measures have coordinates on the $10^{-8}$ grid and
total masses $160.8398$ (A161a), $161.6996$ (A162a), $161.5015$ (A162b) and $160.9428$
(A161b); `family.json`'s $M + 2db + d^2c$ equals each claimed mass exactly; the 217
claim's `removed_mass` equals $\sum_k m_k(1 - \mu_k \phi)$ over the 140 multipliers
$\mu_k$ with $\phi$ the claim's `factor`, not $\sum_k m_k(1 - \mu_k)$; all 140 modified
primitives lie in $[0, C]^2$; the anchors 749858, 719881 and 931866 appear in
`native-audits.json` only as sampled replays and 932856 not at all.

## Claims in Scope

| Key | Bound | Anchor (folder) | Construction | Stated mass |
| --- | --- | --- | --- | --- |
| K188 | $s(188) \ge 6929/500$ | A161a, $S = 6429/500$, $p = 4$ (`repeated/161--749858-12.858-100-uniform`) | strips, $d = +1$ | $187999999/10^6$ |
| K189 | $s(189) \ge 13881/1000$ | A162a, $S = 12881/1000$, $p = 3$ (`repeated/162--719881-12.881-100-uniform_finish`) | strips, $d = +1$ | $188999999/10^6$ |
| K218 | $s(218) \ge 7433/500$ | A162b, $S = 6433/500$, $p = 3$ (`repeated/162--931866-12.866-100-uniform`) | strips, $d = +2$ | $217999999/10^6$ |
| K137s | $s(137) \ge 11881/1000$ (FOLLOWUP table, superseded) | A162a | strips, $d = -1$ | `repeated/claims.json` |
| K137e | $s(137) \ge 59406523/5000000$ | A162a (`envelopes/…`) | regions, centred, plain | `envelopes/claims.json` |
| K138e | $s(138) \ge 59410049/5000000$ | A162a | regions, centred, `round_steps` 8 | `envelopes/claims.json` |
| K162e | $s(162) \ge 2576221/200000$ | A162a | regions, centred, `round_steps` 8 | `envelopes/claims.json` |
| K161f | $s(161) \ge 8036307/625000$ | A161a | regions, seam $q = 18553/5000$, plain | comment 7020627554 |
| K217 | $s(217) \ge 1857/125$ | A161b, $S = 1607/125$, $p = 3$ (`corner_trim/161--932856-…_217_fastMix15`) | 140 corner multipliers, $C = 11/5$, then strips, $d = +2$ | $21699999/10^5$ |

## Notation

A measure file lists primitives $(R_k, m_k)$. Following `INTEGER_CHECKER.md`, its measure
on the board $[0,S]^2$ gives each of the eight images of $R_k$ under the symmetries of the
board mass $m_k/8$, uniformly; $f$ is the resulting density and $M = \sum_k m_k$. A tile is
a closed unit square, any orientation; it is admissible in a board if it lies inside it.
$\rho = \sqrt{1/2}$. The band of an anchor with $p$ periods is
$B = [a, a + p]$, $a = (S - p)/2$.

## Statements the Derivations Need

- **D0 (input).** For each anchor, every admissible tile in $[0,S]^2$ captures at least 1
  of $f$. Certified by the anchor's receipts with the kernel; R1 reviews the kernel. Here:
  the measure the receipts certify is the measure each derivation uses (identity), and the
  receipts cover every orientation and every centre the derivation needs (domain).
- **D1 (periods).** $f(x+1, y) = f(x, y)$ almost everywhere for $x, x+1 \in B$ and every
  $y$; the same with the axes exchanged.
- **D2 (strip lemma).** For $p \ge 3$, integer $d$ with $p + d \ge 2$, the extension $g_d$
  on $[0, S+d]^2$ (exterior kept, far side translated by $d$, band filled periodically)
  gives every admissible tile at least 1.
- **D3 (strip mass).** $\int g_d = M + d(b_x + b_y) + d^2 c$, with $b_x$, $b_y$ the masses
  of one full-length unit strip of $B$ on each axis and $c$ of one unit cell of $B^2$.
- **D4 (region lemma).** Split $[0,T]$ at $q$; regions $[0, q+r]$ (offset 0) and
  $[q-r, T]$ (offset $S-T$) on each axis; $g(P) = \max f(P + t_i)$ over the regions
  containing $P$. If $r \ge \rho$ and $\max(q, T-q) + r \le S$, every admissible tile of
  $[0,T]^2$ captures at least 1 of $g$.
- **D5 (circumradius rule).** For $P$ in one quadrant about $(q,q)$, the region of the
  opposite quadrant may be dropped where $\lvert P - (q,q) \rvert > \rho$.
- **D6 (region mass).** $\int g < n$ for each region claim, and the stated mass is an
  upper bound of $\int g$.
- **D7 (corners).** Only primitives in the corner squares of side $C$ change, weights stay
  nonnegative, a tile meeting a corner square has its centre in that corner's zone, and the
  local receipts certify the modified measure as counted (factor included) on the whole
  zone at every orientation.
- **D8 (corner mass).** The band is untouched, so D1 to D3 hold for the modified measure,
  and $M' + 4b + 4c = 21699999/10^5 < 217$.
- **D9 (pigeonhole).** Capture at least 1, nonnegative density, mass below $n$ and
  disjoint interiors exclude $n$ tiles in side $T$, so $s(n) \ge T$.

D2, D4, D5, D7's localization and D9 are proofs; the review re-derives them by hand. The
rest are finite and are decided by programs.

## Checks, Methods and Expected Outcomes

Every program is this lane's own, imports nothing from the source or this repository, uses
the Python standard library only, and runs under CPython 3.14.7 as `python -I`; C++ builds
with the host's g++ 13.3.0, `-O2 -std=c++17`. Exact means `fractions.Fraction` or integers.

- **C1 `rr2_measure.py` (module).** Reads a measure file; parses exact rationals; checks
  $\sum m_k$ against `total_mass`, every $m_k \ge 0$, every image inside $[0,S]^2$; expands
  the eight images; reports the coordinate grid.
- **C2 `rr2_strips.py` (D1, D3, D8; K188, K189, K218, K137s, K217).** Decides D1 exactly:
  for each unit strip of $B$ and each axis, the clipped images, translated to the first
  strip, give the same signed corner weights (a finite sum of half-open rectangle
  indicators is determined almost everywhere by its corner weights, and conversely).
  Computes $M$, $b_x$, $b_y$, $c$ by exact clipping, then $M(d)$; checks $p \ge 3$,
  $p + d \ge 2$, side $S + d$, $M(d) < n$, and equality with `family.json` and the stated
  masses. Reports the widest centred band on which D1 holds. For K217 it builds the
  modified measure $m_k \mu_k \phi$, checks each modified primitive lies in $[0,C]^2$,
  $\mu_k \ge 0$, the band misses the corner squares, D1 for the modified measure, and
  `old_mass`, `removed_mass`, `new_mass` exactly. Expected: all pass. Controls, each
  expected to be refused: a band primitive moved by $10^{-8}$; a band primitive's mass
  times $1 + 10^{-12}$; $p$ one above the widest periodic band; $n - 1$ in place of $n$;
  for K217 a multiplier on a primitive outside $[0,C]^2$, and a negative multiplier.
- **C3 `rr2_envelope.py` with `rr2_envelope.cpp` (D4 hypotheses, D5, D6; K137e, K138e,
  K162e, K161f).** Checks $r = 707107/10^6 \ge \rho$ (by squares) and
  $\max(q, T-q) + r \le S$. Computes rigorous integer upper and lower bounds of
  $\int_{[0,T]^2} g$ by a sweep over the whole board: coordinates exact on the
  $10^{-8}$ grid, each image's density rounded up (upper) or down (lower) to $2^{-40}$,
  the maximum taken over the regions containing each cell. For `round_steps` claims the
  opposite region counts only inside the disk: cells wholly inside or outside are decided
  by exact integer tests; for a straddling cell the area inside the disk comes from the
  closed form in long double, widened by $10^{-15}$ either way. Expected: upper bound
  below $n$ for all four; lower bound at most the stated mass (a stated mass below this
  review's lower bound would mean the source integrated less than its construction
  needs, which would be blocking). Cross-check: the plain construction at $T = S - 1$ on
  A162a must give C2's $M(-1)$, since both copies of the overlap then lie in the periodic
  band. Controls: synthetic measures with hand-computed envelopes (uniform density: mass
  $T^2$; a thin strip: the union of its translates; a patch seen only through the disk:
  the quarter-disk area, bracketed); $r = 707106/10^6$ refused; a seam with
  $\max(q, T-q) + r > S$ refused; for information, each claim's side plus $1/1000$.
- **C4 `rr2_selftest.py`.** Holds C1 to C3 to the synthetic cases above; run before the
  freeze and recorded.
- **C5 `rr2_sample.py` (time permitting; decides nothing).** Exact capture of random
  rational-angle tiles: under $g_d$ for K188 and K217 equal to the capture of the
  translated tile under the anchor; for the region claims, each tile inside its region
  and its translate inside $[0,S]^2$.
- **C6 (after the freeze).** Reads the source's derived-step programs
  (`followup/verify.py`, `repeated/period_verify.py`, `envelopes/envelope_exact.py`,
  `envelope_grid.py`, `envelope.cpp`, `corner_trim/verify.py`, `split_corner.py` and what
  they import) against D1 to D9, citing file and line; learns the receipt header format
  and writes `rr2_receipts.py` (disclosed as written after the freeze) to check D0's
  identity and domain for A161a, A162a, A162b, A161b and the corner receipts: every
  record `PASS`, angle bins covering $[0, \sqrt2 - 1]$ in $\tan(\theta/2)$, centre boxes
  covering $[S/2, S - w]^2$ (anchors) or the corner zone (local), rounded outward, and the
  measure digests matching the files the derivations read; for K217 that the local
  receipts certify $m_k \mu_k \phi$, not $m_k \mu_k$.
- **C7 (after the freeze) replay.** From a copy of the folder, read before it runs:
  `python3 followup/verify.py`; the author's 161 snippet; and, within budget, the native
  replays of A161a, A162a, A162b, A161b and the corner receipts with at most two workers.
  Mutations the source's verifier is expected to refuse: a band rectangle of A162a moved
  by $10^{-8}$; K138e's stated mass numerator lowered by one; one corner multiplier of
  K217 halved; K188 with $n = 187$; K161f with $q = 1/2$; K162e's side raised by $10^{-6}$
  with the stated mass kept. A mutation it accepts is a finding about the verifier.

## Order

1. This plan, the retained issue text and the source digests are committed and pushed
   with their SHA-256 in `frozen/plan-frozen-digest.txt`.
2. C1 to C4 are written and run on synthetic inputs only, then frozen (checker freeze 1);
   then they run on the source's data. C5, if written, is frozen before it runs.
3. Only then is any source program opened (C6) or run (C7).
4. The findings are frozen before PR 1051, the import lane's notes, review R1 and the
   record at these counts are read.

## Budget

The owner's 40 CPU-hours for this item; at most two worker processes; any single
computation stops at 30 minutes and is recorded undecided. Expected total under 10
CPU-hours.
