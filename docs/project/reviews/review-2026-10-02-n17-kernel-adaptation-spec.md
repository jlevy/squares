---
title: n17 Kernel Adaptation Specification
date: 2026-10-02
status: planning-review
---
# n17 Kernel Adaptation Specification

**Session:** 168, BC-418, lane K1. **Baseline:** main after PR 265 and PR 269, with
`0dabde12` (the unique-state cover) under review.
**Question:** what is n11’s geometric kernel, exactly, and what has to change for an
Opus lane to run it on n17 in two modes: the isolated sub-pattern certificates of
[H-267](../../../packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md)
and the capture of the endpoint’s occupancy state into the exp-244 neighbourhood.

This is a build specification.
It changes no bound, verdict or frontier field.
Every statement about n11 is read from the retained native checkers under
`packing/devtools/` and from the pinned upstream source
(`Queuingtheorydotcom/11SquaresOptimal` at `f9e0de71`, cloned read-only for this review;
paths below starting `src/` are relative to that clone).
Statements about n17 come from the retained tools and records named inline.
Design choices are marked as such, and the closing table separates the two.

## Summary

- **The kernel is an ownership induction over closed angle rows.** Each owner keeps a
  closed partition of its half-angle chart $t\in[0,1]$ into rows, each row an outer
  centre polygon with residual polygons, plus an owned hull of points strictly inside
  the square in every surviving pose.
  One update proves, row by row, that every legal centre is either forbidden (its strict
  core would contain another owner’s owned point, or it collides with every surviving
  pose of a partner) or lies in the new residual; a complete update promotes the common
  core of the residuals to new owned points.
- **It is a checker in this repository, not a producer.** The native modules replay
  n11’s published proposals exactly; nothing here chooses residual polygons, cores,
  collision regions, owner orders or splits.
  The producer is the main thing the adaptation must build.
- **The size-generic part is almost all of it.** Only the frame constants ($U$, $L$,
  $B$), the 16-cell normalised cover and its half-turn canonicalisation, the mask-length
  and inventory pins, and the three capture branch predicates are n11-specific.
- **Two caps, not one.** n11 ran everything at $U-T\approx2\times10^{-21}$. The n17
  exclusion cap $1169/250$ is $4.7\times10^{-4}$ above $S^{\ast}$, and at that cap the
  feasible set around the family extends about $0.02$ to $0.08$ in the $\infty$-norm,
  two orders beyond $r=1/5000$. Sub-pattern exclusion keeps $1169/250$; capture must run
  at a rational $U'$ within about $10^{-12}$ of $S^{\ast}$, with the cover’s cells kept
  in the $U$-frame and the wall bounds centred.
- **Mode A for H-267 is already in v9.** The upstream checker accepts generic wall seeds
  with a partial mask and transfers by containment; the counting (majority-feature) mode
  that n11’s 59 fields used is a second engine with its own producer.
  The first slice replays n11 mask 0 through the counting path and runs one n17
  sub-pattern through the induction path.

## 1. What n11’s Kernel Is

### 1.1 Frame and Inputs

The frame constants are $U=387708359002281417731/10^{20}$, $L=191/50$ and $B=L/U$
(`packing/devtools/check_n11_optimality_field_mask0.py` lines 35–37; asserted upstream
in `src/evidence/research/phase3/work/phase3/hull/audit_capture_v9.py` lines 141–143).
Field coordinates are physical coordinates times $B$: unit squares become squares of
side $B$ in $[0,L]^2$ (PROOF.md lines 128–157). A cover cell $V_j$ in the normalised
$[0,1]^2$ becomes the owner’s *world* $B/2+(L-B)V_j$ (`field_mask0.py` line 509; v9 line
151). Orientation is the half-angle chart $t=\tan(\theta/2)\in[0,1]$ with
$c(t)=(1-t^2)/(1+t^2)$, $s(t)=2t/(1+t^2)$ (`field_mask0.py` line 141).

The inputs of one node are, from the schema the checkers admit
(`check_n11_capture_root_node.py` lines 88–130; v9 lines 136–236):

| Input | Where it is read | Meaning |
| --- | --- | --- |
| cells | cover JSON, 16 polygons, half-turn $j\mapsto15-j$ | closed owner domains |
| cap $U$, scale $B$ | node header | the container $[0,L]^2$ in field units |
| mask | node header | the occupied cells, one owner each; a generic seed may use a partial mask (v9 lines 148–149) |
| owned points per owner | seed `groups` | each proved strictly inside the square for every legal centre in the cell and every angle, by `ownership` (`field_mask0.py` lines 155–218; upstream `work/geometry/audit_wall_kernel.py` `check_point`, line 51) |
| angle rows per owner | seed `cells`, or the phase-two adaptive rows | a closed partition of $[0,1]$ |
| constraints | node header | branch predicates: `half_angle` (owner, bound, keep) and centre halfplanes (owner, normal, upper) |

A wall seed has `bins` uniform rows per owner, each with outer domain equal to the cell
clipped by the row’s wall bounds and one residual polygon equal to that domain
(`check_n11_generic_sequential.py` lines 150–217; v9 lines 183–199).

