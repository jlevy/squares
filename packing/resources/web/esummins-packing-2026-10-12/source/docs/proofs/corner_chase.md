# The CORNER CHASE — POKE in its true form (the sense is not forced), TOP-2, FLAT-ABOVE, NO-ROTATE from the global Ψ-minimum, Lemma TWO-POKERS (s* = 3.9342 > ŝ), and what the chase closes: the type-F ring on the window — A248, 2026-09-17

The PI (00:30): *"if the close meeter A is flush with the floor, it has to slide far enough from the wall to allow a
second meeter B from above; B is tilted so a corner pokes down into BL00 — the tilt has to be CCW for the poking corner
to be at the wall side; then BL01 needs a second meeter … B′ has to be torque-pinned … Follow the non-internal pinning
options around the outside: I think we run into a contradiction — everything cannot be pinned without an internal
square."*  This note makes each step exact for every n, proves what is a theorem, refutes the one step that is false
with an exact witness, derives NO-ROTATE from A233's Ψ-minimum (naming the retreat), and runs the chase with external
pinners only.  The chase does reach a closed-form inequality that fails on the window — not from pinning but from
room: two pokers on one wall need side ≥ s* = 3.9342370 > ŝ (Lemma TWO-POKERS) — so on [3.82, ŝ] every type-F
corner's wall slot is met by an interior square and a ring of four type-F corners is impossible; what it does not
reach is the type-T corner (both meeters tilted), which is 95 % of the corpus.  Tags: [T] proved, [T-computed]
certified computation, [S] routine given cited items, [M] measured, [F] false as stated (with the witness), [C]
obligation.  Sources: `construct_towards.md` (A246: TYPE-F-OWN, NOT-SELF-SUFFICIENT, the patterns), `local_lock.md`
(A233: `PsiMin`, `Retreats`), `snap_down.md` (A245: STACK, WALL-CLICK, H-ROOM), `ring_swap.md` (SWAP),
`perimeter_walk.md` (A247: PROJECTION, the 764-packing corpus), `wall_torque.md` (ONE-TILTED, TWO-CONTACT),
`wedged_seal.md`, `k0_count.md`, `cross.md` (A240: LOCKED flags).  Code `attempts/A248-corner-chase/code/`
(`geom248`, `chase248`, `twopokers248`, `notches248`, `external248`, `summarise248`, `pages248`, `test248`,
`run248.sh`); results `results/chase248.{md,jsonl}`, `chase248_summary.json`, `twopokers248.json`,
`notches248_*.json`, `external248_*.json`; pages `docs/residue_map/campaigns/A248-corner-chase/{bl_structure,
two_pokers,chase_ring,twelve_stuck_fail}.svg`; Lean `Statements/Open/CornerChase.lean`.

## 0. Verdict

