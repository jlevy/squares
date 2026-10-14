# HANDEDNESS — counting tilt handedness across the container: TORQUE-ID exactly (global, per wall, per corner), the probe on 1 393 stressed witnesses, and why no handedness count separates a four-crowd from an optimum — A234, 2026-09-15

The PI (19:00): "the fact that we need 'not all four at once' plus the gear lemma is why I was thinking of counting handedness across
the container, since a convex shape can't provide a net torque; that would allow Trump et al. (one or more non-simple corners) AND
extend up in n."  This file (i) states and proves the torque identity in its three forms — about the container centre, per wall,
about each corner point — with Lemma W's handedness sign, all n-free; (ii) tabulates on every witness with a stress (A217's 486
witnesses incl. the 193 four-crowds, the 883 genuine free FJ points, Trump, S02, S07, 21 record packings n = 5 … 55) the
per-square (χ, N, d, W, τ^wall), per-wall (pressure, first moments, handedness mix) and per-corner (arm moments) data, with LP
ranges over the multiplier polytope; (iii) tests the three candidate counts of the brief and every scalar the data suggests for a
separation between four-crowds and ≤ 3-crowd optima; (iv) says exactly what Trump and the ring share that defeats the count.
Tags: [T] proved, [S] routine, [M] measured, [F] false (with the witness), [C] obligation.  Sources: `local_lock.md` (RADIAL,
CHAIN, NO-SELF-STRESS), `two_grains.md` (Lemma W, TORQUE-ID's first statement), `wall_torque.md` (RING, TWO-CONTACT,
ONE-TILTED, the deficit), `k0_count.md` (PUSH, HOLD), A217 `notes/torque.md` (C1–C3), A219 `rows219`.  Code
`attempts/A234-handedness/code/` (`stress234.py`, `hand234.py`, `summarise234.py`, `global234.py`, `pages234.py`, `test234.py`);
results `results/hand234.{jsonl,md}`; pages `docs/residue_map/campaigns/A234-handedness/`.  No Lean file: nothing separates, so
there is no axiom to document (the FJ predicate has no object in the readable layer; the identities are prose [T]).

## 0. Verdict

