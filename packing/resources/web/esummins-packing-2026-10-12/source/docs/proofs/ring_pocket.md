# RING-POCKET(11) — the all-ADJ ring family, the BOX-VALID pierce and its price, and the analytic route through the INSCRIBED DISC — A251, 2026-09-17

A249 built the ALL-ADJ TYPE-T RING (eight tilted wall touchers, every one reaching the far slot of its wall, all
twelve border cells doubly met by the eight; an exact rational witness at ŝ) and killed the one explicit witness by
A237's PIERCE(1) certificate: its pocket holds ONE square, 8 + 1 = 9 < 11.  A250's count leaves exactly that family.
RING-POCKET(11) is the same statement for the WHOLE family: the pocket of every all-ADJ ring on [3.82, 4) holds at
most TWO unit squares, so 8 + 2 < 11.  This note (i) parametrises the family exactly and proves Lemma GAP, (ii) makes
PIERCE BOX-VALID in the sound direction (cores under-approximated, pocket over-approximated) and PRICES it — the
product law reappears in its COUNTING form and the route stops at the design, (iii) opens the analytic route that
replaces it: the INSCRIBED DISC (Lemma INRADIUS + Lemma THREE-DISC reduce RING-POCKET to a RADIUS, Lemma CENTRE-DISC)
and proves Lemma MID-NOTCH, which kills the wall notches outright on the window, and (iv) says exactly what is left.
Tags: [T] proved, [T-computed] certified / exactly verified, [S] routine given cited items, [M] measured,
[F] false as stated, [C] obligation.  Sources: `type_t_chase.md` (A249: T-CELLS / T-TIP / T-SLOTS, the ring, its
pocket), `attempts/A250-family-stuck/results/family250.md` (FAMILY-STUCK, the count minimum 9 below 4),
`pocket_waste.md` (A237: Lemma JAGGED, the coverable sandwich, PIERCE, Lean `capacity_le_of_pierce`),
`ring_capacity.md` (A236: Lemma TWO, POCKET(n)), `corner_chase.md` (A248: TWO-POKERS), A242/A243 (the product law on
pose boxes), A171 (multibox cores).  Code `attempts/A251-ring-pocket/code/` (`geom251`, `family251`, `cert251`,
`joint251`, `analytic251`, `test251`, `summarise251`, `pages251`, `run251.sh`, `finish251.sh`); results
`results/pocket251.md` (+ `cert251.json`, `joint251.json`, `analytic251.json`); pages
`docs/residue_map/campaigns/A251-ring-pocket/{ring_pocket,notch_bound,failing_box}.svg`; Lean
`Statements/Open/RingPocket.lean`.

## 0. Verdict

