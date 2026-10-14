# Slot crowds for the pinned classes: SLOT-CROWD, SLOT-SLIDE, the slot-crowd certificate, and Theorem N-S — A94, 2026-09-04

Target (A94 BRIEF, PI observation 2026-09-03): generalise A92's K0-BLOCKED machinery from the four
corner slots of k0_00 to the completable slots of ANY Young class S with pins, so that k5_11 and
k5_16 (A57's shadow classes) — and then the protected tier — die on [3.82, ŝ − δ_∞] by ONE
certificate chain instead of A57's four-side slack-core grid, leaving only the shell
(ŝ − δ_∞, ŝ] to the tree. Labels: [T] proved, [S] routine given cited items, [M] measured
(`attempts/A94-slot-crowds/`), [C] open. Conventions: `k0_blocked_side.md` (A92: μ_c, d_c, Lemma
B-YES, Lemma CW, Lemma SLIDE, Theorem N), `nocrit_k0_blocked.md` (A90: Fact A, Lemma K, Lemma
CLUSTER, consistent selections), `k0_route.md` (K0-FREE, teleport), `closed_disjoint_bridge.md`
(Lemma B, B.0(a)–(c), B′), `stuck_rows.md` §1 (unclipped completable boxes, census s-stability),
A58 `notes/theory.md` (CC-1(iii) clip census, CC-2/CC-3), the frozen `verify_case.py` (header
claim). s0 = 969271/250000 = ŝ + 4.1·10⁻⁷, ŝ = 3.877083590022814, window W = [3.82, ŝ].

## 0. Verdict

> **[T] Lemma SLOT-CROWD (§2).** In every packing at side m ∈ [3.82, s0) that contains the pins of
> a Young class S, every USABLE unclipped completable slot p of S (one whose extension class
> S ∪ {p} is certified dead on a window containing m) is met, open-interior, by ≥ 2 NON-pin squares.
> ∀-packings, no selection: the single-meeter (or empty) case teleports onto p and lands in
> S ∪ {p} (the CC-3 mechanism with A56/A61's window certificates in place of an s0 certificate —
> exactly Lemma K0-FREE with k1_00's tree replaced by a k6 certificate). For k5_11 the usable slots
> are BL(1,1), BR(0,1), TL(1,0) (extensions k6_18, k6_20, k6_20: FULL window) and TR(0,0)
> (k6_23: window [3.82, 3877/1000)); for k5_16 they are BR(0,1), TR(0,1), TR(1,0) (k6_29, k6_30,
> k6_28: FULL) and BL(1,0) (k6_23); k5_16's BR(1,0), TL(1,0) extend to k6_27 (OPEN, A61 in
> flight) and are unusable today. Trump canary on the EXACT Trump (60-digit A03 data, Fractions):
> all six unclipped completable slots of trump5 are doubly met by free squares, second depths
> 0.016049 / 0.280083 / 0.252050 / 0.264033 / 0.305293 / 0.155475 — A58's float census reproduced
> exactly, and the mechanism is consistent with Trump at ŝ.
>
> **[T] Lemma SLOT-SLIDE (§3).** For such a packing at side m and a usable slot p with certified
> extension window [3.82, ŝ′_p): the second-largest depth of p's non-pin intruders satisfies
> d₂(p) ≥ ŝ′_p − m. Retreat direction = the slot-frame diagonal away from the slot's two BACKED
> sides (the predecessor pins / the corner walls); the retreat cluster is the joint forward closure
> of ALL shallow intruders among the NON-pin squares; the container grows at the two far walls;
> **the pins are not fixed and are never obstacles**: every pin BLOCK (a corner's Young diagram)
> translates rigidly with its two anchoring walls, which keeps it AT ITS SLOTS in the grown
> container, and the relative motion of every other object w.r.t. a block is always "away from the
> block's anchoring walls", which is feasible for a Young down-set (Lemma SWEEP, §3.1). The
> (C)-contact case the brief anticipated ("a pin blocks the retreat") does not arise. Bonus: the
> proof is the JOINT translation of all shallow intruders, which costs d₂ in side — this is also
> the correct proof of A92's "d₂(c) ≥ ŝ − m" (A92 §3.1's sequential proof gives only the SUM bound
> Σ_{i≥1} d_i ≥ ŝ − m, which does not imply the d₂ bound when a corner has ≥ 3 intruders; §3.4).
>
> **[T] The certificate (§4).** CS(S; s, m_lo; δ, e): one measure at fixed side s with the k pin
> cores SLACKENED by ρ ≥ (λ − 1)A_S (λ = s/m_lo, A_S = max |α| over the pins = 3/2 here; Lemma B′)
> and the slot families F_p(a_w) in the SLOT FRAMES with pad a_w = λ(1−δ) + (λ−1)(1/√2 + max(i,j))
> (Lemma B-YES-S: the slot's backed vertex moves by (λ−1)(i,j) under dilation — an extra
> (λ−1)max(i,j) over A92's corner pad); verified by 1 + r_max runs of the frozen verifier (run A:
> cores, n = 11 + 2m_u e; run B_r: weights/(1+re), the exact complement E_r of "meets ≥ r widened
> slot boxes" exempt), because a square can meet several slot boxes at once (an axis-aligned square
> centred near (2.44, 2.44) meets all four of k5_11's usable boxes at s0) — the count is by
> INCIDENCES, budget N + 2m_u e (Lemma CW-S). **[M] §4.4: LP passes at every window, NO certified
> PASS.** Window (s0, G2] (the one that decides which A57 sides go): both classes pass the LP at
> δ ∈ {0.3, 0.2} only (k5_11 η = −0.80/−0.25, k5_16 −0.95/−0.58) and fail at δ ≤ 0.1 (k5_11 at δ =
> 0.1, e = 1/8: τ = 7.007 vs budget 7 — 0.007 short, minmass 0.91); the δ = 0.2 certifications
> FAIL on holes in every run (incl. eps_geo repairs). Since Theorem N-S needs δ ≤ 0.0446 for the
> chain to remove even G4 (and ≤ 0.0154 to remove G2–G4), **δ_∞ ≥ 0.2 at the s0 side: the chain
> removes NO A57 side.** Window (G4, 3.82]: k5_11 passes the LP at δ = 0.1, 0.04, 0.02 (e = 1/8,
> η −0.25/−0.22/−0.21), k5_16 at 0.1 (η −0.16); the converged δ = 0.1 node (minmass 1.0000, 39
> atoms) was certified at close-out: **run A PASS, run B₁ PASS, runs B₂–B₄ FAIL with 30–32 exact
> HOLES** (the incidence rows r ≥ 2 are what the LP does not price — a geometric refusal, not a
> degeneracy; eps_geo cannot cure real holes). A certified δ = 0.1 on that slab would in any case
> prove only "no k5_11 packing at m ∈ [3.82, G4) with all four usable slots doubly met at depth ≥
> 0.1", while SLOT-SLIDE guarantees only d₂ ≥ ŝ′ − m ≥ 0.0438 there: the slab-killing certificate
> is δ ≤ 0.0438, i.e. the δ = 0.04 LP pass (η −0.22, minmass 0.88, unconverged) — worth one attempt
> only after a converged re-solve, and predicted to fail the same way (the δ = 0.02 node, minmass
> 0.90, failed B₂–B₄ identically). The slab is anyway covered parametrically by A96, so this is a
> mechanism/paper result: the slot-crowd LP is LIVE at the low side and DEAD at the s0 side.
>
> **[T] Theorem N-S (§5).** CS(S; s, m_lo; δ, e) PASS + SLOT-CROWD + SLOT-SLIDE ⇒ no packing
> containing S's pins at any side m ∈ [m_lo, s) ∩ [3.82, ŝ′_S − δ], ŝ′_S = min over the used slots
> of the extension window's upper end (3877/1000 for both classes if the k6_23 slot is used, s0
> otherwise). A chain of such certificates kills [3.82, ŝ′_S − δ_∞] and A57's G1 tree (slack-core
> side s0, slab (3.861637, s0]) kills the shell; **G2/G3/G4 become unnecessary iff δ_∞ ≤ 0.01536
> (3877/1000 − 3.861637); G3/G4 iff δ_∞ ≤ 0.02998; G4 iff δ_∞ ≤ 0.04455.** The chain's pad ratio
> per step is 0.698 (vs A92's 0.440), so the number of certificates from δ = 0.05 down to 0.012 is
> 4, each a root LP + ≤ 5 verifier runs — hours, not desktop-days — IF the LP passes.
>
> **[T] The Trump-image ceiling (§6): the protected tier is NOT crowd-killable except k4_05,
> corners4 and (partly) k4_11.** If a Trump image g·ẑ contains the pins of S, it is a packing of
> class S at side ŝ whose usable slots are doubly met at depths d₂(g,p); a certificate at depth
> δ ≤ δ_T(S) := max_g min_p d₂(g,p) is FALSE (Trump refutes it) and one at δ > δ_T reaches at most
> ŝ − δ_T. Exact values: k4_03 3.72, k4_06 3.72, k4_08 3.61 (below the window floor 3.82 even with
> k5_11/k5_16 dead — the chain is VOID for them), k4_11 3.861 (via BL(0,2), where Trump's crowd is
> the 0.016-deep sq7), trump5 3.72; k4_05 and corners4 have no compatible image (no ceiling; corners4
> gets its 8 usable slots only once k5_16 is dead on the whole window). The k ≤ 3 classes have NO
> usable slot today (every extension is a protected k4 class or an s0-only A55 kill).

## 1. Setting

### 1.1 Classes, pins, packings of a class

Young classes as in A53 (`Census.lean`): S is a D4-orbit of pin sets; a pin set P_S is k slots
(α_j + β_j s, β ∈ {0,1}², |α| ≤ 5/2). A **packing containing the pins of S at side m** ("of class
S", the MONOTONE hypothesis `ContainsPins P_S m`, K1) is a family of 11 closed unit squares in
[0, m]² with pairwise disjoint interiors, k of which are axis-aligned with centres exactly at
slot_j(m). The other N = 11 − k are the **non-pin** squares (they may be axis-aligned at other
slots — irrelevant). k5_11: pins (1/2,1/2), (1/2,3/2), (3/2,1/2), (1/2, m−1/2), (m−1/2, 1/2), N = 6.
k5_16: (1/2,1/2), (1/2,3/2), (1/2, m−1/2), (m−1/2, 1/2), (m−1/2, m−1/2), N = 6.

### 1.2 Completable slots, the clip census, extension classes and their windows

Cell (i, j) of corner c: offsets i along the wall-normal x-axis and j along y from c; its slot box
B_p(m) = the closed unit square centred at the cell's slot. **Completable** = Young-ready (its
predecessors (i−1, j), (i, j−1) are pins, offsets ≤ 2). **Clipped** = the open box interior meets
the open interior of some pin square (the census is s-stable over [3.82, s0]: `stuck_rows.md` §1;
re-verified exactly at 191/50 and s0 by `attempts/A94-slot-crowds/code/slots94.py`). The
**extension class** of p is the Young class of P_S ∪ {slot p} (k+1 pins; D4-canonicalised against
the census names). [M, exact: `results/slots94.json`]

| class | cell | slot at s0 | clipped by | extension | window status of the extension (A56/A61 scoreboard) |
|---|---|---|---|---|---|
| k5_11 | BL(0,2) | (1/2, 5/2) | TL pin (1/2, s−1/2) | — | — |
| k5_11 | **BL(1,1)** | (3/2, 3/2) | — | k6_18 | FULL [191/50, s0] |
| k5_11 | BL(2,0) | (5/2, 1/2) | BR pin (s−1/2, 1/2) | — | — |
| k5_11 | **BR(0,1)** | (s−1/2, 3/2) | — | k6_20 | FULL (A61 re-solve) |
| k5_11 | BR(1,0) | (s−3/2, 1/2) | BL pin (3/2, 1/2) | — | — |
| k5_11 | **TR(0,0)** | (s−1/2, s−1/2) | — | k6_23 | PARTIAL: [191/50, 3877/1000] parametric + {s0} |
| k5_11 | TL(0,1) | (1/2, s−3/2) | BL pin (1/2, 3/2) | — | — |
| k5_11 | **TL(1,0)** | (3/2, s−1/2) | — | k6_20 | FULL |
| k5_16 | BL(0,2) | (1/2, 5/2) | TL pin | — | — |
| k5_16 | **BL(1,0)** | (3/2, 1/2) | — | k6_23 | PARTIAL to 3877/1000 |
| k5_16 | **BR(0,1)** | (s−1/2, 3/2) | — | k6_29 | FULL (A61) |
| k5_16 | BR(1,0) | (s−3/2, 1/2) | — | k6_27 | OPEN (A61 in flight) — unusable |
| k5_16 | **TR(0,1)** | (s−1/2, s−3/2) | — | k6_30 | FULL |
| k5_16 | **TR(1,0)** | (s−3/2, s−1/2) | — | k6_28 | FULL |
| k5_16 | TL(0,1) | (1/2, s−3/2) | BL pin (1/2, 3/2) | — | — |
| k5_16 | TL(1,0) | (3/2, s−1/2) | — | k6_27 | OPEN — unusable |

So both classes have 8 completable slots; k5_11 has 4 unclipped, k5_16 has 6, and U_S := the
usable ones (bold) number 4 each. (The brief's "8 each?" counted the clipped cells; clipped slots
yield nothing — the teleport would overlap the clipping pin, `stuck_rows.md` §2 Rem. (ii).)

**Extension windows.** For an extension class T with a FULL parametric row the kill is
`stratum_kill` at every side m ∈ [3.82, s0) for interior-disjoint packings (Lemma B applied to the
parametric certificate at a side s″ ∈ (m, s0] with the ε-fat cores, `closed_disjoint_bridge.md`
B.3); write W_T = [3.82, s0). For k6_23 the parametric PASS covers [191/50, 3877/1000], so
W_{k6_23} = [3.82, 3877/1000) (the fixed-s0 certificate binds only a 4·10⁻¹⁰ shell below s0 and
is not used). Put ŝ′_p := sup W_{S∪{p}} and, for a set U of slots, ŝ′_U := min_{p∈U} ŝ′_p: for
either class, ŝ′ = 3877/1000 if the k6_23 slot is in U and s0 otherwise.

### 1.3 Slot frames, depth, and the containment lemma

For a slot p = cell (i, j) of corner c define the **slot frame** Φ_p^{(m)} : (x, y) ↦ (x′, y′) =
(u − i, v − j) where (u, v) is c's corner frame (u = x or m − x, v = y or m − y). In it the box
B_p is [0,1]², the two BACKED sides are x′ = 0 (a predecessor pin if i ≥ 1, c's wall if i = 0) and
y′ = 0 (likewise), and the two FREE sides are x′ = 1, y′ = 1. Depth of a square Q at p:

  μ_p(Q) := min_{q∈Q} max(q′_x, q′_y),   d_p(Q) := max(0, 1 − μ_p(Q))

(A90's corner depth with the frame origin at the backed vertex; a corner root box is the case
i = j = 0). Let R_p := {x′ < 0, y′ < 1} ∪ {y′ < 0, x′ < 1} (open).

**Lemma CONT [T] (containment).** Let P be a packing containing the pins of S at side m, p an
unclipped completable slot of S, Q a non-pin square of P. Then Q ∩ R_p = ∅. Consequently
d_p(Q) > 0 ⟺ int Q ∩ int B_p ≠ ∅, and every argmin point of μ_p(Q) < 1 lies in [0, 1)².

*Proof.* R_p ∩ (0, m)² is covered by the open interiors of the pins backing p together with a
finite union of segments (nowhere dense): in the frame, {x′ < 0, y′ < 1} ∩ container is (for
i ≥ 1) the open predecessor pin (i−1, j) at x′ ∈ (−1, 0), y′ ∈ (0, 1), the pin (i−1, j−1) below
it if j ≥ 1, further pins/outside-container beyond, and the shared edges; for i = 0 it is outside
the container; {y′ < 0, x′ < 1} symmetrically. (Young: the cells (i′, j′) with i′ ≤ i−1, j′ ≤ j
and those with j′ ≤ j−1, i′ ≤ i are pins or lie outside the container.) int Q is open, disjoint
from every open pin (interior-disjointness) and inside (0, m)²; if int Q met the open set R_p the
intersection would be a nonempty open set inside the nowhere-dense union of segments —
impossible; so int Q ∩ R_p = ∅ and Q = cl(int Q) ⊆ cl(R_p^c) = R_p^c. For the equivalence: if μ_p(Q)
< 1 the argmin point q has max(q′) < 1 and q ∉ R_p, so q′_x, q′_y ≥ 0; interior points of Q near q
have max < 1 and (being in int Q, an open set avoiding R_p) coordinates > 0, hence lie in (0,1)²;
conversely an interior point in (0,1)² has max < 1. ∎

Remark. A92's k0 setting is the case i = j = 0 with walls for pins. The lemma is where the
clip census enters: at a CLIPPED slot the backing is a pin that itself meets int B_p and the
argument (and the teleport of §2) fails — which is why clipped slots are excluded.

## 2. [T] Lemma SLOT-CROWD (∀-packings)

**Lemma SLOT-CROWD.** Let S be a Young class, p an unclipped completable slot of S, T = S ∪ {p}
its extension class, and suppose T is dead on W_T (no packing containing the pins of T at any side
in W_T). Then every packing P containing the pins of S at a side m ∈ W_T has ≥ 2 NON-pin squares
meeting int B_p(m).

*Proof.* Let n_p be the number of non-pin squares meeting int B_p(m). Pins do not meet it
(unclipped, s-stable). If n_p ≤ 1: let Q be the meeter if n_p = 1, else any non-pin square (N ≥ 1).
P′ := P with Q replaced by the slot square B_p(m) itself. B_p(m) ⊆ [0, m]²; int B_p(m) is disjoint
from the interior of every other square of P; so P′ is a packing at side m (`teleport_packing`),
and it contains axis-aligned squares at all slots of P_S ∪ {p} = P_T: `ContainsPins P_T m P′`, at a
side m ∈ W_T — contradicting T's kill. ∎

Applied to k5_11/k5_16 with the windows of §1.2: every packing of class k5_11 at side m ∈ [3.82,
3877/1000) has ≥ 2 non-pin meeters at each of BL(1,1), BR(0,1), TL(1,0), TR(0,0) (and at the first
three for m ∈ [3.82, s0)); k5_16 likewise at BL(1,0) (m < 3877/1000), BR(0,1), TR(0,1), TR(1,0).
Remarks. (i) This is A58's CC-3 with the s0 certificate replaced by a WINDOW certificate, hence
∀-packings at every side of W_T — no K*-maximal minimiser, no exact-stratum hypothesis (the
teleported packing is only required to CONTAIN the pins of T, which is what the parametric kills
exclude: K1, `instratum_bridge.md`). (ii) The quantifier is exactly Lemma K0-FREE's, with k1_00's
tree (K0-O1, open) replaced by k6 certificates that EXIST: for the pinned classes the slot-crowd
lemma is unconditional, which k0_00's corner-crowd lemma is not. (iii) Canary: Trump (side ŝ ∈
W_T for T ∈ {k6_19, k6_22, k6_24}) has exactly two free meeters at trump5's slots BL(1,1), TR(0,1),
TR(1,0) — consistent (§7); the lemma says nothing at trump5's slots BR(0,1) (k6_21 OPEN) and
BL(0,2) (k6_07 open above 3.827), where Trump also has two, one of them at depth 0.016.

## 3. [T] Lemma SLOT-SLIDE

### 3.1 Lemma SWEEP (a Young block never obstructs motion away from its walls)

Let D be a Young diagram at corner c realised as the union of the closed unit cells C_{ij} at c's
slots (a down-set in c's cell order), inside [0, m]². Let X ⊆ [0, m]² be closed with int X ∩ int D
= ∅, and let v ∈ ℝ² point AWAY from c's two walls (in c's corner frame, v_x, v_y ≥ 0). Then
int(X + v) ∩ int D = ∅.

*Proof (BL frame).* Suppose q + v ∈ int C_{ij} with q ∈ int X, (i,j) ∈ D. Then q ∈ R :=
(i − v_x, i+1 − v_x) × (j − v_y, j+1 − v_y) ∩ (0, ∞)². Every point of R with non-integer
coordinates lies in the open cell (⌊x⌋, ⌊y⌋) with ⌊x⌋ ≤ i, ⌊y⌋ ≤ j and ⌊x⌋, ⌊y⌋ ≥ 0, i.e. in an
open cell of D (down-set); so int X ∩ R ⊆ (grid lines) ∪ (int X ∩ int D) = grid lines, but int X ∩
R is open and nonempty (it contains q) — an open subset of the grid lines, contradiction. ∎

The same statement with D replaced by a block DISPLACED rigidly, and with X a moving object, is
what "relative motion away from the block's walls" means below.

### 3.2 The motion: cluster, walls and pin blocks

Fix a packing P containing the pins of S at side m, a usable slot p with frame Φ_p, u := the
frame diagonal (1,1)/√2 (pointing from the backed vertex into the box and beyond), and the two
FAR walls of p := the container walls in the frame directions +x′, +y′ (they are the walls
opposite to corner c). Let τ := t/√2 be the displacement of each far wall.

* The **cluster** C = C_u(X₀) of a set X₀ of NON-pin squares: the forward closure of X₀ under
  "N presses M against u" among NON-pin squares only (A90 Lemma CLUSTER's relation for a consistent
  selection S on the non-pin pairs; near-wall rows of members: c's walls; far-wall rows: the far
  walls). Members translate by t·u.
* **Pin blocks.** The pins of S at corner c′ form c′'s Young diagram D_{c′}; the block D_{c′}
  translates by the displacement of ITS anchoring walls: (τ in the far-x direction if c′ is
  anchored at the far x-wall, else 0; likewise in y). So D_c (the slot's own corner) is fixed, the
  diagonally opposite corner's block moves by t·u, and the two other blocks move along one axis.
  In the grown container [0, m + τ]² (normalised so that c's walls stay put) every pin is again
  EXACTLY at its slot: slot_j(m + τ) = slot_j(m) + (β_j,x τ, β_j,y τ) in c's frame.
* **Outsiders** (non-pin, not in C) and c's walls stay fixed; the far walls recede by τ.

**Lemma MOVE [T].** For all sufficiently small t > 0 (and, enlarging C at the first activation of an
inactive member–outsider row as in A92 §3.1, for every t > 0) the configuration z_t is a packing
containing the pins of S at side m + τ.

*Proof, pair by pair.* (member, member): rigid. (member, non-pin outsider): Lemma CLUSTER — affine
rows with nonnegative slope when active (closedness), positive margin when inactive. (member,
pin block D_{c′}): the relative displacement of the member w.r.t. the block is, per axis, 0 if the
block is anchored at the moving wall of that axis (both move by τ) and +τ outward (away from c′'s
wall) otherwise — in every case a vector pointing away from c′'s walls (or zero): Lemma SWEEP with
X = the member (closed, in the old container, interior-disjoint from the block). (outsider, pin
block): the relative displacement of the outsider w.r.t. the block is −(the block's displacement),
which is inward from the block's moving walls = away from them: Lemma SWEEP. (block, block): the
relative displacement of D_{c″} w.r.t. D_{c′} is, per axis, 0 or ±τ away from c′'s wall (c″'s
displacement is outward at c″'s anchoring walls; if c′ is anchored at the same moving wall the two
cancel, otherwise c″ moves toward the moving wall, which is c′'s far wall): Lemma SWEEP. Walls:
members move away from c's walls and with the far walls; blocks move exactly with their walls;
outsiders are fixed against receding walls. Pins stay axis-aligned at slots(m + τ). ∎

So there is no (C) contact: a pin can touch a member, but a touching pin never obstructs, because
its block moves with the very wall the cluster is retreating toward, and every other relative
motion is away from a down-set's anchoring walls.

**Depth bookkeeping [T].** μ_p(M + tu) = μ_p(M) + τ exactly for members (max(x′+τ, y′+τ) =
max(x′,y′) + τ); outsiders unchanged; B_p(m + τ) = B_p(m) in c's frame (the slot is anchored to
c's walls) and no pin meets its interior at any side of the window (unclipped, s-stable). Hence
no square's depth at p increases and no new intruder appears.

### 3.3 Statement and proof

**Lemma SLOT-SLIDE.** Let P contain the pins of S at side m ∈ W_T, T = S ∪ {p} dead on W_T =
[3.82, ŝ′_p), p unclipped completable, and let Q₀, Q₁, …, Q_k (k ≥ 1) be the non-pin intruders of
p (d_p > 0), Q₀ the deepest, d₂ := d_p(Q₁) ≥ d_p(Q_i) (i ≥ 2). Then m + d₂ ≥ ŝ′_p, i.e.
**d₂(p) ≥ ŝ′_p − m.** (With SLOT-CROWD: every packing of class S at side m has, at every usable
slot, TWO non-pin intruders of depth ≥ ŝ′_p − m.)

*Proof.* Let C := C_u({Q₁, …, Q_k}) and translate as in Lemma MOVE up to t = √2·d₂ (τ = d₂),
enlarging C at most N − 1 times (all members are non-pin squares). At the end every Q_i (i ≥ 1), being a member, has μ_p ≥
(1 − d_p(Q_i)) + d₂ ≥ 1: not an intruder (Lemma CONT). Q₀ is a member or not; either way at most
one non-pin square meets int B_p(m + d₂), and the configuration is a packing containing the pins
of S at side m′ := m + d₂. If m′ < ŝ′_p then m′ ∈ W_T and Lemma SLOT-CROWD's teleport gives a
packing containing the pins of T at m′ ∈ W_T — contradiction. ∎

### 3.4 The joint translation, and a correction to A92 §3.1

A92's Lemma SLIDE slides the shallow intruders OUT ONE AT A TIME and charges the SUM T = Σ_{i≥1}
d_c(Q_i); its "Equivalently: d₂(c) ≥ ŝ − m" does not follow from that proof when a corner has ≥ 3
intruders (three intruders of depth (ŝ − m)/2 have T > ŝ − m and d₂ < ŝ − m). The joint
translation above — one cluster generated by ALL the shallow intruders, moved by √2·d₂ — costs
exactly d₂ in side and proves the d₂ form, for corners (A92, pins absent) and for slots alike.
Theorem N (A92 §3.3) uses the d₂ form; it is therefore this proof that A93 T2 should formalise
(`stratum_kill`'s SLIDE piece), and A92 §3.1 should be read with "C := C_u({Q₁,…,Q_k}), t = √2 d₂"
in place of Steps 1–2. Nothing else in A92 changes.

## 4. The slot-crowd certificate

### 4.1 [T] Lemma B-YES-S (the crowd hypothesis transfers to side s, with the slot pad)

Let P contain the pins of S at side m ∈ [m_lo, s), λ := s/m ∈ (1, s/m_lo], F := Δ_λP (centres
scaled by λ about the origin, tilts unchanged; B.0: a strictly disjoint family in [0, s]²). Let p =
cell (i, j) be a slot of S. If a non-pin Q ∈ P has μ_p^{(m)}(Q) ≤ a, then Q′ := Δ_λQ satisfies

  μ_p^{(s)}(Q′) ≤ a_w(p; a, λ) := λa + (λ − 1)(1/√2 + max(i, j)).

*Proof.* Frame at side m: x′ = σ_x(x − v_x(m)) with σ_x = ±1 and v(m) = α_v + β_v m the backed
vertex; note v_x(s) = λ v_x(m) − (λ−1)α_v and σ_x α_v = i (BL-type axis: σ = +1, α_v = i;
BR-type: σ = −1, α_v = −i). Take q ∈ Q with max(x′, y′) = μ_p^{(m)}(Q) ≤ a; q′ := q + (λ−1)c_Q ∈ Q′
(Q′ = Q + (λ−1)c_Q). Its s-frame coordinate is x″ = σ_x(q_x + (λ−1)c_{Q,x} − v_x(s)) = x′ +
(λ−1)c′_x + (λ−1)i with c′_x = σ_x(c_{Q,x} − v_x(m)) ≤ x′ + h(θ) ≤ x′ + 1/√2 (a point of a unit
square is within h(θ) ≤ √2/2 of its centre in each coordinate). So x″ ≤ λx′ + (λ−1)(1/√2 + i) ≤
λa + (λ−1)(1/√2 + i); same in y with j. ∎

For the corner root (i = j = 0) this is A92's Lemma B-YES. Numerics (window (s0, G2 = 965601/
250000), λ − 1 = 3670/965601): a_w(0.05) = 0.96010, a_w(0.02) = 0.99022 (max(i,j) = 1); window
(G4 = 958303/250000, 3.82), λ − 1 = 3303/955000: a_w(0.04) = 0.96923, a_w(0.02) = 0.98930; full
window (s0, 3.82), λ − 1 = 14271/955000: a_w(0.05) = 0.98971 and a_w(0.03) > 1. The pad
(λ−1)(a + 1/√2 + max(i,j)) is at most 0.0405 on the full window; a_w < 1 iff
δ > δ_pad(m_lo) := (1 + 1/√2 + max(i,j))(s − m_lo)/s = 0.6982·(s0 − m_lo) at s = s0 with max(i,j)=1
(A92's constant 0.4403 becomes 0.6982 for the slots at offset 1; the corner slot TR(0,0) keeps
0.4403).

### 4.2 [T] Lemma CW-S (the certificate and its 1 + r_max frozen runs)

Fix S (pins P_S, k, N), a side s, a window floor m_lo (λ_S := s/m_lo), a set U of usable slots
(m_u := |U|), δ ∈ (0,1), e ∈ ℚ_{>0} with 2m_u e ∈ ℤ, and:
 * pin cores K_j := the axis-aligned square centred at slot_j(s) with half-side 1/2 − ρ, ρ >
   (λ_S − 1)·A_S, A_S := max_j |α_j|_∞ (= 3/2 for k5_11, k5_16);
 * slot families F_p(a_w) := {admissible poses Q ⊆ [0,s]² : μ_p^{(s)}(Q) ≤ a_w(p; 1−δ, λ_S)},
   p ∈ U, and for r ≥ 1 the sets F^{(r)} := {Q : #{p ∈ U : Q ∈ F_p(a_w)} ≥ r};
 * a finite atomic measure μ on [0, s]².
Suppose (A) μ(Q) ≥ 1 for every admissible Q meeting no K_j; (B_r) μ(Q) ≥ 1 + re for every
admissible Q meeting no K_j with Q ∈ F^{(r)}, r = 1..r_max (r_max ≥ the largest r with F^{(r)} ≠ ∅);
(C) μ([0,s]²) < N + 2m_u e. Then **no packing containing the pins of S at a side m ∈ [m_lo, s) has,
at every p ∈ U, two non-pin squares of depth d_p ≥ δ.**

*Proof.* Let P be such a packing, F = Δ_λP, λ = s/m ≤ λ_S. The k dilated pins are axis-aligned at
distance (λ−1)|α_j| < ρ from slot_j(s) (B.0(c)), so each contains K_j in its open interior. The N
dilated non-pin squares Q′ are admissible (B.0(b)), pairwise disjoint (B.0(a)), and disjoint from
the dilated pins, hence meet no K_j. For each p ∈ U the two non-pin squares of depth ≥ δ at p
(μ_p^{(m)} ≤ 1 − δ) dilate into F_p(a_w) (Lemma B-YES-S), so Σ_{Q′} r(Q′) ≥ 2m_u where r(Q′) :=
#{p : Q′ ∈ F_p(a_w)} (the two meeters of a slot are distinct squares; a square counted at several
slots is counted once per slot on both sides). Each Q′ with r(Q′) = r ≥ 1 lies in F^{(r)}, so
μ(Q′) ≥ 1 + r e by (B_r); those with r = 0 have μ(Q′) ≥ 1 by (A). Disjointness: Σ_{Q′} μ(Q′) ≤
μ([0,s]²) < N + 2m_u e ≤ N + e Σ r(Q′) ≤ Σ_{Q′} μ(Q′). ∎

**Verification with the frozen `verify_case.py`.** Run A: certificate (s, atoms, weights w, n =
11 + 2m_u e ∈ ℤ, cores = {K_j}, no NO-families); PASS = (A) + (C) (header claim: μ(Q) ≥ 1 for every
non-exempt admissible Q — exempt = meets a core — and total < budget = n − k). Run B_r: same
atoms, weights w/(1 + re) (exact), same cores, NO-families = E_r := an exact rectilinear cover of
poses that meet AT MOST r − 1 of the families F_p(a_w) (each E_r box certified, in Fractions, to be
disjoint from F_p(a_w) for all p ∈ U except ≤ r − 1 of them), n = 1000 (dummy); PASS = (B_r): a
Q ∈ F^{(r)} lies in no E_r box and meets no core, so it is non-exempt and μ(Q)/(1+re) ≥ 1. Each
run's soundness is the verifier's own header claim (V.CASE, Lean-proved); Lemma CW-S is the only
mathematics on top. (Since r ≤ m_u ≤ 4 the certificate is ≤ 5 files on one atom list.) Why the
multiplicity: unlike A92's four corner boxes (pairwise > √2 apart, CC-1(ii)), the usable slot boxes
of k5_11 are 0.877 apart in each axis and an axis-aligned square centred at (2.4385, 2.4385) meets
all four at s0; counting incidences (budget N + 2m_u e) is the sound bookkeeping, counting
distinct crowd squares (budget N + m_u e) would over-charge. The multiplicity histogram is a
diagnostic the chore reports.

### 4.3 The objects (definitions the chore implements; `attempts/A94-slot-crowds/notes/chore_slot_cert.md`)

Families: A92's staircase outer cover G_p ⊇ F_p(a_w), built IN THE SLOT FRAME with the same exact
disjointness test (f = `corner85.f_min_max` is nondecreasing in both centre coordinates and
(√2/2)-Lipschitz in θ for EVERY centre — no quadrant assumption; the centre grid is extended to
frame coordinates [−1, a_w + 3/4]² because a non-exempt pose may graze the backing pins' ρ-shells).
E_r: the absolute 0.02-grid cells (per θ-bin) whose non-disjoint slot set has ≤ r − 1 elements,
merged only between cells with identical non-disjoint sets. LP: the class node (pin boxes of
half-width ρ/√2, sym C1) at side s with rhs(Q) = 1 + e·#{p : Q in the dilated G_p}, budget
N + 2m_u e; A92's `lpbox92` hooks unchanged in kind. Constants: ρ_min = 0.00571 (s0, G2), 0.00519
(G4, 3.82), 0.02242 (s0, 3.82); e ∈ {1/8, 1/4, 1/2, 1} (n = 12, 13, 15, 19; budget 7, 8, 10, 14).

### 4.4 [M] Results (Opus chore; `attempts/A94-slot-crowds/notes/slotcrowd94_report.md`)

Chore 2026-09-04, 397 min wall, 23 LPs, 4 certification chains (A92 engine copied, frozen
verifier sha 521cb01f…, C1 quotient, budget N + 2m_u e with m_u = 4, lp_time 900 s two-stage,
rho 0.00572 / 0.00520). Phase-0 canaries all PASS: the chore's slot frames reproduce the exact
Trump depths of §7 to 0.0 (all 8 slots); no Trump image realises either class's pin hypothesis
at any window; the e = 0 exact-pin regression reproduces the class root τ (k5_11 5.874 vs A54/A57
5.906, k5_16 5.960 vs 5.973 — warm-start tolerance).

| class | window | δ | e | budget | τ | η | minmass | verdict |
|---|---|---|---|---|---|---|---|---|
| k5_11 | (s0, G2] | 0.3 | 1/2 | 10 | 9.198 | −0.80 | 0.95 | LP-PASS, not certified |
| k5_11 | (s0, G2] | 0.2 | 1/2 | 10 | 9.750 | −0.25 | 0.62 | LP-PASS; cert FAIL (A and B₁–B₄ holes; eps_geo 0.002/0.004 FAIL) |
| k5_11 | (s0, G2] | 0.1 | 1/2, 1/4, 1/8 | 10, 8, 7 | 10.596, 8.062, **7.007** | +0.60, +0.06, **+0.007** | 0.68–0.91 | refused |
| k5_11 | (s0, G2] | 0.05 | 1/2, 1/4, 1/8 | 10, 8, 7 | 10.848, 8.432, 7.084 | +0.85, +0.43, +0.08 | | refused |
| k5_11 | (s0, G2] | 0.02 | 1/2, 1/8 | 10, 7 | 11.000, 7.116 | +1.00, +0.12 | | refused |
| k5_11 | (G4, 3.82] | 0.1 | 1/8 | 7 | 6.750 (conv.) | −0.25 | 1.0000 | LP-PASS; **cert FAIL: A PASS, B₁ PASS, B₂/B₃/B₄ 31/32/32 HOLES** (close-out run, 1794 s) |
| k5_11 | (G4, 3.82] | 0.04 | 1/8 | 7 | 6.778 | −0.22 | 0.88 | LP-PASS, not certified (the slab-killing δ) |
| k5_11 | (G4, 3.82] | 0.02 | 1/8 | 7 | 6.787 | −0.21 | 0.90 | LP-PASS; cert FAIL (A PASS, B₁ PASS, B₂–B₄ FAIL) |
| k5_16 | (s0, G2] | 0.3 / 0.2 | 1/2 | 10 | 9.051 / 9.424 | −0.95 / −0.58 | 0.83 / 0.94 | LP-PASS; δ = 0.2 cert FAIL (holes, eps_geo FAIL) |
| k5_16 | (s0, G2] | 0.1 | 1/2, 1/4, 1/8 | 10, 8, 7 | 10.644, 8.313, 7.146 | +0.64, +0.31, +0.15 | | refused |
| k5_16 | (G4, 3.82] | 0.1 | 1/8 | 7 | 6.839 | −0.16 | 0.92 | LP-PASS, not certified |

Readings. (i) At the s0 side the LP-passing set is δ ≥ 0.2 for both classes — an order of
magnitude above the 0.0154 that would retire G2–G4 and 4.5× above the 0.0446 that would retire
G4 alone; δ_∞ ≥ 0.2 there. The k5_11 knife edge at δ = 0.1, e = 1/8 (τ = 7.007 vs 7) says the
crowd bonus at e = 1/8 with 8 incidences buys exactly the class root's deficit (0.126 at
δ = 0.1) and no more: the ghost realises about half of the incidences at shallow depth, as
predicted in §5. (ii) At the G4 side (τ falls with the side, A82) the LP passes down to δ = 0.02,
but no certificate closes: run A and B₁ pass, the multiplicity runs B₂–B₄ fail on 30–32 exact
holes at depth 56 — poses meeting ≥ 2 widened boxes with mass < 1 + re. The LP's row oracle (A92's
two-pass scheme with the dilated G) does not surface those rows, and 2 witness-feedback rounds do
not converge them: the incidence rows are the unpriced part of the certificate. This is a
certification-engine gap (A94-G4), not a refutation of the mechanism, but it is the same
"holes inside the crowd family" refusal A92 met at δ = 0.2. (iii) What run A + B₁ alone certify is
nothing: with distinct crowd squares counted once, 4 doubly-met slots force only ≥ 2 distinct
crowd squares (one axis-aligned square meets all four boxes), so 6 + 2e < 7. The families
(overshoot 3–11 %, r_max = 4 on the grid at δ ≤ 0.05) and the exact E_r covers are sound and
reusable. No certificate of this attempt claims anything.

## 5. [T] Theorem N-S (composition) and the re-price of A57

**Theorem N-S.** Let S ∈ {k5_11, k5_16}, U ⊆ U_S, ŝ′ := ŝ′_U (§1.2). If CS(S; s, m_lo; δ, e) passes
(all 1 + r_max runs), then no packing containing the pins of S exists at any side
m ∈ [m_lo, s) ∩ [3.82, ŝ′ − δ].
*Proof.* Such a packing has, at every p ∈ U, two non-pin intruders (SLOT-CROWD, m ∈ W_T) of depth
≥ ŝ′_p − m ≥ ŝ′ − m ≥ δ (SLOT-SLIDE); Lemma CW-S excludes it. ∎

**The chain and the shell.** A finite list of passing certificates whose kill intervals cover
[3.82, ŝ′ − δ_∞] proves: no packing of class S at any side in [3.82, ŝ′ − δ_∞]. A57's G1 tree
(the s0 slack-core tree, δ_pin = 10⁻², Lemma B′ slab (3.861637, s0]; `A57 notes/lemmas.md` T23)
kills every packing whose pins are within 7.07·10⁻³ of the slots — in particular every packing of
class S — at every m in its slab, ŝ included. Hence:

| δ_∞ (with ŝ′ = 3877/1000) | class S dead on | A57 sides still needed |
|---|---|---|
| ≤ 0.015363 (= 3.877 − 3.861637) | [3.82, ŝ] (chain ∪ G1 slab) | **G1 only** — G2, G3, G4 unnecessary |
| ≤ 0.029984 (= 3.877 − 3.847016) | chain ∪ G2 ∪ G1 | G1, G2 (G3, G4 unnecessary) |
| ≤ 0.044550 (= 3.877 − 3.832450) | chain ∪ G3 ∪ G2 ∪ G1 | G1, G2, G3 (G4 unnecessary) |
| > 0.044550 | — | all four (the chain removes nothing) |

(With ŝ′ = s0, i.e. the k6_23 slot unused, add 8.4·10⁻⁵ to each threshold.) The chain itself: at
side s0 a certificate with window [m_lo, s0) needs δ > 0.6982(s0 − m_lo) (a_w < 1) and kills up to
ŝ′ − δ, i.e. ≈ 30 % of its slab; from δ = 0.05 the sub-windows [ŝ − 0.05, s0), [ŝ − 0.0349, s0),
[ŝ − 0.0244, s0), [ŝ − 0.0170, s0) reach δ = 0.0119 in four steps IF each LP passes — the same
"LP constant δ_∞, geometric convergence" picture as A92, with ratio 0.698 instead of 0.440. The
grid alternative (a certificate at each of A57's sides s with window = the slab below it) is the
same count with easier LPs (τ falls with the side, A82) and is what the chore runs at G4 first.
Price: one certificate = one root LP (≈ 15 min, C1) + ≤ 5 verifier runs (minutes each) —
hours per class, against A57's ≈ 1.6 desktop-days per side (T23: 6.4 desktop-days for 4 sides at 5
workers). Every A57 leaf already emitted stays valid (its slab); nothing is retracted.

**The U_S / m_u caveat, honestly.** `slots94.json`'s `usable` field lists the FULL-window
extensions only (m_u = 3 per class); the chore ran m_u = 4, counting the k6_23 slot (k5_11 TR(0,0),
k5_16 BL(1,0)), whose extension is dead on [3.82, 3877/1000) only. A certificate with U ∋ that slot
therefore composes through Theorem N-S with ŝ′ = 3877/1000: exact for every window with s ≤ G2
(< 3877/1000) — all the slab windows — and for the s0 windows it kills [m_lo, s0) ∩ [3.82,
3877/1000 − δ], leaving the sliver [3877/1000, s0) to A57's G1 slab (which covers it). The
certificate files themselves are statements about the DECLARED U and are unaffected; the budget
N + 2m_u e with m_u = 4 is the right one for them. Had k6_23 been avoided (m_u = 3, budget 6 + 6e)
the LPs would have been strictly harder (fewer incidences to charge) — the chore's choice is the
favourable and sound one. **Status after the chore: no certified PASS, so the composition is not
instantiated for either class; A57's four sides (now A96's parametric pass) remain the kill.**

**Uniqueness clause.** Unchanged: at ŝ the G1 slab applies.

## 6. [T+M] The protected tier: the Trump-image ceiling

**Lemma CEIL-T [T].** Let g·ẑ (a D4 image of Trump, side ŝ) contain the pins of S, and let U be
a set of usable slots of S with second-largest non-pin depths d₂(g, p) in the image. (i) If
δ ≤ δ_T(S, U) := max_g min_{p∈U} d₂(g, p) then CS(S; s, m_lo; δ, ·) cannot pass for any window
containing ŝ (its claim is false at the image). (ii) Theorem N-S with such an S reaches at most
ŝ − δ_T(S, U) from below. *Proof.* (i) the image is a packing of class S at side ŝ ∈ [m_lo, s)
with two non-pin squares of depth ≥ δ at every p ∈ U; a PASS would contradict Lemma CW-S's
conclusion. (ii) kills need δ > δ_T. ∎

[M, exact on the 60-digit Trump, `code/protected94.py` → `results/protected94.json`; usable slots
from `slots94.json`, "after" = with k5_11/k5_16 dead on the window (A94 + A57 G1), k6_23-type
partial windows counted as usable]:

| class | k / N | unclipped | usable now → after | compatible images | δ_T now / after | chain ceiling ŝ − δ_T | verdict |
|---|---|---|---|---|---|---|---|
| k5_11 | 5 / 6 | 4 | 4 → 4 | none | 0 | ŝ | **LP-limited only** |
| k5_16 | 5 / 6 | 6 | 4 → 4 (6 if k6_27 lands) | none | 0 | ŝ | **LP-limited only** |
| trump5 | 5 / 6 | 6 | 4 | id | 0.1555 | 3.7216 | VOID (Trump is its own crowd) |
| k4_03 | 4 / 7 | 5 | 1 → 2 | transpose | 0.2801 / 0.1555 | 3.597 / 3.722 | **VOID on W** |
| k4_06 | 4 / 7 | 5 | 1 → 2 | transpose | 0.3053 / 0.1555 | 3.572 / 3.722 | **VOID on W** |
| k4_08 | 4 / 7 | 7 | 3 → 3 | id, transpose | 0.2640 | 3.613 | **VOID on W** |
| k4_11 | 4 / 7 | 7 | 4 → 5 | id | 0.0160 (BL(0,2): Trump's sq7) | 3.8611 | chain reaches ≤ 3.861 − pad ≈ 3.85; shell to P-TREE |
| k4_05 | 4 / 7 | 5 | 1 → 3 | none | 0 | ŝ | LP-limited (weak with 1 slot) |
| corners4 | 4 / 7 | 8 | 0 → 8 | none | 0 | ŝ | LP-limited, after k5_16 |
| k3_01…k3_05, k2_00…k2_02, k1_00, k0_00 | | | 0 → 0 | (images exist; δ_T = 0 whenever a usable slot holds an image's own single corner square) | | | **blocked**: every extension is a protected k4 class or an s0-only A55 k4 kill |

So the PI's "then the protected tier": three of the six protected k4 classes (k4_03, k4_06,
k4_08) are exactly as crowd-protected as trump5 — their compatible Trump image sits with all
usable slots doubly met at depth ≥ 0.155, so no slot-crowd certificate can reach the window — an
exact obstruction, before any LP, of the same kind as K1-protection (a kill would refute Trump's
image). They keep Lemma P-TREE (A84). k4_11's escape is the one shallow crowd Trump has (sq7 at
0.016 in BL(0,2)); k4_05 and corners4 have no image and become crowd-eligible once k5_11/k5_16 are
dead on the window (corners4 needs k5_16 for ALL eight of its slots — the K1 lattice's
`sup_k5 = [k5_16]` in another guise). The k ≤ 3 tier is blocked one level down: it needs window
forms of A55's eight s0-only k4 kills (A82's cold PASSes at 3.833212 say those LPs are easy) and
the protected k4 kills; both are the tower's next rung, not this attempt's.

