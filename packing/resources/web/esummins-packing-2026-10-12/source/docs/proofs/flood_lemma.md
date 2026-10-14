# The Flood Lemma, second attempt: Lemma SNAP (the η-disturbance drain), the simultaneous move set as one static census (FLOOD-T), and the exact stall (CELL-INTERLOCK) — A101, 2026-09-05

Target (A101 BRIEF): T1 Lemma SNAP — a near-axis square within η of a completable cell snaps
into it at the same side unless the cell is strictly crowded; the swept region, simultaneous
snaps, the box-level (T) leaf and its yield on A57's witness holes. T2 Theorem FLOOD under the
strict convention and the simultaneous move set (ALIGN, cell TELEPORT, WALL-SLIDE, corner
exchange), or the exact stall, with the side threshold from A87's floor sweep. T3 composition and
Lean-readiness. Labels: [T] proved, [S] routine given cited items, [M] measured
(`attempts/A101-flood-lemma/{code,results,logs,notes}`, two second-scale read-only scripts), [F]
finding, [C] open. Conventions: `exchange_lemma.md` (A98: cells, Young diagrams, N(D), X(D),
Lemmas TWO, FLOOD-D, FLOOD-M, X, CAP, RELEASE-CL, EXPOSE, INTERLOCK), `slot_crowds.md` (A94: slot
frame, μ_p, d_p, Lemma CONT, SLOT-CROWD, SLOT-SLIDE, usable slots), `k0_route.md` (A85: K0-FREE,
K0-WIDEN, `teleport_packing`), `k0_blocked_side.md` (A92: SLIDE, Theorem N, CEIL),
`nocrit_k0_blocked.md` (A90: corner frame, Lemma K, CLUSTER), A87 `notes/degen87.md` (the
simultaneous greedy, the tangency law), A85 `results/strict85.json` (strict convention), A96
`notes/pocket96.md` (pocket exemption yield). ŝ = 3.877083590022814, s0 = 969271/250000, window
W = [3.82, ŝ]. Fact (A98 §1): closed squares Q, R with disjoint interiors satisfy R ∩ int Q = ∅.

## 0. Verdict

