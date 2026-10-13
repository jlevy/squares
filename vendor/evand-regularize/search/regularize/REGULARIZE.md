# REGULARIZE — display regularization of record packings (prototype, started 2026-10-09)

**Goal (Evan, 10-09):** drawings of the record packings that are "regularized" and "pretty": fewest angle groups
(exact test), squares on the grid where the slack allows, exact contacts, consistent orientation.  A derived *view* at
the same side S*; never a certificate change.  Iterative ("try things and see"); the cases worth discussing are the
ones where tie-breaks matter.  Background: jlevy's X-049 (`packing/campaign/explorations/X-049-...md` in the clone)
regularizes Couzo/de Winter records by greedy one-axis slides; his atlas shades by full-side contact count, so
loose squares render light.

## Code (`search/regularize/`)
- `reg.py N [--gravity yx|xy|sum] [--sym on|off] [--orient best|g] [--merge on|off] [--keep on|off]`: one record.
- `gallery.py N... --variants yx,xy,keep,keepxy,nosym,o1`: PNG rows in `runs/regularize/` (+ `index.html`).
- `census.py --procs K`: all 324 records, three gravity variants (+ nosym where the rigid part is symmetric);
  `runs/regularize/census.jsonl`.  ~7 s per record at n = 300; full census ~5 min on 10 processes.

Input: the 80-digit KKT point `search/exact/batch/work/n-N/{witness,polished}.exact.txt` + its free-square list.

## Method (v0)
1. **Orientation**: score each of the 8 container symmetries: empty-area centroid toward the top right; then tilted
   mass toward the top right; then emptiness toward the top rather than the right.  The last key only ever separates
   an image from its diagonal transpose (the first two keys are transpose-invariant): flagged `topright`, a convention.
   A tie on all three keys: `orient`.
2. **Angle groups**: θ mod 90 in (−45, 45], equal to 1e-50 at 80 digits (θ and −θ distinct).  Free squares are
   re-assigned to a group holding a force-carrying square (nearest angle first), else to a new 0 or 45 group;
   feasibility by the translation LP.  (Levels 1/3 of the plan, exact field test and certificate-backed merging of
   *determined* angles, not done yet: v0 only moves free squares.)
3. **Placement**: translation LP at fixed angles and fixed S*.  With angles fixed, non-overlap along a chosen
   separating face normal is linear in the centres, so every LP point is a true packing.  Trust region 0.5, normals
   re-chosen per iteration.  Objective = gravity toward the bottom-left corner (`yx` = down then left, weights
   (1e-3, 1); `xy`; `sum`).  Rigid-part symmetries (exact, 1e-40) imposed as equalities, free squares paired by
   nearest image.  `keep`: exact face contacts of the source are equalities (chains slide as units).
4. **Refine**: all centres re-solved at 80 digits from the constraints tight at the LP point (iterative refinement,
   min-norm least squares; constraints among unmoved squares kept only if exact in the input, < 1e-14).
5. **Verify**: every pair (separating-axis gap) and wall at 80 digits, min gap ≥ −1e-50.

Uniqueness probe: on the optimal face (objective ≤ opt + 1e-10) min/max a fixed random direction; spread > 1e-6 =
`face` (gravity does not decide).

