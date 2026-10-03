---
title: n17 W7 Closure Review
date: 2026-10-02
status: planning-review
---
# n17 W7 Closure Review

**Session:** 168, BC-418, lane R3 (independent adversarial reviewer).
**Reviewed:** `packing/src/sqpack/hull_kernel/` and
`packing/devtools/check_n17_subpattern.py` at commit `fe152c30`, the receipt
`packing/campaign/explorations/X048-session-168-pilots/receipts/kernel-closure-W7-bins64.json`,
and lane K2’s saved seed and node objects for the same closure (SHA-256 `8949a798…` and
`2d516d00…`), re-produced in a fresh process during this review.
**Question:** can the first certified n17 sub-pattern exclusion, W7 = {corner-SW,
side-N0, side-W0, side-W1, side-W2, interior-SW, interior-W} at cap $U = 1169/250$, be
admitted to the census?
**Method:** every number below was recomputed by scripts of my own that import nothing
from `sqpack` or the checker (`transfer_count.py`, `w7_search.py`, `verify_cert.py`),
plus a mutation harness (`mutate.py`) that feeds the kernel’s checker deliberately
unsound objects and records what it refuses.
The scripts and their logs are in the session scratchpad under `lanes/r3/`. Nothing in
the record was edited.

## Summary

- **Verdict: no blocking defect found.** Each of the five new grammar pieces is sound,
  with the invariant it rests on stated below and the line that enforces it named.
  The checker refused 25 of the 26 unsound mutations I fed it, including a
  collision-region vertex pushed $10^{-7}$ past its tightest facet and a promoted point
  pushed $10^{-7}$ past its tightest common-core plane; the 26th, an unowned seed point,
  ends as `INCOMPLETE` and excludes nothing.
- **The transfer count is reproduced exactly:** 8 distinct D4 images of W7, 133,152 of
  the 346,104 states, 16,701 of the 43,593 orbits, by direct enumeration and by
  inclusion–exclusion.
  The endpoint’s state contains no image of W7, so the certificate does not exclude the
  endpoint.
- **The geometry is tight.** My own float search places the seven squares with worst
  violation $9.0\times10^{-3}$ (two seeds, 63 restarts), below the selector’s reported
  best penetration of $1.1\times10^{-2}$; the selector’s number is not a lower bound and
  should not be quoted as one.
  No feasible placement was found, so the search did not falsify the closure, and the
  two six-cell sub-patterns that drop either interior cell are placeable with margins of
  $0.02$ to $0.03$.
- **The certificate re-checks.** Lane K2’s fresh-process run at `fe152c30` reproduced
  the seed and node byte for byte (digests `8949a798…`, `2d516d00…`) and certified the
  closure again. My verifier, which imports nothing from the kernel, re-proved the seed,
  the whole owned-hull chain, all 19,282 partner cover rows, and 270 rows in full (every
  row of the closing step and four per earlier step): 596 collision regions by my own
  Minkowski hulls and 2,076,688 exact facet inequalities, and 270 coverage proofs by an
  exact area argument rather than a sweep.
  It derives the same closure.
  The closure rests on collision regions: all 64 rows of side-N0’s last step need one
  against side-W2, and none is covered by forbidden regions alone.
- **Bottom line: admissible, under three conditions** (section 5): the record binds the
  saved objects and a receipt from a committed tool; the independent re-check is
  retained, ideally extended to every row; and the “minus one cell” stalls are recorded
  as controls. The checker is sound as far as this review can find; what remains is
  custody and breadth, not soundness.

## 1. What the Certificate Claims and How It Argues

The kernel keeps, for each of the seven owners, a closed partition of its half-angle
chart $t\in[0,1]$ into 64 rows, each row a finite union of closed convex *residual*
polygons containing every centre the owner can have at those angles, and a closed convex
*owned hull* $K_i$ of points strictly inside square $i$ in every surviving pose.
One step updates one owner against the others’ current state.
Both facts are statements about *every* packing satisfying the hypothesis (seven
distinct unit squares with centres in the seven closed cells, inside $[0,U]^2$, any
orientations), and each step derives new ones from old ones, so there is no circularity.

