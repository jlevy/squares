# NORMAL-RING — what a family-stuck packing looks like after LEXICOGRAPHIC normalisation: the pinwheel of four common-tilt pairs, its exact domain D, the LOCKED wall, and the least side of every other pinwheel of rows — A258, 2026-09-21

The coordinator's reading (A258 BRIEF): VALUE-WLOG lets us maximise any potential; every exchange lemma becomes a
property of the maximiser; after W exchanges onto T each wall of A249's ring carries a ROW OF TWO; so the normal ring
is a pinwheel of four common-tilt pairs, 8 coordinates + s.  This note proves the normal-form theorem, writes the
family and its domain exactly, tests the reading on the corpus and by an exact LP scan, and says what is false.
Every lemma is stated for m = ⌈√n⌉, s ∈ (m−1, m), ε = m − s where it can be.  Tags: [T] proved, [T-computed] exact
finite computation, [M] measured, [C] conjecture, [F] false as stated (witness).  Sources: `common_sense.md` (A255),
`ring_swap.md` (CELLS), `peel.md` (A254), `type_t_chase.md` (A249), `corner_chase.md` (A248), `mintilt253.md`.
Family file for A259: `attempts/A258-normal-ring/notes/family258.md`.  Code `attempts/A258-normal-ring/code/`
(`geo258`, `dom258`, `side258`, `scan258`, `norm258`, `poker258`, `retreat258`, `exact258`, `pages258{,b}`, `test258`, `run258.sh`); results
`attempts/A258-normal-ring/results/`; pages `docs/residue_map/campaigns/A258-normal-ring/`; Lean
`Statements/Open/NormalRing.lean`.

## 0. Verdict

