# The Artifact Contract

Four files carry a campaign.
The **idea board** is the one-page map of everything anyone has considered; an
**exploration report** proposes ideas at length; a **hypothesis** states one claim so it
could be wrong; an **experiment** records one round against it.
The last three are soft-schema artifacts — validated YAML frontmatter carries what a
tool reads, and the body carries what only a person reads.

This file explains the fields and why each exists.
The schemas themselves are in `../assets/` — copy them into the campaign, cut them down,
and keep `additionalProperties: false` everywhere, because a typo that validates is a
lie waiting.

| Artifact | Schema | Written by |
| --- | --- | --- |
| `ideas.md` | none — checked, not validated | codifier |
| `series/NNN-slug/README.md` | `assets/series.schema.yaml` | whoever opens the pass |
| `explorations/X-NNN-*.md` | `assets/exploration.schema.yaml` | explorer |
| `hypotheses/H-NNN-*.md` | `assets/hypothesis.schema.yaml` | codifier |
| `experiments/exp-NNN-*.md` | `assets/experiment.schema.yaml` | runner |

The rule that keeps the schemas small: **promote a value into YAML only when something
consumes it** — the accept rule, the ledger, the registry status view, the claim
protocol. Everything else is prose.

## The idea board

`ideas.md` is the only unvalidated file in the chain, and deliberately so: it is a
one-page map of the whole idea space, and what makes it valuable — grouping, ranking,
and a clause saying why each idea might work — is judgment that a schema would flatten.
Start from `../assets/ideas-template.md`.

What *is* mechanical is its referential integrity, checked in both directions:

- every `H-NNN` the board names exists in `hypotheses/`
- every artifact in `hypotheses/` appears on the board

The first catches a board that drifted ahead of the registry; the second catches a
hypothesis registered without ever being visible to the next agent that arrives.
`../assets/ledger.py` runs both.

The board tracks an idea only until it is registered.
After that the row is a pointer and the ledger owns the outcome, which is what keeps the
board from becoming a second record that disagrees with the first.

## The series

One pass of the loop under one generation of tooling, carrying the experiments taken on
that instrument. The registry and the idea board span the campaign; only the rounds
belong to a series.

```yaml
id: series-001
slug: smoke-n11
title: Smoke pass — reproduce what is known, try the obvious hypotheses
status: open                   # open | closed | superseded; one open at a time
opened: 2026-08-22
goal: >-
  Prove the loop works end to end on cheap, checkable claims before anything
  subtle is attempted.
opened_because: first series   # the field that earns a series its existence
instrument:
  name: sqsearch
  version: 0.1.0
  commit: <sha>
  selftest: "sqsearch --selftest — geometry, determinism, and the s(5) control"
supersedes: null
carries_forward: []            # nothing yet; a later series lists what survives
budget: one overnight session
```

`opened_because` is the load-bearing field.
Opening a series says *the numbers before this point were taken on a different
instrument*, so if nothing changed, the work belongs in the series already open.
`carries_forward` is the opposite claim — that a specific earlier round’s conclusion
survives the change — and listing one is an assertion, where omitting it merely costs a
re-run.

Experiment ids stay globally monotonic across the campaign; the series is a directory
and a field, never a namespace.

## The exploration report

Deliberately the thinnest contract of the three.
Its job is to be *easy to write and hard to constrain*, because the value of an idea
report is proportional to how little the format shaped what went into it.
The frontmatter exists only so the codifier can find reports and cite them; the body is
unstructured prose of any length.

```yaml
id: X-004                      # stable, never reused
title: Where the n=11 basin structure might be exploitable
date: 2026-08-22
author: claude-opus-5          # person, agent, or model
campaign: packing.s11          # which campaign commissioned it
brief: >-                      # what the explorer was asked to look into
  Read the annealing literature and the local record catalogue; propose search
  strategies that have never been aimed at this instance.
sources:                       # what was actually read, so a reader can retrace
  - resources/papers/gensane-ryckelynck-2005-improved-dense-packings
  - https://kingbird.myphotos.cc/packing/squares_in_squares.html
proposes: [H-011, H-012, H-013] # filled in by the codifier, not the explorer
```

