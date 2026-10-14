# Research: Regularizing Every Known-Best Packing for Display

**Date:** 2026-10-11 (last updated 2026-10-12)

**Author:** Joshua Levy, with Claude (session_017JNnKDwL74rnktr9s8BdjP)

**Status:** Complete (spikes, recommendations, the owner’s decisions of 12 October 2026
and the full run; a pass for grid regions and the re-run of the counts whose witnesses
change are in progress)

**Bead:** think-pwmi (epic think-cdud).

## Overview

The atlas draws each known-best packing of $n$ unit squares, $n = 1..324$, with the
house renderer: a square’s hue is its angle class and its shade is how many of its four
sides it shares whole with a wall or a same-angle neighbour.
Under those two conventions a packing’s regular structure (rows, blocks, strips,
symmetric tilted bands) should read at a glance as a few uniform hue families in dark,
even shades. It often does not, because the witnesses the record holds carry slack and
noise the drawing makes visible: a row a few hundredths off its wall renders light, a
square tilted a few hundredths of a degree off the axis leaves the axis hue altogether,
and a tilted band whose angles differ by more than a microradian splits into several
hues.

**Regularization** redraws a packing the record already holds so that it reads cleanly,
without changing its side, its evidence tier or its credit.
This document collects what the project has done about it so far, what each approach
fixed and could not fix, what the spikes of 11 October 2026 showed on 25 pilot counts
and the full run of 12 October on all 324, and the standard approach recommended for
regularizing every result: an automated pass under the
[regularization policy](../policies/regularization-policy.md), with judgment reserved
for the cases the automation cannot decide.

The owner’s request (11 October 2026): regularize all current results “using something
similar to what Evan Daniel has done”, with a standard policy and automation wherever
possible and judgment on the trickier cases, so that the results look right in the
diagrams’ colour conventions.

## Questions to Answer

1. What makes a known-best drawing look irregular in the house conventions, and how much
   of it is the packing and how much the witness’s representation?
2. What has the project tried, what did each approach fix, and what did each leave?
3. What does Evan Daniel’s process add, and what does it cost in the record’s terms
   (side, identity, credit)?
4. On the pilot counts, what changes, and does the result look cleaner by the house
   measures: fewer hue classes, more full-side contacts, no square lighter than before?
5. What is the standard procedure for all 324 counts: which counts it can settle
   automatically, which need review, and which need a different route (an algebraic
   field, or a register result first)?

## Scope

**In scope:** the display layer for the known-best atlas and case pages; the two
generators (`regularize_axis_components/2` and Evan Daniel’s vendored regularizer); the
side, identity, shading and labelling rules; the spikes run on 11 October 2026; the plan
for a full run.

**Out of scope:** new upper bounds as such (a certificate below the verified bound is a
register result and goes through the import runbook, not this document); proofs of local
optimality; the renderer’s palette.

## Findings

### How the House Conventions Read a Packing

Two renderers draw packings, and they decide hue and shade differently.

|  | House renderer (atlas, website, case pages) | Stage rule (workbench) |
| --- | --- | --- |
| Code | `packing/src/sqpack/render/color.py` | `packages/workbench/src/core/geometry.ts` `contactFacts` |
| Hue | Angle classes seeded at $10^{-6}$ rad and merged where full-side contacts link them; right angles pinned to hue 0 (green), 45 degrees to hue 1, the rest by class size | Half-degree angle classes |
| Shade | 4 minus the number of sides shared whole with a wall or a same-class neighbour, both ends within $2 \times 10^{-6}$ | Centres a side apart within 0.01, angles within half a degree |
| What it exposes | Any slack above $2 \times 10^{-6}$, and any tilt above a microradian | Slack above a hundredth; tilts above half a degree |

So the house drawing is strict: it shows the witness exactly as retained.
A row 0.03 off its wall is light; an “axis” square tilted 0.01 degrees is not green; two
squares of one tilted band that differ by $10^{-5}$ rad are two hues.
Nothing in the drawing distinguishes a real gap from representation noise, which is why
the layer exists.

### Why Drawings Look Irregular

The census of 2 October 2026 (X-049, “Why Grid Squares Render Light”) settled the first
question: light shading is not inexact arithmetic.
Of 45,468 green (axis-aligned) squares in the atlas, 7,725 rendered light:

- **5,272 structural:** they border a tilted square, a hole or a staggered row, and
  should stay light.
- **2,419 slack:** they sit beside a real gap or sideways shift of $2 \times 10^{-5}$ to
  0.5 in the retained coordinates.
  Almost all are in records that came from optimizer packets (Couzo, de Winter): at
  $n = 102$ every one of 69 green squares was light, with the top row 0.0298 from the
  wall.
- **34 in the precision band**, missing contact by less than ten times the renderer’s
  tolerance.

Where squares do touch, the arithmetic is fine (median contact residual 0, largest
$2 \times 10^{-6}$). The slack is in the packings as retained: optimizers stop when the
side stops improving, and a square that carries no load is left wherever it was.

Three other sources of irregularity matter for hue rather than shade:

- **Near-axis tilts.** Float optimizers almost never return an exactly zero angle: at
  $n = 301$, 131 squares sit between $10^{-6}$ rad and 0.68 degrees.
  Each leaves the green class; 265 squares atlas-wide are not green for this reason
  alone.