### 1.2 State

For every owner $i$ in the mask:

- **Rows.** A list of closed intervals $[a,b]$ partitioning the allowed angle interval,
  each with `outer_domain` (a convex polygon in field coordinates: the hull of its
  residual vertices, clipped to the world by eight support directions `SUPPORT_NORMALS`,
  `check_n11_capture_transition_pilot.py` line 33, lines 78–86; v9 lines 91–104) and
  `residual_polygons` (a finite union of convex polygons, possibly points or segments,
  never dropped for zero area).
- **Owned hull** $K_i$: a convex polygon of points strictly inside square $i$ in every
  pose that survives (`groups`).

Rows carry a `reference` and a `prior_reference` so that every row cites the exact
accepted predecessor whose interval contains it (`root_node.py` lines 133–147).

### 1.3 The Update Rule

One *step* updates one owner $i$ against the current state of all others.
For each row $[a,b]$ (v9 lines 306–346; native `root_node.py` lines 178–252 and
`generic_sequential.py` lines 258–382):

1. **Inherited domain.** Start from the predecessor row’s outer domain, intersected with
   the owner’s branch halfplanes and with *self-hull cuts*: for the midpoint axes
   $n=(c,s),(-s,c)$ the square must contain $K_i$, so $n\cdot x\le\min_{K_i}n\cdot p+E$
   and the mirror bound, where $E=B\max(\text{factor})/2$ is a support bound valid for
   every angle in $[a,b]$ (upstream `own_hull_constraints.py` lines 18–41; native
   `transition_pilot.py` lines 89–114).
2. **Legal domain.** Clip by the one-sided wall bounds: with
   $w=\min_{t\in\{a,b\}}(c(t)+s(t))$ and $h=Bw/2$, centres lie in $[h,L-h]^2$; the
   quadratic $1-w+2t-(1+w)t^2\ge0$ on $[a,b]$ proves $c+s\ge w$ on the whole row
   (`transition_pilot.py` lines 226–238; v9 lines 119–120 and 188–191).
3. **Strict core.** A proposed convex polygon $Q_i$ (vertices relative to the centre,
   field frame) is checked to lie strictly inside the square of side $B$ at every angle
   of the row: for each vertex and sign, the quadratics
   $B/2-\sigma x-2\sigma yt+(B/2+\sigma x)t^2>0$ and its rotation on $[a,b]$
   (`transition_pilot.py` lines 117–137; v9 lines 43–56). In the counting mode the core
   is the axis square of side $q=(B-10^{-12})/\text{factor}$ at the midpoint angle
   (`field_mask0.py` lines 349–370).
4. **Forbidden regions.** For every other owner $j$, the Minkowski set $K_j-Q_i$: a
   centre there puts a point of $K_j$ inside $Q_i$, an interior overlap (`root_node.py`
   lines 233–237; v9 lines 122–123).
5. **Universal collision regions.** For a partner $j$ with a complete current pose cover
   (every row $r$: domain $D_r$, core $Q_j^r$), a proposed polygon $P$ is accepted when
   for every live row and every facet $(n,h)$ of $Q_j^r-Q_i$,
   $n\cdot p\le h+\min_{y\in D_r}n\cdot y$ for all $p\in P$. Then square $i$ at any
   centre of $P$ overlaps square $j$ in *every* pose $j$ can still take, so $P$ is
   forbidden. An empty partner cover is an explicit contradiction, never an empty
   quantifier (upstream `phase3/collision/validate_collision_kernel_v3.py` lines 23–87;
   native `transition_pilot.py` lines 196–223 and the integer backend
   `n11_integer_collision.py` lines 70–123). The partner cover itself is admitted row by
   row against the partner’s accepted state (`root_node.py` lines 150–175).
6. **Residual cover.** Prove that the legal domain is covered by the forbidden regions,
   the collision regions and the proposed residual polygons: an exact vertical sweep at
   every edge-crossing abscissa and between consecutive ones (`field_mask0.py` lines
   462–496; upstream `arrangement_audit_v2.py` lines 102–133), with a separate
   closed-segment cover for point and segment domains
   (`check_n11_closed_degenerate_cover.py` line 83; v9 lines 72–90). The residual
   polygons become the row’s new residuals; their hull, clipped by the eight supports,
   is the new outer domain.
7. **Common-core planes.** For the row’s residual vertices $V$ and each facet $(n,h)$ of
   $Q_i$, the plane $n\cdot x\le h+\min_{v\in V}n\cdot v$: a point satisfying all planes
   of all rows lies inside $Q_i$ at every surviving pose, hence strictly inside square
   $i$ (`transition_pilot.py` lines 247–279; v9 lines 337–342).

After a *complete* step (rows partition the allowed interval), the proposed
`common_owned_kernel` must satisfy every plane; its hull with $K_i$ is compressed to a
few grid points, each an exact convex combination of that hull’s vertices, and $K_i$
grows (`check_n11_capture_step0.py` lines 143–155; `root_pilot.py` lines 267–302; v9
lines 347–358 with `audit_residual_kernel.verify_convex_combinations`). Steps may refine
the partition (a row may cite any predecessor containing it) and may revisit an owner
(census contract lines 1101–1127).