The node has 58 steps.
The west wall pins first (side-W2 to 12 live rows and a residual box of
$0.11\times0.05$, side-W1 to 20 rows), side-N0 starts owning points at round 4, and at
step 57 every row of side-N0 is covered by forbidden regions and collision regions with
no residual: the owner has no pose, and the closure `all_parent_poses_forbidden` is
derived by the checker (`sequential.py` lines 337–350 and 435), not read from the
producer.

## 2. Soundness of the New Grammar Pieces

### (a) Partner pose covers from the hull of each accepted row’s residual vertices: sound

**Invariant.** For every surviving packing, the partner’s pose $(y, t_j)$ has $t_j$ in
some accepted row $r$ of the partner and $y$ in that row’s residual union, which is
contained in the hull $D_r$ of the residual vertices.
Rows with empty residual contain no pose.

**Where enforced.** `sequential.py` `admit_partner_covers` lines 275–323: the cover must
have exactly one item per accepted row (line 300), each item cites its row by reference
and interval (lines 302–306), a live item’s domain must equal `hull` of the accepted
row’s residual vertices exactly (lines 307–316), its core must pass `strict_core` over
the row’s interval (lines 317–319), an empty row must be declared empty (lines 311–314),
and a cover with no live row is refused rather than treated as a vacuous quantifier
(line 321). The accepted rows partition $[0,1]$ because the seed rows are the uniform
bins (`node.py` line 168) and every later step’s rows are checked by
`complete_refinement` (`sequential.py` lines 80–104). The cover is taken from the
partner’s *current* accepted rows, `rows[partner]`, at line 299.

**Attempts to break it.** A domain with one vertex dropped, a domain with one vertex
added, a stale cover copied from an earlier step, a live row declared empty, a cover
with every row declared empty, a core scaled by $1.02$ and a core scaled by $1+10^{-6}$:
all refused (`mutate.log`).

### (b) Collision regions verified by `integer_universal_collision`: sound

**Invariant.** If $p$ satisfies, for every live partner row $(D_r, Q_r)$ and every facet
$(n, h)$ of the Minkowski difference $Q_r - Q_i$,
$n\cdot p\le h+\min_{y\in D_r}n\cdot y$, then for every $y\in D_r$, $p-y\in Q_r-Q_i$, so
$p+q_i=y+q_r$ for some $q_i\in Q_i$, $q_r\in Q_r$: a point strictly inside square $i$
(centre $p$, any angle in the row) and strictly inside the partner’s square (centre $y$,
any angle in row $r$). With (a), every pose the partner can still take collides with
square $i$ at $p$, so $p$ is forbidden.
The region is convex and the inequalities are linear, so checking the vertices checks
the region.

**Where enforced.** `collision.py` lines 233–284: the Minkowski difference is the exact
hull of pairwise differences in homogeneous integers (lines 257–263), facets are taken
from a counterclockwise chain with outward normals $(b_y-a_y,\ a_x-b_x)$ scaled by the
positive denominators (lines 265–268), the minimum over $D_r$ is taken over its vertices
by cross-multiplication (lines 269–275), and every vertex of the region is tested
against every facet of every live row, with any single failure a refusal (lines
278–283). The quantifier is universal in all three positions; nothing is skipped on an
empty list because an empty partner family is refused at line 242. `sequential.py` lines
172–180 admit a region only for a partner whose cover was admitted under (a), and the
region must also lie in the row’s legal domain (`collision.py` lines 245–248), which
does not bear on soundness but keeps the cover proof honest.

**Attempts to break it.** A region vertex pushed $10^{-7}$ past its tightest facet
(slack $5\times10^{-5}$) while staying in the legal domain: refused with “region escapes
universal collision set”.
A vertex pushed outward of the legal domain, a region naming the owner itself, and a
region naming a partner whose cover was removed: refused.
Independently, my verifier recomputed every facet check of 596 collision regions in the
certificate in exact rationals, 2,076,688 inequalities (section 4).

### (c) Replace-mode owned hulls capped at 16 vertices: sound