- **Angle noise inside tilted bands.** Evan Daniel’s exact solve groups angles by exact
  equality and finds 2,400 distinct rotation groups over the 324 records, 1,172 after
  merging; $n = 66$ goes from 31 groups to 2. Not every split is noise: $n = 175$ has a
  true 0.801-degree column, and whether $n = 71$’s two-class split is load-bearing is
  open (H-050).
- **Decimal witnesses.** 106 of the 324 witnesses are decimal (most from the Kingbird
  catalogue). Rounded to 36-digit rationals, 73 of them overlap by a sliver, so no exact
  frame exists at the record’s side without changing it.

### What Has Been Tried

**`regularize_axis_components/2`** (this project, 2 October 2026, X-049 “Exact
Regularization”). Straighten every square within $10^{-4}$ rad of the axis, slide each
axis square one axis at a time toward its lattice slot until it meets an exact contact,
hold any move that lowers a house or stage count (its own or a neighbour’s), and verify
the result twice over $\mathbb{Q}$ at the witness’s side.
It is sound at the same side by construction, and it is the only generator that measures
non-regression. Today it changes 68 records, leaves 182 unchanged and refuses 74; on the
68 it changes, light green squares fall from 4,666 to 2,609 with no regression, and 149
squares are held. It cannot touch tilted structure, impose symmetry, merge hue classes,
or frame a decimal witness that overlaps at dilation 1.

**Dilation** (`--smallest-dilation`, measured 2 October 2026). Scaling the decimal
witnesses’ rational poses by $1 + 10^{-p}$ until they verify frames all 89 then refused,
but changes the side, and changed only two squares’ shading.
The atlas README’s ruling of that day refused it: a dilated view certifies a side the
register does not hold, which is a tier promotion under a drawing’s name.

**Evan Daniel’s regularizer** (`search/regularize`, 9 and 10 October 2026, vendored here
at `675a5ea`). Re-solve the packing to an 80-digit KKT point of minimizing the side;
hold the angles and side fixed and move the centres by a translation LP, so every LP
point is a packing; impose the largest container symmetry; choose coincident faces with
a MILP; merge free squares’ angles into existing groups, and undetermined groups too
(`conservative` path-tests each merge; `fewest` also merges determined groups within 5
degrees); refine and verify at 80 digits; write a rational certificate dilated by
$1 + 10^{-20}$. It reaches tilted structure, symmetry and the decimal records, and its
lists change 147 records (the project’s tool, 68). Its cost in the record’s terms: its
side is never the witness’s; its “same packing” is a sampled numerical path test; and at
three of T-146’s fifteen counts no symmetry pairs its squares one to one with the
credited packing.

**T-146** (10 October 2026). Fifteen of Evan Daniel’s regularized certificates were
below the register’s bound and became register results, the first to carry a typed
`regularizations` credit.
The review accepted them for finite feasibility only and measured 10 to 239 squares
moved beyond $10^{-3}$.

**Same-side exact re-solve** (planned in the assessment’s slice 3, built in this
session). Take the regularized view’s angles in the witness’s own exact rotation frame,
find the contacts tight at the generator’s point, and solve them over $\mathbb{Q}$ at
the witness’s own side.
Where every rotation is rational in the witness’s frame this turns Evan Daniel’s view
into a `same`-side view; it is the step that lets “clean” and “no side changed” hold
together.

**Proposed, not built:** exact compaction of the remaining slack squares inside a fixed
tilted structure (think-qun0), releasing the 149 held squares by joint moves
(think-mkyx), and views over $\mathbb{Q}(\sqrt{2})$ and other fields for the refused
decimal records (think-yk2h). A renderer-side fix, loosening the house tolerance, would
reach only the precision band (34 squares then, 65 now), so it was never pursued.

### Rules Already Decided

- **A regularized drawing changes no side, frontier value, evidence tier or credit**,
  and never replaces the witness (epic think-los0, 2 October 2026; the index’s policy
  line; the regularization policy, section 1).
- **Non-regression:** no square’s house or stage count may fall (X-049; policy
  obligation 4).
- **No dilated frames** (atlas README, 2 October 2026; policy decision-table row 4).
- **A certificate below the verified bound is a register result first** (policy section
  1, row 3).
- **Identity is measured, not asserted:** the record says “the same packing” in its own
  voice only with a `measured` basis (results schema; policy section 2).
- **Credit:** the packing stays its finder’s; the regularization is credited by
  `regularizations` items; Evan Daniel’s method is credited whenever his code made the
  view (policy section 7; the vendored README).
- **The website shows regularized drawings only, with no badges**, and its legend keeps
  only tilt colours and contact shades (owner, 5 and 9 October 2026).

### The Spikes of 11 October 2026

**The pipeline.** `devtools.regularize_evand` drives the vendored code at `675a5ea`: the
witness written at full precision as upstream’s input, the exact solve, the regularizer
(`conservative`, `coincide`, source orientation), the certificate imported and decided
on three exact routes, `devtools.regularize_same_side` to bring the view to the
witness’s own side over $\mathbb{Q}$, identity by `arrangement_gap`, the house and stage
contact histograms, and the policy’s decision table.
`devtools.regularize_gallery` draws each count’s source, regularized view and current
layer view with the house renderer.
Run outputs stay outside the repository; nothing in the record changed.

