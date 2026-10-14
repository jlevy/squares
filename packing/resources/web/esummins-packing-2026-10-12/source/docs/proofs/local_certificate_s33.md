# LOCAL at S33 — the selection tree around A122's k6_07 minimum, with the full load-bearing set and no Trump cut — A125, 2026-09-07

Companion to `local_certificate.md` (A116, Theorem LOCAL and Lemmas SAT / COVER / LEAF / RELAX / STAB — used here
verbatim, nothing restated) and to A119's exact form (rational Farkas leaves, independent checker). New here: the
theorem applied to a **second class and a second kind of minimum**, with **L = the entire non-pin load-bearing set**
rather than a chosen load path, and with the Trump canary satisfied **on position alone**, so the certificate carries
no cut. Labels as in `local_certificate.md`: [T] proved, [S] routine, [M] measured
(`attempts/A125-s33-local-cert/{code,results,certs,logs,notes}`), [F] finding, [C] open. Conventions unchanged:
s0 = 969271/250000 = 3.877084, ŝ = 3.877083590022814, W = [3.82, s0], pins in A57's δ-cores (h = δ/√2, δ = 1e-2).

## 0. Verdict

> **The S33 minimum certifies at (r, ρ) = (0.2, 10°) and (0.05, 20°) with NO cut of any kind, with L = all five
> non-pin squares and P = all six k6_07 cells — the whole eleven-square skeleton, nothing dropped — and the limiter
> is neither Trump nor a rearrangement of L ∪ P but the tilt-cell count at ρ = 20°, r ≥ 0.1.** [M] §2–§4. Every leaf
> is a rational Farkas vector, and A119's independent checker validates the exported certificates unchanged. The
> consumer, however, is thin: exactly **one** alive node of A107's 1 421 (S33's own gallery node, A60/trump5
> `c0_Y0335`) lies inside, and what stops the rest is not the boxes' radius but the **sixth pin `BL(0,2)`** — the very
> cell that distinguishes k6_07 from trump5 (§5).

## 1. The object [T + M]

`a125lib`. **S33min** (A122 `results/exact.json`, the 50-digit Lagrange solution; rank-14 contact system,
Fritz–John residual 8.3e-9, all eleven squares load-bearing, no rattler) has s\* = 3.9169308657139205630…, class
**k6_07** under the identity of D4, cells `BL(0,0) BL(0,1) BL(0,2) BL(1,0) BR(0,0) TR(0,0)`. So Theorem LOCAL's data is

    L = { f0, f1, f2, f3, f4 },     P = the six k6_07 cells,     |L| + |P| = 11 = n.

**Reduction DROP is vacuous here** [T]: L ∪ P is the whole packing, so the certificate quantifies over nothing less
than an eleven-square configuration, and A116 §5's r = 0.3 limiter — "a rearrangement of L ∪ P that the DROPPED
squares would forbid" — cannot arise. That is the structural difference from S02 (L ∪ P = 9 of 11) and S07 (8 of 11),
and it is why no witness and no unresolved leaf appears anywhere in the grid.

**S38min** (second data point) has s\* = 3.9289146852229777, class **k6_21** under the D4 element `diag`,
(x, y, t) ↦ (y, x, −t); the image's slot squares land on k6_21's cells `BL(0,0) BL(0,1) BL(1,0) TL(0,0) TL(1,0)
TR(0,0)` to 1e-9 and the five free squares carry the common tilt 90° − 41.754063° = 48.245937°. A122's far-side crest
at 42.7941° (s = 3.934378) is a property of the C₂ ∧ C₃ family, not of N, and plays no part below.

The LP is 28-dimensional (5 free bodies × (x, y, θ) + 6 pin offsets + s) against A116's 22 (S02) and 19 (S07); the
root census finds 16–21 near pairs of 55 and 5·10²–1.6·10⁸ leaves after the interval screen.

## 2. The Trump canary is satisfied on position alone — no cut [M]

`a116lib.trump_in_N` over all eight D4 images, at **every** point of the grid and for **both** shadows:
`inside = False`, `ops = []`. This is A122 §8 checked inside the tree's own hypothesis rather than by a distance
table: at S33min the keystone `f0` is **upright** while Trump's nearest square is at 40.182°, so `f0`'s box contains
no Trump square for any r < 0.2054 **or** any ρ < 40.18°; at S38min the tightest free box is 0.2947 from any Trump
square and `f1`'s is 0.6771. Contrast A116 §4–§5, where S07's N had to be cut by `F_T(θ) > s0` from r ≥ 0.033 /
ρ ≥ 4.82° onward because Trump sits inside every larger box, and the uncut runs went ALIVE with witnesses at
side F_T(θ) < s0. **S33's certificate has no canary to dodge**: the cut column of every row below is `None`, and that
is a result, not an omission.

