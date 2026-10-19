# BOX-MEETERS — who meets a corner box in normal form: one toucher per wall is a theorem, everything else FLOATS; a floater lands unless it is JAMMED (drawn); the window exclusions as box-valid LP certificates — A261, 2026-09-21

The brief (A261 BRIEF): after A258, BOX-MEETERS(11) — "in a family-stuck maximiser of the lexicographic potential on
[3.82, ŝ] every corner box is met by exactly two squares, both wall touchers, one on each of its walls, the eight
distinct" — rests on O1 TOUCH-NORMAL, O2 TWO WALLS / no third meeter, O3 certificates for A258's [M] least sides.
This note proves what is a theorem, draws what is false, and prices + launches O3.  Everything in §1–2 is stated in
the corner quadrant and is s-FREE: it holds for every n and every side s > 1 + √2 (m-free).  Tags: [T] proved,
[T-computed] exact finite computation with its own verifier, [M] measured, [C] conjecture, [F] false as stated
(witness).  Sources: `normal_ring.md` (P1–P4, the family D′), `k0_count.md` (Lemma PUSH), `wedged_seal.md`,
`construct_towards.md` (SQUARE-IN-TRIANGLE, TWO-CORNERS), `sideband.md` (A2: cells), `ring_swap.md` (CELLS).
Code `attempts/A261-box-meeters/code/` (`census261`, `local261`, `jam261`, `checkjam261`, `verify261` + `ivl261`
(the verifier), `cert261`, `chain261`, `price261`, `test261`, `pages261` + `svg261`, `run261.sh`); results
`attempts/A261-box-meeters/results/`; certificates `attempts/A261-box-meeters/certs/`; pages
`docs/residue_map/campaigns/A261-box-meeters/`; Lean `Statements/Open/BoxMeeters.lean`.

## 0. Verdict

