# Grain discharge near Trump: local completeness, the rigid/flex dichotomy, and the hinge wall — A76, 2026-09-02

Target (A76 BRIEF, PI's bottom-up direction): grow the certified exclusion region around Trump's
packing ẑ OUTWARD, grain by grain (grain = contact structure), on the K1-protected exact strata
(k ≤ 4 tier), and hand the radius R to the pair-LP as the enlarged basin-exclusion row P-B(R)
(`pair_kill.md` §6.8). Everything is in t = tan(θ/2) coordinates (E.COORD), Trump's frame (the
D4 images are handled by pulling the packing back, §6), with the pins of the class as EXACT linear
rows. Labels: [T] proved, [S] routine given cited items, [M] measured/computed exact (interval)
or float (stated), [C] open. Code: `attempts/A76-grain-discharge/code/`; certificates:
`attempts/A76-grain-discharge/certs/grain_*.json`, checker `certs/verify_grain.py` (stdlib,
exact rationals, monotone rational trigonometry, 5 corruption gates).

**Headline (findings first).** (i) Local completeness is a theorem with an exact certificate
(Lemma G-R, §1): on the box B = ẑ ± (r_c = 10⁻², r_t = 2·10⁻³, r_s = 10⁻²) every contact of every
packing is one of 78 explicitly listed corner–edge/corner–wall rows (36 Trump rows, 20 edge-end
coincidences of the flush uprights, 22 contact-type switches), out of 1936 candidates — BY
CONSTRUCTION, not by search. (ii) The grain lattice of k4_08 in Trump's frame has 1.7·10⁷
grains (§2); every grain is either RIGID (rank 34: Krawczyk gives z = ẑ, excluded by the exact
stratum) or S-FLEXIBLE (rank < 34: the drain-flex Lemma DF, §3, gives a feasible curve that
strictly decreases the side, so the packing is not a minimiser) — there is no third case within
Trump's row set ([T], §3.4: no positive dependency at ẑ, and e_s ∉ span of any proper
sub-basis). (iii) **THE WALL [M]:** both discharges are box-nonsingularity certificates, and
their radius is governed by the same constant that capped A36/A40 (ω_b = 1/κ_eff = 0.052
reappears as the drain-flex ratio of the HINGE grains: a flush pair of the tilted strip degraded
to a single-corner contact). At the target box the census finds 13 702 hard grains among the
143 370 of co-dimension ≤ 4 (ratios up to 48); the all-pass box is ≈ 10⁻⁴, i.e. **A76 certifies
no radius beyond A22/A36/A40 for stuck minimisers of the exact strata**. The grain structure
turns the wall into a covering problem whose cost is ~ratio^d per hard grain of co-dimension d
(size law §5); the priced residue is a d-dimensional continuation campaign (~10⁷ Krawczyk
steps for (10⁻², 2·10⁻³)), for a gain of ≤ 1.5× over A40 in centre radius and none in tilt. The
supplied radius for P-B(R) is therefore the per-coordinate reading of the existing basin
theorems (§7): (r_c, r_t) = (3.7·10⁻³, 1.85·10⁻³) from A36 (exact-checked), (6.55·10⁻³,
3.27·10⁻³) from A40 (now EXACT-rechecked, §7), versus the uniform 3/2000 in use.
(iv) Trivial radii: k4_05 and corners4 have no compatible Trump image; within d_min = 0.4365
resp. 0.8445 (sup-norm, any coordinate) of ANY Trump image no exact packing of these classes
exists at all (§6). (v) By-product: the first t-native exact Krawczyk enclosure of ẑ
(`grain_trump_tnative_r5e-4.json`, ratio 0.103 at 1/2000; contracts up to the uniform t-box
1/250) — the E.COORD re-emission of A22's rigidity rung in rational trigonometry.

## 0 Setting and conventions

