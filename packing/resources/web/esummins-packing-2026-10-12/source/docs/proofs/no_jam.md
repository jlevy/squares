# NO-JAM — a corner whose box meeter FLOATS dies by ROOM, not by count: the JAM ring exists, its pocket holds one square (drawn), two opposite JAMs leave none; what is [T], what is certified, what is open — A262, 2026-09-22

The brief (A262 BRIEF): after A261, BOX-MEETERS(11) rests on NO-JAM(11) — *no normal-form family-stuck packing of 11
on [3.82, ŝ] has a doubly-met corner box with a FLOATING meeter*.  The coordinator's reading: a JAM corner spends
three squares (A, C, X) where the ring spends two, so with j JAM corners the outer structure has ≥ 8 + j squares and
the pocket is smaller; kill by COUNT + ROOM.  This note enumerates the corner types, proves the count exactly, shows
where the reading is wrong (the count kills nothing), reduces NO-JAM(11) to ONE room statement, measures it on the
whole window, certifies the cheap half, prices the other, and searches honestly.  Tags: [T] proved, [T-computed]
box-valid certificate with its own verifier, [M] measured, [C] conjecture, [F] false (witness).  Sources:
`box_meeters.md` (A261), `normal_room.md` (A259), `locked_wall.md` (A260), `normal_ring.md` (A258).  Code
`attempts/A262-no-jam/code/` (`geom262`, `multi262`, `fam262`, `ring262`, `adv262`, `search262`, `span262`,
`float262`, `held262`, `sector262`, `cert262` + `tree262` + `verify262`, `price262`, `pages262`, `run262.sh`,
`chain3.sh`); results, certs, logs beside it; pages `docs/residue_map/campaigns/A262-no-jam/`; Lean
`Statements/Open/NoJam.lean`.  Notation as in A259: O = (s/2, s/2), corner frame BL, w(θ) = cos θ + sin θ.

## 0. Verdict

> **[T] COUNT (any m; Lean `jam_count_core`).**  Every square meets the unit band or contains O, and at most one
> contains O (HOLE-ONE).  Per wall w: τ_w touchers, of which 2 − e_w serve its end boxes (e_w = boxes of wall w with
> no wall-w toucher) and u_w are MIDDLE; every box has ≥ 2 meeters, at most one toucher per wall (SAME-WALL), the
> rest floaters; a floater meets ≤ 1 box.  So n = 8 − E + U + F_box + F_rest with F_box ≥ E.  **The count kills
> nothing**: n = 11 is consistent with it (E = 1, F_box = 3, U = 0, F_rest = 1).  What kills is ROOM:
> **[T] if every unit square of [0, s]² interior-disjoint from the MINIMAL box-serving structure S_min (two meeters
> per box, 8 squares) contains O in its interior, then n ≤ 9** — every other square (middle touchers, extra box
> meeters, slot squares, the centre square) lies in that pocket, and two squares containing O overlap.
> So **NO-JAM(11) ⟸ ROOM(S_min) ≤ 1 for every 8-structure with a non-PAIR corner** (§2); the third-meeter corner
> needs nothing new (monotonicity: S_min is the PAIR ring, A259 / A260 apply).
>
> **[F] the reading "8 + j" and "j ≥ 2 needs room 0".**  In every JAM ring found the wall square X IS the next box's
> meeter (wall 3 = X alone + the floater C), so the outer structure has 8 squares for j = 1 and 8 for j = 2 too; and
> room ≤ 1 already gives n ≤ 9 < 11 for every j.  [M] j = 2 OPPOSITE corners: a ring exists (t = +0.0016 at ŝ) and
> its pocket holds NO free square at all (room 0, `jam_two.svg` (a)); j = 2 ADJACENT: no ring found (best −0.0078).
>
> **[M] JAM RINGS EXIST on the whole window** (`ring262`, `adv262`: 8 squares, exact check, margin 0.0104 at ŝ,
> 0.0099 at 3.82; 34 rings from structured starts; `jam_ring.svg`): a floor row, right row, ceiling row, X on the
> left wall serving TL, C floating 0.57–0.72 off the wall meeting the BL box by a sliver 0.003–0.010 deep.  **ROOM:
> every free square of every JAM ring contains O** — pierce margin ≤ −0.070 at ŝ, ≤ −0.105 at 3.82 (exact centre
> sets, 1° grid), adversary over the 11-coordinate family pushed to its boundary: ≤ −0.085 (ŝ) / −0.133 (3.82);
> capacity exactly 1 (`capacity259`); ring + its one free square is never family-stuck (`fam262`, 12 cells).
> **[M] HELD-JAM (P4) does NOT exclude the JAM ring**: the bare ring never blocks C's retreat (35/35 rings admit
> 27–85 of 89 directions), but a single free square G blocks every retreat direction in 31/35 (G contains O).
>
> **[T-computed, launched] the cheap half**: the TL sectors need only a 3-square corner PAIR (ceiling row + X; no
> second wall square: `pair3`, 4 parameters, ≈ 3 CPU-h, verifier `verify262`).  **[M] + pilot** the BL sectors: a
> 7-parameter box-valid kernel (`cert262 jam`: cores of A, A₂, X, C; PRUNE by the DIRECT-JAM conditions) certifies
> every sampled JAM point at radius 1/64–1/16, worst point margin −0.235, but the full tree is priced 15 (median) to
> 500 (mean) CPU-h (`price262`, heavy tail): a pilot on the witness tilt cell runs with an 8 h budget.
>
> **Plainly.**  NO-JAM(11) is **[C]**, reduced to ROOM(JAM ring) ≤ 1: [T] reduction, [M] on the whole window with
> margin 0.07, [T-computed] on the TL sectors (when `pair3` ends), BL sectors [M] + priced; with `meeters_split`
> ⟹ BOX-MEETERS(11) (Lean `box_meeters_262` from the axiom `jam_count`).  FAMILY-STUCK-EXIST(11), k0_00: unchanged.

