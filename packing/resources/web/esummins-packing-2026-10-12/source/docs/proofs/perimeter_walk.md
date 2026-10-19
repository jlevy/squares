# The PERIMETER WALK — the catalogue of realisable cell-sets, the walks around the twelve cells, and what a bounded search can and cannot certify about them — A247, 2026-09-16

The PI (23:30): *"set down BL's two meeters, then chase the meeter counts around the twelve cells; the admissible walks
should be few, and each is a small geometric case."*  This note (i) proves the CATALOGUE — which subsets of the
twelve border cells one unit square can meet: exactly the subsets of a corner's five-cell neighbourhood, with an exactly
verified witness for each (§2); (ii) proves two closed-form kills that a walk must obey, TWO-FAR and the theorem
UPPER-END (no 12-stuck packing of eleven squares at side ≥ 4 + √2 — A244's conditional bound made a theorem) (§2.2–2.3);
(iii) defines the WALK as the incidence structure of a 12-stuck packing at meeting level η, counts the walks the
catalogue and the proved lemmas allow, exactly (§3), and reproduces every corpus packing's walk in the list (§3.4); (iv)
runs the certified interval branch-and-bound on the pairs of squares of a walk and says plainly what it decides (§4).
**The answer to the PI's question is negative in the precise sense of §3: the walks are not few** — the proved rules
leave 69 of the 136 meeter pairs per corner and 20 825 free-square triples, and the count is 6.6·10¹⁰ labelled walks
(8.3·10⁹ up to D4); the PI's "few" needs the pose-type structure (flat meeter + tilted partner at every corner), which
is not a proved case split, and even under it the count is in the thousands (§3.3).  Tags: [T] proved here, [T-computed]
certified by interval arithmetic with exact witnesses, [S] a route with a gap, [M] measured, [F] fails, [C] obligation.
Code `attempts/A247-perimeter-walk/code/` (`geo247`, `enc247`, `bb247`, `search247`, `spec247`, `verify247`,
`catalogue247`, `pairs247`, `ring247`, `walks247`, `triples247`, `pages247`, `run247.sh`, `counts247.sh`), results
`results/walk247.md` (+ `catalogue247*.{md,jsonl}`, `pairs247_*.jsonl`, `walks247_*.jsonl`, `triples247_*.jsonl`), pages
`docs/residue_map/campaigns/A247-perimeter-walk/{catalogue,walks,tight_case}.svg`, Lean `Statements/Open/PerimeterWalk.lean`.
Sources: `construct_towards.md` (A246: the rules, NOT-SELF-SUFFICIENT, TYPE-F-OWN, SLOT-MET(η)), A244 `twelve244.md`
(the 282 + 482 twelve-stuck packings, corrected lane B), `wall_slot243.md`, `wedged_seal.md`, `ring_capacity.md`.

## 0. Verdict

> **[T] CATALOGUE (PROJECTION).**  A unit square at any side s > 2 + √2 meets cells of at most one corner neighbourhood
> N_c = {c00, c01, c10, c′10, c″01} (the five ring cells centred at c00); every subset of N_c is realisable below side 4
> (an exact rational witness each, §2.1), and every subset with c00 removed is realisable by a square that meets no
> corner box (the free-square catalogue).  So the catalogue has 4 × 2⁵ entries, 10 + 8 D4 orbits.  [M] Every square of
> the 764 corpus 12-stuck packings (sides 4.000010 … 4.5, meeting depth > 0 and > 10⁻⁵) has its cell-set in it.
>
> **[T] TWO-FAR.**  Two meeters of one corner cannot both reach the same far slot (s > 7/2).  **[T] UPPER-END.**  No
> packing of eleven unit squares at side ≥ 4 + √2 is 12-stuck (n-general: needs n ≥ 12 above 4 + √2).
>
> **[T-computed] The count** (§3): with the catalogue, NOT-SELF-SUFFICIENT and TWO-FAR the labelled walks number
> **66 112 676 788** (transfer-matrix count, exact); with SLOT-MET added, 15 684 260 866 (36 options per corner); under
> the PI's type-F picture at every corner (conditional, §3.3), 960 769 (4 options per corner; SLOT-MET adds nothing there).  [M] Every corpus packing's walk at level 0
> is allowed (0 missing of 764).
>
> **[F] The pair table** (§4): of the 851 pair problems (exact form, level (0.05, 0.07), window [3.82, ŝ]) the certified
> branch-and-bound decided 759 (697 feasible with exact witnesses, 62 infeasible: 21 same-corner, 28 meeter–free, 13
> free–free, none adjacent) within 2·10⁵ boxes each; 92 are undecided.  The undecided pairs are the η-DEGENERATE ones: the exact form's constraints "depth ≥ η" and
> "depth ≤ η′" leave a forced overlap of order η, and the branch-and-bound's cost grows like η⁻ᵏ; the same degeneracy that
> left SLOT-MET's limit [S] in A246.  The 62 kills cut the counts by a factor ≈ 5 (65 options per corner, 16 989 free
> triples: 13 453 179 721 labelled walks; 4 562 962 219 with SLOT-MET; 820 161 = 102 945 up to D4 under type-F) — nowhere
> near "few"; the triple searches over the type-F list run detached (§4.4).  **STUCK-EXIST(11) is not closed on the window**; k0_00 unchanged.

