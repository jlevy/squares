---
title: Gate Cost at the Widened Corpus
date: 2026-09-07
---
# Gate Cost at the Widened Corpus

What the pull-request surface costs now that the known-best corpus runs to n = 324, and
what the two steps that stopped fitting were replaced with.
Bead `think-lmlr`, the W5 efficiency slice of the
[atlas expansion plan](../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md).

The corpus grew from n = 1..100 to n = 1..324 on 2026-09-07 (commits `32b796cc`,
`6e21c4ca`, `282dee9d`): 324 cases and 52,650 unit squares against 100 and 5,050. Two
sweeps grew with it and one did not, and the readings below are what decided which of
them stayed on every pull request.

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
are not. The atlas reading keeps its per-subprocess receipts, because the split between
its one expensive member and its seven cheap ones is what that reading is for.

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
| `checks`, `geometry`, `suite` | unchanged | unchanged | unchanged |

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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