Configuration z ∈ R³⁴: (cx_i, cy_i, t_i) for i = 0..10 and s = z₃₃; corners q_k(i) = c_i +
R(t_i)h_k with cos = (1−t²)/(1+t²), sin = 2t/(1+t²). Trump's contact configuration ẑ is the
unique zero of A22's 34-row system S in its box (A22 notes §3: uprights exactly upright, c₀ =
(½,½), c₁ = (3/2,½), c₃ = (½,3/2), c₂ = (ŝ−½,½), c₅ = (ŝ−½,ŝ−½)); z0 is A22's 60-digit rational
centre converted to t (tilted squares: 70-digit rationals, `results/z0_t.json`; uprights
snapped to the exact structure); centre residual of all 42 Trump rows ≤ 6.0·10⁻⁶⁰ [M exact].
A box is B = z0 ± (r_c on centres, r_t on tilts, r_s on s), ∞-norm; "R" below always means
this triple. Row functions (g ≥ 0 where used as inequalities): wall (containment), edge
(corner k of square i beyond edge e of square j), dist, teq (t_i − t_j), pin rows
(cx_i − α − βs, cy_i − α − βs, t_i for a Trump slot), and the formal row ES (value 0, gradient
e_s). The Trump-frame pin set of a class S under a compatible image g is P = g⁻¹·pins(S) ⊆
{0,1,2,3,5} (§6); a pin is a square exactly at its slot, i.e. three linear equalities.

Consumer (what must be excluded): a teleport-stuck global minimiser z of σ with σ(z) = m̃ ≤ ŝ,
skeleton EXACTLY S (`unique_transfer.md` §2–3, `pair_kill.md` §6 Lemma P-B), lying in B after
the D4 pull-back. Minimiser ⇒ every hypothesis below marked (min).

## 1 [T] Lemma G-R (local completeness by construction)

**Lemma G-R.** Let z ∈ B be any packing (11 closed unit squares in [0, s]², s = z₃₃, pairwise
interior-disjoint). Then every pair contact of z is witnessed by a corner–edge row
E{i}c{k}-{j}e{e} with value 0 and tangential coordinate in [−½, ½], and every wall contact by a
corner–wall row with value 0. Consequently the active contact set of z is a subset of

  PA(B) := { candidate rows r (176 corner–wall + 1760 corner–edge) : 0 ∈ [g_r](B), and for
             edge rows [τ_r](B) ∩ [−½, ½] ≠ ∅ },

where [·](B) are the exact interval enclosures over B.

