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
  layer still draws four views above $U$, at 18, 26, 66 and 85, each an exception
  question 13 names; a pass may replace them, never add to them);
- row 10 of the decision table admits;
- improves on today’s drawing under the policy’s
  [improvement rule](../policies/regularization-policy.md#11-the-improvement-rule)
  (question 14): worse on none of its goals and better on at least one.

The rule is stated once, in the policy, and `devtools.improvement_rule` reads it from
there; this guide does not restate it.
Its goals are the seven measures below, the side, and exactness.
The seven measures are the drawing’s light, uneven and near-axis squares, its distinct
angle classes and its hues, fewer being better, as `devtools.census_drawing_regularity`
counts them from the house renderer’s colouring; and its house and stage totals of full
shared sides, more being better.
Classes and hues catch a square turned a hair off its group: at n = 236 two squares
0.000537 degrees off drew seven hues where today’s drawing has six, while the other five
measures tied. Exactness is the gain of a view that replaces a numerically checked
witness; a view that ties today’s drawing on every goal is no improvement, and the
change is not made.

Where more than one view of a count passes, the first in this order is drawn: Evan
Daniel’s, then grid-slack’s by rising straightening threshold.
A passing view that another passing view dominates, being worse on some measure and
better on none, is skipped.
`devtools.regularize_select` applies exactly these rules.
A view at row 7 or 8 goes to the owner, and a view below $U$ is registered before it is
drawn; both are described below.
A view below $U$ is a smaller packing, so once validated it becomes the count’s house
best packing, by the import runbook’s
[house rule](../../../packing/campaign/result-import.md#the-house-rule).

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

The driver of Evan Daniel’s regularizer costs about 13.7 CPU-hours over all 324 counts
(49,302 CPU-seconds in the `evand-regularize-full` receipt, 3.8 hours of wall at four
workers) and writes a receipt for each run.
A handful of re-housed counts takes 2 to 4 CPU-minutes each
(`evand-regularize-adopt518-v2-rerun-2026-10-13`: 2,097 CPU-seconds for 15 counts).
The grid-slack generator takes seconds to a few minutes a count.
Each grid-slack run has one straightening threshold, half a degree by default; run other
thresholds into their own directories, since views from runs at 1 and 5 degrees are
admitted on the same terms.

An algebraic house, whose witness states its squares in a real number field, runs the
same commands. Since version 2 (think-mbdw, 26 October 2026) the grid-slack generator
starts from that witness’s own exact pose, re-solves in its field and writes the view
there, at the witness’s side; both exact routes for a number field decide it, as the
policy’s obligation 1 names them.
Evan Daniel’s driver solves such a witness to a rational side just above the algebraic
$U$, which is not drawn (row 4). The 21 runs on the seven algebraic houses of 23
October, at three thresholds, took 28 CPU-minutes in all (43 to 499 seconds of wall a
count on a host at a load of 10 to 20), nine tenths of it `exact_verify` over the field;
the independent route took 1 to 12 seconds a view.

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

Today’s drawing is the picture the tree draws at the count, read from `--tree`, this
checkout by default: the layer’s view where the improvement rule makes it the default
picture (step 5), else the house drawing.
A view the layer holds but does not draw is never the reference: at n = 176 the axis
tool’s view is held for two more uneven squares, so a view is judged against the house.
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
A view replaces the layer’s only where it is worse than today’s drawing, as step 3 reads
it, on none of the improvement rule’s goals; otherwise the layer keeps its view, and the
call’s `kept_why` names the goals.
So an admission never makes the drawn picture worse.

### 5. Render and Record

```bash
python -m devtools.render_regularized_atlas --update
python -m devtools.default_drawings --update
python -m devtools.flip_regularization --update
python -m devtools.regularized_drawings
python -m devtools.render_results --update
```

These redraw the views, decide each count’s default picture and its regularization
state, flip-regularize each default picture, regenerate `results.yaml`’s
`regularized_drawings` and each case record’s `regularization` note, and regenerate
`frontier/RESULTS.md`. Run `default_drawings` before `regularized_drawings`: where a
view is not its count’s default picture, the note opens by saying that the house drawing
is drawn and why, read from the default record.
Update the layer’s counts in the atlas README’s regularized-views section by hand.

Flip regularization is the last stage, separate from the others and fast, and it changes
no file but its own record.
After `default_drawings` has decided which picture each count draws,
`flip_regularization --update` decides, from that picture’s retained rendering, the
rotation and flip that put its heaviest quadrant lower right and the heavier of that
quadrant’s neighbours lower left, by the rule of
[policy section 13](../policies/regularization-policy.md#13-flip-regularization), and
writes them to `atlas/known-best/flip-regularization.json` in a few seconds.
The composites and the site apply the pose when they draw, and the house drawing as
published keeps its source’s pose.
`python -m devtools.flip_regularization --n N` prints a count’s quadrant weights and
which stage decided its pose, and `--check` is the records-tier step
`flip regularization record is current`.

A drawn view is the count’s default picture, on the site, the atlas and the posters,
where it improves on the house drawing under the same rule
([policy section 12](../policies/regularization-policy.md#12-the-default-picture)); the
case page keeps the house drawing as published.
The homepage and atlas page start with Regularized and offer Original for comparison
with those same current house packings.
The chooser does not change which views pass the improvement rule.
The command writes `atlas/known-best/default-drawings.json` and prints how many views
are defaults. The posters show the defaults as they stood when they were drawn and may
trail until the next version or a redraw (`build_known_best_atlas --update-composites`).

The same record’s `states` gives every count, n = 1..324, its regularization state: what
is drawn, the drawn picture’s measures, the witness (its id, its source’s key, path and
revision, and its side), the runs that decided that witness, and one of `regularized` (a
view of Evan Daniel’s regularizer or the grid-slack generator is drawn),
`regular-as-published` (the house drawing has no uneven and no near-axis square, no
strong view of the count has lapsed, and `PENDING_ALLOWED` does not hold it for its
bead’s runs), `decided-no-better` (the strong generators ran on this witness and drew
nothing the improvement rule takes), `exempt` (set aside on the owner’s recorded word,
with the bead that owns it and a review date within 14 days) or `pending`.
`regularization-owed`, a drawing left unregularized on an open bead as the exact
algebraic houses were from 23 to 26 October 2026, is retired: the records tier fails a
count in it, and the import runbook’s
[regularization step](../../../packing/campaign/result-import.md#adopt-a-house-then-regularize-it)
says what a change that moves a house does instead.
The axis tool’s view alone never makes a count regularized: it is the reference and
fallback. A count is `decided-no-better` without an entry of its own where the layer
holds a strong generator’s view of the current witness that the rule does not draw;
otherwise the decision goes into `default_drawings.SETTLED` with the runs, the outcome,
where it is recorded and the witness’s source key, path, revision and side it was made
on, so a new house, a new certificate file or an upstream fix makes the count pending
again. Every run the entry names must be held by the retained evidence under
`packing/cases/regularized_drawings/` (`default_drawings.run_records`): a grid-slack
run’s block at `<bead>-<date>/<run directory>/run.json`, or a driver run’s
`receipt.json` there, each beside the run’s reports (`n-<count>/report.json.gz`), which
say which counts the run covered.
A run that only the layer’s index records is not enough, since the index drops a run’s
block once no entry draws from it: `python -m devtools.default_drawings --retain-runs`
copies the block to `settled-runs/<run id>/run.json` while the index still has it.
A copy is deleted with the last entry that names its run, and the gate fails on one no
entry names. A decision that still owes runs or a recorded outcome (`owed`) is not
settled, and the gate fails it.
The ten decided counts of 15 October 2026 owed think-0ut1 grid-slack at 1 and 5 degrees
or their per-count outcomes until its runs of 16 October 2026, whose outcomes the atlas
README gives count by count; none owes anything now.
Recording each run’s outcome on the index, so that a decision needs no entry, is
think-4ov9. An entry where the layer’s own strong view already decides the count fails
the gate. When a pull request regularizes a pending count, it takes the count off
`default_drawings.PENDING_ALLOWED`.

The note says who regularized the drawing and that a pure regularization, one whose side
is not below $U$ and which so proves no new bound, is not a result (the policy’s section
9, question 16): by the Squares Project, with the generator’s credit line, the side
relation, the registered result that holds the packing and the view.
Where the drawn regularization’s exact side is itself registered as an upper bound, the
note names that result instead; where a result registers this project’s regularization
of a count the layer does not draw by that method, the note credits it and names the
result; where the house is itself a regularization its source published, the source is
credited first. Where Evan Daniel’s regularizer or the grid-slack port of his placement
made the view, the note and the register’s item also name this project’s modifications
to it, or say it ran unmodified (the policy’s section 7): the owner asked on 13 October
2026 that they be noted.
They are read from the view’s index entry, so the retry rungs must be there.
`layer` records them from a run’s reports; for a view admitted without them, run the
counts again and record them from the new run, which writes only where its view is the
drawn view byte for byte and the entry records no rungs or retry yet, names the new run
as the entry’s `run.rungs_from`, and adds its receipt’s block to the index’s `runs`:

```bash
python -m devtools.regularize_evand rungs --run-dir $RUNS/evand --repo-root ..
```

The new run is named by its directory, `evand-regularize-<run directory>`, so give it a
directory no earlier run used.
Where a supplying run’s id already names another run,
`rename-run --from ID --to ID --note TEXT --repo-root ..` gives it a distinct one and
records why on its block (`id_note`), as the fresh run of the #518 counts was renamed
`evand-regularize-adopt518-v2-rerun-2026-10-13`.

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
  tests/test_render_regularized_atlas.py tests/test_improvement_rule.py \
  tests/test_default_drawings.py
python -m devtools.release_pin --check
```

`--records` holds the index to the views and witnesses by digest, re-renders the
drawings, checks the register, and measures every drawn view against its house drawing
again (`default pictures improve on their house drawings`), listing the counts that keep
the house picture and why.
`every drawn picture is regularized, regular as published, decided or exempt on the owner's word`
reads each count’s state back without measuring, holds it to the index, and fails on a
pending count that `PENDING_ALLOWED` does not name, on a named count that is no longer
pending, on a `SETTLED` entry made on another witness or no longer needed, and on one
naming a run the retained evidence does not hold, under another generator, or whose
record shows it did not run that count, and on a copy in `settled-runs/` that no entry
names; on a `regularization-owed` count, a decision that still owes something, and an
exemption without the owner’s recorded word or past its review date; and, against
`--base-ref`, on a house the change moves that does not land regularized, regular as
published, decided or exempt on the owner’s word, or whose flip pose the flip record
does not hold. It prints the list’s size and the houses the change moves.
`bead tree` fails a change to `default_drawings.py` whose list or exemptions name a bead
that is not open. Run it alone with `python -m devtools.default_drawings --check-state`.
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
section 5 describes: one entry in `packing/atlas/known-best/regularized/reviews.yaml`
naming the count, the date, the reviewer, the decision and its reason, the generator and
its version (the index’s `pin`, `source_commit` and `patches`), the run, output and row,
the source witness as it identifies itself (id, source key, path, revision and side),
and the gallery the reviewer decided from.
Then the same `layer` call that admits a run’s row-10 views draws the reviewed one, its
entry keeps the table’s row-7 decision and names the record, and `--check-atlas` holds
the two to each other.
A record lapses with its witness or its generator’s version, as at n = 211, which the
owner admitted on 16 October 2026; `--check-atlas` names which lapsed.

## Register Candidates

A view whose side is below $U$ is a smaller packing than the house best packing, and it
is registered as a result (row 3), however it was made.
It is taken through the import runbook’s stages like any report, crediting the packing’s
finder and the regularizer, and once validated it is adopted as the house best packing
in the pass that validates it, by the
[house rule](../../../packing/campaign/result-import.md#the-house-rule).
Its bound is new only where no earlier certificate already stated that side exactly, as
one had at the 33 counts where the record carried Evan Daniel’s side rounded up, and no
larger count’s verified upper bound is at or below it; otherwise the result says which
result already proves the bound (the policy’s section 9, question 16). The selection
lists it under register candidates and never admits it.
Register such views as one batch result through the
[import runbook’s](../../../packing/campaign/result-import.md#stage-3-record) record and
validate stages, with a `regularizations` item for each count, as `T-155` registered 59
counts through `devtools.register_regularized_bounds`. Where an earlier result’s
certificate states the same side, the item names it as `first_certified_in`, as 33 of
`T-155`’s name `T-101`, and the case note then says the side proves no new bound;
`python -m devtools.regularized_drawings --check` fails an item that should name one and
does not. A grid-slack view is registered the same way as a batch of its own, as `T-156`
registered $n = 290$ with `select --batch grid-slack --run-dir RUN ... --n N ...`, then
`decide` and `controls` with the same `--batch`. Read the next count’s ceiling as well
as the view’s own: $s(n) \le s(n + 1)$, so where the next count’s verified upper bound
is at or below the view’s side, the bound is not new.
`T-156`’s was not, since `T-155`’s certificate at $n = 291$ is at the same side; the
selection records such a ceiling (`implied_by`), and the result says its bound follows
by monotonicity, as `T-002` says of a lower bound, and is kept as the certificate of the
count’s own packing.
The selection refuses a view whose side lies above the next count’s ceiling: that
ceiling already proves more than the view, and the count’s bound is registered by
monotonicity instead.
Once the register moves $U$ to the view’s side, the view is at the bound:
`reclassify --refresh-bounds` decides a driver run’s view again, the selection decides a
grid-slack view against the new $U$, and the next selection can draw either.

## When a Witness Changes

A drawn view lapses when its source witness changes, by a new record at the count or a
corrected witness (policy section 5). In `packing-validate --records`, `--check-atlas`
reports the stale view until `--update-atlas` redraws it, and `--check-state` reports
the pending count after that.
A review record of the count lapses only when the witness identifies itself otherwise; a
witness re-derived with the same id, source key, path, revision and side leaves it
standing, and then `--check-atlas` asks for the record to be withdrawn or confirmed in a
new one, since `layer` would draw the old view again.
A house adoption is the usual cause, and these steps belong to the pull request that
adopts it: the import runbook’s
[Adopt a House, Then Regularize It](../../../packing/campaign/result-import.md#adopt-a-house-then-regularize-it)
schedules them under the pass’s compute cap, and `devtools.adopt_houses` prints the
counts it re-houses with these commands when it writes.
To redraw the count:

1. Once `python -m devtools.build_known_best_atlas --update` has written the new
   witness, draw the axis tool’s view of it with
   `python -m devtools.regularize_axis_components --update-atlas --n N`. Where another
   generator’s view lapses, the axis record carries a `lapsed` block naming that
   generator and its run.
   It names the last strong view that lapsed: later houses carry it, whatever the
   count’s state, until a strong generator’s view is admitted again.
2. Run `python -m devtools.default_drawings --update`. The count is now `pending`, even
   where the new house has no uneven and no near-axis square, and `--check-state` fails
   on it. So is a count `PENDING_ALLOWED` names, whatever its new house reads.
3. Run both generators on the new witness, grid-slack at 0.5, 1 and 5 degrees and Evan
   Daniel’s driver, then select and admit as above: 5 to 25 CPU-minutes a count in all.
   Give each run a directory no earlier run used, since the layer records a run by its
   directory’s name; `adopt_houses` prints names that carry the adoption’s day and its
   lowest and highest re-housed count, which no run in the index has and another
   adoption that day, of other counts, does not print.
   Where neither draws better, settle the count in `default_drawings.SETTLED` with the
   runs and the new witness’s source key, path, revision and side.
   Retain each run’s evidence in the same pull request, as for any settlement (above):
   its reports with its `run.json` or `receipt.json` under
   `packing/cases/regularized_drawings/<bead>-<date>/<run directory>/`, or, for a run
   only the index records, its block, copied by `default_drawings --retain-runs`. A
   count an adoption re-houses is never deferred to `default_drawings.PENDING_ALLOWED`:
   its runs are owed in the adoption’s pull request, by the import runbook’s
   [house rule](../../../packing/campaign/result-import.md#the-house-rule), and an
   adoption whose runs do not fit under the pass’s compute cap is staged with them in
   `select_houses.PENDING_ADOPTION`. List each re-housed count’s drawing before and
   after in the pull request with
   `python -m devtools.default_drawings --compare <(git show origin/$BASE:packing/atlas/known-best/default-drawings.json)`,
   which reads the record of its base branch, `BASE` being `main` unless the pull
   request is stacked. Where a strong view gives way to a drawing worse than it on a goal
   of the improvement rule, whatever drew it, the table names those goals, and marks
   each such count that still reads pending, “its runs are owed in this pull request”.
   The axis tool’s view of the new witness is drawn wherever it improves on the new
   house, which says nothing of the view the count lost (review D1 of #641). Where a
   corrected witness’s runs must wait, allow each count the table does not mark in
   `PENDING_ALLOWED` with the open bead that owns its runs, and name the witness the
   correction replaced in `default_drawings.CORRECTED` (its source, path, revision and
   exact side, as the base branch’s record names them), in the pull request that
   corrects the witness, so the deferral is reviewed.
   `--check-state --base-ref origin/main` holds the entry to the base record and fails
   it wherever the house moved, whatever import moved it.
   Then run `default_drawings --update` again, since the record copies the entry into
   the count’s reason, and step 5, since `--update-atlas` redrew the axis views.
   Nothing but review limits how many counts join the list; the gate prints its size.

Until 15 October 2026 the lapse was only printed, and the adoptions of #553, #598 and
#614 left twenty counts drawn without a strong generator’s decision on their witness: at
n = 176 the raw house was drawn while the index said `regularized`. Those twenty are the
allowlist’s first entries (think-la7h, think-kpm3, think-3zi3). Fourteen of them lost a
strong view before the axis record kept a `lapsed` block, and the Evan Daniel views of
272 and 304 were never admitted to the index at all.
Their entries in the list are the record of it, so a count on the list stays pending
whatever a new house reads (review B1 of #641). The list is therefore an input to each
count’s state, not only a measure of the pending set, and the gate cannot judge two
changes to it. Dropping an entry whose count then reads regular as published passes, and
drops the runs its bead owes; adding a count whose house reads regular passes, and holds
it pending.
Both are reviewed decisions: the pull request that makes one shows the bead’s
runs or the `--compare` table (review C2 of #641). Holding the fourteen lapses in code,
apart from the list, would let the gate refuse the first, and is think-k6rj.

A run that decides allowed counts takes them off `PENDING_ALLOWED` in its own pull
request. Close a bead that the list, an exemption or a decision’s `owed` names only once
the pull request that takes its last count off has merged.
`bead tree` fails any change to `default_drawings.py` whose record names a bead that is
not open, entries it inherited included, and hosted CI checks each pull request merged
with `main`. So the run’s own pull request passes with its counts removed, and every
other pull request’s next run sees them gone.
A bead closed before its pull request merges turns every other open pull request that
touches `default_drawings.py` red until that merge (review B4 of #636).

While another pull request is changing a count’s witness, leave the count out of `layer`
with `--exclude N`. Run and admit from one revision: a grid-slack view is admitted
against the witness the checkout holds, and the layer records that witness’s digest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