> **T1 — Lemma SNAP holds, and its sound form is the DESTINATION form (§1.1, Lemma SNAP-D):**
> a square Q within η of a lattice cell C (any tilt, in fact) can be replaced by the exact cell
> square at the same side iff no OTHER square meets the open cell int C. The swept region of the
> brief is NOT needed for soundness — a packing is a configuration, not a motion (Lemma FLOOD-M),
> and the physical align-and-slide can even dig into a backing pin to second order (§1.2, remark) —
> but it is given explicitly and is contained in the η-disturbance ball B(C; η, θ) = C inflated by
> ε₀ = η + (cos θ + sin θ − 1)/2 ≤ η + θ/2 (Lemma SNAP-SWEEP, (i)). **Simultaneous snaps (ii) =
> Lemma MULTI (§1.4):** a set of squares moves onto a set T of target cells iff the cells of T are
> pairwise interior-disjoint (automatic inside one corner lattice; NOT across lattices below side 4:
> BL(2,0) and BR(0,0) overlap) and no UNTOUCHED square meets any int C ∈ T — the moving squares may
> crowd each other's targets freely, which is exactly why the one-at-a-time greedy stalls (the
> record's squares 4 and 5 each block the other's snap by 10⁻⁴) and the joint move certifies.
> **The dichotomy (iii) is sharper than "snap or crowded" (§1.3, Lemma SHELL):** if Q has tilt θ
> and centre within η (L∞) of C's centre and R ≠ Q meets int C, then R's certified SAT penetration
> depth into C is ≤ √2·ε with ε := η + 1/2 − 1/(2(cos θ + sin θ)) ≤ η + θ/2, and — at a corner cell
> or an unclipped completable slot of a pinned class (Lemma CONT applies) — R's corner-frame depth
> d_C(R) ≤ (1 + √2)ε. So the residue after SNAP is not "crowded cells" but "cells crowded ONLY by
> grazers of depth O(η + θ)": the tangency law of A87/degen87 (a 10⁻⁸ nick beside a 6·10⁻⁶
> disturbed square is not a block) is the θ, η → 0 case, now a theorem. **Composition with SLIDE
> (Lemma SNAP-SIDE, §1.5):** at a k0 corner (modulo K0-O1) or a usable slot of k5_11/k5_16
> (unconditional), an η-disturbed square at side m forces m ≥ ŝ′_C − (1 + √2)ε — in the window a
> disturbance is possible only within (1 + √2)ε of the extension window's top; Trump's upright
> at BL(0,2) (η = 0.0326, crowded by sq7 at 0.016 ≤ (1 + √2)·0.0326 = 0.079; extension k6_07 open,
> ŝ′ = 3.827) is consistent. **Leaf (T) = SNAP-T (§1.6):** destination form — a node box for one
> square inside B(C; η, θ) with every other non-pin box's shadow missing int C (padded for the
> window) is a free logic kill into S ∪ {C}; simultaneous version for stacked cells; no swept
> region. **Yield on A57 [M, `snap_yield101`]: silent.** The η-ball population is pocket96's pocket
> population (all boxes within (0.01, 1°) of a cell centre are at k5_16's BR(1,0)/BL(1,0)/BL(1,1),
> 53 holes of 5 500 in pocket96's population, 73 over all A57 groups; 31 at usable cells), and the
> leaf needs the OTHER five non-pin squares localised away from int C, which no A57 node provides
> (one interior square conditioned, four or five free) — the existential-filter law of A89–A98,
> once more. The holes' actual pattern is FLUSH, not η-disturbed: within 0.01 of a lattice
> coordinate in ONE axis at tilt ≤ 1° there are 160 k5_11 holes against a pin column/row and 97
> k5_16 holes against a usable cell's row/column (`results/snap_yield101.json` `flush`): squares
> resting against a pin and displaced ALONG it — for those the destination criterion is the same
> and the leaf is equally silent. **Zero FAIL nodes flip**, as for pocket96 and EX.
>
> **T2 — Theorem FLOOD: not proved; the simultaneous move set is characterised EXACTLY and the
> stall is measured on the corpus.** [T] **Lemma FLOOD-T (§2.1):** every static move of the
> simultaneous set (ALIGN, cell TELEPORT, TELEPORT_FREE, full WALL-SLIDE, the static Young flood
> at any corner, and their simultaneous combinations) is ONE multi-teleport onto a pairwise
> interior-disjoint set T of lattice cells of ANY of the four corner lattices, and it exists iff
> X(T) := N(T) − |T| ≤ 0 (N(T) = #squares meeting int T) — Lemma FLOOD-D with "Young diagram at one
> corner" replaced by "any disjoint cell set across all four lattices". A packing converts to k ≥ 1
> by the static simultaneous set iff some T containing a corner cell has X(T) ≤ 0. **The exact
> stall is CELL-INTERLOCK (§2.2):** X(T) ≥ 1 for every pairwise-disjoint T containing a corner
> cell; it implies A98's INTERLOCK (Young T's are special cases) so RES-CI ⊆ RES-X. Below side 4
> |T| ≤ 9 (Lemma NINE) and the corner block has X = 2 (CAP), so the census is finite: min over
> 2¹¹ movable sets of (|S| − max independent cell set), exact. [M, `cellflood101`, interval-
> certified at tol 10⁻⁹ and 10⁻⁶] **record_s0115 (3.98548) is CELL-INTERLOCKED at BL and BR:
> X_min = 1 over ALL disjoint cell sets of all four lattices (no free cell anywhere, no
> single-meeter cell, both tolerances) — cross-corner helpers do not rescue the interlock; it
> converts at TR and TL (X = 0 with T = {TR(0,0), TR(0,1)} / {TL(0,0), TL(1,0)}, the nick corners).
> Trump: X_min = 1 over EVERY nonempty T of non-exact cells (argmin BR(2,0), two meeters) — rigid;
> CANARY PASS.** Degen87's 6/8 dead classes are the TR/TL conversions plus side-≥-4 rows. **Side
> threshold [M, k0dir2_87 floor sweep, running]:** lowest strictly K0-BLOCKED side found at depth
> floor δ = 10⁻⁶: **4.0000016** (300/300 seeds blocked at best, min over seeds), at δ = 10⁻⁴:
> **4.000023** (291 seeds, in flight; floors 10⁻³, 10⁻² queued), against the exact record at
> δ ≤ 1.7·10⁻⁸: 3.98548. So m*(δ) is FLOOR-DEPENDENT — ≤ 3.9855 for δ ≤ 1.7·10⁻⁸, ≈ 4.000 for
> δ ≥ 10⁻⁶ on 591 seeds — and in every case ≥ ŝ + 0.108. FLOOD in the form "strictly
> K0-BLOCKED(δ) ⇒ converts / ⇒ side ≥ 4 − o(1)" is supported, not proved; what the theory delivers
> below side 4 is the quantitative link of Lemma SHELL: **K0-BLOCKED(δ) has no η-disturbed corner
> square with (1 + √2)(η + θ/2) < δ** (§2.4, Corollary OFFSET) — every deepest intruder of a
> strictly blocked corner is off its slot by ≥ δ/(1 + √2) in position or ≥ 2δ/(1 + √2) in tilt.
> The dynamic moves (partial slides, RELEASE retreats, the corner exchange's rigid re-fit) are
> outside the static census; degen87 tried them on the record's BL/BR: none fires [M].
>
> **T3 — composition (§3).** FLOOD-T is a ∀-packings (T)-leaf family for every tree, k0 and
> pinned alike (pins untouched: T avoids pin interiors), no selection, no criticality; if
> CELL-INTERLOCK exclusion held below ŝ it would discharge k0_00's `stratum_kill` piece in the
> PLAIN form modulo K0-O1-ALL exactly as A98 §8 (the flood output is a census class killed by the
> k ≥ 1 campaigns); the uniqueness clause needs displacement < r_B. **It removes nothing today**
> from the protected tier (A100: 3 500–4 200 CPU-h) or A57: SNAP-T/FLOOD-T are silent at every
> node whose free squares are unlocalised. Lean (§3.2): SNAP-D IS `teleport_packing`
> (Selection.lean) at the cell centre; MULTI is a Finset fold of it with the rational cell–cell
> SAT gap max(|dx| − 1, |dy| − 1) ≥ 0; SHELL is a finite lemma in the u/v coordinates
> (`mem_interior_iff_uv`): the axis box K = [c − a, c + a]², a = 1/(2(cos θ + sin θ)), lies in Q,
> and a square interior-disjoint from K is separated from C along one of C's axes by ≥ −ε or along
> one of its own by ≥ −√2ε; SNAP-SIDE composes with A93's `SlabKill`/`ShellKill` interface through
> Lemma SLOT-SLIDE's d₂ ≥ ŝ′ − m. Chip A101 on K0.RESN; residue RES-CI recorded.

## 1. T1 — Lemma SNAP

### 1.1 Setting and the destination form

Packing P at side m: eleven closed unit squares in [0, m]², pairwise interior-disjoint. Lattice
cells: for a corner c and i, j ≥ 0 with i + 1 ≤ m, j + 1 ≤ m, the cell c(i, j) is the closed
unit square at offsets (i, j) from c along c's walls (BL(i, j) = [i, i+1] × [j, j+1], the other
corners by the D4 map; at s0 the cells are the census slots α + β s0). A square Q of P is
**η-disturbed at C** (η ≥ 0, tilt θ ∈ [0, 45°]) if |c_Q − c_C|_∞ ≤ η and tilt(Q) = θ; C is
**crowded** (strictly: open interiors) if some square R ≠ Q of P meets int C.

**Lemma SNAP-D [T].** Let Q ∈ P and C a lattice cell inside the container, Q η-disturbed at C
or not. P′ := P with Q replaced by C is a packing at side m iff no square R ≠ Q of P meets int C.
If C is a completable slot of a Young class S whose pins P contains and S ∪ {C} is dead on a
window containing m (A94 §1.2), then P does not exist.

*Proof.* C ⊆ [0, m]² by "inside the container"; C is interior-disjoint from every R ≠ Q iff
int C ∩ int R = ∅ for all such R (closed squares; the Fact of A98 §1). This is `teleport_packing`
(Lean, hypotheses `hbox`, `hfree`) with Q's index as the teleported one. The second clause is
Lemma SLOT-CROWD's proof: P′ contains the pins of S ∪ {C}. ∎

Remarks. (a) The hypothesis "η-disturbed" plays no role in soundness: ANY square is a valid
filler of a free cell (K0-FREE, TELEPORT). What the disturbance buys is §1.3–1.5. (b) "Strictly
crowded" is the exact statement int R ∩ int C ≠ ∅ (depth > 0); the lab's certified conventions
(depth > 10⁻⁹ exact, > 10⁻⁶ strict) are search-side bars, and a move accepted under a bar is
sound only if the exact certificate of the destination passes — degen87's design (its final
certificate is the only load-bearing object) is the correct one, and Lemma SHELL below says WHY
the bar never bit on the record (the only blockers of a disturbed square's cell are grazers).

### 1.2 The swept region — Lemma SNAP-SWEEP ((i) of the brief)

Let Q have centre c and tilt θ ∈ [0, 45°], h(θ) := (cos θ + sin θ)/2 (its half-extent along
either axis), and let C be a cell with |c − c_C|_∞ ≤ η. Define the snap motion as the rotation
of Q about c to tilt 0 followed by the translation of the axis-aligned square Q₁ := [c − 1/2,
c + 1/2]² to C, and the **swept region** S(Q, C) := (rotation sweep) ∪ (translation sweep).

**Lemma SNAP-SWEEP [T].** (i) The rotation sweep is contained in the axis box [c − h(θ), c +
h(θ)]² (the bounding box of Q itself), and the translation sweep is the axis box spanned by
Q₁ ∪ C; hence S(Q, C) ⊆ B(C; η, θ) := C inflated by ε₀ := η + h(θ) − 1/2 = η + (cos θ + sin θ −
1)/2 ≤ η + θ/2 (θ in radians) on every side — the **η-disturbance ball**. (ii) If a square R
meets S(Q, C) then R meets B(C; η, θ); if R is interior-disjoint from Q then R meets B \ int Q,
the shell of width ≤ 2ε₀ around C.

*Proof.* h is decreasing on [0, 45°] (h′ = (cos θ − sin θ)/2 ≥ 0 read from 45° down), so every
intermediate square Q_φ, φ ∈ [0, θ], has bounding box [c − h(φ), c + h(φ)]² ⊆ [c − h(θ), c +
h(θ)]². The translation sweep of an axis box along a straight segment is the axis box spanned by
its endpoints. Both lie in C inflated by max(η + h(θ) − 1/2, η) = ε₀. (ii) is immediate. ∎

Remark (why the motion is not used for soundness). Q η-disturbed at a cell backed by an exact
pin P (predecessor cell) satisfies Q ∩ int P = ∅ but may poke past P's edge line above P's top
by O(ηθ) (a counter-clockwise tilt with its leftmost vertex above y = 1); rotating about the
centre then swings the near-vertical left edge into int P. A path avoiding the pins exists
(translate first, by η, then rotate), but no path is needed: Lemma FLOOD-M / SNAP-D decide by the
destination. The swept region's only role is (ii) — the box-level localisation of a blocker —
and Lemma SHELL does that job more sharply.

### 1.3 The shell bound — Lemma SHELL ((iii) of the brief, sharpened)

Put a(θ) := 1/(2(cos θ + sin θ)) (the half-side of the largest axis-aligned square centred at c
inside a unit square of tilt θ: its corner (a, a) satisfies a(cos θ + sin θ) = 1/2) and

  ε = ε(η, θ) := η + 1/2 − a(θ) ≤ η + θ/2 − 3θ²/4 ≤ η + θ/2.

**Lemma SHELL [T].** Let Q be η-disturbed at C with tilt θ, and let R be a closed unit square
interior-disjoint from Q with int R ∩ int C ≠ ∅ (a crowder of C). Then:

 (a) [SAT form, any setting] the SAT penetration depth of R into C — the least overlap of the
     projections of R and C onto the four edge normals of the two squares, the quantity
     degen87/strict85 certify — is at most √2·ε; in particular at most ε along C's own axes.
 (b) [corner-frame form] If moreover R ∩ R_C = ∅ where R_C := {x′ < 0, y′ < 1} ∪ {y′ < 0, x′ < 1}
     in C's slot frame (true for every non-pin square when C is a corner cell — the walls — or an
     unclipped completable slot of a class whose pins P contains: Lemma CONT), then the
     corner-frame depth d_C(R) = 1 − min_{q ∈ R} max(q′_x, q′_y) satisfies d_C(R) ≤ (1 + √2)ε,
     provided ε ≤ 1/4.