*Proof.* Two convex polygons with disjoint interiors that touch have a nonempty contact set
K = Q_i ∩ Q_j ⊆ ∂Q_i ∩ ∂Q_j. Pick p ∈ K. If p is a corner of Q_i, then p lies on an edge
segment of Q_j (p ∈ ∂Q_j), and the row "corner p of i on that edge of j" has depth g = 0 and
tangential coordinate in [−½, ½]; symmetrically if p is a corner of Q_j. Otherwise p is interior
to an edge of each square; the two edges pass through p with Q_i, Q_j on opposite sides (a
separating line through p exists and contains both edges near p), so the edges are collinear
and K is a segment whose endpoints are corners of the squares — apply the first case to an
endpoint. Wall contacts: a corner of the square lies on the wall (the extreme point of a convex
polygon in a direction is attained at a vertex). The enclosures are sound: `verify_grain.py`
evaluates every candidate row over B in outward-rounded exact arithmetic with the monotone
rational-trig enclosures (cos even/decreasing in |t|, sin increasing, dcos decreasing on
|t| < 1/√3, dsin even/decreasing — elementary derivative signs, in the checker's docstrings), so
a row with 0 ∉ [g_r](B) or [τ_r](B) ∩ [−½,½] = ∅ is inactive-or-non-contact everywhere on B. ∎

**Certificate [M exact].** `grain_k4_08_rc1e-2_rt2e-3.json` [PA]: on B = (10⁻², 2·10⁻³, 10⁻²),
|PA| = 78: the 36 A22 contact rows; 20 edge-end coincidence rows of the flush uprights (0,1),
(0,3) and the corner–corner pair (1,3) (e.g. E1c0-0e1, E0c1-1e0 — all among the pinned squares
of k4_08, hence fixed); and 22 NEW rows that are inactive at ẑ but reachable on B — the
contact-type switches: sq7's corner 3 onto sq4's bottom/right edge (E7c3-4e0/e1, the blocked
slide of A53's Trump canary, gap 0.0126), the reversed 3–7 and 4–7 contacts (E3c2-7e2,
E7c3-3e1/e2, E4c1-7e3), the strip gaps 6–7 and 8–9 (E6c0-7e2, E7c2-6e0, E8c2-9e0, E9c0-8e2),
and the endpoint switches of the four ring flush pairs (E7c1-9e0/e3, E7c2-9e2, E8c1-10e0/e3,
E8c2-10e2, E9c0-7e0, E9c3-7e1/e2, E10c0-8e0, E10c3-8e1/e2). Size law of the row universe
(anisotropic boxes, exact, `logs/pa_scan2.log`): |PA| = 56 for r_c + 1.4 r_t ≲ 6·10⁻³ (no new
row: the first entrant is the 7–4 slide at uniform r = 4·10⁻³), 78 at (10⁻², ≤ 2·10⁻³), 86 at
(1.5·10⁻²…4·10⁻², 2·10⁻³) (adds the 3–4 and 4–3 upright switches). Uniform t-boxes: 56 rows to
3·10⁻³, 58 at 4·10⁻³, 78 at 5·10⁻³.

The A37/A51 atlas lesson is honoured: the universe is generated by the checker, not by the
producer, and completeness is the lemma above, not a search.

## 2 The grain lattice (by construction)

A **grain** is an active-row pattern. Rows come in contact GROUPS with finite STATE lists; a
grain is a choice of state per group (plus the pins, always active). For k4_08 in Trump's frame
(pins 0,1,3,5; `code/census.py`):

* flush tilted pairs (6,9), (7,8), (7,9), (8,10), (9,10): states FLUSH = {corner row a, tie
  t_i − t_j} (rank 2), PA = {a}, PB = {b} (single-corner "hinge" contacts, rank 1), OPEN;
* point contacts 1–8, 2–8, 3–7, 4–7, 4–6, 5–9: ON/OFF;
* wall rows of the unpinned squares: sq2 (4 rows, 16 subsets), sq4 (2 rows), sq6, sq10;
* (for classes with unpinned uprights) the flush-upright and corner–corner rows of (0,1),
  (0,3), (1,3).

Identities used to pick independent representatives [T]: (i) the four wall rows of a corner
square satisfy (q₀ₓ − q₃ₓ) − (q₁ᵧ − q₀ᵧ) ≡ 0 identically (rank 3 everywhere; the fourth row is
implied by the other three); (ii) FLUSH TIE IDENTITY: for a flush pair with antipodal contact
corners h_a = −h_b and opposite owner edges, g_a − g_b ≡ 0 on {t_i = t_j} (n_j·R(h_a + h_b) = 0),
so "both corner rows active" ⟺ "one corner row + tie" on B (two contact points force a
segment contact, hence parallel edges, hence t_i = t_j by the tangential margins); (iii) the
four ring ties form a cycle (rank 3). The pins' own contact rows (walls of 0,1,3,5, D0-1, D0-3,
the flush-upright coincidences) are implied by the pin rows. Exact-stratum consistency: the
broken pin's slot pattern (two corners on one wall + one on the adjacent wall ⇒ at the slot) is
the FULL state of its wall group, excluded by hypothesis; all other states are admitted (empty
states are harmless — they need no certificate but cost none of the completeness argument).

Counts [M]: 15 groups, 4⁵·2⁶·16·4·2·2 = 16 777 216 grains for k4_08; by co-dimension d = 34 −
rank at ẑ: d=0: 45 (rigid), d=1: 734, d=2: 5 782, d=3: 29 319, d=4: 107 535, d=5: 45 712,
d=6: 924 among those with rank ≥ 28, the rest deeper. Every grain is ⊇ a basis (d = 0) or is
itself S-flexible; the discharge only ever needs (K) on bases and (DF) on the grain's own
independent representative (§3), and (DF) is DOWNWARD-closed (a certificate for A covers every
A″ ⊆ A, §3.2), (K) UPWARD-closed — so a finite antichain of certificates + a split tree over
groups covers the lattice; the checker's [K]/[D1] blocks are the leaves of that tree
(`verify_grain.py` header; the tree itself is trivial combinatorics).

## 3 [T] The discharge lemmas