### 1.4 Termination and Certificate Format

A node closes in one of three ways (v9 lines 238–248 and 376–385):

- `all_parent_poses_forbidden`: a complete step for an owner whose rows all have empty
  residuals (the owner has no pose);
- `owned_hulls_intersect`: two owned hulls intersect, a common point in two interiors
  (v9 lines 128–134);
- **capture**: every live row of every owner lies inside the guard — its angle interval
  inside one of the role’s half-angle intervals and every residual vertex inside the
  role’s centred box $x/B-U/2$ (v9 lines 238–248; the n17 analogue is in section 4).

A branch tree is a set of node files `exact_branch_owned_hull_v1` (capture) or
`exact_generic_owned_hull_v1` (exclusion), each with `parent {path, sha256}`,
`initial {groups, cell_references}`, `constraints`, `steps[]`, `final_state`,
`contradiction`, `closed`, and the two flags `mask_exclusion_proved` and
`global_optimality_proved` that a node never sets (v9 lines 253–391). A step holds
`index`, `owner`, `prior_owned_hulls`, `allowed_half_angle`,
`prior_partner_pose_covers {partner: rows}`, `rows[]`, `complete`,
`common_owned_kernel`, `compression_source_hull`, `inner_grid_compression`. A row holds
`reference`, `prior_reference`, `interval`, `self_hull_cuts`, `input_domain`,
`core_vertices`, `collision_regions[{partner, vertices, status}]`, `residual_polygons`,
`common_core_halfplanes`, `outer_bounds`, `outer_domain`. A child adds at most one
predicate to its parent’s constraint list and consumes a copy of the parent’s accepted
state; the three n11 predicates are $y_{15}\le5/4$, $t_{13}\le147/512$ and
$t_2\le183/512$, both sides closed (`check_n11_capture_child_node.py` lines 61–74 and
91–120; census contract lines 2087–2100). An unconditional generic contradiction
transfers to every canonical mask containing the node’s mask or its half-turn (v9 lines
402–405).

### 1.5 Where the Code Lives

| Piece | Upstream (pinned `f9e0de71`) | Native replay in this repository |
| --- | --- | --- |
| Node replay, update loop, promotion, closure | `audit_capture_v9.py` lines 136–391 | `check_n11_capture_root_node.py` `check_step` lines 315–448; `check_n11_capture_child_node.py` `check_step` lines 558–713; `check_n11_generic_sequential.py` `check_row` lines 258–382 |
| Ownership of a point | `work/geometry/audit_wall_kernel.py` `check_point` line 51 | `check_n11_optimality_field_mask0.py` `ownership` lines 155–218 |
| Strict core over a row | v9 lines 43–56 | `check_n11_capture_transition_pilot.py` lines 117–137; `check_n11_capture_root_pilot.py` lines 106–138 |
| Self-hull cuts | `phase3/hull/own_hull_constraints.py` lines 18–52 | `transition_pilot.py` lines 89–114; `generic_sequential.py` lines 220–244 |
| Wall bounds | v9 lines 119–120, 188–192 | `transition_pilot.py` lines 226–238 |
| Universal collision | `phase3/collision/validate_collision_kernel_v3.py` lines 23–87 | `transition_pilot.py` lines 196–223; `n11_integer_collision.py` lines 70–123 |
| Residual cover sweep | `phase3/hull/arrangement_audit_v2.py` lines 102–133 | `field_mask0.py` lines 423–496; `n11_fast_exact_cover.py`; `n11_indexed_exact_cover.py`; `check_n11_closed_degenerate_cover.py` |
| Common core and compression | v9 lines 337–358; `phase3/hull/audit_residual_kernel.py` line 20 | `check_n11_capture_step0.py` lines 143–155; `root_pilot.py` lines 267–302 |
| Branch predicates and conditional view | v9 lines 107–117, 264–275 | `child_node.py` lines 61–74, 284–331 |
| Counting-mode field packet | `phase3/audit/audit_wall_mask_chain_v3.py` lines 56–169; `phase3/audit/independent_weighted_cover.py` lines 42–117 | `field_mask0.py` lines 349–546; `check_n11_optimality_field_runner.py` lines 42–79, 475–762 |
| Transfer by containment | v9 lines 402–405; `audit_wall_mask_chain_v3.py` line 103 | `field_mask0.py` lines 578–610; `field_runner.py` lines 720–762 |
| Pose inclusion into the local box | `candidate-capture/audit_complete_capture438.py` | `check_n11_optimality_pose_inclusion.py` lines 106–125, 181 |

The native modules are byte-pinned by their receipts (`GEOMETRY_SHA`, `FIRST_SHA`,
`STEP0_SHA` and so on) and must not be edited; the adaptation copies and parametrises.

## 2. What Changes for n17

### 2.1 Size-Generic Parts

Everything in section 1.3 is written for an arbitrary owner count: the ownership test,
the row envelope, cores, self-hull cuts, wall bounds, Minkowski forbidden regions,
universal collision, the sweeps, the common-core planes and compression.
The owner loops iterate over the mask; nothing indexes a fixed square count except the
inventory pins. The checker grammar (references, predecessors, partner covers, complete
steps, closure kinds) is also generic.