> **[T] SAME-WALL (any n, any s).**  Two unit squares touching the SAME wall of a corner cannot both meet its open
> box: a separating line would need a normal n (from the first to the second) with n_u > 0 (the second touches the
> floor: PUSH (ii)) and −n_u > 0 (so does the first).  With WEDGED-SEAL: **a doubly-met box has at most ONE toucher
> per wall, none touching both, and every further meeter FLOATS** (touches no wall at all: a meeter lies in
> [0, 1+√2)²).  So O2 is not a separate obligation: "same-wall pair" = a toucher + a second-layer FLOATER (A255's
> rand_0_0441), "third meeter" = a floater.  **BOX-MEETERS ⟺ no floating box meeter** (+ TWO-CORNERS for "distinct").
>
> **[T] what the normal form gives about a floater C** (§1): **P1⁺** (family form of P1: a family Π of disjoint
> wall-touching cells of ANY pose with |M(Π)| ≤ |Π| is met by touchers only); **BLOCKER-SIDE** (a square blocking C's
> straight drop to the floor lies under C's RIGHT flank — separated from C by a line of POSITIVE slope; mirror for
> the wall; proof: SQUARE-IN-TRIANGLE); **STRIP-LANDING** (if C sits between a lower-right line of slope angle α′ and
> an upper-left line of slope angle ξ ≤ α′ and the sweep is free, C slides to a wall along any direction in
> [ξ, α′] and lands: in particular at COMMON TILT a floating row end always lands).
>
> **[F] "a straight slide lands it / what blocks it is a lower box meeter"** (brief, task 1): witness **LIFT** — the
> END square of a wall row pushed 0.41 off its wall; both straight drops blocked (by the wall's next square X, 0.052,
> and by the floor's A), all margins 0.052; yet C lands by STRIP-LANDING.  The right test is any-pose P1, not a drop.
> **[F] TOUCH-NORMAL from P1 inside the corner** — witness **JAM, the JAMMED FLOATER** [M, exact geometry check]:
> A (floor, 13.7°) and C (FLOATS 0.72 off the wall, 13.7°) meet the box, X (wall, 27.9°) above; pair gaps ≥ 0.0104,
> box depths 0.0104 / 0.069; **every wall-touching unit cell of any tilt that meets C overlaps A or X by ≥ 0.0090,
> and no empty wall cell exists (−0.069)**.  The wedge between X's edge (steep) and A's edge (shallow) closes
> TOWARDS the wall (ξ > α′): C fits where no wall toucher does.  The family persists at ring offsets (a₀ ≤ 0.8:
> margin 0.0033, tilts 18.3° / 16.4° / 18.4°).  So O1 is NOT a corner lemma; what remains is ring-level (§1.5).
>
> **[M] corpus** (`census261`): below side 4 the doubly-met corners are 29 PAIR (+ 56 on the rings), 2 FLOAT1,
> 1 FLOAT2 (not 0, as the brief says: `cp85_032`, s = 3.9240, TR) — all three are rattlers within 4·10⁻³ of a wall
> with a FREE straight drop; no third meeter, no same-wall toucher pair anywhere (3 242 doubly-met corners).
>
> **[T-computed] O3, so far** (§3): the exclusions are recast as "no x ∈ [0,1]⁴ × [3, 3.8771] satisfies the ring LP
> for ANY per-wall tilts", certified per dyadic tilt box by LP duals + an outward-rounded MEAN-VALUE bound, own
> verifier, the admissible separating axes fixed by PUSH (≤ 2 per corner — [M] identical to A258's numeric forms,
> 800/800).  **No closed-LP certificate can reach a flat wall** (§3.2: at tilt 0 the closed relaxation is feasible
> at s = 3), so the certified domain is tilts ∈ [0.703°, 45°] per wall plus EXACTLY flat walls as their own jobs.
> Status at exit: §3.4.  **[F] (mine, caught by the engine): "a slab of near-flat tilts is excluded"** — the one-sense
> family D′ reaches tilt 0.7°–1.4° on one wall at ŝ (b → 1⁻); only the EXACTLY flat row costs 3.9347.
>
> **Plainly:** BOX-MEETERS(11) is **[C]**; reduced to one statement, NO-JAM(11) (§1.5).  FAMILY-STUCK-EXIST(11),
> ONLY-RING(11), k0_00: **unchanged**.

## 1. O1 — floating box meeters

Corner frame (u, v) of BL; box (0,1)²; C a unit square of the quadrant meeting the box and touching no wall
("floater"); h_u, h_v > 0 its wall distances (both < 1, since C has a point below 1 in each coordinate).
DROP cells T_u := C − h_u e_u, T_v := C − h_v e_v (unit cells touching a wall, ⊆ the quadrant, both meet C).

**1.1 P1⁺ [T] (any n, s).**  *Let P\* maximise Φ₁ (the number of wall touchers) and have a non-toucher.  For every
family Π of pairwise interior-disjoint wall-touching unit cells ⊆ [0,s]² (any poses) with |M(Π)| ≤ |Π|: every
square of M(Π) is a toucher, and |M(Π)| = |Π| or no non-toucher lies outside M(Π).*  Proof: Lemma CELLS with
X = M(Π) ∪ (|Π| − |M(Π)| further squares, non-touchers first) gives a packing at side s with
Φ₁ − #touchers(X) + |Π| touchers.  ∎  |Π| = 1 is A258's P1.  |Π| = 2: if a wall cell T has M(T) = {C, X}, C a
floater, then NO wall-touching cell T₂ disjoint from T has M(T₂) ⊆ {C, X} — C's blocker has nowhere else on the
walls to go (the Φ₁-analogue of P2′).  By acyclicity of "below" for disjoint convex sets, every straight drop of a
floater is blocked by a chain of squares ending in a TOUCHER — of any wall (this is all A258's remark "poked under
from every wall side" contains).

**1.2 BLOCKER-SIDE [T] (s-free).**  *Let Y be a unit square of the quadrant, interior-disjoint from C, meeting T_v.
Every line separating them, with normal n pointing from Y to C, has n_v > 0 and n_u < 0.*  Proof: take p ∈ int Y ∩
int T_v; p + τ e_v ∈ int C for some τ ∈ (0, h_v], so n·p < β < n·p + τ n_v: n_v > 0.  If n_u = 0, Y ⊆ {0 ≤ v ≤ β}
with β ≤ h_v < 1: no unit square.  If n_u > 0, Y lies in the right triangle with legs u₀ = β/n_u, v₀ = β/n_v; C has
a point q of the open box with n·q ≥ β, so β < n_u + n_v, i.e. 1/u₀ + 1/v₀ > 1: no unit square (SQUARE-IN-TRIANGLE,
`construct_towards.md`; Lean core `blocker_side_core`).  ∎  Mirror: a blocker X of T_u is separated from C by a
normal m (from X to C) with m_u > 0 > m_v.  So **a blocked floater sits between two lines of positive slope: its
floor-side blocker below-right, its wall-side blocker above-left** — the geometry of a row END pushed off its wall.
By PUSH (i) the box's other meeter is separated from C by a line of positive slope too.

**1.3 STRIP-LANDING [T] (s-free) and the witness LIFT.**  *Let every square other than C lie in
{n·x ≤ β_A} ∪ {m·x ≤ β_X}, n = (−sin α′, cos α′), m = (sin ξ, −cos ξ), α′, ξ ∈ (0°, 90°), and C in the wedge between.
If ξ ≤ α′ then for ψ ∈ [ξ, α′] the translates C − t (cos ψ, sin ψ) stay in the wedge (d·n = sin(α′ − ψ) ≥ 0,
d·m = sin(ψ − ξ) ≥ 0; Lean `strip_landing_core`) until C touches a wall: a wall-touching cell T with M(T) ⊆ {C};
by P1, P\* has no such floater.*  At common tilt the two lines are A's upper-left edge and X's lower-right edge:
parallel.  **Witness LIFT** (`results/local261_seeded.jsonl`, page `floating_meeter.svg` (a)): the END square of a
wall row of tilt 14.6° pushed 0.414 off the wall, X slid down onto it, A below; least margin **0.052** (pair gaps,
box depths, drop overlaps); both straight drops blocked, by TOUCHERS; the landing cell is C slid along its own edge.
**[F] my first search**: random-start Nelder–Mead on the blocked-drop scenarios returned sup-margin 0.0000 on all of
A, B, B2, C, D, E (`results/local261.jsonl`) — while LIFT (= the mirror of B2) has margin 0.052.  Those rows are
**UNRELIABLE non-results**, kept only as a warning: contact structures need seeded starts.

**1.4 The JAMMED FLOATER [M, exact check] — the counterexample.**  When ξ > α′ the wedge closes towards the corner.
`jam261` maximises min(pair gaps, box depths, float distances, −J), J := sup over wall-touching cells T (both
walls, all tilts and positions) of min(gap(T, A), gap(T, X), depth(T, C)).  Witness
(`results/jam261_polished.json`, checked by `checkjam261.py` from the poses alone — containment, SAT gaps, J by a
1° × 0.01 grid + Nelder–Mead from the 150 best cells, and the same for EMPTY cells):

| | centre | tilt | touches | box depth |
|---|---|---|---|---|
| A | (1.535, 0.604) | 13.67° | floor | 0.0693 |
| C | (1.328, 1.594) | 13.69° | nothing: 0.724 off the wall, 0.990 off the floor | 0.0104 |
| X | (0.676, 2.514) | 27.91° | wall | — (does not meet) |

gaps C–A 0.0104, C–X 0.0109; **J = −0.0090, empty-cell sup = −0.069**.  It is a robust open set of poses, a LOCAL
counterexample (three squares; s-free, so for every m ≥ 4).  [M] the third-meeter variant (X also meets the box):
none found (−0.09; unreliable, see 1.3); A258's C4 slice: none.  What the corner cannot decide: whether the REST of a
ring closes around a JAM corner — wall 3 then carries ONE toucher X (START, tilt φ_X) and the floater C as its END.

**1.5 What remains, exactly — NO-JAM(11) [C].**  *At s ∈ [3.82, ŝ] no packing of 11 in normal form (P1⁺, P2–P4) has a
doubly-met box with a floater.*  By 1.2–1.3 a floater is a JAM: blocked below-right by a floor-side square and
above-left by a wall-side square with ξ > α′ — for ring squares of sense +, **φ_X > φ_A: the wall's next toucher is
tilted MORE than the floor's start square** (witnesses: +14.2°, +2° at a₀ ≤ 0.8).  Routes: (i) P1⁺ with |Π| = 2, 3:
C → the slot-like cell it leaves free once A's row slides (the slot [0,1]² is met by A and C only, overlaps 0.069 /
0.010) — needs slack at the floor's END corner, false on D_tight; (ii) a ring-level certificate: the JAM corner + three
rows of two, 11 + 1 coordinates, the inner sup J making it a min-max — not priced, no benchmark taken; (iii) hand
arithmetic [M] on the first witness (a₀ = 0.947 ⟹ b₀ = 0.69 ⟹ the BR and TR corners cannot both close with tilts
≤ 45°) does NOT extend to the a₀ ≤ 0.8 witnesses.

## 2. O2 — same-wall pairs, third meeters

**2.1 SAME-WALL [T]** — §0; Lean core `same_wall_core`, prose axiom `meeters_split`.  The brief's two patterns:
"two floor touchers" is impossible outright (page `same_wall.svg` (a): an illustration, NOT a packing, overlap red);
"row start + second-layer square" is a toucher + floater, hence O1; on the corpus it occurs once below 4
(rand_0_0441, s = 3.9352, TR: floater 1 sits 2.4·10⁻⁶ under the ceiling, free drop — a rattler; page (b)).
**2.2 Count [T].**  Meeter centres lie in distinct cells of the 2 × 2 grid at 1 (A2): ≤ 4 meeters; with one toucher
per wall present, a third meeter floats and is separated from BOTH by lines of positive slope (PUSH (i)), i.e. it
lies in the chain B (upper-left) – C – A (lower-right) or outside it.  At common tilt with C between the facing
edges the strip has width a sin φ + b cos φ − 1 < 1 for a, b < 1 [T]; in general **[M] none found** (C4 slice A258;
scenario C and JAM3 here, both from unreliable random starts) — it is the case "X meets the box" of NO-JAM.
**2.3 Does a third meeter break the classification?**  Not by the family count (|M| only grows), and A258's
classification uses only the two touchers; but the floater is then the ring's ninth square and must be HELD (P4): it
meets the box, so RETREAT asks that it cannot be re-posed off the box — covered by NORMAL-ROOM's pocket (A259), not
by anything here.

## 3. O3 — the window exclusions as certificates

**3.1 The statement certified per job** (senses σ, row lengths l, tilt domain): *for every tilt vector in the domain
there are no a ∈ [0,1]⁴, s ∈ [3, 3.8771] with b_w = s − κ_w(φ_w) − a_w ∈ [0,1] and, at every corner, a separating
edge normal in the OPEN second quadrant.*  **[T] the admissible axes**: both corner squares meet the open box, so by
SAT + PUSH (i), (ii) a separating edge normal m (from the floor's START square to the wall's END square) has
m_u < 0 < m_v; a square of tilt θ ≢ 0 has exactly one such normal, a FLAT square none.  Closed forms (any senses;
θ_A = σ_A α, θ_B = σ_B β, μ the normal's angle, w(x) = |cos x| + |sin x|):
`sep = −cos μ · a + sin μ · b + (cos μ + sin μ)(w_β − w_α)/2 − [w(μ − θ_B) + w(μ − θ_A)]/2`, μ = α + 90° (σ_A = +),
180° − α (σ_A = −), likewise for B — A258's E_A, E_B when σ = ++ ([M] `test261`: equal to `dom258.corner_forms` on
800/800 random corners, all four sense pairs: A258's "[M] the other axis never decides" is now [T]).
**Leaf certificate**: a list of (pattern ∈ {form 0, form 1, any}⁴, y ∈ ℝ₊¹²); S := Σ yᵢ rowᵢ ≤ 0 on the feasible set
(Lean `cert_core`), S is linear in x, so min S is attained at one of 32 vertices; per vertex the verifier takes the
better of the natural and the MEAN-VALUE enclosure over the tilt box (outward rounding by `nextafter`, cos / sin
padded 2·10⁻¹⁵, κ, w, cos − sin and κ′ enclosed by monotonicity, κ's coefficient grouped) and demands > 0 for
patterns covering all admissible choices.  Boxes come from a bisection tree in preorder: they tile by construction.
Overestimation of the bound: ×1.0–2.9 of the true variation (was ×5–8 with natural extension only).
**3.2 [T] No closed-LP certificate reaches flat — and the margin law.**  At tilt 0 the closed conditions (a, b ≤ 1)
are satisfied at s = 3 (a = 1, b = 0 on every wall: squares side by side); strictness (a, b < 1) is invisible to a
Farkas row.  Near flat the infeasibility margin of the mixed patterns is ∝ ε (the tilt) while the forms vary by
O(h) over a box of width h, so h/ε ≈ 0.07–0.1: ≈ 4·10³ leaves for the corner cube [0.7°, 2.8°]⁴ (measured:
1 438 leaves on 39 % of it) and a log-divergent count as ε → 0.  Hence: tilts ∈ [TMIN, 45°], TMIN = 45°/64 = 0.703°,
+ EXACTLY flat walls as separate jobs (a flat square owns no admissible axis).  **NOT covered: some tilt in
(0°, 0.703°)** — [M] only (A258's polish went to 0.05°).  Near-flat is not an exotic regime for the ONE-sense family
(it exists there), which is why a "flat slab" job is FALSE: the engine found feasible centres at once.
**3.3 Jobs** (50): M1 + + + −, M2 + + − −, M3 + − + − (rows of two); F0_xyz (wall 0 exactly flat, senses xyz of walls
1–3: 8), F02_xy (walls 0, 2 flat: 4; adjacent flat walls: [T] the two squares overlap); R\<lengths\>_\<senses\>:
every ring with a row of THREE up to rotation / reflection (35).  **Benchmark / price** (`price261`, Monte-Carlo of
∫ h⁻⁴): M1 ≈ 4·10⁵ leaves (heavy tail; the margin 3.9298 − 3.8771 lives near (14°, 14°, 14°, 11°), τ\* = 0.0074),
M2 ≈ 1·10⁴, M3 ≈ 2·10⁴, F0_ppp ≈ 7·10⁴, the rest 10³–10⁴; measured rate 45–75 boxes/s ⟹ **M1 ≈ 5–25 CPU-h, all
others together ≈ 2–3 CPU-h: within the 50 CPU-h limit, launched** (48 h budget, M1 last).
**3.4 Status at exit** — `results/cert261.jsonl` (one row per finished job: leaves, seconds, verifier verdict);
the chain re-verifies each certificate with `verify261.py` as it finishes.  See the LOG entry for the list at exit.
Certificates over 1 MB are not committed (`certs/*.leaves`, `*.tree` are git-ignored; `certs/manifest.json` has
sha256 + leaf counts; regenerate with `run261.sh cert`, deterministic).

## 4. General m

m-FREE (corner statements, any n, s > 1 + √2): SAME-WALL, the meeter types, P1⁺, BLOCKER-SIDE, STRIP-LANDING, LIFT,
JAM, the admissible-axes lemma and the closed forms of §3.1, the certificate kernel (κ_w = (l_w − 1) sec φ + w is
already general in l_w).  m = 4 ONLY: the job list (rows of 2 or 3, s ∈ [3, 3.8771]), "opposite walls never
interact", the numbers.  For m ≥ 5 the same engine certifies "no pinwheel of rows of lengths l_w ∈ {m−2, m−1}" with
s ∈ [m−1, s₀]; the flat obstruction of §3.2 is the same (side m − 1 at tilt 0).

## 5. The chain to ONLY-RING(11), value form

packing at s ⟹ [T `exists_normalForm`] a packing not family-stuck (k ≥ 1 classes) or a NORMAL-FORM family-stuck P\*
⟹ [C **NO-JAM(11)** = `touch_normal`] no box meeter of P\* floats ⟹ [T-prose `meeters_split`: SAME-WALL +
WEDGED-SEAL + TWO-CORNERS] every box has exactly two meeters, touchers of its two walls, eight distinct
(= BOX-MEETERS, Lean `box_meeters`) ⟹ [T A258 §3.1] each wall carries a row of two, a row of three or an open pair
⟹ [T-computed §3, on tilts ≥ 0.703° and exactly flat; [M] on the slab] rows: one sense, rows of two, not flat
⟹ [C A258/A260: locked walls, open pairs of unequal tilts] the hybrid normal ring (`rows_classified`) ⟹
[A259/A260 room] FAMILY-STUCK-EXIST(11).  Lean `normal_ring_of_parts`, `only_ring_value_261`: theorems from the two
[C] axioms.  **Remaining obligations, exactly:** (R1) NO-JAM(11) — incl. the third-meeter case; (R2) the tilt slab
(0°, 0.703°) of §3.2 for the mixed and row-of-three patterns, and exactly-flat rows inside row-of-three rings;
(R3) M1 (and any job unfinished at exit) to completion + verifier; (R4) pinwheels with an OPEN PAIR wall are not
"pinwheels of rows": A260's hybrid family; (R5) the Lean prose axioms.

## 6. What the brief had wrong

1. "Below 4 the corpus has NO doubly-met corner without a wall toucher": there is one (cp85_032, FLOAT2) + two
   FLOAT1 — all rattlers with a free drop, so the intended point stands.  2. "A straight slide of C toward the wall
   (what blocks it must itself be a lower box meeter)": [F] — LIFT: the blocker is the wall's NEXT square, not a
   meeter, and C lands anyway by another cell.  3. "Two floor touchers … show it is not family-stuck": stronger —
   impossible [T].  4. O2 is not independent of O1.  5. "Coarse boxes should do": true in the bulk (leaf width
   ≈ 3°–6°), false near flat (h ∝ tilt) and near (14°, 14°, 14°, 11°); and "no flat row" cannot be a slab statement.
6. BAND-COUNT does not explain the corpus: the corpus floaters are rattlers; the structural floater is JAM.

## 7. Lean, reproduce

`Statements/Open/BoxMeeters.lean`: theorems `same_wall_core`, `blocker_side_core`, `strip_landing_core`, `cert_core`,
`box_meeters`, `normal_ring_of_parts`, `only_ring_value_261`; axioms [T-prose] `meeters_split`, `rows_classified`; [C] `touch_normal`
(= NO-JAM); opaque `FloatingMeeter`, `BoxMeetersForm`; build + audit 0 sorry.  Reproduce:
`bash attempts/A261-box-meeters/code/run261.sh test|census|pages` (≤ 2 min each), `local` (unreliable rows, 10 min),
`python code/jam261.py` + `checkjam261.py` (JAM_COARSE=1 for the search; ≈ 10 min), `cert [hours]` (detached,
resumable, `logs/STOP`), `verify`.
