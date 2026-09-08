# Agenda 030, lane A: Corner and wall structure

Retained planning-lane report for
[X-021](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md),
written by a Fable sub-agent at maximum effort on 2026-09-08 under BC-291 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md).
The report is reproduced as delivered, with its own status labels; X-021 carries the
coordinator’s reading of it.
Nothing here is a registered round or a new bound.

## A — Corner and wall structure of 11-square packings, 3.81 ≤ L ≤ U

Author: research-mathematician sub-agent, 2026-09-08. Repository read-only; all scripts
under `scratchpad/corner/`. Reference sides: `3.81`, `q = 96/25 = 3.84`,
`U = 3.877083590022814`.

**One-paragraph verdict.** X-019’s two elementary facts (four distinct corner blockers;
the identity `min_Q(x+y) = g_x + g_y + sin φ`) are correct as stated.
Beyond them, insertion saturation (IS) plus local geometry proves a handful of exact,
clean statements — an overhang strengthening that shrinks the forced corner box from
side 1 to side `κ = L − 2.96`, an exact corner-core lemma (every square meeting the
corner triangle `T_d` contains the box `[d,1]²`), which raises X-019’s uniqueness
threshold from `1/√2` to the sharp value `1`, the exact blocker-pose region, a
wall-service lemma, and monotonicity occupancy counts — but it proves **no positive
corner penetration** and **no angular restriction** on any blocker.
Both are refuted at the level of the *method*: Trump’s own fourth corner at `L = U` has
penetration `0.8445` and a free corner box of side `0.8317`, and Trump’s packing placed
in `[0,3.95]²` (where IS still holds) has a free corner box of side `0.9046` against a
forced box of side `0.99`. What the proved facts do buy is a **sound, complete,
implementable case cover of the corners by penetration depth** (Theorem B) and a
**corner-class certificate** (Theorem A) whose gain is a single LP away from being
measured.
The retained-certificate census in §2.6 already decides Theorem A negatively on
the retained `3.81` site set (the corner-region minimum equals the global minimum, so
the corner class can carry no surplus there) and shows that the corner-hugging
placements are uniformly the tightest constraints — which is exactly what Theorem B’s
banking credits and its domain clip deletes, so the sign of Theorem B’s gain is
undetermined without a run.

Notation. `C = [0,L]²`; `Q_1..Q_11` closed unit squares in `C`, pairwise disjoint
interiors. `S₁₂ = 99/25 = 3.96` (T-017). `κ := L − 2.96` (`0.85`, `0.88`, `0.9171` at
`3.81`, `3.84`, `U`). A *corner frame* is the D4 image putting a chosen corner at the
origin with `C` in the closed first quadrant.
In a corner frame a unit square has orientation `θ ∈ [−π/4, π/4]` (mod `π/2`), folded
angle `φ = |θ|`, axis-parallel extent `e = cos φ + sin φ ∈ [1, √2]`, half-extent
`h = e/2`, centre `(a,b)`, wall gaps `g_x = a − h ≥ 0`, `g_y = b − h ≥ 0`.
`T_ε := {x,y ≥ 0,
x + y ≤ ε}` (closed corner triangle), `K_ρ := (0,ρ)²` (open corner box),
`δ(Q) := min_{p∈Q}(x+y)` (penetration of `Q` toward the corner), `δ_j := min_i δ(Q_i)`
in corner `j`’s frame.

* * *

## 1. Results proved

### Lemma 0 (insertion saturation with overhang)

Let `d_1, d_2, d_3, d_4 ≥ 0` with `d_1 + d_2 ≤ S₁₂ − L` and `d_3 + d_4 ≤ S₁₂ − L`. Every
closed unit square `P ⊂ [−d_1, L + d_2] × [−d_3, L + d_4]` satisfies
`int P ∩ int Q_i ≠ ∅` for some `i`. Valid for every `L ≤ S₁₂`.

*Proof.* Translate everything by `(d_1, d_3)`. The container goes to
`[d_1, d_1+L] × [d_3, d_3+L] ⊂ [0, S₁₂]²` because `d_1 + L ≤ S₁₂ − d_2 ≤ S₁₂` (same in
`y`), and `P` goes to a subset of `[0, L + d_1 + d_2] × [0, L + d_3 + d_4] ⊂ [0, S₁₂]²`.
If `int P` met no `int Q_i`, the twelve translated closed unit squares would have
pairwise disjoint interiors inside `[0, S₁₂]²`, contradicting T-017. ∎

**Corollary 0.1.** (a) In every corner frame some `Q_i` has `int Q_i ∩ K_κ ≠ ∅` (take
`P = [−d, 1−d]²`, `d = S₁₂ − L`; then `int P ∩ int Q_i ⊂ (0, 1−d)² = K_κ`). (b) In every
wall frame and for every `t ∈ [0, L−1]` some `int Q_i` meets `(t, t+1) × (0, κ)`. (c)
Every unit square in `C` is met (X-019’s form, `d = 0`). Nothing else is gained: an
interior probe cannot overhang, and a probe overhanging one wall has exactly the trace
in (b).

*Remark.* This is the only place T-017’s margin `S₁₂ − L` enters; a proof of `s(12) = 4`
would give `κ = L − 3` (`0.84` at `3.84`). The corner box forced to be blocked shrinks
as the twelve-square bound improves, which is the correct direction.

### Lemma 1 (four distinct corner blockers — X-019, checked)

Choose for each corner `j` a square `B_j` with `int B_j ∩ K_κ^{(j)} ≠ ∅` (exists by
0.1(a)). Then `B_1, …, B_4` are pairwise distinct; indeed no square meets two corner
boxes.

*Proof.* A square meeting `K_κ^{(j)}` and `K_κ^{(j')}`, `j ≠ j'`, has in one coordinate
points `< κ` and `> L − κ`, so its extent `e > L − 2κ = 5.92 − L ≥ 2.04 > √2 ≥ e`. ∎
X-019’s version (`κ = 1`, gap `L − 2 > √2`) is also correct; there is no gap in its
argument.
With `κ` the blockers are forced *closer* to the corners, which is the point of
Lemma 0.

### Lemma 2 (corner penetration identity — X-019, checked, with the minimiser)

For a unit square with pose `(g_x, g_y, θ)` in a corner frame,
`min_{p∈Q}(x + y) = a + b − cos θ = g_x + g_y + sin φ`, attained at the lowest vertex
`(g_x + sin φ, g_y)` when `θ ≥ 0` and at the leftmost vertex `(g_x, g_y + sin φ)` when
`θ ≤ 0`; also `max_{p∈Q}(x+y) = a + b + cos θ`.

*Proof.* `x + y` is linear, so its extrema over `Q` are at the vertices
`c ± e_1/2 ± e_2/2`, `e_1 = (cos θ, sin θ)`, `e_2 = (−sin θ, cos θ)`, where it takes the
values `a + b + {−cos θ, −sin θ, sin θ, cos θ}`; on `[−π/4, π/4]`, `cos θ ≥ |sin θ|`, so
the minimum is `a + b − cos θ` at
`c − e_1/2 − e_2/2 = (a − (cos θ − sin θ)/2, b − (cos θ + sin θ)/2)`, which is
`(g_x + sin θ, g_y)` for `θ ≥ 0`. Substituting `a = g_x + h`, `b = g_y + h`,
`2h = cos φ + sin φ` gives `g_x + g_y + sin φ`. ∎ Hence `Q` meets `T_ε` iff
`g_x + g_y + sin φ ≤ ε`, which forces `φ ≤ arcsin ε` and `g_x + g_y ≤ ε − sin φ`
(X-019’s consequences, correct).
Numerical check: `lemmas_check.py` (1), max error `1.3e−15` over 20 000 random poses.

### Lemma 3 (corner core) — new

Let `0 ≤ d ≤ 1`. Every unit square `Q` in the closed quadrant that meets `T_d` contains
the closed box `[d, 1]²`. The box is exact: `⋂{Q : Q meets T_d} = [d,1]²`.

*Proof.* Reflecting in the diagonal fixes `T_d` and `[d,1]²`, so assume `θ ≥ 0`. With
the lowest vertex `v = (g_x + sin θ, g_y)`, `Q = {v + s e_1 + t e_2 : s, t ∈ [0,1]}`,
and for `p = (x,y)` the coordinates are `s = α cos θ + β sin θ`, `t = β cos θ − α sin θ`
with `α := x − g_x − sin θ`, `β := y − g_y`. The hypothesis is `g_x + g_y + sin θ ≤ d`.
For `(x,y) ∈ [d,1]²`: `α ≥ d − g_x − sin θ ≥ g_y ≥ 0` and
`β ≥ d − g_y ≥ g_x + sin θ ≥ sin θ ≥ 0`.
- `s ≥ 0`: both terms are nonnegative.
- `s ≤ 1`:
  `s ≤ (1 − g_x − sin θ) cos θ + (1 − g_y) sin θ = cos θ + sin θ − [g_x cos θ + g_y
  sin θ + sin θ cos θ] ≤ cos θ + sin θ − sin θ cos θ ≤ 1`, the last since
  `1 − cos θ − sin θ + sin θ cos θ = (1 − cos θ)(1 − sin θ) ≥ 0`.
- `t ≥ 0`: using `β ≥ g_x + sin θ` and `α ≤ 1 − g_x − sin θ`,
  `t ≥ (g_x + sin θ) cos θ − (1 − g_x − sin θ) sin θ = g_x (cos θ + sin θ) + sin θ (cos θ + sin θ − 1) ≥ 0`.
- `t ≤ 1`: `t ≤ β cos θ ≤ (1 − g_y) cos θ ≤ 1`. So `s, t ∈ [0,1]` and `p ∈ Q`.
  Exactness: the axis-parallel squares `[g, g+1] × [d−g, d−g+1]`, `g ∈ [0,d]`, all meet
  `T_d` (at `(g, d−g)`) and their intersection over `g` is `[d,1]²`. ∎

Numerical check: `common_core.py` (grid intersection against 121×181 poses per level)
returns a core of extent exactly `[d,1]²` and grid area `≈ (1−d)²` for
`d = 0.05, …, 0.6`, and the four corners of `[d,1]²` lie in every one of 721×61 boundary
poses.

*Lemma 3′ (closed-square Stromquist Lemma 1, for reference).* If `Q` lies in the
quadrant and its centre is in `[0,α] × [0,β]` with `α, β ≤ 1`, then `(α, β) ∈ Q`. Proof:
`(α − a, β − b) ∈
[0, 1−h]²`; its square-frame coordinates are
`u ∈ [0, (1−h)(cos θ + sin θ)] = [0, 2h(1−h)] ⊂
[0, ½]` and `v ∈ [−(1−h) sin θ, (1−h) cos θ]`, and
`(1−h) cos θ ≤ ½ ⇔ (1 − cos θ)² + sin θ cos θ ≥ 0`. ∎ (Checked: 0 violations in 200 000
random poses, `lemmas_check.py` (3).)

### Lemma 4 (uniqueness of the corner occupant, sharp threshold 1) — improves X-019

For `ε < 1` at most one packed square meets `T_ε`; occupants of `T_ε` at different
corners are distinct for every `ε ≤ 1`. The threshold is sharp: `[0,1]×[1,2]` and
`[1,2]×[0,1]` both meet `T_1` with disjoint interiors.

*Proof.* Two occupants both contain `[ε,1]²` (Lemma 3), a box with nonempty interior;
for convex bodies `int(Q_1 ∩ Q_2) = int Q_1 ∩ int Q_2`, so their interiors meet.
Distinctness across corners: a square meeting `T_ε` at two corners has extent
`> L − 2ε ≥ L − 2 > √2`. ∎ X-019’s argument (centres in a triangle of diameter `√2 ε`,
incircles of radius ½) is correct but gives only `ε < 1/√2`. The global search
`two_occupants.py` (12 differential-evolution restarts + Nelder–Mead polish over both
poses) finds the minimum of `max(δ(Q_1), δ(Q_2))` over disjoint pairs to be `1.0000000`
at exactly the sharp configuration.

### Lemma 5 (exact blocker-pose region) — new