**Pilot 1: the policy’s edge cases.** Fifteen counts: the epic’s pilot set (10, 26, 70,
101, 129, 146, 200, 324), records the current layer has no view of (5, 10, 11, 17, 37,
51), the T-146 counts whose identity failed one to one (129, 292), and the generator’s
known failure (261). “Light” below means squares that share at most one whole side, as
the house renderer counts them.
Outcomes are reported in the words the owner asked for on 11 October 2026 (policy
section 4, “How a decision is reported”): **admitted**, **held** (a visible improvement
waiting on the record), **refused** (a visible change that fails a rule), **no change**
(the picture would not change, whatever row matched) and **no view** (the generator
produced nothing). The row that decided is given with each.

| $n$ | Witness | Outcome (policy row) | Angle classes | Light squares | Four-side squares | What moved |
| --- | --- | --- | --- | --- | --- | --- |
| 5, 10 | decimal, Göbel family | no change (row 4; same side impossible) | 2 | unchanged | unchanged | nothing visible |
| 11 | decimal | no change (row 10; $10^{-33}$ off the witness) | 2 → 2 | 6 → 6 | 1 → 1 | nothing visible |
| 17 | decimal | no change (row 3: a candidate $10^{-22}$ below the bound) | 3 → 3 | unchanged | unchanged | nothing visible |
| 26 | decimal | **admitted** (10) | 2 → 2 | 1 → 0 | 7 → 8 | one rattler, 0.31, onto the grid |
| 37 | decimal | held (3): register first, $9.9 \times 10^{-15}$ below | 4 → 4 | unchanged | unchanged | 7 squares, up to 0.16 |
| 51 | $\mathbb{Q}(\sqrt{2})$ | no change (row 4; no rational frame) | 2 | unchanged | unchanged | nothing visible |
| 70 | rational (Xu) | held (3): T-146’s side, $1.5 \times 10^{-10}$ below | 6 → 4 | 21 → 16 | 33 → 35 | 10 moved, 6 turned |
| 101, 200 | decimal | no change (row 3: candidates about $10^{-14}$ below) | 2 → 2 | unchanged | unchanged | nothing |
| 129 | rational | held (3): T-146’s side, $1.3 \times 10^{-10}$ below | 8 → 6 | 27 → 19 | 79 → 79 | 20 moved (up to 0.87), 2 turned |
| 146 | rational | held (3): T-146’s side, $9.8 \times 10^{-11}$ below | 3 → 3 | 38 → 35 | 80 → 80 | 24 moved |
| 261 | rational (Xu) | no view (1): the exact solve finds it not jammed | 2 | unchanged | unchanged | nothing |
| 292 | rational (Rehwaldt after Couzo) | **admitted (10)** | **24 → 9** | **132 → 54** | **84 → 198** | 102 moved (up to 0.42), 17 turned |
| 324 | grid | no change (5) | 1 | 0 | 324 | nothing |

Identity was one to one at every count that produced a view.
The run cost 857 CPU-seconds and 670 seconds of wall time at two workers.
At $n = 292$ the stages took 240 s (exact solve), 49 s (regularizer), 22 to 32 s (each
exact route), 170 to 206 s (same-side re-solve) and 72 s (`arrangement_gap`).

**What the pilot shows.**

- **Where the packing has a tilted band assembled by an optimizer, the change is large
  and exactly what the colour conventions need.** At $n = 292$ the band’s 24 hue classes
  become 9, the light squares fall from 132 to 54, and squares with all four sides
  shared rise from 84 to 198, at the record’s exact side.
  The current layer reaches 124 there.
- **Where the packing is a Göbel-style 45-degree family or a clean grid, there is little
  to do.** At 5, 10, 11, 17, 51, 101, 200 and 324 nothing visible moves.
  Those drawings already read cleanly, so leaving them as they are costs nothing
  visually.
- **Re-solving finds a lower packing nearby.** At 70, 129 and 146 the exact solve lowers
  the side by about $10^{-10}$, and the regularized view is a `solved` certificate below
  the case record’s bound.
  Those three sides equal T-146’s registered certificates, which the case records have
  not yet adopted as their bound.
  At 70 and 129 the solve also turns a tilted band (0.0115 degrees at 70), which no
  exact rotation of the witness matches, so the same-side re-solve refuses.
  At 146 it turns nothing: every rotation stays within $10^{-10}$ degrees of the
  witness’s, and only the re-solve’s first tolerance, $10^{-12}$ degrees, refused it.
  The full run’s re-solve matches within a sine of $10^{-9}$ and admits 146 at its own
  side. Starting the regularizer from the witness’s own pose instead (`--frame witness`)
  did not help: upstream’s 80-digit verification finds overlaps of about $10^{-10}$
  there.
- **Row 3 is mostly rounding.** At 17, 37, 101 and 200 the same-side view is exact at
  the witness’s printed side, which lies $10^{-22}$ to $10^{-14}$ below a verified bound
  that is an exact certificate’s side rounded up at fourteen decimals.
  Each is technically a new verified bound, so the policy holds the drawing until it is
  registered.

**Pilot 2: where upstream merges most.** Ten counts chosen from upstream’s best-choice
list by how many rotation groups it merges, including three the current layer refuses
(66, 87, 260).

