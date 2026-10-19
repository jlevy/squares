# COMMON-SENSE — the local lemma behind ONLY-RING: the sense of a wall toucher, the NORMAL CELL (SLIDE-NORMAL as Lemma CELLS on a tilted cell), one-step normalisation, and what is false — A255, 2026-09-20

The PI: *"Assume a corner non-simple.  Its root has two meeters.  Pick up both: if either adjacent unit box becomes
free, put the two down in root + that box — now simple.  By recursion the second-meeter requirement is chased round the
outside.  Because of HOW two meeters can meet the root, for the chain to keep failing to simplify we need common-tilt
squares along the sides, which force the other corners into similar common-tilt corner packings."*  Addendum (evening):
any feasible motion inside the fixed container is a reduction (the side is kept by definition), and Lemma SLIDE-NORMAL:
the second meeter of a wall toucher's cell slides to the adjacent wall toucher of the same tilt unless blocked.
This note states the chase for every n (m = ⌈√n⌉, s ∈ (m−1, m), ε = m − s), proves what is a theorem, tests the rest on
the corpus FIRST, then by local search, and says plainly what is false.  Tags: [T] proved, [T-computed] exact finite
computation, [M] measured, [C] conjecture, [F] false as stated (witness).  Sources: `ring_swap.md` (SWAP / CELLS),
`peel.md` (A254: cells, FAMILY-STUCK(n), RING(n), ONLY-RING), `type_t_chase.md` (T-SLOTS, the ring), `corner_chase.md`
(type F, the CW poker, TWO-POKERS), `family250.md`, `mintilt253.md`.  Code `attempts/A255-common-sense/code/`
(`geo255`, `sense255`, `slide255`, `local255`, `blocked255`, `ringsense255`, `summarise255`, `pages255`, `run255.sh`);
results `attempts/A255-common-sense/results/sense255.md` (+ jsonl); pages
`docs/residue_map/campaigns/A255-common-sense/`; Lean `Statements/Open/CommonSense.lean`.

## 0. Verdict

