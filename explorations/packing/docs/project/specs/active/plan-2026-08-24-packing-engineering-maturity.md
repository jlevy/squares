---
title: Packing Engineering Maturity and Research-Loop Scalability
description: Plan for separating experimental code from maintained research infrastructure and making refactors safe
author: Codex and project maintainers
date: 2026-08-24
status: draft
---
# Feature: Packing Engineering Maturity and Research-Loop Scalability

**Date:** 2026-08-24

**Author:** Codex and project maintainers

**Status:** Draft

## Overview

Make the packing codebase easier for agents and maintainers to understand, change, and
reuse across successive research loops.
The project needs stronger engineering where code is shared or carries evidence, while
preserving a low-ceremony place for focused experiments and case-specific mathematical
checkers.

The organizing principle is **assurance proportional to reuse and consequence**. Code
that is used by many experiments, persists research state, defines an evidence tier, or
sits on a correctness boundary receives the clearest interfaces and strongest tests.
Code written to answer one narrow question may stay direct and specialized, provided its
scope and evidential role are explicit.

This plan begins with two foundations:

- a visible maturity map that says what each module is for and how much maintenance it
  warrants;
- a layered testing harness that characterizes current behavior before structural
  changes and keeps reusable contracts safe during refactors.

The detailed cleanup inventory will be added incrementally as modules are reviewed.

## Goals

- Reduce the time agents spend discovering which files matter, which behavior is
  authoritative, and which abstractions are safe to reuse.
- Distinguish one-off exploration code, retained case-specific evidence, reusable
  research components, and correctness-critical infrastructure.
- Organize the Python tree into explicit module families for shared foundations, stable
  research-loop tools, and case-specific investigations, with one-way dependency rules
  between them.
- Concentrate API design, documentation, testing, typing, error handling, and
  performance work on code expected to serve future research loops.
- Preserve the freedom to write direct, hypothesis-specific code without prematurely
  generalizing it.
- Establish a fast, deterministic test framework for reusable Python behavior and keep
  the existing integration, replay, exact-check, differential, and negative-control
  layers.
- Make behavior-preserving refactors demonstrably safe through characterization and
  contract tests written before structural changes.
- Keep research artifacts, numerical claims, and generated views traceable to the code
  and contracts that produced them.
- Measure orientation cost, gate cost, and research-loop bottlenecks before optimizing
  them.
- Standardize the Python project on Python 3.14 only, including project metadata,
  lockfiles, lint and type-check targets, CI, scripts, and contributor documentation.
- Bring maintained Python code to the repository’s `tbd` Python and general engineering
  standards: a high lint floor, modern types, explicit errors, atomic output, and
  concise comments and docstrings that explain non-obvious intent.
- Provide clean, self-documenting CLIs that expose reusable operations without
  duplicating their implementations.
- Replace substantial Bash orchestration with typed Python when Python provides clearer
  state, errors, tests, portability, or composition.
- Add a packing `development.md` that gives maintainers and agents one entry point for
  setup, module boundaries, maturity rules, commands, testing, and contribution
  standards.
- Remove obsolete paths, duplicated concepts, stale comments, misleading names, and
  accidental compatibility code when no real consumer requires them.

## Non-Goals

- Turning every script into a reusable library or every mathematical checker into a
  framework extension.
- Rewriting correct proof checkers solely to make their internal style uniform.
- Hiding domain-specific geometry behind generic abstractions with no second real use.
- Replacing the existing packing gate with a conventional unit-test suite.
- Banning every shell script.
  A short shell launcher remains acceptable when it has no meaningful state, branching,
  data parsing, or orchestration logic.
- Treating line count, test count, coverage percentage, or number of modules as a
  quality target by itself.
- Optimizing `sqsearch` or another component without evidence that it limits research
  throughput.
- Adding process steps, compatibility shims, hashes, schemas, or indirection without a
  named failure they prevent.
