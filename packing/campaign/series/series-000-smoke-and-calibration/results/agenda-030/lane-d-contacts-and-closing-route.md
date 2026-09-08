# Agenda 030, lane D: Contact lemmas and the closing route

Retained planning-lane report for
[X-021](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md),
written by a Fable sub-agent at maximum effort on 2026-09-08 under BC-291 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md).
The report is reproduced as delivered, with its own status labels; X-021 carries the
coordinator’s reading of it.
Nothing here is a registered round or a new bound.

## D — Contact and spanning lemmas for side-minimal packings of 11 squares, and the closing route to s(11) = U

Date: 2026-09-08. Repository read-only (branch `claude/squares-n11-constraints-wl9atd`);
all working files under `scratchpad/D-contacts/`. Scripts were run with the project venv
(`packing/.venv/bin/python3`, Python 3.14.7, numpy 2.5.2, scipy 1.17.1); the outputs
quoted below are saved beside each script as `*.out`.

Notation: `U = 3.877083590022814` (Trump), `L_low = 3.810025723614703` (T-022),
`q = 96/25 = 3.84`, `B = 9977/10000` (the retained shrink), folded angle
`θ ∈ [0°, 45°]`, projection width `w(θ) = cos θ + sin θ ∈ [1, √2]`. A *minimizer* is a
packing at side exactly `s(11)`. Every claim is tagged PROVED, CHECKED (numerically,
with script), CONJECTURED or OPEN.

## 0. Feasibility map in one page

| Question | Answer | Status |
| --- | --- | --- |
| Must a minimizer have a contact chain joining two opposite walls? | Yes, in at least one direction (Lemma S). Both directions cannot be forced by the shrinking argument (n = 2 counterexample); Trump spans both. | PROVED |
| Point or positive-length contacts in the chain? | Nothing forces positive length: Göbel’s n = 5 optimum spans through the middle square by four corner-on-edge point contacts. | PROVED (by example) |
| Number of squares touching a wall | Spanning walls: ≥ 1 each; a third wall by translation; the fourth cannot be forced (n = 2). Flush (axis-aligned) squares per wall ≤ 3. Trump: left 3, bottom 3 (2 flush + 1 point), right 2 (1 + 1), top 3. | PROVED / CHECKED |
| Must some square have a positive-length wall or square contact? | No general argument; true in every known optimum; at n = 11 OPEN. | OPEN |
| Contact-graph rank | Some minimizer in every fixed-angle cell has 22 independent active translation rows, every square in ≥ 2 incidences, no isolated square (Lemma V). Angular rank is not forced (n = 6 rattler; n = 5 second-order flex). Trump: rank 10 segment graph, connected contact graph. | PROVED / CHECKED |
| Chain consequences at 3.84 | Chain length k ≥ 3. A 3-chain forces all three squares tilted (≥ 0.67°), two ≥ 14.05°, one ≥ 19.84°, and contains no axis-aligned square. k ≥ 4 forces nothing (three axis-aligned plus one arbitrary suffice). Trump’s shortest chains have k = 5 and k = 4. | PROVED, CHECKED — a free case split, no headroom for current instruments |
| Are minimality constraints usable at a fixed rational side? | Only with a tolerance: dilation from the (unknown) minimal side to q turns every contact into a δ-near-contact, δ = (q/L_low − 1)√2 = 0.01113 at 3.84 (Lemma T). | PROVED |
| Can conditional or “capture” dot certificates close the band? | Governed exactly by the fractional-packing value: a depth-1 family of value ≥ 11 with ≥ 1 unit of weight outside the conditioned region kills the certificate (Lemma D). With B = 9977/10000 the {0°,45°} packing already kills every capture certificate at side ≥ 3.876681 < U. At 3.84 the retained BC-200 family gives ≥ 8.87 of restricted value on corner-box conditions: not yet a kill, not yet headroom. | PROVED + CHECKED |
| Does narrowing [L1, U] make the rest “arguable away”? | No. The discard ball at target U − η shrinks as η → 0 (radius 0.054 at 3.84, 0.025 at 3.869, floor 0.004); nine-point forcing weakens (θ0: 2.44° → 1.97°); the case tree is governed by the competitor question, not the band’s width. | PROVED arithmetic on retained constants |
| The equality run above U in X-014 | Needs two conditions the sketch omits: L1 − U < κ ρ0/4 ≈ 10⁻⁵ (packings at side U + σ near Trump extend to distance ≥ σ and up to ~2σ/κ = 174σ), and B = 1 (Lemma D + exp-064 arithmetic). | PROVED (short argument) |
| Realistic route to s(11) = U | Structure theorem (ownership or normal form) + exact fixed-angle algebra over Q(u) + the modulus lemma; dot certificates alone cannot finish. Earliest hopelessness signal: the B = 1 fractional value at L ≈ 3.86–3.87 exceeding 11 with diffuse weight (Session S3). | assessment |

## 1. Results proved

### 1.1 Compactness and the three representative reductions

**Lemma 0 (minimizers exist).** The set of packings of 11 closed unit squares in
`[0, L]²` (interiors disjoint) is a closed subset of the compact set
`([0, L]² × [0, π/2))^11` (closure: containment and separation are closed conditions;
angles are taken mod π/2 on the compact circle).
`s(11) = inf{L : a packing exists}` is attained: take packings at sides `L_k ↓ s(11)`,
embed them in `[0, L_1]²`, and pass to a convergent subsequence; the limit is a packing
at side `s(11)` (each square’s closed container condition passes to the limit after
rescaling the anchor).

Three reductions are used below, and they compose (each preserves “is a minimizer”):

- **(R1) quarter turn.** Rotating the whole configuration by 90° about the container’s
  centre is a symmetry of the problem, so a direction-specific statement may be stated
  “after a quarter turn”.
- **(R2) translation.** A minimizer translated within `[0, L]²` until some square
  touches a chosen wall is a minimizer.
- **(R3) LP vertex.** Fix the angles and, for each pair, one separating axis that
  separates the pair at the given minimizer (a “SAT selection”). Containment and the
  selected separations are linear in the 22 centre coordinates; the feasible set at
  fixed side `L = s(11)` is a nonempty bounded polytope (bounded because centres lie in
  `[0, L]²`); it has a vertex, and every point of it is a minimizer with the same
  angles.

### 1.2 Lemma S (spanning) and what it does not give

**Lemma S.** Let `P = {Q_1, …, Q_n}` be a minimizer at side `L = s(n)`, `n ≥ 1`. Let `G`
be the contact graph (`i ~ j` iff `Q_i ∩ Q_j ≠ ∅`). Then some connected component of `G`
contains a square meeting the wall `x = 0` and a square meeting `x = L`, or some
component contains a square meeting `y = 0` and one meeting `y = L`.

*Proof.* Suppose neither.
For each component `C` write `a_C = min x`, `b_C = max x`, `c_C = min y`, `d_C = max y`
over `⋃ C`. By assumption `max(a_C, L − b_C) > 0` and `max(c_C, L − d_C) > 0` for every
`C`. Put `ε_h = min_C max(a_C, L − b_C)`, `ε_v = min_C max(c_C, L − d_C)`, and
`ε_d = min dist(⋃C, ⋃C')` over distinct components; `ε_d > 0` because distinct
components are disjoint compact sets (two squares in different components do not
intersect, by definition of `G`). Let `ε = min(ε_h, ε_v, ε_d/3) > 0`. Translate each
component rigidly by `(h_C, v_C)` with `h_C = −ε` if `b_C > L − ε` and `0` otherwise,
`v_C` likewise. If `b_C > L − ε` then `L − b_C < ε ≤ ε_h ≤ max(a_C, L − b_C)`, so
`a_C ≥ ε_h ≥ ε` and the shifted component has `x ∈ [a_C − ε, b_C − ε] ⊂ [0, L − ε]`; if
`b_C ≤ L − ε` it already has `x ∈ [0, L − ε]`. Same vertically.
Each shift has length `≤ ε√2 < ε_d/2`, so distinct components stay disjoint; squares
inside a component keep their relative positions, so interiors stay disjoint.
The result is a packing in `[0, L − ε]²`, contradicting minimality.
∎

**Remarks (all PROVED).**

1. *“Or”, not “and”.* For `n = 2`, `s(2) = 2`, the minimizer `[0,1]²`, `[1,2]×[0,1]`
   spans horizontally and no component spans vertically.
   So the shrinking argument cannot force both directions.
   A different minimizer, `[0,1]²` and `[1,2]²` touching at `(1,1)`, spans both.
   Whether **some** `n = 11` minimizer spans both directions is OPEN (a packing in an
   `L × H` rectangle with `H < L` would be the obstruction; Session S1 bounds `H` from
   below by rectangle certificates).
2. *Representative.* By (R1) and (R2): some minimizer has a contact chain joining the
   left and right walls and a square touching the bottom wall.
   This is a strictly stronger symmetry-breaking premise than the single bottom anchor
   used in the hybrid review, at no cost.
3. *Point contacts suffice.* Göbel’s `n = 5` optimum (four axis-aligned corner squares,
   one 45° square whose four edges pass through the inner corners of the corner squares)
   spans left–right through the middle square by two corner-on-edge point contacts; its
   only positive-length contacts are wall contacts.
   So Lemma S cannot be strengthened to positive-length chain contacts by any argument
   that applies to all `n`.
4. *Trump* (CHECKED, `trump_structure.py`): contact graph connected (one component);
   shortest left–right chain `0–6–8–9–1` (contacts point, segment, segment, point; both
   wall contacts flush), shortest bottom–top chain `0–6–8–2` (point, segment, point).

### 1.3 Corollary C (chain projections) — the quantitative consequence

**Corollary C.** In the spanning direction (say `x`), let `Q_{i_1}, …, Q_{i_k}` be a
path in `G` from a square meeting `x = 0` to one meeting `x = L`. Then
`Σ_j w(θ_{i_j}) ≥ L`, where `w(θ) = cos θ + sin θ` is the width of the `x`-projection.

*Proof.* The projection of a closed unit square at folded angle `θ` onto the `x`-axis is
a closed interval of length `w(θ)`. Consecutive squares share a point, so consecutive
projections intersect; the union of the `k` projections is therefore a single interval,
which contains `0` and `L`. Hence the lengths sum to at least `L`. ∎

