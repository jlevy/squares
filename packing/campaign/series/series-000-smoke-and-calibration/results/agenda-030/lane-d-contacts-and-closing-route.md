# Agenda 030, lane D: Contact lemmas and the closing route

Retained planning-lane report for
[X-021](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md),
written by a Fable sub-agent at maximum effort on 2026-09-08 under BC-291 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md).
The report is reproduced as delivered, with its own status labels; X-021 carries the
coordinator’s reading of it.
Nothing here is a registered round or a new bound.

**Correction, 2026-09-08.** The
[dated correction below](#correction-of-2026-09-08-duality-scope-cap-and-retained-continuation)
governs the acceptance rule, strict capture scope, retained-net cap and continuation.
The original report, scratch scripts and reported runs remain historical evidence; the
missing session-100 scratch state cannot be used as a replay input.

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
| Fixed-angle rank and contacts | Every preselected SAT cell containing a minimizer has a vertex with 22 independent active selected rows, but a tight selected pair row need not be a physical contact. Separately, each connected component of the full fixed-angle feasible space at any feasible side has a representative with 22 independent genuine contact rows and every physical contact component touching the left and bottom walls. Angular rank is not forced (n = 6 rattler; n = 5 second-order flex). Trump: rank 10 segment graph, connected contact graph. | PROVED / CHECKED; corrected September 10 |
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

### 1.4 Lemma V (the corrected LP-vertex statement) and the rank question

**Lemma V.** Let `P` be a minimizer.
Fix its angles and a SAT selection valid at `P`. Then there is a minimizer `P'` with the
same angles such that (a) the active rows among the 44 wall rows and the 55 selected
pair rows have rank 22, and (b) every square has at least two linearly independent
active selected rows involving its centre coordinates.

*Proof.* Part (a) is (R3). For (b), full column rank forces the two columns of each
square to be independent after restriction to the active rows.
∎

The original version inferred that every active selected pair row was a physical
contact, and hence that no square was contact-free.
That implication is false: projection intervals can share an endpoint along the chosen
axis while the squares remain positively separated along another SAT axis.
An exact four-square selected-polytope vertex with one such square is given in the
[September 10 structural review](../../../../../../docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md#4-repair-to-the-retained-vertex-argument).
Thus Lemma V’s rank statement survives inside every preselected cell, while its contact
conclusion is withdrawn.

**Proposition V+ (genuine-contact representative).** Fix a feasible side, labelled
orientations, and one connected component of the full feasible translation space.
That component contains a representative in which every physical contact component
touches both the left and bottom walls and 22 independent active translation rows are
genuine wall or pair contacts.
Every square has two linearly independent contact normals when the other centres are
fixed.

The proof first minimizes `f = Σ_i(x_i+y_i)` over the whole connected component, then
breaks ties lexicographically in all centre coordinates.
It next chooses a strictly slack separating row for every physically disjoint pair.
The selected cell containing that minimizer lies inside the same component, and the
minimizer is its vertex; consequently its 22-row basis cannot use a false contact from a
disjoint pair. Translating any physical contact component left or down would lower `f`,
so every component meets both walls.
The full proof, exact counterexample and quantifier boundaries are in the
[structural review](../../../../../../docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md#3-a-normal-form-at-the-trial-side).

Proposition V+ chooses a suitable SAT cell after minimizing over a full connected
component. It does not establish the original physical-contact conclusion in every
preselected cell, force a literal corner occupant, or restrict the angles to a finite
set.
A one-square contact component is allowed when that square touches both named walls;
accordingly, “no isolated square” is not used for the square-only contact graph.

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

1. **Minimality lemmas are not automatically dilation-stable.** Lemma S, Corollary C and
   the minimizer-specific use of Lemma V hold at the unknown side `s(11)`, while a
   certificate is run at a fixed rational side.
   Lemma T is their bridge, and it costs `0.011` of contact tolerance at 3.84.
   Proposition V+ is different: it is proved directly at every feasible fixed side and
   needs no dilation transfer.
   Any other optimum-only structural lemma handed to a fixed-side certificate must state
   its δ-robust form.
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

## Session-100 — duality kill tests and the B = 1 value (2026-09-08)

Lane BC-294 of Agenda 030, hypothesis H-129, bead `think-7lp3`, session-100: one
research lane of 2.5 hours (04:27:52Z to 06:57:52Z) on one worker of a four-core machine
shared with five other agents (load average 4 to 6 throughout), `PACK_JOBS=1`. Wall
times below are therefore not comparable with the planning lane’s or with BC-200’s.
Nothing here allocates an identifier or edits a shared record; the frozen families and
states are under the lane scratchpad (`scratchpad/lane-294/`) and their bytes are what
the numbers below were verified from.
Notation is Section 1.6’s: `q = 96/25`, `B = 9977/10000`, `U = 3.877083590`, a *family*
is a finite set of weighted closed squares in `[0, q]²` with exact depth at most 1 at
every vertex of its own arrangement, and its *value* is its total weight.

### The question and the reading rule

By Lemma D (Section 1.6) the covering mass of *every* measure a certificate could use is
at least the value of any family the measure must cover, and the same inequality holds
with the placements restricted to those disjoint from a region `R` (the conditional
program of X-014 Lemma 2) and with the thresholds of a capture certificate.
Two instances are measured here.

- **`B = 1` at `q`.** The placements are closed *unit* squares at the net directions.
  A unit square at angle `θ ∈ [0, π/4]` contains a `B`-square at a net angle whenever
  Condition 4 holds (`B(1 + D) < 1`), so a family of unit squares bounds from below the
  covering mass of every `(B, net)` the method can use, and of the shrink-free `B = 1`
  instrument with the continuum of directions in particular; `verify_ceiling` reports
  this as the `unit` regime when the *declared* `(B, net)` satisfies Condition 4.
  Declared with `square_side = 1` the same bytes are verified in the `net` regime with
  `B = 1`, a weaker statement about the same family, so both declarations are reported.
  A value `≥ 11` with at least one unit of weight outside Trump’s neighbourhood kills
  every one-body certificate at `q` and above, capture included (D2); a value below 11
  decides nothing by itself.
- **Restricted values at `q` with the retained `(B, net)`.** The placements are the
  retained `B`-squares at the retained 181-direction net, disjoint from `R`. The cell’s
  thresholds: kill at `≥ 10` (one boxed blocker is worth about one unit of fractional
  weight, Section 1.6 D4, so `10 + capacity(Π_b) ≥ 11`), alive below `9.5`, undecided
  between, or when only a lower bound exists.

The reading rule for what each number *is*: a verified family gives an exact lower bound
on the fractional packing value and hence on every covering mass; a covering LP on a
finite site set whose row generation converged gives, by the same weak duality applied
to the discrete site measure, an upper bound on the fractional packing value over the
placements at the net directions — in floating point with the row oracle’s tolerance
`10⁻⁹`, not exact — and a site LP whose rows did not converge is context only.

### Falsifiers, stated before the runs

- For every family below: an exact-depth failure (`verify_ceiling` condition K2) on the
  frozen bytes refutes the value claimed for it; there is no other refutation.
  Every family was verified from its bytes after the run that produced it, and the
  polished families a second time under the re-declared `(B, net)`.
- For a claimed kill: the same K2 check, plus the exact disjointness of every placement
  from the region (asserted in the restricted driver on every family it judged) and the
  exact weight split.
- For a claimed “alive”: the row generation must report `converged` on the final site
  set; a deadline stop leaves the region undecided whatever the objective says.

### Instruments used

The cutting-plane loop of `sqpack.fractional.cutting` is the entry the cell names, and
it was driven by three scratch scripts (appendix), none of which touches an instrument
file:

- `unit_loop.py` runs `cutting_plane_loop` with `square_side = 1` on a merged net (the
  retained 180-step net plus seven steps of `h/8` above `0°` and Trump’s `u` with seven
  steps of `h/8` on either side, 203 directions), warm from BC-200’s state at `191/50`
  with the carried rows’ direction indices remapped onto the merged net and every row
  clamped into the unit centre domain.
- `polish_family.py` is new in kind: the loop restores feasibility by dividing every
  weight by the exact maximum depth (BC-200: `11.06` at the sites became `9.91`), which
  discards everything the family had below depth 1 elsewhere.
  With the support fixed the arrangement and its vertex set do not move, so the polisher
  solves `max Σ w_e` over one weight per D4 orbit subject to exact depth `≤ 1` at a
  working set of vertices, rounds *down* to a common denominator, re-decides every
  vertex exactly with `depths_above`, adds the violated ones and repeats; the result is
  verified by `verify_ceiling` like any other family.
  It is the measurement instrument this lane would ask to have built (OR-1), and it is
  reported as scratch because the cell names no instrument file.
- `restricted_loop.py` re-drives the loop with a disjointness filter on the dual side:
  the row oracle (`generate.placement_cells`) runs on the real sites plus phantom points
  of weight 1000 filling `R` at spacing `1/16`, so placements deep in `R` are never the
  least-covered cells it proposes; each surviving cell is tested for disjointness in
  floats with a margin, snapped, and re-tested exactly (separating-axis test in
  `Fraction`) before it is held; the D4-symmetrised family is disjoint from `R` because
  `R` is D4-symmetric, and the driver asserts that on every family it judges.
  The instrument’s sites and duals are D4-symmetric, so it computes the restriction off
  a D4-symmetric region only: the four corner boxes together, or the central box.
  A single corner box or the corner triangle are not symmetric programs, and the
  instrument cannot express them; they inherit a kill from the four-box result (a family
  disjoint from four boxes is disjoint from one) and never an “alive”, and
  `subrestrict.py` reads their lower bounds off any verified family exactly.
- `trump_split.py` scales Trump’s exact pose (`cases.trump11.packing`, 40-digit
  enclosures) by `q/U`, closes it under D4, and splits a family’s weight by folded angle
  (within `1°` of `0°` or of `40.181937°`) and by position (within `0.05` of a scaled
  Trump centre of that class).

### Remarks proved without a run

- **The `B = 1` value at `q` is at least 10** (proved).
  `s(10) = 3 + √2/2 < 96/25` (`frontier/n-010.md`, proved), so ten closed unit squares
  pack in `[0, q]²`; that packing is a family of value 10 with depth at most 1, whatever
  its angles are. Hence every `B = 1` covering measure at `q` has mass at least 10, and a
  `B = 1` certificate at `q`, if one exists, has mass in `[10, 11)`. The same holds at
  every larger side. Nothing in this lane can lower the `B = 1` covering value below 10;
  the question is only whether it reaches 11.
- **Monotonicity in the shrink** (proved, one line).
  A family of unit squares at side `L` scaled by `B` is a family of `B`-squares at side
  `BL`, and conversely, so `ν*₁(L) = ν*_B(BL)`. The `B = 1` value at `q` is the
  retained-shrink value at `Bq = 3.831168`, inside the band `[3.810, 3.868983]` between
  the retained certificate frontier (T-022) and the retained shrink’s plain cap; the
  site LP at `191/50 = 3.82` with converged rows was `11.0556` (BC-200), which is an
  upper bound on the finite-net value there and does not decide `Bq`.
- **What the D4-symmetric instrument can and cannot compute** (proved).
  A D4-symmetric family disjoint from one corner box is disjoint from all four, so the
  symmetric loop computes the four-box program; conversely a family disjoint from the
  four boxes is disjoint from any one, so `ν*(off one box) ≥ ν*(off four boxes)`, and a
  kill of the four-box program is a kill of the single-box program while an “alive”
  four-box reading says nothing about one box.
  The corner triangle `x + y ≤ 1/2` lies in the half-unit box, so
  `ν*(off the triangle) ≥ ν*(off the half box) ≥ ν*(off the unit
  box)`. The single-box and triangle programs have only the diagonal reflection as
  symmetry and need an instrument with sites that are not D4 orbits (BC-204’s domain
  generalisation, or the same loop with individual sites), which does not exist yet.

### The `B = 1` value at `q = 96/25`

**Inputs.** `n = 11`, `outer_side = 96/25`, placements of side exactly 1; net = the
retained `net_half_tangents(207107/500000, 180)` (half-tangent step
`h = 207107/90000000`, last direction `45.000043°`) plus `h·k/8` for `k = 1..7`
(`0.033°` steps above `0°`) and `u_T = 228871/625725` (Trump’s `tan(a/2)` to
`limit_denominator(10⁶)`, `40.181937°`) with `u_T ± h·k/8` for `k = 1..7` (`0.029°`
steps): 203 directions.
Warm start: BC-200’s state at `191/50` (12761 sites, 9868 rows), sites and rows shifted
by `(q − 191/50)/2 = 1/100`, the grid seed for `(96/25, 1)` added, rows remapped onto
the merged net and clamped into the unit centre domain: 16125 initial sites in 2113 D4
orbits, 13305 rows after the first row generation.
`support_cap = 96`, `cap = 150` orbits per iteration, `rows_rounds = 12`,
`rows_per_direction = 3`, row denominator `10⁶`, weight denominator `10⁹`,
`select_above = 1.000001`, budget 30 minutes, one worker, `PACK_JOBS = 1`, load average
4 to 7 on four cores.

**Iteration 0** (the only one that completed; the process was killed at about 05:01Z
after saving its state, and the budget did not allow a restart): site LP objective
`11.169805` with the row generation *not* converged (12-round cap, 1074 s), raw dual
total `11.136308` at the sites, exact maximum depth `9989418081/8000000000 = 1.248677`
at `(1.000547, 1.839449)` over 2877776 vertices (317548 above 1), depth-scaled value
`8.918484`. The site LP is context: its rows did not converge, so it bounds nothing.

**Result (verified twice).** The value of the `B = 1` reading is the loop’s iteration-0
depth-scaled family:

```
89090463224/9989418081 = 8.918484...
```

verified from the state bytes by `devtools.replay_ceiling_family --check`: 768
placements, exact maximum depth exactly `1` over 2877776 vertices (3775 decided
exactly), total `89090463224/9989418081`, `check: reproduced` (553 s), declared as
`square_side = 1` on the 203-direction net (`net` regime, `B = 1`, K3 fails as it must
below 11). The polisher’s final pass verified the same bytes re-declared at
`square_side = 9977/10000` (Condition 4: `B(1 + D) = 0.9999959 < 1`), which is the
every-`(B, net)` statement: `regime = unit`, `symmetric_only = True` (the 203-direction
net’s last direction is `45.000043°`, so placements there are admissible through their
mirror), exact maximum depth exactly `1` over 2877776 vertices (3775 decided exactly),
total `89090463224/9989418081 = 8.918483790`, `statement: nothing: K3 total weight at
least n` (1839 s, the polisher’s whole run).

The polisher did not improve it in the one round the block allowed: on the working set
of 12028 vertices (the 3072 corners plus every vertex above depth `0.95`) the bounded LP
reached exactly `11.000000`, and the exact re-check found depth `4/3` at 20256 vertices,
so that round’s scaled contribution was `8.25`; the near-band of the candidate (`0.999`)
was added and the deadline stopped the run.
The number says what the cell needs to know about the loop: with a support of 96 orbits
the site LP at `11.17`, the near-tight LP at `11.00` and the exactly feasible value at
`8.92` are three different quantities, and only the last is a bound.

The value is a lower bound on the `B = 1` fractional packing value at `q` and on the
mass of every covering measure any `(B, net)` could use there and at every larger side.
The proved floor is `10` (remark above), above it; so this family measures how far the
loop is from the truth at `q` after one iteration, not the truth.

**Weight split against Trump’s placements** (`trump_split.py` on the same bytes; Trump’s
pose scaled by `q/U = 0.990435`, D4-closed; angle band `1°`, centre radius `0.05`): of
the total `8.918484`, `3.224868` lies within `1°` of the axis directions, `0.026704`
within `1°` of `40.181937°`, and `5.666911` at other angles (the mass sits at `1°`,
`13°`, `25°` to `36°` and `41°` to `44°`: the family is diffuse, not Trump-shaped);
`2.991038` lies inside Trump’s neighbourhood (angle band and centre within `0.05` of a
D4 image of a scaled Trump centre) and `5.927446` outside it.
Lemma D2 would need `≥ 11` in total with `≥ 1` outside; the outside weight is there five
times over, the total is not.

**Sub-restrictions of the same family** (`subrestrict.py`, exact): disjoint from one
unit corner box `76291493608/9989418081 = 7.637231`; from the four corner boxes
`37894584760/9989418081 = 3.793473`; from the half-unit corner box and from the corner
triangle `x + y ≤ 1/2` (exact triangle test) `81373249834/9989418081 = 8.145945`; from
the central unit box `20936487880/3329806027 = 6.287600`; from the strip `x ≤ 1/10`
`6.614027`. Boxing one corner removes `1.28` of fractional weight from this family, the
order of one square, as D4 read off BC-200 (`9.91 → 8.87`).

### Restricted values at `q` with the retained `(B, net)`

**Inputs common to the restricted runs.** `n = 11`, `outer_side = 96/25`,
`square_side = B = 9977/10000`, the retained 181-direction net
(`net_half_tangents(207107/500000, 180)`); warm start BC-200’s state at `191/50` shifted
by `1/100` with the grid seed for `(96/25, B)` added; carried rows meeting the region
dropped exactly before the first solve; `support_cap = 96`, `cap = 150`,
`rows_rounds = 6` (12 did not fit the budget under load), `rows_per_direction = 3` after
the filter with `survey = 12` cells surveyed per direction, phantom points of weight
1000 at spacing `1/16` filling the region, row denominator `10⁶`, weight denominator
`10⁹`, `select_above = 1.000001`, one worker, `PACK_JOBS = 1`. The driver asserts exact
disjointness of every placement of every family it judges, so a family it reports is
disjoint from the region by construction and by check.

- **Four corner boxes** `[0,1]² ∪ [q−1,q]×[0,1] ∪ [0,1]×[q−1,q] ∪ [q−1,q]²`: 1156
  phantom points; 5322 of the 9868 carried rows are disjoint from the union; 16285
  initial sites in D4 orbits; 26-minute budget from 05:02Z.

  The loop ran three iterations in 1735 s (iteration 2 cut by the deadline in its row
  generation): sites 16285 → 17485 → 18633, rows 7320 → 8076 → 8241 (no snapped row was
  dropped by the exact re-test), site LP `7.324503`, `7.142857`, `7.142857`, none with
  converged rows (6-round cap, then the deadline), raw duals `7.3245`, `7.1340`,
  `7.1429`, exact maximum depths `1.429636`, `1.155661`, `1.162935`, scaled values
  `5.123335`, `6.173135`, `6.142096`. The best in-loop floor is iteration 1’s
  `28536196648/4622642825 = 6.173135` over 3135372 vertices; its polished value is
  `57599999944/9199999991 = 6.260870`, verified below.
  The site LP at `7.14` with unconverged rows is context only: the filtered oracle had
  not finished pricing the restricted placements, so nothing bounds the restricted value
  from above in this block.
  **Verified:** the loop’s own `verify_ceiling` on the iteration-1 family from its
  bytes: exact maximum depth exactly `1` over 3135364 vertices, total
  `28536196648/4622642825 = 6.173135`, `net` regime at `B = 9977/10000` on the retained
  net (K3 fails, as it must below 11; the family is a floor, not a ceiling).
  `subrestrict.py` on the same bytes: the weight disjoint from any one corner box, from
  the half box and from the corner triangle is the whole `6.173135` (it is disjoint from
  all four boxes by construction), and `3.412321` of it is also disjoint from the
  central box. **Polished (verified):** one polisher round on the same support (working
  set 4052 vertices above `0.95` plus the corners; the LP reached `7.2` and the exact
  re-check found depth `1.15`, so the round’s scaled candidate is kept) gives value
  `57599999944/9199999991 = 6.260870`, verified by `verify_ceiling` from its bytes:
  exact maximum depth exactly `1` over 3135364 vertices (26265 decided exactly), `net`
  regime at `B = 9977/10000`, `symmetric_only`; the support is the loop’s, so every
  placement is exactly disjoint from the four boxes.

### Classification

Thresholds are the cell’s: `B = 1` kills at `≥ 11` with a unit of weight outside Trump’s
neighbourhood; a restricted region kills at `≥ 10`, is alive below `9.5`, and is
undecided otherwise or when no converged covering LP bounds it from above.
Every lower bound below is the value of a family verified from its bytes by
`verify_ceiling`; every upper-bound column is empty because no row generation converged
in the block.

| Region at `q = 96/25` | Placements | Verified lower bound (family, regime) | Upper bound | Classification |
| --- | --- | --- | --- | --- |
| whole container, `B = 1` | unit squares, 203-direction net | `8.918484` (polished iteration-0 support, `unit` regime re-declared at `9977/10000`; the loop’s own scaled family `8.918484` replayed) and the proved floor `10` | none (site LP `11.17`, rows unconverged) | **undecided**; not a kill (below 11), not alive (no converged LP) |
| four corner boxes | retained `B`-squares, 181-direction net, disjoint | `6.173135` (loop iteration 1, `net` regime); polished `6.260870`; sub-restriction of the `B = 1` family `3.793473` | none (site LP `7.14`, rows unconverged) | **undecided**; far below 10, and “alive” needs a converged LP the block did not reach |
| one corner box `[0,1]²` | not a D4-symmetric program | inherits every four-box lower bound; sub-restriction of the `B = 1` family `7.637231` | none (instrument cannot express the program) | **undecided** (a four-box kill would transfer; none exists) |
| corner triangle `x + y ≤ 1/2` | not a D4-symmetric program | inherits the four-box bounds; sub-restriction of the `B = 1` family `8.145945` | none | **undecided**, same reason |
| central unit box | D4-symmetric; loop cancelled under load | sub-restriction of the corners family `3.412321`; of the `B = 1` family `6.287600` | none | **undecided**; no loop was run on it |
| `B = 1` at `3.86`, `3.87` | — | not started | — | **not started** (the `3.84` run did not converge) |

A `B = 1` family’s sub-restrictions transfer to the retained `(B, net)` program: under
Condition 4 every unit placement contains a `B`-square at a net angle, and a sub-square
of a placement disjoint from `R` is disjoint from `R`, so the contained `B`-squares form
an admissible restricted family of the same weight and no greater depth.

### What the readings say about the routes, BC-204 and H-129

- **No kill at `q` at this depth of search, on either side.** The best verified `B = 1`
  family at `96/25` has value `8.918484`, against the kill threshold 11, and the best
  verified family off the four corner boxes has value `6.260870`, against 10. Both are
  lower bounds, both are far from their thresholds, and neither says the threshold is
  unreachable: the site LPs above them (`11.17` unconverged at `B = 1`, `7.14`
  unconverged off the corners) bound nothing, and the proved floor `ν*₁(q) ≥ 10` leaves
  the `B = 1` question open in both directions.
- **Routes (b) and (c) survive this block, untested rather than confirmed.** Lemma D2
  would kill every capture design and route (c) with a `B = 1` family of value `≥ 11`
  carrying a unit of weight away from Trump’s placements; the family found carries
  `5.927446` outside Trump’s neighbourhood and `2.991038` inside it (angle bands:
  `3.224868` within `1°` of `0°`, `0.026704` within `1°` of `40.18°`), so the *shape* of
  a would-be kill is diffuse and not Trump-like, but its value is not there.
  Route (b)’s premise — that integer-hull cuts must push the fractional value below 11 —
  is neither confirmed nor refuted at `q`; boxing one corner removes `1.28` of
  fractional weight from the best `B = 1` family and all four remove `5.13`
  (sub-restriction), while the loop run *on* the four-box program keeps `6.17` (polished
  `6.260870`); one box costs the order of one square, as Section 1.6 D4 read off BC-200,
  and four cost more than four because the family’s mass is in the corners.
- **BC-204 is not yet worth building for corner conditioning.** The single-box and
  triangle programs would need it; the four-box program, which the symmetric loop
  computes, sits at a floor of `6.260870` with an unconverged LP at `7.14`, and until a
  converged restricted LP or a polished family above `9.5` exists the instrument has no
  threshold to aim at.
  What is worth building first is the polisher as an instrument step of the loop (the
  scaled-versus-polished gap below is the measurement), and an unloaded run of the
  `B = 1` loop to convergence at `q`.
- **H-129.** The claim (no `B = 1` family of value `≥ 11` up to `3.87`) is neither
  refuted (no family reached 11 at `3.84`, the easiest of its three sides) nor supported
  at the exit’s standard (no converged covering LP below 11 at `3.87`, nor at `3.84`
  where the unconverged site LP was `11.17`). Recommended status: `open`, with this
  block’s reading recorded as “`B = 1` at `3.84`: verified `≥ 8.918484`, proved `≥ 10`,
  site LP `11.17` unconverged; `3.86` and `3.87` not started”.

### Obstructions met in the block

- **The loop’s scaling step is the bottleneck, not the LP.** At 16125 sites the site LP
  was `11.17` and the raw dual `11.14`, but one vertex at depth `1.2487` cut the family
  to `8.92`. Re-optimising the weights on the fixed support against exact vertices (the
  polisher) is the missing step between the loop’s two numbers; its first attempt found
  the LP unbounded because an orbit none of whose images passes through a near-tight
  vertex has no constraint at all, and the fix is structural: every placement’s corners
  are vertices of the arrangement, so seeding the working set with all of them gives
  every orbit its own row `w_e/8 ≤ 1`.
- **One iteration is what thirty minutes buys on a shared core.** Iteration 0 of the
  `B = 1` loop cost 23 minutes (18 of them row generation at 203 directions and 12
  rounds); the process was then killed at about 05:01Z by something outside the driver
  (exit 144, memory free), so the `B = 1` reading rests on one iteration’s support.
  BC-200 needed nine iterations at `191/50` to reach `9.91`; a lane that wants the
  loop’s own value to converge needs an unloaded core and hours, which is the planning
  lane’s estimate and not this block’s.
- **The polisher’s working set must be near-tight, not wide.** A band of `0.5` on the
  scaled family selected 2204492 of the 2877776 vertices; the exact screen alone took
  1731 s under load and the constraint build was killed by the memory cgroup at 10 GB
  (`dmesg`: `Memory cgroup out of memory: Killed process ... anon-rss:9998976kB`). A
  band of `0.95` selects about nine thousand, which with the 3072 corners is the right
  first working set; the violated vertices of each round then add what the LP needs.
  Two of the block’s 2.5 hours went to learning this.

### Appendix — scripts as run (lane scratchpad `scratchpad/lane-294/`)

All scripts were run from `packing/` with the project venv (Python 3.14), `PYTHONPATH=.`
for the one that imports `cases`, `PACK_JOBS=1`; the frozen families and states they
wrote are beside them.
Fences are `text` because the lint floor formats Python fences in Markdown.

#### `unit_loop.py`

```text
"""BC-294, priority 1: the B = 1 depth-scaled family at side 96/25.

Runs `sqpack.fractional.cutting.cutting_plane_loop` with unit placements
(square_side = 1) on a net that is the retained 180-step net plus fine steps
near 0 deg and near Trump's angle (u = tan(a/2), the root of 5u^8 - 10u^7 - 2u^6
+ 14u^5 + 12u^4 - 6u^3 + 2u^2 + 2u - 1 in (0.36, 0.37)), warm-started from the
retained BC-200 state at 191/50 with positions recentred and sizes fixed at 1.
The direction indices of the carried rows are remapped onto the merged net.

Usage (from packing/, project venv):
    python unit_loop.py --side 96/25 --minutes 30 --out DIR
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.ceiling import CeilingCertificate, verify_ceiling
from sqpack.fractional.colgen import Rows
from sqpack.fractional.cutting import (
    cutting_plane_loop,
    family_record,
    iteration_table,
    load_state,
    rows_from_exact,
    warm_start,
)
from sqpack.fractional.generate import net_half_tangents

ANGLE_LIMIT = Fraction(207107, 500000)
STEPS = 180
BC200_STATE = Path(
    "campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json"
)
U_MIN_POLY = (5, -10, -2, 14, 12, -6, 2, 2, -1)


def trump_half_tangent(denominator: int = 10**6) -> Fraction:
    """A bounded rational within 1e-9 of Trump's u = tan(a/2), by bisection."""
    def poly(x: Fraction) -> Fraction:
        acc = Fraction(0)
        for c in U_MIN_POLY:
            acc = acc * x + c
        return acc
    lo, hi = Fraction(36, 100), Fraction(37, 100)
    assert poly(lo) * poly(hi) < 0
    for _ in range(60):
        mid = (lo + hi) / 2
        if poly(lo) * poly(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return ((lo + hi) / 2).limit_denominator(denominator)


def merged_net(fine: int = 8, reach: int = 7) -> tuple[tuple[Fraction, ...], list[int], Fraction]:
    """The retained net, plus `reach` steps of h/fine near 0 and around Trump's u.

    Returns (net, old_index -> new_index map for the retained net, Trump's u)."""
    base = net_half_tangents(ANGLE_LIMIT, STEPS)
    h = base[1] - base[0]
    ut = trump_half_tangent()
    extras = {h * k / fine for k in range(1, reach + 1)}
    extras.add(ut)
    for k in range(1, reach + 1):
        extras.add(ut + h * k / fine)
        extras.add(ut - h * k / fine)
    net = tuple(sorted(set(base) | extras))
    position = {t: i for i, t in enumerate(net)}
    remap = [position[t] for t in base]
    return net, remap, ut


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--side", type=Fraction, default=Fraction(96, 25))
    ap.add_argument("--square", type=Fraction, default=Fraction(1))
    ap.add_argument("--minutes", type=float, default=30.0)
    ap.add_argument("--iterations", type=int, default=40)
    ap.add_argument("--cap", type=int, default=150)
    ap.add_argument("--support-cap", type=int, default=96)
    ap.add_argument("--rows-rounds", type=int, default=12)
    ap.add_argument("--warm", type=Path, default=BC200_STATE)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tag = f"{args.side.numerator}-{args.side.denominator}"

    net, remap, ut = merged_net()
    old_side, points, carried = load_state(args.warm)
    if len(remap) == 181:
        carried = [(remap[d], x, y) for d, x, y in carried]
    sites, exact_rows = warm_start(
        points, carried, old_side=old_side, new_side=args.side,
        square_side=args.square, half_tangents=net,
    )
    rows = rows_from_exact(exact_rows, sites, net, args.square)
    settings = {
        "n": 11, "outer_side": str(args.side), "square_side": str(args.square),
        "net": {"base": f"{STEPS} steps to {ANGLE_LIMIT}", "directions": len(net),
                "trump_u": str(ut), "trump_u_float": float(ut),
                "extras": "h/8 steps: 7 above 0 and 7 either side of Trump's u"},
        "warm": str(args.warm), "warm_side": str(old_side),
        "warm_sites": len(points), "warm_rows": len(carried),
        "initial_sites": sites.size, "initial_orbits": len(sites.orbits),
        "minutes": args.minutes, "iterations": args.iterations, "cap": args.cap,
        "support_cap": args.support_cap, "rows_rounds": args.rows_rounds,
        "rows_per_direction": 3, "row_denominator": 10**6, "weight_denominator": 10**9,
    }
    print(json.dumps(settings, indent=1), flush=True)
    log_handle = (args.out / f"unit-loop-{tag}.log").open("a")
    started = time.perf_counter()
    try:
        log = cutting_plane_loop(
            11, args.side, args.square, net,
            sites=sites, rows=rows, exact_rows=exact_rows,
            support_cap=args.support_cap, cap=args.cap,
            max_iterations=args.iterations,
            deadline=started + 60.0 * args.minutes,
            rows_max_rounds=args.rows_rounds, rows_per_direction=3,
            log_sinks=(sys.stdout, log_handle),
            state_path=args.out / f"unit-state-{tag}.json",
        )
    finally:
        log_handle.close()
    wall = time.perf_counter() - started
    print(f"stopped: {log.stopped}; {wall:.0f} s wall")
    print(f"best scaled total {log.best_scaled_total} = {float(log.best_scaled_total):.6f} at iteration {log.best_iteration}")
    print(iteration_table(log.iterations))
    summary = {
        "settings": settings, "seconds": wall, "stopped": log.stopped,
        "best_scaled_total": str(log.best_scaled_total),
        "best_scaled_total_float": float(log.best_scaled_total),
        "best_iteration": log.best_iteration,
        "iterations": [it.as_dict() for it in log.iterations],
    }
    if log.best_family is not None:
        fam = log.best_family
        verdict = verify_ceiling(fam)
        print(f"verify_ceiling (declared B=1, net regime): proved={verdict.proved} regime={verdict.regime} max_depth={verdict.max_depth} vertices={verdict.vertices} total={float(verdict.total_weight):.6f}")
        prov = {"tool": "lane-294 unit_loop.py", "settings": settings,
                "best_iteration": log.best_iteration, "stopped": log.stopped,
                "verify_ceiling": {"proved": verdict.proved, "failures": list(verdict.failures),
                                   "max_depth": str(verdict.max_depth), "vertices": verdict.vertices,
                                   "decided_exactly": verdict.decided_exactly, "regime": verdict.regime,
                                   "symmetric_only": verdict.symmetric_only, "statement": verdict.statement}}
        (args.out / f"unit-family-{tag}.json").write_text(json.dumps(family_record(fam, prov), indent=1) + "\n")
        summary["verdict"] = prov["verify_ceiling"]
    (args.out / f"unit-summary-{tag}.json").write_text(json.dumps(summary, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### `polish_family.py`

```text
"""Depth polishing: re-optimise a frozen family's weights against exact vertices.

The cutting-plane loop restores feasibility by dividing every weight by the
exact maximum depth, which throws away everything the family had below depth
1 elsewhere (BC-200: raw 11.06 at the sites, 9.91 after scaling). This keeps
the support fixed -- the arrangement, hence its vertex set, does not move when
only weights change -- and solves

    max sum_e w_e   s.t.  sum_e (m_e(v) / 8) w_e <= 1  for every working vertex v,

with one weight per D4 orbit of eight images (m_e(v) = images of e containing
v), rounds the solution DOWN to a common denominator, re-decides the depth at
every vertex exactly with `depths_above`, adds every violated vertex to the
working set and repeats. The output is verified by `verify_ceiling`.

Usage (from packing/, project venv):
    python polish_family.py FAMILY.json --out POLISHED.json [--minutes 15]
      [--declare-square 9977/10000]   # re-declare (B, net) so the verdict is the unit regime
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from sqpack.fractional.ceiling import (
    SCREEN_MARGIN,
    CeilingCertificate,
    Placement,
    arrangement_lines,
    container_vertices,
    float_family,
    loose_membership,
    verify_ceiling,
)
from sqpack.fractional.cutting import depths_above, family_record


def memberships(fam: CeilingCertificate, pts: list[tuple[Fraction, Fraction]]) -> list[list[int]]:
    """Exact member lists of every point, float-screened as `depths_above` screens."""
    normals, offsets, halves, _ = float_family(fam)
    arr = np.array([[float(x), float(y)] for x, y in pts])
    tight = halves[None, :] - SCREEN_MARGIN
    out: list[list[int]] = []
    chunk = max(1, 2_000_000 // max(1, len(fam.placements)))
    for start in range(0, arr.shape[0], chunk):
        block = arr[start : start + chunk]
        loose = loose_membership(block, normals, offsets, halves)
        first = np.abs(block @ normals[:, 0, :].T - offsets[None, :, 0]) <= tight
        second = np.abs(block @ normals[:, 1, :].T - offsets[None, :, 1]) <= tight
        strict = first & second
        for local in range(block.shape[0]):
            x, y = pts[start + local]
            members = list(np.flatnonzero(strict[local]))
            for m in np.flatnonzero(loose[local] & ~strict[local]):
                if fam.placements[int(m)].contains(x, y):
                    members.append(int(m))
            out.append([int(m) for m in members])
    return out


def rebuild(fam: CeilingCertificate, orbit_weights: list[Fraction]) -> CeilingCertificate:
    pl = [
        Placement(p.half_tangent, p.centre_x, p.centre_y, orbit_weights[i // 8] / 8, p.side)
        for i, p in enumerate(fam.placements)
    ]
    return CeilingCertificate(fam.n, fam.outer_side, fam.square_side, fam.half_tangents, tuple(pl))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("family", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--minutes", type=float, default=15.0)
    ap.add_argument("--band", type=Fraction, default=Fraction(95, 100))
    ap.add_argument("--denominator", type=int, default=10**9)
    ap.add_argument("--declare-square", type=Fraction, default=None)
    args = ap.parse_args()
    t0 = time.perf_counter()
    deadline = t0 + 60 * args.minutes
    rec = json.loads(args.family.read_text())
    fam = CeilingCertificate.from_record(rec.get("best_family", rec))
    if args.declare_square is not None:
        fam = CeilingCertificate(fam.n, fam.outer_side, args.declare_square, fam.half_tangents, fam.placements)
    n_pl = len(fam.placements)
    assert n_pl % 8 == 0, "expected a symmetrised family (8 images per entry)"
    orbits = n_pl // 8
    for e in range(orbits):
        ws = {fam.placements[8 * e + k].weight for k in range(8)}
        assert len(ws) == 1, f"orbit {e} has unequal image weights"
    w = [fam.placements[8 * e].weight * 8 for e in range(orbits)]
    print(f"family: {n_pl} placements, {orbits} orbits, total {float(sum(w)):.6f}, side {fam.outer_side}, placement side {fam.placements[0].side}", flush=True)

    lines = arrangement_lines(fam)
    vertices = container_vertices(fam, lines)
    print(f"vertices: {len(vertices)} ({time.perf_counter() - t0:.0f} s)", flush=True)

    working: dict[tuple[Fraction, Fraction], list[int]] = {}
    band, _, _ = depths_above(fam, vertices, args.band)
    pts = [(x, y) for _, x, y in band]
    # Every placement's corners are arrangement vertices; seeding them gives every
    # orbit at least its own constraint w_e / 8 <= 1, so the LP is bounded.
    corner_set = {c for p in fam.placements for c in p.corners()
                  if 0 <= c[0] <= fam.outer_side and 0 <= c[1] <= fam.outer_side}
    pts = list(dict.fromkeys(pts + sorted(corner_set)))
    for pt, mem in zip(pts, memberships(fam, pts)):
        working[pt] = mem
    print(f"round 0 working set: {len(working)} vertices above {float(args.band)} ({time.perf_counter() - t0:.0f} s)", flush=True)

    best = (sum(w), w, fam)
    rnd = 0
    while True:
        rnd += 1
        keys = list(working.keys())
        rows_i, cols_j, vals = [], [], []
        for r, k in enumerate(keys):
            counts: dict[int, int] = {}
            for m in working[k]:
                counts[m // 8] = counts.get(m // 8, 0) + 1
            for e, c in counts.items():
                rows_i.append(r); cols_j.append(e); vals.append(c / 8.0)
        from scipy import sparse
        A = sparse.csr_matrix((vals, (rows_i, cols_j)), shape=(len(keys), orbits))
        res = linprog(c=-np.ones(orbits), A_ub=A, b_ub=np.ones(len(keys)), bounds=[(0, 8.0)] * orbits, method="highs")
        if not res.success:
            print("LP failed:", res.message); break
        lp_val = -res.fun
        D = args.denominator
        new_w = [Fraction(int(np.floor(max(v, 0.0) * D)), D) for v in res.x]
        cand = rebuild(fam, new_w)
        viol, worst, decided = depths_above(cand, vertices, Fraction(1))
        total = sum(new_w)
        print(f"round {rnd}: LP {lp_val:.6f} on {len(keys)} constraints; rounded total {float(total):.6f}; exact max depth {float(worst):.9f}; violated {len(viol)}; decided {decided} ({time.perf_counter() - t0:.0f} s)", flush=True)
        if worst <= 1:
            if total > best[0]:
                best = (total, new_w, cand)
            # tighten: a feasible optimum on the working set that is exactly feasible everywhere is the fixed point
            break
        scaled = total / worst
        if scaled > best[0]:
            best = (scaled, [x / worst for x in new_w], cand.scaled(1 / worst))
        # add violated vertices (all of them) and a near band of the candidate
        near, _, _ = depths_above(cand, vertices, Fraction(999, 1000))
        new_pts = [(x, y) for _, x, y in near if (x, y) not in working]
        for pt, mem in zip(new_pts, memberships(cand, new_pts)):
            working[pt] = mem
        print(f"  added {len(new_pts)} vertices (working {len(working)})", flush=True)
        if time.perf_counter() > deadline:
            print("deadline reached"); break

    total, w_best, fam_best = best
    verdict = verify_ceiling(fam_best)
    print(f"verify_ceiling: proved={verdict.proved} regime={verdict.regime} symmetric_only={verdict.symmetric_only} max_depth={verdict.max_depth} vertices={verdict.vertices} decided={verdict.decided_exactly} total={verdict.total_weight} = {float(verdict.total_weight):.9f}")
    print("statement:", verdict.statement)
    prov = {"tool": "lane-294 polish_family.py", "source": str(args.family), "rounds": rnd,
            "band": str(args.band), "denominator": args.denominator,
            "verify_ceiling": {"proved": verdict.proved, "failures": list(verdict.failures),
                               "max_depth": str(verdict.max_depth), "vertices": verdict.vertices,
                               "decided_exactly": verdict.decided_exactly, "regime": verdict.regime,
                               "symmetric_only": verdict.symmetric_only, "statement": verdict.statement}}
    args.out.write_text(json.dumps(family_record(fam_best, prov), indent=1) + "\n")
    print(f"wrote {args.out}; {time.perf_counter() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### `restricted_loop.py`

```text
"""BC-294, priority 2: restricted fractional packing values at 96/25 (Lemma D1).

The cutting-plane loop of `sqpack.fractional.cutting`, re-driven with a
disjointness filter on the dual side: every placement row must be disjoint
from a D4-symmetric closed region R (the four unit corner boxes, or the
central unit box). The oracle is `generate.placement_cells` on the real sites
plus phantom points of large fixed weight filling R, so that placements deep in
R are never the least-covered cells it proposes; each proposed cell is tested
for disjointness in floats with a margin, snapped to a bounded rational, and
re-tested exactly (separating-axis test in Fractions) before it is held. The
D4-symmetrised dual family is then disjoint from R because R is D4-symmetric,
and its total over its exact maximum depth is a lower bound on the fractional
packing value over placements disjoint from R at this (L, B, net).

Usage (from packing/, project venv):
    python restricted_loop.py --region corners --minutes 30 --out DIR
    python restricted_loop.py --region centre  --minutes 30 --out DIR
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from sqpack.fractional.ceiling import CeilingCertificate, Placement, arrangement_lines, verify_ceiling
from sqpack.fractional.colgen import LpSolution, Rows, SiteSet, solve_lp
from sqpack.fractional.cutting import (
    Iteration,
    coverage_matrix,
    family_record,
    iteration_table,
    load_state,
    rows_from_exact,
    screened_separation,
    snap_centre,
    support_entries,
    symmetric_placements,
    warm_start,
)
from sqpack.fractional.generate import LP_FEASIBILITY, direction_net, net_half_tangents, placement_cells

ANGLE_LIMIT = Fraction(207107, 500000)
STEPS = 180
B = Fraction(9977, 10000)
BC200_STATE = Path("campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json")
Box = tuple[Fraction, Fraction, Fraction, Fraction]


def region_boxes(name: str, L: Fraction) -> list[Box]:
    one = Fraction(1)
    if name == "corners":
        return [(0, 0, one, one), (L - 1, 0, L, one), (0, L - 1, one, L), (L - 1, L - 1, L, L)]
    if name == "centre":
        return [(L / 2 - Fraction(1, 2), L / 2 - Fraction(1, 2), L / 2 + Fraction(1, 2), L / 2 + Fraction(1, 2))]
    if name == "halfcorners":
        h = Fraction(1, 2)
        return [(0, 0, h, h), (L - h, 0, L, h), (0, L - h, h, L), (L - h, L - h, L, L)]
    raise ValueError(name)


def box_disjoint_exact(p: Placement, box: Box) -> bool:
    x0, y0, x1, y1 = (Fraction(v) for v in box)
    cs = p.corners()
    xs = [c[0] for c in cs]; ys = [c[1] for c in cs]
    if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
        return True
    ax, ay, u, bx, by, v = p.slabs()
    half = p.side / 2
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for (nx, ny, c) in ((ax, ay, u), (bx, by, v)):
        vals = [nx * x + ny * y for (x, y) in pts]
        if max(vals) < c - half or min(vals) > c + half:
            return True
    return False


def disjoint_exact(p: Placement, boxes: list[Box]) -> bool:
    return all(box_disjoint_exact(p, b) for b in boxes)


def disjoint_float(x: float, y: float, cos: float, sin: float, half: float, boxes: list[Box], margin: float = 1e-7) -> bool:
    """Closed square vs closed boxes, separated by more than `margin` on some axis."""
    cx = [x + half * (su * cos - sv * sin) for su, sv in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    cy = [y + half * (su * sin + sv * cos) for su, sv in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    for (x0, y0, x1, y1) in boxes:
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        if max(cx) < x0 - margin or min(cx) > x1 + margin or max(cy) < y0 - margin or min(cy) > y1 + margin:
            continue
        u = x * cos + y * sin; v = -x * sin + y * cos
        pu = [px * cos + py * sin for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        pv = [-px * sin + py * cos for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        if max(pu) < u - half - margin or min(pu) > u + half + margin or max(pv) < v - half - margin or min(pv) > v + half + margin:
            continue
        return False
    return True


def phantom_points(boxes: list[Box], spacing: Fraction = Fraction(1, 16)) -> np.ndarray:
    pts = []
    for (x0, y0, x1, y1) in boxes:
        nx = int((x1 - x0) / spacing) + 1; ny = int((y1 - y0) / spacing) + 1
        for i in range(nx):
            for j in range(ny):
                pts.append((float(x0 + i * spacing), float(y0 + j * spacing)))
    return np.array(pts)


def solve_rows_filtered(sites: SiteSet, square_side: Fraction, half_tangents, rows: Rows, exact_rows, boxes: list[Box], phantom: np.ndarray, *, max_rounds: int, rows_per_direction: int, survey: int, deadline: float | None, row_denominator: int) -> LpSolution:
    """`colgen.solve_rows` with the region masked by phantom points and held rows filtered."""
    points = sites.points(); sizes = sites.sizes(); membership = sites.membership()
    columns = len(sites.orbits)
    directions = direction_net(half_tangents)
    outer = float(sites.outer_side); side = float(square_side); half = side / 2
    aug_points = np.vstack([points, phantom])
    n_real = points.shape[0]
    if rows.matrix.shape[0] == 0:
        rows.matrix = np.zeros((0, columns))
    weights = np.zeros(columns); duals = np.zeros(len(rows))
    solution = LpSolution(weights, duals, rows=len(rows))
    if len(rows) > 0:
        warm = solve_lp(sites, rows)
        if warm is not None:
            weights, duals, objective = warm
            solution.weights, solution.duals, solution.objective = weights, duals, objective
    for round_index in range(max_rounds):
        if deadline is not None and time.perf_counter() >= deadline:
            solution.stopped = f"deadline reached after {round_index} rounds"; return solution
        solution.rounds = round_index + 1
        site_weights = np.concatenate([weights[membership], np.full(phantom.shape[0], 1000.0)])
        violated = 0; added = 0; least = float("inf"); least_covered = float("inf")
        for index, direction in enumerate(directions):
            cos, sin = float(direction.ux), float(direction.uy)
            kept = 0
            for mass, cu, cv, covers in placement_cells(aug_points, site_weights, direction, outer, side, keep=survey):
                x = cos * cu - sin * cv; y = sin * cu + cos * cv
                if not disjoint_float(x, y, cos, sin, half, boxes):
                    continue
                least_covered = min(least_covered, mass)
                if mass >= 1 - 1e-9:
                    break
                row = np.zeros(columns)
                real = covers[:n_real]
                np.add.at(row, membership[real], 1.0)
                if row.sum() == 0:
                    solution.stopped = "a placement covers no site: the sites cannot cover"; return solution
                violated += 1; least = min(least, mass)
                if rows.add(index, (cu, cv), row):
                    added += 1
                kept += 1
                if kept >= rows_per_direction:
                    break
        solution.rows = len(rows); solution.least_covered = least_covered
        if violated == 0 or (added == 0 and least >= 1 - LP_FEASIBILITY):
            solution.objective = float(sizes @ weights)
            solution.stopped = "converged: every placement covers mass 1"; return solution
        if added == 0:
            solution.stopped = f"a held row is violated by {1 - least:.3e}: the solver's point is off"; return solution
        solved = solve_lp(sites, rows)
        if solved is None:
            solution.stopped = "linear program refused the generated rows"; return solution
        weights, duals, objective = solved
        solution.weights, solution.duals, solution.objective = weights, duals, objective
    solution.stopped = f"round limit {max_rounds} reached"
    return solution


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", choices=["corners", "centre", "halfcorners"], required=True)
    ap.add_argument("--side", type=Fraction, default=Fraction(96, 25))
    ap.add_argument("--square", type=Fraction, default=B)
    ap.add_argument("--minutes", type=float, default=30.0)
    ap.add_argument("--iterations", type=int, default=40)
    ap.add_argument("--cap", type=int, default=150)
    ap.add_argument("--support-cap", type=int, default=96)
    ap.add_argument("--rows-rounds", type=int, default=12)
    ap.add_argument("--survey", type=int, default=12)
    ap.add_argument("--warm", type=Path, default=BC200_STATE)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    L = args.side; Bs = args.square
    net = net_half_tangents(ANGLE_LIMIT, STEPS)
    directions = direction_net(net)
    boxes = region_boxes(args.region, L)
    phantom = phantom_points(boxes)
    old_side, points, carried = load_state(args.warm)
    sites, carried = warm_start(points, carried, old_side=old_side, new_side=L, square_side=Bs, half_tangents=net)
    exact_rows = [(d, x, y) for d, x, y in carried if disjoint_exact(Placement(net[d], x, y, Fraction(1), Bs), boxes)]
    rows = rows_from_exact(exact_rows, sites, net, Bs)
    settings = {"n": 11, "outer_side": str(L), "square_side": str(Bs), "region": args.region,
                "boxes": [[str(v) for v in b] for b in boxes], "phantom_points": int(phantom.shape[0]),
                "net": f"{STEPS} steps to {ANGLE_LIMIT} ({len(net)} directions)",
                "warm": str(args.warm), "warm_side": str(old_side), "warm_sites": len(points),
                "warm_rows": len(carried), "warm_rows_disjoint": len(exact_rows),
                "initial_sites": sites.size, "initial_orbits": len(sites.orbits),
                "minutes": args.minutes, "cap": args.cap, "support_cap": args.support_cap,
                "rows_rounds": args.rows_rounds, "rows_per_direction": 3, "survey": args.survey,
                "row_denominator": 10**6, "weight_denominator": 10**9}
    print(json.dumps(settings, indent=1), flush=True)
    started = time.perf_counter(); deadline = started + 60 * args.minutes
    iterations: list[Iteration] = []
    best_scaled = Fraction(0); best_family = None; best_iter = -1; stopped = ""
    select_above = Fraction(1000001, 1000000)
    tag = f"{args.region}-{L.numerator}-{L.denominator}"
    for index in range(args.iterations):
        if time.perf_counter() >= deadline:
            stopped = f"deadline reached before iteration {index}"; break
        t = time.perf_counter()
        solution = solve_rows_filtered(sites, Bs, net, rows, exact_rows, boxes, phantom, max_rounds=args.rows_rounds, rows_per_direction=3, survey=args.survey, deadline=deadline, row_denominator=10**6)
        new_exact = []
        dropped = 0
        for held in range(len(exact_rows), len(rows)):
            d = rows.directions[held]
            x, y = snap_centre(directions[d], rows.centres[held], L, Bs, 10**6)
            if disjoint_exact(Placement(net[d], x, y, Fraction(1), Bs), boxes):
                new_exact.append((d, x, y))
            else:
                dropped += 1
        exact_rows.extend(new_exact)
        rows = rows_from_exact(exact_rows, sites, net, Bs)
        s_rows = time.perf_counter() - t
        t = time.perf_counter()
        solved = solve_lp(sites, rows)
        if solved is None:
            stopped = f"the linear program refused the snapped rows at iteration {index}"; break
        weights, duals, objective = solved
        s_lp = time.perf_counter() - t
        t = time.perf_counter()
        entries = support_entries(exact_rows, duals, net, support_cap=args.support_cap, weight_denominator=10**9)
        if not entries:
            stopped = f"the dual is empty at iteration {index}"; break
        family = CeilingCertificate(11, L, Bs, net, symmetric_placements(entries, L, Bs))
        assert all(disjoint_exact(p, boxes) for p in family.placements), "a family placement meets the region"
        lines = arrangement_lines(family)
        sep = screened_separation(family, lines, sites, cap=args.cap, select_above=select_above)
        worst = sep.max_depth
        s_sep = time.perf_counter() - t
        raw = family.total_weight
        scaled = raw if worst <= 1 else raw / worst
        rec = Iteration(index=index, sites=sites.size, orbits=len(sites.orbits), rows=len(rows), support=len(entries), rows_converged=solution.converged, rows_stopped=solution.stopped, rows_objective=solution.objective, objective=objective, raw_total=raw, max_depth=worst, scaled_total=scaled, vertices=sep.vertices, decided=sep.decided, violating=sep.violating, added=0, seconds_rows=s_rows, seconds_lp=s_lp, seconds_separation=s_sep)
        iterations.append(rec)
        if scaled > best_scaled:
            best_scaled, best_iter = scaled, index
            best_family = family if worst <= 1 else family.scaled(1 / worst)
        print(f"iteration {index}: sites={sites.size} orbits={len(sites.orbits)} rows={len(rows)} dropped={dropped} support={len(entries)} rows_objective={solution.objective:.6f} converged={solution.converged} ({solution.stopped}) objective={objective:.6f} raw_total={float(raw):.6f} max_depth={float(worst):.6f} scaled_total={float(scaled):.6f} vertices={sep.vertices} violating={sep.violating} seconds rows={s_rows:.1f} lp={s_lp:.1f} sep={s_sep:.1f}", flush=True)
        state = {"outer_side": str(L), "square_side": str(Bs), "region": args.region,
                 "sites": [[str(x), str(y)] for orbit in sites.orbits for x, y in orbit],
                 "rows": [[d, str(x), str(y)] for d, x, y in exact_rows],
                 "best_scaled_total": str(best_scaled), "best_iteration": best_iter,
                 "iterations": [it.as_dict() for it in iterations]}
        if best_family is not None:
            state["best_family"] = family_record(best_family)
        (args.out / f"restricted-state-{tag}.json").write_text(json.dumps(state) + "\n")
        if worst <= 1 and solution.converged:
            stopped = f"feasible family with converged rows at iteration {index}"; break
        selected = sep.chosen
        if not selected:
            stopped = f"no vertex to add at iteration {index}"; break
        new_orbits = tuple(orbit for _, orbit in selected)
        sites = SiteSet(L, (*sites.orbits, *new_orbits))
        addition = coverage_matrix(exact_rows, SiteSet(L, new_orbits), net, Bs)
        rows.matrix = np.hstack([rows.stacked(), addition])
        rows.keys = {row.tobytes() for row in rows.matrix}
        rec.added = len(new_orbits)
        print(f"  added {len(new_orbits)} orbits, deepest {float(selected[0][0]):.6f}", flush=True)
    else:
        stopped = f"iteration cap {args.iterations} reached"
    wall = time.perf_counter() - started
    print(f"stopped: {stopped}; {wall:.0f} s wall")
    print(f"best scaled total {best_scaled} = {float(best_scaled):.6f} at iteration {best_iter}")
    print(iteration_table(iterations))
    summary = {"settings": settings, "seconds": wall, "stopped": stopped, "best_scaled_total": str(best_scaled), "best_scaled_total_float": float(best_scaled), "best_iteration": best_iter, "iterations": [it.as_dict() for it in iterations]}
    if best_family is not None:
        verdict = verify_ceiling(best_family)
        print(f"verify_ceiling: proved={verdict.proved} regime={verdict.regime} max_depth={verdict.max_depth} vertices={verdict.vertices} total={float(verdict.total_weight):.6f}")
        prov = {"tool": "lane-294 restricted_loop.py", "settings": settings, "best_iteration": best_iter, "stopped": stopped,
                "verify_ceiling": {"proved": verdict.proved, "failures": list(verdict.failures), "max_depth": str(verdict.max_depth), "vertices": verdict.vertices, "decided_exactly": verdict.decided_exactly, "regime": verdict.regime, "symmetric_only": verdict.symmetric_only, "statement": verdict.statement}}
        (args.out / f"restricted-family-{tag}.json").write_text(json.dumps(family_record(best_family, prov), indent=1) + "\n")
        summary["verdict"] = prov["verify_ceiling"]
    (args.out / f"restricted-summary-{tag}.json").write_text(json.dumps(summary, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### `trump_split.py`

```text
"""Weight of a verified family near Trump's placements versus away from them.

Trump's pose (cases.trump11.packing, exact in Q(u)) is scaled by q/U into
[0, q]^2 (centres scaled, sides stay 1) and closed under D4. A family placement
is "near Trump" when its folded angle is within `--deg` of a Trump square's
folded angle (0 or 40.181937 deg) and its centre is within `--radius` of a D4
image of a scaled Trump centre in that angle class. Also printed: the weight
per folded-angle band irrespective of position (Lemma D2 reads either).

Usage (from packing/, project venv): python trump_split.py FAMILY.json [--side 96/25]
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from cases.trump11.packing import build
from sqpack.fractional.ceiling import CeilingCertificate


def to_float(field, e) -> float:
    field.refine_to(40)
    lo, hi = field.enclose(e)
    return float((lo + hi) / 2)


def folded_deg(half_tangent: Fraction) -> float:
    a = math.degrees(2 * math.atan(float(half_tangent))) % 90.0
    return min(a, 90.0 - a)


def d4_images(x: float, y: float, L: float):
    return [(x, y), (L - y, x), (L - x, L - y), (y, L - x), (L - x, y), (x, L - y), (y, x), (L - y, L - x)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("family", type=Path)
    ap.add_argument("--side", type=Fraction, default=Fraction(96, 25))
    ap.add_argument("--deg", type=float, default=1.0)
    ap.add_argument("--radius", type=float, default=0.05)
    args = ap.parse_args()
    rec = json.loads(args.family.read_text())
    fam = CeilingCertificate.from_record(rec.get("best_family", rec))
    L = float(args.side)
    squares, side, field = build()
    U = to_float(field, side)
    scale = L / U
    trump = []
    for s in squares:
        cs = [(to_float(field, x), to_float(field, y)) for (x, y) in s]
        cx = sum(c[0] for c in cs) / 4; cy = sum(c[1] for c in cs) / 4
        ang = math.degrees(math.atan2(cs[1][1] - cs[0][1], cs[1][0] - cs[0][0])) % 90.0
        ang = min(ang, 90.0 - ang)
        trump.append((cx * scale, cy * scale, ang))
    classes = sorted({round(a, 4) for _, _, a in trump})
    print(f"Trump at U={U:.9f}; scaled by {scale:.6f} into side {L}; folded angle classes {classes}")
    total = fam.total_weight
    near_pos = Fraction(0); near_ang = {c: Fraction(0) for c in classes}; other = Fraction(0)
    bands: dict[int, Fraction] = {}
    for p in fam.placements:
        a = folded_deg(p.half_tangent)
        bands[int(a)] = bands.get(int(a), 0) + p.weight
        x, y = float(p.centre_x), float(p.centre_y)
        in_ang = None
        for c in classes:
            if abs(a - c) <= args.deg:
                in_ang = c
        if in_ang is None:
            other += p.weight; continue
        near_ang[in_ang] += p.weight
        hit = False
        for (tx, ty, ta) in trump:
            if abs(ta - in_ang) > 1e-6:
                continue
            for (ix, iy) in d4_images(tx, ty, L):
                if math.hypot(x - ix, y - iy) <= args.radius:
                    hit = True; break
            if hit: break
        if hit:
            near_pos += p.weight
    print(f"total {float(total):.6f}")
    for c in classes:
        print(f"  angle within {args.deg} deg of {c:.4f}: {float(near_ang[c]):.6f}")
    print(f"  angle outside both bands: {float(other):.6f}")
    print(f"  in Trump's neighbourhood (angle band AND centre within {args.radius} of a D4 image of a scaled Trump centre): {float(near_pos):.6f}")
    print(f"  outside that neighbourhood: {float(total - near_pos):.6f}")
    print("  weight by folded-angle degree band:", {k: round(float(v), 4) for k, v in sorted(bands.items())})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

#### `subrestrict.py`

```text
"""Exact weight of a verified family disjoint from each single region (Lemma D1).

A sub-family of a depth-1 family is depth-1, so the total weight of the
placements disjoint from a closed region R is a lower bound on the fractional
packing value over placements disjoint from R, at this (L, B, net) and every
larger side. The D4-symmetric loop can only compute the four-box program
directly; this reads the single-box, half-box, corner-triangle and central-box
lower bounds off any verified family (the same separating-axis test in
Fractions as lane D's family_restrict.py, with an exact triangle test added).

Usage (from packing/, project venv): python subrestrict.py FAMILY.json [--side 96/25]
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.ceiling import CeilingCertificate, Placement


def box_disjoint(p: Placement, x0, y0, x1, y1) -> bool:
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


def triangle_disjoint(p: Placement, s: Fraction) -> bool:
    """Closed square vs the closed triangle x >= 0, y >= 0, x + y <= s (SAT on 5 axes)."""
    tri = [(Fraction(0), Fraction(0)), (s, Fraction(0)), (Fraction(0), s)]
    cs = p.corners()
    axes = [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(1), Fraction(1))]
    ax, ay, u, bx, by, v = p.slabs()
    axes += [(ax, ay), (bx, by)]
    for (nx, ny) in axes:
        a = [nx * x + ny * y for (x, y) in cs]
        b = [nx * x + ny * y for (x, y) in tri]
        if max(a) < min(b) or min(a) > max(b):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("family", type=Path)
    ap.add_argument("--side", type=Fraction, default=Fraction(96, 25))
    args = ap.parse_args()
    rec = json.loads(args.family.read_text())
    fam = CeilingCertificate.from_record(rec.get("best_family", rec))
    Q = args.side
    assert fam.outer_side == Q, f"family side {fam.outer_side} != {Q}"
    one, h = Fraction(1), Fraction(1, 2)
    boxes = {
        "corner box SW [0,1]^2": [(0, 0, one, one)],
        "four corner boxes": [(0, 0, one, one), (Q - 1, 0, Q, one), (0, Q - 1, one, Q), (Q - 1, Q - 1, Q, Q)],
        "half-unit corner box SW [0,1/2]^2": [(0, 0, h, h)],
        "central unit box": [(Q / 2 - h, Q / 2 - h, Q / 2 + h, Q / 2 + h)],
        "left strip x<=1/10": [(0, 0, Fraction(1, 10), Q)],
    }
    total = fam.total_weight
    print(f"family {args.family.name}: {len(fam.placements)} placements, side {Q}, placement side {fam.placements[0].side}, total {float(total):.6f}")
    for name, bl in boxes.items():
        w = sum((p.weight for p in fam.placements if all(box_disjoint(p, *b) for b in bl)), start=Fraction(0))
        print(f"  disjoint from {name:36s}: {float(w):.6f}  ({w})")
    w = sum((p.weight for p in fam.placements if triangle_disjoint(p, h)), start=Fraction(0))
    print(f"  disjoint from {'corner triangle x+y<=1/2 (exact)':36s}: {float(w):.6f}  ({w})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Correction of 2026-09-08: Duality Scope, Cap, and Retained Continuation

W9 review at PR 127 identified three errors in the original interpretation and a
continuation that cannot be reproduced from the retained inputs.
This section supersedes those statements while preserving the reports and scripts above.

### What a fractional value decides

Lemma D’s finite covering/packing duality applies to the same fixed placement and site
domains; its continuum obstruction uses weak duality.
A finite-site LP dual is constrained only at those sites.
Its value eleven does not establish pointwise depth at most one.
A verified finite family below eleven supplies a lower bound on the optimum and cannot
show that the optimum is below eleven.
In particular, S2’s original “alive below 9.5” rule is withdrawn: an alive reading
requires an exact covering upper bound below 9.5 on the entire stated restricted domain.
A loop that finds a family below 9.5 is inconclusive.
Likewise a restricted family of weight ten defeats a residual threshold-ten covering
program; defeating the full threshold-eleven conditional program additionally requires a
jointly depth-feasible anchored contribution or a dual on its full domain.

For H-129, confirmation requires an exact measure of mass below eleven covering every
contained unit placement at side 3.87 and every orientation.
A finite-net covering upper bound has only finite-net scope; `B = 1` supplies no angular
shrink margin.
Refutation requires a finite closed-unit family of weight at least eleven,
exactly contained with pointwise depth at most one, at a side at most 3.87. Other
results remain inconclusive, including every session-100 result.

If such a family has total `T ≥ 11` and verified outside weight `O ≥ 1` for the stated
neighbourhood `N`, then `T + δO ≥ 11 + δ` defeats the strict capture inequality
`M < 11 + δ` for every `δ ≥ 0`. This conclusion concerns that capture shape and domain.
It does not rule out geometric conditioning on a different domain, ownership at
equality, capacity or compatibility cuts, or a finite case tree.
References above to deciding the whole ambitious tier negatively, or to every
record-conditioned certificate, exceed the lemma’s scope.

**Finite-family stability lemma (proved).** A finite depth-one family of closed unit
squares contained at side `L > √2` remains feasible at some side `L − ε`, with the same
angles and weights. For each square let `w_i ≤ √2` be its projection width and map each
centre coordinate continuously by

`c_i(ε) = w_i/2 + (c_i − w_i/2)(L − ε − w_i)/(L − w_i)`.

This ensures containment when `0 < ε < L − max_i w_i`. If arbitrarily small ε created
depth above one, one overweight subset of the finitely many placements would recur along
a sequence ε tending to zero.
Its witnessing points lie in a compact container; a convergent subsequence and
closedness put the limit point in every original square of that subset, contradicting
depth at most one. Thus an attained finite value-eleven family also obstructs a pure
strict one-body ladder approaching its side from below.
An unattained supremum of eleven or a finite-site dual of eleven does not supply this
argument. Equality and ownership arguments remain separate.

### Correct retained-net capture cap

The script `net_end_check.py` used `delta = 45 − last_deg < 0` and then
`cos(delta) + sin(delta)`, incorrectly obtaining a required side below `B`. Containment
requires the absolute angular difference.
Let `t = 207107/500000`, `θ = 2 atan(t) > π/4`, `δ = θ − π/4`, `B = 9977/10000`, and
`s_H = 2 + (4/3)√2`. A sufficient condition is the **strict** inequality

`L > C_B = B s_H (cos δ + sin δ) = B(2√2 + 8/3)·2t/(1 + t²)`.

Scale the Hämäläinen packing by `L/s_H` and take the concentric B-cores at the net
directions.
Strictness places each closed core inside its parent’s interior, so the cores
are pairwise disjoint as closed sets, and their unit weights have depth one.
At equality the original packing’s touching closed squares do not themselves have depth
one. This is why `L ≥ B s_H`, as stated in Corollary D3, was not established.

The corrected cap is still below U. The rational upper bound `√2 < 665857/470832`
follows from `665857² − 2·470832² = 1`, and substitution gives

`C_B < 22275352724718225/5745980944770482 < 38767/10000 < U`.

For the middle comparison the cross-multiplied positive gap is
`38767·5745980944770482 − 10000·22275352724718225 = 916038735025694`; the last
comparison follows from the retained Trump root isolation.
Thus at every `L ≥ 38767/10000` the five nearly diagonal cores defeat strict Trump
capture for an angular neighbourhood of radius below `4.8°`. The symbolic corrected
threshold, rather than the old rounded `3.876681`, governs the sharper statement.

The ten-square floor also needs closed-boundary care: start with the known packing at
`s(10) < q`, dilate it to q, and take concentric closed unit squares strictly inside its
larger squares. This gives the stated depth-one family of weight ten.

### A stronger retained unit control and its replay

[Exp-070](../../experiments/exp-070-h-064-n11-fractional-resume.md) retains a stronger
family than BC-200’s original state: 768 placements at `L = 191/50`, side
`B = 9977/10000`, exact depth one and weight `21342289572/2055263195`. Its file is
[`agenda-025/bc-232-leg-01-family.json`](../agenda-025/bc-232-leg-01-family.json).
Scale every centre and side by `10000/9977`, preserving weights and angles.
The new closed unit family has the same pointwise depth and fits at
`38200/9977 < 96/25`, since `38200·25 = 955000 < 957792 = 9977·96`. It follows exactly
from the retained source verification that

`ν*_1(96/25) ≥ 21342289572/2055263195 ≈ 10.384212408`.

This corrects the original statement that the 3.82 record says nothing about the unit
value at q. It leaves H-129 unresolved.
The family can be transported and independently replayed without a search, from
`packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.transport_ceiling_family \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json \
  --scale 10000/9977 --side 96/25 --verify --out /tmp/n11-unit-control.json
```

`transport_ceiling_family` scales all geometry exactly and optionally recentres it in a
larger container.
It preserves the exact source and destination half-tangents and records
the source’s Git/path identity.
For state input it remaps each row by tangent identity, refusing an inconsistent source
net or a destination missing an angle.
A legacy state needs its net in `best_family`; an index alone is never a direction
identity. The transport is an instrument control, not an experiment that improves a
packing bound.

The W9 replay on 2026-09-08 independently checked the transported family at q:
`max_depth = 1`, `2702488` arrangement vertices, `19335` exact tie decisions, and
unchanged weight `21342289572/2055263195`. The only failed ceiling condition is
`K3 total weight at least n`, as expected for a family below eleven; `proved = false`
must not be read as a depth failure or promoted to an eleven-square obstruction.
The input is Git-bound to `883d5ef8d4b971057977cd0c3c42f900f937f1de` at the retained
family path above. The local replay receipt is `/tmp/n11-pr127-unit-control.json`; the
command and tracked input regenerate it, and the receipt is not a repository artifact.

### Missing scratch evidence and the next instrument

Session-100’s named `scratchpad/lane-294/unit-3-84/unit-state-96-25.json`, its family
and the plateau run-1 state are absent from this checkout.
Their reported values remain historical readings, not independently replayable artifacts
on this branch. The original embedded `unit_loop.py` is **unsafe for resuming its own
state**: its `len(remap) == 181` condition is always true, so the already merged
203-direction indices are remapped again, changing angles or raising `IndexError`.
Preserve the script as evidence; use a net-bound driver for any continuation.

The next instrument block starts from the retained exp-070 family above.
A fixed-support polisher must preserve that feasible control, seed a bounded working
set, and record both an exactly feasible family and an exact upper bound on that fixed
support before calling it optimal.
Duplicate vertex-incidence vectors are identical constraints; componentwise dominated
vectors can be dropped because weights are nonnegative.
This avoids storing millions of coordinate-keyed copies of the same inequality.
The original one-round polisher result located a scaling loss; it did not prove that
reweighting this support recovers the loss, or that the LP is no longer a bottleneck.

Full-dual pricing must use a retained state and an exact pointwise separation check.
A newly found violating point diagnoses the old truncated stop.
Returning no candidate from a truncated or floating survey is inconclusive.
Only after these controls should a separately registered search target q for lower-bound
progress or 3.87 for the endpoint obstruction, with the corrected primal/dual acceptance
rule above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