- Changing mathematical claims, experiment priorities, or evidence standards as a side
  effect of engineering cleanup.

## Background

The packing exploration now combines several kinds of work in one self-contained tree:

- a reusable Python package for geometry, exact arithmetic, quenching, canonicalization,
  and atlas storage;
- a Rust search engine;
- campaign state, schemas, generated ledgers, and a runner;
- reusable operational tools;
- one-off and case-specific exact checkers tied to particular values of `n`, papers,
  hypotheses, or experiment checkpoints;
- retained fixtures, event logs, proof records, and generated views.

The project already has a substantial assurance perimeter.
`test.sh` currently runs 30 steps covering lint and types, Rust checks, independent
packing verification, exact certificates, differential checks, replay, schemas,
generated-file consistency, provenance, historical regressions, and 37 mutation-based
negative controls. The gate passes at the starting revision.

That perimeter does not yet provide an efficient refactoring loop for shared Python
code. `pytest` is available as a development dependency, but there is deliberately no
pytest configuration because the previous configuration collected no actual tests and
reported success. Most checks are executable scripts with embedded self-tests.
This is appropriate for many proof and artifact checks, but it leaves reusable library
behavior without a clearly separated, fast test surface.

The codebase also contains intentional asymmetries that should remain visible rather
than be normalized away.
An exact checker for one theorem and a shared quench routine have different consumers,
expected lifetimes, performance needs, and acceptable interfaces.
Applying the same engineering process to both would either burden the checker or
under-engineer the shared routine.

The current layout does not make these distinctions obvious enough.
Shared library code, stable research-loop machinery, command-line entry points, and
case-specific checks are separated mainly by convention and filenames.
The current `test.sh` is also a large orchestration program with a generic name and
substantial domain assumptions embedded in shell functions.
It should become a clearly named, self-documenting Python command rather than remain a
file that future agents must reverse-engineer to understand the project’s validation
architecture.

## Design

### Approach

Classify first, protect behavior second, and refactor in bounded slices.
Do not begin with a repository-wide reorganization.

For each area:

1. State its purpose, consumers, evidence role, expected lifetime, and current
   limitations.
2. Assign a maturity class based on actual reuse and consequence.
3. Record the observable behavior that must survive cleanup.
4. Add the smallest missing tests or characterization fixtures needed to protect that
   behavior.
5. Make one structural change at a time with the focused tests and packing gate green
   before and after.
6. Update the maturity map when the component’s role or guarantees change.

### Maturity Classes

The classes describe engineering expectations, not scientific importance.
A narrow proof checker may contain the most important result in the repository while
remaining case-specific code.

| Class | Intended use | Engineering expectations |
| --- | --- | --- |
| **E0: Scratch exploration** | Short-lived investigation whose output is not retained as evidence | Optimize for speed of learning. Keep outside maintained import paths. Delete or promote it when the investigation ends. No framework work required. |
| **E1: Retained case code** | A checker, reconstruction, or analysis for a named `n`, source, hypothesis, or experiment | State the exact scope and evidence tier. Retain inputs and outputs needed for replay. Include focused self-tests or negative controls for the failure modes that could invalidate the conclusion. Generalization is optional. |
| **E2: Reusable research component** | Code expected to support multiple hypotheses, values of `n`, proposers, or campaigns | Provide a documented contract, stable typed interfaces, deterministic tests, explicit errors, representative performance measurements, and examples. Avoid case-specific policy in the shared implementation. |
| **E3: Trust or persistence boundary** | Independent verification, exact certification, schemas, artifact persistence, provenance, or orchestration that can misstate research status | Meet E2 expectations plus independent or differential checks, tested failure paths, atomic state changes where applicable, versioned persisted formats, and mutation or negative controls for named soundness failures. |

Promotion is deliberate.
Repeated copying or a second real consumer is evidence that an E1 tool may belong in E2.
Being large, clever, old, or frequently edited is not enough.
Demotion and deletion are also valid when a reusable path has no remaining consumer.

