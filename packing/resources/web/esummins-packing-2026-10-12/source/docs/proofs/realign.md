# REALIGN — how a grain re-aligns once a corner is settled: Lemma WALL-EXCESS, the anchored drain, the dichotomy, and what it closes — A231, 2026-09-15

The PI (09:50): "any actual assertion would require us to make some statement about how the grain re-aligns — the grain
that's now corner settled"; (10:05): "each non-flush corner corresponds to at least one grain, so there must be at least one
grain we can select where draining that grain to flush improves the global packing … doing so removes the wastage along the
outer wall where that grain meets the wall".  This file (i) proves the wall-wastage lemma in the form that is true
(Lemma WALL-EXCESS: a chord budget, plus the sealed-pocket area), (ii) defines the anchored re-alignment exactly and tests it on
every corner-swapped four-crowd the lab has (the ring, the 193, the 40 window-over-met crowds, A226's eight CROWD-ABOVE crowds
at n = 26 … 55), (iii) states Lemma REALIGN with the flush-side / kink-side dichotomy read off the chain menu, proves the
feasibility and the monotonicity that can be proved, and (iv) says what closes.  Tags: [T] proved, [S] routine given cited
items, [M] measured, [F] false as stated (with the witness), [C] conjecture / obligation.  Sources: `two_grains.md` (CLICK,
EXTENT, LEAN-SLIDE, FLUSH, the ring's chain formulas), `grain_flood.md` (GRAIN-LP, GRAIN, CONT, INHERIT, the menu Λ, Y, D, F_T),
`ring_swap.md` (SWAP, STEP, CELLS, RAISE, CORNER-SWAP), `one_flush.md` (ONE-FLUSH ⟺ UNCROWD, CROWD-ABOVE), `wall_budget.md`
§1.1 (Lemma WALL-F), `descent.md` D3 / `descent_grains.md` §6 (common-tilt moves).  Code `attempts/A231-realign/code/`
(`geomn231.py` n-general geometry + the fixed-tilt LP with a pinned slot, `inputs231.py`, `realign231.py`, `summarise231.py`,
`pages231.py`, `test231.py`, `run231.sh`), results `results/realign231.{md,jsonl}` (964 rows), pages
`docs/residue_map/campaigns/A231-realign/`, Lean `Statements/Open/Realign.lean`.  n-general throughout; n = 11 in §5.

## 0. Verdict

> **[T] Lemma WALL-EXCESS** (§1): the squares touching a wall have pairwise-disjoint chords `1/max(cos θ_i, sin θ_i) ≥ 1` on
> the line at distance 1/√2 from it (Lemma WALL-F on the touchers), so Σ_i 1/max(c_i, s_i) ≤ s and the wall carries at most
> ⌊s⌋ touchers; each term exceeds 1 by the EXCESS `1/max(c_i, s_i) − 1`, zero only flush.  The PI's Σ(cos θ_i + sin θ_i) ≥ k is
> true but not a budget (projections overlap, `wall_budget.md` §1.3); the chord form is.  Sealed pockets — consecutive touchers
> in contact, the pocket holding no unit square — are waste [T]; two touchers of common tilt φ sealed by a vertex-on-edge contact
> have floor spacing exactly `1/max(cos φ, sin φ)` and pocket area exactly `tan(min(φ, 90° − φ))/2`; the PI's "two triangles per
> square, Σ sin θ cos θ" overcounts by what the neighbour takes back.  **[M] The anchored re-alignment** (§2): after A222's
> CORNER-SWAP the fixed-tilt SHRINK with the settled square pinned lowers the side STRICTLY on 783 of the 792 corner-swapped
> cases (678/686 on the 193 four-crowds, 73/74 on the 30 window-over-met crowds not among them, 32/32 on the eight CROWD-ABOVE
> crowds, n = 26 … 55); the 9 exceptions all reach 4.000 < s0 when every tilted square re-aligns.  The grain IN CONTACT with the
> settled square is EMPTY after the shrink in 472 of 686 cases (the meeters are gone; S sits between flat squares) and is the
> whole opposite chain (6–10 squares) in 195 of the other 214; its anchored move is never blocked (0/214), flush-side on 196,
> kink-side on 10, unloaded on 8, and continues down to 4.000 on 194.  **[F] "Each non-flush corner corresponds to a grain we
> can drain"**: the corner's grain is the two meeters' grain, and the swap CONSUMES the meeters; what re-aligns afterwards is
> whatever leans on S, often nothing.  **[T] Lemma REALIGN's dichotomy is a statement about the value function s_min, not about
> a formula** (§3): on the menu, F_T is flush-side above 24.3° yet Trump's grain is kink-side because the loaded basis changes
> (INHERIT (iii)); the horn is the sign of ds_min/dt along the anchored move, decided per packing.  **[F] The area horn** (§4):
> even with EVERY wall square at 45° and sealed, the waste is 2⌊s/√2⌋ − 1 = 3 at n = 11 against s(11)² − 11 = 4.03 — no
> contradiction; the bound beats the slack only from n = 55 on (9 > 8.14), and never under the hypothesis actually available
> (four kink-side CORNER grains: ≤ 3).  **What closes** (§5): at n = 11 the four-crowd exclusion on [3.82, ŝ) needs STEP alone
> (a corner swap exists) with k1-a — Lean `fourcrowd_dead_of_step_kill`, no REALIGN — i.e. RAISE(0 → 1) as before; REALIGN is
> what ONE-FLUSH needs at general n (Lean `one_flush_of_realign`: REALIGN + STEP ⇒ ONE-FLUSH(n)), and its content is the STRICT
> improvement, [M] on 792/792 cases, [C] as a theorem.  k0_00 unchanged.

## 1. Lemma WALL-EXCESS (any n) [T]

**1.1 The chord form.**  Fix a wall w, frame it as {y = 0}, h₀ := 1/√2.  A square Q of tilt θ (φ := dist(θ, 90°ℤ) ∈ [0, 45°])
TOUCHES w iff its lowest point has height 0.  Lemma WALL-F (`wall_budget.md` §1.1, [T]): the open chords int Q ∩ {y = h₀} of
all squares are pairwise disjoint sub-segments of (0, s) × {h₀}, hence Σ_Q |chord| ≤ s; and a toucher's chord is EXACTLY
`1/cos φ = 1/max(cos θ, sin θ)` (its lowest vertex at the origin, the line y = h₀ ∈ [sin φ, cos φ] cuts the lower-left edge
and the right edge, length cos φ + sin φ tan φ).  Hence for the touchers T_w of w:

  **Σ_{i ∈ T_w} 1/max(cos θ_i, sin θ_i) ≤ s,  each term ≥ 1 with equality iff the square is flush;  |T_w| ≤ ⌊s⌋.**

The EXCESS of a toucher is `e(θ) := 1/max(cos θ, sin θ) − 1 ∈ [0, √2 − 1]`, and Σ e(θ_i) ≤ s − |T_w| is the wall's slack.
[F] The PI's Σ_i (cos θ_i + sin θ_i) ≥ k is true (each projection ≥ 1) but the projections of disjoint touchers can OVERLAP
(`wall_budget.md` §1.3: by up to 0.092), so it bounds nothing; the chord sum does, and cos θ + sin θ ≥ 1/max(cos θ, sin θ)
[T: (c + s)·max(c, s) ≥ c² + s² = 1], so the chord excess is the smaller of the two.  Lean: `lemma_WALL_EXCESS` (axiom, this
prose), `chordT_ge_one`, `wall_count_le` (theorems).  ∎

**1.2 Sealed pockets.**  Let i, i+1 be consecutive touchers of w (no other toucher's floor point between theirs) IN CONTACT at a
point p, and let R be the region bounded by w, the boundary arc of i from its floor point to p, and the arc of i+1 from p to
its floor point.  R is SEALED iff no unit square fits inside R.  [T] A sealed pocket is waste: no square's interior meets R.
*Proof.* ∂R ⊂ ∂i ∪ ∂(i+1) ∪ w; a square Q with int Q ∩ R ≠ ∅ and int Q ⊄ R meets ∂R (int Q connected), i.e. contains a
boundary point of i or i+1 in its open interior, hence meets that square's interior (a boundary point of a convex body with
interior is a limit of interior points) — contradiction; and int Q ⊂ R is excluded by sealing.  ∎  A sufficient sealing
condition: height(R) < 1 (a unit square's vertical extent is ≥ 1).  **Common tilt, exact [T].**  Two touchers of tilt
θ ∈ (0°, 90°), i's lower-right edge from its floor vertex v_i in direction d₁ = (cos θ, sin θ), i+1's lower-left edge from
v_{i+1} in direction d₂ = (−sin θ, cos θ), contact p = v_i + a d₁ = v_{i+1} + b d₂ with a, b ∈ [0, 1] and both floor vertices on
the floor: a sin θ = b cos θ.  Interior-disjointness of two translates by t = v_{i+1} − v_i = a d₁ − b d₂ needs |t·d₁| = a ≥ 1
or |t·d₂| = b ≥ 1, so a = 1 (θ ≤ 45°, b = tan θ) or b = 1 (θ ≥ 45°, a = cot θ): the floor spacing is `x_{i+1} − x_i = a cos θ +
b sin θ = 1/max(cos θ, sin θ)` — WALL-EXCESS's chord, attained — and the pocket is the right triangle with legs a, b at p,
area `ab/2 = tan(min(θ, 90° − θ))/2`, height a sin θ = min(sin θ, cos θ) < 1: sealed.  So a sealed wall grain of k touchers at
common tilt φ wastes `≥ (k − 1) tan φ / 2` between its members, and a member touching the side wall too (a corner toucher)
seals a further corner triangle of area `sin φ cos φ / 2` between the two walls and its lower-left edge.  **[F] Two triangles
per square.**  The two triangles under a toucher's lower edges have total area sin φ cos φ, but the neighbour in sealed
contact occupies part of them: the union of i's right triangle and i+1's left triangle exceeds the pocket by `sin φ cos φ −
tan φ/2` (0.144 at 30°, 0 at 45°) — that is what the neighbour "takes back".  **[T] An unsealed gap.**  If consecutive touchers
are not in contact, a third square Q may poke into the gap; the pocket below the height of Q's lowest point is still waste
(the same argument on the region below Q), but no bound in the tilts alone survives: Q can reach the floor, and then it is a
toucher and the pair was not consecutive.  Mixed tilts: the pocket is the triangle (v_i, v_{i+1}, p), area = spacing · height(p)/2;
a flat square beside a tilted toucher seals the tilted square's whole lower triangle sin φ cos φ / 2.

**1.3 What the drain recovers [T where stated].**  Draining a wall grain to flush turns every chord into 1: the chord bound
s ≥ Σ_i 1/max(c_i, s_i) drops to s ≥ k.  That is a LOWER bound decreasing, not the side decreasing: the side along the drain
is the LP value s_min(θ(t)) (Theorem CONT), decided by the loaded basis (INHERIT).  Where it IS quantitative: if the loaded
wall-to-wall chain is of EXTENT type (Lemma EXTENT, `two_grains.md` §2.2: vertex-to-vertex kisses and wall vertices, no gap
terms) then s = Σ_j (cos φ_j + sin φ_j) along the drain and the drop to flush is `Σ_j (cos φ_j + sin φ_j − 1) ≥ Σ_j e(θ_j)`,
at least the wall excess.  For gap / ladder chains (Λ, F_T) the formula can rise toward alignment and the drain stops at a
kink (§3).

## 2. The anchored re-alignment, defined and measured

**2.1 Definitions [T].**  P a FOUR-CROWD at side s₀ < ⌈√n⌉ (every corner box met by ≥ 2 squares).  CORNER-SWAP at c
(`ring_swap.md` §2.1): X = the two meeters, X′ = the slot square S at c + one LEFTOVER L in U(X) \ int S — a packing P′ at the
SAME side (Lemma SWAP).  The SHRINK: min s over the centres at P′'s tilts with S pinned to its slot (rows c_S = ½ or s − ½,
affine in (c, s)), the alternating separating-axis LP of Lemma GRAIN-LP warm-started at P′: value s_lp0 ≤ s₀ (P′ is feasible),
configuration P₀.  The ANCHORED GRAIN: G_h = the contact component of S among the tilted squares of handedness h at P₀ (for each
h that touches S), G_comp = the component among all tilted squares, G_all = every tilted square.  The ANCHORED MOVE of G: its
members rotate toward their own alignment ('+' → 0°, '−' → 90°; diamonds → 0°), every other square keeps its tilt, S stays
pinned, and at each of 20 steps the side is minimised over the centres — variant A with P₀'s contact axes kept (lean contacts
slide), variant B with every axis re-selected.  HORN: FLUSH-SIDE if the first step lowers the side, KINK-SIDE if it raises it,
FLAT if unchanged (an unloaded grain).  ENDPOINT: where the path's minimum sits — flush (t = 1), kink (interior), start (t = 0),
or blocked (P(S, θ(t)) ∩ {c_S = slot} = ∅ at some step; the blocking pairs and whether the free axes are feasible there are
recorded).  Inputs (`inputs231.py`): the ring and the 193 four-crowds with A222's `z_swapped` at every corner where CORNER-SWAP
succeeded (686 of 772 corners); the 40 four-crowds of A222's 1,172 on which the window-shaped 8-cell family is over-met in every
sub-family (10 of them are among the 193; the other 30 swapped here by A222's region search, 74 of 120 corners); A226's eight
CROWD-ABOVE crowds with the explicit RETRACTION swap ((A′, B′) → (slot, flush neighbour), verified packings, 32/32).

**2.2 Lemma ANCHOR-SLIDE [T] (feasibility at a lean).**  Pinning S adds two equality rows affine in (c, s) with no tilt in them;
Lemma LEAN-SLIDE (`two_grains.md` §2.5) applies verbatim: a lean contact row g = n_A(θ_A)·(v(θ_B, c_B) − c_A) − ½ has centre
coefficient ±n_A ≠ 0 at every t, so a single lean never blocks the anchored move — the vertex slides on the edge; a block is
P(S, θ(t)) ∩ {c_S = slot} = ∅, a global cycle of rows (a pin above, a caged rattler, or a released pair's stale axis).  [M] Never
observed: 0 blocked paths in 214 + 12 + 63 anchored runs and 0 in the 1,148 'all' runs (`realign231.md`).  ∎

**2.3 Lemma ANCHOR-MONO [T] (monotonicity where the formula is monotone).**  Along the anchored move with the loaded basis B
constant, s(t) = F_B(θ(t)) (INHERIT (i)); S's rows contribute constants (S is flush and pinned: its chain segment is a unit
length and its corner is fixed), so the chain through S has a FLUSH SEGMENT and F_B is the menu formula of the remaining tilted
part plus a constant.  If that part is of extent type, F_B decreases strictly toward alignment (Lemma EXTENT); if it is a ladder
Λ(θ) = 2 + 4t/(t² + 1) or a column Y, F_B increases toward alignment on both sides of 45° (`two_grains.md` §2.3); a gap chain F_T
decreases toward 0° on θ > 24.3° and increases below; D = F_T(90° − θ) mirrors it toward 90°.  Hence on the flush side of an
extent basis the anchored move is side-decreasing until the basis changes (a kink) or the grain is flush.  ∎  [M] compA is
non-increasing at every step on 178/214 (193) and 9/12 (win40); the upticks are INHERIT (iii) branch turns after a descent
(largest 0.025, `realign_worst_w207_crowd.svg`: compA ends at 4.089 after a kink at t = 0.55, compB and allA reach 4.000).

**2.4 What was measured (`realign231.md`) [M].**

| population | cases (witness × corner) | swap exists | SHRINK strict (s_lp0 < s₀) | G_comp empty | compA: flush-side / kink-side / flat | compA endpoint flush / kink / start / blocked | compA ends < s₀ | allA ends < s₀ |
|---|---|---|---|---|---|---|---|---|
| ring + 193 four-crowds | 772 | 686 | 678 / 686 | 472 / 686 | 196 / 10 / 8 | 194 / 9 / 11 / 0 | 213 / 214 | 510 / 510 |
| 30 window-over-met crowds | 120 | 74 | 73 / 74 | 62 / 74 | 10 / 1 / 1 | 10 / 1 / 1 / 0 | 12 / 12 | 64 / 64 |
| 8 CROWD-ABOVE (n = 26 … 55) | 32 | 32 | 32 / 32 | 32 / 32 | — | — | — | 14 / 31 (allB 32 / 32) |

Per witness: every one of the 193 has ≥ 1 corner where swap + shrink is strict (193/193); 119/193 have a corner whose G_comp is
flush-side, unblocked and ends below s₀; the 30 and the 8 likewise 30/30 and 8/8 by the shrink.  The 9 non-strict shrinks
(w047 TR, w053 TR, w059 BR, w107 TL, w108 TL, w147 BR, w183 BL/TL, crowd_10_0424 TR) have G_comp empty or unloaded, and their
'all' path reaches 4.000 < s₀.  The ring (§4 of the table): BL has no swap (rattler 0 in the pocket, A222); BR: 4.1099 → 4.0637
by the shrink, S touches one '+' square (20°) that is UNLOADED (flat horn) and 'all' clicks to 4.000; TR: 4.1099 → 4.0648, S
between two flat squares, G_comp = ∅; TL: 4.1099 → 4.0919, G_comp = the whole eight-square chain, flush-side, monotone to 4.000
(page `ring_realign_rand_0_0569_t20.svg`); the one-handed part G_− alone ends at a kink 4.0383 (t = 0.9) in variant A and at
4.000 in B.  Size of G_comp when non-empty: 6–10 in 195/214 — S leans on the OTHER chain, not on "its" grain, because the
meeters that made the corner's grain are the swapped squares.  The CROWD-ABOVE crowds: S touches only the flush neighbour
(G_comp = ∅ in 32/32); the shrink alone recovers most of the slack (n = 26: 5.8107 → 5.6444 against the record 5.6213; n = 55:
7.9729 → 7.9488 vs 7.9458), the rest being the three remaining crowds' tilted meeters; the 'all' move (which also rotates the
record's own grain) is kink-side on 20/31 of them — the record's grain is at its kink minimum, exactly the dichotomy's horn (b).

## 3. Lemma REALIGN — the statement, the dichotomy made exact, what is proved

**Lemma REALIGN(n) [C], candidate.**  Let P be a four-crowd at side s₀ < ⌈√n⌉ admitting a CORNER-SWAP at c (STEP).  Then n unit
squares pack at some side < s₀.  Mechanism: the SHRINK of the swapped packing, then the anchored move of the grain leaning on S
along the flush-side of its loaded basis to the first kink or to flush.  Equivalent forms [T]: REALIGN(n) = UNCROWD(n)
restricted to four-crowds with a swap; REALIGN(n) + STEP(n) ⟹ ONE-FLUSH(n) (Lean `one_flush_of_realign`).

**The dichotomy, exact [T as definitions, M].**  At the shrunk packing P₀ with loaded basis B (an optimal dual of the LP with S
pinned) and anchored grain G at tilt(s) θ:
 (a) FLUSH SIDE: ds_min/dt < 0 along the anchored move at t = 0.  The move is feasible at every lean (2.2), side-decreasing while
     B stays optimal (2.3), and ends either FLUSH (G's chain segment becomes k unit lengths; if the WHOLE packing is then flush
     the side is ≥ ⌈√n⌉ by Lemma FLUSH — which is why, above ⌈√n⌉, the witnesses all end at 4.000) or at a KINK where a new
     basis with the opposite monotonicity takes over (INHERIT (ii)): a k ≥ 1 packing with a settled corner and a tilted grain
     at the kink tilt.  On the menu the flush-side ranges are: extent chains everywhere; F_T on θ > 24.3° (toward 0°); D on
     θ < 65.7° (toward 90°); Λ, Y nowhere (their minima are at 45°, and toward alignment they rise).
 (b) KINK SIDE: ds_min/dt ≥ 0 at t = 0.  The endpoint is P₀ itself: a k ≥ 1 packing at side s_lp0 ≤ s₀, in a class whose tree
     is certified when the settled corner's class is (at n = 11: every k ≥ 1 class on the window).
 [T] In BOTH horns the endpoint is a k ≥ 1 packing at side ≤ s₀ — but that much is Lemma SWAP alone (the swap is side-
 preserving); the CONTENT of REALIGN is strictness, s_end < s₀.  [M] Strict on 783/792 cases by the shrink and on 792/792 by
 shrink-or-move.  [C] In general: the shrink is strict iff the swapped packing is not itself a fixed-tilt LP vertex at s₀, i.e.
 iff removing the two meeters released the load path through c; the one witness where the anchored grain fails to improve
 (w183 BL: G_− unloaded, compA flat) improves at TL instead.  No proof that a swap ALWAYS releases the load path is offered here.
**[T] The horn is a property of s_min, not of a formula.**  Trump's grain has loaded chain F_T at 40.18°, flush-side by the
formula (F_T decreases toward 0° above 24.3°), yet s_min RISES below 40.18° (`grain_flood.md` §3.3: the Trump-down basis takes
over at 0.0031 per degree) — the horn must be read on the value function.  So "kink-side ⟹ tilts near 45°" is [F]: kink minima
sit at 40.18° (Trump), 45° (S07), 48.4° (S02), and a basis change can make any tilt a kink.  On the witnesses, the compA horn
against the anchored grain's tilts: the 10 kink-side cases have members at 7°–50° mixed (w112 TR: 7.4°, 7.5°, 50°) — kinks of
crossing branches, not diamonds.

## 4. The area horn (PI addendum (2)) [T computed, F as a closing argument]

Hypothesis H₁ ("all four corner grains kink-side"): each corner has a toucher pair at tilt φ ≥ φ* on its two walls, sealed.
Waste ≥ 4 · (corner triangle sin φ* cos φ* / 2 + one sealed pocket tan φ*/2): at φ* = 45°: 4 · (0.25 + 0.5) = 3.0; at φ* = 40°:
4 · (0.246 + 0.420) = 2.66.  Hypothesis H₂ (the strongest: EVERY wall square is a sealed 45° diamond): ⌊s/√2⌋ diamonds per wall,
waste = 4 corners · ¼ + 4 walls · (⌊s/√2⌋ − 1) · ½ = 2⌊s/√2⌋ − 1.  Slack = s(n)² − n (a packing at side s has uncovered area
s² − n ≥ waste).  Records (`one_flush.md` §2):

| n | s(n) | s² − n | H₁ at 45° | H₂: 2⌊s/√2⌋ − 1 | contradiction? |
|---|---|---|---|---|---|
| 5 | 2.7071 | 2.33 | 3.0 | 1 | H₁ only (four flush corners indeed, Göbel) |
| 10 | 3.7071 | 3.74 | 3.0 | 3 | no |
| 11 | 3.8771 | 4.03 | 3.0 | 3 | **no** (the brief's "√2 s > 5.03": s² − 11 = 4.03, waste 3) |
| 17 / 18 / 19 | 4.68 / 4.82 / 4.89 | 4.86 / 5.26 / 4.87 | 3.0 | 5 | H₂ at 17, 19 |
| 26 / 28 / 29 | 5.62 / 5.82 / 5.93 | 5.60 / 5.92 / 6.21 | 3.0 | 5 / 7 / 7 | H₂ at 28, 29 |
| 37 / 40 | 6.60 / 6.83 | 6.54 / 6.63 | 3.0 | 7 | H₂ |
| 50 / 51 / 55 | 7.57 / 7.70 / 7.95 | 7.33 / 8.30 / 8.14 | 3.0 | 9 / 9 / 9 | H₂ |

So the area horn kills only the all-diamond walls (H₂) — and only from n = 17 on, never at n = 11 — and never the hypothesis
the dichotomy actually delivers (H₁: 3.0 < s² − n for every n ≥ 10).  It cannot be repaired by WALL-F either: four kink-side
corner pairs at φ ≥ 40° use 4/cos 40° = 5.2 of the 4 s ≥ 15.5 of wall chord.  As `one_flush.md` §3.3 (c) says for O(ε) crowds,
here for kink crowds: area charges do not close; horn (b) has to be handled by the certified k ≥ 1 classes.  [M] Horn census on
the 193 + 30: at the corners with a non-empty anchored grain, flush-side 206 / kink-side 11 / flat 9; every witness has a
strictly improving corner (§2.4), 129 have a flush-side anchored drain that succeeds.

## 5. What closes

**n = 11.**  [T] Lean `fourcrowd_dead_of_step_kill`: at a side m where no packing contains a corner slot square (k1-a on
[3.82, ŝ)), a four-crowd admitting a corner swap does not exist — STEP(11) + k1-a empties the four-crowds of k0_00 with NO
re-alignment; with K0-FREE for the singly-met corners this is `ring_swap.md`'s RAISE(0 → 1) route, unchanged.  REALIGN adds the
mechanism by which a four-crowd is beaten (a strict improvement — value AND the non-optimality of every four-crowd) and the
measurement that the mechanism never blocks; it does not shorten the obligation: [C] STEP(11) on the window (no four-crowd
below 4.0014 is known; `ring_swap.md` §2.1: CORNER-SWAP fails at 86/772 corners, holds at ≥ 1 corner on 193/193), and k1-a.
Uniqueness at ŝ: unchanged (SWAP-RIGIDITY, `ring_swap.md` §1.7).  **General n.**  [T] Lean `one_flush_of_realign`: REALIGN(n) +
STEP(n) ⟹ every optimal packing below ⌈√n⌉ has a singly-met corner (ONE-FLUSH(n), form (a): no optimal four-crowd); the census
of a packing problem then starts from a settled corner at every n.  Both hypotheses are [C]; the evidence is 792/792 strict
improvements and 0 blocks.  [F] on the way: the projection budget, "two triangles per square", "kink-side ⟹ near 45°", and the
area horn as a closing argument.

## 6. Lean, files, obligations

`Statements/Open/Realign.lean`: `FourCrowdN`, `CornerSwapped`, `TouchesFloor`, `chordT`; axioms `realign` ([C], n-general) and
`lemma_WALL_EXCESS` ([T] in §1.1); theorems `one_flush_of_realign`, `fourcrowd_dead_of_step_kill` (std axioms only),
`chordT_ge_one`, `wall_count_le`; `lake build` + `lean/audit.py` exit 0, no sorry.  Obligations: O-STEP (a corner swap at some
corner of every four-crowd below ⌈√n⌉ — the ring's BL shows a single corner can fail), O-STRICT (the shrink or the anchored move
lowers the side strictly: a released load path), O-WALLF-LEAN (the chord lemma in Lean, routine), O-POCKET (the sealed-pocket area
in Lean, routine).  Resume: `bash attempts/A231-realign/code/run231.sh` (rows appended and committed every 25; the table and
pages regenerate at the end).