*Proof.* Work in C's frame, C = [0, 1]², c = c_Q ∈ [1/2 − η, 1/2 + η]². The axis box K := [c −
a, c + a]² lies in Q: a point p with |p − c|_∞ ≤ a has |(p − c)·e| ≤ a(|cos θ| + |sin θ|) = 1/2
for each edge normal e of Q, so p ∈ Q. Hence K ⊇ [ε, 1 − ε]² =: K₀ (c − a ≤ 1/2 + η − a = ε and
c + a ≥ 1 − ε), and int K₀ ⊆ int Q, so R ∩ int K₀ = ∅.
(a) K₀ and R are closed convex sets with disjoint interiors, so they are separated by a line
parallel to one of the edges of K₀ or of R (SAT for two convex polygons: some edge normal of one
of them separates). Along an edge normal of K₀ — an axis — R lies in {x ≤ ε} or {x ≥ 1 − ε} or
the same in y, so its overlap with C's projection [0, 1] is ≤ ε. Along an edge normal e of R
(angle φ): the projection of K₀ onto e is an interval of half-width a₀(|cos φ| + |sin φ|),
a₀ = 1/2 − ε, and the projection of C onto e is the concentric interval of half-width (|cos φ| +
|sin φ|)/2, so C's projection exceeds K₀'s by ε(|cos φ| + |sin φ|) ≤ √2 ε on each side; R's
projection, disjoint from K₀'s, overlaps C's by at most √2 ε. The SAT depth is the minimum over
the four normals of the overlap, hence ≤ √2 ε (and ≤ ε whenever the separating normal is an
axis).
(b) Let q ∈ R with max(q_x, q_y) < 1 − (1 + √2)ε; we derive a contradiction. Since R misses R_C,
q_x ≥ 0 and q_y ≥ 0 (a point with q_x < 0 has q_y ≥ 1, excluded). Since q ∉ int K₀ and
max(q) < 1 − ε, q_x ≤ ε or q_y ≤ ε; say q_y ≤ ε (else swap axes). Let w(x) be the length of R's
vertical chord at abscissa x (a concave function on R's horizontal support [x_L, x_R], x_R − x_L
= 2h(φ) ≥ 1, maximum ≥ 1 since the vertical chord through R's centre has length 1/cos φ or
1/sin φ ≥ 1). For x ∈ I := (ε, 1 − ε) the chord avoids int K₀, so it lies in {y ≤ ε} or in
{y ≥ 1 − ε}; for x < 1 it also lies in {y ≥ 0} (R misses {y < 0, x < 1}); chord endpoints vary
continuously in x, and the chord at x = q_x (if q_x ∈ I) contains q with q_y ≤ ε, so every chord
at x ∈ I ∩ [q_x, ·) or (·, q_x] connected to it through I lies in [0, ε] and has w ≤ ε. Let x* be
an abscissa of maximal chord (w(x*) ≥ 1 > ε, so x* ∉ I). Case x* ≥ 1 − ε: concavity between x_L
(w = 0) and x* gives w(x) ≥ (x − x_L)/(x* − x_L) ≥ (x − x_L)/√2 on [x_L, x*] ⊇ [q_x, 1 − ε),
where also w ≤ ε; so x − x_L ≤ √2 ε for all x < 1 − ε, i.e. x_L ≥ 1 − (1 + √2)ε, and q_x ≥ x_L
≥ 1 − (1 + √2)ε — contradicting max(q) < 1 − (1 + √2)ε. Case x* ≤ ε: symmetrically x_R ≤ (1 +
√2)ε, so R's horizontal support has length ≥ 1 and x_L ≤ (1 + √2)ε − 1 < 0: R has points with
x < 0, which (R misses R_C) have y ≥ 1. R's leftmost vertex L = (x_L, y_L) has y_L ≥ 1, and its
lowest vertex B = (x_B, y_B) has y_B ≤ q_y ≤ ε; L and B are adjacent vertices (tilt φ ∈ [0, 45°];
for φ = 0 take the lower-left corner for both roles) joined by an edge with |Δx| = sin φ, |Δy| =
cos φ, so cos φ ≥ 1 − ε, sin φ ≤ √(2ε − ε²), and x_B = x_L + sin φ ≤ (1 + √2)ε − 1 + √(2ε) < 0
for ε ≤ 1/4 — then B ∈ {x < 0, y < 1} = part of R_C, contradiction. (If q_x ≤ ε instead of q_y
≤ ε, exchange the axes.) ∎

