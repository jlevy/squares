# The PI's wall-torque limitations, made exact: Lemmas CEIL, TWO-CONTACT, ONE-TILTED, STRUT / Theorem SO, and the test of Lemma RING — A219, 2026-09-14

The PI's three limitations (A219 BRIEF 19:10, addendum 19:30): L1 "WLOG S < ⌈√n⌉"; L2 "squares cannot load along a wall
without a net torque"; L3 "they require squares pushing out from the centre to keep them pinned; the holders have to meet in the
middle in a way that still torque-balances".  This file states each as a lemma (n-general, n = 11 corollary), proves what is a
theorem, says where L2 is false as stated, tests L3 (Lemma RING) on every four-crowd witness A217 found, adds the PI's second-order
test (addendum 2b: Lemma STRUT, Theorem SO) and prices RING as a finite structure question.  Tags: [T] proved, [M] measured, [F]
false, [C] conjecture / obligation.  Code `attempts/A219-wall-torque/code/`, results `results/ring219.{md,jsonl}`,
`second_order219.md`, `second219.jsonl`, `holder219.jsonl`, `structures219.json`; pages `docs/residue_map/campaigns/A219-wall-torque/`;
Lean `Statements/Open/LemmaCEIL.lean`, `TwoContact.lean`, `OneTilted.lean` (built, audited, no sorry).

## 0. Verdict