### Module Record

Each reviewed area will get one compact record in this plan or a linked engineering map:

- path and responsibility;
- maturity class and rationale;
- callers, produced artifacts, and external consumers;
- authoritative contract and known limitations;
- required correctness, reproducibility, and performance properties;
- current tests and missing failure coverage;
- cleanup decision: retain, clarify, split, promote, demote, consolidate, or remove;
- acceptance evidence for the change.

This record is the main orientation surface.
It should link to detailed module docs rather than repeat them.

### Provisional Boundaries to Review

These are starting hypotheses, not final classifications:

- `sqpack.verify` and exact-field verification are E3 correctness boundaries.
- campaign schemas, ledger generation, event replay, and durable recording are E3
  persistence or provenance boundaries.
- quench, canonicalization, atlas, worker selection, and shared packing models are E2
  candidates, with some functions approaching E3 because research conclusions depend on
  their semantics.
- `sqsearch` is a reusable proposer and screening engine, but not an independent
  validity oracle.
- theorem-, paper-, and `n`-specific tools under `tools/check_*.py` are generally E1
  retained case code unless they expose a demonstrated shared kernel.
- generated views and retained campaign results are artifacts, not reusable code, and
  should point back to the generator and schema that own them.

### Target Module Families

The inventory will settle exact package names, but the dependency direction is a design
requirement:

```text
case-specific checks and reconstructions
                    |
                    v
stable research-loop tools and commands
                    |
                    v
shared packing foundations
```

**Shared packing foundations** contain the smallest reusable domain library: typed
packing models, geometry predicates, exact arithmetic, verification contracts, common
serialization types, and other mechanisms with multiple real consumers.
They must not import a named packing, hypothesis, campaign round, or value of `n`.

**Stable research-loop modules** contain maintained iterative machinery used across
research rounds: quench and refinement workflows, proposer interfaces, event and atlas
operations, measurements, replay, and campaign-facing services.
These modules may use the shared foundations but must not acquire one-off branches for
Trump, `n=5`, or a single experiment.
Stable CLIs are thin adapters over this layer.

**Case modules** contain retained E1 work for a named configuration, theorem, source,
hypothesis, or value of `n`. Trump reconstruction and certification, Stromquist source
checks, and `n=5` tangent-cone analysis are representative cases.
Each case may use the shared and loop layers, but shared modules never import a case.
A case module can remain direct and specialized; its README or module docstring must
state its question, inputs, evidence tier, retained outputs, and limits.

**Scratch work** remains outside importable maintained packages and is either removed or
promoted to a case module when its result becomes part of the record.

Moving a helper upward requires a second real consumer or a clearly identified common
contract. Similar-looking code is not enough.
Moving policy downward is also important: a reusable layer that contains an `n=11`
exception is a boundary violation to resolve, not a convenience to preserve.

### Python 3.14 and Code-Quality Baseline

Python 3.14 is the sole supported Python runtime for the packing project.
The migration must update every source of version truth together, including:

- `project.requires-python`, the uv lock, and the development environment;
- Ruff’s target version and BasedPyright’s Python version;
- CI and local validation commands;
- scripts, type syntax, standard-library choices, and compatibility branches;
- the packing README and `development.md`.

Until support is deliberately expanded, project metadata should express the same
single-version policy rather than imply untested support for older or newer
interpreters. No Python 3.11-3.13 compatibility aliases or conditionals remain unless a
named external consumer requires them.

The quality floor applies by maturity class.
E2 and E3 code must satisfy the full Ruff and BasedPyright configuration with zero
warnings, use modern and complete types at public boundaries, use absolute imports and
`Path`, preserve exception context, write durable outputs atomically, and keep side
effects at explicit boundaries.
Per-file lint exceptions require a narrow written reason and must not exempt an entire
module from a rule family for convenience.