### 3.1 Lemma K (rigid grains)

Let A be a grain whose independent representative A′ has rank 34 at ẑ, and let
`verify_grain.py` [K] PASS for a 34-row basis F ⊆ A′ ∪ pins on B (Krawczyk: K(B) = −Y F(z0) +
(I − Y[J](B))(B − z0) ⊂ int(B − z0)). Then every packing z ∈ B whose active set contains A is
Trump's packing ẑ. *Proof.* Krawczyk (Neumaier 5.1.7): F has exactly one zero in B; ẑ ∈ B
(|ẑ − z0| ≤ 10⁻⁵⁰, A22) and every Trump row and pin row vanishes at ẑ (A22 §3 exact structure),
so the zero is ẑ; z has F(z) = 0. ∎ Consequence for exact strata: ẑ has five simple squares
(trump5), so **no packing in B with a rigid grain lies in an exact class of the k ≤ 4 tier**
— the class hypothesis is used here and only here. (This is also the Trump canary of §8: the
rigid grain's unique solution IS Trump, never "excluded" by a certificate.)

Rigid grains containing NEW rows (§1) have ẑ ∉ their variety; Krawczyk at z0 then either
proves the variety empty in B (K(B) ∩ (B − z0) = ∅) or isolates a different critical point z*
whose side must be compared with ŝ (the "isolated CP with σ > ŝ" branch of the BRIEF). None
was needed for the certificates below (the new rows only enter at the target box, whose full
discharge is the open residue of §5); the machinery is generic.

### 3.2 Lemma DF (drain-flex: s-flexible grains are not minimisers)

**Lemma DF.** Let z ∈ B be a packing with active contact set A (all other candidate rows
strictly positive at z), let A′ ⊆ A be an independent representative such that every row of
A \ A′ is implied by A′ on B (identities (i)–(iii) of §2; pins included in A′), and suppose

  (DF)  for every ζ ∈ B, e_s ∉ span{∇g_a(ζ) : a ∈ A′} and these gradients are independent.

Then z is not a minimiser of σ: there is a smooth curve of packings through z along which the
container side strictly decreases. *Proof.* By (DF), the map G = (g_a)_{a∈A′} has full-rank
Jacobian at z, so V = {G = 0} is a smooth manifold near z (implicit function theorem) with
tangent space T = ker J_{A′}(z). Since e_s ∉ rowspace(J_{A′}(z)) = T^⊥, some y ∈ T has
e_s·y < 0. Take a smooth curve γ ⊂ V with γ(0) = z, γ′(0) = y. Along γ: the rows of A′ stay 0
(definition of V), the rows of A \ A′ stay 0 (implied), every other candidate row is > 0 at z
and stays > 0 for small parameter (continuity), and the pin rows stay 0. Hence γ(τ) is a packing
with the same contacts (Lemma G-R: nothing else can touch on B) at side s(γ(τ)) = ŝ_z +
τ(e_s·y) + O(τ²) < s(z) for small τ > 0. ∎ (Pins ride with the container: the pin rows are
part of A′, so the curve keeps them exactly at their slots of the shrinking side.)

**Certificate [D1].** With M(ζ) = [J_{A′}(ζ); e_s] ((|A′|+1) × 34) and a rational 34 ×
(|A′|+1) matrix Y, the check ‖M(B)Y − I‖_∞ < 1 (row-sum norm of the interval matrix) proves
M(ζ)Y nonsingular for every ζ ∈ B, hence M(ζ) of full row rank, i.e. (DF). Y is the rational
rounding of the float pseudo-inverse of M(z0); the checker never trusts it.

**Downward closure [T].** (DF) for A′ implies (DF) for every A″ ⊆ A′ (smaller span); so a
[D1] certificate for a grain discharges every grain with fewer active rows (subject to the
same implied-row bookkeeping), and the hard part of the lattice is its TOP (few contacts
broken), which is where the hinge grains live (§4).

### 3.3 Lemma D2″ (chain necessity — a free structural pruner)

**Lemma D2″.** Let z be a packing at side m̃ and, for an axis a ∈ {x, y}, let G_a be the graph
on the 11 squares plus the two a-walls, with an edge for each square–square contact and each
square–a-wall contact (contacts with the other two walls are NOT edges: sliding along them is
free). If z is a minimiser of σ, then for some binding axis a (the a-extent equals m̃) G_a has a
path from the far a-wall to the near a-wall. *Proof.* Suppose not. For each binding axis a, let
C_a be the connected component of the far a-wall in G_a; it misses the near a-wall. Translate
all squares of C_x by (−ε, 0) and all squares of C_y by (0, −ε) (a square in both moves
diagonally; if only one axis binds, only that move). Contacts inside a component are preserved
by its rigid translation; a contact between a moved and an unmoved square, or between the
x-moved and the y-moved sets, would be an edge putting both in the same component — impossible;
sliding along the non-a walls is free; squares of C_a keep positive clearance from the near
a-wall; every unmoved square has positive clearance from the far a-wall (else it would be in
C_a). So for small ε the family is a packing whose binding extents all drop by ε: σ decreases.
∎ In Trump's frame every x-chain and every y-chain passes through the tilted strip (the
uprights touch no far wall square directly), so a minimiser's grain must contain a wall-to-wall
path through the strip: the "floating strip" grains (all strip-external contacts open) are
excluded outright, at ANY radius, with no arithmetic. (Not needed for the discharge count below
— those grains are S-flexible with tiny D1 ratios — but it is the bottom-up analogue of L6
without Fritz-John, and it is exact.)