## 1. Setting: the ring, the meeting level, the walk

Container [0, s]², s ∈ [3.82, ŝ] (then up to 4).  Twelve cells in ring order BL00 BL10 BR10 BR00 BR01 TR01 TR00 TR10
TL10 TL00 TL01 BL01 (A244 `cells244`: c00 the corner box, c01 up the corner's vertical wall, c10 along its horizontal
wall).  N_c := the five consecutive ring cells centred at c00; SLOTS(c) := N_c ∖ {c00} = c's two own slots and the far
slot of each of its walls; a free-square WINDOW := SLOTS(c).  D4 acts on the ring (rotation swaps the kinds 01 ↔ 10,
`geo247.check_d4`).  A square MEETS a cell iff their interiors overlap; the SAT depth is the min over the four separating
axes of the projection overlap, > 0 iff they meet (A244).  **Level η**: the cell-set S_i(η) of square i is the set of
cells it meets with depth > η; a packing is η-12-STUCK if every cell lies in ≥ 2 of the S_i(η) (η = 0 is 12-STUCK).
**Walk** (exact form): the multiset {S_i(η)} with the hypothesis |M_c| = 2 (two meeters per corner box; THREE-IN-BOX,
three squares meeting one box, is undecided by the search, §4); so 8 meeters, each with {c00} + a subset of SLOTS(c),
and 3 free squares, each with a subset of a window or nothing.  Two walks are the same up to relabelling and D4.
**Soundness of a kill**: a pair (S, S′) is INFEASIBLE at level (η, η′) when no two interior-disjoint unit squares in
[0, s]², s in the range, meet their cells with depth ≥ η and every other cell of their neighbourhoods with depth ≤ η′
(η′ ≥ η); a walk containing such a pair is the walk of no η-12-stuck packing.  The closed-form kills are monotone
(they use only "meets"), hence valid at every level and, being about packings, at every n.

## 2. The catalogue [T] and the two new lemmas