E1 code remains linted and typed, but may use domain-shaped functions or local data
structures that would be inappropriate in a general API. It is not required to grow
generic interfaces, plugin systems, or configuration layers.

### CLI Design and Naming

Every maintained CLI should make its purpose and operating contract clear from its name
and `--help` output.
Entry points should parse arguments into typed values, call a library or research-loop
operation, and render the result.
Domain behavior does not live only inside argument handlers.

Shared CLI rules:

- descriptive command and file names; avoid names such as `test.sh`, `runner.py`, or
  `check.py` when the surrounding directory is required to understand them;
- concise module docs and command help that state purpose, inputs, outputs, side
  effects, evidence tier, and examples without requiring campaign history;
- machine-readable JSON or JSONL modes for agent and campaign use when output is a data
  contract, alongside concise human-readable output where useful;
- data on stdout, diagnostics on stderr, and nonzero exit status for any partial or
  complete failure;
- explicit non-interactive behavior and no progress decoration in non-TTY contexts;
- one implementation behind programmatic and CLI entry points, with no copy of the
  algorithm in a command wrapper;
- consistent naming for `check`, `verify`, `replay`, `render`, `run`, and `update`, with
  each verb assigned one documented meaning.

The current `test.sh` must be replaced with a name that communicates that it is the
packing project’s full validation gate.
The replacement should offer discoverable step selection, list its checks and tiers,
preserve stable diagnostics and exit behavior, and expose orchestration as testable
Python rather than shell functions.
The exact command name is part of the module and CLI inventory decision.

### Bash Policy

Use Python instead of Bash when a script owns state, parses structured data, coordinates
parallel work, handles timeouts or process groups, performs nontrivial branching, or
needs focused tests.
Those are application responsibilities, and Python provides types, structured
exceptions, deterministic tests, and cross-platform behavior that shell does not.

Bash remains appropriate for a short, transparent launcher or a few direct tool
invocations where its entire behavior is obvious on one screen.
Do not translate tiny shell glue into a Python framework merely for uniformity.
Existing shell files will be classified by this rule; migration priority follows
complexity and failure cost.

### Development Guide

Create `explorations/packing/development.md` and link it from the packing README. It
will be the entry point for engineering work and will include:

- Python 3.14 and uv setup, locked dependency commands, and supported platforms;
- the module tree, dependency direction, and E0-E3 maturity model;
- where to put scratch work, retained case checks, shared foundations, loop tools,
  commands, fixtures, and generated artifacts;
- fast tests, focused checks, the full validation gate, deep checks, and CI;
- Ruff, formatting, BasedPyright, Rust, Markdown, and pre-commit commands;
- CLI design, error, output, naming, and non-interactive conventions;
- the Bash policy and criteria for migrating an existing script;
- the red-green-refactor workflow and rules for reviewing golden changes;
- compatibility, persisted-format, provenance, and atomic-write policies;
- how to profile a full research loop and record a justified optimization;
- links to `tbd` guidelines rather than copied versions that can drift.

The guide documents stable engineering policy.
Research status, current hypotheses, and historical defects remain in their existing
owners.

### Testing and Refactor-Safety Harness

The test system will have distinct layers with explicit jobs:

| Layer | Purpose | Expected scope |
| --- | --- | --- |
| **Fast behavioral tests** | Protect reusable Python contracts during ordinary edits | Pure functions, boundary cases, errors, deterministic state transitions, serialization, and small integration seams. No network, wall-clock dependence, or uncontrolled randomness. |
| **Characterization and contract tests** | Freeze observable behavior before a refactor where the intended contract is not yet isolated | Public outputs, CLI exit behavior, schemas, event shapes, and small stable traces. Characterize only behavior we intend to preserve. |
| **Mathematical and property checks** | Verify domain invariants over representative and adversarial inputs | SAT agreement, containment, exact sign behavior, symmetry invariance, work-budget monotonicity, and similar properties. |
| **Golden and replay checks** | Expose broad stable state changes in complex flows | Human-reviewable artifacts with unstable fields normalized. Semantic tolerances for numerical fields; byte equality only where bytes are the contract. |
| **Negative and mutation controls** | Demonstrate that a guard rejects the named failure it exists to catch | Existing private-snapshot controls plus focused additions for new trust boundaries. |
| **Full packing gate** | Integrate every evidence and infrastructure layer | Current `test.sh` responsibilities, moved behind a descriptive Python command and kept as the final local and CI gate rather than duplicated inside pytest. |