[M, `results/cellflood101.json` `shell_check`] 2·10⁵ random (Q, R) pairs, η ∈ {10⁻³, …, 0.1},
θ₀ ∈ {0.5°, …, 10°}: max SAT depth / (√2 ε) = 0.768 over 1 485 crowders; max d_C / ((1 + √2)ε) =
0.409 over the 532 crowders satisfying CONT. Both bounds hold with slack; (a) is within 25 % of
sharp.

**Corollary SNAP-DICHOTOMY [T] ((iii)).** For Q η-disturbed at C with tilt θ: either P′ = (P with
Q ↦ C) is a packing at side m (Lemma SNAP-D), or C is crowded and EVERY crowder is a grazer: SAT
depth ≤ √2 ε(η, θ) (and d_C ≤ (1 + √2)ε under CONT). So "snap or crowded" is a dichotomy, and the
residue after SNAP is the set of cells whose disturbed owner is accompanied by a grazer of depth
≤ √2 ε — nothing deeper can coexist with a disturbed owner. The tangency law: at the record's TR
corner sq6 is 6.1·10⁻⁶ off TR(0,1) at tilt 1.9·10⁻⁶ deg (ε = 6.1·10⁻⁶ + 1.7·10⁻⁸), so any crowder
of TR(0,1) is a grazer of depth ≤ 8.7·10⁻⁶; and sq6's own nick into the NEIGHBOURING cell TR(0,0)
(1.7·10⁻⁸) is bounded by SNAP-SWEEP (i): a square whose bounding box overhangs a neighbouring
cell by ≤ ε₀ penetrates it by ≤ ε₀ = 6.1·10⁻⁶. [F] The lab's "strict convention" tol = 10⁻⁶
counts a crowder as a block iff its certified depth exceeds 10⁻⁶; by SHELL an η-disturbed square
with √2 ε(η, θ) < 10⁻⁶ can only be accompanied by crowders BELOW the bar — the strict count then
sees the cell as singly met and proposes the snap, and the exact certificate accepts it iff the
grazer's depth is exactly 0 (a tangency) or the grazer itself moves (Lemma MULTI). That is the
whole mechanism of degen87's record run.

### 1.4 Simultaneous snaps — Lemma MULTI ((ii))

**Lemma MULTI [T].** Let M = {(Q₁, C₁), …, (Q_r, C_r)} with distinct squares Q_i ∈ P and lattice
cells C_i inside the container. The configuration P_M := (P \ {Q_i}) ∪ {C_i} is a packing at
side m iff (1) the cells C_i are pairwise interior-disjoint and (2) no square of P outside
{Q₁, …, Q_r} meets any int C_i. Condition (1) is automatic for distinct cells of ONE corner
lattice and fails across lattices exactly when |Δx| < 1 and |Δy| < 1 between the two cell
centres (below side 4: BL(i, j) and BR(i′, j) overlap iff i + i′ ∈ {2, 3}, etc.).

*Proof.* P_M's squares are the untouched ones (pairwise interior-disjoint, in the container),
the cells (in the container; pairwise interior-disjoint by (1)), and cell–untouched pairs
(interior-disjoint by (2)). Necessity is the same list read backwards. Two axis-aligned unit
squares have SAT gap max(|Δx| − 1, |Δy| − 1), rational. ∎

Consequences. (a) The moving squares Q_j may meet int C_i for j ≠ i: the near-cell neighbours of
a stack crowd each other's cells by O(η) (record: sq4 aligned alone overlaps sq5 by 10⁻⁴, sq5
alone overlaps sq4 by 7·10⁻⁹) and only the joint move certifies — degen87's finding 1 is this
lemma. (b) With Lemma SHELL: for a stack of η-disturbed squares Q₁, …, Q_r on cells C₁, …, C_r
of one lattice, every crowder of C_i is either one of the Q_j (a neighbour in the stack) or a
grazer of depth ≤ √2 ε; so the joint snap of the WHOLE stack fails only if a non-stack grazer
exists — the residue of a disturbed stack is a grazer, never an interlock of the stack with
itself. (c) For a class consumer: if P contains the pins of S, the C_i are unclipped completable
slots (in any order, with earlier ones as the predecessors of later ones), and S ∪ {C_i} is dead
on a window ∋ m for SOME i, then P does not exist (kills climb containment: K1).

### 1.5 Composition with SLIDE — Lemma SNAP-SIDE

**Lemma SNAP-SIDE [T].** Let P at side m ∈ [3.82, ŝ) contain an η-disturbed square Q at C with
tilt θ and ε = ε(η, θ) ≤ 1/(2 + √2), where either (k0) C is a corner cell and K0-O1 holds (Lemma
SLIDE in its joint form, A94 §3.4: d₂(c) ≥ ŝ − m), or (pinned) P contains the pins of S, C is a
usable unclipped completable slot of S with extension window top ŝ′_C (Lemma SLOT-SLIDE: d₂(C) ≥
ŝ′_C − m). Then

  m ≥ ŝ′_C − (1 + √2)·ε(η, θ)   (ŝ′_C = ŝ in the k0 case).

