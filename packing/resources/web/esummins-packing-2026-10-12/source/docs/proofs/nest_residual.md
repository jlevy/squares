# THE NEST RESIDUAL of NO-FLOAT2 — what (NEST) forces on the four squares: D's two parallel edges cannot both separate (NOT-BOTH), the vertical budget (Σ) excludes every shallow nest (tan α ≤ 0.95 at η → 0), the horizontal budget (WEDGE) and the FLAT-C poke bound the steep end; the candidate landing cells are Y's left normal cell N_Y and X's lower normal cell N_X; no NEST quadruple is in hand ([M] search running) and NEST-emptiness is [C]; two doc slips fixed — A279, 2026-09-24

The brief (A279 BRIEF): in the NEST residual of `no_float2.md` (Y under a high D, C at the wall) find the cell of ANY pose
that lands D or C (i), chase the count (ii), or draw the surviving configuration (iii); fix the two glosses.  Derivation in
pieces `attempts/A279-nest-residual/notes/nest279_part0..3.md`; code `attempts/A279-nest-residual/code/` (`nest279` the
two-stage search: NEST feasibility, then any-pose cells; `page279`); results beside it; page
`docs/residue_map/campaigns/A279-nest-residual/nest_residual.svg`; Lean `Statements/Open/NestResidual.lean`.  Notation as
`no_float2.md`: BL frame, B = (0,1)², floaters C (upper-left), D (lower-right), blockers X (of T_u(C)), Y (of T_v(D)); arcs
α (D→C separators), η (Y→D), ξ (X→C); (NEST) η₊ < α₋ ≤ α₊ < ξ₋.  Tags [T] [T-computed] [M] [C] [F].

## 0. Verdict

> **[T] NOT-BOTH** (part 2.2).  D's lower-right and upper-left edge lines are parallel (slope angle θ_D); Y beyond the first
> gives η₊ ≥ θ_D, C beyond the second gives α₋ ≤ θ_D — under (NEST) at most one holds.  So in a NEST quadruple either C sticks
> out to the LEFT of D's left vertex below the extension of D's upper-left edge, or Y pokes up past the extension of D's
> lower-right edge right of D's right vertex.  **[T] D HIGH** (2.3): Y's top vertex under D's lower-right edge forces
> h_v(D) ≥ 1 − sin θ_D and h_u(D) < 1 − sin θ_D + sin θ_D tan θ_D; the flat floor cells fail iff x_L(Y) < 1 + sup I(C).
> **[T] (Σ)** (part 3.1; Lean `sigma_core`).  Inscribed-disc centres on opposite sides of a separator are ≥ 1 apart across it;
> C reaches below height 1 and Y touches the floor, so
>   (m_Y,x − m_C,x) tan η + (m_D,x − m_C,x)(tan α − tan η) > sec α + sec η − 1/2 − 1/√2 ≥ 0.793,
> and with the offsets bounded (2.62, 1.21) every SHALLOW nest is impossible: at η → 0, tan α > 0.95 (α > 43.5°); the excluded
> region of the (tan η, tan α) half-plane is the hatch of page panel (b).  **[T] (Σ′)** with vertices: h_v(D) ≥ w_Y − (t_Y,x −
> x_b) tan η ≥ 1 − (cos a + cos θ_D) tan η and h_v(D) < 1 − w_D + (h_u(D) + cos θ_D) tan α (Lean `sigma_prime_low`).
> **[T] (WEDGE)** (3.3): C lies between the wall and ℓ′; its inscribed disc gives h_u(D) ≥ 1/2 + 1/(2 sin α) + (h_v(D) + cos θ_D −
> 1 − w_C/2) cot α, so h_v(D) + cos θ_D < 1 + w_C/2 and steep α needs a nearly flat C.  **[T] FLAT-C** (Lean `flat_c_core`): a
> flat C at height y₀ < 1 forces D's left vertex under C's bottom edge: h_v(D) < 1 − cos θ_D, h_u(D) ≥ 0.70, and then (Σ′)
> gives tan η > cos θ_D/(cos a + cos θ_D) (η > 18° for θ_D ≤ 60°).  These do not yet meet in a contradiction: [C].
> **Candidate cells** (part 2.6).  (a) flat floor cells — fail in NEST; (b) SWEEP — empty by (NEST); (c) **N_Y := Y − sec a·e_x**
> (Y's left normal cell, `normal_ring.md` (E1); inside the container iff x_L(Y) ≥ sec a; P1 lands D iff C, X miss it; for a
> flat-ish Y it is the flat cell in disguise); (d) **N_X := X − sec φ_X·e_y** (inside iff X_low ≥ sec φ_X; lands C iff D, Y miss
> it — on A277's witness it meets D by 0.044, so it is NOT a cell there [T-computed]); (e) tilted cells hugging C's lower-right
> or D's upper-left edge.  A non-wall-touching cell raises no Φ₁; P4 RETREAT needs it to meet fewer border cells than D, and D
> meets B — a cell missing all border cells would do, none was found; no new potential is proposed (none proved).
> **The count chase (ii)** (2.5): FAMILY-STUCK at BL with M(B) = {C, D} forces a THIRD meeter of c01 = [0,1]×[1,2] and of
> c10 = [1,2]×[0,1] (P1⁺, Π = {B, c01}, {B, c10}); in the 4-square model X_low ∈ [1, 2) and x_L(Y) ∈ [1, 2).  "Y meets B" is
> not forced by the inequalities above (x_L(Y) = 1 is consistent with (Σ), (WEDGE)); the chase closes only with the exact
> geometry, i.e. the [M] search or a certificate.
> **[M] the search** `nest279` (stage 1: sup of min(local terms, NEST margin) over the 4-square model with X, Y touchers; stage 2
> adds −J_any).  Two runs were lost to an optimiser plateau (rows kept as `nest279_stuck_run0/1.jsonl`, both [F] as evidence);
> the continuous-margin run is RUNNING AT EXIT and commits its rows itself (`results/nest279.jsonl`; `logs/STOP` stops it).  No
> NEST quadruple is in hand; A277's `float277` (sup ≤ 0, boundary optimum) never explored the NEST end.
> **The residual's dimension and cheapest certificate.**  Unchanged from A278: 10 parameters (12 with free blockers), s = ŝ
> worst.  Cheapest: A278's tree restricted by (NEST) as a PRUNE, plus (Σ)/(WEDGE)/FLAT-C as analytic prunes (each monotone in
> the box — interval versions of linear inequalities in the vertex coordinates), then cell (flat / N_Y / N_X / D-pose sweep)
> and shadow by cores; a 2-D slice bench (h_v(D) × α_Y) first (< 1 CPU-h).  Not launched.
> **NO-JAM(11) still lacks**: unchanged — pair3 (TL, BR); 5b's capped cells; 5d = BL-CAP-2(C, D) [C] (= L, whose NEST part
> is this note) and BL-CAP-2(A, C) [C]; Lean `jam_count`, `float2_local` axioms.  k0_00 unchanged.