The likely fast Python runner is pytest because it is already locked as a development
dependency and supports focused test selection.
Adopting it requires safeguards against D-004’s false-green failure:

- tests live in an explicit directory and use unambiguous names;
- the gate fails on empty collection and asserts that the intended test surface ran;
- proof scripts ending in `_test.py` are renamed or excluded deliberately rather than
  being accidentally collected;
- the pytest step is only one named layer of the full validation command;
- no checker is migrated merely to increase pytest’s test count.

Before changing a reusable component, add or identify tests for its current observable
contract.
When current behavior is wrong, write a failing test for the corrected contract
instead of blessing the defect as a characterization fixture.
Structural and behavioral changes remain separate.

### Orientation Surface

The packing README should lead a new agent to a compact engineering map that answers:

- Where do I put a disposable probe, retained case checker, reusable module, or
  correctness boundary?
- Which command gives fast feedback for the module I am changing?
- Which artifacts and research claims consume this code?
- What is exact, solver-polished, floating-point screening, provisional, or generated?
- What limitations and open defects constrain reuse?
- What must pass before a result or refactor can be retained?

The map should describe the present design.
Historical defects remain in the defect log and Git history unless the history is
necessary to understand a current constraint.

### Backward Compatibility Requirements

- **Internal code:** **DO NOT MAINTAIN** by default.
  Update repository-owned callers, tests, and docs together; do not retain aliases for
  hypothetical consumers.
- **Library APIs:** Verify whether `sqpack` has an external consumer before breaking a
  public surface. If none exists, **DO NOT MAINTAIN**. If one exists, name it and choose
  the smallest coordinated migration or deprecation.
- **Server APIs:** **N/A**; none are currently identified.
- **Plugin and extension APIs:** **N/A**; none are currently identified.
- **CLI contracts:** Treat campaign recipes, retained commands, and agent automation as
  real repository-owned consumers.
  Update them together and test exit codes and structured output.
  Preserve old forms only when a non-coordinated consumer is named.
- **File formats:** **VERSION + FAIL FAST** for persisted campaign, atlas, event, and
  certificate formats.
  **MIGRATE** only when retained data from an older emitted format must remain readable.
- **Persisted client state:** **N/A** unless a future interactive atlas introduces it.
- **Database schemas:** **N/A**; no database is currently identified.

## Implementation Plan

### Phase 1: Classification and Safety Foundation

- [ ] Inventory Python, Rust, shell, campaign, and generated-code surfaces by purpose,
  callers, evidence role, and expected lifetime.
- [ ] Assign provisional E0-E3 classes and review ambiguous boundaries with the project
  maintainer.
- [ ] Define the concrete shared-foundation, stable-loop, case, command, and scratch
  module layout and enforce its one-way dependency rules.
- [ ] Record existing checks against each reusable or trust-boundary component and
  identify unprotected behavior needed for refactoring.
- [ ] Establish the explicit fast Python test layout and runner, including a
  negative-controlled failure on empty or missing test collection.
- [ ] Add a focused-test command surface so agents do not need the full gate for every
  edit.
- [ ] Add characterization and contract tests for the first reusable cleanup targets
  before moving or splitting code.
- [ ] Move the whole project to Python 3.14 only and align metadata, uv, Ruff,
  BasedPyright, CI, commands, and documentation.
