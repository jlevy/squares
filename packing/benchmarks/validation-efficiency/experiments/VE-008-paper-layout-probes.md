---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-008
  title: Reuse one paper visit for figure and credit probes
  registered: "2026-10-14"
  tier: exploratory
  control_label: paper-layout-control
  candidate_label: paper-layout-combined
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target:
    - tests/test_site_glyphs.py::test_every_paper_sets_every_figure_one_way
    - tests/test_site_glyphs.py::test_the_first_figure_is_the_drawing_alone_at_the_first_papers_width
    - tests/test_site_glyphs.py::test_every_paper_lays_the_front_out_one_way[1280]
    - tests/test_site_glyphs.py::test_every_paper_lays_the_front_out_one_way[390]
---
# Reuse one paper visit for figure and credit probes

Registered before candidate measurements.
Implementation was authorized just before this record was written; no candidate
measurement had been observed.
Status: rejected by the exact-report validity oracle; the routine-code optimization was
withdrawn. No timed control/candidate observations ran.

## Hypothesis and Frozen Criterion

Reuse one paper visit for figure and credit probes should remove repeated work from the
retained strict-checkpoint workload.
This is a hypothesis, not an established saving.
Alternate three control/candidate observations through the maintained validation-timing
instrument. Every observation must pass its full semantic oracle.
Require at least 15% reduction in median inclusive wall, nonoverlapping ranges and
allocated worker-seconds at most 1.25 times control.
Report median and range with a separate complexity judgment; a miss stays a miss.
No confirmatory speedup, full-shard admission or three-minute result follows.

## Semantic Guards

Keep the same three real papers and widths 1280/390. The control keeps separate figure
DPR2 and credit DPR1 visits.
The candidate reads credits before the existing figure probe in one fresh DPR2 page.
Before timing, every field, order and value from all six credit reports must equal the
DPR1 control, and all six figure reports must equal their unchanged control.
Any mismatch rejects this candidate; no dropped fields or tolerance widening.
Keep the independent platform, disabled-head and unflagged glyph controls.

## Regime and Measurement

The two arms use identical frozen source bytes and the same four semantic cases,
including their complete site fixture in each fresh process.
The thin `benchmarks.paper_layout_timing` driver passes an explicit pytest-plugin
condition, captured in the command receipt: `control` calls the unchanged independent
figure and credit readers; `candidate` calls the combined reader through the same shared
fixture. No source files are alternated between observations.
Count rendering, browser setup, settling and both probes inside inclusive command wall.

Use existing Python 3.14 and the locked environment, warm filesystem caches, fresh
pytest processes and private fixtures, PACK_JOBS=1 and one native thread.
Retain exact source inputs, commands, allocation, raw output and JUnit through the
existing campaign instrument.
Other source edits may be light; no known heavy local measurement overlaps these
observations. Keep all original failures and incomplete observations.

The common baseline starts from source `77152fb83`, with the reviewed functional font
and CLI repairs and the shared-publication integration held at its local default of off.
Capture the complete frozen source state before verification and all six alternating
observations; do not substitute a different rendered corpus or source revision between
arms. Every observation explicitly passes `--site-publication=local`, keeping the
shared-publication cache off despite any ambient CI state.
The existing validation-timing instrument records actual source, dirty state, command,
interpreter, allocation and raw results automatically.
Retained hosted timings identify the candidate, not recoverable time or CPU attribution.

## Bootstrap Chronology

The first verification command stopped before pytest collection or browser launch in
0.719 seconds: the timing instrument intentionally narrows `PYTHONPATH`, and the primary
project interpreter could not import KPress while loading the explicit benchmark plugin.
Its failed start/end receipt is retained unchanged; no report comparison or performance
observation completed.

The existing locked external environment has Python 3.14.7 and the required
dependencies.
Actual browser verification used that absolute interpreter; the six planned
timed observations did not run.
Its KPress source is clean at the repository’s pinned revision; the referenced workbench
tools match the frozen source.
The instrument still places the candidate’s `packing/src` and `packing` first for
project imports. No dependency was installed and no driver or production workaround was
added.

All frozen production and test inputs were checked unchanged before the corrected
verification. Source-freeze v2 retains this chronology and the automatically captured
interpreter/module context; the original snapshot and failed receipt remain available.

The external-interpreter verification next reached the unchanged full site fixture, then
stopped in 12.792 seconds because four new synopsis links were absent from the committed
Git inventory. No layout probes or comparison completed.
The publication link guard was kept intact; a normal docs-only commit included the four
registered experiment records before source-freeze v3.

Each timed observation’s complete retained report must also equal the verified canonical
report outside the timed interval.
Any changed field invalidates that observation and stops the screen; no field is dropped
or normalized to obtain agreement.

## Outcome: Exact-Report Refusal

The completed source-freeze-v3 oracle took **130.667 seconds** and refused the
candidate. Both arms returned 62 figure rows and 68 credit rows.
All credit fields matched exactly between the independent DPR1 reader and the combined
DPR2 reader. One figure field differed: `n11-lower-bounds-explainer.html`, width 1280,
figure 3, `share` was `0.371` in the independent control and `0.372` in the candidate.
The other fields, report order and inventories matched.
The cause of that difference was not established.

The frozen validity rule rejected this candidate before performance sampling.
There were **zero timed observations**: no three-pair screen, timing median, range or
speedup verdict exists.
The 0.719-second import bootstrap failure and 12.792-second Git inventory fixture
failure above remain failed receipts; neither is a performance sample or a passing
semantic result. No tolerance was widened, report field dropped or oracle retried after
the one-field refusal.

The combined reader, shared test fixture and cost-only tests were withdrawn.
The independent APIs and all original figure, front, platform and disabled-head checks
remain. The functional font/CLI repairs and literal-code browser negative controls are
retained. Exact candidate source snapshots, the reproduction patch and the moved thin
driver remain under `pr599-integration/ve008-paper-layout/rejected-candidate/` in the
closeout evidence archive, outside disposable scratch.
The full raw report is `report-verify-27b2a2e74c4543de8792a355e4253693.json`; its oracle
run is `928cfb49348b4dda828cc1e2f5fbab24`.

## Evidence

Raw receipts and source snapshots belong in the existing task closeout archive under
pr599-integration, outside disposable scratch.
The campaign report is generated from retained records; this experiment has an explicit
validity refusal and no performance result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
