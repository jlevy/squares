# Regularization Policy

A **regularization** redraws a packing the record already holds so that it reads
cleanly: near-axis squares straightened, contacts closed, sub-blocks aligned, symmetric
where the packing allows it.
This policy governs every regularized drawing and every regularization the register
records, whichever generator made it: this project’s `regularize_axis_components/2`,
Evan Daniel’s regularizer as vendored here, or a reviewed adjustment of either.
It says what a regularized view must satisfy, what the automated pass decides by itself,
what a reviewer decides, and how each decision is recorded and credited.

Neighbouring documents own the rest.
[`epistemics.md`](../../../epistemics.md#parallel-projects-and-their-credit) owns credit
and the rungs; the
[atlas README](../../../packing/atlas/known-best/README.md#the-regularized-views)
describes the layer and how to rebuild it;
[`development.md`](../../../development.md#the-deep-gate-the-deferred-surface-before-the-merge)
places the gates; and the
[assessment of Evan Daniel’s process](../research/research-2026-10-11-evand-regularization-assessment.md)
is the evidence behind the rules below.

## 1. Purpose and Scope

Regularization is for drawings.
It never changes a side, a frontier value, an evidence tier or a credit under a
drawing’s name.
A drawing made from a regularized view carries the record’s tier from the
source witness, never the view’s own verification, and the view never replaces the
witness.

A run produces two kinds of output, and they take different paths:

| Output | What it is | Where it lives | Path in |
| --- | --- | --- | --- |
| **Regularized view** | An exact packing of the credited arrangement at the side the record already states | `packing/atlas/known-best/regularized/` and its `index.json`; the atlas and site drawings made from it | The automated pass ([section 4](#4-the-automated-pass)), then review ([section 5](#5-manual-review-and-adjustment)) |
| **Register result** | An exact certificate whose side is below the case’s verified upper bound: a new verified upper bound, however it was made | An entry in [`results.yaml`](../../../packing/frontier/results.yaml) with one `regularizations` item per count | The [import runbook’s](../../../packing/campaign/result-import.md#stage-3-record) record and validate stages, as `T-146` took |

A certificate that proves more than the record holds is registered as a result first,
and its drawing enters the layer only after that.

## 2. Definitions

| Term | Meaning |
| --- | --- |
| Source witness | The atlas witness `packing/witnesses/known-best/n-NNN.yaml` a view is derived from |
| $s_W$ | The source witness’s side: its exact side, or for a decimal witness the printed side of its stated rational promotion, the 36-digit pose at dilation 1 |
| $U$ | The case’s verified upper bound when the view is decided |
| $s_V$ | The view’s exact certified side |
| Generator | The code that made a view: `regularize_axis_components/2` in `packing/devtools/regularize_axis_components.py`, or Evan Daniel’s exact solver and regularizer vendored under `vendor/evand-regularize/`, driven by `packing/devtools/regularize_evand.py` and brought to the witness’s side by `packing/devtools/regularize_same_side.py`. A generator’s version is its own version, or for the vendored code the pin plus its ordered local patches. |
| `same` | Side relation: $s_V = s_W$ exactly, in the witness’s frame or a recorded isometry of it |
| `bound` | Side relation: $s_V = U$ exactly, where that is not $s_W$. The view certifies exactly the side the register already verifies, so it is a drawing frame (owner, 12 October 2026); at $n = 206$, $U$ is the side of Evan Daniel’s exact solve of the same packing (T-098), and the regularized certificate reproduces it. A `regularizations` item, whose `side` knows `same` and `solved`, writes it `solved`: the view was solved to that side |
| `solved` | Side relation: any other exact side, including Evan Daniel’s certificate, which scales the solved point by $1 + 10^{-20}$ and rounds the side up. Never written as `same` or `bound`. |
| Identity | Whether the view is still the credited packing, measured by `arrangement_gap` in `packing/devtools/check_half_angle_area.py` between view and source witness under the best of the box’s eight symmetries: `one_to_one`, `moved` (beyond $10^{-3}$), `max_move` and `max_turn_deg`, recorded as `identity: {basis: measured, measured_in, …}` in the register’s terms |
| Non-regression | No square’s contact count falls under the house rule (gap $2 \times 10^{-6}$) or the stage rule (gap $0.01$, half a degree), as `census_atlas_contact_shades.witness_shades` measures it |
| Free square | A square with no load-bearing contact in the exact solve: a rattler, or a force-free square |
| Level | Evan Daniel’s classification of a run, recorded as his: 0, nothing moved; 1, only free squares touched; 2, the same packing by his sampled path test; 3, that test blocked. It informs review and decides nothing. |
| Alternate | An arrangement at the record’s side that this project does not draw as the credited packing |

## 3. Admission Obligations

A view enters the drawing layer only if every obligation holds.
They are checked in this order, and the first that fails is the refusal the index
records.

1. **Exact validity.** The retained view is decided valid over $\mathbb{Q}$ by both
   maintained exact routes, `sqpack.witness.exact_verify` and the independent checker
   `packing/devtools/check_rational_witness_independent.py`; a view converted from Evan
   Daniel’s format is also decided by the third route, `check_half_angle_area.py`. His
   own checkers may be replayed as evidence about the source and never decide.
   A view that two routes here cannot decide, such as a pose over a number field today,
   is not admitted. The index’s digest binds the verdict to the view’s bytes.
2. **Side relation.** $s_V$ is computed exactly and the relation recorded.
   A drawing needs `same` or `bound`, and $s_V \ge U$. A view with $s_V < U$ is
   registered as a result first and drawn after (owner, 12 October 2026: “regularize and
   correct always”), and a `solved` view with $s_V > U$ is not a drawing frame
   ([the decision table](#the-decision-table)). Where the witness’s side is above $U$
   and a view at the bound exists, that view is the one decided and drawn, and the
   same-side view is set aside with its measurements (owner, 13 October 2026: a valid
   view has “equal or smaller side”).
3. **Identity.** Measured and recorded for every view, from every generator: the
   one-to-one pairing with the witness, each square turned by more than $10^{-6}$ (as a
   sine) that the run’s recorded angle changes do not name, and the largest move.
   A changed pose no longer stops a view (owner, 13 October 2026: “the pose doesn’t
   matter if it changes as long as it’s optimal and conforms with our regularization
   guidelines”): a view without the pairing, with an unnamed turn or with a move over
   $1/2$ is admitted when every other obligation holds, and the reason it is admitted
   with names the change.
4. **Non-regression.** Neither the house nor the stage total of shared sides falls,
   against the source witness or against the admitted view it would replace.
   A view in which some square’s count falls while neither total does goes to review
   (owner, 12 October 2026).
5. **Labelling.** The index entry says `label: regularized`, the view’s id ends in
   `-regularized`, the drawing’s title and description say “regularized”, the container
   drawn is the view’s certified side, and the credit line of [section 7](#7-credit) is
   carried.
6. **Provenance.** The index entry names the generator and its version; the method and
   every parameter that differs from the generator’s defaults; the inputs by digest (the
   source witness and, for the vendored generator, the exact-solve input); the run
   receipt; the review record, if any; and the measurements of obligations 2 to 4. The
   index header cites this policy.

**The move bound is a measurement, not a gate.** Until 13 October 2026 a move over $1/2$
sent a view to review.
The bound came from the fifteen views `T-146` measured, where no view that paired one to
one moved a square more than $0.496$ and each of the three that did not needed a move of
at least $0.589$, and from the then layer’s largest move, $0.421$ at $n = 181$. It is
still measured and named, and decides nothing.

## 4. The Automated Pass

### What Runs

| Stage | Tool | Default |
| --- | --- | --- |
| 1. Input | `regularize_evand.py` writes each witness as the generator’s text input | Full precision: a rational witness printed exactly, never reduced to binary64 |
| 2. Exact solve | The vendored exact solver, through the driver | 80 digits and a timeout per count; a count that will not certify is reported, never polished |
| 3. Regularize | The vendored regularizer, through the driver | `conservative`, `coincide` placement, the source orientation |
| 4. Import | The driver converts each certificate to a rational Witness/v2 view | Decided on three routes; identity and shades measured |
| 5. Same side | `regularize_same_side.py` re-solves the view’s tight contacts over $\mathbb{Q}$ at $s_W$ | Wherever every rotation in the view is rational in the witness’s frame |
| 6. Reference | `regularize_axis_components/2` | Unchanged: the fallback, and the reference for non-regression |
| 7. Classify | The driver applies the table below | Index entries, the review queue, the candidate list and the receipt |

The generator runs on request, never as a gate ([section 8](#8-gates)). Every run writes
a receipt: the generator version, the interpreter, each count’s status, sides and
seconds, and the run’s cost.
The [regularization process](../guides/regularization-process.md) gives the commands
that run the generators, choose one view per count and admit it.

### The Decision Table

A count can yield two outputs, each classified on its own: the vendored generator’s
certificate at its own side, and, where stage 5 succeeds, a same-side view at $s_W$. The
first row that matches decides.

| Row | Measured outcome | Decision | Index record |
| --- | --- | --- | --- |
| 1 | No output: no valid certificate, an infeasible start, a stall or a timeout | Refuse; the current view or the witness stands | `refused`, `generator-failed`, with the status |
| 2 | A route here refuses the output | Refuse, and open a defect bead | `refused`, `invalid` |
| 3 | $s_V < U$, under any relation | Register first: a result through the import runbook, in batches, with its identity measured for its `regularizations` item; drawn once registered | None; the receipt lists it |
| 4 | `solved`, $s_V > U$ | Not a drawing frame | None, `dilated-side` |
| 5 | `same` or `bound`, and the view’s pose equals the witness’s exactly | No view | `unchanged` |
| 6 | Retired 13 October 2026: a view not one to one, or with a turn the recorded angle changes do not name, goes on to rows 7 to 10, the change named | None | None |
| 7 | `same` or `bound`, a square’s house or stage count falls against the witness or the view it would replace | Refuse when a house or stage total falls; review when neither does | `refused`, `regression`, or the review queue |
| 8 | `same` or `bound`, variant `fewest` with a merge of determined groups, or level 3 | Alternate: review only, never drawn as the packing | Review queue |
| 9 | Retired 13 October 2026: a move over $1/2$ goes on to row 10, named | None | None |
| 10 | `same` or `bound`, no regression, `conservative`, level 2 or below | Admit, naming any change of pose | `regularized` |

Row 10 is the only automatic admission.
Rows 6 and 7 were refusals until the owner’s answers of 12 October 2026: a case the
rules cannot settle goes to review, and only an exact route’s refusal or a fall in a
total refuses. Rows 6 and 9 were retired by the owner’s answers of 13 October 2026: the
pose may change, so only rows 7 and 8 still send a view to a person.
Views from `regularize_axis_components/2` are classified by the same table; having no
variant or level, they meet row 10’s last two conditions by construction.
A view in the review queue is not drawn until a review record admits it.

**How a decision is reported** (owner, 11 October 2026). “Refused” is kept for a view
that would change the drawing and fails an obligation.
A run reports every count in one of these words, in this order of precedence:

| Reported as | When | Rows |
| --- | --- | --- |
| **no view** | The generator produced nothing to judge; the witness or the current view stands | 1 |
| **no change** | The view would draw the same picture: no square moves beyond $10^{-3}$ or turns, and the angle classes and the house contact counts are the source’s. Whatever its side relation, nothing is drawn differently, so there is nothing to refuse; a side below $U$ is still listed as a register-result candidate in the receipt | 3 to 7 and 10, when nothing visible changes; 5 |
| **refused** | The view changes the drawing and an exact route refuses it (2), or a house or stage total falls (7) | 2, 7 |
| **held** | The view changes the drawing, passes every route, and waits on the record: a register result first (3) or a side the record does not hold (4); the reason is shown with it | 3, 4 |
| **review** or **alternate** | A square loses a contact while no total falls (7), or as row 8 says | 7, 8 |
| **admitted** | Row 10 | 10 |

This changes how decisions are worded, not what is drawn: only an admitted view, or a
reviewed one, enters the layer.

Two kinds of admitted view are listed first in the gallery for the reviewer:

- **A tie-break of taste:** the generator dropped a symmetry for a coincidence, fell
  back from its coincidence placement, or reported an optimum that is not unique.
- **Two candidates:** both generators yield an admissible view.
  The vendored generator’s view is kept, and the project’s is recorded beside it as the
  reference.

## 5. Manual Review and Adjustment

**Who reviews:** the owner, or a person the owner names in writing as the layer’s
reviewer. An agent prepares the gallery and may draft a recommendation, and the review
record names the person who decided: the rule
[No Blind Trust](../../../epistemics.md#no-blind-trust) sets for the rungs, evidence
from an agent and the decision from a person.

**What the reviewer sees:** a gallery the driver renders for each pass.
For each count in the review queue or flagged, it draws the source witness and the view
side by side with the house renderer at one scale and orientation, and gives the side
relation and $s_V - s_W$; the identity measurements; each square’s house and stage
counts before and after, with changed squares marked; the generator, variant, level and
recorded angle changes; any symmetry imposed or dropped; and the other generator’s view,
where there is one.

**What a reviewer may decide:**

| Decision | How it is made reproducible |
| --- | --- |
| Admit a row 8 alternate | Only once question 2 is answered yes, and then labelled an alternate, never the credited packing |
| Choose symmetry or contact, attached or separate sub-blocks, or a placement style | A per-count generator parameter in the review record, which the driver reads on every later run |
| Choose an orientation | A recorded isometry of the witness’s frame, as `devtools/atlas_orientation.py` records them |
| Choose between the two generators | A per-count choice in the review record |
| Reject a view | The review record; the previous view or the witness stands |
| Change how the generator works | A reviewed patch ([section 6](#6-forking-the-vendored-generator)) |

**What a reviewer may not do:**

- Edit a view’s coordinates or angles by hand.
  Every pose comes from a generator run and, for `same`, from the exact re-solve.
- Admit a view that fails any obligation of [section 3](#3-admission-obligations), or
  override rows 1 to 7.
- Change a side, a tier or a credit.
- Draw an alternate as the credited packing.

**The review record:** each decision is to be one record in
`packing/atlas/known-best/regularized/reviews.yaml`, a hand-written input beside the
index.
A record holds the count, the date, the reviewer, the decision and its reason; any
parameters or generator choice; the generator version and source-witness digest it was
made against; and the gallery it was made from.
The index entry will name its record, and a records-tier check will hold the two to each
other. Neither the file nor the check exists yet: the first review creates both, and
until then no view rests on a review record.
A review of a whole pass may also be written up under `docs/project/reviews/` and mapped
in the document map.

**Re-review:** a record lapses, and its count goes back through the automated pass, when

- the source witness changes, by a new record at the count or a corrected witness;
- the vendored generator is re-pinned or patched, or the project’s generator changes
  version;
- this policy changes an obligation or a threshold; or
- an owner answer to an open question bears on the count.

A lapsed adjustment is re-applied only if its parameters still produce a view that meets
every obligation, and the reviewer confirms it in a new record.

## 6. Forking the Vendored Generator

Evan Daniel’s exact solver and regularizer, `search/exact` and `search/regularize` in
[evand/square-packing](https://github.com/evand/square-packing), are MIT-licensed and
vendored under `vendor/evand-regularize/` at the pin its manifest `vendored.yaml`
records, with his licence notice kept.
The project may patch them, on four conditions:

- **A patch is a recorded, reviewed local change.** The manifest’s `local_changes` lists
  each one (the path, the kind of change, the date, the bead and the reason), the
  vendored README describes it under Local Changes, and the review that accepted it is
  the pull request that made it, so the unpatched pin can always be rebuilt.
  `devtools.check_vendored_evand` holds the tree to the manifest.
  An unrecorded edit under the vendored tree is a defect.
- **The version travels with the view.** A patched generator’s version is the pin plus
  its ordered local changes, and every view and receipt it produces carries that
  version.
- **A patch changes how views are made, not what admits them.** Section 3 applies
  unchanged, and every view a patch could change goes back through the pass with its
  review records lapsed.
- **Credit stays with the method.** A view made by the vendored code, patched or not, or
  by a port of it, credits Evan Daniel’s method ([section 7](#7-credit)).

A patch that fixes a defect in the upstream code is reported to its author, as
[`epistemics.md`](../../../epistemics.md#parallel-projects-and-their-credit) asks of
every defect found here.

## 7. Credit

| Whose work | How it is credited |
| --- | --- |
| The packing’s finder | Keeps the packing’s credit through the register result that holds it, which a regularization names as `of`. A regularized drawing keeps the finder’s citation line. |
| The regularization | `by: project`, with `method` naming the generator and variant, for this project’s runs; another regularizer’s bibliography key for theirs, as `T-146` credits Evan Daniel’s lists |
| Evan Daniel’s method | Whenever his generator or a derivative made the view: `method` names it (“Evan Daniel’s regularizer, `conservative`, `coincide`”); the index and every drawing made from the view carry the line *Regularized by the Squares Project with Evan Daniel’s regularizer (evand/square-packing, MIT)*; and a register result is credited `Levy after Daniel` through `builds_on`, which cites a bibliography key for the vendored code |
| This project’s tool | `by: project`, `method: regularize_axis_components/2`, credited as the Squares Project |
| This project’s modifications to his regularizer | Named beside his credit wherever his regularizer or the grid-slack port of his placement made the view, as `modifications`: the retry rungs its solve climbed (`dps-100`, `force-kkt`, the `first-pass` shim), the vendored copy’s patches its `method` names (the replica patch `probe-flat-stall-stop`), and the exact re-solve that brought it to the witness’s side (`devtools.regularize_same_side`); a grid-slack view is this project’s port of his coincidence placement (`regularize_grid_slack`), not his code. Where none applied the record says *unmodified* |

The record states a regularization as the same packing in its own voice only where the
identity basis is `measured`. A regularization taken in from elsewhere states its
identity as its source’s claim until a measurement here decides it.

The owner asked on 13 October 2026: “If we’re using our own modifications to Evan
Daniel’s regularizer, we should note that as well.”
Each drawn view’s item in `results.yaml`’s `regularized_drawings` and its case record’s
`regularization` note (question 16) name them, read by `devtools.regularized_drawings`
from the view’s index entry alone: the rungs from `run.rungs`, or before the retry
ladder from `run.retried_with`, and the patches from `method`. A view admitted after the
ladder and before `run.rungs` existed has its rungs recorded from its run’s reports by
`python -m devtools.regularize_evand rungs`, which writes them only where a report
reproduces the drawn view byte for byte, never over rungs or a retry already recorded,
and names the run that supplied them as `run.rungs_from`. A registered result’s own
regularization (`by: project` in its `regularizations`, as `T-155`’s 59 are) names them
too, written by the same tool from the item’s `method` and `side`: the patches and the
same-side re-solve.
An item records no solve, and `T-155`’s selection kept none while its
runs’ reports are not retained, so its items say in `modifications_unrecorded` that
whether the solve climbed a retry rung is not recorded, rather than reading as
*unmodified*. Where the layer draws that very solve, the item reads the rungs from the
drawn entry instead and records nothing as unrecorded, so the register and the drawing
read one solve one way: the result registers the drawing itself, and its registration
receipt (`T-155`’s `selection.json`) names, at that count, a run whose receipt the
entry’s run block records, with the entry’s output and exact side.
At fourteen counts `T-155`’s certificate is the full run’s view the layer draws, which
ran no retry, so its item reads *unmodified* or names the same-side re-solve alone.
At 87 the layer draws a later run’s view at the same side, which says nothing of the
solve `T-155` registered, so its item still says the rungs are not recorded.

## 8. Gates

The generator costs about three to four CPU-hours for $n = 1..324$, far above any
routine gate’s wall ceiling.
So it runs on request with a receipt, and the gates hold the decisions it produced
([OR-13](../../../operating-rules.md#or-13-every-fast-check-runs-in-ci-only-the-unavoidably-slow-ones-leave),
[OR-17](../../../operating-rules.md#or-17-every-routine-gate-has-a-wall-ceiling-and-anything-above-it-is-selected-on-purpose)).

| Check | What it holds | Where it runs |
| --- | --- | --- |
| `regularized atlas views match their index` | The index against the manifest, the witnesses and the views, by digest; with the layer’s contract, also the generator, method, side relation, identity and review-record fields; every drawn view’s exact side against $s_W$ and against the case record’s $U$, decided exactly, with the views above $U$ named in `ABOVE_U` | Records tier, every pull request |
| `regularized atlas drawings match their index` | Every drawing re-rendered from its retained view | Records tier, every pull request |
| `default pictures improve on their house drawings` | Every drawn view measured against its house drawing again, each count’s default picture decided under the improvement rule ([section 11](#11-the-improvement-rule)) and held to `default-drawings.json` | Records tier, every pull request |
| `results rungs are earned and the view agrees` | `devtools.check_results` on each register result’s `regularizations` items, and on `regularized_drawings` and every case record’s `regularization` note against the layer’s index | Records tier, every pull request |
| `regularized atlas views re-derive exactly` | Every `regularize_axis_components/2` view re-derived byte for byte; every other generator’s view decided again over $\mathbb{Q}$ on the maintained routes, its square count, identity and shades re-measured and its digests held | Deferred: the `regularized-views` job, whose 450 s ceiling bead think-uomm revisits |
| The generator run | The views reproduced from the pinned code and inputs | On request only, with a receipt |

## 9. Owner Decisions

The assessment’s eight
[open questions](../research/research-2026-10-11-evand-regularization-assessment.md#open-owner-questions),
the four the pilots of 11 October 2026 raised, the three the owner settled on 13 October
2026 after the stack’s re-posed views were audited, and the owner’s rule of the same day
on credit and results, each with its answer or, where none is recorded, the default the
policy applies until there is one.

1. **Variant:** `conservative` only; `fewest` is not run.
   *Answered by the owner on 12 October 2026:* yes.
   At $n = 129$ `fewest` lost 26 of 79 four-side squares and the one-to-one pairing.

2. **A `fewest` merge of determined groups as the same packing:** no.
   Such views are alternates (row 8) and are not admitted.

3. **Exact views below the verified bound:** *answered by the owner on 12 October 2026,
   “regularize and correct always”:* every such view is registered as a result through
   the import runbook, in batches with a `regularizations` item per count, and drawn
   once registered (row 3). The first batch is the exact packings at the decimal
   witnesses’ printed sides, about $10^{-14}$ below bounds rounded up at fourteen
   decimals.

4. **Irrational optima:** the status quo.
   A dilated certificate is not a drawing frame (row 4), and views over a number field
   are a follow-up, $\mathbb{Q}(\sqrt{2})$ first; $n = 11$, whose proved optimum lies in
   a field of degree 8, stays drawn from its witness.

5. **Orientation:** the source’s; any isometry is recorded as `atlas_orientation`
   records one.

6. **Tie-breaks of taste:** the generator’s defaults, flagged in the gallery for the
   reviewer.

7. **Method credit:** the owner directed on 11 October 2026 that the vendored code be
   properly credited, so its notice and the vendored README carry Evan Daniel’s credit.
   Until the owner says where else, the index, the drawings and a register result’s
   `builds_on` carry it as [section 7](#7-credit) states.
   Since the regularized view became the default picture
   ([section 12](#12-the-default-picture)), the composites carry it too, and so does the
   case page that draws one; the atlas README names it in its account of the layer.
   Both composites print the owner’s approved two-line wording:

   ```text
   Drawn packings are regularized for cleaner display using Squares Project rules,
   based on Daniel’s regularizer
   ```

   Their SVG metadata retains the full generator credits in `data-generator-credits` and
   the depicted regularized cases in `data-regularized-cases`. The compact printed
   credit does not replace that attribution.

8. **Retention of the solve:** kept.
   The solved points and contact structures go in a pinned packet or release asset
   outside Git
   ([OR-18](../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)),
   named by digest in the receipt: they can be discarded later, and a discard cannot be
   undone.

9. **A view at exactly the verified bound:** *answered by the owner on 12 October 2026:*
   admitted, as the side relation `bound` (rows 5 to 10). It certifies exactly what the
   register holds.

10. **Cases the rules cannot settle:** *answered by the owner on 12 October 2026:* they
    go to review, not to refusal.
    Row 7 sends a view to review unless a total of shared sides falls, as row 6 did
    until question 14 retired it; only an exact route’s refusal or a falling total
    refuses.

11. **A view that changes nothing visible:** *answered by the owner on 12 October 2026:*
    as now. It is reported as no change and no file is written for it.

12. **Registered refinements the case records have not adopted:** *answered by the owner
    on 12 October 2026, as recommended:* the register’s lower exact certificates
    (`T-146` at its fifteen counts first) become the atlas witnesses before their counts
    are admitted, once the case-record rewrite (#403) and `T-146`’s custody item allow,
    and after the imports in flight at the same counts land.
    A view derived from a witness that later changes is re-reviewed (section 5). The
    intake’s #518, merged on 12 October 2026, adopted these houses on the case records
    directly, citing an owner decision of 11 October 2026 not to wait for #403; #559
    regularizes its 42 counts again on the new witnesses.

13. **What a valid view is:** *answered by the owner on 13 October 2026:* “valid means a
    valid packing with equal or smaller side”, “with exact verification”, where the side
    is “optimal as best as known”.
    A view is valid when both maintained exact routes accept it and its side is at most
    $U$. A same-side view above $U$ gives way to a view at the bound where the solve
    reached it (obligation 2), and the grid-slack generator tries a rational $U$ first
    wherever the witness’s side is above it.
    A view at a side below $U$ is a new result and is registered, as question 3
    answered. Seven drawn views sit above $U$ and stay, by name, until a view at $U$
    draws as well. At 18, 26, 66 and 85 Evan Daniel’s views are rationals about
    $10^{-30}$ above a closed-form optimum, the status quo of question 4. At 110, 241
    and 297 the drawing is at Francisco Couzo’s decimal side, $3 \times 10^{-12}$ to
    $1.3 \times 10^{-11}$ above Evan Daniel’s exact optimum: the view at $U$ draws fewer
    shared sides at 110 and 241 (bead think-jnso) and goes to the owner at row 7 at 297.
    `packing/tests/test_regularize_select.py` reads every drawn view’s side against $U$
    and fails on a view above it at any other count, and on a listed count once it is
    drawn at $U$.

14. **A changed pose:** *answered by the owner on 13 October 2026:* “once things have
    been verified correct, that they are equal or better, we can commit and use them.
    the pose doesn’t matter if it changes as long as it’s optimal and conforms with our
    regularization guidelines.”
    Rows 6 and 9 are retired: no pairing, an unnamed turn or a move over $1/2$ is named
    in the admission’s reason and decides nothing.
    Rows 7 and 8 stand, so a per-square loss of contact still goes to review.
    “Equal or better” is the choice rule of section 10, item 4, now an answer, and since
    the owner’s further answer of the same day it is the improvement rule of
    [section 11](#11-the-improvement-rule), which is stated there and nowhere else: a
    view replaces the drawing only when it improves on it.
    Of the rule’s seven measures, classes and hues joined after a review of #559 found a
    view at 236 that tied the other five and drew one more hue; exactness counts as a
    goal because an exactly verified view at a side no larger than $U$ replaces a
    numerically checked witness (question 15). `devtools.regularize_select` applies the
    rule, and the [regularization process](../guides/regularization-process.md) says how
    a pass runs. The grid-slack generator’s straightening threshold is a per-run setting:
    a view from a run at 1 or 5 degrees is admitted on the same terms as one from the
    default half degree.

15. **Exact verification of every packing:** *answered by the owner on 13 October 2026:*
    “Every packing, even after regularization, should be exactly verified.”
    Every view the layer draws is decided by both exact routes, at admission and again
    by `--verify-atlas`. The packings drawn without a view, and the decimal witnesses
    the case pages draw, are not; the verification gaps review of 13 October 2026
    records them as a serious gap to be filled, as the owner asked.

16. **Credit and results:** *answered by the owner on 13 October 2026:* “can we review
    how we’re doing credits?
    It seems like we should put a note on our frontier records about which ones have
    done regularization and if the regularization is due to us (squares project)”, and
    “Any new upper bounds should also be recorded as results.
    Pure regularization should not be considered a new result, but it is a credited part
    of the frontier record.”
    A pure regularization, one whose exact side is not below $U$ and which so proves no
    new bound, redraws a registered packing and is never a result: it changes no side,
    frontier value, evidence tier or credit, and no register result is made for one.
    It is credited in `results.yaml`’s `regularized_drawings` and on the case record of
    every count the atlas draws regularized.
    The record’s generated `regularization` field says who regularized the drawing
    (`by: project`, with the generator, its credit line and this project’s
    modifications, section 7), at which side relation (`same` or `bound`), which
    registered result holds the packing (`of`, or that none does), and the view’s path.
    Where the drawn regularization is itself registered, as `T-155`’s are at fifteen
    drawn counts, the field names that result (`registered_in`) and the note says the
    exact side is registered in it; the drawing adds no further result.
    `T-155` registers 59 exact sides: 26 are new and prove new upper bounds, and 33
    equal the sides of Evan Daniel’s earlier certificates (`T-101`), which the record
    had carried rounded up and which `T-101`’s replay already proves.
    At those 33, eight of them drawn, the item names `T-101` as `first_certified_in`,
    and the note says that the regularization is the Squares Project’s, that its exact
    side is registered in `T-155`, and that the same side was first certified by Evan
    Daniel’s certificate (`T-101`), so it proves no new bound.
    Where a result registers this project’s own regularization of a count that the atlas
    does not draw, as `T-155` does at 43 counts, or draws by another method, as at 227,
    the field carries it too, after any drawing: in the register’s terms (`method`,
    `side`, `of`, `registered_in`) with the generator its method names, its credit line
    and its modifications, and the note credits the Squares Project and names the
    result, so every record whose count this project regularized says so whether or not
    the view is drawn. Where the house is itself a regularization its source published,
    as `T-146`’s certificates are, the field credits the source first, in the register’s
    terms (`by` its bibliography key, `of` the result whose packing it regularizes,
    `registered_in` the result that registered it).
    `devtools.regularized_drawings` writes it from the layer’s index, its check in the
    records tier holds every case record to the index, and the site’s case page prints
    its note. An exactly verified side below $U$ is always registered as a result however
    it was made (row 3, question 3), as `T-155` registered the exact views below the
    bound. It is a new upper bound only where no earlier certificate already stated that
    side exactly and no larger count’s verified upper bound is at or below it, since
    $s(n) \le s(m)$ for $m > n$. Otherwise the result says that its bound is not new and
    names the result that already proves it: at the 33 of `T-155`’s counts where Evan
    Daniel’s certificate stated the side first, the item names `T-101` as
    `first_certified_in`, and `T-156`, which registered the grid-slack view of $n = 290$
    on 13 October 2026 at the witness’s own side `2.4e-15` below $U$, says that its
    bound follows by monotonicity from `T-155`’s certificate at $n = 291$, at the same
    side. The owner decided on 13 October 2026 to keep `T-156`, to say so, and to keep
    the grid-slack view as the certificate of $n = 290$’s own packing at that side
    (jlevy/squares#587); that view draws no change, so the atlas draws nothing new
    there.

An answer, like any other change to this policy, is an owner decision recorded here with
its date. It replaces the default, and the counts it bears on are re-reviewed.

## 10. Implemented on the Owner’s Standing Instruction, for Confirmation

On 12 October 2026 the owner asked for the work to run “autonomously end-to-end
overnight to make sure that we have regularized versions of everything by the time we’re
done and everything is PR’d and ready to merge”, with “all versions that are regularized
… properly captured in our frontier records”.
The stack implements the choices below under that instruction.
None is an answer to a question of section 9 until the owner confirms it; each is
recorded where it is implemented, and reversing one is a change to that layer.

1. **Rotation matching:** a regularized view’s rotation matches the witness’s within a
   sine of $10^{-9}$, the tolerance of #511’s re-solve, a thousand times below the turn
   threshold of obligation 3 (#511).
2. **Retrying a solve that gives no view,** once per rung and each attempt listed in the
   receipt: a failed solve at 100 digits; a witness not jammed only at noise level with
   upstream’s `--force-kkt`, kept only where the side falls by at most $10^{-10}$; a
   converged solve whose certificate upstream refused, or whose active-set step failed
   after a converged first pass, passed on to the regularizer; a timeout solved again
   with a recorded replica patch that stops upstream’s zero-mode probe at its floor,
   applied outside `vendor/` (#511). The views are decided by this project’s exact
   routes as always.
3. **A third generator:** `regularize_grid_slack`, this project’s port of Evan Daniel’s
   coincidence placement, started from the witness’s exact frame (near-axis squares
   straightened under 0.5 degrees where a placement stays feasible), brought to the
   record’s side by the same exact re-solve, and credited to his method (section 7)
   (#530).
4. **Choosing between generators:** where both yield an admissible view, Evan Daniel’s
   is drawn unless the grid-slack view is better on a measure of the drawing (light,
   uneven or near-axis squares, or a house or stage total) and worse on none (#548). The
   owner confirmed this rule on 13 October 2026, with the measures section 9, question
   14 lists.
5. **The layer’s contract and checks:** every index entry names its generator; the
   records-tier check reads each non-axis view against its entry, and the full tier
   re-derives the axis tool’s views and decides every other view again on both exact
   routes (#548).
6. **The frontier record of a drawing:** each drawn view’s regularization is recorded in
   the register’s terms in `results.yaml`’s generated `regularized_drawings`, `of`
   resolved to the registered result that holds the packing; a count whose packing no
   registered result holds is listed as unregistered (#548). A drawing proves no bound,
   so no register result is made for one.
   The owner confirmed this on 13 October 2026 (section 9, question 16), and each drawn
   count’s case record now carries the same credit in its generated `regularization`
   note.
7. **Registering exact views below the bound** (question 3’s answer, carried out in
   #549): the row 3 views outside the counts #518 and #553 re-housed are registered as
   one batch result, `T-155`, with the case records’ exact forms moved to the registered
   sides and their printed values kept, so no citation weakens.
   Where a registered side is exactly the side of an earlier exact certificate, as it is
   of Evan Daniel’s (T-101) at 33 counts, that bound was already published, and the
   records cite the earlier certificate’s independent replay beside the batch’s.

## 11. The Improvement Rule

The owner, 13 October 2026: “tie is fine on exactness or regularity as long as it is
making some improvement wrt our regularity or heuristic goals”, and “that should be
codified in our regularization standards doc”.
The rule below is that answer.
It decides whether a view is drawn in place of today’s drawing (question 14), and
whether a drawn view is a count’s default picture in place of its house drawing
([section 12](#12-the-default-picture)).

<!-- BEGIN RULE: improvement (devtools.improvement_rule) -->

A view improves on a drawing when it is worse than the drawing on none of the goals and
better on at least one.
Ties on the other goals are fine, and a tie on every goal is no improvement.

- light squares: fewer is better
- uneven squares: fewer is better
- near-axis squares: fewer is better
- angle classes: fewer is better
- hues: fewer is better
- house total of full shared sides: more is better
- stage total of full shared sides: more is better
- exact side: smaller is better
- exactness: exactly verified is better than numerically checked

<!-- END RULE: improvement -->

The marked text is the rule’s one statement: two sentences and its goals, one line each,
with the direction in which each is better.
The first five goals are regularity as the house renderer’s colouring shows it, counted
by `devtools.census_drawing_regularity`; the house and stage totals are the full shared
sides of `regularize_evand.contact_partners`; the exact side is a larger one worse; and
exactness is an exactly verified view against a numerically checked witness.
`devtools.improvement_rule` reads the statement from this file and decides it, and its
readers take it from there: `devtools.regularize_select` prints it in the rule it
reports, and `devtools.default_drawings` prints it with its check.
That check parses the goal lines and compares them with the goals and directions the
code judges, both ways, so a goal added or dropped here, or a direction changed, fails
it until the code agrees.
Every view the layer draws is exactly verified, so exactness is never worse.
A change to the rule is an owner decision recorded here, made to the statement and to
the code together.

## 12. The Default Picture

**Owner decision, 13 October 2026.** Asked “why do we even have ‘house’ on the diagrams?
are there any benefits other than the historic accuracy?
I’d be inclined to make all diagrams just default to regularized ones”, the owner
approved the plan “regularized drawing is the default where one exists; house kept as
‘as published’ on case pages and the toggle; posters redrawn”, adding that “having
original records seems good but it seems like regularization should be a strict
improvement if we’ve done it correctly”.

So a count’s default picture is its regularized view wherever the layer draws one that
is valid and improves on the house drawing:

1. both maintained exact routes accept it, as its index entry records;
2. its exact side is at most $U$, or it is one of the views question 13 names above it;
3. it improves on the house drawing under the rule of
   [section 11](#11-the-improvement-rule), measured as the selection measures a view
   against today’s drawing.

Everywhere else the house drawing is the picture.
That includes a drawn view that ties an exactly verified house drawing on every goal at
its own side, whose picture differs from the house’s by little more than a square’s
small slide, and at most counts by less than a pixel at tile size; the layer keeps such
views, admitted before this rule, and draws none of them by default.

Where the default is the view, the homepage and atlas tiles, the frontier survey’s
thumbnail, both posters and the case page draw it, and the case page keeps the house
drawing one click away as *as published*, with the credit of the source whose packing it
pictures.
The owner’s follow-up on 13 October 2026 adds **Regularized | Original** to the
homepage and atlas page.
Each page starts with Regularized, using the defaults above and the house drawing where
no view passes the improvement rule.
Original shows the current house packing as published, with its source credit.
Switching preserves the tiles and their links, and the drawing choice lasts for that
page only; a new page starts with Regularized.
Without scripts, the default drawings remain available.
Where the layer holds a view that is not the default, the case page’s regularization
note says why it draws the house drawing.
The house witness stays the record’s witness, and the view changes no side, value, tier
or credit (section 1). `devtools.default_drawings` writes each count’s default and its
reason to `packing/atlas/known-best/default-drawings.json`; its check, in the records
tier on every pull request, measures every view against its house drawing again, fails
when the record or a default departs from the rule, and lists the counts that keep the
house picture and why.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