- [ ] Define semantic golden comparison for numerical outputs and retain exact byte
  comparison only for fields whose bytes are contractual.
- [ ] Replace `test.sh` with a descriptively named Python validation command with
  discoverable steps, focused selection, structured failures, and tests of its
  orchestration.
- [ ] Inventory remaining Bash and migrate scripts that own application logic; retain
  only bounded, transparent shell glue.
- [ ] Run the complete packing gate from a clean checkout in CI and retain local focused
  and full-gate workflows.
- [ ] Write `development.md`, publish the compact engineering map, and link both from
  the packing README.

### Phase 2: Incremental Cleanup and Maturation

- [ ] Prioritize cleanup by repeated orientation cost, correctness risk, and measured
  research-loop waste rather than file size alone.
- [ ] Clarify or split modules that mix case-specific policy with reusable mechanisms.
- [ ] Move named packing, theorem, hypothesis, and `n`-specific logic into explicit case
  modules without forcing it through reusable APIs.
- [ ] Consolidate duplicate implementations only after identifying the shared contract
  and a second real consumer.
- [ ] Remove dead paths, stale comments, misleading maturity claims, accidental
  wrappers, and unsupported compatibility branches.
- [ ] Make shared CLI and persistence failures explicit, actionable, and covered by
  failure-path tests.
- [ ] Profile reusable hot paths under representative research loops, then optimize the
  measured bottlenecks behind unchanged contracts.
- [ ] Review each completed area against its maturity class and update the engineering
  map, tests, and linked beads in the same change.
- [ ] Reassess whether any retained E1 code has earned promotion or should be archived
  after each research loop.

## Testing Strategy

Every cleanup bead must name the behavior at risk and the smallest test layer that
protects it. The default refactoring loop is:

1. Run the focused existing tests and capture the baseline.
2. Add a failing contract test if the desired behavior is absent, or a characterization
   test if correct behavior exists but is unprotected.
3. Make one structural change without changing the contract.
4. Run the focused tests after each step.
5. Run lint, types, and the relevant mathematical or replay checks.
6. Run the full packing gate at the integration checkpoint.
7. Review any fixture or golden diff as a behavior change; never regenerate it solely to
   make the gate green.

Tests should be few, behavior-focused, deterministic, and independent of implementation
details. Failure paths and exit codes are part of the contract.
Exact and differential checks remain separate implementations where independence
supplies the assurance.

The harness itself needs tests proving that it can fail: an empty collection, a changed
stable golden field, a numerical change outside tolerance, a schema mismatch, and a
known invalid packing must all make their owning layer red with an actionable message.

## Rollout Plan

- Land the maturity model, module inventory, and test-harness foundation before broad
  file moves or API cleanup.
- Migrate one reusable boundary at a time.
  Keep the old and new paths only when a named consumer prevents a coordinated change.
- Keep the full packing validation command green at integration checkpoints and make CI
  exercise the same locked environment from a clean checkout.
- Do not interrupt active research experiments for cosmetic cleanup.
  Apply the model to touched modules first, then address high-cost untouched areas
  through explicit beads.
- Treat changes to persisted formats, numerical semantics, evidence tiers, or exact
  claims as behavioral work with their own review and migration decisions.

## Initial Work Areas

This section will become the prioritized cleanup inventory.
Each entry must use the module-record fields above and link to an implementation bead.
Initial candidates are:

- testing layout and focused command surface;
- module maturity and ownership map;
- shared-foundation, stable-loop, and case-module boundaries;
- Python 3.14-only migration and uniform tool configuration;
- descriptive CLI naming and a reusable command architecture;
- migration of the full validation gate from `test.sh` to Python;
- Bash inventory and migration of scripts with application logic;
- packing `development.md` and README routing;
- `sqpack.quench` responsibilities, contracts, termination, and numerical stability;
- canonical identity and atlas observation boundaries;
- campaign runner, ledger, persistence, and CLI error contracts;
- reusable geometry and exact-verification boundaries;
- case-specific checker layout and naming;
- generated artifacts and schema ownership;
- gate composition, selection, diagnostics, and CI;
- performance measurement around the quench-dominated research loop.