## 1. Corner types  (task 1)

Doubly-met box, meeters ≤ 4 (A2 cells), ≤ 1 toucher per wall (SAME-WALL [T]), touchers of both walls distinct
(TWO-CORNERS).  By (touchers on wall u, on wall v, floaters):

| type | (t_u, t_v, f) | squares at the corner | shared with the adjacent corners | wall counts | room statement |
|---|---|---|---|---|---|
| PAIR | (1,1,0) | A (floor START), B (wall END) | A's row END serves the next box, B's row START the previous | τ = 2, e = 0 both walls | A259 PAIR / A260 hybrid |
| THIRD | (1,1,≥1) | PAIR + floater(s) C | as PAIR; C is a pocket square | as PAIR | **none new [T]**: S_min = the PAIR ring, C ∈ its pocket, so C contains O and n ≤ 9 |
| JAM | (1,0,1) | A (floor, meets), C (floats, meets), X (wall, above C, misses the box) | X serves the wall's other box (every ring found) or is a MIDDLE toucher under a START square S ([M] `span262`, pending) | floor τ = 2, e = 0; wall τ = 1 (+u), e = 1 | §2, this note |
| mirror JAM | (0,1,1) | reflection across the diagonal | | | reflection |
| FLOAT2 | (0,0,≥2) | C, D float, both meet; blockers A′ (floor) and X′ (wall) meet neither | both walls e = 1 | | none; [M] `float262` (pending) |

[T] X misses the open box (0,1)² ⟺ X's LOWEST point is at height ≥ 1: with X's leftmost vertex (0, y_X) and edges (cos φ_X, sin φ_X), (sin φ_X, −cos φ_X) the lowest point is y_X − cos φ_X, so the condition is y_X − cos φ_X ≥ 1 (the leftmost vertex is then at height ≥ 1 + cos φ_X).  [The earlier gloss "y_X ≥ 1 − cos φ_X" was a slip: A278 erratum, fixed A279.]
[T] C serves no wall slot as a toucher; it may MEET a slot (in the drawn ring C meets BL01 with A and X) — that
counts for family-stuck but not for the wall's row.  [T] a floater meets one box only (boxes are s − 2 > 1.8 apart).
**Global structures by (j, shared)**: j = 1: the JAM RING (walls 0–2 rows of two or open pairs, wall 3 = X + C):
8 outer squares.  j = 2 opposite (BL, TR): walls 1, 3 = START + floater: 8 outer.  j = 2 adjacent (BL, BR): wall 0
= A alone serving BL, its BR box served by a floater; wall 3 = X + C: 7 touchers + 2 floaters = 9?  No — [M] no
such ring closes (§4).  X as a middle toucher adds one (9 outer) only if a START square S fits above it under the
ceiling: [M] pending; the room statement is unaffected (S only shrinks the pocket; the TL sector then uses S).

