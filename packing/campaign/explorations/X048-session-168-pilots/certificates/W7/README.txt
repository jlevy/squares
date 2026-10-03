W7 closure certificate: format of the saved objects
=====================================================

Two files, each gzip of UTF-8 JSON in canonical form (keys sorted, separators "," and
":" with no spaces). Each file is named by the SHA-256 of its decompressed bytes:

  seed-<sha256>.json.gz   the wall seed   (schema "generic_wall_seed_v1")
  node-<sha256>.json.gz   the proof node  (schema "exact_generic_owned_hull_v1")

A reader should decompress, check the digest against the file name, and parse.
Every number is an exact rational written as a decimal string "p/q" or "p" (parse with
fractions.Fraction or any exact rational type). No floating point appears.

Frame (not stored; fixed by the problem)
----------------------------------------
Container [0, U]^2 with U = 1169/250. Field coordinates equal physical coordinates
(B = L/U = 1). A unit square's centre lies in the centre box [1/2, U - 1/2]^2.
Cells: the 24 cells of the H-266 unique-state cover, `ring-3-voronoi-8-tabbed-unique`,
built by packing/devtools/check_n17_capacity_one_cover.py build_cover(UNIQUE_24), in
that order (index 0 corner-SW, 1 corner-SE, 2 corner-NW, 3 corner-NE, 4 side-S0,
5 side-N0, 6 side-W0, 7 side-E0, 8 side-S1, 9 side-N1, 10 side-W1, 11 side-E1,
12 side-S2, 13 side-N2, 14 side-W2, 15 side-E2, 16 interior-SW, 17 interior-NW,
18 interior-W, 19 interior-S, 20 interior-N, 21 interior-E, 22 interior-SE,
23 interior-NE). The seed's "world" lists the 24 cell polygons (counterclockwise,
hull normal form) so a reader can check them against the cover tool.
Orientation: the half-angle chart t = tan(theta/2) in [0, 1], with
cos = (1 - t^2)/(1 + t^2) and sin = 2t/(1 + t^2); a square is the same set modulo a
quarter turn, so t in [0, 1] covers every orientation.
W7's mask is [0, 5, 6, 10, 14, 16, 18]: corner-SW, side-N0, side-W0, side-W1, side-W2,
interior-SW, interior-W.

The claim
---------
No packing of unit squares in [0, U]^2 has seven distinct squares with centres in the
seven closed cells of the mask, one per cell (the other ten squares are unconstrained).
By containment and the D4 symmetry of container and cover it excludes every 17-cell
state containing a D4 image of the mask: 16,701 orbit representatives, 133,152 states.

Seed (generic_wall_seed_v1)
---------------------------
mask_index: null (a partial mask); mask: owner cell indices; U, B; bins: 64.
groups: {owner: [points]}: points proved strictly inside the owner's square for every
  centre in its closed cell and every angle (some owners own none: [] is allowed here).
cells: {owner: [64 rows]}; row i covers t in [i/64, (i+1)/64] and holds
  interval, reference {"kind": "wall_seed", "owner", "row"}, outer_domain = the cell cut
  by the row's legal box [h, U - h]^2 with h = min over the two endpoints of
  (cos + sin)/2 (valid on the whole row by a quadratic check), residual_polygons =
  [that domain] (or [] if empty), outer_bounds = [].
world: the 24 cells.

Node (exact_generic_owned_hull_v1, sequential grammar)
------------------------------------------------------
parent null, constraints [], guard_source null, mask_index null, mask, U, B,
source {"sha256": the seed's digest}, initial {groups, cell_references},
steps [...], final_state {...}, contradiction, closed, terminal,
mask_exclusion_proved false, global_optimality_proved false.

A step updates one owner. Fields: index, owner, allowed_half_angle ["0","1"],
complete true, prior_owned_hulls {owner: hull} (the state before the step),
prior_partner_pose_covers {partner: [one item per accepted row of that partner, in
order]} where an item is {reference, interval, domain, core}: domain is the hull of
that partner row's residual vertices (every centre the partner can take at those
angles), core a convex polygon (relative to the centre) strictly inside the partner's
square at every angle of its row; empty rows have domain [] and core [].
rows [64]: each row has interval, prior_reference (the accepted predecessor row, same
interval here), reference {"kind":"phase3","node","step","row"}, input_domain (a convex
polygon containing the required domain = hull(predecessor outer_domain) cut by the row's
legal box), core_vertices (the owner's strict core Q_i for the row), collision_regions
[{partner, vertices}], residual_polygons, common_core_halfplanes [{normal, upper}],
outer_bounds [{normal, upper}] (eight support lines), outer_domain.
common_owned_kernel: points satisfying every common-core halfplane of every live row.
compression_source_hull = hull(prior owned hull + kernel); inner_grid_compression
{vertices, witnesses [{point, indices, weights}], denominator 2^20, original_vertices,
retained_vertices, mode "replace"}: each new point is the exact convex combination of
at most three source-hull vertices given by its witness, on the 2^-20 grid; with
mode "replace" the owner's new owned hull is the hull of the new points alone.

What a row proves (the checker's obligations)
---------------------------------------------
1. The core is strictly inside the square of side 1 at every angle of the row: for each
   vertex (x, y) and sign s, the quadratics 1/2 - s x - 2 s y t + (1/2 + s x) t^2 > 0
   and 1/2 - s y + 2 s x t + (1/2 + s y) t^2 > 0 on the row's closed t-interval.
2. Forbidden regions K_j - Q_i for every other owner j with a nonempty owned hull K_j:
   a centre there puts a point of K_j inside Q_i, an interior overlap.
3. Each collision region R against partner j: for every live item (D_r, Q_r) of j's
   pose cover and every facet n.z <= h of the polygon Q_r - Q_i, every vertex p of R
   satisfies n.p <= h + min over D_r of n.y, and R lies in the required domain. Then for
   p in R and every partner pose (y in D_r, angle in row r), p - y lies in Q_r - Q_i, so
   the two squares share an interior point.
4. The required domain is covered by the forbidden regions, the collision regions and
   the residual polygons (exact vertical sweep).
5. common_core_halfplanes are, for each edge (n, h) of Q_i, n.x <= h + min over the
   residual vertices of n.v; outer_bounds contain every residual vertex; outer_domain is
   the owner's cell cut by the outer bounds.
After all rows: every kernel point satisfies every plane of every live row and lies in
[0, U]^2; the compression witnesses hold.

Closure
-------
After each complete step the checker derives closure itself:
all_parent_poses_forbidden when the stepping owner's rows all have empty residuals, or
owned_hulls_intersect when its owned hull meets another's. The node's contradiction must
equal the derived one. Here: {"kind": "all_parent_poses_forbidden", "owner": 5
(side-N0), "step": 57}.

How to re-check with this repository
------------------------------------
From packing/: uv run --frozen --all-extras --group dev python -m
devtools.check_n17_subpattern --check-saved <this directory> --output <receipt>
(loads only the checker; the producer is never imported).
