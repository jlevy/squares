# X-048 Session 167 Pilots: Receipts

Session 167 dispatched the lanes of BC-406, the coordinating entry the
[n17 route review](../../../../docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md)
selected. Two of its lanes built retained tools whose outputs are kept here: the
mechanical half of the H-261 local-minimum checker, and a go/no-go pilot for H-262’s
charge-floor census engine.

These are **planning evidence, not admitted results**. Neither run is an experiment
record, and no hypothesis verdict rests on them until an independent review admits it.
Unlike the route review’s exploratory receipts, both tools are in the repository, lint
clean and tested, so every number here can be reproduced from `packing/`.

## H-261: The Mechanical Half of the Local-Minimum Checker

`devtools/check_n17_local_minimum.py` (SHA-256 `49455478…`, bound in the receipt), built
by lane A2-build, Opus at extra-high effort.
It works in exact rational arithmetic at the point H-258 uses: the exp-237 root-box
midpoint with the H256 centroid sliders.
It reuses `check_n17_core_stress.complete_stress` at commit `2fbf8d29` read-only.

| Receipt | What it holds |
| --- | --- |
| `receipts/local-minimum-target.json` | Every check passes. Six exact zero weights. The kernel of the 52 positive rows has rank 46 and equals the span of the six slider generators; all 58 rows have rank 50 with lineality $\xi_6$ and square 13 along $v$. Exact, provably optimal nonnegative duals for all 90 signed non-slider directions; the largest is $175.848\ldots$ for $-\omega_{11}$. All 135 unavailable owner alternatives are strictly negative, the least $-0.0557998\ldots$ (7/14 and 14/17). |
| `receipts/local-minimum-control-kernel-row.json` | A perturbed 5-bottom row raises the rank to 47: refused. |
| `receipts/local-minimum-control-infeasible-dual.json` | A withheld 4-top row leaves $-\omega_{11}$ with an exact ray: refused. |
| `receipts/local-minimum-target.log` | Progress log of the 49 to 53 second target run on one worker. |

The exact duals settle the route review’s open exploratory items.
The ten minor coordinates whose float simplex left residuals up to 1.5, and the three
directions the exploratory script reported as having no dual, all have exact nonnegative
duals. The float values were simplex artefacts.

Still missing before H-261 can be tested:

- the curvature bounds and the ratio test;
- transfer from the rational point to the algebraic root box;
- uniformity over the slider domain, which needs a slider-parameterised layout in the
  stress builder.

Reproduce:
`uv run --frozen --all-extras --group dev python -m devtools.check_n17_local_minimum --output FILE`,
with `--control kernel-row` or `--control infeasible-dual` for the controls.

## H-262: The Charge-Floor Engine Pilot

`devtools/pilot_n17_charge_floors.py` (SHA-256 `549ade62…`), built by lane B, Fable at
extra-high effort. It keeps R068’s 20,860 sites, rules and weights, whose budget
$M=17{,}000{,}448{,}944$ it reconstructs exactly.
It forces the parent side to $A_U=4.613/4.676$ and charges each pose by its open parent.
For each of the six D4 cell classes of the H259 grid, it sweeps the exact arrangement in
position over a refined angle grid.
A sampled floor is the charge of an actual legal pose, so it is an upper estimate of the
true floor; survivor counts made with sampled floors are therefore lower bounds on the
counts any exact floor instrument for this charge would give.

| Receipt | What it holds |
| --- | --- |
| `receipts/charge-floors-pilot.json` | The six floors and their witnesses; the endpoint positive control; the exact survivor counts; the structural ceiling |
| `receipts/charge-floors-pilot.log` | The 125-second run on two workers |
| `receipts/charge-floors-recount.log` | A recount from the retained floors |

The findings, all read from the JSON:

- **The charge collapses at U.** Sites spaced for cores of $0.9999993\,A_{\rm R068}$ let
  a square of side $0.99667\,A_{\rm R068}$ pass between them.
  The six class floors run from $0.063$ (corner) to $0.930$ (interior edge) of $M/17$,
  so no floor test can bite.
- **Nothing is excluded.** The two subcontainer cuts leave 61,563,363 states and
  7,703,312 D4 orbits by Burnside.
  Adding the floor test leaves the same counts, 77 times H-262’s rejection threshold of
  $10^5$. The route review’s “about 7.7 million orbits” was states divided by eight.
- **A ceiling for H-262’s registered class.** Among the cut survivors there are 2,375
  class-count vectors, and 5,970 orbits share the endpoint’s own vector $(4,4,3,2,4,0)$.
  An antipodal-pair argument shows that a single D4-symmetric linear per-cell floor
  vector leaves at least 30,966 orbits whatever charge it comes from, so H-262 as
  registered cannot be confirmed.
  *Scope, corrected 2026-10-02 after the
  [independent review](../../../../docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md):*
  this lane first stated the ceiling as charge-independent for all per-cell floors.
  The review found that it holds only for one symmetric linear floor vector.
  Asymmetric floors, families of charges, orientation-refined states and nonlinear pair
  floors all escape it; an unconstrained search over asymmetric floor vectors reached 6
  orbits, before asking whether any charge realises such a vector.

Reproduce:
`uv run --frozen --all-extras --group dev python -m devtools.pilot_n17_charge_floors --output FILE --workers 2`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
