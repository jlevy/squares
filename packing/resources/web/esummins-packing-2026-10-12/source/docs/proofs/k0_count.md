# Lemma K0-COUNT — the PI's torque line in its counting form: what is a theorem, what the witnesses refute — A218, 2026-09-14

The PI's reading (A217 BRIEF 17:40; `attempts/A217-torque-probe/notes/PI_teleport_torque.md`): a corner met by two
squares, both held in the corner, is a jammed joint whose equilibrium constrains the packing.  A217 probed the torque
form and what survived was a COUNT (`notes/torque.md` §4): four doubly-met open corners need 8 distinct meeters plus
≥ 4 along-wall holders = 12 > 11.  This file states the count exactly, proves the two geometric facts it rests on
(Lemma PUSH and Lemma HOLD — the brief's G1, in the only form in which it is true), and reports that its two
remaining hypotheses (LOAD and DISTINCT — the brief's G2) are FALSE on A217's witnesses, with the witnesses drawn.
Tags: [T] proved here, [S] supported, [M] measured, [F] false (with the witness), [C] obligation.  Code:
`attempts/A218-k0-count/code/count218.py` (the test), `fig218.py` (the pages); results `attempts/A218-k0-count/
results/count218.md`, `count218.jsonl`; pages `docs/residue_map/campaigns/A218-k0-count/`; Lean
`Statements/Open/K0Count.lean` (Lemma PUSH as a named axiom, built and audited).

## 0. Verdict

> **[T] Lemma PUSH (any n, any side).**  Two unit squares in the quadrant of a corner, both meeting the OPEN unit
> corner box, push each other OUT: every line separating them has a normal with a strictly positive component in
> the corner frame (i), and a strictly positive component ALONG any corner wall the pushed square touches (ii).
> Both clauses are proved from Lemma B0 / B0′ of `sideband.md`; measured 10,638 of 10,638 loaded partner pushes on
> A217's 2,732 witnesses.
>
> **[T] Lemma HOLD (any n, s > 1 + √2) — G1.**  At a Fritz-John point, a meeter of a doubly-met open corner that is
> PRESSED by its partner (positive multiplier on the pair) has a HOLDER: a third square pushing it toward the corner,
> along its wall if it touches one.  This is exactly what force balance gives, no more.
>
> **[T, vacuous] Lemma K0-COUNT.**  If at every one of four doubly-met open corners the two meeters press on each
> other (LOAD) and the four holders can be chosen distinct and distinct from the eight meeters (DISTINCT), then
> n ≥ 12.  **[F] Both hypotheses fail** (§5).  DISTINCT (the brief's G2, "a holder serves at most two meeters"): the
> true sharing bound is FOUR, a holder is a meeter of the ADJACENT corner in 1,986 of 6,351 loaded holder relations,
> and a FORCE-BALANCED four-crowd with NINE squares exists (`rand_0_0569|t20`, side 4.1099: a compression ring
> through the eight meeters with one link; only the tilt bound is loaded).  LOAD: at the genuine k0 Fritz-John
> points 61 of the 70 doubly-met corners have BOTH meeters carrying no load at all (rattler crowds).  **The count
> does not close k0_00; the k0_00 obligation is unchanged.**  What survives of Lemma TORQUE is C4 as measured (no
> FJ point with four 2-crowds, 0 of 883) and its mechanism, now read two ways: a forced four-crowd wants to SETTLE a
> corner — a meeter slides out along its wall (the CROWD pull is the missing along-wall holder, 3,071 of 3,261) or a
> corner square turns flat (the HELD bound torque is the aligning one, 494 of 494) — the drain, not a count.

## 1. Setting

Packing P of n unit squares in [0, s]², s > 1 + √2.  Corner c, frame (u, v) = distances from its two walls, box
B_c = (0, 1)²; a square MEETS c iff its interior meets B_c (`geom217.meets_box`, exact SAT).  c is SETTLED iff the
slot square [0,1]² (frame) is in P, and then it is c's only meeter (Cor. B1, `sideband.md` §4): doubly met ⇒ open.
A square in the quadrant meeting B_c has centre in [1/2, 1 + 1/√2)² (F1, F2 of `sideband.md`); two meeters are
interior-disjoint and have centres in distinct cells of the 2 × 2 grid at 1 (Lemma A2); meeters of distinct
corners are distinct squares when s − 2 > √2 (K0-2's disjointness).  A meeter of a doubly-met corner touches at
most one of c's walls (Cor. B1) and neither far wall (its extent is < 1 + √2 < s).  Notation: w(φ) = |cos φ| +
|sin φ| (even, 90°-periodic, in [1, √2]); a unit square of tilt θ has half-width w(φ − θ)/2 in the unit direction
at angle φ, so its support there is m·z + w(φ − θ)/2, and its axis half-widths are w(θ)/2.  Lemma B0 (`sideband.md`
§3): w(φ) − (cos ζ − sin ζ) w(ζ + φ) ≥ 2 sin² ζ for ζ ∈ [0°, 90°] and all φ; Lemma B0′: (cos γ + sin γ) w(ψ) +
w(ψ − γ) ≥ 2 (cos γ + sin γ).  Replacing ζ by 90° − ζ in B0 gives its mirror  w(φ) + (cos ζ − sin ζ) w(φ − ζ) ≥
2 cos² ζ  (B0*).

FJ stress (`drain_lemma.md` D3′, `drain_flow_k0.md` §1, A217 `stress217.py`): at a Fritz-John point of NLP(S) the
multipliers λ ≥ 0 of the active rows form a frictionless force network — a wall row is a force λ·(inward normal) at
the touching vertex; a pair row is a force λ n on the non-owner at its touching corner and −λ n on the owner, n the
owner's outward edge normal, i.e. the unit normal of a line {n·x = β} weakly separating the owner (n·x ≤ β) from the
other (n·x ≥ β); every square is in force and torque balance (λ₀ = 0 self-stresses included: only the per-square
balances are used).  The FORCE OF R ON Q is the sum over the loaded rows of the pair.  In c's frame a square H HOLDS
a meeter Q of c iff the force of H on Q has a strictly negative u- or v-component; ALONG ITS WALL iff Q touches the
floor and F_u < 0, or the u-wall and F_v < 0.  A RATTLER MEETER carries no loaded row at all.

## 2. [T] Lemma PUSH

**Lemma PUSH.**  Let A, B be unit squares in the closed quadrant, both meeting (0, 1)², and let {n·x = β}, |n| = 1,
weakly separate them: A ⊆ {n·x ≤ β}, B ⊆ {n·x ≥ β}.  Then
  (i) n_u > 0 or n_v > 0;
  (ii) if B touches the floor v = 0 then n_u > 0; if B touches the wall u = 0 then n_v > 0.
For the cell pair {NW, SE} with both meeters wall-touching (A up the u-wall, B along the floor) this gives n_u > 0
and n_v < 0: A pushes B down the floor away from the corner, B pushes A up the wall away from the corner.

*Proof of (i).*  Suppose n_u ≤ 0 and n_v ≤ 0; put m = −n = (cos φ, sin φ), φ ∈ [0°, 90°].  B ⊆ {m·x ≤ −β} gives
m·c_B + w(φ − θ_B)/2 ≤ −β.  A meets the open box at p with 0 < p_u, p_v < 1 and A ⊆ {m·x ≥ −β}, so −β ≤ m·p <
cos φ + sin φ = w(φ) (m ≥ 0, m ≠ 0).  B in the quadrant has c_B ≥ (w(θ_B)/2, w(θ_B)/2) componentwise (its support
in −e_u is −u_B + w(θ_B)/2 ≤ 0), hence m·c_B + w(φ − θ_B)/2 ≥ [w(φ) w(θ_B) + w(θ_B − φ)]/2 ≥ w(φ) by B0′ (γ = φ,
ψ = θ_B).  So w(φ) ≤ −β < w(φ).  ∎

*Proof of (ii).*  Let B touch the floor at b = (b_u, 0) and suppose n_u ≤ 0; by (i) n_v > 0.  Then β ≤ n·b =
n_u b_u ≤ 0.  If n_u = 0, A ⊆ {v ≤ β/n_v} ⊆ {v ≤ 0} cannot meet the open box; so n_u < 0 and n = (−sin α, cos α)
with α ∈ (0°, 90°).  Put u₀ := −β/sin α (≥ 0), so that the separating line is ℓ: v = tan α · (u − u₀), A lies in the
wedge {0 ≤ v ≤ tan α (u − u₀)} and B above ℓ.
  *B gives u₀ ≥ sin α.*  B's support in the direction −n = (sin α, −cos α) (angle α − 90°) is u_B sin α − v_B cos α
  + w(θ_B − α)/2 ≤ −β = u₀ sin α.  Touching the floor means v_B = w(θ_B)/2, and the quadrant gives u_B ≥ w(θ_B)/2;
  so u₀ sin α ≥ [w(θ_B − α) − (cos α − sin α) w(θ_B)]/2 ≥ sin² α by B0 (ζ = α, φ = θ_B − α).
  *A gives min_A u ≥ u₀ + cos² α / sin α.*  A's support in the direction n (angle 90° + α) is −u_A sin α +
  v_A cos α + w(θ_A − α)/2 ≤ β = −u₀ sin α, and v_A ≥ w(θ_A)/2 (A above the floor), so u_A sin α ≥ u₀ sin α +
  [cos α · w(θ_A) + w(θ_A − α)]/2.  A's leftmost point is at u_A − w(θ_A)/2, hence
      (min_A u) sin α ≥ u₀ sin α + [(cos α − sin α) w(θ_A) + w(θ_A − α)]/2 ≥ u₀ sin α + cos² α
  by B0* (ζ = α, φ = θ_A + α, using w even: w(θ_A − α) = w(α − θ_A) and the substitution θ_A ↦ −θ_A).
  Together min_A u ≥ sin α + cos² α / sin α = 1/sin α ≥ 1: A has no point with u < 1 and cannot meet the open box.
  The wall clause is the mirror (u ↔ v).  ∎

*Remarks.*  (1) The proof of (i) is Theorem B's clause (P) at c = 1 (`sideband.md` §3): a push toward the corner
would make A a "pressed-type" partner, which the unit box excludes.  At the WIDENED box (0, 1 + w)² (i) can fail
exactly in the (P) configuration — B the pressed square, A beyond the diagonal — where B is held by its two walls
and needs no holder; on s0 pages the lemma is to be used with that exception.  (2) Both clauses are sharp in their
constants (u₀ = sin α with B's edge along ℓ; min_A u = 1/sin α with A's edge along ℓ).  (3) Nothing uses FJ: PUSH is
a statement about two interior-disjoint meeters and their SAT axis.

## 3. [T] Lemma HOLD (G1)

**Lemma HOLD.**  Let P be at a Fritz-John point (any λ₀), s > 1 + √2, c a doubly-met open corner with meeters A, B,
and suppose the force of A on B is nonzero (a pair row between them is loaded).  Then some square C ∉ {A, B} holds
B.  If B touches c's floor, C can be chosen with F_u(C → B) < 0 (it holds B ALONG THE FLOOR); mirror for the u-wall.

*Proof.*  The force of A on B is λ n, λ > 0, n as in Lemma PUSH.  If B touches the floor, n_u > 0 by PUSH (ii);
otherwise n_u > 0 or n_v > 0 by (i), say n_u > 0.  The u-balance of B reads λ n_u + Σ_{C ∉ {A,B}} F_u(C → B) +
F_u(walls → B) = 0.  c's u-wall pushes +u, c's floor pushes 0 in u, the far walls are out of reach (§1); so
F_u(walls → B) ≥ 0 and Σ_C F_u(C → B) ≤ −λ n_u < 0: some square C ∉ {A, B} has F_u(C → B) < 0.  ∎

*Remarks.*  (1) Silent when the pair row A–B is unloaded.  (2) In the {NW, SE} configuration with both meeters
wall-touching, PUSH gives n = (+, −) and HOLD gives a floor holder of B and a wall holder of A: the corner is a JOINT
passing the u-wall's push into the floor row and the floor's push into the wall column.  (3) Nothing says the holder
is not a meeter of another corner, nor that two corners' holders differ — §5.  (4) At the CROWD witnesses the
external crowd row IS the missing holder: its force equals minus the partner push's along-wall component in every
pulled corner (`count218.jsonl`, e.g. `crowd_10_0007|crowd0.05` BL: partner (+0.526, −0.122), pull (−0.526, 0)).

## 4. Lemma K0-COUNT (the count, exactly)

**Lemma K0-COUNT (any n).**  Let P be a packing of n unit squares in [0, s]², s > 2 + √2, at a Fritz-John point,
with every corner box doubly met and open.  Assume
  (LOAD)     at every corner the pair row between the two meeters is loaded, and
  (DISTINCT) the four holders supplied by Lemma HOLD (one per corner, of a meeter pressed by its partner) can be
             chosen pairwise distinct and distinct from the eight meeters.
Then n ≥ 12.  *Proof.*  Eight distinct meeters (corner boxes ≥ s − 2 > √2 apart) plus four further distinct
squares.  ∎  **Corollary (n = 11).**  Under LOAD and DISTINCT no 11-square FJ point has four doubly-met open
corners; with Lemma K0-2 (`fj_census_k0.md` §3: the k-maximal σ-minimiser has every corner box met by ≥ 2 squares)
the k-maximal minimiser would have a settled corner — the k0_00 obligation in MinForm (`drain_flow_k0.md`).
**LOAD and DISTINCT are false in general (§5); the corollary is not available.**

Why the hypotheses are exactly these.  LOAD is what makes HOLD bite: without it a meeter may be a rattler or be
held by squares that are not its partner.  DISTINCT is the brief's G2.  The holder of BL's floor meeter pushes it in
−x and sits on its far side, centre x ≤ 1 + 1/√2 + √2 = 3.12; BR's floor meeter has centre x > s − 1 − 1/√2 ≥ 2.11
at s ≥ 3.82; they can touch at every side ≤ 2(1 + 1/√2) + √2 = 4.83 — so BL's holder CAN be BR's floor meeter, each
holding the other toward its own corner (§5, the ring).  The true sharing bound is FOUR: a 45° square at the centre
touching four 45° corner meeters along its edges (centres offset (±1/√2, ±1/√2)) holds a meeter of every corner and
fits at every s ≥ 3.82.

## 5. [M/F] The hypotheses on A217's witnesses (`count218.md`, snapshot 2026-09-14 17:45; the crowd search grows)

For every doubly-met open corner of every distinct FJ-feasible local optimum in A217's search files (SETTLED /
K0FREE / BOXK0 = genuine FJ points of the free problem; HELD = tilt bound active; CROWD = crowd rows active) the FJ
stress (`stress217.analyse`, HiGHS LP on the active rows; forces below 10⁻⁶ discarded as LP noise) was read in the
corner frame.  6,565 corners in 2,732 witnesses.

| class | corners | A–B loaded | meeters | rattler meeters | corners with both meeters rattlers | partner pushes: PUSH (i) / (ii) | pressed meeters with a holder | holder relations that are meeters of another corner |
|---|---|---|---|---|---|---|---|---|
| SETTLED | 57 | 20 | 114 | 70 | 33 | 40 / 40 | 40 of 40 | 3 of 58 |
| K0FREE | 70 | 5 | 140 | 126 | **61** | 10 / 10 | 10 of 10 | 2 of 16 |
| BOXK0 | 6 | 3 | 12 | 6 | 3 | 6 / 6 | 6 of 6 | 4 of 10 |
| HELD | 2,444 | 2,208 | 4,888 | 397 | — | 4,416 / 4,416 | 4,415 of 4,416 (one at 4·10⁻⁶, threshold) | 908 of 5,239 |
| CROWD | 3,988 | 3,083 | 7,976 | 1,690 | — | 6,166 / 6,166 | 5,241 of 6,166 + 3,181 pulled instead | 1,986 of 6,351 |

Per witness, N := |meeters of doubly-met open corners| + |holders that are no meeter of any corner| (+ the number
of corners carrying an external pull, for HELD / CROWD):

* **HELD four-crowds (7 witnesses): N = 9 … 11, no pulls.**  `rand_0_0569|t20` (side 4.1099, page
  `count218_held_rand_0_0569_t20.svg`): meeters 4, 5 (BL), 6, 7 (BR), 8, 10 (TR), 2, 3 (TL), tilts 70° / 20°;
  every meeter pressed by its partner with n = (+, −) in its frame; the floor meeters 4 and 6 hold EACH OTHER along
  the floor, the wall meeters 5 and 2 hold each other up the left wall, 7 and 8 up the right wall, and ONE
  non-meeter, square 9, holds both ceiling meeters 10 and 3 — a closed compression ring through the eight meeters
  with one link, in force balance with nine squares; the only external row is the tilt bound.  **A force-balanced
  four-crowd needs 9 squares, not 12.**
* **CROWD four-crowds (997): N = 8 … 11, N + pulled corners = 10 … 15.**  `crowd_10_0297|crowd0.02` (side
  4.179, page `count218_crowd_crowd_10_0297_crowd0.02.svg`): seven of the eight meeters carry NO load; the eighth is
  a wall-hugger pulled by one crowd row.  The count has nothing to grip on a rattler crowd.
* **Genuine k0 FJ points: 61 of 70 doubly-met corners have both meeters unloaded** (sides 4.00–4.47); the K0FREE
  witness with three 2-crowds (4.2855, page `count218_k0free_rand_0_0239_free.svg`) has three rattler crowds.  At
  the SETTLED optima 33 of 57 (Trump's own TL corner is loaded: squares 6 and 4, A217 C5).

So: Lemma PUSH and Lemma HOLD hold on every loaded push; LOAD fails on most crowds that exist at FJ points;
DISTINCT fails by the ring.  **The count is not the mechanism of C4.**  What the witnesses show the mechanism to be
is the DRAIN: a forced four-crowd is never stationary — a meeter wants out along its wall (CROWD: the pull is along
the touched wall in 3,071 of 3,261 pulled meeters, and it is exactly the holder HOLD asks for) or a corner square
wants to turn flat (HELD: the bound torque is the aligning one, sign χ, 494 of 494, A217 C3) — and the k0 local
optima below 3.9 all drain to settled-corner optima (A217 §1, A87 §5.4).  That is Theorem DF-K0's H1 in its
original form; the k0_00 obligation is unchanged (`drain_flow_k0.md` §7, `residue_ledger.md` §4).

## 6. What is usable

* Lemma PUSH is a PAIR statement on two meeter poses: for cover boxes of a corner's reach set whose poses touch
  their walls (NW-cell box against the u-wall, SE-cell box on the floor) every admissible separating axis has
  n = (+, −) — a sound prune of the K0-PAIR list (`k0_route.md` §4.4): pairs whose only separating axes have n_u ≤ 0
  or n_v ≥ 0 are dead.  Its value on the cascade is not measured (the exact pair test already decides these pairs;
  PUSH is a reason, not a new kill).
* Lemma HOLD is a structural filter for a k0 FJ census (`fj_census_k0.md` §3, beside K0-1…K0-4): a loaded corner
  pair needs a holder edge on the far side of each pressed meeter.  A88 measured such existential filters as inert.
* The ring `rand_0_0569|t20` is the object a torque argument would have to exclude: eight wall-touching tilted
  meeters in a compression ring, each corner a {NW, SE} joint, the missing quantity a torque of sign χ on a corner
  square.  Whether a ring can ever be torque-balanced at n = 11 is the sharpest open form of the PI's conjecture — a
  finite structure question (8 meeters, ≤ 3 links, the joint types) that Lemma H-LOC's certificate (`fj_census_k0.md`
  §4, 0.78 s per structure) could decide; a NO would exclude loaded rings only, not rattler crowds, so it does not
  close k0_00 either.

## 7. Lean, obligations

`Statements/Open/K0Count.lean`: `lemma_PUSH` (axiom; hypotheses `InQuadrant`, `Meets q 1`, `Separates n β q₁ q₂`;
conclusion (i) ∧ (ii)); builds, `#print axioms` lists only itself, audited in `lean/AUDIT.md` (A216's audit, exit
0, no sorry).  Obligations: O-PUSH — Lemma B0, B0′ and B0* as `wrel`-type inequalities plus the sharp (F2)
`cx ≥ (cos θ + sin θ)/2` (the same items `SecondMeeterCriterion` needs, `sideband.md` §5 (ii)); Lemma HOLD is prose
over the FJ multipliers (no Lean object for NLP(S) in the readable layer).  Nothing in `Main.lean` depends on this
file.  Ledger: `residue_ledger.md` §4 (A218 note); the k0_00 row of the one-table version is unchanged.
