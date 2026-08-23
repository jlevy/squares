# Review: The Tooling Layout, and What It Would Take to Clean Up

**Date:** 2026-08-23

**Author:** Claude (agent)

**Status:** Current — a map, not a plan of record.
Nothing here is scheduled.

The scripts under `explorations/packing/` accumulated one experiment at a time, and it
shows: nineteen entry points across three directories, two unrelated things both called
a “negative control”, and a `pytest` configuration that runs green while collecting
nothing. None of it is broken — `test.sh` passes end to end — but the layout now costs
more to read than it should, and two of the names actively mislead.

This maps the issues and what each would cost to fix.
It does not fix them.

## The findings, worst first

### T-1. Two unrelated things are both called a negative control

| File | What it actually is |
| --- | --- |
| `negative_control.py` (root) | A **study**. Does the exact verifier reject perturbed packings, and where does float64 have a tolerance blind spot? Its output is a result quoted in the reports. |
| `tools/negctl.py` | A **harness**. Applies the corruptions in `controls.yaml`, runs the gate, and confirms each check fires. |

Different jobs, different directories, near-identical names — and `negctl` reads as an
abbreviation of the *other* file.
`test.sh` invokes both, ninety lines apart.
This is the one a newcomer will get wrong, and it is the item worth fixing even if
nothing else here is.

Suggested: `negative_control.py` → `studies/float_blind_spot.py`, `tools/negctl.py` →
`checks/run_controls.py`. Neither name then describes the other’s job.

### T-2. `pytest` is configured, collects nothing, and exits 0

Concretely, from `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["sqpack", "tools", "tests"]
python_files = ["test_*.py", "*_test.py"]
```

`tools/perimeter_test.py` and `tools/regression_test.py` match `*_test.py` and sit in a
declared testpath, so pytest collects them by pattern.
Neither defines a single `def test_*`; both are `main()` scripts.
`tests/` does not exist at all.
The result: `uv run pytest` prints `no tests collected` and exits **0**.

A green run that checks nothing is the failure mode this directory’s whole defect log is
about, and the `_test.py` suffix is what creates the expectation.
Two honest ways out, and the first is the better one:

1. **Drop the pytest config and rename off `_test.py`.** `test.sh` is the gate, it
   works, and nothing here wants a second test runner.
2. Give the three scripts real `def test_*` wrappers so pytest exercises them.

### T-3. The three gate checks live in two different places

`differential_test.py` is at the root; `perimeter_test.py` and `regression_test.py` are
in `tools/`. All three are gate checks, all three are invoked by `test.sh`, and two of
the three lines that invoke them are adjacent.

### T-4. `tools/` mixes generating with checking

| Role | Files |
| --- | --- |
| Generate an artifact | `render_defects.py`, `render_tables.py`, `export_trump11.py` |
| Check something | `validate_schemas.py`, `perimeter_test.py`, `regression_test.py`, `negctl.py`, `check_generated_exempt.py` |

The checkers are the gate; the generators are the build.
Splitting them is the change that makes `test.sh` readable as a list of checks.

### T-5. The root directory is a grab-bag of three kinds

- **Runners**: `run_quench.py`, `run_baseline.sh`, `run_basin_entry.sh`
- **Studies** whose output is quoted in reports: `verify_trump11.py`,
  `negative_control.py`, `derive_field.py`, `bench.py`
- **A gate check**: `differential_test.py`

### T-6 and T-7, minor

`verify_trump11.py` (root) and `tools/export_trump11.py` split one subject across two
directories. And `tools/check_generated_exempt.py` — added in this same PR — is an
awkward name that would become `checks/generated_exempt.py` under any of the above.

## A layout that would resolve T-1 through T-5

```
explorations/packing/
  checks/      run_controls.py  controls.yaml  schemas.py
               perimeter.py  regression.py  differential.py  generated_exempt.py
  render/      defects.py  tables.py  export_trump11.py
  runs/        quench.py  baseline.sh  basin_entry.sh
  studies/     verify_trump11.py  float_blind_spot.py  derive_field.py  bench.py
  test.sh      sqpack/  sqsearch/  campaign/  frontier/
```

## What it would cost, and where the risk actually is

The mechanical part is small.
The risk is entirely in what does *not* get checked.

**The gate would catch these renames immediately.** `controls.yaml` carries 30 `file:`
and `run:` fields, each read or executed by the harness; `defects.yaml` carries 27
`recorded_in` paths, each existence-checked by `validate_schemas.py`. A stale entry in
either fails `test.sh` on the next run.

**Prose would rot silently.** Nothing verifies that a script named in a Markdown
document still exists:

| Name | Markdown files naming it |
| --- | --- |
| `run_quench.py` | 5 |
| `negctl.py` | 3 |
| `perimeter_test.py` | 3 |
| `negative_control.py` | 2 |
| `differential_test.py` | 2 |
| `validate_schemas.py` | 2 |

Those are the references a rename would break without telling anyone — in the
conventions, the handoff, the postmortem, and the round artifacts that cite the tool
they ran.
A rename sweep should ship with a check that every `tools/…py`-shaped string in
a Markdown file resolves, on the same reasoning that put `check_generated_exempt.py` in
the gate: a list that is trusted rather than enforced drifts.

## Recommended order, if it is done at all

1. **T-1 and T-2.** The two that actively mislead, and both are cheap.
   T-2 may be a four-line deletion in `pyproject.toml` plus three renames.
2. **T-3, T-4, T-5** as one move, with the Markdown-reference check landing first.
3. T-6 and T-7 fall out of step 2 for free.

## What not to do

Not during a round.
Round artifacts record the commit they ran at, and `exp-001`’s engine
commit is already orphaned by an earlier rebase — the gate reports it every run and it
cannot be repaired. A rename sweep in the middle of a series makes that kind of
archaeology harder for no gain.
Between series is free; mid-series is not.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
