# ONE-FLUSH — can a corner always be teleported to flush?  The survey, the refutations, the exact obligation — A226, 2026-09-14

The PI (23:40): "We know from Trump that not all corners are flush, and I suspect that in the general case no non-trivial
optimal solution has 4 flush corners, but we need some way of showing that in the general case AT LEAST ONE corner can
always be teleported to flush."  For the k0 exclusion to work at any n it must be something invalid about the IDEA of
packing n into side < ⌈√n⌉.  This file (i) surveys every best-known packing below ⌈√n⌉ for its corner status, (ii) states
the conjecture in the only form that survives the survey and an explicit construction, (iii) says what a general mechanism
must and must not be, and (iv) states the exact residual obligation at n = 11 and in general.  Tags: [T] proved here,
[S] routine given cited items, [M] measured, [F] false (with the witness), [C] conjecture / obligation.  Sources:
`k0_route.md` §3 (K0-FREE, teleport), `ring_swap.md` (SWAP, CELLS, RAISE, the count), `two_grains.md` (FLUSH, CLICK-DOWN
⟺ STUCK-4), `wall_torque.md` (CEIL, TWO-CONTACT, ONE-TILTED, RING), `k0_count.md` (PUSH, HOLD, the count), `wall_budget.md`
(WALL-F, FLOAT), `frame_census.md`, `corner_seal.md`, `descent.md` (Lemma CH), `sideband.md` (A1, A2, Theorem B, B1, B2).
Code `attempts/A226-one-flush/code/` (`svg226.py` the Ellsworth-SVG parser + exact SAT checks, `survey226.py`, `crowd226.py`,
`pages226.py`), data `data/ellsworth/square-N.svg` (kingbird.myphotos.cc/packing, fetched 2026-09-14), results
`results/survey226.{md,jsonl}`, `crowd226.{md,jsonl}`, `ring11_226.jsonl`; pages `docs/residue_map/campaigns/A226-one-flush/`;
Lean `Statements/Open/OneFlush.lean`.

## 0. Verdict

> **[M] Survey (21 record packings, n = 5, 10, 11, 17, 18, 19, 26–29, 37–41, 50–55; every one re-verified as a packing by
> exact SAT from Ellsworth's coordinates).**  Every record packing below ⌈√n⌉ has AT LEAST THREE flush corners; twenty of
> the twenty-one have FOUR; Trump's n = 11 is the only one with a non-flush corner (TR: the offset top square, depth 0.156,
> and the 40.18° square, depth 0.168).  No record packing has a doubly-met corner other than Trump's one.  So ONE-FLUSH
> holds on the whole survey with room to spare, and **[F] the PI's second conjecture ("no non-trivial optimal packing has
> four flush corners") is false**: n = 5 and n = 10 (Göbel) are PROVED optimal and have four flush corners, as do all
> eighteen later records.  Trump is the exception, not the rule.
>
> **[T]+[M] The all-packings form is false.**  "No teleport-stuck packing at any side < ⌈√n⌉" (STUCK(n); at n = 11
> A223's CLICK-DOWN ⟺ STUCK-4) fails as soon as the record has a corner DOMINO (flush corner square + flush along-wall
> neighbour) at every corner: Proposition CROWD-ABOVE (§3) builds, at EVERY side S > s(n), a packing with all four corner
> boxes doubly met — slide the corner square ε up its wall, tilt the neighbour by ε/2 so that its vertex pokes into the
> strip underneath, translate the rest by (ε, ε).  Verified as packings at S = s(n) + (⌈√n⌉ − s(n))/2 < ⌈√n⌉ for n = 26,
> 28, 29, 37, 40, 50, 51, 55 (`crowd226.md`, page `crowd_above.svg`).  Hence **Theorem PERIMETER ("four doubly-met
> corners force side ≥ f(n) ≥ ⌈√n⌉") cannot hold for any f with f(n) > s(n)**, and every LOCAL mechanism (corner waste,
> chord deficit, wall budget, a per-corner side charge) is doomed: a doubly-met corner costs O(ε) area and O(ε) side.
>
> **[T] The only form with content is about the OPTIMUM: Conjecture ONE-FLUSH(n) — every optimal packing at side
> s(n) < ⌈√n⌉ has a corner met by ≤ 1 square**, i.e. s(n) is attained in the class of packings with a flush corner (K0-FREE
> teleports the lone meeter), and every optimal packing exchanges into one of that class.  At n = 11 this IS the k0_00
> obligation on [3.82, ŝ]: value (no optimal packing below ŝ has four crowds, hence with k1-a none exists) and uniqueness
> (every packing at ŝ raises to a Trump image).  Lean `one_flush` (n-general axiom over `IsPacking n s Q`),
> `optimal_not_stuck`, `no_optimal_of_kill` (theorems).  **[M] At n = 11 the construction of §3 gives nothing below 4**:
> the eight-square crowd ring at S ∈ {3.90, 3.95, 3.99} leaves a pinwheel that holds ONE further square, not three
> (`ring11_226.jsonl`, page `ring11.svg`; A217: no four-crowd local optimum below 4.0014).  **k0_00 unchanged**: the
> obligation is ONE-FLUSH(11) on the window, a statement about minimisers whose proof must be an IMPROVEMENT argument
> (every four-crowd at side S admits a packing at side < S), not a counting, waste or perimeter bound.

