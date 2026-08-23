# Conventions for `explorations/packing/`

Every convention this project runs on, in one place.
Read this before adding an artifact, a round, a series, or a tool.

Each rule is marked **[checked]** when something fails on a violation, or
**[convention]** when it rests on care alone.
The distinction is the point: a rule nothing enforces is a rule that will drift, so the
standing goal is to move rules from the second column to the first.
`./test.sh` is what does the checking.

## 1. Identity

One id per thing, three digits, never reused.
The prefix says what kind of thing it is.

| Layer | Id | Scope | Example |
| --- | --- | --- | --- |
| Campaign | contract namespace | the directory | `packing.squares` |
| Series | `series-NNN` | campaign | `series-000` |
| Round (experiment) | `exp-NNN` | **campaign, not series** | `exp-003` |
| Hypothesis | `H-NNN` | campaign, spans series | `H-016` |
| Exploration report | `X-NNN` | campaign | `X-001` |
| Search/proof strategy | `search:N`, `proof:N` | the frontier catalogues | `search:12` |
| Basin (planned) | canonical key, plus a `B-NNN` alias | campaign, spans series | — |

**Rounds do not restart at `exp-001` in each series, and this is deliberate.** A series
is a directory and a field, not a namespace.
`exp-003` names one round forever, wherever it lives, which is what makes cross-series
references work — and they are common: a series’ `carries_forward` names rounds from an
earlier one, a hypothesis aggregates rounds across all of them, and the atlas will cite
the round that discovered a basin.
Per-series numbering would make every one of those a compound key, and a bare `exp-001`
in prose would be ambiguous.

The series is never lost, because the round records it in a `series:` field and lives in
that series’ directory.

**Cardinality**, so the shape of the record is unambiguous:

| Relation | Cardinality |
| --- | --- |
| round → series | exactly one |
| round → hypotheses | **one or more** — a round may test several |
| hypothesis → rounds | zero or more — sweep cells and replications |
| hypothesis → exploration reports | zero or more (`derived_from`) |
| hypothesis → strategies | zero or more (`strategy_refs`) |

So `exp-` does **not** map one-to-one onto `H-`. Four rounds currently reference
`H-016`: one three-cell round and its three per-cell replacements.

**Ids are never reused, and never renumbered except on merge collision.**
[checked: whole-set uniqueness] When two branches collide, the newer campaign renumbers
and the change is recorded as an annotation on the affected artifacts, never as a silent
edit.

**Reserved ids.** [checked] `H-003`–`H-010` and `H-013`–`H-015` are held for entries
that exist as prose in the
[standing review’s register](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register)
but are not codified here yet.
They are declared in a `reserved-ids` comment on the idea board.
A reserved id may be *named* but not *linked*, and a reservation that has been fulfilled
is flagged stale.

## 2. Naming

**Files and directories carry the full id followed by a kebab-case slug.** [checked]

```
campaign/series/series-000-smoke-and-calibration/
campaign/series/series-000-smoke-and-calibration/experiments/exp-003-baseline-n11-target.md
campaign/hypotheses/H-002-lp-in-cell-polish.md
campaign/explorations/X-001-standing-review-and-search-philosophy.md
campaign/series/series-000-smoke-and-calibration/results/exp-003-baseline-n11-target.jsonl
```

The id in the filename must equal the id in the frontmatter.
[checked] Raw run data takes the id of the round that produced it.

Research documents and reviews keep the repository’s dated form:
`research-YYYY-MM-DD-topic.md`, `review-YYYY-MM-DD-topic.md`.

