# NOCRIT for K0-BLOCKED: the retreat selection, the exact residue, and why the FJ form is the wrong statement — A90, 2026-09-03

Target (A90 BRIEF): Theorem NOCRIT — a K0-BLOCKED packing of 11 unit squares (every corner's open
unit slot met by the interiors of ≥ 2 squares) is not a Fritz-John point of the enclosing-side
function — proved, or a restricted form with its exact residue, or an explicit obstruction; then
the composition k0_00 = DF-K0 + NOCRIT + K0-FREE + k ≥ 1 kills. Labels: [T] proved, [S] routine
given cited items, [M] measured (T3, `attempts/A90-nocrit-blocked/notes/t3_report.md`), [F]
finding, [C] open. Conventions: `drain_flow_k0.md` (DF-K0, FJ, D3′), `tilt_floor_k0.md` (A89:
LOCK, MENU, JAM-0, TF-U, ID), `k0_route.md` (K0-FREE, K0-WIDEN, K0-PAIR, K0-REUSE),
`structure_lemmas.md` (L1, L6), A44 `notes/theory.md` (L8–L10), A58 `notes/theory.md` (CC-2).

## 0. Verdict

> **NOCRIT holds in a RESTRICTED (selected) form, with an exact residue; the FJ form of the
> brief is the wrong statement and is bypassed.**
>
> * [T] **The FJ form cannot be the theorem.** Lemma BLIND (§2): an FJ certificate is a statement
>   about the loaded rows only; moving any square that carries no positive multiplier (rattlers,
>   and every unloaded but touching square), keeping the packing at the same side, preserves the
>   certificate verbatim. So "K0-BLOCKED ⇒ not FJ" can be true only for ROOM reasons that FJ does
>   not see (whether 8 intruders fit around a loaded core), and the brief's route — count the
>   far-side locks of Lemma MENU against the loads an FJ point can carry (L1, L6, per-wall caps,
>   H-LOC) — cannot close: flush-lock (Lemma LOCK (b)) and every other lock is a statement about
>   contacts that EXIST, not about multipliers that are POSITIVE (A89-G1's wall, again). The
>   rattler case (a) of the brief is decided this way: a rattler intruder never spoils FJ.
> * [T] **Theorem NOCRIT-SEL (§3).** Let Ψ(z) := Σ_corners Σ_squares d_c(Q_i) be the total
>   intrusion (d_c = corner intrusion depth, tolerance-exact: a tangency has d = 0). Over the
>   compact set M(m) of σ-minimisers there is a Ψ-minimal one, z*. At z*, for EVERY intruder Q of
>   every corner c and every cardinal retreat direction e of Q (Lemma K: an intruder is x-side,
>   y-side or corner-type; it retreats along e_x, e_y, or both), the retreat cluster C_e(Q) —
>   the set of squares that must move with Q when Q translates along e, closed under "presses
>   against e" — is ANCHORED: it contains a square on the far wall in direction e, or an intruder
>   of another corner (or a tangent square) whose depth strictly increases under e. The proof is
>   exact and first-order: all rows are affine in the centres, so a cluster translation is a
>   packing at side m for small t (no second-order term, flat strata irrelevant), and Ψ is
>   piecewise-linear with negative right-derivative. FJ is used NOWHERE; criticality (DF-K0's
>   H1) is not the hypothesis, minimality is, exactly as in TF-U.
> * [T] **Closed cases.** At z*: no intruder is a rattler (cluster = {Q}); every intruder is
>   PRESSED toward its corner, for each of its cardinal retreat directions, by a neighbour on
>   its far side (the far walls are > 1.4 away); the JAM-0 partner (case (ii)) is y-side and is
>   pressed from above by a third square whose own upward cluster must reach the top wall; an
>   axis-aligned intruder at offset (a, b) is pressed from the right if a ≥ b and from above if
>   b ≥ a. Every anchoring column that reaches a far wall has ≥ 3 squares at side ≥ 1 + 2√2 =
>   3.8284 and, below that, ≥ 3 except in a diamond-ghost regime (two tilts within 6.1° of 45°,
>   intruder depth < 0.0084) (Lemma COL).
> * **The residue is RES(4) (§4): a K0-BLOCKED σ-minimiser at which all eight (or more)
>   intruders are anchored in all their cardinal retreat directions — a FRAME: wall-to-wall (or
>   corner-to-corner, exactly rate-matched) contact columns of ≥ 3 squares in both axes, passing
>   through the corner crowds, built from the 8 intruders and the 3 free squares.** RES(4) is a
>   geometric statement about contacts at the SELECTED minimiser; nothing in this file refutes
>   it, and nothing in the lab's counting (L1/L6/L8 are about loads) can. Its price as a
>   SelForm (C) leaf of A85's tree is the K0-ROT/TF-U verdict: free at deep nodes, silent at the
>   frontier — **A85's price stands.** The plateau clause (Lemma PLATEAU, §4.3) sharpens
>   corner-to-corner anchoring: a rate-matched column slides at constant Ψ to an endpoint that
>   is K0-FREE, wall-anchored, or a new contact.
> * **Where "all four corners blocked" enters (§5).** Nowhere in the reduction: Theorem
>   NOCRIT-SEL is proved corner by corner and uses only "corner c is met by ≥ 2 squares" at the
>   corner whose intruder retreats. It enters ONLY in the refutation of the residue: RES(1) (one
>   blocked corner, anchored) is REALISED by Trump — TL's shallow intruder sq4 is y-side (retreat
>   = down), its downward cluster runs through the strip to the floor, the deep intruder sq6 is
>   corner-type and its two clusters reach the floor and the right wall; Trump is rigid, RES
>   holds at TL, and Theorem NOCRIT-SEL does not exclude it (canary [M]: Trump critical, TL
>   2-crowd locked). A refutation of RES(4) must therefore use ≥ 2 blocked corners, and the
>   proof shape is Lemma COL's count against 11 squares — four corners' columns, ≥ 3 squares
>   each, in both axes, with the corner squares of Trump's frame replaced by tilted 2-crowds.
> * [M] **T3 (§7):** the retreat mechanism is confirmed at full strength on A87's 520 exits —
>   the freeing square is the non-deepest intruder 520/520, retreatable by a single-square
>   cardinal translation 508/520 (511 with the diagonal), unlocked 515/520; the 12 exceptions
>   are coordinated multi-square motions (a motion-class gap of the translation test, not a
>   lock); Trump canary PASS (critical, TL 2-crowd locked, RES true, not excluded); BLIND
>   hunt 0/167 K0-BLOCKED FJ points, with 70/167 points short of blind squares outright.
> * **Composition (§6).** k0_00 = SEL-Ψ (Ψ-minimal σ-minimiser exists; Lean: compactness +
>   continuity, S1–S5 of A89 §9.3 with Ψ for Φ) + Theorem NOCRIT-SEL (z* K0-BLOCKED ⇒ RES(4)) +
>   [¬RES(4), OPEN] + Lemma K0-FREE (teleport; k1_00's tree, K0-O1) — at every side of the
>   window, the ŝ clause through the Φ-minimal-non-image trick of TF-U (ii). It discharges the
>   k0_00 piece of `stratum_kill` (C.K4TIER) in the `StratumKillSel` form; DF-K0's H1 is not
>   consumed. The PI conjecture in its n = 11 form becomes: "¬RES(4)", i.e. no Ψ-minimal
>   σ-minimiser is a frame.

## 1. Setting and definitions

Packings: eleven closed unit squares Q_i = Q(c_i, θ_i), pairwise interior-disjoint, inside
[0, m]²; M(m) = the packings at side m (compact in the 33 pose coordinates, `tilt_floor_k0.md`
§1); m = s(11) the attained minimum (D1) unless said otherwise. Consistent selections S and their
rows as in `drain_flow_k0.md` §1: near-wall rows q ≥ 0, far-wall rows m − q ≥ 0, pair rows
(corner_{k*}(j) − c_i)·u ≥ 1/2 with dominance rows; S-feasible ⇒ interior-disjoint; every packing
is S-feasible for some consistent S.

**Fact A (rows are affine in the centres).** Every row of every selection is an affine function
of the centre coordinates (c_i, c_j) at fixed tilts: wall rows are corner coordinates c + R(θ)w,
pair rows are (c_j + R(θ_j)w_{k*} − c_i)·u(θ_i) − 1/2 and their dominance rows do not involve
centres at all. [T: read off. This is `fjsecond87.md` §2's "centre–centre block of ∇²L is
exactly zero".] Consequently, along a motion that translates a set C of squares by t·v (tilts
fixed, the other squares fixed), every row is affine in t: g_k(t) = g_k(0) + t·Σ_{i∈C} ∇_{c_i}g_k·v.

**Corner frame, depth.** For a corner c, the corner frame is the D4 map sending c to the origin
with the container in the positive quadrant (coordinates written (x, y)). For a square Q put

  μ_c(Q) := min_{p ∈ Q} max(p_x, p_y)   (closed Q; a continuous function of the pose),
  d_c(Q) := max(0, 1 − μ_c(Q))            (intrusion depth; = A89's depth when positive).

[T] d_c(Q) > 0 ⟺ int Q ∩ (0, 1)² ≠ ∅ (A58's "Q meets the corner box"): if μ < 1 some p ∈ Q has
max(p_x, p_y) < 1, nearby interior points of Q have the same, and int Q ⊂ (0, m)², so they lie
in (0, 1)²; conversely an interior point in (0, 1)² has max < 1. A tangency (Trump's square 3 on
the top edge of the BL slot) has μ = 1, d = 0: the tolerance law of `k0dir87.md` is built in.
**Intruder** at c: d_c(Q) > 0. A square intrudes at most one corner (CC-1(ii)); an intruder's
far-wall rows have margin > 1.4 (`tilt_floor_k0.md` §1). **K0-BLOCKED**: ≥ 2 intruders at every
corner; **K0-FREE**: some corner has ≤ 1 intruder (Lemma K0-FREE's hypothesis).

**Selection functional.** Ψ(z) := Σ_c Σ_i d_c(Q_i) ≥ 0, continuous on pose space.

**Argmin set, retreat cone.** S_c(Q) := Q ∩ [0, μ]² (μ = μ_c(Q)) — the points of Q attaining
the min; it is nonempty, convex, and contained in the two sides {x = μ} ∪ {y = μ} of the box
(Q ∩ [0, μ)² = ∅ by minimality). The **retreat cone** K_c(Q) := {v ∈ ℝ² : t ↦ μ_c(Q + tv) is
strictly increasing on [0, t₀) for some t₀ > 0}.

## 2. [T] Lemma BLIND and the status of the FJ form

**Lemma BLIND.** Let (z, s) be an FJ point of NLP(S) with certificate (λ₀, λ), and let
U := {squares i : λ_k = 0 for every row k involving Q_i}. Let z′ be any packing at side s that
agrees with z on the squares not in U. Then (z′, s) is an FJ point of NLP(S′) for every
selection S′ consistent with z′ that agrees with S on the rows among the squares not in U, with
the SAME certificate (λ₀, λ) (zero on every row involving U).

*Proof.* Stationarity λ₀∇s = Σ λ_k ∇g_k involves only rows with λ_k > 0, all among the non-U
squares, whose poses and hence gradients are unchanged; those rows are active at z (λ_k g_k = 0)
and remain active at z′ (unchanged poses); every other row has λ_k = 0 and only needs g_k ≥ 0,
which is z′'s feasibility. ∎

*Consequences.* (i) A rattler (no active row) is in U; so is every square all of whose contacts
are unloaded. Hence the FJ property is INSENSITIVE to whether the squares of U intrude corners:
"K0-BLOCKED ⇒ not FJ" (at any side) can hold only because of ROOM — the loaded core, which FJ
sees, may leave no space for |U| squares to double every corner. That is a packing-density
question about the unloaded set, and no argument that reasons on multipliers (L1 loaded degree
≥ 2, L6 wall-to-wall loaded chain, the per-wall load caps, Lemma H-LOC) can decide it: they
constrain the loaded core only. (ii) The brief's route — Lemma MENU's far-side set counted
against the loads — has the same defect one level up: Lemma LOCK (b) (and MENU, which is LOCK
for a wall pivot) says a square is locked iff its ACTIVE contacts CAN carry a couple away from
flush; the multipliers that an FJ certificate happens to put on them are irrelevant, and a
locked square may carry zero load (A89's o170). Lockedness is geometric; only geometric
counting can refute it. (iii) The corpus is consistent with (i): A87's 167 FJ points have
1–7 rattlers at 152 of them and are all K0-FREE, and the directed search never produced a
K0-BLOCKED FJ point — but [M, T3 task 4] the blind hunt (re-placing the unloadable squares of
those points to double every corner while keeping the certificate) measures directly whether
the room exists at those cores; see `t3_report.md`. The correct n = 11 statement is therefore
the selected one, §3, which needs no criticality at all.

## 3. [T] Theorem NOCRIT-SEL

### 3.1 Lemma K (retreat trichotomy)

**Lemma K.** Let Q be an intruder at c, μ = μ_c(Q) < 1, S = S_c(Q). Exactly one of:
 (X) S ⊂ {x = μ} and S ≠ {(μ, μ)}: Q's leftmost point is a vertex or a vertical edge, lying
     (partly) strictly below the diagonal. Then K_c(Q) = {v : v_x > 0} and μ_c(Q + t e_x) =
     μ + t (rate 1).
 (Y) the mirror: K_c(Q) = {v : v_y > 0}, rate 1 along e_y.
 (D) S = {(μ, μ)}: the diagonal point is a vertex of Q, or lies in the relative interior of an
     edge of Q with inward normal n_Q having n_Q,x > 0 and n_Q,y > 0. Then e_x, e_y ∈ K_c(Q),
     with rates ρ_x, ρ_y > 0: for the edge case ρ(v) = v·n_Q/(n_Q,x + n_Q,y), i.e. ρ_x =
     n_Q,x/(n_Q,x + n_Q,y), ρ_y = n_Q,y/(n_Q,x + n_Q,y); for a lowest vertex with edge
     directions (cos α, sin α), (−sin α, cos α), α ∈ (0, 90°), ρ_x = cos α/(sin α + cos α),
     ρ_y = sin α/(sin α + cos α) (the other vertex types by the same computation, always
     ρ_x, ρ_y > 0); for the axis-aligned vertex ρ_x = ρ_y = 1.
In all cases K_c(Q) is an open convex cone containing the open positive quadrant, t ↦ μ_c(Q + tv)
is convex and piecewise-linear, and at least one of e_x, e_y lies in K_c(Q).

*Proof.* S is convex (argmin of the convex function max(p_x, p_y) over the convex set Q) and
lies in the union of the two perpendicular segments {x = μ, 0 ≤ y ≤ μ}, {y = μ, 0 ≤ x ≤ μ}, so
it is contained in one of them or is their common point: the trichotomy. Convexity in t:
(p, t) ↦ max(p_x + tv_x, p_y + tv_y) is jointly convex, and a minimum over p ∈ Q of a jointly
convex function is convex in t; piecewise-linearity: min over the polytope Q of a max of two
affine functions. Case (X): every point of Q has x ≥ μ, so μ_c(Q + te_x) ≥ μ + t, with equality
at the translated leftmost point below the diagonal; for v with v_x ≤ 0 the point of S with
y < μ (which exists by S ≠ {(μ,μ)}) gives μ_c(Q + tv) ≤ max(μ + tv_x, y + tv_y) ≤ μ for small
t. Case (D), edge: near (μ, μ) the square is the half-plane {(p − (μ,μ))·n_Q ≥ 0} with n_Q
pointing away from the corner; parametrise the edge by (μ, μ) + s(−n_Q,y, n_Q,x); then
max(μ − s n_Q,y + t v_x, μ + s n_Q,x + t v_y) is minimised where the two arguments agree, at
value μ + t (n_Q,x v_x + n_Q,y v_y)/(n_Q,x + n_Q,y), which is the claimed rate; points off the
edge only increase the max (the edge is the boundary of the half-plane on the corner side). If
n_Q were axis-parallel, S would be a segment (case X or Y). Vertex: the same computation along
the two edges from the vertex; the minimum over the wedge is attained on one of the two edges,
because the level sets of max(p_x, p_y) are the boxes [0, λ]² and the smallest box meeting the
wedge meets it on the wedge's boundary (if its corner (λ, λ) were interior to the wedge, a
smaller box would still meet it). ∎

### 3.2 Lemma CLUSTER (feasible retreat of a pressed set)

Fix a packing z at side m, a consistent selection S, a set C of squares and a direction e. Say
that an outsider N ∉ C **presses** a member M ∈ C against e if some active S-row between M and N
has ∇_{c_M} g · e < 0 (the contact force on M, along the selected axis, has a component against
e). C is **e-closed** if no outsider presses a member; C is **wall-anchored** (for e) if some
member has an active far-wall row whose outward normal is e (the far wall in direction e);
C_e(Q) := the smallest e-closed set containing Q (the forward closure of "is pressed by").

**Lemma CLUSTER.** If C is e-closed and not wall-anchored, then for all sufficiently small t > 0
the configuration z_t (members translated by te, tilts and outsiders fixed) is S-feasible, hence
a packing at side m.

*Proof.* Rows among members: unchanged (rigid translation). Rows between a member M and an
outsider N: affine in t (Fact A) with slope ∇_{c_M}g·e ≥ 0 when active (closedness), and
inactive rows have positive margin. Wall rows of members: the near wall in direction e has
outward normal −e, so its row increases; walls parallel to e are unchanged; the far wall's row
decreases at rate 1 but is inactive by the no-anchoring hypothesis, so it keeps a margin for
small t. Dominance rows do not depend on centres. ∎

### 3.3 The selection and the theorem

**Lemma SEL-Ψ.** M(m) is compact and Ψ is continuous, so Ψ attains its minimum on M(m) at some
z*. The same holds on any compact subset of M(m) stable under small translations of subsets of
squares that preserve the packing property — in particular on the non-Trump-image packings at
ŝ (closed by basin isolation, E.A36, exactly as in TF-U (ii)).

**Theorem NOCRIT-SEL.** Let z* minimise Ψ over M(m) (or over the non-image packings at ŝ). Then
for every corner c, every intruder Q at c, every e ∈ {e_x, e_y} ∩ K_c(Q) (in c's frame) and
every consistent selection S, the cluster C_e(Q) is **anchored**:
  (W) wall-anchored — some member touches the far wall in direction e — or
  (I) intruder-anchored — some member N and corner c′ ≠ c satisfy d_{c′}(N + te) > d_{c′}(N)
      for all small t > 0 (N is an intruder or a tangent square of c′ that deepens under e).
In particular, if z* is K0-BLOCKED then every one of its ≥ 8 intruders is anchored in each of
its cardinal retreat directions, for every consistent selection (RES(4), §4; the residue may
be tested with the selection that gives the smallest clusters).

*Proof.* Suppose C := C_e(Q) is neither. By Lemma CLUSTER, z_t is a packing at side m for small
t > 0, so z_t ∈ M(m) (σ ≤ m and m is the minimum; for the ŝ-variant, z_t stays outside every
image basin for t < r_B − dist(z*, images)). Ψ(z_t) − Ψ(z*): only members' depths change;
d_c(Q + te) decreases at the positive rate of Lemma K (strictly, by convexity of μ with positive
right-derivative); every other member's depth at every corner is nonincreasing for small t by
¬(I) (its μ is convex piecewise-linear, so "not strictly increasing depth for small t" means
nondecreasing μ), and at c itself every member's depth is nonincreasing (e ∈ closure of K_c for
every square of c… precisely: μ_c(N + te) ≥ μ_c(N) for e ∈ {e_x, e_y}, since translating away
from the corner along an axis cannot decrease max(p_x, p_y)). Hence Ψ(z_t) < Ψ(z*) for small t,
contradicting minimality. ∎

Remarks. (1) No selection multiplier, no FJ, no second-order term is used: the argument is
Lemma CLUSTER (exact affine feasibility) + Lemma K (exact rates) + compactness — the flat strata
of `fjsecond87.md` are irrelevant (item (c) of the brief). (2) The hypothesis at the corner c
is only "Q intrudes c"; K0-BLOCKED is not used in the proof (item (b): see §5). (3) The theorem
constrains the deepest intruder too (Ψ is the total intrusion), which is why the residue is a
statement about all eight intruders and not about the shallower ones only; a version with the
shallower-only functional Ψ₂ = Σ_c (Σ d − max d) gives the same conclusion for the non-uniquely-
deepest intruders and nothing for the deepest — strictly weaker, not used. (4) Rotations are
not used; a rotational retreat (A89's Lemma MENU motion for a wall blocker) would shrink the
residue further where it applies, but MENU's motion is toward FLUSH, not away from the corner,
and does not decrease d in general; a proper rotational retreat cone is left [C].

### 3.4 [T] Closed cases

**Corollary 1 (rattlers; item (a)).** At z*, no intruder is a rattler: a rattler has no active
row, so C_e(Q) = {Q} for every e, it touches no wall, and it deepens at no other corner (a
square intrudes or is tangent to at most one corner: tangency to a second corner's slot needs
extent > m − 2 ≥ 1.82 > √2). Retreat along a cardinal direction of Lemma K contradicts SEL-Ψ.
(TF-U's clause "rattlers are flush" is compatible: apply Ψ-minimality first, then Φ among the
Ψ-minimisers; both selections can be imposed lexicographically on the compact set of Ψ-minimal
minimisers, and a flushing rotation of a rattler does not change Ψ.)

**Corollary 2 (every intruder is pressed).** At z*, for every intruder Q and every cardinal
e ∈ K_c(Q), Q has an active pair row with ∇_{c_Q}g·e < 0: a neighbour on Q's far side in
direction e. (C_e(Q) = {Q} otherwise, and Q cannot touch its far walls.) So a corner-type
intruder (Lemma K (D)) is pressed both from the right and from above; an x-side intruder from
the right; a y-side intruder from above. An axis-aligned intruder [a, a+1] × [b, b+1] is
corner-type if a = b (pressed on both far sides), x-side if a > b (pressed from the right),
y-side if a < b (pressed from above).

**Corollary 3 (the two-square corner jam, item (ii)).** In Lemma JAM-0's configuration (P
axis-aligned at offset g < 1/√2, N with a vertex v in the L-strip, tilt ≤ arcsin g, depth ≤
g²/√(1−g²)): v is N's lowest (resp. leftmost) vertex and is the unique point of S_c(N), lying
strictly left of (resp. below) the diagonal, so N is y-side (resp. x-side); at z*, N is pressed
from above by a third square T (Corollary 2), and C_{e_y}(N) = {N, T, …} must be anchored:
either the column of pressers above N reaches the top wall (T itself cannot for g ≤ 0.3: N's
tilt is ≤ 17.5°, N's top is at height ≤ 1 − d + cos α + sin α ≤ 2.26, so T's highest point is
≤ 2.26 + √2 = 3.67 < 3.82 ≤ m — the column needs a fourth square), or a top-corner intruder in
the column deepens. This is exactly A89 §5.2's "presser within r of u",
with the missing global clause supplied: the presser must itself be pressed, up to the wall.

**Corollary 4 (K0-REUSE pocket).** For g < δ_pin = 0.02 the pocket is k1_00's tree (K0-REUSE,
∀-packings); Corollary 3 adds nothing there and is not needed.

## 4. The residue RES(4)

### 4.1 Statement

**RES(4).** A K0-BLOCKED packing z ∈ M(m) such that every intruder Q of every corner is anchored
(W or I) in each of its cardinal retreat directions. Theorem NOCRIT-SEL: if the Ψ-minimal
minimiser is K0-BLOCKED it is a RES(4) configuration. Hence

  ¬RES(4) at side m  ⟹  the Ψ-minimal minimiser is K0-FREE  ⟹  (Lemma K0-FREE) no minimiser
  at side m < ŝ; every minimiser at ŝ is a Trump image.

### 4.2 [T] Lemma COL (anchoring columns are long)

Let C be wall-anchored for e from an intruder Q at c, and let Q = N₀, N₁, …, N_k be a chain of
members, each pressing the previous against e, with N_k on the far wall (such a chain exists by
the definition of C_e as a forward closure). The union N₀ ∪ … ∪ N_k is connected (consecutive
members touch), contains a point with e-coordinate < 1 (Q's intruding point) and a point with
e-coordinate m, so its e-extent exceeds m − 1 ≥ 2.82; each unit square has e-extent
|cos θ| + |sin θ| ≤ √2. Hence k + 1 ≥ 3 whenever m − 1 ≥ 2√2, i.e. **m ≥ 1 + 2√2 = 3.82843**, and
for m ∈ [3.82, 3.82843) a two-square column (k = 1) forces both extents > 2.82 − √2 = 1.4058,
i.e. both tilts within 6.3° of 45°, and Q's intruding point within 2√2 − (m − 1) ≤ 0.0084 of the
slot boundary (μ_c(Q) ≥ m − 2√2, so d_c(Q) ≤ 0.0084). ∎ An intruder-anchored column (I) ending at an intruder N of
the opposite corner along the axis of e has ≥ 2 squares (N has a point with e-coordinate
> m − 1 ≥ 2.82, Q one with < 1); it is "mutual": by the symmetry of pressing (∇_{c_M}g = −∇_{c_N}g
for a pair row), Q ∈ C_{−e}(N).

### 4.3 [S] Lemma PLATEAU (mutual anchoring slides)

Suppose at z* the cluster C = C_e(Q) is not wall-anchored and is intruder-anchored only through
members N whose depth at their corner c′ increases under e with rate exactly equal, in total, to
the total decrease of the retreating members' depths (Ψ has zero right-derivative along the
cluster translation; by Lemma K this is the case, e.g., for an x-side Q at BL and an x-side N at
BR in a horizontal column: both rates are 1). Then the translation z_t stays in M(m) with
Ψ(z_t) = Ψ(z*) for t ∈ [0, t₁], where t₁ is the first t at which (a) a new S-row becomes
active, or (b) some retreating member's depth reaches 0, or (c) a member's argmin type changes;
and z_{t₁} ∈ M(m) is again Ψ-minimal. At t₁: in case (b) with the corner having exactly two
intruders, z_{t₁} is K0-FREE (contradiction with K0-BLOCKED via Lemma K0-FREE); in case (a) the
new contact either enlarges the cluster (an outsider now presses a member: if it is wall-
anchored we are in (W) at z_{t₁}; if it is an intruder of a THIRD corner that retreats under e,
Ψ strictly decreases beyond t₁, contradiction; if it deepens, the plateau continues with a new
rate balance or ends) or is a contact of a member with the far wall (W). *Proof.* Along
[0, t₁] all rows are affine and stay ≥ 0 (Lemma CLUSTER's argument with a uniform margin up to
the first activation), depths are affine (no argmin-type change), so Ψ is constant; M(m) is
closed. ∎ So corner-to-corner anchoring is never terminal: the residue RES(4) can be taken with
every column WALL-anchored at some point of its plateau, or ending on a strict rate mismatch
(a positive-dimensional exceptional set: exact equality of the rates of Lemma K, which are
determined by tilts).

### 4.4 The shape of RES(4) (what a refutation must beat)

Take the generic case (no rate ties, every column wall-anchored). At each corner c, each of its
two intruders has cardinal retreat directions by Lemma K; a corner-type intruder needs BOTH
clusters anchored: a column to the opposite vertical wall and a column to the opposite
horizontal wall, each ≥ 3 squares (Lemma COL), each starting at the intruder and proceeding
monotonically (each member presses the previous along e, so the members' e-coordinates
increase: the column is a monotone chain of contacts along e). The union over the four corners
is a **frame**: wall-to-wall chains of contacts in both axes through the corner crowds — the
geometric skeleton of Trump (his frame is the diagonal strip plus the three slot squares) with
every slot square replaced by a tilted 2-crowd. The 3 free squares and the 8 intruders supply
all members; a member may serve several columns (a bottom horizontal column {P_BL, F, P_BR}
anchors P_BL rightward and P_BR leftward at once).

**[F] What counting gives and does not give.** Two opposite intruders cannot anchor each other
directly against the walls (a 2-square wall-to-wall column needs 2√2 ≥ m, false); a horizontal
wall-to-wall column needs ≥ 3 squares; a K0-BLOCKED frame with all eight intruders corner-type
needs, per axis, columns from both bottom corners and both top corners — at least two
horizontal and two vertical wall-to-wall chains sharing squares — and 11 = 8 + 3 squares can
in principle supply four chains of three (the two middle members of the vertical chains being
intruders of the adjacent corners, the horizontal chains' middles the three free squares and
one intruder): the count alone does not close. What does not exist in the lab is a theorem
that four such chains cannot coexist with eight intruders in [0, ŝ]²; it is a finite geometric
question about contact chains (each chain a 3-square wall-to-wall contact structure of the
kind A47's spans quantise: 1 + 2√2 = 3.8284 is inside the window, and A47's exception
certificate at 2√2 + 1 kills exactly the flush-free 3-chain of span 1 + 2√2 — but a frame
column need not be flush-free), and it is the exact locus where "all four corners blocked" is
used: RES(1) is realised (Trump), RES(2)/RES(3) are not excluded by anything here.

## 5. The canary and the four-corner locus

[M, T3 task 3] Trump (TL frame; A03 exact data): sq4 = [0, 1] × [0.8445, 1.8445], μ_TL = 0.8445,
S = {(x, 0.8445) : 0 ≤ x ≤ 0.8445} — case (Y): retreat = e_y (down, in container coordinates),
rate 1; K_TL(sq4) = {v_y > 0}; e_x ∉ K (sliding sq4 along the left wall to the right does not
reduce its intrusion until x > 0.8445). Its downward cluster is the strip below it and reaches
the floor: (W). sq6 (tilt 40.18°, depth 0.1683) is expected corner-type (its lower-left edge
crossing the diagonal of the TL frame; T3 measures), retreating along both cardinals with both
clusters wall-anchored (Trump is rigid, A22). So RES holds at Trump's TL, Theorem NOCRIT-SEL
excludes nothing at Trump, and the FJ status (critical, TL 2-crowd flush-locked by far-side
contacts per A89 §6) is untouched: **canary PASS by construction**. At Trump's three other
corners the single intruder is the slot square (μ = 0, corner-type with ρ = 1), whose clusters
contain the strip and are wall-anchored by rigidity; the theorem constrains it and is satisfied.

**The four-corner locus, exactly.** Theorem NOCRIT-SEL uses "corner c doubly met" nowhere and
"K0-BLOCKED" nowhere; it is a statement about every intruder of every corner of the Ψ-minimal
minimiser. The hypothesis "all four corners blocked" is used ONLY to (i) state the residue
RES(4) and (ii) refute it — and (ii) is open. At Trump the residue's condition holds at the
one blocked corner; a proof of ¬RES(4) must therefore use ≥ 2 blocked corners, through Lemma
COL's count of wall-to-wall chains against 11 squares (§4.4). The brief's expectation — that
the shallower intruder is never flush-locked when all four corners are blocked — is replaced by
the exact statement: at the selected minimiser the shallower intruder is never RETREAT-free;
its retreat is blocked by a monotone contact column to the far wall (or a rate-matched mutual
column), and Trump's TL supplies the column from the strip.

## 6. Composition and Lean-readiness (T2)

**Composition (if ¬RES(4) is established at every side m ∈ [3.82, ŝ]).** For the lower bound:
m := s(11) (D1); z* := a Ψ-minimal element of M(m) (SEL-Ψ); by Theorem NOCRIT-SEL + ¬RES(4), z*
is K0-FREE; by Lemma K0-FREE (k1_00's tree at every side of the window, K0-O1; Theorem U at ŝ),
m ≥ ŝ with equality only at Trump images. The statement proved is "the Ψ-minimal σ-minimiser
is not in k0_00 unless it is a Trump image": not `StratumKillMin` (which quantifies over ALL
minimisers) but its selected form `StratumKillSel` of A89 §9.3 with Ψ in place of Φ, which the
two top-level consumers accept in the same way. For uniqueness at ŝ: minimise Ψ over the non-image packings at ŝ
(compact by E.A36), apply the same theorem (Lemma SEL-Ψ's second clause), get a K0-FREE
non-image packing at ŝ, contradicting Lemma K0-FREE's equality clause. No DF-K0, no H1, no FJ,
no drain, no induction on 11 − k; the "well-foundedness for flat strata" of the brief is
Lemma PLATEAU (a plateau is a constant-Ψ feasible segment in the compact M(m); its end is a new
contact, a wall, or a K0-FREE point — A87's plateau-end data are the [M] instance).

**Axiom fed.** `stratum_kill` (C.K4TIER), k0_00 part, in a third form:
  StratumKillSel Ψ : ∀ s ∈ wnd, ∀ z, CfgPacking s z → (∀ s′ z′, CfgPacking s′ z′ → s ≤ s′) →
    (∀ z′, CfgPacking s z′ → Ψ z ≤ Ψ z′) → ¬InStratum k0_00 s z,
plus the ŝ-variant over non-images. Hypotheses added: global σ-minimality (as `StratumKillMin`)
and Ψ-minimality among minimisers (new). Consumers: `s_eleven_ge_of_sel` / `s_eleven_unique_of_sel`
— one `obtain` each from `IsCompact.exists_isMinOn` (A89 S1–S4, with Ψ continuous: d_c is a
min over the closed square of a continuous function, S2). New Lean obligations beyond A89's
list: (N1) Fact A as a lemma on the row family (affine in centres — the rows are already
polynomial in `(c, t)`; the statement is that the centre-degree is ≤ 1, `ring_nf`-checkable);
(N2) Lemma CLUSTER (finite induction over rows, each affine with nonnegative slope or positive
margin); (N3) Lemma K's rate formulas (a `nlinarith`-sized computation per case); (N4) the
depth function `d_c` and its equivalence with `int Q ∩ (0,1)² ≠ ∅` (uses `mem_interior_iff_uv`);
(N5) ¬RES(4) — the open residue, which if it lands as a certificate tree needs the same
`classKilledAt_of_tree` consumer with SelForm leaves as K0-ROT/TF-U (A86 `Composition.lean`).
Lemma K0-FREE and its dependency (k1_00's tree) are unchanged.

**Restricted-form pricing.** ¬RES(4) is the residue. Two ways to pay: (i) as a SelForm (C)
leaf in A85's k0_00 tree: at a node with all squares localised, test whether eight intruder
boxes can be anchored — box-level reachability of monotone contact chains to the far walls in
both axes; free at deep nodes, silent at the frontier (the 3 free squares can be any column's
middle), i.e. **no effect on A85's measured price (3 200–7 000 CPU-h)**, the K0-ROT / TF-U
verdict; (ii) as a direct finite geometric theorem on frames (four ≥ 3-square wall-to-wall
contact chains in [0, ŝ]² through eight intruders), a census of the kind A47 did for spanning
chains — unpriced [C]; the T3 data (every K0-BLOCKED flow exits by a blocker sliding away, and
the blocker's cluster is measured un-anchored at the exit, `t3_report.md`) say the frame is
absent from every basin the search visited, which is evidence, not a proof.

## 7. [M] What T3 measured (`attempts/A90-nocrit-blocked/notes/t3_report.md`, Opus chore)

* **Exit events, 520/520 re-run bitwise** (the seed stream needs `selftest()`'s pool priming
  first — `t3_90.prime_pool`). At the last K0-BLOCKED point the sliding blocker is the
  NON-DEEPEST intruder **520/520**; its depth sits on the 1e-9 tolerance floor (median 1.0e-9,
  max 4.3e-3); 398/520 are rattlers at that point (already slid clear). RETREATABLE by a
  cardinal translation **508/520** (507 of them with the singleton cluster), 511/520 with
  (1,1); not flush-locked (LOCK (b) LP) 515/520; MENU-unlocked 100/108 where MENU applies.
  LOCK and RETREATABLE never both hold. The 12 non-retreatable exits: each has exactly one
  blocking vertex-on-edge contact, a 3–4-square cluster wall-anchored in all 12 (RES holds for
  that blocker), and the flow's actual exit motion is a coordinated 9–11-square SQP step in
  all 12 (Q the sole mover in 0/520); in 10 of 12 the exit is the tolerance crossing of a
  continuously vanishing depth. **Reading:** the residue is a MOTION-CLASS gap, not a locking
  gap — single-square rigid translation certifies 98 % of the exits; the rest need the
  cluster/container to move together (remark (4) of §3.3: rotations and coordinated motions
  would shrink RES further).
* **The 4 K0-BLOCKED non-FJ endpoints:** RES(z) holds at 2 (both s0380 points), fails at 2
  (s0076, s0259: two retreatable non-deepest intruders each). The certified Gordan direction
  decreases a non-deepest intruder's depth at **4/4** (at s0380-2nd all four corners shed
  their second intruder at once) — so RES is a genuine extra condition, not implied by
  "K0-BLOCKED and not FJ", and Gordan's 34-coordinate motion does what a translation cannot.
* **Trump canary: critical (cone residual 0.0, m_active 42, rank 34), TL 2-crowd locked, not
  excluded by RETREAT.** K(sq4) = {e_y}: argmin set {(0, 0.8445), (0.8445, 0.8445)} — case (Y)
  as §5 predicts; K(sq6) = {e_x} (argmin (0.8317, 0.6452), case (X) — not corner-type as §5
  guessed; the conclusion is unchanged). C_{e_y}(sq4) = {0,1,2,3,4,7,8} wall-anchored on the
  floor; C_{e_x}(sq6) = {5,6,9,10} wall-anchored on x = s. sq4 LOCK (b)-locked by a
  self-stress; sq6 MENU-locked by its far-side contact with sq4 (closing rate −0.261 under the
  flush-ward rotation). RES(Trump) = true. **PASS.**
* **BLIND hunt: 0/167 obstructions.** Loadable sets by per-row LP; unloadable-square counts
  |U| ∈ {0..7} (median 3); deficient corners D ∈ {3, 4}; **70/167 points have |U| < D** —
  Lemma BLIND's budget is short outright; for the other 97 the repositioning search never
  produced a valid packing with any corner's occupancy raised (every "closer" configuration
  is infeasible: overlap ≈ 4.7e-2, σ grown to 4.7–4.9). Heuristic, not a proof; the 17 FJ
  endpoints of k0dir87 have no stored z (data gap, ~50 min replay). [F] The counting half is
  a hard fact and suggests the shape of an FJ-form argument at these cores: the loaded
  skeleton of a k0 FJ point consumes 4–11 squares (median 8), leaving too few blind squares
  to double all four corners — but loaded squares may intrude corners too, so it is not a
  theorem.

## 8. Obligations ledger

| # | item | status |
|---|---|---|
| A90-O1 | Lemma BLIND; FJ form of NOCRIT is not the right statement; brief's load-counting route closed | [T] §2 |
| A90-O2 | Lemma K (retreat trichotomy, exact rates), Lemma CLUSTER (affine feasibility), Lemma SEL-Ψ | [T] §3.1–3.3 |
| A90-O3 | Theorem NOCRIT-SEL: at the Ψ-minimal minimiser every intruder is anchored in each cardinal retreat direction | [T] §3.3 |
| A90-O4 | Closed cases: rattlers (a), pressed intruders, JAM-0 partner (ii), pocket (K0-REUSE) | [T] §3.4 |
| A90-O5 | Lemma COL (≥ 3-square columns for m ≥ 1 + 2√2; ghost regime below), Lemma PLATEAU (well-foundedness) | [T] §4.2–4.3 |
| A90-G1 | ¬RES(4): no Ψ-minimal σ-minimiser at side ≤ ŝ is a frame (four anchored corner crowds) | **OPEN** — the exact residue; realised at ONE corner by Trump; no counting proof; price = SelForm leaf (silent at A85's frontier) or a frame census [C] |
| A90-O6 | Canary: Trump critical, TL 2-crowd locked, not excluded (RES(1) holds at TL) | [T] §5; [M] T3 |
| A90-O7 | T3 empirical checks under these definitions | [M] §7, `attempts/A90-nocrit-blocked/notes/t3_report.md` |
| A90-G2 | retreat by rotations / coordinated cluster motions (shrinks RES; 12/520 exits need it) | [C] |
| A90-O8 | Lean-readiness: StratumKillSel Ψ + N1–N5 | note §6, no `lean/` edits |
