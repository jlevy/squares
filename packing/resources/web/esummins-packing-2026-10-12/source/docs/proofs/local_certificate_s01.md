# LOCAL-S01 — the basin of the "room at side 4" family is a LINE, not a ball: Theorem S01-LINE, its exact certificate per class frame, and what it consumes — A188, 2026-09-09

Target (A188 BRIEF, from A187's finding): of the 63 alive gallery pages, 23 minimise to family **S01** (A107's
side-4.000 shadow, `docs/residue_ledger.md` §1a) and 11 to **S03** (3.942809); neither had a local certificate
in any frame.  Build S01's.  Labels: [T] proved, [S] routine given cited items, [M] measured
(`attempts/A188-s01-basin/{code,results,notes,logs}`, ≤ 2 BelowNormal processes, read-only on every other
attempt), [F] finding, [C] open.  Conventions as `local_certificate.md`: s0 = 969271/250000 = 3.877084,
class pins on slot lines in slack cores of half-width h = δ/√2, δ = 10⁻², tilt exactly 0; `k5_11` =
{BL(0,0), BL(0,1), TL(0,0), BL(1,0), BR(0,0)}, `k5_16` = {BL(0,0), BL(0,1), TL(0,0), BR(0,0), TR(0,0)},
`trump5` = {BL(0,0), BL(1,0), BL(0,1), BR(0,0), TR(0,0)}.  The chord lemma is A144's
(`attempts/A144-guard-lines/notes/spec.md` LINE-1/LINE-2, `code/guardline.py` `minchord_box`).

## 0. Verdict

> **S01 is not a critical point.  It is the plateau {side = 4} of configurations in which one axis-parallel
> line crosses FOUR unit squares through their unit-chord bands — three of A107's 62 "variants" are visible on
> the representative alone (§1).  Its local certificate is therefore A144's chord-sum inequality with four
> terms, and its basin is a LINE object: unbounded along the line, half-width 0.207 across it at ANY tilt
> (0.408 at ±10°), exact in rationals, no LP, no tilt cells, no Hessian (§2–§3).  In every class frame the
> certificate is emitted for every line through a pin row or column (72 entries, all DEAD, §3).  Its consumer:
> 15 of the 23 S01 pages and 10 of the 11 S03 pages have their conditioned box inside a certified band —
> always on a line carrying ONE pin, so the LocalCompose YES leaf still owes two boxes to the NO children; no
> page dies outright (as A144 already found), and the NO side that would retire them is exactly A144's
> guard-line LP column (`guardlines` field, v3 clause), not a tree (§4–§5).**

## 1. What S01 is [T + M]

**The representative** (A107 `shadows.json` S01; `attempts/A188-s01-basin/notes/s01_identity.json`): trump5's
five slots + six free squares at s* = 4.000000000006:

| square | pose (x, y, tilt) | t = tan(θ/2) | contacts (A107) |
|---|---|---|---|
| f1 | (1.500, 1.686, 0°) | 0 | f3 (vertex-on-edge), BL(0,1) |
| f3 | (2.500, 1.499, 0°) | 0 | f1, f4, BL(1,0), BR(0,0) |
| f4 | (3.500, 1.500, 0°) | 0 | f3, f5, BR(0,0) (flush column), right wall |
| f2 | (1.725, 3.500, 0°) | 0 | f5, top wall |
| f5 | (2.517, 2.500, 0°) | 0 | f2, f4, TR(0,0) |
| f0 | (0.747, 2.715, 13.5°) | **free** | none — a rattler |

BL(0,0) touches nothing either (a second rattler); the tilt of f0 and the positions of f0, f2 (along the top
wall), f5 and f1 (along the row) are free at side exactly 4: **the side-4 set has positive dimension — a
plateau, not a strict or kink minimum**.  [M] Lines with ≥ 4 unit chords on the representative
(`s01exact188.py`): y = c for c ∈ [1.190, 1.995] crosses BL(0,1), f1, f3, f4 with chord exactly 1 each (the
lock); y = 1.000 crosses the bottom row BL(0,0), BL(1,0), BR(0,0) and f3; x = 1.000 crosses the BL column and
f0; x ∈ [3.005, 3.015] crosses BR(0,0), f4, f5, TR(0,0).  A107's "62 combinatorial variants" are which four
squares carry the lock and which cells are empty; the value is the same for all of them.

**Why the side is exactly 4.** [T] On the lock line, Lemma LINE-1 (A144) gives s ≥ Σ|l ∩ Q_i| = 4 for every
configuration in which the four squares keep a full chord; and 4 is attained (the 4×4 grid with five holes is
a packing of 11 at side 4).  So s_S01 = 4 exactly, locked by {BL(0,1), f1, f3, f4} in the representative — a
pin and three free squares — and by other quadruples in the other variants.

