# NO-FLOAT2 — two floaters meeting one corner box are always positive-slope separated (case (N) is empty), both outer drops need blockers X, Y outside {C, D}; a SHADOW CELL (a wall cell whose part outside D no admissible square can reach) lands D in every packing containing the four, and A277's Y-poke witness has one (flat floor cell, margin 0.032); the theorem itself is [C], reduced to a 4-square local statement L; CAP-2(A, C) at the JAM corner does not close by hand (S1–S4), residual priced by cert277's jam kernel — A278, 2026-09-24

The brief (A278 BRIEF): prove NO-FLOAT2 (no corner box of a Φ₁-maximal family-stuck packing at s ∈ [3.82, ŝ] is met by
two floaters) by identifying the cell through which P1 lands D once all four drops are blocked, or draw the residual;
then BL-CAP-2(A, C) by the analytic route or its residual and price.  Derivation in pieces
`attempts/A278-no-float2/notes/nofloat278_part0..6.md`; code `attempts/A278-no-float2/code/` (`cell278` the exact
witness cell + disc-test certificate, `flat278` the flat-cell search, `page278`); results beside it; page
`docs/residue_map/campaigns/A278-no-float2/no_float2.svg`; Lean `Statements/Open/NoFloat2.lean`.  Notation as
`float2_room.md`: BL frame, wall x = 0, floor y = 0, B = (0,1)², floaters C (upper-left), D (lower-right), drops
T_u, T_v, strips S_u, S_v, blockers X (of T_u(C)) and Y (of T_v(D)).  Tags [T] [T-computed] [M] [C] [F].

## 0. Verdict

> **[T] FLOAT-SLOPE** (part 2).  Two interior-disjoint unit squares of the quadrant both meeting the open box are
> separated ONLY by positive-slope lines, and one of them is upper-left of EVERY separator (SQUARE-IN-TRIANGLE with
> β < n_u + n_v from the far square's box point; NOTCH-NARROW for an axis-parallel separator; the separating normals of
> two convex bodies form one arc).  A277's MUTUAL case (N) never occurs: in a FLOAT2 corner D can block only T_v(C), C
> only T_u(D), and **T_u(C), T_v(D) have blockers X, Y outside {C, D}** (DROP-P1), X above-left of C, Y below-right of
> D (BLOCKER-SIDE).  **Cor. 2.2**: with M(B) = {C, D} no wall cell of any pose disjoint from B is met by ⊆ {C, D}
> (P1⁺, Π = {B, T}) — the box is not the landing cell, but it forbids every empty wall cell.
> **[T] SHADOW-CELL** (part 3).  Sh(O) := the points of [0,s]² covered by no unit square interior-disjoint from the
> obstacle set O.  If a wall-touching cell T has int T ∖ int D ⊆ Sh({C, D, X, Y}) and misses C, X, Y, then in EVERY
> packing containing the four squares T is met by D alone and P1 (CELLS, |Π| = 1) lands D.  Sufficient test: dist(T ∖
> int D, K_outer) > 1/√2 with K_outer ⊇ the admissible centres (distance ≥ ½ from every obstacle, inside [½, s−½]²);
> Lean `shadow_cell_core`.  **Theorem 3.1 [T]: NO-FLOAT2 ⟸ L**, L = "every FLOAT2 quadruple (C, D, X, Y) has a shadow
> cell for D or for C" — a statement about four squares (the other seven can only lie outside the shadow).
> **[T-computed] the witness lands.**  A277's Y-poke witness (all four drops blocked, gaps C–D 0.00227, D–Y 0.00055):
> low footprints I(C) = (0.368, 0.424), I(Y) = (1.548, 2.745) leave the flat floor cells F_x, x ∈ (0.424, 0.548), met
> by D alone; T = F_0.486 has dist(T ∖ int D, K_outer) = 0.7390 > 0.7071 (`cell278`): the sliver under D's lower-right
> edge, the D–Y wedge and the wall–D–C pocket are in the shadow.  So no packing containing these four is normal — A277's
> J_D = +0.024 made exact and independent of the remaining squares.  [T-computed] SWEEP lands it too: a Y→D separator
> of slope 77.2° exceeds the D→C one (12.9°), so D slides down-left at any ψ ∈ [12.9°, 77.2°] free of C and Y (part 6).
> **[C] NO-FLOAT2 itself.**  The residual R (part 4) is L's domain minus the shadow-cell points: 10 parameters with
> toucher blockers (C, D: 6; X: 2; Y: 2), 12 with free blockers; s = ŝ is the worst case (ADM grows with s).  Every
> residual point satisfies (NEST) η₊ < α₋ ≤ α₊ < ξ₋ (part 6: Y's separators from D all shallower than every C–D
> separator, X's from C all steeper) — Y UNDER a HIGH D, C pushed to the wall: the opposite end from the witness, where
> the flat cell is doubtful.  [M] `float277` (A277) found sup ≤ 0 on the 4/5-square any-pose model; [M] `flat278`
> (flat cells only, running at exit: `results/flat278.jsonl`) says whether flat cells alone suffice on the model.
> Certificate designed (prune by hypotheses + (NEST), cell by footprints, shadow by cores; every step monotone), NOT
> priced below 10³ CPU-h by naive extrapolation from cert277's 6-parameter 30–1000; not launched.
> **[C] BL-CAP-2(A, C)** (part 5) does not close by hand.  [T] S1: a floor-sector miss lies below a line through O of
> slope ψ ∈ [−45°, 45°), a wall-sector miss left of one; S2: floor-sector centres have q_y ≤ s/2 − ½ sec ψ ≤ 1.4385
> for ψ ≥ 0 (higher only by (s/2 − q_x) tan|ψ| for ψ < 0); S3/S4: two side-by-side misses force the left/lower one
> into [0, 1.4385] × [0, 2.15] (resp. its mirror), a unit square in the corner interior-disjoint from A and C — [C] it
> does not exist.  last_two's stacking needs a gap strip, strip_jam's LEFT / CL speak of strip squares, flat_x's
> extremal square has q_y ≥ 1.5 and is not a floor-sector miss at ψ ≥ 0 [T].  Price: cert277 --fam jam (5 parameters,
> bench 6/6 CERT, 5 of them ROOM, 0.18 s/point), A277's 3–100 CPU-h; X and A₂ may be added as obstacles.  Not launched.
> **NO-JAM(11) still lacks**: pair3 (TL, BR); 5b's capped cells c5_4 / c5_5; 5d = BL-CAP-2(C, D) [C] (deleted iff L
> is certified or proved) and BL-CAP-2(A, C) [C]; Lean `jam_count` axiom.  k0_00 unchanged.