**Numbers** (CHECKED, `chain_arithmetic.py`): since `w ≤ √2`, `k ≥ ⌈L/√2⌉ = 3` for every
`L ∈ [3.84, U]`. For `k = 3` at `L = 3.84`: each width `≥ L − 2√2 = 1.01157` (tilt
`≥ 0.667°`), two widths `≥ (L − √2)/2 = 1.21289` (tilt `≥ 14.05°`), one width
`≥ L/3 = 1.28` (tilt `≥ 19.84°`); a 3-chain containing an axis-aligned square needs the
other two to sum to `2.84 > 2√2`, impossible.
At `L = U` the same bounds read `2.86°`, `15.55°`, `21.04°`. For `k ≥ 4` nothing
follows: three axis-aligned squares and one arbitrary square have total width `≥ 4 > U`.

**Verdict on non-triviality.** Corollary C is a genuine, free case split — “some
spanning 3-chain of three strongly tilted mutually touching squares exists” versus
“every spanning chain has ≥ 4 squares” — but it buys no headroom for the current
instruments: the class program (exp-064) already cannot close compositions with two or
more tilted squares at 3.84, and at Trump’s pose the inequality holds with slack `2.35`
(`6.23` versus `3.88`) on the shortest chain.
It is recorded because it is the *only* consequence of spanning that is quantitative,
and because a future ownership-type argument (Session S6) can use it to prune
chain-adjacent cases.

### 1.4 Lemma V (the LP-vertex representative) and the rank question

**Lemma V.** Let `P` be a minimizer.
Fix its angles and a SAT selection valid at `P`. Then there is a minimizer `P'` with the
same angles such that (a) the active rows among the 44 wall rows (one per square and
wall) and the 55 selected pair rows have rank 22; (b) every square has at least two
active rows involving it; (c) no square is contact-free.

*Proof.* (a) is (R3). (b): if a square had at most one active row, the active matrix
would have rank ≤ 1 on that square’s two columns, so its rank would be ≤ 21. (c) follows
from (b): an active wall row is a wall contact and an active pair row is a pair contact.
∎

**What is not forced (PROVED by examples).** The angular part of the rank: the `n = 6`
optimal family (five axis squares at lower-left corners `(2,0),(2,1),(2,2),(0,2),(1,2)`,
the sixth free to rotate about `(1,1)` inside the vacant `2 × 2`) has a square with a
genuine one-parameter rotational freedom, so no lemma valid for every optimum can force
the angular rank to exceed `n − 1`; and Göbel’s `n = 5` middle square has its angle
fixed only at second order (X-007/X-012), so first-order arguments cannot force it
either. What *is* true at Trump’s pose (CHECKED): 11 wall incidences (9 flush, 2 corner
points), 14 pair contacts (7 positive-length segments
`(3,4),(3,5),(6,7),(6,8),(7,9),(8,9),(9,10)` of lengths
`1, 1, 0.975, 0.881, 0.881, 0.975, 0.666`, and 7 point contacts
`(0,6),(1,9),(2,8),(2,10),(4,5),(4,8),(5,6)`), segment-equality components
`{0},{1},{2},{3,4,5},{6,…,10}` with wall-anchored squares `0–5`, one unanchored
component, angular rank `10` — agreeing with the PR108 review and exp-013. The smallest
strictly positive pair gap is `0.0249` (pairs `(6,9)` and `(8,10)`), which is the
Euclidean counterpart of BC-199’s chart gap cap `0.0059`.

**Flush counts (PROVED, trivial).** Two axis-aligned unit squares flush on the same wall
have `x`-projections with disjoint interiors, so at most `⌊L⌋ = 3` squares are flush on
any wall for `L < 4`. Trump attains 3 on the left and top walls.

### 1.5 Lemma T (robust transfer to a fixed rational side)

Structural facts proved for minimizers hold at the unknown side `s(11) ∈ [L_low, q]`,
not at `q`. They transfer with a tolerance:

**Lemma T.** Let `P` be a packing at side `L ∈ [L_low, q]` and `λ = q/L ≤ q/L_low`.
Scaling `P` by `λ` gives 11 disjoint closed squares of side `λ` in `[0, q]²`; the
concentric unit squares `Q_i'` form a packing at side `q` such that (i) if
`Q_i ∩ Q_j ≠ ∅` in `P` then `dist(Q_i', Q_j') ≤ (λ − 1)√2`; (ii) if `Q_i` touches a wall
in `P` then `Q_i'` is within `(λ − 1)/√2` of that wall; (iii) angles are unchanged.

*Proof.* A point of the side-`λ` square is at distance at most `(λ − 1)√2/2` from the
concentric unit square (attained at a corner); apply it to the common point of two
touching scaled squares, and to the wall-contact point.
∎

At `q = 3.84`: `λ ≤ 1.007867`, contact tolerance `0.01113`, wall tolerance `0.00556`
(CHECKED). Consequence: any structural lemma to be *used* at 3.84 must be stated with
these tolerances ("a δ-chain spans the container", “a square is within `0.0056` of the
left wall”). T-017’s insertion saturation is already robust in this sense (it holds at
every side `≤ 3.96`). The tolerance shrinks as the certified lower bound rises.

### 1.6 Lemma D (LP duality governs every conditional and capture certificate)

This is the result that quantifies Part II. It is elementary and, as far as I can find,
is not stated in the record (X-014 uses weak duality only for the unconditional
ceiling).

Setting (finite version, exact): sites `S`, admissible placements `Λ` (each a closed
`B`-square at a net direction), a set `N ⊂ Λ` of “conditioned” placements, a threshold
`t(P) ≥ 0` for each `P ∈ Λ`. The generalized covering program is `min Σ_s μ_s` subject
to `Σ_{s ∈ P} μ_s ≥ t(P)` for all `P ∈ Λ`, `μ ≥ 0`. Its dual is the generalized
fractional packing `max Σ_P t(P) y_P` subject to depth `Σ_{P ∋ s} y_P ≤ 1` at every site
and `y ≥ 0`. Strong duality holds (both feasible).

Three instances:

- **Unconditional certificate**: `t ≡ 1`; exists iff `ν*_S(Λ) < 11` (the ceiling theorem
  in X-014/`ceiling.py`).
- **Conditional certificate (X-014 Lemma 2)** on a box `b`: `t = 1` on `Λ_b ∪ Π_b`
  (cores disjoint from `I_b`, plus cores inside the box’s placements), `t = 0`
  elsewhere. Exists iff the fractional packing value over `Λ_b ∪ Π_b` is `< 11`.
- **Capture certificate** (thresholds `1` on a neighbourhood `N` of the record’s own
  placements, `1 + δ` outside): exists for the pair `(N, δ)` iff for every
  depth-feasible `y`, `Σ_{P∈N} y_P + (1 + δ) Σ_{P∉N} y_P < 11 + δ`. Then every packing
  at that side has all eleven cores inside `N`: cores outside `N` contribute `≥ 1 + δ`
  each and the total is `< 11 + δ`.

**Lemma D (kill criterion; continuum version by weak duality alone).** Let `μ` be any
measure on `[0, L]²` with `μ(P) ≥ t(P)` for all placements `P` in a family, and let
`y ≥ 0` be weights on finitely many such placements with pointwise depth `≤ 1`. Then
`M = μ([0, L]²) ≥ ∫ depth dμ = Σ_P y_P μ(P) ≥ Σ_P t(P) y_P`. In particular:

- (D1) a depth-1 family of value `≥ 11` supported on cores disjoint from `I_b` (plus
  cores in the box) proves that no conditional certificate for box `b` exists on this
  `(L, B, net)`, at every larger side, for every site set and weights;
- (D2) a depth-1 family with `Σ y ≥ 11` and `Σ_{P∉N} y_P ≥ 1` proves that no capture
  certificate `(N, δ)` exists for any `δ ≥ 0`.

*Proof.* The chain of inequalities is the one in the `ceiling.py` docstring with the
thresholds inserted.
For (D2): `Σ t y = Σ y + δ Σ_out y ≥ 11 + δ`. ∎

**Corollary D3 (capture is capped by the shrink, PROVED from exp-064’s exact
arithmetic).** With `B = 9977/10000`, at every side `L ≥ B(2 + (4/3)√2) = 3.876681` the
eleven cores of the `{0°, 45°}` (Hämäläinen) packing scaled by `B` fit in `[0, L]²`
(exp-064 records this as `L/B > 2 + (4/3)√2`, exact; at `L = U`,
`U/B = 3.886021 > 3.885618`). Five of those cores are at `45°`, `4.82°` from Trump’s
`40.18°` direction, hence outside any neighbourhood `N` of Trump’s placements of angular
radius below `4.8°`; they carry weight `5 ≥ 1`. By (D2) no capture certificate exists at
any `L ∈ [3.876681, U]` with this `B`. The gap `U − 3.876681 =
0.000402` is the same `0.000403` exp-064 found for the class control, now read as a cap
on *every* record-conditioned certificate, not only the two-end-cell class.
Since `3.876681 < U`, the endpoint is unreachable with `B < 0.997804 = U/(2 + (4/3)√2)`;
with `B = 1` the Hämäläinen packing needs side `3.885618 > U` and this particular kill
disappears. The premise that the scaled 45° squares contain `B`-cores *at a net
direction* was checked on the retained net (`net_end_check.py`): its last direction is
`45.000043°`, offset `4.3 × 10⁻⁵` degrees from 45° against an allowance of `0.0059°`;
the scale `λ = U/s_H = 0.997804` exceeds both `B` (axis squares) and
`B(cos δ + sin δ) = 0.997699` (45° squares).

**Corollary D4 (what conditioning can buy is measurable from below, CHECKED).** The
retained BC-200 family (760 placements at `191/50`, exact depth `≤ 1`, total `9.907906`)
is a valid depth-1 family in `[0, 3.84]²` when anchored at any corner (weak duality
transfers upward in `L`). Its weight disjoint from a closed unit corner box is
`≥ 8.8732`; from a half-unit corner box `≥ 9.0293`; from a central unit box `≥ 7.0992`;
from the strip `x ≤ 1/10` `≥ 7.2788` (`family_restrict.py`). Reading: boxing one blocker
into a unit corner box removes about one unit of *fractional* weight, exactly the
integral count; the box does not by itself create headroom.
A conditional corner-box certificate at 3.84 is not killed by these numbers (they are
lower bounds, and `8.87 + capacity(Π_b) < 11`), but it is alive only if the true
restricted value stays below `≈ 10`; Session S2 decides that with the cutting-plane
loop.

### 1.7 The equality run above U: the missing conditions (PROVED, short)

X-014 proposes one run at rational `L1 > U` in which the certificate half refutes every
box outside the `ρ0`-ball and the modulus lemma closes the ball.
Two conditions are needed that the sketch does not state.

