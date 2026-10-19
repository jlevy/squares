# PEEL — the n-general ring + poker, and the onion inequality s ≥ 2 + s(n − 4(m − 2)) — A254, 2026-09-20

The PI (2026-09-20): *"I suspect in the general form ONLY-RING is true for all non-trivial side lengths,
s < ⌈√n⌉."*  The coordinator: HOLE-ONE (A253) is the m = 4 case of a recursion — peel the ring off, the rest lives in
a square of side s − 2.  This note (i) defines the border-cell system, FAMILY-STUCK(n), the ring and ONLY-RING(n) for
every m = ⌈√n⌉, s ∈ (m − 1, m), ε := m − s; (ii) proves PEEL where it is a theorem and says exactly where it is not;
(iii) tabulates every n ≤ 100 below ⌈√n⌉; (iv) says what it does for n = 11; (v) lists what in the brief was wrong.
Tags: [T] proved, [T-lit] literature, [T-computed] exact finite computation, [M] measured, [C] conjecture, [F] false.
Sources: `mintilt253.md` (A253: HOLE-ONE, NOTCH-NARROW), `centre_disc.md` (A252), `type_t_chase.md` (A249),
`family250.md` (A250), `ring_swap.md` (A222 CELLS), `ring_capacity.md` (A236: band / core / straddler, TILT-BAND,
BAND-FLUSH, NO-CLOSURE), A226 survey, `docs/papers/{nagamochi2005_R37,ellsworth_squares_in_squares}.txt`.
Code `attempts/A254-peel/code/` (`cells254`, `table254`, `search254`, `summarise254`, `pages254`, `test254`,
`run254.sh`); results `attempts/A254-peel/results/peel254.md`; pages `docs/residue_map/campaigns/A254-peel/`;
Lean `Statements/Open/Peel.lean`.

## 0. Verdict

