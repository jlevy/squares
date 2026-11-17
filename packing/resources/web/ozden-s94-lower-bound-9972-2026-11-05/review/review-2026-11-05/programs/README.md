# Programs of the Stage 4 Review of #910 (think-xzxd)

These programs were written for the stage 4 mathematical review of Doğa Özden’s
certificate for $s(94) \ge 2493/250$ (issue #910), by the separately prompted review
lane. They were written from the mathematics: the theorem and lemmas N0, D and C1 of
`packing/sqverify_fast/SOUNDNESS.md`, read as a specification, and the certificate’s own
JSON. No program reads or reuses any checker’s source.
The lane did not read `sqverify_fast/src/`, the lab’s `tools/audit.py`,
`tools/test_audit.py`, `tools/rescale.py`, `tools/replay.py`, `checks/` or
`exploratory/`, or the import lane’s tool `devtools.audit_dilated_measure`.

Everything runs under the project’s CPython 3.14.7 with gmpy2 and NumPy, through
`run.sh`, which uses isolated mode (`-I -B`) at `nice -n 19` with this directory on
`sys.path`. Receipts are in `../out/`.

```bash
run.sh PROGRAM.py ARGS...
```

`CERT` below is `source/certificate/n94-L9972.json.gz` of the packet
`ozden-s94-lower-bound-9972-2026-11-05`, and `PACKET` is the packet directory.

## What Each Program Does

| Program | Decides | Reads | Receipt |
| --- | --- | --- | --- |
| `xzcommon.py` | nothing (library) | the certificate | none |
| `premises.py PACKET HOSONO_GZ OUT` | the exact premises (below) | certificate, its JSON text, Hosono’s `candidate.json.gz`, the 99/100 mutant | `premises.json` |
| `axis_exact.py CERT OUT` | direction 0 over its whole quadrant, in exact integers | certificate | `axis-r0.json` |
| `capture_exact.py CERT R X Y [FACTOR]` | the exact capture at one pose (library and command) | certificate | printed |
| `bnb.py CERT R OUT [--mass-factor] [--threshold] [--region]` | one oblique direction over its whole quadrant (or a region), proved bounds in binary64 | certificate | `sample/bnb-rN.json`, `controls/…` |
| `bnb_exact.py CERT R X0 X1 Y0 Y1 OUT` | one oblique direction over a small region, in exact rationals | certificate | `exact-box-…json` |
| `poses_exact.py PACKET SAMPLE_DIR RECEIPTS_READ OUT` | exact captures at named poses, the controls’ witnesses included | certificate, `controls/`, the merged receipts, this review’s `sample/` | `poses-exact.json` |
| `validate_bnb.py CERT OUT R…` | nothing: cross-checks `bnb.py`’s per-box quantities against exact captures | certificate | `validate-bnb.json` |
| `read_receipts.py PACKET PREMISES OUT` | nothing about coverage: reads the lab’s archive as data | `receipts/`, `controls/` | `receipts-read.json` |
| `sample.sh CERT OUT_DIR R…` | runs `bnb.py` for a list of directions |  | `sample/` |
| `explore_measure.py`, `explore_measure2.py` | nothing: the coordinate order `[x1, y1, x2, y2]` and the D4 expansion, before the library existed | certificate | printed |
| `explore_landscape.py`, `explore_minima.py` | nothing: a float look at the capture to size the deciders | certificate | printed |
| `peek_index.py` | nothing: printed the index’s fields once | `receipts/INDEX.json.gz` | printed |

## The Deciders

### Direction 0: `axis_exact.py`

At $\theta = 0$ the core is axis-aligned, and
$F(x, y) = \sum_k \rho_k\, o(x; x_1, x_2)\, o(y; y_1, y_2)$ with
$o(z; z_1, z_2) = |[z - h, z + h] \cap [z_1, z_2]|$ and $h = B/2$. Each $o$ is
continuous and affine between consecutive points of $\{z_1 \pm h, z_2 \pm h\}$, so on
each cell of the grid of all such points (inside $[L/2, U_0]$, with both ends) $F$ is
bilinear, and its least value on the closed quadrant is at a grid vertex.
The program evaluates $F$ at every vertex exactly: all values are integers over the
common denominator $P \cdot D_c^2$, where $D_c$ is the l.c.m. of the coordinate
denominators (68 bits) and $P$ that of the densities (34,667 bits).
Each column is swept in $y$ by exact slope updates, and the least vertex is checked by
direct evaluation.

### Oblique Directions: `bnb.py`

For a box of centres $C = [x_0, x_1] \times [y_0, y_1]$ with centre $p_0$ and
half-widths $d_x, d_y$:

1. **Classification.** A rectangle is inside every $Q(p)$, $p \in C$, if its
   outward-rounded copy satisfies $|u \cdot (m - p_0)| + e_u + b_u \le h - \tau$ and the
   same along $v$, where $m$ is its centre, $e_u = c w_x + s w_y$ its half-extent along
   $u$ and $b_u = c d_x + s d_y$ the box’s. It is outside if the outward copy is
   separated from every $Q(p)$ along $u$, $v$, $x$ or $y$ by more than $\tau = 10^{-9}$.
   Both tests are triangle inequalities.
   Their binary64 error is below $10^{-13}$, far inside $\tau$.
2. **The centre.** For a boundary rectangle, its vertical section at abscissa $a$ is
   $\max(0, \eta(a))$ with
   $\eta(a) = \min(y_2, p_y + F_1, p_y + F_2) - \max(y_1, p_y + G_1, p_y + G_2)$, where
   $F_1 = (h - c\xi)/s$, $F_2 = (h + s\xi)/c$, $G_1 = (-h - c\xi)/s$,
   $G_2 = (s\xi - h)/c$ and $\xi = a - p_x$. As a minimum of affine functions less a
   maximum of affine functions, $\eta$ is concave.
   So on any piece between nodes,
   $\int \max(0, \eta) \ge \max(0, \int \eta) \ge \max(0, \text{trapezoid})$, and the
   sum over pieces bounds the area below for any nodes in $[x_1, x_2]$. The program uses
   the 14 nodes that contain every breakpoint: both ends, the square’s four vertex
   abscissae, and the eight crossings of the square’s edge lines with $y = y_1, y_2$.
   With these the bound is exact up to rounding, as `validate_bnb.py` shows.
   Integrating over the inward-rounded rectangle can only lower it.
3. **The gradient.** The capture is $C^1$ in $p$: translating the square by $t e_1$ is
   translating $R$ by $-t e_1$ relative to it, so by Fubini
   $\partial_x |R \cap Q(p)| = \sigma(x_1) - \sigma(x_2)$, the lengths of $R$’s left and
   right edges inside $Q(p)$, which are continuous in $p$. The same holds in $y$ with
   the bottom and top edges.
   For each edge, $\eta(a; p)$ is concave in $p$, since every piece is affine in $p$. So
   its least value on $C$ is its least corner value.
   Its greatest value is at most the least, over the nine (top, bottom) piece pairs, of
   that pair’s greatest corner value.
   An edge is stable on $C$ when one top piece is least and one bottom piece is greatest
   at all four corners, and $\eta$ has one strict sign there, all with margin $2E$. Then
   its length is affine on $C$, since a comparison of affine functions that holds at the
   corners holds on the box.
   A rectangle with both edges stable contributes an affine function, which is summed
   exactly through its corner values, so cancellations between rectangles are kept.
   The others contribute intervals, each cut by
   $|\sigma(x_1) - \sigma(x_2)| \le \min(y_2 - y_1,
   (x_2 - x_1)/(sc))$, since every piece has slope at most $c/s + s/c = 1/(sc)$ in $a$.
4. **Acceptance.** By the mean value theorem along $p_0 \to (p_x, p_{0,y}) \to p$,
   $F(p) \ge F_{\mathrm{lo}}(p_0) - G_x d_x - G_y d_y$ on $C$. A box is accepted when
   that, less its error budget, is at least the threshold, and is otherwise split along
   the coordinate with the larger term.
   A box whose centre estimate is below the threshold by $10^{-7}$ stops the run as a
   counterexample candidate.
   A box that cannot be split, or a run that passes its node limit, stops the run as
   unresolved.

### Error Budget

Write $u = 2^{-53}$. Every input to $\eta$ is a binary64 number (node, box corner) or
the nearest binary64 value to an exact rational ($c$, $s$, $h$, coordinates), with
relative error at most $u$. Each operation adds a relative error of at most $u$, and
every magnitude is bounded: $|\xi| < 10$, $h < 1/2$, $c \ge 3/5$, $s > 0$. Under these
bounds, one piece value $p_y + F_1$ is within $10u + 73u/s$ of its exact value, and
$\eta$ within $40u + 146u/\min(s, c)$. The program uses twice the larger bound
$E_\eta = (64 + 256/\min(s, c)) \cdot 2u$, and $E_\sigma$ adds the effect of
nearest-float edge coordinates.
A trapezoid sum of width $w$ is within
$w(E_\eta + 64 \cdot 2u (y_2 - y_1 + 1)) + 64u \cdot T$ of the exact sum of its pieces.
The box’s centre bound subtracts that budget for every rectangle, plus $10^{-9}$ for the
inside masses’ float sum (at most 6,720 terms of total 94, so below $10^{-10}$) and a
relative $128u$ per pair for the remaining sums.
The largest whole budget in any run is about $10^{-9}$. Every acceptance clears it.

### Small Regions: `bnb_exact.py`

The same three steps in gmpy2 rationals: exact classification without slack, exact
centre captures by polygon clipping, and exact edge-length enclosures with exact
stability tests. No error budget is needed.

## Runs and What They Printed

[`../out/RUNS.md`](../out/RUNS.md) lists every run with its arguments, receipt, what it
printed and its CPU cost, and `../out/sha256sums.txt` the bytes that ran.
The review, `review-2026-11-05-ozden-s94-9972.md`, reports the results.

## The Independence Record

For `packing/frontier/verifiers.yaml`, each deciding program (`axis_exact.py`, `bnb.py`,
`bnb_exact.py`, `capture_exact.py` through `poses_exact.py`, and `premises.py` as a
premise check) carries this record:

- `read`: `mathematics` and `specification` (`sqverify_fast/SOUNDNESS.md`’s theorem and
  lemmas N0, D, C1, R1 to R5, and the crate’s README for verdict meanings),
  `certificate-format` (the certificate’s own JSON), and `producer-output` (the lab’s
  receipts and control witnesses, read to compare).
  The review of #890’s certificate was read only after every program had run and the
  findings were frozen.
- `clean_room`: true. Its author read none of the producer’s verification code: not
  `sqverify_fast/src/`, the lab’s `verifier/` copy, `tools/`, `checks/` or
  `exploratory/`.
- `shares`: none.
- `written_by`: Claude (Anthropic), the stage 4 review lane, `tbd-strong-max` at maximum
  reasoning.
- `overlaps_producer`: `system-family`, since the lab’s agents included Claude agents;
  `separate_prompt` true and `separate_code` true.
  The lab’s checker, `sqverify-fast`, is this project’s own crate (lane W2), whose
  source no program here reads.

Coverage, for the evidence entries: `axis_exact.py` decides direction 0 in full;
`bnb.py` decides 25 of the 4,972 directions in full (a sample of 25 directions, each
whole); `bnb_exact.py` decides one region of direction 3663; `poses_exact.py` evaluates
named poses. Together: sampled, 26 of 4,972 directions.

`validate_bnb.py`, `read_receipts.py`, `tabulate.py`, `bands_regions.py` and the
`explore_*.py` and `peek_index.py` programs decide nothing.