In a corner frame with `θ ≥ 0`, put `m(Q) := min_{p∈Q} max(x,y)` and
`t* := (g_y + cos φ − g_x)/(sin φ + cos φ)`. Then `int Q ∩ K_ρ ≠ ∅ ⇔ m(Q) < ρ`, and
```
m(Q) = (g_x cos φ + g_y sin φ + sin φ cos φ)/(sin φ + cos φ)   if t* ∈ [0,1]
     = max(g_x, g_y + cos φ)                                   if t* < 0
     = max(g_x + sin φ, g_y)                                   if t* > 1 .
```
(For `θ ≤ 0` swap the roles of `x` and `y`.)

*Proof.* `int Q ⊂ (0,∞)²`, so `int Q` meets `K_ρ` iff some point of `Q` has
`max(x,y) < ρ` (interior points of `Q` near it do too).
For the formula: for heights `y ∈ [g_y, g_y + cos φ]` the leftmost point of `Q` at
height `y` lies on the edge `E` from the leftmost vertex `(g_x, g_y + cos φ)` to the
lowest vertex `(g_x + sin φ, g_y)`, so every `p ∈ Q` at such a height has `max(x,y) ≥`
the value on `E` at that height; for `y > g_y + cos φ`, `max(x,y) ≥ y >
max(g_x, g_y + cos φ)`, the value at the top of `E`. So `m(Q) = min_E max(x,y)`. Along
`E`, `(x,y) = (g_x + t sin φ, g_y + (1−t) cos φ)`, `x` increasing and `y` decreasing, so
`max(x,y)` is minimised where `x = y` (`t = t*`) if `t* ∈ [0,1]` and at the appropriate
endpoint otherwise.
∎ (`lemmas_check.py` (5): 0 mismatches against the SAT test in 50 000
random poses.)

**Corollaries.** (i) Every *snug* square (`g_x = g_y = 0`) at any angle blocks `K_κ`:
`m = sin φ cos φ/(sin φ + cos φ) ≤ 1/(2√2) < κ`. (ii) An axis-aligned blocker has
`g_x, g_y < κ`. (iii) A `45°` blocker has `(g_x + g_y)/2 + 1/(2√2) < κ`, i.e.
`g_x + g_y < 0.993 / 1.053 / 1.127` at `3.81 / 3.84 / U`. (iv) Every blocker of `K_κ`
has penetration `δ(Q) ≤ 2 m(Q) < 2κ` (the minimising point `p*` has
`x + y ≤ 2 max(x,y)`), i.e. `δ < 1.70 / 1.76 / 1.834`. (v) A blocker with `δ ≤ 1` has
`φ ≤ arcsin δ` (Lemma 2); a blocker with `δ ∈ (1, 2κ)` is unrestricted in angle.

### Lemma 6 (occupancy from monotonicity) — elementary, new in this form

For `w ≥ 0` and `k` with `L − 2w < s(k)`: at most `k − 1` squares are contained in the
closed central box `[w, L−w]²`, so at least `12 − k` meet the open annulus
`C \ [w, L−w]²`. In a corner frame, for `L − w < s(k)`: at most `k − 1` squares are
contained in `[w, L]²`, so at least `12 − k` meet the open corner L-strip
`{x < w} ∪ {y < w}`. *Proof.* A square not meeting the open annulus lies in the closed
central square of side `L − 2w < s(k)`, which by definition of `s(k)` cannot hold `k`
unit squares. Same for the corner L-strip.
∎ With `s(2) = 2`, `s(5) = 2 + 1/√2`, `s(6) = 3`, `s(10) = 3 + 1/√2`, `s(11) ≥ 3.810025`
(`thresholds.py`):

| at side | ≥10 squares meet the annulus / corner L-strip of width > | ≥7 for width > | ≥6 for width > | ≥2 for width > | ≥1 for width > |
| --- | --- | --- | --- | --- | --- |
| 3.81 | 0.905 / 1.810 | 0.551 / 1.103 | 0.405 / 0.810 | 0.051 / 0.103 | 0 / 0 |
| 3.84 | 0.920 / 1.840 | 0.566 / 1.133 | 0.420 / 0.840 | 0.066 / 0.133 | 0.015 / 0.030 |
| U | 0.9385 / 1.877 | 0.585 / 1.170 | 0.4385 / 0.877 | 0.085 / 0.170 | 0.0335 / 0.067 |

Trump check (`trump_structure.py`, `trump_more.py`): squares contained in `[w, S−w]²`
are `{6, 8, 9}` for every `w ≤ 0.5` and `{8}` for `0.585 ≤ w < 1` (bounds `≤ 5`, `≤ 4`,
`≤ 1`: satisfied); the bottom-right corner L-strip at `w = 1.17` (box side
`2.7071 = s(5)`) is avoided by exactly `4 = k−1` squares (`{3,4,5,8}`), so the corner
form is **tight** on Trump.

### Lemma 7 (wall service) — new

Fix a wall frame, `W := (0,L) × (0,κ)`, `𝒮 := {i : int Q_i ∩ W ≠ ∅}`, and traces
`τ_i := π_x(int Q_i ∩ W)` (open intervals).
(a) Every closed interval `[t, t+1] ⊂ [0,L]` meets some `τ_i`; in particular `|𝒮| ≥ 2`.
(b) If `|𝒮| = 2` then `𝒮 = {B, B'}` are the two corner blockers of this wall and
`g(B) + e(B) + 1 + g(B') + e(B') > L`, with `g(B)` the gap of `B` to the left side wall,
`g(B')` that of `B'` to the right side wall, `e = cos φ + sin φ`. Consequences: two
axis-aligned blockers alone need `g(B) + g(B') > L − 3 ≥ 0.81`; two snug `45°` blockers
alone need `L < 1 + 2√2 = 3.8284`, so for `L ≥ 3.8284` (all of `[3.8284, U]`, in
particular `3.84`) a third square meets `W`; if both blockers meet `T_ε` with
`ε ≤ 0.214`, a third square meets `W` for every `L ≥ 3.81` (the threshold solves
`1 + 4ε + 2√(1−ε²) = 3.81`; it is `0.2225` at `3.84` and `0.2330` at `U`).

*Proof.* (a) is Corollary 0.1(b). (b) `B ∈ 𝒮` because `int B ∩ K_κ ≠ ∅` and `K_κ ⊂ W`;
same for `B'`; they are distinct (Lemma 1). If `𝒮 = {B, B'}`:
`τ_B ⊂ (g(B), g(B) + e(B))` and `τ_{B'} ⊂ (L − g(B') − e(B'), L)`. Put
`t := min(g(B) + e(B), L − 1) ≥ 0`. `[t, t+1]` misses `τ_B`, so it meets `τ_{B'}`:
`t + 1 > L − g(B') − e(B')`. If `t = g(B) + e(B)` this is the claim; if `t = L − 1` then
`g(B) + e(B) ≥ L − 1` and the claim holds a fortiori.
For the `T_ε` corollary use `g ≤ ε`, `sin φ ≤ ε`, `e ≤ ε + √(1 − ε²)`. ∎ Trump check
(`trump_more.py`): on every wall the two-blocker sum is `3.000` (three walls) or `3.845`
(top wall, `B = sq2` with gap `0.8445`) against `L = 3.877`, so a third square is forced
on each wall; Trump has 4–5 serving squares per wall.

### Theorem A (corner-class certificate; sound, unrun)

Let `R_κ` be the set of admissible unit-square placements `Q ⊂ C` with
`int Q ∩ K_κ^{(j)} ≠ ∅` for some corner `j` (`R_κ` is D4-invariant; membership is
decided by Lemma 5). Let `μ` be a nonnegative atom measure on `C` satisfying Conditions
1–4 of the retained certificate format for `(B, net)`, let `w_c ≥ w_f ≥ 0`, and suppose
(1) every admissible core `P` (a `B`-square at a net direction) that lies inside some
placement `Q ∈ R_κ` has `μ(P) ≥ w_c`; (2) every admissible core has `μ(P) ≥ w_f`; (3)
`μ(C) < 4 w_c + 7 w_f`. Then eleven unit squares do not pack in `[0,L]²`.

*Proof.* By Lemma 1 the four blockers are distinct squares in `R_κ`; their cores
(Condition 4) are cores inside placements in `R_κ`, so each has mass `≥ w_c`; the other
seven have mass `≥ w_f`; the eleven cores are pairwise disjoint, so
`4 w_c + 7 w_f ≤ μ(C)`. ∎ *Implementation note.* Imposing (1) on a superset of the true
core set is safe. A cheap safe superset: cores whose centre is within `1/√2` of some
`K_κ^{(j)}` (every unit square is inside the disk of radius `1/√2` about its centre).
The LP is X-014 Lemma 3’s with a region class instead of an angle class: variables
`(μ, w_c, w_f)`, homogeneous objective `μ(C) − 4 w_c − 7 w_f`, normalise `w_f = 1`.
Because `R_κ` is D4-invariant the folded solver applies unchanged; only the row
generator needs the region predicate.
A gain exists iff the optimum is negative.

### Theorem B (complete corner cover by penetration depth; sound, unrun)

Fix thresholds `0 < d_1 < ⋯ < d_m ≤ 1`. For each corner `j`, `δ_j ∈ [0, 2κ)` (Lemma
5(iv)); bin it into `[0, d_1], (d_1, d_2], …, (d_{m−1}, d_m], (d_m, 2κ)`. For a bin
vector `σ`:
- if `δ_j ≤ d_k` (bin `≤ k`): a **unique** square `O_j` meets `T_{d_k}` (Lemma 4,
  `d_k ≤ 1`; for `d_k = 1` uniqueness may fail and one uses any occupant),
  `O_j ⊇ [d_k, 1]²` in corner `j`’s frame (Lemma 3), `φ(O_j) ≤ arcsin d_k`, and every
  other square is disjoint from `int O_j`;
- if `δ_j > d_{k−1}` (bin `≥ k`): the closed triangle `T_{d_{k−1}}` meets no square.

*Case certificate.* Let `I ⊆ {1..4}` be the corners banked in case `σ` with boxes
`X_j = [d_{k_j}, 1]²_j`, and let `X'_j ⊂ X_j` be a box provably inside every admissible
core of every occupant of `T_{d_{k_j}}` (the core is the concentric `B`-square at the
nearest net direction; it contains the occupant shrunk about its centre by
`β = B/(cos δ + sin δ)`, `δ` the half-gap, so `X'_j = [d + η, 1 − η]²` with
`η = (1 − β) · 1.42 ≈ 0.005` suffices, since an occupant’s centre has coordinates
`≤ d + 0.707 < 1.42`). Let `D_σ` be the admissible domain: cores whose enclosing unit
square avoids every free triangle of `σ` — per direction this is the rotated-container
centre domain cut by the half-planes `a + b > d + cos θ` (one per free corner, Lemma 2),
hence **convex**, so `sweep.centre_domain` needs only a clip, not a new engine.
If a nonnegative atom measure `μ` satisfies (1) every core in `D_σ` disjoint from all
`X_j`, `j ∈ I`, has `μ ≥ 1`, and (2) `μ(C) − Σ_{j∈I} μ(X'_j) < 11 − |I|`, then no
packing lies in case `σ`. *Proof.* The `11 − |I|` non-occupants have cores in `D_σ`
disjoint from each `O_j ⊇ X_j`, hence of mass `≥ 1`; each occupant’s core contains
`X'_j`; all eleven cores are disjoint, so `Σ_{j∈I} μ(X'_j) + (11 − |I|) ≤ μ(C)`. ∎ The
cases are exhaustive and pairwise disjoint by construction (each `δ_j` is in exactly one
bin), D4 acts on bin vectors, and the all-top-bin case with `m = 0` is the unconditional
certificate. The extreme cases are named for §4: **flush-four** (`I = {1,2,3,4}`, `d_1`
small: seven cores in `C` minus four near-unit corner boxes), **three-plus-one**
(Trump’s pattern: three banked corners and one corner in a deep bin `δ ≥ 0.7`),
**octagon** (all four corners in the top bin: eleven squares avoiding four `T_d`).

### Summary of what is *not* proved (see §3)

