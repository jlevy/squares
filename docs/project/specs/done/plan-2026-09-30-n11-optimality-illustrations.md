---
title: Plan for Proof-Linked n11 Optimality Illustrations
date: 2026-09-30
status: implemented
---
# Plan for Proof-Linked n11 Optimality Illustrations

**Beads:** initial plan `think-yc42`; holistic review `think-8j43`; implementation under
`think-75cp`\
**Scope:** The published T-060 explainer and its HTML, Markdown, and PDF editions.

## Implementation Record

The static publication set is implemented: twelve SVGs in eleven numbered figures,
including the retained construction and cover/mask pair.
Integration is tracked by `think-rlg8`; the five figure beads below retain the separate
changes. No browser interaction is needed to read a figure or follow an implication.

| Holistic review finding | Implemented change | Bead |
| --- | --- | --- |
| 1: Pose and owner vocabulary | Definitions precede the invariant; ownership is asserted for valid packings, allowing the outer cover to retain impossible extra poses. | `think-rlg8` |
| 2: Denominator reference | The positive quantity is named before the local ratio is introduced. | `think-rlg8` |
| 3: Capture conditions | All six new closed cuts label the ten-node tree; inherited prefixes are checked and the near leaf still requires the fixed-T theorem. | `think-y0um` |
| 4: Whole implication | Figure 2 gives both routes to optimality, with section links; the witness footer reserves U for the rational cap. | `think-c27c` |
| 5: Safe elimination | A schematic precedes the Minkowski formula; a separate four-panel accepted row distinguishes center positions, core offsets, forbidden regions and a magnified residual. | `think-cpv2` |
| 6: Charge capacity | Median projection and the accepted mask-0 example precede the general transfer formula. | `think-jjq5` |
| 7: Symmetry | Four transformed point views use the fixed cells; a source-bound strict distance ban illustrates the overlay test. | `think-jjq5` |
| 8: Capture versus isolation | The algebraic contradiction and graph precede the local contact census. | `think-0k78` |
| 9: Exact endpoint | Two container frames follow the same smaller packing to the fixed-T contradiction. | `think-0k78` |
| Center-cell capacity | Exact cell 9 and two hypothetical open disks illustrate the all-cell strict diameter lemma. | `think-y0um` |

Astra-max review checked the mathematical implications and source bindings.
Sol reviewed the prose and rendered figures.
Integration checks cover source mutations, closed cuts, complete figure slots, immutable
citations, caption rendering, shared screen/print type, and publication input selection.
The PR records final command results and hosted checks.
This publication change does not rerun the geometric proof ensemble.

The remaining design sections retain the rationale and acceptance limits.
Optional selectors are deferred: static panels answer the current reader questions and
keep the same argument available in print.

## Overview

The
[earlier explainer](../../../../packing/devtools/templates/n11-lower-bounds-explainer-article.md)
lets a reader manipulate a square and see covered mass, then shows the finite-angle
reduction and its cost.
Its screen controls teach a specific mechanism; captions and static figures carry the
argument into print.
The
[T-060 paper](../../../../packing/devtools/templates/n11-optimality-review-article.md)
began with four source-bound SVGs: the exact-construction witness, sixteen Voronoi
cells, case-438 mask, and capture ancestry.
Those drawings establish the objects and the proof’s structure, but do not yet show
*why* a center cell has capacity one, how a pose row is eliminated or retained, how
charge excludes a mask, or why the local inequality rules out nonzero motion.

The next visuals should answer those questions at the point where the paper asks them.
They explain accepted computations; rendered pixels, user gestures, and rounded numbers
never become proof premises.

The [holistic review](../../reviews/review-2026-09-30-n11-explainer-intuition.md)
prioritizes the whole argument before detailed certificate mechanics.
The first release should let readers follow the contradiction from an arbitrary smaller
packing to the exact endpoint.
The worked geometry row becomes useful once that route is clear.

## Reader Roadmap and First Release

Keep the provenance-first opening, exact theorem and construction.
Immediately after them, add a two-route map:

```text
Exact construction at T ---------------------------------> s(11) <= T

Assume a packing with side S < T
  -> put the same packing inside a rational cap U > T
  -> assign its centers to one of 2,184 continuous case classes
  -> exclude 2,180 classes by exact certificates
  -> use symmetry to bring every survivor to case 438
  -> capture all surviving poses in checked bounds
  -> map the same smaller container into the fixed-T frame
  -> apply local isolation: it must be the construction
  -> its span T contradicts fitting in S < T -------------> s(11) >= T

Both routes --------------------------------------------> s(11) = T
```

This is the logic for the figure, not its final layout.
Use two short stacked routes with section links in HTML and complete captions in print.
Group classification, exclusion and symmetry into one visual block; group capture, exact
frame and isolation into a second, keeping their distinct implications labeled.
The counts describe classes of continuous possibilities, not individual packings or
probabilities. Arrow width and colored area must not imply a measured amount of search
space.

The completed illustration set needs three coordinated explanations, rather than seven
new figures at once:

1. **Whole-proof map:** two halves of the theorem, with the smaller-packing assumption
   visible throughout. Add a short plain-language preview of the exact endpoint.
2. **Possibility versus certainty:** reuse the cell map for a capacity inset; introduce
   a possible-center region and a guaranteed inner core in one simple collision
   schematic. The exact four-panel row follows as the auditable worked example.
3. **Capture, isolation and contradiction:** annotate the existing capture tree and pair
   it with the fixed-`T` local inequality and the unchanged smaller container.
   The branch near the construction is an enclosure, not already a uniqueness result.

Use one visual vocabulary throughout: physical squares, possible center regions,
guaranteed interiors, and forbidden center regions have distinct outlines or hatching as
well as shared palette colors.
Keep physical positions, core offsets and abstract perturbation coordinates in
separately labeled panels.
Captions say whether a panel is a lemma schematic, a rendering of accepted exact data,
or an algebraic graph.
Start with static figures.
Add interaction only when a specific reader question cannot be answered as clearly by
the printed panels.

## Goals and Boundaries

- Tie each displayed datum to a retained exact input or accepted checker result, or
  label the figure as a schematic of a stated lemma.
- Give each screen interaction a legible static state and a caption that survives in
  Markdown and PDF. Keyboard, touch, and reduced-motion behavior belong in the same
  implementation slice as the interaction.
- Keep the existing witness and cover/mask figures.
  Add mechanism where those figures leave a reader to infer a proof step from a picture
  of its inputs.
- Keep the old point-certificate prover separate: its mass-atoms and direction-net
  controls do not verify T-060’s case-conditioned geometry.

No visualization will rerun the 2,180 exclusions, animate an arbitrary packing as if
every frame were certified, or suggest global uniqueness of optimal packings.
A projection of the 33-dimensional local rectangle will be identified as a projection,
not as the isolation theorem.

## Visual Map