### 2.2 n11-Specific Constants and Hand Choices

| Item | Where | n11 value | n17 replacement |
| --- | --- | --- | --- |
| $U,L,B$ | `field_mask0.py` 35–37; v9 141–143 | $U\approx T+2\times10^{-21}$, $L=191/50$ | exclusion cap $U=1169/250$; capture cap $U'$ (section 4.1); design: $L=U$, $B=1$, so field equals physical |
| Cover and world | `field_mask0.py` 133–138 (requires 16 cells), 509; v9 151 | normalised $[0,1]^2$ cells | the 24 physical cells of `check_n17_capacity_one_cover.UNIQUE_24` (lines 198–219), already in $[1/2,U-1/2]^2$; world is the cell itself |
| Injectivity | v9 line 153 asserts every cell has diameter below 1 | true for n11 | false for the 12 side cells (depth $0.911$, width $0.705$); capacity one comes from the depth–width wall lemma (exp-246), so the kernel binds the cover receipt instead of asserting diameters |
| Canonicalisation and transfer | `field_mask0.py` 592; v9 404; half-turn $15-j$ | one involution | the exact D4 permutations of `check_n17_capacity_one_cover.d4_permutations` (line 778); a certificate for $G$ transfers to every state containing any image $g(G)$, because container and cap are D4-symmetric (design, needs review) |
| Mask length, counts | `MASK`, `len(...)==11`, 130 seed points, 69 rows, 28 kernel points, 217 rows | published objects | none; counts are reported, not pinned |
| Wall-seed bins | v9 182; `generic_sequential.py` 164 ($\le128$) | producer choice | producer choice; start at 64 |
| Branch predicates | `child_node.py` 61–74 | $y_{15}\le5/4$, $t_{13}\le147/512$, $t_2\le183/512$ | none fixed; chosen by the producer when a residual is bimodal (section 4.4) |
| Guard | `local-capture-guards.json`, v9 238–248: a box per role in centred unit coordinates and half-angle intervals | n11’s focused radii | the 45-coordinate target of section 4.2, a convex polygon per owner |
| Frame map to the local theorem | PROOF.md 524–536: a quarter turn plus $U/2\to T/2$ | case 438’s D4 image | identity plus translation $(S^{\ast}-U)/2$, because the endpoint state is its own orbit representative |
| Chart seam | PROOF.md 518–519: $(t-1)/(t+1)$ near $t=1$ | axis squares | the same for the ten axis squares; the tilted squares sit at $t^{\ast}\approx0.362$ and square 16 at $t\approx0.503$ after reduction modulo $\pi/2$ |

### 2.3 The n17 Frame

Seventeen squares, 136 pairs, cap $U=1169/250$, centre box $[1/2,U-1/2]^2$
(`check_n17_capacity_one_cover.py` lines 80–83). The unique-state design has four corner
cells of side $79/100$, twelve side cells (middle cell of each wall deepened to $93/100$
and narrowed to $257/375$), and eight interior Voronoi cells with tabs and clips (lines
198–219); 346,104 states and 43,593 D4 orbits.
Cells overlap: side-S0 and side-W0 share the square $[1.29,1.411]^2$, and the tabs make
the axis interior cells touch the middle side cells.
The state convention is existential: a packing realises every 17-subset of distinct
closed cells that contains its centres.
That is harmless for exclusion, whose antecedent is closed-cell membership exactly as in
n11 (PROOF.md lines 228–230), and it is why the unique-state check exists for capture.

Running the retained tool on the unique design (this review, output in the lane
scratchpad) gives the endpoint’s state at the H256 centroid:

| Square | Cell | Margin | Square | Cell | Margin |
| ---: | --- | ---: | ---: | --- | ---: |
| 1 | corner-SW | 0.790 | 10 | side-N0 | 0.123 |
| 2 | side-S0 | 0.210 | 11 | interior-W | 0.110 |
| 3 | side-W0 | 0.210 | 12 | interior-N | 0.274 |
| 4 | corner-NW | 0.790 | 13 | side-S1 | 0.021 |
| 5 | corner-SE | 0.790 | 14 | interior-E | 0.104 |
| 6 | side-S2 | 0.247 | 15 | side-N1 | 0.333 |
| 7 | side-E0 | 0.210 | 16 | side-N2 | 0.108 |
| 8 | corner-NE | 0.790 | 17 | side-E1 | 0.067 |
| 9 | side-W2 | 0.024 |  |  |  |

The seven empty cells are side-W1, side-E2 and the interior cells SW, NW, S, SE and NE.
Over the slider triangle the least margin is $0.002111$ (square 13), from the `0dabde12`
commit message.

### 2.4 Tilted Squares, Square 6 and the Sliders

The record’s root is $t^{\ast}\approx0.362044$ (exp-237 certificate, `box.midpoint`), so
squares 9 to 14 (`THETA_LABELS`, `check_n17_endpoint_feasibility.py` line 37) are tilted
by $\theta^{\ast}=2\arctan t^{\ast}\approx39.80^{\circ}$, and square 16 by
$-2\arctan(0.330949)\approx-36.6^{\circ}$. The brief’s $40.77^{\circ}$ does not appear
in the record and should be reconciled before any row partition is seeded.