## 7. Canaries

* **Exact Trump, slot depths** [M, `results/trump_canary94.json`]: trump5's 8 completable slots:
  BL(0,2) free meeters (4: 0.967442, 7: 0.016049); BL(1,1) (7: 0.542145, 8: 0.280083); BL(2,0)
  clipped by pin 2 (overlap 0.122916 = 4 − ŝ) + sq8 0.432354; BR(0,1) (10: 0.524494, 8: 0.252050);
  BR(1,0) clipped by pin 1 + sq8; TR(0,1) (10: 0.542145, 9: 0.264033); TR(1,0) (9: 0.451358, 6:
  0.305293); TL(0,0) (6: 0.168321, 4: 0.155475). Every unclipped slot doubly met (A58 §5
  reproduced exactly); the containment lemma holds for all six free squares at all eight slots
  (no point behind a backed side below height 1; sq4 is flush with the left wall, x′ = 0, allowed).
  Corner depths (A92 convention) TL 0.168321 / 0.155475, the other corners single pins: agrees
  with A90 §5 and A92 §4. **PASS** (the mechanism of §2 is consistent with the minimiser).
* **The lemma at trump5 is not a theorem about Trump's shallow crowd:** SLOT-SLIDE at ŝ gives
  d₂ ≥ 0, vacuous; the slot BL(0,2) with d₂ = 0.016 would, at a side m < ŝ − 0.016 in a class
  where its extension were dead, be excluded — consistent, since no such packing exists.