| $n$ | Witness | Outcome (policy row) | Angle classes | Light squares | Four-side squares | What moved |
| --- | --- | --- | --- | --- | --- | --- |
| 66 | decimal | **admitted** (10) | 2 → 2 | 0 → 0 | 33 → 33 | 24 squares by up to 0.025, into the packing’s symmetry |
| 86, 127 | rational | no view (1): the exact solve finds the newer witness not jammed | — | — | — | nothing |
| 87 | decimal | held (3): register first, about $10^{-14}$ below | 3 → 3 | 16 → 16 | 49 → 49 | 6 squares, up to 0.003 |
| 102 | rational | held (3): T-146’s side, $7.9 \times 10^{-11}$ below | 4 → 3 | 29 → 26 | 46 → 46 | 15 moved, 1 turned |
| 126 | rational | **admitted (10)** | **5 → 2** | **26 → 7** | **51 → 55** | 15 moved, 3 turned |
| 206 | decimal (Couzo) | **admitted (10, `bound`)**; held (4) before 12 October | **44 → 4** | **135 → 26** | **32 → 144** | 96 moved, 40 turned |
| 260 | decimal | no change (row 3: a candidate about $10^{-14}$ below) | 2 → 2 | 0 → 0 | 188 → 188 | nothing |
| 267 | rational | held (3): register first, $2.5 \times 10^{-11}$ below | 9 → 5 | 41 → 37 | 196 → 196 | 31 moved, 10 turned |
| 295 | rational | review (7): 22 per-square counts fall, no total does; refused before 12 October | 2 → 2 | **62 → 3** | **101 → 166** | 122 moved |

It cost 1,598 CPU-seconds and 933 seconds of wall time at three workers; the exact solve
at $n = 260$ alone took 801 s.

Three cases decide how the policy should read:

- **$n = 206$ is the clearest picture of what regularization is for.** Near-axis noise
  gives the source 44 angle classes, so the drawing scatters colour across a region that
  is a grid; the regularized view has 4 classes and a dark carpet.
  Its side is not the witness’s printed side, but it is **exactly the verified upper
  bound**: the certificate’s side and the case record’s bound are the same rational,
  $232189979115498488075628916091 / 15625000000000000000000000000$, because T-098 made
  that bound from Evan Daniel’s exact solve of this same packing.
  Row 4 held it as a side other than the witness’s, but it certifies nothing the
  register does not already hold, and it passes every other check: no square’s count
  falls, the pairing is one to one, and the largest move is 0.37. The owner’s answer of
  12 October 2026 admits it as the side relation `bound`.
- **$n = 295$ improves on every histogram total** (light squares 62 to 3, four-side 101
  to 166) and is refused because 22 individual counts fall: one square loses a house
  contact and a row of squares loses a stage contact each.
  Strict per-square non-regression, written for the axis tool’s single slides, is too
  strict for a generator that moves a whole band; this is a case for review, and since
  12 October 2026 row 7 sends it there.
- **$n = 86$ and 127 fail in the exact solve** on the newer witnesses the record now
  holds, which upstream never solved.
  The current layer’s views stand there.

**The `fewest` variant** (owner question 1), run at 129 and 292 from the same solves:

| $n$ | Variant | Rotation groups | Identity | Four-side squares | Outcome |
| --- | --- | --- | --- | --- | --- |
| 129 | `conservative` | 10 → 6 | one to one | 79 → 79 | held (3) |
| 129 | `fewest` | 10 → 4 | **not one to one** | **79 → 53** | held (3) |
| 292 | `conservative` | 24 → 9 | one to one | 84 → 198 | admitted (10) |
| 292 | `fewest` | 24 → 7 | one to one | 84 → 198 | alternate (8) |

`fewest` merges two more groups at each count and, at 129, loses 26 four-side squares
and the one-to-one pairing T-146’s review also found missing.
It buys little for the colour conventions and costs identity.

### The Full Run of 12 October 2026

All 324 counts ran with the pilots’ settings (`conservative`, `coincide`, source
orientation, the KKT frame, 1,800 s limits on the exact solve and the regularizer) at
four workers, against the witnesses `main` held that day, and were decided under the
owner’s answers of 12 October.
It cost 49,290 CPU-seconds (13.7 CPU-hours) and 3.8 hours of wall time, about twice the
pilots’ fit: the exact solve took 100 to 700 s a count between $n = 240$ and 254 alone.

| Outcome | Counts | Rows |
| --- | --- | --- |
| **admitted** | 32: 20 at the witness’s side (`same`), 12 at the verified bound (`bound`) | 10 |
| review | 13: 106, 172, 199, 207, 211, 228, 259, 295, 297, 301, 305, 306, 307 | 6 (8), 7 (4), 9 (1) |
| refused | 3: 110, 179, 241, where a house or stage total of shared sides falls | 7 |
| held, register first | 30 | 3 |
| no view | 18: the exact solve finds the witness not jammed (10), fails (4), times out (290, 302), certifies an invalid point (1) or stops at a local minimum (303) | 1 |
| no change | 228: 176 already in the regular pose, 38 register candidates and 14 others with nothing visible to change | 3, 4, 5, 10 |

Row 3 lists 71 register candidates in all, the input to the batch registration
(think-omqv). Of the eight row 6 reviews, seven turn a square that the regularizer’s
recorded angle changes do not name, and one (228) has no one-to-one pairing.

**A wider rotation tolerance.** Comparing this layer with #515, a parallel
implementation, showed that the exact solve leaves the rotations it does not turn within
$10^{-10}$ degrees of the witness’s (7.5e-11 at $n = 146$), and that the same-side
re-solve’s tolerance of $10^{-12}$ degrees refused those views as `unmatched-rotation`.
The re-solve now matches within a sine of $10^{-9}$, about $5.7 \times 10^{-8}$ degrees,
#515’s tolerance and a thousand times below the policy’s turn threshold.
The 34 counts the first tolerance refused ran again from the import stage (3,356 s of
wall at two workers):