Square 6 is free: its cell side-S2 has width $0.705$ and circumradius above $1/2$, so
the common core of all its poses is empty and it owns nothing at the seed.
As a partner, its universal collision set over a whole cell is also empty.
So square 6 contributes no contraction and needs none: the local theorem drops it.
Its only duties are to be an owner with one coarse row (so the state is complete) and to
supply, through H-268, the halfplanes on squares 5 and 13 that the kernel inherits as
necessity theorems, the way n11 inherited D4 halfplanes (PROOF.md lines 296–304).

The sliders are coordinates the capture does not have to contract: $a=-\delta\xi_5$,
$b=-v^{\ast}\cdot\delta r_{11}$, $z=v^{\ast}\cdot\delta r_{13}$, with the certified box
$B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$ (exp-244). In the
kernel they are directions in which the guard polygon of squares 5, 11 and 13 is long
(section 4.2).

## 3. The Field-Certificate Mode for H-267

### 3.1 What a Certificate Says

For a cell set $G$ with $|G|=k\le7$: no packing in the cap-$U$ container has $k$
distinct squares with centres in the closed cells of $G$, one per cell.
The other $17-k$ squares are unconstrained, which is what makes the certificate transfer
by containment to every state $J\supseteq G$ and, by D4, to every state containing an
image of $G$.

There are two ways to prove it, and n11 used both.

### 3.2 Mode A: Ownership Induction on $k$ Owners

This is v9’s generic mode with a partial mask (lines 148–149): a wall seed on the $k$
cells, owned points proved from the cells alone, uniform bins, then owner updates until
`all_parent_poses_forbidden` or `owned_hulls_intersect`. The native replay is
`check_n11_generic_sequential.py`; the accepted case-2129 execution checks 70 seed
points, 88 seed rows, 18 updates and 144 rows in 22.6 seconds wall (census contract
lines 1133–1141), and the 32-case final batch averaged 636 CPU-seconds per case (lines
2376–2380). n11 used this on eleven owners; on $k\le7$ owners every step is cheaper.
Nothing in the mode knows the mask is partial except the transfer rule.

### 3.3 Mode B: The Counting Packet

A packet (`audit_wall_mask_chain_v3.py` lines 88–104; `field_runner.FieldSpec` lines
42–79) declares rational *sites*, nonnegative integer point weights, *majority-hull*
features (an odd set of $2m-1$ sites with threshold $m$ and a weight), a *budget* $b$
equal to the sum of all weights, required owners $O$ with their owned points, and
per-cell thresholds $q_i$ with $P=\lbrace i:q_i>0\rbrace$.

A square *captures* a point resource when its strict core contains the point, and a
majority feature when its core’s projection contains the median site projection in every
direction, which is decided on the coordinate axes and the normals to site pairs
(`field_mask0.py` lines 397–410; census contract lines 754–760). Each resource has
capacity one: two disjoint strict cores have a separating direction, and the same median
cannot lie in both projected cores (lines 761–764). The proof obligation for cell
$i\in P$ is, for every row of a complete partition of $[0,1]$: every legal centre lies
in a region of total weight at least $q_i$, where the regions are the feature strips and
point boxes (physical atoms) and the collision boxes around owned points of the other
owners in $O$, which count as covered because they are impossible, not because they
carry charge (`field_runner.py` lines 529–584 and 619–717). Then any state
$J\supseteq O$ with $\sum_{i\in P\cap J}q_i>b$ is impossible, equality excluded (lines
720–762; census contract lines 133–143).

n11’s mask 0 is the whole mechanism in one packet: $O=\lbrace0,1,2,3,6\rbrace$, one
five-site feature of weight one, $q_1=q_2=1$, budget one, 55 owned points, 136 rows (67
and 69), 453 direct and 459 transferred cases (`field_mask0.py` lines 594 and 632;
`receipts/field-mask0/`).

### 3.4 The n17 Analogue of Mask 0

Mask 0 is the bottom row of four cells plus one above.
The n17 bottom row is corner-SW, side-S0, side-S1, side-S2, corner-SE, and the endpoint
occupies all five, so the row itself is feasible; the lane-F arity-six sweep flagged the
row plus one cell above or beside it (bulk-exclusion design, lines 242–244). The first
n17 target is therefore an arity-six class of that shape, for instance
$\lbrace\text{corner-SW},\text{S0},\text{S1},\text{S2},\text{corner-SE},\text{interior-S}\rbrace$,
with interior-S empty at the endpoint.
Its infeasibility is a proxy conjecture until the kernel closes it.
The owners of a mode-A run are the six cells; the first owners to update are the ones
whose wall bounds already cut deepest (the corners), then the side cells, so that the
corner owned hulls grow before the crowded middle is attacked.

### 3.5 The Method Control