| Priority and reader question | Figure or interaction; print state | Exact source and reusable part | Acceptance risk |
| --- | --- | --- | --- |
| **P0 — How does the entire proof fit together?** | Two-route overview after the theorem and witness: construction gives the upper bound; an assumed smaller packing passes through exhaustive restrictions and the fixed-`T` contradiction. Print retains every premise arrow. | The [whole-proof review](../../reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance), [accepted composition](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json), and existing article sections. | Counts are continuous case classes, not packings. Capture and isolation are separate; the exact frame must precede applying the fixed-`T` conclusion. No global-uniqueness claim or area-proportional funnel. |
| **P0 — How do the four capture leaves cover every possibility?** | Annotate Figure 3’s edges with the exact closed $y_{15}$, $t_{13}$, and $t_2$ cuts. Selecting a leaf highlights its assumptions and accepted outcome; print shows all four leaf predicates and the ten-node ancestry together. | [Source graph](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json), [child-state checker](../../../../packing/devtools/check_n11_capture_child_node.py), and [pose-inclusion result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json). Reuse the current tree layout and node labels. | Both sides include equality; no endpoint is lost. Edges are proof dependencies, not square trajectories. The near leaf gives an enclosure; the separate local theorem discharges it. |
| **P0 — Why does a local linear obstruction cover a finite neighborhood?** | Diagram the normalized displacement $0<\tau\le1$ and the impossible inequality $\tau\le c_j\tau^2$ with $c_j<1$. An optional branch/coordinate selector reads only accepted margins; print fixes the worst certified ratio and states the full $128\times33\times2$ signed-coordinate census. | [Local-isolation result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json), [checker](../../../../packing/devtools/check_n11_optimality_local_isolation.py), and [pose-inclusion receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json). Reuse the old explainer’s exact-versus-preview readout convention. | Show that the inequality follows from the signed-coordinate duals and curvature bounds, not from a sampled motion. A line graph is an algebraic schematic, not a plot of 33-dimensional feasible poses. Do not use a rounded ratio to establish strictness or present fixed-`T` isolation as global uniqueness. |
| **P0 — How can a cap at $U>T$ settle the exact value $T$?** | A two-frame commutative diagram follows a hypothetical packing of side $S<T$ into the centered $U$ cap, through the field coordinate conversion, then by a rigid alignment into the fixed-`T` container. Print shows the complete arrows and the nested $S$ and $T$ containers. | [Pose-inclusion checker](../../../../packing/devtools/check_n11_optimality_pose_inclusion.py), [final composer](../../../../packing/devtools/check_n11_final_composition.py), and [accepted composition](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json). Reuse the paper’s frame formulas rather than a new geometric animation. | The field scale $B=L/U$ changes coordinates; it does not rescale a physical unit-square packing. The final map is a rigid rotation and translation. Trump’s exact span $T$ contradicts $S<T$; the drawing must not assert uniqueness at side $U$ or at every optimal pose. |
| **P1 — Why can a cell hold only one center?** | Extend Figure 2 with one selected cell, its physical diameter bound, and two hypothetical centers whose radius-`1/2` disks overlap. Print uses a visually clear cell; an optional selector can expose all checked bounds. | Sixteen rational polygons bound by the [D4 receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json) and the independent [cell checker](../../../../packing/devtools/check_n11_optimality_d4.py). Reuse the current cell SVG coordinates and labels. | Compare the exact squared diameter with $1/(U-1)^2$; keep boundary ties closed. The cell contains a center, not necessarily the square. Displayed centers are hypothetical, not a packing or a measured minimum. |
| **P1 — How does an owner update preserve every possible pose?** | Four aligned panels for one accepted row: admitted center domain and whole angle interval; square-relative strict core and a partner’s owned hull; the reconstructed closed $K+(-Q)$ forbidden center region; residual cover and the row’s contribution to a complete ownership update. A step control may reveal panels in order. Print contains all four panels. | Use generic case 2095, step 1, owner 10, row 17 from its [accepted full result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json), source-bound by the [generic fresh checker](../../../../packing/devtools/check_n11_generic_fresh.py). The row has one triangular residual; its checker reconstructs owned-hull obstacles rather than copying proposed collision polygons. Reuse exact polygon-to-SVG and accessible labels. | Bind the row, accepted predecessor, and complete successor. Keep center positions distinct from core offsets, and show the whole closed interval, not a sampled angle. Strict interiors justify rejecting the forbidden boundary. Cover the independently established legal domain, including residual segments and points. Ownership promotion waits for every row of the complete closed angular cover, common-core and compression checks; one row supplies only a contribution. This is a noncandidate case, not case-438 capture. |
| **P1 — Why can a field charge exclude many masks?** | A small two-core median-projection example, paired with a set diagram for required-owner membership and the strict sum $\sum q_i>b$. A selector can switch between a qualifying and a nonqualifying retained mask; print fixes one checked qualifying example and one counterexample to the transfer rule. | [Field checker](../../../../packing/devtools/check_n11_optimality_field_mask0.py), [field receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json), and [exclusion inventory](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json). Reuse the current mask cell IDs and highlight style, not the older article’s atom canvas. | Charge is median *projection* support, not “three sites inside a core.” Required owners and strict budget must be checked for every mask shown; equality is not an exclusion. A two-core drawing illustrates capacity one, not all 1,904 field cases. |
| **P2 — Why do four surviving masks reduce to case 438?** | A single point’s four reflected/rotated views over the current cell map, with label sets and one strict distance ban; print uses a four-view strip plus a short statement of exhaustive search. | [D4 checker](../../../../packing/devtools/check_n11_optimality_d4.py) and [accepted D4 result](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json). Reuse the cover SVG; derive overlay regions from the retained rational object. | An irregular cell need not rotate into one cell. Retain shared boundaries, including eight singleton overlay regions, and distinguish an illustrative ban from the exhaustive 220-region/1,572-ban search. |