> **[F] COMMON-SENSE as a LOCAL lemma** (the brief's candidate: "family-stuck ⟹ the wall touchers at a corner have one
> sense, else some family in the neighbourhood has |M(Π)| ≤ |Π|").  The local counter-hypothesis — root c00 met by
> exactly B, A; c01 also by C ∉ {A,B}; c10 also by D ∉ {A,B,C} (every CELLS family of {c00,c01,c10} over-met); two
> designated wall touchers of different sense (+/−, or flat/tilted) — is REALISED in **19 of 20** pair types
> (B–A across the corner, B–C along the wall, B–D, C–D; margins 0.006 … 0.046, every witness re-verified by
> `test255`; `local_witnesses.svg`); the 20th (C flat on the wall, D tilted on the floor) is UNDECIDED (sup −0.0002,
> 60 restarts).  The problem is s-free (§3.1), so this holds for every m ≥ 4.  With the addendum's clause "the slide
> is BLOCKED" (a fifth square meets the normal cell) the feasible set SHRINKS TO THE EDGE: W:+− is realised by 0.0019
> only, K:+− (the mixed corner) was NOT found (−0.0006, 25 restarts); the other six rows run detached (§3.2).
> **Sense is not forced by anything inside one corner's neighbourhood.**
>
> **[T] What is a theorem** (n-general): SENSE-INVARIANT (§1); **NORMAL-CELL** — SLIDE-NORMAL in its true form is
> Lemma CELLS on ONE TILTED CELL T = s₁ ± sec φ · e_wall: if T is met by at most one square other than s₁, that square
> (whoever it is — no path, no order on the second meeters) exchanges onto T at the same side (§2.2); **ONE-STEP
> NORMALISATION** — maximise the longest common-tilt wall row over ALL packings at side s: either some packing at s is
> not family-stuck, or a ROW-NORMAL family-stuck packing exists, in which every end cell of every longest row is out of
> the container or met by ≥ 2 squares; no iteration, so no termination question (§2.3; Lean `exists_max_potential`,
> `value_form_normal`, `exists_rowNormal`: theorems).
>
> **[M] Corpus** (489 + 486 + 15 ring witnesses; `sense255.md`): toucher-sense violations are COMMON (A244 ≥ 4: 381
> of 1 956 doubly-met corners; A217 ≥ 4: 813; A217 < 4: 20) and **every one is reduced by Lemma CELLS at scope ≤ L2**
> (N_c ∪ the two adjacent neighbourhoods); 92 % already inside N_c, mostly by a corner domino.  Below 4 exactly one violating
> corner is locally stuck in N_c (`rand_0_0163|t3`, s = 3.9504, TL: ceiling touchers at −36.5° and +3°): it reduces by
> a single adjacent corner box ({BL00}, met by square 3 only; likewise {TR00}) (drawn).  All 15 ring witnesses have one sense.  SLIDE-NORMAL: on the rings every in-container
> normal cell is met by exactly ONE square, the next toucher, of the same sense (112 of 112) — the ring is one teleport
> per wall from row-normal; on the corpus 1 785 of 2 955 in-container normal cells are BLOCKED, mostly by the next wall
> square + another meeter of the cell ("Wa").
> **[F] the PI's claim (c), literally** ("a square above s₁, at its tilt, poking down past it can never be a second
> meeter of the cell"): `rand_0_0441|free`, s = 3.9352: toucher 9 (−36.8°) on x = 0, square 10 at the same tilt in
> the second layer meets BL01 with depth 0.265 (drawn).  It is a Trump-like grain (tilt 37°) in a k1 packing; at ring
> tilts the claim is open.
>
> **[M] Ring level** (`ringsense255`, detached): the all-ADJ ring with a prescribed sense pattern, 43 orbits × 2 sides.
> COMPLETE: the pinwheel exists at both sides (controls, +0.021 at 3.99, +0.011 at ŝ); **0 of the 84 mixed rows
> (42 orbits × {3.99, ŝ}) has a ring** — best mixed sup-margin −0.0140 (8 restarts each; `sense255.md` §5).  This is
> the first [M] evidence FOR common sense — at ring level, where the brief's local form fails.  Not a certificate
> (16 coordinates: out of reach of the interval engine, A247 §4.3).
>
> **Plainly:** COMMON-SENSE is **not proved, false as a local statement, open in normal form**.  ONLY-RING(11),
> FAMILY-STUCK-EXIST(11), k0_00: unchanged.

## 1. Sense [T]

φ(Q) := ((θ + 45°) mod 90°) − 45° ∈ (−45°, 45°], θ any edge direction of Q; sense(Q) := sign φ (flat: 0; |φ| = 45°:
none).  **SENSE-INVARIANT [T]:** the perimeter frames of the four walls differ by quarter turns and a quarter turn
fixes θ mod 90°, so "tilt measured the same way round the perimeter" IS the sign of the global tilt; a reflection of
the container flips every sense.  Hence a C4 or C2 pinwheel has one sense, and A249's pattern σ = 00110011 (frame
tilts) is the constant pattern ++++++++ (the BR and TL frames are reflected).  A wall toucher of sense + has its wall
vertex as the UPPER end of its wall-side edge pair walking counter-clockwise; the CW poker of `corner_chase.md` §1.1
(cos θ = 3/5) has φ = −36.87°, the CCW one φ > 0: the two pokers of A248 are the two senses beside a flat (sense 0).

## 2. Normal form (the addendum)

**2.1 VALUE-WLOG [T].**  The value statement is "no packing of n unit squares at side s".  Any operation P ↦ P′ with
P′ a packing at the SAME side — an exchange (SWAP), a collision-free motion, or just a valid end packing — is
admissible: the argument may choose which packing at side s it studies.  The brief's guard ("not a reduction unless
side-non-increasing") was vacuous: the container is fixed.  Caveats, exactly:
(i) UNIQUENESS at s = ŝ: the one-step form (§2.3) picks a maximiser unrelated to the given P, so it proves nothing
about P.  Use the ITERATED form: each step re-packs ONE square (|Y| = 1).  If a chain of k steps from a k0 packing P
ends at a Trump image, P is Trump with ≤ k squares re-packed in (⋃Y) ∪ Free: k = 1 is Theorem U [T]; k ≤ 3 is
SWAP-RIGIDITY [M, A222 §1.7]; k ≥ 4 is [C].  (ii) TERMINATION: the iterated form needs a potential; the row length of
the row being extended grows by one per step but another row may shrink — so normalise in ONE step (§2.3).
(iii) A step may strip a cell of a meeter: then P′ is not family-stuck — the first horn, handled by the k ≥ 1 classes.