No lower bound on `δ_j`, no lower bound on any corner-box overlap, no upper bound on the
distance from a container corner to the nearest square vertex, no restriction of any
blocker’s angle beyond Lemma 5(v), no lower bound on the area of squares inside a wall
strip.
Each is false at `L = U` for Trump’s fourth corner or is refuted for the method by
the loosened Trump witness.

* * *

## 2. Numerical checks (scripts in `scratchpad/corner/`)

All scripts run with `packing/.venv/bin/python3` (3.14, numpy/scipy/mpmath); `geom.py`
holds the SAT helpers, `trump_pose.py` reconstructs Trump’s pose from
`cases/trump11/packing.py`’s closed forms (root `u = 0.36576930760467729…` of
`U_MIN_POLY`, `a = 40.18193729032972°`, `s = 3.877083590022814177…`, matching the record
to all printed digits).

### 2.1 Trump’s packing is valid and its corners are as claimed (`trump_structure.py`)

All 11 squares contained; least pairwise SAT separation `−2.2e−16` (touching).
Corner data:

| corner | `δ_j` | attained by | blockers of `K_1` / `K_κ` / `K_{0.5}` | largest free axis box `[0,a]²` | nearest vertex |
| --- | --- | --- | --- | --- | --- |
| BL `(0,0)` | 0 | sq0 | {0} / {0} / {0} | 0 | 0 |
| BR `(S,0)` | 0 | sq1 | {1} / {1} / {1} | 0 | 0 |
| **TR `(S,S)`** | **0.844525** | sq2 | {2,10} / {2,10} / **∅** | **0.831679** | **0.844525** |
| TL `(0,S)` | 0 | sq3 | {3} / {3} / {3} | 0 | 0 |

At the TR corner sq2 is axis-aligned, flush to the top wall, at gap `0.8445` from the
right wall (`δ = 0.8445 + 0 + 0`); sq10 is tilted `40.18°`, flush to the right wall,
with `δ = 0 + 0.8317 +
sin 40.18° = 1.4769`. Both meet `K_κ` (`κ = 0.9171`); sq2’s overlap with the forced box
is a strip of width `0.9171 − 0.8445 = 0.073`. Trump’s fourth corner is therefore an
actual packing at side `U` in which the corner box of side `0.8317` is entirely free.

Wall strips: squares meeting the open strip of width `w` are, for every `w ≤ 0.5`:
bottom `{0,1,7}`, right `{1,10}`, top `{2,3,4}`, left `{0,3,5}`; at `w = κ`: bottom
`{0,1,6,7,9}`, right `{1,2,9,10}`, top `{2,3,4,10}`, left `{0,3,5,6}`. The centre
`(1.9385, 1.9385)` lies in sq8 (distance 0); the next nearest squares are sq6, sq9 at
`0.3226`.

### 2.2 Loosened Trump: the method-level witness (`loosened_trump.py`)

Trump’s packing point-reflected (TR corner to BL) and translated into `[0, L']²`,
verified valid at each `L'`:

| `L'` | `κ(L')` | blockers of `K_κ` | free axis box `a` | free triangle `ε` | nearest vertex |
| --- | --- | --- | --- | --- | --- |
| `U` | 0.9171 | {2,10} | 0.8317 | 0.8445 | 0.8445 |
| 3.90 | 0.9400 | {2,10} | 0.8546 | 0.8904 | 0.8677 |
| 3.95 | 0.9900 | {2,10} | 0.9046 | 0.9904 | 0.9203 |
| 3.9599 | 0.9999 | {2,10} | 0.9145 | 1.0102 | 0.9310 |

IS holds at every `L' < 3.96`. So an argument that used only IS and geometry valid for
all `L ≤ 3.96` cannot prove that any corner box of side `< 0.9046` is met, that `T_ε` is
occupied for any `ε < 0.99`, or that a vertex lies within `0.92` of every corner: at
`L' = 3.95` the forced box has side `0.99` and the free box has side `0.9046`, a margin
of `0.085`.

### 2.3 Lemma checks (`lemmas_check.py`)

(1) identity error `1.3e−15`; (2) `min_θ max_{p∈Q_snug} min(x,y) = 1.0` exactly (every
unit square in the quadrant reaches the closed quadrant `[1,∞)²`, which is why an
L-shaped free region with arms of width `< 1` never admits a probe); (3) Lemma 3′: 0
violations / 200 000; (4) the snug diamond has `δ = 0.70711`, touches both walls, and
meets `K_ρ` for every `ρ ≥ 0.7072` including `κ`; (5) Lemma 5 formula vs SAT: 0
mismatches / 50 000; (6) wall-service thresholds as quoted in Lemma 7.

### 2.4 Two occupants (`two_occupants.py`)

Global minimisation of `max(δ(Q_1), δ(Q_2))` over disjoint pairs in the quadrant:
optimum `1.0000000000` at `Q_1 = [0,1]×[1,2]`, `Q_2 = [1,2]×[0,1]` (separation
`8.9e−16`, centre distance `√2`). Consistent with Lemma 4 (`ε* = 1`) and shows X-019’s
`1/√2` was not sharp.

### 2.5 Common core (`common_core.py`)

For `d ∈ {0.05, …, 0.6}` the grid intersection of all corner-occupant squares has extent
exactly `[d,1]²` and area `≈ (1−d)²` (0.912, 0.819, 0.648, 0.497, 0.366, 0.255, 0.164),
confirming Lemma 3’s exactness numerically.

### 2.6 Where the retained 3.81 certificate is tight, by geometric class (`cert_readout.py`)

Readout of the repository’s own exact integer mass grid
(`sqpack.fractional.sweep.scaled_mass_grid`) over all 181 net directions of
`certificate.json` (1121 atoms, `B = 0.9977`, least cell mass `4001/4000`). Each
reachable event cell is classified by its midpoint centre and the concentric unit square
at the net direction (a readout, not proof-grade class membership): meets some `K_κ`
(`κ = 0.85`), meets some `K_1`, meets some `T_ε`, or is contained in the central box
`[w, L−w]²`. Result (all 181 directions, 567 130 649 reachable cells):

| class of cell (unit square at net direction) | cells | min mass | ≤ 1.005 | ≤ 1.02 | ≤ 1.05 | ≤ 1.1 |
| --- | --- | --- | --- | --- | --- | --- |
| all | 567 130 649 | **1.000250** | 2 452 476 | 10 184 524 | 23 112 904 | 50 583 976 |
| meets some `K_κ`, `κ = 0.85` | 137 377 014 | **1.000250** | 515 316 | 2 372 106 | 7 430 402 | 17 776 302 |
| meets some `K_1` | 262 639 348 | 1.000250 | 680 710 | 3 219 076 | 9 896 686 | 23 498 814 |
| meets some `T_0.05` | 2 808 | 1.000250 | **2 808** | 2 808 | 2 808 | 2 808 |
| meets some `T_0.1` | 21 176 | 1.000250 | **21 176** | 21 176 | 21 176 | 21 176 |
| meets some `T_0.2` | 85 036 | 1.000250 | **85 036** | 85 036 | 85 036 | 85 036 |
| meets some `T_0.3` | 364 940 | 1.000250 | 251 216 | 364 940 | 364 940 | 364 940 |
| meets some `T_0.5` | 2 606 880 | 1.000250 | 441 368 | 1 741 508 | 1 988 156 | 2 606 880 |
| meets some `T_0.7` | 9 989 324 | 1.000250 | 488 596 | 2 154 068 | 3 727 136 | 7 082 184 |
| contained in `[0.5, L−0.5]²` | 290 567 277 | 1.000295 | 1 092 912 | 3 458 892 | 5 870 156 | 14 716 684 |
| contained in `[0.9, L−0.9]²` | 79 033 300 | 1.000295 | 1 086 792 | 3 411 456 | 5 164 280 | 9 287 284 |

Reading. (i) The global minimum `4001/4000` is attained inside every corner class, so on
this site set the corner-class weight of Theorem A is forced to `w_c = 1`: **no headroom
from over-covering the corner region here.** (ii) Every placement whose square meets
`T_0.2` — all 85 036 cells, at every direction — is within `0.005` of tight, and those
meeting `T_0.3` within `0.02`: the certificate spends *exactly* one unit of mass per
corner, positioned so that any near-flush square captures barely `1`. (iii) Tight cells
are not concentrated in the corners relative to their share (the `κ`-corner class holds
24 % of all cells and 21 % of the `≤ 1.005` cells); the certificate is tight
“everywhere”, as complementary slackness predicts for an optimised dual.
Consequence for Theorem B: a banked corner credits precisely the mass that these
uniformly tight corner-hugging cells were capturing, and the clip in a deep-avoidance
branch deletes precisely these tightest constraints — so both branches remove the
binding cells, and whether the LP re-optimises to a lower total is exactly the question
S2/S3 must run. Nothing in this readout predicts the sign of that gain.

### 2.7 Local probe-freeness of the corner alternatives (`local_probe.py`)

With a single blocker present, maximise the SAT separation of a unit probe `P ⊂ [0,W]²`
from the blocker (six DE restarts; a negative maximum means every probe in the window
overlaps the blocker’s interior).
Window `W = 2`: near-miss axis blocker `[0.87, 1.87]²` → `−0.130`; snug `45°` diamond →
`−0.086`; snug `22.5°` square → `−0.047`; flush control `[0,1]²` → `0.000` (the probe
`[1,2]²` touches, which is legal).
So no probe fits anywhere near the corner in any of the three alternatives; in `W = 2.2`
probes appear only at `(1.7, 1.7)`, i.e. away from the corner, where a real packing’s
other squares block them.
This is the precise sense in which the alternatives are “locally IS-consistent”; it is
not a packing witness (only the near-miss alternative has one, §2.2).

* * *

## 3. Obstructions — what does not work, and why

**O1. No positive corner penetration is forced.** Neither `δ_j ≤ ε` for some `ε < 2κ`,
nor a lower bound on the overlap of a blocker with `K_κ`, nor a vertex within distance
`d` of the corner, follows from IS + geometry.
Three independent refutations: (i) *at `L = U`*, Trump’s TR corner (§2.1): `δ = 0.8445`,
free box `0.8317`, nearest vertex `0.8445` — so every candidate of the form “each corner
has `δ_j ≤ ε`” with `ε < 0.8445`, “each corner box `[0,a]²` is met” with `a ≤ 0.8317`,
or “a vertex within `d < 0.8445` of each corner” is **false at `L = U`**, hence at best
true strictly below `U`, out of reach of any argument valid up to `U`; (ii) *for the
method*, §2.2: at `3.95` IS holds and the free box is `0.9046` against the forced
`0.99`; (iii) *locally*, the near-miss blocker `[κ−η, κ−η+1]²` leaves `[0, κ−η]²` free
and, by §2.3(2) and §2.7, no probe fits in the L-region `{min(x,y) < κ−η}` nor anywhere
in the `[0,2]²` corner window; the remaining probes are blocked elsewhere by other
squares. The sharpest true statement is Lemma 5(iv): `δ_j < 2κ`.

**O2. No angular restriction on blockers.** Lemma 5(i): every snug square of every angle
blocks `K_κ`; so “some/at least two/at least three blockers within `δ` of `0°` or `45°`”
is unprovable by these means.
The snug-`22.5°` corner square admits no probe in the `[0,2]²` window (§2.7), so it is
IS-consistent locally like the diamond and the near-miss square.
The only proved angle information is conditional on depth (`φ ≤ arcsin δ_j` for the
unique occupant when `δ_j ≤ 1`). Trump has all four blockers axis-aligned, so “all
blockers axis-aligned” is true at `U` for the only known packing and unreachable by the
method (the `45°` snug diamond alternative is not refuted: it blocks `K_κ`, avoids `T_ε`
for all `ε < 0.7071`, and no probe fits near it — §2.3(4)). I could not build a full
packing at side `≤ 3.96` with a corner diamond; that alternative is therefore “not
refuted, not realised” (Stromquist’s `0/45` optimum at `3.8856 <
3.96` exists but its corner structure was not reconstructed here).