*Proof.* Q ⊇ K₀ = [ε, 1 − ε]², so μ_C(Q) ≤ ε and d_C(Q) ≥ 1 − ε > (1 + √2)ε ≥ d_C(R) for every
other meeter R (Lemma SHELL (b); CONT holds in both settings). So Q is the deepest intruder and
d₂(C) ≤ (1 + √2)ε; SLIDE / SLOT-SLIDE give d₂ ≥ ŝ′_C − m. ∎

Reading. In the window, an η-disturbed square at a dead-extension cell forces the side to within
(1 + √2)(η + θ/2) of the extension window's top: at G4 = 3.8325 (ŝ − 0.0446) no square is within
η = 0.018 of a corner slot at tilt ≤ 0.5°; at G2 (ŝ − 0.0155) none within 0.0064. Near-flush
ghosts are NOT a window phenomenon except in the top slab — the quantitative form of A92's "nicks
are bounded below by ŝ − m", now with the displacement of the OWNER rather than the depth of the
nick. Canary: Trump (m = ŝ) has one disturbed square, the upright sq4 at BL(0,2) with η = 0.03256,
θ = 0: (1 + √2)ε = 0.0786 ≥ d₂ = 0.01605 (sq7) ✓, and the extension trump5 ∪ {BL(0,2)} = k6_07 has
ŝ′ = 3.827 (partial window), bound m ≥ 3.748 — vacuous, as it must be at ŝ. The three slot corners
hold exact squares (η = 0) with no crowder (X = 0): the identity move. PASS.

### 1.6 The (T) leaf — SNAP-T, and its yield on A57's witness holes

**Leaf SNAP-T (definition).** Tree at side s (A57: s0; A96: parametric) for a class S with pins
P_S; node with boxes β_j (rect × tilt-interval) for some of the N non-pin squares. Fixed cell C =
an unclipped completable slot of S whose extension S ∪ {C} is dead on a window containing the
node's side range (A94 §1.2: usable). Test: (1) some box β_q lies inside the η-ball, i.e. every
pose of β_q is a square within η of C's centre at tilt ≤ θ₀ — OPTIONAL, see (3); (2) for every
other non-pin square j, shadow(β_j) ∩ int C^w = ∅, where C^w is C inflated by the window pad
w_C := (λ_max − 1)(|α_C|_∞ + 1 + √2/2) (Lemma K0-WIDEN's bookkeeping for a cell at slot α + βs,
|α|_∞ ≤ 5/2: at most 0.061 on the full window; 0 at fixed side); unlocalised squares have shadow =
everything. Verdict: no packing of the node exists (Lemma SNAP-D + SLOT-CROWD's kill; ∀-packings,
(T)-type, monotone in sub-boxes). (3) The box β_q is irrelevant to soundness: if at most ONE
non-pin shadow reaches int C^w the node is dead whatever that square's box is — SNAP-T is the
box-level Lemma SLOT-CROWD, and the η-ball hypothesis only names the natural filler.
Simultaneous version: cells C₁, …, C_r pairwise interior-disjoint (unclipped completable in some
order), at most r non-pin shadows reach ∪ int C_i^w and S ∪ {C_i} is dead for some i.

**Yield [M, `attempts/A101-flood-lemma/results/snap_yield101.json`, read-only over 488 witness
files of `attempts/A57-shadow-trees/certs/**`, 13 688 boxes = 5 500 holes + 8 185 undecided].**
(a) η-ball population (whole box within η of a cell centre in L∞, tilt range within θ₀ of 0 mod
90°, all 36 cells of all four lattices at the node's side): (0.01, 1°): 81 boxes, 73 holes, 31 at
usable cells, in 14 files; (0.02, 2°): 232 boxes, 184 holes, 72 usable, 26 files; restricted to
pocket96's population (G1 trees + epsgeo): 53 / 120 holes, 16 / 32 usable — all at k5_16's
BR(1,0) [k6_27, OPEN — unusable], BL(1,0) [k6_23], BL(1,1) [not completable for k5_16], plus a few
k5_11 boxes at TR(0,1)/BL(1,2) (not completable). This is pocket96's pocket population (32/46
holes at its tolerances; the difference is the population — my glob includes stale repairedPASS
witness files, slack/D2/L1/zonescan groups — and the centre-based L∞), i.e. ~1 % of the holes.
(b) The dominant near-lattice pattern is FLUSH, not η-disturbed: boxes within 0.01 of a lattice
coordinate in ONE axis at tilt ≤ 1° — a square resting against a pin column/row (k5_11: 160
holes against pins, 83 against clipped cells, 79 other; k5_16: 64 against pins, 97 against usable
cells, 60 against unusable ones), displaced ALONG the pin by 0.05–0.8 — exactly pocket96's
"near-flush against PIN squares". For those, Lemma SNAP-D's destination test is the same (the
cell they would slide into must be met by nobody else), so the leaf's condition is unchanged.
(c) The leaf's condition (2) fails at EVERY A57 node: the k5_11/k5_16 trees condition one
interior square (a Y-cell) plus, at depth 2, one more; the remaining four or five non-pin
squares are constrained only by the measure, their shadows cover int C, and the count of
reaching shadows is ≥ 4 ≫ 1. **Nodes flipped: 0 of 249 (pocket96's) / 0 over all groups.** The
one thing SNAP adds over pocket96 for A57 is that the consumer no longer needs a slack (δ_pin)
re-emission of the k6 kills — the snap lands EXACTLY on the cell and the existing 3·10⁻⁸-tolerance
k6 certificates apply — which turns pocket96's "0 at the emitted tolerance" into the same 0 at
any tolerance: the obstruction was never the tolerance, it is condition (2). Existential-filter
law (A89 §9, A90 §6, A91 §9, A98 §7): free at deep nodes, silent at the frontier; A57/A96 prices
unchanged.

## 2. T2 — Theorem FLOOD, the simultaneous move set, the exact stall

### 2.1 Lemma FLOOD-T: the static simultaneous set is one census

The moves of degen87/flood87 and the brief, restricted to those that place squares EXACTLY on
lattice cells: ALIGN (a disturbed square onto its cell), cell TELEPORT (the sole meeter of a cell
onto it), TELEPORT_FREE (any square onto an unmet cell), full WALL-SLIDE (an axis-aligned wall
square onto the nearest wall cell), the static Young flood (Lemma FLOOD-D: N(D) squares onto the
cells of D), and any simultaneous combination of them. Each replaces a set of squares by a set
of cells; call the target set T.

**Lemma FLOOD-T [T].** For a packing P at side m and a set T of lattice cells of any of the four
corner lattices, pairwise interior-disjoint and inside the container, with N(T) := #{Q ∈ P :
int Q ∩ int T ≠ ∅} and X(T) := N(T) − |T|: there is a packing P′ at side m consisting of the
11 − N(T) squares of P not meeting int T and N(T) cells of T (any N(T) of them) iff X(T) ≤ 0.
Every static move of the simultaneous set is of this form with T its target set. Consequently P
converts to a packing with an exact corner square (k ≥ 1) by the static simultaneous set iff
some pairwise-disjoint T containing a corner cell c(0,0) has X(T) ≤ 0; and P converts into a
packing containing the pins of a Young class S′ iff some such T ⊇ (cells of S′ not already exact)
has X(T) ≤ 0 with the exact squares of S′ untouched.

