# Drain-flow for k0_00: Theorem DF-K0, its three obligations, and what H1 really is — A87, 2026-09-03

Target (A87 BRIEF, PI redirect after A85): replace the k0_00 VOLUME tree (`k0_route.md`, 45–100
desktop-days) by a drain-flow / downward-induction argument whose sole obligation is a global
Fritz-John exclusion H1 ("no k0 configuration with s < ŝ is FJ-critical"), motivated by A85's
critical-point search (262 k0 optima, none below ŝ, all under-contacted). This file states DF-K0 at
drain-v3 rigour, discharges or voids its three obligations (a)/(b)/(c), identifies H1 exactly, and
records why H1 is not cheaper than the tree. Labels: [T] proved, [S] routine given cited items,
[M] measured, [F] finding, [C] open. Companions: `drain_lemma.md` v3 (D1, D2, D3′, T3, Gordan form),
`structure_lemmas.md` (L1–L7), `k0_route.md` (A85's tree, §9 re-split), `unique_transfer.md` /
`Composition.lean` (A86: `StratumKillMin`, both consumers proved), A30 (`attempts/A30-t3-pilot/`,
the T3 pilot), A76 (`grain_discharge.md`, the structure-lattice wall). Pilot: `attempts/A87-drain-flow/`.

## 0. Verdict

> **DF-K0 HOLDS — and it is two lines, not a flow.** In the selected (minimiser-only) form of
> `stratum_kill` that A85 §9 wrote and A86 composed in Lean (`StratumKillMin`, `Composition.lean`
> 159–204), the k0_00 obligation reads "no global σ-minimiser lies in k0_00 at any side of the
> window (and none at ŝ)". A global minimiser exists (D1) and is a Fritz-John point of every
> selection consistent with it (D3′). So **H1(ŝ) ⇒ the k0_00 instance of `StratumKillMin`**,
> with no hypothesis on the other strata, no induction on 11 − k, no selection, and at every side
> of the window at once. The brief's obligations: **(a)** the drain step exists in its
> qualitative first-order form (Gordan direction, Lemma DS) and is NOT NEEDED — attainment (D1)
> is the terminal point of every drain; the quantitative form ("a contact forms within bounded
> motion") is false as a mechanism and unnecessary. **(b)** is VOID: the k ≥ 1 strata are
> codimension-3 subvarieties (a square exactly on a corner slot: two centre equations and one tilt
> equation), a continuous s-nonincreasing motion from a k0 configuration reaches them with
> probability zero, so there is no "drain exit → higher stratum" map; the only k-raising mechanism
> in the lab is the discrete teleport (CC-2, `teleport_packing`), whose well-founded induction is
> `unique_via_chain` (Lean, A78) — and the lower bound needs neither. **(c)** is VOID: for a global
> minimiser "stuck but non-critical" cannot occur (D3′ holds for EVERY consistent selection,
> stuckness or not); the selection of B.SEL enters only the ∀-packings uniqueness at ŝ, which the
> split composition replaces by "every packing at ŝ is a minimiser".
>
> **H1 IS T3.** H1 is exactly `drain_lemma.md`'s T3 exclusion program restricted to k0 — and the
> restriction prunes NOTHING at cell level (k0 is open and dense; a cell either contains no
> feasible point or contains k0 points). A30's verdict on T3 as a coordinate-cell cover therefore
> applies verbatim: the first-order test is exact for the GRADIENT HULL of a cell (Gordan), so it
> fires only at the discharge scale h* set by the contact geometry (A30: h* ≈ 10⁻³ on a generic
> non-critical cell at s = 3.9, D2 reach 0.015·(s₀ − s*) = 0 at s*), and the number of cells is the
> 33-dimensional volume at that scale (10⁶³ at h = 10⁻², 10¹⁰⁶ at 5·10⁻⁴), NOT the size of the
> critical set. The measure-zero critical set is the wrong complexity measure: a certificate
> "no FJ point in B" has to be checked on all of B. The PI's expectation "most boxes exclude
> immediately by an s-gradient-nonzero argument" confuses "∀ z ∈ B ∃ descent direction" (true,
> cheap to state) with "∃ one direction feasible on all of B" (what an interval certificate needs;
> false on coarse boxes, whose selection menus are full). Measured on k0 cells in §5.
>
> **Route for k0_00: A85's tree stands** (45–100 desktop-days at f₂ ≈ 0.85). What DF-K0 buys:
> the k0_00 obligation is legitimately MinForm, so every minimiser-only rule — D2 slack (b),
> Gordan/Farkas (c1), K0-ROT rotation descent, CC-2′ crowd rows — is an admissible (C)-type leaf
> in the tree (Lemma F-LEAF, §4), and an FJ certificate is window-complete by construction (s is a
> variable of the system). Neither changes the price: at the residue those leaves are dominated
> by the (D)/(D′) value boxes already in place; their niche is a residue chain landing on an
> UNKNOWN structure at side < s₀ + 1.6·10⁻³, where the Farkas test decides "not a minimiser"
> without a certified value box.

## 1. Setting

As in `drain_lemma.md` v3: configurations z = (c_i, θ_i)_{i ≤ 11} (t = tan(θ/2) when a polynomial
form is wanted), D₀ = feasible configurations with the min corner at the origin, σ(z) = side of the
minimal enclosing axis-aligned square, m = min σ (attained, D1, Lean `attained_thm`). Selections S,
NLP(S) = {min s : containment rows q ∈ [0, s], S's separation + dominance rows ≥ 0}, S-feasible ⇒
interior-disjoint, every z ∈ D₀ is S-feasible for some consistent S (D3′ (ii)). FJ at (z, s) for
NLP(S): λ₀ ≥ 0, λ ≥ 0, λ₀ + Σλ = 1, λ₀∇s = Σ λ_k ∇g_k, λ_k g_k = 0 (v3 sign).

Strata. `Census.lean`: `skeleton s z` = the Young-form pin set; a cell is a skeleton cell iff its
whole down-set — the corner slot (c, 0, 0) included — is occupied by squares sitting EXACTLY on
the corner grid (`IsSkelCell`, `Occupied`, `OccupiesSlot q c ↔ q.set = slotSet c`). Hence

**[T] k0_00 ⟺ no square of z is exactly a corner slot square** (axis-aligned, centre at
(½, ½) or its D4 images). Its complement in configuration space is the union over 11 squares and
4 corners of {c_i = slot, θ_i ≡ 0 mod π/2}: a closed semi-algebraic set of **codimension 3**.
k0_00 is open and dense in D₀ (and in every stratum's closure). [S: from the definitions.]

Critical set. C_k0(s̄) := {z ∈ D₀ ∩ k0_00 : σ(z) ≤ s̄ and (z, σ(z)) is FJ for NLP(S) for every
consistent S}. (The "for every" is what D3′ delivers at a minimiser; a certificate may refute
ANY one consistent selection per point, §3.3.)

**H1(s̄):** C_k0(s̄) = ∅. The brief's H1 is H1(ŝ⁻) (σ < ŝ); uniqueness needs H1(ŝ) (σ ≤ ŝ).

## 2. [T] Theorem DF-K0

**Theorem DF-K0.** (i) If H1(ŝ⁻) holds, every global σ-minimiser z* with skeleton ∅ has σ(z*) ≥ ŝ.
(ii) If H1(ŝ) holds, then `StratumKillMin {k0_00}` holds: for every s ∈ wnd and every packing z at
side s that attains s(11), z ∉ k0_00. Consequently, with AllForm = the other non-Trump classes
(their trees) and MinForm = {k0_00}, `s_eleven_ge_of_split` and `s_eleven_unique_of_split`
(`Composition.lean`) give s(11) = ŝ and uniqueness.

*Proof.* (i) Let z* attain m = min σ (D1). If m < ŝ and skeleton(z*) = ∅, then for every selection
S consistent with z*, (z*, m) is a global minimiser of NLP(S) (S-feasible ⊆ D₀, z* ∈ S-feasible,
and s ≥ σ(z) ≥ m on the S-feasible set), hence an FJ point (D3′, F. John 1948, no CQ). So
z* ∈ C_k0(ŝ⁻), contradicting H1(ŝ⁻). (ii) A packing z at side s ∈ wnd attaining s(11) is a global
σ-minimiser with σ(z) = s ≤ ŝ (Trump packs at ŝ). If z ∈ k0_00 then, as in (i), z ∈ C_k0(ŝ),
contradicting H1(ŝ). The two consumers are theorems of `Composition.lean` (A86) taking exactly
`StratumKillAll AllForm` and `StratumKillMin MinForm` with `hpart` the partition. ∎

Remarks. (1) No hypothesis "every k ≥ 1 stratum is excluded below ŝ" is used INSIDE DF-K0; the
other classes enter only through the composition, as always. (2) No induction on 11 − k. (3) The
window is covered at once: H1(ŝ) is a statement about σ ≤ ŝ, and the minimiser's side is whatever
it is. (4) Exactness of the stratum is used nowhere (the class hypothesis is only "skeleton = ∅",
and H1 is stated on the closure-blind set C_k0 — a certificate of H1 on a cell never has to decide
k0 membership: see §3.1).

## 3. The three obligations

### 3.1 (a) Drain step — [T] qualitative, [F] quantitative form void

**Lemma DS (first-order drain step).** Let z ∈ D₀, S a consistent selection, and suppose (z, σ(z))
is NOT an FJ point of NLP(S). Then there are y ∈ ℝ³⁴ with y_s := ∇s·y < 0 and ε₀ > 0 such that for
0 < ε < ε₀: z + εy (configuration part) is a packing at side σ(z) + ε y_s, hence
σ(z + εy) ≤ σ(z) − ε|y_s|.

*Proof.* Gordan's alternative for the active rows A(z) of NLP(S) at (z, σ(z)): either FJ
multipliers exist (excluded) or there is y with ∇s·y < 0 and ∇g_k·y > 0 for all k ∈ A(z) (the
exact first-order dichotomy of `drain_lemma.md` T3(c1), λ₀ = 0 branch included). Along z + εy,
active rows are ε∇g_k·y + O(ε²) > 0, inactive rows stay > 0 by continuity, so all S rows hold ⇒
interior-disjoint (soundness of S); for an active containment row g = s − q, ∇g·y = y_s − ∇q·y > 0
gives q(z + εy) ≤ σ(z) + ε y_s + O(ε²) — the extreme corner retreats faster than the side shrinks —
and inactive containment rows hold by continuity. ∎

What the brief asked beyond this — "s drops by a definite amount OR a contact forms within bounded
motion" — is NOT available and NOT needed. Not available: ε₀ depends on second-order terms and the
inactive margins at z; along a piecewise flow (re-select when a new row activates) the steps can
shrink geometrically and the flow can asymptote to a limit point WITHOUT forming a new contact or
descending a definite amount (feasible-direction methods jam — Zoutendijk's classical failure; a
Topkis–Veinott-type step rule repairs it for the algorithm, but the argument then IS an
attainment/compactness argument). Not needed: the terminal object of every drain is a global
σ-minimiser, whose existence is D1 (compactness in 34 coordinates, Lean `attained_thm`), and D3′
says it is FJ for every consistent selection. The drain-flow picture is a heuristic reading of
"D1 + D3′"; DF-K0 uses the theorems, not the picture. D2 (centroid shrink) is the special case of
Lemma DS with y = uniform contraction about the container centre (valid when all pair rows are
slack: their gradients need not be beaten); it is a leaf rule, not a flow step.

### 3.2 (b) Exit well-foundedness — [F] VOID; the correct well-foundedness is the teleport chain

The exit map "drain exit → which stratum" does not exist. A k ≥ 1 stratum is contained in
{some square is exactly a corner slot square}: codimension 3 (§1). A drain from a k0 configuration
is a curve in the open dense set k0_00; it meets a codimension-3 set only non-generically, and a
descent direction has no reason to seek it (nothing in NLP(S) rewards axis-alignment at a slot).
The stratum boundary reached by draining is therefore NOT a higher stratum; draining stays in k0
and ends (§3.1) at a k0 FJ point — which is what H1 excludes. In particular there is nothing to
induct on: the "downward induction on 11 − k, base = the killed strata" is not how the lower bound
composes. Two true statements replace it:

* [T, Lean] `unique_via_chain` (A78, `UniqueChain.lean`): strong induction on 11 − k with the
  DISCRETE teleport (CC-2: a corner box met by ≤ 1 square is exchanged for the slot square at the
  SAME side, `teleport_packing`) reaching a teleport-stuck packing, then Theorem U collapses back.
  This is a jump, not a flow; k rises by ≥ 1 per step; it serves the ∀-packings uniqueness at ŝ.
* [T] For the LOWER BOUND no induction is needed at all: the attained minimiser lies in exactly
  one class (`stratify`), each class supplies its kill in its own form (All or Min), and DF-K0 is
  the k0_00 kill in Min form — independent of the others.

The brief's "s′ ≤ s (draining never increases s)" is true and irrelevant: the minimiser's side is
the minimum; nothing drains below it.

### 3.3 (c) Selection compatibility — [F] VOID in MinForm; the ∃-selection weakening is a no-op

For a GLOBAL minimiser z*, D3′ gives FJ for EVERY selection consistent with z* — slide-stuck,
teleport-stuck, k-maximal or not. "Stuck but non-critical" is impossible for z*. For a
non-minimiser, stuckness (CC-2′: every corner box doubly met; A71 `stuck_rows.md`) says nothing
about criticality and need not: the MinForm obligation quantifies over minimisers only. The B.SEL
selection (k-maximal representative) enters the top level only through `unique_via_chain` for the
∀-packings uniqueness clause; `s_eleven_unique_of_split` replaces that by "every packing at ŝ is a
σ-minimiser once s(11) = ŝ is known" and re-uses `StratumKillMin` at s = ŝ — hence H1 must hold at
σ = ŝ, not only below (Theorem DF-K0 (ii)).

A possible weakening of H1 — "for each z there EXISTS a consistent S with FJ(S) failing" (D3′ gives
∀S at a minimiser, so refuting one S per point suffices) — buys nothing on a cell: a cell around
a flush tie contains near-tie points on both sides, each consistent with exactly one of the two
tied selections, so both selections must be refuted anyway (A30's "union form blocked at flush
ties"; the per-selection sweep handles it at 2 ms/selection). Recorded so it is not re-proposed.

## 4. [T] Lemma F-LEAF — minimiser-only leaves in the k0_00 zone-tree (the honest partial)

Because the k0_00 obligation is MinForm (Theorem DF-K0 (ii) is the same statement whichever
route certifies it), a zone-tree for k0_00 (`k0_route.md` §6 route 2, Lemma P-TREE with k_S = 0)
may use, besides (K)/(C)/(T)/(D)/(D′), any leaf that excludes only σ-MINIMISERS:

* **(F) Farkas leaf:** all 11 squares localised in P-boxes B (the tree's F-boxes pulled back
  by 1/λ over λ ∈ [1, λ_max], as in K0-ROT (iv)), s-box [σ_min(B), ŝ_hi] with ŝ_hi a rational
  upper enclosure of ŝ; the leaf certifies, for every straddling selection of B's menu, an
  interval-verified direction y with ∇s·y < 0 and ∇g·y > 0 on B (T3(c1)). Then B contains no FJ
  point of any consistent selection with σ ≤ ŝ, hence no global minimiser (D3′).
* **(B) slack leaf:** D2 on B (min pairwise gap > 0 uniformly): no minimiser.
* **(R) rotation-descent leaf:** K0-ROT (v): σ(R_φ z) < σ(z) on B for a rational rotation.
* **(S) stuck-row leaf:** a CC-2′ 2-crowd row violated on B (A71 SR-1/SR-2), since a
  σ-minimiser can be taken teleport-stuck — NOTE this one needs the k-MAXIMAL minimiser, i.e.
  the B.SEL representative; it is admissible only if the Lean consumer is fed the k-maximal
  minimiser (it is: `stratify` picks it), and it must not be mixed with (F)/(B)/(R) claims that
  quantify over all minimisers unless both hold — keep (S) leaves flagged.

*Soundness.* Lemma P-TREE's Step 3 (leaf verdict ⇒ no packing reaches the leaf) becomes "no
σ-minimising packing reaches the leaf"; the composition `classKilledAt_of_tree` is then consumed
through `StratumKillMin` instead of `StratumKillAll` (A86: both consumers proved). The (D) leaves
(tube) already give the equality clause. ∎

*Value [F].* At the tree's residue (all 11 squares localised at the landing scale 1.6·10⁻³, or
5·10⁻³ at a ghost) the (D)/(D′) value boxes are STRONGER (∀-packings) and cheaper (one certificate
per box vs. one Farkas cell per (r/h*)³³ sub-cells, §5); (F) is worth having only where no value
box exists — a residue chain contracting onto a structure unknown to A37/A85 at side
< s₀ + 1.6·10⁻³ — where it decides "not a minimiser" from first-order data alone. Lean-readiness:
(R) needs no derivative; (F) needs interval gradients of rows that are rational in t
(A76's t-native exact kernel, `verify_grain.py`, has them). Not priced into the route; [C] optional.

## 5. [M] H1 as a certificate: what the pilot measured (`attempts/A87-drain-flow/`)

Engine: A30's `t3lib.py` (copied), s-box clipped to s₀ = 969271/250000, cells of half-width h in all
33 coordinates; verdicts (a) interval-infeasible, (a-σ) σ_min(cell) > s₀, (a-menu) empty selection
menu, (b) D2 slack, (c1) union Gordan/Farkas, (c1-sweep) per-selection Farkas, alive.
Reference points: the 262 k0 optima of `cp85_k0_search.json` (Δ := σ − s₀ ∈ [0.0101, 1.12];
contacts min 3 / median 11 / max 24 counting walls; n_axis_aligned 0 for 25 of them), Trump
rotated by 10⁻³ and by 5·10⁻⁸ (a genuine k0 packing at side ≤ s₀).

Selftest 7/7 (corruption gates). Full tables: `notes/pilot_report.md`, `results/j1_ladder.jsonl`,
`j2_survey.jsonl`, `j2_summary.json`, `j3_degeneracy.json`, `j4_projection.json`.

**5.1 Per-cell cost** (single process, BLAS pinned): build_cell + clip 0.015 s; (a)+(b) 0.115 s;
menu 0.63 s; union Farkas LP 0.06 s; **cheap path 0.80 s**; per-selection Farkas 2.5 ms
(69 000 selections); a capped sweep cell (3 000 selections) 8.2 s. One A85 LP node (1 700 s) =
2 100 cheap cells — the answer to (i), per cell; per VOLUME see §6.

**5.2 h*(Δ) ladder (J1).** h ∈ {0.05 … 10⁻⁴}; `.` alive, A-σ = σ_min(cell) > s₀.

| cfg | σ | Δ = σ − s₀ | contacts | 0.05 | 0.02 | 0.01 | 0.005 | ≤ 0.002 |
|---|---|---|---|---|---|---|---|---|
| r1 best k0 optimum | 3.887213 | 1.01·10⁻² | 13 | . | . | . | A-σ | A-σ |
| r2 no axis-aligned square | 3.905653 | 2.86·10⁻² | 8 | . | . | A-σ | A-σ | A-σ |
| r3 / r4 / r5 (σ ≈ 3.956 / 4.000 / 4.243) | | 0.079 / 0.123 / 0.366 | 15 / 7 / 9 | A-σ | A-σ | A-σ | A-σ | A-σ |
| r6 Trump rotated 10⁻³ | 3.880959 | 3.87·10⁻³ | — | . | . | . | . | A-σ (h ≤ 0.002) |
| r7 Trump rotated 5·10⁻⁸ (ghost, σ ≤ s₀) | 3.877084 | −2.2·10⁻⁷ | — | . | . | . | . | . down to h = 10⁻⁸ |

h*/Δ (largest excluded h over Δ): 0.49, 0.35, 0.63, 0.41, 0.14, 0.52 — every exclusion is (a-σ),
i.e. L ≈ 2–3; NO cell of any configuration was ever excluded by (a), (a-menu), (b) or (c1); the
capped per-selection sweeps at the largest alive h: 3 000/3 000 alive for r1, r2, r6, r7 (menus
2¹⁶–2³⁴). r7 (a genuine k0 packing at side ≤ s₀, 2·10⁻⁷ from ẑ) stays alive at h = 10⁻⁸: the x-wall
rows (X = σ − 4·10⁻⁸) straddle activity at every tested h, so the un-rotation direction cannot be
certified — the Trump shell of §6.3 in vivo.

**5.3 Near-feasible survey (J2): 262 optima × h ∈ {0.05, 0.02, 0.01, 0.005, 0.002} + 70 offset
cells = 1 380 cells.** Verdicts: a-σ 1 306, alive 74, **(a)/(a-menu)/(b)/(c1-union): 0**. By h:
alive 31 / 27 / 16 / 0 / 0 (h = 0.05 … 0.002). By Δ-bin: [0.01, 0.02) 40 alive of 92;
[0.02, 0.05) 26 of 55; [0.05, 0.1) 8 of 48; Δ ≥ 0.1: 0 of 1 185. **The PI's key number — cells
with σ_min ≤ s₀ excluded with no FJ solve — is 0 of 74 (0.0 %) at every h.** h*/Δ over the 262:
median 0.41 (censored at the ladder top for 245; uncensored n = 17: median 0.47, range 0.35–0.50),
reason a-σ in all 262 cases. Offset cells (±h/2, 14 optima with σ < 3.9): 30 alive / 40 a-σ.

**5.4 Degeneracy at the 14 optima with σ < 3.9 and r6 (J3).** Active rows at the point
(|g| ≤ 10⁻⁶, first consistent selection per contact pair): m = 19–27, gradient rank 17–22, flat
dimension on the 33 configuration coordinates 10–16, rattlers 1–4 (0 for r6). **FJ multipliers
INFEASIBLE at 13 of 14 optima and at r6** (max-min-λ LP, λ₀ = 0 branch also infeasible); feasible
only at o012 (σ = 3.897, 27 rows, rank 22, with a λ₀ = 0 self-stress). Krawczyk in complementarity
form is moot where FJ is infeasible; at h = 10⁻³ every one of the 15 cells is a-σ; at the smallest
non-a-σ h (0.01–0.02) all are alive with 3 000/3 000 selections alive.

**[F] The under-contacted k0 "optima" are, with the sampled selections, NOT Fritz-John points.**
A04/A85's optimiser (penalty continuation + SLSQP on an active set thresholded at 2·10⁻³) stops at
first-order points of the PENALISED problem; with 19–24 active rows of rank 17–22 and e_s outside
their cone, Gordan gives a strict descent direction at 13 of the 14 lowest ones. So the premise
"the k0 critical set is a union of under-contacted manifolds at s ≥ ŝ + 0.0101" is unsupported by
the census that motivated it: those points are under-contacted BECAUSE they are not critical, and
the true k0 FJ points (where the drains of these points end) are unknown — possibly lower. This
does not touch DF-K0 (which quantifies over the true minimiser) but removes the empirical comfort
behind H1. Caveat: a corner–corner tie admits several consistent selections and only one was
sampled per pair; FJ feasibility for a different tie selection is not excluded — the sweeps at
the alive cells (all selections alive) do not resolve this either way. [C] re-run A85's CP search
with an FJ-polish (Newton on the active-set FJ system, A30 `polish`) to find the genuine k0
critical points and their sides; ~1 desktop-hour.

**5.5 Projection (J4).** Uniform 33-dim cover of D₀ / (8·11!): 10³⁹·⁶ cells at h = 0.05, 10⁶²·⁷ at
10⁻², 10⁹⁵·⁷ at 10⁻³ (A30: 10⁶³ / 10¹⁰⁶ / 10¹²¹ at 10⁻² / 5·10⁻⁴ / 1.75·10⁻⁴). One A85 landing box
(radius 1.6·10⁻³) needs 10⁶·⁷ cells at h = 10⁻³ (10³ CPU-h cheap path, 10⁴ with sweeps), 10³¹·⁷ at
1.75·10⁻⁴; one ghost drain box (5·10⁻³): 10²³ cells at 10⁻³. And no measured h excludes a
σ-feasible cell at all, so these are the costs of a test that returns "alive".

## 6. [T+M] Why H1 is not cheaper than the tree (the price)

1. **Locality.** Gordan is exact for the interval hull of the gradients on a cell: the union
   Farkas LP is infeasible iff FJ multipliers exist for SOME gradient tuple in the hull. On a
   coarse cell the hull contains tuples of a jammed configuration (the same contacts can be
   active anywhere in the cell), so ε = 0 identically (A30 P3, h = 10⁻²: 18 straddling pairs,
   menu 4·10⁸, 60 000 selections, 0 killed; h = 10⁻³: 44 % of 32 768 selections killed; h ≤
   3·10⁻⁴: D2). The discharge scale is h* ~ gap / L (L = the row Lipschitz constant ≈ 2–4), i.e.
   the slack of the configuration, which at the window's top is ZERO (D2 reach 0.015·(s₀ − s*)).
2. **Dimension.** An LP node of A85's tree localises ONE square (3 coordinates, half-width 0.026
   at depth 2) and kills the remaining 30-dimensional factor by counting; an FJ cell must
   localise all 33 coordinates. The cover count is (volume)/(2h*)³³ — A30's 10⁶³ at h = 10⁻²,
   10¹⁰⁶ at 5·10⁻⁴, before the /8·11! quotient; after it (§5.5) 10³⁹·⁶ / 10⁶²·⁷ / 10⁹⁵·⁷ at
   h = 0.05 / 10⁻² / 10⁻³, and the measured h* on σ-feasible k0 cells is NONE. Per-cell cost
   0.5 s (cheap path) is 3 400× cheaper than an LP node; the cell count is 10⁶⁰× larger.
3. **Critical points.** The only FJ points with σ ≤ s₀ are (conjecturally) the eight Trump images
   (not k0). Around each, cells of half-width h within δ_kill = c·h (c ∈ [1.15, 3.75] measured,
   scale-invariant, A30 X) survive and must be discharged by the basin (A36, stratum-blind,
   σ ≥ ŝ with equality only at ẑ ⇒ no k0 point with σ ≤ ŝ in the box): the cell grid must be
   aligned with the basin box and refined to h ≤ r_B/(c − 1) so that every cell outside it is at
   distance ≥ c·h — the endgame shell of A30 (7.8·10⁸ cells per image at h = 1.75·10⁻⁴ with A22's
   r_N; fewer with A36's r_B = 3/2000 but the count is set by c³³, not by r_B). And the
   certificate must be stated at σ ≤ ŝ (an algebraic enclosure), NOT at s₀: at s₀ the rotational
   ghosts R_φ ẑ, |φ| ≤ 1.06·10⁻⁷, are genuine k0 packings at side ≤ s₀ (K0-ROT §5.2), not FJ, but
   at distance 2·10⁻⁷ from ẑ — no cell containing ẑ can be Farkas-killed, and cells small enough
   to separate them are absurd. At ŝ_hi with A22's 10⁻⁵⁰ enclosure the ghosts with σ ≤ ŝ_hi lie
   within 6·10⁻⁵¹ of ẑ, inside every basin box.
4. **The under-contacted optima** (the PI's "critical manifolds"): FJ points with m active rows
   are generically ISOLATED modulo rattlers (stationarity is 34 equations in the m + 1
   multipliers; e_s ∈ span of the active gradients is a codimension-(34 − m) condition on z;
   a square with no active row contributes three 0 = 0 rows, so the FJ set has dimension
   3 × #rattlers plus any dependency among the loaded rows). They sit at Δ ≥ 0.0101 above s₀:
   a cell of half-width h around one is killed by (a-σ) as soon as L·h < Δ (measured
   h* = Δ/2.15, §5.2–5.3 — a pure s-clip effect, no FJ content), by
   A37/A85 3S value boxes at h = 5·10⁻³ (A86 replayed 12 of them), and along a rattler's range
   the cover is (range/h)³ cells per rattler — a nuisance, not a wall. Their FJ Jacobian in the
   complementarity form is singular (multiplier polytope of positive dimension, A30 P1/P3), which
   kills Krawczyk-on-FJ but is irrelevant to the Farkas/(a) route — and §5.4 says most of them are
   not FJ points at all with the sampled selections (13 of 14 below 3.9; FJ infeasible).
5. **Structure branching** (A30's own recommendation: branch on contact graphs, one global
   algebraic FJ solve per structure, no coordinate cells) removes the c³³ factor but replaces it by
   the structure count and by global root isolation of 34-variable polynomial systems: A76
   measured the grain lattice of ONE pinned class inside a box of radius 10⁻² around Trump at
   1.7·10⁷ grains, with 13 702 hard grains among the 143 370 of codimension ≤ 4, and certified NO
   radius beyond A22/A36/A40 (`grain_discharge.md`). The global k0 structure lattice (no pins,
   all of D₀) is unpriced and larger by orders of magnitude; the per-structure global solve is a
   Bézout-sized homotopy (degree ≤ 4 rows, 34 unknowns). Not a route within the lab's horizon.

**Price.** H1 as a coordinate-cell cover: 10⁶²·⁷ cells × 0.8 s ≈ 10⁵⁹ CPU-h at h = 10⁻² — and
at that h no σ-feasible k0 cell is excluded, so the true figure is worse (h* undefined: 0 of 74
σ-feasible cells killed at any h ≥ 0.01; below that every k0 cell in the census is a-σ, i.e.
"not at side ≤ s₀" — the trivial part). Even ONE A85 landing box costs 10³ CPU-h at h = 10⁻³
without being discharged. H1 by structure: unpriced, ≥ A76's wall. Against A85's 3 200–7 000
CPU-h (45–100 desktop-days) the comparison is not close: **H1 is its own, astronomically more
expensive, tree.** A85's tree remains k0_00's route.
The k ≤ 3 classes of the tier inherit nothing from H1 (same locality), but they DO inherit the
MinForm observation: any protected class may be moved to MinForm and use Lemma F-LEAF's leaves.

## 7. Obligations ledger

| # | obligation | status |
|---|---|---|
| DF-O1 | D1 attainment | LEAN (`attained_thm`, A68) |
| DF-O2 | D3′ FJ necessity per consistent selection, v3 sign | PROSE (drain_lemma.md), standard |
| DF-O3 | `StratumKillMin` consumers | LEAN (`s_eleven_ge_of_split`, `s_eleven_unique_of_split`, A86) |
| DF-O4 | H1(ŝ): C_k0(ŝ) = ∅ | OPEN — equals T3 restricted to k0; not affordable as a cover (§6); k0_00 stays on A85's tree |
| DF-O5 | (a) quantitative drain / (b) exit map / (c) stuck-non-critical | VOID (§3): not needed; (b)'s map does not exist (codim-3 strata) |
| DF-O6 | Lemma F-LEAF Lean form ((R) no derivative; (F) t-native interval gradients) | [C] optional, no price effect |
