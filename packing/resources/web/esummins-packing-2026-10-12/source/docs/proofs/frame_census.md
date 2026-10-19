# The frame census: RES(4) as a finite object, its bound, its count and its price — A91, 2026-09-03

Target (A91 BRIEF): enumerate the residue RES(4) of Theorem NOCRIT-SEL (`nocrit_k0_blocked.md`
§4) as an exact finite object mod D4, test geometric realisability in [1 + 2√2, ŝ] (and the
diamond-ghost regime [3.82, 1 + 2√2) below it), and price per-frame exclusion against A85's tree
(3 200–7 000 CPU-h). Labels: [T] proved, [S] routine given cited items, [M] measured (T2/T3,
`attempts/A91-frame-census/notes/`), [F] finding, [C] open. Conventions: `nocrit_k0_blocked.md`
(Lemma K, CLUSTER, COL, PLATEAU, RES(4), corner frame, depth d_c, argmin set S_c, retreat cone
K_c), `tilt_floor_k0.md` (LOCK, MENU, JAM-0, ID), `k0_route.md` (K0-FREE, K0-D4, reach sets),
`structure_lemmas.md` (L1, L6). m ∈ W = [3.82, ŝ], ŝ = 3.877083590…; m₀ := 1 + 2√2 = 3.828427.

## 0. Verdict

> **The frame census is finite, exactly countable at its skeleton levels, and astronomically
> large: L1 (roles, types, masks, one terminal per slot) = 5.73·10²⁸ frames mod G [EXACT lower
> bound labelled/|G|; MC 1.28·10²⁹ ± 1.3·10²⁸; 97 % trivial stabilisers], L0 = 1.9·10¹⁶, L2
> (first links) ≈ 10³⁷ orbits [MC bracket 10³⁹–10⁴¹ labelled], L3 (full columns) ≤ 1.6·10⁵⁹
> [EXACT upper bound], nonempty (the archetype is a witness). The whole combinatorial filter
> (Lemmas F1–F4, R1–R5) buys ×3.3 at L0 and ×2.9·10⁴ at L1; Lemma COL's ≥ 3-member clause is
> VACUOUS at L1 (Lemma F7 [T]). The box-level geometry (R6: interval-linear LP over roles,
> masks, Lemma K type rows, Lemma F6 link rows) kills 99.68 % ± 0.62 % of L2 frames at 3.8 ms,
> so the realisable census at L2 is ≈ 1.2·10³⁸ labelled [EXTRAPOLATED, bracket 10³⁶–10³⁹], price
> ≈ 1.3·10³² CPU-h against A85's 3 200–7 000: **the route loses by ~28 orders of magnitude**, and
> the 0.3 % of frames that survive the box LP — the archetype among them — are exactly the ones
> no box-level relaxation closes (the archetype stays open at tilt-bin depth 10, 111 boxes,
> margin +0.104). Canaries: archetype enumerated and untouched by R1–R5 (PASS), Trump absent
> (PASS), the four k0dir87 K0-BLOCKED endpoints satisfy every constraint of §2 on their real
> geometry (PASS). A90-G1 confirmed in numbers: ¬RES(4) is not a counting statement; it is paid
> as a SelForm (C) leaf in A85's tree (§9), price unchanged.**
>
> Correction to the chore's reading [T, §7.3]: the archetype's CLUSTERS are all WALL-anchored
> (every forward closure reaches a far wall through the slot squares 2/5 and the left-wall
> column 0/3/4); the "100 % (I)-anchored, 2-member columns" of `t2_report.md` is the
> minimal-chain extraction stopping at the first admissible (I)-terminal. Lemma PLATEAU is
> therefore NOT what the archetype family needs (§8): with the corner-weighted functional
> Ψ^(w) every rate-1 cluster is strictly anchored or wall-anchored (Lemma W-GEN [T]); the only
> plateaus left are tilted-D rate ties (codimension ≥ 1) whose slide iteration is the exact
> gap [C]. The residue that survives all of this is the wall-anchored frame — Trump's skeleton
> with tilted 2-crowds — and it dies only by geometry at localised nodes.

## 1. The frame, exactly

### 1.1 Roles