**Invariant.** Every point of $\mathrm{hull}(K_i\cup\text{kernel})$ is strictly inside
square $i$ in every surviving pose: $K_i$ by induction, each kernel point because it
satisfies every live row’s common-core planes $n\cdot x\le h+\min_v n\cdot v$ (so
$x-y\in Q_i$ for every residual vertex $y$, hence for every residual centre), and the
set of points strictly inside a square is convex.
Any set of points each proved a convex combination of that hull’s vertices is owned, and
so is its hull, whether or not it contains the old $K_i$.

**Where enforced.** `sequential.py` lines 404–418 (kernel points against every plane of
every row, dead rows contributing none; replace mode builds the new hull from the
compression points alone); `node.py` `compression_points` lines 313–345 (source hull
must equal `hull(prior + kernel)`, every retained point an exact convex combination of
at most three source vertices on the $2^{-20}$ grid, counts pinned).
The cap only weakens later steps; a smaller $K_i$ gives smaller forbidden regions and
weaker self-cuts, never a wrong one.

**Attempts to break it.** A retained vertex moved by one grid unit with its witness left
in place, an extra retained point with a copied witness, a kernel point pushed $10^{-7}$
past its tightest plane with the compression receipt rebuilt around it, and a prior hull
with an extra point: all refused.

### (d) Empty seed groups: sound

**Invariant.** An owner that owns nothing contributes no forbidden region, no self-cut
and no hull-intersection closure; its rows are its full legal domain.
Nothing is proved from an empty hull.

**Where enforced.** `node.py` lines 153–161 (`allow_empty_groups` only waives the
nonemptiness requirement; every listed point is still proved by `ownership`);
`sequential.py` line 181 drops the empty Minkowski set; `self_hull_cuts` is reached only
when cuts are supplied (line 137), and the producer supplies none; `hulls_meet` returns
no witness for an empty hull (line 227); promotion from an empty hull with a nonempty
kernel is `hull(kernel)` (line 413). In W7 five of the seven owners start empty, and
side-N0, the closing owner, owns nothing until round 4.

**Attempts to break it.** An unowned point added to a seed group is not refused but
reported `INCOMPLETE` by the ownership bisection (the tool then excludes nothing); a
seed row with a vertex dropped is refused.
The `INCOMPLETE` path fails safe but should be read as “unproved”, not as a refusal.

### (e) Closure derivation and the transfer: sound

**Invariant.** `all_parent_poses_forbidden`: the owner’s rows partition $[0,1]$ and
every row’s legal domain was covered by forbidden and collision regions with no
residual, so every legal pose of the owner is impossible.
`owned_hulls_intersect`: a common point of two owned hulls is strictly inside both
squares. Transfer: D4 maps the container and the cell set onto themselves, so a packing
realising a state $S\supseteq g(G)$ is carried by $g^{-1}$ to a packing realising
$g^{-1}S\supseteq G$, which the certificate forbids.

**Where enforced.** `sequential.py` `derived_closure` lines 337–350, run after every
step from the accepted state (line 435), and the declared closure must equal the derived
one with `closed` and `terminal` consistent (lines 437–442); `hulls_meet` lines 225–235
re-checks its witness against both hulls.
`frame.py` validates that every action maps the cell set onto itself by exact vertex-set
identity and that the actions are closed under composition (lines 67–78, 294–302), and
`states_containing` (lines 226–236) tests containment under every action.

**Attempts to break it.** A false `all_parent_poses_forbidden` and a false
`owned_hulls_intersect` declared on a live final step: both refused.
The count is reproduced in section 3.

### What I looked for and did not find

- A reversed quantifier: the collision loop refuses on the first failing (row, facet,
  vertex) triple; the partner cover requires one item per row.
- An inward rounding: `outward_round` rounds support bounds up; the producer’s grid
  rounding is never trusted, since every retained point carries an exact witness and the
  checker recomputes the planes.
- An open cell: every clip, residual, forbidden and collision region is closed, and the
  sweep decides closed coverage.