* **A57 consistency:** the certificates of §4 speak about sides < s (never above); A57's G1 kills
  are s0 slack-core tree leaves of the same classes on the slab (3.861637, s0]; the two are
  independent kills of overlapping side ranges and neither is read by the other's code.
* **Images:** no Trump image contains the pins of k5_11 or k5_16 (Trump's TL corner is clear at
  depths 0.168/0.155, nothing within 10⁻² of the TL slot), so the engine's image-realisation gate
  is vacuous for them; for trump5 it fires at a_w ≥ 0.98395 (the BL(0,2) crowd) — reported, never
  run.

## 8. Lean-readiness (what A93's `crowd_sound` generalises to)

* `crowd_sound` (A93 T1) is stated for four corner boxes with the 8-square count. The slot form
  needs: (i) `checkCaseI` with the k pin cores (already supported: CaseChecker's cores) and the
  (P2) exemption for core-meeting poses; (ii) per-slot widened families F_p(a_w) with the slot
  frame = a corner frame composed with an integer translation (Zones/D4 machinery + `Φ_p`), and
  the pad of Lemma B-YES-S (one `max` and one Lipschitz bound, `bprime_containment`-style);
  (iii) r_max runs B_r with exemption sets E_r, and the counting lemma Σ_{Q′} (1 + e r(Q′)) ≥
  N + 2m_u e from "each usable slot has two distinct meeters" (a Finset double-count: Σ_p 2 ≤
  Σ_p #meeters(p) = Σ_{Q′} r(Q′)); (iv) Lemma B's pin-slack clause (λ−1)A_S < ρ (`lemma_B` /
  B.0(c) in Dilation.lean, already Lean). No new checker.
* SLOT-CROWD = `teleport_packing` + `class_kill` of the extension class instantiated by the
  parametric window certificate (`ParamBridge`) — one lemma per usable slot, with the window
  hypothesis W_T explicit (k6_23's [3.82, 3877/1000)).
* SLOT-SLIDE = Lemma MOVE (Fact A/CLUSTER for non-pin pairs — A90's N1–N2 — plus Lemma SWEEP, a
  floor-function argument on unit cells) + the exact diagonal rate + the joint-cluster iteration
  (≤ N − 1 enlargements) + SLOT-CROWD at the landing side. The pin-block motion is a definable
  map on the pose vector (per-pin displacement β_j·τ), so `ContainsPins P_S (m + τ)` is by
  `simp` on slot affinity. A93 T2 should formalise the JOINT form (§3.4) for corners as well.
* Theorem N-S composes into `stratum_kill`'s k5_11/k5_16 pieces as: chain certificates (V.CASE
  replays) + SLOT-CROWD + SLOT-SLIDE on [3.82, ŝ′ − δ_∞] and A57's G1 leaves (`classKilledAt_of_tree`,
  slab form via B′) on the shell.

