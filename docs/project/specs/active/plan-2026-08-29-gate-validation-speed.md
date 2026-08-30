# Feature: Gate Validation Speed

**Date:** 2026-08-29

**Author:** Claude (agent), from a working session with the repository owner

**Status:** Draft

## Overview

Make the validation surface fast enough that the checks which actually catch defects get
run before every push, by fixing what makes them slow rather than by running fewer of
them.

The work is measured throughout.
Every number below was taken on one container on 2026-08-29 and is reproducible; where a
number replaces an earlier one, the earlier one was wrong rather than stale.

## Goals

- **A pre-push tier under about two seconds.** Registry, schema, and generated-view
  checks are the ones that break CI, and they should cost nothing to run.
- **Tier membership argued from what a step can catch and how often it can catch it**,
  not from what the tier happens to contain today.
- **No step wearing another step’s name.** Exact geometry inside a step called
  `soft-schema validation` is why that step was slow and why nobody looked.
- **No speedup that weakens a claim.** Every change either preserves the verdict exactly
  or carries a differential test proving it does.

## Non-Goals

- **A validation result cache.** Considered and rejected below; the measurement that
  motivated it disappears once the validator is replaced.
- **Reducing what is checked.** No step is dropped, no test is skipped, no tolerance is
  loosened. `D-365` and `D-366` are repaired rather than routed around.
- **A general step-dependency graph.** `BC-062` proposed a reachability-scoped selector
  and was retired into `BC-075` because it answers “which steps can this change reach”
  when the prior question is “which steps should anyone run now”.

## Background

### What was measured

`D-369` classified seven CI failures on one branch.
Every one was a registry, generated view, or declared contract going stale, and none was
a behavioural test. The checks that caught them were reachable only through `--fast`,
which costs about eight minutes because one step is roughly 87% of it, so skipping it
kept looking like the cheaper move.

`D-370` then found that the pre-push tier’s own cost was not where anyone would guess.
Profiling `soft-schema validation` at `67.4s`:

| Work | Cost |
| --- | ---: |
| Schema-validating the 100 frontier cases | `0.38s` |
| Schema-validating the frontier datasets | `0.03s` |
| Schema-validating `defects.yaml` | `0.08s` |
| Schema-validating 208 witness files | `8.64s` |
| `verify_packing` over 96 grid packings, inside `cross_checks` | `10.29s` |

The schema checks were already instant.
What surrounded them was not.

### What has already landed

Three fixes took the step to `15.5s` and the records tier from `70s` to `15.9s`:

- Both loaders in `sqpack.yamlio` now sit on `yaml.CSafeLoader`. PyYAML’s pure-Python
  scanner was 163 of 245 profiled seconds, over 12.6 million `check_token` calls, while
  libyaml ships with the pinned wheels.
- `Draft202012Validator` is built once per schema rather than once per document.
  329 artifacts declare 23 schemas, so each was re-read and re-compiled fourteen times
  over.
- The grid replay is bucketed, which is sound rather than convenient: `verify_packing`
  establishes that every piece is a unit square, two unit squares overlap only if their
  centres are within `sqrt(2)`, and a bucket of side 2 with its eight neighbours
  contains every such pair.
  166,650 exact pair tests became 57,665 with nothing skipped that a full sweep would
  have judged.

`lint floor (python)` split into `lint floor (ruff)` at under a second, the half that
caught `D-369`’s `F601`, and `type floor (basedpyright)` at `36s`, which left the tier.

### What remains, and the alternatives that were measured

`6.06s` of jsonschema descent over 208 witness files carrying 3.7 MB of exact rationals,
and `3.58s` of exact geometry.

**A Rust validator settles the first.** Same schemas, same payloads, 314 documents:

| Validator | Compile | Validate |
| --- | ---: | ---: |
| `jsonschema` (current, pure Python) | `0.1 ms` | `6,010 ms` |
| `fastjsonschema` (generates Python source) | `114.6 ms` | `667 ms` |
| **`jsonschema-rs`** (PyO3 bindings to the Rust crate) | `3.0 ms` | **`10.7 ms`** |