## 2. The unit-chord band and Theorem S01-LINE [T]

**Lemma CHORD-BAND [T].**  Let Q be a unit square at tilt θ (fold θ into [0°, 45°]) and l an axis-parallel
line at signed distance v from its centre.  Then |l ∩ Q| ≥ 1 iff |v| ≤ γ(θ) := (cos θ + sin θ)/2 − sin θ cos θ,
and min_θ γ(θ) = γ(45°) = (√2 − 1)/2 = 0.20710….  *Proof.*  A144's (CH): the chord is 1/cos θ on
|v| ≤ (cos θ − sin θ)/2 and decreases linearly to 0 at |v| = (cos θ + sin θ)/2; solving chord = 1 on the linear
piece gives |v| = γ(θ).  γ(0) = 1/2, γ is decreasing on [0°, 45°] (γ′ = (cos θ − sin θ)(1/2 − (cos θ + sin θ))
< 0 there), so its minimum is at 45°.  ∎  Consequently **W_ANY := 207/1000 < γ(45°)** is a band half-width
that works at every tilt, and for a tilt window [0, ρ] the width is γ(ρ) (exact values [M], from
`minchord_box` by bisection: 0.4082 at ρ = 10°, 0.3195 at 20°, 0.2500 at 30°).

**Theorem S01-LINE [T] (n-general).**  Let l be an axis-parallel line inside [0, s]², and let a packing of n
unit squares contain m distinct squares Q_1..Q_m whose centres satisfy |v_i| ≤ γ(θ_i) (for a pin in its slack
core: |v| ≤ 1/2 − h, which holds for every c in the pin's full-chord interval [y_p − (1/2 − h), y_p + (1/2 − h)]).
Then s ≥ m.  In particular m = 4 gives s ≥ 4 > s0, so the hypothesis

  N_l(k, w) := "the k pins whose full-chord interval contains c are in their cores, and (4 − k) OTHER squares
  have centres within w ≤ W_ANY of l, ANY position along l, ANY tilt"

is Dead(N, s0) for every c with the band inside the container; with the tilt of the free squares restricted
to [0, ρ] the width grows to γ(ρ).  *Proof.*  Lemma CHORD-BAND gives |l ∩ Q_i| ≥ 1 for each of the m
squares; Lemma LINE-1 (A144) gives Σ|l ∩ Q_i| ≤ s.  ∎  (Lean shape: A144's `chord_sum_le_side` plus the
one-variable inequality of Lemma CHORD-BAND — a `nlinarith` in cos θ, sin θ with sin² + cos² = 1.)

**Remark (why the general tree is the wrong tool here).**  Theorem LOCAL (`local_certificate.md`) would
certify the same region through selections and tilt cells; Lemma RELAX's loss is the McCormick term
(q-range)·hw/2, so its radius is set by r·ρ — while S01-LINE has no tilt dependence at all.  The A116 tree is
run on the row N only as the frozen-chain cross-check (§3, [M]).

## 3. The certificate per frame [M, exact]

`attempts/A188-s01-basin/code/s01cert188.py` → `results/s01_basin.jsonl`: for each frame, each axis-parallel
line through a pin row / column (the k pins whose full-chord intervals meet), each tilt variant {any, ±10°,
±20°, ±30°}: the box set (4 − k free bands), the admissible c-interval (1/1000 inside the pins' full-chord
interval; the exact endpoint is minchord_box's degenerate-tilt limit case), and the exact rhs of LINE-2
checked at three c's.  **72 entries, 72 DEAD, rhs = −0.122916 = s0 − 4 exactly for k ≤ 2** (k = 3 lines,
the A144 node-level kill, need only chord > 0.877084 of the fourth square: band 0.2686 at any tilt, rhs
−2·10⁻⁵).  Per frame (the `any` variant; the band is ±0.207 across, whole container along, tilt free):

| frame | line | pins on it (k) | free boxes | c-interval |
|---|---|---|---|---|
| all three | y = c | BL(0,1) (1) | 3 | [1.008, 1.992] |
| all three | x = c | BL column: k5_11 / k5_16 {BL(0,0), BL(0,1), TL(0,0)} (3), trump5 {BL(0,0), BL(0,1)} (2) | 1 / 2 | [0.269, 0.992] / [0.207, 0.992] |
| all three | y = c | bottom row: k5_11 / trump5 {BL(0,0), BL(1,0), BR(0,0)} (3), k5_16 {BL(0,0), BR(0,0)} (2) | 1 / 2 | [0.269, 0.992] / [0.207, 0.992] |
| all three | y = c | top row: k5_11 {TL(0,0)} (1), k5_16 {TL(0,0), TR(0,0)} (2), trump5 {TR(0,0)} (1) | 3 / 2 / 3 | [2.885, 3.670] |
| k5_11, trump5 | x = c | BL(1,0) (1) | 3 | [1.008, 1.992] |
| all three | x = c | right column: k5_11 {BR(0,0)} (1), k5_16 / trump5 {BR(0,0), TR(0,0)} (2) | 3 / 2 | [2.885, 3.670] |
| any frame, k0_00 included | either | none (0) | 4 | [0.207, 3.670] |

**The frozen-chain cross-check** (`tree188.py`; A116's selection tree on the row N = frame pins + boxes of
radius r, tilt ±ρ around f1, f3, f4 of the representative dilated to s0): trump5 (0.1, 10°) DEAD, certified
minimum 3.883082 in 23 s / 5,823 nodes; the full (r, ρ) grid per frame and the t-emission through A133's
generator + independent checker are in `results/tree188_<frame>.jsonl` and `results/tcerts188.jsonl` (see the
A188 report and the registry row for the radii reached; refusals there are wall caps of the relaxation, the
LINE certificate above is the object).

## 4. The consumer [M]

`consumer188.py` → `results/consumer188.jsonl`, `results/consumed188.jsonl`.  For every alive page and every
pin line of its OWN record: is the page's conditioned box H a full member of some band (exact
minchord(H, l) ≥ 1 at an admissible c), i.e. does the YES leaf "H + (3 − k) other squares in the band" die by
S01-LINE; does A107's representative configuration have (4 − k) non-pin squares on the line; what fraction of
the LP dual support does.