Fix a packing z ∈ M(m). For a corner c and a square Q write μ_c(Q) = min_{p∈Q} max(p_x, p_y) in
c's frame. Q is an **open intruder** at c if μ_c(Q) < 1 (d_c > 0), **tangent** at c if μ_c(Q) = 1,
and **free** if μ_c(Q) > 1 for all four corners. A square with μ_c(Q) ≤ 1 is a **home square** of
c; hc(Q) := c. K0-BLOCKED: every corner has n_c ≥ 2 open intruders.

**Lemma F1 (roles).** [T] (i) A square is a home square of at most one corner. (ii) n_c ≤ 5.
(iii) The K0-BLOCKED role patterns (n_BL, n_BR, n_TR, n_TL; f = 11 − Σ n_c free squares) are, mod
D4: (2,2,2,2; 3), (3,2,2,2; 2), (3,3,2,2; 1) with the two 3's adjacent or opposite, (4,2,2,2; 1),
(3,3,3,2; 0), (4,3,2,2; 0) with the 4 and the 3 adjacent or opposite, (5,2,2,2; 0) — nine
patterns.
*Proof.* (i) A home square of c contains a point of the closed box [0,1]² at c; two such boxes are
≥ m − 2 ≥ 1.82 > √2 apart. (ii) A home square of c lies within √2 of [0,1]², hence inside
[0, 1 + √2]² ∩ [0, m]², of area (1 + √2)² = 5.83; interior-disjoint unit squares → ≤ 5. (iii)
Enumerate n_c ≥ 2, Σ ≤ 11, n_c ≤ 5, mod D4. ∎

### 1.2 Types and slots