- 102, 103 and 146 move from held to **admitted** at the witness’s own side, and 123
  from held to review.
- Six admitted views move from `bound` to `same`, the witness’s exact side: 132, 156,
  182, 206, 268 and 304. 110 and 241 stay refused, now measured at the witness’s side.
- 22 still fail the re-solve: 15 with a rotation the solve turns beyond the tolerance
  (70, 129, 267 and 12 others), four views that do not close at $s_W$ (210, 228, 240,
  273\) and three whose exact coordinates are too long to write (270, 272, 306). 210,
  240 and 273 are admitted at the bound; at 270 and 272 the solved view’s own side is
  the witness’s, an exact certificate at that side, so they are admitted as `same`.

After the re-run the run decides **35 admitted** (29 `same`, 6 `bound`), 14 review, 3
refused, 26 held, 18 no view and 228 no change.

What the full run adds to the pilots:

- **The bound relation admits what the witness’s side cannot.** Six of the 35 admitted
  views (177, 181, 210, 240, 271, 273) have exactly the verified bound as their side,
  where the re-solve at $s_W$ turns a band or does not close: the exact solve reproduces
  the side the register already certifies.
- **Bent bands keep their tilts.** At 237 to 241, 270 to 273 and 304 to 307 the band
  bends through 20 to 30 distinct angles that are determined, not free, so
  `conservative` leaves them; the shading improves (at 271, light squares 135 to 91 and
  four-side squares 72 to 143), but the hues stay.
  Merging them is `fewest`’s change, which the owner declined.
- **Grid regions stay noisy where no view is produced.** At 302 the exact solve timed
  out and at 303 it stopped at a local minimum, so the drawings keep the witness’s
  slack: at 302, 76 of 242 axis squares share at most one side, and 10 squares sit
  between $0.0001$ and $0.44$ degrees off the axis, each in its own hue.
  The current axis-tool view leaves 33 light and 9 near-axis there.
  A pass for axis regions, independent of the exact solve, is being built.
- **42 counts change witness in #518**, which adopts reviewed lower houses (T-146 at 13
  counts, T-150 at 146 and 261, and others), so their results here are measured against
  the old witnesses and are run again on the new ones.

### What Reached the Record by the Morning of 12 October 2026

The owner asked overnight for regularized versions of everything, in pull requests ready
to merge and captured in the frontier records.
Four pieces of work followed the full run, each in its own layer.