**O3. Wall strips: IS forces occupancy, not area.** Corollary 0.1(b) makes the width-`κ`
strip a 1-net (Lemma 7) but a strip of width `κ − η` can be free of every square as far
as probes are concerned (no unit square fits in a strip of width `< 1`). Area alone
excludes a free width-1 strip only for `L(L−1) < 11`, i.e. `L < 3.854`
(`thresholds.py`): at `U` even the area argument allows it.
Monotonicity (Lemma 6) supplies counts for the *annulus* and the *corner L-strip*
because those complements are squares; a single-wall strip’s complement is an
`L × (L−w)` rectangle, for which no capacity theorem is on record here (see S3).

**O4. The centre.** The central unit probe (and its rotations) is met, but a single
square can meet all of them (Trump’s sq8 contains the centre).
A pinwheel of four unit squares around a square hole of side `w < 1` is IS-consistent,
and a free disk of radius `< 1/√2` around the centre is IS-consistent; the strongest
consequence is that some square’s interior meets the open disk of radius `1/√2` about
the centre (trivial: the closed disk contains the axis probe).
So “forced occupancy of the central region” is vacuous beyond “not a unit-square hole”.

**O5. What IS cannot add to the covering LP.** Every unconditional point/measure lemma
(Stromquist’s Lemmas 1–4, Lemma 3′ here) is already priced by the unconditional covering
LP; the plateau at `3.82` is the LP’s value, not a missing lemma.
IS-derived structure helps only through (a) a case split with a *convex* domain clip and
*banked* boxes (Theorem B) or (b) a class count (Theorem A, Lemma 6 annulus classes).
Both are LPs the current code almost runs; neither has a provable gain without running
it.

**O6. Lemma 7 does not compound.** A third serving square can be shared by two adjacent
walls (a diamond with the edge `x + y = 2` wrapping the flush corner square’s outer
vertex serves both strips without meeting `K_κ`), so “third square per wall” yields only
two additional distinct squares (opposite walls), not four.

* * *

## 4. Proposed research sessions (each 2–4 h, parallelisable)

### S1 — Corner-class LP (Theorem A) at 3.82 and 3.84

- **Question.** Is the optimum of `min μ(C) − 4 w_c − 7 w_f` (with `w_f = 1`, `μ ≥ 0`,
  corner-region cores `≥ w_c`, all cores `≥ 1`) negative at `3.82`, and at `3.84`?
- **Entry.** `classcert.py`’s two-threshold LP; a region predicate for cores (safe
  superset: core centre within `1/√2` of a `K_κ`, or the exact Lemma 5 test on the union
  of the cell’s angles); D4-folded site sets from the `3.82` runs (grid-built and
  atom-seeded) if retrievable, else the `3.81` atoms scaled.
- **Instrument.** The existing column-generation loop with one extra row class; exact
  decision by the sweep restricted to the region (the region is a union of event cells
  per direction only approximately — decide on a superset of cells, which is safe).
- **Falsifier.** Optimum `≥ 0` on a converged site set at `3.82`; more sharply, the
  §2.6-style census showing tight cells inside `R_κ` (then `w_c = 1` is forced and the
  gain is zero).
- **Exit.** A certificate at `3.82` (a new rung — moves `s(11)`) or a scoped
  obstruction: “on site sets X, Y the corner class carries no surplus; tight corner
  cells listed”.
- **Hours.** 2–3. **Headroom mechanism.** Four identified squares must sit in a small
  D4-symmetric region; the certificate may over-cover that region at a cost lower than
  `4(w_c − 1)`. This is the cheapest test of whether *any* corner information has value.
  **Dependencies.** None.
  **Parallel.** Yes, with S2–S4.

### S2 — Flush-four and three-plus-one branches of Theorem B at 3.84

- **Question.** With `d_1 = 0.05`: (a) does a measure exist with
  `μ(C) − Σ_{j=1..4} μ(X'_j) < 7` covering every core disjoint from the four boxes
  `[0.05, 1]²_j` (flush-four)?
  (b) with three boxes banked and the fourth corner in the bin `δ ≥ 0.7` (free
  `T_{0.7}`), does the LP fall below `8` (three-plus-one, Trump’s pattern)?
- **Entry.** `sweep.centre_domain` extended by half-plane clips (`a + b > d + cos θ` per
  free corner; convexity preserved) and a “banked box” exclusion in the row generator
  (cores meeting a banked box are not constrained); objective with the `μ(X'_j)` credits
  (`X'_j = [d+0.005,
  0.995]²`). The T-018 pipeline otherwise unchanged; the net must span a quarter turn if
  the case breaks D4 (three-plus-one does; flush-four does not).
- **Instrument.** Column generation + exact sweep on the clipped domain; independent
  replay by the interval route.
- **Falsifier.** LP value `≥ 7` (resp.
  `≥ 8`) on a converged site set — then the case cannot be closed by this measure family
  at `3.84`; report the tight cells.
- **Exit.** A verified case certificate with its complement (the other bin vectors)
  listed, or an exact obstruction naming the residual region’s covering value.
- **Hours.** 3–4. **Headroom mechanism.** Banking relocates up to one unit of mass per
  corner into a box no other square can enter, and the domain clip deletes
  corner-hugging placements; the residual-seven problem is a covering problem for seven
  squares in a plus-shaped region of area `≈ 10.7`, where the certificate no longer pays
  for four corners. **Dependencies.** None (a small code extension, not a new engine).
  **Parallel.** Yes.

### S3 — Deep-avoidance branch: octagon and single-diamond corners

- **Question.** For `d = 0.6` (and `0.7`): (a) does the unconditional LP on the octagon
  `C` minus four `T_d` (all corners in the top bin) fall below `11` at `3.84`? (b) for
  one corner in the top bin and the other three unconstrained, below `11`? (c) does
  banking the box `[0.354, 1.06]²` (contained in every snug `45°` corner square) plus
  free `T_{0.7}` close the “snug diamond corner” case at `3.84`?
- **Entry.** S2’s domain clip; nothing else.
- **Instrument.** As S2. **Falsifier.** LP value `≥ 11` (resp.
  `≥ 10` for (c)) on a converged site set.
  **Exit.** Certificate or obstruction per sub-case; for (a)/(b) the *side* at which the
  clipped LP first drops below `11` is itself a useful number (how much a deep-avoided
  corner costs a packing).
  **Hours.** 2–3. **Headroom mechanism.** Deleting `T_d` removes exactly the placements
  that force mass into the corner point region; if those were the binding cells at
  `3.82`, the plateau moves.
  **Dependencies.** Shares S2’s clip.
  **Parallel.** Yes.

### S4 — Adversarial witnesses for the corner alternatives

- **Question.** Does a packing of eleven unit squares at side `≤ 3.96` exist with (a) a
  snug `45°` corner square, (b) all four corners with `δ_j ≥ 0.5`, (c) a corner blocker
  at `22.5°`? Each found witness refutes the corresponding Theorem B branch *as a method
  target at that side* and calibrates how far above `U` the branch is closable.
- **Entry.** Stromquist’s Theorem 3 packing (`3.8856`, all angles `0/45`) reconstructed
  from the literature or by search; a numerical packing search (penalty method / the
  atlas tools) seeded by Trump’s pose, Hamalainen’s pose, and the loosened Trump family
  of §2.2.
- **Instrument.** Float search + exact SAT verification of any candidate
  (`sqpack.verify`).
- **Falsifier.** None in the logical sense (failure to find proves nothing); a found
  witness is decisive.
  **Exit.** Exact witnesses with their corner data, or a scoped “no witness found below
  side X in Y minutes” note.
  **Hours.** 2. **Headroom mechanism.** Negative: tells S2/S3 which branches cannot
  close at which sides.
  **Dependencies.** None.
  **Parallel.** Yes.

### S5 (optional) — Rectangle capacity `11 ∉ L × (L − w)`

- **Question.** For `L = 3.84`, the largest `w` with a certificate that eleven unit
  squares do not pack in an `L × (L−w)` rectangle (would prove every wall strip of width
  `w` is met by a square, strengthening O3 beyond area’s `w ≤ 0.975`).
- **Instrument.** The T-018 pipeline with a rectangular container (the centre domain is
  a rotated rectangle; convex).
  **Falsifier.** LP `≥ 11` at `w = 0.5`. **Hours.** 2. **Value.** Low for `3.84`
  directly (a strip class adds only two forced squares), higher as a reusable capacity
  tool. **Parallel.** Yes.

* * *

## 5. Open questions, ranked by expected value

1. **Does the `3.82` plateau measure over-cover the corner region?** On the retained
   `3.81` atoms the answer is no (§2.6: corner minimum = global minimum), so Theorem A
   is dead unless the LP, re-solved with the corner class as a variable threshold, moves
   mass into the corners at a cost below `4(w_c − 1)`; S1 should be run once as that LP
   and then dropped if the optimum is `≥ 0`. Corner conditioning otherwise goes through
   Theorem B’s banking (S2/S3).
2. **Value of the flush-four residual-seven LP at `3.84`** (S2a). This is the branch
   where all the mass mechanisms act at once; a value below `7` would be the first
   conditional exclusion with a named complement.
3. **How much does a deep-avoided corner cost?** The side at which the octagon-clipped
   LP first drops below `11` (S3a) is a quantitative “corner tax” — a number no current
   record has.
4. **Is a snug-diamond corner realisable at side `≤ 3.96`?** (S4a) It is the one
   alternative in O2 that is neither refuted nor realised; a witness would kill the
   diamond branch as a target near `U`, and its absence after a real search would raise
   the priority of S3c.
5. **Sharpen Lemma 7 to a per-wall third-square theorem under weak angle hypotheses**
   (e.g. both blockers within `20°` of axis), and combine with Lemma 6 into a
   wall/annulus class certificate.
   Small expected gain; cheap.
6. **Exact `s(12) = 4` (or any improvement of `3.96`)** shrinks `κ` toward `L − 3`; the
   corner data of Trump (`0.8445` gap, `0.073` overlap with `K_κ` at `U`, `0.033`
   overlap if `κ = L − 3`) shows the fourth corner sits close to the saturation limit —
   a curiosity worth recording, not a lever.

<!-- Scripts: scratchpad/corner/{trump_pose,trump_structure,trump_more,geom,lemmas_check,
two_occupants,common_core,loosened_trump,thresholds,cert_readout}.py -->

## Appendix: scripts and outputs as run

Retained verbatim from the lane’s working directory on 2026-09-08. Scripts that import
`sqpack` were run through the project environment; the rest are standard-library Python.
None has been promoted to `devtools/`; the first lane that reuses one owns that
promotion.

### `cert_readout.out`

```text
L=3.81 B=0.9977 atoms=1121 scale=200000 directions=181 kappa=0.8500
  direction 0/180 (0.00 deg): min all so far 1.00025
  direction 20/180 (5.27 deg): min all so far 1.00025
  direction 40/180 (10.52 deg): min all so far 1.00025
  direction 60/180 (15.72 deg): min all so far 1.00025
  direction 80/180 (20.86 deg): min all so far 1.00025
  direction 100/180 (25.92 deg): min all so far 1.00025
  direction 120/180 (30.87 deg): min all so far 1.00025
  direction 140/180 (35.71 deg): min all so far 1.00025
  direction 160/180 (40.43 deg): min all so far 1.00025
  direction 180/180 (45.00 deg): min all so far 1.00025

class, reachable cells, min mass, cells with mass <= 1, <=1.005, <=1.02, <=1.05, <=1.1
all                     567130649 1.000250        0  2452476 10184524 23112904 50583976
corner_box_0.850        137377014 1.000250        0   515316  2372106  7430402 17776302
corner_box_1.0          262639348 1.000250        0   680710  3219076  9896686 23498814
T_0.05                       2808 1.000250        0     2808     2808     2808     2808
T_0.1                       21176 1.000250        0    21176    21176    21176    21176
T_0.2                       85036 1.000250        0    85036    85036    85036    85036
T_0.3                      364940 1.000250        0   251216   364940   364940   364940
T_0.5                     2606880 1.000250        0   441368  1741508  1988156  2606880
T_0.7                     9989324 1.000250        0   488596  2154068  3727136  7082184
central_0.5             290567277 1.000295        0  1092912  3458892  5870156 14716684
central_0.9              79033300 1.000295        0  1086792  3411456  5164280  9287284
```

