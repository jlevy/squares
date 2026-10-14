# Regularization Process

This guide takes a regularized drawing from a generator run to a merged pull request:
run the generators, choose one view per count, admit the chosen views into the layer,
record them, validate, and open the pull request.
The [regularization policy](../policies/regularization-policy.md) says what a view must
satisfy ([section 3](../policies/regularization-policy.md#3-admission-obligations)), how
the decision table decides it
([section 4](../policies/regularization-policy.md#4-the-automated-pass)) and what the
owner has settled ([section 9](../policies/regularization-policy.md#9-owner-decisions));
this guide does not restate it.
The [atlas README](../../../packing/atlas/known-best/README.md#the-regularized-views)
describes the layer the views are drawn into.

## What May Be Merged

The owner, 13 October 2026: “As long as things are more regular and at least as good in
terms of efficiency of the packings, then we can merge things.”
A pull request may change a count’s drawing only to a view that

- both maintained exact routes accept, `sqpack.witness.exact_verify` and the independent
  checker (question 15);
- has a side no larger than the verified upper bound $U$ (question 13), and no larger
  than the side today’s drawing is drawn at where that drawing is exactly verified (the
  layer still draws seven views above $U$, at 18, 26, 66, 85, 110, 241 and 297, each an
  exception question 13 names; a pass may replace them, never add to them);
- row 10 of the decision table admits;
- is worse than today’s drawing on none of the seven measures below, and is better on
  one or draws the packing at a smaller side (question 14).

The seven measures are the drawing’s light, uneven and near-axis squares, its distinct
angle classes and its hues, fewer being better, as `devtools.census_drawing_regularity`
counts them from the house renderer’s colouring; and its house and stage totals of full
shared sides, more being better.
Classes and hues catch a square turned a hair off its group: at n = 236 two squares
0.000537 degrees off drew seven hues where today’s drawing has six, while the other five
measures tied.

A change that improves no measure and leaves the side unchanged is not made.
The one exception replaces a drawing that is not exactly verified, a numerically checked
witness, with an exactly verified view at a side no larger than $U$ and worse on no
measure.

Where more than one view of a count passes, the first in this order is drawn: Evan
Daniel’s, then grid-slack’s by rising straightening threshold.
A passing view that another passing view dominates, being worse on some measure and
better on none, is skipped.
`devtools.regularize_select` applies exactly these rules.
A view at row 7 or 8 goes to the owner, and a view below $U$ is registered before it is
drawn; both are described below.

## The Steps

Run every command from `packing/`, each after
`uv run --frozen --all-extras --group dev`. Keep run directories outside the checkout;
the examples use `RUNS=/tmp/regularize`.

### 1. Run the Generators

```bash
python -m devtools.regularize_evand run --run-dir $RUNS/evand --n 87 106 152 --workers 2
python -m devtools.regularize_grid_slack --n 146 176 199 --run-dir $RUNS/grid-0.5
python -m devtools.regularize_grid_slack --n 146 176 199 --run-dir $RUNS/grid-5 \
  --near-axis-degrees 5
```

The driver of Evan Daniel’s regularizer costs three to four CPU-hours over all 324
counts and writes a receipt for each run.
The grid-slack generator takes seconds to a few minutes a count.
Each grid-slack run has one straightening threshold, half a degree by default; run other
thresholds into their own directories, since views from runs at 1 and 5 degrees are
admitted on the same terms.

### 2. Decide Finished Runs Again After a Change

When the decision table changes, or a register result moves $U$, decide a finished
driver run again from its reports.
`reclassify` rewrites the reports in place, so run it on a copy to keep the run as it
was decided, and keep the copy’s directory name, which `layer` records the run by:

```bash
mkdir -p $RUNS/redecided && cp -R $RUNS/evand $RUNS/redecided/evand
python -m devtools.regularize_evand reclassify --run-dir $RUNS/redecided/evand \
  --refresh-bounds
```

The selection needs no such step first: it decides every report as `reclassify` would,
and the commands it prints for step 4 reclassify a copy of any run whose stored reports
are stale.
Grid-slack runs need none: `regularize_grid_slack.decided` decides their views
when they are selected and again when they are admitted.

### 3. Select

```bash
python -m devtools.regularize_select --evand-run $RUNS/evand \
  --grid-run $RUNS/grid-0.5 $RUNS/grid-5 --workers 3 \
  --output $RUNS/selection.json --markdown $RUNS/selection.md
```

Today’s drawing is read from `--tree`, this checkout by default.
The tool decides every view on both exact routes, which takes seconds for a small count
and about four minutes for the largest views (n = 271 at half a degree), so give it the
workers the host has.
It prints the chosen views, the register candidates and the commands for step 4. The
JSON report lists every candidate with its verdicts and the reasons it was not chosen.
A note that a run measured a view against another drawing than the tree’s means the
layer changed after the run; run that count again before admitting it.

### 4. Admit

Run the commands the selection printed, in order and in one shell.
`layer` reads a driver run’s stored reports, so where a stored report differs from the
selection’s decision of it (a run written before a same-side view above $U$ was set
aside, say, which as stored would admit that view), the commands first copy the run into
a scratch directory under its own name and `reclassify` the copy, and admit from the
copy; the run itself is never rewritten.
Then comes one `layer` call for the driver runs, whose `--exclude` leaves out the counts
those runs would admit but were not chosen from them, then one call per grid-slack run,
with an empty `--run-dir`:

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R $RUNS/evand "$copies/0/evand"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/evand" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/evand" --repo-root .. \
  --exclude 110
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. \
  --grid-run $RUNS/grid-5 --grid-counts 146 176
```

Each call writes the views into `packing/atlas/known-best/regularized/` and their
entries into its `index.json`, then runs the layer’s check.

### 5. Render and Record

```bash
python -m devtools.render_regularized_atlas --update
python -m devtools.regularized_drawings
python -m devtools.render_results --update
```

These redraw the views, regenerate `results.yaml`’s `regularized_drawings`, and
regenerate `frontier/RESULTS.md`. Update the layer’s counts in the atlas README’s
regularized-views section by hand.

### 6. Commit, Then Re-pin

Commit the data first, under a `data:` subject whose body names the counts, the runs and
the `layer` commands.
Then write the pin and commit that one line on its own:

```bash
python -m devtools.release_pin --update
git commit -m "release: re-pin DATA_REVISION to <data commit>" src/sqpack/release.py
```

The re-pin subject names the short hash of the data commit it pins.
`release_pin --update` refuses while data changes are uncommitted.

### 7. Validate

```bash
packing-validate --records
python -m devtools.regularize_axis_components --verify-atlas
python -m pytest tests/test_regularize_evand.py tests/test_regularize_grid_slack.py \
  tests/test_regularize_select.py tests/test_regularized_drawings.py \
  tests/test_render_regularized_atlas.py
python -m devtools.release_pin --check
```

`--records` holds the index to the views and witnesses by digest, re-renders the
drawings and checks the register.
`--verify-atlas` decides every drawn view again on both exact routes and takes several
minutes at four workers; CI runs it in the deferred `regularized-views` job.
`test_regularize_select.py` holds every drawn view’s side to $U$, except at the counts
question 13 names.

### 8. Open the Pull Request

Use `tbd shortcut create-or-update-pr-simple`. The description leads with what the
branch cost
([OR-9](../../../operating-rules.md#or-9-a-pull-request-leads-with-what-the-branch-cost)),
then gives the selection’s table, the run directories and the commands, and lists what
goes to the owner. The reviewer reruns the selection from the same runs, or reads its
JSON report, and checks that every drawn view has no refusal.

## The Review Queue

The selection never admits a view that row 7 sends to review (a square’s contact count
falls while no total does) or that row 8 calls an alternate.
List those views in the pull request for the owner.
A driver run draws them for review with

```bash
python -m devtools.regularize_gallery --run-dir $RUNS/evand --output gallery.html \
  --n 232 --with-current-layer
```

and a grid-slack run leaves each view’s `drawing.svg` beside its report.
A view the owner admits is drawn only through a review record, which the policy’s
section 5 describes and which does not exist yet.

## Register Candidates

A view whose side is below $U$ proves a new upper bound (row 3). The selection lists it
under register candidates and never admits it.
Register such views as one batch result through the
[import runbook’s](../../../packing/campaign/result-import.md#stage-3-record) record and
validate stages, with a `regularizations` item for each count, as `T-155` registered 59
counts through `devtools.register_regularized_bounds`. Once the register moves $U$ to
the view’s side, the view is at the bound: `reclassify --refresh-bounds` decides a
driver run’s view again, the selection decides a grid-slack view against the new $U$,
and the next selection can draw either.

## When a Witness Changes

A drawn view lapses when its source witness changes, by a new record at the count or a
corrected witness (policy section 5). `packing-validate --records` then reports that the
witness changed since its view was derived.
To redraw the count:

1. Draw the axis tool’s view of the new witness with
   `python -m devtools.regularize_axis_components --update-atlas --n N`, which reports
   the lapsed view.
2. Run both generators on the new witness, then select and admit as above.

While another pull request is changing a count’s witness, leave the count out of `layer`
with `--exclude N`. Run and admit from one revision: a grid-slack view is admitted
against the witness the checkout holds, and the layer records that witness’s digest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