### 3.4 [T+M] The dichotomy is exhaustive on Trump's rows; FJ/Gordan is available but weaker

At ẑ, A22's multiplier λ on the basis S is unique and strictly positive (min 0.0175). For any
grain A ⊆ (Trump rows) with rank < 34: if e_s ∈ span(∇g_A(ẑ)) then, writing this combination
over S (every Trump row is in span S, the redundant rows through the identities of §2), we get a
second representation of e_s over the basis S, hence λ_k = 0 for the rows of S outside A —
contradiction. So **every proper sub-grain is s-flexible at ẑ and every rank-34 grain is
rigid: no grain needs a second-order (inequality) certificate at ẑ.** [M float] There is no
positive dependency among the 50 candidate rows at ẑ (max Σλ subject to Σλ_k∇g_k = 0, 0 ≤ λ ≤ 1,
equals 0), so the λ₀ = 0 branch of Fritz John never occurs and a Gordan direction exists for
every FJ-infeasible grain; 21 rows carry λ_k > 0 in EVERY FJ solution (`logs/`, min λ: E10c3-9e0
0.0103, E9c0-7e1 0.0205, E8c2-10e3 0.0346, …, W10c1[x=s] 0.32) — the smallest necessary
multipliers sit exactly on the ring's flush pairs, the hinge modes of §4. The Gordan test over
a box needs the direction y to open every active row strictly, so for a grain missing a
necessary row k it must close k at rate ≥ 1/λ_k and its box radius is ≲ λ_k/(‖J⁻¹‖·L) — worse
than (DF), which only needs e_s ∉ span. The third tool, the mixed inequality certificate
(A22's positive-spanning form with the active rows as free-sign equalities; A36's max-form;
A40's anchor form), is what A36/A40 already deployed stratum-blind up to 3.7·10⁻³ / 6.55·10⁻³
(θ-world) — at ẑ it exists for every grain, and its radius is capped by the same constant.

## 4 [M] Radii: the measurements

All boxes are (r_c, r_t, r_s = r_c) unless stated; "t-uniform r" = (r, r, r). Ratios are the
exact interval quantities of the certificates (Krawczyk max|K_i|/r_i; D1 row-sum norm), except
the census (§4.3), which uses the float proxy Σ_c hw_{ic}|Y_cj| with exact half-widths hw
(identical up to the centring of the enclosure).

**4.1 Rigid grain (Lemma K), Trump's own contact structure.** t-uniform: A22's S contracts at
r = 1/2000 (0.103), 1/500 (0.413), 1/250 (0.827); fails at 3/500 (1.24). Pinned bases: k4_08
0.749 / k4_11 0.765 / k4_03 0.752 / trump5 0.740 at 1/250 — the pins buy ≈ 10 % in the uniform
radius. Anisotropic, pinned k4_08: (10⁻², 2·10⁻³) 0.818 PASS, (10⁻², 10⁻³) 0.751, (2·10⁻²,
10⁻³) 1.44 FAIL, (4·10⁻³, 10⁻²) 3.3 FAIL; unpinned S already fails at (10⁻², 2·10⁻³) (1.125): the
pins DOUBLE the admissible centre radius (5·10⁻³ → 10⁻²) while the tilt radius is capped at
≈ 4·10⁻³ either way. Certified: `grain_k4_08_rc1e-2_rt2e-3.json` [K] (ratio 0.8176) and the
unpinned t-native enclosures at 1/2000 and 1/250.

**4.2 Drain-flex radius law vs co-dimension** (pinned k4_08, random drops of d rows from the
22 free basis rows, 6 samples each, ratio at (4·10⁻³, 4·10⁻³) / (10⁻², 2·10⁻³)):
d=1: 0.7–2.5 / 0.75–3.6; d=2: 0.6–1.3 / 0.7–1.6; d=3: 0.4–0.9 / 0.35–1.3; d=5: 0.2–0.7; d=8:
0.19–0.34 / 0.18–0.34; d=12: ≈ 0.15; d=18: 0.01–0.36. **The fewer contacts a grain keeps, the
farther it drains**: grains with ≥ 8 contacts broken pass at boxes ≈ 5× the target; the top
of the lattice is the only hard part.

**4.3 Hard-grain census** (`code/census.py`, all grains of co-dimension ≤ 4 of k4_08; "hard" =
D1 ratio ≥ 1, i.e. not dischargeable on that box as a whole):

| box (r_c, r_t) | hard / 143 370 | d=1 (734) | d=2 (5 782) | d=3 (29 319) | d=4 (107 535) | max ratio |
|---|---|---|---|---|---|---|
| (10⁻³, 10⁻³) | 113 | 64 | 43 | 6 | 0 | 10.7 |
| (2·10⁻³, 2·10⁻³) | 335 | 139 | 134 | 56 | 6 | 21.4 |
| (5·10⁻³, 10⁻³) | 658 | 164 | 272 | 173 | 49 | 23.9 |
| (10⁻², 2·10⁻³) | 13 702 | 405 | 1 886 | 4 755 | 6 656 | 47.8 |

The worst grains, at every box: two flush pairs of the ring 7–8–10–9 degraded to single-corner
hinges (flush7-9 = PB, flush8-10 = PA, ratio 47.8; flush7-9 = PA, flush9-10 = PA, 22.9; ratios
scale ∝ box), optionally combined with sq2's partial wall states; single hinges (E7c2-9e3 or
E9c1-10e2 or E9c3-6e0 or E10c0-8e1 dropped, 2–5) and sq2's corner-rotation mode (W2c0[y=0]
dropped while W2c1[y=0], W2c1[x=s] stay: 3–5) come next. These are precisely A40's saturation
faces ("a flush pair in its switched selection with the couple arm lost", growth rate 0.052 =
1/κ_eff) and A46/A48's bridge/press modes: a hinged flush contact transmits no torque, the
strip becomes a floppy linkage, and its first-order side response e_s·y is ~2 % per unit
motion — positive at ẑ (so the grain drains, Lemma DF at ẑ), but a box-wide certificate must
exclude that the response vanishes somewhere in B, and that costs the full κ_eff.