> **[T] TORQUE-ID in three forms** (§1), every n: (G) the wall forces of any FJ point have zero moment about the container centre
> — equivalently Σ_i τ_i^wall = −C, the aligning self-torques of the wall-touchers against the circulation C of the wall pressure;
> with Lemma W this is the HANDEDNESS SUM S := Σ_{tilted} χ_i W_i d_i = C + F, F the self-torque of the flat wall-touchers (free
> in [−W_i/2, W_i/2] each).  (W) There is NO per-wall identity: a wall's pressure and moment are constrained only by the global
> identities and the trivial bounds ([M] the polytope span of a wall's pressure is up to 1.0 on free FJ points).  (K) About each
> corner point the arm's floor rows turn it one way (≥ 0), its wall rows the other (≤ 0), and the external pair rows supply the
> difference: this is the rigid-body equilibrium of the arm, RADIAL's rotational twin, and it excludes nothing by itself.
> [M] residual ≤ 3·10⁻⁵ on 1 393 witnesses, ≤ 6·10⁻⁶ on 1 363 doubly-met corners; Lemma W's sign 2 920 / 2 920.
>
> **[F] No handedness count separates.**  Every scalar built from (χ, N, d, W, positions) that the identities constrain —
> perimeter flips, mixed walls, the signed load imbalance, the demand of anti-aligning torque and its along-wall / interior
> supply, |C|, |C| relative to its bound, |S|, |F|, the meeters' S — has a range on the 193 four-crowds that overlaps its range on
> the 883 free FJ points AND on the optima (§3, table in `hand234.md`).  The one quantity that separates is the external load
> (RING: every four-crowd needs a tilt bound or a crowd pull), which is not a count.  **[M] The global relaxation**: the four
> rigid-body identities (two force sums, the moment about O, the s-row) are satisfiable by the WALL rows alone, λ ≥ 0, on 178 of
> the 193 four-crowds (the 15 exceptions have a wall with no contact at all or a single contact); so nothing derived from
> TORQUE-ID + Lemma W + pressure bounds can see a four-crowd — what fails there is the PER-SQUARE balance (TWO-CONTACT on the
> tilted meeters and their holders), which no global count carries.
>
> **[T]+[M] What Trump and the ring share** (§4): a torque-neutral reservoir on the walls that carries pressure at zero net
> handedness, and a circulation whose scale beats the self-torques by the factor s − 1.  Trump's reservoir is its six flush
> squares (edge-on-wall: two vertex rows each, self-torque free in ±W/2 — C spans 0.33 over Trump's polytope, S = 0.035 fixed);
> the ring's is its ± pairs (the ceiling carries sq 10 '+' and sq 3 '−' at equal loads 0.196; S itself spans [−0.117, +0.117]).
> Handedness counting sees a flat square and a ± pair identically.  And at every n the identity is slack: a wall-toucher's
> self-torque is at most W/2 while its lever arm about the wall's midpoint is up to (s − 1)/2, so |S| ≤ P/2 ≤ 1/2 ≪ (s − 1)·P/2 =
> the circulation's reach — |C|/bound is 0.03 at Trump, 0.09 at the ring, ≤ 0.66 on every witness.  The premise "eight tilted
> meeters each carrying N_i d_i" is false as well: 324 of the four-crowds' 1 544 meeters carry no wall load.  k0_00 unchanged.

## 1. TORQUE-ID exactly (task 1)

**Setting** (A217/A219 row model, any n).  Packing at an FJ point of NLP(S): rows g_k ≥ 0 (near-wall q_a ≥ 0, far-wall s − q_a ≥ 0,
pair rows n·(q_k(p) − c_o) − ½ ≥ 0 with n an outward edge normal of the owner o), multipliers λ ≥ 0, λ₀ e_s = Σ λ_k ∇g_k, λ₀ = 1
(NO-SELF-STRESS, `local_lock.md` §3.3).  Row k's force on square i is F_{k,i} = λ_k ∇_{c_i} g_k, applied at the row's contact
point q_k; its θ_i-gradient is the torque (q_k − c_i) × F_{k,i} [T, A217 §2: q = c + R(θ)h, ∂_θ q = J(q − c)].  Stationarity in
(c_i, θ_i) is force and torque balance of square i.  A pair row applies ±λn at the same point to its two squares.

**1.1 Lemma TORQUE-ID (G) [T].**  For any point O,
  Σ_{wall rows k} λ_k (q_k − O) × n_{w(k)} = 0,   n_w the inward wall normal.
Equivalently, writing (q − O) × n = (q − c_i) × n + (c_i − O) × n:  **Σ_i τ_i^wall = −C**, τ_i^wall := Σ_{wall rows of i} λ (q − c_i) × n
(the wall self-torque of square i) and C := Σ_floor λ x̃_i + Σ_right λ ỹ_i − Σ_ceil λ x̃_i − Σ_left λ ỹ_i (x̃, ỹ the centre's
coordinates from O; each term is that wall's first moment of pressure about its midpoint, in the rotational sense).
*Proof.* Square i's moment about O: Σ_k (q_k − O) × F_{k,i} = Σ_k (q_k − c_i) × F_{k,i} + (c_i − O) × Σ_k F_{k,i} = 0 + 0.  Sum
over i; the two terms of a pair row are ±λn at one point and cancel; the wall rows remain. ∎  With the force identities
(Σ wall forces = 0 ⇒ P_{x=0} = P_{x=s}, P_{y=0} = P_{y=s}; the s-row ⇒ P_{x=s} + P_{y=s} = 1) these are the four rigid-body
equations of the packing as one body.  External rows (tilt bounds, crowd pulls), where present, add their moments about O.

**1.2 Lemma W [T, A217 §2]** and the handedness form.  A square of tilt φ = θ mod 90° touching a wall at a vertex with force W
receives τ = W (sin φ − cos φ)/2 about its centre, on every wall: sign −χ, χ = +1 for φ < 45°, −1 for φ > 45°, 0 at 0° and 45°
(d(φ) := |sin φ − cos φ|/2 ≤ ½).  A flat square touching a wall along an edge has two vertex rows and τ ∈ [−W/2, W/2], free.  So
  **S := Σ_{tilted touchers} χ_i W_i d_i = C + F**,  F := Σ_{flat touchers} τ_i^wall,  |F| ≤ Σ_{flat} W_i/2.
[M] 2 920 / 2 920 loaded tilted touchers have sign(τ^wall) = −χ; S = −Σ_{tilted} τ^wall on every witness (test234).

**1.3 (W) No per-wall identity [T]+[M].**  The wall rows of one wall enter the balance of every square that touches it, whose other
rows are pair rows to squares that need not touch that wall; summing the balances of ANY subset of squares leaves the external
pair rows of the subset, which vanish only for a subset closed under contact — a component of the contact graph, which at an
optimum is everything (`local_lock.md` CHAIN).  So a wall's pressure P_w and its moments M_w^c (centres), M_w^q (contact points)
are constrained only by 1.1 and by the bounds 0 ≤ P_w, |M_w^q| ≤ (s/2) P_w, |M_w^c| ≤ ((s − 1)/2) P_w (a wall-toucher's centre is
at least (cos φ + sin φ)/2 ≥ ½ from the wall's ends).  [M] The polytope span of P_w: median 0 but up to 1.000 on the free FJ
points and the optima (the split of the far-wall unit between x = s and y = s is free whenever a flat corner square touches both).

**1.4 (K) Lemma ARM-MOMENT [T].**  Corner c with frame (u, v), corner point p_c, any set U of squares (the arm: the meeters of c,
or their loaded component).  In the frame (det-adjusted),
  Σ_{near-floor rows of U} λ q_u − Σ_{near-wall rows of U} λ q_v + Σ_{far rows of U} λ (q × n) + Σ_{external pair rows} λ (q − p_c) × F_member
  (+ external rows) = 0,
the first sum ≥ 0 (the floor pressure turns the arm away from the u-wall), the second ≤ 0 (the wall pressure turns it toward the
floor), far rows: u = s contributes +λ q_v, v = s contributes −λ q_u.  *Proof.* 1.1's argument with O = p_c on the squares of U;
the pair rows internal to U cancel, the external ones stay.  Signs: (q_u, q_v) × (0, 1) = q_u ≥ 0, (q_u, q_v) × (1, 0) = −q_v ≤ 0. ∎
Reading: together with RADIAL (the radial component of the same external forces) the external load on an arm is the exact negative
of its wall reaction — the arm is a rigid body in equilibrium.  [M] 1 363 / 1 363 doubly-met corners: residual ≤ 6·10⁻⁶, floor
term ≥ 0, wall term ≤ 0.  Trump's TL: floor +0.432, wall −0.289, external pair rows −0.144 (sq 7, sq 9 through sq 6 and sq 4).
The ring's BL: floor 0, wall −0.689, external pairs +0.988 (the adjacent crowds' meeters), the tilt bound −0.300.

## 2. The probe (task 2) — `results/hand234.md`

1 393 witnesses, all with a bounded FJ stress (L1-minimal λ; the polytope explored by LPs for the linear functionals C, S, F,
S_meet, P_w).  Groups: OPT (Trump, S02, S07, the 21 records n = 5 … 55: 24), FJ (A217's genuine free FJ points: 883, n2 ≤ 3 —
0 four-crowds), W3 (A217's other witnesses, external rows allowed: 293), FOUR (the 193 four-crowds, all with external load
0.13 … 9.95).  Per square χ, N, d, W, τ^wall, τ^contact split into along-wall / interior holders, τ^ext; per wall P, M^c, M^q, the
loaded touchers with their perimeter coordinate and handedness; per corner the arm moments; the three candidates:

| candidate | value on Trump | on the ring (`rand_0_0569|t20`, 4.1099) | OPT / FJ / FOUR ranges | separates? |
|---|---|---|---|---|
| (a) perimeter handedness flips (cyclic sign changes of χ along the loaded tilted touchers); walls carrying both signs | 0 flips (sq 10, sq 6 both '+'); 0 mixed walls | 2 flips (+ + + − −: 6, 7, 10 '+', 3, 5 '−'); 1 mixed wall (the ceiling) | flips OPT {0}, FJ {0, 2}, FOUR {0, 2, 4} (56 / 125 / 12); mixed walls FJ 0–2, FOUR 0–3 | no: 56 four-crowds have a one-handed loaded perimeter (0 flips) like every optimum |
| (b) anti-aligning demand Σ χ W d of the tilted touchers vs its supply (along-wall holders / interior holders / external rows) | demand 0.035, all from interior holders (sq 6 ← sq 9, sq 10 ← sq 8); along-wall 0 | demand 0.117: along-wall −0.035, interior +0.134, external +0.019 (the tilt bound on sq 7) | demand OPT ±0.11, FJ ±0.50, FOUR ±3.98; along-wall share OPT/FJ 0, W3 −0.17, FOUR −0.01; external share FOUR 1.10 | no: the split is unconstrained; only the external term separates, and it is RING |
| (c) circulation vs self-torque: C, its bound (s − 1)P/2, S, F, S_meet | C = −0.083 (bound 2.88, ratio 0.029), S = +0.035 (fixed in the polytope), F = +0.118 (range [−0.21, 0.12]), S_meet = 0.016 | C = +0.275 (bound 3.11, ratio 0.088), S = +0.117 (range [−0.117, +0.117]), F = 0, S_meet = 0.117 | ratio OPT ≤ 0.13, FJ ≤ 0.33, FOUR ≤ 0.66; |S| OPT ≤ 0.11, FJ ≤ 0.50, FOUR ≤ 3.98; |S_meet| FJ ≤ 0.50, FOUR ≤ 3.98 | no: every range overlaps; the FOUR maxima are the crowd pulls (P up to 9.95), the FOUR minima are 0 |

The full scalar table (19 quantities, min / max / median per group, Trump and ring columns) is in `hand234.md`; the only "YES"
is `ext_load`.  Per-wall handedness mix: on the four-crowds 85 have no mixed wall, 79 one, 25 two, 4 three — and Trump's walls are
one-handed too (every tilted toucher '+').  The 883 free FJ points with n2 ≤ 3 include 242 with loaded tilted touchers and 29 with
2 flips: the flip count is not a property of crowds.

## 3. The search for a separating inequality (task 2, second half) — [F]

A necessary inequality on (χ_i, N_i, d_i, positions) satisfied by every ≤ 3-crowd optimum and violated by every four-crowd would
have to follow from the identities of §1 (the only sign information the walls impose is Lemma W) and the geometry of crowds.  Two
measurements close this off.  (i) [M] **The global relaxation** (`global234.py`): the LP {λ ≥ 0 on the wall rows only; Σ F = 0;
Σ (q − O) × F = 0; Σ_far λ = 1} — every consequence of TORQUE-ID and the force identities, external rows dropped — is FEASIBLE on
178 / 193 four-crowds (292 / 293 W3, 3 / 3 optima).  The 15 infeasible four-crowds have a wall with no contact (12) or a single
contact point on a wall that cannot balance the moment (3: `w167`, `w201`, `w212`; the one W3 exception `w404_held` is of the
same kind); none of them is a candidate for a crowd that is a packing minimiser.  Since Lemma W's torques are carried by the wall rows themselves, any inequality in
(χ, N, d, positions) derived from the identities is implied by this LP's feasibility and so holds at 178 four-crowds.  (ii) [M]
**The per-square balance is what fails**: RING (A219, now CHAIN for all n) — the free FJ LP with the pair rows and every square's
balance is infeasible 193 / 193.  The difference between (i) and (ii) is TWO-CONTACT on the tilted meeters and Lemma HOLD on
their holders, a statement about individual squares' torque balance that has no global sum.  (iii) The brief's premise for (c),
"eight tilted meeters each ≥ N_i d_i": 324 of 1 544 four-crowd meeters carry no wall load (a meeter need not touch its walls in
the stress: the ring's sq 2, 4, 8), and ONE-TILTED guarantees only one tilted meeter per corner, whose wall load may be 0.

## 4. What Trump and the ring share (task 3, negative clause)

**[T] Scale.**  |τ_i^wall| ≤ W_i/2 for every wall-toucher (d ≤ ½, and a flat edge's two rows give |τ| ≤ W/2), so |S − F| =
|Σ τ^wall| ≤ P_total/2 = 1 (P_total = 2 by the force identities).  The circulation C = Σ_w M_w^c has reach ((s − 1)/2) P_total =
s − 1.  So the identity S = C + F constrains C to an interval of width ≤ 2 inside one of width 2(s − 1) ≥ 2(2 + √2 − 1) = 4.83: the
walls' torque budget is slack by the factor s − 1 at every n ≥ 5, growing with n.  Nothing bounds S from below: |S| ≤ Σ W d, with
equality iff all loaded tilted touchers have one handedness, and S = 0 is available to any packing whose tilted wall load is
balanced between the two handednesses or carried by flat squares.

**[M] The shared reservoir.**  Trump: the six flush squares carry 1.59 of the wall pressure 2.00; their self-torques F range over
[−0.21, +0.12] in the polytope while S = +0.035 is fixed (sq 6 at 40.18° on the ceiling, sq 10 on the right wall), and C over
[−0.08, +0.25]: the flat squares absorb the tilted strip's aligning torque without any handedness appearing.  The ring: no flat
square is loaded (F = 0); the two half-rings of opposite tilt (BL, TL meeters at 70°, BR, TR at 20°) put both handednesses on the
walls with equal ± loads on the ceiling, S ranges over [−0.117, +0.117] in the polytope, and C over [−0.23, +0.27].  In both the
circulation used is 3–9 % of its reach.  A count of handedness sees these two reservoirs as the same thing — a wall contact with
zero net handedness — and it is exactly the thing an optimum with a flush corner (Trump, S07: F = −0.295 carries the whole
circulation) and a self-supporting ring (S free, F = 0) both have.  This is A223's Lemma TWO-GRAIN read from the walls: the ring
is two opposite grains, Trump one grain plus flat squares, and to the torque identity a flat square is a grain of either sign.

**[C] What would separate.**  The quantity the four-crowds do not have is a WALL-ROW-ONLY stress that also balances each meeter:
TWO-CONTACT says a tilted meeter with along-wall load needs two contacts, HOLD that its holder pushes it toward the corner, CHAIN
that the holder chain reaches a far wall — and the handedness count adds to these nothing, because the chain's torque bookkeeping
is per square and closes on every square (C2, C3 of A217 are identities).  The residue stays LOCKED-CROWD-FREE(n) (`local_lock.md`
§1.2) with the per-square balance as its only known force-side content; at n = 11, RAISE(0 → 1) / STEP.  k0_00 unchanged.

## 5. Files, reproduction

`python hand234.py` (64 s: 1 393 stresses, 20 LPs each), `python summarise234.py`, `python global234.py` (appends the relaxation),
`python pages234.py` (2 pages, 12 panels, geometry check printed per panel), `python test234.py` (30 checks: Lemma W on 800 random
poses and walls, pairwise cancellation of pair-row moments about a random point, TORQUE-ID global and per corner on Trump, S07, the
ring, the n-general row model against A217's on Trump, the handedness calculus).  S02 is A110's polished pinwheel (coordinates
1e-8): the LP carries a 1e-6 slack on the stationarity equation for it and the records; the residuals above include that slack.