| population | pages | H inside a certified band | on a k = 2 line (owes 1 box) | on a k = 1 line (owes 2) | dead outright (k = 3) | representative on the line |
|---|---|---|---|---|---|---|
| S01 | 23 | **15** | 1 | 14 | 0 | 8 |
| S03 | 11 | **10** | 0 | 10 | 0 | 1 |
| all alive | 63 | 37 | 1 | 36 | 0 | 12 |

[S] As A187 §5 says, containment is necessary, not sufficient: the YES leaf is dead, the NO children ("at most
3 − k − 1 other squares in the band") are LP nodes nobody has run.  **0 pages retired.**  [F] The eight S01
pages whose representative already carries four chords on one line (Y0952, Y0959, Y0147, Y0325, Y0308, Y0985,
…; `support_full` + k ≥ 4) are pages whose LP dual support IS an S01 configuration — the LP's inscribed cores do
not see the chord sum, which is A144's finding on Y0147 (τ 5.000 → 4.877 = 5 − (4 − s0) with the guard column
active, `certify.py` unable to express it).

## 5. The contract and what remains

* **The YES leaf** (LocalCompose, A126/A136 pattern): hypothesis = the page's pins + H + (3 − k) boxes
  b_j = [0, s] × [c − 0.207, c + 0.207] × [0°, 90°] (distinct witnesses); certificate = one entry of
  `results/s01_basin.jsonl` (exact rhs < 0) — checkable by `guardline.minchord_box` alone; no frozen verifier
  of the record has a field for it (A144 spec §3: the `guardlines` field of the v3 clause).
* **The NO side** is the whole price: per page (3 − k) LP children with a "≤ 2 − k other squares in the band"
  clause, or — equivalent and already built — A144's guard column on the same line, whose in-vitro re-solve
  moved Y0147's τ by exactly the S01 margin.  [C] Deploying A144 (the v3 `guardlines` clause + the column at
  emission) is what turns these 15 + 10 containments into kills; nothing in a tree does.
* **S03** (`notes/s03_identity.json`): s* = 3 + 2√2/3 = 3.942809, a KINK minimum of the corner-on-edge chain
  (two squares at exactly 45°, t = √2 − 1, wedged between an axis-aligned square and a corner cell), with
  distinct variants per frame (A107 minima: 2 in trump5, 3 in k5_16 groups); its basin is a Theorem-LOCAL
  object (A116 tree per variant), not a line — pilot in the A188 report, the rest [P].

## 6. Obligations ledger

| # | item | status |
|---|---|---|
| A188-O1 | S01 = the side-4 plateau; lock = four unit chords on one line; s_S01 = 4 exactly | [T] §1, [M] identity |
| A188-O2 | Lemma CHORD-BAND, γ(45°) = (√2 − 1)/2; Theorem S01-LINE (n-general) | [T] §2 |
| A188-O3 | the 72 exact certificates (all frames, all pin lines, four tilt variants) | [M] §3 |
| A188-O4 | frozen-chain cross-check (A116 tree, A133 t-emission + checker) on the row N | [M] §3 |
| A188-O5 | consumer on the 63 alive pages; the NO side named (A144 guard column) | [M] §4, [C] §5 |
| A188-O6 | S03 identified; its basin | [S] §5, [P] |