**4.4 All-pass radius.** At (10⁻³, 10⁻³) the hardest grain has ratio 10.7, so the box on which
EVERY grain of co-dimension ≤ 4 is discharged by [K]/[D1] as a whole is ≈ 10⁻⁴ (t-uniform) —
below A22's 5·10⁻⁴ (A22's inequality certificate uses the hinge's second corner row as an
inequality, which (DF) discards). A76's box discharge is therefore dominated by A22, and a
fortiori by A36 (3.7·10⁻³) and A40 (6.55·10⁻³, θ-world), which handle the hinge faces with
relative-tilt floors and tie cuts.

## 5 The wall and the size law (what the bottom-up front can and cannot do)

**Statement [T+M].** Every grain discharge available at drain-v3 rigor — Krawczyk (K),
drain-flex (DF), Gordan/FJ, and the mixed inequality certificates of A22/A36/A40 — is a
statement that some matrix built from the row Jacobian is nonsingular (or a cone is empty) over
the WHOLE box, and its admissible box radius is ρ ≈ 1/(‖Y‖·L) where L is the Lipschitz constant
of the Jacobian (all 33 coordinates contribute O(r) to it) and ‖Y‖ the preconditioner norm,
which for the hinge grains is 1/(smallest necessary multiplier) ≈ 1/0.01–1/0.05. No pinning
changes this (pins fix 12 coordinates but the hinge modes live in the strip). Hence the
bottom-up front hits the κ_eff wall at the same radius as the top-down basin theorems.