### `cert_readout.py`

```text
"""Where is the retained 3.81 certificate tight?  Census of reachable event cells by geometric class.
Uses the repository's own exact grid (sqpack.fractional.sweep.scaled_mass_grid); the classification of a
cell uses the cell's midpoint centre and the concentric UNIT square at the net direction (a readout, not a
proof-grade class membership).  Classes: meets a corner box of side kappa; meets a corner triangle T_eps;
contained in the central box [w, L-w]^2.  Output: per-class minimum mass and tight-cell counts."""
import sys, json
from fractions import Fraction
import numpy as np
sys.path.insert(0, "/home/user/squares/packing/src")
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.sweep import scaled_mass_grid, weight_scale

cert = json.load(open("/home/user/squares/packing/cases/n11_fractional_certificate/certificate.json"))
L = Fraction(cert["outer_side"]); B = Fraction(cert["square_side"])
lim = Fraction(cert["angle_limit"]); steps = int(cert["direction_steps"])
atoms = tuple(Atom(str(k), Fraction(x), Fraction(y), Fraction(w)) for k, (x, y, w) in enumerate(cert["atoms"]))
scale = weight_scale(atoms)
Lf = float(L); kappa = Lf - 2.96
half_tangents = [lim * k / steps for k in range(steps + 1)]
print(f"L={Lf} B={float(B)} atoms={len(atoms)} scale={scale} directions={len(half_tangents)} kappa={kappa:.4f}", flush=True)

eps_list = (0.05, 0.1, 0.2, 0.3, 0.5, 0.7)
w_list = (0.5, 0.9)
classes = ["all", f"corner_box_{kappa:.3f}", "corner_box_1.0"] + [f"T_{e}" for e in eps_list] + [f"central_{w}" for w in w_list]
mins = {c: np.inf for c in classes}
tight = {c: {t: 0 for t in (1.0, 1.005, 1.02, 1.05, 1.1)} for c in classes}
counts = {c: 0 for c in classes}

for idx, t in enumerate(half_tangents):
    d = rotation_from_half_tangent(str(idx), t)
    mg = scaled_mass_grid(atoms, d, L, B, scale)
    red, grid = mg.reduction, mg.grid
    ue = np.array([float(x) for x in red.u_events]); ve = np.array([float(x) for x in red.v_events])
    umid = (ue[:-1] + ue[1:]) / 2; vmid = (ve[:-1] + ve[1:]) / 2
    I = []; J = []
    for i, j0, j1 in red.spans:
        I.append(np.full(j1 - j0 + 1, i)); J.append(np.arange(j0, j1 + 1))
    I = np.concatenate(I); J = np.concatenate(J)
    mass = grid[I, J] / scale
    u = umid[I]; v = vmid[J]
    c, s = float(d.ux), float(d.uy)
    # centre in container frame: (x,y) = R^{-1}(u,v) where u = c x + s y, v = -s x + c y
    x = c * u - s * v; y = s * u + c * v
    # unit square vertices at the net direction
    e1 = np.array([c, s]); e2 = np.array([-s, c])
    V = [np.stack([x, y], 1) + sx * e1 / 2 + sy * e2 / 2 for sx in (-1, 1) for sy in (-1, 1)]
    xs = np.stack([p[:, 0] for p in V], 1); ys = np.stack([p[:, 1] for p in V], 1)
    xmin, xmax, ymin, ymax = xs.min(1), xs.max(1), ys.min(1), ys.max(1)
    # penetration toward each corner: min over vertices of (x'+y') in that corner's frame
    pen = np.minimum.reduce([(xs + ys).min(1), ((Lf - xs) + ys).min(1), ((Lf - xs) + (Lf - ys)).min(1), (xs + (Lf - ys)).min(1)])
    def meets_corner_box(k):
        # Lemma 5 crossing formula in each folded corner frame (validated against SAT in lemmas_check.py).
        out = np.zeros(len(x), bool)
        phi = abs(np.arctan2(s, c))
        if phi > np.pi/4: phi = np.pi/2 - phi
        sp, cp = np.sin(phi), np.cos(phi)
        for fx, fy in ((xs, ys), (Lf - xs, ys), (Lf - xs, Lf - ys), (xs, Lf - ys)):
            gx = fx.min(1); gy = fy.min(1)
            low_x = fx[np.arange(len(x)), fy.argmin(1)]
            fold_a = low_x >= gx + sp - 1e-9     # lowest vertex right of the leftmost: chain (gx,gy+cp)->(gx+sp,gy)
            t = (gy + cp - gx) / (sp + cp)
            m_a = np.where(t < 0, np.maximum(gx, gy + cp), np.where(t > 1, np.maximum(gx + sp, gy),
                           (gx*cp + gy*sp + sp*cp) / (sp + cp)))
            t2 = (gx + cp - gy) / (sp + cp)
            m_b = np.where(t2 < 0, np.maximum(gy, gx + cp), np.where(t2 > 1, np.maximum(gy + sp, gx),
                           (gy*cp + gx*sp + sp*cp) / (sp + cp)))
            out |= np.where(fold_a, m_a, m_b) < k
        return out
    sel = {"all": np.ones(len(x), bool),
           f"corner_box_{kappa:.3f}": meets_corner_box(kappa), "corner_box_1.0": meets_corner_box(1.0)}
    for e in eps_list: sel[f"T_{e}"] = pen <= e
    for w in w_list: sel[f"central_{w}"] = (xmin >= w) & (xmax <= Lf - w) & (ymin >= w) & (ymax <= Lf - w)
    for cname, m in sel.items():
        if m.any():
            counts[cname] += int(m.sum())
            mins[cname] = min(mins[cname], float(mass[m].min()))
            for thr in tight[cname]:
                tight[cname][thr] += int((mass[m] <= thr + 1e-12).sum())
    if idx % 20 == 0:
        print(f"  direction {idx}/{steps} ({2*np.degrees(np.arctan(float(t))):.2f} deg): min all so far {mins['all']:.5f}", flush=True)

print("\nclass, reachable cells, min mass, cells with mass <= 1, <=1.005, <=1.02, <=1.05, <=1.1")
for cname in classes:
    print(f"{cname:22s} {counts[cname]:10d} {mins[cname]:.6f} " + " ".join(f"{tight[cname][t]:8d}" for t in (1.0, 1.005, 1.02, 1.05, 1.1)))
```

### `common_core.py`

```text
"""Common core K(d) = intersection of all unit squares Q in the quadrant with min_Q(x+y) <= d,
i.e. all corner occupants of T_d.  Numerical estimate on a point grid against a dense pose sample.
Family: pose (gx, gy, phi) with gx,gy>=0, phi in [-45,45] deg, gx+gy+sin|phi| <= d.
The intersection over a subfamily is a superset, so the reported core is an OUTER estimate;
we also test the four corners of the axis box [d,1]^2 against a very fine boundary sample."""
import numpy as np
from geom import unit_square

def square_from_gaps(gx, gy, th):
    h = (np.cos(th) + abs(np.sin(th))) / 2
    return unit_square(gx + h, gy + h, th)

def inside(P, pts, tol=1e-12):
    """boolean mask: pts inside convex CCW polygon P (closed)"""
    m = np.ones(len(pts), dtype=bool)
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        cr = (b[0]-a[0])*(pts[:,1]-a[1]) - (b[1]-a[1])*(pts[:,0]-a[0])
        m &= cr >= -tol
    return m

def poses(d, n_phi=181, n_g=121):
    out = []
    for th in np.linspace(-np.pi/4, np.pi/4, n_phi):
        s = abs(np.sin(th))
        if s > d: continue
        rem = d - s
        # boundary surface gx+gy = rem (the extreme members) and a few interior levels
        for lev in (rem, 0.5*rem, 0.0):
            for gx in np.linspace(0, lev, n_g):
                out.append((gx, lev - gx, th))
    return out

for d in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
    xs = np.linspace(0, 1.6, 321)
    X, Y = np.meshgrid(xs, xs)
    pts = np.stack([X.ravel(), Y.ravel()], axis=1)
    m = np.ones(len(pts), dtype=bool)
    for gx, gy, th in poses(d):
        m &= inside(square_from_gaps(gx, gy, th), pts)
    core = pts[m]
    if len(core) == 0:
        print(f"d={d:.2f}: core empty (on grid)"); continue
    area = m.sum() * (xs[1]-xs[0])**2
    print(f"d={d:.2f}: core grid-area ~ {area:.4f}, x in [{core[:,0].min():.3f},{core[:,0].max():.3f}], "
          f"y in [{core[:,1].min():.3f},{core[:,1].max():.3f}]; "
          f"axis box [d,1]^2 corners all in core? "
          f"{all(inside(square_from_gaps(gx,gy,th), np.array([[d,d],[1,d],[1,1],[d,1]])).all() for gx,gy,th in poses(d, 721, 61))}")
```

### `geom.py`

```text
"""Small exact-enough convex geometry helpers (floats, explicit tolerances)."""
import numpy as np

def unit_square(cx, cy, theta):
    """Closed unit square, centre (cx,cy), orientation theta (radians), CCW vertices."""
    c, s = np.cos(theta), np.sin(theta)
    e1 = np.array([c, s]); e2 = np.array([-s, c])
    ctr = np.array([cx, cy])
    return np.array([ctr - e1/2 - e2/2, ctr + e1/2 - e2/2, ctr + e1/2 + e2/2, ctr - e1/2 + e2/2])

def box(x0, y0, x1, y1):
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], dtype=float)

def edge_normals(P):
    n = []
    for i in range(len(P)):
        e = P[(i+1) % len(P)] - P[i]
        n.append(np.array([e[1], -e[0]]))
    return n

def separation(P, Q):
    """Max over candidate axes of the gap between projections (SAT).
    >0: disjoint with that gap; =0: touching; <0: interiors overlap (value = -min penetration)."""
    best = -np.inf
    for nrm in edge_normals(P) + edge_normals(Q):
        nn = np.linalg.norm(nrm)
        if nn == 0:
            continue
        nrm = nrm / nn
        pP = P @ nrm; pQ = Q @ nrm
        gap = max(pQ.min() - pP.max(), pP.min() - pQ.max())
        best = max(best, gap)
    return best

def interiors_overlap(P, Q, tol=1e-12):
    return separation(P, Q) < -tol

def contained_in_box(P, L, tol=1e-12):
    return P.min() >= -tol and P.max() <= L + tol

def min_lin(P, a, b):
    """min over P of a*x + b*y"""
    return float((P @ np.array([a, b])).min())
```

### `lemmas_check.py`

