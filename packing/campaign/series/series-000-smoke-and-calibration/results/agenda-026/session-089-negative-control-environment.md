# Session 089: Negative-Control Environment Diagnosis

The full gate at `a105f729` failed one step: negative controls.
It took 1447.15 seconds wall; every other step, including exhaustive exact behavioral
tests, passed. The corrected negative-control replay is pending at this handoff, so this
is not a full-green gate result.

This is `think-h264`, W7 pipeline-improvement/correctness, commissioned for
21:38:35–21:53:35 UTC on 2026-09-06. The source snapshot was
`/private/tmp/squares-launch-publish.ofyZXu`; the full-gate log is
`/private/tmp/squares-pr101-a105-full.log`. Git commit `a105f729` identifies the source.
These temporary paths locate the diagnostic run, not durable repository artifacts.
No research target, source change, dependency installation, or shared-environment
repointing was needed.

## Cause and Reproduction

The coordinator invoked the main checkout’s Python 3.14 with `PYTHONPATH=src` from the
immutable snapshot. That snapshot has no `packing/.venv`. In
[the control runner](../../../../../devtools/run_negative_controls.py), `clone_tree`
links each worker’s `.venv` to `ROOT / ".venv"` only when the latter exists.
The link was therefore absent.

`run_one` sets `UV_NO_SYNC=1`, but this does not make `uv` use the interpreter that
launched the parent.
The first worker `uv run` created an ordinary, empty worker `.venv`. Its Python lacked
the installed project dependencies.
All 67 failed controls in the full log invoke `uv run ... python`: 51 use
`python -m pytest`; the other 16 invoke the synopsis, canonicalization, or basic-bounds
checks. The runner truncates failed-command diagnostics to 120 characters, which hid the
final import errors in the full-gate summary.

The focused diagnostic used the unchanged `clone_tree`, `run_one`, and
`run_control_command` functions on one private copy under
`/private/tmp/squares-h264-diagnostic-sw80ewf6/worker`. It cleared
`UV_PROJECT_ENVIRONMENT` and `VIRTUAL_ENV`, put the main environment’s `bin` first on
`PATH`, and printed each complete command result before the runner truncated it.
The worker `.venv` was absent before these controls and present afterward as a
directory, not a symlink.

The two unchanged controls from [controls.yaml](../../../../../devtools/controls.yaml)
were:

- `synopsis - dateline duplicates volatile campaign progress`, running
  `uv run --frozen --quiet python -m devtools.check_synopsis`;
- `interval promotion - certificate endpoints rounded to nearest, not outward`, running
  `uv run --frozen --group dev python -m pytest tests/test_promote_krawczyk.py -q`.

Both commands exited 1 for missing dependencies, without reaching their intended
assertions. The synopsis traceback reached the private worker’s
`devtools/check_synopsis.py`, then `devtools/check_rung_figures.py`, and ended with:

```text
  File "/private/tmp/squares-h264-diagnostic-sw80ewf6/worker/packing/src/sqpack/yamlio.py", line 18, in <module>
    import yaml
ModuleNotFoundError: No module named 'yaml'
```

The interval command reported:

```text
/private/tmp/squares-h264-diagnostic-sw80ewf6/worker/packing/.venv/bin/python3: No module named pytest
```

## Verified Invocation Repair

Binding `UV_PROJECT_ENVIRONMENT` to the existing main environment made both controls
fire on their registered assertions, with syncing still disabled.
The synopsis check reported `Date dateline repeats campaign progress`. The interval test
reported `the serialized endpoints no longer enclose the root they were rounded from`.
The diagnostic used the same private source copy for both environment settings.

A separate replay through the public control-runner CLI also passed:

```bash
# Working directory: /private/tmp/squares-launch-publish.ofyZXu/packing
/usr/bin/time -p env \
  UV_CACHE_DIR=/private/tmp/squares-uv-cache \
  UV_PROJECT_ENVIRONMENT=/Users/levy/wrk/github/squares/packing/.venv \
  UV_NO_SYNC=1 \
  PYTHONPATH=src \
  PATH="/Users/levy/wrk/github/squares/packing/.venv/bin:$PATH" \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m devtools.run_negative_controls devtools/controls.yaml \
  -k 'certificate endpoints rounded to nearest' -j 1
```

It reported `1 negative controls fire as expected`. The control took 2.795 seconds; the
whole command took 5.05 seconds wall, 3.51 seconds user CPU, and 1.22 seconds system
CPU. The control time is included in the command wall time.
The earlier full gate’s failed negative-control step took 125.33 seconds, included in
the 1447.15-second full-gate wall time.