The mask-0 packet is replayed through the adapted code path, not through the frozen
checker: the n11 frame (16 normalised cells, $U$, $B=L/U$, the half-turn group) is one
instance of the frame abstraction, and the n17 frame is another.
The replay must reproduce the retained receipt exactly: 55 ownership proofs with the
same methods and margins, 136 rows with the same core sides and event counts, and the
same 453 and 459 case lists.
Agreement is checked against `receipts/field-mask0/result.json` and against a run of the
frozen `check_n11_optimality_field_mask0` on the same inputs.
A second control for mode A is case 2095 through the same abstraction
(`check_n11_generic_fresh.py`: five sequential states, 160 rows).

### 3.6 The Consumer

An exact set-union consumer over the 43,593 orbit representatives: for each certified
$G$ and each $g\in D4$, every representative whose state contains $g(G)$ is excluded;
the union is formed by set identity, not by count (census contract lines 795–800). The
endpoint state must survive every certificate; a certificate that excludes it is a
soundness failure of the kernel, not a result.
Partial, timed-out or refused certificates exclude nothing.

## 4. The Capture Mode

### 4.1 Two Caps

**Measured.** n11’s cap satisfies $U-T\approx2.1\times10^{-21}$ (PROOF.md line 131
against the decimal of $T$ in its README). n17’s exclusion cap gives
$U-S^{\ast}=1169/250-4.67553009\ldots\approx4.7\times10^{-4}$. The first-order slope at
the endpoint is $\kappa_\infty=1/175.8$ side per unit $\infty$-norm in the softest
direction $-\omega_{11}$, with the stiffest coefficients near 48 (route review, lines
101–105).

**Consequence.** At cap $1169/250$ a configuration can move about $0.083$ along
$-\omega_{11}$ and about $0.02$ in the stiff directions while keeping its side at or
below $U$. Those are feasible packings of side above $S^{\ast}$; they are not
counterexamples, and no sound capture at that cap can exclude them.
The brief’s formulation, “every packing in the endpoint’s occupancy state with side
$\le U$ lies within the local theorem’s neighbourhood”, is false at $U=1169/250$ and
true only at a cap within about $r\kappa_\infty\approx10^{-6}$ of $S^{\ast}$.