`proposes` is written **back** into the report once codification happens, which makes
the trail navigable in both directions and makes an unmined report visibly unmined.
A report that yields nothing keeps `proposes: []` and stays in the record; “we read this
and found nothing worth testing” is a result.

The body has no required sections.
A useful default is: what was read, what looks promising and why, what looks like a dead
end and why, and what would have to be true for each idea to work.
Ideas of wildly varying quality in one report are correct and expected.

## The hypothesis registry

One artifact per claim.
**Status is not a field** — it is generated from the experiments that reference the id,
the same way the ledger is generated from artifacts.
A referenced id that has no registry artifact fails the reference check.

```yaml
id: H-012                      # never reused; next free number
kind: hypothesis               # hypothesis | open_question
claim: >-                      # stated so it can be wrong
  Basin-hopping from the 45-degree family reaches the Trump configuration for
  n=11 within 10^6 local optimisations.
lane: search                   # campaign-declared: e.g. search | proof
derived_from: [X-004]          # the exploration report(s) this came from
strategy_refs: [search:12]     # into the campaign's existing strategy taxonomy
criterion:
  shape: record                # paired | conditions | record | determination
  metric: best_side            # the metric or question that would show it
  direction: lower             # predicted direction or outcome
instrument: >-                 # what would measure this
  explorations/packing/search/basinhop.py, scored by sqpack.verify at exact precision.
instrument_ready: false        # not built yet -> the ledger reads this as blocked
regime: single host, deterministic seed, exact validity oracle
instance: {axis: n, point: 11} # where this claim is being made
sweep:                         # optional: the cells this claim should eventually cover
  axis: n
  points: [10, 11, 12]
priority: 2                    # 1 = do next; the codifier's ranking, revisable
cost_estimate: 4 CPU-hours     # what one round is expected to consume
prereqs: [H-003]               # hypotheses or instruments that must land first
replication: false             # may a second operator re-run the same cell?
registered: 2026-08-22         # ISO date, or "retroactive"
notes: >-
  Trump's packing is rigid, so the basin may be narrow; a null result here is
  evidence about the basin, not only about the method.
```

Four fields carry most of the weight and are worth getting right:

- **`kind`.** An idea that cannot be stated so it could be wrong is registered as
  `open_question` rather than forced into a criterion it does not have.
  Open questions sit in the registry, are visible in the ledger, and are not counted as
  measurable queue items.
  Losing them is worse than not formalizing them.
- **`derived_from`.** The link back to the prose the claim was compressed out of.
  When a round’s result is confusing, the report is usually where the missing context
  is, and the board row is the one-line version of the same thing.
- **`strategy_refs`.** Where a campaign already has a taxonomy of approaches — a
  strategy catalogue, a technique inventory — hypotheses cite it rather than
  re-describing. That is what lets the ledger report coverage by *family*: which whole
  classes of approach have never been tried is a far more useful question than which
  individual ideas are open.
- **`sweep`.** Declaring the intended cells up front is what turns a scattering of runs
  into a sweep with visible holes.
  A hypothesis confirmed on one cell of a declared sweep is confirmed on that cell only.

The `registered` date is what makes pre-registration checkable: accepting on a criterion
other than the campaign’s default outcome is legitimate only when the registry artifact
declared it before the measurement ran.
Converting an existing hand-maintained table wholesale would back-date registrations
that never happened — mark those `retroactive`, so enforcement is honest from the first
real registration.

## The experiment spine