> **[T] CEIL, TWO-CONTACT, ONE-TILTED are theorems** (§1–3), n-general, one-line to one-paragraph proofs, Lean axiom files with the
> n = 11 corollary `Fits 11 4` proved.  **[F] L2 as stated is false** for flat squares (edge-to-edge along-wall compression has zero
> torque: the simple packing's rows; on the ring, squares 3, 5, 10 are balanced by wall + two contacts) and for 45° diamonds pinched
> between a wall and a flat square; its true content is TWO-CONTACT on the TILTED meeters, of which every doubly-met open corner has
> at least one (ONE-TILTED).  **[M] Lemma RING holds on all 193 witnesses** (8 HELD + 185 CROWD four-crowds): with the tilt floor /
> crowd rows dropped and the contact structure kept, the free FJ LP is infeasible 193 / 193 — no loaded four-crowd is force- and
> torque-balanced by walls and meeters alone; the missing load is a TORQUE on the tilted meeters (torque-only external loads close the
> balance on 8 / 8 HELD, 37 / 185 CROWD; always anti-aligning, 128 : 10) or a force along the meeter's wall toward its corner /
> into its wall (348 of 351 external meeter forces).  Adding one interior holder never balances 11 squares: the non-meeter squares have
> no room next to a loaded meeter (0 feasible poses at the witness side, 193 / 193 scanned so far); after a 15 % dilation the drains
> return to side 4.000 with ≤ 2 doubly-met corners (free) or keep the four-crowd only with crowd pulls (Σλ ≥ 0.16), never an FJ
> four-crowd (`holder219.jsonl`, run continuing).  **[M] Second order (2b):** the ring's square 6 IS a two-force strut and its
> rotation about the 7-contact IS a first-order zero mode of the loaded core (Lemma STRUT, verified: floor +6.0·10⁻⁴, 7-contact
> +2.5·10⁻⁷, 4-contact −7.5·10⁻⁷ at 1 mrad), but the side INCREASES at second order along it (v₂ = +0.381): the ring is not a
> saddle there; in the 11-square configuration the mode is blocked outright by the caged rattler 0.  Across the witnesses Theorem SO
> excludes 11 of 182 stationary CROWD four-crowds as second-order saddles (6 curve-verified) and 29 more as not Fritz-John under
> another consistent selection; no HELD witness.  **[C] RING as a finite structure question: 2.6·10¹¹ structures (h ≤ 3 interior
> holders; 2.6·10⁷ with none), 2.3·10⁶ CPU-days at 0.78 s each** — not a route; and RING excludes LOADED four-crowds only: the
> rattler crowds (61 of 70 doubly-met corners at genuine k0 FJ points) stay with H1 = T3|k0 (`drain_flow_k0.md` DF-O4, OPEN).
> **k0_00 is unchanged.**

## 1. [T] Lemma CEIL (L1)

**Lemma CEIL (any n).**  `s(n) ≤ ⌈√n⌉`: the grid packing puts ⌈√n⌉² ≥ n unit squares in [0, ⌈√n⌉]².  Hence a packing of side
≥ ⌈√n⌉ is beaten or tied by the simple packing, and a MINIMISER has side < ⌈√n⌉ exactly when s(n) < ⌈√n⌉ — false for n = k², k² − 1,
k² − 2 (s(n) = k there), true at n = 11.  *Proof.* Q_i = [i mod k, i mod k + 1] × [i div k, i div k + 1], k = ⌈√n⌉, i < n ≤ k². ∎
**Corollary (n = 11).**  `Fits 11 4` (Lean, from the axiom and ⌈√11⌉ = 4); the stronger certified bound S ≤ ŝ = 3.877084 (Trump's
packing, `attained_thm`) is what every test below uses.  Lean: `LemmaCEIL.lean` (`simple_packing_fits` axiom, `fits_eleven_four`
theorem).  Obligation: the grid family in Lean (routine).

## 2. [T] Lemma TWO-CONTACT (L2 made exact)

Setting: frictionless contact forces; a wall force is normal to the wall at the touching point; a square–square force at a vertex of
Q lying on an edge of Q′ is along Q′'s edge normal; at a vertex of Q′ on an edge of Q, along Q's edge normal; two squares touching
at two points share a segment (parallel edges) and their force is along that common normal.  A CONTACT of Q is one other body (a wall
or a square) touching it; its force is the sum over the shared rows.

**Lemma TWO-CONTACT (any n, any side).**  Let Q be a unit square of tilt θ (mod 90°) with θ ∉ {0°, 45°, 90°}, touching a wall (at
its unique extreme vertex v) with wall force W > 0.  If Q is in force and torque balance with EXACTLY ONE further loaded contact,
contradiction.  Hence a loaded tilted wall square has ≥ 2 further loaded contacts.
*Proof.*  Two forces in balance are equal, opposite and collinear (torque about the centre: (v − p) × F = 0 with F = −W n, n the
wall normal, so the second force acts at a point p of Q on the line L = v + ℝn).  (a) p a vertex of Q: the vertex abscissae along the
wall are c ± (cos θ ∓ sin θ)/2; two coincide only if sin θ cos θ = 0 (θ ∈ {0°, 90°}) or sin θ = cos θ (θ = 45°); so p = v, and a
second body touching Q at v with a force along ±n would have an edge through v parallel to the wall — the wall itself.  (b) p in the
relative interior of an edge of Q (Q's vertex on Q′'s edge is case (a) with roles swapped; a shared segment is this case): the force is
along Q's edge normal, never ±n since no edge of Q is wall-parallel for θ ∉ {0°, 90°}.  A second WALL: perpendicular walls give
non-collinear normals; opposite walls are out of reach (s > 2 > √2). ∎
**The exceptions are real.**  θ = 45°: L passes through the centre and the opposite vertex; a flat square pressing on that vertex
from above (its edge normal = −n) balances Q with ONE contact — A217's torque-neutral corner diamonds (C5).  θ ∈ {0°, 90°}: flush,
edge contact, along-wall compression with zero torque — the simple packing's rows.  On the ring `rand_0_0569|t20` squares 3, 5, 10
(tilted 20°) are balanced by wall + TWO contacts (`ring_loadpath_rand_0_0569_t20.svg`, A218) — consistent with the lemma, and the
reason L2's "net torque" is not a constraint by itself: the wall torque W(sin θ − cos θ)/2 (Lemma W) is what the two contacts supply.
**Corollary (n = 11, S ≤ ŝ).**  Every loaded tilted meeter of a doubly-met open corner (tilt ∉ {45°}) has ≥ 2 loaded contacts besides
its wall: its partner and/or holders — the "holder" of Lemma HOLD (`k0_count.md` §3) is forced even without a partner push.
Lean: `TwoContact.lean` (`two_contact_core`: the geometric core (a) as an axiom; (b) is the tilt condition).

## 3. [T] Lemma ONE-TILTED

**Lemma ONE-TILTED (any n, any side).**  Two axis-parallel unit squares inside the container that both meet the open corner box
(0, 1)² overlap.  So of the two meeters of a doubly-met open corner at least one is tilted.  *Proof.*  A flat square in the quadrant
meeting the open box is [a, a+1] × [b, b+1] with 0 ≤ a, b < 1; two such have |a − a′|, |b − b′| < 1. ∎  L2's force is therefore on
a tilted meeter at every doubly-met corner: by TWO-CONTACT it needs its partner AND a holder, or two holders (the K0FREE / BOXK0
witnesses realise the 45° exception: their loaded meeters are diamonds, A217 C5).  Lean: `OneTilted.lean` (`one_tilted`, axiom).

## 4. [M] Lemma RING (L3) — the test

**Conjecture RING (n = 11, S ≤ ŝ).**  No loaded four-crowd (four doubly-met open corners, every meeter carrying a loaded contact)
is force- AND torque-balanced by walls and meeters alone; some meeter needs a holder that is no meeter, and the interior holders
cannot balance in the room left.

*Test* (`ring219.py`, 3 s for all 193; `results/ring219.md`).  For each HELD / CROWD four-crowd witness: the active rows at the point
(walls, pair rows on every tied axis, A217's convention — the NLP(S) rows, line rows included), the external rows (tilt bound, crowd)
DROPPED; LP {Aᵀλ = e_s, λ ≥ 0} (λ₀ = 1) and the self-stress LP.  **INFEASIBLE 193 / 193** (also on the rows loaded in the
bounded stress alone: 189 / 189 where that stress is LP-feasible).  Minimal external load closing the balance (L1 over unit loads on
every coordinate): torques alone suffice on 8 / 8 HELD (Σ|τ| 0.25–0.59, the tilt floor supplied 0.59 on the ring) and 37 / 185 CROWD;
the external torque on a meeter is anti-aligning (opposite to its wall torque) in 128 of 138 cases; the external FORCE on a meeter
points along its wall toward its corner (175) or into its wall (114) in 289 of 292 CROWD cases (3 radial), 4 of 4 HELD — the PI's
"out from the centre, toward its wall" reading, with the along-wall component (Lemma HOLD's holder) the larger class.  Per witness
0–7 meeters carry external load (median 4 HELD, 3 CROWD); non-meeters carry some in 130 of 193 witnesses (the holders themselves need
holding — L3's second clause).  Pages: `ring_residual_rand_0_0569_t20.svg` (the ring with its torque residual per meeter),
`best_attempt_<wid>.svg` (the best 11-square attempt).

*One interior holder* (`holder219.py`, detached, resume block in `ring219.md`).  Target = the meeter with the largest external load,
direction = its external force (or a push at a vertex producing its torque); holder = the least-loaded non-meeter; poses = the
holder's vertex on the target's edge / the target's rearmost vertex on the holder's edge, priced by the free residual; then A217's
optimiser from the best pose, free and with the four crowds forced.  At the witness side NO pose is feasible (the free space at
S ≤ 4.2 is slivers: 0–1 feasible slots for a unit square anywhere in the container); after a uniform 15 % dilation poses exist and the
drains give: free → side 4.000 with 0–2 doubly-met open corners (never 4); crowd-forced → four-crowds held by crowd pulls
(Σλ_crowd ≥ 0.16, free FJ residual ≥ 0.12), no FJ four-crowd, none below ŝ.  RING is not refuted by any 11-square attempt.

## 5. [T] Lemma STRUT and Theorem SO — the second-order exclusion (addendum 2b)

**Lemma STRUT (any n).**  Let Q carry exactly two loaded point contacts, at P₁ and P₂, with collinear forces (F at P₁, −F at P₂,
F ∥ P₂ − P₁ — the two-force member).  Then the rotation of Q about P₁ (either sense) has every loaded row of Q stationary at first
order: the row at P₁ is fixed by the pivot, and the row at P₂ changes at rate ω n·J(P₂ − P₁) = 0 since n ∥ F ∥ P₂ − P₁.  It is a
first-order zero mode of the loaded structure iff the unloaded active rows it closes can be opened by the unloaded squares (a
completion LP) — the ring's mode is exactly this, with the caged rattler 0 refusing (§5.2).  *Proof.* rows219 gradients. ∎

**Theorem SO (the second-order necessary condition, selection form).**  Let z* be a packing at side s*, S a consistent selection
(one separating axis per touching pair; walls; the external rows of the problem considered), λ₀ = 1 multipliers Λ_S ≠ ∅ (KKT for
NLP(S)).  Let y be a first-order zero mode: e_s·y = 0, ∇g_r·y ≥ 0 for every row of S.  Put E(y) = {r : ∇g_r·y = 0} and
    v₂(y) := min { e_s·w : ∇g_r·w ≥ −yᵀ∇²g_r y, r ∈ E(y) } = max_{λ ∈ Λ_S ∩ supp ⊆ E(y)} yᵀ∇²L(λ) y,  L = s − Σ λ_r g_r
(LP duality; the dual is the reduced Hessian of the Lagrangian on the mode).  If v₂(y) < 0 (or the primal is unbounded), the curve
x(t) = z* + t y + t² w/2 is feasible for small t > 0 (rows in E: t²(κ_r)/2 ≥ 0 with κ_r = yᵀ∇²g_r y + ∇g_r·w ≥ 0; rows with
∇g_r·y > 0: positive at first order; the selected axes certify non-overlap) and s(x(t)) = s* + t² v₂/2 < s*: **z* is not a local
minimiser of the side, hence no σ-minimiser** (D1 / D3′: a minimiser is a local minimum of every NLP(S) whose feasible set contains
it).  If Λ_S = ∅ and no self-stress exists, z* is not even Fritz-John for NLP(S) and is excluded at first order (D3′).  ∎
*Caveats.* (i) v₂ depends on the completion y (the unloaded squares' motion); the L1-minimal completion keeps the most rows tight
and is CONSERVATIVE (a negative verdict is robust, a non-negative one is not a proof of local minimality).  (ii) w is searched in
|w|∞ ≤ 10 (the sign of v₂ is the statement).  (iii) Every negative verdict is re-checked on the curve at t = 10⁻⁴…10⁻³
(violations ≤ 50 t³, side decrease): "curve-verified".  (iv) A self-stress (λ₀ = 0 only) leaves the first-order verdict open.

**5.2 The ring** (`second219.py --only rand_0_0569|t20`; page `ring_mode_rand_0_0569_t20.svg`).  Square 6: loads from 4 (P4 =
(2.0586, 0.9397), F = (0.538, 0.196)) and 7 (P7 = (2.9983, 1.2817)); moment of F about P7 = −2.7·10⁻¹¹; floor row active, λ = 0.
Rotation about P7 clockwise, 1 mrad: floor gap +5.98·10⁻⁴ (rate 0.598 / rad), gap to 7 +2.5·10⁻⁷ (quadratic), gap to 4 −7.5·10⁻⁷
(quadratic; the strut condition) — the PI's numbers — AND gap to the rattler 0: −6.4·10⁻⁴ (first order).  Loaded core (rattler
rows dropped): the mode is a first-order zero mode (2 rows open: the floor and one line row), **v₂ = +0.381 > 0 — the side increases
at second order; the ring + floor is not a saddle along the strut mode.**  With rattler 0's rows kept: the completion LP is
infeasible — 0 sits in the pocket of 4 and 5 (edge-edge contacts on two sides) with its corner at the triple point P4 = 4's corner =
6's corner, and 6's rotation drives into it: **the mode is blocked in the 11-square configuration.**  (A caged rattler is a genuine
obstruction for local minimality; for a GLOBAL minimiser it is not, since the rattler may be moved wherever its free region allows —
here it cannot leave the pocket continuously.)  One further core-variant mode (rotation of 6 about its floor vertex, the whole ring
bending) returns v₂ = −6.8·10⁻⁴ with w at the box and fails the curve check: recorded, not claimed.

**5.3 All witnesses** (`results/second_order219.md`, 158 s).  Variants: bounded (all active rows: the problem the witness is a local
optimum of), loaded_ext (walls + pairs + the loaded external rows), core (loaded_ext on the loaded squares), free.  Candidates: the
rotation of every square about every one of its active contact points (both senses; STRUT-labelled when its loads are two point
loads) and the eigenvectors of the reduced Hessian at the LP multiplier; completion by LP; selection per pair by the best axis.
HELD 8: stationary 7 (one has no λ₀ = 1 multiplier even with the tilt bound), zero modes at 5, strut modes at 3, **second-order
saddles 0** (core: the marginal ring mode above), not Fritz-John under another selection 3.  CROWD 185: stationary 182, zero modes
at 119 (strut modes at 48), **second-order saddles 11 (curve-verified 6–9 depending on the variant; none on a strut mode), not
Fritz-John under another consistent selection 29** (no self-stress either: excluded at first order by D3′ — SLSQP's own selection
was KKT, another tied axis at a vertex–vertex contact is not).  Free variant: no witness is stationary (as A217 found: the bound /
crowd multipliers are positive).  So: the second-order test bites on a fifth of the CROWD four-crowds and on none of the HELD ones;
the PI's strut mechanism is real (48 witnesses carry a strut mode) but stiff (v₂ ≥ 0 on every strut mode tested).

## 6. [C] The finite structure question, counted and priced

**Structure.**  A loaded four-crowd contact structure: 8 meeters m_{c,w} (corner c, cell against wall w), per meeter a WALL bit and
≤ 2 HOLDERS ∈ {other meeter (not the partner), interior square I₁…I_h, h ≤ 3}; per corner a PARTNER bit; each interior square touches
≥ 1 meeter, interior squares may touch each other; LOADED: every meeter has ≥ 1 contact.  (`structures219.py`: cross graphs of the
24 non-partner meeter pairs with holder-degree ≤ 2 by DFS, interior attachments by inclusion–exclusion, wall/partner bits per corner.)
**Count.**  Labelled 1.18·10¹³ (h = 0: 2.1·10⁸, h = 1: 5.6·10⁹, h = 2: 2.1·10¹¹, h = 3: 1.2·10¹³); orbits under D4 × S_h ≈
**2.6·10¹¹** (h = 0: 2.6·10⁷; h = 1: 3.5·10⁸).  The TWO-CONTACT prune on the wall/partner bits alone removes 10 %.  **Price at 0.78 s
per structure (H-LOC, `fj_census_k0.md` §4): 2.3·10⁶ CPU-days; the no-interior-holder slice alone 232 CPU-days, one interior holder
3 200 CPU-days.**  Even the smallest slice is A85's whole tree.  A proof of RING by structures is not a route; what would make it one
is a reach lemma cutting the 24 cross pairs to the ≤ 8 adjacent-corner pairs (diagonal meeters CAN touch at S ≤ ŝ: two diamonds with
centres 1.16 apart) and a bound h ≤ 1 — neither is available.

**What RING would and would not close.**  RING excludes LOADED four-crowds.  At the genuine k0 FJ points 61 of 70 doubly-met corners
are RATTLER crowds (both meeters unloaded, `k0_count.md` §5); a rattler crowd is invisible to force balance.  The lemma that covers a
corner box met by ≤ 1 square is K0-FREE (teleport, [T], Lean `teleport_packing`, `k0_route.md` §3); a doubly-met rattler crowd is
covered by nothing proved: it is the H1 = T3|k0 obligation (`drain_flow_k0.md` DF-O4, OPEN — the drain, which A217 / A218 measured:
every k0 local optimum below 3.9 drains to a settled-corner optimum).  So even RING proved would leave k0_00 where it is.

## 7. Lean, files, obligations

`Statements/Open/LemmaCEIL.lean` (`simple_packing_fits` axiom; `ceil_sqrt_eleven`, `fits_eleven_four` theorems), `TwoContact.lean`
(`two_contact_core` axiom, `IsVertex`), `OneTilted.lean` (`one_tilted` axiom): `lake build` exit 0, `lean/audit.py` exit 0, no
sorry, each axiom its own only non-standard dependence (`lean/AUDIT.md`).  Obligations: O-CEIL the grid family; O-2C the vertex
abscissae computation; O-1T the flat-square set and `mem_interior_iff_uv`.  Lemma STRUT / Theorem SO are prose over NLP(S) (no
Lean object for the multipliers in the readable layer).  Nothing in `Main.lean` depends on these files.
Code: `rows219.py` (rows, analytic Hessians, LPs), `ring219.py`, `modes219.py` (selection, completion, v₂, curve check),
`second219.py`, `holderpose219.py` / `holder219.py`, `structures219.py`, `draw219.py` / `pages219.py`, `test_rows219.py`.