**Design.** Keep the census and the sub-pattern exclusions at $U=1169/250$, where the
cover is certified; exclusions at a larger cap hold for every smaller side by the
centred embedding (PROOF.md lines 143–151). Run the capture at $U'$, the upper end of a
rational enclosure of $S^{\ast}$ from the exp-237 root box ($U'-S^{\ast}\le10^{-12}$),
with the cells kept in the $U$-frame and the wall bounds centred: the legal centre box
for a row becomes $[(U-U')/2+h,\ (U+U')/2-h]^2$ in place of $[h,L-h]^2$
(`transition_pilot.py` lines 233–237 are the four lines to generalise).
The antecedent of the capture is then: a packing of side $S\le U'$, centred in
$[0,U]^2$, realising the endpoint state.
Its first-order feasible set has $\infty$-radius about $2\times10^{-10}$, which is what
makes contraction to $1/5000$ possible at all.
The frame map to the local theorem is the translation $(S^{\ast}-U)/2$, exact because
$S\le S^{\ast}$ embeds centred in $[0,S^{\ast}]^2$ (PROOF.md lines 532–536).

### 4.2 The Target

The guard replaces n11’s role boxes with one convex polygon per owner in centred
coordinates $p-U/2$, compared with the endpoint centre $c_i^{\ast}-S^{\ast}/2$ enclosed
in exact rational intervals (as `check_n11_optimality_pose_inclusion.py` lines 119–125
do), and one angle interval per owner:

| Owner | Centre polygon | Angle |
| --- | --- | --- |
| 1–4, 7–10, 12, 14–17 | the box $\lvert x-x^{\ast}\rvert\le r$, $\lvert y-y^{\ast}\rvert\le r$ | $\lvert\theta-\theta^{\ast}\rvert\le r$ |
| 5 | $\lvert y-y^{\ast}\rvert\le r$, $x^{\ast}-\tfrac14\le x\le x^{\ast}$ | $\lvert\theta-\theta^{\ast}\rvert\le r$ |
| 11 | $\lvert u^{\ast}\cdot(c-c^{\ast})\rvert\le r$, $-v^{\ast}\cdot(c-c^{\ast})\in[0,\tfrac1{12}]$ | $\lvert\theta-\theta^{\ast}\rvert\le r$ |
| 13 | $\lvert u^{\ast}\cdot(c-c^{\ast})\rvert\le r$, $v^{\ast}\cdot(c-c^{\ast})\in[-\tfrac18,\tfrac1{16}]$ | $\lvert\theta-\theta^{\ast}\rvert\le r$ |
| 6 | its cell | $[0,\pi/2]$ |

with $r=1/5000$ and the roster of `check_n17_local_minimum.coordinate_lifts` (lines
288–304). Angle radii are converted to $t$ with exact derivative bounds on $2\arctan t$
(`pose_inclusion.py` lines 106–118), about $1.1\times10^{-4}$ in $t$ at $t^{\ast}$.
Vertex checks suffice by convexity (PROOF.md lines 515–518).

Two faces need care.
The faces $a\ge0$ and the walls hold exactly after the map into $[0,S^{\ast}]^2$, not in
the $U$-frame, so the guard tests them with the $10^{-12}$ slack and the composition
charges the map. The face $b\ge0$ rests on the 9/11 contact, which the local theorem
drops (H-268, lines 66–67); if the kernel delivers only $b\ge-\delta$, the cheap fix is
to widen $B_W$ in $b$ and re-run exp-244 (15 seconds).

### 4.3 Owners, Rows and Inherited Facts

Sixteen contracting owners and square 6 coarse.
The seed is the endpoint state’s wall seed at cap $U'$: for every owner, its cell
clipped by the centred wall bounds, 64 uniform bins, owned points from the cell alone.
H-268’s bounds ($a\le21/100$, $z\ge-1/20$, $b\le3/40$ on the tabbed design; to be re-run
on the unique design) enter as centre halfplanes on owners 5, 11 and 13 in the root’s
constraint list, with their receipt bound as a premise.
Partner covers are complete current rows, as in n11; the integer collision backend is
the default.

### 4.4 Branch Predicates and the Producer’s Policy

n11 split when a residual was bimodal and chose predicates by hand.
The producer should split a row only when two consecutive updates leave an owner’s
residual with two components whose angle or centre separation exceeds the row width, and
record the predicate as a closed `half_angle` or centre halfplane exactly as n11’s
grammar does, so the child checker needs no change.
The capture review’s falsifier is more than 16 splits before the $10^{-3}$ scale.

### 4.5 What the Pilot Must Measure

Per round (one update of every contracting owner), in the receipt:

- live rows per owner, total live angle width per owner and the widest live row;
- per owner, the bounding half-extents of the residual union in the target coordinates
  (position and angle), and the ratio to the previous round, which is the contraction
  factor $g$ per owner and per coordinate class;
- owned-hull vertex count and area per owner, and the number of promoted points;
- per update: CPU and wall time, rows checked, partner rows admitted, collision
  facet–vertex checks, cover events and probes;
- rounds at which the worst half-extent first falls below $10^{-2}$, $10^{-3}$,
  $3\times10^{-4}$ and $2\times10^{-4}$, and the round at which progress stops;
- the endpoint control after every update: the exact enclosure of the endpoint pose must
  lie inside some live row of every owner.
  Its loss is a soundness failure.

The capture review’s stop condition applies: $g>0.95$ at the $10^{-3}$ scale, or more
than 16 splits before $10^{-3}$, means the n11 architecture is the wrong engine for n17
whatever the radius (capture feasibility review, lines 230–235).

## 5. Staged Build Plan

Each slice names its deliverable, tests, controls and cost.
All code under the lint floor; the heavy runs leave CI and keep only their controls in
the fast tier (OR-13).

### Slice 1: Frame Abstraction, Mask-0 Replay, One n17 Sub-Pattern

**Deliverable.** A library package `packing/src/sqpack/hull_kernel/` with a `Frame`
(cap, capture cap, scale, closed cells as physical polygons, symmetry group as cell
permutations, orbit representatives) and the generic primitives copied from the frozen
modules and parametrised: ownership, row envelope and strict core, self-hull cuts,
centred wall bounds, Minkowski forbidden regions, universal collision (integer backend),
the reference and indexed sweeps, common-core planes and compression, the counting-mode
atoms and weighted cover, and the containment-plus-symmetry transfer.
Two frame adapters: `n11` from the retained cover object, and `n17` from
`check_n17_capacity_one_cover.build_cover(UNIQUE_24)`. A first mode-A producer,
deliberately simple: fixed bins, round-robin owner order, residual polygons by exact
polygon subtraction of the forbidden union from the legal domain, cores from the row
envelope, collision regions as the intersection of the domain with the collision
halfplanes, kernel as the plane intersection, compression on a $2^{-20}$ grid, no
splitting. A tool `devtools/check_n17_subpattern.py` that runs the producer and then the
checker on a named cell set and writes a receipt in the v9 node grammar.

**Scope, exactly.** (1) Replay n11 mask 0 through the counting path on the `n11` frame
and match the retained receipt: 55 points, 136 rows, 453 and 459 cases.
(2) Replay case 2095 through the mode-A checker on the `n11` frame against the five
published states. (3) Run the mode-A producer on the n17 frame for one arity-six
wall-row-plus-one class (section 3.4) at $U=1169/250$ and report closure or the stalled
state with its residual extents.

**Tests.** The frame abstraction reproduces the frozen functions bit for bit on the n11
inputs (same `Fraction` outputs); the n17 adapter’s cells equal the cover tool’s; D4
transfer on a hand-built three-cell pattern lists exactly the eight images; the counting
consumer refuses budget equality, a lost owner, a duplicate atom and a seam gap (census
contract lines 801–803).

**Controls.** Positive: a two-cell pattern whose cells lie within distance $1-\epsilon$
of each other must close in one update.
Negative: the five-cell bottom row must *not* close, and the endpoint’s poses must
remain inside the residuals at every update.
Refusal: the n17 frame with the diameter assertion restored must refuse the side cells.

**Cost.** One Opus lane, one to two days; the runs take minutes.

### Slice 2: Producer with Refinement, and the Residue

**Deliverable.** Adaptive row splitting (split the widest live row of the owner whose
residual shrank least), owner ordering by residual area, a stall detector, and a batch
runner over the selector’s arity $\le7$ classes with per-class receipts; the exact
set-union consumer over the 43,593 representatives with D4 transfer; the residue count
and the endpoint’s survival.

**Tests and controls.** Every certificate is re-checked by the checker from its receipt
alone; mask 0 and case 2095 remain the method controls; the consumer’s union is
recomputed from the receipts by a second implementation.

**Cost.** Two to four days of build; CPU hours for the certificates (a few hundred
classes at minutes each), a few CPU-hours for the consumer.
This is the H-267 instrument.

### Slice 3: Capture Pilot on the Endpoint State

**Deliverable.** `devtools/pilot_n17_capture.py`: the capture seed at $U'$, H-268’s
halfplanes as premises, square 6 coarse, the guard polygons of section 4.2, and the
per-round measurements of section 4.5 in a receipt.
It stops at a budget, at the guard, or at a stall.

**Controls.** The endpoint control after every update; n11 root-self step 0 replayed
through the same code path (217 rows, 149 partner rows, 64.9 seconds with three workers,
census contract lines 1264–1271); a run at $U=1169/250$ that must *fail* to contract
below the first-order blob, as a check that the two-cap distinction is real.

**Cost.** Two days of build; the run is bounded by the capture review’s model at 100 to
400 CPU-hours for the full contraction, with the pilot cut at a few CPU-hours to measure
$g$.

### Slice 4, If Needed: Counting-Mode Producer and Branches

Only if mode A stalls on wall-row classes: a feature search for majority packets (the
upstream discovery tree has n11’s `phase2/minimize_mask0.py`, outside the proof), and
the branch-predicate policy of section 4.4 if the pilot’s residuals are bimodal.

## 6. Risks

1. **There is no producer.** n11’s residual polygons, cores, collision regions, kernels,
   owner orders and splits came from discovery code the proof does not publish; the
   repository holds checkers only.
   The producer is the cost, and it is unpriced (capture review, lines 89–91). This is
   the place the adaptation most likely stalls, in slice 2 or 3.
2. **Contraction stall.** n17’s slope $\kappa_\infty$ is nine times smaller than n11’s;
   the probe showed that linear propagation does not contract at all and that the power
   is in the angle rows (capture review, lines 142–153). If $g$ approaches one at the
   $10^{-3}$ scale the architecture fails regardless of radius.
3. **The cap.** If the capture is run at $1169/250$ it cannot succeed, and the failure
   would look like a stall.
   Section 4.1 is load-bearing and needs an independent read.
4. **Overlapping cells and the state convention.** The kernel is sound on closed cells
   whatever the overlaps, but the consumer’s orbit count and the unique-state margin
   ($0.002111$) are what make the capture a single case; packings near the family that
   realise a neighbouring state are feasible only at sides above $S^{\ast}$ by far more
   than $U'-S^{\ast}$, which the two-cap design relies on.
5. **Rational growth.** Every clip and hull multiplies denominators; n11 needed an
   integer homogeneous backend and gmpy2 for 31.5 million inequalities at the root.
   n17 has 136 pairs and three times the partner rows; the integer backend and the
   indexed sweep must be defaults, not options.
6. **The chart.** Ten axis squares sit at the $t=0$ and $t=1$ seam and need the
   $(t-1)/(t+1)$ conversion in the guard; a wrong angle for the tilted squares (the
   $40.77^{\circ}$ in the brief against $39.80^{\circ}$ in the record) would seed the
   rows away from the endpoint and the endpoint control would catch it late.
7. **Mode B needs its own search.** If the wall-row classes do not close by induction,
   the counting producer is a second program with no n17 precedent.
8. **The slider faces.** $b\ge0$ and $z\le1/16$ are not wall facts; if the kernel cannot
   deliver them, $B_W$ must be widened and exp-244 re-run before the capture’s target is
   final.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured from n11 code and record | Every line reference in sections 1 and 2.2; the mask-0 packet numbers; the case-2129, case-2095, step-0 and batch costs; $U-T$ |
| Measured from n17 tools and records | The unique-state cover’s cells, the endpoint’s state and margins (this review’s run); $t^{\ast}$ and the angle classes; the 45-coordinate roster; $B_W$ and $r$; $\kappa_\infty$ and the dual coefficients |
| Derived here, needing review | The two-cap argument of section 4.1 and the feasible-set radius at $1169/250$; the D4 transfer rule for sub-patterns on a D4-invariant cover; the guard polygons of section 4.2 |
| Design choices | $L=U$, $B=1$; binding the cover receipt in place of the diameter assertion; H-268 halfplanes as inherited premises; the producer policies of slices 1 and 2; the slice boundaries and costs |
| Conjecture | That the wall-row-plus-one class is infeasible; that mode A closes it; that $g<0.95$ |

The cover run’s output is in the session scratchpad (`lanes/k1/cover-unique.json`),
outside the record; the upstream clone is read-only and nothing from it enters the
repository.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