(i) *Size of `L1 − U`.* The BC-240 chart is anchored at the container’s lower-left
corner and does not quotient translations, so Trump’s packing translated by `(σ, 0)` is
a packing at side `U + σ` at chart distance exactly `σ` from `z*`; packings at side
`U + σ` therefore exist outside the `ρ0`-ball as soon as `σ > ρ0`. In the other
direction, a feasible pose `z* + v` in a branch satisfies `a_j·v + σ e_j + R_j(v) ≥ 0`,
and the modulus bound gives `κ‖v‖ ≤ σ + (K/2)‖v‖²`; on the half-ball `‖v‖ ≤ ρ0/2 = κ/K`
(uniform pair, `ρ0 = 2κ/K`) the quadratic term is at most `(κ/2)‖v‖`, so `‖v‖ ≤ 2σ/κ`,
and nearby packings can extend to distance up to `2σ/κ ≈ 174σ`. These are genuine
packings the certificate half cannot refute.
The run is sound only if `2σ/κ < ρ0/2`, i.e.
`σ < κρ0/4 = 0.011480 × 0.0023089/4 ≈ 6.6 × 10⁻⁶` (the per-row pair gives the same
order, `≈ 1.2 × 10⁻⁵`). A rational `L1` this close to `U` exists (e.g. `U` rounded up at
the sixth decimal, `3.877084 − U = 4.1 × 10⁻⁷`), so this is a constraint, not a
refutation.

(ii) *The shrink.* By Corollary D3 the certificate half at any `L1 ≥ 3.876681` cannot
exist with `B = 9977/10000`; the equality run requires `B = 1` (open placements, the
continuum of directions decided by interval arithmetic — X-014’s own `n = 12` design).

So the only sound closing designs are: a **tree at side exactly `U` over `Q(u)`**, with
the exact field-valued LPs of `sqpack.exact_lp` deciding fixed-angle cells and the
modulus lemma deciding the ball; or the **`B = 1` capture run at `U + σ`, `σ < 10⁻⁵`**,
which additionally needs the `B = 1` relaxation to have no diffuse value-11 fractional
packing at `U + σ` (Session S3 measures this).

## 2. Numerical checks (scripts in `scratchpad/D-contacts/`)

| Script | What it computes | Key output |
| --- | --- | --- |
| `trump_structure.py` (run with `PYTHONPATH=packing`, project venv) | Exact pose from `cases.trump11.packing` → 40-digit enclosures → floats (tolerance 1e-12); wall incidences, pair contacts classified segment/point, components, shortest spanning chains, segment-equality rank | 11 wall incidences (9 flush + 2 points), 14 pair contacts (7 segments + 7 points), contact graph connected, chains `0–6–8–9–1` (widths sum 6.228) and `0–6–8–2` (4.818), angular rank 10; smallest strict gap 0.0249 |
| `chain_arithmetic.py` (plain python3) | Chain bounds at 3.84/3.86/3.869/U; θ0(s); Lemma T tolerances; discard radii from BC-199 constants; linear allowance σ/κ; shrink caps | k ≥ 3; 3-chain tilts 0.667°/14.05°/19.84° at 3.84; θ0 = 2.44° (3.84), 1.97° (3.869), 1.85° (U); δ = 0.01113; radii 0.0537 (3.84), 0.0364 (3.86), 0.0251 (3.869), 0.0127 (3.875), floor 0.0040; capture cap 3.876681 |
| `family_restrict.py` (project venv) | BC-200 depth-1 family placed in `[0, 3.84]²`; exact weight disjoint from corner boxes, strips, centre box (separating-axis test in `Fraction`) | 8.8732 (unit corner box), 9.0293 (half-unit corner box), 7.0992 (central unit box), 7.2788 (strip x ≤ 0.1) |
| `net_end_check.py` (project venv) | Corollary D3’s premise on the retained net: last direction versus 45°, and the containment inequality for the scaled Hämäläinen squares | last direction 45.000043°, allowance 0.0059°; λ = 0.997804 ≥ 0.997699 |

Cross-checks: the contact inventory agrees with exp-013 (14 zero-gap pairs, 20 wall
corner coordinates = 9 flush × 2 + 2 points) and with the PR108 review’s seven segments;
the modulus arithmetic reproduces `ρ_uniform = 2κ/K = 0.002309` from BC-199’s `κ` and
`K`.

## 3. Obstructions — what does not work, and why

1. **Minimality lemmas are not dilation-stable.** Everything in §1.2–1.4 holds at the
   unknown side `s(11)`, and a certificate is run at a fixed rational side.
   Lemma T is the only bridge, and it costs `0.011` of contact tolerance at 3.84. Any
   session that proves a structural lemma and hands it to a certificate must state the
   lemma in δ-robust form.
2. **The fractional plateau governs every dot route.** By Lemma D a conditional or
   capture certificate exists exactly when the *restricted* fractional packing value is
   below the threshold.
   The record knows `9.908 ≤ ν*(3.82) ≤ 11.056` (BC-200) and nothing converged at
   3.84–3.85. If `ν*(3.84) ≥ 11` with diffuse weight — which the round-11 restricted
   optima at 3.82 suggest — then conditioning on one square’s box buys at most the ≈ 1
   unit of weight the box removes (Corollary D4), and the whole of route (b) must come
   from compatibility cuts (integer-hull inequalities), not from boxes.
3. **Shrink caps.** Plain certificate: `3.868983`. Capture: `3.876681` (Corollary D3).
   Both are below `U`; nothing with `B < 0.9978` reaches the endpoint.
   `B = 1` removes these two caps and leaves the plateau.
4. **No lemma forces positive-length contacts, axis alignment or angular rank.** Göbel’s
   `n = 5` and the `n = 6` rattler are the counterexamples to any all-`n` statement; at
   `n = 11` the corner-blocker geometry (X-019) shows a 45° square snug in a corner
   blocks the box while touching nothing flush.
   H-121 (some minimizer has angles in `{0, θ}`) remains the key OPEN normal-form
   statement and no motion argument for it is in sight.
5. **The intermediate tier has no instrument and no size estimate.** Between the modulus
   ball (`ρ_row = 0.0040`, or `0.054` at target 3.84) and any conditioning radius the
   tools could reach (`≥ 0.3` before a box removes a unit of fractional weight), uniform
   boxes in the 33-chart number `(0.3/0.004)^33 ≈ 10^62`. Krawczyk-type contraction
   needs radius `≈ κ/K ≈ 10⁻³ < ρ0`, so it does not extend the ball.
   Only exact fixed-angle LPs over enumerated SAT branches could fill the tier, and
   their raw count is `4^25 · 8^30 ≈ 10^42` even inside the axis-plus-one-angle family
   (hybrid review).
6. **“Narrow enough” is the wrong frame.** Narrowing the target band `[L1, U]` from 3.84
   to 3.869 shrinks the discard ball (0.054 → 0.025), weakens the composition forcing
   (θ0 2.44° → 1.97°), and does not touch the competitor question.
   The width of the band enters a proof only through Lemma 1’s mass gap `ε(L)`, and
   BC-201 showed the tight set at `ε = 0.01` is still `0.76%` of the cells with positive
   area — a search, not a check.

## 4. Part II — architecture, status of the six measurements, and the three routes

### 4.1 Layers as the repository envisions them

| Layer | Proved today | Measured | Missing | Decisive measurement |
| --- | --- | --- | --- | --- |
| Certificate ladder (T-018/T-022) | `s(11) ≥ 3.810026`; ceiling and cap theorems | restricted optima 11.000/11.056 at 3.82, 11.23 unconverged at 3.85; `ν*(3.82) ≥ 9.908` | the true `ν*(L)` for `L ∈ [3.82, 3.87]` | X-014 #1 (BC-200): run, inconclusive |
| Lemma 1 tight cores / exact cover | Lemma 1, Corollaries 1a/1b | tight set 4.08% at `ε = 1/20`, positive area, 22,132 components (BC-201/exp-063) | an exact-cover engine (BC-207/BC-248 blocked on guards) | X-014 #3: run; reading “search” |
| Class certificates (Lemma 3) | `classcert.py`; composition (11,0) closed at Trump’s side by 19 near-axis cells; nine-point closes `n1 ≤ 1` below U | two-end-cell class refuted by the shrink cap (exp-064); 12 compositions price 5.5 min at grid 39 | compositions with ≥ 2 tilted squares at 3.84 (BC-286 planned, unrun) | X-014 #4: partial |
| Conditional certificates (Lemma 2) | the lemma; Lemma D above bounds its reach | BC-200 family restricted: ≥ 8.87 outside a corner box (this report) | non-convex admissible domain in sweep/generate/interval/colgen (BC-204 blocked) | X-014 #5 handshake: never run; #6 n = 13 calibration: never run (BC-205 blocked; BC-211 unconverged) |
| Local theorem at Trump (H-022) | exp-013 (128 zero cones), BC-199/BC-240 radius `ρ_row = 0.0040426`, `C_row = 12.873`, BC-241 review complete | — | independent replay of per-face witnesses (BC-240 refusal list); a radius in a chart with side free | X-014 #2: run; kill did not fire |
| Near-axis / near-45 auxiliaries (H-036 programme) | H-106, H-108, H-109, H-123, H-124 accepted at 1939/500 under premises | P12 escape (exp-121) refutes the unconditional near-axis 12-point cover; diamond cover refuted (exp-122) | H-036 itself; axis compatibility `no_chain` | — |
| Global capture (H-103) | typed-backbone packet BC-245 (obligations, no proofs) | — | everything | — |

### 4.2 Quantifying “narrow enough” (CHECKED arithmetic)

| `L1` | band `U − L1` | discard radius `(η/C_row)^{1/2}` | θ0(L1) | Lemma T tolerance at `L1` | fraction of gap removed |
| --- | --- | --- | --- | --- | --- |
| 3.84 | 0.0371 | 0.0537 | 2.44° | 0.0111 | 44.7% |
| 3.86 | 0.0171 | 0.0364 | 2.12° | 0.0186 | 74.5% |
| 3.869 | 0.0081 | 0.0251 | 1.97° | 0.0219 | 87.9% |
| → U | 0 | floor 0.0040 | 1.85° | — | — |

Every column that a case tree consumes gets *worse* as `L1 → U`. The set of packings
with side in `[L1, U]` is, for all we know, empty except Trump’s orbit; a proof must
exhibit that, and its cost is set by how much of configuration space a general argument
can discard *at side `U`*, not by `U − L1`.

### 4.3 The three closing routes, their case trees, and the lemma that would change each