## 1. What the brief had wrong (or loose)

1. "Every point of the 10-parameter residual satisfies (NEST)" holds for the P1-SENSE residual (no cell met by D or C alone
among the four — A278 part 6's hypothesis "the sweep meets no fifth square"); L's residual (shadow cells) is larger: a
sweep cell exists when (NEST) fails but its part outside D need not be in the shadow.  NEST-emptiness would prove the
4-square P1-sense statement, not L; L then needs the sweep cell's shadow (a fifth-square question).  2. "Use CELLS's full
generality — a cell need not touch a wall — then Φ₄ RETREAT may rise": only if the cell meets FEWER border cells than D, and
D meets B; a new potential needs its exchange step proved — none is proposed here.  3. The flat-X gloss, as the brief says, is
fixed (`k0_knowledge.md` s.1, `no_jam.md` s.1: X misses (0,1)² iff y_X − cos φ_X ≥ 1).  4. Right in the brief: Y under a high
D forces C to the wall side (WEDGE); the normal cells of Y and X are the cells to test; the count needs the third meeters.

## 2. Lean, reproduce

`Statements/Open/NestResidual.lean`: theorems `nest_not_both_edges`, `sigma_core`, `flat_c_core`, `sigma_prime_low` [T]
(arithmetic cores); opaque `NestSubResidual`; no new axiom; one import line in `Statements.lean`; `lean/AUDIT.md` 0 sorry.
`python page279.py` (< 10 s, asserts every drawn claim); `python nest279.py --stage nest --restarts 24 --seeds 1,2,3,4`
(≈ 7 min per seed, one python, BelowNormal, resumable, `logs/STOP`).  General n: parts 2–3 are s-free and n-free; the
numbers 2.62, 1.21, 0.95, 0.70 use only unit squares and the box.