```text
"""Numerical checks of the elementary lemmas used in the report."""
import numpy as np
from geom import unit_square, separation, box, interiors_overlap, min_lin

# (1) corner penetration identity: min_Q(x+y) = gx + gy + sin|theta| for theta in [-45,45] deg
rng = np.random.default_rng(0)
err = 0
for _ in range(20000):
    th = rng.uniform(-np.pi/4, np.pi/4); gx, gy = rng.uniform(0, 2, 2)
    h = (np.cos(th) + abs(np.sin(th))) / 2
    Q = unit_square(gx + h, gy + h, th)
    err = max(err, abs(min_lin(Q, 1, 1) - (gx + gy + abs(np.sin(th)))))
print("(1) identity max error:", err)

# (2) L-shape lemma: every unit square in the quadrant contains a point with min(x,y) >= 1;
#     min over snug poses of max_Q min(x,y) = (u + 1/u)/2 with u = cos+sin.
worst = np.inf
for th in np.linspace(-np.pi/4, np.pi/4, 2001):
    h = (np.cos(th) + abs(np.sin(th))) / 2
    Q = unit_square(h, h, th)
    # max of min(x,y) over the square: sample boundary densely (convex function's max is on boundary)
    ts = np.linspace(0, 1, 2001)
    pts = np.concatenate([Q[i] + np.outer(ts, Q[(i+1)%4] - Q[i]) for i in range(4)])
    worst = min(worst, np.minimum(pts[:,0], pts[:,1]).max())
print("(2) min over snug poses of max_Q min(x,y):", worst, " (claim: exactly 1, at theta=0)")

# (3) closed Lemma 1: unit square in quadrant with centre in [0,a]x[0,b], a,b<=1, contains (a,b).
bad = 0
for _ in range(200000):
    th = rng.uniform(-np.pi/4, np.pi/4); h = (np.cos(th) + abs(np.sin(th))) / 2
    a, b = rng.uniform(h, 1, 2)   # a,b <= 1 and centre must be >= h
    cx, cy = rng.uniform(h, a), rng.uniform(h, b)
    Q = unit_square(cx, cy, th)
    # membership of (a,b): rotate into the square frame
    d = np.array([a - cx, b - cy]); c, s = np.cos(th), np.sin(th)
    uu = d[0]*c + d[1]*s; vv = -d[0]*s + d[1]*c
    if max(abs(uu), abs(vv)) > 0.5 + 1e-12: bad += 1
print("(3) closed Lemma 1 violations:", bad)

# (4) the snug 45-degree diamond: blocks the kappa-box for kappa >= 0.7072, avoids T_eps for eps < 1/sqrt2
D = unit_square(1/np.sqrt(2), 1/np.sqrt(2), np.pi/4)
print("(4) diamond min(x+y) =", min_lin(D, 1, 1), "; min x,y =", D[:,0].min(), D[:,1].min())
for kap in (0.70, 0.7072, 0.85, 0.88, 0.917, 1.0):
    print(f"    diamond meets open box (0,{kap})^2:", interiors_overlap(D, box(0, 0, kap, kap)))

# (5) blocker condition: crossing formula (gx cos + gy sin + sin cos)/(sin+cos) < kappa  vs SAT test
mism = 0
for _ in range(50000):
    th = rng.uniform(0, np.pi/4); gx, gy = rng.uniform(0, 1.2, 2); kap = rng.uniform(0.8, 1.0)
    h = (np.cos(th) + np.sin(th)) / 2
    Q = unit_square(gx + h, gy + h, th)
    c, s = np.cos(th), np.sin(th)
    t = (gy + c - gx) / (s + c)
    if 0 <= t <= 1:
        pred = (gx*c + gy*s + s*c) / (s + c) < kap
    elif t < 0:   # crossing before the leftmost vertex: min of max(x,y) at leftmost vertex? then it's the vertex (gx, gy+c)
        pred = max(gx, gy + c) < kap
    else:
        pred = max(gx + s, gy) < kap
    if pred != interiors_overlap(Q, box(0, 0, kap, kap)): mism += 1
print("(5) crossing-formula vs SAT mismatches:", mism)

# (6) wall-service thresholds: 1 + 4e + 2 sqrt(1-e^2) = L
from scipy.optimize import brentq
for L in (3.81, 3.84, 3.877083590022814):
    e = brentq(lambda e: 1 + 4*e + 2*np.sqrt(1 - e*e) - L, 0, 0.5)
    print(f"(6) L={L:.6f}: both-corners-in-T_eps forces a third bottom-strip square for eps < {e:.6f}")
    print(f"    two-square service needs g1+g2+e1+e2 > L-1 = {L-1:.4f}; with e<=sqrt2: g1+g2 > {L-1-2*np.sqrt(2):.4f}; axis: g1+g2 > {L-3:.4f}")
```

### `local_probe.py`

```text
"""Local IS-consistency of corner alternatives: in the window [0,W]^2 with ONE blocker present, is there any
unit probe P subset [0,W]^2 whose interior avoids the blocker?  Maximise SAT separation(P, blocker) subject to
containment; a maximum < 0 means every probe in the window overlaps the blocker's interior."""
import numpy as np
from scipy.optimize import differential_evolution
from geom import unit_square, separation, box

def best_probe(blocker, W, seeds=6):
    def obj(v):
        P = unit_square(*v)
        pen = max(0, -P.min()) + max(0, P.max() - W)
        return -separation(P, blocker) + 100 * pen
    best = None
    for sd in range(seeds):
        r = differential_evolution(obj, [(0.5, W - 0.5), (0.5, W - 0.5), (-np.pi/4, np.pi/4)], seed=sd,
                                   tol=1e-12, maxiter=1500, popsize=30, polish=True)
        if best is None or r.fun < best.fun: best = r
    return -best.fun, best.x

kappa = 0.88
cases = {
    "near-miss axis blocker [k-0.01, k+0.99]^2, k=0.88": box(kappa - 0.01, kappa - 0.01, kappa + 0.99, kappa + 0.99),
    "snug 45-degree diamond": unit_square(1/np.sqrt(2), 1/np.sqrt(2), np.pi/4),
    "snug 22.5-degree square": unit_square((np.cos(np.pi/8)+np.sin(np.pi/8))/2, (np.cos(np.pi/8)+np.sin(np.pi/8))/2, np.pi/8),
    "flush axis square [0,1]^2 (control: probes fit beside it)": box(0, 0, 1, 1),
}
for W in (2.0, 2.2):
    print(f"window [0,{W}]^2")
    for name, Bk in cases.items():
        sep, v = best_probe(Bk, W)
        print(f"  {name:60s}: max separation = {sep:+.5f}  (probe centre ({v[0]:.3f},{v[1]:.3f}), angle {np.degrees(v[2]):.1f} deg)"
              f"  -> {'NO probe fits locally' if sep < -1e-9 else 'a probe fits'}")
```

### `loosened_trump.py`

```text
"""Trump's packing placed in [0, L']^2 for L' = 3.95 (< 3.96, so insertion saturation holds there),
reflected so that its non-flush corner is at the container's bottom-left, and pushed to the top-right.
Reports the free corner region: a method-level witness for what IS + geometry cannot force."""
import numpy as np
from trump_pose import squares, S
from geom import *

for Lp in (S, 3.90, 3.95, 3.9599):
    off = Lp - S
    # reflect (x,y) -> (S-x, S-y) so the TR corner goes to BL, then translate by off
    sq = [np.array([[S - x + off, S - y + off] for x, y in q]) for q in squares]
    sq = [q[::-1] for q in sq]  # keep CCW after point reflection (orientation preserved by point reflection, actually)
    valid = all(contained_in_box(q, Lp, 1e-9) for q in sq) and all(
        separation(sq[i], sq[j]) >= -1e-9 for i in range(11) for j in range(i+1, 11))
    kap = Lp - 2.96
    lo, hi = 0.0, 2.0
    for _ in range(60):
        mid = (lo+hi)/2
        free = not any(interiors_overlap(q, box(0, 0, mid, mid)) for q in sq)
        lo, hi = (mid, hi) if free else (lo, mid)
    eps = min(min_lin(q, 1, 1) for q in sq)
    bl = [i for i, q in enumerate(sq) if interiors_overlap(q, box(0, 0, kap, kap))]
    dmin = min(np.linalg.norm(q, axis=1).min() for q in sq)
    print(f"L'={Lp:.4f} offset={off:.4f} valid={valid} kappa={kap:.4f} blockers(kappa-box)={bl} "
          f"free axis box a={lo:.4f} free triangle eps={eps:.4f} nearest vertex dist={dmin:.4f}")
    # also: is any unit probe insertable?  (sanity: must be no, since L' < 3.96) -- check a few obvious probes
    probes = [box(0, 0, 1, 1), box(0, 0, 0.99, 0.99)]
    for P in probes:
        print(f"   probe {P[0]}..{P[2]} blocked by {[i for i,q in enumerate(sq) if interiors_overlap(q,P)]}")
```

### `thresholds.py`

```text
"""Threshold table for the report: kappa, monotonicity strip widths, area thresholds, at the reference sides."""
import numpy as np
U = 3.877083590022814; s11 = 3.810025723614703
known = [(2, 2.0, "s(2)=2"), (5, 2 + 1/np.sqrt(2), "s(5)=2+1/sqrt2"), (6, 3.0, "s(6)=3"),
         (10, 3 + 1/np.sqrt(2), "s(10)=3+1/sqrt2"), (11, s11, "s(11)>=3.810025... (T-022)")]
for L in (3.81, 3.84, U):
    print(f"\nL = {L:.6f}")
    print(f"  kappa = L - 2.96 = {L-2.96:.6f}   (corner box side forced blocked by T-017 overhang)")
    print(f"  2*kappa = {2*(L-2.96):.6f}  (every corner-box blocker has penetration delta < 2 kappa)")
    print(f"  diamond blocker bound: gx+gy < 2kappa - 1/sqrt2 = {2*(L-2.96)-1/np.sqrt(2):.6f}")
    for k, sk, name in known:
        # squares avoiding the open annulus of width w are in [w,L-w]^2 (side L-2w); at most k-1 if L-2w < s(k)
        w_ann = (L - sk) / 2
        # squares avoiding the corner L-strip of width w are in [w,L]^2 (side L-w)
        w_L = L - sk
        print(f"  {name:28s}: >= {11-(k-1):2d} squares meet any open annulus of width > {w_ann:.4f}; "
              f">= {11-(k-1):2d} meet any corner L-strip of width > {w_L:.4f}")
    # area: squares avoiding a single wall strip of width w are in an L x (L-w) rectangle; impossible if L(L-w) < 11
    print(f"  single wall strip (area only): a free strip of width w needs L(L-w) >= 11, i.e. w <= {L - 11/L:.4f}")
    # wall-service lemma thresholds
    print(f"  wall service: two squares alone need g1+g2+e1+e2 > L-1 = {L-1:.4f}; axis-aligned pair: g1+g2 > {L-3:.4f}; "
          f"tilted pair (e<=sqrt2): g1+g2 > {L-1-2*np.sqrt(2):.4f}")
    # nine-point angle
    th0 = np.degrees(np.arcsin(4/L/np.sqrt(2)) - np.pi/4)
    print(f"  nine-point threshold theta0 (cos+sin = 4/L): {th0:.4f} deg")
```

### `trump_more.py`

```text
import numpy as np
from trump_pose import squares, S
from geom import *
kappa = S - 2.96
# Lemma 6 tightness: squares avoiding the open corner L-strip {x<w or y<w} at each corner
def to_corner(q, k):
    x, y = q[:,0].copy(), q[:,1].copy()
    if k in (1, 2): x = S - x
    if k in (2, 3): y = S - y
    return np.stack([x, y], 1)
print("corner L-strip avoidance (squares contained in [w,S]^2 in corner coordinates):")
for w in (0.17, 0.5, 0.8771, 0.9, 1.0, 1.17, 1.5, 1.8771):
    row = []
    for k in range(4):
        qs = [to_corner(q, k) for q in squares]
        inside = [i for i, q in enumerate(qs) if q.min() >= w - 1e-9]
        row.append(f"c{k}:{inside}")
    print(f"  w={w:.4f} (box side {S-w:.4f}): " + "  ".join(row))
# wall service: for each wall, the squares meeting the kappa-strip, their traces, and the two-blocker inequality
print("\nwall service in the kappa-strip (kappa=%.4f):" % kappa)
frames = {"bottom": lambda q: q, "right": lambda q: np.stack([q[:,1], S - q[:,0]], 1),
          "top": lambda q: np.stack([S - q[:,0], S - q[:,1]], 1), "left": lambda q: np.stack([S - q[:,1], q[:,0]], 1)}
for nm, f in frames.items():
    qs = [f(q) for q in squares]
    serving = [i for i, q in enumerate(qs) if interiors_overlap(q, box(0, 0, S, kappa))]
    traces = {}
    for i in serving:
        q = qs[i]; pts = []
        for j in range(4):
            a, b = q[j], q[(j+1) % 4]
            if a[1] < kappa: pts.append(a[0])
            if (a[1]-kappa)*(b[1]-kappa) < 0:
                t = (kappa-a[1])/(b[1]-a[1]); pts.append(a[0]+t*(b[0]-a[0]))
        traces[i] = (min(pts), max(pts))
    # 1-net check: every [t,t+1] in [0,S] meets some open trace
    ts = np.linspace(0, S-1, 4001)
    ok = all(any(lo < t+1 and hi > t for lo, hi in traces.values()) for t in ts)
    # corner blockers on this wall
    b1 = [i for i, q in enumerate(qs) if interiors_overlap(q, box(0, 0, kappa, kappa))]
    b2 = [i for i, q in enumerate(qs) if interiors_overlap(q, box(S-kappa, 0, S, kappa))]
    print(f"  {nm:6s}: serving={serving} 1-net={ok} blockers left={b1} right={b2} traces=" +
          ", ".join(f"sq{i}:({lo:.3f},{hi:.3f})" for i, (lo, hi) in traces.items()))
    # two-blocker inequality with the actual first blockers
    i1, i2 = b1[0], b2[0]
    q1, q2 = qs[i1], qs[i2]
    e = lambda q: q[:,0].max() - q[:,0].min()
    g1 = q1[:,0].min(); g2 = S - q2[:,0].max()
    print(f"          g1+e1+1+g2+e2 = {g1:.3f}+{e(q1):.3f}+1+{g2:.3f}+{e(q2):.3f} = {g1+e(q1)+1+g2+e(q2):.3f} vs L = {S:.3f} "
          f"-> two blockers alone {'suffice' if g1+e(q1)+1+g2+e(q2) > S else 'do NOT suffice'}; |serving|={len(serving)}")
```