**2.1 PROJECTION [T].**  On one wall the cells' along-wall intervals are (0,1), (1,2), (s−2, s−1), (s−1, s); a unit
square has extent ≤ √2 along any axis, so it cannot meet cells whose intervals are (0,1) and (s−1,s) (gap s − 2 > √2);
on the other axis likewise.  A set of cells with no such pair has all its x-intervals among the three left ones or the
three right ones, and its y-intervals likewise — i.e. it lies in one N_c.  Sufficiency: the axis-aligned square centred
at (s − 2.5 + ε, ·) meets all five cells of N_c iff s < 4 (`hand244`'s witness at ŝ: (1.393, 1.393, 0)), and monotonicity
gives every subset.  [T-computed] `catalogue247`: the 30 minimal cell pairs outside every N_c are INFEASIBLE by the
single-square branch-and-bound (η = 0, window and corpus range); each of the 16 meeter sets and 48 free sets (a free set
avoids the four boxes) has an exact rational witness, in the monotone form (level 10⁻³) and in the EXACT form at levels
(0.05, 0.07) and (0.02, 0.03) (`catalogue247_exact_*.md`, with the tilt bins in which each set is realisable: the sets
using a far slot need tilt < 15° or > 75°, the diagonal free set {c01, c10} without c00 is realisable at every tilt).
[M] corpus: 764 packings × 11 squares, 0 violations, max cells 4 above 4 (5 needs s < 4).

**2.2 Lemma TWO-FAR [T] (any n, s > 7/2).**  Two interior-disjoint unit squares A, B cannot both meet c00 and the far
floor slot c′10 (in the frame of c: (0,1)² and (s−2, s−1) × (0,1)).  *Proof.*  Each contains a segment from a point of
the box (u < 1, v < 1) to a point of the far slot (u > s − 2, v < 1); both segments lie in {v < 1} and cross every
vertical line u = t, t ∈ [1, s−2].  The separating line ℓ of A and B is not vertical (both squares have points at u < 1
and u > s − 2), so on the strip 1 ≤ u ≤ s − 2 the two segments are ordered, say A's above B's, with ℓ between them; B
lies below ℓ, hence below A's segment, hence its vertical chord at every u ∈ [1, s−2] has length < 1 (top < 1, bottom
≥ 0).  But a unit square of tilt θ has vertical chord ≥ 1 except within sin θ cos θ ≤ 1/2 of its two ends; the strip has
width s − 3 > 1/2, so it cannot lie in one end.  ∎  Mirror: no two meeters of c both reach c″01.  (The corpus obeys it
trivially: above 3 + √2 no meeter reaches a far slot at all.)  Consequence for the walk: ADJ supply into a slot comes
from at most one meeter of the adjacent corner, so a slot's two suppliers are never both ADJ.

**2.3 Theorem UPPER-END [T].**  No packing of eleven unit squares at side s ≥ 4 + √2 is 12-stuck.  *Proof.*  Above
4 + √2 the intervals (1,2) and (s−2, s−1) are > √2 apart, so (PROJECTION with this extra pair) every square meets cells of
ONE corner only: a meeter of c meets ⊆ {c00, c01, c10}, a free square ⊆ {c01, c10} of one corner.  Let T be the number of
corners with ≥ 3 meeters; Σ|M_c| ≥ 8 + T, so f ≤ 3 − T free squares.  A corner with exactly two meeters gets ≤ 3 of its
4 slot incidences from them (NOT-SELF-SUFFICIENT, A246 [T]) and none from another corner's meeter, so it needs a free
square whose cells lie in its own two slots — a free square dedicated to it.  Hence 4 − T ≤ f ≤ 3 − T.  ∎  (n-general:
n − 8 − T ≥ 4 − T needs n ≥ 12.)  With A244's 482 certified 12-stuck packings up to 4.5 and STUCK-EXIST(11) [C], the
twelve-cell window for n = 11 is exactly [4, 4 + √2) up to the open statement below 4.  Lean: `two_far`,
`upper_end_twelve_stuck` (axioms [T]), `twelve_stuck_side_lt`, `twelve_stuck_sides` (theorems).

## 3. The walks: the count, exactly

**3.1 The method** (`ring247`, `walks247`).  Per corner the unordered pair {D_A, D_B} of slot subsets (136 raw), filtered
by the kills; per wall between consecutive corners c, c′ a boolean matrix (the adjacent-corner pair facts) and the
counts each option contributes to the two slots of that wall; the 3 free squares as a multiset of window subsets (with
∅), 20 825 raw.  For each free multiset the walks are the closed 4-cycles (BL, BR, TR, TL) whose wall matrices — the
adjacency AND "own + adjacent + free counts ≥ 2 on both slots of the wall" AND the free-vs-meeter facts — compose, and
their number is the trace of the product of the four matrices: an exact count, no sampling, 70 s.  The list is written
when it is short; membership of a given walk is decided directly (`walk_allowed`).