Use [`repren`](https://github.com/jlevy/repren) for renames — it moves files and
rewrites references in one pass, which is what keeps the two in step.

## 3. Artifacts

**Frontmatter is authoritative; the body is for people.** [checked: schema] A consumer
reads the YAML and must not parse prose for structured values.
The body carries the judgement, the history and the caveats — the things that would be
lies if forced into a field.

**Every artifact declares its schema and is validated against it.** [checked]
`status: enforced` means something fails when the artifact is wrong.
An artifact that declares a schema nothing loads is the exact failure this project keeps
finding in its own sources.

**Promote a value into YAML only when something consumes it** — the accept rule, the
ledger, the checker.
[convention] Everything else is prose.

**Cross-field rules live in the checker, not the schema.** [checked] softschema 0.6.2
rejects `allOf` object composition under `status: enforced`, so a conditional would
invalidate every artifact rather than the offending one
([jlevy/softschema#41](https://github.com/jlevy/softschema/issues/41)).

## 4. Evidence

**Three tiers, and each says what a number may claim.**
[checked: recorded in `subject.precision`]

| Tier | Instrument | May claim |
| --- | --- | --- |
| `f64_screen` | `sqsearch` | a candidate was proposed |
| `polished` | LP-in-cell quench | this is the basin, named and exactly valued |
| `exact` | `sqpack` over ℚ(α) | validity — and only here, a record |

**`beat_record: true` may only be written at `precision: exact`.** [convention] A record
packing has pairs touching at exactly zero separation; no floating-point check can
decide those.

**Claims are separated by evidential status** — proved, computationally verified, best
known, or asserted-but-unverified — and citations sit near the claims they support.
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
`exp-001` violates this — its commit was orphaned by a rebase — and carries an
annotation saying so.

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
Beads track build work, never scientific claims — a bead may say “build the instrument
for H-002”, never “H-002 is confirmed”.

**One series is open at a time.** [checked]

**The runbook is frozen while rounds are running.** [convention] The accept rule, the
tolerances, the metric vector and the control cells do not change mid-series.

## 8. Layers that must not blur

**`sqpack` owns validity.
`sqsearch` owns move-loop energy.** [checked: differential test] `pair_depth` is a
metric shaped for annealing, not a verdict, and a second implementation at that layer is
fine — as long as it never gets to say what is valid.
20,000 near-contact pairs are checked against the oracle on every run of `test.sh`.

**Proposers propose and nothing else.** [convention] A proposer never quenches,
canonicalizes, decides validity, or writes the atlas, so a new strategy cannot change
what a basin means.

## 9. Code and docs

**Python first; accelerate what a profile says is slow, not what looks slow.**
[convention] The measurements behind this are in the
[plan spec](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md#stack-and-boundaries--decided-by-measurement).

**Dependencies are pinned, and nothing released in the last 14 days.** [convention]
`test.sh` selects an interpreter that has what it needs, falling back to a pinned `uv`
runner.

**Markdown is formatted by flowmark**, automatically on commit.
[checked: hook] Exclusions are evidence-based, not precautionary, and each one states
its measured reason in [`.flowmarkignore`](../../.flowmarkignore).

**Relative links must resolve.** [checked] The campaign’s checker walks every relative
Markdown link. This project has needed that twice.

**Docs follow the common documentation guidelines** and carry the footer.
[convention]

## 10. What the gate actually enforces

`./test.sh`, in order:

1. Exact verification of Trump’s packing, and the negative control showing why float
   cannot do it
2. Frontier corpus structure, and its soft-schema validation
3. Generated tables in sync with the frontier data
4. Strategy catalogue integrity
5. `sqsearch --selftest` — geometry against a naive reference, determinism, the `s(5)`
   positive control, and the recomputed-overlap guard
6. The differential test between search energy and the validity oracle
7. The campaign record: schema validation, id uniqueness, dangling references, unknown
   series, more than one open series, stale claims, cross-field verdict rules,
   idea-board reconciliation, reserved-id rules, dead links, and ledger freshness

Everything else on this page is convention, and convention is what drifts.
When a rule here is broken and nothing catches it, the fix is a check, not a reminder.

## Defect classes

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

A soundness defect gets a postmortem, not just a fix — see
[the first one](docs/project/postmortems/postmortem-2026-08-23-soundness-class.md),
whose rules R1–R4 apply to code that does not exist yet.
[convention]

## Defects

Every defect found in this toolchain is recorded in [`defects.yaml`](defects.yaml) and
rendered to [`defects.md`](defects.md).
A defect is a bug, an inefficiency, or a record that disagreed with its evidence — not
an approach tried and rejected on its merits, which belongs in `campaign/ideas.md` under
Dead ends.

Two fields carry most of the value and are worth filling in honestly rather than
generously. `detected_by` says what *actually* caught it, which is how we learn which
detectors to build more of.
`regression` names the check that now prevents recurrence, and the literal `none` is a
legitimate and useful answer — the generated view collects those into the list that
predicts what will come back.
[checked]

Open defects must carry a bead, soundness and validity defects must state whether the
error flattered or understated the result, and every row must point at the artifact
carrying its narrative.
[checked]

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