**(a) Trump’s combinatorial type, then exact algebra.** Closing step: given the 25
incidences with a feature selection, the 42 rows have rank 33 (exp-013), so the pose is
an isolated real solution; all real solutions of the contact system are finitely many
and each is checked for feasibility over `Q(u)` (the Gensane–Ryckelynck/Ellsworth
elimination; the degree-8 polynomial has finitely many real roots).
This step is cheap.
The premise — every packing at side `≤ U` has Trump’s type — *is* the
theorem.
Tree size without structure: choosing ~22 active rows among ≈ 44 wall rows and ≈
440 typed pair features, `C(484, 22) ≈ 10^40` raw; with H-121 (angles in `{0, θ}`) the
SAT product is `4^25 · 8^30 ≈ 10^42` raw (hybrid review), most infeasible but unproved
so. **The single lemma that changes the estimate most is an ownership (localization)
lemma:** an unavoidable set of 11 marks (or 10 marks with a forced double owner, as in
Stromquist’s Theorem 1 at `n = 10`) at side 3.84 (robustly, Lemma T). With every square
localized to within ≈ 1 of a known mark, each square has ≤ 4–6 possible neighbours and
most separating axes are determined by geometry; the cell count drops to roughly
`2^{20}` fixed-angle LPs — feasible.
Evidence against getting it cheaply: exp-121’s escape at 3.878 for the near-axis
12-point cover, and the fact that the *weighted* certificate at 3.81 needs 1121 atoms of
total mass 10.86 where an integral ownership set would need ≤ 11 marks of mass 1.

