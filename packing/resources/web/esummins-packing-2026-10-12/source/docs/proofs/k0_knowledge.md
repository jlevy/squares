# k0 — THE KNOWLEDGE DOCUMENT: everything the lab knows about k0 as a class (A275, 2026-09-23)

What is true, false, certified, measured, conjectured, and which routes are dead — compiled from the repo only, with
exact citations, for the PI's overview and as the onboarding text for every future k0 theory agent.  **No new
mathematics is in this file.**  Every entry repeats a source's own statement and tag; where two sources disagree both
are recorded with their dates and the later one is named.  Spine: `k0_route.md` §13 (A264, 2026-09-22, updated through
A273).  Brief: `attempts/A275-k0-knowledge/BRIEF.md`.  Status counts of running certificate chains are read from the
index files on 2026-09-23 (read-only; nothing was launched or touched).

## 0. How to read it

**Tags** (as the sources use them):
* **[T]** proved in prose (the proof is in the cited file); **[T-prose]** a proved-in-prose statement that Lean carries
  as a named axiom; **[S]** routine given cited items; **[T given X]** proved modulo the named item X.
* **[T-computed]** a finite computation with its own verifier (certificate files + verifier named); **[T-computed\*]**
  a certificate whose detached chain has not finished (the index file says how much is done).
* **[M]** measured (optimiser, sampling, search) — evidence, not proof.
* **[C]** conjecture / open obligation.  **[F]** false as stated, with the witness.  **[D]** dead route (this file's tag
  for s.7; the sources say "[F as a route]", "not a route", "stop at the design", "priced out").
* **[Q]** (A242/A243) a question: a missing lemma named so that a route can be judged.

**Citations.**  `file §x` means `docs/proofs/file.md` unless a path is given; "Lean `name`" is the declaration in
`lean/PackingCertMathlib/PackingCertMathlib/Statements/Open/<File>.lean` (kind as `lean/AUDIT.md` lists it, generated
2026-09-23 18:37: theorem = std axioms only unless noted; axiom = a named prose/open item).  A### is the attempt.

**Symbols fixed for the whole file.**  s0 = 969271/250000 = 3.877084; ŝ = Trump's side = 3.877083590022814;
s0 − ŝ = 4.0998·10⁻⁷; window W = [3.82, ŝ]; λ = s0/m, λ_max = s0/3.82 = 1.0149426 (`k0_route.md` §1).  m := ⌈√n⌉ for
n-general statements (m = 4 at n = 11), ε = m − s.  w(θ) = cos θ + sin θ.  O = the container centre (s/2, s/2).
"The corpus" = the lab's stored packings (s.10).  "k0_00 unchanged" is the verdict line of every doc A218–A274.

**Reading order for a new agent.**  s.8 (the chain as of today) → s.5 (what is false: do not repeat it) → s.7 (what
is dead: do not re-price it) → s.1 (definitions) → s.2–s.4 → s.6 (what is open, and what would close each item).

**How to use this document.**  Read s.0.5 (one page) first; then read ONLY the sections your brief names.  The appends
(s.11 A278, s.12 A279, and later ones) update s.2–s.8 in place of re-editing them — check them for your topic.

## 0.5 The k0 exclusion in one page (as of 2026-09-24)

**What k0 is, and why room, not force.**  k0_00 = packings of 11 unit squares with no square flush at a census slot
(s.1); the target is "none at any side in [3.82, ŝ]".  A same-side exchange (Lemma CELLS) turns any packing with an
under-met border family into one with a flush corner, which k1_00's tree kills — so only FAMILY-STUCK packings remain,
and those are excluded by ROOM (the ring's pocket holds one square: 8 + 1 < 11); force / torque / handedness arguments
were abandoned because they cannot see unloaded (rattler) crowds, 61 of 70 corners at the k0 FJ points (s.2.6, s.7.3).

**The chain in 8 steps** (s.8; `k0_route.md` §13):
- Swap to a flush corner unless family-stuck; k1_00's tree kills the flush case — [T] + dependency [C] (s.2.1, s.6).
- Pick the most orderly packing (lexicographic normal form P1–P4) — [T] (compactness [T-prose]) (s.2.1).
- At most one square covers the centre O; every other square meets the unit band — [T] (s.2.3).
- Each corner box: ≤ 1 toucher per wall, extra meeters float — [T] (s.2.4); corner types PAIR / THIRD / JAM / FLOAT2 (s.1).
- JAM and FLOAT2 corners need their own room statement (link 5): the strip lemma [T on the flat corner, A276 FLAT-X /
  CORNER; T-computed* outside it: index273 67/81 cells, 43 CERT, 24 OPEN-LAYER on 2026-09-24] + `pair3` [not
  landed] + link 5d [C] (s.3, s.6, s.8).
- Each wall is a row of two, a row of three or an open pair — [T-prose] (s.8 link 7); the other pinwheels are excluded
  below ŝ: A261 50/50 [T-computed], near-flat cube [T], slab jobs [C] (s.2.5, s.3).
- Open pairs survive only as locks held by a free square — [T] (s.2.1).
- Room: every free square of the (hybrid) normal ring contains O — [T-computed] on D′ and the common-tilt hybrid
  (A259, A260), [T-computed\*] independent tilts (20 P2 cells open), [C] non-ADJ = CAPACITY-2 (s.3, s.6).  Then 8 + 1 < 11.

**The two open CAP-2 conjectures of link 5d** (s.6, s.11, s.12):
- [C] BL-CAP-2(C, D) (FLOAT2 corner; Lean `bl_cap2_float2`) — made unnecessary by NO-FLOAT2 (= the 4-square statement L,
  Lean `float2_local`), whose P1-sense residual is (NEST); NEST-emptiness proves the P1-sense statement, not L (A279).
  Closes by: `cert277` (30–1000 CPU-h) or a NO-FLOAT2 certificate / proof (NEST prunes first).
- [C] BL-CAP-2(A, C) (JAM with any holder) — S1–S4 [T], no hand proof; closes by `cert277 --fam jam` (5 params, 3–100 CPU-h).

**Five FALSE turns not to repeat** (s.5):
- "Counting closes it" — every count (K0-COUNT, sweep, NO-CLOSURE, family ILP = 9) has slack at n = 11 (s.5.1).
- "One corner decides" — COMMON-SENSE, TOUCH-NORMAL, POKE's sense are false locally; Trump has a locked 2-crowd (s.5.2).
- "A disc radius bounds the pocket" — CENTRE-DISC about O fails at the corner MOUTH; the DISC LEMMA is false (s.5.2–5.3).
- "There is a tilt floor / positive minimum tilt" — θ_min = 0; the limit is the domino pinwheel (s.5.2).
- "The domain box is the condition" — STRIP₂ with "h_u, h_v < 1" for tilted C; (U3)–(U6) from H1–H5 (s.5.3).

**Three pitfalls** (s.10.6): an optimiser's sup is not evidence (A272's −0.005 was +0.0079); census counts are not
closed classes ("k5 closed at the window pad" read the G1 slab pad as the window); a verifier bin or a soft
(penalty) feasibility is not a certificate — re-check exactly, bisect on disagreement.

## 1. DEFINITIONS (fixed)

**k0 / k0_00.**  The packings of 11 unit squares whose skeleton is empty: no square is axis-aligned at a census slot
(Lean `skeleton s z = ∅`); its monotone hypothesis is TRUE of every packing, so its tree is the zone-tree of the whole
problem.  [F] "k0_00 is empty" as a bare set: a rotation R_φ of Trump by 0 < |φ| ≤ 1.0574·10⁻⁷ is a k0_00 packing at
side ≤ s0 (σ(R_φ ẑ) = ŝ + 3.877|φ| + O(φ²)); the target is "no k0_00 packing at any side m ∈ [3.82, ŝ]" (at ŝ every
packing is a Trump image, not in k0_00).  `k0_route.md` §1, §5.2 (A85).  "k ≥ 1 classes" = skeletons with ≥ 1 slot
square (k1_00, k5_11, k5_16, trump5, …), each with its own tree/ledger.