> **[T] The family is a bounded box in 17 coordinates** (§1): per corner the wall meeter's (θ_B, δ_B) and the floor
> meeter's (θ_A, δ_A), plus the side.  All-ADJ forces δ ∈ (s − 2 − w(θ), 1) ⊆ (0.406, 1) on the window, so the box is
> [0, 90°]⁸ × [0.406, 1]⁸ × [3.82, 4].  **[T] Lemma GAP**: on each wall the two touchers' extents overlap or leave a
> gap < 4 − s ≤ 0.18 (both reach past s − 2, so (δ + w) + (δ′ + w′) > 2s − 4).
>
> **[T] The box-valid certificate is sound and [F as a route] priced out** (§2).  Over a parameter box the CORE of a
> member — the square of the box-centre pose with half-side (½ − ρ)/w(Δθ), ρ the centre displacement, Δθ the tilt
> deviation — lies inside that member at EVERY parameter of the box ([T], `test251.test_core_sound`: 0 violations on
> 2 400 samples), so the pocket is OVER-approximated by container minus cores and a PIERCE certificate on the
> over-pocket is valid for every ring of the box.  At A249's ŝ witness the certificate survives a uniform core shrink
> of **ε\* = 0.0952 for PIERCE(1)** at the centre and **ε\* = 0.1397 for PIERCE(2)** (points (1.739, 1.939),
> (2.139, 1.939)) — cores of half-side 0.360 instead of 0.5.  But ε\* = 0.1397 admits a box of half-width only
> **r = 0.0312** in all 17 coordinates, and the window then needs **3.9 × 10¹⁸ boxes** (D4 quotient included) at
> ≈ 0.5 s each: **5 × 10¹⁴ CPU-h against a 200 CPU-h stop, a factor 3 × 10¹²**.  The product law is NOT the cores
> going empty (that needs r = 0.121); it is the COUNT — 17 coordinates at a radius the certificate fixes.  **Stop at
> the design.**  The AREA bound is worse, not better: coverable 2.736 < 3 at the witness (so the area bound alone
> gives capacity ≤ 2 there) but it breaks at ε = 0.03.
>
> **[T] The analytic route replaces the pierce by a RADIUS** (§3).  **Lemma INRADIUS**: a unit square contains the
> open disc of radius ½ about its centre, so interior-disjoint unit squares have centres ≥ 1 apart.  **Lemma
> THREE-DISC**: three points pairwise ≥ 1 apart do not fit in a disc of radius R < 1/√3 = 0.57735 (two of them subtend
> ≤ 120° at the centre, so their distance is ≤ √3 R).  Hence **Lemma CENTRE-DISC ⟹ RING-POCKET**: if every unit square
> of the pocket has its centre within 1/√3 of the container centre, the pocket holds at most two — no pierce, no
> boxes, one number.  **[T] Lemma MID-NOTCH** (§3.3) closes the wall notches: a disc of radius ½ between the two
> touchers' inner edge lines and the wall would need g(θ) + g(θ′) < 2(4 − s) ≤ 0.36 with g(t) = (1 + sin t)/cos t −
> 2 sin t, whose minimum is **0.72355 at 26.261°** — so 1.44711 < 0.36, absurd: **no wall notch of an all-ADJ ring
> holds a disc of radius ½ at any s > 3.27645**.  In the ROBUST form the case analysis actually needs (separation
> margin 1/(2√2) rather than ½) the constant is min g₂ = 0.19658 at 28.904° and the notch is dead for s > 3.80342 —
> the window clears it by 0.017.  A249's poking free square is consistent: it enters the notch with a CORNER, its
> inscribed disc stays central.
>
> **[C] What is NOT closed**: the CORNER wedge (a disc between the wall meeter's lower edge and the floor meeter's
> left edge) and the vertex sectors of the separation case analysis, i.e. Lemma CENTRE-DISC itself.  So
> **RING-POCKET(11) is [T-computed] on the sampled family and [C] as a theorem**; the family-stuck existence
> obligation on the window is NOT closed — it now reads: CENTRE-DISC for the all-ADJ ring (a radius bound in 17
> parameters), plus the non-ring / mixed family-stuck structures A249 §3.4 leaves.  **k0_00 unchanged.**

## 1. The family, exactly (task 1)

**1.1 Parameters.**  Corner frame per corner c ∈ {BL, BR, TR, TL} (A249 `geom249`): the WALL meeter B with wall
vertex L = (0, δ_B + cos θ_B) and lowest vertex V = (sin θ_B, δ_B); the FLOOR meeter A with lowest vertex
V_A = (δ_A + sin θ_A, 0) and leftmost vertex W_A = (δ_A, cos θ_A).  Constraints of the ALL-ADJ ring
(`type_t_chase.md` §2.3): 0 < θ < 90°, δ > 0 (WEDGED-SEAL), δ < 1 (T-CELLS: both meeters meet their corner box),
δ + w(θ) > s − 2 (each meeter reaches the far slot of its wall — the all-ADJ supply), the eight squares pairwise
interior-disjoint and inside [0, s]², s ∈ [3.82, 4).  Since w(θ) ≤ √2, **δ > s − 2 − √2 ≥ 0.406** on the window: a
bounded box in 17 coordinates, [0, 90°]⁸ × [0.406, 1]⁸ × [3.82, 4] (`family251.bounds`).  D4 acts on the family by
permuting corners and swapping the roles A ↔ B, and the capacity of the pocket is D4-invariant, so a fundamental
domain divides any box count by at most 8 — immaterial against §2.

**1.2 Lemma GAP [T] (any n, s < 4).**  *Let B, B′ be the two touchers of one wall, with wall extents [δ, δ + w(θ)]
from one end and [δ′, δ′ + w(θ′)] from the other.  If both reach the far slot then the extents overlap or the gap
between them is < 4 − s.*  *Proof.*  δ + w(θ) > s − 2 and δ′ + w(θ′) > s − 2 give (δ + w) + (δ′ + w′) > 2s − 4, and
the gap is s − (δ + w) − (δ′ + w′) < s − (2s − 4) = 4 − s.  ∎  So the wall is uncovered (in extent) only on [0, δ] and
[s − δ′, s] with δ, δ′ < 1 — the two corner notches — plus a middle gap of length < 0.18 on the window.  [M] at the ŝ
witness all four walls OVERLAP by 0.147 (`analytic251`, `test251.test_gap_lemma`).