## 2. The count and the reduction  [T]

**2.1 Band.**  Below side 4 a unit square missing the band lies in [1, s−1]², side < 2 ≤ w + 1/w, so it contains O
in its interior (HOLE-ONE tilt form, A259 §2.1); two such overlap: ≤ 1 centre square, ≥ 10 band squares.
**2.2 Count.**  n = Σ_w τ_w + F_box + F_slot + F_centre, τ_w = (2 − e_w) + u_w (a toucher serves ≤ 1 box: its wall
extent w ≤ √2 < s − 2), F_box ≥ Σ e_w (each box short of touchers has ≥ 2 − t_k floaters) — Lean `jam_count_core`.
**2.3 ROOM ⟹ n ≤ 9.**  Let S_min pick two meeters per box (touchers first).  ROOM(S_min): every unit square in
[0, s]² interior-disjoint from S_min has O in its interior.  Then every square of P ∖ S_min contains O, so |P ∖ S_min|
≤ 1 and n ≤ 9.  Consequences: U = 0 (a toucher is ≥ s/2 > √2 from O), F_box = E (no extra meeters), F_slot = 0.
Monotone: ROOM(S) ⟹ ROOM(S′) for S′ ⊇ S.  So the THIRD type is free, and the JAM type needs ROOM of the JAM RING.
**2.4 MISS ⟹ a corner sector** (A259 §2.2 verbatim): a free Q missing O has (q − O)·n ≥ ½ for a normal n at a wall
and lies in one half of the container: 8 sectors, two per corner; dropping every square not at that corner is sound.
For the JAM ring: BR, TR sectors = A259's PAIR with all four squares present ([T-computed] by A259's tree); TL
sectors = the ceiling row + X only (**pair3**, 4 parameters: A259's PAIR without the wall row's second square);
BL sectors = {A, A₂, X, C} (**jam**, 7 parameters).  s is eliminated exactly as in A259 §2.3 (for n = −v, −u:
n_x + n_y ≤ 0).  [M] `sector262` on 43 JAM rings: worst BL-floor −0.305, BL-left −0.362 (with the four corner
squares only: −0.310 / −0.362), TL-left −0.336, TL-ceil −0.124 (ceiling row + X only: −0.249 / −0.089).
**2.5 HELD-JAM.**  The wedge between A's edge (slope angle α′) and X's edge (ξ > α′) OPENS away from the corner:
for ψ ∈ [α′, ξ] the translates C + μ(cos ψ, sin ψ) stay clear of A and X (Lean `retreat_cone_core`, the mirror of
STRIP-LANDING); after μ ≥ max((1 − h_v)/sin ψ, (1 − h_u)/cos ψ) C meets no border cell at all (Lean
`retreat_leaves_box_core`; its far reach ≤ 1 + √2 < s − 1).  By P4 the sweep is blocked by a FREE square G.
[M] `held262`: the other ring squares never block every direction (35/35), a single G exists in 31/35 (thin:
blocking area 10⁻⁵ … 3·10⁻³), 4/35 rings are excluded by P4 alone.  HELD-JAM is a constraint on the 9th square,
not an exclusion.

## 3. Room of the JAM ring  (task 2)