559 times faster than what runs now, and 62 times faster than `fastjsonschema`.

**Two alternatives were measured and rejected**, and both are recorded so neither is
proposed again:

- **`ruamel.yaml`** is slower, not faster.
  On 81 of this repository’s own files, 1 MB: PyYAML `CSafeLoader` `0.128s`, PyYAML pure
  `1.370s`, ruamel `typ="safe"` `1.991s`, ruamel `typ="safe", pure=False` `1.976s`,
  ruamel round-trip `2.730s`. Its `pure=False` engages no C parser in this build, and
  its value is comment-preserving round-trips, which nothing here needs.
- **A modification-time or content-hash validation cache.** Hashing all 315 artifacts
  costs `8.4 ms` against `0.62 ms` to `stat` them, so the key would have been a content
  hash rather than an mtime heuristic, which can serve a stale pass after a
  `git checkout` restores a same-size variant.
  The reason to reject it is not cost but need: it existed to avoid six seconds that the
  Rust validator turns into ten milliseconds.
  A cache is a correctness-sensitive mechanism carrying a permanent invalidation
  obligation — the artifact, its schema, and the transitive checker source all have to
  enter the key, or it serves a stale pass.
  Do not build one to buy back ten milliseconds.

## Design

### Approach

Three independent changes, in an order where each makes the next easier to judge.
The first is a drop-in with a differential proof.
The second moves work between steps without changing what is checked.
The third is the tier contract, which is only arguable once the first two have removed
the noise.

### Components

**`devtools/validate_schemas.py`** holds the validator construction, already funnelled
through one cached `_validator(schema_path)` helper, so the swap is one function body
and two attribute names.

**`devtools/check_basic_bounds.py`** holds `verify_grid`, which is the exact geometry
currently reached from `cross_checks`.

**`src/sqpack/cli/validate.py`** holds the `Step` table and the tier flags.
`Step` already carries `fast` and `records`.

**`benchmarks/`** is where a decision-bearing measurement belongs once it is repeatable,
per `OR-1`. The validator comparison is currently a scratch script and must not stay
one.

### API changes

`jsonschema-rs` maps onto the current call sites without a shim:

| `jsonschema` | `jsonschema-rs` |
| --- | --- |
| `Draft202012Validator(schema)` | `Draft202012Validator(schema)` |
| `error.message` | `error.message`, byte-identical on the cases checked |
| `error.path` | `error.instance_path`, the same list |

`iter_errors` exists on both, so the `sorted(..., key=lambda e: list(e.path))` ordering
survives with one attribute rename.

Distribution is `abi3` from `cp310`: one wheel serves 3.10 through 3.14 and later, on
macOS x86_64 and arm64, `manylinux_2_17` x86_64, and `win_amd64`. No Rust toolchain in
CI, no source build on any platform this project uses, and no wheel churn on a Python
bump. Pin the version, per `tbd guidelines supply-chain-hardening`.

## Implementation Plan

### Phase 1: The validator, and the geometry it was hiding

- [ ] Add `jsonschema-rs`, pinned, to the project dependencies; keep `jsonschema`
  installed, because the differential test needs both.
- [ ] Swap `_validator` to `jsonschema_rs.Draft202012Validator` and rename `e.path` to
  `e.instance_path` at the one call site.
- [ ] Add `benchmarks/bench_schema_validation.py`: a repeatable comparison over the real
  corpus that prints both timings and the differential verdict, so the choice can be
  re-argued rather than remembered.
- [ ] Add a differential test asserting the two validators agree on every artifact in
  the corpus and on a generated family of mutations of each: dropped required keys,
  retyped values, emptied arrays, unexpected properties.
  A validator that accepts what the old one rejected is a soundness regression, and this
  is the check that would catch it.