## 3. The measured grid [M] (`results/grid_S33*.jsonl`, `grid_S38.jsonl`)

A119's tree (one interval census per tilt cell, shared across leaves; the parent's Farkas vector inherited into each
child), `min_cell_deg = 0.05`, kill margin s0 + 1e-8, cap 1 800 s. Entries: certified minimum (the lowest closed
leaf's Farkas bound over the final cover) / tree nodes / tree wall.

**S33, k6_07 frame, L = f0…f4, no cut**

| r \ ρ | 5° | 10° | 20° |
|---|---|---|---|
| 0.05 | DEAD 3.879029 / 3 / 0 s | DEAD 3.877104 / 7 749 / 26 s | DEAD 3.877086 / 413 215 / 1 233 s |
| 0.10 | DEAD 3.877765 / 821 / 12 s | DEAD 3.877085 / 17 131 / 36 s | OPEN (cap) 3.877088 / 1 773 853 |
| 0.20 | DEAD 3.877130 / 7 063 / 25 s | **DEAD 3.877085 / 420 899 / 1 001 s** | OPEN (cap) 3.877087 / 1 264 247 |

**Largest certified: (0.2, 10°) and (0.05, 20°)** — the same two corners A116 certified for S02, reached with five
free bodies instead of four and with no cut. **S38, k6_21 frame, the single requested point: (0.1, 10°) DEAD,
certified 3.877093, 337 951 nodes, 1 400 s.**

**The measured minimum is s\* itself** [M]: box-constrained SLSQP inside N from 25–60 starts returns **3.916931 at
every certified S33 N**, i.e. the true minimum over N is the shadow minimum. The certified bound (3.87709) is
therefore 0.04 below the truth — the relaxation's loss, not the geometry's — and the kill has a margin of only
1e-6…5e-5 over s0 while the object it kills is 0.0398 above s0. The same reading as A116's ρ ≥ 20° rows.

## 4. The limiter [F]

Not Trump (§2); not a rearrangement of L ∪ P (§1: there is nothing to drop); but **the tilt-cell count at ρ = 20°,
r ≥ 0.1**. Five tilt dimensions must be bisected to ≈ 1° before the McCormick term ((q-range) × cell width) falls
below the margin, and the DFS does not empty its stack inside the cap — nor inside three times the cap:

| N | cap | nodes | closed leaves | certified min of the closed part | witnesses | unresolved |
|---|---|---|---|---|---|---|
| (0.1, 20°) | 1 800 s | 672 797 | 331 150 | 3.877093 | 0 | 0 |
| (0.1, 20°) | 5 400 s | 1 773 853 | 876 474 | 3.877088 | 0 | 0 |
| (0.2, 20°) | 1 800 s | 557 616 | 311 399 | 3.877087 | 0 | 0 |
| (0.2, 20°) | 5 400 s | 1 264 247 | 715 814 | 3.877087 | 0 | 0 |

**[F] Both are OPEN, not alive — and here that is a structural statement, not an absence of evidence.** A119's
correction of A116 turned three of four "capped" ρ ≥ 20° cells into ALIVE: a checked packing of L ∪ P below s0 sat
inside N, because the squares that would have blocked the rearrangement had been dropped from L. At S33 nothing is
dropped (§1), and 3 million nodes across the two cells produced **no witness at all**. `(0.05, 20°)` closes
(413 215 nodes, 1 233 s), so the ρ = 20° frontier lies between r = 0.05 and r = 0.1 — the identical frontier A116
reported for S02 and A119 for its ρ ≥ 20° cells, and the identical remedy (a C implementation of the census + LP, or
adaptive cell widths).

## 4a. The exact certificates and the independent check [M] (`certs/`, `results/check_local.json`)

Same object and same file format as A119 T1, so A119's checker — `check_local.py` + `exactiv.py`, imported unmodified
by `code/check125.py` (only the report is written under A125, since A119's own `main` writes into A119's results) —
reads them unchanged: no numpy, no scipy, no generator code, every decision in exact dyadic-rational interval
arithmetic, every Lemma RELAX row rebuilt by the checker itself, every `branch` justified by showing the omitted
selections impossible on the cell, every `dead` leaf's rational Farkas vector (multipliers in 2⁻⁴⁰ℤ) required to give
a bound > 969271/250000.

| certificate | bisect cells | branch | imp/infeas | dead leaves | multipliers | gz | generator | checker | verdict, min bound |
|---|---|---|---|---|---|---|---|---|---|
| **S33 (0.2, 10°)** | 197 978 | 7 017 | 33 366 | 215 904 | 4 385 025 | 34.3 MB | 1 228 s | 5 034 s | **VALID**, 3.877085097 |
| S33 (0.05, 20°) | 194 160 | 6 399 | 81 624 | 196 048 | 2 935 516 | 18.9 MB | 1 251 s | 4 078 s | **VALID**, 3.877086096 |
| S33 (0.1, 10°) | 8 052 | 321 | 974 | 8 758 | 185 809 | 1.70 MB | 57 s | 245 s | **VALID**, 3.877084626 |
| S33 (0.2, 5°) | 2 844 | 415 | 754 | 3 804 | 81 532 | 0.69 MB | 25 s | 106 s | **VALID**, 3.877131332 |
| S33 (0.05, 10°) | 3 486 | 260 | 649 | 3 747 | 78 768 | 0.77 MB | 26 s | 90 s | **VALID**, 3.877114509 |
| **S38 (0.1, 10°)** | 157 776 | 6 015 | 79 519 | 174 160 | 3 022 417 | 21.5 MB | 1 085 s | 4 942 s | **VALID**, 3.877107298 |
| **total** | 564 296 | 20 427 | 209 496 | **602 421** | **10 689 067** | 77.9 MB | 3 672 s | **14 497 s** | **6/6 VALID** |

Against A119's five certificates (53 094 dead leaves, 769 440 multipliers, 1 072 s of checking in total), the S33
headline alone is **4× the leaves and 5.7× the multipliers**, and the set is 11× and 14× — the price of five free
bodies and a 28-variable LP. Every min bound clears s0 = 969271/250000 = 3.877084; the tightest margin is
6.3·10⁻⁷ at (0.1, 10°) and the loosest 4.7·10⁻⁵ at (0.2, 5°).
Dual inheritance is left ON in the generator (a child is closed on the inherited vector only when that vector
certifies the bound on the CHILD's own rows), which is what makes a 2·10⁵-leaf certificate generable in 20 minutes;
the checker is the arbiter either way, and it re-derives every bound from the file.

## 5. Consumer [M] (`results/consumer.json`)

A116 §7(b)'s test with one necessary widening: the node's LP-support representative (A107 `extract.json` `cfg`,
eleven poses at s0, carried into the class frame) is matched **injectively against every body of N — the |L| free
boxes AND the |P| pin cores**. Testing the pins is what makes a trump5 node admissible against a k6_07 N at all:
trump5's five cells are a subset of k6_07's six, so the sixth, `BL(0,2)`, must be found in the support; it is not free
by the node's class. Over all 1 421 alive nodes carrying a support (A57 963, A60/trump5 283, A61 14, plus A107's
Part-II k0 nodes):

| N | inside (struct_op) | inside (any D4) | pin-eligible | of which A60/trump5 |
|---|---|---|---|---|
| S33/k6_07 (0.2, 10°) | **1** | **1** | 30 | 25 |
| S33/k6_07 (0.2, 5°), (0.1, 10°), (0.1, 5°), (0.05, 20°), (0.05, 10°) | 0 | 0 | 30 | 25 |
| S38/k6_21 (0.1, 10°) | 0 | 0 | 102 | 25 |

The single node inside is **S33's own gallery node, `c0_Y0335` (A60/trump5, level 1)**, at centre deviation 0.1044
and tilt deviation 8.699° — so it needs r ≥ 0.1047 and ρ ≥ 8.70°, which is exactly why it appears at (0.2, 10°) and
nowhere else on the grid.

**[F] What blocks the rest is the sixth pin, not the radius.** The body of N whose nearest support square is furthest
outside its own tolerance is `BL(0,2)` for **1 065 of the 1 421** nodes (then `BL(1,0)` 199, `TR(0,0)` 94); only 30
nodes have all six k6_07 cells fillable by distinct tilt-0 squares inside their δ-cores. The three basin-mates A122
identified are blocked in three different ways, none of them by the free boxes:

| gallery node | blocked by | reading |
|---|---|---|
| S34 `c0_Y0859` (A60) | `BL(0,2)` centre 0.0065 (inside h = 0.00707) but **tilt 0.75° ≠ 0**; and `f4` needs ρ ≥ 22.9°, r ≥ 0.265 | the sixth square is there but tilted |
| S35 `c0_Y0334` (A60) | `BL(0,2)` centre **0.0262 > h**; free boxes would fit at r ≥ 0.106, ρ ≥ 11.9° | the sixth square is LIFTED (cf. Trump's own 0.0326 lift) |
| K19 `node_053` (A38, Part II) | `BL(1,0)` 0.1326 off its cell; `f4` needs ρ ≥ 42.9° | a different skeleton |

For S38/k6_21 the same phenomenon with its own distinguishing cell: `TL(1,0)` blocks 1 020 of 1 421, and S38's own
node `c0_Y0169` needs r ≥ 0.2703 at ρ = 40°.

Distance census (the minimal centre radius at which a full match exists, over the eight D4 images): at ρ = 40°,
**2 nodes at r ≤ 0.2 and 10 at r ≤ 0.3** would be inside a k6_07 N (all but one A60/trump5) — i.e. the consumer grows
only when the tilt half-width reaches 40°, which is the far side of the ρ = 20° frontier of §4.

## 5a. What this removes from trump5's residual tree [M]

**One node of 325.** `docs/residue_ledger.md`'s protected-tier row gives A60's trump5 cover 325 alive nodes in
A107's input (S01 196, S07 18, S02 12, …), of which 283 carry an LP-support representative; `docs/budget.md`'s
protected-tier row prices the 15 protected classes excluding k0_00 — "conditioning trees per exact stratum; trump5's
residual tree" — at 3 800 CPU-h (range 2 900–6 300, 32 wall-days at five workers). The largest certified S33
neighbourhood kills the YES leaf of exactly **one** of those nodes, `c0_Y0335`, the level-1 node A107 matched to S33
itself; at A57's measured ~850 s for a non-logic node that is ≈ 0.24 CPU-h, i.e. **≈ 0.006 % of the protected-tier
row — inside the noise of its own range, and it does not move the budget's central estimate.** The reason is
structural rather than a matter of radius (§5): the certificate's hypothesis is a **k6_07** one, with six pin cores,
while a trump5 node carries only five, so the sixth cell `BL(0,2)` — precisely the cell Trump *lifts* — must already
be occupied, upright and inside its δ-core in the node's own support; it is the binding obstruction at 1 065 of the
1 421 alive nodes, and only 25 of the 283 trump5 supports fill all six cores at all. Nor is S33 what the window has
to exclude: it stands 0.0398 above s0 (A122 §7), so its neighbourhood prunes only nodes the cover has already
localised onto k6_07's skeleton. The lever that would widen this is visible in the distance census — the consumer
grows to 2 nodes at r ≤ 0.2 and 10 at r ≤ 0.3 **only once ρ reaches 40°**, which is on the far side of §4's ρ = 20°
frontier — and, more cheaply, promoting `BL(0,2)` from a pin to a free BOX would let the 258 trump5 supports that
leave that cell empty or lifted be tested at all (the mirror of A116-G2's "blocking squares as boxes": relaxing a pin
instead of adding a box, at the cost of one more free body in an already 28-variable LP). Against that, the price
side is favourable and unchanged from A116 §7(c): one certified N costs 25 s–1 250 s of tree plus ~5 s of vectorised
sampling, and is shared by every node inside it; the 90 s–5 034 s of independent rational checking is paid once per
certificate, not per node.

## 6. Obligations ledger

| # | item | status |
|---|---|---|
| A125-O1 | S33min and S38min as packings in their class frames (k6_07 identity, k6_21 `diag`), slot squares on the class cells | [T] `a125lib.selfcheck` |
| A125-O2 | Theorem LOCAL with L = the full non-pin load-bearing set; DROP vacuous | [T] §1 |
| A125-O3 | the Trump canary satisfied on position alone; no cut anywhere on the grid | [M] §2 |
| A125-O4 | the measured grid; largest certified (0.2, 10°) and (0.05, 20°); the ρ = 20° limiter | [M] §3–§4 |
| A125-O5 | sampling drawn → tested → hits, ≥ 10⁴ tested per certified N, 0 hits | [M] `results/sampling.json`, `N_boxes.json` |
| A125-O6 | rational Farkas certificates, validated by A119's independent checker | [M] `certs/`, `results/check_local.json` |
| A125-O7 | consumer counts and the `BL(0,2)` finding | [M] §5 |
| A125-G1 | (0.1, 20°) and (0.2, 20°) — open at the cap, not alive; a faster census/LP would close them | [C] |
| A125-G2 | the S33 N as a YES leaf inside A60's residual tree (A120's deployment path) | [C] |