*Proof.* Lemma MULTI with M = (meeters of int T) → (any N(T) cells of T), condition (2) being
"no non-meeter meets int T" (true by definition) and (1) the hypothesis on T; if X(T) ≤ 0 there
are enough cells. Conversely a multi-teleport onto targets T′ ⊆ T needs every meeter of int T′
to move, so N(T′) ≤ |T′|. ALIGN, TELEPORT, TELEPORT_FREE, WALL-SLIDE are the cases |T| = 1 with
N(T) ∈ {1, 1, 0, 1} (WALL-SLIDE's destination cell must be free of others — degen87 checks
exactly that, and its partial slides are not cell placements); FLOOD-D is T = D Young. ∎

Remarks. (a) The moving squares' identities do not matter (teleport), only the count; the
"natural" filler (the nearest, the disturbed owner) matters for the displacement bookkeeping
(§3, the uniqueness clause) and for search heuristics. (b) Cells of DIFFERENT corner lattices
in one T are the new freedom over A98: below side 4 the four lattices are offset by m − 3 ∈
(0.82, 1) and a square can be a meeter of cells of several lattices; a free cell of ANOTHER
lattice pays for a crowder of the corner cell exactly as a free Young cell does (Lemma X's
increment: adding a cell met by n new squares changes X by n − 1). (c) Pinned classes: T must
avoid the pins' interiors (unclipped cells) if the pins are to stay; then FLOOD-T is the
generalisation of SLOT-CROWD's teleport to cell SETS.

**Lemma NINE [T].** At side m < 4 at most 9 pairwise interior-disjoint axis-aligned unit squares
fit in [0, m]². *Proof.* Pick δ ∈ (0, (4 − m)/3) and p_k := k(1 − δ), k = 1, 2, 3; every open
unit interval (a, a + 1) ⊂ (0, m) contains some p_k (the intervals (p_k − 1, p_k) cover [0, m − 1]
since p₁ < 1, p_{k+1} − 1 < p_k and p₃ > m − 1). The squares whose open x-extent contains p_k have
pairwise interior-disjoint open unit y-extents in (0, m), at most 3 of them (m < 4). ∎ So
|T| ≤ 9 in every census below side 4, and Lemma CAP (every square meets every corner's 3 × 3
block, X(block) = 2) bounds one family of T's; the census is finite.

### 2.2 The exact stall: CELL-INTERLOCK, and its measurement

**Definition.** P is CELL-INTERLOCKED at corner c if X(T) ≥ 1 for every pairwise interior-
disjoint set T of lattice cells (any lattices, inside the container) with c(0,0) ∈ T; CELL-
INTERLOCKED if so at all four corners. RES-CI := {K0-BLOCKED CELL-INTERLOCKED packings at side
m ∈ [3.82, ŝ)}.

[T] P fails to convert to k ≥ 1 by the static simultaneous set iff P is CELL-INTERLOCKED
(Lemma FLOOD-T). Young diagrams at c are special T's, so CELL-INTERLOCK ⇒ A98's static INTERLOCK
condition X(D) ≥ 1 ∀ D; hence **RES-CI ⊆ RES-X**, and it is the residue of a STRICTLY larger
move set (cross-lattice helpers, non-Young helper cells, simultaneous stacks). The dynamic moves
— partial wall slides, RELEASE-CL retreats of untouched squares, the corner exchange's rigid
re-fit (Lemma EXPOSE) — change the configuration and may unlock a later multi-teleport; the
reachable set under (static ∪ rigid) is not characterised here [C]; on the corpus none of them
fires where the static set stalls (degen87: 0 partial slides and 0 flood re-fits on the record's
BL/BR; A98 §6.3: no untouched square retreated out of a cell in any run).

**[M] The census (`attempts/A101-flood-lemma/code/cellflood101.py`, 11 s; interval-certified
"meets" at tol 10⁻⁹ and 10⁻⁶ on the exact rational poses, A87's certifier re-implemented verbatim;
X_min(c) = min over movable sets S ⊆ squares of |S| − MIS(cells all of whose meeters lie in S,
containing c(0,0), conflict = cell overlap), exact by enumeration of the 2¹¹ sets).**