**2.2 Lemma NORMAL-CELL [T] (any n, any s) — SLIDE-NORMAL in CELLS form.**  Let s₁ be a wall toucher of tilt φ,
0 < |φ| < 45°, e the unit vector along its wall, d = ±1, **T := s₁ + d · sec φ · e**.  (a) T is a unit square touching
the same wall, int T ∩ int s₁ = ∅, and T ∩ s₁ is a segment of length 1 − tan|φ| (edge to edge).  (b) If T ⊆ [0,s]² and
at most one square D ≠ s₁ of P meets int T, then (P ∖ {D}) ∪ {T} (or, if none, (P ∖ {any}) ∪ {T}) is a packing at side
s.  *Proof.*  (a) project on s₁'s edge normal ν making angle |φ| with e: the translation has ν-component
sec φ · cos φ = 1 = the width of s₁ in direction ν; the wall distance is unchanged.  (b) Lemma CELLS
(`ring_swap.md` §1.3: cells of ANY pose; Lean `cells_swap`) with Π = {T}.  ∎
Consequences.  The PI's "C slides without obstruction" needs no path and no choice of C: ONE obstructing square is
not an obstruction — it is the slider.  "Blocked" means |M(T)| ≥ 2.  The PI's order on second meeters (blocker (a):
"a nearer meeter") disappears.  For flat s₁, T = s₁ ± e (the band lemma's cell).  Towards a corner T is OUT
(δ < 1 < sec φ): rows start at the root meeters.

**2.3 Rows and ONE-STEP NORMALISATION [T].**  A ROW is a set {s₁ + k sec φ e : k = 0 … ℓ−1} ⊆ P of wall touchers;
ℓ(P) := the longest row length (0 if no tilted wall toucher), ≤ n.  Members of s₁'s row other than s₁ are translates
of T by ≥ 2 sec φ along e, hence interior-disjoint from T: the exchange of 2.2 (b) at an END cell of a longest row
raises ℓ by ≥ 1 (the slider D is never in that row; if no square meets T, move any square outside the row —
one exists, since a row of all n squares has length n sec φ > s).  **Theorem.**  Let P maximise ℓ over all packings at side s.
Then P is ROW-NORMAL: every end cell T of a longest row is ⊄ [0,s]² or met by ≥ 2 squares.  So: *if a packing at side
s exists, then a packing at side s exists that is not family-stuck, or one that is family-stuck and row-normal.*
Lean: `exists_max_potential`, `value_form_normal` (theorems, std axioms), `exists_rowNormal` (from the [T-prose]
axioms `normal_cell_step`, `rowPotential_le`).  What it does NOT give: normality of the shorter rows simultaneously
(a lexicographic maximiser of the sorted row-length vector gives it: same proof), wall-touching root meeters, or sense.

**2.4 Blockers, classified [M + T].**  T blocked by D₁, D₂.  (b) D = the next wall square W: for m = 4 it is the
facing corner's toucher (T-SLOTS (b)), the ring's mutual service; on the rings it is the ONLY square meeting T, so the
ring is NOT row-normal — it is one teleport per wall from a longer row, consistent with A253 (the bare ring settles).
(a) D another meeter of c: no contradiction (no order is needed).  (c) D of the second layer: **[F] literally** (§0
witness); [M] below 4, 32 of 53 second-layer blockers over s₁ meet s₁'s own cell.  Type F: the flat A has the band
cell as T; the poker is not in a row, and sense 0 matches either poker — type F is a SECOND structure, not excluded by
any sense argument: on the window it costs one free square per type-F corner (A248), ≤ 3.

## 3. The tests

**3.1 Local search, no slide clause [M] (`local255`, 4 min).**  Quadrant frame; B, A meet c00; C meets c01, not c00; D
meets c10, not c00; pairwise disjoint; two designated TOUCHERS (exact touching: cx = w(θ)/2) with prescribed senses;
the rest unconstrained; sup of the least margin by Nelder–Mead.  Every square lies in [0, 2 + √2]², so for
s > 2 + √2 the far walls never bind: **the local problem is s-free and identical for every m ≥ 4** — what changes with
m is only WHO C can be (m = 4: the facing corner's toucher may reach c01; m ≥ 5: c01, c02, … are served by the wall's
own row until mid-wall, A254 §1.2).  Result: 6 common-sense controls FEASIBLE; **19 / 20 violating types FEASIBLE**;
P4:0+ UNDECIDED (−0.0002: C flat above the root behaves like FLAT-ABOVE, A248 §1.3 — the one candidate for a
certificate, 9 coordinates; not run, not priced: no 20-box benchmark was taken).  No tree was launched.  (triples247's engine cannot express exact touching — a measure-zero constraint; had a type been
infeasible the enclosures of `enc247` wrapped with the touching parametrisation were the plan.)

**3.2 Local search WITH the slide-block clause [M] (`blocked255`).**  Fifth square E; s₁ = B with slider C on the wall
(W types) or s₁ = A with slider D (K types, the mixed corner surviving its floor row's normalisation); some square
other than s₁ and the slider meets T.  W:+− FEASIBLE by 0.0019; K:+− NOT FOUND (−0.0006, 25 restarts); the remaining rows are in
`sense255.md` §4 (detached, 80 restarts).  **The slide-block clause bites**: the blocked counter-hypothesis survives
only marginally on the wall and is not found at the corner — the PI's clause is where the local content is, and the
blocked types (12 coordinates) are the right targets for a certificate, not the unblocked ones.  What would forbid it is the COUNT — each
blocked row end consumes a non-ring square, and n − 4(m−2) is 3 at n = 11 — i.e. a global argument.

**3.3 Corpus [M]** — §0 and `sense255.md` §1–2.  The corpus is not family-stuck anywhere (A250), so it can only say at
what SCOPE the violators reduce: ≤ L2 always.  **3.4 Ring level [M]** — §0 and `sense255.md` §5.

## 4. The lemma, as it should now be stated

**Conjecture COMMON-SENSE(n) [C] (normal form).**  *In a ROW-NORMAL family-stuck packing at s ∈ (m−1, m), the wall
touchers that meet border cells are all tilted and of ONE sense* (Lean `common_sense`).  Known: [F] without
"row-normal" and without the global hypothesis (§3.1–3.2); [M] true on every ring witness; type-F corners are the
flat + tilted exception that must be excluded separately (TWO-POKERS + the free-square count on the window; [M] open
above s* = 3.934).  **The chain.**  ROW-NORMAL [T, WLOG] + COMMON-SENSE [C] + RING-OF-COMMON-SENSE [C: root meeters
wall-touching; four rows of m−2 closing round the corners; the rest pokers — the count 4(m−2)+1 of A254 is [T]]
⟹ ONLY-RING(n) in VALUE form (Lean `only_ring_value`: theorem from the two [C] axioms) ⟹ with MONOTONE-ROOM
(A253/A254 [C]) `peel_excludes_value` ⟹ FAMILY-STUCK-EXIST(11).  Still needed, exactly: (N1) TOUCH-NORMAL — a floating
root meeter can be moved to its wall (not proved; the corpus has 520 doubly-met corners with no wall toucher at all, every one in A244, s ≥ 4);
(N2) COMMON-SENSE in normal form — a GLOBAL statement: the evidence to seek is ring-level (§3.4), not local;
(N3) type-F exclusion on (s*, 4); (N4) the corner step (B and A of one sense): locally free (P1 types), so it must
come from the two rows meeting at the corner both being blocked; (N5) the room.

## 5. What the brief had wrong

1. The guard on "reducible" (corrected by the addendum; §2.1 states the caveats).  2. COMMON-SENSE without the slide clause is not local: the
search on the counter-hypothesis returns FEASIBLE in 19 of 20 types; with the clause it is marginal / not found.
2b. **A bug of mine, caught by the page geometry check:** the first `local255` / `blocked255` runs used a soft
containment term (1 + 10·violation) that let free squares leave the quadrant by ≤ 0.097; all 26 + 3 rows of
`results/archive/*_v1_containment_bug.jsonl` are INVALID (they claimed 20/20 and W margins 0.023–0.035).  Fixed by
parametrising free squares inside the quadrant (cx = w/2 + a²); every current witness is re-verified by `test255`.  3. SLIDE-NORMAL needs neither a path, nor a minimal C, nor blocker (a): it is CELLS on {T}.
4. Claim (c) is false literally.  5. "The chain c01, c02, … is not overlapped by the facing corner until mid-wall":
right, and the local lemma is literally the same statement for m ≥ 5 because it is s-free (§3.1).

## 6. Lean, reproduce

`Statements/Open/CommonSense.lean`: theorems `exists_max_potential`, `value_form_normal`, `exists_rowNormal`,
`only_ring_value`, `peel_excludes_value`; axioms `rowPotential_le`, `normal_cell_step` [T-prose], `common_sense`,
`ring_of_common_sense` [C]; opaque `rowPotential`, `RowNormal`, `CommonSenseN`; build + audit 0 sorry.  Obligations:
O-NORMAL-CELL-LEAN (2.2 over `sqSet` via `cells_swap`), O-COMMON-SENSE(n), O-RING-OF-CS(n), O-TOUCH-NORMAL.
Reproduce: `bash attempts/A255-common-sense/code/run255.sh corpus|local|blocked|ring|pages` (corpus 15 s; local 5 min;
blocked ≈ 15 min; ring detached ≈ 6–10 h, resumable, `logs/STOP`).
