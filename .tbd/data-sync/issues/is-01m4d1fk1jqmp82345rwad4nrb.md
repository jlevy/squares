---
type: is
id: is-01m4d1fk1jqmp82345rwad4nrb
title: "W3: evaluate n17 extensions and higher-dimensional packing models"
kind: task
status: closed
priority: 2
version: 4
delegate: codex-fibonacci-generalizations
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-08T05:58:49.648Z
updated_at: 2026-10-08T06:12:05.869Z
started_at: 2026-10-08T06:02:41.110Z
closed_at: 2026-10-08T06:12:05.868Z
close_reason: "Completed W3 synthesis with three independent reviews: concrete pose-space certificate, generalized finite-field models, and exact genus-18 absolute-period negative control; results retained in bead notes. No new packing bound claimed."
resolution: null
duplicate_of: null
---
User follow-up to the Fibonacci-torus audit asks which extensions/generalizations could help n17, including higher-dimensional alternatives. Read-only W3 assessment with three independent algebra, geometry/topology and primary-source reviewers. Distinguish bounded pose-space kernels/moment hierarchies, higher-genus translation surfaces and Jacobians, higher-rank lattice/cut-and-project descriptions, and finite-field pair encodings. Verify theorems and derive concrete acceptance conditions without running a target experiment, changing existing scientific verdicts or editing the active source checkout. Retain the synthesis and primary references in this record and answer the user directly.

## Notes

W3 synthesis, independently reviewed in algebra, geometry/topology and primary literature. This was a read-only assessment; no target experiment, solver run, source edit or new packing bound.

Priority: bounded pose-space positivity and higher-order compatibility are the most credible extensions for n17. A single square has coordinates (x,y,theta mod pi/2); all seventeen labeled poses give 51 real coordinates at fixed container side. Define P_S as every pose wholly contained in [0,S]^2, with a graph edge for interior overlap. Independent sets are exactly packings; compactness and the topological packing-graph condition hold. The walls and independent orientations must stay in this domain.

A precise sufficient certificate: find v:P_S -> R^d and one uniform C<16 such that ||v(p)||^2 <= C for every contained pose and <v(p),v(q)> <= -1 for every pair with disjoint interiors, including touching. Seventeen compatible poses would imply 0 <= ||sum v(p_i)||^2 <= 17C-272 < 0. Equivalently K=1+<v,v> has K-J positive semidefinite, K<=0 on compatible distinct poses, and diagonal below17. This is the finite-feature specialization of de Oliveira Filho--Vallentin Theorem2.1. The vector proof itself needs no continuity; continuous features permit literal use of the published kernel theorem. This two-point certificate need not exist even in arbitrarily large dimension when the true capacity is16; higher-order hierarchy convergence does not imply two-point success. All inequalities need continuum-wide exact or interval proof; a sampled SDP is reconnaissance only.

For richer relaxations, de Laat--Vallentin Theorems1--2 give strong duality and finite convergence of their infinite-dimensional hierarchy on compact topological packing graphs. This promises neither low-order success nor a practical finite SDP. Bekker--de Oliveira Filho's convergence theorem concerns their explicitly normalized k-point formulation including the empty set; do not transfer it to arbitrary reduced implementations. For polynomial SOS, retain every separating-axis alternative and an Archimedean quadratic module, such as through a redundant ball constraint. Sparse blocks need their own coverage/consistency argument. Pairwise-compatible domains can lack a joint realization; actual fixed square poses that are pairwise disjoint already form a valid packing. The proposed gain concerns lost domain/moment consistency, not an invented three-body collision rule.

A genuine surface generalization: for N disjoint, strictly interior unit-square holes with positive gaps, glue opposite outer edges and each hole's opposite edges by translations. The resulting closed orientable translation surface has genus N+1, N cone points of angle6pi, and area S^2-N; for N17 it belongs to H(2^17) in genus18. Periods in an adapted symplectic basis are (S,iS) and (z_j,-i z_j), with |z_j|=1. Hole positions are absent from these absolute periods; the minus sign accounts for the negative hole-area contributions. Its Jacobian is separately a complex18-dimensional, real36-dimensional torus. Higher genus still means a two-dimensional surface.