- The angle chart: $t\in[0,1]$ covers $\theta\in[0,\pi/2]$ and a square is invariant
  under quarter turns; the rows are closed, so a pose at a row boundary is in both rows.
- The wall: the legal box uses the half-extent $\min(c+s)/2$ over the row’s endpoints,
  proved on the whole row by the quadratic at `induction.py` lines 84–88; $U=L$ and
  $B=1$ so field and physical coordinates coincide.
- A partner cover that omits poses: the cover must list every accepted row and its
  domain must equal the hull of the current residual exactly.

One observation that is not a defect: the checker verifies a residual polygon’s
*coverage* role only; a residual extending outside the cell would still be accepted, and
the next step’s domain would be the cell cut by its supports.
That is sound because the hypothesis confines the centre to the cell anyway, and the
producer’s residuals are subsets of the legal domain in any case.

Two provenance observations, neither about the kernel’s arithmetic:

- The receipt’s fourteen `kernel_sha256` digests equal the modules at `fe152c30` byte
  for byte, but its `tool_sha256` (`13b5fd56…`) matches no committed version of
  `check_n17_subpattern.py` (`562e1b9d`: `893b5206…`; `214601ac`: `3b9e9264…`;
  `fe152c30`: `9f45b3a9…`). The receipt was written by a working-tree copy of the tool.
  The tool only orchestrates `admit_seed`, `replay_sequential` and the transfer, and the
  fresh-process re-check of saved objects (section 4) does not depend on it, but the
  admitted record should cite a committed tool.
- The receipt’s producer and checker ran in one process on in-memory objects; the
  `node_sha256` and `seed_sha256` it reports were the only trace until lane K2’s re-run
  saved the objects. Admission should bind the saved files, not the receipt’s digests
  alone.

## 3. The Geometry and the Transfer Count

**Transfer.** `transfer_count.py` reads the cover tool’s 24 cells and D4 permutations,
checks the eight permutations form a group, enumerates all $\binom{24}{17}=346{,}104$
states, and counts those containing any of the 8 distinct images of W7: **133,152**
states, confirmed by inclusion–exclusion over the images, in **16,701** orbits of the
43,593 (canonical form by minimum over the group).
Both numbers equal the receipt’s. The endpoint’s state (the seventeen cells in the
adaptation spec’s table) contains no image of W7.

**Placement search.** `w7_search.py` minimises, by Nelder–Mead on a soft-max surrogate
and then on the true objective, the worst of: the separating-axis penetration of every
pair, the signed distance of every centre outside its closed cell, and every container
excursion. Zero would be a feasible placement and a counterexample to the certificate.

| Pattern | Seed | Restarts | Best worst-violation | Tight pairs at the optimum |
| --- | ---: | ---: | ---: | --- |
| W7 | 1 | 40 | $9.05\times10^{-3}$ | W1–W2, W1–interior-W (both at the optimum value), interior-SW–interior-W ($2.3\times10^{-3}$) |
| W7 | 2 | 23 | $9.22\times10^{-3}$ | corner-SW–W0, N0–W2, W1–W2, W1–interior-W (all at the optimum value) |
| W7 minus interior-W | 3 | 3 | $0$, feasible with margin $3.1\times10^{-2}$ | — |
| W7 minus interior-SW | 3 | 1 | $0$, feasible with margin $2.0\times10^{-2}$ | — |

Both W7 seeds converge to the same arrangement: corner-SW nearly axis-parallel in its
corner, W0 against the wall at $y\approx1.7$, W1 pushed to the right edge of its cell
($x\approx1.38$–$1.40$, $y\approx2.63$–$2.66$) and tilted about $61^{\circ}$, W2 back at
the wall ($x\approx0.67$, $y\approx3.395$) at the same tilt, interior-W at the far
corner of its cell ($2.35, 2.34$) at the same tilt, and N0 in its upper right.
The column cannot be staggered enough: W1 and W2 share an orientation and are $0.99$
apart along their common axis.
So the best placement my search finds is infeasible by $9\times10^{-3}$, the selector’s
$1.1\times10^{-2}$ was not the infimum, and the two six-cell sub-patterns that drop
either interior cell are placeable with margins of $0.02$–$0.03$, in line with the
selector flagging nothing but interior crowds at arity 6. A float search proves nothing
either way; its value here is that it did not find the counterexample that a false
closure would have. The kernel’s final residuals (receipt `final_extents`) put W2 at the
*right* edge of its cell ($x\in[1.255, 1.364]$, $y\in[3.339, 3.386]$), not where the
near-feasible float arrangement puts it; that is no contradiction, since a residual need
only contain the feasible poses and there are none, but it means the certificate’s path
to contradiction and the float search’s tightest arrangement differ, which is worth
knowing before the second certifier (the interval branch-and-bound pilot) is compared
with it.

