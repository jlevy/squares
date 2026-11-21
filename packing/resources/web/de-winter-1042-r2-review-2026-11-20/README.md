# R2 Derived Lower Bounds: C2 Custody Checkpoint

This packet preserves an interrupted independent review of the derived lower bounds in
[issue #1042](https://github.com/jlevy/squares/issues/1042), with its C2 continuation of
21 November 2026. The source is Joost de Winter’s work after Hiroaki Hosono at
[JoostdeWinter/square-packing `21d944c43098e2261ab7d713cd10f02a5eb13f3d`](https://github.com/JoostdeWinter/square-packing/tree/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19).
The review remains in progress under `think-bgi2`. This is a custody checkpoint, with no
accepted complete Stage 4 review or change to a verification or confirmation rung.
C2 and C3 below are check names in the [frozen plan](programs/review-plan.md).

## Retained Results and Limits

The [C2 receipt](out/resume-2026-11-21/c2-confirmed/c2.json) records exact periodicity
and mass checks D1, D3 and D8, and the corner weight, placement and arithmetic checks
within D7. It contains the strip claims at 137, 188, 189 and 218, the corner-modified
claim at 217, and six refused negative controls.
The 137 calculation uses the superseded strip side `11881/1000`; the stronger
four-region claim is assigned to C3.

The frozen program’s label `STRIP_AND_CORNER_CLAIMS_DECIDED` has this component scope.
Anchor coverage and receipt identity (D0), local coverage of the exact modified corner
measure, and the construction lemmas and pigeonhole argument remain pending.
These computations therefore establish no complete lower bound.
The programs are retained here but are not yet cited by registered evidence entries.

| Artifact | Meaning |
| --- | --- |
| [C2 receipt](out/resume-2026-11-21/c2-confirmed/c2.json) | The unchanged frozen checker run on the 17 pinned source inputs; all six controls refused |
| [Checkpoint summary](out/resume-2026-11-21/review-checkpoint.json) | Source and freeze references, scoped results, host, timing, guard summary and pending work |
| [Synthetic self-test](out/selftest.json) | Pre-freeze synthetic checks; its `failed` list is empty |
| [Synthetic plumbing](out/plumbing.json), [strips](out/plumbing-strips.json) and [envelopes](out/plumbing-envelope.json) | End-to-end driver exercises on invented measures; they decide nothing about the source claims |

The plumbing retains `CONTROL_ACCEPTED` for its hard-coded `n_minus_1_at_189` control
and an envelope exit of 1 with `NOT_DECIDED` outcomes.
Its synthetic 161 board intentionally fails the fit hypotheses.
Those outcomes remain part of the freeze and are separate from the six refusals on the
actual C2 inputs.

## Freeze, Interruption and Continuation

The original rR2 reviewer froze the plan on 20 November 2026 at 19:51:16 UTC, before
writing the checker, and was interrupted at about 20:40 UTC. The replacement rR2b
reviewer froze the checker at 21:09:01 UTC after synthetic runs and before source-data
runs or opening any producer program.
The [plan digest list](frozen/plan-frozen-digest.txt) and
[checker digest list](frozen/checker-frozen-digests.txt) retain those boundaries.
Their commits are `3a02ec8d29190155dcaf1b806ff6b1474722b2f5` and
`1e86fd925a92b0458b65d8431b83f7327a6c46b6`, respectively.

A Codex reviewer continued on 21 November, checked the frozen files and the 17 C2
inputs, and ran the frozen C2 checker.
The first run placed its timeout inside the memory guard’s process tree.
A second run placed the 1,800-second GNU timeout outside that tree and produced the same
report byte for byte.
The confirmation receipt is authoritative; the first run’s separate copy and full
supervision logs remain in external custody.
The retained report is 9,287 bytes with SHA-256
`dcf90c4b9b5d1fa53d05ccd469c9350de33f443a211f81701ec29f2f761c371d`. Only the checkpoint
summary’s two receipt references are corrected for publication; the frozen plan,
programs, synthetic outputs and raw C2 receipt retain their bytes.

The resumed review records that no producer program was opened or run and C6/C7 remain
unopened.
The plan requires its findings to be frozen before reading PR #1051, the import
lane’s notes, R1’s review or the record at these counts.
The Codex integration editor read the published R1 review as a custody-publication
precedent and did not author or rerun an R2 checker.
This editorial work adds no independent mathematical findings.
The independent continuation must retain its own read boundary; a reviewer exposed to
those other findings must disclose that exposure.

## Source Custody and Reproduction

The [C2 input list](out/resume-2026-11-21/c2-inputs.sha256) selects 17 files totaling
1,321,443 bytes from the original [source inventory](programs/source-files.sha256). The
recovery matched all 17 hashes to that frozen inventory before execution and checked
them again afterward.
Paths in both lists are relative to the upstream `lower_bounds_2026_11_19/` directory.

The
[source declaration](../de-winter-lower-bounds-2026-11-19/acquisition/declaration.json),
[source manifest](../de-winter-lower-bounds-2026-11-19/acquisition/sources.json) and
[subtree digest list](../de-winter-lower-bounds-2026-11-19/acquisition/upstream-subtree.sha256)
record the earlier intake’s custody at the same pin.
Seven C2 JSON inputs already have matching retained copies in that source packet.
The ten compressed measures, `proof/k100.json.gz`, `k300.json.gz` and `k900.json.gz`
under the listed repeated-strip and corner folders, are pinned-only there and were
recovered into external storage for C2. This checkpoint does not contain those ten
payloads. They can be recovered from each listed path under the exact upstream pin;
verify the compressed bytes against the C2 input list before reading them.
A durable mirror of bulk payloads belongs in the project’s hosted-data custody route.

| Program | Role |
| --- | --- |
| [rr2_measure.py](programs/rr2_measure.py) | Exact rectangle-measure reader and eight-image expansion used by the checks |
| [rr2_strips.py](programs/rr2_strips.py) | C2 periodicity, mass and corner arithmetic checks and controls |
| [rr2_envelope.py](programs/rr2_envelope.py) and [rr2_envelope.cpp](programs/rr2_envelope.cpp) | Pending C3 region-mass checks; the Python driver compiles the C++ program |
| [rr2_selftest.py](programs/rr2_selftest.py) | Synthetic checks of the reviewer’s arithmetic and geometry |
| [rr2_plumbing.py](programs/rr2_plumbing.py) | Creates a synthetic source layout and exercises the drivers |

These programs use the reviewer’s own implementation and Python’s standard library, with
no imported producer code.
The frozen plan records the source prose, formats and data the authors read.
The recorded C2 command, after recovering and checking the inputs, is:

```bash
"$PYTHON_3147" -I -B "$PACKET/programs/rr2_strips.py" \
  --source "$SOURCE" --controls --out "$OUTPUT"
```

`PYTHON_3147` names the CPython 3.14.7 interpreter, `PACKET` this directory, `SOURCE`
the recovered `lower_bounds_2026_11_19/` directory, and `OUTPUT` a new receipt path.
The recorded wrapper used one worker, waited for a live memory guard before releasing
the checker, and kept the 1,800-second timeout outside the guarded subtree.
For a guarded rerun, keep the timeout outside the monitored tree and account for
the run against the same review budget.

## Host, Cost and Pending Work

C2 ran on Darwin 25.5.0 arm64 with CPython 3.14.7. The confirmation used 13.44 seconds
elapsed, 12.90 user and 0.11 system; the first run used 13.22 seconds elapsed, 12.63
user and 0.09 system.
Their combined measured workload CPU was 25.73 seconds.
The confirmation’s guard recorded two pauses and resumes, 18.5 seconds paused, no
harvest, no kill and no abort.
The workload and guard exited zero.
Elapsed workload time, guard-watched time and cumulative CPU are distinct measures.
The public summary omits local paths and process inventories; the full supervision
records remain external.

C3 remains undecided.
Its frozen recipe specifies GNU g++ 13.3.0 with `-O2 -std=c++17`; the available Apple
clang 21 and Homebrew GCC 14.2 were not substituted.
Its disk-area calculations use `long double` and a fixed widening, so an alternative
compiler or arithmetic environment needs an explicit reviewed amendment.
A matching Linux/GCC environment and recorded arithmetic assumptions are pending, and no
producer envelope inputs were fetched in this continuation.

C6’s producer-code audit and receipt identity/domain checks, C7’s source replay and
mutations, and the remaining mathematical arguments stay pending under the frozen order.
The original 40 CPU-hour allowance is cumulative, with at most two workers and a
30-minute ceiling per computation.
Spending from the interrupted reviewer, synthetic checks and compilation has not been
reconciled with the two C2 runs.
Further computation needs that account and a recorded budget decision; this checkpoint
does not reset the allowance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