**Corner box, meets, simple square.**  B_c = the closed unit box at corner c; Q MEETS B_c iff int Q ∩ int B_c ≠ ∅
(A58's convention; `k0_route.md` §1).  A SIMPLE (settled, flush) corner = the slot square [0,1]² of the corner frame is
in P; then it is c's only meeter (Cor. B1, `sideband.md` §4; = WEDGED-SEAL, `wedged_seal.md` §0).  The widened box
B_c^w = B_c(s0) grown by w = (λ_max − 1)(1 + √2/2) = 0.025509 into the container (Lemma K0-WIDEN, `k0_route.md` §4.1).
DOUBLY MET / K0-BLOCKED / four-crowd: every corner box met by ≥ 2 squares (`k0_blocked_side.md` §0 (A92); A217).

**The 12 border cells and the 8m − 20 general system.**  Per corner c: c00 (the box), c01 (the wall slot up c's
wall), c10 (the floor slot along c's floor) — twelve cells at m = 4 (A244 `cells244`; `family250.md` §1.1).  Along a
wall the intervals are (0,1), (1,2), (s−2,s−1), (s−1,s); only the facing pair (1,2)/(s−2,s−1) can overlap, and it is
disjoint iff s ≥ 4, so below 4 the conflict graph is a perfect matching on the eight slots (max family 8, 1295
admissible families), empty at s ≥ 4 (max family 12, 4095 families) [T] (`family250.md` §1.3).  General m: the four
boxes + per wall the LEFT chain L_j = [j, j+1] and RIGHT chain R_j = [s−j−1, s−j], j = 1..m−3: **8m − 20 cells**;
L_j, R_j′ overlap iff j + j′ = m − 2 (a NARROW ribbon, width ε) or m − 1 (a WIDE overlap, width 1 − ε) [T]
(`peel.md` §1.1, A254).  The five-cell corner neighbourhood N_c = {c00, c01, c10, c′10, c″01} (`perimeter_walk.md` §0,
A247).  The SLOT-OVERLAP RIBBON of a wall = [s−2, 2] × [0,1] (`centre_disc.md` §0, `normal_ring.md` §2).

**Slots, ribbons, eps.**  "eps" has three uses in the sources: (i) ε = m − s (the distance below the trivial side;
`peel.md`, `normal_ring.md`); (ii) ε₀ = 0.703° = π/256, A261's TMIN, the lower tilt limit of the closed-LP window
certificates (`box_meeters.md` §0, `three_lemmas.md` §0); (iii) Lemma EPS (A227, `lemma_eps.md`): the wedges of a
near-simple square's cell (C \ F = four convex wedges W_R, W_L, W_T, W_B; the PINWHEEL feet; depth bound
w̄ ≈ δ + θ0/2) — a tree-engine rule (Rule EPS), n-general.  EPS as a distance in certificate code is 10⁻⁹ (A273).

**FAMILY-STUCK and its relatives** (`family250.md` §1.1, A250; `ring_swap.md` §1.3, A222).  M(Π) = the squares whose
interiors meet a cell of Π.  **CELLS** (Lean `cells_swap`, theorem): a packing exchanges at the same side into one
containing every cell of a disjoint family Π iff |M(Π)| ≤ |Π| (§0's wording; §1.3 states and proves the "if").
**K0-FREE** = CELLS with |Π| = 1 at a corner (`k0_route.md` §3, A85).  **swap_packing** (Lean theorem, `RingSwap.lean`):
replacing X ⊆ P by |X| unit squares inside U(X) = (⋃X) ∪ Free keeps the packing; **teleport_of_swap** = |X| = 1 gives
`teleport_packing`.  **TWELVE-STUCK** = every one of the 12 cells met by ≥ 2 squares (A244); **PAIR-STUCK** = also every
domino {c00, c01}; **FAMILY-STUCK** = |M(Π)| > |Π| for EVERY admissible family (n-general; Lean `FamilyStuckN`,
`familyStuck_twelveStuck`).  TELEPORT-STUCK = every corner box met by ≥ 2 (Lean `TeleportStuck`, `TwoGrains.lean`).

**Meeter / toucher / floater / poker / holder / rattler.**  A MEETER of c meets int B_c.  A TOUCHER touches a wall
(a WALL TOUCHER of wall w).  A FLOATER is a box meeter touching no wall; SAME-WALL + WEDGED-SEAL make every box meeter
beyond one toucher per wall a floater (`box_meeters.md` §0, A261).  A POKER (A252's corrected structure) is a FREE
square meeting BOTH slots of one wall, by convexity with its corner in the overlap [0,1] × [s−2, 2] (`centre_disc.md`
§0); the SEATED poker stands in a row's TOOTH at the row's tilt (`normal_ring.md` §2).  A248's POKE is the older use:
a tilted wall square beside a flat meeter that pokes into the corner box (`corner_chase.md` §1).  A HOLDER of a meeter
Q is a square whose force on Q (FJ stress) has a strictly negative component toward the corner; ALONG ITS WALL if
along the wall Q touches (`k0_count.md` §1, A218).  A RATTLER MEETER carries no loaded row (ibid.).  A LOCK is a free
square meeting a normal cell of an open pair; it is HELD iff (P ∖ {W, F}) ∪ {T} is SATURATED (`locked_wall.md` §1.2).

**Sense / handedness.**  φ(Q) := ((θ + 45°) mod 90°) − 45°, sense(Q) := sign φ (flat 0; 45°: none); SENSE-INVARIANT
[T]: a quarter turn fixes θ mod 90°, so sense is frame-free round the perimeter, a reflection flips it; a C4 or C2
pinwheel has one sense (`common_sense.md` §1, A255).  A223's HANDEDNESS: '+' for θ mod 90 ∈ (0°, 45°), '−' for
(45°, 90°), 'D' at 45°, 'F' flat (`two_grains.md` header).  FRAME handedness equals global at BL, TR and is swapped
at BR, TL (`two_grains.md` §1.4).  Type F corner = a flat meeter on a wall + a tilted partner; type T = both meeters
tilted (`corner_chase.md`, `type_t_chase.md`, A248/A249).

**Rows, normal cell, potentials, P1–P4** (`common_sense.md` §2.2–2.3, A255; `normal_ring.md` §0, §1.2, A258).
NORMAL CELL of a wall toucher s₁ of tilt φ: T := s₁ ± sec φ · e_wall (a unit square touching the same wall, sharing a
segment of length 1 − tan|φ| with s₁); NORMAL-CELL [T]: if T is met by ≤ 1 square D ≠ s₁, D exchanges onto T (Lemma
CELLS with Π = {T}).  A ROW = {s₁ + k sec φ e : k = 0..ℓ−1} ⊆ P of wall touchers.  Φ = (Φ₁, Φ₂, Φ₄, Φ₃)
lexicographically: Φ₁ = #wall touchers; Φ₂ = sorted vector of maximal common-tilt row lengths; Φ₄ = −#(border cell,
non-toucher) incidences (the RETREAT term); Φ₃ = −Σ (counter-clockwise wall coordinate of the touchers).  A maximiser
satisfies **P1** touch-normal (every wall-touching unit cell met by a toucher or by ≥ 2 squares, if a non-toucher
exists); **P2** row-normal modulo longer rows; **P2′** a free square blocking a normal cell with W has nowhere else
to go; **P4** RETREAT (no re-posing of non-touchers lowers the incidence count: a free square in a slot is HELD);
**P3** every maximal row is blocked against the clockwise slide.  **P1⁺** = the family form of P1: a family of disjoint
wall-touching cells of any pose with |M(Π)| ≤ |Π| is met by touchers only (`box_meeters.md` §1.1, A261).

**Corner types** of a doubly-met box (`no_jam.md` §1, A262; (touchers on u, on v, floaters)): **PAIR** (1,1,0) — A the
floor START, B the wall END; **THIRD** (1,1,≥1) — PAIR + floater(s); **JAM** (1,0,1) — A on the floor meets, C floats
and meets, X on the wall ABOVE C misses the box (its LOWEST point ≥ 1: with X's leftmost vertex (0, y_X), edges (cos φ_X, sin φ_X), (sin φ_X, −cos φ_X), X_low = y_X − cos φ_X ≥ 1 — A278 erratum, fixed A279) and jams C; mirror JAM (0,1,1);
**FLOAT2** (0,0,≥2) — two floaters meet, the blockers meet neither.

**The ring families.**
* **All-ADJ ring, 17 coordinates** (A249/A251): eight wall-touching tilted meeters, each reaching the far slot of its
  wall; per corner (θ_B, δ_B) of the wall meeter and (θ_A, δ_A) of the floor meeter, plus s; all-ADJ forces
  δ ∈ (s − 2 − w(θ), 1) ⊆ (0.406, 1) on W, so the box is [0, 90°]⁸ × [0.406, 1]⁸ × [3.82, 4] (`ring_pocket.md` §0-§1).
* **The normal ring, domain D** (`family258.md` §2, A258): the pinwheel of four common-tilt ROWS OF TWO of one sense,
  parameters (a_w, φ_w) + s, b_w := K(φ_w, s) − a_w, K = s − sec φ − cos φ − sin φ; (D1) 0 < φ_w < 45°; (D2) a_w,
  b_w < 1 (row ends meet both boxes); (D3) a_w + sec φ_w < 2, b_w + sec φ_w < 2 (slot cut: all 12 cells met by exactly
  two ring squares); (D4) max(E_A, E_B) ≥ 0 at every corner (common tilt: a sin φ + b cos φ ≥ 1).  **D′** = D without
  (D3).  **D_tight** = all four corners in contact (C4, explicit).  Least side 1 + sec φ + cos φ + sin φ + tan(φ/2).
* **Hybrid family D^h** (`family258.md` §7): D′ with r ∈ {0..3} walls replaced by LOCKED walls (an open pair s₁, W with
  open gap e = s − a − b − sec φ₁ − w(φ₁) > 0 and a free square in the open notch): 8 + 2r coordinates + s.
* **The JAM ring** (`no_jam.md` §0): floor row, right row, ceiling row, X on the left wall serving TL, C floating
  0.57–0.72 off the wall meeting the BL box by a sliver 0.003–0.010.
* **ADJ / non-ADJ**: ADJ = every toucher reaches its far slot (s₁: a + w(φ₁) > s − 2; W: δ_W < 2); without ADJ the
  open shift reaches e ≤ 1.169 (≤ 0.349 with ADJ) [M] (`open_pairs.md` §0 (c), §3.1, A263).

**The JAM corner hypotheses H1–H5** (`ring_domain.md` §0 notation, A271; BL frame, wall x = 0, floor y = 0; C the
floater, T_u = C − h_u e_x its WALL DROP, S = T_u ∖ C the STRIP; X the wall toucher; A the floor toucher; s̄ the
side).  **H1** X meets the open TL box (X_top > s̄ − 1), X ⊆ the container, X misses the open BL box (X_low ≥ 1).
**H2** int X ∩ int T_u ≠ ∅ (X holds C), int X ∩ int C = ∅.  **H3** C meets the open box and floats (h_u, h_v > 0);
A meets the open box; int A ∩ int C = ∅.  **H4** s̄ ∈ [3.82, ŝ]; family-stuck and normal (P1–P4).  **H5** HELD-JAM (not
used).  A271: only H4's side bounds are ever used.  Ring domain (D1)–(D2), (U1)–(U9): `strip_enclosure.md` §3 (A267).
C meets (0,1)² iff h_u cos θ + h_v sin θ < cos θ + sin θ − sin θ cos θ (Lean `open_box_tilted`, `last_two.md` §0, A266).

**The slabs G1–G4 and the window.**  A57's four side slabs (the k5 trees' sides): G1 = (3.861637, s0] (ŝ included),
G2 = (3.847016, 3.861637], G3 = (3.832450, 3.847016], G4 = [3.82, 3.832450] (`slot_crowds.md` §5 table;
`docs/shadows/STATUS.md` per-slab table, A270).  "g1 pad" = the G1 slab's pad, NOT the window (A270 BRIEF line 3; see
s.5).  The k0 chain's own "slab" (`open_pairs.md` §5, A263) is different: some wall's tilt in (0, 0.703°).

**Value form vs uniqueness form.**  VALUE: "no packing of 11 unit squares at side m < ŝ" — any same-side operation
(exchange, motion) is admissible, so the argument may choose which packing at side m it studies (VALUE-WLOG [T],
`common_sense.md` §2.1).  UNIQUENESS at ŝ: the one-step normal form proves nothing about the given P; the iterated
form re-packs one square per step, and a k-step chain ending at a Trump image is k = 1 Theorem U [T], k ≤ 3
SWAP-RIGIDITY [M], k ≥ 4 [C] (ibid.; `ring_swap.md` §1.7).  AllForm vs MinForm: `stratum_kill` for every packing vs
for σ-minimisers only (`k0_route.md` §9; `drain_flow_k0.md` §0, A87: the k0_00 obligation is legitimately MinForm).

## 2. THEOREMS about k0

One or two lines each; n-general unless "n = 11" is said.  Format: tag, NAME — statement.  Source; Lean; attempt.

### 2.1 Exchange and normalisation

- [T] **K0-D4** — equivariant /8 quotient of any zone-tree with (K)/(C)/(D)/(D′)/(T) leaves; instance (i) the
  interior-first root (Theorem A38.1 + `d4_wlog`), instance (ii) the corner seed.  `k0_route.md` §2; A85.
- [T] **K0-FREE** — a packing at m ∈ [3.82, ŝ] with a corner box met by ≤ 1 square does not exist (m < ŝ) or is a
  Trump image (m = ŝ), GIVEN k1_00's tree (k1-a/k1-b) and Theorem U; ∀-packings, no selection.  `k0_route.md` §3;
  Lean `teleport_packing`; A85.  Corollary **K0-FREE′**: every non-image packing on W has every corner doubly met.
- [T] **K0-WIDEN** — a meeter of B_c(m) dilates to a meeter of B_c^w(s0), w ≤ 0.025509; converse for the unwidened
  box.  `k0_route.md` §4.1; Lean `k0_widen_stmt` (theorem, `Dilation.lean`); A85.
- [T] **K0-BLOCKED (structure)** — else eight distinct squares in the four widened reach sets, ≤ 3 free (widened boxes
  are 1.826 > √2 apart).  `k0_route.md` §4.2; A85.
- [T] **K0-ATLAS** — a node whose eleven squares lie in an A37 atlas box (V ≥ s0) is empty for m < s0 (dilates have
  strictly positive wall margins).  `k0_route.md` §4.3, §12; Lean `PackingCert.Atlas.atlas_dilated_kill_fold`; A85/A86.
- [T] **K0-PAIR (a)** — two axis-aligned squares meeting int[0,1]² overlap (w = 0).  (b) [T+M] the corner 2-crowd space
  has interior in the 6-dim pose space and contains same-sense tilted pairs (exhibit, SAT gap 0.0441).  (c) [S] the
  rigidity that exists is box-level.  `k0_route.md` §4.4; A85.  [S] **K0-REUSE** — the near-slot pocket is k1_00's
  tree + a one-square ladder.  `k0_route.md` §4.5.
- [T] **K0-ROT** — at a σ-minimiser D⁺σ ≥ 0 and D⁻σ ≥ 0 (one-sided rotation derivatives with the exact
  centre-height term); a (C) leaf in the selected form only.  `k0_route.md` §5.1; A85.
- [T] **SWAP / STEP / CELLS** — a same-side exchange of X ⊆ P into |X| squares of U(X) is a packing; the sweep's
  step; a packing exchanges into one containing a disjoint cell family Π whenever |M(Π)| ≤ |Π|.  `ring_swap.md` §1.1–1.3;
  Lean `swap_packing`, `teleport_of_swap`, `cells_swap` (theorems); A222.
- [T] **RAISE(0 → 1) + k1-a ⟹ k0_00 empty** — `ring_swap.md` §1.5; Lean `no_packing_of_raise` (theorem; RAISE itself is
  the axiom `raise_zero_one`, [C]); A222.
- [T] **SWAP-LEAF** — a cell with an injection naming X, |X| fixed-pose unit squares (one the corner slot), and one
  exact MISS certificate per (square, role outside X) is empty wherever k1-a holds; **X-FORCED** (|X| ≥ u, the number
  of unboxed roles); **SPLIT-INVARIANCE** (A185's split never lowers u; only conditioning does).  `swap_leaf.md` §0;
  Lean `swap_leaf_dead`, `swap_leaf_exchange`, `swap_leaf_corner` (theorems, std only); verifier `verify_swap232.py`;
  A232.
- [T] **WALL-SLOT** — a wall slot met by ≤ 1 square swaps in its slot square at the same side (with SLOT-MET [S] the
  corner becomes singly met, then K0-FREE).  `attempts/A243-reach-root/notes/wall_slot243.md`; Lean `wall_slot_link`
  (axiom, `StuckExist.lean`); A243.
- [T] **FAMILY-STUCK is the right hypothesis; dead at s ≥ 4** — no 11-square configuration at side ≥ 4 is
  family-stuck (the twelve cells are a legal family), hence RAISE at every s ≥ 4.  `family250.md` §1.2, §2.1; Lean
  `no_family_stuck_ge_four`, `raise_of_ge_four`, `family_stuck_of_stuck_exist` (theorems); A250.
- [T] **VALUE-WLOG, NORMAL-CELL, ONE-STEP NORMALISATION** — a longest-row maximiser exists and is row-normal or some
  packing at s is not family-stuck.  `common_sense.md` §2.1–2.3; Lean `exists_max_potential`, `value_form_normal`,
  `exists_rowNormal` (theorems), `normal_cell_step` (axiom [T-prose]); A255.  (Its last line "simultaneous
  row-normality" is [F], s.5.)
- [T] **NORMAL-FORM** — a lexicographic maximiser of (Φ₁, Φ₂, Φ₄, Φ₃) exists with P1, P2, P2′, P3, P4; the compactness
  step is [T-prose].  `normal_ring.md` §1.2; Lean `exists_lex_max`, `exists_normalForm` (theorems) over the axioms
  `touchPotential_le`, `rowVecPotential_le`, `normal_form_step` [T-prose]; A258.  Chain link 1: `normal_ring_value`.
- [T] **UNLOCK = P2′; HELD; LIFT** — a lock survives in the maximiser iff (P ∖ {W, F}) ∪ {T} is saturated; F + λv
  clears T after λ_T = e sin φ.  `locked_wall.md` §1; Lean `unlock_swap`; A260.
- [T] **The common-tilt exchange is P2′ again** — in the maximiser every unequal-tilt open pair is held by a free
  square in every such cell.  `open_pairs.md` §0 (b), §4; A263.
- [T] **REDUCE** — the 3-for-3 exchange (corner domino + one leftover) is `cells_swap` with k = 3.  `snap_down.md` §3;
  Lean `reduce_three_for_three`; A245.
- [T] **EXTREMAL(n) / NO-ROTATE** — the Ψ-minimal optimal packing has no retreating square (global minimum: several
  squares may move); the FLUSH-STACK click changes Ψ by (4 − s) − d_c(B) − d_c′(B′) − d_c(B′).  `local_lock.md` §1;
  `corner_chase.md` §2; Lean `no_retreat_of_psiMin`, `psiMin_no_lowering`, `no_rotate`; A233/A248.
- [T] **SLIDE** (∀-packings, modulo k1-a) — at every corner of a K0-BLOCKED packing at m < ŝ, d₂(c) ≥ ŝ − m.
  `k0_blocked_side.md` §3.1 (A92); the joint-translation proof is A94's (`slot_crowds.md` §3.4); Lean `lemma_SLIDE`.
- [T] **DF-K0** — H1(ŝ) ⟹ the k0_00 instance of `StratumKillMin`; the drain step is unnecessary, the exit map does
  not exist (codim-3 strata), selection compatibility is void.  `drain_flow_k0.md` §0, §2 (A87); Lean consumers
  `s_eleven_ge_of_split`, `s_eleven_unique_of_split` (A86).  **F-LEAF** [T]: minimiser-only (C) leaves are admissible.
- [T] **Lemma CH / D1 / D2** (descent) — a corner met at depths d₁ ≥ d₂ converts rigidly to simple at side cost d₂;
  conversion descent yields exactly 0 at a k0 corner at every side.  `descent.md` (A194; ledger §4 A194 note).

### 2.2 Counting (every count below closes nothing at n = 11 — s.5)

- [T, vacuous] **K0-COUNT** — under LOAD and DISTINCT at four doubly-met open corners, n ≥ 12.  `k0_count.md` §4; A218.
- [T] **CEIL** — s(n) ≤ ⌈√n⌉ (Lean `fits_eleven_four` from the axiom `simple_packing_fits`).  `wall_torque.md` §1; A219.
- [T] **FLUSH** — n axis-aligned unit squares need side ≥ ⌈√n⌉ (Lean `lemma_FLUSH` axiom [T in prose],
  `flush_eleven_four`).  **FOUR-WALL (conditional)** and **CLICK-DOWN ⟺ STUCK** [T] (Lean `four_wall`,
  `no_stuck_in_window` over the axiom `click_down` [C]).  `two_grains.md` §3; A223.
- [T] **Perimeter count** — family-stuck needs n ≥ 4⌊s⌋ − 3 = 4(m − 2) + 1; closes for no n ((m − 3)² ≥ 0).
  `family250.md` §2.1; `peel.md` §1.2; A250/A254.  `ring_swap.md` §1.4: counting closes only for n ≤ 4.
- [T] **NO-CLOSURE** — 4(m − 2) + ((m − 2)² − 3) + 4 = m² − 3 ≥ n whenever s(n) < m; at n = 11: 8 + 1 + 4 = 13 ≥ 11.
  With TILT-BAND, BAND-FLUSH, BAND-COUNT, CORE-CAP, Lemma TWO.  `ring_capacity.md` §0, §2–3; Lean `count_never_closes`;
  A236.
- [T] **BAND-COUNT (general)** — at s ∈ (m−1, m), s > 2 + √2, at most 4(m − 2) squares of ANY packing are band squares.
  `peel.md` §2.1; Lean `band_count` (axiom [T-prose]); A254.  **PEEL-0** [T]: core squares pack at side s − 2, so
  s ≥ 2 + s(k).  `peel.md` §2.2; Lean `core_fits`, `peel_side_bound`, `peel_no_straddler` (theorems); A254.
- [T] **COUNT (NO-JAM)** — n = 8 − E + U + F_box + F_rest, consistent with 11; **ROOM(S_min) ≤ 1 ⟹ n ≤ 9** for every
  corner type.  `no_jam.md` §0, §2; Lean `jam_count_core`, `no_jam_of_count`, `box_meeters_262`; A262.
- [T] **8 + 1 < 11** — eight ring squares + one square containing O.  Lean `openPairs_excludes`, `normalRoom_count`,
  `k0_value_of_factors`, `lockedWall_excludes`; `k0_route.md` §13 link 11.
- [T] **The ninth square** — every cell of the bare normal ring has exactly two ring meeters; |M(Π)| − |Π| ≥ 1 unless
  Π is maximal; so a ninth square meets a third box or both slots of one wall.  `normal_ring.md` §2; A258.
- [T] **gap_needs_two_misses**; **CAPACITY-2 = three gap statements**; **gap_interval_centre** (a unit interval in
  [1, s − 1] contains s/2).  `strip_plug.md` §0; `last_two.md` §0; Lean same names, `capacity_two_of_gap`; A265/A266.

### 2.3 Room (what fits in the pocket)

- [T] **HOLE-ONE** — in a square container of side σ ≤ 2 every unit square contains the centre, so at most one fits;
  applied to σ = s − 2 the slack is (4 − s)/2 > 0 exactly on s < 4.  **NOTCH-NARROW** [T] — a unit square does not fit
  a rectangle with a side < 1.  So capacity(flush-limit pocket) = 1 for s ∈ (3, 4): 8 + 1 = 9 < 11.
  `mintilt253.md` §0, §3 (A253); tilt form Lean `hole_one_tilt` (`normal_room.md` §2.1, A259).
- [T] **INRADIUS, THREE-DISC, CENTRE-DISC ⟹ capacity ≤ 2, MID-NOTCH** (no wall notch of an all-ADJ ring holds a
  disc of radius ½ for s > 3.27645; robust form s > 3.80342), **GAP** (a wall's two touchers overlap or leave a gap
  < 4 − s).  `ring_pocket.md` §0, §3; Lean `inradius_sep`, `capacity_le_two_of_centre_disc` (theorems), axioms
  `unit_square_inball`, `three_disc`, `mid_notch_wall` [T-prose]; A251.
- [T] **MOUTH, CONTACT-TRIPLES, NOTCH-SEP, TWO-VERTEX, TWO-PIECES, POKER-ANCHORED; ring + POKER structure** — sixteen
  eight-cell families are met by the ring alone, so the only protection is a poker; if the admissible centres beside
  the pinned poker have diameter < 1, capacity ≤ 2.  `centre_disc.md` §0, §5; Lean `capacity_le_two_of_two_pieces`,
  `capacity_le_two_of_anchor`, `ring_pocket_of_poker_residual` (theorems), `ring_has_poker`, `pocket_count_three`
  (axioms [T-prose]); A252.
- [T] **LIMIT-UNIQUE(4) + USC** — the flush stratum of the all-ADJ family is exactly the two pinwheels, so some
  τ₀ > 0 (NOT effective), uniform on [3.82, 4 − η], gives capacity ≤ 1 for all rings with all eight tilts < τ₀.
  `peel.md` §0, §2.4, §5; A254.
- [T] **JAGGED, WEDGE (J3), PIERCE (J4)** — k points, one in the interior of every unit square inside P, bound the
  capacity by k.  `pocket_waste.md` §0, §2; Lean `capacity_le_of_pierce`; A237.  **POCKET-CAP** [T]+[M]: a stable ring
  is impossible if its pocket's capacity is < n − p.  Lean `ring_capacity_of_pocket_cap` etc. over axiom `pocket_cap`.
- [T] **NORMAL-ROOM reduction** — a free square missing O forces, at one corner, a CORNER-PAIR violation (4 parameters,
  s eliminated: Lean `corner_frame_mono`); TOOTH; WEDGE (the START gap holds nothing if a < 1).  `normal_room.md` §2;
  Lean `hole_one_tilt`, `tooth_flat`, `normalRoom_excludes`, axiom `pair_pierce`; A259.
- [T] **OPEN-TOOTH** (least depth in the open notch ≥ cos φ − (e/2) sin 2ψ); **PLUG** (a′ ∈ (0.354 + ρ, 1) ⟹ no free
  square meets [0, ρ]²; closes CORNER-NOTCH with the layer certificate).  `locked_wall.md` §0, §2, §4; Lean
  `open_tooth_at_tilt`, `plug_kernel`, `poke_chord` (theorems), axiom `hybrid_pierce`; A260.  **plug_graded** [T]
  (ρ = 1/4, 1/8, 1/16), `strip_plug.md` §0, A265.
- [T] **FACTORISATION with the PRINCIPAL NORMAL** — a free square missing O violates at one corner one of P2 / WE / WS,
  each two squares and four parameters, tilts independent; **WEDGE-NOTCH** in closed form (≤ 12 vertex values of a
  2-variable LP).  `open_pairs.md` §0 (a), (a′), §1–2; Lean `principal_normal`, `factor_cover`, `wedge_depth_common`,
  `clip_mono` (theorems), axiom `factor_pierce`; A263.
- [T] **ADJ side bound** — test each box at s_eff = min(SMAX, hi_b + w(hi_φW) + 2, hi_a′ + w(hi_φ₁′) + 2) (corner-frame
  monotonicity).  `strip_plug.md` §0; Lean `adj_side_bound`, `p2_of_adj_side`; A265.
- [T] **GAP-CELL, BLOCKER-SIDE for the gap, STRIP-CHAIN** (common tilt, e ≥ sec φ₁) — pieces of the non-serving gap.
  `three_lemmas.md` §0 Lemma 2 (a)–(c); A264.  **Non-ADJ count** [T]: a non-served far slot needs a FREE third meeter;
  non-ADJ walls carry a free square in the unserved slot (Lean `nonadj_free_meeter`).  `open_pairs.md` §3.1; A263.
- [T] **STRIP for a flat C in standard orientation** (chord / column / shrink).  `strip_plug.md` §0, §1.3; Lean
  `strip_of_two_obstacles` (STRIP against {C, X} ⟹ A264's `strip_lemma`); A265.
- [T] **WEDGE-FLOAT** — if C meets the open box with h_v < 1 < h_v + cos θ, every quadrant square free of C with a point
  in S has its centre strictly above height 1 (A and WEDGED-SEAL not used).  `strip_enclosure.md` §0, §1; Lean
  `wedge_float_core`; A267.  [T-prose] **STRIP₂-IN-RING** on (D1)–(D2), (U1)–(U9): Lean `strip_two_in_ring` (axiom),
  `wedge_extent_core`, `strip_in_ring_of_enclosure`; A267.
- [T] **SLOPE, LOW** — a floater sharing its box with a floor toucher has L_h ≥ 1.121 (> 1, no uniform margin, in the
  steep case); (D1), (D2), (U1), (U2), (U9) are theorems from H1–H3.  `ring_domain.md` §0, §2; Lean `low_core`,
  `lh_gt_one`, `lh_gt_one_steep`, `tangent_core`, `u1_core`, `u9_core`, `x_high`; A271 (+ the A271 follow-up after
  A273's flag, commit 7cb36df98: `lh_gt_one` covers α ≤ 45°, cases α > 45° by the top vertex and `lh_gt_one_steep`;
  s.5.4 item 7).
- [T] **Lemma CL** — the case q_y > X_top with Q left of X is dead ((D − cos φ) cot φ ≤ c); **the reduction** of every
  other case to a statement about a point and convex sets; `centre_right_core`.  `strip_jam.md` §0; Lean `cl_core_i`,
  `cl_core_ii`, `d_low_core`, `centre_right_core`; A272.  (The statement it reduced to, the DISC LEMMA, is [F]: s.5.)
- [T] **DROP LEMMA is h_v-invariant (4 parameters); ⟹ STRIP₂-IN-JAM** by A272's reduction; **the limit θ = φ = 0
  holds with ZERO margin**.  `disc273.md` §1, §2.1, §5; A273.  Lean unchanged (`DiscLemma` opaque).

- [T] **ONE-DROP, MUTUAL, the drop form of P1** (A277) — a square interior-disjoint from a box-meeting floater blocks at most
  one of its two drops (BLOCKER-SIDE + its mirror on one separating normal); two floaters meeting the open box are separated
  by a positive-slope line — then only the upper-left one's floor drop and the lower-right one's wall drop can be blocked by
  the other — or block no drop of each other; in the Φ₁-maximiser every drop of every non-toucher is blocked.  Lemma LOW holds
  with a FLOATING lower-right square in A's role (its proof uses only a point of that square under the separator).
  `float2_room.md` §1, §5.1; Lean `one_drop_core`; A277.
- [T] **CAP-2 is the room statement of link 5d** (A277) — n ≤ 8 + cap(S_8) with EVERY non-S_8 square (middle touchers,
  blockers) a pocket square; two misses ⟹ two BL-sector misses (PAIR corners kill theirs); so a non-PAIR corner needs
  **BL-CAP-2 of its two box meeters** (no two disjoint BL-sector misses; diameter < 1 of the admissible-centre region
  suffices), not ROOM — which is FALSE for FLOAT2 whenever a blocker outside S_8 misses O.  The strip lemma STRIP₂-IN-JAM
  transfers to a FLOAT2 floater verbatim iff its blocker serves the far box (H1); the indirect JAM needs no reduction (its
  holder is a pocket square).  `float2_room.md` §0, §3, §5; Lean `cap2_count_core`, `cap2_of_diam`, `float2_ten`; A277.
### 2.4 Corner geometry

- [T] **SIDEBAND (a)** (sharp constant c), **Lemma A1** (ℓ∞ centre separation ≥ 1/√2), **A2** (two meeters' centres
  in distinct cells of the 2 × 2 grid), **Theorem B** (a second meeter exists iff one of (NE), (W), (S), (P) holds),
  **Cor. B1** (a pressed first meeter admits no second meeter of the unit box).  `sideband.md` §0; Lean
  `Sideband.not_both_ne`, `linf_sep`, `distinct_cells`; A169.
- [T] **Theorem CEIL (per corner)** — every corner of every packing has min(d₁, d₂) ≤ 1 − 1/√2, equality only for the
  diagonal 45° pair.  `k0_blocked_side.md` §2.1; A92.
- [T] **PUSH** — two quadrant squares meeting the open corner box push each other OUT (n_u > 0 or n_v > 0; along the
  wall a pushed square touches).  **HOLD** — at an FJ point a pressed meeter has a holder.  `k0_count.md` §2–3;
  Lean `lemma_PUSH` (axiom [T in prose]); A218.
- [T] **ONE-TILTED** — two axis-parallel squares both meeting the open corner box overlap.  `wall_torque.md` §3; Lean
  `one_tilted` (axiom [T in prose]); A219.
- [T] **WEDGED-SEAL** — a corner square touching both walls (any tilt) has no second box meeter; = Cor. B1.
  `wedged_seal.md` §0; Lean `wedged_seal` (theorem via `lemma_PUSH`); A239.
- [T] **TILT-MIN binds UPWARD** (sin θ ≤ δ; partner's lowest point ≥ 1 − (δ − sin θ) tan θ) and **DEPTH-BUDGET**
  d_A + d_B ≤ 1 (flat wall meeter + any partner).  `pocket_waste.md` §1; A237.
- [T] **REACH, GEAR-RATIO, LEVER** — for flat + tilted crowds under torque balance (structure statements).
  `attempts/A239-rings-below-4/notes/rings_below_4.md`; ledger §4 A239 note; A239.
- [T] **A246's rules** — TWO-CORNERS, MAX-FIVE, SQUARE-IN-TRIANGLE (1/a + 1/b ≤ 1), NOT-SELF-SUFFICIENT, TYPE-F-OWN,
  ADJ-REACH, CAP-REDUCTION.  `construct_towards.md` §0, §5; A246.
- [T] **CATALOGUE (PROJECTION)** — a square meets cells of at most one corner neighbourhood N_c (s > 2 + √2); every
  subset realisable below 4; **TWO-FAR** (s > 7/2); **UPPER-END** (no 12-stuck 11-packing at s ≥ 4 + √2).
  `perimeter_walk.md` §0; Lean axioms `two_far`, `upper_end_twelve_stuck`; A247.
- [T] **POKE's true form, TOP-2, FLAT-ABOVE**; **TWO-POKERS** — two wall-touching type-F pokers on one wall need
  s ≥ s* = 2 + min_θ[tan(45° − θ/2) + tan(θ/2) + sec θ] = 3.9342370 > ŝ (minimum [T-computed], 146 403 boxes).
  `corner_chase.md` §0, §3.2; Lean `two_pokers_window` (theorem), axioms `top_two`, `flat_above`, `two_pokers`
  [T-prose]; A248.
- [T] **T-CELLS, T-TIP, T-SLOTS; FAMILY-STUCK per corner and per wall** (8 outside incidences; ADJ supply ≤ 1 per slot).
  `type_t_chase.md` §0, §1, §3; Lean axioms `t_cells`, `t_cells_floor`, `t_tip` [T-prose]; A249.
- [T] **Lemma STACK** (mutual wall pair ordered, clearance < 4 − s, stack height ≥ 2) and **WALL-CLICK** (under
  H-ROOM).  `snap_down.md` §1–2; Lean `lemma_STACK` (axiom [T in prose]); A245.
- [T] **SAME-WALL, BLOCKER-SIDE, STRIP-LANDING** — ≤ 1 toucher per wall at a doubly-met box, every further meeter
  floats.  `box_meeters.md` §0, §1; Lean `same_wall_core`, `blocker_side_core`, `strip_landing_core` (theorems),
  `meeters_split` (axiom [T-prose]); A261.
- [T] **Corner closed forms** of the normal ring: (D4), E_A, E_B exact signed separations; the B-type's other axis
  never separates when a < 1.  `family258.md` §2; A258.  **ROW-THREE** and **ALT-SIDE** need side > 4 at common tilt
  (Lean `row_three_poly`, `alt_side_poly`), `normal_ring.md` §3.2–3.3; A258.

### 2.5 Window exclusions (which pinwheels of rows exist below ŝ)

- [T] **NEAR-FLAT CUBE** — at a mixed (+,−) corner with tilts ≤ ε₀ = 0.703° BOTH offsets exceed 1 − λ, λ = ε₀/2 +
  ε₀²/2; at (−,+) one offset exceeds 1 − μ; at (+,+) the END offset exceeds 1 − ε₀²/2 − a tan ε₀; with a_w + b_w ≤ s − 2
  the patterns + + + −, + − + − are infeasible for s < 3.9813 and + + − − for s < 3.9814 (margin 0.104–0.106 at ŝ).
  `three_lemmas.md` §0 Lemma 3, §3; Lean `cube_pppm`, `cube_pmpm`, `cube_ppmm`, `slab_cube_264` (theorems) over the
  axioms `mixed_corner_pm`, `mixed_corner_mp`, `pinwheel_corner_pp` [T-prose]; A264.  (Replaces A263's axiom
  `slab_cube` for rings of pairs; `slab_cube` is still declared in `OpenPairs.lean` per AUDIT — s.5.4.)
- [T] **ROW-THREE / ALT-SIDE at common tilt** need side > 4 (§2.4).  `normal_ring.md` §3.2–3.3; A258.
- [T] **TWO-POKERS on the window** — no wall carries two type-F pokers on [3.82, ŝ] (Lean `two_pokers_window`); with
  [M] SEPARATE-NOTCHES: no 12-stuck 11-packing on the window has four type-F corners [T given M].  `corner_chase.md` §0;
  A248.
- [T] **FAMILY-STUCK dead at s ≥ 4** (§2.1) and **UPPER-END** (12-stuck dead at s ≥ 4 + √2) (§2.4).
- (Certified parts of the window exclusions — A261's LP certificates, A263's slab jobs — are in s.3; the measured
  least sides of the other pinwheels are in s.4.)

### 2.6 Force and torque facts (A217–A240) — which are theorems, which were superseded

None of these is in the current chain (s.8): the chain is load-free (A222 onward, `ring_swap.md` §1.8: "Loads are never
used … rattler crowds are covered").  They stand as theorems about FJ points and as the reasons the load routes died.
- [T] **PUSH, HOLD** (A218, §2.4).  [T, vacuous] **K0-COUNT** (A218, §2.2) — its hypotheses LOAD, DISTINCT are [F] (s.5).
- [T] **CEIL, TWO-CONTACT** (a loaded tilted wall square, tilt ∉ {0°, 45°, 90°}, needs ≥ 2 further loaded contacts;
  Lean `two_contact_core` axiom), **ONE-TILTED**.  [T] **STRUT** (a two-force member's rotation about one contact is a
  first-order zero mode) and **Theorem SO** (second-order necessary condition, selection form: v₂ < 0 ⟹ not a
  σ-minimiser).  `wall_torque.md` §1–3, §5; A219.
- [T] **Lemma W** (a wall torques a square toward its own alignment: τ = W(sin θ − cos θ)/2), **TORQUE-ID** (circulation
  term), **CORNER-LOAD** (frame handedness decides floor- vs wall-loaded corner), **EXTENT**, **LEAN-SLIDE**.
  `two_grains.md` §1.2–1.4, §2.2, §2.5; A223 (Lemma W is A217 §2).
- [T] **WALL-EXCESS** — touchers' chords 1/max(cos θ_i, sin θ_i) ≥ 1 on the line at 1/√2 are disjoint, Σ ≤ s, excess
  zero only flush; sealed pocket area tan(min(φ, 90° − φ))/2 at common tilt.  `realign.md` §1; Lean
  `lemma_WALL_EXCESS` (axiom [T]), `chordT_ge_one`, `wall_count_le`; A231.
- [T] **LOCALITY** (the lock is decided inside the arm [0, 1 + 2√2]²), **RADIAL** / Corollary **CHAIN** (a loaded arm
  is held by a net corner-ward push from outside; the loaded component reaches a far wall), **NO-SELF-STRESS** (λ₀ = 1).
  `local_lock.md` §0, §2–3; A233.  **Superseded:** A219's [M] RING ("no loaded four-crowd balances by walls and meeters
  alone", 193/193) — A233: "A219's RING measured on 193, now a one-line theorem for all n" (CHAIN).  Neither excludes
  anything: Trump's TL crowd satisfies CHAIN.
- [T] **TORQUE-ID in three forms** (G) global, (W) no per-wall identity, (K) per corner = RADIAL's rotational twin
  (Lemma ARM-MOMENT).  `handedness.md` §0; A234.
- [T] **NO-VV-IND** — a vertex-on-vertex row outside the span of the other active rows carries no load (the feasible
  set near a VV contact is a union, a reflex corner); **CONCURRENT**, **KNIFE**.  `no_vv.md` §0; Lean
  `no_vv_of_not_mem_span`, `no_vv_pair` (theorems); A235.
- [T] **PARTNER-TORQUE** (contact torques read the tilt difference and the contact position, never handedness);
  **chains (iii)** = CHAIN; **CROSS-PLANAR** (a left-right and a floor-ceiling chain share a square or touch).
  `cross.md` §0; Lean `crossing_lemma` (axiom, classical), `chains_meet`, `chains_share_or_touch` (theorems); A240.
- [T] **K0-ROT** (A85, §2.1) — Trump's rotation profile is V-shaped, D⁺σ = D⁻σ = 3.877 [M] (`k0_route.md` §5.2).
- **What superseded the force line as a whole:** A222's CELLS / RAISE (load-free; covers rattler crowds, which are 61
  of 70 doubly-met corners at A217's genuine k0 FJ points, `k0_count.md` §5), then A250's FAMILY-STUCK and A258's
  NORMAL-FORM.  The drain reading (A217/A218: "a forced four-crowd wants to SETTLE a corner") survives only as
  motivation (`k0_count.md` §0).

## 3. CERTIFIED facts [T-computed] — status read from the index files on 2026-09-23

Every certificate below follows the pattern of s.10 (box tree + own independent verifier, bisect-on-disagreement,
tiling check).  "ok" = the tree's cell verdict; "verified" = the independent verifier's `bad = 0`.
- [T-computed] **A259 NORMAL-ROOM corner-PAIR tree** (10a) — domain D′, s ∈ [3.82, 3.8771]: `attempts/A259-normal-room/
  certs/pair259_index.jsonl` 81/81 ok; verifier `verify259.py` rerun (bisected re-certification of 9 independent-cover
  failures, which were the verifier's ψ = 0 bin, `results/verify259.md`): `results/verify259.json` leaves CERT 78 099,
  PRUNE 3 066, LAYER 5 184, OPEN 0, **bad 0** (commit 8512d81d1, 2026-09-22).  **COMPLETE** (the chain's "index
  filling / verify259 rerun alive" is older than this commit).
- [T-computed] **A260 LAYER + hybrid corner-PAIR trees** (10a layer, 10b) — `attempts/A260-locked-wall/certs/`
  layer260 / hybA260 / hybB260 / hybAB260 indices each **81/81 ok**; `results/verify260.json`: layer 93 CERT, hybA 9 375
  CERT + 13 309 PRUNE, hybB 28 648 + 32 521, hybAB 58 903 + 83 162, OPEN 0 everywhere, **bad 0**.  **COMPLETE** for the
  all-ADJ common-tilt hybrid family, e ∈ (0, ½] (`locked_wall.md` §3.3).  (The chain's "8/81 at A260's exit" is older.)
- [T-computed] **A261 window-exclusion LP certificates** (8a: rows of three, exactly flat walls, mixed senses at tilts
  ≥ 0.703°) — `attempts/A261-box-meeters/results/cert261.jsonl`: **50/50 jobs done and verified**, feasible 0,
  undecided 0 on every job (the chain's "11/50 verified at A261's exit" is older).  Method `box_meeters.md` §3.
- [T-computed\*] **A263 factor certificates** (10c) — `attempts/A263-open-pairs/certs/P2263_index.jsonl`: 70 of 81
  cells indexed, **50 ok, 20 not ok** (cells 2,4 2,5 3,4 3,5 3,6 4,4 4,5 4,6 4,7 5,4 5,5 5,6 5,7 6,4 6,5 6,6 6,7 6,8 7,5
  7,6; e.g. 7,6: FAIL 301 757 / CERT 20 307 leaves after 14 838 s); WE263 1/1 ok; WS263 3/3 ok.  No A263 verifier
  output is on disk.  A265 [T] diagnosed the first five failing cells as a SIDE mismatch (s.5); its re-run lane
  `attempts/A265-strip-plug/certs/P2265_index.jsonl`: 2,4 / 2,5 / 3,4 **ok**, 3,5 / 3,6 **not ok**; `results/
  verify265.json` bad 0 with OPEN leaves 3 837 (3,5) and 911 (3,6).  Of the fifteen later failing cells, 4,4 is named
  open in `k0_route.md` §13's closing paragraph; 4,5 … 7,6 appear in no source text yet (index only).
- [T-computed\*] **A262 `pair3` and the `jam` kernel** (5a, 5b) — `chain3.sh` ran `float262` (twice, after a fork
  retry, `attempts/A262-no-jam/logs/chain3.log`, last write 2026-09-23 11:59); **no `pair3` index exists** (the
  `certs/` directory is empty).  `pair3` is priced ≈ 3 CPU-h, the 7-parameter `jam` kernel 15 (median) – 500 (mean)
  CPU-h (`no_jam.md` §0).  Not landed.
- [T-computed\*] **A266 `strip266`** (5b off the ring domain; LEFT-SHADOW box tree, own verifier `verify266`) — budgeted
  lane `jam`: `attempts/A266-last-two/certs/strip266_jam_index.jsonl` 6/6 cells **not ok** (≈ 75 000 leaves each, the
  budget); `results/verify266_jam.json` bad 0, leaves CERT 110 070, PRUNE 91 356, **OPEN 248 622**.  Full tree priced
  ~5·10³ CPU-h (`last_two.md` §0) — see s.7.
- [T-computed\*] **A273 DROP-LEMMA tree** (5b, 4-parameter, box-valid penumbra test, independent `verify273`) —
  `attempts/A273-disc-lemma/certs/index273.jsonl`: 42 of 81 (θ, φ) cells indexed (θ-bins 1–5, i.e. θ ∈ [5°, 30°]);
  **40 CERT, all verified PASS** (`results/verify273_index.jsonl`); **c5_4 (θ 25–30°, φ 20–25°) and c5_5 (θ 25–30°,
  φ 25–30°) hit the 400 000-box cap: OPEN-LAYER with 127 845 / 154 644 OPEN leaves** ("PASS with … OPEN leaves: not
  certified").  θ-bins 6–8 and 0 not yet run; the corner θ ≤ 5° ∧ φ ≤ 5° is OPEN by design (s.6).  disc273 §4
  expected only the corner-adjacent cells c1_0 / c0_1 to be expensive — the capped cells are elsewhere (s.5.4).
- [T-computed] **A265 `strip265`** — no unit square interior-disjoint from C and X has an interior point in the strip
  (worst −9 = no such square, both sectors) on the JAM rings tested: `attempts/A265-strip-plug/results/strip265.json`
  n = 432 (the doc says 18 at exit, 323 in the lane).  A statement about the tested rings only.
- [T-computed] **A264 `cube264`** — the corner-lemma constants at 60 digits; 0 violations on 20 000 random near-flat
  corners against exact SAT.  `three_lemmas.md` §0.
- [T-computed] **TWO-POKERS minimum** ≥ 1.934236 over the whole triangle by 146 403 monotone-enclosure boxes
  (`twopokers248`).  `corner_chase.md` §0; A248.
- [T-computed] **SLOT-MET(η)** — for meetings of depth ≥ η, by interval branch-and-bound, η = 0.05 … 10⁻⁷ (191 525 –
  649 243 boxes, guard 10⁻⁹, `attempts/A246-construct-towards/results/slotmet246_*.json`); the depth-free limit stays
  [S].  `construct_towards.md` §0; A246.
- [T-computed] **A247 pair table** — of 851 pair problems (level (0.05, 0.07), window [3.82, ŝ]) the branch-and-bound
  decided 759 (697 feasible with exact witnesses, 62 infeasible), 92 undecided (η-degenerate); the walk counts
  66 112 676 788 → 13 453 179 721 labelled walks after the 62 kills.  `perimeter_walk.md` §0; A247.
- [T-computed] **A250 ILP count** — below 4 the exact minimum number of squares of a family-stuck incidence structure
  is **9** (13 at s ≥ 4), unchanged by SLOT-MET and the 62 pair kills; the corpus: 0 of A244's 488 twelve-stuck and 0
  of A217's 486 witnesses are even PAIR-stuck.  `family250.md` §0, §2.2, §4; `count250.py`; A250.
- [T-computed] **The all-ADJ type-T ring exists at ŝ** (exact rational witness, C2 pinwheel at tilt 14.6°, margin 0.037,
  `attempts/A249-type-t-chase/results/twotilted249_ring2.json`, `test249.test_ring_exact`) and its pocket has capacity
  ≤ 1 (PIERCE(1) residual 0).  `type_t_chase.md` §0; Lean `two_tilted_ring_exists` (axiom [T-computed]); A249.
- [T-computed] **Pocket certificates at explicit rings** — A226's rings at 3.90 and the window family ring(S, θ ≤ 30°)
  hold ONE square (PIERCE(1), `pocket_waste.md` §0, A237); A249's ŝ witness survives a core shrink ε* = 0.0952 for
  PIERCE(1) and 0.1397 for PIERCE(2) (`ring_pocket.md` §0, A251); poker margin +0.00166 at A249's ring and residual
  centre set EMPTY beside it (`centre_disc.md` §0, A252); the flush-limit pocket decomposition in rational arithmetic
  at six sides (`mintilt253.md` §0, §5, A253).
- [T-computed] **CELLS/meeting census on the corpus** — `cells254` enumerates all 15 / 1 295 / 65 535 / 3 111 695
  admissible families at m = 3..6 (`peel.md` §1.2, A254); A250 conflict graph (`fam250.conflicts`, `test250`).
- [T-computed] **Older k0 certificates**: Theorem A38.1 (root occupancy at s0, `root_s0.json`); the first certified
  k0_00 interior kill `certs/k0_00/s1int_l2_l2_p114_010` (A85); A92's Theorem S(0.3) (`certs/runA_S_d0.3_e1_v2.json` +
  `runB_…`, frozen `verify_case.py` PASS — no K0-BLOCKED packing on [3.82, s0) has every second intruder at depth
  ≥ 0.3; `k0_blocked_side.md` §0); A115's 22 level-1 + 13 level-2 + 2 level-3 + 10 A85/A99 cells certified dead for
  29.8 CPU-h (`residue_ledger.md` §4); A86's atlas + 12 ghost-drain boxes replayed in Lean (`AtlasCheck.lean`, 48/49
  with L ≥ s0; `k0_route.md` §12).

## 4. MEASURED facts [M] the chain leans on (not proved)

- [M] **No k0 local optimum below ŝ**: 262 k0 optima from 516 targeted runs, best at s0 + 0.0101 (four axis-aligned
  squares off their slots by 1.6·10⁻³–8.6·10⁻³), first with no axis-aligned square at s0 + 0.0286.  `k0_route.md`
  §4.5–4.6, §10; `attempts/A85-k0-route/results/cp85_k0_search.json`; A85.
- [M] **No four-crowd / 12-stuck / family-stuck packing below 4 was ever found**: A217 lowest four-crowd local optimum
  4.0013–4.0014 (`ring_swap.md` §2.3, `two_grains.md` §0); A244: 482 verified 12-stuck packings from 4.000010 to 4.5,
  none below 4 in 434 descents + 4 056 fixed-side restarts, none LOCKED; the 4-stuck control 4.000015
  (`attempts/A244-twelve-stuck/notes/twelve244.md` §0); A250's family search: none on [3.82, 4.6], least side where even
  the |Π| ≤ 3 rows are met ≈ 4.0017 (`family250.md` §3).  Evidence, not proof (A244 §2 says how strong).
- [M] **Normal-form reading on the corpus rings** (46 rings): poker removed, W → T on 4/4 walls in 46/46 and 46/46 land
  in D; poker kept, the poker's wall is LOCKED on 43/44 (lock shift 0.0005 … 0.13).  `normal_ring.md` §0, §3.5; A258.
- [M] **Least sides of the other pinwheels of rows** (`side258`, exact LP per tilt vector, grid 11⁴ + polish): mixed
  + + + − 3.9298 (per-wall tilts; not all-ADJ), + − + − 3.9484, + + − − 3.9767, a flat row 3.9347, a flat row of three
  3.9814, row of three with tilts ≥ 3° 4.0126; ≥ two rows of three > 4.  Margin 0.053 in the side at ŝ.
  `normal_ring.md` §0, §3.2–3.4; A258.  (8e of the chain.)
- [M] **Ring-level COMMON-SENSE on [3.82, ŝ]**: 0 of 84 mixed-sense all-ADJ ring rows (42 orbits × {3.99, ŝ}) close
  (best −0.0140).  `common_sense.md` §0; A255.  With per-wall tilts it fails above 3.9298 (s.5).
- [M] **ROOM on the families beyond the certified parts**: ROTATED-HOLE sharp form, sup miss-margin → −(4 − s)/2 from
  below (24 adversary runs, 5 241 + 6 177 random pairs; MONOTONE-ROOM "true in normal form") (`normal_room.md` §0,
  A259); hybrid family with independent tilts sup −0.0654 at ŝ, corpus 46/46 (`locked_wall.md` §0, A260); factors
  sound on 82 test rings × 4 corners, every factor < 0 (max −0.0654 / −0.0051) (`open_pairs.md` §0, A263); GAP-DEPTH-ONE
  quadrant form 2 046 pairs, least 1.0027 (`locked_wall.md` §0).
- [M] **JAM rings exist on the whole window** (`ring262`, `adv262`: 8 squares, exact check, margin 0.0104 at ŝ, 0.0099
  at 3.82; 34 rings) and **ROOM ≤ 1 on them**: every free square contains O, pierce margin ≤ −0.070 at ŝ, ≤ −0.105 at
  3.82, adversary ≤ −0.085 / −0.133; capacity exactly 1; ring + its one free square never family-stuck.  `no_jam.md` §0;
  A262.  j = 2 OPPOSITE: a ring exists (t = +0.0016 at ŝ), room 0.  j = 2 ADJACENT: rings EXIST (t = 0.0071 at ŝ,
  0.0010 at 3.82), capacity 1 (A264, correcting A262 — s.5).  j = 3, 4: rings only at 3.95 / 3.99, room 0, none on the
  window.  `three_lemmas.md` §0 Lemma 1; A264.
- [M] **Adversary / search** (5e): 399 structured starts, capacity ≤ 1 always, no 11-witness (`search262`; the file has
  552 rows today).  `k0_route.md` §13 5e; `three_lemmas.md` §4.5.
- [M] **HELD-JAM does not exclude the JAM ring**: the bare ring never blocks C's retreat (35/35), a single free square G
  blocks every retreat direction in 31/35.  `no_jam.md` §0; A262.
- [M] **The FLOAT2 witness (5d)**: `attempts/A262-no-jam/results/float262.json` (chain3 output, 2026-09-23 11:59):
  verdict "JAMMED FLOAT2 EXISTS", sup_t = +0.00224 over 108 starts; poses (x, y, tilt rad) C (0.7307, 1.5955, 0.2525),
  D (0.9503, 0.6035, 0.2246), A (1.9911, 0.6090, 0.2522), X (0.6549, 2.6825, 0.3988) in the file; drawn in
  `docs/residue_map/current/k0_stuck_2026-09-23.svg` panel (b); now cited in `k0_route.md` §13 5d.  The corpus census below 4 had
  1 FLOAT2 corner, a rattler with a free straight drop (`cp85_032`, s = 3.9240) (`box_meeters.md` §0).  No room
  statement for FLOAT2 exists (chain 5d stays [C]).
- [M] **Middle toucher (span262)**: `results/span262.json` sup_t −0.0327 at cap ŝ (72 starts) — no JAM ring with X a
  middle toucher under a START square found there.  (Reported as "pending" in `no_jam.md` §1; the file is 2026-09-21.)
- [M] **STRIP₂ on the true domain** (tilted C): 60/60 in-domain samples certify under the box test at radius 0.0025,
  exact pocket empty (`last_two.md` §0, A266).  On A271's violators of (U3)–(U6): sup t = 0.00000, approached only as
  C's box depth → 0 (`ring_domain.md` §0).  (U8) positive under H1–H3, adversary minimum +0.094 (ibid.).  The residual
  R = H1–H3 ∖ ring inequalities is ~18 % of the H1–H3 set (`mc271`, 20 000 samples).
- [M] **STRIP₂'s own margin near the flat corner** — A273: square slack −0.0049 (8°), −0.0027 (5.9°), −0.0012 (4°),
  −0.0003 (2°), −0.00008 (1°), "roughly 0.15 θ² rad" (`disc273.md` §5).  A274 (later, same day): first order ≈ 0.5 θ on
  the diagonal θ = φ, second order ≈ 0.25 θ² on the edge φ = 0 (X flat) — "A273's roughly 0.15 θ² is 0.25 θ²"
  (`attempts/A274-flat-corner/results/r1_274.md`).  The two are recorded in s.5.4.
- [M] **CAPACITY-2**: no two interior-disjoint misses on any ring tried — A260's 32 non-ADJ adversary rings have an
  EMPTY miss region (`cap266`); A265's FULL-corner witness is not a ring (overlap 0.007).  `last_two.md` §0; A266.
- [M] **SEPARATE-NOTCHES** — no free square serves two adjacent notches (sup margin −0.003 at ŝ, −0.006 at 3.82).
  `corner_chase.md` §0; A248.
- [M] **MIN-TILT** — the joint ring + poker margin M(τ, s) > 0 for every τ tested down to 0.1° (5.7·10⁻⁸ at ŝ); the
  pocket capacity is CONSTANT 1 along the tilt ladder τ = 26° … 6° at ŝ (PIERCE(1) + region search); θ_max(s) ∈
  (26°, 30°) at ŝ.  `mintilt253.md` §0, §5; A253.
- [M] **ONE-FLUSH survey** — 21 record packings (n = 5 … 55, re-verified by exact SAT): every one below ⌈√n⌉ has ≥ 3
  flush corners, 20 have four; Trump is the only one with a doubly-met corner (TR).  `one_flush.md` §0; A226.
- [M] **RAISE on the witnesses** — holds on all 4 534 A217 witnesses at their own sides; below 4 every witness has a
  corner met by ≤ 1.  **SWAP-RIGIDITY** of Trump for |Y| ≤ 3: no different re-packing found (201 subsets).
  `ring_swap.md` §0, §1.7; ledger §4 A222 note; A222.
- [M] **Corpus corner census below 4** (3 242 doubly-met corners): 29 PAIR (+ 56 on the rings), 2 FLOAT1, 1 FLOAT2, all
  three rattlers within 4·10⁻³ of a wall; no third meeter, no same-wall toucher pair.  `box_meeters.md` §0; A261.
- [M] **Sense on the corpus** — toucher-sense violations are common and every one reduces by Lemma CELLS at scope ≤ L2;
  on the rings every in-container normal cell is met by exactly ONE square, the next toucher (112/112).
  `common_sense.md` §0; A255.
- [M] **Mechanism measurements of the dead load routes** (not leaned on by the chain; for the record): RING 193/193
  (A219), click to 4.000 on 193/193 four-crowds (A223), anchored re-alignment strict on 783/792 (A231), CHAIN 1 013/1 013
  (A233), handedness ranges overlap (A234), VV unloadable at every optimum (A235 + addendum), locked same-handed 215 : 11
  (A240).  Sources: s.2.6.

## 5. FALSE statements [F] — what was claimed, the witness, and why it failed

This section is what stops agents repeating them.  Grouped by theme; each: the claim (who made it) — the witness
(file / page) — why.

### 5.1 Counting and capacity claims

- [F] **"Four doubly-met open corners need 8 meeters + ≥ 4 along-wall holders = 12 > 11"** (A217's count; the brief's
  G2 "a holder serves at most two meeters").  Witness: `rand_0_0569|t20` (side 4.1099), a FORCE-BALANCED four-crowd
  with NINE squares — a compression ring through the eight meeters with one link (page
  `count218_held_rand_0_0569_t20.svg`); the true sharing bound is FOUR (a 45° centre square touching four 45° corner
  meeters); LOAD fails on 61 of 70 doubly-met corners at genuine k0 FJ points (rattler crowds).  `k0_count.md` §0, §4–5;
  A218.
- [F] **"The perimeter sweep count closes"** (PI, A222: each exposed cell needs a SECOND meeter; "k0 and k1 trivially
  empty if the count holds").  An exposed cell needs ONE remaining meeter (a teleport); over 8 cells the sweep needs
  Σ|M_k| ≤ 8 while ≥ 9 squares meet them when every corner is doubly met; counting closes only for n ≤ 4.
  `ring_swap.md` §0, §1.4; A222.
- [F] **"Records are rings" / Lemma BAND as a structure statement** — every record n = 5..55 is cross-braced (Trump has
  5 straddlers of depth up to 0.94); on 193 witnesses the loaded component contains a core square in 67.
  `ring_capacity.md` §0; A236.  The band-plus-core count excludes a four-crowd for NO n (NO-CLOSURE).
- [F] **The composition of A246's rules forces s ≥ 4** — the rules bound COUNTS, satisfiable with f = 3 at every side;
  a wall with two flat meeters at offsets δ, δ′ > s − 3 is a packing for s < 4.  `construct_towards.md` §0, §3; A246.
- [F] **The family-stuck count closes the window** — the ILP minimum below 4 is 9 ≤ 11 under every proved layer.
  `family250.md` §0, §2.2; A250.  (Also [F] "the count alone" for type-T rings: `type_t_chase.md` §0 (A249).)
- [F] **"> 3 free squares in the gap"** (A264 brief) and **"two squares in the notch need width ≥ 2 > e"** (A266
  brief) — the derived count is TWO (a square meeting a floor cell can contain O: [1.44, 2.44] × [0.95, 1.95] at ŝ),
  and two near-flat squares STACK in a gap of width 1.17.  `three_lemmas.md` §0 Lemma 2 (d); `strip_plug.md` §0;
  `last_two.md` §0; A264/A265/A266.
- [F] **"8 + j" and "j ≥ 2 needs room 0"** (A262 brief) — X IS the next box's meeter, so the outer structure has 8
  squares for j = 1 and j = 2; room ≤ 1 already gives n ≤ 9.  `no_jam.md` §0; A262.

### 5.2 Local, corner and force claims

- [F] **"A 2-crowd is a mixed-sign V or contains an axis-aligned blocker"** (PI/advisor prune, A85).  Witness: the
  floating same-sense pair A (tilt 40°, lowest vertex (0.643, 0.7)) / B (tilt 30°), SAT gap 0.044; 32 % of the 33 656
  surviving pair boxes are same-sense.  `k0_route.md` §4.4 (b); A85.  Why: the pair space has interior.
- [F] **SIDEBAND "within 1 of a wall" at the widened box** — two 45° diamonds at (1.01, 1.7226) / (1.7226, 1.01), gap
  0.00777; **SIDEBAND (b) "the other centre lies outside that band"** — Q1 = [0.1, 1.1] × [0, 1], Q2 at 2.866°.  The
  true forms are the sharp constant c and A2's distinct cells.  `sideband.md` §0; A169.
- [F] **L2 "squares cannot load along a wall without a net torque"** — flat squares compress edge-to-edge along a wall
  with zero torque (the simple packing's rows); 45° diamonds pinched between a wall and a flat square.  The content is
  TWO-CONTACT.  `wall_torque.md` §0, §2; A219.
- [F] **"The chain formula decreases toward alignment"** — the corner-anchored ladder Λ(θ) = 2 + 4t/(t² + 1) is MINIMAL
  at 45° and rises to 4 at alignment.  **TWO-GRAIN as geometry** — 12/193 four-crowds have ONE grain meeting all four
  corners; `w062_crowd` has all eleven squares '+' (crowd-held).  **TORQUE-ID as an obstruction by itself** — nothing
  bounds the circulation.  `two_grains.md` §0, §1.3, §2.3; A223.
- [F] **"No non-trivial optimal packing has four flush corners"** (PI) — n = 5 and 10 are PROVED optimal with four;
  18 later records too.  **STUCK(n) for all packings / Theorem PERIMETER** — Proposition CROWD-ABOVE builds four
  doubly-met corners at EVERY side > s(n) from a record with corner dominoes (verified n = 26, 28, 29, 37, 40, 50, 51,
  55; page `crowd_above.svg`); a doubly-met corner costs O(ε).  `one_flush.md` §0; A226.
- [F] **"Each non-flush corner corresponds to a grain we can drain"** — the swap CONSUMES the meeters.  **The area
  horn** — all-diamond sealed walls waste 2⌊s/√2⌋ − 1 = 3 < s(11)² − 11 = 4.03.  `realign.md` §0; A231.  Also "kink-side
  ⟹ tilts near 45°" (ledger §4 A231 note).
- [F] **"At a k-maximal minimiser below ⌈√n⌉ no corner box is doubly met by locked meeters"** (A233 brief) — Trump's TL
  corner is doubly met (nick sq4, 40.18° carrier sq6), both LOCKED, and Trump is k-maximal.  `local_lock.md` §0; A233.
- [F] **"A handedness count separates a four-crowd from an optimum"** — every candidate scalar's range on the 193
  four-crowds overlaps its range on the 883 free FJ points and the optima (`hand234.md`).  `handedness.md` §0; A234.
- [F] **NO-VV as a consequence of local optimality in general** — at stuck configurations the VV row is in the span of
  the others (82/82); 25/26 HELD witnesses with a loaded tilted VV are FJ under every consistent selection.
  `no_vv.md` §0; A235.  (Coordinator addendum 2026-09-15: with COMPOSITE edges the records' 12 contacts are not genuine
  VV; "s.5's 'false' refers to the naive classification only" — `no_vv.md` addendum.)
- [F] **Lemma OPPOSE** ("corner jams require opposing torques") — locked corners same-handed 215 : 11 (free FJ points
  44 : 1).  **Alternation of wall grains** — 0/193.  **"The shared square is obstructed"** — 90 tilted interior crossing
  squares carry both chains unloaded; Trump crosses at a flush square.  `cross.md` §0; A240.
- [F] **TILT-MIN as a lower bound θ ≥ θ_min for locked corners** (a tilt floor) — A89: no loaded tilt floor by any local
  argument; the HELD witnesses sit at their generator's floor.  **"A unit square cannot approach a tilted edge closer
  than a tilt-dependent margin"** — a square parallel to the edge approaches at distance 0.  `pocket_waste.md` §0; A237.
- [F] **The PI's STACK dichotomy** (contact forced; a handedness pairing forced) — two flat squares [0,1]×[0.9,1.9],
  [0,1]×[1.95,2.95] are a mutual pair at 3.82 with a gap 0.05; floating pairs 2 235 / 4 000.  **"The packing after the
  click is at no larger side"** — the global click raises the side on 7/115 and 102/550 (max 0.049).  `snap_down.md` §0;
  A245.
- [F] **POKE's directional claim** (the poker's tilt sense is forced) — exact witness beside A = [19/20, 39/20] × [0,1]:
  cos θ = 3/5, lowest vertex (4/5, 9/10), CW sense; 7 of 288 corpus type-F views are CW.  **Pinning forces an interior
  square** — not in the exchange form.  `corner_chase.md` §0, §1.1, §2.2; A248.
- [F] **TWO-TILTED as a window bound** — the mutual type-T wall problem has sup SAT margin +0.078 at 3.82: s_T* < 3.82;
  the all-ADJ type-T ring EXISTS at ŝ.  `type_t_chase.md` §0, §2; A249.
- [F] **CENTRE-DISC about the container centre** (A251 §3.5's "one inequality", A252 brief) — Lemma MOUTH: the mouth
  disc's distance from O tends to (s/2 − 3/2)√2 > 1/√3 iff s > 3 + 2/√6 = 3.81650 (the whole window); far_O = 0.628
  at 3.99 on feasible rings.  **Every INRADIUS-only criterion in the flat-flat limit** — a corner notch holds the disc
  of radius ½ at (½, ½) but no unit square (page `notch_disc.svg`).  The brief's premise (inscribed disc small) — it
  has radius 0.771 at ŝ.  `centre_disc.md` §0; A252.  (Consequence: A251's axiom `centre_disc_ring` was REMOVED.)
- [F] **A positive minimum tilt θ_min(s)** (PI, A253) — θ_min(s) = 0 on the whole window; the limit is the four-corner
  domino pinwheel.  `mintilt253.md` §0, §2; A253.
- [F] **"The flush limit of the general ring is the pinwheel" for m ≥ 5** — the flush stratum keeps wall slack; also
  "equality at n = 65" (the only equality n ≤ 100 is n = 84).  `peel.md` §0, §6; A254.
- [F] **COMMON-SENSE as a LOCAL lemma** — the local counter-hypothesis is realised in 19 of 20 pair types (margins
  0.006 … 0.046, `local_witnesses.svg`), s-free; **the PI's claim (c)** (a square above s₁ at its tilt poking down past
  it is never a second meeter) — `rand_0_0441|free`, s = 3.9352, depth 0.265.  `common_sense.md` §0; A255.
- [F] **"Every normal-form family-stuck packing is the pinwheel of four pairs"** — the normal form is the HYBRID ring
  (43/44 corpus walls locked by the poker).  **`common_sense.md` §2.3's simultaneous row-normality** — rows (3,1) →
  (2,2) → (3,1) cycle.  **"Mixed-sense pinwheel of pairs cannot close"** — with PER-WALL tilts + + + − exists from
  s = 3.9298 (tilts 14.02°, 14.02°, 14.02° | 10.94°; `excluded.svg` (d)): a drawn counterexample to ring-level
  COMMON-SENSE on the stretch (ŝ, 4), not on [3.82, ŝ].  `normal_ring.md` §0, §1.2, §3.3, §6; A258.
- [F] **NORMAL-ROOM without (D2)** — drop "every row end meets its corner box" and a free square missing O exists at
  every side (+0.17 at ŝ), two disjoint ones at 3.95 / 3.99 (`capacity259.json`, `worst_case.svg`).  `normal_room.md`
  §0; A259.
- [F] **"A straight slide lands a floater / what blocks it is a lower box meeter"** — witness LIFT (a row END pushed 0.41
  off its wall, both straight drops blocked, lands by STRIP-LANDING).  **TOUCH-NORMAL from P1 inside the corner** —
  witness JAM, the JAMMED FLOATER (every wall-touching cell meeting C overlaps A or X by ≥ 0.0090).  **"A slab of
  near-flat tilts is excluded"** (A261's own, caught by its engine) — D′ reaches 0.7°–1.4° on one wall at ŝ.
  `box_meeters.md` §0; A261.

### 5.3 The strip / disc sequence and the certificate readings (A263–A274)

- [F] **P2 without the principal normal** — a 44° square hugging the right wall where the dropped W′ stood misses O "to
  the floor" by +0.03 (`fact263_rows_v0.jsonl`).  **ROOM ≤ 1 as a bare-ring statement on non-ADJ wide gaps** — for
  e ≳ 1 + w(φ₁) − sec φ₁ a unit cell touching the wall fits in the gap (drawn).  **"3.9347 − Cφ"** — wrong limit: the
  near-flat mixed ring tends to the domino pinwheel at ANY side.  `open_pairs.md` §0, §5.4, §7; A263.
- [F] **The reading of A263's OPEN P2 leaves as a corner layer "b ≥ 0.98"** — they sit at b ∈ [0.88, 1] and the failing
  square is on the centre line, 0.7 from the right wall; a REAL P2 miss at 3.8771, where those boxes are not all-ADJ
  (a′ + w(φ₁′) = 1.822 < s − 2): a SIDE-MISMATCH artefact (ADJ imposed at 3.82, evaluated at 3.8771).
  `strip_plug.md` §0; A265.
- [F] **STRIP₂ as A265 stated it for a tilted C** ("0 < h_u, h_v < 1" as "C meets the open box") — h_u = 0.963,
  h_v = 0.848, θ_C = 31.7°, X flat at y_X = 2.81: a FLAT square at (0.599, 0.820) is free of C (+0.084) and X (+0.515)
  and meets int T_u (depth 0.47) (`probe266`, page `strip_tilted.svg`); the flat-C chord proof does not carry (chords
  bounded by C's lower-left edge up to h_u + sin θ_C).  `last_two.md` §0; A266.
- [F] **(U3), (U4), (U5), (U6) as consequences of H1–H5** — `adv271` minima −0.199 (U3: θ = 34.5°, φ = 0°), −0.300
  (U4), −0.243 (U5), −0.184 (U6), all with |φ − θ| ≥ 13° (pages (b)–(d)); they are RING-level facts.
  `ring_domain.md` §0; A271.  And **on the near-flat corner θ, φ ≤ 5°** ("R1 is dead", tagged "[F as consequences]"):
  exact H1–H3 witnesses W1 (U4 = −0.2985, θ = 0.500°, φ = 4.997°) and W2 (U5 = cos φ − 1 = −0.0038, θ = 0); numerically
  U3 −0.0325, U4 −0.7378, U5 −0.0038, U6 −0.00047 on the sub-box; only (U8) holds ([T] via 1.82 − w(θ)).
  `attempts/A274-flat-corner/notes/flat274_part2.md`, `results/r1_274.md`, `results/witness274.json`; A274.
- [F] **The DISC LEMMA** (A272: a point q above L_h at distance ≥ ½ from Ξ and Γ within 1/√2 of the strip is
  impossible) — exact Fraction witness `witness273`: h_u = 17/20, h_v = 199/200, tan(θ/2) = 7/100 (8.01°), X_low =
  211/100, φ = 0, side 387/100, q = (2409/1600, 1294051/500000), p = (99221/100000, 21099/10000); disc slack up to
  +0.0079.  Why: the distance form forgets the CONE — the drop conv(D(q, ½) ∪ {p}) crosses X's corner (overlap 1.1·10⁻³).
  Also [F]: A272's "sup slack −0.005, attained only as h_v → 1" (an optimiser artefact along a flat direction).
  `disc273.md` §0, §7; A273.  (A272's Lean axiom `strip_two_in_jam_of_disc` stands on an opaque `DiscLemma`.)
- [F] **The tilt-split guess** — A272's brief split the violators on |φ − θ|; A272: "the case split is not on
  |φ − θ| … the worst points have X FLAT" (`strip_jam.md` §0 "What the brief had wrong").  A274: the zero-margin
  direction is φ ≪ θ (0.25 θ² at φ = 0), not the diagonal (0.5 θ).  A273's "boundary layer h_v → 1" — not a layer
  (h_v-invariance); the layer is θ, φ → 0 (`disc273.md` §7.2).

- [F] **The FLOAT2 witness as a normal-form object** (`float262.json`, A262; the A277 brief's "A on the floor and X on the wall
  block their drops") — D's floor drop is FREE (h_v(D) = 0.0047; overlap 0 with A, X, C, exact): A is a MIDDLE toucher (leftmost
  x = 1.382) blocking nothing; D drops (Φ₁ + 1) and the corner is a JAM corner inside H1–H3.  "JAMMED FLOAT2 EXISTS" is A261's
  coarse-grid J (the drop cell is off the grid).  A floor toucher Y (77.2°, left vertex under D's right vertex) blocks the drop
  with gaps ≥ 0.00055 and all four drops are then blocked [T-computed], yet P1 lands D on a flat floor cell (J_D = +0.024).
  Also [F]: "S_min = {C, D} + their blockers" (the blockers are pocket squares, not S_min); "the sectors are pair-type
  certificates already run" (independent tilts; two-obstacle ROOM fails by +0.64 on the dropped witness); "the P4 chain reduces
  the indirect jam to the direct one" (the toucher holds the last link, not C).  `float2_room.md` §2, §7; A277.
### 5.4 Pitfalls from other classes, and source disagreements (recorded both ways, later named)

- [F] **"k5 closed at the window pad"** (k5, but a k0 pitfall) — "g1" is A57's G1 SLAB (3.861637, s0], not the window;
  k5_11 / k5_16 are NOT dead on G1 (290 A57 G1 cover boxes never emitted + two s0-only pages), and nothing on G2–G4.
  `attempts/A270-k5-lower-slabs/BRIEF.md` line 3; LOG 2026-09-23 A270; `docs/shadows/STATUS.md` per-slab table.
- [F] **The rowing rule** "row a class C when every one-slot EXTENSION of C is full-window closed" (A241's brief) —
  unsound: Lemma K1 climbs UP containment; a packing with skeleton exactly C carries no fifth simple square.  Closed
  extensions give only SLOT-CROWD (forced cells).  `residue_ledger.md` §3 A241 note; LOG 2026-09-16 A241; A241.
- [F] **Price of the corner seed "25–30 desktop-days"** (A84) — the seed is a 10¹⁶-node cover (`k0_route.md` §8.4).
  **"The corner seed forces the selected form"** (A84) — void (K0-FREE is ∀-packings, `k0_route.md` §3, §9).
- [F] **A87's quantitative drain; (b) exit map; (c) selection compatibility** — void / false as mechanisms
  (`drain_flow_k0.md` §3).  **A92's route-3 object** (an 8-core K-leaf) does not exist (empty core for δ < 0.134).

**Source disagreements** (each recorded both ways; the later source is named):
1. **Chain status lines vs index files.**  `k0_route.md` §13 (A264–A273 edits, 2026-09-22/23): A259 "index filling /
   verify259 rerun alive", A260 hybAB "8/81", A261 "11/50 verified", A263 P2 "41/81, five OPEN".  Index files read
   2026-09-23: A259 81/81 + verified bad 0 (commit 8512d81d1, 2026-09-22); A260 81/81 ×4, bad 0; A261 50/50 verified;
   A263 P2 70/81 indexed, 20 not ok.  The files are later.  (s.3.)
2. **j = 2 adjacent JAM rings.**  A262 (2026-09-22, `no_jam.md` §0): "no ring found (best −0.0078)".  A264 (later, same
   day, `three_lemmas.md` §0 "N6 corrected [F → M]"): they EXIST, t = 0.0071 at ŝ, capacity 1.  A264 is later.
3. **STRIP₂'s margin at the flat corner.**  A273 (`disc273.md` §5): ~0.15 θ².  A274 (later, `r1_274.md`): 0.25 θ² at
   φ = 0 and 0.5 θ on θ = φ; A274 reproduces A273's data points.  A274 is later.
4. **DISC LEMMA.**  A272 (`strip_jam.md` §0): [M] holds, sup slack −0.005.  A273 (later): [F], +0.0079.  A273 is later;
   `strip_jam.md` carries A273's correction banner.
5. **`slab_cube`.**  A264 (`three_lemmas.md` §0): "`slab_cube` is no longer an axiom" (replaced by `slab_cube_264` for
   rings of pairs).  `lean/AUDIT.md` (2026-09-23 18:37, later) still lists `slab_cube` as an axiom (OPEN) declared in
   `OpenPairs.lean`.  Both true at once if the old axiom was left declared; not checked here.
6. **`centre_disc_ring`.**  A251 introduced it as an axiom [T-computed]; A252 (later) refuted its premise and REMOVED
   it (`centre_disc.md` §5); AUDIT has no such entry today.  A252 is later.
7. **Lemma LOW's Lean core.**  A271's first Lean file (commit 31062dbb1, 2026-09-23 15:44) had `lh_gt_one` with the
   hypothesis cos α ≥ 0.7071 only.  A273 (`disc273.md` §7.5, §2.4) flagged it: "worth checking before any other
   certificate leans on it"; A273 does not use LOW.  The A271 follow-up (commit 7cb36df98, 2026-09-23 18:37, later):
   "α is not a frame convention", α ∈ (45°, 90°) is a genuine case (least L_h 1.1405), covered by A's top vertex
   (L_h ≥ 1.121) and `lh_gt_one_steep` + `tangent_core` (L_h > 1, no uniform margin); (D1) [T] survives
   (`RingDomain.lean` header; `ring_domain.md` §0 as it reads today).  Resolved by the later commit.
8. **A273's Lean/AUDIT note.**  `disc273.md` §0: "Lean unchanged (DiscLemma is opaque; its prose content is [F]; AUDIT
   note)".  `lean/AUDIT.md` (2026-09-23 18:37) and `StripJam.lean` contain no A273 note.  Recorded, not fixed here.
9. **A273's price.**  `disc273.md` §4: "all cells but the corner-adjacent ones in seconds to minutes".  Index (later):
   c5_4 / c5_5 (θ 25–30°) capped at 400 000 boxes with OPEN leaves.  The index is later.
10. **Strip prices.**  A265: STRIP tree ≈ 1–3 CPU-h.  A266 (later): ~5·10³ CPU-h ("A265's 1–3 CPU-h was wrong").
   A272: disc-lemma tree ~20 / 10² CPU-h.  A273 (later): hours (for the DROP form).  Later ones stand.
11. **`strip265` ring count.**  `strip_plug.md`: 18 at exit, 323 in the lane.  `strip265.json` today: n = 432.
12. **FLOAT2.**  `no_jam.md` §1 (A262): "[M] `float262` (pending)"; `three_lemmas.md` §4.5 (A264): "not run".
   `float262.json` (2026-09-23 11:59, committed 2026-09-23): "JAMMED FLOAT2 EXISTS", sup_t +0.00224.  The file is later.
13. **SLIDE's d₂ bound.**  A92's sequential proof gives only Σ_{i≥1} d_i ≥ ŝ − m; A94's joint translation gives the
   d₂ bound (`slot_crowds.md` §0, §3.4).  A94 is later.
14. **A85's f₂ and the k0 frontier.**  A85: f₂ = 1/3 at A60 defaults, FAILs are coverage holes.  A99 (later, REGISTRY
   A99): "A85's k0_00 FAILs are LP row-generation failures, so f2 ~ 0".  A115 (later): a plain 240 s warm re-solve
   certified 10 of 55 cells — "the stored node results were simply row-generation-incomplete" (`residue_ledger.md` §4).

## 6. CONJECTURES [C] still in the chain — exactly, and what would close each

Numbered by chain link (s.8).  "Theory" = a hand proof; "certificate" = a box tree + verifier (price where a source
gives one).
- [C] **5a / 5b `pair3`** — the TL sectors of a JAM corner, and the BL sectors with T_u as the END square: a row of two
  + one wall square, 4 parameters.  Certificate: A262's `tree262 pair3` + `verify262`, ≈ 3 CPU-h; chain3 ran `float262`
  and has not produced a `pair3` index.  `no_jam.md` §0; `three_lemmas.md` §0 Lemma 1; `k0_route.md` §13.
- [C] **5b STRIP₂-IN-JAM on the near-flat corner θ_C ≤ 5° ∧ φ_X ≤ 5°** — the DROP LEMMA's margin → 0 there (zero at
  θ = φ = 0), so "no box tree closes it; it needs a hand proof" (`disc273.md` §5).  Theory routes: A273's fan sketch
  (the drop's apex angle > 90° vs a channel opening ≤ 5°; "not written out"); A274's R1 (the ring domain) is DEAD (s.5.3);
  A274's R2 (direct slot argument, second order along φ → 0) not done (`r1_274.md` "For the theory agent").
  Alternative: A271's ring inequalities as a ring-level statement (the ~10³ CPU-h residual certificate, not launched,
  `ring_domain.md` §0).  Outside the corner: the DROP tree, 40/81 cells certified + verified, c5_4 / c5_5 capped with
  OPEN leaves, θ-bins 0, 6–8 pending (s.3).
- [C] **5b off the ring domain, the older route** — `strip266` [T-computed\*]: a full tree priced ~5·10³ CPU-h; the
  budgeted six cells are all OPEN at the budget.  Superseded in the chain by the DROP form (A273), kept as the fallback.
- [C] **5d — indirect jams, FLOAT2 corners, a middle toucher above X = TWO CAP-2 STATEMENTS** (A277, `float2_room.md`):
  BL-CAP-2(C, D) for a FLOAT2 corner (Lean axiom `bl_cap2_float2`) and BL-CAP-2(A, C) for a JAM corner with any holder
  (direct, indirect, middle toucher above X) — no two interior-disjoint BL-sector misses free of the two box meeters.  What
  would close each: the diameter certificate `cert277` (6 / 5 parameters, 0.02 s per box, 12/12 bench points CERT), priced
  30–1000 / 3–100 CPU-h, not launched (add a P1-aware PRUNE first); or a theorem that no normal-form FLOAT2 corner exists
  ([M] `float277`: sup 0, attained only where a floater becomes a toucher); or, for FLOAT2 corners whose blockers serve
  their far boxes, the 4-parameter dropped pair (~3 CPU-h) + 5b's strips.  [C] INDIRECT-FREE (no free square meets
  S_u(C) under H1 with X above C, holding or not) would leave middle touchers as the only indirect holders.
- [C] **6 — the Lean axiom `jam_count`** (= 5a–5d); BOX-MEETERS(11) is [T from 5] (`box_meeters_262`).
- [C] **8b — the slab** (some wall in (0, 0.703°), not all): A263's 492 engine jobs [T-computed\*], "priced 1–10⁵ leaves
  each, 2·10⁷ for the boxes adjacent to the cube" (`open_pairs.md` §0 (d), §5.2); no slab-job index exists on disk.
  The all-near-flat cube itself is [T] (8c).
- [C] **10c — the remaining P2 cells** — 20 of 70 indexed cells not ok (s.3); A265's s_eff fix certified three of its
  five, 3,5 / 3,6 still OPEN.  Certificate route: the s_eff + graded-plug re-run (`cert265`) on every not-ok cell.
- [C] **10d — CAPACITY-2 on the non-ADJ family** = MISS-IN-GAP ∧ GAP-HOLDS-ONE-MISS ∧ ONE-UNSERVED-WALL (Lean axioms
  `miss_in_gap`, `gap_holds_one_miss`, `one_unserved_wall`; `capacity_two_of_gap` [T]).  GAP-HOLDS-ONE-MISS: the
  horizontal half is [T] (`gap_interval_centre`), the vertical half [C] (the wedge / lip cases), plus the sub-case
  1 + w − sec φ₁ ≤ e < sec φ₁ and the wedge case φ_W ≠ φ₁.  Theory: "P1 on the lower gap square is still the way"
  (`last_two.md` §0).  Certificate: the non-ADJ trees P2n / WEn / WSn (queued; they "will mark exactly this region
  OPEN", `k0_route.md` §13 10d).  [M] `cap266`: no two disjoint misses on any ring tried.
- [C] **The [T-prose] Lean axioms of the chain**: `meeters_split`, `band_count`, `normal_form_step` (with
  `touchPotential_le`, `rowVecPotential_le`), the three corner lemmas `mixed_corner_pm`, `mixed_corner_mp`,
  `pinwheel_corner_pp`, `strip_two_in_ring`, `strip_two_in_jam`, `strip_two_in_jam_of_disc` (whose opaque `DiscLemma`
  is [F] as stated — s.5.3; the DROP form has no Lean statement yet), `lemma_PUSH`, `two_pokers`, `top_two`,
  `flat_above`.  Closing each is a Lean formalisation of a prose proof (the files' "O-…" obligations).
- [C] **The Lean axiom `touch_normal`** (= NO-JAM(11), `box_meeters.md` §7).  **`rows_classified` is [T-prose]**: the
  prose is [T] (`normal_ring.md` §3.1) and the Lean statement is a documented axiom — retagged [T-prose] in
  `k0_route.md` §13 link 7 and `box_meeters.md` §7 (coordinator, 2026-09-23; A261's file had tagged it [C]).  The Lean
  consumers `k0_value_of_factors` / `k0_value_of_hybrid` also depend on the axiom `normal_ring` (AUDIT).
- [C] **Dependency: k1_00's tree** (K0-O1: (k1-a) no corner-pinned packing on [3.82, ŝ), (k1-b) at ŝ a Trump image) —
  every exchange lemma (K0-FREE, CELLS/RAISE, SWAP-LEAF, WALL-SLOT, link 12) consumes it; A84 priced it 200–300 CPU-h
  (`k0_route.md` §3, §6 table).  Its status is k1_00's own ledger, not this file.
- [C] **Uniqueness at ŝ** — SWAP-RIGIDITY of Trump for k ≥ 4 re-packed squares (k = 1 Theorem U [T], k ≤ 3 [M]).
  `common_sense.md` §2.1 (i); `ring_swap.md` §1.7.  **The stretch (ŝ, 4)** — [M] only (chain link 13).

**Forms of the k0 obligation that the chain has superseded** (each still a named [C] axiom; none is on the chain's
path, but each is a statement someone may try to prove again — know what it would buy):
- [C] **RAISE(0 → 1)** (A222, `raise_zero_one`) ⟸ **STUCK-4(11)** = **CLICK-DOWN** (A223, `click_down`; `stuck4_eleven`,
  `stuck4_unlocked_eleven`, A242) ⟸ nothing proved; **STEP** (A231: a corner swap exists; with k1-a kills every
  four-crowd, `fourcrowd_dead_of_step_kill`).
- [C] **ONE-FLUSH(n)** (A226, `one_flush`; the optimum form) ⟸ **LOCKED-CROWD-FREE(n)** (A233, `locked_crowd_free`) ⟸
  **RING-CAPACITY(n)** (A236, `ring_capacity`) ⟸ **POCKET(n)** (A237, `pocket_cap`); **REALIGN** (A231, `realign`) +
  STEP ⟹ ONE-FLUSH(n).  **SEAM** (A223): one tilted grain at every optimum below ⌈√n⌉.
- [C] **STUCK-EXIST(11)** (A246, `stuck_exist_eleven`) ⟹ **FAMILY-STUCK-EXIST(11)** (A250, `family_stuck_exist_eleven`;
  the weaker, current existence form) ⟸ RING-POCKET(11) (A251, `ring_pocket_eleven`) ⟸ RING-POKER-RESIDUAL(11)
  (A252, `ring_poker_residual`) + `family_stuck_non_ring`; **SNAP-DOWN(11)** (A245, `snap_down`);
  `corner_chase_closes`, `type_t_chase_closes` (A248/A249).
- [C] **ONLY-RING(n), MONOTONE-ROOM(n)** (A253/A254, `only_ring`, `ring_peel`; ⟹ `peel_excludes`), **QUANT-ROOM(11)**
  (an effective τ₀), **COMMON-SENSE(n)** (A255, `common_sense`, `ring_of_common_sense`), **NORMAL-RING(11)** (A258,
  `normal_ring`, hybrid form).  MONOTONE-ROOM is [M] "true in normal form" (A259).
- [C] **H1 = T3|k0** (A87, DF-O4 OPEN): no k0 configuration with s < ŝ is FJ-critical — "not affordable as a cover".
- [C] **RING** as a structure census (A219; 2.6·10¹¹ structures), **LOCK-FREE⁺(< 4)** (ledger §4), **NO-VV-STRESS(n)**
  (A235), **RES-N(δ_∞)** (A92-G1, the nicked slab) — the load-era forms.

## 7. DEAD ROUTES [D] — the reason each died and its price, so nobody re-prices them

The recurring reasons: **PRODUCT LAW** (a leaf that needs every one of several independent roles localised at once
multiplies the per-role counts — four corners, eight meeters, 17 coordinates); **DIMENSION** (a box cover of a
positive-dimensional family at the radius a certificate fixes); **MARGIN vs BIN** (the certificate's tilt / box bins
cost more than the statement's margin, or the margin is zero); **FALSE LEAF** (the leaf's statement is false or does
not hold on a cell's fibre); **LOAD** (a force argument cannot see rattler crowds).

### 7.1 The volume trees (the k0_00 zone tree and its cascades)

- [D] **A38 root power** — the far-field tree at s0: a per-node LP DECISION wall, 70–700 desktop-days as an open-ended
  floor (`attempts/A38-root-power/results/rootpower_report.md`; `k0_route.md` header).  A84: ≥ 100 desktop-days plain.
- [D] **A85 interior-first tree** — level 1 undecidable (η −0.12…−0.34, all repairs fail); depth 2 decides (τ = budget −
  1.0…1.27) at ≈ 1 000 s LP + 630–860 s certification per node; f₂ = 1/3 at A60 defaults.  **Price 3 200–7 000 CPU-h if
  f₂ ≈ 0.85, ≥ 3·10⁴ CPU-h if f₂ = 1/3.**  "The order-of-magnitude cut the brief asked for does not exist along
  C1–C3."  `k0_route.md` §0, §7–8; A85.  Reason: MARGIN (certification reliability at η ≈ −1).
- [D] **A85 corner seed as a cover (C3)** — N_pair ≈ 3.4·10⁴ per corner, 2.9·10¹⁶ four-corner nodes after prunes and
  /8; level 1 alone 2.8·10⁴ attemptable LP nodes (≈ 1.3·10⁴ CPU-h); no finite case list (K0-PAIR (b)).  `k0_route.md`
  §7.2, §8.4; A85.  Reason: PRODUCT LAW + DIMENSION.
- [D] **A87 H1 as a certificate (T3 restricted to k0)** — the restriction prunes nothing at cell level; the cell count is
  the 33-dimensional volume at the discharge scale: 10⁶³ cells at h = 10⁻², 10¹⁰⁶ at 5·10⁻⁴.  `drain_flow_k0.md` §0,
  §6; A87.  Reason: DIMENSION.
- [D] **A92 crowd certificate chain** — certified only at δ = 0.3 (Theorem S(0.3)); δ = 0.2 undecided (LP a
  non-converged lower bound; 65/65 run-B holes); δ ≤ 0.1 impossible for the weighted root LP; the residue RES-N(δ_∞)
  and uniqueness at ŝ are not reached.  `k0_blocked_side.md` §0, §5–6; A92.  Reason: MARGIN.
- [D] **A99 k0 tree v2** — "NET PRICE INCREASE, not the ~10x asked for"; R1 (sub-box re-verification) 0/1; the frontier
  9 341–21 661 CPU-h.  REGISTRY row A99; LOG 2026-09-05 A99; `residue_ledger.md` §4.  A115 (warm re-solves) removed
  1 023–2 372 CPU-h of it for 29.8 CPU-h, leaving twelve CONVERGED-ALIVE cells (τ = budget, minmass 1: "no LP time kills
  them"); the ledger's one-table row: "12 cells; tree priced ~12,000 CPU-h after A115".  A115 T3: corner rows at the
  node level kill nothing genuinely alive — at depth 0 every Trump image realises nine corner incidences against a
  budget of eight, so the root crowd LP can never pass.  Reason: the LP cannot see K0-FREE (the K01 supports have
  one DEEP meeter per corner).
- [D] **A143 corner-first root / A166 nearest-corner sub-tree** — sound covers, not cheaper (A143 kills 0 of 216 level-1
  cells).  `residue_ledger.md` §4 A143, A166 notes.
- [D] **A165–A168 / A183 / A191 the PI's k0 cascade on l1_104** — sound, does not close the cell; A191: 17 of 64 alive
  S2 nodes DEAD (frozen verifier), 305 s per node; A195's re-price (`docs/budget.md` "The cascade route"): eleven
  cells × 1 375 CPU-h (deep kill rate 1.00) = 15 125 CPU-h … × 359 647 (rate 0.95, "the measured S3 rate carried
  down") = 3 956 117 CPU-h, "not purchasable".  Reason: PRODUCT LAW (the kill rate per level compounds).
- [D] **A232 SWAP-LEAF on the k0 root cells** — the eleven converged-alive cells box ONE square (u = 10), so the leaf asks
  for ten disjoint squares in [0, 3.82]² avoiding H's reach set (s(10) = 3.70711, slack 0.113); the search places 6–9;
  A185's split cannot help (SPLIT-INVARIANCE).  `swap_leaf.md` §0; A232.  Reason: FALSE LEAF at that depth (the leaf
  is sound; it is only available at the crowd-conditioned root, u = 3, which is the cascade again).
- [D] **A242 crowd root, leaf L1 = NO-ROOM(m = 3) over the eight cores** — L1 fires only when ALL EIGHT roles are at
  A60's box scale: ≈ 1.7·10¹⁷ cells, **≈ 10¹⁵ CPU-h** at 20–35 s/cell; L2 (BOX-GORDAN, [T] new) is gated by L1's own
  weakness (worst pocket gap 0); L3 dropped (a quantifier: A239's lemmas need the Ψ-minimiser).
  `attempts/A242-crowd-root/notes/crowd242.md` §0; A242.  Reason: PRODUCT LAW.
- [D] **A243 REACH-SUMMARY re-root** — the 16-coordinate grid g¹⁶/8 = 1.25·10¹⁵ cells at g = 10; R1 (REACH) and R2
  (LEVER) are not cell inequalities ([Q-ALONG-WALL], [Q-STRUCTURE]); R3 subtracts only the FIBRE's cores, empty in every
  occupied bin at h = 0.2 — the honest price returns to A242's ≈ 10¹⁵ CPU-h.
  `attempts/A243-reach-root/notes/reach243.md` §0; A243.  Reason: FALSE LEAF on the fibre + PRODUCT LAW.

### 7.2 The structure censuses and ring certificates

- [D] **A219 RING as a finite structure question** — 2.6·10¹¹ structures (h ≤ 3 interior holders), 2.3·10⁶ CPU-days at
  0.78 s each (232 CPU-days without interior holders); and it would exclude LOADED four-crowds only.
  `wall_torque.md` §0, §6; A219.  Reason: PRODUCT LAW + LOAD.
- [D] **A233 arm structure list** — finite and small (≤ 10⁷ row lists per corner at H ≤ 5), but it decides only LOCKED,
  and locked corners exist at the optimum (Trump's TL).  `local_lock.md` §0, §4; A233.  Reason: FALSE LEAF.
- [D] **A247 perimeter walks** — 66 112 676 788 labelled walks (13 453 179 721 after the 62 pair kills; 820 161 up to
  the type-F conditional); per-walk bounded search over 11 poses + s is out of reach; 92 pair problems η-degenerate.
  `perimeter_walk.md` §0; `family250.md` §2.3; A247/A250.  Reason: PRODUCT LAW + MARGIN (the η-degeneracy).
- [D] **A251 box-valid PIERCE over the 17-coordinate ring family** — ε* = 0.1397 admits a box half-width only r = 0.0312
  in all 17 coordinates: **3.9·10¹⁸ boxes ≈ 5·10¹⁴ CPU-h** against a 200 CPU-h stop ("stop at the design"); the AREA
  bound breaks at ε = 0.03.  `ring_pocket.md` §0; A251.  Reason: DIMENSION ("the COUNT — 17 coordinates at a radius the
  certificate fixes").
- [D] **A252 disc criteria** — every INRADIUS-only criterion fails in the flat-flat limit (s.5.2).  Reason: FALSE LEAF.
- [D] **A237 area / waste form of POCKET-CAP** — needs a tilt floor ≥ 32° at n = 11 (none exists); closes at no n ≥ 18.
  `pocket_waste.md` §0; A237.  Reason: MARGIN (O(ε) waste).
- [D] **A266 `strip266` (5-parameter LEFT-SHADOW tree for STRIP₂)** — ~5·10³ CPU-h for the 27 root cells (535 s per
  1/1200 sub-cell; the 1° tilt bins cost 0.017 of a 0.005–0.02 margin); the plain annulus test 170 CPU-h per root cell;
  launched budgeted, every cell OPEN at the budget (s.3).  `last_two.md` §0, §1.3; `k0_route.md` §13 5b; A266.
  Reason: MARGIN vs BIN.
- [D] **A262 7-parameter `jam` kernel** — priced 15 (median) – 500 (mean) CPU-h, heavy tail (`price262`); made
  unnecessary by A264's reduction to `pair3` + STRIP (`three_lemmas.md` §0 Lemma 1: "The 7-parameter `jam` job is then
  unnecessary").  `no_jam.md` §0; A262/A264.  Reason: DIMENSION (superseded by a 4 + 2-square split).
- [D] **A271 residual certificate on R** (the ring-inequality violators, ~18 % of H1–H3) — ~10³ CPU-h, not launched
  ("over the 20 CPU-h line by two orders").  `ring_domain.md` §0; A271.  Superseded by A273's DROP form (hours).
- [D] **The DROP tree on the corner θ, φ ≤ 5°** — cannot be bought at any price: STRIP₂'s own margin → 0 (`disc273.md`
  §5, §7.3).  Reason: MARGIN = 0.

### 7.3 Dead theory routes (a proof shape that cannot work, with the reason)

- [D] **Counting** — K0-COUNT (LOAD, DISTINCT false), the perimeter sweep (closes only n ≤ 4), NO-CLOSURE (slack 2 at
  n = 11, closes at no n), A246's composition (locally feasible below 4), the family ILP (9 ≤ 11).  Why: "the rules
  are local and the obstruction below 4 is global" (`family250.md` §2.2).  A218/A222/A236/A246/A250.
- [D] **Force / torque / handedness** — RING needs loads (rattler crowds invisible: 61/70 corners), handedness never
  separates, OPPOSE false, NO-VV not forced; A222: "Loads are never used" in the route that replaced them.  A218–A240.
- [D] **Local per-corner closures** — every LOCAL mechanism (corner waste, chord deficit, wall budget, per-corner side
  charge) is doomed: a doubly-met corner costs O(ε) (CROWD-ABOVE, `one_flush.md` §0); a locked 2-crowd exists at the
  optimum (Trump's TL, `local_lock.md` §0); COMMON-SENSE is false locally (`common_sense.md` §0).  A226/A233/A255.
- [D] **Area / waste / tilt floor** — no tilt floor exists (A89; TILT-MIN binds upward; θ_min = 0); waste of a
  near-flush ring is O(ε).  `pocket_waste.md` §0; `mintilt253.md` §0.  A237/A253.
- [D] **Disc / radius bounds on the pocket** — the MOUTH and the flat-flat notch (A252); "the proof of the pocket bound
  must use SQUARE room … a disc radius alone cannot do it".
- [D] **Ring-domain transfer at small angles (A274 R1)** — (U3)–(U6) fail on exact H1–H3 witnesses inside θ, φ ≤ 5°.
- [D] **Drain / flow as a proof** — the quantitative drain is false as a mechanism, the exit map does not exist
  (codim-3 strata), H1 is T3 (DIMENSION).  `drain_flow_k0.md` §0, §3; A87.  CLICK-DOWN ⟺ STUCK-4 (the click is the
  conjecture, not a mechanism below 4, where no test object exists), `two_grains.md` §0; A223.

## 8. THE CURRENT CHAIN — `k0_route.md` §13 copied and re-tagged as of 2026-09-23

Source: `k0_route.md` §13 (A264, 2026-09-22, with A265–A273 edits).  The tags are §13's; "TODAY" adds what the index
files and the later notes (A273 index, A274) say.  Files in `docs/proofs/` unless noted.

1. **A packing of 11 at side s ∈ [3.82, ŝ] is family-stuck or reduces to the k ≥ 1 classes** [T] — `normal_ring.md`
   §1.2 (Lean `normal_ring_value`); the k ≥ 1 classes are the k1_00 / k5 trees (their own ledgers).  TODAY: unchanged;
   the reduction consumes k1_00's tree (s.6, dependency).
2. **NORMAL FORM** [T]: a lexicographic maximiser of (Φ₁, Φ₂, Φ₄, Φ₃) with P1, P2, P2′, P3, P4 (RETREAT) —
   `normal_ring.md` §1 (Lean `exists_normalForm`; compactness [T-prose]); P1⁺ — `box_meeters.md` §1.1.  TODAY: unchanged.
3. **BAND-COUNT / HOLE-ONE** [T]: ≤ 1 square contains O, every other square meets the unit band — `peel.md` §2.1,
   `normal_room.md` §2.1 (Lean `hole_one_tilt`; `band_count` [T-prose]).  TODAY: unchanged.
4. **MEETERS SPLIT** [T]: a doubly-met box has ≤ 1 toucher per wall, none touching both, every further meeter floats
   (SAME-WALL, WEDGED-SEAL, TWO-CORNERS) — `box_meeters.md` §0, §2 (Lean `same_wall_core`; `meeters_split`
   [T-prose]).  Corner types PAIR / THIRD / JAM / FLOAT2 — `no_jam.md` §1.  TODAY: unchanged.
5. **COUNT + ROOM ⟹ n ≤ 9 for every corner type** [T] — `no_jam.md` §2.3 (Lean `jam_count_core`, `no_jam_of_count`);
   the third-meeter type is free by monotonicity.  So NO-JAM(11) = ROOM(JAM ring) ≤ 1, per JAM corner (sectors):
   - 5a. TL sectors = **pair3** (4 parameters) [T-computed\*, A262 chain3].  TODAY: **not landed** — chain3 ran
     `float262` (2026-09-23 11:59); no `pair3` index.
   - 5b. BL sectors = **pair3 at BL with T_u** [T given STRIP] + **STRIP₂**.  The history, each step later than the
     one before: A265 STRIP [T] for a flat C, [T-computed] on the rings tested; A266 **[F] as A265 stated it for a
     tilted C**, [M] 60/60 on the true domain, [T-computed\*] `strip266` (~5·10³ CPU-h, budgeted); A267 STRIP₂-IN-RING
     [T-prose] (WEDGE-FLOAT [T], `wedge_extent_core`) on the ring domain (D1)–(D2), (U1)–(U9), 43/43 JAM rings;
     A271: (D1), (D2), (U1), (U2), (U9) are THEOREMS from H1–H3, (U3)–(U6) FALSE as consequences, (U8) [M] +0.094;
     A272: the problem reduces [T] to the DISC LEMMA [M]; **A273: the DISC LEMMA is [F]** (`witness273`); the corrected
     DROP LEMMA (4 parameters, h_v-invariant) is certified by a box-valid penumbra tree + `verify273` EXCEPT the corner
     θ ≤ 5° ∧ φ ≤ 5°, which needs a hand proof.  So 5b = STRIP₂-IN-JAM [T-prose, the DROP form] + the drop tree
     [T-computed when verify273 passes, outside the corner] + the corner [C] + `pair3`.
     TODAY: the drop tree has 42/81 cells, **40 CERT and verified PASS**, c5_4 / c5_5 capped with OPEN leaves, θ-bins
     0 and 6–8 not run; **A274: the ring-domain route R1 is DEAD on the corner** ((U3)–(U6) fail there on exact H1–H3
     witnesses; only (U8) holds); STRIP₂'s own margin there is 0.25 θ² at φ = 0, 0.5 θ on θ = φ (A274, correcting
     A273's 0.15 θ²).  The corner stays [C]; no Lean statement of the DROP form exists.
   - 5c. j = 2 opposite: room 0 [M]; j = 2 adjacent: rings exist, capacity 1 [M] — per-corner sectors apply
     (`three_lemmas.md` §4.4); j ≥ 3: none on the window [M].  TODAY: unchanged.
   - 5d. Indirect jams (a non-toucher blocker), FLOAT2 corners, a middle toucher above X: [M] pending (`float262`,
     `span262`) — no room statement [C].  TODAY: `float262.json` reports "JAMMED FLOAT2 EXISTS" (sup_t +0.00224,
     chain output, committed 2026-09-23); `span262.json` sup_t −0.0327 at ŝ.  Still no room statement: [C].
   - 5e. Adversary / search: 399 structured starts, capacity ≤ 1 always, no 11-witness [M].  TODAY: `search262.jsonl`
     has 552 rows; no source text reports on the extra rows.
6. **BOX-MEETERS(11)** [T from 5]: every box has exactly two meeters, wall touchers, eight distinct — `box_meeters.md`
   §5 (Lean `box_meeters_262` from the axiom `jam_count` [C = 5a–5d]).  TODAY: unchanged.
7. **ROW CLASSIFICATION** [T-prose]: each wall carries a row of two, a row of three or an open pair — `normal_ring.md`
   §3.1.  TODAY: prose [T]; Lean `rows_classified` a documented axiom, retagged [T-prose] in `k0_route.md` §13 and
   `box_meeters.md` §7 (was [C]); `touch_normal` stays [C] = NO-JAM (s.6).
8. **WINDOW EXCLUSIONS**:
   - 8a. Rows of three, exactly flat walls, mixed senses at tilts ≥ 0.703° on every wall: A261's LP certificates
     [T-computed\*: 11/50 verified at A261's exit].  TODAY: **[T-computed] — `cert261.jsonl` 50/50 done and verified,
     feasible 0, undecided 0.**
   - 8b. The slab (some wall in (0, 0.703°), not all): A263's 492 engine jobs [T-computed\*, queued after WE].  TODAY:
     no slab-job index on disk; the last line of A263's `logs/chain263.log` is P2 cell 7,6 (14 838 s).  [C] until they run.
   - 8c. **The all-near-flat cube of every mixed pattern: [T]** — `three_lemmas.md` §3 (Lean `slab_cube_264`).
   - 8d. One sense, common tilt, rows of two: the normal family D′ / the hybrid ring — not excluded, it exists; room 10.
   - 8e. Mixed senses with per-wall tilts exist from s = 3.9298 > ŝ [M, A258] — outside the window.
9. **LOCKS AND OPEN PAIRS** [T]: an open pair survives only HELD by a free square (UNLOCK = P2′; LIFT) —
   `locked_wall.md` §1; unequal tilts survive only as locks — `open_pairs.md` §4.  Non-ADJ walls carry a free square in
   the unserved slot [T, Lean `nonadj_free_meeter`].  TODAY: unchanged.
10. **ROOM: every free square of the hybrid normal ring contains O**:
    - 10a. Normal D′: A259's PAIR tree [T-computed\*: index filling] + A260's LAYER (PLUG) [T + T-computed, 0 bad].
      TODAY: **[T-computed] — 81/81 cells, `verify259.json` bad 0 (CERT 78 099, PRUNE 3 066, LAYER 5 184, OPEN 0).**
    - 10b. Hybrid, common tilt, all-ADJ, e ≤ ½: hybA / hybB / hybAB [T-computed\*: 8/81 at A260's exit].  TODAY:
      **[T-computed] — 81/81 each, `verify260.json` bad 0, OPEN 0.**
    - 10c. Hybrid, independent tilts, all-ADJ: A263's P2 ∧ WE ∧ WS [T] reduction + certificates; A265 [T]: the OPEN
      leaves are a SIDE mismatch, re-run at s_eff + graded plug (2,4 / 2,5 / 3,4 certified by `verify265`; 3,5 / 3,6 in
      A265's lane); WS 3 cells, WE 1 cell.  TODAY: WE 1/1 ok, WS 3/3 ok; **P2 70/81 indexed, 50 ok, 20 not ok**; A265's
      lane: 3,5 / 3,6 not ok (OPEN leaves 3 837 / 911, bad 0).  [T-computed\*] with twenty cells to repair.
    - 10d. Non-ADJ (wide gap, e up to 1.169): ROOM is [F] as a bare-ring statement; STRUCTURE closes the strip (GAP-CELL,
      BLOCKER-SIDE, STRIP-CHAIN [T] for e ≥ sec φ₁ at common tilt); the statement needed is CAPACITY-2 (Lean
      `gap_needs_two_misses`) = three gap statements (Lean `capacity_two_of_gap`), all [C]; the stack's upper square
      contains O horizontally [T] (`gap_interval_centre`), vertically [C].  [M] `cap266`: no two disjoint misses on any
      ring tried.  TODAY: unchanged; P2n / WEn / WSn not run.
11. **8 + 1 < 11** [T]: eight ring squares + one square containing O — Lean `openPairs_excludes`, `normalRoom_count`.
    Hence no normal-form family-stuck packing of 11 on the window ⟹ FAMILY-STUCK-EXIST(11) fails in value form ⟹ with 1:
    **k0_00 is empty** (Lean `k0_value_of_factors`, `lockedWall_excludes`).
12. **k0_00 via CELLS / K0-FREE** [T]: Lemma CELLS (`ring_swap.md` §1.3, Lean `cells_swap`), K0-FREE = |Π| = 1;
    RAISE(0 → 1) is exactly 11 (`ring_swap.md` §0).
13. **The stretch (ŝ, 4)** [M only] and **uniqueness at ŝ** (the iterated VALUE-WLOG: SWAP-RIGIDITY k ≤ 3 [M], k ≥ 4
    [C]) are outside this list.

**Still [C] or waiting, TODAY** (compare `k0_route.md` §13's closing paragraph, A266): 5a/5b `pair3` (not landed);
5b the DROP tree's remaining cells (θ-bins 0, 6–8; c5_4 / c5_5 capped) and the near-flat corner θ, φ ≤ 5° (a hand
proof; R1 dead); 5d FLOAT2 / indirect jams / middle toucher (no room statement; a jammed FLOAT2 configuration is now
[M]); 6's axiom `jam_count`; 8b the slab jobs; 10c the twenty P2 cells; 10d the three gap statements of CAPACITY-2;
the [T-prose] Lean axioms (s.6); the dependency k1_00's tree; the stretch; uniqueness k ≥ 4.  **Closed since §13 was
last written**: 8a (A261 50/50), 10a (A259 verified), 10b (A260 81/81 ×3 + layer).

**Plain-language summary — what k0 exclusion at n = 11 now rests on.**  Suppose eleven unit squares fit in a square of
side between 3.82 and Trump's 3.877084.  If some border cell (a corner box or a wall slot next to it) is crowded by
too few squares, the squares can be swapped, at the same side, so that a corner square sits flush — and then the
k1_00 tree (a separate, owed computation) rules the packing out.  So we may assume every family of border cells is
over-crowded ("family-stuck"), and among all such packings we pick the most orderly one (the lexicographic normal
form: most wall-touching squares, longest equal-tilt rows, free squares as far from the border as they can go).  In
that form each corner box is met by exactly two squares, one on each wall; each wall carries a row of two tilted
squares, a row of three, or an open pair held apart by a free square; and the eight wall squares form a pinwheel
ring.  Every other square must lie in the ring's central pocket, and the whole case analysis comes down to one
statement: every free square of the pocket covers the centre point O, so the pocket holds at most one square — 8 + 1
= 9 < 11 (the other pinwheels of rows are excluded below ŝ separately: the window exclusions).  The pieces are PROVED
where they are theorems (the hole-one lemma, the flush limit, the near-flat cube), CERTIFIED by box trees with
independent verifiers on the normal ring, the hybrid ring and the window exclusions' LP part, and
still OWED in four places: (i) corners where a box meeter floats off its wall (the JAM corner — `pair3` and the strip
lemma, whose last piece is a thin near-flat corner that no computation can reach and that needs a hand proof);
(ii) the FLOAT2 and indirect-jam corners (no room statement at all yet); (iii) twenty open cells of the independent-
tilt pair certificate and the near-flat slab jobs; (iv) rings whose wall squares do not reach the far slots (non-ADJ),
where the needed statement is only that two free squares cannot both miss O.  Underneath all of it: the k1_00 tree,
and the Lean formalisation of the [T-prose] steps.

## 9. GENERAL n

**9.1 Which items are m-free** (stated for every n; the sources' own "n-general" / "any n, any s" lines).  Exchange:
SWAP, STEP, CELLS, `teleport_packing`, NORMAL-CELL, UNLOCK / HELD / LIFT, WALL-SLOT, SWAP-LEAF, VALUE-WLOG, NORMAL-FORM
(P1–P4, "any n, any s").  Corner geometry: SIDEBAND (a), A1, A2, Theorem B, PUSH, HOLD, ONE-TILTED, WEDGED-SEAL,
TILT-MIN, SAME-WALL, BLOCKER-SIDE, STRIP-LANDING, T-CELLS / T-TIP / T-SLOTS, STACK (2 + √2 ≤ s < 4), A246's rules
(s ∈ (2 + √2, 4]; only f = n − 8 uses n), CATALOGUE (s > 2 + √2), TWO-FAR (s > 7/2), EPS-1…6.  Room: HOLE-ONE (any
square container of side ≤ 2), NOTCH-NARROW, INRADIUS, THREE-DISC, MID-NOTCH, TWO-PIECES, POKER-ANCHORED, PIERCE,
PLUG ("any n, s, m"), WEDGE-FLOAT ("any n, s-free"), the NORMAL-RING corner closed forms ("a two-square statement").
Counting: CEIL, FLUSH, the perimeter count n ≥ 4(m − 2) + 1, NO-CLOSURE, BAND-COUNT (general), PEEL-0.  Force:
TWO-CONTACT, STRUT, Theorem SO, Lemma W, TORQUE-ID, LOCALITY, RADIAL, CHAIN, NO-VV-IND, CROSS-PLANAR.  Sources: s.2.

**9.2 Which are m = 4 (n = 11) only.**  The border system's perfect-matching conflict graph below 4 (`family250.md`
§1.3); row lengths ℓ ≤ 3 and "opposite walls never interact" (`normal_ring.md` §4); LIMIT-UNIQUE(4) (the flush stratum
is exactly the two pinwheels — "[F]" for m ≥ 5, `peel.md` §0); HOLE-ONE's use at σ = s − 2 (slack (4 − s)/2);
TWO-POKERS' window statement (s* = 3.9342 > ŝ; "for n ≥ 16 (s ≥ 4) TWO-POKERS is empty", `corner_chase.md` §5); every
number of §3.2–3.4 of `normal_ring.md` and every certificate of s.3; the JAM analysis (H1 uses s̄ ≥ 3.82); the lock
statistics; Theorem U, the basin, k1_00's tree, SWAP-RIGIDITY (Trump-specific).  K0-FREE's MECHANISM is n-general
(O-TELEPORT-N, `local_lock.md` §5); its KILL is the n = 11 k1_00 tree.

**9.3 NORMAL-RING(n) and its general facts** (`normal_ring.md` §4, A258).  [C] NORMAL-RING(n): four rows of m − 2 of
one sense, K = s − (m − 3) sec φ − w(φ), a + b = K, a, b < 1, the same corner condition, plus locked walls.  [T] for all
m: NORMAL-FORM P1–P3; a row of m − 2 with a, b < 1 is row-normal; the corner closed forms; least side (m − 3) sec φ + w +
1 + tan(φ/2) → m − 1; **the tight normal ring's flush limit is the TIGHT PINWHEEL for every m** (a row has no internal
gaps: A254's wall slack lives only in rings that are not row-normal).  General system: 8m − 20 border cells; family-
stuck needs one poker in a NARROW ribbon (`peel.md` §1.2).

**9.4 PEEL / the onion** (`peel.md`, A254).  [T] PEEL-0: k core squares ⟹ s ≥ 2 + s(k).  With BAND-COUNT, a packing with
NO straddler has s ≥ 2 + s(n − 4(m − 2)) — exactly the tight flush pinwheel (four 1 × (m − 2) wall blocks; pocket =
hole [1, s − 1]² ⊔ four isolated notches); HOLE-ONE is m = 4 (n′ = 3, s(3) = 2).  For m ≥ 5 only the weaker
s ≥ (s(n′) + m + 1)/2 on the whole flush stratum (POKE: pocket squares poke into mid-wall gaps).  Conditional [C]:
ONLY-RING(n) + MONOTONE-ROOM(n) ⟹ "no family-stuck packing below 2 + s(n − 4(m − 2))" (Lean `peel_excludes`).  Table
(36 values n ≤ 100 below ⌈√n⌉, on the tight pinwheel): THEOREM-WINDOW 6 (n = 5, 10, 11, 18, 19, 29), THEOREM-AT-RECORD
3 (17, 26, 27), RECORDS-ONLY 26, EQUALITY 1 (n = 84), NOT-EXCLUDED 0 (`results/peel254_table.md`).  n = 11: "nothing
new is closed".

**9.5 The PI's structural reading, as the sources state it.**
- **ONLY-RING** [C] (the PI; `mintilt253.md` §4, `peel.md` §1.3): every family-stuck packing below m contains the ring;
  its other squares are ≥ 1 poker and free squares.  Plausible from the ILP (the minimal structure is the all-ADJ ring +
  one poker), not proved; "the count does not prove uniqueness".  At n = 11 the chain replaces it by NORMAL-FORM +
  BOX-MEETERS + ROW CLASSIFICATION (links 2–7).
- **RETREAT** (the coordinator's addendum, P4 / Φ₄): free squares sit where they meet the fewest border cells; a poker
  that is not HELD does not count, and nothing can hold a seated poker ("beside a seated poker no unit square fits at
  all") — `normal_ring.md` §0, §2.1; HELD-JAM does NOT exclude the JAM ring (`no_jam.md` §0).
- **The domino pinwheel is the limit** [T]: the τ → 0 limit of the all-ADJ ring is the four-corner domino pinwheel with
  capacity exactly 1 (`mintilt253.md` §0); the near-flat mixed ring tends to it at ANY side (`open_pairs.md` §5.4); the
  flush limit of the tight normal ring is the tight pinwheel for every m (`normal_ring.md` §4); A226's CROWD-ABOVE builds
  four crowds from corner dominoes at every side > s(n) (`one_flush.md` §0).
- **Why a variational argument is needed for all n** — A226: the all-packings statement STUCK(n) is false for every n
  whose record has corner dominoes, and a doubly-met corner costs O(ε), so "the obligation is ONE-FLUSH(n) … a
  statement about minimisers whose proof must be an IMPROVEMENT argument (every four-crowd at side S admits a packing at
  side < S), not a counting, waste or perimeter bound" (`one_flush.md` §0).  A233: the extremal (Ψ-minimal optimum)
  route is n-general and reduces ONE-FLUSH(n) in value form to LOCKED-CROWD-FREE(n) (`local_lock.md` §0).  A255/A258:
  VALUE-WLOG makes the choice of packing free, and the lexicographic normal form is the variational selection the n = 11
  chain uses.  **SEAM** [C] (A223): every optimum below ⌈√n⌉ is flush squares + ONE tilted grain — consistent with
  n = 5, 10, 11, 19 (`two_grains.md` §4).
- **n-general evidence** [M]: the ONE-FLUSH survey (21 records, n = 5 … 55: ≥ 3 flush corners each; Trump the only
  doubly-met corner) — `one_flush.md` §0; records are cross-braced, none a ring — `ring_capacity.md` §0.

## 10. TOOLS AND CONVENTIONS for the next agent

**10.1 The corpus** (read-only; every file is some attempt's result).
- A217 witnesses: `attempts/A217-torque-probe/results/witnesses217.jsonl` (486 FJ-feasible local optima, sides
  3.886746 … 5.001260; classes SETTLED / K0FREE / BOXK0 / HELD / CROWD) + `search217_*.jsonl` (the 4 534 packings A222
  tested); the ring `rand_0_0569|t20` (side 4.1099) is in it.
- A244 twelve-stuck: `attempts/A244-twelve-stuck/results/twelve244.jsonl` (489 rows, 488 twelve-stuck, 4.000010 … 4.5,
  interval-certified), `twelve244_ctrl.jsonl` (the 4-stuck control), `probe244_below4.jsonl` (the failed sub-4 probe).
- Ring witnesses: A249's exact all-ADJ type-T ring at ŝ `attempts/A249-type-t-chase/results/twotilted249_ring2.json`
  (+ `twotilted249_ring.json`, `twotilted249_wall.json`); A226's crowd rings `ring11_226.jsonl`; A253's ring + poker rows
  (`attempts/A253-min-tilt/results/room253.jsonl`, `mintilt253_curve.jsonl`).
- A258's normal rings: `attempts/A258-normal-ring/results/` (`norm258.jsonl`, `poker258.jsonl`, `exact258.json`,
  `side258.jsonl`, `typeF258.json`); the 46 corpus rings = A253's 44 ring + poker rows + A255's 2 controls.
- A262's JAM rings: `attempts/A262-no-jam/results/ring262.jsonl`, `adv262.jsonl`, `search262.jsonl` (A264's 323 = ring262
  + search262 at five sides); `float262.json`, `span262.json`.
- Exact counterexamples: `witness273` (A273, the DISC LEMMA), `attempts/A274-flat-corner/results/witness274.json` (W1, W2),
  `adv271` / `r1_274.json` (ring-inequality violators, rationalised), A248's CW poker, A252's `notch_disc.svg` notch, A266's
  `probe266 --nobox` strip squares.
- k0 optima: `attempts/A85-k0-route/results/cp85_k0_search.json` (262 k0 optima, 516 runs); records: A226's survey
  (21 packings, Ellsworth's coordinates, re-verified by exact SAT).

**10.2 The exact-check tools.**
- Geometry check (exact SAT on edge normals): A217 `geom217.meets_box`; rational squares via tan(θ/2) in Fractions
  (`witness273`, `witness274.py`); interval certification in mpmath (`verify244`, `verify250`: inflate, then 40-digit
  intervals for containment, pairwise interior-disjointness, depths).
- The 12-cell family test: `attempts/A250-family-stuck/code/fam250.py` (conflict graph, every admissible family, Hall
  check; `test250`), `fam262` (12 cells on a ring + free square), `cells254` (general m).
- Region search: `attempts/A222-ring-swap/code/region222.py` (c-space per tilt, greedy, polish, exact check);
  `capacity259` (exact centre sets per tilt bin).
- PIERCE: `attempts/A237-pocket-waste/code/pocket237.py` (box-valid PIERCE: (P ⊖ K) ⊆ ∪(p_i + K) per tilt bin; Lean
  `capacity_le_of_pierce`); A251's sound cores `geom251.core_members` (half-side (½ − ρ)/w(Δθ)).
- Swap leaf: `verify_swap232.py` (`swap-leaf-certificate-v1`).  Frozen verifiers `verify_case.py` (sha 521cb01f…) and
  `verify_case_v4.py` are never edited.

**10.3 The certificate pattern** (A259 onward; each item is a lesson with its source).
1. A box test that is sound by construction: cores that lie inside EVERY member of the box (verified vertex-by-vertex
   with intervals), kernels / hulls per tilt bin, float margins EPS = 10⁻⁹ (`disc273.md` §2).  Subtract only CORES,
   never reach sets (A242 §2: "the free region over-approximated as container MINUS THE CORES").
2. An OWN verifier that imports none of the tree's code, re-derives every leaf with a different binning and directed
   rounding, replays the split for a tiling identity (no gap, no overlap, every leaf used once) — `verify259/260/263/
   265/266/273`.
3. BISECT ON DISAGREEMENT: a leaf the verifier cannot close is bisected by the tree's rule (depth ≤ 6–8) and every piece
   re-verified; still open ⇒ DISAGREE, never green (`verify259.md`: the nine first-run MISMATCHes were the verifier's
   ψ = 0 bin, kernel footprint 0.9957 < 1 — "the verifier's bin, not a hole").
4. SIDE / ADJ consistency: evaluate each box at the side its own hypotheses allow (s_eff), never impose a domain at one
   side and test at another (A265 §0: A263's OPEN P2 leaves were exactly that); PRUNE only by hypotheses the verifier
   re-derives (A273 §2.4, §3 (ii)).
5. Budget + index: one index row per cell, OPEN leaves counted, "PASS with OPEN leaves: not certified" (A273's index).

**10.4 The SVG rules** (the briefs of A260–A271, repeated in every page note): every panel geometry-checked (the drawn
squares ARE the checked configuration — `page274` asserts it), a note per panel saying what it IS, slivers drawn with a
10× inset, undecided regions grey stipple; pages under `docs/residue_map/campaigns/<Ann>/`.

**10.5 The ops rules** (every brief A241 onward, e.g. `attempts/A274-flat-corner/BRIEF.md` lines 3–7): ONE heavy python at
a time (BelowNormal, affinity 0xFFFF, PYTHONDONTWRITEBYTECODE=1); LAUNCH-AND-EXIT (detached, resumable runs with
`logs/STOP`; never wait on a run); tiny-step writing (≤ 120 lines per Write, a commit after every piece with explicit
pathspecs, fetch + plain merge only, no response over ~15k tokens); never touch another campaign's files or processes.

**10.6 Pitfalls** (each has cost the lab at least one attempt).
- **An optimiser's sup is not evidence.**  A272's "sup slack −0.005 on H1–H3, attained only as h_v → 1" was an artefact;
  the exact witness has +0.0079 (A273).  A253: "a failure to find a ring at a smaller τ would not be a proof either way,
  and at τ = 0.1° the margins are at the optimiser's resolution".  A244: "EVIDENCE, not proof".
- **Census counts vs closed classes.**  "census 0 alive" counted A57 tree ROWS; 290 G1 cover boxes were never emitted
  (A270, LOG 2026-09-23); "k5 closed at the window pad" read the G1 slab pad as the window (s.5.4).  A107: a glob bug
  read zero files silently ("264 k0_00 node jsons … were silently reading zero files", LOG).  A113 / A107: "a slot-set
  match is not a packing match" (`residue_ledger.md` §4).
- **Soft containment.**  An optimiser's penalty (soft) feasibility is not a packing: every candidate is re-checked exactly
  (A244 inflate + intervals; A274 rationalises every minimiser and re-checks all H1–H3 tests in Fractions); A265's
  FULL-corner witness overlapped by 0.007 and was not a ring (`last_two.md` §0).  A domain written as a loose box is
  not the geometric condition: "h_u, h_v < 1" is not "C meets the open box" once C tilts (A266).
- **Verifier bins.**  A verifier with a different binning can fail a correct leaf (A259's ψ = 0 bin); the tilt bin can
  cost more than the margin (`strip266`: 0.017 of a 0.005–0.02 margin); a zero-margin layer cannot be binned at all
  (A273's corner).
- **Stored results can be incomplete.**  A85's FAILs were row-generation-incomplete; a plain warm re-solve certified
  cells no queue had reached (A115, `residue_ledger.md` §4).
- **A refuted statement can survive as a Lean axiom.**  A251's `centre_disc_ring` had to be removed (A252); A272's
  `strip_two_in_jam_of_disc` still stands on the opaque `DiscLemma` whose prose content is [F] (A273; no AUDIT note
  yet, s.5.4).
- **"Unchanged" is the honest default.**  Every doc A218–A274 ends "k0_00 unchanged" unless a chain link moved; say
  which link, with its tag, or say unchanged.

## 11. APPENDS — A278 (2026-09-24), NO-FLOAT2 (`no_float2.md`; parts `attempts/A278-no-float2/notes/`)

- s.2.3 [T] **FLOAT-SLOPE** — two interior-disjoint unit squares of the quadrant both meeting the open box are separated only by
  positive-slope lines, and one is upper-left of EVERY separator (SQUARE-IN-TRIANGLE with β < n_u + n_v; NOTCH-NARROW; the
  separating normals form one arc).  A277's MUTUAL case (N) is empty; in a FLOAT2 corner T_u(C), T_v(D) are blocked by squares
  outside {C, D}.  `no_float2.md` §0; Lean `float_slope_core`; A278.
- s.2.1 [T] **SHADOW-CELL** — a wall-touching cell T of any pose with int T ∖ int D inside the shadow of an obstacle set O ∋ D
  (points no unit square interior-disjoint from O covers) and missing O ∖ {D} is met by D alone in every packing ⊇ O; P1 lands D.
  Disc test: dist(T ∖ int D, K_outer) > 1/√2.  **NO-FLOAT2 ⟸ L** (four squares).  Lean `shadow_cell_core`; A278.
- s.2.1 [T] **Cor. 2.2 / SWEEP** — with M(B) = {C, D} no wall cell disjoint from B is met by ⊆ {C, D}; D lands by a slide in any
  direction between the C–D and Y–D separator angles unless the Y–D separators are all shallower ((NEST)).  A278 parts 2, 6.
- s.3 [T-computed] **A277's Y-poke witness lands** — flat floor cell [0.486, 1.486] × [0,1] met by D alone, shadow margin 0.0319
  (`cell278`); also by SWEEP (Y→D 77.2° > C→D 12.9°).  No normal-form FLOAT2 corner on disk (as A277 said, now exact).
- s.6 [C] **NO-FLOAT2** — = L on 10 (12) parameters; residual satisfies (NEST) η₊ < α₋ ≤ α₊ < ξ₋ (Y UNDER a high D, C at the
  wall); certificate designed (prune / cell / shadow by cores), naive price > 10³ CPU-h, not launched.  Lean axiom `float2_local`.
  [C] **BL-CAP-2(A, C)** — S1–S4 [T] (misses lie below / left of lines through O; floor-sector centres q_y ≤ 1.4385 at ψ ≥ 0;
  side-by-side misses force one into [0, 1.4385] × [0, 2.15]); no hand proof; cert277 --fam jam (5 params, 3–100 CPU-h).
- s.5 [F] **the gloss "X misses B iff y_X ≥ 1 − cos φ_X"** (s.1 JAM entry, `no_jam.md` §1) — the LOWEST point of X must be ≥ 1
  (X ⊆ {y ≥ 1}); the leftmost vertex is then at height ≥ 1 + cos φ_X.  H1 and `float2_room.md` have it right.  A278 part 1.
- s.8 5d — unchanged: two CAP-2 statements [C]; NO-FLOAT2 would delete `bl_cap2_float2` and is itself [C] (A278).

## 12. APPENDS — A279 (2026-09-24), THE NEST RESIDUAL (`nest_residual.md`; parts `attempts/A279-nest-residual/notes/`)

- s.2.3 [T] **NOT-BOTH, D HIGH** — under (NEST) D's parallel edge lines (angle θ_D) are not both separators (Y beyond the lower-right
  one gives η₊ ≥ θ_D, C beyond the upper-left one α₋ ≤ θ_D); Y's top vertex under D's lower-right edge forces h_v(D) ≥ 1 − sin θ_D
  and h_u(D) < 1 − sin θ_D + sin θ_D tan θ_D.  Lean `nest_not_both_edges`; A279 part 2.
- s.2.3 [T] **(Σ), (Σ′)** — inscribed-disc centres across the C|D and D|Y separators: (m_Y,x − m_C,x) tan η + (m_D,x − m_C,x)(tan α −
  tan η) > sec α + sec η − 1/2 − 1/√2 ≥ 0.793 (C below 1, Y on the floor); every shallow nest is impossible (tan α > 0.95 at η → 0;
  page panel (b)).  Vertex form: h_v(D) ≥ 1 − (cos a + cos θ_D) tan η, h_v(D) < 1 − w_D + (h_u(D) + cos θ_D) tan α.  Lean `sigma_core`,
  `sigma_prime_low`; A279 part 3.
- s.2.3 [T] **(WEDGE), FLAT-C** — C between the wall and the steep separator: h_u(D) ≥ 1/2 + 1/(2 sin α) + (h_v(D) + cos θ_D − 1 −
  w_C/2) cot α, so h_v(D) + cos θ_D < 1 + w_C/2; a flat C at height y₀ < 1 forces D's left vertex under its bottom edge: h_u(D) ≥ 0.70,
  h_v(D) < 1 − cos θ_D, then η > 18° (θ_D ≤ 60°).  Lean `flat_c_core`; A279 part 3.
- s.2.1 [T] **the cells to test in NEST** — flat floor cells fail iff x_L(Y) < 1 + sup I(C); SWEEP is empty; N_Y := Y − sec a·e_x (Y's left
  normal cell, (E1); inside the container iff x_L(Y) ≥ sec a) lands D iff C, X miss it; N_X := X − sec φ_X·e_y (inside iff X_low ≥ sec φ_X)
  lands C iff D, Y miss it.  [T-computed] on A277's witness N_X meets D (0.044), N_Y is outside the container.  A279 part 2.6.
- s.2.2 [T] **count chase** — FAMILY-STUCK with M(B) = {C, D} forces third meeters of c01 = [0,1]×[1,2] and c10 = [1,2]×[0,1] (P1⁺,
  Π = {B, c01}, {B, c10}); in the 4-square model X_low, x_L(Y) ∈ [1, 2).  "Y meets B" is NOT forced by (Σ)/(WEDGE).  A279 part 2.5.
- s.4 [M] **nest279** — two-stage search (NEST feasibility over the 4-square model, then any-pose cells), running at exit, self-committing
  (`attempts/A279-nest-residual/results/nest279.jsonl`); two earlier runs stuck on an optimiser plateau are kept as [F]-evidence rows.
  No NEST quadruple in hand; A277's `float277` never explored the NEST end (its optimum is a boundary).
- s.6 [C] **NEST-emptiness** — "no FLOAT2 quadruple satisfies (NEST)" would prove the P1-SENSE 4-square statement (every FLOAT2 corner
  has a sweep or normal cell met by D or C alone among the four), NOT L: a sweep cell's part outside D need not be in the shadow.
  Cheapest certificate: A278's tree with (NEST), (Σ), (WEDGE), FLAT-C as monotone prunes; 2-D slice bench first.  A279 part 3.4.
- s.5 [F→fixed] the gloss "X misses B iff y_X ≥ 1 − cos φ_X" is corrected in s.1 and `no_jam.md` §1 (A279).
- s.8 5d — unchanged: two CAP-2 statements [C]; `float2_local` [C] stands; NestResidual.lean adds no axiom (A279).

## 13. APPENDS — A280 (2026-09-24), THE DROP LEMMA AT STEEP C (`attempts/A280-drop-steep/notes/drop280.md`)

- s.5.3 [F→diagnosed] **"A273's OPEN layer at θ ≥ 25° is a weak drop test or a miss"** — neither: every sampled OPEN
  leaf is OUTSIDE H1–H3 (X wholly above T_u, exact area X ∩ T_u = 0, dip D ≤ 0.004 < (D-low) 0.136–0.184).  A273's
  `prune4` omitted H2's "int X meets int T_u" and Lemma LOW.  c6_2 10/10, c7_6 191 729/191 732, c8_3 189 943/189 949
  OPEN leaves pruned by DLOW; the rest are big boxes left by the 400k cap.  `diag280`; A280 §0.
- s.4 [M] **drop slack at the open leaves** — negative everywhere (−0.00006 … −0.0002 on the DLOW slivers, −0.017 …
  −0.32 at the big boxes): no counterexample to the DROP LEMMA at steep C.  Two ZERO-MARGIN limits of the drop lemma,
  both outside H1–H3: D → 0 with X above T_u; h_u → 1 on the (D-low) boundary (q = (½, L_h) at the wall, the unit
  square between the wall and C's left vertex, slack −0.0012 at h_u 0.9999) — excluded by LOW + the open box
  (h_u ≤ 0.854 at θ = 40°).  Any drop-type tree must prune with H2 and LOW.  A280 §0, §4; page (c).
- s.2.3 [T] **DLOW, SEP, LOWF** (box prunes) — (D-low) D ≥ (c − sin φ) tan(min(θ, φ)); separating axis X | T_u;
  LOW full range (F4): L_h ≥ LOWB(θ) = min(1/√2 + tan(45° − θ/2), min_α G(α, θ)), G = cos α + c − s + (c + s − 1) tan α
  (case (c) is prose in (F4); Lean `lh_gt_one_steep` proves only G > 1) — LOWB 1.344 / 1.284 / 1.228 / 1.173 / 1.109
  at θ 25 / 30 / 35 / 40 / 45°.  `prune280`, `verify280` (mpmath.iv); A280 §2.
- s.3 [T-computed] **tree280 + verify280 bench** — c6_2, c7_6, c8_6, c8_3, c5_4 CERT in 51–327 boxes (≤ 1 s) and
  verify280 PASS (coverage, 0 disagreements) vs A273's 400k boxes / OPEN; `_bench` files.  The run over the 29 steep
  cells not CERT in index273 is LAUNCHED gated on A273's chain (`run280.sh`, ~0.1–0.3 CPU-h, commit per cell).
- s.5.4 [erratum] the brief's strengthening (LEFT + height split) — LEFT is already Γ (P1); the chord conditions of the
  height split are implied by the disc (central symmetry); the missing pieces were prunes.  Sound further option, unused:
  the quarter-turn orbit of p about q lies in int Q (drop → conv(D(q, ½) ∪ orbit)).  A280 §1, §3.
- s.8 5b — STRIP₂-IN-JAM [T on the corner (A276) + T-computed outside it: A273's CERT cells + A280's steep cells when
  run280 lands] + `pair3`; the ring route (U3)–(U6), (U8) is not needed at steep C.

## 14. APPENDS — A281 (2026-09-28), CORNER COST (`docs/proofs/corner_cost.md`; parts `attempts/A281-corner-cost/notes/`)

- s.1 [T] **Wall ROLES.**  A PAIR corner is class F (one flat + one poker) or T (both tilted); each corner puts one meeter on
  each of its walls, so a wall carries a pair from {Φ (flat), Π (poker), τ (T-meeter)}: six wall types ΦΦ, ΦΠ, ΠΠ, Φτ,
  Πτ, ττ; a corner is T, Ff (flat on its outgoing wall) or Fw.  Exclusive along-wall extents: Φ: 1 + d; Π: min(y_L, y_R)
  ≥ 1 + min(ψ(θ), 1 − cos θ) > 1 (reach y_T ≥ 2); τ: d + min(cos θ, sin θ) (Lemma EXT).  A281 part 1.
- s.2.4 [T] **SIDE per wall type** — ΠΠ dead on W (TWO-POKERS); ΦΠ: s ≥ 3 + d + (1 − sin θ_f)(sec θ_f − 1) (= FLAT-ABOVE
  read from the flat: the flat sits within s − 3 of its corner, never meets the poker's slot; the poker always meets the
  flat's slot); ΦΦ: s ≥ 2 + d + d′; Φτ: s ≥ 1 + d + d′ + w(θ′); Πτ: infimum ≈ 3 (no window bound).  [T-computed] exact
  4-square witnesses of the five live types at 3.82 and ŝ (margins 0.06–0.10; `wall281_pairs.json`).  A281 part 2, 7.
- s.2.4 [T-computed] **A poker's slot is supplied by a T neighbour's wall meeter of EITHER global sense** (frame tilt 18.4°
  opposite sense, margin 0.051; 45.8–46.2° same sense, 0.005–0.012; the row continuation) — **erratum to A248** ("on the
  window every type-F poker's slot is met by an interior square": true only with a type-F wall neighbour; A248's f = 4
  corollary unaffected).  The flat never supplies it (sup 0, the y₀ = y_T limit).  A281 part 3, 7; page (b).
- s.2.2 [T] **The f-table** (15 D4 orbits of corner classes; `count281.py`; Lean `Statements/Open/CornerCost.lean`:
  `allF_is_pinwheel`, `notches_of_noPiPi`, `hasT_or_pinwheel` by `decide`; `realised_has_T`, `no_allF_realised` over the
  bridge axioms `no_PiPi_window` [T-prose] and `notches_le_three` [M]).  SIDE (no ΠΠ wall) kills 3/4 orbits at f = 4, 2/4
  at f = 3, 1/5 at f = 2, none at f ≤ 1; the room count (FAMILY-STUCK dominoes + ninth square + PROJECTION sharing) needs
  h ≤ 2 free squares everywhere and kills NOTHING (A250 in role form); SEPARATE-NOTCHES [M] kills exactly the f = 4
  pinwheel (h_sep = 4 > 3, A248); normal-form locks (ΦΠ, Φτ walls are never rows) need ≤ 2.  Ten orbits survive side +
  count, every one with a T corner except the pinwheel; f = 0 survives with h = 1 = the ribbon poker.  What closes the
  survivors is ROOM on the (hybrid) ring, not any count.  A281 part 6.
- s.2.6 [T-cond] **F3 torque** — the flat has no FORCED wall torque (edge pressure supplies any torque in [−W/2, W/2]); the
  poker (TWO-CONTACT) with only {wall, own flat, a vertical top load} is torque-balanced only if d = sin θ + cos³ θ ≥ 0.98
  (A239 LEVER), which the ΦΠ side bound d < s − 3 ≤ 0.877 forbids: in the all-F pinwheel every LOADED poker has an interior
  contact (or the far floor meeter at R).  With a T neighbour on the poker's edge the lever arm is free: nothing.  T3: LEVER
  is type-F only; the C2 type-T ring has loop gain 1; CHAIN is met by the walls — torque adds nothing to T2.  LOCKED
  (A233) ≠ LOADED: every torque line is conditional on the k ≥ 1 rows AND on load.  A281 part 4, 5.
- s.5.4 [precision] "ONE-SENSE on W certified by A261 + the cube" omits the slab [C]; "LEVER ⟹ s > 4" is for type-F crowds;
  "F costs one interior holder per corner" holds only for the pinwheel (part 8 lists ten errata).
- s.3/s.4 [T-computed]/[M] **8-square outer structures** of the orbits (`wall281_rings.json`, part 7 table 7.2; rows still landing at exit -- a later agent reads them; `finish281.sh` commits them): the all-F
  pinwheel EXISTS on all of W (C4 witness d = 0.662, θ = 14.2°, y_V = 0.948 at ŝ; margins 0.045 / 0.052) — A248's f = 4 kill
  is a HOLDER kill, not a side kill; Ff/Ff/Ff/T exists (0.047 / 0.054); orbits with a ΠΠ wall fail (−0.0003 … −0.0004).
