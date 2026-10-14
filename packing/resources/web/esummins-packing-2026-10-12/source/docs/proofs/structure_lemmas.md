# Structure-space pruning lemmas (advisor draft v1, 2026-08-26)

Setting (from docs/proofs/drain_lemma.md v3). ẑ ∈ D₀ minimises σ with value m ≤ s₀ (exists by D1);
normalise the min corner to the origin, container [0, m]². Fix a consistent selection S and an FJ
certificate (λ₀, λ) ≥ 0, λ₀ + Σλ = 1 (exists by D3′), rows g ≥ 0, stationarity λ₀∇s = Σ λ_k ∇g_k.

Graphs. The ACTIVE-CONTACT graph G: vertices = the 11 squares plus 4 wall nodes W_left, W_right,
W_bot, W_top; one edge per active contact (pair separation row active, or containment row active =
square-wall edge). The SUPPORT graph H ⊆ G: edges whose multiplier is strictly positive (for a flush
contact, positive on at least one of its two rows). "Loaded square" = a square with an H-edge.

Fact 0 (one edge per pair). The contact set of two convex bodies with disjoint interiors is an
intersection of convex sets, hence convex: a single point or a single segment. So G is SIMPLE; a
flush (segment) contact is ONE edge carrying TWO constraint rows (two contact points), a point
contact is one edge with one row. Same for square-wall edges.

## L1 (loaded degree ≥ 2)
Every loaded square has H-degree ≥ 2. Proof: stationarity in the two centre coordinates of square i
reads Σ_{edges at i} λ·n = 0, where each n is the (unit) contact normal and only contact/containment
rows involve c_i. If i has exactly one H-edge, the sum is a single nonzero vector (for a flush edge,
two positive multiples of the SAME normal) — contradiction. ∎

## L2 (degree-2 collinearity — thin branch)
If a loaded square has H-degree exactly 2 with point contacts, force balance forces the two contact
forces equal-magnitude and ANTIPARALLEL, and torque balance forces a COMMON LINE OF ACTION through
both contact points parallel to the shared normal direction. This is a codimension-≥1 geometric
condition: degree-2 vertices are admitted in enumeration only as flagged thin branches. (If one of
the two edges is flush, torque balance instead constrains the resultant of its two rows to act along
the line through the other contact point; same codimension count.) ∎

## L3 (floating components: rattler or self-stress)
Let K be a connected component of G (active contacts) containing NO wall node. Then either
 (i) every internal multiplier of K vanishes — all K-squares are unloaded (support-degree 0), and K
     enters the FJ system only through feasibility (a composite rattler); or
 (ii) K carries a COMPRESSION SELF-STRESS: λ_K ≥ 0, λ_K ≠ 0 with A_Kᵀ λ_K = 0 (pure internal
     equilibrium, no objective coupling — Trump's pinwheel strip is the model, though it also
     touches walls).
Proof: K has no containment rows, so the stationarity rows for K's coordinates involve only K's
internal contact multipliers, and the objective (∇s has no component in K's coordinates; K's squares
carry no s-row) contributes nothing: A_Kᵀ λ_K = 0. Either λ_K = 0 or it is a self-stress. ∎
Enumeration use: floating components are EITHER deleted (case i — their squares join the rattler
set) OR must additionally satisfy the self-stress row system (case ii) — a separately excludable
certificate. No floating component may carry load any other way.

## L4 (planarity)
G (squares + 4 wall nodes) is a planar simple graph. Proof: for each edge pick a point p in the
contact set; draw the edge c_i → p → c_j (for a wall edge, c_i → p with p on the wall, then along
the wall's outward strip to the wall node placed outside the container). Each half-segment lies in
its own closed square (convexity, p on the boundary of both), so two edges can only meet inside a
common square, where all half-segments emanate from the single centre point c_i — no crossing. Wall
strips are disjoint from all squares and from each other except at the container corners, where the
4 wall nodes are joined in a cycle outside. ∎  Consequently |E(G)| ≤ 3(k + 4) − 6 on a loaded core
of k squares, and every subgraph inherits the bound.

## L5 (metric caps — all certified-interval checkable)
 (a) Touching squares have centre distance in [1, √2] (flush: exactly achievable at 1; corner-corner
     diagonal: √2). Squares with an active contact in a selection satisfy the same bounds.
 (b) No square touches two OPPOSITE walls (needs extent ≥ s₀ ≥ 3.8 > √2). Wall-degree ≤ 2, and the
     two walls must be adjacent (a corner square).
 (c) Squares touching one wall have centres within √2/2 of it and pairwise centre distance ≥ 1: at
     most ⌊s₀·(≈1.1)⌋ + 1 = 5 per wall (conservative; the enumerator may compute a tighter cap).
 (d) Kissing cap: the neighbours of square i have centres in the disk of radius √2 about c_i,
     pairwise ≥ 1 apart — at most 12 by the standard disk-packing count (conservative; true square
     kissing is ≤ 8, use 12 unless the sharper bound is separately certified).

## L6 (wall-to-wall load path — the stress lemma's core)
If λ₀ > 0, let x be a binding axis (σ = the x-extent; at least one exists). Then some SINGLE
connected component of H touches BOTH W_left and W_right (resp. both y-walls if y binds).
Proof: ∂/∂s of stationarity gives λ₀ = Σ λ over the far-wall (x = s) containment rows, so λ₀ > 0
forces a loaded square on W_right. Take its H-component C. Sum the x-coordinate stationarity rows
over all squares of C: internal contact forces cancel in pairs (Newton's third law — each internal
edge appears with both signs), leaving  (total λ from W_left edges of C) − (total λ from W_right
edges of C) = 0,  because y-wall normals have no x-component and C has no other external edges. The
right-hand load is positive, hence so is the left — C touches both walls. ∎
Corollary (span count): consecutive centres in a chain are ≤ √2 apart and end centres are within
√2/2 of their walls, so a spanning chain has at least ⌈(s₀ − √2)/√2⌉ + 1 = 3 loaded squares at
s₀ ≈ 3.877 (Trump's diagonal strip has 5).
λ₀ = 0 branch: the whole certificate is a global compression self-stress (A ᵀλ = 0, λ ≠ 0) — its own
excludable row system; enumerated as one extra branch per structure, never silently dropped.

## L7 (binding-axis wall contacts)
On a binding axis both extreme containment rows are active in G (min-corner 0 and max-corner s are
achieved). If only one axis binds, the other axis's extent is < σ and its walls may be untouched.
(Trivial from σ = max extent and the normalisation; recorded so the enumerator does not assume all
four walls are touched.)

## Soundness ledger for the enumerator
HARD prunes (proved above): L1, L3 (with the self-stress branch kept), L4, L5(a,b,d at 12), L6
(with the λ₀ = 0 branch kept), L7, Fact 0 (simple graphs).
THIN branches (kept, flagged): L2 degree-2 vertices; self-stress branches of L3/L6.
SOFT filters (report-only, NOT prunes until separately proven): Maxwell-style total row count
m ≥ 3k + 1 (NOT a theorem — degenerate structures can jam with fewer independent rows), L5(c)
per-wall cap at 5, kissing at 8, and any realizability test that is not interval-certified.
