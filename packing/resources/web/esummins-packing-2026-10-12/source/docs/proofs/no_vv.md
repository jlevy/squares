# Lemma NO-VV — loaded vertex-on-vertex contacts between non-parallel squares at a minimiser: the exact statement, what is a theorem, and the exact obstruction — A235, 2026-09-15

The PI (2026-09-15, 20:20): *"if you epsilon-perturb ALL the dimensions and let it relax, the point-on-point configuration
won't survive; point-on-side is absolutely valid — the expected way torque is applied to stabilise rotation."*  The coordinator's
probe (20:30, A217's witnesses): a LOADED vertex-on-vertex contact between non-parallel squares occurs at NONE of the ~700 loaded
contacts of the 117 genuine Fritz-John points kept in `witnesses217.jsonl`, but at 26 / 184 HELD configurations and 6 / 185 CROWD
four-crowds — the ring's lean 4|6 (70° on 20°) is one.  This file states the lemma exactly for every n, proves what is a theorem,
names the obstruction, and tests every step.  Tags: [T] proved, [S] routine, [M] measured, [F] false with the witness, [C]
obligation.  Sources: `wall_torque.md` §5 (Lemma STRUT, Theorem SO), `local_certificate.md` (Lemma SAT, STAB), `drain_lemma.md`
(D1, D3′), `local_lock.md` §3 (NO-SELF-STRESS), `contact_census.md`.  Code `attempts/A235-no-vv/code/` (`vv235.py` census +
two-selection test, `select235.py` every consistent selection, `roll235.py` the rolling plane, `local235.py` Theorem SO with
A219's candidates, `test235.py`, `pages235.py`), results `results/novv235.md` (+ `census235.jsonl`, `novv235.jsonl`,
`select235.jsonl`, `local235.jsonl`), page `docs/residue_map/campaigns/A235-no-vv/ring_vv_4_6.svg`, Lean
`Statements/Open/NoVV.lean` (two theorems, no new axiom).

## 0. Verdict

> **[T] NO-VV is a theorem exactly in the PI's sense — for a contact whose row is independent of the other active rows (the
> "epsilon-perturbed", LICQ situation): the two-selection principle (a minimiser is a local minimum of NLP(S_A) AND of NLP(S_B),
> because the feasible set near a VV contact is the UNION {g_A ≥ 0} ∪ {g_B ≥ 0}, a reflex corner, not the intersection) forces the
> contact force to be zero (Corollary NO-VV-IND, Lean `no_vv_of_not_mem_span`, `no_vv_pair`).  [F] It is NOT a consequence of local
> optimality in general: at every stuck configuration we have, the VV row lies in the span of the other active rows (82 / 82
> tilted VV contacts; the stuck configurations are over-braced: 26–45 rows per consistent selection against 34 coordinates), and 25 of the 26 HELD
> witnesses with a loaded tilted VV contact are Fritz-John under EVERY consistent selection (2⁷–2¹⁶ enumerated each) and have no
> second-order saddle (Theorem SO, A219's candidates) — the exact obstruction is an OVER-BRACED, TORQUE-LOCKED contact: the loads on
> the two squares are not concurrent at the common vertex, so no rotation about it is a first-order zero mode (Lemma CONCURRENT) and the
> knife-edge of the rolling plane (Lemma KNIFE: the VV rows' curvature along any rolling is −F_P·(c_B − P) < 0) is unreachable — the
> rolling plane is blocked at first order at 48 of the 55 loadable tilted VV contacts, in both selections.  [T]+[M] What the
> two-selection principle DOES exclude at first order: 6 of the 55 contacts — 5 of the 7 CROWD witnesses that carry one, and
> 1 HELD — every exclusion attributable to the VV pair (flipping its axis alone restores FJ).  [M] At the 883 genuine free FJ points,
> Trump, S02, S07 and the 21 survey records (n = 5..55) every tilted VV contact is UNLOADABLE and a VV-free balanced stress exists —
> the PI's claim holds on everything we have — but the local tests do not explain it; the records square-38 / square-40 show that a
> tilted VV contact can be PRESENT (and loadable) at a conjectured optimum: the diamond tips at lattice notches.  Consequences: the
> k5 / k0 trees bound LPs over polyhedra and gain nothing; an FJ census gains the two-selection row test (1 LP per VV pair per leaf,
> bites on 6 / 33 witnesses); four-crowds are not excluded (5 of 185).  k0_00 unchanged.**

## 1. The objects (any n)

**Lemma POINT [T].**  Two unit squares A, B with disjoint interiors and tilts differing by a non-multiple of 90° meet in at most one
point.  *Proof.*  A ∩ B is convex and lies in ∂A ∩ ∂B; two points give a segment in ∂A ∩ ∂B, hence on an edge of each, so the
edges are collinear — parallel squares. ∎  So a contact of non-parallel squares is VE (the point is a vertex of exactly one of
them, in the relative interior of an edge of the other) or VV (a vertex of both); two edge interiors cannot cross at a single point.

**Lemma VV-AXES [T].**  At a VV contact of non-parallel A, B at P, exactly one edge e of A through P and exactly one edge f of B
through P are separating lines, and the pair's tight separating-axis rows (Lemma SAT's g_σ) are exactly
    g_A := n_e·(b − c_A) − ½   (B's vertex b = P against the line of e),   g_B := n_f·(a − c_B) − ½   (A's vertex a = P against f).
*Proof.*  Let A's wedge at P span the directions [α, α + 90°] and B's [β, β + 90°]; disjoint interiors ⟺ β ∈ [α + 90°, α + 270°].
The line of A's edge in direction α separates iff B ⊂ [α + 180°, α + 360°] iff β ∈ [α + 180°, α + 270°]; the line of the edge in
direction α + 90° separates iff β ∈ [α + 90°, α + 180°]; both iff β = α + 180° — parallel, diagonally opposite.  Same for B.  B's
other vertices lie strictly outside the line of e for non-parallel tilts, so no further row of the pair is tight. ∎
(`test235.py`: 400 random VV configurations.)

**Lemma REFLEX [T] (the union).**  Near a VV contact the pair is interior-disjoint iff g_A ≥ 0 OR g_B ≥ 0.  In the plane of the
relative translation u of B's vertex the feasible directions are {n_e·u ≥ 0} ∪ {n_f·u ≤ 0}: a reflex cone of angle
180° + ∠(n_e, −n_f) > 180° whose complement, the overlap wedge, is A's wedge together with the reflected wedge of B; it contains the
full lines along e and along f (the vertices sliding past each other).  *Proof.*  Lemma SAT with only the two axes of VV-AXES able
to be tight. ∎  (Inset of the page: the ring's 4|6 has ∠(n_e, −n_f) = 40°, overlap wedge 140°, feasible cone 220°.)
Both rows are EXACTLY zero along every rotation of A about P and of B about P (P is fixed and lies on the rotating line): the
2-dimensional ROLLING family y(φ) = cos φ·ρ_A + sin φ·ρ_B keeps the VV contact to all orders (`test235.py`, finite rotations).

## 2. Lemma NO-VV — the statement

Setting: NLP(S) as in Theorem SO (`wall_torque.md` §5): rows = walls, one separating axis per touching pair, the external rows of the
problem considered (tilt bound / crowd); FJ multipliers (λ₀, λ) ≥ 0, λ₀ e_s = Σ λ_r ∇g_r; by Lemma NO-SELF-STRESS λ₀ = 1 at every
FJ point of the side problem (`local_lock.md` §3.3).  Two consistent selections contain a VV contact: S_A (axis e) and S_B (axis f),
agreeing elsewhere.  The contact is LOADED in a multiplier when λ_A > 0 (in NLP(S_A)) or λ_B > 0 (in NLP(S_B)); LOADABLE when some
multiplier loads it; NECESSARILY loaded when every multiplier of the corner system (both rows) does.  The parallel case (tilts
equal mod 90°: corner-to-corner lattice coincidences, flush contacts of overlap 0) is EXCLUDED from the lemma: it is a flush contact
with the two rows along one normal (`structure_lemmas.md` Fact 0) and is loaded at the simple packing and at Trump (PAR corner
points: 480 at the SETTLED witnesses).

**Lemma NO-VV (n-general).**  Let z* be a local minimiser of the side over packings (or over any NLP with additional smooth external
rows whose feasible set near z* is the union structure of Lemma REFLEX at the pair) with a VV contact between non-parallel squares
A, B at P.  Then
 (i) [T] (two-selection principle) z* is a Fritz-John point of NLP(S_A) and of NLP(S_B): the contact force at P is realisable
     along n_e alone in one balanced stress and along n_f alone in another (D1 / D3′: F ∩ U = (F_{S_A} ∪ F_{S_B}) ∩ U, a local
     minimum over a union is a local minimum over each part; more generally z* is FJ under EVERY consistent selection);
 (ii) [T] (NO-VV-IND) if ∇g_A ∉ span{∇g_B, ∇g_r : r ∈ R} (R = the other rows of the selection) then λ_A = 0 in every multiplier of
     NLP(S_A), and symmetrically for B; in particular, under LICQ the contact is unloaded — the PI's perturbation claim, exact;
 (iii) [T] (the rolling plane) if the rotation of B about P (either sense, other squares fixed) is a first-order zero mode of NLP(S)
     then every loaded contact force on B passes through P (Lemma CONCURRENT), and along the rolling family the VV rows contribute
     −F_P·(c_B − P) ω_B² − (−F_P)·(c_A − P) ω_A² < 0 to yᵀ∇²L y (Lemma KNIFE; F_P the force on B at P, in the physical cone between
     n_e and −n_f) — Theorem SO's v₂ then decides, and a loaded VV whose rolling is a zero mode is a knife-edge;
 (iv) [F] without (ii)'s hypothesis the conclusion "unloaded" FAILS as a local statement: 25 HELD witnesses (§4).
*Proofs.*  (i) as stated.  (ii) two representations e_s = Σ_R λ_r ∇g_r + λ_A ∇g_A = Σ_R μ_r ∇g_r + λ'_B ∇g_B give
λ_A ∇g_A = Σ_R (μ_r − λ_r) ∇g_r + λ'_B ∇g_B, so λ_A ≠ 0 would put ∇g_A in the span (Lean `no_vv_of_not_mem_span`; no sign condition is
used).  (iii) CONCURRENT: 0 = e_s·y = Σ λ_r ∇g_r·y with every rate ≥ 0 and λ ≥ 0 forces rate 0 on every loaded row, and the rate of a
row of B under rotation about P is ω × (moment of its unit force about P).  KNIFE: along the true rotation both rows are identically
zero, so yᵀ∇²g y = −∇g·z″ with z″ = (−(c_B − P), 0): yᵀ∇²g_A y = n_e·(c_B − P) = h_B > 0 (B's centre is on the outer side of e) and
yᵀ∇²g_B y = −n_f·(c_B − a) = ½; the Lagrangian term is −λ_A h_B − λ_B/2 = −F_P·(c_B − P) (`test235.py` on the ring: h_B = 0.7044).
(iv) §4. ∎

## 3. Route (ii) on the data: the hypothesis never holds at a stuck configuration [M]

At every one of the 82 tilted VV contacts of the census the VV row lies in the span of the other active rows and its partner
(`census235.jsonl`, `gA_in_span`; A217's convention: walls, both axes of every tied pair, line rows, external rows; the full set has
rank 3n + 1 at 61 of 1,393 witnesses).  Per consistent selection (`select235.jsonl`, the 31 HELD / CROWD witnesses with a loadable
tilted VV, 2⁴–2¹⁶ selections each): 26–45 rows against 34 coordinates, redundancy (rows − rank) 0–12; the VV row is independent of the
selection's other rows and its partner in 2,272 selection-instances, ALL at four CROWD witnesses (w125, w134, w135, w142) — exactly
where NO-VV-IND applies, it forces the contact unloaded in those selections, and that is what fails there (§4: the two-selection test
excludes all four).  At the 26 HELD witnesses the VV row is dependent in every selection: the stuck configurations of the bounded
problem are over-braced by construction (flush pairs carry two rows per axis, wall rows meet at the corner squares, triple points), so
the generic case in which NO-VV is a theorem is the case that does not occur there.  At the free FJ points the 12 tilted VV contacts
are unloadable (max over the polytope = 0) for another reason — a VV-free stress exists.

## 4. Route (iii): the rolling plane, the complete local test, the obstruction [M]

For each of the 55 loadable tilted VV contacts (HELD 26 witnesses, CROWD 5), each selection S_A, S_B and the corner system S_AB:
72 directions of the rolling plane (5°), each completed by LP (the other squares move for free, `modes219.complete`), first-order
feasibility by the per-pair best axis, v₂ by Theorem SO's LP, negatives curve-checked (`roll235.py`, 16 s):

| outcome | contacts |
|---|---|
| rolling plane BLOCKED at first order in S_A and in S_B (every φ infeasible) | 48 |
| one selection not Fritz-John at all (EXCL-1, the two-selection test) | 6 (5 CROWD, 1 HELD) |
| feasible rolling directions with v₂ < 0 — but under the direction's own selection, which is not FJ (a first-order exclusion, D3′) | 1 (w323, pair 3|6) |
| verified second-order saddle on the rolling plane | 0 |

What blocks the ring's 4|6 (page): rotation of 6 about P is stopped ccw by 7's corner on 6's edge (the flush 6|7, rate −0.50) and cw
by 6's floor vertex (rate −0.34) and the tilt bound; rotation of 4 is stopped ccw by 4's wall row (loaded, rate −0.34) and its tilt
bound (loaded, 0.166) and cw by 0's and 5's rows.  Lemma CONCURRENT explains the pattern: a loaded square with a wall contact at a
vertex other than P, or a flush partner, cannot roll about P.  A219's strut mode of square 6 is a rotation about the 7-contact, not
about P (v₂ = +0.381 there; the 4|6 vertex leaves 4 at second order) — the PI's objection ("you walked a line in that space that is
technically still balanced") is answered: the whole rolling plane at the contact was tested, and it is not a plane of zero modes.

The complete first-order test (`select235.py`: every consistent selection, exhaustive at 29 / 31 witnesses, 2¹⁴ samples at 2): FJ under
ALL selections at 25 / 26 HELD; NOT FJ at 1 HELD (w323: 512 / 1,024 selections, all those using S_B at the pair 6|10) and at 5 / 5 CROWD
(w125, w134, w135, w142, w153: 8–3,072 failing selections each) — every failure is attributable to the VV pair (flipping its axis
alone restores FJ).  The complete second-order test (`local235.py`: A219's candidates — every square's rotation about every contact
point, both senses, and the eigen-directions of the reduced Hessian — bounded variant): HELD 26 stationary, zero modes at 5, saddles 0;
CROWD 5: not KKT under the mode's selection at 5 / 5 (the same exclusions).  **So 25 HELD witnesses carry a loaded tilted VV contact
(necessarily loaded at 11 of them; no VV-free stress at any) and pass every local necessary condition we can test.**  They are local
optima of the BOUNDED problem (the tilt floor supplies the missing torque), so as a statement about local minimisers of an NLP with
external rows NO-VV is false, and its truth for the free side problem cannot come from first- and second-order conditions at the
contact alone.

## 5. The free problem [M] / [C]

At the 883 genuine free FJ points (SETTLED 470, K0FREE 458, BOXK0 72 incl. duplicates across the two lists), Trump, S02, S07 and the
21 records: tilted VV contacts exist at 6 FJ witnesses (12 contacts, all at side 4.000 with rattlers) and at square-38 (4) and
square-40 (8) — 45° diamonds whose tips sit at the notch between two flat squares, loadable up to 0.71 / 1.00 with both selections
KKT — and at every one of them a balanced stress with all tilted VV rows at zero exists (`vv_free_stress`).  The stress form
    **NO-VV-STRESS(n): at a minimiser some balanced stress is supported on vertex-on-edge and flush contacts only**
holds on all 24 optima and 883 FJ points and is what the PI's claim means for the contact graph (the graph itself may contain a
tilted VV, as square-40 shows).  Why it holds is not local: a HELD survivor becomes a free FJ point exactly when its loaded tilt
bound is replaced by a holder square supplying the same torque — the room for which is what A219's holder search (`ring219.md`) never
found at the witness side.  NO-VV-STRESS for the free problem is therefore [C], entangled with HOLD / RING, not a separate lever.

## 6. Consequences

(a) **The k5 / k0 trees.**  The leaf LP (Lemma LEAF) bounds s over a polyhedron at fixed tilts; nothing there is a stationary point,
so no row pair can be dropped: prune 0 %.  In a Fritz-John CENSUS (Theorem CC (e), A219's structures, A233's row lists) the sound
prune is the two-selection test — at a VV pair the leaf must be FJ under both axes (one extra LP per VV pair per leaf, ~3 ms) — and
NO-VV-IND when the leaf's rows are independent (never, §3).  Bite on the data: 6 of the 33 HELD / CROWD witnesses with a loadable
tilted VV; the 25 survivors are not touched.  One page: `results/novv235.md` §3.
(b) **Four-crowds.**  7 of 185 CROWD witnesses carry a loadable tilted VV, 5 of them are excluded by the two-selection test (they were
among A219's 29 "not FJ under another selection"); the other 178 have none.  NO-VV does not exclude crowds.
(c) **n-general contact graph.**  "Every optimal packing has a balanced stress supported on VE + flush contacts only" is consistent
with all 21 survey records (n = 5..55), Trump, S02, S07 [M]; "the contact graph of an optimal packing has no tilted VV edge" is
FALSE if square-38 / square-40 are optimal (loadable VV edges present, unloaded in some stress).

## 7. Lean, files, obligations

`Statements/Open/NoVV.lean`: `no_vv_of_not_mem_span`, `no_vv_pair` — theorems (the independent-rows core, an abstract module
statement; no axiom), `lake build` + `lean/audit.py` exit 0, no sorry.  Prose [T]: POINT, VV-AXES, REFLEX, the two-selection
principle (D1 / D3′), CONCURRENT, KNIFE.  Obligations: O-VV1 the wedge computation of VV-AXES in Lean over `PSq` (routine); O-VV2
NO-VV-STRESS for the free side problem [C] (§5, with HOLD / RING).  Nothing in `Main.lean` depends on this file.

## Addendum (coordinator, 2026-09-15 22:10) -- composite edges: the PI's correction to s.5

The PI (22:00): "two same-grain aligned squares effectively have a single shared top edge, and if the vertex of
another square lies on the seam, that is not a VV load, it is a VE load (where the E is actually two Vs coincident)."
Re-classifying every vertex-on-vertex contact between non-parallel squares with the symmetric COMPOSITE-EDGE test
(one of the two squares has a parallel neighbour sharing the point with collinear edges through it, so the other
square's vertex sits on a composite edge): the n = 38 and n = 40 records' 12 contacts are ALL vertex-on-composite-
edge (the flush square's corner sits on the boundary line of a 45-degree band, two parallel diamonds' collinear
edges), NOT genuine VV; the survey has 0 genuine VV contacts, SETTLED 0, BOXK0 0, K0FREE 2 (both unloaded, as
NO-VV-IND requires), HELD 17 and CROWD 4 (held configurations).  So the contact-graph form of Lemma NO-VV holds on
every optimal packing we have in the PI's sense: [M] no genuine (isolated, non-composite) vertex-on-vertex contact
between non-parallel squares at any record or settled optimum; loaded genuine VV never.  s.5's "false" refers to
the naive classification only.  Code: the coordinator's probe (attempts/A235-no-vv/code/composite_probe.py).