| packing | side | corner n_meet (BL BR TR TL) | X_min per corner | argmin T | free / single-meeter cells |
|---|---|---|---|---|---|
| record_s0115, tol 10⁻⁹ | 3.98548 | 2 2 2 2 | **1 1 0 0** | BL: {BL(0,0)} (moved 0, 1); BR: {BR(0,0)} (2, 3); TR: {TR(0,0), TR(0,1)} (6, 7); TL: {TL(0,0), TL(1,0)} (4, 5) | none / none |
| record_s0115, tol 10⁻⁶ | 3.98548 | 2 2 1 1 | 1 1 0 0 | TR: {TR(0,0)} (7); TL: {TL(0,0)} (5) | none / TR(0,0), TR(0,1), TR(0,2), TL(0,0) |
| polish12/15/21/24, anchored0/1/2 | 4.0000001–4.107 | 2 2 2 2 (polish12 BL → 1 at 10⁻⁶) | not computed (side ≥ 4: 16-cell lattices, static flood vacuous, A98 §6.1) | — | free: none; single at 10⁻⁶: polish12 12 cells, polish21 5, anchored1/2 BL(0,1)+TL(0,1) |
| TRUMP, both tols | ŝ | 1 1 1 2 | 0 0 0 **1** (the three 0's are the identity: the exact slot squares) | TL: {TL(0,0)} (4, 6) | none / none |

**Readings.** (i) The record is CELL-INTERLOCKED at BL and BR: with every helper cell of every
lattice allowed, the best T is the bare corner cell with its two intruders — no free cell exists
anywhere in the packing (36 cells, all met), no single-meeter cell exists at the exact tolerance,
and every candidate helper costs ≥ 1 new square. The BL/BR interlock of A98 §5 (adjacent crowds
locked through the 4 − m = 0.0145 overlap of their arm cells) is therefore a stall of the FULL
static simultaneous set, not only of the corner-local flood. (ii) The record converts at TR and
TL because those corners are NICKED: T = {TR(0,0), TR(0,1)} with N = {sq6, sq7} — the same 2-cell
diagram A98's static census found (X = 0 at [1,1]); at tol 10⁻⁶ the nicks vanish and the corner
cells are singly met (strict85). Degen87's k = 7 is this conversion continued by further
multi-teleports (TL(0,1) ← sq8, TL(0,2), TL(1,0), TR(0,2)). (iii) **Trump is rigid: X_min = 1 over
EVERY nonempty set of non-exact cells** (argmin BR(2,0), met by two squares) — no multi-teleport
of any kind exists at ŝ, as uniqueness demands. CANARY PASS. (iv) Under the strict convention
(10⁻⁶) the record's TR/TL corners are singly met and Lemma K0-FREE applies directly (strict85);
the census confirms that the strict bar changes nothing at BL/BR.

### 2.3 The side threshold [M, `attempts/A87-drain-flow/results/k0dir2_87.jsonl`, in flight]

k0dir2_87 (A87 chore, running: `k0dir2_87.py run 300 1700`, floors 10⁻⁶, 10⁻⁴, 10⁻³, 10⁻²):
per seed, the lowest side reached by a directed descent CONFINED to K0-BLOCKED(δ) (every corner
met by ≥ 2 squares at certified depth ≥ δ), 300 seeds per floor from A85's pair census.

| floor δ | seeds | blocked at best | lowest σ_best_blocked | next four |
|---|---|---|---|---|
| 10⁻⁶ | 300 | 300 | **4.0000016** | 4.0000030, 4.0000030, 4.0000067, 4.0000125 |
| 10⁻⁴ | 291 (running) | 291 | **4.000023** | 4.000053, 4.000087, 4.000141, 4.000160 |
| 10⁻³, 10⁻² | queued | | | |

Against: the exact record at δ ≤ 1.7·10⁻⁸ (its TR/TL second depths 1.7·10⁻⁸, 8·10⁻⁹): 3.98548
(k0dir87), and strict85's six exact packings K0-BLOCKED(10⁻⁶) at 4.0000041–4.107. **So the
empirical threshold m*(δ) := inf{side of a K0-BLOCKED(δ) packing} is floor-dependent: m*(δ) ≤
3.98548 for δ ≤ 1.7·10⁻⁸, and no K0-BLOCKED(δ) packing below 4.0000016 is known for δ ≥ 10⁻⁶ (591
confined descents, all converging onto side 4 from above with the shallowest second intruder on
the floor — k0dir87's picture).** Every value is ≥ ŝ + 0.108. Whether m*(10⁻⁶) < 4 is not decided
by a search; the conjecture the sweep supports is m*(δ) ≥ 4 − o(1) as δ grows past the nick
scale, i.e. "a strictly blocked packing below side 4 needs a nick", which is what Theorem FLOOD
under the strict convention would say. Not a theorem here [C].

### 2.4 What is proved below side 4

**Corollary OFFSET [T] (from Lemma SHELL (b) at a corner cell).** In a K0-BLOCKED(δ) packing
(each corner met by two squares at corner-frame depth ≥ δ) no corner cell has an η-disturbed
square with (1 + √2)·ε(η, θ) < δ: the deepest intruder of every corner is displaced from the slot
centre by η ≥ δ/(1 + √2) − θ/2, or tilted by θ ≥ 2(δ/(1 + √2) − η). At δ = 10⁻⁶ this is
η + θ/2 ≥ 4.1·10⁻⁷ — the strict convention excludes exactly the sub-nick disturbances; at δ = 0.3
(A92's certified Theorem S(0.3)) it is η + θ/2 ≥ 0.124 — the crowds A92's certificate kills have
no near-slot member at all (consistent with Theorem CEIL's near-diagonal pairs).

*Proof.* Apply SHELL (b) with CONT = the walls: the second intruder's depth is ≤ (1 + √2)ε. ∎

This is the exact content of "the η-disturbance drain" below side 4: a strictly blocked corner
cannot be a disturbed corner. It does not bound the side; Theorem CEIL/CAP/NINE-type counting
does not close FLOOD (A92 §2.2: the pair charge is ≤ 1 per corner, 4 < E(ŝ)); the mechanism the
brief names (removing the deepest intruder of the least-intruded cell releases the squares
anchored through it) is Lemma RELEASE-CL's dynamic clause, outside the static census, and on the
record it releases only slide-INS at BL/BR (A98 §3.2 (c)) which the census already prices.

**The pinned generalisation [T].** For P containing the pins of S at m ∈ W_T: replace "corner
cell" by "usable unclipped completable slot", CONT by Lemma CONT, K0-O1 by the extension kill;
Lemma FLOOD-T with T avoiding pin interiors, Lemma SNAP-SIDE (pinned), Corollary OFFSET (every
usable slot's deepest non-pin intruder is off the slot by ≥ (ŝ′ − m)/(1 + √2) − θ/2 — SLOT-SLIDE
makes δ = ŝ′_C − m). So the same statements climb the ladder (SLOT-CROWD's "every usable slot is
doubly met" plus "and its owner is not disturbed"); the stall is CELL-INTERLOCK with pins fixed.

## 3. T3 — composition and Lean

### 3.1 Composition

If CELL-INTERLOCK exclusion held below ŝ — "no K0-BLOCKED packing at m ∈ [3.82, ŝ) is CELL-
INTERLOCKED" — then for every packing at m < ŝ: K0-FREE (some corner singly met, needs K0-O1) or
FLOOD-T converts it at the same side into a packing containing the pins of a census class with a
nonempty skeleton (T ∋ c(0,0) exact; the class is the maximal Young part of the exact cells,
D4-canonicalised), killed on the window by K0-O1-ALL; so no packing at m < ŝ: `stratum_kill`
(k0_00) in the PLAIN form, hypotheses = K0-O1-ALL, no selection, no criticality, no tree (A98 §8
verbatim, with RES-X replaced by the smaller RES-CI). Uniqueness at ŝ: as in A98, delivered only
when the conversion's displacement is < r_B = 3/2000; a nick corner's 2-cell conversion moves
the disturbed owner by ≤ η + O(θ) and the crowder by ≤ 1 (the teleport is not small): the
uniqueness clause is NOT delivered by FLOOD-T's teleport form, only by the physical snap of an
η-disturbed stack with η + θ/2 < r_B and no teleported crowder — noted, not pursued.

Per class (SLOT-CROWD form): FLOOD-T with pins fixed is a (T)-leaf family for every pinned tree
(a node where the boxes prove X(T) ≤ 0 for some usable T is dead); with the protected tier's
shallow conditioning (A100: one cover square, then ladders) the free squares are unlocalised and
the leaf is silent, as SNAP-T is on A57 — **nothing removed from the 3 500–4 200 CPU-h tier or
from A57/A96 today.** What would change the price is a theorem, not a leaf: CELL-INTERLOCK
exclusion (item 1 of `residue_map.md` §8, now with the smaller residue) or its two-corner form
(item 3).

### 3.2 Lean-readiness (Skeleton / ThetaT conventions, A93's Crowd/Slide machinery)

* **SNAP-D = `teleport_packing`** (`Selection.lean` line 111: `CfgPacking m z → ∀ i c, c-slot box in
  the container → (∀ j ≠ i, interior-disjoint from slotBox c) → CfgPacking m (z with i ↦ slot c)`)
  at c = the cell centre `slotCentre m (corner, i, j)`; the class consumer is `class_kill` of
  the extension instantiated by the parametric window certificate (A94 §8, `ParamBridge`). No
  new lemma.
* **MULTI**: a Finset fold of `teleport_packing` over M, with the cell–cell rows `sat_squares` on
  exact rational axis-aligned poses (gap = max(|Δx| − 1, |Δy| − 1) ≥ 0, decidable in ℚ) and the
  cell–untouched rows by hypothesis (2); Lean shape `multi_teleport : CfgPacking m z →
  PairwiseDisjointCells T → (∀ j ∉ dom M, ∀ C ∈ T, IntDisj (z j) C) → CfgPacking m (z.update M)`.
  FLOOD-T is MULTI plus the counting `N(T) ≤ |T| → ∃ injection meeters → T` (Finset.card).
* **SHELL**: a finite geometric lemma in the u/v coordinates of `mem_interior_iff_uv`
  (`Attain.lean`): (1) the axis box K = [c − a, c + a]² ⊆ Q(c, θ) for a = 1/(2(cos θ + sin θ)) —
  four inequalities |a(±cos θ ± sin θ)| ≤ 1/2; (2) K₀ = [ε, 1 − ε]² ⊆ K when |c − c_C|_∞ ≤ η; (3)
  SAT for two closed squares with disjoint interiors gives a separating edge normal (A64's
  pull-back / `CaseSat.lean`'s separation); (4) the projection arithmetic of §1.3 (a). Part (b)
  (the chord argument) is heavier (concavity of the width function) — state it as the
  obligation `shell_mu : … → d_C R ≤ (1 + √2) ε` with the CONT hypothesis `R ∩ R_C = ∅` in the
  slot frame Φ_p of A94 §1.3, consumed only by SNAP-SIDE; the SAT form (a) is what the certifier
  conventions use and is `nlinarith`-sized after the four-case split.
* **SNAP-SIDE**: SHELL (b) + `slot_slide` (A94 §3, the JOINT-cluster form A93 T2 formalises) + the
  order "Q deepest" (d_C(Q) ≥ 1 − ε > (1 + √2)ε); consumer `ShellKill`/`SlabKill` of
  `Composition.lean` (K0.RESN's Lean interface) — the statement "no packing of class S at side m
  < ŝ′ − (1 + √2)ε has an ε-disturbed square at a usable slot" is a `ClassKilledAt`-shaped
  clause on a sub-hypothesis, one lemma per usable slot.
* **CELL-INTERLOCK exclusion** (if it lands): `cellflood_kill : CfgPacking m z → K0Blocked z →
  ∃ T, X(T) ≤ 0` — the leaf `exchange_flood` of A98 §8 (E5) with the cell-set quantifier; the
  replay certificate of a conversion is the final 11-square configuration with the exact cells,
  checked by `sat_squares` (V.CASE), as for flood87/degen87.

## 4. Canaries

* Trump, exact 60-digit data, both tolerances: X_min = 1 over every nonempty set of non-exact
  cells (§2.2) — no multi-teleport exists; the disturbed upright sq4 (η = 0.0326 at BL(0,2)) is
  crowded by sq7 at depth 0.01605 ≤ (1 + √2)·0.0326 (SHELL (b) ✓) and its extension k6_07 is open
  at ŝ (ŝ′ = 3.827), so SNAP-SIDE is vacuous; TL's crowd {4, 6} at 0.155/0.168 is not a
  disturbance of anything (nearest cells 0.10–0.44 away, tilt 40.18°). PASS.
* record_s0115: CELL-INTERLOCKED at BL/BR, converts at TR/TL — agrees with A87 (depth-1
  exchange), A98 (static census), degen87 (global degeneration), strict85 (K0-FREE at 10⁻⁶).
* SHELL: 2·10⁵ random pairs, both bounds hold (ratios 0.77 / 0.41).

## 5. Obligations ledger

| # | item | status |
|---|---|---|
| A101-O1 | Lemma SNAP-D (destination form = `teleport_packing`), SNAP-SWEEP (i: sweep ⊆ η-ball), MULTI (ii), SHELL (iii, SAT and corner-frame forms), SNAP-DICHOTOMY, SNAP-SIDE, Corollary OFFSET | [T] §1, §2.4 |
| A101-O2 | SNAP-T leaf (destination form; simultaneous version); yield on A57's witnesses | [T]+[M] §1.6 — 0 nodes flip (silent; existential-filter law) |
| A101-O3 | Lemma FLOOD-T (the static simultaneous set = one multi-teleport census over all four lattices), Lemma NINE, CELL-INTERLOCK = the exact stall, RES-CI ⊆ RES-X | [T] §2.1–2.2 |
| A101-O4 | cell-set census on the corpus + Trump (exact, two tolerances); SHELL numerical check | [M] §2.2, `results/cellflood101.json` |
| A101-G1 | **Theorem FLOOD / CELL-INTERLOCK exclusion below ŝ (or below 4 under the strict convention)** | **OPEN** — record is CELL-INTERLOCKED at two corners at 3.985; no four-corner CELL-INTERLOCK known; m*(δ) floor-dependent (§2.3) |
| A101-G2 | the dynamic closure (rigid re-fits, partial slides, RELEASE retreats) of the static set: characterise or measure beyond degen87's greedy | [C] |
| A101-G3 | k0dir2_87 floors 10⁻³, 10⁻² (in flight) → m*(δ) table completion | [M] A87 |
| A101-O5 | composition (plain StratumKill modulo K0-O1-ALL if G1 lands; nothing removed today) and Lean shapes | [T] §3 |