## 4. The Certificate Spot-Check

**The objects.** Lane K2 re-ran the tool in a fresh process from a worktree at
`fe152c30` (tool digest `9f45b3a9…`, the committed one) with `--save-objects`. The
producer is deterministic: the saved seed (`seed-8949a798….json.gz`, 8.9 kB) and node
(`node-2d516d00….json.gz`, 16.2 MB) have exactly the digests the original receipt
reports, and the fresh checker certified the closure again: `PASS_CERTIFIED_CLOSED`, 58
steps, 3,712 rows, 133,152 states, 16,701 orbits, producer 838 s, checker 930 s.

**My verifier.** `verify_cert.py` (410 s, exact `Fraction` arithmetic, its own hull,
clip, Minkowski difference, half-angle quadratics and area subtraction; no import from
`sqpack` or `devtools`) checked, from the two files and the cover tool’s cells alone:

- both files are canonical JSON whose SHA-256 is the file name, the node binds the seed,
  the seed’s 24 world polygons equal the cover’s cells, and the mask is W7;
- the seed: the four owned points (two for corner-SW, two for interior-SW) are re-proved
  owned by my own bisection on the half-angle with the interval product bound over the
  cell cut by the legal box; every one of the 448 seed rows is the cell cut by the row’s
  legal box, with that domain as its one residual;
- every step: the step’s prior hulls equal my replayed state; each of the 19,282 live
  partner cover rows has domain equal to the hull of the partner’s current residual
  vertices and a core strictly inside the square over the row’s interval; every promoted
  point satisfies every common-core plane of every live row, with the planes recomputed
  from the published core and residual vertices; every compression witness is an exact
  convex combination on the $2^{-20}$ grid; replace-mode hulls never exceed 16 vertices;
  dead rows have no outputs;
- 270 rows in full, all 64 rows of the closing step 57 and four sampled rows of each
  earlier step: the required domain (predecessor outer domain cut by the legal box), the
  strict core, 596 collision regions against every live row of their partner’s cover and
  every facet of my own Minkowski difference (2,076,688 inequalities), and coverage of
  the required domain by forbidden, collision and residual regions by the area argument:
  closed clipping subtraction leaves pieces of total area exactly zero, which suffices
  because an uncovered set would be relatively open and so of positive area;
- the closure: at step 57 none of side-N0’s 64 rows is closed by the wall box, every row
  carries a collision region against side-W2 (whose cover has 12 live rows) and 54 also
  carry one against interior-W; no row is covered by the six forbidden regions alone;
  every residual is empty; the derived closure is `all_parent_poses_forbidden` for owner
  5 at step 57, equal to the declared one, with no step after it; the final state equals
  the replayed one.

The verifier was first exercised on an 8-bin W7 stall (14 steps, all 112 rows in full,
257 collision regions), so its row logic is not specific to the closing node.

**Mutation suite.** `mutate.py` fed the kernel’s own checker 26 deliberately unsound
variants of the 8-bin objects (the unmutated objects pass): a collision-region vertex
$10^{-7}$ past its tightest facet; a vertex outside the legal domain; a region naming
the owner or an unadmitted partner; a partner cover domain shrunk, grown, stale, with a
live row declared empty, or with every row declared empty; a partner core scaled by
$1.02$ and by $1+10^{-6}$; the owner’s core scaled; a residual dropped or shrunk, with
and without its planes recomputed; a kernel point $10^{-7}$ past its tightest plane with
the compression rebuilt; a moved and an extra retained hull vertex; a grown prior hull;
a missing row; a false `all_parent_poses_forbidden` and a false `owned_hulls_intersect`;
a seed row with a vertex dropped; and an unowned seed point.
All 25 of the first kind were refused with the expected message; the unowned seed point
ends in `IncompleteError` (the ownership bisection cannot prove a negative), which the
tool reports as `INCOMPLETE` and excludes nothing.