> **[T] PEEL-0 (any n, any s; Lean `core_fits`, `peel_side_bound`).**  The CORE squares of a packing at side s
> (those inside [1, s−1]²) translate to a packing at side s − 2.  So a packing with k core squares has
> **s ≥ 2 + s(k)**.  With BAND-COUNT (§2.1: at most 4(m − 2) band squares at s ∈ (m−1, m), s > 2 + √2) a packing
> with NO straddler has s ≥ 2 + s(n − 4(m − 2)).  The tight flush pinwheel — four 1 × (m−2) wall blocks, pocket =
> hole [1, s−1]² ⊔ four isolated 1 × (1−ε) notches — is exactly this case; HOLE-ONE is m = 4 (n' = 3, s(3) = 2).
> This is A236's count with X = 0 straddlers: n ≤ m² − 7, against NO-CLOSURE's m² − 3 with X ≥ 4.
>
> **[T] but weaker off the tight pinwheel.**  For m = 4 the flush stratum of the all-ADJ ring family is EXACTLY the
> two pinwheels (Lemma LIMIT-UNIQUE, §2.4), so by upper semicontinuity of capacity there is τ₀ > 0, uniform on
> [3.82, 4 − η], with: every all-ADJ ring whose eight tilts are all < τ₀ has pocket capacity ≤ 1 (8 + 1 = 9 < 11) —
> on the whole 17-coordinate family, not only A253's common-tilt slice; τ₀ is NOT effective.  For m ≥ 5 the brief's
> "the flush limit is the pinwheel" is **[F]**: the flush stratum is a family (each wall keeps slack 1 − ε − b_w),
> pocket squares poke a corner into the mid-wall gaps (Lemma POKE: depth ≤ gap/2), and the theorem on the whole
> stratum is only **s ≥ (s(n') + m + 1)/2** (§2.3).
>
> **[C] everything that would make PEEL a tool:** ONLY-RING(n) (a family-stuck packing below m contains the ring) and
> MONOTONE-ROOM(n) (the pocket of a tilted ring holds no more than the hole of the tight pinwheel).  Lean
> `only_ring`, `ring_peel` [C] ⟹ `peel_excludes`.  Neither is proved for any n.
>
> **Table (36 values n ≤ 100 below ⌈√n⌉), verdict on the tight pinwheel:** THEOREM-WINDOW 6 (n = 5, 10, 11, 18,
> 19, 29: none anywhere below m, from proved values), THEOREM-AT-RECORD 3 (17, 26, 27: none at the record side),
> RECORDS-ONLY 26, EQUALITY 1 (**n = 84**, not 65), NOT-EXCLUDED 0.  **n = 11: nothing new is closed**;
> RING-POKER-RESIDUAL(11) is closed only on the non-effective neighbourhood {all tilts < τ₀}; k0_00 unchanged.

## 1. The border-cell system, FAMILY-STUCK(n), the ring, ONLY-RING(n)  (task 1)

**1.1 Cells [T-definition].**  Wall coordinate t ∈ [0, s] along each wall, depth [0, 1] off it.  Border cells: the
four corner boxes, and per wall the LEFT chain L_j = [j, j+1] and the RIGHT chain R_j = [s−j−1, s−j],
j = 1 … m−3: **8m − 20 cells** (m = 3: the 4 boxes; m = 4: A244/A250's twelve; m = 5: 20).  Chains stop at m − 3
because the perimeter family (`ring_swap.md` §1.4) uses per wall a cells from one end and m − 3 − a from the other.
**Conflicts [T]:** L_j and R_j' overlap iff j + j' ∈ (s − 2, s), i.e. j + j' = m − 2 (a NARROW ribbon
[j+1−ε, j+1], width ε) or j + j' = m − 1 (a WIDE overlap [j, j+1−ε], width 1 − ε); corner boxes conflict with
nothing; cells of different walls are disjoint for s ≥ 3.  ([T-computed] `cells254`: the SAT conflict graph equals
this prediction for m = 3 … 6; 4, 12, 20 conflicts at m = 4, 5, 6.)  The coordinator's description is correct.

**1.2 FAMILY-STUCK(n) [T-definition] and the count [T].**  A packing is FAMILY-STUCK when |M(Π)| > |Π| for every
family Π of pairwise interior-disjoint border cells (A250 §1, verbatim).  Maximal families: four boxes + per wall a
SPLIT a ∈ {0 … m−3} (cells L_1..L_a, R_1..R_{m−3−a}): (m−2)⁴ families of 4(m − 2) cells.  So family-stuck needs
**n ≥ 4(m − 2) + 1 = 4⌊s⌋ − 3** (A250 §2.1 is already this).  **The count closes for no n:** the least n with
⌈√n⌉ = m is (m−1)² + 1, and (m−1)² + 1 − (4m − 7) = (m − 3)² ≥ 0 (n = 5 = 4·3 − 7 at m = 3 is the tight case).
**[T-computed] the bound is attained at the incidence level** (`cells254.json`, m = 3, 4, 5, 6, explicit C4 pinwheel
ring at tilt 6°, pairwise SAT margin ≥ 0.025, all 15 / 1 295 / 65 535 / 3 111 695 admissible families enumerated):
every border cell is met by ≥ 2 ring squares (the mid-wall slots ARE served: L_j by touchers j, j+1; R by reach),
min(|M(Π)| − |Π|) = 0 for the bare ring (it teleports, Lemma CELLS), and = **1 with ONE abstract poker in ANY narrow
ribbon** (k = 2 … m−2), = 0 with a poker confined to a wide overlap.  m = 4 reproduces A250's 9.
**[T] why one poker, and where.**  A free square protects a maximal family only by meeting one of its cells;
the families are products of per-wall splits, so a poker set hits all of them iff on SOME wall it hits every
split.  Split a leaves the band interval (a+1, a+2−ε) uncovered (a wide overlap); so one poker suffices iff its
band footprint on that wall is not inside a single wide overlap — e.g. a corner in a narrow ribbon [k−ε, k]×[0, 1].
At m = 3 the poker is a fifth square meeting a corner box.

**1.3 The ring [T-definition].**  RING(n) at s ∈ (m−1, m): 4(m − 2) squares, m − 2 touching each wall (each exactly
one wall), all tilted, the first and last toucher of each wall meeting the corner boxes at its ends (every box
doubly met), every border cell met by ≥ 2 of them.  Common handedness is NOT part of the definition (A249's ring is
the C2 pinwheel σ = 00110011; `cells254` builds the C4 one).
Parameters: per toucher (θ, p) with p its lowest extent along the wall; the wall's slack is
s − Σ widths − a − b, a, b the end offsets.  [M] exists for m = 3 … 6 at 6° (above).
**Conjecture ONLY-RING(n) [C] (the PI).**  *Every FAMILY-STUCK packing of n unit squares at a side s ∈ (m−1, m)
contains a RING(n); its other n − 4(m−2) squares are ≥ 1 poker and free squares.*  Lean `only_ring`.

**1.4 Evidence.**  For: [T-computed] the minimum count 4(m−2)+1 is the ring + poker incidence structure for
m = 3..6 (§1.2) and A250's ILP says the same with NSS / TWO-FAR / SLOT-MET / 62 pair kills at m = 4; [T] TWO-POKERS
(A248) kills the type-F ring on [3.82, ŝ].  Against / open: [T-computed] A250 §2.3 — at n = 11 (not 9) every
structural minimum collapses (ADJ suppliers may be 0, three free squares may feed slots), so mixed and non-ring
structures are NOT excluded by counting; A249 §3.4 / A252 §5 leave them open; as s → m the narrow ribbons vanish
(ε → 0) and the wide overlaps become whole cells, so "one poker" degenerates.  [M] `search254` (A250's search
generalised: all families |Π| ≤ 2 + all maximal ones as penalty rows, full Hall re-check of every end point) at
n = 5, 10, 17 was launched detached on a small budget; rows land in `results/search254.md` — a failure to find is
not evidence of absence at this budget.  **ONLY-RING(n) is not claimed for any n.**

## 2. PEEL  (task 2)

**2.1 Lemma BAND-COUNT, general form [T].**  *s ∈ (m−1, m), s > 2 + √2: at most 4(m − 2) squares of ANY packing are
band squares* (no four-crowd hypothesis, unlike A236 §2.4).  *Proof.*  A band square is flush and touches a wall
(BAND-FLUSH).  A flush wall toucher whose interval meets (0, 1) or (s−1, s) meets that corner box; two flush
touchers meeting the same box from its two walls overlap unless they are the same (corner) square: [a, a+1]×[0, 1]
and [0, 1]×[b, b+1], a, b ∈ [0, 1), share (a, 1)×(b, 1).  So ≤ 4 band squares meet a corner box.  The others have
their intervals in [1, s−1], length s − 2 < m − 2: at most m − 3 per wall.  B ≤ 4(m−3) + 4.  ∎  Lean `band_count`
[T-prose axiom].  Sharp: the pinwheel, and the grid minus a row and a column.
**2.2 Theorem PEEL-0 [T] (Lean `core_fits`, `peel_side_bound`, `peel_no_straddler`: theorems, std axioms only).**
*If k squares of a packing at side s are core (⊆ [1, s−1]²) then k unit squares pack at side s − 2; hence
s ≥ 2 + s(k).  A packing with no straddler has s ≥ 2 + s(n − B) ≥ 2 + s(n − 4(m−2)).*  *Proof.*  Translate by
(−1, −1): unit squares, containment in [0, s−2]² and disjoint interiors are preserved.  ∎
**Corollary FLUSH-PEEL (the coordinator's PEEL, exact hypothesis).**  The TIGHT flush pinwheel — left wall block
[0,1]×[1, m−1] and its C4 images (or the mirror) — has pocket = hole [1, s−1]² ⊔ four ISOLATED notches
[0, 1−ε]×[0, 1] ([T-computed] `test254`: shapely, m = 4..8, four sides each; areas (s−2)², 1−ε).
**NOTCH-NARROW general [T]:** width 1 − ε = s − (m−1) < 1 and a unit square has width ≥ 1 in every direction, so a
notch holds none; isolated, so no square straddles into it.  Hence all n − 4(m−2) other squares are core and
**s ≥ 2 + s(n − 4(m−2))**.  With n = m² − k the inner count is (m−2)² + 4 − k (Lean `peel_inner_count`):
[T-lit] Nagamochi Thm 2(i) s(j²−1) = s(j²−2) = j gives s ≥ m for k ≤ 6 (the brief is right), and Kearney–Shiu /
Bentz's s(j²−3) = j for j = 3..7 extend it to k = 7 for m ≤ 9 (n = 18, 29).

**2.3 The flush stratum for m ≥ 5, Lemma POKE and the slack form [T].**  Let the touchers' tilts → 0 in RING(n).
Per corner the two limit squares [0,1]×[δ_B, δ_B+1], [δ_A, δ_A+1]×[0,1] are interior-disjoint iff δ_B ≥ 1 or
δ_A ≥ 1, and both δ ≤ 1 (box met): one offset is exactly 1.  A wall cannot carry offset 1 at both ends
(1 + (m−2) + 1 = m > s), so exactly one per wall: the pinwheel PATTERN is forced, start offset a = 1, end offset
b_w ∈ [0, 1−ε], and the wall keeps **slack 1 − ε − b_w ≥ 0** in its m − 3 gaps.  The "every cell doubly met" clauses
are closed conditions satisfied by contact and pin nothing.  So for m ≥ 5 the flush stratum is a family, the tight
pinwheel is its corner b_w = 1 − ε, and the brief's "all non-ring squares lie in a square of side s − 2" is **[F]**
on the rest.  *Lemma POKE [T].*  A unit square whose part in {x < 1} lies in a slot of width g < 1 has exactly ONE
vertex there, at depth ≤ (g/2) sin 2φ ≤ g/2 (φ its tilt).  *Proof.*  Two adjacent vertices inside: the line x = 1
cuts two parallel edges, chord ≥ 1 > g.  Three inside: the two neighbours of the max-x vertex span a diagonal
within 45° of the y-axis, y-extent ≥ 1 > g.  One vertex at depth t: the chord at the mouth is t(tan φ + cot φ)
≤ g.  ∎  ([M] `test254`: 27 822 random squares fitting a slot, 0 violations.)  Corner notches have width b_w < 1
and stay isolated.  So every non-ring square lies in [1 − g/2, s − 1 + g/2]², g the largest gap ≤ 1 − ε:
**FLUSH-PEEL-g [T]:  s − 2 + g ≥ s(n')**, and on the whole stratum **s ≥ (s(n') + m + 1)/2** (table column
"slack").  It excludes by theorem only s < m − ½ for k ≤ 6.  Lossy: a poke of depth g/2 needs φ = 45°.

**2.4 m = 4: Lemma LIMIT-UNIQUE and the neighbourhood theorem [T].**  In the all-ADJ family (A251: eight wall
touchers, δ < 1, reach δ + w(θ) > s − 2) the closed conditions are δ ≤ 1 and δ + 1 ≥ s − 2, i.e. δ ∈ [s−3, 1].
Two touchers of one wall: δ + δ' ≤ s − 2 < 2, so at most one offset 1 per wall; §2.3 forces exactly one per wall and
per corner, and then the other is ≤ s − 3, hence = s − 3.  **The flush stratum is exactly the two tight pinwheels.**
*Lemma USC [T]:* capacity is upper semicontinuous on the closed family (limits of interior-disjoint squares in the
container are interior-disjoint; SAT gaps are continuous).  With HOLE-ONE + NOTCH-NARROW (capacity 1 at both
pinwheels, every s < 4): **there is τ₀ > 0, uniform for s ∈ [3.82, 4 − η], such that every all-ADJ ring with all
eight tilts < τ₀ has pocket capacity ≤ 1.**  Off the common-tilt slice, in all 17 coordinates — but by compactness,
so τ₀ is not explicit.  *Lemma HOLE-POKE [T]* (the quantitative seed): if pocket squares lie in the hole plus slots
of width g ≤ 4 − s on opposite walls, a square of width w = cos φ + sin φ sits in a container of side
σ + g(w² − 1), σ = s − 2, and HOLE-ONE's quantity is f(w) = 1 − (w−1)² + (2−σ)·w(w² − 2) < 1 on [1, √2] for σ < 2
(w² ≤ 2): still at most one square.  ([M] `test254` grid.)

## 3. The honest gap: MONOTONE-ROOM(n)  (task 2, second half)

Off the flush stratum the pocket is not a square: each toucher intrudes ι(τ) = cos τ + sin τ − 1 into the hole
(TILT-BAND: no floor) and opens wedges of angle τ against its wall, into which a free square pokes a corner — the
poker does exactly this, to depth ~1.  **Conjecture MONOTONE-ROOM(n) [C]** (Lean `ring_peel`): *the pocket of a
RING(n) at side s holds at most N(s − 2) unit squares.*  Known: [T] at the tight pinwheel (§2.2); [T] near it for
m = 4 (§2.4, non-effective); [M] A253: capacity ≡ 1 at every sampled tilt at ŝ.  **Named failure mode (m ≥ 5):** as
stated it is doubtful on SLACK rings (b_w < 1 − ε): there the true flush-limit bound is FLUSH-PEEL-g, not N(s−2),
and nothing known forces tightness — the ADJ reach that pins m = 4 has no analogue pinning b_w.  The strongest
provable monotone form is therefore: *pocket(τ) squares lie in [1 − h, s − 1 + h]² ⟹ s ≥ 2 + s(n') − 2h* [T,
trivial], with h ≤ g/2 on the flush stratum [T] and **h(τ) unbounded by anything proved for τ > 0** (the poker
reaches h ≈ 1).  The exact missing statement: **QUANT-ROOM(n) [C]** — an explicit c(m) with: every pocket square of
a RING(n) of max tilt τ and wall slack g, other than ≤ p pokers, lies in [1 − g/2 − cτ, s − 1 + g/2 + cτ]².  At
m = 4 it would make τ₀ explicit: τ₀ = (4 − s)/(2c) (0.0615/c rad at ŝ), which is what a box-valid certificate on
the complement {max τ ≥ τ₀} needs.

## 4. The table  (task 3; `results/peel254_table.md`, 36 rows)

Records: the local copy of Ellsworth's page (2026), cross-checked against A226's 21 poses (0 disagreements > 10⁻⁵).
Proved: Göbel s(5); Kearney–Shiu s(6); Stromquist s(10) and s(11) ≥ 2 + 4/√5; Bentz s(13), s(46), s(22), s(33);
Nagamochi Thm 2: (i) s(j²), s(j²−1), s(j²−2) = j; (ii) **s(N) ≥ √(N − 2⌊√N⌋ + 1) + 1** otherwise (checked
against the paper's text; Thm 1: ν(a, b) < ab − (a+1−⌈a⌉) − (b+1−⌈b⌉), a, b ≥ 2); monotonicity.  tight = 2 + LB(n').

| verdict (tight pinwheel) | n |
|---|---|
| THEOREM-WINDOW: 2 + LB(n') ≥ m | 5, 10, 11, 18, 19, 29 |
| THEOREM-AT-RECORD: rec(n) < 2 + LB(n') < m | 17 (4.7071 > 4.6755), 26 (5.7071 > 5.6213), 27 (5.7889 > 5.7071; uses Stromquist's s(11) bound) |
| RECORDS-ONLY: needs rec(n') optimal | 28, 37–41, 50–55, 65–71, 82, 83, 85–89 |
| EQUALITY: 2 + rec(n') = rec(n) | **84** (2 + rec(52) = 9 + 1/√2 = rec(84), Stenlund) |
| NOT-EXCLUDED | none (it would be a new record: s(n) ≤ 2 + s(n') whenever s(n') ≥ m − 3) |

n = 28 is the instructive miss: it needs s(12) > 3.8244; proved is 3.7889 (lab-certified 3.82 does not reach).
For n ≥ 37 the proved LB(n') is Nagamochi's (ii), ≈ 0.5 below the records — **PEEL as an inductive tool is
hostage to lower bounds at n' that do not exist yet** (the lab's s(11) would feed n = 27 only, already a theorem).
Pages (geometry-checked, a note per panel, undecided = grey stipple): `peel_n17.svg` (12 + Göbel's 5 at 4.707107,
a packing; record smaller), `peel_n65.svg` (28 + Cantrell's 37 at 8.598620, a packing, NOT a record; and the record
side 8.535534 with the hole side 6.535534 stippled: whether 37 fit there is open), `peel_n84.svg` (the equality).

## 5. What this does for n = 11  (task 4)

* PEEL at the tight pinwheel IS A253's HOLE-ONE certificate — nothing new there.
* New [T]: LIMIT-UNIQUE(4) + USC (§2.4) extend "capacity ≤ 1" from the common-tilt slice's limit point to a full
  17-dimensional neighbourhood {all eight tilts < τ₀} of the flush stratum, for every s ∈ [3.82, 4 − η].
* **It does not close RING-POKER-RESIDUAL(11).**  No short argument exists: continuity gives no explicit τ₀, and the
  complement is where the family actually lives (A249's ring: 14.5°).  **Exact remaining case:** all-ADJ rings with
  max_i τ_i ≥ τ₀ — a compact set, certifiable by A253's box-valid PIERCE(1) once τ₀ is explicit, i.e. given
  QUANT-ROOM(11) with its constant c (§3).  And ONLY-RING(11) itself (mixed / non-ring structures) is untouched.
* k0_00: **unchanged**.  FAMILY-STUCK-EXIST(11) not closed.

## 6. What the brief had wrong

1. **"Equality at n = 65 (2 + s(37) = 8.5987 = record)" — wrong.**  rec(65) = 5 + 5/√2 = 8.535534 (Göbel 1979);
   2 + rec(37) = 8.598620 exceeds it by 0.0631.  The only equality for n ≤ 100 is **n = 84**.
2. **"Beats the record at 28, 37, 38, 50" — only if rec(12), rec(17), rec(18), rec(26) are optimal**; by theorem
   the list is 5, 10, 11, 17, 18, 19, 26, 27, 29.  (rec(50) is now 7 + 4/7 = 7.571429, Schadt Dec 2025.)
3. **"The flush limit of the general ring is the pinwheel" — true for m = 4 only** (LIMIT-UNIQUE); for m ≥ 5 the
   flush stratum has wall slack and the theorem is the weaker slack form (§2.3).
4. Correct as stated: the ribbon widths 1 − ε and ε, the notch width s − (m−1), the inner count (m−2)² + 4 − k,
   k ≤ 6 from Nagamochi (and k = 7 for m ≤ 9 from Bentz / Kearney–Shiu), "one poker breaks all sixteen" (and all
   (m−2)⁴ maximal families for m = 3..6).

## 7. Proved / conditional, Lean, reproduce

**Proved (n-general):** BAND-COUNT general; PEEL-0 / CORE-FITS (Lean theorem); FLUSH-PEEL at the tight pinwheel;
NOTCH-NARROW general; POKE; FLUSH-PEEL-g; the conflict structure and the count 4(m−2) + 1 with its one-poker
criterion; LIMIT-UNIQUE(4), USC, HOLE-POKE.  **Conditional on ONLY-RING(n) + MONOTONE-ROOM(n):** "no family-stuck
packing below 2 + s(n − 4(m−2))" (`peel_excludes`), hence k0 exclusion at n from lower bounds at n'.
Lean `Peel.lean`: theorems `peelShift_sqSet`, `core_fits`, `peel_side_bound`, `peel_no_straddler`,
`peel_inner_count`, `peel_excludes`; axioms `band_count` [T-prose], `only_ring` [C], `ring_peel` [C]; opaque
`FamilyStuckN`, `HasRing`; build + `lean/audit.py`: 0 sorry.  Obligations: O-BAND-COUNT (Lean), O-ONLY-RING(n),
O-MONOTONE-ROOM(n), O-QUANT-ROOM(11).
Reproduce: `bash attempts/A254-peel/code/run254.sh table|cells|pages|search` (table 1 s; cells ≈ 2 min incl. m = 6;
pages 5 s; search detached, resumable, `logs/STOP`); `python attempts/A254-peel/code/test254.py` (20 s).
