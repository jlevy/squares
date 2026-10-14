# A203 -- H-consistency and piece-level pair compatibility in the fast count: the lemmas, for any n

The layer is the PI's.  Two readings of 2026-09-10 fixed it: on `fast30_k5_16_interior_Y0839.svg` (18:20) --
*"looking at how tight the BR and TR meeter options are, it seems like clipping H on both of those (and settling the
mutual clip) should basically kill all the options there ... Is there any way we bake something into the fast step to
help kill these super small slots?"* -- and on `fast30_k5_16_interior_Y0191.svg` (17:40) -- the TL(1,0) meeter pair
passes the hull tests (CN 1.056) but no pair of MEETING poses is disjoint: *"Is the geo pre-check ensuring that there
are options with enough distance between them?"* (`attempts/A202-fast30/notes/PI_pair_table_pieces.md`).  The
coordinator's grid check on Y0839 (`y0839_csp_gridcheck.py`) made the first reading exact: the count's witness option
in cell 10 has 78 admissible meeting poses and NOT ONE is disjoint from ANY admissible H pose, which the pairwise hull
table (A1 / CN / MK) cannot see.  So the fast count is made a small CSP on PIECES: every option must be compatible
with H (H exists), H must be compatible with some option of every slot a free square must meet, and a cover must
admit a COMMON H piece.  Every rule below is a SOUND necessary condition; an undecided pair is compatible; the
verdicts are `[C: closed-form trace]` -- no verifier clause exists yet (the certificate is the JSON trace).

Setting and notation = A202's `notes/fast30.md` s.0 (pieces = closed centre rect x closed tilt sub-bin; w(a) =
|cos a| + |sin a| the axis-parallel width of a unit square tilted by a; pins with certified cores; H = the conditioned
square with its record box x tilt window; forced slots p with widened open boxes B_p+, Theorem FC).  Code:
`code/csp203.py` (rule S, the node trees, the cached compatibility), `satbatch203.py` (rule S vectorised),
`csp203b.py` (units, option piece sets, the feedback), `csp203c.py` (masks, settle, the mutual clip), `count203.py`
(the count with the H-mask), the copies of A202's `fast30.py` / `fast30b.py` / `rules202.py` / `fig202.py`
(modified only here), `fig203b.py` (the page), `run203.py` / `run203.sh`.

## 1. Lemma PC (piece compatibility, rule S)  [T]

Let F, G be interior-disjoint unit squares with centres c_F, c_G and tilts t_F, t_G.  Then for some axis direction
phi in {t_F, t_F + 90} or {t_G, t_G + 90} (the square whose axis it is called A, the other B):

    |(c_G - c_F) . (cos phi, sin phi)|  >=  1/2 + w(t_B - phi)/2.

*Proof.*  Two convex polygons with disjoint interiors have a separating line parallel to an edge of one of them
(the separating-axis theorem); the projections of A and B on that edge's normal have disjoint interiors, so the
distance between the projected centres is at least the sum of the projected half-widths: 1/2 for A on its own axis,
w(t_B - phi)/2 for B (the projection of a unit square on a direction at angle a to its axes has half-width
(|cos a| + |sin a|)/2).  []

**Rule S (the piece-pair test).**  For pieces P_1 = R_1 x [a_1, b_1] and P_2 = R_2 x [a_2, b_2] let D = R_2 - R_1
(a closed rect: the centre differences d), with corners (r_k, alpha_k) in polar form.  For a tilt sub-interval
[p_0, p_1] of piece i's bin the projection distance on piece i's axes is bounded by

    max_{d in D, phi in [p_0, p_1]} |d . a(phi)|  <=  max_k  r_k cos( dist([p_0 - alpha_k, p_1 - alpha_k], 90 Z) )

(|d . a| is linear in d, so maximal at a corner of D; on the two axes phi, phi + 90 together |cos| v |sin| =
cos(dist to the nearest multiple of 90)), and the other square's half-width is at least 1/2 + w_min([a_j - p_1,
b_j - p_0])/2 (w is 90-periodic and concave between multiples of 90, so its minimum over an interval is at an
endpoint, or 1 when the interval contains a multiple of 90).  If the bound is < the half-width for every
sub-interval of BOTH bins (sub-intervals of width <= `step` = 4 deg; every comparison with the margin EPS = 1e-9 on
floats of outward-rounded rects), Lemma PC has no axis: NO pose pair of the two pieces is interior-disjoint -- the
pair is EXCLUDED.  Lemma CN is the special case "every corner of D has r_k < 1"; rule S exceeds CN only through the
tilt coupling (up to 1/2 + 1/sqrt2 = 1.207); beyond that distance no pair can be excluded (the fast pre-filter).
`csp203.sat_dead` (scalar), `satbatch203.sat_dead_batch` (numpy over a block of pairs; the sub-interval count is the
block's maximum -- finer, still sound).  Fuzz (`scratch/fuzz203.py`, 6000 random pairs at centre distance 0.85-1.25,
bins <= 20 deg): 2872 pairs declared dead, 300 random pose pairs + the 64 corner/endpoint pose pairs each: **0
refutations** (2026-09-10).

