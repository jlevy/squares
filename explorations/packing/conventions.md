# Conventions for `explorations/packing/`

**The definitive registry of every convention and naming this project uses.** Where
another document restates an id or naming convention, this one wins.
Changing program status remains owned by `SYNOPSIS.md`, and schemas and source artifacts
remain authoritative for their own fields and evidence.
Read this before adding an artifact, workflow phase, round, series, or tool.

Each rule is marked **[checked]** when something fails on a violation, or
**[convention]** when it rests on care alone.
The distinction is the point: a rule nothing enforces is a rule that will drift, so the
standing goal is to move rules from the second column to the first.
`packing-validate` is the authoritative checking surface.

## 1. Identity

One id per thing, three digits, never reused.
The prefix says what kind of thing it is.

| Layer | Id | Scope | Example |
| --- | --- | --- | --- |
| Campaign | contract namespace | the directory | `packing.squares` |
| Series | `series-NNN` | campaign | `series-000` |
| Experiment | `exp-NNN` | **campaign, not series** | `exp-003` |
| Hypothesis | `H-NNN` | campaign, spans series | `H-016` |
| Exploration report | `X-NNN` | campaign | `X-001` |
| Agent session | `session-NNN` | campaign | `session-001` |
| Agenda | `agenda-NNN` | campaign | `agenda-001` |
| Agenda cell | `AA-NNN`, prefix declared per agenda | its agenda | `BC-001` |
| Frontier case | `n-NNN` | `frontier/`, one artifact per `n ≤ 100` | `n-011` |
| Search/proof strategy | `search:N`, `proof:N` | the frontier catalogues | `search:12` |
| Defect | `D-NNN` | the directory, logged in `defects.yaml` | `D-014` |
| Bead | `think-xxxx` | the repository’s `tbd` queue (prefix set in `.tbd/config.yml`) | `think-1s0h` |
| Theoretical result | `T-N` | `SYNOPSIS.md` shorthand; the registry artifact it cites is authoritative | `T-2` |
| Review finding | `R-N`, `F-NN` | the review document that declares them | `R-2`, `F-07` |
| Basin (planned) | canonical key, plus a `B-NNN` alias | campaign, spans series | — |

**Experiment ids do not restart at `exp-001` in each series, and this is deliberate.** A
series is a directory and a field, not a namespace.
`exp-003` names one experiment record forever, wherever it lives, which is what makes
cross-series references work—and they are common: a series’ `carries_forward` names
rounds from an earlier one, a hypothesis aggregates rounds across all of them, and the
atlas will cite the round that discovered a basin.
Per-series numbering would make every one of those a compound key, and a bare `exp-001`
in prose would be ambiguous.

The series is never lost, because the experiment records it in a `series:` field and
lives in that series’ directory.