**3.2 The count.**  Kills used: NOT-SELF-SUFFICIENT (both meeters ⊇ {c01, c10}) and TWO-FAR (both ∋ the same far slot):
136 → **69 options per corner** (65 with the pair table's kills).  Labelled walks: **66 112 676 788**, by free squares carrying cells: 0 → 160 000,
1 → 29 129 440, 2 → 1 907 890 776, 3 → 64 175 496 572 (`walks247_lemmas_level0.jsonl`).  Up to relabelling and D4
(≤ 8 per orbit) that is ≥ 8.26·10⁹ walks.  With SLOT-MET (each own slot met by one of its corner's meeters; A246
[T-computed] at depth ≥ η, [S] at 0): 36 options per corner and **15 684 260 866** labelled walks (0 → 160 000,
1 → 15 904 800, 2 → 643 651 938, 3 → 15 024 544 128).  With the pair table's 62 certified kills (§4.2) the free
triples fall to 16 989 and the walks to **13 453 179 721** (65 options) and **4 562 962 219** with SLOT-MET (35).  So the plain answer: **the walks are not few** — with the proved,
monotone rules the freedom is 69 per corner × 20 825 free triples, and no count-type inequality is violated.

**3.3 The PI's picture as a conditional count [C].**  Suppose every corner is of A246's type F: a flat meeter on one
wall with set {c00, own slot} or {c00, own slot, far slot of that wall} (δ > s − 3) and its tilted partner with
{c00, other own slot} or {c00, other own slot, far slot of the other wall} — 4 options per corner (8 with the choice of
wall, 4 up to the diagonal).  Then: **960 769** labelled walks (0 free squares carrying cells → 1: the all-ADJ
wall-grain ring, A246 §3.4 (b) at every wall; 1 → 288; 2 → 25 168; 3 → 935 312); SLOT-MET is automatic in this picture.
With the pair table's kills: **820 161** labelled, **102 945 up to D4** (`walks247_window_exact_0.05_typef.jsonl`, listed).
Even this conditional list is not "few": the free squares are the
freedom (a free square can carry 1–4 of the eight slots in 48 ways), and a per-walk bounded search over 8 + 3 poses is
what A246 §3.4 called the 8-pose room statement.

**3.4 The corpus reproduces [M].**  At level 0 every one of the 764 corpus 12-stuck packings (282 A217 crowds, 482 A244
certified, sides 4.000010–4.5; |M_c| = 2 at every corner in all of them) has its exact walk ALLOWED by the catalogue,
the two lemmas and the counts (`walks247 --corpus`: 764 checked, 0 missing).  The lemmas are the only facts used here
because the pair table's kills are certified on the window only (the corpus sits above 4).  A244's observation that above
3 + √2 the supply is 12 OWN + 5 FREE with no ADJ is TWO-FAR's and PROJECTION's prediction, and such walks are in the
list (the free squares carry the 4 outside incidences).

## 4. Per-walk geometry: the pair table and the degeneracy [F]

**4.1 The tool** (`bb247`, `enc247`, `verify247`).  A problem: the side s ∈ [s₀, s₁] and k ≤ 3 squares with required
cells (depth ≥ η), avoided cells (depth ≤ η′), containment, pairwise disjointness.  The enclosures are TIGHT: the only
trigonometric dependency in a SAT projection is a cos θ + b sin θ or w(φ) = |cos φ| + |sin φ| of a single tilt, whose
exact range over an interval is closed-form (`enc247`; soundness on 20 000 random boxes, and tight ⊆ A246's loose).
Verdicts: INFEASIBLE = every box discarded by an enclosure (guard 10⁻⁹, hull-consistency contraction on the centres);
FEASIBLE = a witness found by sampling + L-BFGS-B / Powell polish and verified in EXACT rational arithmetic (the tilt
rationalised onto the unit circle, all depths as Fractions); UNDECIDED / BUDGET otherwise.  Every catalogue witness is
exact in this sense.

**4.2 The pair table** (`pairs247`, exact form, level (0.05, 0.07), window, budget 2·10⁵ boxes per pair, 851 canonical
pairs = 76 same-corner + 136 adjacent + 76 opposite + 396 meeter–free + 167 free–free): **697 FEASIBLE** (exact rational
witnesses; 212 of the 212 adjacent/opposite pairs), **62 INFEASIBLE** (same-corner 21 — e.g. a meeter on both far slots
with a partner on either far slot; meeter–free 28 — e.g. the diagonal free square {c01, c10} beside a meeter that reaches
the far floor slot without its own; free–free 13), **92 undecided** (51 of the 76 same-corner pairs, 27 meeter–free, 14
free–free) — the list is in `results/walk247.md`.  THREE-IN-BOX (three meeters of one box, monotone form): undecided at
3·10⁵ boxes.

**4.3 Why the search does not decide** [T, as an analysis].  In the exact form at threshold η the constraints "meets
with depth ≥ η" and "does not meet: depth ≤ η′" are adjacent (η′ = η is the sound choice; the gap η′ − η = 0.02 is a
relaxation that keeps every true walk and makes the single-square problems decidable in a second).  The pair kills that
matter are the touching-limit ones — NOT-SELF-SUFFICIENT, the near-flush meeter with a partner, the corner-triple square
with a {c00, c01} partner — whose forced overlap is of order η: the branch-and-bound must resolve a 7-dimensional
product of two thin (thickness ~η) regions to width ≪ η, i.e. η⁻ᵏ boxes with k ≈ 4–5; at η = 0.05 that is beyond
10⁷ boxes per pair (NOT-SELF-SUFFICIENT itself, a theorem, is undecided at 3·10⁶ boxes at η = 0.1).  A246 met the same
wall on SLOT-MET and paid it with a 6-dimensional reduction proved by hand (CAP-REDUCTION).  Without such a reduction
per pair the table cannot be completed by search, and the per-walk 8-pose searches (task 3) are out of reach by the
same factor.  What the walk enumeration therefore delivers is exact counts under proved rules, not kills.

**4.4 The triples** (`triples247`, detached, resumable): over the first 5 000 walks of the type-F list there are 1 662
distinct touching triples (a corner's two meeters and a third square sharing a cell, or three along a wall); each runs the
three-square search (10 dims + s) at budget 2·10⁵ boxes; a certified triple kills every walk containing it.  The run
continues after this note (`results/triples247_window_exact_0.05.jsonl`, `results/walk247.md` §4 summarises it; the
same η-degeneracy applies, so most will be undecided).

## 5. Plain answers to the brief's questions

* How many walks exist at s ≤ ŝ: 66 112 676 788 labelled (≥ 8.26·10⁹ up to D4) under the proved rules; 15 684 260 866
  with SLOT-MET; 13 453 179 721 / 4 562 962 219 with the 62 certified pair kills; 960 769 → 820 161 (102 945 up to D4)
  under the conditional type-F picture.  Not few.
* Killed analytically: every walk with a self-sufficient corner (NSS) or with two meeters of one corner on the same
  far slot (TWO-FAR) — 67 of the 136 corner options, i.e. all but 69^4/136^4 ≈ 6.6 % of the raw corner configurations;
  above 4 + √2 every walk (UPPER-END).  Killed by the bounded search: 62 pairs (4 more corner options, 3 836 free
  triples), no triple yet.  Remaining: everything else; the corpus's own walks are among them.
* STUCK-EXIST(11) on the window: **not closed**; k0_00 unchanged.  Conditional upper end: now a theorem (UPPER-END).
* n-general: PROJECTION, TWO-FAR, the catalogue and the count are n-independent except through the free-square count
  f = n − 8 (the multiset of f free sets; f = 3 at n = 11) and Lemma TWO; UPPER-END is the statement that above
  4 + √2 a 12-stuck packing needs n ≥ 12.  At other n the walk count changes only through f.

## 6. Files, resume

`bash attempts/A247-perimeter-walk/code/run247.sh test|catalogue|pairs ETA|walks ETA|triples ETA|pages`;
`bash code/counts247.sh` (the counts + corpus check, ~6 min); the pair table resumes from its jsonl (rows done are
skipped; `--only-status BUDGET --budget N` re-runs the undecided ones with a larger budget; `logs/STOP` stops it);
`triples247 --walks <list> --eta 0.05 --eta-avoid 0.07` runs the triple searches over a listed walk set (none listed:
the counts exceed the list cap; `--type-f --slotmet` lists the conditional walks).  Lean:
`Statements/Open/PerimeterWalk.lean` (build + audit).