New analytical negative control for a period-only n17 strategy: prescribe S=21/5 and z_j=1 for all17 holes. The period image is (Z+iZ)/5, its covolume1/25, signed area16/25, and induced covering degree16. The seventeen zero orders are all2 and sum to34=2g-2. Refined Haupt therefore realizes exactly this marked absolute-period character in H(2^17), since16>2. Yet17 axis-parallel unit squares cannot fit in side21/5: their centers lie in [1/2,37/10]^2; divide each axis into four intervals of width4/5, yielding16 bins. Two centers in one bin force interior overlap. Thus genus, cone orders, lattice periods and a homology marking do not enforce the required square-hole embedding. This uses no external n17 lower bound. The cover cannot be assumed square-tiled over one branch value: seventeen ramification points of local degree3 need at least four branch values in a degree16 cover.

The inverse needs actual embedded outer/hole cuts, sector ordering, relative placement and an injective planar developing map. Relative periods omitted by absolute periods have N-1 complex dimensions (32 real for17 holes); outer cuts are additional data. Positive-gap packing approximations exist by dilating centers and container while retaining unit sizes, but contact limits can collapse corridors, alter strata or invalidate the cut diagram. Any invariant must survive those limits. For generic nonlattice periods the refined Haupt theorem admits all positive-area characters even in the prescribed stratum, so absolute periods alone generically retain only the area bound. A possible surface route must constrain the embedded perpendicular unit-loop system and outer square cuts, then reject the control above.

Arithmetic extensions survive after relaxing freeness. On F17 x F17, (alpha,beta)->(alpha,-beta) has17 fixed points and136 two-cycles; [alpha,beta]->{alpha+beta^-1,alpha-beta^-1} bijects the nonfixed orbits with unordered pairs. AGL(1,17) acts transitively with stabilizer2, lifted by (alpha,beta)->(a alpha+b,a^-1 beta). This split algebra is different from the field F289. Over F289, the Fibonacci root obeys phi^17=1-phi, phi^18=-1, phi^9=4, has order36, and projective order9; its action on P1(F17) is two nine-cycles, not a17-label action. The full nonsplit torus is cyclic18. No higher-dimensional ambient construction removes the involution obstruction to a regular induced action on136 pairs.

A replacement quadratic template is eta=(3+sqrt13)/2, B=[[0,1],[1,3]]. det(B+3I)=17, Z[eta]/(eta+3)=F17, eta maps to14 of order16 (14^8=-1). Translation1 and eta yield AGL(1,17), still with pair stabilizer2. The modulus has changed; no physical contact or return-map model follows. Conversely coker(A-I) makes A act trivially, so an index17 cokernel alone does not provide a nontrivial multiplier. In general, Z^d/(A^m-I)Z^d and Norm(u^m-1) generalize the finite modules, but still require geometry-derived matrices and verified boundary/cell transfer.

Higher-rank cut-and-project/Minkowski embeddings can organize exact candidate coordinates. Projection need not preserve separation; window selection supplies neither square orientations nor wall clearance. These are plausible seeds, not lower-bound certificates without capture. Likewise unrestricted motion-group bulk density bounds for squares cannot exceed the area argument because squares tile with density1; finite-container kernels must retain position relative to walls.

Selected next discriminator: choose one existing unresolved n17 domain with complete wall, angle and branch constraints. Compare the standing relaxation with a small explicitly defined PSD/moment or joint-domain block. Accept only a rigorously certified excluded region or improved occupancy bound that the baseline leaves open, with accepted endpoint configurations as positive controls and no loss of continuum coverage. Codify a hypothesis and acceptance rule before any target run. Existing X048 endpoint, contact and slider work is a baseline, not something to restart. The general-purpose source directory and active source checkout were not changed.

Primary references:
- [Compact packing kernels, Theorem2.1](https://arxiv.org/html/1308.4893)
- [Packing hierarchy, Theorems1--2](https://arxiv.org/abs/1311.3789)
- [Normalized k-point hierarchy, Theorem4.2 and section3 caveat](https://arxiv.org/abs/2306.02725)
- [Lasserre polynomial moments, Assumption4.1 and Theorem4.2](https://web.mit.edu/~a_a_a/Public/Publications/refs_for_seb_blog/Lasserre.pdf)
- [Refined Haupt theorem, Theorem1.1](https://arxiv.org/html/2002.12901v3)
- [Independent prescribed-singularity theorem](https://arxiv.org/abs/2003.02216)
- [Minkowski embeddings and projection windows](https://journals.iucr.org/a/issues/2020/05/00/ae5086/index.html)