The existing exact witness already answers “What attains $T$?” and needs no second
placement drawing. In its article adaptation, replace the atlas footer’s generic “U
Trump” label with “Trump construction at $T$”: the article reserves $U$ for the larger
rational cap. Preserve the retained atlas source.

The first additions are the whole-proof map and the capture-to-contradiction
explanation. A reader-facing capture summary can show four leaves with their closed
predicates, while the full ten-node ancestry remains in an adjacent technical figure or
linked table. Preserve every dependency and state join.
The near leaf must lead through the checked fixed-`T` frame before local isolation and
the span contradiction.

## Implementation Slices

The priorities in the visual map describe teaching order.
The following beads own the work; they are separate reviewable changes under
`think-75cp`.

| Order | Bead | Deliverable and reader check |
| --- | --- | --- |
| First, parallel drafts | `think-c27c` | Whole-proof map and short reading path. Can the reader distinguish the upper-bound construction from the lower-bound contradiction? |
| First, parallel drafts | `think-0k78` | Local-inequality schematic and exact-frame endpoint. Can the reader explain why capture alone is insufficient, and why the same smaller packing reaches a contradiction without shrinking? |
| Alongside the endpoint | `think-y0um` | Closed capture-cut labels, followed by the center-cell capacity inset. Can the reader see that no boundary case was discarded and that cells contain centers? |
| Next | `think-cpv2` | Simple possibility/core collision schematic followed by the accepted four-panel geometry row. Can the reader explain one safe elimination and what remains to complete the update? |
| Next | `think-jjq5` | Median-projection capacity and strict charge example, then a separate D4 overlay checkpoint. Can the reader distinguish these reductions from the worked geometry row? |

Draft the roadmap and endpoint in parallel with disjoint figure assets; integrate shared
renderer and article changes in one lane.
Reuse the shared typography and SVG roles.
Add new figure slots and tracked inputs deliberately, rather than preserving the current
four-slot count as a design constraint.

Start with complete static HTML, Markdown and PDF. After reviewing those, consider a
capture-leaf highlighter whose default and printed state show every branch.
Defer branch and coordinate selectors until a reader question establishes their value.
Do not make interaction a prerequisite for understanding or auditing any step.

Review the paper text and figure placement with the user’s line edits before changing
figure numbering or captions.
The first rendered checkpoint is the overview plus the endpoint; detailed certificate
illustrations follow that checkpoint.

## Verification and Publication

For every generated figure, compare its displayed case IDs, intervals, polygon vertices,
inequalities, and statuses with source-bound exact data before rounding to pixels.
Test malformed or missing source data as a render refusal.
A visual test must inspect HTML and the static PDF page at normal print scale; the
screen interaction must expose the same mathematical statement through keyboard controls
and text, with no hidden required step.
The publication check should reject absent figures, duplicate SVG IDs, remote or active
SVG content, stale render inputs, and an interaction that prints as an empty panel.
Keep diagrams explicitly explanatory.
Proof credit rests on the reviewed mathematical implications and observed source-bound
executions; the final composition checks their joins.

## Open Decision

The case-2095 row is the proposed first detailed worked-row implementation, after the
overview and endpoint, because its exact reconstructed owned-hull obstacles and one
triangular residual make the lemma visible.
Review its source-bound polygons and complete-step successor before final layout.
The
[first capture row](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json)
is a separate, stronger example: its collision region is checked against all 149 partner
rows, 93 live, not merely against one fixed owned hull.
If shown later, label that universal obligation and keep its complete
[step receipt](../../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json)
separate from the single-row receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