**Hierarchy.**  A node = (hull rect, list of tilt intervals, children); the test on a node pair is rule S over every
interval pair (a superset of the pieces: sound); a node pair is COMPATIBLE when some leaf pair under it is not
excluded, evaluated top-down with the first compatible leaf pair stopping the search, and cached per node pair and
per leaf block (`csp203.Compat`).

## 2. The variables (any n)

* **H's units.**  A202's alive H pieces (its box split nsub_h x nsub_h, tilt window in nbins_h bins, refined 2
  levels under P / W / the meet clip) grouped by their depth-`ud` ancestor (ud = 1: at most 8 x 8 x 8 = 512 units);
  a unit is a node whose leaves are its alive fine pieces.  H's units never grow; a unit dies with all its pieces.
* **An option row's pieces.**  A202's row (g, S) (cell g, slot set S) gets the piece set  P(g, S) = the intersection
  over p in S of the surviving pieces of slot p in cell g  (dyadic pieces: the intersection of two lists is the
  finer piece wherever one contains the other, `csp203b.inter_pieces`).  *Sound:* a pose of a free square with
  centre in g meeting every B_p+ (p in S) lies in a surviving piece of every slot p in S (each slot's rules are
  necessary conditions on a meeter of p), hence in P(g, S).  A row with P(g, S) empty is dropped.  The row's node:
  hull -> coarse groups (sub-rect x coarse tilt bin) -> the pieces as leaves.

## 3. Lemma HC (H-consistency)  [T]