The worker’s absolute `src` and `packing` paths remain first in `PYTHONPATH`, so the
commands execute the mutated worker source while using the installed dependencies.
The observed mutation assertions confirm that this repair did not substitute unmodified
main-checkout code. No expectations were relaxed.
The coordinator has started the 163-control replay with this environment binding and
without the `-k` filter; this diagnostic did not duplicate it or rerun the full gate.

## Separate Snapshot Finding

After the environment repair, the synopsis control also reported dead links to
`.github/workflows/deep-gate.yml` and `.github/workflows/branch-mergeability.yml`. Both
files exist in the immutable source and are linked from `SYNOPSIS.md`, but
`ROOT_DOCUMENTS` omits `.github`, so the private worker lacks them.
The intended dateline assertion still fired.

This omission is separate from the missing-dependency cause of the 67 failures.
No snapshot-copying change was made.
A separately prioritized follow-up can add the referenced workflow evidence in
`packing/devtools/run_negative_controls.py` and retain a clean-snapshot link control in
`packing/tests/test_negative_controls.py`. This diagnosis makes no claim that an
unmutated worker passes every document check.

## Repair Addendum: Referenced Workflow Evidence

The preceding sections retain the environment diagnosis at its 21:49 handoff.
This addendum records `think-lpoq`, the separately authorized W7 repair on integration
line 101, commissioned for 21:51:00–22:06:00 UTC on 2026-09-06. The Git base at this
repair handoff is `cf299e6c`; the changes are limited to
`packing/devtools/run_negative_controls.py`, `packing/tests/test_negative_controls.py`,
and this addendum.

### Corrected replay of the original failed step

The coordinator’s environment-corrected replay on the unchanged `a105f729` snapshot
completed with exit 0 and `163 negative controls fire as expected`. Its log is
`/private/tmp/squares-pr101-a105-negative-controls-replay.log`. The slowest individual
control took 23.304 seconds; total process wall time and CPU were not measured and
remain unavailable.

That replay, combined with the other passing steps in the original 1447.15-second
invocation, discharges the old failed-step obligation.
The original invocation still failed one step.
The replay did not include the new workflow-copying fix below and is not evidence for
that fix.

### Snapshot repair and controls

The new regression first ran the complete synopsis checker in an unmutated private
snapshot. It failed with exactly two diagnostics: missing `deep-gate.yml` and
`branch-mergeability.yml` links.
This isolated the evidence omission from the earlier dependency failure and from any
intentional mutation.

The repair extends the existing referenced-file scan to `.github/workflows` and copies
selected files relative to the repository root.
It does not copy the whole workflow directory.
The existing size calculation counts every selected file against the unchanged snapshot
cap.

Two fast regressions in
[test_negative_controls.py](../../../../../tests/test_negative_controls.py) cover the
repair:

- A private selection fixture keeps an existing referenced workflow once, omits an
  unreferenced workflow and a nonexistent link, and refuses to follow a workflow symlink
  outside the selected root.
- The real snapshot passes the complete unmutated synopsis checker, preserves both
  workflow files byte for byte, and copies exactly the selected workflow evidence.
  The unchanged registered dateline mutation then fires on its expected assertion,
  without a dead-link diagnostic, and the synopsis bytes are restored.

Measured invocations used project Python 3.14 through frozen uv from `packing/`:

| Check | Result | Pytest time | Process wall | User CPU | System CPU |
| --- | --- | ---: | ---: | ---: | ---: |
| New clean-snapshot regression before the fix | 1 expected failure | 2.22 s | 2.46 s | 1.59 s | 0.70 s |
| Both new controls after the fix | 2 passed | 3.37 s | 3.61 s | 2.61 s | 0.89 s |
| Final focused file, quick lane | 16 passed; 1 slow test deselected | 8.07 s | 8.32 s | 5.72 s | 1.93 s |

The final test command was:

```bash
/usr/bin/time -p env UV_CACHE_DIR=/private/tmp/squares-uv-cache \
  uv run --frozen --no-sync --all-extras --group dev python -m pytest \
  tests/test_negative_controls.py -q -m 'not slow and not exhaustive_exact' \
  --durations=5
```

The new real-snapshot test’s final call time was 4.23 seconds.
Ruff check and BasedPyright report zero findings on both changed Python files, and Ruff
format reports both files formatted.
The initial Ruff `RUF005` finding was corrected before these final checks.
Flowmark’s automatic-format check passes on this report.
No full suite, research target, dependency synchronization, shared-environment change,
or repeat of the coordinator’s 163-control replay ran for this repair.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