| Field | What it is | Notes |
| --- | --- | --- |
| `id` | `exp-NNN`, stable, never reused | filename starts with it; created by exclusive create |
| `title` | one line, declarative | “Memoize the parent resolved for the previous upsert” |
| `date` | ISO date measurements were taken |  |
| `series` | which pass this round belongs to | `series-001`; ids stay globally monotonic |
| `hypotheses` | registry ids this tested (`H-007`) | ≥1; free-riding results register a new H first |
| `tier` | `exploratory` or `confirmatory` | what kind of evidence this claims to be |
| `subject` | what was measured, on what | campaign-specific; the reproducibility record |
| `instance` | the point on the instance axis | `{axis: n, point: 11}`; what a sweep groups by |
| `method` | how, precisely enough to re-run | control/candidate or budget; provenance; `operator` |
| `lease` | claim expiry while `in-progress` | absent once the round is recorded |
| `results` | list of typed result shapes | see below |
| `complexity` | what the change costs to carry | lines, deps, new failure modes, notes |
| `verdict` | decision + primary criterion + one-sentence reason | the only judgment field |

`method.operator` records who or what ran the round (`"claude-opus-5"`, a person’s
handle) — it is what lets different agents or models attack the same registry and be
compared later, and it is one third of the duplication key in
[unattended.md](unattended.md).

`method` should carry re-run provenance at whatever precision the domain affords: binary
hashes for compiled systems, `commit` + `entry_point` + `command` for experiment code,
`budget` for searches.
A number nobody can re-run is a number nobody can defend.

`instance` is separate from `subject` on purpose.
The subject says what the numbers are evidence *about* and rarely changes; the instance
is the dimension you deliberately vary, so it is the grouping key for every sweep view.
Campaigns with genuinely one instance still record it — it costs one line and it is what
makes the second instance cheap.

## The four result shapes

Declare which shapes your campaign uses; an artifact may carry several (a packing round
usually carries `record` + `determination`). The shape and criterion are named in the
hypothesis *before* anything runs.

**`paired`** — control vs candidate, decided on paired differences (fdu):

```yaml
- shape: paired
  metric: wall_ns
  control_median: 2022071226.5
  candidate_median: 1852852604.5
  change_pct: -7.348            # median of PAIRED differences, not the ratio of medians
  ci95_low_pct: -10.424
  ci95_high_pct: -6.119
  passes_acceptance: true       # whole interval on the accepting side of the threshold
  ci_excludes_zero: true        # the measurement says something at all
  direction: improved           # improved | regressed | unclear | unknown
  pairs: 20
```

**`conditions`** — labeled arms, median with range, overlap decides (metabrowser):

```yaml
- shape: conditions
  metric: srv_scanning_ms
  control_median: 650
  candidate_median: 394
  control_range: [621, 690]
  candidate_range: [342, 561]
  change_pct: -39.4
  overlapping: false            # true means: not a result on its own, never "a small win"
```

**`record`** — a score against a standing best (search campaigns):

```yaml
- shape: record
  metric: best_side
  direction: lower              # which way is better, declared not assumed
  score: 3.8770835900228142
  standing_best: 3.8770835900228142
  standing_best_source: "frontier/n-011.md (Trump 1979)"
  beat_record: false
  runs: 40                      # attempts behind the best score
```

**`determination`** — a categorical outcome from a declared enum (proofs, gates):

```yaml
- shape: determination
  question: "does basin-hopping reach the Trump basin for n=11"
  outcome: reached              # from the campaign's declared enum
  checked_by: "sqpack.verify, exact"   # the independent checker that makes it real
```

Four flags on `paired` because one boolean cannot say what happened: fdu collapsed them
into `significant` once, and a *regression* became indistinguishable from a null result.
Derive flags from the interval when writing the artifact; never store an opinion the
bounds beside it could contradict.

## Decisions

| Decision | Means | Required extras |
| --- | --- | --- |
| `accepted` | claim resolved in its favor, change kept |  |
| `rejected` | claim resolved against — measured and refuted, or under the bar |  |
| `unresolved` | measured; could not be resolved; the reason is the finding | reason must say why |
| `blocked` | cannot be tested yet | name the missing instrument or regime |
| `abandoned` | search explored under a budget and stopped; not refuted, out of promise | `budget_spent`, `best_reached`, `reopen_when` |
| `superseded` | a later experiment replaced this answer | point at it |
| `baseline` | no candidate; establishes the numbers |  |
| `in-progress` | round claimed and running | `lease.expires`, `method.operator` |

