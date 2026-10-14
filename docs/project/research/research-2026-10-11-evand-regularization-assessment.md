# Assessment: Evan Daniel’s regularization process, and adapting it to every packing n = 1..324

**Bead:** think-kl2v (epic think-cdud; feeds think-ux1v). **Date:** 2026-10-11.
**Scope:** this assessment and its plan were written as the whole of pull request #497,
which has since taken the [regularization policy](../policies/regularization-policy.md)
as well.
The regularization itself (think-ux1v) is not started and lands later in its own
pull requests, after the owner answers the questions at the end.
**Upstream:** `attic/evand-square-packing` at `060c1a1` (main’s head on 2026-10-11),
read in full under `search/regularize/`, `search/exact/` and `search/exact/batch/`;
nothing under the checkout was modified.
Three counts ($n = 10$, 26 and 70) were run through the whole pipeline in a scratch
replica tree under a scratch virtualenv, with `python -I`; the timings and the
cross-tabulation are in the appendix, [Measurements](#appendix-measurements).
The cross-tabulation, the tilts of the refused records and the certificates’ angles are
re-derived by `packing/devtools/compare_evand_regularization.py` (OR-1), whose commands
the appendix gives.

**Amended 2026-10-11, the upstream pin.** Upstream’s head has since moved to `675a5ea`
(`675a5eaa8712542daac8b4515b0f69ad7044df44`, 2026-10-11T10:34-06:00). Between the two
commits, `search/regularize/` and `search/exact/` gained
`search/regularize/posted_cert.py`, `search/exact/lean_batch/run-2026-10-10b.out` and
raw certificates under `lists/certs/raw/` for the 16 records posted after the lists
(146, 153, 155, 156, 176, 181, 207, 211, 238, 239, 261, 270, 271, 272, 304, 305), which
upstream draws “as posted (raw) … until they are regularized”: 15 are new files, and n =
261’s replaces the `register_cert.py` conversion with a posted refinement.
Nothing else there changed
(`git diff --stat 060c1a1 675a5ea -- search/regularize search/exact`). The code the
pipeline runs, `lists/best.json`, `lists/alternates.json` and the 324 chosen
certificates are byte-identical, so every measurement here, made at `060c1a1`, holds at
`675a5ea`; `crosstab` run against `675a5ea`’s `lists/best.json` reproduces the
appendix’s figures. The adaptation pins `675a5ea`.

**Amended 2026-10-12, the project-side figures and the answers.** Every figure here
about the project’s own layer (its 68 regularized, 182 unchanged and 74 refused records,
the cross-tabulation’s project side and the refused records’ split by tilt) was measured
against `packing/atlas/known-best/regularized/index.json` at `5c9f4f2`, and stays as
written. The index has moved since with main’s records: on 12 October 2026, after #518
and #553, it reads 71 regularized, 181 unchanged and 72 refused, 42 of them with every
tilt at 45 degrees and 30 with another (`compare_evand_regularization refused-tilts`).
The owner answered on 12 October 2026, question 3 first;
[section 9 of the regularization policy](../policies/regularization-policy.md#9-owner-decisions)
records each answer, and the default it applies where none is recorded.
think-ux1v is carried out in the stacked pull requests #509 to #559.

## Conclusions in brief

1. The process is a translation-LP display regularizer over an 80-digit KKT point.
   Angles are fixed per iteration, so every LP point is a true packing; symmetries and
   coincident faces are imposed as equalities; angle groups are merged where a
   feasibility LP at side $S^{\ast}$ says they can be.
   Its output is checked at 80 digits and then written as a rational certificate that is
   a *dilated* copy: scaled by $1 + 10^{-20}$ about the origin corner and rounded up, so
   the certified side $S'$ is never $S^{\ast}$. The two upstream checkers, and this
   project’s two maintained exact routes, accept every certificate tried here.
2. The certificate proves $s(n) \le S'$ exactly and nothing else.
   “Exact optimum” means a KKT point of $\min S$ subject to the detected contact
   structure, with numerical second-order, multiplier and corner-corner checks at 80
   digits; “same packing” (level 2) means a float LP found translations at $S^{\ast}$ at
   0.01-degree samples along one straight angle path.
   Neither is a proof, and the upstream log says so.
3. Dependencies are numpy, scipy (HiGHS LP and MILP) and mpmath, all already in this
   project’s lockfile; the licence is MIT and covers `search/regularize/` and
   `search/exact/`. The inputs the regularizer reads (`batch/work/*.exact.txt`, and the
   refreshed store inputs under `runs/`) are not in the checkout; the committed
   `batch/inputs/` and an exact solve regenerate them.
   Full cost for $1 \le n \le 324$ is about 3 to 4 CPU-hours on this host (roughly 1 to
   1.5 hours wall at four workers): far above any routine gate ceiling, so the generator
   runs on request and only the verification is gated.
4. Upstream’s best-choice lists change 147 of the 324 records (30 rattlers only, 117
   level 2) and re-orient 48; this project’s `regularize_axis_components/2` changes 68.
   Every record the project changes, upstream also changes; upstream additionally
   changes 72 of the project’s 74 refused records and 7 of its 182 unchanged.
   It can, because it works on the KKT point and certifies a dilated rational copy,
   which is exactly what the project’s atlas layer refused on 2026-10-02 as “a tier
   promotion under a drawing’s name” or “changes the side”.
5. The sound adaptation keeps the upstream code as a pinned third-party generator and
   puts every decision in this project’s checkers and record: convert the witness at
   full precision, run the exact solve and the regularizer at the pin, import each
   certificate through the existing `evand-cert` adapter, decide it over $\mathbb{Q}$ on
   both maintained routes, measure identity with `arrangement_gap`, and then, where
   every rotation in the view is rational in the witness’s own frame, re-solve the tight
   contacts over $\mathbb{Q}$ at the witness’s side so the view is literally at the same
   side. Where that is impossible (an irrational optimum: squares at exactly 45 degrees,
   as at 43 of the project’s 74 refused records, or other irrational tilts, as at
   $n = 11$), the view is a dilated certificate whose side relation the owner must rule
   on: a register result where $S'$ is below the verified bound, and otherwise not a
   drawing frame under the current atlas policy.
   *Amended 2026-10-11:* the plan now vendors the pinned generator at `675a5ea` under
   `vendor/evand-regularize/` with Evan Daniel’s MIT notice and credit, and reviews and
   adjusts its automated output by hand under the
   [regularization policy](../policies/regularization-policy.md) (section 5).
6. Recommend adopting the `conservative` variant only, in the source orientation, as the
   drawing layer’s generator where it is sound at the same side; keep
   `regularize_axis_components/2` as the fallback and as the non-regression reference;
   treat `fewest` merges of determined groups as alternates, never drawn as the same
   packing in the project’s own voice.
   Eight owner questions are listed at the end; question 3 should be answered first,
   because it decides what slice 4 is.

## 1. The process, step by step

The driver is `reg.regularize` (`search/regularize/reg.py:1074-1142`), run per count by
`atlas.py compute` (`atlas.py:42-71`), with the two lists built by `lists.py`. The order
is: load, free-square angle merge, determined-angle merge under a policy, orientation,
symmetry detection, placement (gravity, pretty or coincide), refine at 80 digits, verify
at 80 digits, certificate.

### 1.1 Inputs and the refresh from the store

`reg.load` (`reg.py:50-67`) reads `search/exact/batch/results.json` for the count’s
status, finder (`by`) and register value, then the 80-digit configuration
`batch/work/n-N/{witness,polished}.exact.txt` (a header line with $n$ and $S$, then $x$,
$y$ and the angle in degrees per square) and its `.json` for the free-square list
(`free_squares_exact`). Angles are folded into $(-45, 45]$ modulo 90 (`fold`,
`reg.py:70-73`). When `runs/regularize/exact/n-N/` holds a refreshed input with
`cert_valid` and `newton_converged` (`refreshed`, `reg.py:38-47`) it is preferred unless
`REG_REFRESH=0`.

`refresh.py` (`refresh.py:35-70`) makes those: `pk.py get best:N` exports the store’s
best packing (register, pending and upstream’s own) to text, `exactsolve.py` solves it;
if the certificate does not validate, `slp2.py` polishes it (a local optimizer, side as
decimal) and exactsolve runs again.
`--stale` (`refresh.py:73-84`) selects every $n$ whose batch input is worse than the
store’s frontier by $10^{-9}$ or is not a KKT local minimum.
REGULARIZE.md ("Refresh from the store") reports 51 of 52 stale records certified, 261
never (exactsolve’s certificate fails at $-4.5 \cdot 10^{-14}$ among redundant contacts
on Ryan Xu’s packing), for which `register_cert.py` (`register_cert.py:21-34`) converts
this register’s rational center-basis witness exactly, $t = s/(1 + c)$, into a
certificate at the posted side instead.

What the checkout holds: `batch/inputs/n-N.txt` (324, the register witnesses reduced to
float64 centres and angles in degrees by `batch/register.py:39-57,117`),
`batch/certs/n-N.cert` (324) and `batch/results.json`. `batch/work/` and all of `runs/`
are gitignored (`search/exact/batch/.gitignore:1` and the root `.gitignore:9`), so
neither the 80-digit KKT points the regularizer reads nor the refreshed store inputs are
present; `batch/reproduce.sh` re-solves from `inputs/` in “~1-2 CPU-hours for all”.
The lists name the input source per count: 272 from the exact batch, 52 refreshed from
the store.

### 1.2 The exact solve

`search/exact/exactsolve.py` (docstring `:2-18`, method in `search/exact/README.md`)
takes an approximate packing and returns a nearby KKT point of **$\min S$ subject to
non-overlap**, with the contact structure detected at the input:

1. contacts: corner-on-side and corner-on-wall incidences whose gap is below a tolerance
   (`find_contacts`, `:104`), chosen from a ladder from $10^{-9}$ to $10^{-6}$ so that
   the contacts admit an equilibrium; pure corner-corner touches are set aside as
   disjunctions;
2. the load-bearing set $A$: the max-support solution of the jam-LP dual,
   $\lambda \ge 0$, $\sum_k \lambda_k \nabla g_k = \nabla S$ (`max_support`, `:198`);
   squares with no contact in $A$ are free (rattlers or force-free);
3. the KKT system on an independent subset $B$ of $A$ (rank-revealing QR), $g_B = 0$ and
   stationarity for every variable, with exact flat directions frozen; Gauss-Newton
   projection onto the contacts (`KKT.polish`, `:305-330`) then chord Newton with
   residuals in mpmath at `dps` digits (default 80) and a float64 Jacobian;
4. free squares re-placed to clearance $\ge 10^{-6}$; wedged ones promoted into the
   system (`:900-941`);
5. verification, numerical: redundant contacts and frozen stationarity rows
   $\le 10^{-70}$; every pair and wall SAT-separated in mp; multipliers re-identified at
   the exact point and an LP for $\max \min \lambda > 0$ (`:996-1008`); reduced Hessian
   of the Lagrangian on $\operatorname{null}(J_A)$, zero modes probed by moving
   $10^{-3}$ and projecting back (`:1011-1032`); the corner-corner MILP for first-order
   descent in every branch (`:1034-1046`); pairs touching but separated by another side
   line are released (`:975-991`);
6. the certificate: scale about the origin corner by $1 + \varepsilon$
   ($\varepsilon = 10^{-20}$), round centres and $t = \tan(\theta/2)$ to $10^{-35}$
   (`rdig = 35`), $S' = \lceil S(1 + \varepsilon) \rceil$ at 30 places, and check with
   `verify_cert.verify` in process (`certificate`, `:725-747`; `:1081-1089`).

`S_exact` is the Newton point’s $S$ printed at `dps - 15` digits (`:956`). “KKT local
min” in `batch/results.json` (318 of 324; 6 “bound only”: 177, 211, 230, 261, 263, 272)
means every numerical test above passed; it is not a proof of local minimality, and the
exact-form and `localmin.py` certificates under `search/exact/minpoly/` are a separate,
later layer (270 exact forms committed) that the regularizer does not use.
The certificate proves $s(n) \le S'$ over $\mathbb{Q}$; it proves nothing at $S^{\ast}$
itself, where feasibility is known only to 80 digits.

Measured here (appendix): 0.3 s at $n = 10$, 0.5 s at $n = 26$, 3.0 s at $n = 70$; the
README says about 5 s at $n = 110$ and “a few minutes” at $n = 300$.

### 1.3 Angle groups and the translation LP

A display group is a class of $\theta \bmod 90$ equal to within `EQ_TOL = 1e-50` at 80
digits (`angle_groups`, `reg.py:124-134`; $\theta$ and $-\theta$ distinct).

`place` (`reg.py:181-298`) is the one feasibility and placement engine.
Variables are the $2n$ centre coordinates; the angles and $S^{\ast}$ are fixed.
For every pair within reach the separating normal is chosen at the current point as the
face normal (of either square) maximizing the gap (`best_normal`, `:149-162`), and the
non-overlap condition along that normal is linear in the centres (`:205-215`), so every
LP point is a true packing, not a linearization.
Walls are variable bounds, with a trust region 0.5 (`:224-235`); symmetries are affine
equalities (`:237-246`, `affine` `:301-308`); kept contacts and straight chains are
equalities (`:216-223`). The objective is per-square linear weights (gravity) plus L1
pulls through auxiliary variables (`absobj`, `:250-266`). HiGHS solves it at primal and
dual feasibility $10^{-10}$ (`:267-269`); iterations re-choose normals until the move is
below $10^{-11}$ or the objective stalls (`:270-284`, status `stalled` or
`not converged`). A uniqueness probe optimizes a fixed pseudo-random direction over the
optimal face and flags a spread above $10^{-6}$ (`:286-297`). Pairs with nearly equal
but distinct angles that are apart in the input keep a clearance `NEAR_GAP = 1e-8`,
because a float LP cannot see that closing a cycle of such contacts needs equal angles
(`:191-200`, `NEAR_DEG = 1` degree).

What stays fixed: $S^{\ast}$, every angle, every symmetry imposed, kept contacts.
What moves: centres, within the trust region per iteration.

### 1.4 Symmetries and coincident faces

Two notions. `symmetries` (`reg.py:111-119`) finds container symmetries
$g = 1, \ldots, 7$ (`d4`, `:78-88`) that map the rigid part onto itself to $10^{-40}$,
completed on the free squares by nearest image (`:1107-1114`). `sym_candidates`
(`:760-779`) is the round-2 rule: every $g$ with an assignment of *all* squares to
nearest images within 0.75 and equal angles, feasibility left to the LP. `pretty_place`
(`:845-898`) tries each candidate alone, then combines feasible ones greedily, with
straight tilted chains (`chain_pairs`, `:782-802`: equal-angle tilted pairs nearly face
to face) as equalities, falling back per chain, then per pair.
The objective (`pretty_objective`, `:824-842`) pulls tilted squares to their cluster’s
centroid (L1) and axis squares toward the bottom-left corner (weights 1.5 and 2) plus
toward their nearest walls (weight 1), with a $10^{-4}$ gravity tie-break.

`coincidences` (`:902-987`) is a MILP (scipy `milp`, time limit 60 s, gap 0): one binary
per candidate coincidence, an equal-angle pair flush along a face normal with zero
offset along the face, or an axis square flush on a wall, a big-M of 4, trust region
0.75 from the pretty point, objective = number of coincidences with the pretty weights
scaled below one coincidence as tie-break.
`pretty_coincide` (`:990-1018`) runs it with and without the chosen symmetry, drops the
symmetry only if that gains a coincidence, then re-places with the chosen coincidences
as equalities and the chosen walls as pins; an infeasible re-placement falls back to the
pretty point (`coinc_replace: infeasible`, 23 records in the round-3 census).
The lists were made with `--style coincide` (`atlas.py:176`).

### 1.5 Angle merging, and the `conservative` and `fewest` variants

`merge_angles` (`reg.py:575-602`) runs first and only on free squares: each is
reassigned to the nearest group holding a force-carrying square, else to a new 0 or 45
group, whenever the feasibility LP at $S^{\ast}$ accepts the new angle.
Only the angle is committed; positions are left to placement.

`merge_determined` (`:660-757`) then runs under `--angle-policy`:

- step 1, ULP merges: groups within `ULP_DEG = 1e-12` degrees of each other merge into
  the larger (inexact inputs; exact data is grouped at $10^{-50}$ anyway);
- step 2, undetermined groups: a group is *movable* if the LP at $S^{\ast}$ is feasible
  with the group’s angle shifted by `PERTURB_DEG = 1e-6` degrees either way (`:718`);
  movable near-axis groups (within 1 degree) are straightened together, then each
  movable tilted group, smallest first, is reassigned to an existing group of at least
  its size (axis preferred when near it), if feasible; determined groups are kept;
- step 3, `fewest` only: determined groups too are moved to the nearest larger group
  within `cap` = 5 degrees, repeatedly, if feasible (`:738-753`).

`free` accepts on LP feasibility alone.
`conservative` additionally requires `path_ok` from the current arrangement for every
accepted change (`accept`, `:680-692`), and the arrangement’s positions follow the path
(`:755-756`). `fewest` is `free` plus step 3; its level is decided afterwards (1.6).
REGULARIZE.md’s round-5 log first described step 3 as “a different packing at the same
side” and dropped it; the 10 October policy readmitted it as the `fewest` variant under
the path test, with level 3 allowed.

### 1.6 Level classification and the sampled path test

`path_ok` (`reg.py:618-657`): rotate every changed square from its current angle to the
target together, linearly in angle, in steps of at most `PATH_STEP_DEG = 0.01` degrees
(at least two); at each sampled angle re-solve translations at $S^{\ast}$ by `place`
from the previous step’s positions, with trust region 0.25, first feasibility only, then
up to eight zero-objective iterations; only squares within radius 3 of a rotating square
may move, and if that fails everything may move; `NEAR_GAP` is switched off for the
path. Returns blocked at the first infeasible sample.
The docstring says it: “sufficient, not necessary (translations only, one angle path)”.

`level_of` (`atlas.py:19-39`): 0 if nothing moved and no angle changed (orientation
aside); 1 if every touched square is free; 2 for `conservative`, or `fewest` without a
determined merge; for `fewest` with determined merges, the angle merges are recomputed
from the source and one joint `path_ok` from the source angles decides 2 or 3.
`samepacking.py` (`samepacking.py:25-57`) is the standalone form of the same test, plus
`kkt_test` (`:60-86`), which re-runs exactsolve on the regularized output and reports
whether it is itself a numerical KKT local minimum at $S^{\ast}$ (27 records with angle
moves were; 177, 238 and 266 fail only the $\lambda > 0$ test because regularization
makes force-free squares touch).

What a level-2 verdict means: at every sample of one straight path in angle space, a
float LP (HiGHS, $10^{-10}$) found a translation of the nearby squares at side
$S^{\ast}$ with no overlap along the chosen normals, with the placement slides
“connected by construction” because each LP iteration’s feasible set is a convex
polytope of valid packings at fixed normals.
It is not shown that the motion between samples is feasible, that the chosen normals
admit every feasible translation, or that the 80-digit refined point (which differs from
the LP point by up to the tight tolerance) lies on the path.
It says nothing about whether another path, or a different arrangement at the same side,
exists.
A level-3 verdict means this one test was blocked, not that a barrier exists (267
is blocked “even on a ~0 deg move”, which the log attributes to the test’s weakness).

### 1.7 Orientation

`shape_of` (`reg.py:510-536`) classifies the tilted part as strip (sagitta below 0.03 of
the side), arc (above 0.08, or two tilted blocks of comparable size) or gray;
`orient_score` (`:539-557`) ranks the eight container images by a lexicographic key
fitted to this project’s atlas drawings (band direction, empty area toward the top
right, then the top), keys compared to $10^{-3}$, final tie-break the source image
(`orientations`, `:560-570`). The merge runs before the orientation (noise-tilted free
squares spoiled the band test).
The best-choice lists keep the source orientation at 276 of 324 and change it at 48.
Orientation is a drawing convention, not regularization; this project records such
isometries explicitly (`devtools/atlas_orientation.py`, the $n = 211$ reflection).

### 1.8 Refine and verify at 80 digits

`refine` (`reg.py:322-462`) re-solves the centres from the constraints tight at the
float LP point: wall contacts within $10^{-9}$, pair gaps below $10^{-9}$ along the LP’s
normal recomputed at 80 digits, symmetry rows; every square is a variable (frozen flat
modes carry about $10^{-17}$ of float noise); a constraint among squares the LP did not
move is kept only if it is an exact contact of the input (below $10^{-14}$), so a true
gap just below the tight threshold is not forced shut (`:382-396`). Twelve rounds of
min-norm least squares with mpmath residuals, residual scaled before the float solve,
stopping below $10^{-75}$. `verify` (`:465-488`) takes the minimum over walls and over
pairs of the best separating-axis gap at 80 digits and passes when that least gap is
$\ge -10^{-50}$ (the run here: $-7 \cdot 10^{-71}$ at $n = 10$, $-1.3 \cdot 10^{-71}$ at
26 and $-3.2 \cdot 10^{-71}$ at 70, i.e. contacts closed to the working precision).

### 1.9 The certificate, the lists and the checkers

`write_cert` (`reg.py:1023-1043`) does what `exactsolve.certificate` does: scale by
$1 + 10^{-20}$ about the origin corner, round to 35 digits, round $S'$ up at 30 places,
verify in process with `verify_cert`. `compute_one` (`atlas.py:42-71`) writes
`n-NNN.cert` and a 50-digit JSON (`S_exact`, `S_cert`, `cert_valid`, `verify_80`, input
source, finder, orientation $g$, symmetry, shape, groups before and after,
`angle_changes`, `policy`, `level`, `level_text`, and the note “regularized display view
of a certified packing at the same side; not a new bound”). `lists.best`
(`lists.py:34-52`) picks per $n$ the verified variant with the fewest groups, ties to
`conservative`, level 3 excluded by default; `package` (`:148-162`) gzips certificate
and JSON deterministically into `lists/certs/` (324 + 4 alternates + the raw 261).
`alternates` (`:55-119`) lists upstream’s four level-3 variants (259, 266, 267 and 302,
the “ours” entries of `alternates.json`; REGULARIZE.md:222 still says five, counting
270’s, which the store refresh superseded, REGULARIZE.md:229) and Ellsworth’s catalogue
drawings at the record side, matched by assignment on the rigid part.

The checkers share no geometry: `verify_cert.py` (`:9-13`, `:35-71`) parses rational
$x$, $y$ and $t$, builds $(c, s)$ from $t$, and requires, with strict inequalities,
every square in the open box and every close pair separated by one of the four face
normals; `verify_cert2.py` (`:4-7`, `:41-68`) builds the four rational corners and
requires no vertex of either square in the closed other and no closed edges meeting.
Both are stdlib `Fraction`. Both decide with strict inequalities (`verify_cert.py:9,63`;
`verify_cert2.py:4-7`): a touching pair or a corner on a wall is refused, so a packing
with its contacts closed could never pass them, and that is why the certificate is a
dilated copy with nothing touching (least wall clearance exactly $\varepsilon/2$, least
gap just under $10^{-20}$, as the T-146 review measured).
This project’s maintained routes accept a zero sign, so a same-side view with exact
contacts is decidable here and not there.
Note on the sample at $n = 10$: the two 45-degree squares (8 and 9) are written with
$t = \tan(22.5^\circ)$ rounded to 35 digits, so each certified square is a rational
rotation just past 45 degrees, not 45 degrees; an exactly 45-degree square has no
rational pose at all.

## 2. Dependencies, licence and cost

**Libraries.** `reg.py`: numpy, scipy (`linprog` HiGHS, `milp`,
`linear_sum_assignment`), mpmath.
`exactsolve.py`: numpy, scipy (linalg, linprog, sparse), mpmath.
`gallery.py` and `atlas.py draw`: matplotlib (drawing only).
`register_cert.py`: PyYAML. The checkers: stdlib.
Python 3.14 runs all of it.
This project’s `pyproject.toml` already declares mpmath, numpy and scipy (lines 20-23;
all three in `uv.lock`), so the adaptation adds no dependency.

**External tools.** The store (`search/packer/pk.py`) and the polish (`slp2.py`, which
imports upstream’s `rigid` and `inc` modules) are needed only by `refresh.py`; this
project’s witnesses replace the store, and a packing that will not certify without
polishing is a case to report, not to polish silently (the upstream log’s own treatment
of 261).

**Licence.** `LICENSE` at the root is MIT, “Copyright (c) 2026 Evan Daniel”;
`README.md:54-59` says the code is MIT-licensed and carves out only `site/www/data/`
(Ellsworth’s drawings).
`search/regularize/` and `search/exact/` are code, so the MIT grant covers them, with
the notice to be kept with any copy.
`CREDITS.md` ("Provenance of this work") says the work was produced by an AI model under
human direction.
The upstream lists’ inputs are this register’s witnesses (CC BY 4.0) and
the store’s.

**Measured cost** (appendix; this 4-core host shared with other lanes).
exactsolve: 0.3, 0.5 and 3.0 s at $n = 10$, 26 and 70.
`atlas.py compute --policy conservative --style coincide` on all three: 2.6 s wall;
`fewest`: 2.5 s. Both upstream checkers: at most 0.22 s per count at $n = 70$. This
project’s two maintained routes on the three certificates: 1.6 CPU s.

**Upstream’s own figures** (REGULARIZE.md): the plain census “~7 s per record at n =
300”; the coincide census “33 CPU-min for the whole census”; `conservative` path tests
“268: minutes -> 9 s” after localisation; exactsolve “n = 300 a few minutes” and the
whole batch “~1-2 CPU-hours”; the samepacking KKT re-solve for the 27 records with angle
moves is another exactsolve each, with timeouts of 1800 s ($n \le 200$) and 3600 s.

**Estimate for $1 \le n \le 324$ here**, from those figures and the measured small
counts: exact solve 1 to 2 CPU-hours; two regularizer variants about 0.6 CPU-hours each,
with the `conservative` path tests adding minutes at a handful of counts; the KKT
re-solve of the angle-moved outputs about 0.3 CPU-hours; exact decision of 324 views on
both project routes about 0.5 CPU-hours (the independent checker tests every pair, about
52,000 at $n = 324$). About 3 to 4 CPU-hours, so 1 to 1.5 hours wall at four workers and
about 2 hours at the two-process cap this lane runs under.
The current `regularized atlas views re-derive exactly` step costs about 800 CPU-seconds
and runs alone under a 450 s ceiling (development.md, deferred jobs); the generator here
is ten to fifteen times that, so under OR-13 and OR-17 it cannot be a routine gate.
What can be gated is the decision of the retained views (section 4.4).

## 3. Soundness obligations for adopting it here

The record’s stance, stated in the batch README upstream too, is that a certificate’s
validity does not depend on how it was produced.
The obligations below are what must hold for a regularized drawing to appear in this
project’s atlas and case pages, independent of the generator.

### 3.1 Exact feasibility at the stated side, verified over Q here

Every view must be decided by this project’s checkers, not by the source’s. The fit is
already built: `devtools/evand_exact_certificates.py` reads Evan Daniel’s text format,
converts $(x, y, t)$ to a rational center-basis Witness/v2 and decides it with
`sqpack.witness.exact_verify` (separating axes over $\mathbb{Q}$,
`src/sqpack/witness.py:626-658`) and, as rational corners computed in the module, with
`devtools/check_rational_witness_independent.py`, which shares no geometry code; its
`check --certs DIR --n ...` subcommand did exactly that on the three certificates made
here (all VALID, 1.6 CPU s). `devtools/check_half_angle_area.py` is the third route
(polygon clipping, area-zero intersection, its own parser) and is the one that carries
`arrangement_gap`; it reads the same format.
The upstream checkers may be replayed as `source-replay` does, as evidence about the
source, never as the decision.
The view witness the layer retains must be the converted rational witness (center-basis,
or corners as the present layer writes), whose verdict is bound to its bytes by the
index’s digest, as the current layer does.

### 3.2 The side relation: `same` or `solved`

This is the obligation the upstream process does not meet by itself, and the one that
decides most of the design.

The certificate is never at $S^{\ast}$. By construction (`reg.py:1031-1034`) its side is
$S' = S^{\ast}(1 + 10^{-20})$ rounded up at 30 places, and every centre is scaled by
$1 + 10^{-20}$, so the certified object is a dilated copy of the view with every contact
opened by about $10^{-20}$ times its distance from the origin corner.
Three cases follow for this register:

- **$S'$ below the register’s verified upper bound.** That is a new verified upper
  bound: it enters the register as a result (as T-146 did at fifteen counts,
  `side: solved`), with the finder’s credit through `of` and the project as regularizer,
  and only then may its drawing stand in the atlas.
  For 73 of the 89 records the layer refused on 2026-10-02 the register’s verified bound
  was the grid ceiling (atlas README, “The regularized views”; the Kingbird catalogue is
  reported evidence never replayed), so a certified view there is a rational packing
  0.05 to 0.46 below the verified bound: a result by any reading, and a replay of the
  catalogue’s reported value that the record has never had.
  This is the largest single consequence of running the process over every count: on the
  order of a hundred register results, not a hundred drawings.

  *Amended 2026-10-11, the grid-ceiling premise.* This bullet is stale and stays as
  written. It quotes the atlas README’s 2026-10-02 count, but T-101 (registered
  2026-10-06) replaced the grid ceiling with Evan Daniel’s exact certificates as the
  verified upper bound at 74 Kingbird counts.
  On the record of 11 October none of the 74 records the layer refuses has the grid
  ceiling as its verified bound: 59 cite
  `E-evand-exact-ceilings-2026-10-05-exact-replay` and 15 other evidence (the Göbel
  family’s exact forms, the $\mathbb{Q}(\sqrt{2})$ and $\mathbb{Q}(\sqrt{7})$ lifts, and
  per-count certificates at $n = 11$, 17, 29 and 51), each read from its case record’s
  verified upper bound.
  A solved view there lands within about $10^{-14}$ of the verified bound, so what the
  regularization can add there is at most a T-146-sized refinement, not a hundred new
  bounds.

- **$S'$ above the verified bound by a relative $10^{-20}$.** Where the register already
  verifies the exact optimum (every exact-form record, e.g. $n = 10$ at
  $3 + \sqrt{2}/2 = 3.70710678118654752440084\ldots$, against
  $S' = 3.7071067811865475244379\ldots$), the certificate certifies a side strictly
  above it. The atlas README’s 2026-10-02 ruling on dilated views refused precisely this
  ("the rest would change the side … not the author’s packing at the certified side").
  Under the policy as written, such a certificate is not a drawing frame.

- **Literally the same side.** Possible only by an exact solve at the witness’s side:
  over $\mathbb{Q}$ where every rotation of the view is a rational rotation in the
  witness’s frame (every axis-aligned square, and tilted squares that keep the basis
  $(c, s)$ of the witness exactly), or over the number field where the register holds
  the exact form. Over $\mathbb{Q}$ the tight-contact system at fixed rational angles is
  linear with rational coefficients, so the float LP proposes which contacts are tight
  and a `Fraction` solve certifies the pose at the witness’s own side: this is what
  `regularize_axis_components/2` already does for axis-aligned squares and what the
  adaptation should do for every rational-rotation view.
  Such a view has its contacts closed, which this project’s routes decide (a zero sign
  is accepted) and upstream’s strict checkers would refuse (1.9), so the same-side view
  is a project-verified object by necessity, never a replay of the source’s verdict.
  The 217 rational witnesses, and every view whose angle merges land on an angle the
  witness already holds exactly, are in reach.
  Exact 45 degrees is not: a square at 45 degrees has no rational pose.
  Of the project’s 74 refused records, 43 hold every tilted square at exactly 45 degrees
  (5, 10, 19, 27, 38, 51, …), and those can be regularized at their exact side only over
  $\mathbb{Q}(\sqrt{2})$; the witness at $n = 51$ is already written over that field,
  and it is the one record the layer refuses for its scalar kind.
  The other 31 hold some other tilt, and no one field serves them: the five tilted
  squares at $n = 11$ are at 40.182 degrees, and its exact side is a root of an
  irreducible degree-8 polynomial (T-060; the case record `packing/frontier/n-011.md`);
  the tilted squares at $n = 17$ are at 36.624 and 39.805 degrees, and at $n = 18$ at
  24.295 degrees. None of the 74 is axis-aligned only.
  The split is `compare_evand_regularization refused-tilts` on the committed witnesses.
  The project’s witness model already admits `algebraic-number-field` scalars and
  `exact_verify` decides them with `field.sign`; the regularizer does not produce them.

The `regularizations` field (`packing/frontier/results.schema.yaml:319-376`, on `main`
since #487) records `side: same | solved`. `same` must mean literally the witness’s
side; a $10^{-20}$ dilation is `solved` with a side above the optimum and should not be
written as `same`. The present atlas index records `view_minus_reported` and
`fits_reported_side` per view; the adapted layer keeps both and adds the certificate’s
exact side.

### 3.3 The same-packing identity, and how it is recorded

The claim that a view is the credited packing rests, in the source, on the path test
(1.6 above) and on the orientation refit; the T-146 review measured each view against
its credited certificate instead, by nearest centres under the eight symmetries
(`arrangement_gap`, `check_half_angle_area.py:1386-1398`, one-to-one or not) and by
optimal assignment, and found at 123, 129 and 292 that no symmetry pairs nearest centres
one to one. The record’s rule, now in the schema, is that it “states a regularization as
the same packing in its own voice only where the basis is `measured`” with at least one
measurement.

For this project’s own run the basis is `measured`, so every view carries
`identity: {basis: measured, measured_in: <tool>, one_to_one, moved (> 1e-3), max_move, max_turn_deg}`
computed here, by `arrangement_gap` or a port of it on the view and its source witness.
The level the source assigns is recorded as what it is: `method` names the variant,
`changes` holds `merged_rotation_groups_deg`, `straightened` and `re_angled` from the
run’s `angle_changes`, and a level-2 verdict is the source’s classification unless the
path test runs here as well, which would make it the project’s measurement and still not
a proof. A view that is not one to one, or whose largest turn exceeds what the angle
policy explains, is not drawn as the packing.

Where the field lives: on a register result for `side: solved` views (the result is the
certificate); for same-side drawing views, in the atlas layer’s index under the same
terms (think-k35c: `of` as the source witness or result, `by: project`, `method`,
`side`, `changes`, `identity`), with a softschema contract.
The witness `certificate` block is still `additionalProperties: true`
(`witnesses/witness.schema.yaml:216-218`); the adapted layer’s `regularization` block
should be typed by the same contract.

### 3.4 Non-regression against the current drawings

The present layer measures every view before and after by the two shading rules
(`census_atlas_contact_shades.witness_shades`: house, gap $2 \cdot 10^{-6}$, and stage,
gap 0.01, half a degree) and holds a square whose counts fall
(`regularize_axis_components.py` docstring, step 4; index totals: 149 held squares, zero
residual regressions).
The upstream objective is different, a maximum of coincident faces plus pulls, and its
“unmoved” squares can carry the LP’s $10^{-12}$ noise before refine; a view may lower a
house count while raising the coincidence count.
The obligation is the one the layer already states: no square’s house or stage count
falls against the source witness, measured by the same census code, and a view that
regresses is refused or held, never shown.
Where both tools produce a view for the same record, the index records both counts and
the choice.

### 3.5 Labelling

Unchanged from the layer’s policy: every drawing made from a view says it is regularized
(index `label: regularized`, the renderer’s title and description, the view’s id
suffix), carries the record’s evidence tier from the source witness and never the view’s
own verification, and the container side drawn is the view’s certified side.
A dilated view, if the owner admits one, must say its side and that it is not the
author’s pose.

### 3.6 What is not imported

The source’s local-minimality claims (RG-11), its “exact optimum” wording and its level
classification are the source’s; the record reports them attributed and decides nothing
from them. The 80-digit KKT points are not retained upstream (RG-1); if the adaptation
retains its own, they are bulk data (OR-18) and belong in a packet or a release asset,
not beside the views.

## 4. Comparison with `regularize_axis_components/2`

|  | `regularize_axis_components/2` (`devtools/regularize_axis_components.py`) | Evan Daniel’s `reg.py` (`coincide`, `conservative`) |
| --- | --- | --- |
| Input frame | the witness’s own exact rational pose at dilation 1 (36-digit promotion of a decimal witness), refused if not exactly a packing within $10^{-9}$ of the printed side | the 80-digit KKT point of the packing re-solved by exactsolve from a float64 reduction of the witness |
| Side | the witness’s side, unchanged (`view_minus_reported: 0`) | $S^{\ast}$ of the KKT point at 80 digits; certificate at $S^{\ast}(1 + 10^{-20})$ rounded up |
| What moves | axis-aligned squares only, one axis at a time, to the nearest lattice slot, stopping at the first exact contact; tilted squares keep their exact pose | every centre, by an iterated translation LP with symmetry, straight-chain and coincidence equalities; free squares’ angles; undetermined groups’ angles; under `fewest`, determined groups within 5 degrees |
| Angles | squares within $10^{-4}$ radians of the axis straightened exactly | groups at $10^{-50}$; free squares re-assigned; near-axis undetermined groups straightened; merges accepted by LP feasibility at $S^{\ast}$ (and the path test under `conservative`) |
| Symmetry | none imposed | the largest feasible container symmetry of the whole packing, dropped only for a coincidence |
| Objective | contact counts under the house and stage rules; a slide must not lower either | coincident faces (MILP), cluster pulls, gravity to the bottom left |
| Orientation | the source’s; isometries recorded separately | refitted by a rule, source at 276, changed at 48 |
| Verification | twice over $\mathbb{Q}$, `sqpack.verify` and the independent checker, at the witness’s side | 80-digit min-gap check at $S^{\ast}$; rational certificate at $S'$ by two stdlib checkers |
| Non-regression | measured per square, held and re-run; zero residual regressions | not measured; uniqueness probe and `stalled` status reported |
| Refuses | 74: 73 decimal witnesses whose 36-digit pose overlaps at dilation 1, 1 algebraic-number-field witness | LP-infeasible starts ("bound only" records; 211, 263, 272 in v0, all placed under `coincide`), stalls, inconsistent near-equal angles |
| Changes, of 324 | 68 (182 unchanged) | 147 (30 rattlers only, 117 level 2) plus 48 re-orientations; rotation groups from 2400 to 1172 at 116 records; symmetry imposed at 101 |
| Identity | by construction the same squares at the same angles, slid along axes into contact | the sampled path test; the T-146 review’s measurement found three of fifteen views not one to one |

The cross-tabulation (`compare_evand_regularization crosstab`, appendix): every one of
the project’s 68 changed records upstream also changes; upstream also changes 72 of the
project’s 74 refused and 7 of its unchanged (40, 65, 82, 101, 122, 145, 308). At
$n = 26$ both slide the same rattler by 0.31 onto the grid; upstream also turns two free
squares back by $10^{-4}$ radians, square 8 to 0 degrees and square 23 to 45 degrees,
which undoes its own exact solve’s perturbation of them (appendix): the project’s
witness already holds both at those angles.
At $n = 70$ (Ryan Xu’s rational witness) the project’s view is 153 snaps of
$6.5 \cdot 10^{-12}$, noise removal of a rational pose; upstream, on its older
DeVincentis input here, slid 13 squares by up to 0.11 with no angle change.

**Replace, extend or run after.** Neither replaces the other.
The project’s tool is sound at the same side by construction and is the only one of the
two that measures non-regression; Daniel’s reaches the tilted structure, the symmetries
and the coincidences the project’s tool leaves alone, and reaches the records the
project’s tool refuses, but only by leaving the witness’s side.
The recommendation is **extend**: the layer gains a second generator, with per-view
`method`, and a view is admitted on the obligations of section 3 whichever generator
made it. Where both yield a view, prefer Daniel’s `conservative` view when it is
literally at the same side (after the exact re-solve over $\mathbb{Q}$ of 3.2) and does
not regress; otherwise keep the project’s. Running Daniel’s process *after* the
project’s (on the project’s view as the input to exactsolve) is not useful: exactsolve
re-detects contacts and re-solves $S^{\ast}$, and the project’s slides are a subset of
the LP’s moves anyway.

**How the gates extend.**

- `regularized atlas views match their index` (records tier,
  `packing/src/sqpack/cli/validate.py:5299`): the digest comparison stays as it is; the
  index gains the per-view generator, method, side relation, identity measurement and
  the contract check (think-k35c). Cost unchanged.
- `regularized atlas views re-derive exactly` (deferred,
  `packing/src/sqpack/cli/validate.py:5318`): keeps re-deriving the project-generated
  views byte for byte.
  The Daniel-generated views cannot be re-derived within any ceiling (3 to 4 CPU-hours,
  a third-party generator at a pin, a MILP with a time limit whose vertex choice is not
  guaranteed stable). For them the deferred step becomes a re-*decision*: every retained
  view decided again over $\mathbb{Q}$ on both routes, its identity re-measured, its
  digests held. That is about 0.5 CPU-hours at one worker, so about 450 s at four: the
  step’s whole ceiling, not inside it.
  `development.md` derived that ceiling from the present step’s four-worker wall (223 s
  for about 800 CPU-seconds), so the re-decision would roughly double the step; it is
  measured, and the ceiling re-derived, before it is armed (OR-17). The generation
  itself is an on-request replay with a receipt (pin, inputs, run cost, outputs by
  digest), on the pattern of the intake replays and `batch/reproduce.sh`.
- `regularized atlas drawings match their index`
  (`packing/src/sqpack/cli/validate.py:5332`): unchanged in kind; it renders each view
  from its retained witness, and a center-basis view renders through the same
  `frame_from_witness` path.
  Cost grows with the number of views (about 0.1 s each at the largest).
- `exact verification` and `check_results`: a `side: solved` view is a register result
  and goes through the import pipeline’s stages and `check_results`’ `regularizations`
  rules (`of` exists, is not the entry, covers $n$, dated no later; `by` among the
  sources or `project`; a `measured` identity carries a measurement).

Two drifts the assessment found are fixed in the same pull request: the atlas README
said “exact derived views of 55 records” and “87 refused”, the 2026-10-02 counts, where
the index now holds 68 regularized and 74 refused (73 Kingbird-derived, and $n = 51$).

## 5. Recommended adaptation plan for think-ux1v

Keep the upstream code as a pinned, read-only generator under `attic/` and put every
decision in project code.
The scratch replica used for the measurements shows the shape: a project driver builds a
replica tree with only the modules the pipeline needs, writes the inputs, runs
exactsolve and `atlas.py compute` with `python -I` from outside the checkout, and reads
the outputs back. Vendoring `reg.py` and `exactsolve.py` into the Python floor (ruff and
BasedPyright at zero findings) would cost a rewrite of 2,300 lines of prototype code and
buy no soundness, because the checkers decide, not the generator.

**Amended 2026-10-11, vendoring.** The paragraph above was this assessment’s
recommendation and stays as written.
The owner has since directed: “We should import and pin the inputs about the
regularization code since we may fork or adjust it based on Evan Daniel’s code, but we
should properly credit it.”
The plan changes in five ways:

- **Vendored at the pin.** The regularization code (`search/regularize/` and the
  `search/exact/` modules it runs) and the committed inputs it reads are vendored at
  `675a5ea` under `vendor/evand-regularize/`, with upstream’s MIT notice kept beside
  them, a provenance file naming the repository, commit, date and copied paths, and
  credit to Evan Daniel as the author of the code and the method.
- **Third-party bytes.** The vendored tree is excluded from this project’s lint and type
  floor and is not reformatted or tidied.
  The argument above was against rewriting the code into the floor; vendoring it as
  third-party bytes costs no rewrite.
- **Forks as recorded patches.** A change to the generator is a reviewed patch on top of
  the pinned copy, recorded with its reason, so the pinned bytes stay comparable with
  upstream and a later pin can be diffed against them; slice 2’s `--orient 0` shim is
  the first candidate.
- **Soundness unchanged.** The checkers decide, not the generator.
  Vendoring changes where the code lives and how a change to it is reviewed, not what
  admits a view.
- **Automated, then reviewed by hand.** The run is automated, and its output is then
  reviewed and adjusted by hand under the
  [regularization policy](../policies/regularization-policy.md); an adjusted view is
  decided by the same checkers and meets the obligations of section 3 like a generated
  one.

Slices, each a lane with its own deliverable and validation (OR-6), each landing in its
own pull request after this one:

**Slice 1: inputs and the exact-solve stage.** `devtools/regularize_evand.py` (name
open): `witness-input` converts each `witnesses/known-best/n-NNN.yaml` to the text
format upstream reads (a header of $n$ and $S$, then centres and degrees) at full
precision (rational witnesses printed exactly as decimals of 40+ digits, not the float64
reduction `batch/register.py` used, so a rational pose is re-solved from its own
digits); `exact-solve` runs upstream `exactsolve.py` at the pin (the vendored copy,
under the amendment above) per count with a timeout, retains `.exact.txt`, `.json`,
`.contacts.json` and `.cert` in a scratch run directory, and writes a receipt: pin,
interpreter, per-count status, `S_exact`, `cert_valid`, `newton_converged`, free
squares, seconds. Validation: the receipt’s `S_exact` against the register’s verified
bound at every count (expect 50 or so below the printed value by $10^{-13}$ to
$10^{-11}$, as upstream found, and the 73 Kingbird-only records far below the grid
ceiling); the `.cert` decided on both project routes; counts that do not certify listed,
not polished. Deliverable: the receipt and the run cost, recorded in the bead.

**Slice 2: the regularizer stage and the import.** `regularize` runs
`atlas.py compute --policy conservative --style coincide` (and `fewest` only if the
owner wants alternates) per count, in the source orientation unless the owner decides
otherwise (`--orient 0` through `reg.regularize`’s `orient` argument; `atlas.py` does
not expose it, so the driver calls `reg.regularize` through a small shim or patches the
argument in the replica, never in the checkout; under the amendment above, a recorded
patch on the vendored copy); `import` converts each certificate through
`evand_exact_certificates`’ parse into a rational center-basis Witness/v2 view, decides
it on both maintained routes and the third, measures identity with `arrangement_gap`
against the source witness, measures house and stage counts before and after with
`witness_shades`, and reads `angle_changes`, `level`, groups and symmetry from the run’s
JSON into the index entry.
Validation: every imported view VALID on all three routes; non-regression counts; the
identity table (one to one, moved, max move, max turn) for every changed view, with the
counts that fail one-to-one listed for the owner.

**Slice 3: the same side over $\mathbb{Q}$.** For every view whose rotations are all
rational in the witness’s frame, `exact-resolve` takes the view’s tight contacts (from
`.contacts.json` or recomputed at $10^{-9}$ as `refine` does), solves the linear system
over `Fraction` at the witness’s side with the LP point as the choice of vertex, and
verifies the result exactly; where it succeeds the view is retained at `side: same`, the
witness’s side, in the witness’s own frame, replacing the dilated certificate; where it
fails (inconsistent tight set, or a rotation the witness does not hold, e.g. a group
merged to exact 45) the view stays a dilated certificate and falls under the owner’s
side policy.
Validation: `view_minus_reported` is exactly zero for every `same` view; the
count of `same` versus `solved` views reported, against the counts that can reach `same`
at all.
Those are the records with an exact rational frame at the witness’s side: the 217
rational witnesses, and views whose merges land on angles the witness holds exactly.
The 73 decimal witnesses the present layer refuses have no exact witness side to
re-solve at, and the frame at $n = 51$ is over $\mathbb{Q}(\sqrt{2})$, so the slice
reports their views as `solved` or not drawn rather than as failures of the re-solve.
This slice is where the project’s existing tool and Daniel’s meet, and it is the one
that makes “clean and regular” and “no side changed” hold together.

**Slice 4: the record.** For `side: solved` views below the verified bound, a results
import through the intake runbook’s stages (a new entry with `regularizations` items,
`of` the credited result, `by: project`, `method` naming the upstream algorithm and pin,
`identity: measured`); for same-side drawing views, the index entries under the
think-k35c contract; RESULTS.md and the result pages print the items (records lane).
What this slice is depends on owner question 3. Validation: `check_results`,
`validate_schemas`, the records tier.

**Slice 5: drawings and gates.** `render_regularized_atlas --update` over the enlarged
index; `overview_sections.atlas_regularized` and the frontier page read the index
unchanged; the three gates extended as in 4.4, with the re-decision step’s cost measured
and its ceiling set; the atlas README and development.md updated (OR-7). Validation:
`packing-validate --records`, the `regularized-views` deferred job green, the drawings’
digests.

**Slice 0, before any of it:** the owner’s answers below, and the run-cost ledger opened
in think-ux1v so each slice records what it cost (OR-9).

## Open owner questions

**Answer question 3 first.** It decides slice 4: running the process over every count
yields certificates below the register’s verified bound at the 73 Kingbird-only records
whose verified bound is still the grid ceiling, and sides just below the printed value
at about 50 more. Under `epistemics.md` those are register results, not drawings, so the
answer decides whether slice 4 is an import of about 120 results through the intake
runbook or a change to the drawing layer only.

1. **Which variant.** `conservative` alone (310 of upstream’s 324 picks; every angle
   move path-tested from the current arrangement), or upstream’s best-choice rule
   (fewest groups, `fewest` at 14 counts: 70, 88, 129, 153, 172, 199, 236, 237, 263,
   269, 271, 292, 297, 301, with determined groups merged by 0.03 to 2.96 degrees)?
   Recommendation: `conservative` for the drawing layer.
2. **May a `fewest` merge of determined groups be drawn as the same packing?** The
   source’s round-5 log first called it “a different packing at the same side”; its
   level-2 verdict rests on the sampled path test, and at 129 and 292 the review found
   no one-to-one symmetry.
   Recommendation: no, in the project’s own voice; such a view is an alternate
   arrangement at the record side, drawable only labelled as such, if at all.
3. **Do solved-to-smaller-side views become register results?** Running the process over
   every count produces, for the records whose verified bound is still the grid ceiling
   (73 of the 89 refused on 2026-10-02), certificates below the register’s verified
   bound (new verified upper bounds that replay the catalogue), and for about 50 others
   sides $10^{-13}$ to $10^{-11}$ below the printed value (the analytic optimum, as
   T-146’s fifteen). The epic says a smaller exact side “enters the register, not just a
   drawing”. May the regularization’s pull requests add that many results, or do they go
   through a separate import, with the drawing layer taking only the same-side views
   until then? *Amended 2026-10-11:* the “73 records at the grid ceiling” behind this
   question has been stale since T-101 (see the amendment in section 3.2). What remains
   is the T-146 kind: sides $10^{-22}$ to $10^{-11}$ below the verified bound, which the
   decision table’s row 3 lists as candidates and draws nothing from.
4. **The side policy for irrational optima.** Where the exact optimum is irrational, a
   dilated certificate is above the verified bound by a relative $10^{-20}$ and the
   atlas README refuses it as a frame.
   No one field covers these records: of the 74 the layer refuses, 43 hold every tilt at
   45 degrees and need $\mathbb{Q}(\sqrt{2})$ (the witness at $n = 51$ is already over
   it); 31 hold other tilts, among them $n = 11$, whose exact side has degree 8 (T-060)
   and needs a field of its own, and $n = 17$ and 18. Options: keep those records
   un-regularized where the project’s tool refuses them (status quo); reverse the
   2026-10-02 ruling for a labelled dilated view; or, later, views over each record’s
   number field at the exact side.
   Recommendation: status quo for the regularization’s first pull requests, with the
   field route as the follow-up think-yk2h, starting with the 43 records over
   $\mathbb{Q}(\sqrt{2})$.
5. **Orientation.** Adopt upstream’s refit (48 records re-oriented) or keep the source
   orientation and record any isometry as `atlas_orientation` does?
   Recommendation: source orientation by default.
6. **Tie-breaks that are taste.** Symmetry imposed against contact (the rattlers at
   $n = 10$ in the corners under symmetry versus floating), the diamond at $n = 26$
   attached or separate, strips sliding as a unit: upstream decided these by Evan
   Daniel’s round-1 picks.
   The owner should pick from a gallery of the few records where it matters (`face` and
   `orient` flags, `sym_dropped_for_coincidence`), before the run is frozen.
   *Amended 2026-10-11:* the owner wants the automated run followed by manual review and
   adjustment under the [regularization policy](../policies/regularization-policy.md),
   so these tie-breaks can also be settled in that review, after the run.
7. **Credit for the method.** The `regularizations` field has one `by`; for this run it
   is `project`, with `method` naming Evan Daniel’s algorithm, variant and pin.
   Is a bibliography credit to the method’s author wanted as well, and where (the
   layer’s index, the atlas README, the bibliography entry already made for T-146)?
   *Amended 2026-10-11:* the owner directed that the vendored code be properly credited,
   so the MIT notice and the provenance file carry Evan Daniel’s credit with the copy
   under `vendor/evand-regularize/`; where else the credit is printed remains open.
8. **Retention of the solve.** Keep the 80-digit KKT points and contact structures the
   run produces (about 10 MB for 324 counts, bulk data under OR-18) as a packet or
   release asset, so that a later lane can re-measure without re-solving, or discard
   them and keep only the receipt?

## Appendix: Measurements

Host: the session’s 4-core container, shared with other lanes; one process at a time per
command. Upstream code at commit 060c1a1 (every file copied below is byte-identical at
675a5ea), copied into a scratch replica tree (`../evand-replica/`) with only
`search/exact/{exactsolve,geom,verify_cert,verify_cert2}.py`,
`search/exact/batch/results.json`, `search/regularize/{reg,atlas,samepacking}.py` and
the committed `batch/inputs/n-N.txt` for $n = 10$, 26 and 70 renamed to
`work/n-N/witness.txt`. Interpreter: a scratch virtualenv (`../evand-venv/.venv`, Python
3.14, numpy 2.5.4, scipy 1.18.1, mpmath 1.4.1), run with `python -I`, never from inside
the checkout. The checkout was not modified.

| Stage | n = 10 | n = 26 | n = 70 |
| --- | --- | --- | --- |
| `exactsolve.py` (80 digits), its own `seconds` | 0.3 s | 0.5 s | 3.0 s |
| same, wall including imports | 1.5 s | 1.1 s | 3.6 s |
| status / cert_valid / free squares | KKT local min / True / [3, 7] | KKT local min / True / [8, 19, 23] | KKT local min / True / [] |
| `atlas.py compute --policy conservative --style coincide --procs 1`, all three | 2.6 s wall |  |  |
| `atlas.py compute --policy fewest`, all three | 2.5 s wall |  |  |
| `verify_cert.py` + `verify_cert2.py`, per certificate | 0.05 s | 0.09 s | 0.22 s |
| project routes (`devtools.evand_exact_certificates check`), all three | 1.6 CPU s, 2.1 s wall |  |  |

Note the $n = 70$ input is the committed 2026-10-05 batch input (Joe DeVincentis’s
packing, $S = 8.88167$), not Ryan Xu’s 8.88096 that the lists refreshed from the store:
the refreshed inputs live under the gitignored `runs/` and are not in the checkout.

Regularized views (conservative, coincide).
Moves and turns are measured against the exact solve’s output, the point the regularizer
reads (its certificate is `batch/certs/n-N.cert`), mapped into the view’s orientation;
they are not measured against the project’s witness.
Squares are numbered from 0, as upstream’s `free` lists are:

| n | orientation g | groups | squares moved more than $10^{-3}$ | largest move | squares turned more than $10^{-6}$ degrees | largest turn | level |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 0 | 3 → 2 | 0 | $10^{-4}$ | 2 (axis rattlers 3 and 7, −0.0057° → 0°) | 0.0057° | 1 |
| 26 | 3 (quarter turn) | 4 → 2 | 1 (rattler slid 0.3106 onto the grid) | 0.3106 | 2 (free squares 8, −0.0057° → 0°, and 23, 45.0057° → 45°) | 0.0057° | 1 |
| 70 | 0 | 2 → 2 | 13 | 0.1121 | 0 | 0 | 2 |

The 0.0057-degree turns are the exact solve’s, undone.
`place_free` (`search/exact/exactsolve.py:637-703`) re-places each free square by an LP
whose bounds are $R = 10^{-4}$ on each centre coordinate and on the angle, in radians,
so a free square can leave the solve turned by up to $10^{-4}$ radians, 0.00573 degrees.
The committed `batch/certs/n-10.cert` holds the axis rattlers 3 and 7 at $-10^{-4}$
radians and the 45-degree squares 8 and 9 at 45 degrees; `batch/certs/n-26.cert` holds
square 8 at $-10^{-4}$ radians and square 23 at 45 degrees plus $10^{-4}$ radians, while
every other 45-degree square is at 45. The batch inputs, the project’s witnesses and the
list certificates hold those squares at 0 and 45 degrees
(`compare_evand_regularization angles` on the four certificates;
`batch/inputs/n-26.txt`; `packing/witnesses/known-best/n-010.yaml` and `n-026.yaml`). No
45-degree square at $n = 10$ is ever turned.
The project’s own layer at $n = 26$ slides the same rattler by 0.3107
(`moves.compactions: 1`, `largest_move_decimal: 3.107e-01`) and turns nothing: its
witness holds square 8 at 0 and square 23 at exactly 45 degrees already, and the layer
leaves tilted squares’ poses alone by design.

Certificate sides: at $n = 10$,
$S' = 3707106781186547524437915429917/10^{30} = 3.7071067811865475244379\ldots$, against
`S_exact`, $3.70710678118654752440084\ldots = 3 + \sqrt{2}/2$ (the register’s verified
bound): $S'$ exceeds the exact side by $3.7 \cdot 10^{-20}$.

Cross-tab, from upstream `lists/best.json` at `060c1a1` and the project’s `index.json`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.compare_evand_regularization \
    crosstab --best <upstream checkout>/search/regularize/lists/best.json
```

Upstream levels 0/1/2 = 177/30/117 (147 changed); variants conservative 310, fewest 14;
orientation kept at 276, changed at 48; inputs: exact batch 272, store-refreshed 52;
rotation groups from 2400 to 1172, fewer at 116 records; symmetry imposed at 101.
Project status by upstream level: refused/0: 2, refused/1: 29, refused/2: 43;
regularized/1: 1, regularized/2: 67; unchanged/0: 175, unchanged/2: 7. Every record the
project changes (68) upstream also changes; upstream changes 79 more: 72 of the
project’s 74 refused (not 11 and 28) and 7 of its unchanged (40, 65, 82, 101, 122, 145,
308).

Refused records by witness tilt, from the committed witnesses alone:

```bash
uv run --frozen --all-extras --group dev python -m devtools.compare_evand_regularization refused-tilts
```

Of 74: 43 with every tilted square at exactly 45 degrees, 31 with another tilt, none
axis-aligned only. The angles quoted at $n = 10$ and 26 come from
`compare_evand_regularization angles` on `search/exact/batch/certs/n-10.cert`,
`n-26.cert` and `search/regularize/lists/certs/n-010.cert.gz`, `n-026.cert.gz`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
