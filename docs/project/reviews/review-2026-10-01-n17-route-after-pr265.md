---
title: n17 Optimality Route After PR 265
date: 2026-10-01
status: planning-review
---
# n17 Optimality Route After PR 265

**Session:**
[166](../../../packing/campaign/agent-sessions/session-166-n17-route-after-pr265.md).
**Baseline:** `fe639945` (main after PR 265 and PR 269). **Review:** two Fable
extra-high mathematical lanes (the proof route; the local endpoint theorem), one factual
survey lane, and coordinator reconciliation.
**Tracking:** planning `think-9fc1` (BC-405), selected coordinator `think-c7kv`
(BC-406).

[PR 265](https://github.com/jlevy/squares/pull/265) certified the known n17 packing’s
exact endpoint, proved a conditional minimum, and built a complete occupancy scaffold.
This W10 checkpoint asks what that leaves for an optimality proof, which route is most
likely to finish one, and what to do next.
It changes no bound, frontier field or experiment verdict.
The numerical findings below come from exploratory scripts retained beside the record;
they are evidence for planning, not admitted results.

## Where n17 Stands

The verified bounds are $4.66044 < s(17) \le 4.6755300936045509516\ldots$, a gap of
about $0.0151$, the narrowest of any open case.
The upper bound is Bidwell’s packing, now certified exactly (H253 to H256). An
optimality proof must show that no packing has a smaller side.
The n11 proof (T-060) did that in two halves, and n17 needs both:

1. **A local theorem.** Near the endpoint, nothing has a smaller side.
   Bidwell’s packing has sliding squares and a free rotating square, so the theorem has
   to quotient those motions out rather than claim isolation.
2. **A global argument.** Cover every possible packing by finitely many cases, exclude
   all but the cases near the endpoint, and capture those into the local theorem’s
   neighbourhood.

| PR 265 piece | Status | Role in a final proof |
| --- | --- | --- |
| Exact rational witness, chart root and physical endpoint (H253 to H256) | Certified | Load-bearing: the construction and the capture target’s centre |
| Contact feature inventory (H257) | Certified | Load-bearing: the first-order row set |
| Conditional minimum ([projection branches](review-2026-10-01-n17-projection-branches.md)) | Correct within its stated box | Not the terminal theorem; useful as a sanity bound |
| Mixed-capacity cover and D4 quotient (H259, H260) | Counts exact; no case excluded | Capacity lemmas reusable; this grid probably replaced |
| Common-core stress (H258) | Instrument stopped at preparation | Load-bearing, and exploratory checks find it valid |

By effort, the construction is done, the local theorem is about half done, and the
global half has a census but no exclusions.
The route lane estimates 5–10% of a complete proof.

## Findings

Neither mathematical lane found an error in PR 265. The route lane re-derived every
inequality of the projection theorem, both capacity lemmas of the mixed cover (the
wall-cell sign is exactly $288 < 289$; interior cells satisfy $5a^2/4 < 1$), the centred
embedding and the Burnside count, and reproduced all eight fixed counts and the
20,155,518 orbits exactly.
The endpoint lane re-derived the projection theorem’s chains, bridge identities and
monotonicity argument by hand.
At the root it finds $(F_2)_\theta=-0.2816$, $(F_2)_\beta=-0.0430$,
$(G_3)_\theta=-0.0616$ and $(G_3)_\beta=+0.5173$, matching the opening review.

### The H258 Stress Is Valid

Both lanes rebuilt the 58-row first-order model and the H258 loads from the
[core-stress review](review-2026-10-01-n17-core-stress.md), separately from each other
but not independently of that review.

- **Exact check (endpoint lane).** At the exp-237 midpoint, $A^\top\lambda = K e_\sigma$
  holds exactly in rational arithmetic in all 52 columns, with the two prescribed
  $\gamma\rho F_2/K$ residuals at $\omega_{12}$ and $\omega_{16}$. The same exact
  identity holds at three unrelated rational points
  $(t,b)=(1/3,1/5),(37/100,33/100),(2/7,3/11)$, which is evidence, not proof, that it is
  a rational-function identity.
- **Weights.** All 58 weights are nonnegative.
  Exactly six are zero: the 5-right and 6-bottom wall pairs and the 9/11 contact pair.
  The smallest positive normalised weight is $0.00608$ (11→12, $E_+$). The five oblique
  moment capacities $kf-|q|$ are $0.221$, $0.052$, $0.0099$, $0.033$ and $0.150$.
- **Double-precision check (route lane).** The normalised residual is
  $2.2\times10^{-16}$ in every column, with the same six zero weights.
- **Loads.** $\mu=0.15093$, $\nu=0.51733$, $\rho=0.042972$, $Z=0.52742$, $L=0.54046$,
  $R=0.49148$, $K=1.72648$.

H258 stalled because `sympy.cancel` on 52 fully substituted rational functions swells
exponentially, not because the mathematics failed.
The Java and `fnm` messages in the retained preparation output are environment noise,
and the 128,454-character weight bounds are an unreduced-fraction artefact.
The exact check runs in 0.24 seconds.

### The Endpoint Is a First-Order Minimum Modulo Its Sliders

The 52 positively weighted rows have rank 46. Their kernel has dimension 6 and is
spanned exactly by the known motions: $\xi_5$, $\xi_6$, $\eta_6$, $\omega_6$, square 11
along $v$ and square 13 along $v$. All 58 rows have rank 50, with a 2-dimensional
lineality space ($\xi_6$ and square 13 along $v$). With the six zero-weight rows as
inequalities, the zero-side face is exactly
$\lbrace\xi_5\le0\rbrace\times\lbrace\eta_6\ge|\omega_6|/2\rbrace\times\lbrace V_{11}=-bv,\ b\ge0\rbrace\times\lbrace V_{13}\in\mathbb{R}v\rbrace$,
the finite motions the first-order review catalogued.
No flex direction raises the side only at second order.

A floating-point simplex finds a nonnegative dual for each of the 90 signed non-slider
coordinate directions.
The largest coefficient is $175.8$, for $-\omega_{11}$ (the 11/12 angle split); next are
$-\omega_{16}$ at $74.2$, $-\omega_8$ at $69$, $-\xi_8$ at $68$ and $+\omega_{9,10,12}$
at $48$. So the side grows at least like $\lVert h\rVert_\infty/176$ outside the slider
cone. Ten minor coordinates returned simplex residuals up to $1.5$ from phase-one
degeneracy and must be redone exactly.

Consequently the local theorem needs no second-order analysis.
The Lagrangian Hessian vanishes on the critical cone, because square 6 appears in no
positive row and the other zero directions are pure translations.
The two lanes give two arguments for the same conclusion:

- The endpoint lane uses n11’s focused-rectangle method with the slider coordinates
  excluded from the saturation argument.
  The n11 curvature bounds (PROOF.md, lines 429–437) give a worst ratio
  $\tfrac12 M_j/r_j$ of $0.86$ at a uniform radius $3\times10^{-4}$, rising to $1.43$ at
  $5\times10^{-4}$, $2.9$ at $10^{-3}$ and $8.6$ at $3\times10^{-3}$. Enlarging
  positions alone does not help because positions and angles are coupled.
  n11’s worst ratio was $0.616$ at radii near $1/64$, so the n17 rectangle is about 50
  times smaller.
- The route lane gives a direct argument: write each positive row’s change as
  $o_i = A_i h$ plus a remainder bounded by $K\lvert h_{\rm ang}\rvert\lvert h\rvert$. A
  negative side change would force
  $\lVert o\rVert \le C_1\lvert h_{\rm ang}\rvert\lvert h\rvert$. Injectivity of $A$ off
  the kernel then forces $h_{\rm ang}=0$ for small $\lvert h\rvert$, because the kernel
  carries no angle except $\omega_6$. That argument is new and needs an independent
  read, especially the angle-chart reduction.

The 135 unavailable owner alternatives have strictly negative margins at the endpoint;
the local theorem must show by Taylor bounds that they stay negative in its box.
The least negative are $-0.0558$ (14/17 along 17’s $e_x$, and 7/14), $-0.0707$ (12/16)
and $-0.147$ (3/11).

### Scope of the Conditional Minimum

The projection theorem is correct as stated.
Its record states the scope too briefly in three places:

- **Side range.** It works in $S\in[4.675,4.676]$ (projection review, lines 54–56).
  Premise-satisfying packings with $S$ in $(4.66044, 4.675)$ are not covered.
  A grid shows the same derivative signs on $[4.66, 4.676]$, so an outward-bound rerun
  would close this.
- **Angle range.** $t\in[0.36,0.37]$ is $\theta\in[39.63^\circ,40.60^\circ]$, only
  $0.17^\circ$ below $\theta^{\ast}$. The monotonicity proof cannot simply be widened:
  on $t\in[0.33,0.40]$, $b\in[0.30,0.37]$, $(F_2)_\beta$ reaches $+0.024$ and
  $(G_3)_\theta$ reaches $+0.138$. A 400 × 400 scan of $S_{\min}(\theta,\beta)$ over all
  common orientations nevertheless has its minimum at the root and grows roughly
  linearly, so the conditional minimum appears global over common orientations.
- **Premises.** It assumes exact common orientation of squares 9, 10, 11, 12 and 14 and
  fixed separating directions.
  A capture step cannot deliver either, so this theorem cannot be the terminal theorem
  (the projection review says so at lines 374–391; the morning report’s summary row
  reads more broadly).

Two premises can be adjusted.
$W_{17}\ge se+\gamma$ holds for every orientation of square 17 and can be dropped.
$W_{15}\ge cd+\gamma$ holds for $\lvert\phi_{15}\rvert\le32^\circ$ but fails when square
15 is co-oriented with square 16 (near $-36.6^\circ$), which is a genuinely different
branch.

### The Cover Ignores Where the Endpoint Sits

At the endpoint, all 17 centres lie in distinct H259 cells (11 boundary, 6 interior),
and no capacity-two cell is used.
Square 9’s centre is at $y=2.7042$, $0.0012$ below the seam $y=1/2+3a=2.7056$ with
$a=919/1250$. The route lane concludes that a capture target around the family straddles
at least two occupancy states, times D4. The cover was chosen without reference to the
endpoint’s geometry; it should be re-chosen so the whole endpoint family, slides
included, sits inside one occupancy state with margin.

### Free Cuts and the Cost of Geometric Exclusion

Two settled cases give exact cuts on the H259 grid at cap $1169/250$:

- **$s(6)=3$:** any 2 × 2 block of cells holds at most five centres, because
  $2a+\sqrt2=2.885<3$.
- **$s(10)=3+1/\sqrt2$:** any 3 × 3 block holds at most nine, because
  $3a+\sqrt2=3.620<3.707$.

Together they leave 61.6 million of the 161,100,756 states, about 7.7 million orbits
(38.2%). A cap of four centres per boundary row is not established: two squares tilted
$28.5^\circ$ in a staircase have tangential spacing $0.835$, and a consecutive-pair
bound places five in a row within $3.545<3.676$.

The n11 replay cost about 640 CPU-seconds per nonfield geometric exclusion (32 cases,
20,359 CPU-seconds;
[census contract](review-2026-09-29-n11-optimality-census-contract.md), lines
2375–2381). n17 has 136 pairs and 52 variables against n11’s 55 and 33, so 1–2 CPU-hours
per geometric leaf is a fair guess.
That makes $10^3$ to $10^4$ geometric leaves affordable, and the global route is
affordable only if a cheaper counting engine excludes more than 99.9% of orbits at the
pattern level.

## Which Route Most Likely Finishes the Proof

| Rank | Route | Main risk |
| --- | --- | --- |
| 1 | **Hybrid:** occupancy cover, conditional charge floors as the bulk exclusion engine, n11-style geometric exclusion for the residue, capture, and the stress-based local theorem | The residue after counting stays above $10^5$; capture into a small neighbourhood of a 6-dimensional family |
| 2 | **Pure n11 architecture:** geometric exclusion only | Strictly dominated by rank 1 (n11 itself used 1,904 field and 276 nonfield exclusions) |
| 3 | **Radius enlargement plus capture** by interval branch-and-bound along the two weak directions | A refinement of rank 1 if capture cannot reach $3\times10^{-4}$ |
| 4 | **Counting to the endpoint** | Cannot prove equality; see below |

A counting certificate proves a strict bound at its target, so it cannot reach the
optimum without a limiting family or an endpoint measure with boundary mass (X-048 R7).
The capacity-one ceiling lemma also bounds this route: a clique-weighted family with
total weight at least 17 at side $S'$ defeats every capacity-one certificate at or above
$S'$ (H-248). The current recipe also appears spent: R068’s ledger is flat, its surplus
fell to 7,404 units, the argmin is the corner cell in every sampled row, and the
source’s next dictionary failed at $4.6605$
([R067/R068 review](review-2026-09-28-n17-guzhou-r067-r068.md), lines 435–451). Its
value is as the exclusion engine inside the hybrid.
The sliders are not the obstruction: charges are piecewise constant in pose, so a family
can be tight.

## The Terminal Theorem

Split the coordinates into the **slider coordinates** $W$ (all three of square 6,
$\xi_5\le0$, square 11 along $-v$, square 13 along $\pm v$) and the 45 **non-slider
coordinates**, with squares 11 and 13 written in the $(u,v)$ frame and angles reduced
modulo $\pi/2$ in the H254 labelling.

**Target statement (H-261).** There is an explicit rational radius $r>0$ such that every
packing of 17 unit squares in $[0,S]^2$ whose non-slider coordinates lie within $r$ of
the endpoint family, with slider coordinates anywhere in the physical slider domain,
satisfies $S\ge S^{\ast}$, with equality only on the family.

The neighbourhood is a product of a box in the non-slider coordinates and the slider
domain.
The six zero-weight rows, the 115 non-contact pairs and the 53 inactive walls can
be dropped, which only weakens the system, so square 6 leaves the argument.
The physical slider domain is the H256 triangle: about $0.11$ in $x_6$ and $0.07$ along
$v$ for square 13; square 5 slides left up to $0.037$ at the centroid ($0.11$ at a
vertex); square 11 slides along $-v$ up to $0.024$ to $0.07$; square 6 rotates by about
$0.1$ to $0.18$ radians.
The stress must be re-verified along the family, because $\tau_{13,14}$ and the 2/13 and
13/14 moment arms vary with the sliders; $A(w)$ is affine in the slider parameters, so
this is a small interval job.

## Selected Work

All of these sit in
[agenda-042](../../../packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md)
under program `post-optimality-low-n`. BC-406 is the selected coordinating entry; it
dispatches lanes A, B and C in parallel.

| Lane | BC | H | Bead | Work | Allocation |
| --- | --- | --- | --- | --- | --- |
| A1 | BC-402 | H-258 | `think-wrgx` | Repair the stress instrument within its frozen criterion: check the 52 identities after clearing the known denominators, in $\mathbb{Q}[t,b]$ with `sympy.polys` ring arithmetic or by exact evaluation on a grid beyond the degree bound; keep the 256-bit outward interval sign audit | Opus 5.5 builds; Fable extra-high reviews the instrument; Fable max reviews the output |
| A2 | BC-407 | H-261 | `think-n95s` | Local minimum modulo the slider cone: exact kernel basis, 90 exact coordinate duals, per-row curvature bounds, the 135 unavailability checks, uniformity over the slider domain, ratio test at an explicit radius | Fable max derives and reviews; Opus 5.5 builds |
| B | BC-408 | H-262 | `think-j1uw` | Free cuts plus conditional charge floors on the H259 grid at cap $1169/250$; count surviving D4 orbits with the endpoint pattern as positive control | Fable extra-high designs; Opus 5.5 builds; Fable max reviews the charge |
| C | BC-409 | H-265 | `think-e6y1` | Resultant of the H255 chart polynomials, factorization over $\mathbb{Q}$, and identification with the catalogue’s degree-18 polynomial | Opus 5.5; Fable extra-high review |
| — | BC-410 | H-263 | `think-x4a6` | Endpoint-adapted cover, compared by survivors under the BC-408 instrument | After BC-408 |
| — | BC-411 | H-264 | `think-11ma` | Per-leaf cost of geometric exclusion on a uniform residue sample at a cap $U\ge S^{\ast}$ | After BC-408 and BC-410 |

**Stop or reconsider conditions.** If H258’s exact identity fails at a rational point,
treat it as a convention mismatch to diagnose before any other lane uses the stress.
If lane B leaves more than $10^5$ orbits, stop BC-410 and BC-411 and return to W3: the
hybrid route needs a stronger counting engine.
If H-261’s certified radius falls below $10^{-4}$, open the interval enlargement along
$\omega_{11}-\omega_{12}$ and $\omega_{16}$ before any capture work.

**Re-scoping `think-11ma`.** Session 165 handed off a pilot “below the certified
endpoint”, with $4.67$ as a candidate cap.
Exclusions at a cap below $S^{\ast}$ cover only smaller sides and would leave
$(4.67, S^{\ast})$ open.
The n11 proof excludes every case except the captured one at a cap $U$ above the
endpoint (PROOF.md, section 3, lines 128–150); the centred embedding applies those
exclusions to every $S\le U$. Only the captured case uses the actual side and the local
theorem (PROOF.md, lines 528–545). BC-411 therefore works at $U\ge S^{\ast}$, samples
orbits uniformly from the BC-408 residue rather than hand-picking leaves, and measures
cost per leaf.

## Deferred and Not Selected

| Work | Why not now | What would select it |
| --- | --- | --- |
| Capture prototype for the endpoint’s occupancy states, from the n11 case-438 pipeline | Needs the H-261 radius and the BC-410 cover | Both accepted |
| Strengthen the conditional theorem: side range to $[4.66,4.676]$, an interval proof over all common orientations, drop the $W_{17}$ premise, widen $W_{15}$ to $\pm32^\circ$, record the 15-parallel-16 branch | Not on the critical path once H-261 exists | A capture step that needs a wider target in angle directions |
| H-248 fractional family at $4.675$, then $4.67$ (BC-387) | Decides whether pure counting is dead, which the hybrid does not need | Spare capacity; it can run beside lane B |
| R7 endpoint measure, R5 backbone, R8 feature changes (X-048) | Unshaped against the hybrid route | A measured gap the hybrid cannot close |

## What Else to Cover

- **Correct the record.** The morning report and the projection review now carry dated
  scope notes that point here.
- **Trust base of a final proof.** The settled cases $s(6)=3$ and $s(10)=3+1/\sqrt2$, if
  used as cuts; R068 (one method, C3) if its charges become the exclusion engine; the
  n11 checker `audit_capture_v9.py` if reused (reviewed, never formalised).
  The H255 root and H256 feasibility share one contraction method, so a check by a
  different method is cheap and worth adding.
- **Formalisation.** The support inequality, the wall-cell capacity, the subcontainer
  cut and “stress implies local minimum” are each a few pages.
  They are the natural first Lean targets, as the n11 exposition itself suggests
  (PROOF.md, lines 807–830).
- **Lemmas to state explicitly.** The two-row parallel-face reduction under Taylor
  remainders, the zero corner weight, and the angle-chart convention modulo $\pi/2$.
- **A reusable instrument (OR-1).** A stress-to-local-minimum certificate applies to any
  reported endpoint with translational sliders: n18, n19, n26 and n29.
- **Other low cases.** n12 (gap $0.031$) remains the parallel secondary; n20 could
  borrow the n21 mechanism.
  Replays are still owed for the Evand $k^2-3$ family, the MacIver lower-bound claim and
  the external Guzhou/anabologyco checker.
- **Resource planning.** n11’s discovery costs are not public, so replay-based estimates
  understate. Every pilot should measure producer time separately.

## Handoff

The next agent starts at BC-406 (`think-c7kv`) and should read, in order:

1. this review;
2. the [morning report](review-2026-10-01-post-optimality-morning.md);
3. the [core-stress review](review-2026-10-01-n17-core-stress.md) and
   [H-258](../../../packing/campaign/hypotheses/H-258-n17-common-core-stress.md);
4. the [first-order review](review-2026-10-01-n17-first-order-branches.md);
5. [PROOF.md](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
   section 3 and lines 394–551 (local theorem and capture);
6. the
   [exploratory receipts](../../../packing/campaign/explorations/X048-route-review/README.md),
   starting with `endpoint-n17_stress.txt`.

Then dispatch lanes A1, B and C in parallel with disjoint deliverables.
Lane A1 owns `devtools/check_n17_core_stress.py` and its tests; lane B owns a new census
tool and its tests; lane C owns a new identification tool.
None of them edits the frontier.

## Evidence Status

| Kind | Items |
| --- | --- |
| Verified by exact computation in the exploratory scripts | Endpoint reconstruction and H257 inventory; stress identity at four rational points; all 58 weight signs; the 6-dimensional kernel and zero-side face; Burnside counts; free-cut survivor counts |
| Double precision only | Route-lane reconstruction; derivative ranges; the global $S_{\min}$ scan; coordinate duals; radius ratios |
| Derived by hand, needing independent review | The first-order-suffices argument; the product form of the neighbourhood; the hybrid cost model |
| Taken on trust | H255 to H257 certificates and outward interval bounds; n11 curvature-bound formula; the R068 replay; the external small-case theorems |

The coordinator re-ran `endpoint/n17_stress.py` and confirmed its exact identity, weight
signs and kernel dimension before writing this review.

## Exploratory Receipts

[`packing/campaign/explorations/X048-route-review/`](../../../packing/campaign/explorations/X048-route-review/README.md)
holds the outputs of both lanes’ fourteen scripts, re-run under the project interpreter,
and says what each script computed.
The sources stay outside the record, as earlier planning probes did, because the lint
floor admits no unlinted Python in `packing/` and its exclusion list is byte-pinned by
the n11 native audit.
The outputs are planning evidence: each number still needs an admitted instrument before
it enters a hypothesis verdict.

## Correction After the Capture Review

*Added 2026-10-02 by Session 167.* The comparison with n11 in
[The Endpoint Is a First-Order Minimum Modulo Its Sliders](#the-endpoint-is-a-first-order-minimum-modulo-its-sliders)
misreads n11’s radius.
PROOF.md line 425 says only that n11’s focused coordinate radii lie *within* the
analytic working box of radius $1/64$. The accepted radii in n11’s pose-inclusion
receipt (`receipts/pose-inclusion/result.json` under the archived n11 source) are about
$9\times10^{-4}$ to $2.3\times10^{-3}$, and the
[capture feasibility review](review-2026-10-02-n17-capture-feasibility.md) reads
$6.5\times10^{-4}$ to $3.3\times10^{-3}$ in position and $1.5\times10^{-3}$ to
$6.8\times10^{-3}$ in angle across all of them.
The exploratory n17 radius of $3\times10^{-4}$ is therefore about 1.5 to 16 times finer
than n11’s, not about 50 times.
The capture review concludes that capture cost is only logarithmic in the radius, so
enlarging the local radius is no longer a precondition for capture work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