- [ ] Move the exact grid replay out of `soft-schema validation`. It belongs with
  `exact verification`, which is where a reader looks for exact geometry and where its
  cost is legible. Nothing about the check changes; only which step reports it.
- [ ] Record the measured before and after in `D-370`.

### Phase 2: The tier contract

- [ ] Re-derive tier membership from what each step can catch and how often, and write
  the argument down. The candidate shape, to be confirmed against the timings rather than
  assumed: `--records` before every push; `--fast` at a block boundary; the default
  before a commit or handoff; `--strict` once or twice a session.
- [ ] Decide `D-366`. The `negative controls` step exceeds the 900-second per-step cap
  at 140 controls, needing `1268s` uncapped.
  Raising the cap weakens the same guard for every other step, so the options are
  sharding the suite, moving it to `--strict` with its own cap, or reducing per-control
  setup cost. The controls themselves are not at fault and none may be dropped.
- [ ] Restate the cadence table in `conventions.md` from measurement after the changes
  land, as it was restated once already when it claimed sixty seconds for an
  eight-minute tier.
- [ ] Roll up this session’s agent logs into the existing `CodexEfficiencyRollup/v2`
  shape, so the tier argument rests on measured coordinator and command time rather than
  impressions of it.

## Testing Strategy

**The differential test is the load-bearing one.** Both validators run over the whole
corpus and over generated mutations of it, and every accept/reject verdict must match.
A first pass over 718 mutations agreed 718 times; the test makes that a standing
guarantee rather than a one-off observation.

**Negative controls** for anything that could silently stop checking:

- A malformed artifact still fails, with the error text a reader can act on.
- A schema change still invalidates the documents that declare it.
- The grid replay still fires on a mutated `build_grid`, in whichever step now owns it.

**The bucketing argument gets a test**, not just a comment: a packing whose overlapping
pair sits in non-adjacent buckets must be impossible for unit squares, and a
deliberately over-large piece must be caught by `check_unit_squares` before the pruning
is relied upon.

**Timing is asserted loosely or not at all.** A wall-clock assertion on a shared runner
is a flaky test; the benchmark reports, the gate does not gate on it.

## Rollout Plan

Phase 1 lands as one change with the differential test alongside it, on a branch off
`main`, verified by `packing-validate --records` plus the full fast behavioural suite,
and by CI on the pull request.
Phase 2 is a contract change to `conventions.md` and the `Step` table and lands
separately, because a tier boundary that moves silently is exactly the failure `D-369`
describes.

There is no migration and nothing to deploy.
A reader who has the repository checked out gets the speed on their next `uv sync`.

## Open Questions

- Does any schema in the corpus use a keyword where `jsonschema-rs` and `jsonschema`
  differ in strictness rather than in speed?
  The differential test answers this for the corpus as it stands; a new schema keyword
  is the case to watch.
- Should `format` assertions be turned on?
  Neither validator asserts formats by default, so behaviour matches today, but the
  agent-session schema declares `format: date-time` and nothing enforces it.
  That is a separate claim-integrity question, not a speed one.
- After the geometry moves, is `exact verification` the right home, or does the grid
  replay belong with the frontier corpus checks that own `E-basic-grid-upper`?

## References

- [`D-369`](../../../../defects.md) — the gate’s cheap checks were hostage to its
  expensive one.
- [`D-370`](../../../../defects.md) — the registry checks were slow because they were
  not registry checks.
- [`D-355`](../../../../defects.md) — a two-file edit verified at `979.79s` against the
  `12.06s` its affected steps need.
- [`D-366`](../../../../defects.md) — the control step outgrowing its own cap.
- `BC-075` in
  [agenda-006](../../../../packing/campaign/agendas/agenda-006-overnight-research-blocks.md)
  — the efficiency block this spec serves.
- [`conventions.md` section 11](../../../../conventions.md) — what the gate actually
  enforces, and the cadence table this spec revises.
- [`operating-rules.md`](../../../../operating-rules.md) — `OR-1` on building the tool,
  and `OR-3` on not waiting on a gate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