In every packing of the page H exists, so a free square realising the row (g, S) has a pose in P(g, S) that is
interior-disjoint from H's pose, which lies in some alive H piece.  Hence: **if no piece of P(g, S) is compatible
(rule S) with any alive H piece, the row (g, S) is dead** -- and with it every row (g, S') with S' a superset of S
(its poses meet every slot of S too).  For a SINGLETON row (g, {p}) this kills every surviving piece of slot p in
cell g (each such piece IS the row's piece set), which feeds A202's unions, caps and Theorem FC.  Letter **H** on
the page (rule "H" in the certificate).

## 4. Lemma MC (the mutual clip)  [T]

Let p be a forced slot (Theorem FC: two distinct non-pin meeters of B_p+) such that no conditioned square other
than H may meet B_p+ (A161's miss test on the other roles' boxes, `roles_reach`).  Then at least one FREE square
meets B_p+ (Corollary FC-count: the non-pin squares are H and the free squares, and two distinct meeters are
needed), i.e. some row (g, S) with p in S is realised by a free square interior-disjoint from H.  Hence: **an H
unit compatible with no alive row containing p is dead** ("MC:p").  Iterating Lemma HC and Lemma MC (rows die ->
units lose their cover -> units die -> rows lose their partners -> ...) reaches a fixed point in milliseconds; H's
surviving pieces are the alive units' pieces, H's box is their hull (never grown), and A202's H-dependent rules
(C, M, L) re-run on the shrunken H in the next round (the fixed point with the option build).  If every unit dies
the page is DEAD (no pose of H is compatible with the free meeter some slot must have).

## 5. The SETTLE refinement (the PI's "settling the mutual clip")  [T]

For a row whose compatible leaf pairs (option piece, H piece) are few (<= 400), each pair is refined: the option
piece is split 2 x 2 x 2 (centre quadrants x tilt halves) up to 3 levels, every child re-tested by A202's rules
(P pins, W walls, C / M against H's hull and groups, L chord rows; R reach for every slot of S; A161's exact miss X
for every slot of S) and by rule S against the H piece; a child failing any test holds no pose realising the row
disjoint from that H piece (each test is a necessary condition; a child's poses are a subset of the parent's, and
the inherited chord bounds are lower bounds for the child).  A pair all of whose children die at some level is
EXCLUDED; when every pair of a (row, unit) dies the unit's bit leaves the row's mask; a row whose mask empties is
dead -- letter **F**.  Budgets: fan-out <= 64 surviving children (else the pair stays compatible), 2 s per row,
6 s per round; results cached per (piece, H piece, S).  Undecided = compatible (sound).

## 6. Theorem COUNT-CSP (the count with the H-mask)  [T]

Theorem COUNT (A198) / COUNT-PAIR (A201) with two more necessary conditions on a cover: (i) the chosen H row
(g_H, S_H) names the units of H that may sit in g_H and meet every slot of S_H (A202's `role_options` clip; the
mask m_H), and every chosen free row (g, S) has its compatibility mask m(g, S) = the alive units with a compatible
piece; a cover needs  m_H AND m(g_1, S_1) AND ... AND m(g_k, S_k) != 0  (H's actual pose is ONE piece, compatible
with every chosen free square) -- the search ANDs along the branch and prunes on empty; (ii) two chosen free rows
must be compatible on their PIECE sets (rule S hierarchically; Lemma A1 on the hulls kept), so a slot's demand-2
pair is tested over the MEETING pieces of the two rows, never over cell hulls (the PI's Y0191 reading).  If the
capped exact search finds no cover, the page is DEAD (`count203.count_search`; prunes counted per rule).  The
bar-H counts (H forced at p when no cover without H at p exists) run with the same masks.

## 7. Soundness checks and the audit

* Fuzz of rule S: s.1.  A202's rules P / W / C / M / L / R / X / meet: A202's fuzz (`fast30.md` s.4).
* Audit of the kills by sampling (`scratch/audit203.py`): for every dead row (H / F) sample admissible poses
  (container, pin cores) on a grid over the row's hull x its tilt intervals that meet every slot of S, and every
  admissible H pose on a grid over H's RECORD box x window; a sampled disjoint pair would refute the kill.  Y0839
  g1: 6 dead rows, 216 / 11 meeting admissible poses each, 2975 H poses, **0 refutations**.  After the fix of the
  artefact below, on the regenerated certificates (7 x 7 x 25 grids; H restricted to the poses meeting every slot
  forced BEFORE the round of the kill -- the forcing is a hypothesis of every later round): Y0839 g1 0, Y0191 g1 0
  (21 rows), Y0054 g1 0 (7 rows, H forced at BL(1,0)), **Y0842 g1 0 (17 rows, the page's kill)**, and the count's
  pair exclusions 0 on all four; Y0044 g1: the four round-2 kills of cell 17's BR(1,0) rows show 89 of 329 meeting
  poses disjoint from SOME record-box H pose meeting BL(1,0) -- every such H pose lies in a unit the round-1 mutual
  clip killed (MC:BL(1,0), units (0, 0-2, 3-7)), and for the 27 of them re-checked no admissible BL(1,0) meeter
  disjoint from the H pose exists in any alive BL(1,0) row (`scratch/audit_y0044.py`): the kills stand on Lemma MC,
  which the sampling does not refute.  Logs `logs/audit_*.log`.
* Kept rule (A202): a stage-0 kill of a page that the exact tests leave alive is a bug until proved otherwise; the
  CSP adds constraints the exact table never had (H-consistency), so its kills are audited by sampling first.
* **The artefact this rule caught (2026-09-10 17:50).**  The first population run "killed" Y0054 at the g1 pad by the
  count: 22 pair exclusions, every one between a free BL(1,0) / BR(1,0) row (cells 5, 10, 15) and H's row at cell 11.
  A201's exact seeded clip had left the page ALIVE at g1, so the kill was suspect; a 15 x 15 x 16 grid over H's
  record box found the admissible disjoint pair F = (1.504, 0.500, 0 deg) | H = (1.949, 1.519, 82.4 deg), both
  meeting BL(1,0)'s box -- REFUTED.  Cause: a fixed role's row is a hull-only node (hull x tilt intervals, no
  pieces); `Compat._ok` walked it as an internal node with NO children, so every (free row, H row) pair that
  survived the hull test was excluded vacuously (`any` over an empty list).  Fix: a hull-only node is a leaf block
  (one row per tilt interval); regression fuzz `scratch/fuzz203b.py` (3,000 random trees / hull leaves against the
  brute force over leaf pairs; the 13 disagreements are the numpy block's finer sub-intervals, checked by pose
  sampling: 0 refutations).  The population results and certificates were regenerated after the fix; the pages
  killed before it (none besides the Y0054 artefact) are not reused.

## 8. Y0839 (both pads)

The witness option of A202's count -- cell 10 serving BL(1,0) + BR(0,1) + BR(1,0), hull [2.190, 2.226] x
[0.698, 0.770], 11 pieces (all at tilt 62-71 deg: the only poses that reach BR(0,1)'s box) -- survives the
node-level rule S against 11 of H's 512 units (nearest at max centre distance 1.0025: two poses at tilt 64.01 in
opposite corners of the two pieces are separated along the common axis by 1.0005 -- but the option's corner pose
does not meet BR(0,1)); the SETTLE refines its 133 compatible leaf pairs, all die (R / X / S on the children), and
the row is DEAD by **F** (315 ms at g1) -- the coordinator's grid conclusion, reproduced in closed form.  The
singleton (10, BR(0,1)) dies the same way (15 pieces killed), and cell 7's BR(1,0) rows (330 pairs).  The mutual
clip kills 87 of H's 512 units (MC:BR(0,1)).  The count then finds another cover (cell 15 for the triple), and the
bar-H count forces H at BR(0,1) (A202 forced nothing).  Verdict ALIVE at both pads: **25 s / 22 s** (A202's
stage 0 is 16 s of it; the CSP: build 0.65 s, masks 2.6 s = 84,714 node tests + 1.86 M leaf pairs in numpy blocks,
settle 3.5 s at g1 / 1.9 s at pad 0; round 2 cached).  Audit by sampling (`logs/audit_Y0839_g1.log`): 0 refutations.

## 9. Y0191, Y0044, Y0054

* **Y0191** ALIVE both pads (14 s / 14 s): the mutual clip kills 416 of H's 512 units (MC:BL(1,0)) before A202's
  forced clip; 21 rows dead (cell 17's BR / TL rows by F, cells 10 / 12 by H); the count's TL(1,0) pair is now
  (8, 18) -- the PI's pair 14 | 18 is NOT excluded by rule S at piece resolution (656 x 282 pieces, hull max
  distance 1.53: the two rows' pieces are too coarse for the closed form; `logs/pair_y0191.log`), while the
  13 | 14 and 13 | 18 TL(1,0) pairs are.  Settling an option PAIR (the analogue of s.5 on both sides) is the
  closed-form next step; A201's exact test remains the fallback.
* **Y0044** ALIVE both pads (17 s / 17 s): H 512 -> 161 units (MC:BL(1,0)), cell 17's rows dead (H / F), H forced
  at BL(1,0) as in A202.
* **Y0054** ALIVE at g1 (33 s: H 512 -> 1 unit, cell 15's seven rows dead by H, H forced at BL(1,0)); DEAD at pad 0
  by A202's FC at BL(1,0) (H provably misses, CN cap 1: s0-only, WINDOW-PENDING).  The first run's g1 "kill" was
  the artefact of s.7 and is withdrawn.

## 10. The table over the 39 pages A202 left alive at stage 0 (both pads; `results/report203.md`)

Columns: A202's stage-0 / stage-1 verdicts; A203's verdict (seconds); H units built -> alive after the mutual clip;
dead rows by rule H / F; the mutual clip's unit kills per slot; the settle's per-rule kills; the CSP milliseconds
(build / masks / settle) of round 1; H forced.

| page | pad | A202 s0 / s1 | A203 (s) | H units -> alive | dead rows H / F | mutual clip | settle kills | count prunes mask / pair | CSP ms build / masks / settle | forced H |
|---|---|---|---|---|---|---|---|---|---|---|
| k5_11_Y0130 | g1 | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 512 | 0 / 4 | - | M:365,P:3924,R:4,S:2099 | - | 406.4 / 482.6 / 458.7 | - |
| k5_11_Y0130 | zero | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 512 | 0 / 4 | - | M:365,P:3900,R:516,S:1583 | - | 419.4 / 534.6 / 423.1 | - |
| k5_11_Y0147 | g1 | ALIVE / ALIVE | **ALIVE** (21) | 512 -> 192 | 1 / 2 | TR(0,0):320 | M:1084,P:696,R:5331,S:8327 | - | 317.0 / 1080.5 / 66.7 | - |
| k5_11_Y0147 | zero | ALIVE / ALIVE | **ALIVE** (19) | 512 -> 189 | 1 / 2 | TR(0,0):323 | M:1036,P:2216,R:5668,S:7181,W:395 | - | 307.2 / 1021.2 / 56.7 | - |
| k5_11_Y0202 | g1 | ALIVE / ALIVE | **ALIVE** (12) | 512 -> 512 | 0 / 0 | - | R:1944,S:986,X:6 | - | 422.0 / 1092.0 / 186.2 | - |
| k5_11_Y0202 | zero | ALIVE / ALIVE | **ALIVE** (12) | 512 -> 512 | 0 / 0 | - | R:24,S:8 | - | 455.0 / 1115.4 / 104.4 | - |
| k5_11_Y0275 | g1 | ALIVE / DEAD | **ALIVE** (15) | 512 -> 511 | 0 / 2 | TL(1,0):1 | C:52,M:329,R:208,S:2023,W:3660 | - | 296.2 / 1422.8 / 288.8 | - |
| k5_11_Y0275 | zero | ALIVE / - | **ALIVE** (15) | 512 -> 511 | 0 / 2 | TL(1,0):1 | C:52,M:329,R:198,S:1825,W:3036 | - | 296.6 / 1365.6 / 275.8 | - |
| k5_11_Y0308 | g1 | ALIVE / ALIVE | **ALIVE** (19) | 512 -> 464 | 0 / 4 | TR(0,0):48 | C:500,M:259,P:396,R:1022,S:9006,W:1050,X:62 | - | 371.8 / 572.0 / 474.7 | - |
| k5_11_Y0308 | zero | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 464 | 0 / 6 | TR(0,0):48 | C:384,M:379,P:396,R:1548,S:9634,W:5398,X:42 | - | 378.6 / 592.5 / 718.7 | TR(0,0) |
| k5_11_Y0662 | g1 | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 446 | 2 / 1 | TR(0,0):48 | C:51,M:269,R:1938,S:4411,W:566 | - | 359.6 / 461.0 / 70.6 | TR(0,0) |
| k5_11_Y0662 | zero | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 432 | 4 / 1 | TR(0,0):48 | C:87,M:777,R:6136,S:9072,W:566 | - | 365.2 / 474.0 / 4014.3 | TR(0,0) |
| k5_11_Y0672 | g1 | ALIVE / ALIVE | **ALIVE** (18) | 512 -> 512 | 0 / 2 | - | M:4,P:12 | - | 440.9 / 694.9 / 47.2 | - |
| k5_11_Y0672 | zero | ALIVE / ALIVE | **ALIVE** (21) | 512 -> 512 | 0 / 2 | - | C:50,M:276,P:12,R:3482,S:2705,W:2262 | - | 368.0 / 664.0 / 2074.7 | - |
| k5_11_Y0738 | g1 | ALIVE / ALIVE | **ALIVE** (16) | 448 -> 448 | 2 / 0 | - | M:286,R:2395,S:5267,X:578 | - | 414.2 / 554.9 / 2400.5 | - |
| k5_11_Y0738 | zero | ALIVE / ALIVE | **ALIVE** (17) | 448 -> 448 | 2 / 2 | - | M:286,R:3071,S:3503,X:831 | - | 402.3 / 777.7 / 2323.6 | - |
| k5_11_Y0985 | g1 | ALIVE / ALIVE | **ALIVE** (24) | 512 -> 441 | 2 / 3 | TR(0,0):48 | C:729,M:761,R:4032,S:15092,W:2144,X:10 | - | 353.5 / 629.1 / 6135.3 | TR(0,0) |
| k5_11_Y0985 | zero | ALIVE / ALIVE | **ALIVE** (22) | 512 -> 423 | 2 / 3 | TR(0,0):48 | C:1039,M:893,R:4583,S:14250,W:2144,X:123 | - | 332.9 / 591.7 / 6144.6 | TR(0,0) |
| k5_11_Y1104 | g1 | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 273 | 5 / 0 | TR(0,0):48 | C:24,M:886,R:3704,S:5820 | - | 449.8 / 742.9 / 3690.6 | TR(0,0) |
| k5_11_Y1104 | zero | ALIVE / ALIVE | **ALIVE** (21) | 512 -> 229 | 5 / 0 | TR(0,0):48 | C:24,M:750,R:3518,S:3466 | - | 473.2 / 784.4 / 2660.8 | TR(0,0) |
| k5_16_Y0027 | g1 | ALIVE / ALIVE | **ALIVE** (28) | 512 -> 512 | 0 / 0 | - | C:280,M:1720,P:1176,R:1072,S:26021,X:1070 | - | 853.7 / 1336.0 / 6017.6 | - |
| k5_16_Y0027 | zero | ALIVE / ALIVE | **ALIVE** (29) | 512 -> 512 | 0 / 0 | - | C:564,M:1410,P:1700,R:194,S:26146,X:554 | - | 936.1 / 1301.7 / 6582.5 | - |
| k5_16_Y0044 | g1 | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 161 | 4 / 4 | BL(1,0):351 | P:896,R:1472,S:1370,W:274 | - | 504.7 / 1334.1 / 318.0 | BL(1,0) |
| k5_16_Y0044 | zero | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 161 | 4 / 0 | BL(1,0):351 | M:356,P:896,R:4388,S:3354,W:274 | - | 503.1 / 1272.4 / 2183.9 | BL(1,0) |
| k5_16_Y0054 | g1 | ALIVE / ALIVE | **ALIVE** (33) | 512 -> 1 | 7 / 0 | - | M:327,S:5031,W:420 | - | 871.6 / 3329.5 / 7091.6 | BL(1,0) |
| k5_16_Y0054 | zero | DEAD / - | **DEAD** (30) | 512 -> 512 | 0 / 0 | - | S:4557 | - | 955.0 / 3562.9 / 6362.6 | - |
| k5_16_Y0083 | g1 | ALIVE / ALIVE | **ALIVE** (31) | 512 -> 33 | 0 / 0 | - | C:3642,M:149,P:3564,R:12800,S:15708,W:3667,X:96 | - | 623.4 / 2095.3 / 6417.2 | BL(1,0) |
| k5_16_Y0083 | zero | ALIVE / ALIVE | **ALIVE** (27) | 512 -> 12 | 0 / 7 | - | C:1518,M:543,P:1768,R:7784,S:25435,W:1882,X:1354 | - | 777.4 / 1919.6 / 6938.8 | BL(1,0) |
| k5_16_Y0099 | g1 | ALIVE / ALIVE | **ALIVE** (18) | 512 -> 512 | 1 / 0 | - | P:336,S:126,W:210 | - | 521.7 / 2106.0 / 164.6 | - |
| k5_16_Y0099 | zero | ALIVE / ALIVE | **ALIVE** (19) | 512 -> 512 | 1 / 0 | - | P:336,S:126,W:210 | - | 438.1 / 2415.7 / 191.6 | - |
| k5_16_Y0191 | g1 | ALIVE / DEAD | **ALIVE** (14) | 512 -> 96 | 10 / 11 | BL(1,0):416 | M:369,P:124,R:3692,S:1823,W:2288 | - | 435.7 / 1013.9 / 653.5 | BL(1,0) |
| k5_16_Y0191 | zero | ALIVE / - | **ALIVE** (14) | 512 -> 96 | 10 / 7 | BL(1,0):416 | M:209,P:124,R:132,S:1287,W:2288 | - | 413.1 / 980.3 / 455.6 | BL(1,0) |
| k5_16_Y0230 | g1 | ALIVE / ALIVE | **ALIVE** (24) | 512 -> 151 | 0 / 0 | BL(1,0):2 | C:2244,M:3797,P:1110,R:3590,S:21773,W:522,X:298 | - | 637.5 / 1714.5 / 4254.8 | BL(1,0) |
| k5_16_Y0230 | zero | ALIVE / ALIVE | **ALIVE** (27) | 512 -> 118 | 0 / 0 | BL(1,0):2 | C:1628,M:1913,P:764,R:3104,S:18263,W:9,X:232 | - | 782.2 / 2055.7 / 3599.4 | BL(1,0) |
| k5_16_Y0249 | g1 | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 512 | 8 / 2 | - | M:60,P:4216,R:268,S:3715,W:2591,X:107 | - | 496.7 / 2343.3 / 643.9 | - |
| k5_16_Y0249 | zero | ALIVE / ALIVE | **ALIVE** (24) | 512 -> 512 | 10 / 2 | - | M:60,P:4078,R:519,S:3441,W:2591,X:107 | - | 638.5 / 2574.0 / 541.0 | - |
| k5_16_Y0275 | g1 | ALIVE / DEAD | **ALIVE** (23) | 512 -> 511 | 0 / 1 | TL(1,0):1 | C:4,M:413,P:128,R:1194,S:1161,W:62 | - | 607.4 / 1573.0 / 582.3 | - |
| k5_16_Y0275 | zero | ALIVE / - | **ALIVE** (25) | 512 -> 511 | 0 / 1 | TL(1,0):1 | M:413,P:124,R:9322,S:5449,W:62,X:850 | - | 545.3 / 1262.6 / 3086.4 | - |
| k5_16_Y0325 | g1 | ALIVE / ALIVE | **ALIVE** (53) | 512 -> 512 | 0 / 1 | - | C:352,M:1362,P:254,S:16097,W:3274,X:2208 | - | 2129.4 / 2036.5 / 8016.0 | - |
| k5_16_Y0325 | zero | ALIVE / ALIVE | **ALIVE** (49) | 512 -> 512 | 0 / 1 | - | C:464,M:1282,P:342,R:616,S:12847,W:4346,X:444 | - | 1587.6 / 2180.0 / 8005.3 | - |
| k5_16_Y0380 | g1 | ALIVE / ALIVE | **ALIVE** (26) | 512 -> 146 | 1 / 3 | - | M:399,R:337,S:25633,W:108 | - | 779.7 / 1473.2 / 3393.0 | BL(1,0) |
| k5_16_Y0380 | zero | ALIVE / ALIVE | **ALIVE** (26) | 512 -> 101 | 3 / 0 | - | M:399,R:775,S:25087 | - | 763.3 / 1949.8 / 3429.4 | BL(1,0) |
| k5_16_Y0402 | g1 | ALIVE / ALIVE | **ALIVE** (34) | 512 -> 273 | 0 / 0 | BL(1,0):239 | S:8214,W:4478 | - | 528.9 / 3165.6 / 6385.6 | BL(1,0) |
| k5_16_Y0402 | zero | ALIVE / ALIVE | **ALIVE** (34) | 512 -> 273 | 0 / 0 | BL(1,0):239 | S:8414,W:4610 | - | 639.5 / 3336.4 / 6405.8 | BL(1,0) |
| k5_16_Y0436 | g1 | ALIVE / ALIVE | **ALIVE** (27) | 512 -> 512 | 0 / 0 | - | S:7528,W:3388 | - | 627.3 / 1810.9 / 7662.3 | - |
| k5_16_Y0436 | zero | ALIVE / ALIVE | **ALIVE** (25) | 512 -> 512 | 0 / 0 | - | M:120,R:1392,S:7575,W:3006 | - | 725.3 / 1581.1 / 6145.5 | - |
| k5_16_Y0460 | g1 | ALIVE / ALIVE | **ALIVE** (57) | 512 -> 132 | 0 / 11 | BL(1,0):380 | M:1968,P:60,R:988,S:39975,W:8006,X:552 | - | 550.1 / 1398.9 / 6433.6 | BL(1,0) |
| k5_16_Y0460 | zero | ALIVE / ALIVE | **ALIVE** (38) | 512 -> 132 | 0 / 5 | BL(1,0):380 | M:1634,P:60,S:21920,W:3360,X:60 | - | 542.0 / 1540.2 / 6332.9 | BL(1,0) |
| k5_16_Y0491 | g1 | ALIVE / ALIVE | **ALIVE** (24) | 512 -> 499 | 3 / 0 | BR(0,1):13 | M:126,R:24,S:440,X:70 | - | 527.0 / 2839.0 / 260.4 | - |
| k5_16_Y0491 | zero | ALIVE / ALIVE | **ALIVE** (26) | 512 -> 497 | 3 / 0 | BR(0,1):15 | M:126,R:96,S:98,X:46 | - | 606.2 / 2839.1 / 240.1 | - |
| k5_16_Y0500 | g1 | ALIVE / ALIVE | **ALIVE** (30) | 512 -> 510 | 0 / 0 | TR(0,1):2 | C:192,M:1194,P:1332,R:220,S:17277,W:705,X:1728 | - | 618.9 / 1769.6 / 6099.4 | - |
| k5_16_Y0500 | zero | ALIVE / ALIVE | **ALIVE** (29) | 512 -> 510 | 0 / 0 | TR(0,1):2 | C:192,M:1176,P:1332,R:812,S:16517,W:705,X:1758 | - | 549.5 / 1675.2 / 6045.7 | - |
| k5_16_Y0565 | g1 | ALIVE / ALIVE | **ALIVE** (28) | 512 -> 512 | 0 / 3 | - | C:39,M:425,P:672,R:28,S:553,W:1308 | - | 876.4 / 3082.1 / 410.2 | - |
| k5_16_Y0565 | zero | ALIVE / ALIVE | **ALIVE** (27) | 512 -> 512 | 0 / 3 | - | C:39,M:425,P:672,S:549,W:1308 | - | 712.8 / 2421.1 / 330.0 | - |
| k5_16_Y0660 | g1 | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 440 | 0 / 3 | BL(1,0):72 | C:12,M:235,P:1108,R:1387,S:3087,W:1107,X:95 | - | 639.9 / 1301.4 / 1441.2 | BL(1,0) |
| k5_16_Y0660 | zero | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 440 | 0 / 3 | BL(1,0):72 | M:731,P:1092,R:8878,S:8111,W:4415,X:754 | - | 614.2 / 1193.6 / 1545.0 | BL(1,0) |
| k5_16_Y0719 | g1 | ALIVE / ALIVE | **ALIVE** (33) | 512 -> 512 | 1 / 0 | - | R:8979,S:9946,W:5128,X:164 | - | 467.1 / 2461.8 / 6370.2 | - |
| k5_16_Y0719 | zero | ALIVE / ALIVE | **ALIVE** (44) | 512 -> 511 | 1 / 0 | TR(0,1):1 | R:17744,S:10648,W:9232,X:564 | - | 871.2 / 3692.4 / 7847.8 | - |
| k5_16_Y0839 | g1 | ALIVE / ALIVE | **ALIVE** (25) | 512 -> 425 | 0 / 6 | BR(0,1):87 | C:336,M:536,P:90,R:10690,S:17401,W:1056,X:1024 | - | 652.2 / 2556.0 / 3510.1 | BR(0,1) |
| k5_16_Y0839 | zero | ALIVE / ALIVE | **ALIVE** (22) | 512 -> 425 | 0 / 6 | BR(0,1):87 | C:136,M:256,P:90,R:3536,S:13045,W:1056,X:332 | - | 475.0 / 2468.5 / 1896.9 | BR(0,1) |
| k5_16_Y0842 | g1 | ALIVE / DEAD | **DEAD** (27) | 512 -> 512 | 0 / 17 | - | M:6978,P:6316,R:128,S:17556,W:16622,X:64 | - | 374.1 / 1451.8 / 6575.5 | BR(0,1) |
| k5_16_Y0842 | zero | ALIVE / - | **DEAD** (29) | 512 -> 512 | 0 / 17 | - | M:6870,P:6172,R:128,S:17242,W:16482,X:44 | - | 424.1 / 1595.3 / 6505.3 | BR(0,1) |
| k5_16_Y0865 | g1 | ALIVE / ALIVE | **ALIVE** (44) | 512 -> 327 | 4 / 0 | BL(1,0):155 | P:1884,S:13063,W:7432 | - | 697.1 / 1860.3 / 6614.4 | BL(1,0) |
| k5_16_Y0865 | zero | ALIVE / ALIVE | **ALIVE** (42) | 512 -> 302 | 4 / 0 | BL(1,0):155 | P:3200,R:1156,S:20294,W:7673,X:20 | - | 609.8 / 1788.7 / 6570.8 | BL(1,0) |
| k5_16_Y0881 | g1 | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 512 | 0 / 8 | - | C:206,M:169,P:6,R:8,S:752,W:438 | - | 616.3 / 2051.9 / 282.7 | - |
| k5_16_Y0881 | zero | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 512 | 0 / 4 | - | C:206,M:113,P:6,S:752,W:438 | - | 631.8 / 2002.4 / 257.8 | - |
| k5_16_Y0941 | g1 | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 512 | 5 / 0 | - | M:1228,R:1920,S:1888,X:48 | - | 629.5 / 1801.7 / 1435.0 | - |
| k5_16_Y0941 | zero | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 512 | 1 / 0 | - | M:1228,R:1844,S:1488,X:48 | - | 648.9 / 1587.8 / 1290.5 | - |
| k5_16_Y0991 | g1 | ALIVE / ALIVE | **ALIVE** (22) | 512 -> 484 | 0 / 4 | BL(1,0):25 | C:208,M:16,P:960,R:476,S:626,W:438 | - | 581.8 / 1803.7 / 356.6 | BL(1,0) |
| k5_16_Y0991 | zero | ALIVE / ALIVE | **ALIVE** (23) | 512 -> 475 | 0 / 0 | BL(1,0):25 | P:216,S:432,W:420 | - | 600.3 / 1732.0 / 309.5 | BL(1,0) |
| k5_16_Y1022 | g1 | ALIVE / ALIVE | **ALIVE** (26) | 496 -> 452 | 4 / 0 | BL(1,0):14,BR(1,0):30 | - | - | 848.6 / 1797.6 / 226.3 | BR(1,0) |
| k5_16_Y1022 | zero | ALIVE / ALIVE | **ALIVE** (27) | 496 -> 452 | 0 / 0 | BL(1,0):19,BR(1,0):25 | R:230,S:162,X:54 | - | 742.6 / 2099.7 / 276.6 | BR(1,0) |
| k5_16_Y1056 | g1 | ALIVE / ALIVE | **ALIVE** (17) | 512 -> 512 | 0 / 7 | - | M:2995,P:1152,R:3328,S:4910,W:1698,X:1152 | - | 449.2 / 1823.5 / 1779.0 | - |
| k5_16_Y1056 | zero | ALIVE / ALIVE | **ALIVE** (16) | 512 -> 512 | 4 / 3 | - | M:483,P:1152,S:1854,W:1698 | - | 449.7 / 1575.1 / 531.3 | - |
| k5_16_Y1110 | g1 | ALIVE / ALIVE | **ALIVE** (20) | 512 -> 512 | 0 / 0 | - | M:212,P:3238,R:853,S:1791 | - | 511.5 / 1684.0 / 2626.4 | - |
| k5_16_Y1110 | zero | ALIVE / ALIVE | **ALIVE** (26) | 512 -> 512 | 0 / 1 | - | M:191,P:11650,R:2139,S:4331,X:88 | - | 512.7 / 1601.9 / 2789.4 | - |
| k5_16_Y1117 | g1 | ALIVE / ALIVE | **ALIVE** (19) | 512 -> 512 | 0 / 0 | - | P:1072,R:4892,S:732,X:72 | - | 483.9 / 1713.2 / 2386.7 | - |
| k5_16_Y1117 | zero | ALIVE / ALIVE | **ALIVE** (21) | 512 -> 512 | 0 / 0 | - | P:1280,R:1080 | - | 455.5 / 1685.4 / 2271.3 | - |

KILLS:
- k5_16_interior_Y0054 zero: FC at BL(1,0): at most 1 distinct non-pin meeter(s) (H provably misses; anonymous cap 1 by CN: union diameter 0.9387 < 1) [pad 0: s0-only, WINDOW-PENDING]
- k5_16_interior_Y0842 g1: FC at BL(1,0): at most 1 distinct non-pin meeter(s) (H provably misses; anonymous cap 1 by CN: union diameter 0.9495 < 1)
- k5_16_interior_Y0842 zero: FC at BL(1,0): at most 1 distinct non-pin meeter(s) (H provably misses; anonymous cap 1 by CN: union diameter 0.9495 < 1) [pad 0: s0-only, WINDOW-PENDING]

**Summary.**  78 (page, pad) runs, median 23 s, max 57 s (13 runs over 30 s: the settle's 6 s budget on pages with
many near pairs -- Y0325, Y0460, Y0865, Y0719 -- on top of A202's 17-28 s).  296 option rows dead (115 by H, 181 by
F), 4,606 H units killed by the mutual clip on every page, H forced on 34 of 78 pads (10 more than A202's stage 0:
Y0839 BR(0,1), Y0308 / Y0985 TR(0,0), Y1022 BR(1,0), Y0660 BL(1,0), Y0842 BR(0,1)).  Kills: **k5_16_interior_Y0842
at the g1 pad** (window-valid; A202 needed stage 1's exact table for it): round 1's F kills (cells 6 and 15) and
round 2's (cell 21, cell 15's BL / BR rows) leave BL(1,0) with a refined union of diameter 0.9495 < 1 (cap 1) and H
provably missing it -- Theorem FC; plus Y0054 at pad 0 (A202's).  Every other page ALIVE: the CSP's value on them is
the H clip (units -> alive), the dead rows and the forcings, all inputs to stage 1 / the trees.