## Metric roles

Declared once per campaign, so the accept rule knows what it scores without being told
per experiment, and so a reader cannot mistake corroboration for a verdict:

| Role | May conclude | Systems perf | Web app | Packing | Proof |
| --- | --- | --- | --- | --- | --- |
| `outcome` | the accept decision | `wall_ns` | hypothesis’s named metric | best score | the determination |
| `cost` | qualifies the win | `cpu_ns` | `transferred_kb` | CPU-hours | budget spent |
| `guard` | a breach rejects, regardless of outcome | `peak_rss_bytes` | “nothing else moved the wrong way” | validity checker | kernel accepts |
| `mechanism` | explains only | `component_ns`, faults | render spans, long tasks | iterations, restarts | subgoals closed |

The guard role is also the validity slot: fdu’s per-trial oracle digest, metabrowser’s
viewport floor, a packing overlap check, and a proof kernel are the same thing — the
independent proof the result is *real* before it may be counted *good*. A run failing a
guard is invalid and is refused at record time, not annotated.

## What the schema cannot carry

Cross-field rules — *abandoned requires `budget_spent`, `best_reached` and
`reopen_when`; superseded requires `superseded_by`; in-progress requires a lease* — read
like `if`/`then` conditionals under `allOf`, and they do not work there.
Measured on 2026-08-22 against softschema 0.6.2: any `allOf` object composition makes an
artifact declaring `status: enforced` fail with
`enforcement_unsupported: enforced closure is unsupported for allOf object composition`,
and the same message is reported for a conforming document and a violating one, so the
conditional masks what it was meant to catch.
Filed upstream as [jlevy/softschema#41](https://github.com/jlevy/softschema/issues/41).
The conditional does not catch the offending artifacts; it invalidates every artifact
including the correct ones.

So those rules live in the checker (`../assets/ledger.py`) alongside the whole-set
invariants, which is a better home for them anyway: a rule about what a *decision*
obliges you to record is campaign policy, and campaign policy is easier to read as ten
lines of Python than as nested JSON Schema.
Keep the frontmatter schema flat and CLI-validatable; put anything conditional in the
checker, and negative-control it once by writing an artifact that should fail.

## Choosing how to write the schema

Hand-write it while it is small (metabrowser’s is 90 lines); compile it from a typed
model only when field count and churn earn the tooling — fdu’s
[experiment.py](https://github.com/jlevy/fdu/blob/main/benchmarks/realtree/experiment.py)
is the worked example of that end, with field descriptions as the documentation every
artifact ships with.

Start from `../assets/experiment.schema.yaml`: replace the `subject` and `instance`
properties with your campaign’s, delete the shapes you did not declare, and replace the
`determination.outcome` description with your campaign’s enum.

## The artifact skeleton

```markdown
---
title: <the experiment title>
softschema:
  contract: <project>.<campaign>:Experiment/v1
  schema: ../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-007
  ... (the validated payload)
---
## What was measured

The claim, the instrument, the instance, and the regime — enough that a reader knows
what kind of evidence follows.

## What was tried

The full research report: what prior evidence suggested, what was actually built and
how (commands, code by commit and entry point, resources consulted), including the
variants that did not survive to the verdict.

## Result

The numbers with their spread, and what they mean against the accept rule.

## What the prediction got wrong

The most reusable section. "Right about the component, wrong about the wall" teaches;
"missed" does not.

## Limits

What this round cannot claim: regimes not covered, cells of the sweep not run, guards
not run, questions opened.
```

Validate at the boundary, every time an artifact is written or merged:

```bash
uvx softschema==0.6.2 validate experiments/exp-007-*.md
```