**3.1 [M] the family.**  `geom262`: walls 0–2 rows of two (δ_w, φ_w), wall 3 = X (δ₃, φ₃) + C (c_x, c_y, θ); HARD
terms only (containment, 27 gaps, tilts, box strictness, C meets the open BL box, C floats) and A261's inner sup J
(no wall cell of any tilt that meets C is free of A and X): t = min(margin, −J) > 0 ⟺ a JAM ring.  From A261's two
witnesses × 16 starts for walls 1, 2: 34 JAM rings (29/32 at ŝ, 5/9 at 3.82), t ≤ 0.0104.  ROOM (`room259`, exact
centre sets, 1°): pierce ≤ −0.0703 at ŝ, ≤ −0.1053 at 3.82; 4 rings at ŝ have NO free square (room 0).  Adversary
(`adv262`: (1+1)-ES on the pierce margin, proposals rejected unless t ≥ 0): the ring is pushed to t → 0 and the
pierce stays ≤ −0.0845 (ŝ), ≤ −0.1335 (3.82) — the room bound is not sharp against the JAM constraint; the flush
value −(4 − s)/2 = −0.0615 is not reached.  Capacity 1 (`capacity259`, exact SAT); the 9-packing is never
family-stuck (the free square meets no cell: min excess 0 on the 8-family).
**3.2 Closed forms (the brief's "C's far vertex vs O").**  C's far vertex is at distance ≤ √2 from its lowest
vertex (h_u, h_v) ∈ (0,1)², so C reaches at most (1 + √2, 1 + √2) — beyond O only by 0.47; a free square Q missing O
towards the floor has q_y ≤ s/2 − ½ + tilt slack ≤ 1.51 and lies right of C's far edge or under it: the BL sectors
are about the strip between A₂'s tooth and C's right flank — no closed form found that beats the certificate; the
region left of C (between C and the wall, above the box) holds no unit square when C is jammed [T-computed per
ring: A261's empty-cell sup ≤ −0.069] but the sector needs the region right of C.  Left as the 7-parameter job.
**3.3 [T-computed, launched] pair3** (`cert262.check_box_pair3`, `tree262 --fam pair3`): cores of the two wall-row
squares and the floor START square over (b, φ, a′, φ′) ∈ [0,1] × [0°,45°]²; PRUNE only off-domain (b, a′ < 1; the
wall row's START a < 1 at s ≥ 3.82) or on core overlap; bins 1°; s_max = 3.8771.  Point margins on the JAM rings'
TL corners −0.041 … −0.061; 11 ms per box; 81 root cells; `verify262`: independent 0.5° bins offset ¼°, exact
dyadic tiling, OPEN listed never counted.  Status at exit: `certs/pair3262_index.jsonl` (chain3).
**3.4 [M] + pilot: jam** (`cert262.check_box`): p = (d₀, α, y_X, φ_X, c_x, c_y, θ); cores of A, A₂, X, C (ρ from
the position radii + (1 + sec·tan) r_φ for the row's second square; C's core from r_pos + the kernel of r_θ);
PRUNE: d₀ ≥ 1; X leaves the container; X meets the open box (y_X < 1 − cos φ_X); C's OUTER approximation misses the
box; X's outer approximation misses C's wall drop T_u; A's and A₂'s miss C's floor drop T_v (the DIRECT-JAM
conditions of A261 §1.2, necessary when the direct blockers are the wall's / floor's touchers); cores overlap.
Every JAM ring's corner certifies as a point (margins −0.54 … −0.74) and at radius 1/16 (`bench262`); 34 random
DIRECT-JAM points certify at radius 1/64 … 1/16, none fails (`price262`); price 7·10⁵ (median) – 2·10⁷ (mean)
leaves × 0.06–0.08 s = **15–500 CPU-h**: over the 50 CPU-h line in expectation, so NOT launched in full; the pilot
`tree262 --fam jam --only 3,4 --sub 6 --budget 28800` (the witness cell α ∈ [15°, 20°], φ_X ∈ [20°, 25°], 64
sub-jobs, resumable) runs after pair3; its index at exit says what fraction of that cell is certified.

## 4. j ≥ 2, and the search  (tasks 2–3)

**[M] `multi262` / `adv262`** (every JAM corner gets A261's witness triple; HARD terms + one inner sup per JAM):
j = 2 OPPOSITE (walls 3, 1 lose their END squares): a ring at ŝ, t = +0.0016; its pocket admits NO unit square at
any of 90 tilts — room 0, n ≤ 8 (`jam_two.svg` (a); Lean `opposite_slab_core`: two floaters within d < ½ of O on
opposite sides leave a slab of width < 1).  j = 2 ADJACENT: best t = −0.0078 (no ring; the two floaters collide with
the floor's single toucher, drawn red in `jam_two.svg` (b)).  j = 3, 4 and further seeds: `adv262` (chain2) — see
the LOG for the rows finished at exit.  **Search** (`search262`): 46 corpus rings (3.82 … 3.99) × 4 rotations × 3
installs (the two witnesses, and the ring's own END square slid along X's edge into a floater) = 552 structured
starts, Nelder–Mead on t, every JAM ring found gets the exact pocket, `capacity259.best_set` (up to 3 disjoint free
squares, exact SAT) and the 12-cell all-families test; an 11-square result would be written to
`results/WITNESS262.json`.  Status at exit: `results/search262.jsonl` (chain2, running).  No witness exists in the
rows finished when this note was written (every finished row: capacity 1, not family-stuck).

## 5. General m, the chain, obligations  (task 4)

**m-free**: the corner types (§1), COUNT (§2.2 with 4(m−2) touchers: Lean `jam_count_core` with k = m − 2),
ROOM ⟹ n ≤ 4(m−2) + 1 (§2.3), HELD-JAM (§2.5), the DIRECT-JAM domain and the `jam` kernel.  **m = 4 only**: the
sector reduction to the container centre (for m ≥ 5 it is PEEL in normal form, A259 §6: the free squares lie in
R_cos, and a JAM corner's C reaches at most 1 + √2 from its corner — [C] that it costs no less than a PAIR corner),
the numbers, the certificates.  **Chain**: packing at s ⟹ [T] normal form ⟹ [C `jam_count` = ROOM(JAM ring)] no
floating box meeter (Lean `no_jam_of_count`: 4(m−2) + 1 < n) ⟹ [T-prose `meeters_split`] BOX-MEETERS (Lean
`box_meeters_262`) ⟹ A258 §3.1 / A261 / A260 ⟹ the hybrid normal ring ⟹ [A259 / A260] FAMILY-STUCK-EXIST(11).
**Remaining obligations, exactly:** (N1) the BL-sector certificate `jam` in full (15–500 CPU-h) or an analytic
sector lemma; (N2) `pair3` complete + `verify262` bad = 0; (N3) INDIRECT jams: C's drop blocked by a non-toucher
K (the chain of blockers of A261 §1.1) — not in the DIRECT-JAM domain, [M] nothing; (N4) JAM rings whose other walls
are OPEN PAIRS (A260's hybrids) and X or the floor row of the other sense; (N5) FLOAT2 corners (`float262`, [M]
pending; no room statement); (N6) j = 2 adjacent / j ≥ 3 (`adv262` pending; opposite j = 2 is [M] room 0); (N7) a
middle toucher above X (`span262`, [M] pending; harmless for ROOM); (N8) Lean: `jam_count` is an axiom, §2.3 is
prose; (N9) the stretch (ŝ, 4) (`search262` covers it [M] only).

## 6. What the brief had wrong

1. "≥ 8 + j outer squares": X is the next box's meeter in every JAM ring; the outer count is 8 for j = 1 and for
j = 2 opposite; "if X is not another box's meeter" is the exception, not the rule.  2. "j ≥ 2 needs room 0": room
≤ 1 suffices for every j (n ≤ 9); room 0 happens anyway for opposite JAMs.  3. "C reaches to the centre": its far
vertex reaches ≈ 1.9–2.0 in the rings found, yet every free square still contains O by ≥ 0.07.  4. The third-meeter
corner is not a new room case (monotonicity).  5. Not in the brief: HELD-JAM (P4) does not exclude the JAM ring —
31/35 rings have a holder; and the count is consistent with n = 11 — ROOM is the whole argument.

## 7. Lean, reproduce

`Statements/Open/NoJam.lean`: theorems `retreat_cone_core`, `retreat_leaves_box_core`, `jam_count_core`,
`jam_count_eleven`, `opposite_slab_core`, `no_jam_of_count`, `box_meeters_262`; axiom [C] `jam_count`; build +
audit 0 sorry.  Reproduce: `bash attempts/A262-no-jam/code/run262.sh ring|adv|span|float2|search|held|sector|pages`
(resumable, `logs/STOP`), `pair3`, `jam [budget-seconds]`, `verify`; `chain3.sh` waits for chain2 and runs
float2 → pair3 → verify → jam → verify → held → sector, committing results at CHAIN3 END.