**Beyond the wall.** A hard grain of co-dimension d is a d-dimensional variety through ẑ.
Its box certificate fails on B but holds on boxes of radius ρ_d ≈ r/ratio around each point
of the variety, so the variety ∩ B can be covered by ≈ (ratio)^d such boxes (rigorous
continuation: at each step a Krawczyk enclosure of the variety point on an augmented square
system + the [D1] check on the step box, for d = 1; an interval implicit-function cover for
d ≥ 2). Cost at (10⁻², 2·10⁻³) for k4_08 [M, from the census]: d=1: 405 × ~48 steps; d=2:
1 886 × ~2 300; d=3: 4 755 × ~10³; d=4: 6 656 × ~4⁴ — about 10⁷ Krawczyk-type steps
(≈ 0.2 s each exact), i.e. ≈ 20–25 CPU-days, plus the (unbuilt) d ≥ 2 continuation machinery,
for a certified (r_c, r_t) = (10⁻², 2·10⁻³) — 1.5× A40's centre radius and 0.6× its tilt
radius. The count of hard grains grows ≈ 20× between (5·10⁻³, 10⁻³) and (10⁻², 2·10⁻³) (658 →
13 702) and the pair-LP wants r_c ≳ 1.6·10⁻² (A66's meeter margins), where the census would
explode further and the row universe grows (|PA| = 86 with the upright switches). **This is
the honest size law: exponential in the hinge co-dimension, with the base set by κ_eff.**

**What does help, and is cheap.** (a) The per-coordinate reading of the basin theorems (§7):
the P-B row has been consuming a uniform 3/2000 where A36 already certifies centres to
3.7·10⁻³ and A40 to 6.55·10⁻³. (b) The trivial radii of the image-free classes (§6). (c) The
K-grain radius (10⁻², 2·10⁻³) is a valid ROW for the LP in the following weaker form: a stuck
exact-k4_08 packing in the (10⁻², 2·10⁻³) box cannot have Trump's full contact structure —
too weak to price (the LP's ghosts have fewer contacts).

## 6 Per-class table (Trump-frame pin sets, images, trivial radii) [M exact]

Compatible images g (g·trump5 ⊇ pins(S), at s0) and the Trump-frame pin sets g⁻¹·pins(S)
(`results/images.json`): k0_00: 8 images, ∅; k1_00: 6, {0},{2},{5}; k2_00: 2, {0,1},{0,3};
k2_01: 4, {0,2},{2,5}; k2_02: 4, {0,5}; k3_01: 1, {0,1,2}; k3_02: 2, {0,1,3}; k3_03: 1,
{0,2,3}; k3_04: 2, {0,1,5},{0,3,5}; k3_05: 2, {0,2,5}; k4_03: 1, {0,1,2,3}; k4_06: 1,
{0,1,2,5}; k4_08: 2 images, both reduce to {0,1,3,5} (the diagonal image is k4_08's own
symmetry — P-B's two zone families are ONE grain problem); k4_11: 1, {0,2,3,5}; **k4_05: no
image, d_min = 0.4365; k4_13 = corners4: no image, d_min = 0.8445** — within d_min (sup-norm
over centres and tilts, in Trump's frame after pull-back) of any Trump image no packing has
all of the class's pins, so the exact class is EMPTY there (a required pin sits at a slot no
Trump square is within d_min of: for corners4 the clear corner, for k4_05 the TL slot). This
is the largest "R" in the table and it prices nothing for the LP (no compatible image ⇒ no
basin row), but it is the exact form of A65's "no feasible corners4 family" near Trump.
Krawczyk ratios of the pinned bases at (10⁻², 2·10⁻³): every Trump-frame pin set of the table
contracts (0.75–0.82, `logs/explore1_uniform.log`, `logs/aniso_scan.log`); the hard-grain
census of the other pin sets at the target box (co-dimension ≤ 2, `logs/census_p*_d2.log`) shows
the same hinge families with ratios 48–53 (k4_03: 2 301 hard of 6 516; k4_11: 14 404 of 40 288;
k4_06: 16 301 of 40 288; k3_02: 13 659 of 37 434); fewer pins add the corner-rotation modes of
the unpinned corner squares and the flush-upright states.

## 7 The radius supplied to P-B(R) and the s-shell bookkeeping

For the consumer (`pair_kill.md` §6.8, Lemma P-B(R)) the zone radii may be read PER
COORDINATE from a basin theorem σ ≥ ŝ (equality iff ẑ) on a θ-world ∞-box of radius h around
(ẑ, ŝ): centre zones r_c ≤ h − √2·ρ_B − slop, tilt zones r_t ≤ h/2 (X.1: |Δθ| ≤ 2|Δt|), side
shell ρ_B ≤ h. A36 (exact-checked by A70, h = 37/10000): (r_c, r_t) = (3.7·10⁻³ − √2ρ_B,
1.85·10⁻³). A40 (h = 5794/884563 = 6.55·10⁻³; EXACT-rechecked in this attempt by `code/a40_check_exact.py`:
2930 certificates, 168 774 checks, 0 failures, 5 corruption gates FAIL as required, 70.5 s at
PREC 330, `results/a40_exact_report.json`): (6.55·10⁻³ − √2ρ_B, 3.27·10⁻³). The
uniform rBasin = 3/2000 currently consumed is the Lean axiom's value, which also pays the
(1+√2) s-slab gate the P-B application does not need (its side is separately within ρ_B).
A76's grain results add nothing to these numbers (§5); the per-class trivial radii (§6) and
the exact-stratum scoping are as in Lemma P-B.

## 8 Canary

Trump's packing ẑ is the unique solution of the rigid grain of every class lattice that
contains his image; the certificates never exclude it — they IDENTIFY it (Lemma K), and the
exact-stratum hypothesis (5 simple squares ⇒ not an exact k ≤ 4 class) is what removes it, as
in Lemma P-B. In the k4_08 lattice Trump's grain is the full state (all FLUSH/ON/complete
walls including sq2's slot pattern) — it is the ONE grain the exact-stratum hypothesis
excludes, and it appears nowhere else. Lemma DF never fires at ẑ itself (the full grain is
rigid), the drain-flex curves of the sub-grains start at packings ≠ ẑ, and Lemma D2″ is
satisfied by Trump (his strip is the wall-to-wall chain). The t-native enclosure
(`grain_trump_tnative_*.json`) re-identifies ẑ with the A22 point. SAFE.

## 9 Status and obligations

* [T] Lemma G-R + exact certificate; Lemmas K, DF, D2″; exhaustiveness of the K/DF dichotomy on
  Trump's rows (§3.4). [M exact] Krawczyk radii (uniform and anisotropic, pinned/unpinned);
  D1 radii of the codim-1 grains (9 of 22 pass at the target box, in the certificate);
  t-native ẑ enclosure. [M float] census (143 370 grains × 4 boxes), radius law vs d.
* [C] the continuation programme of §5 (d ≥ 2 rigorous patch covers; ~10⁷ steps) — priced,
  not started; the new-row rigid grains' CP-isolation branch (§3.1) — machinery generic,
  unused. Both are only worth running if the LP measurement of `pair_kill.md` §6.8 shows the
  basin-row margin to be strongly increasing in r_c beyond 6.55·10⁻³.
* Checker `certs/verify_grain.py`: NEW trusted code (stdlib), 5 corruption gates FAIL as
  required; not in the TCB until a second implementation or a Lean port; its kernel (rational
  trig with monotone enclosures) is the natural next rung for the A22 Lean replay (E.COORD).