## 1. The conjectures, exactly

**Setting (any n).**  P a packing of n unit squares in [0, S]², k := ⌈√n⌉, S < k (so n > (k − 1)²).  Corner c with frame
(u, v) = distances from its two walls; the open corner box (0, 1)²; Q MEETS c iff int Q ∩ (0, 1)² ≠ ∅; c is FLUSH iff the
slot square [0, 1]² (frame) is in P (then it is c's only meeter, Cor. B1); c is SINGLY MET iff ≤ 1 square meets it, DOUBLY
MET iff ≥ 2 do; P is TELEPORT-STUCK (a FOUR-CROWD) iff every corner is doubly met.  [T] K0-FREE (`k0_route.md` §3, Lean
`teleport_packing`): a singly-met corner exchanges, at the same side, into a flush one.

**Conjecture ONE-FLUSH(n) [C].**  If s(n) < ⌈√n⌉ then every OPTIMAL packing (side s(n)) has a singly-met corner.
Equivalent forms [T]: (a) no optimal packing is a four-crowd; (b) every optimal packing exchanges (K0-FREE) into an optimal
packing with a flush corner; (c) s(n) = s_k1(n) := inf{side : a packing with a corner slot square} AND the infimum's every
attainment class contains all optimal packings up to one teleport.  The VALUE part (s(n) = s_k1(n)) needs only SOME optimal
packing to be singly met somewhere; the UNIQUENESS part at n = 11 needs EVERY packing at ŝ to be.

**Conjecture FOUR-FLUSH-FREE [F].**  "No non-trivial optimal packing has four flush corners": refuted by the proved optima
n = 5 (Göbel 1979: four corner squares and one diamond) and n = 10 (Göbel 1979, Stromquist 2003: two 3-cell staircases,
two corner squares, one 45° strip) and by every record in §2 except Trump.  What is true of the survey [M]: every record
below ⌈√n⌉ has ≥ 3 flush corners (THREE-FLUSH, [C] as a conjecture about optima); only Trump uses a fourth corner for a
crowd, and its crowd is the cheapest kind (a flat square offset 0.156 along the ceiling and one tilted square).

**STUCK(n) [F as an all-packings statement, §3].**  "No teleport-stuck packing at ANY side < ⌈√n⌉."  At n = 11 A223 proved
CLICK-DOWN ⟺ STUCK-4; §3 shows STUCK(n) is false for n = 26, 28, 29, 37, 40, 50, 51, 55 and that ONE-FLUSH is its only
surviving content.  At n = 11 STUCK-4 is untested on (ŝ, 4) and vacuous below ŝ if s(11) = ŝ; on [3.82, ŝ) it coincides
with ONE-FLUSH(11) + the non-existence being proved.

## 2. The survey [M]

Method (`svg226.py`): Ellsworth's SVGs encode each packing as merged rectilinear paths (flush blocks) and `<use>` copies of a
unit rect under nested transforms with the numbers in XML entities (30–100 digits); the parser expands the entities,
composes the transforms, decomposes every rectilinear polygon into unit cells (exact inside test on the vertex lattice,
count = area), and returns (centre, tilt) per square in a y-up frame.  Every packing is then checked: n squares, all in
[0, s]², pairwise interior-disjoint by SAT with tolerance 1e-9 (the worst overlap over all 21 is 3.3e-16).  Corner status by
SAT of each square against the open box; flush = axis-aligned with centre (½, ½) in the frame (1e-7).  Trump is also read
from `certs/trump11_certificate.json` as a cross-check (same status, TL ↔ TR by the certificate's reflection).

| n | side | ⌈√n⌉ | slack | tilted | flush | singly met | doubly met | BL BR TR TL | source |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 2.707107 | 3 | 0.293 | 1 | 4 | 4 | 0 | F F F F | Göbel 1979, proved (Göbel) |
| 10 | 3.707107 | 4 | 0.293 | 2 | 4 | 4 | 0 | F F F F | Göbel 1979, proved (Stromquist 2003) |
| 11 | 3.877084 | 4 | 0.123 | 5 | 3 | 3 | 1 | F F 2 F | Trump 1979, rigid |
| 17 | 4.675530 | 5 | 0.324 | 7 | 4 | 4 | 0 | F F F F | Bidwell 1998 |
| 18 | 4.822876 | 5 | 0.177 | 8 | 4 | 4 | 0 | F F F F | Hämäläinen 1980 / Gustafsson 1981 |
| 19 | 4.885618 | 5 | 0.114 | 8 | 4 | 4 | 0 | F F F F | Wainwright 1979 (Cottingham) |
| 26 | 5.621320 | 6 | 0.379 | 9 | 4 | 4 | 0 | F F F F | Friedman 1997 (26b) |
| 27 | 5.707107 | 6 | 0.293 | 5 | 4 | 4 | 0 | F F F F | Göbel 1979 |
| 28 | 5.824445 | 6 | 0.176 | 12 | 4 | 4 | 0 | F F F F | Ellsworth Dec 2025, rigid |
| 29 | 5.933833 | 6 | 0.066 | 14 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth Dec 2025 |
| 37 | 6.598620 | 7 | 0.401 | 15 | 4 | 4 | 0 | F F F F | Cantrell 2002 |
| 38 | 6.707107 | 7 | 0.293 | 6 | 4 | 4 | 0 | F F F F | Göbel 1979 |
| 39 | 6.810722 | 7 | 0.189 | 15 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth Jan 2026 |
| 40 | 6.828427 | 7 | 0.172 | 16 | 4 | 4 | 0 | F F F F | Göbel 1979, rigid |
| 41 | 6.926693 | 7 | 0.073 | 15 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth Jan 2026 |
| 50 | 7.571429 | 8 | 0.429 | 16 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth Dec 2025 |
| 51 | 7.700799 | 8 | 0.299 | 22 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth 2026 |
| 52 | 7.707107 | 8 | 0.293 | 8 | 4 | 4 | 0 | F F F F | Göbel 1979 |
| 53 | 7.822876 | 8 | 0.177 | 14 | 4 | 4 | 0 | F F F F | Cantrell 2002 / Ellsworth 2026 |
| 54 | 7.846667 | 8 | 0.153 | 16 | 4 | 4 | 0 | F F F F | Cantrell 2005 / DeVincentis 2014 |
| 55 | 7.945771 | 8 | 0.054 | 18 | 4 | 4 | 0 | F F F F | Schadt / Ellsworth 2026 |

Trump's TR crowd: the ceiling square #2 (flat, frame centre (0.500, 1.345), depth 0.1555) and #10 (40.182°, frame centre
(1.536, 0.705), depth 0.1683).  Pages `survey_small.svg`, `survey_mid.svg`, `survey_large.svg` (each panel re-checked, note
per panel).  Not surveyed: n ≥ 65 (the brief's list ends at 54; nothing in the argument depends on them).  Reading: the
optimum never pays for a crowd it does not need; Trump needs one because its tilted strip must reach the TR corner region
(the lifted column of `grain_flood.md`'s F_T chain) — a corner is crowded only when a load path ends there.

## 3. Proposition CROWD-ABOVE [T], its verification [M], and what it kills

**3.1 One corner (BL frame, floor variant) [T].**  Let A = [0, 1]² be a flush corner square with a flush floor neighbour
B = [1, 2] × [0, 1] (a DOMINO), and ε > 0 small.  Put A′ = [0, 1] × [ε, 1 + ε] and let B′ be B rotated CLOCKWISE by
θ = ε/2 with its bottom-left vertex at p = (1 − η, y_b), y_b = (sin θ + ε)/2, η = 0.9 (ε − y_b) tan θ.  Then: (i) B′ ⊂ {y ≥ 0}
(its lowest vertex p + (cos θ, −sin θ) has height y_b − sin θ = (ε − sin θ)/2 > 0); (ii) the points of B′ with x < 1 lie on
the two edges at p, at heights in (y_b − η tan θ, y_b + η cot θ) ⊂ (0, ε) since y_b + η cot θ = y_b + 0.9 (ε − y_b) < ε; hence
int B′ ∩ int A′ = ∅ and int B′ ∩ (0, 1)² ≠ ∅ (the vertex p itself); (iii) B′ ⊂ [1 − η, 1 + cos θ + sin θ] × [0, y_b + cos θ]
⊂ [0, 2 + ε/2] × [0, 1 + ε/2].  So A′ and B′ both meet the open corner box and are interior-disjoint.  The WALL variant is
the mirror in the diagonal u = v (A′ = [ε, 1 + ε] × [0, 1], B′ up the wall).  ∎  Note (ii): the second meeter's depth is
O(ε²) — it barely enters the box — while A′'s depth is 1 − ε.

**3.2 The packing [T].**  P a packing at side s with dominoes at all four corners (eight distinct squares; automatic when
s ≥ 4), S = s + w, ε := w/2.  Replace each corner's (A, B) by (A′, B′) in that corner's frame and translate the remaining
n − 8 squares (the CORE) by (w/2, w/2).  The core lies in [w/2, s + w/2]² ⊂ [0, S]².  A′ against the core: a core square
that touched A's top edge (y = 1) moved up by w/2 = ε, to y ≥ 1 + ε = A′'s top — it touches A′ at most, and no other core
square reaches x < 1 at heights below 1 + ε.  B′ against the core: the core moved right and up by ε ≥ ε/2 ≥ B′'s growth in either direction (iii), so squares
that touched B's right edge or top edge are at ≥ 2 + ε resp. ≥ 1 + ε, beyond B′.  Squares that could move INTO B′ from the
left or below are only A (removed); into A′ only B (removed).  The other corners' new squares stay inside their own
corner's [0, 2 + ε/2] × [0, 1 + ε/2] region, disjoint from each other when S ≥ 4 + ε and from the core by the same shifts.
Hence a packing at side S with EVERY corner box doubly met (A′ and B′ at each).  ∎  Verified exactly (`crowd226.py`,
`crowd226.md`): S = s + (k − s)/2 < k, all four corners with 2 meeters, worst SAT overlap 2·10⁻¹⁰ (n = 55) — 1e-12 otherwise.

| n | record | k | S | ε | meeters BL BR TR TL | verified |
|---|---|---|---|---|---|---|
| 26 | 5.621320 | 6 | 5.810660 | 0.0947 | 2 2 2 2 | yes |
| 28 | 5.824445 | 6 | 5.912222 | 0.0439 | 2 2 2 2 | yes |
| 29 | 5.933833 | 6 | 5.966917 | 0.0165 | 2 2 2 2 | yes |
| 37 | 6.598620 | 7 | 6.799310 | 0.1003 | 2 2 2 2 | yes |
| 40 | 6.828427 | 7 | 6.914214 | 0.0429 | 2 2 2 2 | yes |
| 50 | 7.571429 | 8 | 7.785714 | 0.1071 | 2 2 2 2 | yes |
| 51 | 7.700799 | 8 | 7.850400 | 0.0748 | 2 2 2 2 | yes |
| 55 | 7.945771 | 8 | 7.972886 | 0.0136 | 2 2 2 2 | yes |

The other records lack a domino at some corner (Göbel strips: the two single corner squares abut the 45° strip; n = 17,
18, 19, 39, 41, 53, 54 likewise at two or one corners; Trump at three) — the construction is not available there, which
says nothing about STUCK(n) for those n.

**3.3 Consequences [T].**  (a) STUCK(n) is false for the eight n above: four-crowds exist at every side in (s(n), k).
(b) inf{side of a four-crowd of n squares} ≤ s(n) for those n; whether the infimum is ATTAINED at s(n) is exactly
ONE-FLUSH(n).  So no bound of the shape "four-crowd ⇒ side ≥ f(n)" can give more than f(n) = s(n), i.e. can only ever
restate ONE-FLUSH — Theorem PERIMETER is either false (f(n) > s(n)) or equivalent to the conjecture.  (c) No LOCAL charge
proves ONE-FLUSH: a doubly-met corner wastes O(ε) area (the strip (0, 1) × (0, ε) minus a poke of area O(ε³)), costs O(ε) of
wall length and O(ε) of side, and CH-A's (1 − d₁)² is ε²; the chord deficit (CH-L) is O(ε); WALL-F's chord sum changes by
O(ε).  Any argument must be GLOBAL and must use minimality.  (d) The count of `k0_count.md` (12 > 11 under LOAD + DISTINCT)
is n = 11-specific: for n ≥ 12 it is no contradiction even under its (false) hypotheses; the PI's "invalid about the idea of
packing n into side < ⌈√n⌉" cannot be a count of squares.  (e) Rattlers: the crowds of §3.1 are UNLOADED (B′ touches
nothing but the floor; A′ touches its wall and the square above it only if it moved exactly ε) — every four-crowd built here
is a rattler crowd, the class A218/A219 could not exclude by loads.

**3.4 n = 11 [M].**  The eight-square ring of §3.1 (variants alternating floor / wall so that adjacent dominoes do not
collide; needs S ≥ 3 + 1.5ε) is a packing at S = 3.90, 3.95, 3.99 with all four corners doubly met; the free region is a
pinwheel — a central (S − 2 − ε)-box with four stubs of width S − 3 − 1.5ε ≈ 0.9 — into which A222's region search
(`region222.place`, greedy over 90 tilts + 40 penalty restarts) fits ONE square, never three (best penalty 4·10⁻⁴ at S =
3.99, ε = 0.02; `ring11_226.jsonl`, page `ring11.svg`).  Consistent with A217 (lowest four-crowd local optimum 4.0014) and
with `ring_swap.md` §1.4's endgame ("3 squares in the cross").  Not a proof of STUCK-4 on (ŝ, 4): only one ring family was
tried.

## 4. What a general mechanism must be

**4.1 What is known to fail (collected).**  The sweep count (`ring_swap.md` §1.4: closes only for n ≤ 4); the torque /
holder count (`k0_count.md`: 12 > 11, hypotheses LOAD and DISTINCT false on the witnesses; n-specific); the click's
monotonicity (`two_grains.md` §2.3: anchored chains rise toward alignment); area / waste (§3.3 (c): O(ε) per crowd against
k² − n ≥ 3); the wall budget (WALL-F is an inequality on chords at height 1/√2, insensitive to an ε-slide); the frame census
(finite but astronomically large at n = 11, `frame_census.md`); and now every all-packings statement (§3).

**4.2 What survives [T].**  At a free Fritz-John point (a local minimiser of the side, `k0_count.md` §1) every doubly-met
corner has (i) a tilted meeter (ONE-TILTED), (ii) no meeter on both walls (B1), (iii) if that meeter is loaded on its wall,
two further loaded contacts (TWO-CONTACT), (iv) if pressed by its partner, a holder (HOLD); (v) the wall forces circulate
(TORQUE-ID).  These are n-general and load-theoretic — they say nothing about a rattler crowd, and §3.3 (e) shows the
crowds that exist above the record are rattler crowds.  The two n-general mechanisms that DO reach rattler crowds are the
exchange lemmas — SWAP / CELLS / RAISE (`ring_swap.md`) — and the CLICK (`two_grains.md`), both side-preserving or
side-decreasing MOVES: exactly the shape §3.3 (b)–(c) demands.  **The general theorem needed is an improvement theorem:**

> **Conjecture UNCROWD(n) [C].**  Every four-crowd P at side S < ⌈√n⌉ admits a packing of n squares at side < S.

[T] UNCROWD(n) ⟺ ONE-FLUSH(n) (⇒: an optimal four-crowd would improve below s(n); ⇐: an optimal packing has a singly-met
corner, so a four-crowd is not optimal and the optimum is a packing at a smaller side).  UNCROWD is the honest statement of
"the k0 exclusion": not that four-crowds cannot exist below ⌈√n⌉ (they can), but that they are never the LAST word — the
minimiser always has a bare corner to settle.  At n = 11 A217's drains ARE UNCROWD in the small: every k0 local optimum below
3.9 drained to a settled corner; its failure mode was the four-crowd at side ≥ 4.0014, above the window.

**4.3 Why the crowds of §3 un-crowd, and what that suggests.**  In §3.1 the improving move is explicit: retract B′ (rotate
by −θ, shift right by η, lower by y_b), lower A′ by ε, shrink the container by w.  What made it possible: the second meeter
was UNLOADED and had room to retreat (the core had moved away).  A four-crowd at side s(n) would have to be one where no
such retreat exists — every meeter caged by loaded contacts — i.e. a free FJ four-crowd; A219's RING measured 0 / 193 at
n = 11 (all four-crowd witnesses need an external crowd pull).  So UNCROWD splits into (α) an unloaded meeter always retreats
(a SWAP-type move at the same side into a singly-met corner, then K0-FREE, then a side decrease unless the packing was
already flush-cornered), and (β) no four-crowd is force-balanced by walls and contacts alone (RING).  (α) is n-general and
plausibly provable (a rattler meeter's retreat region is its free configuration component; it retreats unless caged, and a
caged rattler is loaded in the limit — Lemma STRUT's setting), (β) is the structure question A219 priced at 2.6·10¹¹
structures for n = 11 and has no n-general form.  Neither is proved here.

## 5. The exact remaining obligation

**n = 11.**  ONE-FLUSH(11) in the strong form on [3.82, ŝ]: every packing at side m ∈ [3.82, ŝ] has a singly-met corner.
Given k1-a (no packing at m < ŝ contains a corner slot square; the k1_00 tree, priced 200–300 CPU-h, not yet certified) and
k1-b (every packing at ŝ with a corner slot square is a Trump image), this closes k0_00 for value and uniqueness (Lean
`no_optimal_of_kill` for the value part with K0-FREE's exchange O-LINK as a hypothesis; `k0_route.md` §3, `ring_swap.md`
§1.7 for uniqueness via SWAP-RIGIDITY).  Its proof cannot be a bound valid above ŝ (§3) and cannot be local (§3.3 (c));
it must be UNCROWD on the window — the drain (A217), the sweep (A222) or the click (A223) made into a theorem, or the trees.

**General n.**  ONE-FLUSH(n) ⟺ UNCROWD(n): with it, s(n) is the minimum over packings with a flush corner, and the
forced-corner cascade (`forced_corners.md`) starts from a pin at every n — the census of a packing problem reduces to its
k ≥ 1 classes.  Evidence: 21 / 21 records (§2), 0 / 883 FJ four-crowds at n = 11 (A217), the counter-family of §3 un-crowds.
THREE-FLUSH (≥ 3 flush corners at every optimum) is the sharper empirical statement and would reduce further to the k3
classes; no mechanism is proposed for it.

## 6. Lean, files

`Statements/Open/OneFlush.lean`: `MeetsCornerN`, `SinglyMet`, `IsOptimalPacking` (n-general over `IsPacking n s Q` and
`Fits`); `one_flush` (axiom [C], n-general, hypothesis s < ⌈√n⌉); `optimal_not_stuck` (theorem: an optimal 11-packing below
4 is not `TeleportStuck`, via `ceil_sqrt_eleven`); `no_optimal_of_kill` (theorem: with K0-FREE's exchange `link` and the
k1-a `kill`, no optimal packing at m < 4).  `lake build` + `lean/audit.py` exit 0, no sorry.  FOUR-FLUSH-FREE gets no axiom
(refuted).  Code, data, results, pages as in the header; the survey and the constructions rerun in ~30 s
(`python survey226.py; python crowd226.py; python crowd226.py --ring11; python pages226.py`).
