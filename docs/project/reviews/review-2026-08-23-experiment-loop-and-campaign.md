# Review: The Experiment Loop, the Campaign, and the Consolidation (PR #5)

> **Lifecycle:** Superseded for current guidance by the
> [campaign runbook](../../../packing/campaign/README.md).
> Retained as a dated review record.

**Date:** 2026-08-23

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

**Reviewed:** [PR #5](https://github.com/jlevy/thinking-scratchpad/pull/5)
(`claude/experiment-loop-access-6a0e36`, 55 files, +7,761/−37): the experiment-loop
skill, the `campaign/` record with its first measured round, the `sqsearch` engine, and
the consolidation that rebuilt the
[plan spec](../specs/active/plan-2026-08-22-minimal-packing-toolkit.md) around a shared
spine. Reviewed from the standpoint of the five research reports, the
[standing review](review-2026-08-23-toolkit-docs-and-first-experiments.md), and the
[search-philosophy report](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
this branch consolidates against — with every load-bearing claim re-run or re-derived in
a fresh container rather than taken from the PR description.

## Verdict

**Adopt the direction; fix the record’s integrity items before leaning on it.**

The consolidation is honest and the discipline is real.
The PR merges a parallel implementation with the strategy layer without erasing either:
conflicts are resolved explicitly and annotated rather than rewritten, the one
correction that ran *against* the reviewed documents (the calibration ladder is
machinery-validation only) is accurately attributed and recorded where it bites, and the
first experiment artifact contains a documented case of the process catching its own
author — a pre-registration miss at `n = 10` that the generated frontmatter exposed and
the prose had glossed.
That is the system working, and it is worth more than the baseline numbers.

The architectural contribution — **proposer over spine** — is a correct and valuable
reading of the hypothesis register, and this review endorses it as the plan’s organizing
principle (see [D-1](#d-1) for the one boundary it must keep).

What needs fixing is narrower but real: the campaign’s schema validation is declared and
not wired (**the exact “tacit failure” class this repository is hardened against
elsewhere**), the first round’s archived record cannot regenerate its configurations,
the 32-bead task tree the PR describes never reached the shared store, and the
renumbering left a handful of stale paths.
All are cheap; none undermines the design.

Findings are numbered `F-*` (defects, with severity) and `D-*` (direction opinions).
Everything marked *verified here* was reproduced in this review’s own container.

## What was verified by running it

| Check | Result |
| --- | --- |
| `explorations/packing/test.sh` on the PR head, fresh container | **passes end to end**, including the new interpreter-selection fallback, the engine gate, and the campaign invariants |
| `sqsearch --selftest` (built with local cargo) | 12/12, positive control recovers `s(5)` to `+4.3e-5` here |
| SAT half-extent simplification (`½ + ½(\|cos Δ\| + \|sin Δ\|)`) | re-derived analytically; selftest agrees with the naive four-axis form to `8.9e-16` over 200k random pairs |
| exp-001’s table (best/median/range/gap per cell) | recomputed from the archived JSONL; **every number matches** — the “lifted, never retyped” discipline held |
| All 10 campaign artifacts against their four schemas | **pass** when validated directly with jsonschema (the artifacts are clean; the wiring is what is missing — F-1) |
| `make skills-check`; `.agents` vs `.claude` mirrors | identical |
| `campaign/ledger.py --check`; `ledger.md` freshness | clean on the committed tree |
| Negative control: schema-invalid artifact through the gate | **passes the whole gate** — the basis of F-1 |
| Relative links across `campaign/`, the revised spec, the skill | 3 real breaks, all renumber residue — F-4 |
| The PR’s 32 beads, after `tbd sync` against `origin/tbd-sync` | **absent** — F-3 |

CI status: the repository has no CI configured on pull requests; nothing was pending or
failing at review time.

## What is right, and worth saying plainly

- **The proposer/spine factorization is the correct reading of the register.** Almost
  every registered strategy is a way of proposing configurations over one downstream
  pipeline (quench → canonicalize → verify → atlas); building that spine once is what
  makes the register cheap and results comparable.
  The reviewed documents implied this; the PR is the first place it is stated as a build
  order, and the revised Phases 2–7 are in genuine dependency order.
- **The tier discipline was directionally right.** The then-current `f64_screen` /
  `polished` / `exact` labels, with `beat_record: true` writable only at `exact` and the
  frontier editable only by a deliberate human-reviewed change, encodes the repository’s
  central lesson (14 zero-gap pairs; no float check can certify) as *process*, not just
  prose.
- **The controls mostly earned their keep.** The `n = 10` positive control killed two
  broken search formulations; the inert `--budget-moves` defect was caught by its own
  tell (results worsening at larger declared budget).
  The original review incorrectly praised `n = 12` as a negative control; `s(12)=4` is
  open, so it is now an open-case calibration (D-042), not known-answer evidence.
  Dead ends are recorded with reasons (GPU loss measured, not asserted; the jammed-grid
  failure mode explained).
  exp-001’s “what the prediction got wrong” section is the best experimental prose in
  the repository so far.
- **The consolidation is faithful.** The codified `H-001`/`H-002`/`H-011`/`H-012` match
  the standing review’s entries; `X-001` is the right provenance bridge; the renumber
  (`H-016`–`H-018`, `series-000`–`006` onto S0–S6) is annotated in the artifact rather
  than erased; the calibration demotion is recorded in `series-000` where a future
  runner will actually see it.
  `H-018` (basin entry) is a genuinely good contribution: the cheapest informative
  measurement runnable today, correctly placed against the strategy report’s calibration
  section.
- **The repo plumbing fixes are evidence-based.** The `test.sh` interpreter fallback
  fixes a real silent-unreachability (and pins versions); the `.flowmarkignore`
  narrowing states its measurement; the skill mirror check turns a drift risk into a
  gate.

## Findings

### F-1 (P1): the campaign’s `status: enforced` schemas are enforced by nothing — verified by negative control

The four campaign schemas are well-written (closed objects, patterned ids, tier enums),
and all ten artifacts declare `status: enforced`. But nothing in the gate validates
them: `tools/validate_schemas.py` covers `frontier/` only, and `ledger.py` checks
referential invariants without ever loading a schema.

*Verified here:* setting `priority: 0` in a hypothesis (violating the schema’s
`minimum: 1`) passes `ledger.py --check` **and** the full `test.sh` —
`ALL CHECKS PASSED`. Only field changes that happen to appear in the rendered ledger get
caught, incidentally, as ledger drift.

This is precisely the tacit-validation failure class the repository documented and
closed for `frontier/` (and filed upstream as softschema#38 when the CLI couldn’t do
it). The campaign reintroduces it at the moment the campaign becomes the record of
scientific claims.

**Fix (small, verified feasible here):** the ~15-line jsonschema loop this review ran —
load each artifact’s declared schema, validate the envelope, fail loud — either inside
`ledger.py`’s `load()` (it already parses every artifact) or as a campaign section in
`tools/validate_schemas.py`, matching the frontier pattern.
All ten current artifacts pass it today, so wiring it costs nothing now and everything
later.

Related, worth carrying with it: the schema comment documenting that softschema 0.6.2
rejects `allOf` object composition under `status: enforced` (`enforcement_unsupported`)
is a measured upstream limitation, found independently of softschema#38. It should be
filed as its own upstream issue rather than living only in a comment — that is the
standing practice here.

### F-2 (P1): exp-001’s archived record cannot regenerate its configurations

Three small holes line up:

1. `run_baseline.sh` filters the engine output to `"kind":"summary"` lines.
   The per-chain records — which carry the **actual best configurations** (`x`, `y`,
   `t`) and the per-chain `overlap` — are discarded.
   The archived JSONL therefore contains no packing and no overlap value.
2. The artifact’s `checked_by` says “overlap == 0 on every reported packing”, but that
   guard is not auditable from the archive (see 1), and in the engine it is asserted
   against the *incrementally tracked* accumulator, not recomputed from the stored best
   (F-5).
3. The recorded `engine_commit: d6a1057` is unreachable — the rebase rewrote the branch,
   so the exact binary that produced the numbers can no longer be rebuilt from the
   recorded provenance.

Each alone is minor; together they break the campaign’s own invariants #9/#10
("provenance captured at the source", “an independent check that the result is real”)
and the promise in `rng.rs` that “a reported configuration can be regenerated from the
numbers in its artifact”.
Determinism was supposed to be the safety net, and the dangling commit cuts it.

**Fix:** archive the chain lines (they are the atlas’s raw material — the revised plan
already says the engine “discards exactly the data the atlas is made of”; the archive
currently does too); add the best configuration and a *recomputed* overlap to the
summary line; annotate exp-001 that its commit predates the rebase (the annotation
pattern is already established in that artifact).
Going forward the provenance rule should require a commit that is an ancestor of the
branch being merged.

### F-3 (P1): the 32 beads did not land — the revised spec currently points at the wrong task tree

The PR body says “32 open beads against the spec in dependency order; `tbd ready`
surfaces the unblocked set”, and the revised spec instructs readers to run
`tbd list --spec …plan-2026-08-22-minimal-packing-toolkit.md`.

*Verified here:* after `tbd sync` against `origin/tbd-sync`, none of the named beads
(`think-ta07`, `think-d5tc`, `think-isa3`, `think-h0hd`) exists, and the spec-linked
listing returns the **old** 16-bead tree — whose phases describe the *pre-revision* plan
the PR just replaced.
The branch carries no bead-store changes, so the new tree exists only in the authoring
environment.

Until the sync happens (or the tree is recreated), the revised plan is un-executable as
written: its own pointer surfaces tasks that contradict it, and the P0 items the PR
correctly identifies (the quench spine; finishing the consolidation) are invisible to
every other agent. The old tree also needs reconciling, not just replacing — several of
its beads (`think-q3hl` LP-in-cell, `think-pmhe` canonical identity, `think-lpse`
ladder, `think-19gf` E4 gating) are the same work items the new phases restate, and
should be updated or superseded explicitly rather than left as parallel truths.

### F-4 (P2): renumber residue — three broken links, one script writing to a dead path, one wrong claim

All from the `series-001 → series-000` / `H-00x → H-01x` renumber, all mechanical:

- `campaign/ideas.md` → `series/001-smoke-n11/experiments/exp-001-baseline-sweep.md`
  (broken; the directory is `000-smoke-and-calibration`).
- `campaign/ideas.md`, Open questions: “Registered as H-004 at
  `hypotheses/H-004-basin-width.md`” — broken link **and** stale claim: the basin-width
  idea was renumbered to `H-018` (the board’s own row 7 says so), while `H-004` is
  reserved for the standing review’s neighbor-transfer hypothesis.
  As written, the board asserts a reserved id is registered.
- `run_baseline.sh` still writes `OUT=campaign/series/001-smoke-n11/results/…` — the
  next invocation of the runbook’s own “running one round” sequence would recreate the
  dead directory and archive the run in the wrong place.
- `exp-001` frontmatter `method.record` carries the same stale path.
- `exp-001`’s annotation links `traps.md` with five `../` where six are needed.

Worth one structural note: `ledger.py`’s two-way reconciliation *cannot* catch the
`H-004` case — reserved ids are exempted from the dangling-reference check by design,
and links are not checked at all.
The masking is the price of the (good) reserved-ids mechanism, so the compensating
control should be a plain relative-link checker in `test.sh` — this repository has now
needed one at least twice (the review-doc placeholder incident, and this).
A cheap additional rule in `ledger.py`: a reserved id may not appear as a markdown link
target on the board.

### F-5 (P2): the overlap guard is asserted against a drifting accumulator

In `search.rs`, `overlap` is maintained incrementally (`overlap − old_local + new_local`
per accepted move, ~4×10⁵ steps per anneal, thousands of anneals per chain), and
`best_overlap` snapshots that accumulator at record time.
It is never recomputed from the stored best configuration; selftest check 8 and the
JSONL both report the accumulator.
`FEASIBLE_EPS = 1e-12` is at the plausible scale of accumulated cancellation error for
runs this long, and the error can go either direction — silently recording a
configuration with real overlap, or silently refusing a genuine record.

**Fix:** one line — recompute `total_overlap(&best)` at record (or at least at report)
time; assert the recomputed value in the selftest.
Two adjacent nits, note-level: the stored `energy` goes stale each step as `lambda`
ramps (the acceptance test compares a new-λ energy against an old-λ one — a small
systematic bias while infeasible; recompute `energy` after the ramp, one multiply-add),
and the budget check between anneals lets a chain overshoot `--budget-moves` by up to
one anneal (~0.4% here; harmless now, worth a cap when “equal budget” comparisons get
tight).

### F-6 (P2): exp-001 is a three-cell sweep recorded as a one-cell round, and the ledger’s queue misreports it

The contract is explicit that a sweep is “ordinary rounds” viewed together — one
instance per round, `sweep.points` declared on the hypothesis so the ledger can show
filled cells. exp-001 measured `n = 10, 11, 12` in one artifact with
`instance: {point: 11}`, so the generated ledger shows H-016’s coverage as
`n: 10 11* 12` — two measured cells unstarred.
Since “an unfilled cell is a queue item”, an unattended runner following the ledger
would re-run `n = 10` and `n = 12`.

**Fix:** either split future sweep rounds one-per-cell (the contract’s intent), or give
the experiment schema a declared multi-cell form and teach `sweep_coverage` to read it.
Either way, annotate exp-001; do not rewrite it.

## Direction opinions

### <a id="d-1"></a>D-1 · `sqsearch` vs `sqpack-core` is two layers, not two competitors — “decide by measurement” is the wrong rule for half of it

The PR leaves the reconciliation open ("decide by measurement, not by which landed
first"). Measurement is the right rule for the *performance* half and the wrong rule for
the *trust* half, and the clean resolution is to name the layers:

- **`sqpack-core` owns validity semantics.** The Scalar-generic separating-axis
  predicate, certificates, the exact path — the spec’s one-predicate rule exists so that
  the fast check and the exact check cannot drift, and nothing about this PR changes
  that.
- **`sqsearch` owns move-loop energy.** Its `pair_depth` is a *metric* (penetration
  depth for annealing), not a verdict, and a search energy legitimately wants shapes a
  verdict never needs (linear penalties, λ ramps).
  A second implementation at that layer is fine — *as long as it never gets to say what
  is valid.*

Concretely: keep `sqsearch` as proposer #1 exactly as the revised Phase 3 says; treat
its `overlap ≤ 1e-12` as a screen that gates nothing downstream (the quench + exact
pipeline re-decides); and at record time, re-check recorded configurations against the
shared predicate — today that is the Python oracle (`sqpack.verify` with the float
backend costs milliseconds on records only, never on moves), later `sqpack-core`. The
selftest’s naive-form check is good but tests `sqsearch` against itself; a 20-line
differential test of `pair_depth == 0` against `sqpack`’s `separated()` on random
near-contact pairs would close the loop between the two codebases that already live in
this repository.

The JSONL seam, meanwhile, is a *good* boundary, not a stopgap: language-agnostic,
append-only, exactly what the proposer contract needs.
PyO3 is a quench-spine concern (Phase 1/2), not a proposer concern; nothing in Phase 3
should wait on it.

### D-2 · The process machinery is worth its weight — but hypothesis ownership needs one explicit rule

A fair worry about this PR is that it adds a second process system beside the beads and
the review’s run protocol.
Having run its gates and read its artifacts, this review’s judgment is that the weight
is earned: the campaign implements the run protocol *as validated artifacts* (its run
records are the manifests; its series are S0–S6; its ledger is the residue rule made
checkable), and exp-001’s self-caught pre-registration miss is exactly the class of
error prose protocols do not catch.

What is left implicit is ownership.
A hypothesis now exists in up to three forms: prose in the standing review’s register, a
codified registry artifact, and (eventually) beads.
Recommended rule, one sentence in the runbook: **once codified, the registry artifact is
canonical; the review’s register entry is historical; beads track build work, never
scientific claims.** Longer term, the register table in the review could be generated
from the registry — the same generated-tables discipline the frontier already uses — so
the two can never disagree.
And the reserved ids should be retired by codifying the remaining eleven entries
(`H-003`–`H-010`, `H-013`–`H-015`), which the PR already tracks; that item inherits
F-3’s sync problem.

### D-3 · The next experiments, in the order the artifacts themselves imply

The revised phase order is right, and this review endorses running it as written.
Within it, the highest-information next steps, cheapest first:

1. **H-018 today** — instrument-ready, minutes of compute, and its result reshapes
   everything after it (a basin-width number for Trump’s cell, from inside).
2. **H-002, the quench** — `scipy`-only, unblocks basin identity, the atlas, H-011,
   H-012, and the then-current `polished` label that exp-001’s own polish-vs-exploration
   distinction showed is urgent.
   The single-cell LP is verified; the loop is the work.
3. **H-011 → H-012** — the census and the premise test, exactly as Phase 5 orders them.
4. Only then strategy proposers (Phase 4), compared through one pipeline.

One addition: since the PR’s own correction demotes `n = 5`/`n = 10` to
machinery-validation, `s(17)` should enter the standing sweep early as the
mechanism-matched cell — cheap to carry from the start, and it is the only calibration
that speaks to record-finding rather than machinery.

### D-4 · File the second softschema limitation upstream

The `allOf`-under-`enforced` refusal is measured, reproducible, and currently documented
only in a schema comment (F-1). It is a distinct limitation from softschema#38 and
deserves its own upstream issue with the minimal repro; the schema comment should then
cite the issue number.
That is the pattern this repository already established, and it is how the workaround
(cross-field rules in `ledger.py`) gets retired eventually.

## Methodology

Reviewed 2026-08-23 in a fresh remote container against
`origin/claude/experiment-loop-access-6a0e36` at `5facf33`, checked out as a worktree;
base `origin/main` at `dbb098a` (the PR #4 merge).
Everything in “what was verified by running it” was executed here: the full `test.sh`
(with a local cargo building `sqsearch` and running its selftest), `ledger.py --check`,
`make skills-check`, direct jsonschema validation of all ten campaign artifacts, a
recomputation of exp-001’s table from its archived JSONL, a relative-link sweep over the
changed trees, and the two negative controls (a schema-invalid artifact through the full
gate for F-1; a rendered-field corruption to establish that only ledger-visible fields
are caught incidentally).
The SAT half-extent identity was re-derived analytically and cross-checked against the
selftest’s 200k-pair comparison; the drift analysis behind F-5 is from reading
`search.rs`’s accumulator arithmetic, not from an observed failure — it is a
sound-instrument argument, not a reproduced bug.
Bead absence (F-3) was established after a clean `tbd sync` reporting “already in sync”
against `origin/tbd-sync`. No changes were made to the PR branch; per the review
workflow, findings are recorded here and on the PR, not fixed.

## References

- [PR #5](https://github.com/jlevy/thinking-scratchpad/pull/5) — the branch under
  review.
- [Review: The Toolkit Docs and the First Experiment Series](review-2026-08-23-toolkit-docs-and-first-experiments.md)
  — the register (H-1–H-15), run protocol, and series plan the campaign codifies.
- [A Search Philosophy for Square Packing](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
  — the strategy layer the consolidation adopts; source of the calibration correction
  the campaign records.
- [Minimal packing toolkit plan spec](../specs/active/plan-2026-08-22-minimal-packing-toolkit.md)
  — revised by this PR; Phases 2–7 and the revision history.
- [Infrastructure for Square-Packing Exploration](../research/research-2026-08-22-infrastructure-for-packing-exploration.md)
  — the one-predicate rule and tier model behind D-1.
- `explorations/packing/campaign/` on the PR branch — the runbook, idea board, registry,
  series-000, exp-001, and `ledger.py`, all read in full.
- [softschema#38](https://github.com/jlevy/softschema/issues/38) — the prior upstream
  filing the F-1/D-4 limitation complements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

## Status Addendum — 2026-08-23, addressed in `060b99d`

Added by the PR author after acting on this review.
The findings above are unchanged; this records what happened to each.
Every P1 was reproduced before being fixed.

| Finding | Disposition |
| --- | --- |
| **F-1** schemas enforced by nothing | **fixed** — `ledger.py` validates every artifact against its declared schema at load time; an unloadable schema is a hard error, not a silent skip. Reproduced first (`priority: 0` passed the whole gate), then negative-controlled. |
| **F-2** archive cannot regenerate configurations | **fixed** — `run_baseline.sh` archives every record; the summary line carries the best configuration and a recomputed overlap. `exp-002`–`exp-004` re-run the sweep on the corrected instrument; all 135 archived records re-derive their own reported side. `exp-001` annotated, not rewritten. |
| **F-3** beads never reached the shared store | **fixed** — `tbd sync` landed them. The old tree is reconciled: `think-q3hl` and `think-pmhe` closed as superseded, `think-lpse` and `think-19gf` updated with cross-references rather than closed, since they are related but distinct. |
| **F-4** renumber residue | **fixed** — all five stale references corrected, plus a sixth the review did not catch (a miscounted `../` depth). Two compensating controls added: a relative-link checker, and a rule that a reserved id may be named but not linked. |
| **F-5** overlap guard on a drifting accumulator | **fixed** — recomputed from the stored configuration at record time; the selftest asserts the recomputed value. The two adjacent nits are recorded in the bead and left: both are sub-1% and neither affects a verdict today. |
| **F-6** three-cell sweep as a one-cell round | **fixed** — split one round per cell; `H-016` now shows `n: 10* 11* 12*`. Exposed a latent bug: `status_of` ranked `accepted` above `rejected`, so `n = 12` passing would have reported a refuted swept claim as confirmed. Corrected. |
| **D-1** name the layers | **adopted, and made a test** — `differential_test.py` checks `sqsearch`’s `pair_depth == 0` against `sqpack`’s `separated()` on 20,000 near-contact pairs, in `test.sh`, mutation-checked. The boundary is enforced rather than described. |
| **D-2** hypothesis ownership | **adopted** — one rule in the runbook: once codified the registry artifact is canonical, the register entry is historical, beads track build work and never scientific claims. |
| **D-3** `s(17)` into the standing sweep | **adopted** — added as the mechanism-matched cell, with value and attribution read from `frontier/n-017.md` (Bidwell 1998) rather than memory; the first draft credited Göbel/Bidwell, which the corpus does not support. |
| **D-4** file the softschema limitation upstream | **deferred** — filing an issue on another repository is an outward action awaiting a go-ahead. Tracked as `think-rk66`. |

Three things this review prompted that it did not ask for:

- **`conventions.md`** consolidates every rule the directory runs on and marks each
  `[checked]` or `[convention]`. Writing it forced three naming rules to become real —
  filenames must carry their own id, slugs must be kebab-case, series directories read
  `series-NNN-slug` — all negative-controlled.
- **A provenance check** in `test.sh`: recorded commits must be reachable from `HEAD`,
  and an orphaned one must carry an annotation.
  It reports `exp-001` exactly as F-2 describes.
- **The re-run reproduces `exp-001`’s numbers to every digit**, which was not guaranteed
  and is the strongest evidence the corrections touched the record rather than the
  search.