> **[F] POKE's directional claim.**  The tilt sense of the poking meeter is NOT forced.  Exact witness (§1.1): beside
> A = [19/20, 39/20] × [0, 1] the square with cos θ = 3/5, sin θ = 4/5, lowest vertex (4/5, 9/10), wall vertex (0, 3/2),
> top vertex (3/5, 23/10) touches the wall, meets the corner box and the wall slot, is interior-disjoint from A (its
> edge V→R crosses height 1 at x = 7/8 ≤ 19/20) and has its lowest vertex FARTHER from the wall than its highest — the
> CW sense.  [M] 7 of the 288 type-F corner views of the corpus are CW.
> **[T] POKE's true form** (§1.2–1.3): the cap of B below height 1 lies in (0, δ]; sin θ ≤ x_V ≤ δ; TILT-MIN
> d ≤ (δ − x_V) tan θ; **TOP-2**: B's top vertex T = (cos θ, y_T) has y_T ≥ 2 (since (1 − sin θ) tan θ ≤ cos θ + sin θ − 1);
> **FLAT-ABOVE**: no flat wall square [0,1] × [y₀, y₀+1] with 0 < y₀ < 2 is interior-disjoint from B (its open diagonal
> V→T crosses the band).  So the second meeter of B's wall slot is a TILTED wall square above B (A245's STACK), or an
> off-wall square through the notch at L; never A (TYPE-F-OWN), never a flat wall square — the flat-ADJ supply of a
> poker's slot (A246 §3.4 (b) on a wall with a poker, and the alternating pattern (c)) is dead at every side.
>
> **[T] NO-ROTATE** (§2), from A233 exactly: `PsiMin` is a GLOBAL minimum, so the excluded retreat may move several
> squares (`psiMin_no_lowering`; `no_retreat_of_psiMin` is the one-square case).  The retreat named: the FLUSH-STACK
> exchange (A245's click at y₀ = 1) of the wall pair (B, B′) into [0,1] × [1,2] ∪ [0,1] × [2,3]; below 4 it changes Ψ by
> exactly (4 − s) − d_c(B) − d_c′(B′) − d_c(B′) (`click_account`), so when d + d′ > 4 − s the window [0,1] × [1,3] ∖
> (B ∪ B′) is met by a THIRD square (`no_rotate`).  Who can supply the block externally: never A (A ⊆ {v ≤ 1});
> always the next corner's flat ceiling meeter or its wall-touching poker (§2.2).  Pinning, in this exchange form,
> forces no interior square.
>
> **[T]/[T-computed] Lemma TWO-POKERS** (§3.2, the closed-form inequality that FAILS on the window): two wall-touching
> pokers on one wall — B beside the lower corner's flat floor meeter, B′ beside the upper corner's flat ceiling
> meeter (offsets < 1) — are interior-disjoint only if
>     s ≥ 2 + ψ(θ) + ψ(θ_f) + sin θ_f + max(cos θ_f tan θ, sin θ − (cos θ − cos θ_f) cot θ_f),  ψ(t) = (1 − sin t)/cos t,
> whose minimum over θ ≤ θ_f is s* − 2 with **s* = 2 + min_θ [tan(45° − θ/2) + tan(θ/2) + sec θ] = 3.9342370** (at
> θ = 15.26°, θ_f = 74.74°, the corner-to-corner contact T = T′); the minimum over the whole triangle is certified
> ≥ 1.934236 by 146 403 monotone-enclosure boxes (`twopokers248`).  [M] the SAT search (pokers floating allowed) has
> sup margin ≤ 0 at 3.82, ŝ, 3.90, 3.93, 3.934 and > 0 from 3.936: the bound is sharp.  **On the k0 window no wall
> carries two type-F pokers** (Lean `two_pokers_window`).
>
> **What the chase closes (§3.3):** on [3.82, ŝ], at a type-F corner the poker's wall slot is met by an INTERIOR
> square — the adjacent corner's flat cannot (FLAT-ABOVE), its poker cannot (TWO-POKERS), its ceiling poker cannot
> (TYPE-F-OWN mirror), other corners' meeters cannot (PROJECTION); a wall carries at most one type-F poker, so four
> type-F corners put four pokers on four walls (a pinwheel) and need ≥ 4 free squares if no free square serves two
> adjacent notches — [M] SEPARATE-NOTCHES (`notches248`, sup margin −0.003 at ŝ, −0.006 at 3.82) — against n − 8 = 3.
> So **no 12-stuck packing of eleven squares on the window has four type-F corners** [T given SEPARATE-NOTCHES [M]]:
> the PI's "cannot be pinned without an internal square" holds for type-F corners in its incidence form, and
> "everything" cannot be.  **[C] What it does not reach:** the type-T corner — both meeters tilted — where TILT-MIN
> has no flat to bind against and the poker's slot may be supplied by the corner itself; 2 912 of the corpus's
> 3 056 corners are type T.  Above s* the external pattern (flats on two opposite walls, mutual pokers on the other
> two) is no longer excluded (the pair is feasible from 3.936; the full 8-ring search reaches margin 0 at 3.97, [M]
> open).  LOCKED-CROWD-FREE(11) / STUCK-EXIST(11) not closed; k0_00 unchanged.
>
> **[M] The 764 twelve-stuck packings** (§4) all fail at S0 (none locked); geometrically 144 of their 3 056 corners are
> type F, whose 46 wall pairs have an UNBLOCKED click on 26 (a Ψ-lowering exchange) and a blocked one on 20; the
> genuine FJ points' 65 locked doubly-met corners are 45 type T, 20 type F, none with a wall pair.

## 1. POKE (task 1)

**Setting** (any n, any side; corner c at the origin, u = distance to the shared wall, v = to the floor).
A = [δ, 1 + δ] × [0, 1] is the flat floor meeter, 0 < δ < 1; B is a second square of the packing meeting (0,1)², in
the quadrant, interior-disjoint from A; by ONE-TILTED B is tilted, θ ∈ (0°, 90°) the angle of the edge leaving its
lowest vertex V = (x_V, y_V); L = V + (−sin θ, cos θ), R = V + (cos θ, sin θ), T = V + (cos θ − sin θ, sin θ + cos θ).

**1.1 [F] The sense.**  "B's lowest vertex is on the wall side" is false: the witness of the verdict
(`geom248.poke_witness_exact`, all fields rational) has x_V = 4/5 > x_T = 3/5.  For θ > 45° the lowest vertex is at
abscissa sin θ > cos θ, and such a poker exists iff δ ≥ sin θ > 1/√2.  Page `bl_structure.svg` (a), (b).

**1.2 [T] The cap and TILT-MIN.**  B ∩ {v < 1} is convex, contains a box point p (u_p < 1) and V; if x_V > δ the
segment [p, V] crosses int A; so the cap lies in {u ≤ δ}, x_V ≤ δ, and x_V ≥ sin θ (L in the container).  R is above
height 1 (else x_R = x_V + cos θ ≤ δ and x_V ≥ sin θ give cos θ + sin θ ≤ δ < 1).  Hence the edge V→R crosses height
1 at x_V + (1 − y_V) cot θ ≤ δ: **d_V := 1 − y_V ≤ (δ − x_V) tan θ ≤ (δ − sin θ) tan θ**.  ∎

**1.3 [T] TOP-2 and FLAT-ABOVE.**  y_T = y_V + sin θ + cos θ ≥ 1 − (1 − sin θ) tan θ + sin θ + cos θ ≥ 2, because
(1 − sin θ) tan θ ≤ cos θ + sin θ − 1 ⟺ sin θ (1 − cos θ) ≤ 1 − cos θ.  With TILT-MIN tight at δ = 1 the wall vertex is
at height 1 + ψ(θ), ψ := (1 − sin θ)/cos θ = tan(45° − θ/2) ∈ (0, 1), and y_T = 1 + ψ + sin θ.  FLAT-ABOVE: for
W = [0,1] × [y₀, y₀ + 1], 0 < y₀ < 2, the open diagonal (V, T) is interior to B, has abscissae in (0, 1) and heights
from y_V < 1 < y₀ + 1 to y_T ≥ 2 > y₀: it meets int W.  ∎  [M] 20 000 random pokers, 0 violations (`test248`); corpus 0.
Consequences: (i) B meets the wall slot c01 = (0,1) × (1,2) (its diagonal crosses it); the SECOND meeter of c01 lies in
(0,1) × (1,2) ∖ B = the NOTCH (the wedge between the wall and the edge L→T, apex L at height 1 + ψ, opening 90° − θ,
abscissae < min(cos θ, (1 − ψ)/tan θ)) plus a sliver right of V→R of height ≤ (1 − δ) tan θ — so it is a tilted wall
square above B, or an off-wall square entering the notch; never A, never a flat wall square.  (ii) If A is tilted too
(type T) nothing here applies: A may itself meet c01 (A2 / NSS allow one meeter on all three cells).

## 2. NO-ROTATE (task 2)

**2.1 [T] The retreat.**  A233's `PsiMin n s Q` is `IsPacking n s Q ∧ ∀ Q′, IsPacking n s Q′ → Ψ(Q) ≤ Ψ(Q′)`: any
Ψ-lowering exchange at the same side, moving any number of squares, is excluded (Lean `psiMin_no_lowering`).  The
PI's "the two left-wall squares rotate out of the way" is A245's WALL-CLICK: (B, B′) replaced by [0,1] × [y₀, y₀ + 2],
a packing iff H-ROOM(y₀).  Below 4 (3 ≤ s < 4): for y₀ < 1 the lower flush square overlaps int A — H-ROOM fails by A
alone; at y₀ = 1 the lower square has depth 0 everywhere and the upper one [0,1] × [2,3] has depth 4 − s at c′ and 0
elsewhere; for y₀ > 1 the cost y₀ + 3 − s is larger.  So the only click is y₀ = 1 and **Ψ(new) − Ψ(old) = (4 − s) −
d_c(B) − d_c′(B′) − d_c(B′)** (`click_account`).  **Lemma NO-ROTATE [T]**: at a Ψ-minimal packing with
d_c(B) + d_c′(B′) + d_c(B′) > 4 − s the flush stack is not a packing: [0,1] × [1,3] ∖ (B ∪ B′) meets a third square
(`no_rotate`).  If the depths sum to ≤ 4 − s the click is Ψ-neutral or raising and NO-ROTATE says nothing (4 − s ≤ 0.18
on the window).  At s ≥ 4 the click lowers Ψ by the depths whenever H-ROOM(1) holds — the corpus test of §4.

**2.2 [T] Who blocks, externally.**  X ∉ {B, B′} blocks iff int X meets (0,1) × (1,3).  A: never.  c′'s meeters: a c′
meeter has a point above s − 1 and extent ≤ √2, so it blocks iff it has interior points in (0,1) × (s − 1, 3); c′'s flat
ceiling meeter at offset δ′ < 1 contains (δ′, 1) × (s − 1, s) and s − 1 < 3: it ALWAYS blocks; c′'s wall-touching poker's
cap below height 3 blocks whenever its depth exceeds s − 4 < 0: always.  A third wall square or an interior square in
the notch also blocks.  In row language: B carries its wall row, the row with A (A's tip on V→R, TILT-MIN tight) and the
row with B′; B′ its wall row, the row with B and one with c′'s crowd or the ceiling — TWO-CONTACT's two further
contacts, supplied by walls and meeters.  **So NO-ROTATE constrains c′'s second meeter to dip below height 3 in the
wall strip, which every type-F ceiling meeter and every wall poker does; pinning alone forces no interior square.**

## 3. The chase (task 3)

**3.1 The external supply of a poker's slot.**  Corner c type F, flat A on the floor, poker B on or near the shared
wall w (touching in the PI's picture).  c01's second meeter, with external pinners only, is a meeter of the adjacent
corner c′ (PROJECTION: c01 ∈ N_c ∩ N_c′ only): (i) c′'s flat meeter on w: excluded by FLAT-ABOVE (it meets c01 iff its
bottom is < 2); (ii) c′'s poker beside a flat on w: its points with u < 1 lie above that flat (a convex set cannot pass
a flat wall square within the strip), so it does not reach c01 (the TYPE-F-OWN mirror); (iii) c′'s poker on w beside
c′'s flat ceiling meeter — the MUTUAL tilted pair of A245's STACK, B's top ≥ 2 interleaving with B′'s bottom ≤ s − 2:
Lemma TWO-POKERS.  On a wall with two flats (A246 (b), the pokers on the floor and ceiling) both slots are supplied
by the flats.

**3.2 [T] Lemma TWO-POKERS** (any n; wall x = 0, corners c at 0 and c′ at (0, s); s ≥ 3).  Let B be a wall-touching
poker of c beside A = [δ, 1+δ] × [0,1], and B′ a wall-touching poker of c′ beside A′ = [δ′, 1+δ′] × [s−1, s], δ, δ′ ≤ 1,
both meeting their boxes.  Then s ≥ 2 + F(θ, θ_f) with F as in the verdict (θ, θ_f the frame tilts, θ ≤ θ_f w.l.o.g.
by the reflection of the wall).  *Proof.*  Put ψ = ψ(θ), ψ_f = ψ(θ_f).  By §1.2–1.3, B's wall vertex L = (0, y_L) has
y_L = 1 − d + cos θ ≥ 1 + ψ, and its top T = (cos θ, y_T), y_T = y_L + sin θ; mirrored, B′'s wall vertex is at
y_L′ ≤ s − 1 − ψ_f and its bottom vertex T′ = (cos θ_f, y_T′), y_T′ = y_L′ − sin θ_f.  B has a vertical chord at
x = a := cos θ_f (a ∈ (0, 1) ⊂ (0, w(θ))) whose top is on the edge L→T when a ≤ cos θ: height y_L + a tan θ; B′ has a
vertical chord at x = a starting at T′; interior-disjointness forces y_L + a tan θ ≤ y_T′ (open chords of a convex
body at an interior abscissa are interior).  Likewise at x = b := cos θ, B′'s chord bottom is on the edge T′→R′ at
height y_T′ + (b − a) cot θ_f and must be ≥ y_T.  Hence s − 1 − ψ_f − sin θ_f ≥ y_T′ ≥ max(y_L + a tan θ, y_T − (b − a)
cot θ_f) ≥ 1 + ψ + max(a tan θ, sin θ − (b − a) cot θ_f).  ∎  The minimum of F: on θ + θ_f = 90° the two terms of the
max coincide and F = h(θ) = tan(45° − θ/2) + tan(θ/2) + sec θ, minimised at θ = 15.2563°, h = 1.9342370; over the
triangle {θ ≤ θ_f} the certified lower bound 1.934236 (146 403 boxes, every term a product or difference of monotone
functions on a box, guard 10⁻⁹) shows the line minimum is the global one: **s* = 3.9342370**.  [M] Floating pokers
(x_V > sin θ) do not help: the 6-parameter SAT sup-margin is ≤ 0 below s* and > 0 from 3.936 (`twopokers248.json`).
n-general: the statement and s* are n-free; the n = 11 corollary is s* > ŝ = 3.877084, i.e. the whole k0 window.
Page `two_pokers.svg`: the tight pair at s* (T = T′) and the same tilts overlapping at ŝ.

**3.3 [T given SEPARATE-NOTCHES] The type-F ring.**  On the window, by §3.1–3.2 every type-F poker's slot is met by
a free square through its notch, and no wall carries two type-F pokers.  Four type-F corners: each poker on one of
its two walls, no wall with two ⟹ each wall carries exactly one poker (a pinwheel; a wall with two flats would leave
three walls for four pokers).  Their four slots (BL01, TL10, TR01, BR10 or the mirror) need free squares; opposite
slots are > s − 2 apart (PROJECTION), and adjacent ones (BL01 and TL10, both in N_TL) are separated by TL's flat on
the shared wall with bottom ≥ 2 (FLAT-ABOVE): [M] SEPARATE-NOTCHES — the sup over all poses of the least margin of one
free square meeting both slots while avoiding B_BL, A_TL, B_TL is −0.003 at ŝ, −0.006 at 3.82, −0.008 at 4
(`notches248`, 8 parameters, 150 restarts) — so no free square serves two, and ≥ 4 > 3 free squares are needed.  ∎
**Interior pinners** (the brief's last question): none are needed for pinning (§2.2); what the interior squares must
do is SUPPLY the four notches, and three cannot.  **Type T** remains: a corner with both meeters tilted has no
TILT-MIN and may supply its own wall slot; the corpus is 93 TTTT : 188 mixed : 1 FFFF (A246), so the closed case is
the rare one.  The mixed rings need the type-T corner's supply pattern — the next step, not this note's.

## 4. Tests (task 4; `results/chase248.md`)

Every corner of every packing is examined from each of its two walls (a VIEW).  **The 764 twelve-stuck packings**
(sides 4.00001–4.5): S0 fails everywhere (none locked, A244).  Geometrically: 5 536 type-T views, 288 F-floor, 288
F-wall (144 type-F corners); pokers 281 CCW, 7 CW; 0 violations of TILT-MIN / TOP-2 / FLAT-ABOVE / TYPE-F-OWN at
depth 10⁻⁶; c01's second supplier beyond the poker: off-wall tilted free 76, wall tilted c′-meeter 46, off-wall
c′-meeter 5 (169 views have the slot met only by touches at 10⁻⁹); of the 46 wall pairs the click (s ≥ 4: gain
−d − d′ < 0) is UNBLOCKED on 26 — a Ψ-lowering exchange, so a Ψ-minimal packing cannot look like these — and blocked
on 20 (c′ 9, interior 7, both 3, A 1).  TWO-POKERS is consistent with them: every wall pair sits at s ≥ 4 > s*.  Page
`twelve_stuck_fail.svg`.  **The genuine FJ points** (883, LOCKED flags from A240): 65 locked doubly-met corners, 45
type T, 20 type F; the locked type-F views reach S3 with an off-wall supplier and no wall pair — consistent with §3.

## 5. What is proved, what the chase needs, n-generality (task 5)

* **[T]** POKE's true form (cap, TILT-MIN, TOP-2), FLAT-ABOVE, NO-ROTATE with the exact click accounting and the
  external blockers, TWO-POKERS (with its minimum [T-computed]) — for every n; NO-ROTATE's accounting for 3 ≤ s < 4.
* **[F]** POKE's sense (exact witness); pinning forcing an interior square (§2.2).
* **[T given [M]]** no 12-stuck eleven-square packing on the window has four type-F corners (SEPARATE-NOTCHES [M]).
* **[C]** the type-T corner; hence LOCKED-CROWD-FREE(11) is NOT given by POKE + NO-ROTATE + the chase; k0_00 unchanged.
* n = 11: s* = 3.9342 > ŝ makes the window statement; for n ≥ 16 (s ≥ 4) TWO-POKERS is empty.
* Lean `Statements/Open/CornerChase.lean`: `psiMin_no_lowering`, `no_rotate`, `two_pokers_window`,
  `optimal_psiMin_not_twelve_stuck` (theorems); `top_two`, `flat_above`, `click_account`, `two_pokers` (axioms
  [T-prose]); `corner_chase_closes` (axiom [C]); build + audit exit 0, 0 sorry.  Obligations: O-TOP2-LEAN,
  O-TWO-POKERS-LEAN (the chord argument over `sqSet`), O-SEPARATE-NOTCHES (a proof), O-TYPE-T (the residue).
* Reproduce: `bash attempts/A248-corner-chase/code/run248.sh test|chase|twopokers|notches|external|summary|pages`
  (chase 70 s, twopokers 3 min, notches 3 min per side, external minutes; nothing left running).