### `trump_pose.py`

```text
"""Numerical reconstruction of Trump's 11-square packing (from cases/trump11/packing.py)
and its corner / wall / annulus structure.  Standalone: only mpmath + numpy.
"""
import mpmath as mp
import numpy as np
mp.mp.dps = 40

U_MIN_POLY = (5, -10, -2, 14, 12, -6, 2, 2, -1)  # highest degree first, u = tan(a/2)

def poly(c, x):
    acc = mp.mpf(0)
    for k in c:
        acc = acc * x + k
    return acc

u = mp.findroot(lambda x: poly(U_MIN_POLY, x), mp.mpf('0.365'))
assert mp.mpf('0.36') < u < mp.mpf('0.37')
cos_a = (1 - u*u) / (1 + u*u)
sin_a = 2*u / (1 + u*u)
side = (6*u + 4) / (1 + 2*u - u*u)
r1 = 1 - (side - 3) * cos_a
u1 = ((1 + r1) * cos_a - 1) / sin_a
v1 = cos_a - sin_a
v2 = (side - 1) / sin_a - r1 - (3 + u1) * (cos_a / sin_a)
x0 = 1 + 2 / cos_a - (side - 2) * (sin_a / cos_a)
a_deg = mp.degrees(mp.atan2(sin_a, cos_a))

def axis_aligned(x, y):
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]

def tilted(ox, oy):
    corners = []
    for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1)):
        px, py = ox + dx, oy + dy - r1
        corners.append((1 + cos_a * px - sin_a * py, 1 + sin_a * px + cos_a * py))
    return corners

SQ = [
    axis_aligned(0, 0),
    axis_aligned(side - 1, 0),
    axis_aligned(x0, side - 1),
    axis_aligned(0, side - 1),
    axis_aligned(1, side - 1),
    axis_aligned(0, side - 2),
    tilted(0, 0),
    tilted(u1, -1),
    tilted(1, v1),
    tilted(u1 + 1, v1 - 1),
    tilted(u1 + 2, -v2),
]
S = float(side)
squares = [np.array([[float(x), float(y)] for x, y in q]) for q in SQ]

if __name__ == "__main__":
    print(f"u = {u}\nangle a = {a_deg} deg\nside s = {side}")
    print(f"x0 = {x0}, r1 = {r1}, u1 = {u1}, v1 = {v1}, v2 = {v2}")
    for i, q in enumerate(squares):
        c = q.mean(axis=0)
        e = q[1] - q[0]
        th = np.degrees(np.arctan2(e[1], e[0])) % 90.0
        print(f"sq{i:2d} center=({c[0]:.6f},{c[1]:.6f}) angle mod 90 = {th:9.6f}  "
              f"xrange=[{q[:,0].min():.6f},{q[:,0].max():.6f}] yrange=[{q[:,1].min():.6f},{q[:,1].max():.6f}]")
```

### `trump_structure.py`

```text
import numpy as np
from trump_pose import squares, S
from geom import *

# --- validity ---
print("side S =", S)
ok = all(contained_in_box(q, S, 1e-9) for q in squares)
print("all contained:", ok)
worst = 0
for i in range(11):
    for j in range(i+1, 11):
        sep = separation(squares[i], squares[j])
        worst = min(worst, sep)
print("min pairwise separation (>= -1e-9 means valid):", worst)

# --- corner frames: map each corner to origin with container in first quadrant ---
def to_corner(q, k):
    x, y = q[:,0].copy(), q[:,1].copy()
    if k in (1, 2): x = S - x
    if k in (2, 3): y = S - y
    return np.stack([x, y], axis=1)
names = ["BL (0,0)", "BR (S,0)", "TR (S,S)", "TL (0,S)"]
kappa = S - 2.96
print(f"\nkappa = L - 2.96 = {kappa:.6f}")
for k in range(4):
    print(f"\n== corner {names[k]} ==")
    qs = [to_corner(q, k) for q in squares]
    pen = [min_lin(q, 1, 1) for q in qs]
    i0 = int(np.argmin(pen))
    print(f"  penetration delta = min_i min_Q(x+y) = {pen[i0]:.6f} attained by sq{i0}")
    for kap in (1.0, kappa, 0.85, 0.5):
        bl = [i for i, q in enumerate(qs) if interiors_overlap(q, box(0, 0, kap, kap))]
        print(f"  blockers of corner box side {kap:.4f}: {bl}")
    # largest free axis-aligned corner box [0,a]^2
    lo, hi = 0.0, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2
        free = not any(interiors_overlap(q, box(0, 0, mid, mid)) for q in qs)
        lo, hi = (mid, hi) if free else (lo, mid)
    print(f"  largest free axis box [0,a]^2: a = {lo:.6f}")
    # largest free corner triangle x+y<=eps
    print(f"  largest free triangle T_eps: eps = {min(pen):.6f}")
    dmin = min(np.linalg.norm(q, axis=1).min() for q in qs)
    print(f"  min vertex distance to corner: {dmin:.6f}")
    # min distance from the corner point to any square (as a set)
    # (vertex distance is enough here since nearest point of a convex polygon to an outside point
    #  may be on an edge; compute properly)
    def dist_pt_poly(p, P):
        best = np.inf
        for i in range(4):
            a, b = P[i], P[(i+1) % 4]
            t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
            best = min(best, np.linalg.norm(p - (a + t*(b-a))))
        return best
    print(f"  distance from corner point to nearest square: {min(dist_pt_poly(np.zeros(2), q) for q in qs):.6f}")

# --- wall strips ---
print("\n== wall strips: squares whose interior meets the open strip of width w along each wall ==")
walls = {"bottom": lambda w: box(0, 0, S, w), "right": lambda w: box(S - w, 0, S, S),
         "top": lambda w: box(0, S - w, S, S), "left": lambda w: box(0, 0, w, S)}
for w in (1.0, kappa, 0.5, 0.2, 0.1, 0.05, 0.01):
    row = {nm: [i for i, q in enumerate(squares) if interiors_overlap(q, f(w))] for nm, f in walls.items()}
    print(f"  w={w:.4f}: " + "; ".join(f"{nm}:{v}" for nm, v in row.items()))

print("\n== squares contained in the central box [w, S-w]^2 (do not meet the open annulus of width w) ==")
for w in (0.01, 0.0335, 0.05, 0.085, 0.1, 0.2, 0.3, 0.4385, 0.5, 0.585, 0.7, 0.9385, 1.0):
    inside = [i for i, q in enumerate(squares) if q.min() >= w - 1e-9 and q.max() <= S - w + 1e-9]
    print(f"  w={w:.4f}: side {S-2*w:.4f}: contained = {inside} (count {len(inside)})")

# --- central disk ---
c = np.array([S/2, S/2])
def dist_pt_poly(p, P):
    # 0 if inside
    inside = True
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        if (b - a)[0]*(p - a)[1] - (b - a)[1]*(p - a)[0] < 0: inside = False
    if inside: return 0.0
    best = np.inf
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
        best = min(best, np.linalg.norm(p - (a + t*(b-a))))
    return best
d = [dist_pt_poly(c, q) for q in squares]
print(f"\ncentre ({S/2:.4f},{S/2:.4f}): distances to squares: " + ", ".join(f"sq{i}:{v:.4f}" for i, v in enumerate(d)))
print("squares containing the centre:", [i for i, v in enumerate(d) if v == 0.0])

# --- bottom-wall service (traces in the strip of height kappa) ---
print("\n== bottom-wall traces in the open strip (0,S)x(0,kappa) ==")
for i, q in enumerate(squares):
    if interiors_overlap(q, box(0, 0, S, kappa)):
        # clip polygon to strip: sample the x-extent of the part with y<kappa
        ys = q[:,1]
        pts = []
        for j in range(4):
            a, b = q[j], q[(j+1) % 4]
            for p in (a,):
                if p[1] < kappa: pts.append(p[0])
            if (a[1] - kappa) * (b[1] - kappa) < 0:
                t = (kappa - a[1]) / (b[1] - a[1]); pts.append(a[0] + t*(b[0]-a[0]))
        print(f"  sq{i}: trace x in ({min(pts):.4f}, {max(pts):.4f})")
```

### `two_occupants.out`

```text
best objective (= eps needed, plus penalty): 1.0000000000000315
square 1: centre (0.500000, 1.500000) angle 0.0000 deg, min(x+y)=1.000000, min x=0.000000 min y=1.000000
square 2: centre (1.500000, 0.500000) angle 0.0000 deg, min(x+y)=1.000000, min x=1.000000 min y=0.000000
separation(Q1,Q2) = 8.881784197001252e-16  centre distance = 1.4142133513572108
compare 1/sqrt2 = 0.7071067811865475
```

### `two_occupants.py`

```text
"""Numerically estimate eps* = sup{eps : two interior-disjoint unit squares in the quadrant
x,y>=0 both meet the closed triangle x+y<=eps}.  X-019 proves eps* <= 1/sqrt2 via centre distance;
this checks whether that bound is sharp (a lower bound on eps* is a found configuration)."""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from geom import unit_square, separation, min_lin

def objective(v):
    cx1, cy1, t1, cx2, cy2, t2 = v
    Q1 = unit_square(cx1, cy1, t1); Q2 = unit_square(cx2, cy2, t2)
    pen = 0.0
    for Q in (Q1, Q2):
        pen += max(0.0, -Q[:,0].min()) + max(0.0, -Q[:,1].min())
    sep = separation(Q1, Q2)
    pen += max(0.0, -sep)
    val = max(min_lin(Q1, 1, 1), min_lin(Q2, 1, 1))
    return val + 50.0 * pen

bounds = [(0.5, 2.5), (0.5, 2.5), (-np.pi/4, np.pi/4)] * 2
best = None
rng = np.random.default_rng(1)
for seed in range(12):
    res = differential_evolution(objective, bounds, seed=seed, tol=1e-12, maxiter=3000, polish=True, popsize=40)
    res2 = minimize(objective, res.x, method="Nelder-Mead", options={"xatol":1e-12,"fatol":1e-14,"maxiter":20000})
    cand = res2 if res2.fun < res.fun else res
    if best is None or cand.fun < best.fun:
        best = cand
v = best.x
Q1 = unit_square(*v[:3]); Q2 = unit_square(*v[3:])
print("best objective (= eps needed, plus penalty):", best.fun)
print("square 1: centre (%.6f, %.6f) angle %.4f deg, min(x+y)=%.6f, min x=%.6f min y=%.6f" %
      (v[0], v[1], np.degrees(v[2]), min_lin(Q1,1,1), Q1[:,0].min(), Q1[:,1].min()))
print("square 2: centre (%.6f, %.6f) angle %.4f deg, min(x+y)=%.6f, min x=%.6f min y=%.6f" %
      (v[3], v[4], np.degrees(v[5]), min_lin(Q2,1,1), Q2[:,0].min(), Q2[:,1].min()))
print("separation(Q1,Q2) =", separation(Q1, Q2), " centre distance =", np.hypot(v[0]-v[3], v[1]-v[4]))
print("compare 1/sqrt2 =", 1/np.sqrt(2))
```