> **[T] NORMAL-FORM (any n, any s).**  Potential Φ = (Φ₁, Φ₂, Φ₄, Φ₃) lexicographically: Φ₁ = number of
> wall-touching squares, Φ₂ = the sorted vector of maximal common-tilt wall-row lengths, Φ₄ = −#{(border cell,
> non-toucher) incidences} (the RETREAT term, coordinator's addendum), Φ₃ = −Σ (counter-clockwise wall coordinate of
> the touchers).  A maximiser exists among the packings at side s and satisfies **P1** (touch-normal), **P2**
> (row-normal MODULO LONGER ROWS), **P2′** (a free square that blocks a normal cell has nowhere else to go), **P4**
> (RETREAT: the free squares cannot be re-posed, singly or jointly, to meet fewer border cells — a poker is HELD),
> **P3** (every row is blocked against the clockwise slide).  Lean: `exists_lex_max`, `exists_normalForm`.
>
> **[M] A poker that is not held does not count, and nothing can hold it** (§2.1).  The seated poker meets its
> wall's slots by a sliver of depth 1 − cos φ (areas 2·10⁻³ / 2·10⁻⁴ at 14.5°, ŝ); slid by sec φ − 1 along the row's
> edge direction it is still a packing (the RING never blocks that slide: 20 of 20 tight rings, 4 sides) and the
> Hall minimum drops 1 → 0.  P4 therefore demands a FREE square in its way — and beside a seated poker no unit square
> fits at all (sup gap −0.10 … −0.17 at 3.82, −0.07 … −0.15 at ŝ, −0.006 … −0.07 at 3.99; 13 rings).
>
> **[T] The family.**  The pinwheel of four common-tilt PAIRS of one sense, parameters (a_w, φ_w) + s, with the exact
> domain **D** (closed forms; common tilt: a sin φ + b cos φ ≥ 1, a + b = s − sec φ − cos φ − sin φ, a, b < 1) is a ring:
> eight squares, a packing, all twelve cells doubly met; rows of two with a, b < 1 are row-normal; the bare ring has
> Hall minimum 0 on the 16 maximal families only; the SEATED poker (the row's tilt, standing in the tooth) makes it
> family-stuck iff the tooth reaches the ribbon.  Least side of the family: **1 + sec φ + cos φ + sin φ + tan(φ/2)**
> (→ 3 as φ → 0): it exists on the whole window, tilts ≈ (0°, 28°) at ŝ.
>
> **[M] Corpus: the reading is RIGHT for the ring and WRONG for the ring + poker.**  46 corpus rings (A253's 44
> ring + poker rows, A255's 2 controls).  Poker removed: W → T is available on 4 of 4 walls in 46/46, and **46/46
> land in D**; 46/46 carry a seated poker again (Hall minimum 1) under one of the two normalisations of a wall
> (W → T or s₁ → T′).  Poker KEPT: **on 43 of 44 rings the poker's wall is LOCKED** — its normal cell is met by W AND
> the poker, |M(T)| = 2 — so the ring + poker is already row-normal with an OPEN PAIR on that wall.  **[F] "every
> normal-form family-stuck packing is the pinwheel of four pairs"**: the normal form is the HYBRID ring (each wall a
> row of two, or an open pair locked by a free square that P2′ says is itself stuck).
>
> **[M] Every other pinwheel of rows needs side ≥ 3.9298 > ŝ** (`side258`: for fixed tilts the least side is an
> exact LP in (a_w, s); grid 11⁴ per-wall tilts + polish): mixed senses + + + − **3.9298** (tilts 14.0, 14.0, 14.0 |
> 10.9 — **a drawn counterexample to ring-level COMMON-SENSE on the stretch window (ŝ, 4)**, not on [3.82, ŝ]);
> + + − − 3.9767; + − + − 3.9484; a FLAT row (type F in normal form) **3.9347** (A248's s* = 3.93424 to 5·10⁻⁴); a row
> of three 3.9814 (flat) / 4.0126 (tilts ≥ 3°).  [T] at common tilt: the alternating pattern and the row of three
> need side > 4 (Lean `alt_side_poly`, `row_three_poly`).  **What the brief had wrong: §6.**
>
> **Plainly.**  NORMAL-RING(11) is **[C]** (hybrid form, §3.5); on [3.82, ŝ] its competitors inside the class
> "pinwheel of rows" are excluded [M] with margin 0.053 in the side.  FAMILY-STUCK-EXIST(11), k0_00: **unchanged**.

## 1. Normalisations and the normal-form theorem  (task 1)

**1.1 The exchanges / motions available [T]** (all keep the side: VALUE-WLOG, `common_sense.md` §2.1).
(E1) NORMAL-CELL (A255): T = s₁ ± sec φ · e, |M(T)| ≤ 1 ⟹ the meeter moves onto T; φ = 0 is the band cell.
(E2) TOUCH-CELL: any unit cell T ⊆ [0,s]² (any pose) touching a wall with M(T) ⊆ {D}, D a non-toucher (or M(T) = ∅
and some non-toucher exists) ⟹ D → T (Lemma CELLS, |Π| = 1); Φ₁ rises.
(E3) PAIR-CELL: T an end cell of a row R with M(T) = {W, F}; T₂ ⊆ [0,s]² any unit cell interior-disjoint from T and
from every square other than W, F ⟹ W → T, F → T₂ (Lemma CELLS, Π = {T, T₂}, |M(Π)| ≤ 2).
(E4) ROW-SLIDE: a maximal row translated along its wall, while the swept region is free.
(E5) RETREAT: non-touchers F₁..F_j (j ≤ 3 at n = 11) re-posed onto unit cells T₁..T_j ⊆ [0,s]², pairwise
interior-disjoint and interior-disjoint from every other square (Lemma CELLS, M(Π) ⊆ {F_i}); in particular any
collision-free motion of a free square, alone or together with the free squares above it.
NOT available: changing a row's tilt, or equalising tilts ACROSS walls.  Within a wall the tilt IS equalised by (E1):
W lands on T at s₁'s tilt.
**1.2 Theorem NORMAL-FORM [T].**  *Among the packings of n unit squares at side s (if any) there is a lexicographic
maximiser P\* of (Φ₁, Φ₂, Φ₄, Φ₃), and:*
**P1** if P\* has a non-toucher, every wall-touching unit cell T ⊆ [0,s]² is met by a toucher or by ≥ 2 squares;
**P2** for every maximal row R and end cell T ⊆ [0,s]²: |M(T)| ≥ 2, or M(T) = {D} with D in a row STRICTLY LONGER
than R;  **P2′** if M(T) = {W, F}, F a non-toucher, W in a row no longer than R, then no unit cell T₂ ⊆ [0,s]² is
interior-disjoint from T and from all squares other than W, F;  **P4** no re-posing (E5) of non-touchers onto
non-touching cells lowers the number of (border cell, non-toucher) incidences — in particular **every unit cell
T₂ ⊆ [0,s]² met by no square other than a free square F meets at least as many border cells as F**: a free square
in a slot is HELD there;  **P3** every maximal row, moved rigidly by −εe
(towards its wall's start corner), meets another square or leaves the container, for every small ε > 0.
*Proof.*  Existence: Φ₁, Φ₂ are bounded integers — a lexicographic maximiser of two bounded ℕ-potentials exists by
the encoding Φ₁(B₂+1) + Φ₂ (Lean `exists_lex_max`, from `exists_max_potential`); on their arg-max set (closed:
touching and "exact translate" are closed conditions, and the toucher set is constant along convergent sequences
there) Φ₄ is upper semicontinuous ("meets" is an OPEN condition, so the incidence count is lower semicontinuous)
and integer-valued, Φ₃ is continuous, and the packing space is compact [T-prose].  P1: (E2) raises Φ₁.  P4: (E5)
keeps Φ₁ (or raises it, if a T_i touches), keeps Φ₂ (non-touchers are in no row) and raises Φ₄.  P2: (E1) at an end cell of
R replaces R's length ℓ by ≥ ℓ + 1 and splits D's row (length ℓ′) into pieces of total ℓ′ − 1; Φ₁ does not fall (T
touches); if ℓ′ ≤ ℓ the multiset of lengths > ℓ is unchanged and one more entry is ≥ ℓ + 1: Φ₂ rises.  P2′: (E3),
same count (F is in no row).  P3: (E4) keeps Φ₁, Φ₂ and raises Φ₃.  ∎
**[F] `common_sense.md` §2.3, last line** ("a lexicographic maximiser of the sorted row-length vector normalises the
shorter rows simultaneously: same proof"): the proof fails when D sits in a LONGER row, and no potential repairs it —
rows (3,1) → (2,2) → (3,1) is a cycle of end-cell exchanges.  P2 is the true form.  **[T] at m = 4 the exception is
narrow:** rows have ℓ ≤ 3 (3 sec φ + w > 4); D in a row of three on the SAME wall is impossible (3 + 1 > s), on the
OPPOSITE wall impossible (2√2 < s), so D is the corner-end square of a row of three on an ADJACENT wall — which needs
side ≥ 3.98 [M, §3.3].  Under the second horn of the value argument (EVERY packing at side s is family-stuck) each
exchanged packing is family-stuck too.

## 2. The normal ring and its domain D  (task 2, first half — details and formulas: `family258.md`)

Wall frames (t, d), walls walked counter-clockwise from their START corners.  Row of two of sense +, tilt φ, start
offset a: Q1 = (a+g,0), (a+w,g), (a+c,w), (a,c); Q2 = Q1 + (sec φ, 0); end offset b = K − a, K = s − sec φ − c − g.
**[T]** a, b < 1 ⟺ the row's ends meet both boxes; then both end cells leave the container (b < 1 < sec φ): the row
is row-normal.  Under the row: a SEALED triangle (legs 1, tan φ).  Above it: the TOOTH, a right-angled notch with
apex (a + sec φ, cos φ), depth 1 − cos φ below d = 1.  **Corner condition [T]** between the A-type (start of wall k:
a, α) and the B-type (end of wall k−1: b, β): max(E_A, E_B) ≥ 0 (`family258.md` (D4)); common tilt:
**a sin φ + b cos φ ≥ 1**.  [T] the B-type's second axis never separates when a < 1; [M] the A-type's second axis
never decides (0 of 60 000).  **D** = (D1)–(D4); **D′** drops the slot cut (D3).  For fixed tilts D is a union of ≤ 16
polytopes in the offsets (`dom258`).  **Least side [T]** (sum the four corner conditions with b ≤ 1):
s ≥ 1 + sec φ + cos φ + sin φ + tan(φ/2) at common tilt, attained by the C4 ring (LP and formula agree to 10⁻¹⁴).
**D_tight [T]**: four corner contacts ⟹ (common tilt) C4 and explicit, a = (Kc − 1)/(c − g), b = (1 − Kg)/(c − g): two
coordinates (φ, s); P3 puts the maximiser there unless a free square blocks a slide.
**The ninth square [T].**  Every cell of the bare ring has exactly two ring meeters; |M(Π)| − |Π| = j − k + Σ_{boxes}
#(walls without a chosen slot) ≥ 1 unless Π is maximal (j = k = 4), where it is 0.  So the ninth square meets a BOX
(a third box meeter) or BOTH slots of one wall, i.e. (convexity) has interior points in a ribbon [s−2, 2] × [0,1].
Inside the ribbon the band is Q1 ∪ Q2 ∪ sealed triangle ∪ TOOTH ∪ the thin wedge under Q2 (part of the next corner's
pocket), so a ribbon poker has a vertex in the tooth: **a + sec φ + cos φ tan(φ/2) > s − 2 and a + sec φ − sin φ
tan(φ/2) < 2** [T necessary]; the SEATED poker (tilt φ, lowest vertex at the apex) realises it [T-computed per ring].
[M] a third box meeter: none on the C4 slice (best depth −0.017 … −0.17 over 64 rings, `poker258`).
**2.1 The poker must be HELD (P4; `retreat258`, `exchange.svg` (c), (d)).**  [T] F's free translations relative
to Q1, Q2 are the closed cone spanned by the row's edge directions u = (cos φ, sin φ), v = (−sin φ, cos φ); along v
its lowest vertex leaves the band d < 1 after sec φ − 1 (0.033 at 14.5°) — and then F meets no border cell, so
**ring + retreated F is NOT family-stuck** (Hall minimum 0 [T-computed per ring]).  [M] no ring square obstructs
that slide (tight C4 rings, 5 tilts × 4 sides: path gap 0 = sliding contact only).  So in normal form the v-slide is
blocked by a FREE square G with gap(F + τv, G) < 0 for some τ ≤ sec φ − 1, G itself not re-posable jointly with F;
by the teleport form of P4, **P\* ∖ {F} leaves no room for a unit cell in the core [1, s−1]²** either.  [M] room for
ANY tenth square beside the seated poker: none (numbers in §0).  This is A252/A253's "residual centre set empty",
now as a consequence the normal form REQUIRES to fail: **HELD-POKER** (`family258.md` §6) is the statement for A259.

## 3. Classification at m = 4  (task 2, second half)

**3.1 Row lengths [T].**  ℓ ≤ 3.  A single toucher cannot meet both end boxes (a + b = s − w(φ) > 2).  So a wall whose
two boxes are served by its own touchers carries a row of two, a row of three, or an OPEN PAIR (s₁, W not a row).
**3.2 ROW-THREE.**  [T] common tilt: a + b = s − 2 sec φ − w < 1, and the END box needs the next wall's A-type above
it: b > tan(45° − φ/2); 2 sec φ + cos φ + sin φ + tan(45° − φ/2) − 4 = 4u²(1 − u + 2u²)/((1+u²)(1−u²)) > 0,
u = tan(φ/2) (Lean `row_three_poly`).  [M] any tilts: least side 3.9814 with a FLAT row of three, 4.0126 with all
tilts ≥ 3°; two or more rows of three: > 4 (least 4.0004, in the flat limit; 4.030 with tilts ≥ 3°).
**3.3 Mixed senses (N4 at ring level).**  A mixed corner (both squares present their high vertex, or both their low
vertex) costs, at common tilt, **max(a + b tan φ, b + a tan φ) ≥ cos φ + sin φ** — both offsets ≥ (w−1) cot φ → 1
as φ → 0, against b ≥ 1 − aφ at a pinwheel corner.  [T] ALT-SIDE: + − + − at common tilt has a = 1,
b = (w−1) cot φ and least side 1 + cos φ (w − 1)/sin φ + sec φ + w, which exceeds 4 by
u(1 − 2u + 6u³ − u⁴)/((1+u²)(1−u²)) (Lean `alt_side_poly`).  [M] common tilt, + + + − and + + − −: least side
4 + φ²/2 + … > 4 at every tilt.  **[F] with PER-WALL tilts** (`side258`): + + + − exists from **s = 3.9298**
(tilts 14.02°, 14.02°, 14.02° | sense − at 10.94°; offsets 0.863, 0.827, 0.687, 0.740; verified: a packing of eight,
boxes doubly met; `excluded.svg` (d) at s = 3.95).  It is NOT all-ADJ — with the slot cut (D3) the same tilts are
infeasible up to 3.99 (−0.0045), which is why A255's all-ADJ sense search found 0 of 84.  So **ring-level
COMMON-SENSE holds on [3.82, ŝ] [M] and fails on (3.93, 4) unless the slots are ring-served.**
**3.4 Type F in normal form.**  A flat toucher is a row of sense 0; NORMAL-CELL gives the band cell; a flat row of two
[δ, δ+2] is row-normal iff δ > s − 3 and then covers both slots of its wall.  Its two end pokers are the END of the
previous row and the START of the next, so a type-F corner is the boundary φ_w = 0 of the row families.  [M] least
side with one flat wall **3.9347** (others ≈ 14.9°; two opposite flat walls 3.9469; adjacent 3.9370; a flat wall
beside a row of the other sense 3.9797) — TWO-POKERS' s* = 3.93424 recovered from a different configuration (the
two pokers sit on the two ADJACENT walls).  **On [3.82, ŝ] the normal form kills type F outright [M]**; on (s*, 4)
it does not (N3 stays open there).
**3.5 The LOCKED wall — the honest statement.**  **Conjecture NORMAL-RING(11) [C].**  *Every normal-form
family-stuck packing of eleven squares at s ∈ [3.82, ŝ] contains a HYBRID NORMAL RING: eight wall touchers, two per
wall, of one sense, the first and last of each wall meeting the boxes, each wall either a common-tilt ROW OF TWO
(then (a_w, φ_w) satisfy D′) or an OPEN PAIR whose two normal cells are each met by a free square (a LOCK); the other
squares are free, at least one of them a tooth poker or a lock.*  [M] 43/44 corpus ring + poker rows have exactly one
lock, the poker (shift W − T along the wall 0.0005 … 0.13).  Known [T]: §3.1; P2′ (after W → T the lock has no room
anywhere).  Open: (O1) TOUCH-NORMAL — box meeters touch walls (P1 gives only: a floating meeter is poked under from
every wall side); (O2) the two meeters of a box lie on its two walls; (O3) the [M] bounds of §3.2–3.4 as
certificates (4 tilt coordinates, an LP per box; margin 0.053 in the side at ŝ; not priced — no benchmark taken);
(O4) locks: either ROOM on the hybrid family (8 + 2r coordinates, r ≤ 3 locked walls, open gap ≤ K − a_min − b_min ≈
0.13) or an unlocking argument.

## 4. General m  (task 4)

**NORMAL-RING(n) [C]:** four rows of m − 2 of one sense, K = s − (m−3) sec φ − w(φ), a + b = K, a, b < 1, the SAME
corner condition (it is a two-square statement) — plus locked walls.  **[T] for all m:** NORMAL-FORM P1–P3; a row of
m − 2 with a, b < 1 is row-normal (b < 1 < sec φ); the corner closed forms; least side (m−3) sec φ + w + 1 + tan(φ/2)
→ m − 1; **the tight normal ring's flush limit is the TIGHT PINWHEEL for every m** (a → 1 − ε, b → 1): a row has no
internal gaps, so A254's wall slack (its [F] for m ≥ 5) lives only in rings that are NOT row-normal — normalisation
removes it wherever no lock intervenes.  **m = 4 only:** ℓ ≤ 3, "opposite walls never interact", §3.2–3.4's numbers,
the lock statistics.

## 5. The chain  (task 5)

packing at s ⟹ [T, Lean `normal_ring_value`] a packing that is not family-stuck (the k ≥ 1 classes) or a NORMAL-FORM
family-stuck one ⟹ [C `normal_ring`] it contains a hybrid normal ring with a HELD poker ⟹ [A259: NORMAL-ROOM on D′
and on the locked walls (O4) — or only the weaker HELD-POKER: no unit square fits in the pocket in the way of a
tooth poker's retreat] ⟹ FAMILY-STUCK-EXIST(11) (Lean `normal_excludes_value`: a theorem with the room as a
hypothesis).  With NORMAL-ROOM ≤ 1 on D′ only: lift the r locks, normalise, 3 − r ≤ 1 ⟹ **r ≥ 2 locks** — the
residual case is two free squares each locking a wall + one more, 12 coordinates.

## 6. What the brief had wrong

1. "After W exchanges onto T each wall carries a row of two": true for the bare ring (46/46), **false with the poker
   present** (43/44 locked walls).  2. "Rows of three cannot pinwheel below 4": true at common tilt [T]; with a flat
   row of three the least side is 3.9814 [M].  3. "Mixed-sense pinwheel of pairs cannot close": **false above 3.9298**
   (per-wall tilts), true on [3.82, ŝ] [M].  4. "8 coordinates — not 17": 8 + 2r with r locks.  5. `common_sense.md`
   §2.3's simultaneous row-normality is false as stated (P2).  Correct: the span arithmetic (2.25 at 14.5°), the end
   cell leaves the container, equal tilts are NOT forced (D allows a tilt spread of 24° at 3.82 [M]), rows ARE pushed
   to a corner (P3).

## 7. Lean, reproduce

`Statements/Open/NormalRing.lean`: theorems `exists_lex_max`, `exists_normalForm`, `alt_side_poly`, `row_three_poly`,
`normal_ring_value`, `normal_excludes_value`; axioms [T-prose] `touchPotential_le`, `rowVecPotential_le`,
`normal_form_step`; axiom [C] `normal_ring`; 0 sorry.  Reproduce: `bash attempts/A258-normal-ring/code/run258.sh
test|dom|norm|poker|pages` (≤ 10 min each), `side` (detached, ≈ 1 h, resumable, `logs/STOP`).
