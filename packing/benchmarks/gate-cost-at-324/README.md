---
title: Gate Cost at the Widened Corpus
date: 2026-09-07
---
# Gate Cost at the Widened Corpus

What the pull-request surface costs now that the known-best corpus runs to n = 324, and
what the three re-derivations that stopped fitting were replaced with.
Bead `think-lmlr`, the W5 efficiency slice of the
[atlas expansion plan](../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md).

The corpus grew from n = 1..100 to n = 1..324 on 2026-09-07 (commits `32b796cc`,
`6e21c4ca`, `282dee9d`): 324 cases and 52,650 unit squares against 100 and 5,050. Two
sweeps grew with it and one did not, and the readings below are what decided which of
them stayed on every pull request.

Then the `checks` job failed the register’s drift rule on the same corpus and the same
day, from a step nobody had been looking at, and
[the section on it](#the-checks-job-and-the-grid-replay-inside-it) is the second slice.
It is written against the first: same box, same instrument, same guard, and a baseline
that is this branch’s tree rather than the commit the first slice started from.

## Protocol

**The instrument is the gate’s own recorder, not a second timer.** Setting
`PACKING_VALIDATION_ARTIFACT_DIR` makes `packing-validate` write, per run, one
`run-*.json` of provenance, one `step-*.json` per step carrying its wall and status, and
one `command-*.end.json` per subprocess carrying its own wall and its argument vector.
Those files are retained under [`runs/`](runs/) exactly as the gate wrote them; nothing
here is transcribed by hand except this prose.
Two kinds were dropped rather than kept: the `command-*.start.json` receipts, whose
every field the matching `.end.json` repeats, and the per-subprocess receipts of the
tier runs, where the step record is the number and forty-eight command records per run
are not. Three readings keep their per-subprocess receipts, because a split inside one
step is what each of them is for: the atlas step’s one expensive member against its
seven cheap ones, and `exact verification` at each end of the second slice’s change.

**Every reading waited for an idle host, and the two that did not say so.** The driver
polls `pgrep -f 'packing-validate|devtools\.|-m pytest'` before each reading and does
not start until it is empty, logging how long it waited.
That guard is not decoration: three unrelated agent sessions ran the push tier, the
negative controls and the exhaustive tier on this machine during the window, and a
contended reading of a twelve-minute step is not a reading of that step.
Every baseline reading, and the speedup table, is from an idle host.
Two of the after-readings -- `--sweeps` and `--checks` -- gave up waiting after five
minutes and ran beside two other processes; the driver logged `PROCEEDING CONTENDED` for
each.
Both are therefore upper bounds, and both are answering a fits-or-does-not question
where an upper bound is the conservative direction.

**Shape and host.** macOS on Apple silicon, ten CPUs, Python 3.14.7 free-threading
build. The baseline is commit `2841eec9`; the after-readings are that commit plus this
branch’s working tree, which is what a contributor running the surface would have.
Each sweeps reading uses the sweeps job’s own declared shape, `--jobs 4 --inner-jobs 2`,
so `PACK_JOBS` reaches a pooled step as it does on CI; the three other pull-request jobs
use theirs.
A single step selected with `--only` reports no tier, so no ceiling is judged
against it, which is why each of those readings is a step wall rather than a tier
verdict.

**Local walls are not CI walls**, and nothing here is written into
`devtools/gate-budgets.yaml` as a `measured_seconds`: that field is only ever a reading
at the tier’s declared reference shape, which is a four-CPU hosted runner.
What these readings support is the ordering and the ratios -- which step is the wall,
what fraction of it moved, and whether the remainder fits inside a declared ceiling with
room. Where a ceiling moved, the register says it was argued from the parts and its
record cleared, which is the same thing `BC-214` and `BC-218` did before.

## Baseline, before any change

Commit `2841eec9`, 2026-09-07, idle host.

| Reading | Shape | Wall (s) |
| --- | --- | ---: |
| `known-best chunk census` | `--only`, `--jobs 4 --inner-jobs 2` | 40.07, 40.01, 40.00 |
| `known-best n=1..100 atlas` (whole step) | `--only`, `--jobs 4 --inner-jobs 2` | 703.28 |
| … `build_known_best_atlas --check` | (inside that step) | 691.19 |
| … the seven other subcommands | (inside that step) | 12.09 |
| `single-square translation escape screen` | `--only`, `--jobs 4 --inner-jobs 2` | 766.26 |
| `packing-validate --checks` | `--jobs 3 --inner-jobs 1` | 118.65 |
| `packing-validate --geometry` | `--jobs 3 --inner-jobs 1` | 51.56 |
| `packing-validate --suite` | `--jobs 1 --inner-jobs 1` | 40.42 |

Three readings for the census because it is under five minutes; one each for the two
steps that are over it.
The census readings span 0.07 s, which is the tightest agreement anywhere in this table
and is what a step pinned at `CALIBRATION_CORPUS` by `D4` should look like: the corpus
tripled and this step did not move.

**The whole `--sweeps` tier was not clocked before the change**, and that is a gap worth
stating rather than papering over.
Two unrelated agent sessions took the host for the whole window the reading needed, the
driver refused to start against a busy machine, and a twenty-minute contended reading of
a tier whose parts are already measured buys less than it costs.
What can be said exactly is that the tier is four units on ten CPUs, so its wall is its
longest unit’s wall: at least the 766.26 s the escape screen took, plus whatever the
other three add through contention.
That is a derivation, not a reading, and it is the only number in this document that is.

Two failures in the four-job readings are pre-existing and unrelated to cost.
`campaign record` failed in `--checks` against an uncommitted session file another
session was editing, and
`test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots` failed in
`--suite` from the frontier-generator work landing on the same branch.
Both readings are still walls of the work the tier does.

### What the baseline says

**The escape screen has stopped fitting rather than merely become dear.** 766.26 s is
6.9× its 110.66 s at n = 1..100, and the pool that produces it is already sized by this
job’s own `--inner-jobs 2` -- so that figure is what the lever buys, not what it costs
unpulled.
It is also within 134 s of the gate’s own 900 s per-step subprocess timeout, on
a machine faster than the hosted runner the timeout was set for.

**The atlas step has one member and seven passengers.** `build_known_best_atlas --check`
is 691.19 s of 703.28 s, 98.3 per cent; the other seven subcommands cost 12.09 s between
them, and five of those are pinned at `CALIBRATION_CORPUS` and cannot grow with the
corpus at all. A step declared as one unit is only as schedulable as its longest member,
which is the same argument that split the chunk census out of it on 2026-09-06 -- at a
different seam, found by the same measurement.

## The speedup, taken before any deferral

`OR-13` puts this first: a check earns its exit from the pull-request surface by its own
measured cost, and the cost has to be the one that is left after the obvious parallelism
has been spent.

`build_known_best_atlas` was building its 324 cases in one process.
Each case reads its own source, normalizes one witness, checks that witness’s semantics
and renders one house SVG, and no case reads another’s output, so the loop is
embarrassingly parallel; the escape screen, the golden basins, the soundness perimeter
and the chunk census already share one answer to how wide such a loop may run, and this
one now asks it too.

| Shape | Wall (s) | CPU (s) | Speedup |
| --- | ---: | ---: | ---: |
| serial (the baseline above) | 691.19 | 691.19 | 1.00× |
| `--jobs 2` | 348.15 | 677.66 | 1.99× |
| `--jobs 4` | 184.34 | 688.74 | 3.75× |

**The evidence that this is the same build, not a faster one.** Every row is a `--check`
run, and `--check` re-derives every witness, every house rendering, every frontier link,
the source index, both composite SVGs and the manifest, and compares each against the
retained bytes; a parallel build that rounded one coordinate differently would fail it.
All three passed. CPU is flat across the three rows -- 691.19, 677.66, 688.74 -- so the
pool divided the work rather than adding any.
`test_a_pool_worker_builds_the_same_bytes_as_this_process` holds the property as an
assertion over three cases chosen to reach all three source layers.

`--update --jobs 4` with a clean `git status` was the originally proposed proof and was
deliberately not run.
`update` redraws every composite PNG unconditionally through cairosvg, which is
independent of `--jobs` and would have dirtied binaries this session cannot restore.
`--check` at each worker count is the stronger half of that evidence anyway: it is the
comparison `update` would have skipped writing after.

The same option makes the slow lane cheaper without changing what it checks.
`test_known_best_composite_contains_every_case_and_square` is the one test that pays a
whole corpus build; it now asks the shared worker policy for its count, and the file’s
35 tests run in 144.33 s with that test at 133.54 s.

**The escape screen was left alone**, because it was already pooled and already sized by
`PACK_JOBS`: its 766.26 s is what two workers cost, not what serial code costs.

**Nothing in the check path was doing avoidable work.** The composite raster and PDF
comparisons already read the receipt each export carries rather than redrawing a
25-by-30-inch page, which is the class of waste worth looking for, and it was not there
to find.

## What still did not fit, and what replaced it

The escape screen is 766.26 s against the sweeps job’s 210 s ceiling, which settles
itself. The atlas rebuild is the one worth stating carefully: 184.34 s is under 210 s,
but it is one step of four, at four inner workers the job cannot give it while three
other steps run, on a machine faster than the hosted runner.
The number that decides it is the shape the job actually runs -- 348.15 s at two inner
workers -- and that is 1.66× the whole tier’s ceiling before the other three steps are
counted. So both re-derivations moved to the deferred surface, and a stand-in took each
one’s place on every pull request.

The stand-ins are not samples of their steps; they are the complement of what was
deferred, which is what lets the two halves be checked as a partition rather than as a
list.

**`known-best atlas records and sample`** keeps the seven subcommands that did not grow
with the corpus and replaces the eighth with `build_known_best_atlas --check --sample`,
which:

- rebuilds every field of `manifest.json` but its per-case entries -- contract, declared
  range, policy, generator, composite records, key order and formatting -- from the
  retained entries and compares the result to the retained bytes;
- re-derives `sources.json` whole, which re-hashes every retained upstream SVG against
  its upstream-declared digest;
- checks that every expected witness and rendering exists and that nothing unexpected
  does, and that no raw Kingbird source directory has been retained;
- compares every one of the 324 frontier records against the witness link the builder
  would write into it, and every manifest `reported_side` against its frontier record;
- holds each composite’s retained SVG to the canvas its own specification computes, and
  every PNG and PDF receipt to that retained SVG’s digest;
- and rebuilds every ninth case in full -- 36 of 324 -- comparing witness text, house
  rendering and manifest entry byte for byte.

**`translation escape screen records and sample`** runs
`screen_translation_escape --check --sample`, which rebuilds the retained screen from
its own cases and exclusions -- aggregate, method block, tolerances, claim boundaries,
contract and formatting, with the JSON-Schema validator and `screen_errors` running on
the way through -- compares that to the retained bytes, checks the records cover exactly
n = 1..324, and re-screens every twenty-seventh record in full.

| Sampled step | Shape | Wall (s) | CPU (s) |
| --- | --- | ---: | ---: |
| `build_known_best_atlas --check --sample` (36 of 324) | `PACK_JOBS=2` | 47.01 | 86.81 |
| `screen_translation_escape --check --sample` (12 of 324) | `PACK_JOBS=2` | 43.83 | 63.84 |

Both were taken while other sessions held part of the machine, so they are upper bounds.

**Why the two strides differ.** The rule is the same for both -- a fixed stride from the
corpus’s first case, so the sample is the same on every run and reaches the 224 cases
the widening added -- but the cost is not.
A screened record’s work grows with the square of n, so every ninth record cost 220.43 s
of CPU and 127.22 s of wall in the screen against 86.81 s and 47.01 s in the atlas.
Nine there would have put a single step above two minutes of a 210 s tier, which is what
the deferral was for.
Twenty-seven brings it back beside the census.

**What the floor is, and why it is the right thing to size against.** The sweeps job is
four units on four CPUs, so its wall is its longest unit’s wall, and the unit that
cannot be made cheaper is `known-best chunk census` -- 90.38 s on CI, 42.11 s here --
because `D4` pins it at `CALIBRATION_CORPUS` and it will not grow with the corpus.
The screen sample lands just above it; the atlas sample lands about forty per cent above
it and does set the tier’s wall, which the tier reading below prices exactly.
What the strides buy is that the number they set it to is a fraction more than the
census rather than a multiple of it.

## After the change

The four pull-request jobs, each run exactly as `packing-validation.yml` invokes it, and
`--fast`, which is their union.

| Reading | Shape | Wall (s) | Ceiling (s) | Of ceiling |
| --- | --- | ---: | ---: | ---: |
| `packing-validate --sweeps` | `--jobs 4 --inner-jobs 2` | 58.48 | 210 | 28% |
| `packing-validate --checks` | `--jobs 3 --inner-jobs 1` | 122.90 | 195 | 63% |
| `packing-validate --geometry` | `--jobs 3 --inner-jobs 1` | 48.38 | 180 | 27% |
| `packing-validate --suite` | `--jobs 1 --inner-jobs 1` | 38.26 | 205 | 19% |
| `packing-validate --fast` | `--jobs 3 --inner-jobs 1` | 229.05 | 700 → 600 | 33% → 38% |

The `--fast` reading was taken against the 700 s ceiling this change then tightened to
600 s; the percentage against the new one is in the second column.

Inside the sweeps tier, over 145.39 s of step time:

| Step | Wall (s) |
| --- | ---: |
| `known-best atlas records and sample` | 58.48 |
| `translation escape screen records and sample` | 44.65 |
| `known-best chunk census` | 42.11 |
| `prospective n=101..324 safe seed` | 0.15 |

Every step passes except the two pre-existing failures named above, which fail the same
way before and after.
The gate reports rather than enforces each band, because a ten-CPU box is not any of
these tiers’ four-CPU reference shape -- which is also why nothing here is written into
the register as a `measured_seconds`.

`--fast` is 229.05 s whole, and its two longest steps are the two sampled ones at 103.59
s and 69.70 s, because that tier runs at `--inner-jobs 1` and their pools get one worker
each. That is the serial price of the stand-ins, and it is the number a contributor
running the surface by hand pays.

Both cleared records now carry the same open item, and the gate states it in its own
verdict: *no cost is recorded for the sweeps tier at 4 cpus, `--jobs 4 --inner-jobs 2`*,
and the same for `fast`. Each was cleared rather than adjusted because the tier it
measured no longer exists, and the first CI run at the reference shape prints the line
to write back.

## The deferral decisions, and the measurement each rests on

| Step | Measurement | Where it runs now |
| --- | --- | --- |
| `known-best n=1..324 atlas rebuild` | 691.19 s serial, 184.34 s at four workers, against a 210 s ceiling | deferred; 348.15 s at the deep gate’s `--inner-jobs 2` |
| `single-square translation escape screen` | 766.26 s at the job’s own `--inner-jobs 2`, within 134 s of the gate’s 900 s per-step timeout | deferred |

**Both fit where they landed**, which a deferral has to establish and not assume.
Run as `deep-gate.yml` invokes them -- `--only` each, `--jobs 2 --inner-jobs 2` -- the
pair is 762.60 s of wall, the screen 762.60 s of it and the rebuild 354.27 s beside it
on the second slot. Both pass.
The rebuild is 354.27 s against the gate’s 900 s per-step subprocess timeout, and both
finish under the `slow behavioral tests` step that already sets that job’s wall, so the
deep gate costs no more wall than it did.

`test_the_pull_request_surface_defers_only_what_was_measured` carries both arguments and
`test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers` requires
`deep-gate.yml` to run exactly the complement, so neither can be deferred here and
forgotten there.

## Ceilings and records

| Tier | Ceiling before | Ceiling after | Record |
| --- | ---: | ---: | --- |
| `sweeps` | 210 s | 210 s | 107.05 s cleared |
| `fast` | 700 s | 600 s | 502.30 s cleared |
| `checks`, `geometry`, `suite` | unchanged | unchanged | unchanged by this slice |

The `checks` row is what the section below then changed: its ceiling still stands at 195
s and its 99.39 s record is cleared, on the same rule and for a step this slice never
touched.

**Two records were cleared and neither was replaced**, which is the register’s own
precedent rather than a shortcut.
`measured_seconds` is only ever a reading at the tier’s declared reference shape -- a
four-CPU hosted runner -- and every reading in this document is from a ten-CPU
development box, so writing one in would leave the drift and stale rules comparing
numbers from different machines.
`BC-214` and `BC-218` cleared this same field twice before for the same reason: the
figure measured a tier that no longer exists.
The gate prints the line to write back on the first run at the reference shape, so
nothing has to be remembered.

**The `sweeps` ceiling did not move**, and that is a decision.
The predicted wall is near the census, around 105 s on the hosted runner, so 210 s
leaves real margin for a slow day -- and it is still below the roughly 390 s of step
time this tier would cost on that runner if its pools stopped parallelising, so serial
degeneration fails here rather than passing quietly.
Tightening it against a prediction rather than a reading is what `OR-14` calls
advertising an aspiration.

**The `fast` ceiling moved down**, because the tier lost its two most expensive steps
and 700 s against a 229.05 s local reading is a hang detector rather than a band.
600 s is about 2.6× that reading, which is the room a tier nobody clocks on CI needs for
a runner of unknown speed.
It is not tightened further for the same reason the `sweeps` one did not move.

`devtools.check_gate_budgets` passes: nine tiers, three with a recorded cost, all
ceilings within 2× of it, all named in `development.md`.

## The `checks` job, and the grid replay inside it

The sweeps job was not the only one the widening reached, and the second one announced
itself rather than being found: on 2026-09-07 the `checks` job ran **189.09 s** against
a recorded 99.39 s -- 1.90x, where the register’s drift rule fails at 1.5x -- and 6 s
under its 195 s ceiling.
The gate’s own verdict named the step in the same breath: `exact
verification` was **133.4 s of it, 70.6 per cent**. That is the first record in this
register cleared by its own rule firing rather than by a re-scoping somebody noticed.

**The baseline here is not `2841eec9`.** It is this branch’s tree with everything above
already applied, commit `1f436895` with a clean working tree, which the gate’s own
`run-*.json` records for every reading.
Same box, same instrument, same idle guard; readings under
[`runs/grid-before/`](runs/grid-before/) and [`runs/grid-after/`](runs/grid-after/),
with the per-subprocess receipts kept for one reading of the step at each end, because
the split between its one growing member and its sixteen fixed ones is what those two
readings are for.

### Baseline

| Reading | Shape | Wall (s) |
| --- | --- | ---: |
| `exact verification` (whole step) | `--only`, `--jobs 3 --inner-jobs 1` | 84.56, 84.11, 83.95 |
| … `check_basic_bounds` | (inside that step) | 34.74 |
| … `dilation_corollary --check-limit-record` | (inside that step) | 26.58 |
| … the fifteen other subcommands | (inside that step) | 23.23 |
| `packing-validate --checks` | `--jobs 3 --inner-jobs 1` | 120.03 |

Three readings of the step because it is under five minutes, and they span 0.7 per cent.
The tier reading is 120.03 s of wall over 219.76 s of step time in 48 steps, every step
passing.

**One member of that step grows with the corpus and it is the one that grew.**
`check_basic_bounds` replays the exact rational grid witness of every case whose
verified upper bound is the grid ceiling -- 305 of the 324 today -- and it was 3.58 s
when [D-370](../../../defects.md) moved it into this step at n = 1..100. The other
sixteen subcommands are fixed cases: one rational control, one limit record, ten
construction replays and four witness checks, none of which can move when the corpus
widens.

**The ratio this box shows against CI is 1.58, in two places at once.** 189.09 / 120.03
for the tier and 133.4 / 84.21 for the step.
That agreement is what makes the local readings below usable for a decision about a
hosted runner; nothing here is written into the register as a `measured_seconds`.

### The cost curve

`check_basic_bounds` gained `--max-n` to take this, which is the only reason that flag
exists.

| Replayed | Grid cases | Wall (s) |
| --- | ---: | ---: |
| n ≤ 100 | 81 | 2.75 |
| n ≤ 200 | 181 | 12.65 |
| n ≤ 324 (all) | 305 | 34.70, 34.94, 34.80 |

**The curve is quadratic in the corpus’s last n, not cubic**, and that is a property of
the check rather than luck.
`verify_grid` buckets its pair enumeration -- two unit squares overlap only if their
centres are within sqrt(2), so a bucket of side 2 and its eight neighbours contain every
pair that could -- so one case is about linear in its own n and the corpus is the sum of
them. A widening to n = 400 would put this near 53 s with nothing else changing.

### The speedup, taken before any deferral

`OR-13` puts this first, and here it is worth doing and does not help.
The replay is a map over independent cases -- `verify_grid` builds its own grid from n
and reads nothing else -- so `check_basic_bounds` now sizes a `ProcessPoolExecutor` from
`sqpack.workers.worker_count`, the same contract `screen_translation_escape` and
`build_known_best_atlas` use.

| Shape | Wall (s) | CPU (s) | Speedup |
| --- | ---: | ---: | ---: |
| serial (`--jobs 1`) | 34.81 | 34.81 | 1.00x |
| `--jobs 2` | 18.58 | 36.64 | 1.87x |
| `--jobs 4` | 9.97 | 38.49 | 3.49x |

**The equivalence evidence is byte-for-byte, not a matching verdict.** The tool’s whole
stdout at one worker and at four hashes to `1caa1409…`, and the sampled run’s to
`6d1e0e63…`, at both counts; `cmp` reports no difference for either pair.
That is stronger than comparing exit codes, because the failure this could introduce is
a reordered failure list rather than a wrong one -- `pool.map` yields by submission
index, and the tool keys its failures by n and prints them in frontier-document order.
`test_a_pool_worker_replays_the_same_verdicts_as_this_process` holds the property as an
assertion over sizes chosen to cross a perfect square, its predecessor and its
successor, where the grid’s own side changes.
CPU is flat across the three rows, so the pool divides the work rather than adding any.

**And it buys the pull request nothing, which is the point of measuring it.** Every
pull-request tier passes `--inner-jobs 1`, so `PACK_JOBS` is 1 and a pooled step is the
serial step there by design -- the same cap that keeps nineteen ordinary tests from
going over the quick lane’s per-test ceiling on contention alone.
What the pool decides is where the deferred copy can live: run as `deep-gate.yml`
invokes it, `--only "exact rational grid replay" --jobs 2 --inner-jobs 2`, the whole
replay is 18.79 s of wall over 36.65 s of cpu, underneath a slow lane that is 890 s.

### What did not fit, and what replaced it

87.56 s of local `--checks` scaled by 1.575 is about 138 s on the reference runner, and
120.03 s scaled the same way is the 189.09 s that was actually observed.
So the local criterion of “under 120 s” is the one number in this decision that would
have been misread: the tier was already at 120.03 s here on the day it failed the drift
rule there.
The deferral is argued on the hosted figure, and the local ones support it by
their ratio.

`check_basic_bounds` is therefore sampled on the pull-request surface and run whole on
the deferred one, as `exact rational grid replay`. The stand-in is the complement rather
than a slice:

- every one of the 324 cases still has its declared grid upper bound, area lower bound
  and Nagamochi lower bound compared against the closed form its evidence record names
  -- that half is 0.14 s of the 34.86 s, and it never left;
- every ninth case that claims a grid witness is still replayed exactly, 34 of 305, from
  the first, so the sample reaches the 224 cases the widening added;
- and what waits for the deep gate is the other eight ninths of the per-case geometry.

| Sampled step | Shape | Wall (s) |
| --- | --- | ---: |
| `check_basic_bounds --sample` (34 of 305) | `PACK_JOBS=1` | 4.12, 4.19, 4.13 |

### After the change

| Reading | Shape | Wall (s) | Ceiling (s) | Of ceiling |
| --- | --- | ---: | ---: | ---: |
| `exact verification` (whole step) | `--only`, `--jobs 3 --inner-jobs 1` | 53.66, 53.57, 53.56 | — | — |
| `packing-validate --checks` | `--jobs 3 --inner-jobs 1` | 87.83, 87.31, 87.54 | 195 | 45% |
| `packing-validate --geometry` | `--jobs 3 --inner-jobs 1` | 48.25 | 180 | 27% |
| `packing-validate --suite` | `--jobs 1 --inner-jobs 1` | 39.00 | 205 | 19% |

The four readings above are of the code change, taken before this document and the
register entry were written.
The three pull-request jobs were then run again with those documents in place, since
`checks` is the tier that reads them, and `--records` with them because a registry
moved: 27.52 s, 86.57 s, 48.93 s and 38.20 s, every step of all four passing, at 9, 44,
27 and 19 per cent of their ceilings.

The step is 84.21 s to 53.60 s, the tier 120.03 s to 87.56 s, and every step passes at
both ends -- the two pre-existing failures the earlier readings carried are gone,
because the uncommitted session file and the frontier-generator work that caused them
have landed. `--geometry` and `--suite` are unchanged within noise, which is what a
change confined to one step of one job should look like.

Inside the tier, over 186.86 s of step time in 48 steps:

| Step | Wall (s) |
| --- | ---: |
| `exact verification` | 55.10 |
| `bead tree` | 31.06 |
| `soundness perimeter` | 29.04 |
| `type floor (basedpyright)` | 21.66 |
| the other 44 | 49.99 |

**This step no longer floors the tier, and that is the number that says the sample is
dense enough.** Three workers divide 186.86 s of step time into 62.29 s, and the longest
step is 55.10 s under it, so the wall is now the queue’s rather than any one step’s. A
denser sample would buy cases the deferred replay already covers and buy them against a
floor that has moved.

### What the remaining wall is, and what this slice did not do

Two levers are visible in these readings and neither is spent here, so they are recorded
rather than taken.

**The queue is submitted in declared order, and the longest step is declared 40th of
48.** Before, the step was 86.71 s and the tier 120.03 s: the step started about 33 s in
and the tier ended when it did.
After, the ideal wall is 62.29 s and the observed one 87.56 s, so about 25 s of this job
is a queue waiting for work it could have started first.
That is worth about 40 s on the reference runner, it is one scheduling decision rather
than a coverage trade, and it belongs to whoever owns the gate’s scheduler rather than
to a slice about one step.

**`dilation_corollary --check-limit-record` is now the step’s largest member at 26.35
s.** It is a fixed case -- one certificate and one limit record, at n = 11 -- so it did
not grow and will not, and it is half of what is left.
Nothing here measured whether it can be made cheaper.

**The per-case predicate was left exactly as it is.** A grid witness’s non-overlap is a
property of the lattice it is built on, so the bucketed pair sweep inside `verify_grid`
is in one sense re-proving what the construction already guarantees, and the coordinates
are integer-valued `Fraction`s where Python `int`s are the same rationals more cheaply.
Both are real options and both were refused: the replay’s contract is an *independent*
exact check of a witness, and a check made cheap by assuming the thing it verifies is
not the same check. `OR-13` asks for the cost to come off the schedule, not off the
predicate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