## Open Questions

- Should the maturity map live in the packing README, a dedicated engineering document,
  or a small machine-readable manifest rendered into documentation?
- What exact package names best express shared foundations, stable research-loop tools,
  and case modules without creating unnecessary distributions or import layers?
- Which `tools/` modules already have multiple consumers and belong in `sqpack`, and
  which only look reusable because they are large?
- Should campaign infrastructure remain packing-specific or expose a reusable kernel for
  future explorations?
- What is the smallest pytest surface that materially improves refactor safety without
  duplicating script-level proof checks?
- Which numerical outputs need semantic comparison, and what domain-derived tolerances
  distinguish harmless solver variation from changed research meaning?
- Which public `sqpack` and CLI surfaces have consumers outside this repository?
- What descriptive name should replace `test.sh`, and should it be exposed as a
  `pyproject.toml` console script or a directly runnable module?
- Which gate steps belong in the fast edit loop, the ordinary integration gate, and an
  explicitly requested deep verification tier?

## Bead Map

`think-9a7v` is the existing engineering epic and now owns this plan.

| Workstream | Beads | Relationship |
| --- | --- | --- |
| Classification and runtime foundation | `think-xdyv`, `think-jc1a` | Module inventory and Python 3.14-only baseline can begin independently. |
| Refactor-safety harness | `think-k1jj` | Blocked by the inventory and Python 3.14 baseline; precedes broad structural cleanup. |
| Module segregation | `think-8waf`, `think-1eij` | Shared, loop, and case boundaries follow the inventory and harness. |
| CLI and shell cleanup | `think-5u59`, `think-dbn6`, `think-9rzc` | Define command contracts before replacing the validation gate or other substantial Bash. |
| Python quality | `think-l03z` | Applies the full quality floor after runtime, tests, and module boundaries are established. |
| Engineering guide | `think-hf1u` | Records the implemented runtime, structure, commands, and validation workflow in `development.md`. |
| Numerical refactor safety | `think-sk15`, `think-lwao`, `think-9qz0`, `think-u97a` | Existing beads retained and linked here; they define stability, golden semantics, termination, and work-budget constraints. |
| Validation infrastructure | `think-lrsk`, `think-cns0` | Existing CI and bounded negative-control work retained; CI waits for Python 3.14 and the replacement validation command. |
| Measured optimization | `think-y91x`, `think-uvmb`, `think-r33j` | Existing performance work retained. Quench optimization now waits for basin stability and semantic golden comparisons. |

Related beads stay with their existing research or review specs because those documents
own their acceptance criteria:

- `think-xzew` profiles the end-to-end research loop, and `think-rthe` acts on measured
  negative-control latency;
- `think-ldq2` owns the campaign trust boundary and lifecycle;
- `think-lcfd` owns two already identified misleading code contracts;
- `think-ugt1` owns atlas drift coverage in the validation gate;
- `think-krqi` owns pair-test accounting as the research budget currency.

Implementation beads must reference rather than duplicate these contracts.
If cleanup absorbs one of them, reconcile its acceptance criteria and ownership before
closing or reparenting it.

## References

- [Packing README](../../../../README.md)
- [Packing synopsis](../../../../SYNOPSIS.md)
- [Packing conventions](../../../../conventions.md)
- [Campaign runbook](../../../../campaign/README.md)
- [Minimal Packing Toolkit](plan-2026-08-22-minimal-packing-toolkit.md)
- [Unattended Square-Packing Research Readiness](plan-2026-08-23-overnight-cartography-run.md)
- `think-9a7v` — engineering-maturity epic linked to this plan

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