Numerical traps found (all fixed, kept for the record): angle-equality test wrapped at ±45° (split the axis group);
merge committed float LP positions (1e-12 noise on "unmoved" squares); permutation direction inverted for quarter
turns (all k² grids refused symmetry); HiGHS default feasibility 1e-7 ≫ tight threshold; squares frozen along exact
flat modes carry ~5e-17 of float noise (n = 38's 45° chain) so refinement must let every square move; nearly-equal
distinct angles (n = 172: 7e-8°) make a float-tight contact cycle exactly impossible: such pairs, if apart in the
input, keep a 1e-8 clearance (`NEAR_GAP`).

## Census v0 (10-09, yx/xy/sum + nosym, keep off)
- 324 records, 0 errors; verified (all variants): 322.  Failures: **199** (LP-level overlap −1.2e-8 around #21/#78,
  not diagnosed), **292** xy (5e-18 inconsistency along a row #173–179).  Refused (LP infeasible at the start): 211,
  263, 272 ("bound only" records, not KKT points).  Stalled (alternate optima): 19, 291.
- 143 records have something to move; angle groups 1937 → 1353 in total, fewer in 101 records (n = 66: 31 → 2;
  n = 102: 25 → 6; n = 87: 16 → 3).
- Tie-break flags: `d_xy` 128, `d_sum` 118 (gravity order changes the picture), `d_nosym` 13 (10, 18, 19, 26, 37, 54,
  85, 107, 227, 258, 267, 290, 291), `face` 9 (18, 19, 26, 54, 85, 227, 258, 290, 291), `orient` 40, `topright` 224.
  37 records have no flag.

## Observations from the gallery (10-09)
- Plain gravity breaks a sliding 45° strip into separately slid pieces (n = 38, 27): ugly.  `keep` fixes it (the
  strip slides as a unit); `keepxy` at n = 38 is the cleanest picture.
- Symmetry imposed (n = 10, 26) gives the "centred" pictures: the n = 26 column under the diamond is centred, as in
  Friedman's drawing; without it the picture is lopsided.  n = 10's top rattler floats on the diagonal (symmetric,
  no contact) vs. against the wall (contact, asymmetric).
- Orientation rule puts the empty area top right; for the Göbel strips (27, 38) that makes the strip run ↘ (big grid
  blocks top-right and bottom-left), the transpose of the source drawings.

## Open questions for Evan (round 1)
1. Strip direction / which corner the main grid block takes (the `topright` convention, 224 records).
2. Symmetric-floating vs. pushed-into-contact when the rigid part is symmetric (n = 10, 19).
3. `keep` on by default?  Gravity order yx vs xy (n = 38: xy keeps the strip whole, yx shifts the top block).
4. Non-unique optima (`face`, 9 records): what should decide (centre in the free interval? second gravity?).

## Round 1 picks (Evan, 10-09) and round 2 rules
Picks: n = 10, 18, 19, 26, 37: the symmetric option (18: no central gap); 54: central strip in contact, fewest gaps
in it; 27, 38: symmetric; strips in general: the central strip an exact straight line where possible.  n = 10 means:
both rattlers hard in the corners, grid aligned, strip centred, symmetric gaps strip-to-rattler.

`--style pretty` (`pretty_place`):
1. **Largest feasible symmetry of the whole packing**, not only of the rigid part: every container symmetry with a
   pairing of all squares (assignment problem on nearest images, equal angles exactly, max distance 0.75) is tested
   by the LP; feasible ones combined greedily.  (n = 27, 38: rigid part has no symmetry, the packing can have three.)
2. **Tilted clusters close up**: each tilted square pulled toward its cluster's centroid (L1, auxiliary variables);
   straight chains (equal-angle tilted squares nearly face to face, offset < 0.25) imposed as equalities, all at
   once, else per chain, else per pair (rigid lattices with real offsets keep their offsets).
3. **Axis squares**: gravity toward the bottom left (1.5, 2) plus pull to the nearest walls (1).  Without symmetry
   gravity wins (vacancies to the top right: plain pull-to-walls moved k²−m holes into the interior, n = 21, 45);
   under symmetry a mirrored pair's gravity cancels and the wall pull puts rattlers in their corners (n = 10).
4. Tie-break: 1e-4 × gravity.

Census (pretty, 10-09): **324/324 verified** at 80 digits (incl. 199, 211, 263, 272, 292 that failed or were refused
under plain gravity); no non-unique optimum; symmetry imposed in 113 records; 131 records move; groups 1937 → 1353;
one stall (307).  Orientation ties (all keys): 40 records.

Open after round 2:
- n = 26: rule 2 attaches the extra 45° square to the diamond; Evan's round-1 pick had it separate, sitting on the
  axis square below (no panel showed the attached version then).
- Orientation: the strip direction / `topright` convention, and the 40 true ties (18 was flagged by Evan too).

## Round 3 (10-09): orientation fitted to jlevy; coincident faces
**jlevy's orientation = the source drawing.**  Best-fit container symmetry between our inputs and his
`witnesses/known-best/n-NNN.yaml` (assignment on centres, equal angles): identity for 317/324 (the rest are different
packings, not rotations); his pipeline has no re-orientation step.  So matching jlevy = keeping the source
orientation, and the question is which rule reproduces the sources:
- axis-only records (159): holes to the top right (row-major grid subsets): our rule matches 0.99;
- tilted records (84): the tilted band runs bottom-left to top-right in 53/65 directional cases; best lexicographic
  rule "band NE, then empty toward the top right, then toward the top" matches 0.46 (old rule 0.19; chance ≈
  0.15–0.25).  Misses are sources drawn NW–SE (17, 18, 50, 51, 66, 171, 230, 257, ...).
`orient_score` is now that rule, keys compared to 1e-3, final tie-break = the source image.  The angle merge now
runs before orientation (noise-tilted free squares spoiled the band test, n = 66).  Source orientation kept: 256/324.

**Coincident faces (Evan, n = 26: lone axis square on the grid, the 45° square with the diamond; "make parallel faces
coincident when possible").**  `--style coincide` = pretty, then a MILP maximizing the number of coincident faces
(equal-angle pairs flush along a face normal with zero offset along the face; axis squares flush on a wall), trust
region 0.75 from the pretty point, tie-break = the pretty linear weights scaled below one coincidence.  Symmetry is
kept unless dropping it gains a coincidence; then re-placed with the chosen coincidences as equalities.
Census (coincide): **324/324 verified**, all placements unique except 271; symmetry imposed 109, dropped for
coincidence in 26, 70, 85, 154, 227; re-placement infeasible (fell back to pretty) in 23 records (86, 106, 126, 127,
129, 146, 151, 154, 176, 179, 204, 207, 228, 236, 241, 258, 263, 272, 292, 297, 298, 299, 302): the MILP's normals /
trust region vs the iterated LP, to diagnose.  33 CPU-min for the whole census.

Other rule choices for "coincident faces" (not tried): count weighted by face length (partial overlaps), lexicographic
before the pulls vs after (now after: pulls first, coincidences from that point), per-square greedy snapping
(jlevy-style), L0 on gaps (fewest distinct gap values).

## Round 4 (10-09): strips vs arcs
Evan (jlevy atlas screenshot): strips run bottom-left to top-right, arcs the other way; "108, 129, 153 start to look
like the border -- there might not be a clean separation".  (Caveat: in jlevy's atlas 108, 129, 153, 154, 155, 179,
180, 199, 207-209, 236-239, ... are now itsnaka SQUISH packings, not our inputs; in our data 108/129/153 are clean
strips, sagitta <= 0.005.)
`shape_of`: principal axis of the tilted centres, quadratic fit of the normal offset; sagitta / S.  Strips <= 0.013,
Couzo arcs 0.11-0.22, gray zone 0.02-0.06 with no clean gap (171: 0.061 is a pair of blocks, 236: 0.060 a kinked
strip).  Kinds: strip (< 0.03), arc (> 0.08, or two+ separate tilted blocks of comparable size: 171, 198), gray
(between: source orientation).  Arc key: band runs top-left to bottom-right, convex side toward the bottom left,
then empty toward the top right.  `--orient-kind strip|arc|source` forces a branch (gallery `as-strip` etc.).
Couzo arcs 155, 180, 208, 240, 272 come out exactly as their sources (= jlevy's look); 211 (de Winter) rotated to
match them.  Agreement with the sources where jlevy's packing = ours: axis-only 159/159, strip 53/73, arc 2/8 (small
Schadt arcs 39, 41, 71 and the pairs 171, 198 rotated by 180° from the source: the bulge key is ~0 for a pair), gray
2/2.

## Round 5 (10-10): angle merging for force-carrying squares too
Evan: 301, 268, 207 look like they have squares that should be exactly grid aligned and aren't; "minimize number of
rotation groups is a high priority".  Cause: Couzo's float witnesses have almost no exactly-zero angle (301: 152
near-axis tilts, 268: 144, 207: 81); the exact solve snaps most to the axis class but keeps the ones its detected
contact structure ties to tilts (301: 131 squares, 1e-6..0.68 deg, 124 of them force-carrying).  That is a valid KKT
point of *that* structure, but not a necessary one: setting all of them to exactly 0 keeps a packing at the same
S* (LP + 80-digit refine/verify) in all three.  v0 only re-assigned free squares.
`merge_determined` (after `merge_angles`, before orientation): (1) straighten every group within 1 deg of the axis
(all at once, else per group, else per square); (2) repeatedly move the smallest tilted group to the nearest larger
group within 5 deg; accepted iff the translation LP at S* is feasible (same exact test as everything else).
Groups: 301 76 -> 4, 268 20 -> 4, 207 55 -> 6, 102 25 -> 4, all verified.  The 5 deg cap is a choice (bigger
rotations of a single square are visible changes); no cap = pure "fewest groups".

## Refresh from the store (10-10)
52 records had a stale batch input (46 beaten since the 10-05 batch by up to 0.03: SQUISH, Couzo updates, ours #399)
or no KKT point (6 "bound only").  `refresh.py --stale`: `pk.py get best:N` -> exactsolve, else slp2 polish ->
exactsolve, into `runs/regularize/exact/n-N/`; `reg.load` prefers a certified refreshed input (`REG_REFRESH=0`
turns it off).  The published exact batch is untouched.  Result: 51/52 certified (129 needed the polish); **261**
not certified even after polishing (stays on its old input).  No refreshed side is below the store's best beyond
rounding (2e-12 .. 8e-10, the exact optimum of the same packing; 305 matched a pending Couzo packing that arrived
mid-run, both certificate checkers VALID).
Atlas (coincide + merge_determined, refreshed inputs): **324/324 verified**; rotation groups 2355 -> 1126.  The
SQUISH bent strips (86, 108, 130, 154, 179, 207, 237, 269, 303) classify as arcs and form their own column running
top-left to bottom-right between the straight strips and the arcs.

## Policy (Evan, 10-10): keep true rotation groups; deliverable = source packings for jlevy's poster
"Keep true rotation groups and only merge when that is actually compatible with the exact packing, tolerance of
~ULPs when we don't have an exact one."  Presentation/colours are secondary.  `merge_determined` rewritten:
- determined angle (neither theta +- 1e-6 deg feasible at S*): kept; merged only with a group equal to 1e-12 deg
  (ULP level; exact data groups at 1e-50 anyway), if feasible;
- not determined (the angle can move at S*: flat rotations, angles frozen at the input's values): reassigned to an
  existing group, near-axis groups straightened together first (one at a time stranded 301's 12 squares at -0.23 deg
  in a tilted chain against a wall, 2e-12 inconsistent), else the nearest larger group, if feasible.
The round-5 version also merged *determined* groups within 5 deg (e.g. 268's -7.747 -> -5.742), i.e. a different
packing at the same side: dropped.  301: 76 -> 8 groups (was 4), 268: 20 -> 4, 207: 20 -> 6.
n = 175 (Ellsworth): a column of 7 squares at 0.801 deg in the source and in ours; not straightenable at S*: a true
rotation group that looks like a misaligned grid column at thumbnail size.
Poster output: `runs/regularize/poster/n-NNN.{cert,json}`: rational certificate of the regularized packing (scaled
by 1 + 1e-20 about the origin corner, as exactsolve; S' = S* + ~1e-19), checked by verify_cert.py in the run and
verify_cert2.py after (`verify2.txt`); JSON = 50-digit configuration, S*, S', provenance, angle changes.
**Run 10-10: 324/324 certificates VALID under both checkers, 324/324 verified at 80 digits; rotation groups 2355 -> 1171.**

## Same packing or not? (10-10)
Path test (`samepacking.py`): rotate the changed squares from source to final angles in <= 0.01 deg steps, re-solving
translations at S* each step.  27 records with angle moves > 1e-3 deg: 25 connected (moves up to 4.6 deg, 70: a caged
square through 22.5 deg); 267 and 302 blocked (joint path and group-by-group in both orders; 267 even on a ~0 deg move,
so probably the test's weakness: translations only, one angle path).  NEAR_GAP must be off on such paths (converging
angles trip it at s ~ 1).  All 27 regularized packings are local minima at S* by exactsolve (S equal to 1e-59, strict
modulo flat motions); 177, 238, 266 fail only the batch's lambda > 0 test because regularization makes force-free
squares touch exactly (promoted, zero multipliers).  Placement moves (LP iterations, coincidence MILP) are connected
by construction: each step stays in a convex region of valid packings (fixed separating normals).

## Decisions (Evan, 10-10): alternates allowed, levels, credit
Alternate packings at the record side are fine (aesthetic choices); publish several variants per n on our site and
let jlevy choose; define the terms; a "new packing at the existing record" may be claimed with careful wording if we
find no publication history (the side is the object of interest; the original finder is the record's source).
Levels for two packings at the same side S:
- 0 identical (container symmetry, relabeling); 1 same up to rattlers; 2 same packing, different arrangement:
  traversable without expansion (path at side <= S; shown by the path test); 3 alternate packing at the record side:
  valid, local minimum, not shown connected ("not shown connected" unless a barrier is shown).
- improvement (side can shrink): "tightened" (reached from the parent by a path that never expands) vs "new nearby";
  either way cite the parent arrangement; observers have both packings.  An improvement that lands in a *new* nearby
  arrangement is a new record claim (Evan): register check first, external post per his OK.
Variants per n: source; conservative (angle reassignments only if path-connected: level <= 2); fewest rotation groups
(determined groups within 5 deg merged too: level 3 allowed, classified by the path test).  Plus a short write-up page
with 3-5 example cases (a rotation, a slide, straightening, a kept true rotation group, an alternate).

## Variants and the two lists (10-10)
`reg.py --angle-policy free|conservative|fewest` (`merge_determined`): conservative = every angle move must pass the
path test from the current arrangement (path_ok: localized LPs, radius 3; 268: minutes -> 9 s; a ULP-move early
return dropped the new angles and looped forever at 267, fixed).  NEAR_DEG raised 0.01 -> 1 deg (302: contact cycles
among near-axis squares with distinct tilts 0.01 deg apart, 8e-11 inconsistent).
Full runs (`atlas.py compute --policy P`, `runs/regularize/poster/P/`): both 324/324 certificates VALID under both
checkers and 80-digit verified.  conservative: levels 0/1/2 = 178/30/116, groups 2355 -> 1171; fewest: 178/30/111/5
(level 3: 259, 266, 267, 270, 302), groups -> 1123.
`lists.py` -> `lists/best.*` (rule: fewest groups among verified variants, ties -> conservative; level 3 excluded
unless `--alternates-as-best yes`): 311 conservative, 13 fewest (70, 88, 129, 153, 172, 199, 236, 263, 269, 271,
292, 297, 301; all level 2 by the joint path test); orientation as source 275, otherwise 49.  `lists/alternates.*`:
ours (5 level-3) + Ellsworth's catalogue drawings at the record side (n <= 324): 40 same as the record up to
symmetry / rattlers, 22 distinct (different tilt structure), 8 same tilts placed differently (untested).
Caveat for the write-up: the path test samples the path (0.01 deg steps), it is not a continuous proof.

## Committed (10-10)
`lists/best.*`, `lists/alternates.*`, `lists/certs/` (gzipped certificate + 50-digit JSON per chosen packing; `alt/`
for our 5 alternates), atlas images `lists/atlas-result.png` (colour by angle) and `lists/atlas-result-groups.png`
(colour by exact rotation group).  Next session: the site viewer (see TODO.md).

## Refresh for the site (10-10 afternoon)
The store had newer records than the lists at 7 n (Couzo #488: 175, 209, 237, 270; ours #489: 132, 308; ry-xu's 261,
registered).  `refresh.py` + `atlas.py compute --ns ... --policy conservative|fewest` for those: 6 certified (VALID under
verify_cert and verify_cert2, 80-digit verified), lists regenerated (`lists.py` now rewrites a cert .gz only when its
content changed, deterministically; it ignores the site's own index entries).  270's level-3 alternate is gone (its record
moved).  **261 still does not certify**: exactsolve's certificate fails at −4.5e-14 among redundant contacts on ry-xu's
packing (`runs/regularize/exact/n-261/input.json`), and the slp2 polish then fails to solve; the lists keep the old 261
and the site draws ry-xu's packing as posted (`site/tools/provenance.py` 'raw').  Its certificate at the posted side comes from the register:
`register_cert.py 261` converts the register's rational witness exactly (bases are exact Pythagorean rotations, t = s/(1+c))
into `lists/certs/raw/n-261.cert.gz`, side 83393899377083393899377/5e21 ≈ 16.67877987541668; VALID under verify_cert and
verify_cert2 (min separation 1e-12: a dilated copy, ~7e-11 above exactsolve's optimum 16.6787798753429).

## Next
- Round-1 feedback → rules; then levels 1/3 of the angle plan (exact field equality for determined angles; merges
  backed by a certificate) and the flat rotational modes `minpoly.py` pins at an arbitrary rational t.
- Fix 199, 292; exact (field) verification of the output instead of 80-digit.