`series-000` predates strict application of this boundary and now contains heterogeneous
calibration and exact-determination work.
Its
[series note](campaign/series/series-000-smoke-and-calibration/README.md#current-scope-and-safe-reading)
states the safe reading; `think-i08r` owns the all-at-once record migration.
Do not use that legacy container as the template for opening another series.

One experiment artifact records one round of research.
Use **round** for the performed work or its sequence position and **experiment** for the
durable `exp-NNN` record.
A lower-level **run** is one command invocation or seed trial; one experiment may
aggregate many runs.
Agent sessions have their own `session-NNN` ids and may produce zero or many
experiments.

**Cardinality**, so the shape of the record is unambiguous:

| Relation | Cardinality |
| --- | --- |
| experiment → series | exactly one |
| experiment → hypotheses | **exactly one** under the current contract; the field remains an array for format compatibility |
| hypothesis → experiments | zero or more—sweep cells and replications |
| hypothesis → exploration reports | zero or more (`derived_from`) |
| hypothesis → strategies | zero or more (`strategy_refs`) |

So `exp-` does **not** map one-to-one onto `H-`: one hypothesis may aggregate many
experiments. Four experiments currently reference `H-016`: one historical three-cell
round and its three per-cell replacements.
A round does not apply its one verdict to several hypotheses.

**Ids are never reused, and never renumbered except on merge collision.**
[checked: whole-set uniqueness] When two branches collide, the newer campaign renumbers
and the change is recorded as an annotation on the affected artifacts, never as a silent
edit.

**Reserved ids.** [checked] No hypothesis ids are currently reserved.
A future reservation is declared in a `reserved-ids` comment on the idea board and names
a claim that exists upstream but is not yet codified.
A reserved id may be *named* but not *linked*, and a reservation that has been fulfilled
is flagged stale.

## 2. Naming

**Files and directories carry the full id followed by a kebab-case slug.** [checked]

```
campaign/series/series-000-smoke-and-calibration/
campaign/series/series-000-smoke-and-calibration/experiments/exp-003-baseline-n11-target.md
campaign/hypotheses/H-002-lp-in-cell-polish.md
campaign/explorations/X-001-standing-review-and-search-philosophy.md
campaign/agent-sessions/session-001-pr15-review-reset.md
campaign/series/series-000-smoke-and-calibration/results/exp-003-baseline-n11-target.jsonl
```

The id in the filename must equal the id in the frontmatter.
[checked] Raw run data takes the id of the round that produced it.

Research documents and reviews keep the repository’s dated form:
`research-YYYY-MM-DD-topic.md`, `review-YYYY-MM-DD-topic.md`.

Use [`repren`](https://github.com/jlevy/repren) for renames—it moves files and rewrites
references in one pass, which is what keeps the two in step.

## 3. Artifacts

**Frontmatter is authoritative; the body is for people.** [checked: schema] A consumer
reads the YAML and must not parse prose for structured values.
The body carries the judgement, the history and the caveats—the things that would be
lies if forced into a field.

**Every artifact declares its schema and is validated against it.** [checked]
`status: enforced` means something fails when the artifact is wrong.
An artifact that declares a schema nothing loads is the exact failure this project keeps
finding in its own sources.

**Promote a value into YAML only when something consumes it**—the accept rule, the
ledger, the checker.
[convention] Everything else is prose.

**Cross-field rules live in the checker, not the schema.** [checked] softschema 0.6.2
rejects `allOf` object composition under `status: enforced`, so a conditional would
invalidate every artifact rather than the offending one
([jlevy/softschema#41](https://github.com/jlevy/softschema/issues/41)).

### Workflow, Focus, Phase, and Slice

**Workflow names purpose and output; focus names the primary quality emphasis.**
[checked for agent sessions] The six numbered workflows and their full contracts live in
[`SYNOPSIS.md`](SYNOPSIS.md#workflow-entry-contracts).
One independently tracked session phase declares one workflow and one primary focus; the
other principles still constrain and may contribute to the work.
`general-improvement` is reserved for genuine repository maintenance outside W1–W6, not
a label for mixed or ordinary core work.

**Implementation stays with its owning workflow.** [convention] Bounded research
corrections stay in W1 or W2, idea probes in W3, process and checker repairs in W4,
measured optimizations in W5, and registered instruments in W6 before measurement.
There is no undefined implementation handoff.

**A phase is contiguous; a slice is bounded.** [checked for phase history] Start a new
phase when workflow or focus changes.
A focus-only change repeats the workflow and is not a workflow switch.
A slice is one time-bounded action inside the phase and need not produce an experiment.
Mechanical delegations inherit the coordinating phase unless they open independently
tracked sessions.

**Current transitions are recorded before the new work begins.** [checked] A phase opens
with its expected output, validation command, kill condition, fallback, start, and
deadline. Its actual outcome and evidence are terminal fields.
The first phase uses `session_start` and no switch reason; later phases name a planned
checkpoint, evidence checkpoint, or user request, and close the old phase before
entering the new one.
Sessions 001–008 predate this convention.
Their v2 workflows are retrospective reconstructions from retained evidence and are not
preregistration evidence.

## 4. Evidence

**Three tiers, and each says what a number may claim.**
[checked: recorded in `subject.precision`]

| Tier | Instrument | May claim |
| --- | --- | --- |
| `f64_screen` | `sqsearch` | a candidate was proposed |
| `polished` | LP-in-cell quench | a numerical endpoint candidate, valued to solver precision |
| `exact` | `sqpack` over ℚ(α) | validity—and only here, a record |

**`beat_record: true` may only be written at `precision: exact`.** [convention] A record
packing has pairs touching at exactly zero separation; no floating-point check can
decide those.

**Claims are separated by evidential status**—proved, computationally verified, best
known, or asserted-but-unverified—and citations sit near the claims they support.
[convention]

**Budgets are in pair-tests**, tiers S/M/L = `1e9`/`1e11`/`1e13`. [convention]
Machine-independent, and comparable across proposers whose move semantics differ.
Wall clock is reported alongside as a courtesy, never as the budget.

**Two things compared at different budgets have not been compared.** [convention]

## 5. Provenance

**Numbers are lifted from run data, never retyped.**
[convention, spot-checked by review] The tables in a round’s body are derived from its
archive.

**An archive must regenerate what its round claims.** [checked for the current rounds]
Every archived record re-derives its own reported side from its own coordinates.

**A recorded commit must be an ancestor of the branch being merged.** [convention]
`exp-001` violates this—its commit was orphaned by a rebase—and carries an annotation
saying so.

**Guards are recomputed, not remembered.** [checked: selftest] The overlap reported for
a configuration is recomputed from that configuration, never read off an accumulator
maintained across hundreds of millions of updates.

## 6. Corrections

**The record is corrected by addition, never rewritten.** [convention] A defective
artifact gets a dated annotation stating what still stands and what does not.
`exp-001` carries three.

**Views are generated and never hand-edited.** [checked: drift] `campaign/ledger.md` and
the frontier tables inside the research documents rebuild from their artifacts; the gate
fails if a committed view is stale.
Generated files are excluded from formatting, because a formatter and a generator will
fight forever.

**The idea board is the one hand-written link in the chain.**
[checked: two-way reconciliation] It is an *input*, not a view, so it is reconciled
against the registry rather than regenerated: every `H-NNN` it names exists, and every
registered hypothesis appears on it.

## 7. Ownership

**Once codified, the registry artifact is canonical.** [convention] The standing
review’s register entry becomes historical.
Beads track build work, never scientific claims—a bead may say “build the instrument for
H-002”, never “H-002 is confirmed”.

**One series is open at a time.** [checked]

**The runbook is frozen while rounds are running.** [convention] The accept rule, the
tolerances, the metric vector and the control cells do not change mid-series.

## 8. Layers That Must Not Blur

**`sqpack` owns validity.
`sqsearch` owns move-loop energy.** [checked: differential test] `pair_depth` is a
metric shaped for annealing, not a verdict, and a second implementation at that layer is
fine—as long as it never gets to say what is valid.
20,000 near-contact pairs are checked against the oracle on every full validation run.

**Proposers propose and nothing else.** [convention] A proposer never quenches,
canonicalizes, decides validity, or writes the atlas, so a new strategy cannot change
what a basin means.

**The vocabulary is fixed, and controlled collisions are explicit.** [convention]
[`SYNOPSIS.md`](SYNOPSIS.md#terminology) defines every term this directory uses in a
narrow sense—campaign, session, experiment, round, run, quench, basin, polish,
exploration, gap, tier, pair-test and the rest—and those definitions apply in artifacts,
beads and reviews.
Write **packing exploration** for the project directory, **exploration
report** for `X-NNN`, and bare **exploration** for reaching another basin.
Write **cell** alone for a cell of configuration space—a choice of separating axis and
order for each pair—and **instance cell**, never bare “cell”, for a position in a sweep.
The two are unrelated objects and the confusion is expensive: one is where the LP is
solved, the other is what a round is run on.

## 9. Code and Docs

**Python first; accelerate what a profile says is slow, not what looks slow.**
[convention] The measurements behind this are in the
[plan spec](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md#stack-and-boundaries--decided-by-measurement).

**Python 3.14 is the sole supported runtime, and dependencies are locked.** [checked]
`pyproject.toml`, `.python-version`, Ruff, BasedPyright, CI, and `uv.lock` express one
runtime policy. Development commands run through the locked uv environment described in
[`development.md`](development.md).

**Code is segregated by maturity and consequence.** [checked] Maintained foundations,
reusable research components, case-specific evidence, developer tooling, and tests live
in separate module families.
The dependency rules and E0–E3 expectations are defined in
[`development.md`](development.md#code-maturity-and-placement).

**Markdown is formatted by flowmark**, automatically on commit.
[checked: hook] Exclusions are evidence-based, not precautionary, and each one states
its measured reason in [`.flowmarkignore`](../../.flowmarkignore).

**Relative links must resolve.** [checked] The campaign’s checker walks every relative
Markdown link. This project has needed that twice.

**Docs follow the common documentation guidelines** and carry the footer.
[convention]

## 10. What the Gate Actually Enforces

`packing-validate` runs thirty-one read-only steps concurrently and replays their output
in declared order. `packing-validate --list` prints the authoritative names and tiers;
the `STEPS` table in `src/sqpack/cli/validate.py` is the only registration point.
What they enforce, grouped:

**Mathematics, checked exactly where the claim is exact.** Exact verification of Trump’s
packing and the negative control showing why float cannot do it; the degree-8 field
re-derived independently (where sympy is installed); the fixed-angle cell rebuilt as a
linear program through independent constraint rows and solved back to Trump’s packing;
Trump’s exact branchwise linearized cones (exp-013); the H-041 repaired-cover exact
certificate and the H-010 printed-cover exact rejection (exp-016, exp-017); the exact
`n = 3, 4` optimal moduli (exp-014, exp-015); and the golden basin maps, whose
proved-case rows are checked against mathematics rather than against a stored snapshot.

**Instruments.** `sqsearch --selftest` (geometry against a naive reference, determinism,
the `s(5)` positive control, the recomputed-overlap guard); the differential test
between search energy and the validity oracle; the basin atlas store invariants; the
basin event record and its replay; basin identity; and the historical regressions each
earlier defect fix left behind.

**The record.** Frontier corpus structure and its soft-schema validation; generated
tables in sync with the frontier data; both strategy catalogues; the defect log (schema,
contiguous ids, open defects carrying beads, links resolving, the generated view in
sync); `SYNOPSIS.md` and `README.md` reconciled against the artifacts and the directory;
the campaign record (schema validation, id uniqueness, dangling references, verdict
rules, idea-board reconciliation, ledger freshness); provenance (every round’s recorded
engine commit reachable, or annotated); the bead tree; and the skills mirrored between
`.agents` and `.claude`.

**Hygiene.** The lint floor (ruff, ruff-format and basedpyright on the Python; clippy
pedantic and rustfmt on the Rust); the soundness perimeter (every component that emits a
configuration is checked by `sqpack` through code it does not share); and the negative
controls in `devtools/controls.yaml`, each a mutation that must be caught in a private
source snapshot.

A skipped check is recorded and re-listed at the end.
`--strict` enables deep golden regeneration and turns every skip into a failure; failed
or incomplete strict surfaces always return nonzero.

**Run the cheapest loop that answers the current question.** The research round is
deliberately separate from the edit/test loop, so an eight-hour hypothesis never makes a
documentation correction take eight hours to validate:

| Loop | Target latency | Use |
| --- | ---: | --- |
| Interactive | under about 2 seconds | Pytest, ledger and schema checks, exact-witness verification, engine self-test |
| Focused | under about 60 seconds | `packing-validate --fast` or `packing-validate --only TEXT` for one component and its controls |
| Checkpoint | about 2 minutes | Normal `packing-validate` before a commit, push, or cross-component handoff |
| Deep handoff | about 5 minutes | `packing-validate --strict` before an unattended campaign, major handoff, or merge |
| Research round | preregistered per hypothesis | Candidate generation or proof search under its own declared timebox |

These are working envelopes, not promises; repeated versioned benchmarks and warm/cold
regimes remain tracked work.

Everything else on this page is convention, and convention is what drifts.
When a rule here is broken and nothing catches it, the fix is a check, not a reminder.

## Defect Classes

One taxonomy, used by [`defects.yaml`](defects.yaml), by the beads (as a `defect-class:`
label), and by any review that reports a problem.
They are separated because they cost completely different things, and treating them
alike is how a critical bug gets the same attention as a stale link.

| Class | The system … | Costs |
| --- | --- | --- |
| **soundness** | asserted something false about the mathematics | a wrong published result; the only class that can |
| **validity** | was correct, but the measurement did not bear on the question | an empty experiment, and the budget spent on it |
| **bookkeeping** | recorded something its own evidence contradicts | misdirected future work; an archive nobody can trust |
| **robustness** | did not finish, or finished only by luck | time, and silently censored data if papered over |
| **performance** | worked, but cost far more than it should | throughput, and the experiments not run because of it |

Soundness and validity defects additionally record a **direction**: `flattering` errors
overstate the result and are the dangerous kind, because they look like success;
`conservative` errors understate it and cost only effort.
Four of the six soundness defects found so far flattered.
[checked]

A soundness defect gets a postmortem, not just a fix—see
[the first one](docs/project/postmortems/postmortem-2026-08-23-soundness-class.md),
whose rules R1–R4 apply to code that does not exist yet.
[convention]

## Defects

Every defect found in this toolchain is recorded in [`defects.yaml`](defects.yaml) and
rendered to [`defects.md`](defects.md).
A defect is a bug, an inefficiency, or a record that disagreed with its evidence—not an
approach tried and rejected on its merits, which belongs in `campaign/ideas.md` under
Dead ends.

Two fields carry most of the value and are worth filling in honestly rather than
generously. `detected_by` says what *actually* caught it, which is how we learn which
detectors to build more of.
`regression` names the check that now prevents recurrence, and the literal `none` is a
legitimate and useful answer—the generated view collects those into the list that
predicts what will come back.
[checked]

Open defects must carry a bead, soundness and validity defects must state whether the
error flattered or understated the result, and every row must point at the artifact
carrying its narrative.
[checked]

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