## 9. Obligations ledger

| # | item | status |
|---|---|---|
| A94-O1 | clip census, extension classes and windows for k5_11/k5_16 (+ tier) | [M] §1.2, `slots94.json` |
| A94-O2 | Lemma CONT (containment in the slot frame) | [T] §1.3 |
| A94-O3 | Lemma SLOT-CROWD (∀-packings, per usable slot, window W_T) | [T] §2 |
| A94-O4 | Lemma SWEEP, Lemma MOVE (pin blocks move with their walls; no (C) contact) | [T] §3.1–3.2 |
| A94-O5 | Lemma SLOT-SLIDE, d₂ ≥ ŝ′_p − m; joint-translation correction to A92 §3.1 | [T] §3.3–3.4 |
| A94-O6 | Lemma B-YES-S (slot pad), Lemma CW-S (incidence budget, 1 + r_max runs) | [T] §4.1–4.2 |
| A94-O7 | certificates CS(S; s, m_lo; δ, e) for k5_11, k5_16 at s0 (windows [G2, s0), [3.82, s0)) and G4 | [M] §4.4 — chore |
| A94-O8 | Theorem N-S; A57 re-price table | [T] §5 |
| A94-O9 | Lemma CEIL-T and the tier table (exact Trump) | [T]+[M] §6 |
| A94-G1 | k6_27's window kill (A61) → k5_16 gains BR(1,0), TL(1,0) | [C] (A61) |
| A94-G2 | window forms of A55's eight s0-only k4 kills + the protected k4 kills → the k ≤ 3 tier's usable slots | [C] next rung |
| A94-G3 | the shell (ŝ′ − δ_∞, ŝ] for k5_11/k5_16: A57 G1 (running) / A96 parametric | [M] A57, A96 |
| A94-G4 | certification-engine gap: the incidence rows (r ≥ 2) are not priced by the row oracle — B₂–B₄ fail on 30–32 exact holes at every LP-passing node; needs an oracle pass at threshold α(1 + re) over the r-level cells (or witness feedback until minmass = 1 on every run) | [C] |
| A94-G5 | at the s0 side the LP stops at δ = 0.2 (k5_11 τ = 7.007 vs 7 at δ = 0.1, e = 1/8): δ_∞ ≥ 0.2 ≫ 0.0446; the chain removes no A57 side | [M] closed negative |