## 1. Statements and proofs — parts 1–3, 6 (one line each; the parts carry the proofs)

FLOAT-SLOPE, Cor. 2.1 (blockers outside {C, D}), Cor. 2.2 (no cell ⊆ {C, D} off the box), Lemma 2.3 SWEEP (landing
directions between the separator angles), Lemma SHADOW-CELL, the disc test, Theorem 3.1, the arcs and (NEST).

## 2. What the brief had wrong

1. "By MUTUAL at most two of the four drops can be blocked at all": at most two can be blocked BY EACH OTHER; all four
are blocked in normal form, two by outside squares.  2. A277's case (N) is empty (FLOAT-SLOPE), so "two distinct
squares Y and X" is right but not for A277's reason; X = Y is not excluded here.  3. The landing cell is not "between
Y and the wall": C's low corner sits at the wall; it is between C's low footprint and Y's.  4. "Prove it is always
available when Y blocks D's straight drop": not proved — it needs h_v(D) small (vertex poke), and (NEST) says the
jammed residual has D high.  5. `k0_knowledge.md` s.1 / `no_jam.md` s.1 gloss "X misses B iff y_X ≥ 1 − cos φ_X" is a
slip: the lowest point of X must be ≥ 1 (X ⊆ {y ≥ 1}, as H1 and float2_room.md say).  6. Right in the brief: the flat
floor cell, ONE-DROP/MUTUAL, the corner box is not the cell, CAP-2 not ROOM.

## 3. Lean, reproduce

`Statements/Open/NoFloat2.lean`: theorems `float_slope_core`, `shadow_cell_core` [T]; opaque `Float2Local`, `NoFloat2`;
axioms `no_float2_of_local` [T-prose], `float2_local` [C]; theorem `no_float2`; one import line; `lean/AUDIT.md` 0 sorry.
`python cell278.py` (20 s), `python page278.py` (10 s), `python flat278.py --restarts 12 --seeds 1,2` (≈ 10–20 min per
seed, one python, BelowNormal, resumable).  General n: everything in parts 2–3 is s-free and n-free; the numbers
(1.4385, 2.15, the sectors) are m = 4.