## 2. BOX-VALID PIERCE, and the price (task 2)

**2.1 The core, and why the direction is the sound one [T].**  Over a parameter box X let member i have box-centre
pose (c̄, θ̄), tilt deviation Δθ = max_X |θ(x) − θ̄| and centre deviation ρ = max_X |c(x) − c̄|.  Then the square of
pose (c̄, θ̄) and half-side **a = (½ − ρ)/w(Δθ)** lies in Q_i(x) for EVERY x ∈ X: for p = c̄ + R̄q with |q|_∞ ≤ a,
|R(θ̄ − θ(x)) q|_∞ ≤ w(Δθ)|q|_∞ (A237's kernel bound) and |R(θ(x))ᵀ(c̄ − c(x))|_∞ ≤ ρ, so |R(θ(x))ᵀ(p − c(x))|_∞ ≤
w(Δθ)a + ρ ≤ ½.  Hence **pocket(x) ⊆ [0, s_max]² ∖ ⋃ core_i(X)** — the pocket is OVER-approximated, the cores
UNDER-approximated; a capacity bound proved for the over-pocket holds for every ring of the box.  This is A242/A243's
direction, made explicit.  ρ and Δθ come from the parameters by Lipschitz constants: |∂centre/∂θ| ≤ 1 + √2/2 = 1.7072,
|∂centre/∂δ| = 1, |∂placement/∂s| ∈ {0, 1, √2} by corner (`family251.deviations`); a box is DISCARDED when
`family251.margin_ub` — the feasibility margin at the centre plus the per-term Lipschitz bump — is negative.
[T-computed] `test251.test_core_sound`: max area of core outside the square over 400 boxes × 6 interior parameters =
0 (exactly); `test_pierce_monotone`: the residual is non-decreasing in the core shrink, as it must be.

**2.2 What the certificate costs.**  At A249's ŝ witness (margin +0.03696, pocket area 7.0318):

| certificate | residual at the exact ring | shrink tolerance ε\* | box half-width r | boxes over the window (/8) |
| --- | --- | --- | --- | --- |
| PIERCE(1) at the centre | 0 | 0.0952 | 0.02106 | 3.14 × 10²¹ |
| PIERCE(2), points re-optimised | 0 | 0.1397 | 0.03120 | 3.93 × 10¹⁸ |
| area bound (coverable < 3) | 2.736 < 3 | ≈ 0.03 | ≈ 0.007 | ≳ 10²⁸ |

and the radius ladder (`cert251.eps_of_radius`, `box_count`): r = 0.005 → ε 0.023, 1.3 × 10³² boxes; 0.01 → 0.046,
9.9 × 10²⁶; 0.02 → 0.091, 7.6 × 10²¹; 0.03 → 0.134, 7.7 × 10¹⁸; 0.05 → 0.220, 1.3 × 10¹⁵; 0.10 → 0.420, 1.1 × 10¹⁰;
0.1213 → 0.5, the cores go EMPTY.  A live box costs ≈ 0.5 s (90 tilt bins at 3°, shapely; 0.77 s at 1°), so the
certificate at its own admissible radius costs **≈ 5 × 10¹⁴ CPU-h**.  **The product law reappears — not as empty
cores (they survive to r = 0.121) but as the box COUNT in 17 coordinates.**  Even buying the whole 200 CPU-h budget
covers 1.4 × 10⁶ boxes, 10⁻¹² of the requirement.  **Stop at the design** (the brief's instruction), and see §3.
The 200-box pilot (`cert251 --stage pilot`, detached) reports the measured discard / certify / fail split and the
per-box time; the numbers above are the design price and do not depend on it.

**2.3 Why PIERCE(2) and not PIERCE(1).**  PIERCE(1) at the container centre certifies capacity ≤ 1 at the exact ring
(A249), but it is the more fragile certificate: it dies at ε = 0.095 while the two-point one lives to ε = 0.140 — a
factor 1.5 in ε and 800 in the box count.  RING-POCKET only needs ≤ 2, so the two-point form is the right target, and
its points sit symmetrically about the centre at ±0.2 along one axis (page `ring_pocket.svg` (b)).

## 3. The analytic pocket: the INSCRIBED DISC (task 3)

**3.1 Lemma INRADIUS [T] (any n).**  *A unit square contains the open disc of radius ½ about its centre; hence two
interior-disjoint unit squares have centres at distance ≥ 1.*  *Proof.*  The square's inradius is ½.  If the centres
were at distance d < 1, their midpoint would be at distance d/2 < ½ from each, so interior to both.  ∎  Lean:
`inradius_sep`, a theorem (from the axiom `unit_square_inball`).  [M] `test251.test_inradius`: least centre distance
1.0396 over 3 000 random disjoint pairs.

**3.2 Lemma THREE-DISC [T] (any n).**  *Three points pairwise at distance ≥ 1 do not lie in a closed disc of radius
R < 1/√3 = 0.57735.*  *Proof.*  Seen from the disc's centre the three points have angular gaps summing to 360°, so
two of them subtend an angle ≤ 120°; their distance is then at most 2R sin 60° = √3 R < 1.  ∎  **Corollary
CENTRE-DISC ⟹ RING-POCKET [T]** (Lean `capacity_le_two_of_centre_disc`, a theorem): if every unit square inside the
pocket has its centre within R < 1/√3 of one fixed point, the pocket holds at most TWO unit squares — so 8 + 2 < 11.
This is the reduction A251 delivers: **RING-POCKET(11) needs one RADIUS, not a pierce and not a box tree.**  It is
the pocket analogue of Lemma TWO (`ring_capacity.md` §2.5), with the disc in place of the square container.

**3.3 Lemma MID-NOTCH [T] (any n, the wall notches).**  *Let B, B′ be the two touchers of the wall u = 0 of an
all-ADJ ring, tilts θ, θ′, offsets δ, δ′ < 1, δ + w(θ) > s − 2 and δ′ + w(θ′) > s − 2.  Let D be a closed disc of
radius ½ with D ⊆ {u ≥ 0}, D above the line of B's edge L → T and below the line of B′'s edge L′ → T′.  Then
s < 4 − 0.72355 = 3.27645.*  *Proof.*  The three half-planes bound a triangle with base
h = (s − δ′ − cos θ′) − (δ + cos θ) on u = 0 and apex at u\* = h/(tan θ + tan θ′); its inradius is
r = h/(tan θ + sec θ + tan θ′ + sec θ′), and D ⊆ triangle forces r ≥ ½, i.e.
h ≥ ½[(1 + sin θ)/cos θ + (1 + sin θ′)/cos θ′].  All-ADJ gives δ > s − 2 − w(θ) and δ′ > s − 2 − w(θ′), hence
**h < 4 − s + sin θ + sin θ′**.  Therefore g(θ) + g(θ′) < 2(4 − s) with g(t) := (1 + sin t)/cos t − 2 sin t.  The
stationary point of g is sec t (sec t + tan t) = 2 cos t, i.e. t\* = 26.261°, and g(t\*) = **0.72355**, so
1.44711 < 2(4 − s): s < 3.27645.  ∎  On the window (s ≥ 3.82) this is a contradiction by a factor 4.
**Consequence: no unit square of the pocket has its INSCRIBED DISC in a wall's middle notch.**  A249's FAMILY-STUCK
poking square (margin +0.0017) is consistent — it enters the notch with a CORNER, its disc stays central.  [M]
`test251.test_mid_notch`: max middle-notch inradius 0.3263 over 20 000 random admissible wall pairs on the window
(bound ½); 0.1174 at the ŝ witness.  Page `notch_bound.svg`.

**3.4 The robust form [T], which is the one a case analysis can use.**  A disc of radius ½ disjoint from a square is
separated from it by an edge LINE only when the nearest point is interior to an edge; in a vertex cone the larger of
the two adjacent edge distances is only ≥ |q − P|/√2 ≥ 1/(2√2) = 0.35355.  Repeating §3.3 with separation margin
μ = 1/(2√2) (the container still gives u ≥ ½) replaces g by **g₂(t) = ½ tan t + μ sec t − sin t**, whose minimum is
**0.19658 at 28.904°**; the notch is then dead for s > 4 − 0.19658 = **3.80342**.  The window [3.82, 4) clears it by
0.017 — tight, but it clears, and this is the form that survives the separation case analysis.

**3.5 What does not close.**  The CORNER wedge: a disc below B's lower edge line V → R and above A's upper-left edge
line W_A → T_A, in {u, v ≥ 0}.  Writing the two distance conditions at the disc centre (u, v) gives
u (tan θ_A − tan θ_B) ≤ δ_B + δ_A tan θ_A − (cos θ_A + ½ sec θ_A) − (sin²θ_B + ½)/cos θ_B
(`analytic251.corner_wedge_bound`): with δ_A, δ_B < 1 the right side is ≤ tan θ_A − 0.914, so the case is EMPTY when
θ_A ≤ 42.4° and θ_A > θ_B, and otherwise gives a one-sided bound on u — a bound, not a contradiction.  Together with
the vertex sectors (4⁸ nominal cases, of which only the four squares nearest a given direction matter) this is the
residue: **Lemma CENTRE-DISC is not proved.**  It is exactly one inequality away from a theorem, and the inequality
is a bound on how far a free square's centre can sit from the container centre.

## 4. Cross-checks (task 4)

* A249's exact ring at ŝ: reproduced from the C2 seed (margin +0.03696 against A249's +0.0370), pocket area 7.0318
  (A249: 7.032), PIERCE(1) residual 0 at the centre (A249: 0), coverable area 2.736 (A249: 2.733).
* The direct region search (A237/A248 `external248.pocket`, A249's numbers): one square fits with gap +0.209, two
  fail at −0.142, three at −0.186 — consistent with capacity 1 at this ring, and with capacity ≤ 2 as the family
  statement.
* Lemma GAP and Lemma MID-NOTCH hold on every family sample the ladder produces (`analytic251.family_checks`);
  0 violations.
* The FAMILY-WIDE search (`joint251`, detached at exit): ring + k free squares as ONE SAT problem in 16 + 3k
  coordinates per side, k = 1, 2, 3, and `--mode far` for max |q − O| — the number Lemma CENTRE-DISC needs.  Rows land
  in `results/joint251.json` / `results/pocket251.md`; the placeholders {FIT3} / {FAR} in §0, the registry row, the LOG
  entry and the ledger note are replaced by the follow-up (resume block
  `attempts/A251-ring-pocket/notes/ring_pocket.md`).

## 5. What is proved, what remains, n-generality (task 5)

* **[T]** the parametrisation and Lemma GAP; the core construction and the soundness of the box-valid pocket
  over-approximation; Lemma INRADIUS; Lemma THREE-DISC; the corollary CENTRE-DISC ⟹ capacity ≤ 2; Lemma MID-NOTCH
  (both forms).  All n-free: GAP and MID-NOTCH use only "two touchers per wall, both reaching past s − 2" and s < 4;
  INRADIUS / THREE-DISC / the corollary are statements about unit squares in any region.
* **[T-computed]** the ŝ witness's pocket (PIERCE(1) and PIERCE(2) residual 0, area bound 2.736 < 3) and the shrink
  tolerances; the family-wide SAT rows when the ladder finishes.
* **[F as a route]** the box-valid certificate over the family: 3.9 × 10¹⁸ boxes ≈ 5 × 10¹⁴ CPU-h.  Stopped at the
  design, with the numbers, as the brief directs.
* **Plainly: RING-POCKET(11) is [C]** — certified at the witness and (pending the ladder) [T-computed] on the sampled
  family, not proved.  **The family-stuck existence obligation on the window is NOT closed**: it needs (a)
  CENTRE-DISC for the all-ADJ ring — §3.5's corner wedge and vertex sectors — and (b) the non-ring residue A249 §3.4
  leaves, namely mixed type-F / type-T rings with ≤ 3 type-F corners drawing free supply, and any family-stuck
  structure whose corner meeters do not all touch their walls.  k0_00 unchanged.
* n = 11 corollary: 8 ring squares + capacity ≤ 2 = 10 < 11.  n-general: the same argument excludes an all-ADJ ring
  skeleton for every n ≤ 8 + capacity, with capacity from CENTRE-DISC's radius.
* Lean `Statements/Open/RingPocket.lean` (build + `lean/audit.py`, 0 sorry): axioms `unit_square_inball`,
  `three_disc`, `mid_notch_wall` [T-prose], `centre_disc_ring` [T-computed], `ring_pocket_eleven`,
  `family_stuck_non_ring` [C]; theorems `inradius_sep`, `capacity_le_two_of_centre_disc`,
  `family_stuck_eleven_of_ring_pocket`.  Obligations: O-CENTRE-DISC (the radius bound over the family),
  O-CORNER-WEDGE (§3.5), O-THREE-DISC / O-INRADIUS (in Lean over `sqSet`).
* Reproduce: `bash attempts/A251-ring-pocket/code/run251.sh test|analytic|joint|far|tol|pilot|summary|pages|ladder`
  (test 3 min; analytic 1 min; joint hours per side; tol 5 min per ring; pilot 200 boxes ≈ 2 min; `logs/STOP`,
  per-side / per-k checkpoints in `results/*.json`).