**The no-view ladder (#511).** A retry ladder for counts where the solve gives no view:
higher precision, a forced KKT step on a noise-level stall, the relaxed gate, and a
replica patch to the vendored solver that stops `probe_flat` at its stall floor
(recorded as a `replica` change in `vendor/evand-regularize/vendored.yaml`). Of the five
counts that keep main’s witness, it recovers 258, 290 and 302:

- 290 certifies and is no change.
- 258 is held, then refused once registered: its totals fall against today’s view.
- 302 certifies with upstream’s two active-set steps.
  Light squares fall from 240 to 81 and house sides rise from 570 to 1,005. It goes to
  review because the solve, not the regularizer, turns squares 114, 115 and 140.

150 and 155 still give nothing.

**The grid pass (#530).** `devtools.regularize_grid_slack` closes free slack and
straightens squares tilted under 0.5 degrees at the record’s side, then re-solves
exactly and decides on both maintained routes.
Over all 324 counts, 72 had a light, uneven or near-axis square in today’s drawing or
Evan Daniel’s view. All 72 gave an exact view, one to one with the witness: 67 at the
witness’s side and 5 at the bound.
Taking a grid view only where it is better on some measure of the drawing census and
worse on none, the atlas would draw 25 grid views.
Against today’s atlas:

- variation (uneven and near-axis squares) falls from 1,344 to 481;
- near-axis squares fall from 248 to 12.

17 of the 25 are among #518’s counts.

**The record (#548).** The layer’s index became a multi-generator contract
(`RegularizedAtlasIndex/v2`): every view names its generator and pin, and carries its
regularization in the register’s `regularizations` terms with identity measured.
`--verify-atlas` decides every drawn view again on both exact routes.
The register gained a generated `regularized_drawings` block that lists each drawing
under the result holding the drawn packing, and `check_results` checks the block.

**The registration (#549).** T-155 registers the exact sides of 59 views that sat just
below their verified ceilings: 5.4e-20 to 9.9e-15 below, V3/C3, S1. Each case record
keeps the decimal it printed.
At 33 counts the side is exactly that of Evan Daniel’s certificate of the same packing
(T-101), so those bounds were already published, and the records cite T-101’s
independent replay beside T-155’s decision; the 26 other sides, the witnesses’ own, are
new. With the bounds refreshed from the records, 16 of the 22 counts held at row 3 are
admitted. 39, 204 and 299 go to review, and 53, 151 and 298 are refused.
A sixtieth count, 176, left the batch when #553 re-housed it below the side of its view.

The end state when T-155 was registered, before #518 and #553 re-housed 51 counts:

| Drawing | Counts |
| --- | --- |
| From a regularized view | **87**: 43 axis tool, 37 Evan Daniel (24 at the witness’s side, 13 at the bound), 7 grid pass |
| Unchanged: the witness is already in the regular pose, or nothing visible changes | 182 |
| The witness as drawn: no generator’s view is admissible yet | 55 |

- **Light squares.** Under the house rule, light squares across the atlas fall from
  7,704 (the witnesses) and 5,647 (main’s layer) to 5,511. No count’s house or stage
  total falls.
- **The record.** 82 drawings are recorded in `regularized_drawings`. Five are listed
  unregistered:
  - 18, 26, 66 and 85 are Kingbird and Friedman packings with verified bounds but no
    register result;
  - 87 is drawn at the witness’s side, 4.3e-16 above T-155’s bound.
- **Still to draw.** Every count is either drawn regularized or has a recorded reason
  for keeping its drawing:
  - the review queue goes to the owner;
  - #518’s 42 counts wait for their new witnesses;
  - the remaining refusals are views whose house or stage totals would fall.

**Addendum, 12 and 13 October 2026: #518’s 42 counts (layer 7).** #518 merged with its
new houses, and the axis tool’s views of them entered the layer.
Both generators were then run on the new witnesses, and each count was decided by the
grid lane’s rule, as in the grid pass above.
As the layer stands on 13 October:

- 14 of Evan Daniel’s views are drawn.
  18 were admitted on 12 October; 270’s lapsed when #553 re-housed it (below), and three
  were withdrawn on 13 October: 236’s because it turned two squares 0.000537 degrees off
  their group and drew one more angle class, and 180’s and 207’s because they tied the
  axis tool’s views on all seven measures at the same side, which the owner’s rule does
  not draw.
- 10 grid views are drawn, at 105, 131, 146, 156, 175, 211, 267, 292, 307 and 308; 305’s
  lapsed with #553.
- 232’s grid view goes to review: five per-square counts fall against #518’s view.
- The other 16 counts keep the axis tool’s view of the new house.
  303 is among them: its new house draws 4 / 8 / 0, which neither generator changes.
- At 302 the new house already draws 0 / 0 / 0, and Evan Daniel’s view adds four full
  sides.

Over the 42 counts as admitted on 12 October, before #553 and the withdrawal at 236,
against #518’s drawings:

- light squares fall from 230 to 133;
- uneven squares fall from 588 to 361;
- near-axis squares fall from 182 to 6;
- house sides rise from 21,701 to 23,038.

#553 then re-housed 270 and 305 again (T-151, T-152), so the Evan Daniel view at 270 and
the grid view at 305 lapsed with the witnesses they were made from, and the axis tool’s
views of #553’s witnesses are drawn there.
The census above was measured before that and before 236’s view was withdrawn.

The end state, with #553 merged:

- 90 counts drawn from a regularized view: 25 axis tool, 48 Evan Daniel (37 at the
  witness’s side, 11 at the bound) and 17 grid;
- 181 unchanged;
- 53 drawn as the witness.

Light squares across the atlas fall from 5,580 to 5,455. The witnesses alone have 7,628,
now that #518 and #553 have re-housed their counts.
85 drawings are recorded in `regularized_drawings`, with the same five listed
unregistered.

## Key Insights

1. **The record’s side is the binding constraint, and it sorts the 324 counts into four
   kinds.** A rational witness (217) can be regularized at its own side over
   $\mathbb{Q}$. A decimal witness whose printed side is at or above its optimum can be
   regularized at its printed side.
   A Göbel-family decimal witness, whose printed side truncates an irrational optimum,
   has no rational packing at that side at all.
   The algebraic witness at $n = 51$ needs its own field.
   The same-side re-solve’s survey of $n = 1..80$ shows this split exactly: every
   rational witness reaches `same`, 15 of 25 decimal witnesses do, and the 10 that do
   not are the Göbel family.
2. **The house renderer is strict, so regularization must be exact.** It counts a shared
   side only when both ends match within $2 \times 10^{-6}$ and merges angle classes
   only within $10^{-6}$ rad.
   A float snap would leave squares one rounding away from contact.
   An exact re-solve over $\mathbb{Q}$ closes contacts with residual zero and makes
   equal angles literally equal, which is what the renderer rewards.
3. **Most of the visible gain is in optimizer-packet records**, the same ones X-049
   found slack in. The Kingbird and Göbel-family drawings are already regular.
4. **Some “candidates” are the register’s own results seen again.** A regularization run
   rediscovers registered-but-unadopted refinements (T-146) and the rounding gap between
   a printed side and its verified bound.
   Both should be settled in the record before a full run, so the run’s candidate list
   means something.
5. **Two generators are complementary.** Evan Daniel’s reaches tilted structure,
   symmetry and angle merges; the project’s tool measures non-regression square by
   square. At $n = 292$ Evan Daniel’s view has fewer light squares than the project’s
   current view (54 against 87) and more four-side squares (198 against 124); at 70 and
   129 the project’s current view changes nothing visible.
6. **The decision table was right about soundness and too blunt about drawings.** Of 25
   pilot counts the first table admitted 4 (26, 66, 126, 292). Eight were held: by
   T-146’s refinements rediscovered and by rounding below the bound (row 3), or by a
   view exactly at the verified bound (row 4, $n = 206$). One was refused for per-square
   regressions while every total improved (row 7, $n = 295$). None of those is a
   soundness problem. Under the owner’s answers of 12 October 2026 the same pilots admit
   5 (206 joins), hold 7, send 1 to review (295) and refuse none.
   Nine change nothing visible, among them the Göbel family and $n = 51$, which would
   need a number field, and three give no view because the exact solve fails (86, 127,
   261).
7. **`conservative` is the right variant.** `fewest` adds a group merge or two and, at
   $n = 129$, costs a quarter of the four-side squares and the one-to-one identity.

## Comparison Matrix

| Criterion | Axis components (`regularize_axis_components/2`) | Evan Daniel’s certificate alone | Evan Daniel + same-side re-solve (recommended) | `fewest` variant | Number-field views |
| --- | --- | --- | --- | --- | --- |
| Side of the drawing | The witness’s, exactly | Dilated, $S^{\ast}(1 + 10^{-20})$ | The witness’s, exactly, where rotations stay rational | As either | The exact optimum |
| Near-axis tilts and slack | Straightens within $10^{-4}$ rad, slides one axis at a time | Fixed by the LP and merges | Fixed | Fixed | Fixed |
| Tilted bands and hue classes | Untouched | Merged | Merged, same side | Merged further | Merged |
| Symmetry | None imposed | Imposed where feasible | Kept from the view | Kept | Kept |
| Decimal witnesses | Refuses 73 | Reaches all | Reaches those whose printed side is not truncated | As left | Reaches the Göbel family |
| Non-regression | Measured per square | Not measured | Measured, by the driver | Measured | To be measured |
| Identity | Same squares by construction | Sampled path test upstream | Measured one to one | Fails at 129 | To be measured |
| Cost for 1..324 | About 800 CPU-s | 3 to 4 CPU-h | 13.7 CPU-h, measured | Similar | Not built |
| Status | In the layer (68 views) | T-146’s fifteen | Full run, 12 October 2026 | Measured | think-yk2h |

## Options Considered

### Option A: Keep the Axis Tool Only

**Description:** the status quo; regularize only straight squares and slack.

**Pros:** sound by construction; already gated; cheap.

**Cons:** leaves every tilted band’s hue noise, imposes no symmetry, and cannot touch
the 73 refused decimal records; at $n = 206$ it leaves 42 of 44 angle classes.

### Option B: Evan Daniel’s Regularizer Through the Same-Side Re-Solve

**Description:** the vendored generator (`conservative`, `coincide`, source orientation)
on the KKT point, each view re-solved over $\mathbb{Q}$ at the witness’s side, decided
on the maintained exact routes, measured, and classified; the axis tool kept as fallback
and as the non-regression reference.

**Pros:** reaches tilted structure and hue classes at the record’s exact side; every
view is exact and verified here; identity and shading are measured, not asserted.

**Cons:** 13.7 CPU-hours for a full run, measured; same side is impossible at
Göbel-family decimals; at counts where the witness is not at its optimum the re-solve
moves the packing and the view lands below the bound instead.

### Option C: Draw Evan Daniel’s Certificates As They Are

**Description:** admit the dilated certificates as drawings.

**Pros:** every count gets a view; no re-solve.

**Cons:** reverses the 2 October ruling; a dilated side certifies something the register
does not say, except where it equals the bound exactly.

### Eliminated Options

- **Loosening the renderer’s tolerance:** reaches only the precision band (65 squares
  atlas-wide) and makes the drawing lie about contacts.
- **Hand-editing coordinates:** the policy forbids it; every pose comes from a generator
  and an exact re-solve.
- **`fewest` as the default:** measured above; alternates only.

## Recommendations

Adopt Option B as the standard procedure for every result, with four amendments to the
policy and two changes to the record made first.
The owner answered each on 12 October 2026: “q1 yes / q2 send to review yes, for
trickier cases we can go to review in general / q3 yes / q4 as we do currently / q5 as
recommended / q6 yes regularize and correct always”.
The policy records the answers in its section 9, and `devtools.regularize_evand` applies
them; how each recommendation was decided follows it below.

**Settle the record before the full run.**

1. **Adopt registered refinements as the atlas witnesses** where the register already
   holds a lower exact side than the case record (T-146 at 15 counts, and any import in
   flight, such as #476 at 267). Then the run regularizes the credited packing at its
   own side instead of rediscovering it; at 70, 102, 129 and 146 the same-side re-solve
   should then succeed, which the next pilot must confirm.
   *Decided:* as recommended, after the case-record rewrite (#403), RG-7 custody and the
   imports in flight (think-cb34).
2. **Register the exact packings at the printed sides in one batch.** Wherever the
   same-side view is exact at a witness’s printed side and that side is below the
   verified bound (37, 87, 101, 200 and 260 in the pilots; 17 waits on the $n = 17$
   intake hold, think-x4v4), one register result with a `regularizations` item per count
   closes the gap between reported and verified and lets the drawings in.
   This is owner question 3 in its current, much smaller form.
   *Decided:* register and correct always, in batches, every exact view below the bound
   (think-omqv).

**Amend the decision table** (policy section 4):

3. **Row 4:** a view whose exact side equals the verified upper bound is admissible as a
   drawing (relation `bound`), since it certifies exactly what the register holds.
   This admits $n = 206$ and every T-098 or T-101 count where the regularizer reproduces
   the certified side. *Decided:* yes; `bound` is decided by rows 5 to 10, and a
   `regularizations` item writes it `solved`, the register’s term.
4. **Row 7:** when per-square counts fall but neither rule’s totals fall (no fewer
   four-side squares, no more light squares), send the view to review instead of
   refusing it. Keep refusal when a total falls.
   *Decided:* yes, and more generally the trickier cases go to review: row 6 (no
   one-to-one pairing, an unnamed turn) does too.
5. **Row 5:** a view within $10^{-9}$ of the witness with no square turned is
   `unchanged`, so a $10^{-33}$ difference ($n = 11$) does not create a file.
   *Decided:* as now. A view that changes nothing visible is reported as no change and
   writes no file, whatever row matched, so the tolerance is not needed.
6. **Question 1:** `conservative` only, as the policy already defaults.
   *Decided:* yes.

**Run it in three batches** (1–108, 109–216, 217–324), each with its receipt, its
gallery and a review record per decision, as the epic’s plan already says.
The automated pass admits row 10; the reviewer sees rows 6 to 9 where they send a view
to review, and the gallery’s flagged tie-breaks.
Where both generators admit a view, keep Evan Daniel’s and record the axis tool’s beside
it.

**Leave alone, deliberately:** the Göbel-family decimal records and $n = 51$, which are
already regular in the drawings and need a number field to be framed exactly
(think-yk2h); and the counts where the exact solve fails (86, 127, 261), where the axis
tool’s view or the witness stands.

**Effort.** About 7 CPU-hours for all 324 counts by a fit to the 25 pilot counts (cost
grows roughly as $n^{2.3}$; the exact solve dominates and has a heavy tail: 801 s at
$n = 260$), so 2 to 3 hours of wall time at three or four workers, mostly in the third
batch. Review: if a tenth to a fifth of counts reach the queue, 30 to 60 gallery entries
for the owner, a few minutes each.
*Measured* in the full run: 13.7 CPU-hours and 3.8 hours of wall time at four workers,
and 13 counts in the review queue, 14 after the tolerance re-run.

## Next Steps

- [x] Owner: answer the amendments and the two record changes above (think-pn0e;
  answered 12 October 2026).
- [ ] Adopt the register’s lower exact certificates as the atlas witnesses (think-cb34).
  #518 adopted them at 42 counts, T-146’s among them, and merged on 12 October 2026,
  after the full pass had run on the witnesses before it; since a changed witness lapses
  every review, those counts are run again (below).
- [x] Register the exact packings at printed sides in one batch (think-omqv): T-155 on
  #549.
- [x] Amend the policy’s decision table, then teach `devtools.regularize_evand.classify`
  the amendments (think-up3h): the policy on #497, the driver on #511.
- [x] The index contract for every generator (think-k35c), then the admission batches
  (think-ux1v): #548 and #549. Review records for the review queue remain.
- [ ] Give `arrangement_gap` a spatial index; it took 72 s of 553 at $n = 292$
  (think-fkmn).
- [x] Record every regularization the project makes with the packing’s provenance, in
  the register’s `regularizations` terms (owner, 11 October 2026): the layer’s v2 index
  and the register’s `regularized_drawings` block (#548).
- [x] A pass for axis regions that closes free slack and straightens near-axis squares
  at the record’s side where the exact solve gives no view or leaves the grid noisy
  (302, 303 and others; owner, 12 October 2026): `devtools.regularize_grid_slack`
  (#530). The owner confirms it as the third generator and chooses its threshold (0.5 or
  5 degrees; think-0mq7).
- [ ] Re-run the 42 counts whose witnesses #518 changed, before any admission there
  (think-cb34, think-ux1v).
- [x] Settle #515, a parallel implementation of this layer, with the owner: closed
  unmerged on 12 October 2026, its rotation tolerance and fixes ported to #511 in
  f0371b68d.
- [ ] After the full run: an explainer paper in the project’s own format, rendered by
  kpress like the $n = 11$ lower-bounds explainer, citing Evan Daniel’s work and
  summarizing this project’s changes with before/after figures (think-scua).

## Methodology

The record’s history comes from a read of the atlas README, X-049, the regularized
index, the reviews of T-098 and T-146, the assessment, the policy, Evan Daniel’s method
log and the beads of epics think-los0 and think-cdud, with every count checked against
the files. The spikes ran `devtools.regularize_evand` at the vendored pin on this host
(four cores, shared), outputs kept outside the repository; the gallery was rendered from
them with `devtools.regularize_gallery`. The cost fit is a least-squares line in log-log
over the 21 pilot counts with $n \ge 26$; it is an estimate, and the full run of 12
October measured the cost by `resource.getrusage` per count, children included.

## References

- [Regularization policy](../policies/regularization-policy.md): the obligations and the
  decision table, amended on 12 October 2026 as this document recommended.
- [Assessment of Evan Daniel’s process](research-2026-10-11-evand-regularization-assessment.md):
  how upstream works, and the adaptation plan these tools carry out.
- [Atlas README, “The regularized views”](../../../packing/atlas/known-best/README.md#the-regularized-views):
  the layer and the 2 October ruling.
- [X-049](../../../packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md):
  why grid squares render light, and the axis tool.
- [Review of T-146](../reviews/review-2026-10-10-evand-regularized-certificates.md): the
  first regularizations the register carries.
- [Evan Daniel’s `search/regularize`](https://github.com/evand/square-packing/tree/675a5eaa8712542daac8b4515b0f69ad7044df44/search/regularize)
  (MIT), vendored under `vendor/evand-regularize/`.
- The tools: `packing/devtools/regularize_evand.py`, `regularize_same_side.py`,
  `regularize_gallery.py`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