By Lemma K every open intruder Q at c has a retreat type τ(Q) ∈ {X, Y, D}: its cardinal retreat
set R(Q) is {e_x}, {e_y} or {e_x, e_y} (in c's frame; in container coordinates e_x = ±x, e_y = ±y
with the signs pointing away from c). A tangent square also has an argmin type by the same
trichotomy (Lemma K's proof uses only μ < ∞), which governs whether it deepens under a direction
(needed for (I)-terminals only); it has no retreat obligation. A **slot** is a pair (Q, e) with Q an
open intruder and e ∈ R(Q). Number of slots: n_X + n_Y + 2 n_D ∈ [8, 22].

### 1.3 Links, columns, anchoring

A **contact** between squares M, N with (any consistent selection's) active pair row has a contact
normal n_M on M (the direction of the force on M; n_N = −n_M). Its **sign class** is
σ(M, N) := (sign n_{M,x}, sign n_{M,y}) ∈ {−, 0, +}² ∖ {(0, 0)} (eight classes; σ(N, M) = −σ(M, N)).
N **presses M against e** iff n_M·e < 0 (Lemma CLUSTER's definition); so a contact presses M
against at most one x-direction and at most one y-direction, and N against the opposite ones. For
a corner-corner kiss (two admissible axes) "presses" means every admissible axis presses
(conservative, as in A90 T3).

A **column** for the slot (Q, e) is a sequence Q = N₀, N₁, …, N_k (k ≥ 1) of distinct squares with
N_{i+1} pressing N_i against e for every i, and a **terminal** N_k of one of two kinds:
 (W) N_k touches the far wall in direction e;
 (I) N_k is a home square of a corner c′ ≠ c that **deepens under e**: μ_{c′}(N_k + te) < μ_{c′}(N_k)
     for small t > 0 —
and no earlier member is a terminal (minimality). A column is exactly a witnessing chain for the
anchoring of C_e(Q) in Theorem NOCRIT-SEL: the cluster is the forward closure of "is pressed
by", so it is anchored iff such a chain exists. The **rate condition** [T, from the proof of
NOCRIT-SEL]: along the translation of the whole cluster C_e(Q) by te,
    Σ_{N ∈ C, hc(N) ≠ c, deepening} ρ_e(N) ≥ Σ_{N ∈ C, hc(N) = c or retreating elsewhere} ρ_e(N),
with the rates of Lemma K (an X/Y-type rate 1; a D-type rate ρ_x = n_x/(n_x+n_y) resp.
cos α/(sin α + cos α) < 1 unless axis-aligned, where it is 1); if C is wall-anchored the condition
is void (CLUSTER's motion is infeasible). Equality is Lemma PLATEAU's case.

**Definition (frame).** A frame is the data F = (roles, τ, ω, Γ): the role map with pattern in
Lemma F1(iii); the type map τ on home squares; the wall mask ω(Q) ⊆ {L, R, B, T} of walls touched;
and for every slot a column Γ(Q, e), such that the set of links used by all columns is
**sign-consistent**: every unordered pair {M, N} used as a link carries one sign class σ(M, N)
that presses in every direction the columns through it require. RES(4) at z is exactly the
statement that z's contact structure contains a frame with z's roles, types and masks, together
with the rate condition on every non-wall-anchored cluster.

### 1.4 Levels (the census is stratified)

 L0 (skeleton)   = (roles, τ, ω)                               [finite, small]
 L1 (anchoring)  = L0 + the terminal of every slot            [finite, product-counted]
 L2 (first link) = L1 + the first member N₁ of every column   [finite]
 L3 (frame)      = L1 + the full columns, sign-consistent      [finite; bracket]

Each level is a sound coarsening of the next (forgetting data), so ¬RES(4) is proved by killing
every L_k object at any k, and a kill at a coarser level covers all its refinements.

## 2. The combinatorial constraints [T]

**Lemma F2 (walls).** (i) A home square of c touches no wall but c's two (far walls are > 1.4
away, `tilt_floor_k0.md` §1). (ii) A square touching two adjacent walls at c has d_c ≥ 1/2, so it
is an open intruder at c; hence a free square touches ≤ 1 wall, and by the exact depth-pair census
(A89 §8.5: no surviving pair box has both members deep-capable at δ = 0.5, over A85's sound cover of
the reach set) **at most one home square per corner touches both of c's walls**. (iii) **Per wall
≤ 3 squares** (N1), and **≤ 1 free square per wall**.
*Proof.* (ii) If Q touches x = 0 at p = (0, a) and y = 0 at q = (b, 0), the segment pq ⊂ Q has
|pq|² = a² + b² ≤ 2, and on it max(x, y) is minimised where x = y, at value ab/(a + b) ≤ 1/2 (max of
ab/(a+b) on a² + b² ≤ 2 is at a = b = 1). (iii) Chord lemma: the chord of a unit square of tilt θ on
the line at distance 1/2 (perpendicular to a wall) from its extreme point toward that wall has length
≥ 1 — for θ ∈ [30°, 45°] it is (1/2)(cot θ + tan θ) = 1/sin 2θ ≥ 1, for θ ∈ (0°, 30°] the chord is
constant 1/cos θ ≥ 1 on the depth range [sin θ, cos θ] ∋ 1/2, and for θ = 0 it is 1. Squares
touching the right wall have pairwise disjoint (up to endpoints) chords on the line x = m − 1/2 inside
(0, m), each ≥ 1, so ≤ 3 since 4 > ŝ. A free right-wall square has its whole part in the strip
{x ≥ m − 1} outside the closed corner boxes, i.e. in y ∈ (1, m − 1), a segment of length m − 2 < 1.88
< 2: at most one chord ≥ 1 fits. ∎

**Lemma F3 (terminals).** Let (Q, e) be a slot at c with e the x-direction (y symmetric).
 (a) A (W)-terminal is a square touching the far x-wall: a home square of one of the two far
     corners c_e (adjacent to c along e) or c_op (opposite) with that wall in its mask, or the free
     square of that wall. At most 3 candidates (Lemma F2(iii)).
 (b) An (I)-terminal is a home square N of c_e or c_op whose argmin type at its corner is X or D
     (i.e. the axis of e is a retreat axis of N at its own corner); a home square of the corner
     adjacent to c across the other axis never deepens under e.
 (c) [T] Mutuality: if N is the (I)-terminal of Q's e-column then Q ∈ C_{−e}(N), −e is a cardinal
     retreat of N, and Q deepens under −e; if N is an open intruder the slot (N, −e) exists and Q is an
     admissible (I)-terminal for it. If neither C_e(Q) nor C_{−e}(N) is wall-anchored and the two
     clusters coincide, the rate condition holds in both directions only with EQUALITY (Lemma
     PLATEAU's plateau): a mutual (I)-column is never terminal; it slides to a wall contact, a new
     contact, or a K0-FREE point. The census keeps (I)-columns (sound); the plateau clause is a
     refinement NOT used here [C: well-foundedness of iterated slides is unproved].
*Proof.* (a) Lemma F2. (b) In c's frame e = +x; in the frame of c_e or c_op it is −x′, toward that
corner along its x′-axis, and μ_{c′} strictly decreases along −x′ iff x′ ∈ K_{c′}(N) (Lemma K: types
X, D); in the frame of the corner adjacent across y it is +x′, away from the corner, and μ is
nondecreasing. (c) Pressing is symmetric (∇_{c_M} g = −∇_{c_N} g on a pair row), so the reversed
chain presses each member against −e; N's type at c′ contains the x′-axis so −e ∈ K_{c′}(N); Q's
depth is piecewise-linear convex in t with positive right-derivative along e, hence strictly
increasing along −e. Rate condition both ways ⇒ Σρ_deep − Σρ_retreat ≥ 0 and ≤ 0. ∎

**Lemma F4 (column length; = Lemma COL).** For m ≥ m₀ every (W)-column has ≥ 3 members: Q, at
least one **middle**, and the terminal; the middle(s) touch no far x-wall (minimality) and, for a
3-column Q–M–R, M's centre lies within √2 of both Q's and R's — its e-coordinate in
[m − 1/√2 − √2, 1 + 1/√2 + √2] = [m − 2.12, 3.12], so M is not a home square of c or of the corner
adjacent across the other axis (their centres have e-coordinate < 1 + 1/√2 ≤ m − 2.12 for m ≥ m₀).
An (I)-column has ≥ 2 members. For m ∈ [3.82, m₀) a 2-member (W)-column exists only with both tilts
within 6.3° of 45° and d_c(Q) ≤ 0.0084 (Lemma COL's ghost clause).

**Lemma F5 (service capacity) [T, weak].** A square serves as (W)-terminal only for slots whose
direction points into its wall (a right-wall square: the x-slots of BL and TL home squares; ≤ n_BL +
n_TL ≤ 8 slots), as (I)-terminal only for slots of the two corners on its own far side along the
axis of its own type, and as a middle only through its contacts: ≤ 8 neighbours (the kissing
number of unit squares), so a square is the first link of ≤ 8 columns and, more loosely, a member
of columns through any of its ≤ 8 incident links. No counting bound below 11 squares
follows: three free squares can each be a middle of every column through the centre, and the
inner home squares of each corner are admissible middles for the opposite corners' columns —
this is A90-G1 ("counting alone does not exclude the frame"), now with the capacities named.

**Lemma F6 (link geometry) [T].** For a link (M → N, e): the centre difference d = c_N − c_M has
|d| ≤ √2 and d·u ≥ 1 for the contact axis u (unit, u·e > 0, both half-extents ≥ 1/2), hence
d·e > −1; and for a 3-column Q–M–R the terminal's centre is within 2√2 of Q's. These are the
box-level necessary conditions the census applies before any LP.

**Lemma F7 (COL is vacuous at L1) [T, T2 finding].** For a slot at c with far wall w, an
admissible middle is any square that is not a home square of the two corners opposite w and does
not touch w. The two corners OF w carry ≥ 4 home squares (K0-BLOCKED) while w carries ≤ 3 squares
(Lemma F2(iii)), so some home square of w's corners misses w and is an admissible middle: every L1
frame admits a ≥ 3-member column for every (W)-slot. Lemma COL kills nothing until the columns
themselves (L2/L3) are specified.

**Lemma F8 (the rate row is a filter) [T].** Under translation by e (c's frame, e = +x), members
with home corner in {c, c_cross} (the near side) have nonincreasing depth and the retreating
ones (types X/D) decrease at Lemma K's rate; members with home corner in {c_e, c_op} never retreat
and deepen iff their type contains the x-axis. Hence a non-wall-anchored cluster needs
Σ_{deep} ρ ≥ Σ_{retreat} ρ with ρ = 1 for X/Y types and axis-aligned D, ρ ∈ (0, 1) for a tilted
D-type. In particular an X/Y-type retreater whose cluster's only deepening member is one tilted
D-type square is NOT anchored: the cluster must extend to a far wall or to further deepening
members (this is the archetype's situation at its X-ends, §7.3). R4 of the spec admitted such
(I)-terminals without the rate row (sound, loose).

## 3. The bound before enumeration [T]

Let G_pat = Π_c S_{n_c} × S_f (relabelling within roles) and G = G_pat × D4, |G| ≤ 2⁴·3!·8 = 768
for (2,2,2,2; 3). Labelled counts (an orbit count is ≤ the labelled count and ≥ labelled/|G|):

 L0: Σ_patterns 3^{Σn_c} · 4^{Σn_c} · 5^f  ≤  9 · 12¹¹ + … ; for (2,2,2,2; 3): 12⁸ · 5³ = 5.4·10¹⁰
     labelled, ≤ 7·10⁷ orbits before Lemma F2's mask constraints (per wall ≤ 3, ≤ 1 free per wall,
     ≤ 1 both-walls square per corner), which the exact counter applies.
 L1: L0 × Π_slots (#admissible terminals) with #adm ≤ 3 (W) + n_{c_e} + n_{c_op} (I) ≤ 7 for
     (2,2,2,2; 3): ≤ 5.4·10¹⁰ · 7¹⁶ = 1.8·10²⁴ labelled, 2.3·10²¹ orbits, crude; exact value by the
     product formula Σ_{τ, ω} Π_slots A(slot; τ, ω) (T2).
 L2: L1 × Π_slots (#admissible first links) with #adm ≤ 10 (any other square; for a (W)-slot above
     m₀ not the terminal): ≤ L1 · 10¹⁶.
 L3: L2 × (chain completions), each chain a sequence of distinct squares: ≤ L2 · (10!)¹⁶ — finite;
     the exact count is bracketed by T2 (Burnside on the labelled group + MC).

So the census is FINITE at every level (the frame is a finite labelled object on 11 squares with
≤ 22 slots), and its L0/L1 strata are exactly countable; what makes it small or large is the
sign-consistency and the geometric realisability, not the combinatorics — the bound above is the
honest statement of A90-G1 in numbers.

## 4. The ghost regime [3.82, m₀)

Same frame with Lemma F4's k ≥ 1 for (W)-columns; a 2-member (W)-column Q–R carries the flags
tilt(Q), tilt(R) ∈ [38.7°, 51.3°] and d_c(Q) ≤ 0.0084, and its terminal R is a far-corner home
square or free wall square whose centre is within √2 of Q's — for R on the far wall this needs
c_R,e − c_Q,e ≥ m − 1/√2 − (1 + 1/√2) = m − 2.41 ≥ 1.41 with |d| ≤ √2: the two centres are
exactly diagonal-adjacent, so R is the far-corner home square adjacent to c along e, itself a
diamond in its own corner box. Bound: L1 gains ≤ 1 extra terminal per x-slot and y-slot (the
2-column option), a factor ≤ 2 per slot; the exact count is reported separately (T2, flag `ghost`).

## 5. D4

D4 acts on frames by its action on corners, walls and directions (types transform as directions:
rotations by 90° and the diagonal reflections swap X ↔ Y, the axis reflections fix types); orbits
are counted by Burnside over G = G_pat × D4 with Fix(g) by the same product formula restricted to
g-invariant labelled data (A88's `burnside88.py` method). Transport of kills across an orbit is
Lemma K0-D4 (`k0_route.md`).

## 6. Census specification (T2) and certificate form (T3)

T2 enumerates L0 and L1 exactly (canonical forms mod G), applies the necessary conditions R1–R5
(`attempts/A91-frame-census/notes/t2_spec.md`), brackets L2/L3 by Burnside + MC over L1 survivors,
tests realisability on samples (box tests, then the interval-linear LP of A88's triage adapted to
role/wall/link rows), and classifies survivors by corner sharing. Erratum to the spec's R5: the
free-square exclusion zone is the plus shape {centre : dist(centre, [0,1]²) < 1/2 at some corner},
NOT its bounding box (forbidding the box over-kills); the chore implemented the plus shape.
Erratum to the spec's C1 role list: Trump's sq8 is tangent at BR (μ = 1 exactly), like sq1 and sq9. Canaries: Trump-with-2-crowds
(roles BL{0,1}, BR{2,8}, TL{4,6}, TR{5,9}, free {3,7,10}, columns read off Trump's contacts) must be
a member at every level and survive R1–R5; Trump is absent (roles [1,1,2,1]); the four K0-BLOCKED
endpoints of k0dir87 must satisfy every constraint of §2 on their real geometry.

T3: per realisable frame the certificate is (K) a case-LP with the frame's rows as hypotheses
(roles → reach-set boxes, masks → wall rows, links → contact rows) or (C) a SelForm leaf; price =
count × per-frame cost vs 3 200–7 000 CPU-h.

## 7. Results [M] (`attempts/A91-frame-census/notes/t2_report.md`, `t3_report.md`; raw in
`results/census91*.json`, `samples91.jsonl`, `t3pilot91.json`, `canary91.json`)

**7.1 Counts.** 89 colours (open intruder 48, tangent 36, free 5), 165 shapes, 35 ordered role
patterns. L0 labelled 1.040·10¹⁹ [EXACT], orbits ≥ 1.249·10¹⁶ (MC 1.88·10¹⁶ ± 5·10¹⁴); L1 labelled
1.558·10³² [EXACT, product formula validated against brute force on 8 shapes to 2·10⁻¹¹], orbits
≥ 5.726·10²⁸ (MC 1.28·10²⁹ ± 1.3·10²⁸, 97 % trivial stabilisers). Tangent flags cost ×22 at L0, ×1.24
at L1. (2,2,2,2; 3) is 41 % of L0 and 0.6 % of L1: the count is dominated by (3,3,3,2)-type
patterns. Ablation [EXACT]: roles only L1 = 4.50·10³⁶ (= §3's 7-per-slot bound); + F2(ii)
9.30·10³²; + per-wall ≤ 3 and ≤ 1 free per wall 1.558·10³². L2: E[#first-link vectors per L1 frame]
= 2.4·10⁸ ± 2.7·10⁸ ⇒ ≈ 3.8·10⁴⁰ labelled [MC, bracket 10³⁹–10⁴¹], ≈ 10³⁷ orbits. L3: ≤ 1.56·10⁵⁹
chain systems [EXACT UB]; sign-consistency passes 0/20 random chain systems on the median frame
(point estimate 5·10⁵⁰, one significant figure). Ghost census (2-member (W)-columns flagged):
same order (≤ ×2 per slot).

**7.2 Realisability and sharing.** R6 = interval-linear LP (23 variables, tilt bins on [0°, 45°];
rows: containment, wall masks, corner intrusion, Lemma K argmin-side type rows — X ⇒ y − x ≤
−cos θ_hi, Y ⇒ x − y ≤ −cos θ_hi, D ⇒ |y − x| ≤ cos θ_lo in c's frame — and Lemma F6 link rows):
kill 315/316 = 0.9968 ± 0.0062 at ~4 ms; the archetype survives with margin +0.104. Realisable at
L2 ≈ 1.2·10³⁸ labelled [EXTRAPOLATED; CI 0–2.4·10³⁸; with the L2 bracket 10³⁶–10³⁹]. Corner
sharing over the 316 R6 survivors: every frame shares column members across all six corner
pairs; a mean 0.33 free squares act as middles and a mean 6 squares serve two corners — the
sharing is carried by the crowds themselves (A90 §4.4 quantified).

**7.3 Canaries.** C1 archetype: roles BL{0, 1(tangent, X)}, BR{2, 8(tangent, D)}, TL{4(Y), 6(X)},
TR{5, 9(tangent, D)}, free {3, 7, 10}; 13 slots; member of L0/L1/L2/L3, passes R1–R5 and sign
consistency; NOT killed by R6 or by the B&B (open at depth 10). Its true clusters [M, this file's
check with A90's `cluster`]: C_{+x}(1) = {1, 2, 8, 10} wall-anchored at x = s; C_{+x}(6) = {5, 6, 9,
10} at x = s; C_{−x}(8) = {0, 1, 3, 4, 7, 8} and C_{−x}(9) = {0, 3, 4, 6, 7, 9} at x = 0; C_{+x}(0),
C_{+y}(0), C_{−x}(2), C_{−x}(5), C_{−y}(4) all wall-anchored — every slot is (W); the rate-1
pairs (1, 8) and (6, 9) are balanced inside wall-anchored clusters, so no plateau exists there.
C2 Trump: open intruders (1, 1, 2, 1), absent. C3: s0380 (11/12 slots anchored), s0076 (7/12),
s0380′ (8/12), s0259 (6/12): every constraint of §2 holds on the real geometry (they are not
Ψ-minimal minimisers, so unanchored slots are expected).

**7.4 Price (T3).** 20/20 uniformly drawn frames close at the ROOT LP in 3.8 ms (range 3–5 ms) —
the generic frame's certificate is one LP; the archetype does not close at any reachable tilt
resolution (111 boxes, 0 kills, all bins below 10⁻³ rad). Total ≈ 1.2·10³⁸ × 3.8 ms ≈ 1.3·10³²
CPU-h vs 3 200–7 000 CPU-h: loses by ~28 orders at L2; applying the (weaker) geometry at L0 would
still be 1.9·10¹⁶ × 3.8 ms = 2·10¹⁰ CPU-h. The route loses twice: on the count and on the survivors.

## 8. Lemma PLATEAU: what it must prove, what is proved, the gap

**8.1 The statement needed.** Let z* be a Ψ-minimal σ-minimiser, (Q, e) a slot, C = C_e(Q) not
wall-anchored and BALANCED (Σ_deep ρ = Σ_retreat ρ, Lemma F8). Required: (i) the slide z_t = z* +
te on C is a packing at side m with Ψ(z_t) = Ψ(z*) for t ∈ [0, t₁], t₁ > 0 the first event — (a) a
new active row, (b) a retreating member's depth reaches 0, (c) an argmin-type change; (ii) z_{t₁}
is again Ψ-minimal, hence RES(4) or K0-FREE; (iii) iterating (i)–(ii) over all balanced slots
TERMINATES at a Ψ-minimal minimiser that is K0-FREE (then Lemma K0-FREE closes) or whose every
cluster is wall-anchored or strictly anchored (then RES(4) holds in its (W)/strict form and Lemma
COL applies to every column). (i)–(ii) are A90 §4.3 [T]: rows and depths are affine on the
segment (Fact A, Lemma K), CLUSTER's margin argument gives feasibility up to the first
activation, M(m) is closed, t₁ ≤ m (the retreating member's far-wall row decreases at rate 1).

**8.2 Lemma W-GEN [T] — the weighted selection removes every rate-1 plateau.** Replace Ψ by
Ψ^(w) := Σ_c w_c Σ_i d_c(Q_i) with positive weights (w_BL, w_BR, w_TR, w_TL) linearly independent
over ℚ (e.g. 1, π, π², π³). Theorem NOCRIT-SEL holds verbatim for Ψ^(w) (its proof uses only:
the retreating member's own term strictly decreases and every other member's term is
nonincreasing under ¬(I); positive weights preserve both), and so do SEL-Ψ and the composition
of A90 §6 (Ψ^(w) is continuous). At a Ψ^(w)-minimal minimiser the right-derivative of Ψ^(w)
along the slide of a non-wall-anchored cluster is D = Σ_{deep} w_{hc(N)} ρ_N − Σ_{retreat}
w_{hc(M)} ρ_M ≥ 0, with retreating corners ⊆ {c, c_cross} and deepening corners ⊆ {c_e, c_op}
(Lemma F8: disjoint sets). If every rate involved is 1 (types X/Y, axis-aligned D), D is a
ℤ-combination of the weights with a nonempty support on the retreat side, hence D ≠ 0 by
ℚ-independence, hence D > 0: the cluster is STRICTLY anchored, no plateau. Consequently
(a) a mutual rate-1 column (X–X, Y–Y, or with axis-aligned D ends) never has both clusters
non-wall-anchored: the two derivatives are ±D with D ≠ 0, and the negative one contradicts
minimality — at least one end is wall-anchored and the other is strictly anchored;
(b) a plateau requires a tilted D-type member whose rate ρ(θ) = cos α/(sin α + cos α) (or the
edge form n_x/(n_x + n_y)) satisfies one polynomial identity in the tilts of the cluster's
members — a set of codimension ≥ 1 in tilt space. ∎

**8.3 The exact gap [C].** For the tilted-D tied clusters, (iii) — termination of the slide
iteration — is unproved: each slide ends at an event and the endpoint is again Ψ^(w)-minimal,
but no potential is known that decreases across slides (a slide can LOSE active contacts with
positive slope and gain one; the lexicographic refinements (Ψ^(w), Ψ_BL, Ψ_BR, Ψ_TR, Ψ_TL) forbid
slides toward lower-priority corners only, and Σ d² is convex along a slide, so a Ψ₂-extremal
selection constrains the initial derivative, not the endpoint), and an accumulating (Zeno)
sequence of slides is not excluded. What would close it: a functional on M(m), continuous,
strictly monotone along every balanced slide whatever its direction — none of the candidates
tried (Ψ_c per corner, moments of inertia, Σ d_c², active-row counts) has a sign independent of
the slide's direction. **Even closed, PLATEAU leaves the wall-anchored frames** (the archetype:
all slots (W), columns of 3–5 members) as the residue, which §7 shows is not a counting kill.

## 9. Consuming the anchoring rows in A85's tree (design, not run)

At a node of A85's k0_00 tree every crowd square is in a reach box B (centre box × tilt bin) and
the free squares in zone boxes. The frame data are then DETERMINED or BOUNDED per node:
 (1) roles: a box inside c's reach set is a home square of c (the node's crowd hypothesis);
 (2) types: T(B) := the set of τ ∈ {X, Y, D} whose type row (§7.2) is satisfiable on B; a box
     with T(B) ⊆ {X, D} has +x as a FORCED retreat, T(B) ⊆ {Y, D} forces +y; T(B) = {X, Y, D}
     forces nothing (Lemma K: at least one cardinal, but which is unknown) — still, D ∈ T(B) is
     needed for "both" and the disjunction X ∨ Y ∨ D is a 3-way case split the tree may take;
 (3) anchoring existence (the SelForm (C-sel) leaf of A90 §6): for every forced slot (B, e) test
     whether SOME chain of boxes B = B₀, B₁, …, B_k exists with consecutive boxes touch-capable
     (box distance ≤ √2 and (c_N − c_M)·e > −1 realisable, A88's TOUCH tables lifted to A85's
     boxes) and B_k far-wall-capable (its centre box within 1/√2 of the wall) or (I)-capable (a
     home box of c_e/c_op with the axis of e in T(B_k)) subject to Lemma F8's rate row on the
     rate bins ρ(T(B), tilt bin) — a graph search on ≤ 11 boxes, microseconds; no chain ⇒ the node
     is killed for the Ψ^(w)-minimal minimiser (StratumKillSel, A90 §6).
It is sound as stated (every quantity is an outer bound of the true frame data) and consumes
Ψ^(w)-minimality only (no FJ, no H1). Its effect is the existential-filter law (A43/A88): at the
pair-box level the test asks for the EXISTENCE of a chain among coarse boxes, which R6's 99.7 %
kill (frames with links SPECIFIED) says nothing about; A85/A89/A90's expectation is "free at deep
nodes, silent at the frontier". To price it: one Opus chore (~1 desktop-hour): implement (1)–(3)
on A85's stored nodes (`attempts/A85-k0-route/results/a85_gate_samples.json`: 1 000 four-corner
pair-box nodes, 300 three-corner, 300 two-corner; the 12 LP nodes of `a85_lp_samples.jsonl`),
measure the kill fraction per level and per tilt bin ON TOP of the exact contradictory gate
(81.9 % at four corners), and the fraction of the 17.9 % attemptable four-corner nodes it
removes; the tree's price moves by that factor on the four-corner frontier and not at all on
the depth-2 interior cells (A85 §7.3), which carry the measured 3 200–7 000 CPU-h.

## 10. Obligations ledger

| # | item | status |
|---|---|---|
| A91-O1 | frame as a finite object (L0–L3), Lemmas F1–F8, D4, ghost regime | [T] §1–§5 |
| A91-O2 | bound before enumeration | [T] §3 (crude; exact L0/L1 by the product formula) |
| A91-O3 | exact census L0/L1, brackets L2/L3, ablation, canaries C1–C3 | [M] §7.1–7.3 |
| A91-O4 | realisability R6 + sharing distribution | [M] §7.2 |
| A91-O5 | price vs A85's tree | [M] §7.4 — loses by ~28 orders; verdict A90 §6(i) stands |
| A91-O6 | Lemma W-GEN (weighted selection kills rate-1 plateaus) | [T] §8.2 |
| A91-G1 | PLATEAU termination for tilted-D ties | **OPEN** §8.3 (not load-bearing for the archetype, which is wall-anchored) |
| A91-O7 | anchoring rows as (C-sel) node tests in A85's tree | design §9; priced as a 1-desktop-hour chore, not run |