**Controls.** Three placeable patterns that share most of W7’s cells were run through
the same producer and checker at the same settings, and all three stalled, as they must:
lane K2’s W7 minus side-N0 (`PASS_CERTIFIED_STALL`, 54 steps, 1,699 s), its endpoint
west-wall arity-7 pattern (14 steps), and my W7 minus interior-W, which the float search
places with margin $0.031$ (`PASS_CERTIFIED_STALL`, 30 steps, 1,920 rows, 701 s, a true
stall with round 4 equal to round 3 and every owner still at 64 live rows;
`control-w6a.json`).

## 5. Bottom Line

**The W7 exclusion can be admitted.** Each new grammar piece has a stated invariant that
the checker enforces at a named line; the checker refuses every unsound mutation tried;
the saved objects reproduce the receipt’s digests and certify in a fresh process; and an
implementation that shares no code with the kernel re-derives the closure from the
objects, re-proving every partner cover, the whole hull chain and 270 rows, including
the closing step entire.
The transfer count is exact and the endpoint survives.

Conditions, in order of weight:

1. **Bind the saved objects.** The admitted record should carry the seed and node files
   (or their digests with the files retained under the exploration), the fresh-process
   receipt from the committed tool (`9f45b3a9…`), and not the original receipt alone,
   whose `tool_sha256` (`13b5fd56…`) is of an uncommitted file.
2. **Retain the independent re-check and widen it.** This review’s `verify_cert.py` and
   its log should be kept beside the receipt with a `.txt` suffix, as the earlier
   reviews did. Its full-row form (all 3,712 rows) costs about ninety minutes on one core
   and should be run once before admission; nothing in the 270 rows suggests it would
   find anything, but a sampled check is a sampled check.
3. **Record the controls.** The two “minus one cell” stalls and the endpoint7 stall
   belong in the record next to the closure, since a kernel that closed a placeable
   pattern would be unsound whatever the certificate said.

**Condition 2, full-row form, done (2026-10-02, 15:56–17:11 UTC).** `verify_cert.py` was
run over the saved objects with every row selected (`… 64` as its last argument, under
`timeout 9000`, log `verify_W7_full.log`): all 58 steps replayed; 3,712 rows examined,
of which 3,324 have a legal domain and were re-proved in full (the other 388 are closed
by the wall box or an empty predecessor and were checked to have empty outputs); all
7,752 collision regions in the node re-verified against every live partner row and every
facet of my own Minkowski difference, 30,952,184 exact inequalities; 3,324 coverage
proofs by the zero-leftover-area argument; 19,282 partner cover rows; the whole
owned-hull chain; derived closure `all_parent_poses_forbidden`, owner 5 (side-N0), step
57, equal to the declared one; final state equal.
Wall time 4,497 s (75 min) on one core.
No row failed.

Not conditions, but worth doing: quote the selector’s best penetration as a search
result, not a margin; have the tool distinguish a seed point it could not prove from a
timeout; and, when the branch-and-bound pilot finishes on W7, compare its path to
contradiction with the kernel’s (section 3 notes they need not coincide).

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured, this review | The transfer count and orbit count; the endpoint’s survival; the placement search minima; the mutation refusals; the certificate spot-check |
| Read from code, this review | The invariants and enforcement lines of section 2 |
| Taken from the record | The receipt’s step and extent counts; the selector’s best penetration; the cover’s cells and D4 permutations (from `check_n17_capacity_one_cover`) |
| Not checked here | The n11-verbatim primitives (`clip`, `hull`, the sweeps, `ownership`), which are byte-pinned by n11’s receipts and were reviewed there |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