## Session-109 — the corner-class LP under the corner-pair condition at 96/25 (2026-09-08)

Research lane BC-292 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-126](../../../../hypotheses/H-126-insertion-saturation-corner-structure.md) and
[H-127](../../../../hypotheses/H-127-corner-class-surplus-at-q.md), bead `think-kx2l`,
session-109, 2.5 hours from 15:35Z on 2026-09-08 on one worker of a shared four-core
host (load average 1.0 to 2.5 throughout; wall times are not comparable with a quiet
machine). The planning report above is untouched; this section is the lane’s result.
Scripts and raw outputs are in the appendix at the end of this section; nothing here is
a registered round, a new bound, or an edit to any registry.

### The question and its falsifiers

Question (the agenda cell, verbatim): does pricing the four corner blockers’ cores above
the rest, or banking their corner boxes, give a covering surplus at 96/25?

The premise the coordinator asked the lane to use is session-101’s corner-pair theorem,
and the lane reads it in the sharper form its own proof gives.
Lemma C′ applied to the pair says that a set of atoms of total weight above `ε` has an
atom inside some *core* — a closed `B`-square at a net direction, strictly inside its
unit square — not merely inside a placement.
So at side `96/25`, with `B = 9977/10000` and the retained 181-direction net, every
packing of eleven unit squares has four distinct squares, one per corner, whose cores
each contain one of that corner’s two marks `m₁ = (3152/3175, 2336/3175)`,
`m₂ = (2336/3175, 3152/3175)` (and their images under the container’s symmetries).
The class this lane prices is therefore “cores containing a mark”, which per net
direction is the union of the marks’ coverage rectangles in the rotated frame — exactly
the event geometry the sweep already has.
No clip and no new engine were needed for the corner class; the centre-domain clip of
Theorem B’s deep-corner bins was not built (see the three-plus-one paragraph).

Two facts about the branches were settled before any run.
First, under a D4-symmetric measure every one of the sixteen mark branches collapses to
the union region: the diagonal reflection through a corner is a container symmetry and
swaps that corner’s two marks, so the folded net cannot tell `m₁` from `m₂`. The
flush-four program under D4 *is* the union-region program.
A branch needs a measure with only the branch’s stabiliser and a mark set closed under
it: the sixteen patterns fall into four D4 orbits — the two *opposite-both* patterns
(stabiliser the Klein group of the two axis reflections, `D2`), the four *U* patterns
(one axis reflection), the two *pinwheels* (`C4`, no reflection) and the eight
asymmetric *J* patterns (trivial stabiliser).
A folded net needs a reflection in the stabiliser, so the `D2` and `U` branches run on
the retained net at two and four times the site count; the pinwheel and `J` branches
need a quarter-turn net and a float centre domain that does not assume `cos ≥ sin`,
which the library does not have.
Second, banking the marks is a special case of pricing: crediting the mark’s own weight
is the class program with `w_c` fixed at that weight, so the class program dominates
mark-banking and only the class program was run.

The program. Sites `S` folded into orbits under a group `G`; a `G`-symmetric measure
`μ ≥ 0` on `S`; thresholds `w_c ≥ w_f ≥ 0` (the order is without loss, since a region
core is also some square’s core and must carry `w_f`). Every admissible core carries at
least `w_f`; every admissible core containing a mark of the chosen set carries at least
`w_c`. The four corner cores are distinct and in the class, the other seven cores carry
`w_f`, and the eleven are pairwise disjoint, so `4 w_c + 7 w_f ≤ M` for every packing: a
measure with `M − 4 w_c − 7 w_f < 0` excludes eleven squares at `96/25`. The LP is
homogeneous and is solved under `4 w_c + 7 w_f = 1` (the *ratio* form, optimum `M*`; a
certificate needs `M* < 1`) or, for a branch, under `w_f = 1` (the *slice* form, optimum
`M − 4 w_c`; a certificate needs it below `7`). For the union program the two forms are
the same object rescaled, because `w_f > 0` at the optimum.

Falsifiers, stated before each run and recorded in the lane checkpoints.
For a site set `S`: a `G`-symmetrised fractional packing `y` of exactly re-derived
admissible placements with depth at most `1` at every site, total weight at least `11 λ`
and weight at least `4 λ` on placements that contain a chosen mark, with `λ ≥ 1`. Weak
duality gives, for every feasible `(μ, w_c, w_f)` on `S`,
`M ≥ Σ_r y_r μ(P_r) ≥ w_c Σ_A y + w_f Σ_{¬A} y ≥ λ (4 w_c + 7 w_f)`, so the residual
`M − 4 w_c − 7 w_f ≥ (λ − 1)(4 w_c + 7 w_f)` is nonnegative and no certificate exists on
`S`. In the slice form the same packing gives `M − 4 w_c − 7 ≥ Σ y − 11` whenever
`Σ_A y ≥ 4`. The second falsifier of the cell, eleven disjoint cores satisfying the
condition, is the integral case of the first and was not available (eleven disjoint
`B`-squares at `96/25` would be a packing at side `3.849`). Only the exact objects
count: the rationalised primal decided by the integer event-cell sweep with the marks’
rectangle boundaries as events, and the dual packing decided in `Fraction` arithmetic on
re-derived rows; every LP objective is context.

### Inputs common to every run

| Input | Value |
| --- | --- |
| Side, shrink | `L = 96/25`, `B = 9977/10000` |
| Net | `t_k = k · 207107/500000 / 180`, `k = 0..180` (181 directions, the retained net; `B(1 + D) < 1` as for T-018) |
| Marks | `m₁ = (3152/3175, 2336/3175)`, `m₂ = (2336/3175, 3152/3175)` and their images: eight points, T-018’s `(197/200, 73/100)` orbit scaled by `128/127` |
| Site set A (grid 79) | `build_site_grid(96/25, 79, 1/10)`: 79 coordinates from `1/10` to `369/100` at pitch `91/1950`, plus the eight marks; folded under the run’s group (D4: 821 orbits over 6249 sites; D2: 1602 orbits; `Sv`: 3163 orbits) |
| Class region | cores whose closed `B`-square contains a chosen mark; per direction the union of the marks’ coverage rectangles `[u_m ± B/2] × [v_m ± B/2]`, whose boundaries are events in both the float separator and the exact sweep (the marks ride along as zero-weight atoms) |
| Row generation | three least-covered cells per direction *per class* below its threshold, rows read at a point of the cell’s overlap with the centre domain as `generate.placement_cells` reads them, deduplicated, until no cell is short by more than `10⁻⁹`; HiGHS on the two-threshold LP with `w_f ≤ w_c` |
| Rationalisation | bump `1000001/1000000`, round up to multiples of `1/4 000 000`, drop empty orbits; group closure of the atoms re-checked exactly |
| Exact primal | `w_c :=` least integer-grid mass over the class cells, `w_f :=` least over all cells, both over all 181 directions on `sweep.scaled_mass_grid` |
| Exact dual | rows with positive dual weight re-derived from their float centre as a `Fraction`: centre inside the closed centre domain, coverage counts per orbit and mark containment decided exactly; `y` rounded down to multiples of `10⁻⁶`, or solved exactly at the tight vertex where the bound sits on a knife-edge; symmetrised depth `Σ_r y_r |P_r ∩ O| / |O| ≤ 1` checked on every orbit |
| Machine | one process, `PACK_JOBS=1`, one BLAS thread; two other lanes on the four cores, load average 1.0 to 2.5 |

### Runs and exact verdicts

**Run 1, the flush-four program (union region, D4, site set A).** Row generation
converged in 17 rounds and 63 s on 6646 rows (load 1.1 to 1.7). LP: ratio optimum
`1.032490975`, `w_c / w_f = 1.103`. Rationalised measure: 289 atoms, mass
`M = 103253/100000`; exact `w_c = 386619/4000000`, `w_f = 175259/2000000`, both attained
at direction `0`; exact residual `M − 4 w_c − 7 w_f = 65009/2000000 > 0`, i.e. in the
slice normalisation `M/w_f = 11.7829`, `w_c/w_f = 1.10299`, residual
`65009/175259 = 0.37093`. Census: 43 305 349 reachable cells, 11 176 736 in the class.
Exact dual: 41 rows, none dropped, maximum symmetrised depth `7999993/8000000`, total
`11.357376`, `4.129958` on mark-containing placements, **`λ = 177459/171875 =
1.0324887 ≥ 1`**: no measure on site set A has a negative residual.

**Run 2, the free control on the same site set (no class, `11 w_f = 1`).** Converged in
16 rounds and 55 s on 7575 rows.
Rationalised: 233 atoms, `M = 2066149/2000000`, exact `w_f = 363641/4000000`,
`M / w_f = 11.363675`. Exact dual: 48 rows, maximum depth `3999997/4000000`, total
`11.363421`, of which `4.018083` on mark-containing placements,
`λ_free = 11363421/11000000 = 1.0330383`.

**The surplus, exactly.** Each optimum lies between its exact dual and its exact
rationalised primal ratio: `free* ∈ [11363421/11000000, 4132298/4000051]` and
`class* ∈ [177459/171875, 2065060/2000051]`, so the corner class lowers the ratio
optimum on site set A by between `11761534471/22000561000000 = 0.000535` and
`35788031/62500796875 = 0.000573` — a real surplus, and between `1.6` and `1.8` per cent
of the gap `0.0325` that separates the free program from the certificate line.
The free dual’s weight on mark-containing placements, `4.018`, is above `4` but below
`4 λ_free = 4.132`, which is why the class constraint binds at all; the class dual then
spends exactly `4 λ` on the corner region and `7 λ` elsewhere.

**Run 3, the opposite-both branch, homogeneous (D2, chosen marks `m₁` and its axis
images, site set A).** The LP converged in five rounds at ratio `1.000000000` with
`w_f = 0`, `w_c = 1/4` and the measure `1/4` at each chosen mark: the trivial banking
measure has residual exactly `0`, and the exact vertex of the dual (36 rows, solved in
`Fraction` arithmetic on the tight system, maximum symmetrised depth exactly `1`, total
exactly `11`, exactly `4` on chosen-mark placements) gives **`λ = 1` exactly**. The
mechanism is general: the chosen marks are sites, a dual packing has depth at most `1`
at each, every chosen-mark placement contains exactly one chosen mark, so `Σ_A y ≤ 4`
and no branch dual can exceed `λ = 1`, while the primal can always bank the four marks
at ratio exactly `1`. A branch program in ratio form sits on this knife-edge whatever
the site set; the informative branch program is the slice `w_f = 1`.

**Run 3b, the opposite-both branch, slice (`w_f = 1`, D2, site set A).** RUN3B

**Run 4, the U branch, slice (`Sv`, chosen marks the bottom-wall marks at the bottom
corners and the side-wall marks at the top corners, site set A).** RUN4

**Run 5, the flush-four program on the corner-refined site set B.** RUN5

### Reading

READING

### The three-plus-one branch

Under the corner-pair premise all four corners carry a mark-containing core
unconditionally, so the cover has one case and the sixteen mark branches are its
refinement; “three-plus-one” in the sense of Theorem B — three corners banked by
penetration depth and the fourth in a deep bin with `T_{0.7}` free — needs the
half-plane clip `a + b > d + cos θ` on the centre domain, in both the float separator
(`generate._CentreDomain` assumes the rotated square and `cos ≥ sin`) and the exact
`reduce_to_spans` (which calls `sweep.centre_domain` directly), together with the banked
boxes `X′_j` and their credits, and a measure with the deep corner’s stabiliser (one
diagonal reflection, four times the site count).
That is a half-session of instrument work the lane did not start, because the flush-four
readings above already bound what any corner banking can buy at this shrink and net: the
corner region is the binding region of the covering dual, not an over-covered one.
Its design is recorded here so the next lane does not re-derive it: the clipped domain
stays convex, so `reduce_to_spans`’ per-slab min/max of the clipped polygon is already
correct for it, and only the float `v_range`/`u_chord` closed forms need a general
convex-polygon replacement.

### Status of H-126 and H-127

STATUS

### Obstructions and mistakes worth recording

OBSTRUCTIONS

### Appendix: scripts and outputs as run

APPENDIX

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