**(b) Conditional certificates on a finite cover + the modulus ball.** Tree:
compositions (12; ≈ 10³ with five angle bins) × position boxes; a box helps only when
`I_b` removes ≈ 1 unit of fractional weight (radius ≲ 0.3), giving ≈ 160 boxes per
square, `160^{11} ≈
10^{24}` ordered (≈ 10^{17} unordered) before any pruning, `≈ 8^{11} ≈ 10^{10}` if only
the 5% near-tight region of BC-201 need be boxed, at minutes per node.
Not a plan without adaptive pruning whose rate is exactly the unrun handshake (#5). The
structural constraints that collapse it: four distinct corner blockers (X-019) fix four
boxes at once; nine-point and the X-018 strict-core lemmas fix the composition side;
Lemma S fixes an anchor chain.
**The lemma that changes the estimate most is a valid integer-hull cut family** — subset
capacities and clique cuts such as “at most one square meets the corner triangle
`x + y ≤ ε`” (X-019, valid for packings, violable by fractional packings) — sufficient
to push `ν*(3.84)` below 11. Lemma D says this is the *only* way conditioning can beat
the plateau.

**(c) Shrink-free certificate (B = 1, open placements, interval-decided directions).**
Removes both shrink caps and can approach `U` rung by rung, and `s(11) ≥ sup L = U`
would follow from `τ*_1(L) < 11` for all `L < U` — but that requires infinitely many
rungs or a parametric family, and the covering value of the `B = 1` relaxation may still
cross 11 below `U` (its own plateau).
Tree size: none (it is a ladder), but each rung is a new soundness surface (open
placements, event-grid semantics on lines, directions as intervals).
**The decisive measurement is `ν*_1(L)` for `L ∈ {3.84, 3.86, 3.87}` with unit closed
placements**, computable today with `ceiling.py`’s `unit` regime and the cutting-plane
loop; a value `≥ 11` at any `L < U` kills (c) and, by Lemma D, every `B = 1` capture
certificate at that side.

## 5. Proposed research sessions (2–4 h each, parallelizable), with dependency graph

Common falsifier discipline: a lemma “for every packing at side ≤ L” is refuted only by
an explicit packing at side ≤ L or by refuting the method; Trump and its D4 images are
the only packings below `U`; loosened packings at 3.88–3.90 test lemmas whose proof
would also apply there.

### S1 — Rectangle no-fit certificates and the wall-proximity lemma

*Question.* What is the largest `H0 < 3.84` such that eleven unit squares provably do
not fit in `[0, 3.84] × [0, H0]`? Equivalently: in every packing at side ≤ 3.84, how
close must some square come to each wall?
*Entry.* `sqpack.fractional` at the retained net; the change is confined to
`sweep.centre_domain` (rotated rectangle instead of rotated square), the float mirror
`generate._CentreDomain` (separate x/y bounds in `_floor/_ceiling/u_chord`), the four
half-planes of `interval.DirectionSearch`, and Condition 1’s symmetry group (rectangle:
the two reflections only, so the net must span a quarter turn; the doubled net exists).
*Instrument.* Column generation at `3.84 × H` for `H ∈ {3.80, 3.81, 3.815, 3.82}`; exact
decision by the sweep and the interval route as for T-018. *Exit.* A frozen rectangle
certificate at some `H0 ≥ 3.81` ("theorem: 11 unit squares do not fit in `3.84 × H0`"),
or the converged restricted optimum ≥ 11 at `H = 3.81` (scoped obstruction: no rectangle
gain at this net). *Falsifier.* A verified packing in `3.84 × H0` (none is known below
the square side). *Buys for 3.84.* Robust structural facts: every wall is within
`3.84 − H0` of a square, both directions have extent ≥ `H0`, hence (with Lemma S) the
anchor chain plus near-contacts on the other two walls — the strongest symmetry-breaking
premise available, and the first rectangle-container bound for `n = 11`. Also settles
whether a both-directions spanning representative can be *forced* at 3.84 (it can if
`H0` can be pushed to 3.84 − δ). *Hours.* 3–4. *Depends on.* nothing.
*Parallel with.* S2, S3, S4, S6.

### S2 — Fractional-packing kill tests for conditional dots at 3.84 (Lemma D1)

*Question.* Over placements disjoint from (i) a unit corner box, (ii) the corner
triangle `x + y ≤ 1/2`, (iii) a unit box at the centre, and (iv) the union of the four
corner boxes, what is the exact-depth fractional packing value at `96/25`? Does any
reach 10 (kill) or stay below 9.5 (headroom)?
*Entry.* `bc-200-family-191-50.json` (760 placements, depth ≤ 1) and
`bc-200-state-191-50.json` as warm start; `sqpack.fractional.cutting.cutting_plane_loop`
with the placement generator filtered by disjointness from the region (a filter on the
dual side needs no domain generalization).
*Instrument.* Cutting-plane loop ≤ 30 min per region on one core; `verify_ceiling` on
the final family (exact depth at all arrangement vertices).
*Exit.* Per region an exact depth-scaled total; classification: kill (≥ 10), alive (<
9.5), undecided. Also the unrestricted `ν*(3.84)` lower bound as a by-product.
*Falsifier.* None needed: both outcomes are theorems about the relaxation.
*Buys for 3.84.* Decides whether BC-204’s non-convex-domain instrument is worth building
for corner-box conditioning at all; converts BC-285/BC-287 from speculation to a priced
plan; a kill redirects effort to integer-hull cuts (H-111, H-119). *Hours.* 2–3.
*Depends on.* nothing.
*Gates.* the conditional-dot instrument (BC-204) and S5’s premise.

### S3 — The `B = 1` relaxation’s fractional value near `U`

*Question.* With closed unit placements (`ceiling.py` `unit` regime) at
`L ∈ {3.84, 3.86,
3.87}`, is there a depth-1 family of value ≥ 11? If so, how much of its weight lies
outside an angular/positional neighbourhood of Trump’s placements (radius 0.05 in
centres, 1° in angle, D4 images included)?
*Entry.* The cutting-plane loop with `square_side = 1`; a direction net dense near 0°
and 40.18° so Trump’s own placements are representable; the BC-200 state as seed after
rescaling placements’ *positions* only (sizes are fixed at 1, so the seed is a warm
start, not a valid family, until re-verified).
*Exit.* A verified family of value ≥ 11 at some `L < U` (kills route (c) and every
`B = 1` capture certificate at that side, Lemma D2, if its outside-`N` weight is ≥ 1),
or a converged covering LP below 11 at 3.87 with `B = 1` (opens route (c): the first
rung above the shrink cap).
*Falsifier.* An exact-depth verification failure on the produced family is the only
refutation of a claimed kill.
*Buys for 3.84.* Nothing directly at 3.84; it is the earliest possible hopelessness
signal for the dot-based endgame (a diffuse value-11 family at 3.87 means no one-body
relaxation can reach `U`, capture included).
*Hours.* 3–4. *Depends on.* nothing.
*Gates.* S5.

### S4 — Corner blockers made quantitative (H-126 sharpened)

*Question.* For the SW corner box `[0,1]²` and its unique-or-several blockers, classify
the blocker poses that overlap every probe `[0,1] × [t, 1+t]`, `t ∈ [0, 0.5]`, and every
probe `[t, 1+t] × [0,1]` (insertion saturation along both walls): is there a uniform
inequality of the form “either a square meets the corner triangle `x + y ≤ ε0` with
`ε0 ≥ 0.15`, or at least two distinct squares meet the corner box, one within angle `φ0`
of an axis”? The falsifier is a local configuration (three or fewer squares) that blocks
all probes while violating the inequality; the analytical tool is X-019’s identity
`min_{p∈Q}(x + y) = g_x + g_y + sin φ`. *Entry.* X-019’s proved four-blocker fact;
T-017; the probe family is finite-dimensional and the blocker’s pose has three
parameters, so exhaustive interval enumeration of blocker poses is feasible with
`sqpack.cover` primitives.
*Exit.* A proved dichotomy with explicit constants (theorem), or an explicit blocking
configuration that defeats every dichotomy of that shape (scoped obstruction, closing
this lead). *Falsifier.* The 45° snug corner square (X-019) already defeats “penetration
alone”; the session must produce a statement that survives it.
*Buys for 3.84.* If the dichotomy holds, each corner contributes either a captured
triangle (a fixed region every certificate can weight heavily: mass there is captured by
exactly one core) or a second localized square — both are integer-hull information
usable as cuts in S2’s sense.
This is the cheapest structural constraint with a real chance of headroom.
*Hours.* 3–4, pure mathematics plus a small enumeration.
*Depends on.* nothing.
*Parallel with.* S1–S3, S6.

### S5 — The sound closing design and its price

*Question.* Write the exact-side tree over `Q(u)` and the `B = 1` capture design at
`U + σ` as one architecture: (i) prove the feasible-set stability `‖v‖ ≤ 2σ/κ` on the
half-ball (the argument in §1.7, in the anchored chart with the retained `κ`, `K`); (ii)
compute `σ_max = κρ0/4` and a rational `L1 ∈ (U, U + σ_max)`; (iii) enumerate the
features whose gap at Trump’s pose is below the capture radius `r` (from the exact pose:
the gaps `0.0249, 0.0249, 0.0326, 0.119, …`) to count the SAT branches active in the
annulus `[ρ0/2, r]`; (iv) price the field-valued LP per branch with `sqpack.exact_lp`.
*Exit.* A costed design (number of branches × exact LP cost) for `r ∈ {0.05, 0.1, 0.3}`,
or the proof that the annulus needs angle subdivision below what the exact LP tolerates.
*Falsifier.* A packing at side `U + σ` outside the predicted region (from the numerical
quench, `sqpack.research.quench`) refutes the stability lemma as stated.
*Buys for 3.84.* Nothing; it is the only session that addresses the *endpoint* honestly.
*Hours.* 2–3. *Depends on.* S3’s answer for whether capture at `U + σ` is even possible
with `B = 1` (if S3 kills it, S5 reduces to the exact-side tree and needs an ownership
lemma from S6 to be finite).

### S6 — An ownership set at 3.84 (Stromquist’s method at the target side)

*Question.* Is there a set of ≤ 11 marks (points or short segments) in `[0, 3.84]²` such
that every contained unit square, at any angle, meets one of them, with the nonavoidance
regions proved by Lemmas 1–4 of Stromquist 2003 (as repaired for Figure 14) and
H-106-style interval readers, *robustly* (Lemma T: marks may be thickened by 0.006)?
*Entry.* T-018’s 93 heaviest atoms (mass > 1/50, carrying 4.28 of 10.86) as candidate
marks; the exp-121 escape instrument as the falsifier engine; `sqpack.cover` for the
mesh checks. *Exit.* An 11-mark unavoidable set with a verified cover (theorem: every
packing at side ≤ 3.84 is localized; the tree of route (a) becomes ≈ 2^20 exact LPs), or
a catalogue of escape squares showing that every ≤ 11-mark set built from the atom
skeleton is avoidable (scoped obstruction with the escape geometry recorded).
*Falsifier.* Any contained unit square avoiding all marks.
*Buys for 3.84.* Everything, if it succeeds; prior ≈ 30% (Stromquist needed 12 marks and
a forced triple at 3.789, and exp-121 found escapes at 3.878). *Hours.* 4. *Depends on.*
nothing. *Parallel with.* all.

### Dependency graph

```
S1 (rectangle / walls)  ──┐
S2 (Lemma-D kill tests) ──┼──> BC-204 instrument decision ──> conditional-dot programme (agenda 029)
S4 (corner dichotomy)   ──┘                                    │
S3 (B = 1 value near U) ──────> S5 (closing design) <──────────┘
S6 (ownership at 3.84)  ──────> route (a) tree size; feeds S5 if S3 kills capture
```

S1, S2, S3, S4, S6 run in parallel on separate cores (S1–S3 need one core each for ≤
30-min LP loops; S4 and S6 are mostly mathematics).
S5 starts after S3’s first result (about two hours in).

## 6. Honest assessment

**Achievable now, in single 2–4 h sessions (proof-of-concept that constraints can be
proved).** Lemma S, Corollary C, Lemma V, Lemma T and Lemma D (this report, about three
hours including checks); S1’s wall-proximity theorem (moderate risk, the instrument
change is bounded and convex); S2’s kill-or-headroom classification (no risk, both
outcomes are theorems); S4’s corner dichotomy (real risk of a counter-configuration,
which would itself be a useful obstruction).
None of these moves the lower bound; S1 is the only one that could produce a new
published-style theorem (a rectangle no-fit) this week.

**Not achievable in sessions of this size.** H-121 (normal form), any lemma forcing
positive-length contacts or angular rank, the ownership set at 3.84 as a theorem (S6 is
a probe, not a proof plan), and the intermediate tier.

**Realistic multi-session path to s(11) = U.**

1. *Weeks 1–2:* S2, S3, S4 decide which relaxation survives.
   If `ν*(3.84) ≥ 11` with diffuse weight, the covering LP must be strengthened by
   integer-hull cuts (corner-triangle cliques, subset capacities, composition rows)
   until it certifies 3.84; that is a publishable rung and the first evidence that
   structure buys headroom.
2. *Months:* push the strengthened `B = 1` ladder toward `U`, measuring `ν*_1(L)` at
   each rung; in parallel attack ownership (S6) with the strengthened measure’s heavy
   atoms as marks.
3. *Endpoint:* only two designs are sound (§1.7): the exact-side tree over `Q(u)`
   finished by the modulus lemma, which is finite only with an ownership or normal-form
   theorem; or the `B = 1` capture run at `U + σ`, `σ < 10⁻⁵`, which needs the
   strengthened relaxation to have no diffuse value-11 fractional packing at `U`.

**Earliest point at which hopelessness could be known.** S3 within one session: a
verified depth-1 family of value ≥ 11 at `L ≤ 3.87` with ≥ 1 unit of weight away from
Trump’s placements proves, by Lemma D2, that no one-body certificate — shrunk or not,
unconditional or conditioned on Trump’s neighbourhood — can close the endpoint; every
subsequent dot-based step then depends on cuts whose sufficiency is unproved.
Route (a) has no comparable kill: a normal-form theorem could always exist, and the only
practical refutation is a second local minimizer near `U` with a different contact type,
which 47 years of search have not produced.

## 7. Open questions ranked by expected value

1. **Ownership at 3.84** (S6): is there an ≤ 11-mark robust unavoidable set?
   Highest value — collapses route (a) to ≈ 10⁶ exact LPs; prior ≈ 30%.
2. **`ν*(3.84)` and `ν*_1(3.87)`** (S2, S3): the numbers that decide routes (b) and (c)
   and the endgame’s capture premise; certain to be answered by measurement.
3. **Both-direction spanning representative / rectangle bound `H0`** (S1): a new theorem
   type with structural corollaries; probability of `H0 ≥ 3.81` high, of `H0 ≥ 3.83`
   unknown.
4. **Corner dichotomy** (S4): the cheapest integer-hull cut with geometric content;
   prior 50%.
5. **A flush-wall or axis-aligned square in some minimizer** (OPEN): plausible, no
   method; a proof would fix one absolute angle and delete 1/11 of the angular
   dimensions.
6. **H-121 normal form**: decisive and out of reach; keep as the statement every partial
   result should be measured against.
7. **Angular rattler exclusion at side ≤ 3.96** (conditional certificate with `I_b` a
   disc of radius √2/2): provable by Lemma-D-style accounting if
   `ν*(container ∖ disc) < 10`; low value, but it removes the `n = 6`-type degeneracy
   from Lemma V’s representative argument.

## Appendix — status of X-014’s six measurements

| # | Measurement | Cell | Status | Outcome and kill |
| --- | --- | --- | --- | --- |
| 1 | `ν*(L)` at 3.82/3.85/3.87 | BC-200 (exp-060) | run, unconverged | `9.9079 ≤ ν*(3.82)`, restricted `τ* = 11.0556` on 12,761 sites; 3.85 at `9.0499` after three iterations; 3.87 never run. No kill defined; the ladder’s top is unlocated |
| 2 | `κ_b`, `K`, `ρ0`, `C` | BC-199, packet BC-240, review BC-241 | complete | `ρ_uniform = 0.0023089`, `ρ_row = 0.0040426`, `C_uniform = 22.4678`, `C_row = 12.8731`; kill (`ρ0 < 10⁻⁶`) did not fire; per-face witnesses not independently replayed |
| 3 | tight-cell census | BC-201 (exp-063) | complete | 4.0754% at `ε = 1/20`; positive area, bounding box = whole domain, 22,132 components; H-065 accepted; the reading is “search”; kill (most of the domain) did not fire |
| 4 | twelve class certificates just above `U` | BC-198 (exp-064) | partial | (11,0) closed at Trump’s side (exact 39123/4096); two-end-cell class unreachable (cap 3.876681); the kill condition ("`n1 = 0` fails to certify above `U`") did not fire for the 19-cell class and fired by arithmetic for the two-end-cell class |
| 5 | handshake at `U − 0.01`, all squares boxed at 0.05 | BC-204 | blocked, never run | needs the non-convex admissible domain in four places; Lemma D and S2 now give a cheaper necessary condition before building it |
| 6 | `n = 13` Bentz calibration at 399/100 | BC-205 (BC-211 precursor) | blocked / unconverged | BC-211’s grid rung at 399/100 never converged inside its wall; the conditional calibration never opened |

## Appendix: scripts and outputs as run

Retained verbatim from the lane’s working directory on 2026-09-08. Scripts that import
`sqpack` were run through the project environment; the rest are standard-library Python.
None has been promoted to `devtools/`; the first lane that reuses one owns that
promotion.

### `chain_arithmetic.out`

```text

=== spanning chain at side L = 3.84
  minimal chain length k >= L/sqrt2 = 2.7153 => k >= 3
  k = 3: every width >= 1.01157 (tilt >= 0.667 deg),
         two widths >= 1.21289 (tilt >= 14.053 deg),
         one width  >= 1.28000 (tilt >= 19.836 deg)
  k = 3 with an axis-aligned square (width 1): other two need >= 2.8400 > 2 sqrt2 = 2.8284? impossible
  k = 4: three axis-aligned squares (width 3) leave 0.840 <= 1 for the fourth => no tilt forced
  k = 4: all four axis-aligned: width 4 >= 3.84: allowed

=== spanning chain at side L = 3.86
  minimal chain length k >= L/sqrt2 = 2.7294 => k >= 3
  k = 3: every width >= 1.03157 (tilt >= 1.839 deg),
         two widths >= 1.22289 (tilt >= 14.850 deg),
         one width  >= 1.28667 (tilt >= 20.479 deg)
  k = 3 with an axis-aligned square (width 1): other two need >= 2.8600 > 2 sqrt2 = 2.8284? impossible
  k = 4: three axis-aligned squares (width 3) leave 0.860 <= 1 for the fourth => no tilt forced
  k = 4: all four axis-aligned: width 4 >= 3.86: allowed

=== spanning chain at side L = 3.869
  minimal chain length k >= L/sqrt2 = 2.7358 => k >= 3
  k = 3: every width >= 1.04057 (tilt >= 2.375 deg),
         two widths >= 1.22739 (tilt >= 15.215 deg),
         one width  >= 1.28967 (tilt >= 20.774 deg)
  k = 3 with an axis-aligned square (width 1): other two need >= 2.8690 > 2 sqrt2 = 2.8284? impossible
  k = 4: three axis-aligned squares (width 3) leave 0.869 <= 1 for the fourth => no tilt forced
  k = 4: all four axis-aligned: width 4 >= 3.869: allowed

=== spanning chain at side L = 3.877083590022814
  minimal chain length k >= L/sqrt2 = 2.7415 => k >= 3
  k = 3: every width >= 1.04866 (tilt >= 2.860 deg),
         two widths >= 1.23144 (tilt >= 15.547 deg),
         one width  >= 1.29236 (tilt >= 21.041 deg)
  k = 3 with an axis-aligned square (width 1): other two need >= 2.8771 > 2 sqrt2 = 2.8284? impossible
  k = 4: three axis-aligned squares (width 3) leave 0.877 <= 1 for the fourth => no tilt forced
  k = 4: all four axis-aligned: width 4 >= 3.877083590022814: allowed

=== nine-point threshold theta0(s), cos+sin = 4/s
  s = 3.820000: theta0 = 2.768 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)
  s = 3.840000: theta0 = 2.440 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)
  s = 3.860000: theta0 = 2.118 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)
  s = 3.869000: theta0 = 1.974 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)
  s = 3.877084: theta0 = 1.847 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)
  s = 3.960000: theta0 = 0.582 deg   (tan band |tan| <= 1/24 at 3.84: cos+sin at atan(1/24) = 1.04076 vs 4/3.84 = 1.04167)

=== robust transfer tolerance from L_low to q
  q = 3.84: lambda = 1.007867; centre-to-centre slack (lambda-1)*sqrt2 = 0.01113; wall slack (lambda-1)/sqrt2 = 0.00556; side-length slack lambda-1 = 0.00787
  q = 3.86: lambda = 1.013117; centre-to-centre slack (lambda-1)*sqrt2 = 0.01855; wall slack (lambda-1)/sqrt2 = 0.00927; side-length slack lambda-1 = 0.01312
  q = 3.869: lambda = 1.015479; centre-to-centre slack (lambda-1)*sqrt2 = 0.02189; wall slack (lambda-1)/sqrt2 = 0.01095; side-length slack lambda-1 = 0.01548

=== local discard radius at target side U - eta (sup norm, anchored 33-chart)
  L1 = 3.84: eta = 0.037084; (eta/C_row)^(1/2) = 0.05367; (eta/C_uniform)^(1/2) = 0.04063; floor rho_row = 0.00404, rho_uniform = 0.00231
  L1 = 3.85: eta = 0.027084; (eta/C_row)^(1/2) = 0.04587; (eta/C_uniform)^(1/2) = 0.03472; floor rho_row = 0.00404, rho_uniform = 0.00231
  L1 = 3.86: eta = 0.017084; (eta/C_row)^(1/2) = 0.03643; (eta/C_uniform)^(1/2) = 0.02757; floor rho_row = 0.00404, rho_uniform = 0.00231
  L1 = 3.869: eta = 0.008084; (eta/C_row)^(1/2) = 0.02506; (eta/C_uniform)^(1/2) = 0.01897; floor rho_row = 0.00404, rho_uniform = 0.00231
  L1 = 3.875: eta = 0.002084; (eta/C_row)^(1/2) = 0.01272; (eta/C_uniform)^(1/2) = 0.00963; floor rho_row = 0.00404, rho_uniform = 0.00231
  modulus 2 kappa / K_uniform = 0.002309 (= rho_uniform check)
  per-feature gap cap = 0.005876: beyond this distance new contacts can appear

=== linear allowance above U: at side U + sigma the first-order rows permit |v| up to ~ sigma / kappa
  sigma = 0.0001: sigma/kappa = 0.0087  (>> rho_row = 0.0040 once sigma > 4.64e-05)
  sigma = 0.001: sigma/kappa = 0.0871  (>> rho_row = 0.0040 once sigma > 4.64e-05)
  sigma = 0.01: sigma/kappa = 0.8711  (>> rho_row = 0.0040 once sigma > 4.64e-05)

=== shrink caps for B = 9977/10000
  plain certificate cap U*B*(cos d + sin d) = 3.868983
  {0,45} class cap B*(2+(4/3)sqrt2) = 3.876681  (< U by 0.000402); U/B = 3.886021 > 3.885618
  at q = 3.84: q/B = 3.848852 < 3.885618: the {0,45} packing does not enter
  B needed for the {0,45} cap to reach U: B >= U/(2+(4/3)sqrt2) = 0.997804

=== how much of the gap the three targets remove
  q = 3.84: removes 44.7% of [L_low, U]; remaining band 0.037084
  q = 3.86: removes 74.5% of [L_low, U]; remaining band 0.017084
  q = 3.869: removes 87.9% of [L_low, U]; remaining band 0.008084
```

### `chain_arithmetic.py`

```text
"""Arithmetic behind the report's quantitative claims (plain python3, no dependencies).

1. Spanning-chain projection bounds at q = 3.84 (and 3.86, 3.869, U).
2. Nine-point threshold angle theta0(s) with cos + sin = 4/s.
3. Robust-transfer tolerance delta(q) = (q / L_low - 1) * sqrt 2.
4. Discard radii (eta / C)^(1/2) from BC-199's constants, and the linear allowance
   sigma / kappa above U.
5. Shrink caps: plain certificate cap U*B*(cos d + sin d) and the {0,45}-class cap
   B * (2 + (4/3) sqrt 2) that also caps any capture certificate with B = 9977/10000.
"""
import math

SQ2 = math.sqrt(2)
U = 3.877083590022814
L_LOW = 3.810025723614703
B = 0.9977
KAPPA = 0.011480272061506444        # smaller modulus class (BC-199)
K_UNIFORM = 4972105219 / 500000000  # 9.944210
RHO_UNIFORM = 288616983 / 125000000000
RHO_ROW = 808514697 / 200000000000
C_UNIFORM = 2808470331 / 125000000
C_ROW = 2574612531 / 200000000
GAP_CAP = 5875508797 / 1000000000000


def tilt_from_width(w):
    """Folded tilt (deg) with cos t + sin t = w, w in [1, sqrt 2]."""
    w = min(max(w, 1.0), SQ2)
    return math.degrees(math.asin(w / SQ2)) - 45.0


def chain_bounds(L):
    print(f"\n=== spanning chain at side L = {L}")
    kmin = math.ceil(L / SQ2 - 1e-12)
    print(f"  minimal chain length k >= L/sqrt2 = {L / SQ2:.4f} => k >= {kmin}")
    # k = 3: widths w1+w2+w3 >= L, each <= sqrt2, each >= 1
    w_all = L - 2 * SQ2          # every one of the three
    w_two = (L - SQ2) / 2        # at least two exceed this
    w_max = L / 3                # at least one exceeds this
    print(f"  k = 3: every width >= {w_all:.5f} (tilt >= {tilt_from_width(w_all):.3f} deg),")
    print(f"         two widths >= {w_two:.5f} (tilt >= {tilt_from_width(w_two):.3f} deg),")
    print(f"         one width  >= {w_max:.5f} (tilt >= {tilt_from_width(w_max):.3f} deg)")
    print(f"  k = 3 with an axis-aligned square (width 1): other two need >= {L - 1:.4f} > 2 sqrt2 = {2 * SQ2:.4f}? "
          f"{'impossible' if L - 1 > 2 * SQ2 else 'possible'}")
    # k = 4: three axis-aligned and one arbitrary?
    print(f"  k = 4: three axis-aligned squares (width 3) leave {L - 3:.3f} <= 1 for the fourth => no tilt forced")
    print(f"  k = 4: all four axis-aligned: width 4 >= {L}: allowed")


def nine_point(s):
    w = 4 / s
    th = tilt_from_width(w)
    return th


def main():
    for L in (3.84, 3.86, 3.869, U):
        chain_bounds(L)

    print("\n=== nine-point threshold theta0(s), cos+sin = 4/s")
    for s in (3.82, 3.84, 3.86, 3.869, U, 3.96):
        print(f"  s = {s:.6f}: theta0 = {nine_point(s):.3f} deg   (tan band |tan| <= 1/24 at 3.84: "
              f"cos+sin at atan(1/24) = {math.cos(math.atan(1/24)) + math.sin(math.atan(1/24)):.5f} vs 4/3.84 = {4/3.84:.5f})")

    print("\n=== robust transfer tolerance from L_low to q")
    for q in (3.84, 3.86, 3.869):
        lam = q / L_LOW
        print(f"  q = {q}: lambda = {lam:.6f}; centre-to-centre slack (lambda-1)*sqrt2 = {(lam - 1) * SQ2:.5f}; "
              f"wall slack (lambda-1)/sqrt2 = {(lam - 1) / SQ2:.5f}; side-length slack lambda-1 = {lam - 1:.5f}")

    print("\n=== local discard radius at target side U - eta (sup norm, anchored 33-chart)")
    for L1 in (3.84, 3.85, 3.86, 3.869, 3.875):
        eta = U - L1
        r_row = math.sqrt(eta / C_ROW)
        r_uni = math.sqrt(eta / C_UNIFORM)
        print(f"  L1 = {L1}: eta = {eta:.6f}; (eta/C_row)^(1/2) = {r_row:.5f}; (eta/C_uniform)^(1/2) = {r_uni:.5f}; "
              f"floor rho_row = {RHO_ROW:.5f}, rho_uniform = {RHO_UNIFORM:.5f}")
    print(f"  modulus 2 kappa / K_uniform = {2 * KAPPA / K_UNIFORM:.6f} (= rho_uniform check)")
    print(f"  per-feature gap cap = {GAP_CAP:.6f}: beyond this distance new contacts can appear")

    print("\n=== linear allowance above U: at side U + sigma the first-order rows permit |v| up to ~ sigma / kappa")
    for sigma in (1e-4, 1e-3, 1e-2):
        print(f"  sigma = {sigma}: sigma/kappa = {sigma / KAPPA:.4f}  (>> rho_row = {RHO_ROW:.4f} once sigma > {KAPPA * RHO_ROW:.2e})")

    print("\n=== shrink caps for B = 9977/10000")
    d_net = math.radians(0.012100)  # Trump tilt offset from net index 159 (X-014)
    cap_plain = U * B * (math.cos(d_net) + math.sin(d_net))
    stromq = 2 + (4 / 3) * SQ2
    cap_capture = B * stromq
    print(f"  plain certificate cap U*B*(cos d + sin d) = {cap_plain:.6f}")
    print(f"  {{0,45}} class cap B*(2+(4/3)sqrt2) = {cap_capture:.6f}  (< U by {U - cap_capture:.6f}); U/B = {U / B:.6f} > {stromq:.6f}")
    print(f"  at q = 3.84: q/B = {3.84 / B:.6f} < {stromq:.6f}: the {{0,45}} packing does not enter")
    print(f"  B needed for the {{0,45}} cap to reach U: B >= U/(2+(4/3)sqrt2) = {U / stromq:.6f}")

    print("\n=== how much of the gap the three targets remove")
    for q in (3.84, 3.86, 3.869):
        print(f"  q = {q}: removes {(q - L_LOW) / (U - L_LOW) * 100:.1f}% of [L_low, U]; remaining band {U - q:.6f}")


if __name__ == "__main__":
    main()
```

### `family_restrict.out`

```text
family: 760 placements at outer side 191/50 = 3.8200, total weight 9.907906

weight of the family DISJOINT from a closed region R, i.e. a lower bound on the
fractional packing value over cores disjoint from R at side 3.84 (weak duality):
  R = corner box SW [0,1]^2                     : weight disjoint >= 8.8732 (family anchored NE); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = corner box NE                             : weight disjoint >= 8.8732 (family anchored SW); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = corner box SE                             : weight disjoint >= 8.8732 (family anchored NW); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = corner box NW                             : weight disjoint >= 8.8732 (family anchored SE); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = central unit box                          : weight disjoint >= 7.0992 (family anchored centre); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = half-unit corner box SW [0,1/2]^2         : weight disjoint >= 9.0293 (family anchored SW); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = corner triangle x+y<=1/2 (bounding box)   : weight disjoint >= 9.0293 (family anchored SW); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = left strip x<=1/10                        : weight disjoint >= 7.2788 (family anchored SE); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)
  R = left strip x<=1/2                         : weight disjoint >= 7.2484 (family anchored SW); a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)

Reading: with ~1 unit of fractional weight available inside a unit-sized box, a
conditional certificate boxing one square there is impossible on this relaxation
whenever the disjoint weight is >= ~10.  Values near 9 leave headroom only if the
true nu* is close to this retained lower bound, which is unknown (BC-200 stopped
unconverged at 9.9079 with the restricted covering optimum at 11.0556).
```

### `family_restrict.py`

```text
"""Lower bounds on restricted fractional-packing values from the retained BC-200 family.

The BC-200 family at outer side 191/50 = 3.82 is a list of 760 weighted closed
B-squares (B = 9977/10000) at net directions with exact depth <= 1 at every
arrangement vertex (verified by sqpack.fractional.ceiling; total 9.907905...).

Two facts let it be reused without recomputation:
  (i)  placed in the corner sub-container [0, 3.82]^2 of [0, q]^2 for q >= 3.82 (or
       translated anywhere inside), the family is still depth <= 1 and admissible, so
       nu*(q) >= 9.9079 for every q >= 3.82 (weak duality, ceiling.py docstring);
  (ii) dropping placements can only lower depth, so the sub-family of placements
       DISJOINT from a region R is a depth-feasible family on the placement set
       Lambda_R = {admissible cores disjoint from R}.  Its total weight is therefore a
       lower bound on the fractional packing value over Lambda_R, and by weak duality a
       lower bound on the mass of ANY covering measure that gives mass >= 1 to every
       core in Lambda_R -- which is what X-014's Lemma 2 conditional program demands
       (plus the cores inside the boxed placements).

So: if the retained weight disjoint from R is >= 11 - c, where c bounds the fractional
weight that cores inside the box can add (<= the depth-1 capacity of the box's core
region, at most ~1.2 for a unit-box-sized region), the Lemma-2 conditional certificate
for that box is impossible on this relaxation at every side >= 3.82, whatever site set
and weights are searched.

We tabulate, for R = the four unit corner boxes (the X-019 blockers), for R = a
unit square at the centre, and for R = each of Trump's eleven placements scaled into
the container (the capture-neighbourhood question), the weight of the family that is
disjoint from R when the 3.82 family is anchored at each of the four corners of
[0, 3.84]^2 (an anchored family must be D4-symmetric for Condition 1 only when used as
a certificate; as a *packing* family any placement inside the container is admissible,
so anchoring at a corner is legitimate).

Run from packing/ with the project venv.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction

from sqpack.fractional.ceiling import Placement

Q = Fraction(96, 25)   # 3.84
FAM = "campaign/series/series-000-smoke-and-calibration/results/bc-200-family-191-50.json"


def load():
    d = json.load(open(FAM))
    outer = Fraction(d["outer_side"])
    pls = [Placement(Fraction(t), Fraction(x), Fraction(y), Fraction(w), Fraction(s))
           for (t, x, y, w, s) in d["placements"]]
    return outer, pls


def shifted(p: Placement, dx: Fraction, dy: Fraction) -> Placement:
    return Placement(p.half_tangent, p.centre_x + dx, p.centre_y + dy, p.weight, p.side)


def box_disjoint(p: Placement, x0, y0, x1, y1) -> bool:
    """Closed placement p and closed axis box [x0,x1]x[y0,y1] have disjoint closures?
    Exact separating-axis test on the box's axes and the placement's axes."""
    cs = p.corners()
    xs = [c[0] for c in cs]; ys = [c[1] for c in cs]
    if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
        return True
    ax, ay, u, bx, by, v = p.slabs()
    half = p.side / 2
    box = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for (nx, ny, c) in ((ax, ay, u), (bx, by, v)):
        vals = [nx * x + ny * y for (x, y) in box]
        if max(vals) < c - half or min(vals) > c + half:
            return True
    return False


def main():
    outer, pls = load()
    total = sum(p.weight for p in pls)
    print(f"family: {len(pls)} placements at outer side {outer} = {float(outer):.4f}, total weight {float(total):.6f}")
    shift = Q - outer  # 0.02
    anchors = {"SW": (Fraction(0), Fraction(0)), "SE": (shift, Fraction(0)),
               "NW": (Fraction(0), shift), "NE": (shift, shift), "centre": (shift / 2, shift / 2)}
    regions = {
        "corner box SW [0,1]^2": (0, 0, 1, 1),
        "corner box NE": (Q - 1, Q - 1, Q, Q),
        "corner box SE": (Q - 1, 0, Q, 1),
        "corner box NW": (0, Q - 1, 1, Q),
        "central unit box": (Q / 2 - Fraction(1, 2), Q / 2 - Fraction(1, 2), Q / 2 + Fraction(1, 2), Q / 2 + Fraction(1, 2)),
        "half-unit corner box SW [0,1/2]^2": (0, 0, Fraction(1, 2), Fraction(1, 2)),
        "corner triangle x+y<=1/2 (bounding box)": (0, 0, Fraction(1, 2), Fraction(1, 2)),
        "left strip x<=1/10": (0, 0, Fraction(1, 10), Q),
        "left strip x<=1/2": (0, 0, Fraction(1, 2), Q),
    }
    print("\nweight of the family DISJOINT from a closed region R, i.e. a lower bound on the\n"
          "fractional packing value over cores disjoint from R at side 3.84 (weak duality):")
    for name, (x0, y0, x1, y1) in regions.items():
        best = None
        for aname, (dx, dy) in anchors.items():
            w = sum(p.weight for p in pls if box_disjoint(shifted(p, dx, dy), Fraction(x0), Fraction(y0), Fraction(x1), Fraction(y1)))
            if best is None or w > best[0]:
                best = (w, aname)
        w, aname = best
        print(f"  R = {name:42s}: weight disjoint >= {float(w):.4f} (family anchored {aname}); "
              f"a Lemma-2 certificate on this box needs the covering LP below 11 - (box core capacity)")
    print("\nReading: with ~1 unit of fractional weight available inside a unit-sized box, a\n"
          "conditional certificate boxing one square there is impossible on this relaxation\n"
          "whenever the disjoint weight is >= ~10.  Values near 9 leave headroom only if the\n"
          "true nu* is close to this retained lower bound, which is unknown (BC-200 stopped\n"
          "unconverged at 9.9079 with the restricted covering optimum at 11.0556).")


if __name__ == "__main__":
    main()
```

### `net_end_check.out`

```text
net size 181 first [Fraction(0, 1), Fraction(207107, 90000000)] last 207107/500000 0.414214
last net direction = 45.000043 deg, offset from 45 deg = -0.000043 deg
Hamalainen scale lambda = U/s_H = 0.997804; B(cos d + sin d) = 0.997699; contains B-core at last net direction: True; axis squares need lambda >= B: True
max admissible offset: 0.005948 deg
```

### `net_end_check.py`

```text
"""Corollary D3 premise: the retained 181-direction net's last direction is close enough to
45 degrees that the Hamalainen {0,45} packing, scaled from side 2 + (4/3) sqrt 2 into the
Trump container, still contains a concentric B-core at a net direction in every square.

Run from packing/ with the project venv.  Output saved as net_end_check.out.
"""
import json
import math
from fractions import Fraction

d = json.load(open('campaign/series/series-000-smoke-and-calibration/results/bc-200-family-191-50.json'))
hts = [Fraction(t) for t in d['half_tangents']]
U = 3.877083590022814
B = 0.9977
sH = 2 + (4 / 3) * math.sqrt(2)
print("net size", len(hts), "first", hts[:2], "last", hts[-1], float(hts[-1]))
last_deg = 2 * math.degrees(math.atan(float(hts[-1])))
delta = 45.0 - last_deg
print(f"last net direction = {last_deg:.6f} deg, offset from 45 deg = {delta:.6f} deg")
lam = U / sH
need = B * (math.cos(math.radians(delta)) + math.sin(math.radians(delta)))
print(f"Hamalainen scale lambda = U/s_H = {lam:.6f}; B(cos d + sin d) = {need:.6f}; "
      f"contains B-core at last net direction: {lam >= need}; axis squares need lambda >= B: {lam >= B}")
print(f"max admissible offset: {math.degrees(math.asin(lam / (B * math.sqrt(2))) - math.pi / 4):.6f} deg")
```

### `trump_structure.out`

```text
side U = 3.877083590022814
folded angles (deg): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 40.181937, 40.181937, 40.181937, 40.181937, 40.181937]
x/y projection widths cos+sin: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.409216, 1.409216, 1.409216, 1.409216, 1.409216]

wall incidences (square, wall, corners on wall; 2 = flush segment, 1 = point):
  square  0 bottom corners=2 SEGMENT
  square  0 left   corners=2 SEGMENT
  square  1 bottom corners=2 SEGMENT
  square  1 right  corners=2 SEGMENT
  square  2 top    corners=2 SEGMENT
  square  3 left   corners=2 SEGMENT
  square  3 top    corners=2 SEGMENT
  square  4 top    corners=2 SEGMENT
  square  5 left   corners=2 SEGMENT
  square  7 bottom corners=1 POINT
  square 10 right  corners=1 POINT
  left  : touching [0, 3, 5], flush [0, 3, 5]
  bottom: touching [0, 1, 7], flush [0, 1]
  right : touching [1, 10], flush [1]
  top   : touching [2, 3, 4], flush [2, 3, 4]

pair contacts: 14 (exp-013 says 14)
  (0,6) POINT length=0.000000
  (1,9) POINT length=0.000000
  (2,8) POINT length=0.000000
  (2,10) POINT length=0.000000
  (3,4) SEGMENT length=1.000000
  (3,5) SEGMENT length=1.000000
  (4,5) POINT length=0.000000
  (4,8) POINT length=0.000000
  (5,6) POINT length=0.000000
  (6,7) SEGMENT length=0.975125
  (6,8) SEGMENT length=0.881217
  (7,9) SEGMENT length=0.881217
  (8,9) SEGMENT length=0.975125
  (9,10) SEGMENT length=0.666224
segment contacts: [(3, 4), (3, 5), (6, 7), (6, 8), (7, 9), (8, 9), (9, 10)] (review lists 7)
smallest strict pair gaps: [(0.024875, 6, 9), (0.024875, 8, 10), (0.032558, 2, 4), (0.118783, 7, 8), (0.231867, 0, 7), (0.236001, 1, 7)]

contact-graph components (point or segment contacts): [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

shortest left-right chain: [0, 6, 8, 9, 1]
  projection widths [1.0, 1.4092, 1.4092, 1.4092, 1.0] sum=6.2276 vs L=3.8771
  consecutive contact kinds: ['pt', 'seg', 'seg', 'pt']
  wall contacts: left=flush, right=flush

shortest bottom-top chain: [0, 6, 8, 2]
  projection widths [1.0, 1.4092, 1.4092, 1.0] sum=4.8184 vs L=3.8771
  consecutive contact kinds: ['pt', 'seg', 'pt']
  wall contacts: bottom=flush, top=flush

segment-equality components: [[0], [1], [2], [3, 4, 5], [6, 7, 8, 9, 10]]
wall-anchored squares: [0, 1, 2, 3, 4, 5]
unanchored components: [[6, 7, 8, 9, 10]] => angular rank 11 - 1 = 10
```

### `trump_structure.py`

```text
"""Trump's exact 11-square pose: wall incidences, pair contacts (segment vs point),
contact-graph components, and spanning chains between opposite walls.

Run from packing/ with the project venv:
    .venv/bin/python3 <this file>

Exact corners come from cases.trump11.packing (Q(u)); they are converted to floats
through the field's exact enclosure at 40 digits, so every classification below uses a
tolerance (1e-12) that is nine orders above the conversion error and nine orders below
the smallest strict gap at the pose (about 5.9e-3 in chart units per BC-199).
Contact counts are cross-checked against exp-013 (14 zero-gap pairs, 11 square-wall
incidences) and the PR108 review's seven segment contacts.
"""
from __future__ import annotations

import itertools
import math
from collections import deque
from fractions import Fraction

from cases.trump11.packing import build

TOL = 1e-12


def to_float(field, e):
    field.refine_to(40)
    lo, hi = field.enclose(e)
    return float((lo + hi) / 2)


def main():
    squares, side, field = build()
    L = to_float(field, side)
    sq = [[(to_float(field, x), to_float(field, y)) for (x, y) in s] for s in squares]
    n = len(sq)
    print(f"side U = {L:.15f}")

    # --- orientation of each square (folded into [0,45])
    angles = []
    for s in sq:
        (x0, y0), (x1, y1) = s[0], s[1]
        a = math.degrees(math.atan2(y1 - y0, x1 - x0)) % 90.0
        angles.append(min(a, 90 - a))
    print("folded angles (deg):", [round(a, 6) for a in angles])
    widths = [math.cos(math.radians(a)) + math.sin(math.radians(a)) for a in angles]
    print("x/y projection widths cos+sin:", [round(w, 6) for w in widths])

    # --- wall incidences: which corners lie on which wall; segment if two corners
    walls = {"left": lambda p: p[0], "bottom": lambda p: p[1],
             "right": lambda p: L - p[0], "top": lambda p: L - p[1]}
    wall_inc = {}  # (i, wall) -> number of corners on the wall
    for i, s in enumerate(sq):
        for w, f in walls.items():
            k = sum(1 for p in s if abs(f(p)) < TOL)
            if k:
                wall_inc[(i, w)] = k
    print("\nwall incidences (square, wall, corners on wall; 2 = flush segment, 1 = point):")
    for (i, w), k in sorted(wall_inc.items()):
        print(f"  square {i:2d} {w:6s} corners={k} {'SEGMENT' if k == 2 else 'POINT'}")
    for w in walls:
        touching = sorted(i for (i, ww) in wall_inc if ww == w)
        flush = sorted(i for (i, ww), k in wall_inc.items() if ww == w and k == 2)
        print(f"  {w:6s}: touching {touching}, flush {flush}")

    # --- pair contacts via separating-axis gaps; classify by dimension of intersection
    def axes(s):
        out = []
        for a in range(2):
            (x0, y0), (x1, y1) = s[a], s[a + 1]
            dx, dy = x1 - x0, y1 - y0
            nrm = math.hypot(dx, dy)
            out.append((-dy / nrm, dx / nrm))
        return out

    def proj(s, ax):
        vals = [p[0] * ax[0] + p[1] * ax[1] for p in s]
        return min(vals), max(vals)

    def sat_gap(a, b):
        best = -1e9
        for ax in axes(a) + axes(b):
            lo1, hi1 = proj(a, ax)
            lo2, hi2 = proj(b, ax)
            gap = max(lo2 - hi1, lo1 - hi2)
            best = max(best, gap)
        return best

    def inter_length(a, b):
        """Length of the intersection of two closed touching squares, by sampling the
        corners of each on the boundary of the other: two distinct common points => segment."""
        pts = []
        def inside(p, s):
            for ax in axes(s):
                lo, hi = proj(s, ax)
                v = p[0] * ax[0] + p[1] * ax[1]
                if v < lo - TOL or v > hi + TOL:
                    return False
            return True
        for p in a:
            if inside(p, b):
                pts.append(p)
        for p in b:
            if inside(p, a):
                pts.append(p)
        # dedupe
        uniq = []
        for p in pts:
            if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-9 for q in uniq):
                uniq.append(p)
        if len(uniq) < 2:
            return 0.0, uniq
        return max(math.hypot(p[0] - q[0], p[1] - q[1]) for p, q in itertools.combinations(uniq, 2)), uniq

    contacts = {}
    strict_gaps = []
    for i, j in itertools.combinations(range(n), 2):
        g = sat_gap(sq[i], sq[j])
        if abs(g) < TOL:
            length, pts = inter_length(sq[i], sq[j])
            contacts[(i, j)] = length
        else:
            assert g > 0, (i, j, g)
            strict_gaps.append((g, i, j))
    print(f"\npair contacts: {len(contacts)} (exp-013 says 14)")
    seg = []
    for (i, j), length in sorted(contacts.items()):
        kind = "SEGMENT" if length > 1e-9 else "POINT"
        if kind == "SEGMENT":
            seg.append((i, j))
        print(f"  ({i},{j}) {kind} length={length:.6f}")
    print("segment contacts:", seg, "(review lists 7)")
    strict_gaps.sort()
    print("smallest strict pair gaps:", [(round(g, 6), i, j) for g, i, j in strict_gaps[:6]])

    # --- contact graph, components, spanning chains
    adj = {i: set() for i in range(n)}
    for (i, j) in contacts:
        adj[i].add(j); adj[j].add(i)
    seen, comps = set(), []
    for i in range(n):
        if i in seen:
            continue
        comp, dq = set(), deque([i])
        while dq:
            u = dq.popleft()
            if u in comp:
                continue
            comp.add(u); dq.extend(adj[u] - comp)
        seen |= comp; comps.append(sorted(comp))
    print("\ncontact-graph components (point or segment contacts):", comps)

    def touches(i, w):
        return (i, w) in wall_inc

    def shortest_chain(w1, w2):
        starts = [i for i in range(n) if touches(i, w1)]
        prev = {s: None for s in starts}
        dq = deque(starts)
        while dq:
            u = dq.popleft()
            if touches(u, w2):
                chain = []
                while u is not None:
                    chain.append(u); u = prev[u]
                return chain[::-1]
            for v in adj[u]:
                if v not in prev:
                    prev[v] = u; dq.append(v)
        return None

    for w1, w2, coord in (("left", "right", 0), ("bottom", "top", 1)):
        ch = shortest_chain(w1, w2)
        print(f"\nshortest {w1}-{w2} chain: {ch}")
        if ch:
            ws = [widths[i] for i in ch]
            print(f"  projection widths {[round(w, 4) for w in ws]} sum={sum(ws):.4f} vs L={L:.4f}")
            kinds = []
            for a, b in zip(ch, ch[1:]):
                key = (min(a, b), max(a, b))
                kinds.append("seg" if contacts[key] > 1e-9 else "pt")
            print(f"  consecutive contact kinds: {kinds}")
            print(f"  wall contacts: {w1}={'flush' if wall_inc[(ch[0], w1)] == 2 else 'point'}, "
                  f"{w2}={'flush' if wall_inc[(ch[-1], w2)] == 2 else 'point'}")

    # --- segment-equality graph (positive-length contacts + flush walls) and its rank
    seg_adj = {i: set() for i in range(n)}
    for (i, j) in seg:
        seg_adj[i].add(j); seg_adj[j].add(i)
    anchored = {i for (i, w), k in wall_inc.items() if k == 2}
    seen, seg_comps = set(), []
    for i in range(n):
        if i in seen:
            continue
        comp, dq = set(), deque([i])
        while dq:
            u = dq.popleft()
            if u in comp:
                continue
            comp.add(u); dq.extend(seg_adj[u] - comp)
        seen |= comp; seg_comps.append(sorted(comp))
    unanchored = [c for c in seg_comps if not (set(c) & anchored)]
    print("\nsegment-equality components:", seg_comps)
    print("wall-anchored squares:", sorted(anchored))
    print("unanchored components:", unanchored, "=> angular rank 11 -", len(unanchored), "=", 11 - len(unanchored))


if __name__ == "__main__":
    main()
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
