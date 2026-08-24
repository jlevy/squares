# Square Packing

A self-contained project directory: the research reports, the local archive of the
literature they cite, the exact verifier and search engine, and the experiment record of
running them.

`s(n)` is the side of the smallest square holding `n` non-overlapping unit squares.
The motivating case is `n = 11`, the smallest instance of this problem that is still
open. Its best known packing dates from 1979 and its best proved lower bound from 2003,
and a gap of roughly 0.088 in the side length separates them.

The work runs on four principles held in balance—correctness, process, insight, and
efficiency—each worked by its own kind of loop, and joined by one **research loop**:
insight agents produce hypotheses, the research loop tests each as a preregistered
experiment against the tooling, correctness decides every verdict at a declared evidence
tier, and process records all of it.
[Operating Principles](#operating-principles) below defines each principle and sketches
the loop; the [campaign runbook](campaign/README.md) runs it.

**New here?** [`TUTORIAL.md`](TUTORIAL.md) is the first-principles orientation: what the
objects are, why the approach is shaped the way it is, and what is established versus
open. Read it once, then [`SYNOPSIS.md`](SYNOPSIS.md) for the state of the program.

## Operating Principles

Successful research here is the result of four principles held in balance.
None can stand in for another, and each has a preeminent goal:

| Principle | Agent focus | Preeminent goal |
| --- | --- | --- |
| **Correctness** | Soundness | Formal validation checkable by third parties, and cross-validation of every claim and report against known research—accurate surveys of prior work included |
| **Process** | Discipline | Operational discipline: results delivered efficiently, priorities balanced, and every piece of work traceable to what happened and when |
| **Insight** | Creativity | Extreme freedom to understand the problem creatively and to form a wide range of hypotheses, using all available information and tooling |
| **Efficiency** | Infrastructure | Iteration on every layer of the stack, as fast as possible, through efficient algorithms and systems engineering |

Balance carries one asymmetry.
Correctness and process hold vetoes—no claim is promoted past its evidence, and no run
counts if it cannot be reconstructed—while insight is never blocked from proposing, and
efficiency may never relax either control to go faster.

### How each principle is worked

Deep work on a single principle is one mode, not the only one, and the four are staffed
differently:

- **Correctness and process are structural first.** The schemas, the gate,
  preregistration, and provenance were set up early and now largely enforce themselves.
  The ongoing mathematical flow is survey work—reviewing, fact-checking, and assembling
  everything known on a topic soundly—and finding and validating the right mechanisms
  for formal verification of key claims and new results.
- **Efficiency runs as performance loops**: dedicated agentic loops measured purely by
  declared performance metrics—gate wall time, solver throughput, pair-tests—so an
  improvement is a number moving, never an impression.
- **Insight runs as dedicated agents** whose job is extreme context efficiency: absorb
  the full current research context, then hypothesize a wide range of connections worth
  pursuing—separately, at whatever depth is needed, by whichever agents or models do it
  best. Output arrives as explorations and candidate hypotheses, never as unrecorded
  opinions.

### The research loop

The architecture that ties the four together is a loop between insight and experiment:

```
insight loop ──> hypotheses ──> preregister ──> run rounds ──> validate ──> record
  (X-NNN)          (H-NNN)     (kill criteria,    (exp-NNN)    (evidence    (ledger,
     ^                          budgets, tiers)                  tiers)      defects)
     └────────── verdicts and negative results return as evidence ──────────────┘
```

An insight phase runs until it has produced a batch of candidate hypotheses.
Each is codified in the registry with a kill criterion and a budget before anything
runs; the research loop then executes them as preregistered experiment rounds against
the tooling; every verdict is decided at a declared evidence tier and recorded in the
generated ledger; and every verdict—refutations and negative results above all—returns
to the next insight phase as evidence rather than discarded work.
In one line: **Insight proposes → Process preregisters → Efficiency executes →
Correctness validates → Process records.**

The loop’s mechanics are already codified: the campaign runbook’s
[bounded research cycle](campaign/README.md#the-bounded-research-cycle) is its clock and
checkpoint protocol, the agenda queue orders its cells, and the
[ledger](campaign/ledger.md) is generated from the artifacts rather than typed.

### The record, by id

Every artifact the loop touches carries a typed id.
The one-line meanings; [`conventions.md`](conventions.md) owns the id rules and
[`SYNOPSIS.md`](SYNOPSIS.md#terminology) the full definitions:

| Id | Names |
| --- | --- |
| `H-NNN` | A registered hypothesis or open question, with its kill criterion and budget written before any run |
| `X-NNN` | An exploration report: the recorded idea source hypotheses are mined from |
| `exp-NNN` | One experiment round: a schema-validated artifact plus its raw JSONL archive |
| `series-NNN` | An ordered group of rounds sharing a runbook; only one open at a time |
| `session-NNN` | One agent session: objective, budget, delegation evidence, stop reason, and handoff |
| `BC-NNN` | One cell in an agenda’s priority queue, currently the basin-map confidence ladder |
| `D-NNN` | One defect: what went wrong, what caught it, and what now stops it recurring |
| `T-N` | The synopsis’s shorthand for a theoretical result established in this repository |
| `think-xxxx` | One bead: a tracked work item in the `tbd` queue |

The basin atlas is the flagship cross-focus instrument.
Insight specifies views that could expose mathematical structure—symmetry orbits,
terminal components, contact types, observed transitions, continuation across `n`, and
proposer-conditioned frequency with uncertainty.
Efficiency makes those views responsive, traceable, and reproducible as both an
interactive explorer and deterministic review snapshots.
Process owns the underlying event and provenance contract; Correctness decides which
relations are observed, inferred, or certified.
A visual embedding is never evidence by itself that two basins are adjacent or that a
sampled cluster is a connected component.

The operating documents divide ownership rather than repeat one another:

| Document | Owns |
| --- | --- |
| [Campaign runbook](campaign/README.md#the-bounded-research-cycle) | Portable slice protocol, clocks, result routing, and experiment rules |
| [Agent sessions](campaign/agent-sessions/README.md) | Versioned objective, budget, delegation evidence, stop reason, and handoff |
| [Basin confidence ladder](campaign/agendas/agenda-001-basin-confidence-ladder.md) | Mutable, size-by-size priority queue separating tool validation, measurement validation, and genuine research |
| [Current launch agenda](docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md) | Broader scientific and operational readiness; the agent loop can work now, while the generic numerical runner remains a no-go |
| [Program review](docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md#the-epic-and-its-bead-map) | Four-focus epic, durable findings, and bead map |

## The Autonomous Work Loop

The outer loop is a portable repository protocol, not a feature of one agent platform.
The `tbd` queue owns ready work, an agent-session artifact owns the current objective
and clocks, and commits plus research artifacts own the evidence.
A native long-running goal, periodic watchdog, scheduler, or human may drive that
protocol. For example, Codex can use a
[durable goal](https://learn.chatgpt.com/use-cases/follow-goals) and a scheduled
watchdog; Claude or another coding agent can use its corresponding continuation and
timer facilities. No platform-only state is authoritative, so changing agents does not
change the work.

Breadth lives in [`campaign/ideas.md`](campaign/ideas.md), the hypothesis registry, and
the bead queue. Narrowness lives in the active slice: one focus, one primary bead, one
question, one promised artifact, and one hard wall-clock bound per agent.
A new idea found mid-slice is recorded and returned to the queue unless it invalidates
the current measurement.
The exact clock and checkpoint protocol is the campaign runbook’s
[bounded research cycle](campaign/README.md#the-bounded-research-cycle).

The outer loop chooses and integrates work; [`campaign/runner.py`](campaign/runner.py)
remains the smaller tool that executes already-preregistered numerical rounds.
Do not turn the runner into a second project manager.

Each autonomous cycle names one focus, one primary bead, one measurable outcome, a
budget, and explicit stop conditions in a versioned
[agent-session artifact](campaign/agent-sessions/README.md).
It then selects one bounded action, delegates independent pieces, runs the narrowest
adequate check, integrates the evidence, updates the durable record, and repeats.
A delegated result is not complete until the parent can see its **outcome, evidence,
files or artifacts, checks, remaining uncertainty, recommended next action, and elapsed
wall time**. The parent owns integration and shared files; delegates receive disjoint
write scopes or read-only briefs.

Use the cheapest loop that answers the current question:

| Loop | Target latency | Use |
| --- | ---: | --- |
| Interactive | under about 2 seconds | Status, ledger and schema checks, exact-witness verification, engine self-test |
| Focused | under about 60 seconds | One changed component and its named negative control |
| Checkpoint | about 2 minutes | Normal `./test.sh` before a commit, push, or cross-component handoff |
| Deep handoff | about 5 minutes | `./test.sh --strict` before an unattended campaign, major handoff, or merge |
| Research round | preregistered per hypothesis | Candidate generation or proof search under its own declared timebox |

These are working envelopes, not promises.
The retained normal-gate observations are 108 seconds at the prior pushed checkpoint,
126 seconds for the first integration, and 114 seconds for the PR #16 absorption.
Repeated versioned benchmarks, fuller stage attribution, and warm/cold regimes remain
tracked work.
The research round is intentionally separate from the edit/test loop, so an
eight-hour hypothesis never makes a documentation correction take eight hours to
validate.

Route each result once:

- a structural idea becomes an exploration (`X-NNN`) and, when falsifiable, a hypothesis
  (`H-NNN`);
- a measurement becomes raw data plus an experiment (`exp-NNN`);
- an implementation or process action updates its bead;
- an actual mistake enters [`defects.yaml`](defects.yaml), categorized by what failed
  and linked to its detector and regression; and
- the outer-loop handoff stays in the agent-session artifact instead of being spread
  across chat summaries.

Stop when the declared budget expires, no ready work remains, three consecutive guards
or runs fail, a decision needs the user, or two cycles fail to move the chosen progress
metric.
This is a cooperative mathematical workspace: optimize for rapid detection, exact
records, and cheap recovery.
The negative-control marker, generated-view drift checks, bounded subprocesses, and
resumable on-disk runner state are useful; per-run worktrees, repository copies, or a
generalized lease/capability system are not the default.

Three documents get you oriented, and they have different jobs.

**[`TUTORIAL.md`](TUTORIAL.md) is the conceptual on-ramp:** the objects, the main
decompositions, the central traps, and the boundary between established and proposed
work. It owns no changing status.

**[`SYNOPSIS.md`](SYNOPSIS.md) is the technical root:** the single account of what this
project knows, how it knows it, and what it is doing next.
The problem, the results established here and their evidential status, the per-`n` lay
of the land, the terminology this directory uses narrowly, the hypothesis registry, and
a roll-up of every experiment run so far.
Its numbers are reconciled against the artifacts in the gate.

**[The basin confidence ladder](campaign/agendas/agenda-001-basin-confidence-ladder.md)
is the mutable priority queue:** it separates tool validation, measurement validation,
and research, and names the next bounded evidence for each `n`. The older
[quench-spine handoff](docs/project/handoff-2026-08-23-quench-spine.md) is explicitly
superseded and retained only as historical provenance.

## Layout

```
explorations/packing/
├── TUTORIAL.md             First-principles orientation for a newcomer: the objects,
│                           why the approach is shaped this way, what is established
├── SYNOPSIS.md             The technical root: results, status, and the experiment
│                           roll-up. Read this after the tutorial.
├── conventions.md          Every rule this directory runs on, and which are checked
├── docs/project/           Reports, reviews, specs, postmortems, and historical
│                           handoffs; active specs and the campaign agenda own priority
├── docs/project/research/  The six research reports (see below)
├── campaign/               The experiment record: hypothesis registry, series, rounds,
│                           and a generated ledger. See campaign/README.md.
├── frontier/               What is known about s(n) for every n <= 100: one
│                           schema-validated artifact per case, plus editorial.
│                           See frontier/README.md.
├── golden/                 Stored calibration endpoint snapshots for small PROVED
│                           cases. Mathematical oracle checks are distinct from the
│                           provisional discovery rows. Rebuilt by tools/golden_basins.py
├── atlas/                  Schema for endpoint observations and provisional summaries
├── resources/              Local archive of the primary literature: papers and web
│                           sources, each kept as original, cleaned .md, and raw
│                           extraction. See resources/README.md.
├── sqpack/
│   ├── field.py            exact arithmetic in Q(alpha): +, -, *, /, exact zero test,
│   │                       exact sign by rational interval arithmetic with bisection
│   ├── verify.py           separating-axis validity check, generic over the scalar
│   │                       type; exact or float backend, optional grid bucketing
│   ├── quench.py           LP-in-cell quench: solve the cell, search the angles,
│   │                       produce a coordinatewise-stationary endpoint candidate
│   ├── canonical.py        provisional endpoint keys: D4- and relabel-invariant
│   │                       geometry plus a contact graph canonical up to isomorphism
│   ├── atlas.py            provisional endpoint-observation store and merge logic
│   ├── closed_form.py      recognise a side as (p + q*sqrt(d))/r, or decline;
│   │                       recognition alone proves neither convergence nor optimality
│   └── packings/trump11.py Walter Trump's 1979 packing of 11 unit squares, exactly
├── derive_field.py         derives the number field from the published polynomial
├── verify_trump11.py       verify the packing and report what it took
├── negative_control.py     show the verifier rejects bad packings, and where float64
│                           fails
├── bench.py                exact vs approximate cost, and scaling with algebraic degree
├── lp_cell.py              rebuild the fixed-angle cell as a linear program, through
│                           constraint rows sqpack/quench.py does not share
├── run_quench.py           quench annealer output, both angle methods
├── run_basin_entry.sh      perturb a known packing and measure the return
├── defects.yaml            the defect logbook: every bug and record defect found here
├── defects.schema.yaml     its contract, enforced in the gate
├── defects.md              generated from defects.yaml; never edited by hand
├── differential_test.py    search energy against the validity oracle, on near contacts
├── run_baseline.sh         the baseline annealer sweep a round is run from
├── tools/                  checkers and generators: the soundness perimeter, the
│                           negative controls, the generated views and their drift gates
├── sqsearch/               tier-1 screening annealer (Rust)
├── test.sh                 run everything and check the expected results
└── frankensim-probe/       two experiments run against Jeffrey Emanuel's FrankenSim,
                            asking whether its certified-arithmetic and RNG layers help
                            here (see that directory's README)
```

## What Has Gone Wrong Here

[`defects.md`](defects.md) is the logbook: every bug, inefficiency and record defect
found in this toolchain, what caught it, and what now stops it recurring.
It is generated from [`defects.yaml`](defects.yaml) and checked in the gate.

It is kept because the aggregate says things no individual bug report can, and two of
those things shape how this directory works:

- **The dangerous defects flatter.** Most soundness failures found here pointed in the
  direction that looks like success, which is why a run that beats the record is treated
  as a bug until proved otherwise.
- **The automated gate is not where soundness failures have been found.** No soundness
  defect in the log was caught by it.
  The rest came from control cells whose answers were known in advance, rules written
  down before the measurement, generated views contradicting their sources, and careful
  reading. Gates confirm what someone already thought to check.

The counts live in [`defects.md`](defects.md), which is generated, and in
[the synopsis](SYNOPSIS.md#the-defect-record), which is reconciled against the same
source in the gate. They are deliberately not repeated here: this paragraph carried them
before, and copied aggregates repeatedly went stale.

## Conventions

[`conventions.md`](conventions.md) consolidates every convention this directory runs on:
the id scheme across all layers, file naming, artifact discipline, the evidence tiers
and what each may claim, provenance, corrections, and which rules are machine-checked
versus which rest on care.
Read it before adding an artifact, a round, or a tool.

## Reports

Written to be read in this order.
They move from what is known, to how it is computed and checked, to what to build, to
where a proof assistant fits, and finally to how to search: the strategy the tooling
exists to serve.

| Report | Scope |
| --- | --- |
| [Packing 11 Unit Squares in a Square](docs/project/research/research-2026-08-22-packing-11-unit-squares.md) | The mathematics of `s(11)`: what is proved, what is only conjectured, and why the available proof technique cannot close the gap |
| [Algorithms and Tooling for Square Packing](docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md) | How packings are searched for, refined from numerical to exact algebraic form, and verified; who holds the records and with what |
| [FrankenSim as a Rust Toolkit for Square Packing](docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md) | First-hand study of a large Rust simulation framework as a source of certified-arithmetic and determinism building blocks |
| [Infrastructure for Square-Packing Exploration](docs/project/research/research-2026-08-22-infrastructure-for-packing-exploration.md) | Synthesis of the two above into a build order: three latency tiers, the language boundary, which symbolic layer to use where, and what to deliberately not build |
| [Lean for Square-Packing Proofs and Validation](docs/project/research/research-2026-08-22-lean-for-packing-proofs-and-validation.md) | Where a proof assistant fits: the upper bound is formalisable today and unclaimed, the lemma layer is the diagnostic first target, and certificates make a result checkable by someone who does not trust our code |
| [A Search Philosophy for Square Packing](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md) | The strategy layer: why volume-weighted search fails precisely at records, the basin atlas over the LP-quench map as the deliverable, diversity over structural descriptors instead of loss-shaping, the LLM at the structural layer, and relaxation ladders into the hard instances |

These six are the research reports.
For the full document set, including the reviews, the postmortem, the campaign runbook
and what each one owns, see the synopsis’s [document map](SYNOPSIS.md#document-map).

The structured record of the problem’s frontier, meaning the best known packing and best
proved lower bound for every `n ≤ 100` with provenance and per-case editorial, lives in
[`frontier/`](frontier/README.md) as soft-schema artifacts rather than as a table inside
a report, so it can be validated and queried.

Claims in the reports are separated by evidential status (proved, computationally
verified, best known, or asserted-but-unverified) and every citation resolves both to a
full reference and to a local copy in [`resources/`](resources/README.md).

The reports have been through a full technical review (2026-08-22): every substantive
claim re-checked against the archived primary sources, the central algebra re-derived
independently at 50-digit precision, and the findings applied to the documents
themselves. Corrections this produced are recorded in the `n = 11` report’s
[Corrections to Common Summaries](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#corrections-to-common-summaries),
its remaining gaps in
[Open Questions](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#open-questions),
and the prioritized path forward in
[A Research Program](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#a-research-program).

## Plan

The implementation plan for the first experiments, meaning search, verify and iterate on
`n = 11` and `n = 12`, is
[plan-2026-08-22-minimal-packing-toolkit.md](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md).
It turns the six reports into seven phases and a bead tree, one epic per phase;
`tbd list --spec docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md`
shows the work items and `tbd ready` the unblocked subset.

The current standing review,
[review-2026-08-23-toolkit-docs-and-first-experiments.md](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md),
audits the toolkit documents, supplies the experiment method they lacked (a hypothesis
register with kill criteria, a run protocol, a series plan starting from an `n = 11`
smoke), and contributes the result the refiner rests on: for fixed angles and a fixed
cell the whole problem is a linear program.
That is **proved**, and the synopsis records it as
[T-2](SYNOPSIS.md#the-cell-decomposition) with two independent implementations.
The review’s register carries the search-philosophy report’s boil-down as hypotheses
`H-011`–`H-015` and series S6, landscape cartography.

## Exact Verification

Record packings are published as high-precision decimals, and there is no public tool
that checks one **exactly**. `sqpack` is that check.

Why precision is not enough: a record packing has squares touching at exactly zero
separation, floating point can certify a strict inequality but not an equality, and
every tolerance that accepts the true contacts also accepts overlaps smaller than
itself. The argument in full, with what it cost when ignored, is
[Why Exactness Is Not Optional](SYNOPSIS.md#why-exactness-is-not-optional).
`negative_control.py` demonstrates both failure modes.

### Use

```bash
python3 verify_trump11.py     # exact verification of s(11) <= 3.877083590022814...
python3 negative_control.py   # exact rejects any overlap; float64 has a blind spot
python3 bench.py              # timings
python3 derive_field.py       # re-derive the field (needs sympy)
./test.sh                     # the whole gate: the above plus the corpus, the
                              # lint floor, the controls, and every drift check
```

Only `derive_field.py` needs a third-party package (SymPy).
The verifier itself is standard library only.

`verify_trump11.py` output:

```
VALID: 11 squares, 55 pairs tested
  container: 20 corner coordinates exactly on the boundary
  pairs:     14 separated with zero gap, 41 strictly
  field:     Q(u), degree 8, u = tan(a/2)
  P(s) == 0 for the published degree-8 polynomial: True
  s = 3.87708359002281417730789706010096270637645566846
```

The 14 zero-gap pairs are the ones no floating-point verifier can certify.
The 33 leading digits match the value published on the
[Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
record page, so this is also an independent check of that record.

### Verifying another packing

Supply the corners in an exact field and call `verify_packing`:

```python
from sqpack.field import NumberField
from sqpack.verify import verify_packing, exact_sign

field = NumberField(min_poly, isolating_interval)  # coefficients high degree first
squares = [...]  # 11 x 4 corners of FieldElements
print(verify_packing(squares, side, sign=exact_sign))
```

The work is in the first line.
Record packings are published as SVG transforms with 33-digit decimal entities and, for
the analytically solved ones, Mathematica source in an XML comment; recovering the field
means reading that by hand, once per packing.
`sqpack/packings/trump11.py` is the worked example.

**The result is a proof only if the field metadata is right, and the constructor does
not yet check that** ([D-053](defects.md), open): `NumberField` requires an irreducible
minimal polynomial and an interval isolating exactly one real root, but verifies only an
endpoint sign change.
A reducible polynomial or a multi-root interval yields unsound exact comparisons.
The built-in Trump witness is independently checked; anything you supply yourself is
not, so verify irreducibility and root isolation before trusting the verdict.

For a quick, non-certifying check, swap in the float backend:

```python
from sqpack.verify import float_sign

verify_packing(squares, side, sign=float_sign(1e-9), bucket=True)
```

`bucket=True` grid-buckets the squares so pair enumeration is linear rather than
quadratic: at `n = 1000` that is 15,936 candidate pairs instead of 499,500.

### Scope

This checks that a *proposed* packing is valid, which is a different and far easier
question than whether it is optimal.
The only rigorous computer-assisted optimality proof for rotatable unit squares in any
container covers three squares in a circle (Montanher et al.
2018); nothing comparable exists for squares in a square.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
