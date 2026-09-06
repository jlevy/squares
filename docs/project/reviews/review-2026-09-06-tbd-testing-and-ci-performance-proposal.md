# Proposal: Testing and CI Performance Guidance

Draft for review; no upstream issue or pull request has been submitted.
This general proposal accompanies the
[validation efficiency and checkpoints plan](../specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md).
The project implementation and its measured results remain in that plan.

## Recommendation

Add one focused guideline, `testing-and-ci-performance.md`, with short crosslinks,
targeted guideline edits, and aligned commit/PR shortcuts.
The existing testing guide already requires independent evidence, fast inner loops,
optimization before deferral, explicit outer tiers, deterministic tests, and measured
timeout increases. Repeating those rules in four places would add maintenance without
closing the gaps.

The new guide should own the operational details that are missing: retained timing
records for long-lived work, interruption evidence, explicit feedback/checkpoint
coverage, total work versus elapsed time, and sound reuse across changes.
The existing guides continue to own assertion quality, gate correctness, agent conduct,
and golden comparison semantics.

## Reviewed Sources and Existing Coverage

Read from `jlevy/tbd` on 2026-09-06. Upstream main at audit completion was
`c43e2d41c245f57a3c9296894ae322269fd7278a`. The links below pin the exact audited
source; check the current upstream text before applying these edits.

| Source | Already covered; preserve it | Focused addition |
| --- | --- | --- |
| [general-testing-rules.md](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/guidelines/general-testing-rules.md) | Independent evidence per test; minimize runtime and maintenance; optimize setup/sleeps/startup before explicit slower tiers; deterministic clocks; measured timeout increases; no empty or silent skips | Crosslink from Related and the inner-loop section to the performance workflow |
| [ci-and-gates-rules.md](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/guidelines/ci-and-gates-rules.md) | Shared entry point; gate negative controls; tested program rather than shell logic; failure localization; caches must be performance-only; controlled/noise-aware performance gates | Crosslink; qualify the unconditional full pre-push instruction when a project has explicit fast feedback and a final checkpoint |
| [general-eng-agent-principles.md](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/guidelines/general-eng-agent-principles.md) | Detailed understanding, verification, end-to-end ownership, scope discipline, no ceremony without a named benefit | One extension to principle 10 linking cost attribution and retained timing evidence |
| [golden-testing-guidelines.md](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/guidelines/golden-testing-guidelines.md) | Captures performance-sensitive timing; filters unstable durations from goldens; immutable setup reuse; independent scenarios in parallel | Keep raw timing separately from normalized correctness goldens; make the sub-100ms target contextual rather than a reason to remove costly evidence |

No new universal time target, percentage improvement threshold, worker count, or
project-specific tier name is proposed.
Those require project measurements and belong in the adopting project’s configuration
and plan.

## Upstream Deduplication

A read-only GitHub search on 2026-09-06 covered issues containing performance, timing,
or checkpoint, and issues or PRs containing testing and guideline.
It found no dedicated validation-performance issue.
This is a scoped search result, not proof that no related work exists in upstream beads.

The related merged [PR #260](https://github.com/jlevy/tbd/pull/260) already strengthens
independent evidence, non-vacuous tests, efficiency, portable goldens, and testable CI
programs. [PR #261](https://github.com/jlevy/tbd/pull/261) removes duplicated guidance
and corrects guideline discovery instructions.
Both are included in the audited main revision.
This proposal builds on those rules and gives detailed timing retention and checkpoint
cost one owner. The only matching issue,
[closed #161](https://github.com/jlevy/tbd/issues/161), concerns context-loading
performance rather than test or CI performance.

Recommend one focused upstream proposal after draft review, with links to these prior
changes. Recheck open issues and the upstream guideline-creation shortcut immediately
before filing or implementing; no local guideline fork is needed for this proposal.

## Proposed New File

Path: `packages/tbd/docs/guidelines/testing-and-ci-performance.md`

The following fenced block is the complete proposed document.

~~~~markdown
---
title: Testing and CI Performance
description: Preserve validation evidence while reducing feedback and checkpoint cost; retain detailed timings, compare elapsed time and total work, bound parallelism, and invalidate reused evidence safely.
author: Joshua Levy (github.com/jlevy) with LLM assistance
category: general
---
# Testing and CI Performance

**Related**:

- `general-testing-rules` (test value, determinism, and explicit outer tiers)
- `ci-and-gates-rules` (gate correctness, wiring, and attributable thresholds)
- `golden-testing-guidelines` (stable correctness recordings)
- `general-eng-agent-principles` (end-to-end ownership and justified process)

Improve how quickly contributors obtain trustworthy evidence. Keep everyday feedback
fast and make expensive final checks affordable. A slow run's measured duration does
not establish that its cost is necessary.

## Review Evidence and Cost Together

Apply the independent-evidence rule in `general-testing-rules` to each expensive test,
control, or job. Record its contract, boundary cases, useful failure localization,
invalidating inputs, measured cost, and any computation shared with other checks.

Preserve overlapping execution when it protects a distinct interface or independent
oracle. Few recent failures do not prove a check has no value. Reduce redundant setup,
duplicate computation, and avoidable serial work before moving evidence to a slower
tier. When replacing a costly check, show which cheaper evidence preserves each
contract and retain a known violation that the replacement rejects.

## Separate Feedback From Final Checkpoints

Define the small checks used while editing, the coverage required on ordinary commits,
and the complete checkpoint required for final review or release. Use the same project
entry point with explicit selections, and document what each selection establishes.

Cheap coverage belongs in ordinary feedback. Run justified expensive checks at the
declared final boundary and again when changes invalidate their evidence. A scheduled
or post-merge run cannot establish that a pre-merge checkpoint passed. Checks that
require external services or special hardware need an explicit acceptance boundary,
owner, and reported limitation; an unavailable check is not a pass.

Test the selections as a coverage contract: every intended check has a placement and
each aggregate propagates failure, cancellation, missing prerequisites, and empty
selections correctly. Report whether a checkpoint is required by repository settings
or is advisory evidence that a reviewer must inspect. Keep required context names
stable when changing display names or scheduling.

## Retain Detailed Timings for Long-Lived Work

Every long-lived run or test must produce retained machine-readable timing records and
a readable summary. Attribute time to individual tests, controls, and phases, including
setup and teardown; separate queue, setup, and execution when those stages exist.
Aggregate elapsed time alone cannot explain the cost.

Record the source revision and dirty state, exact command and selection, relevant
configuration, runtime/toolchain, host, worker limits, cache regime, and outcome. Include
failed, timed-out, and cancelled work. Write completed measurements incrementally and
retain partial output when interrupted. Mark interrupted or incomplete observations
explicitly; do not present their shorter time as an improvement. Document any hard-kill
or missing-provider-data limitation instead of inventing completed timings.

Use existing test-runner and CI reports when they contain this detail. Add a maintained
instrument with a known-failure test when they do not. Keep performance measurements
separate from normalized golden files: removing a duration from a correctness diff
must not discard the timing record used for performance analysis.

Exercise recorder failures as well as workload failures: a failed artifact write must
release borrowed workers, snapshots, and other bounded resources. Keep capture
configuration out of nested isolated workloads unless propagation is intentional and
tested, so instrumentation cannot change which refusal a negative control exercises.
A focused regression should prove cleanup and parent recording survive without
starting a second potentially blocked worker.

## Measure Elapsed Time and Total Work Separately

Elapsed time measures the contributor's wait. Summed job or worker durations measure
work spent across concurrent execution; billed runner time includes setup and other
provider costs. Report the quantities actually measured and their boundaries. Summed
overlapping phase durations are not elapsed time or necessarily CPU time.

State whether CPU accounting includes threads and descendant processes. A parent
process counter may miss pool or service workers, or charge a child's earlier work when
it is reaped later. Label incomplete observations and never use them as complete test
CPU for a threshold or efficiency claim.

Before benchmarking, declare the baseline, target metric, equivalence checks, and
acceptance rule. Compare repeated runs under comparable source, host, configuration,
and cache conditions; interleave baseline and candidate when shared-host noise matters.
Report variation and retain negative results. One successful CI run verifies integration
but does not establish a statistical speedup. Use the attributable-threshold rules in
`ci-and-gates-rules` rather than failing unrelated changes on noisy timings.

## Put Bounded Parallelism on the Critical Path

Measure which job or phase determines completion before adding runners. A job split can
remove queueing but cannot shorten an indivisible operation within a job. Consider
algorithm improvements and shared immutable setup before duplicating that operation.

Bound both outer jobs and internal worker pools, including subprocesses that ignore the
outer worker setting. Measure startup, repeated setup, total work, and elapsed time;
state when reduced latency costs more compute. Verify identical selection, independent
worker state, deterministic results where required, and failure/cancellation propagation.

## Give Every Check One Stable Identity

Expose the existing gate inventory as named checks with stable family membership.
Examples of families are record validation, fast behavior, slow behavior, exhaustive
replay, and negative controls; use each project's existing names. A family selector
expands into the same check identities as the full entry point. It is a supported
selection interface, not an ad hoc shell command assembled from filenames.

For each check, declare what contract it establishes, its dependencies, the executable
command or program, and the result evidence that proves completion. Keep independent
oracles and refusal controls as separate identities when they protect different
contracts, even if their implementation shares setup. A family with no resolved checks
is an error unless the project explicitly defines and reports it as inapplicable.

## Make Invalidation a Testable Dependency Contract

Add explicit dependency declarations to that inventory: implementation modules and
transitive helpers, selected test and control definitions, registries and data,
schemas, generated inputs, renderer or generator sources, runtime and lockfiles,
submodule revisions, runner configuration, and relevant environment settings.

At selection time, resolve the exact comparison base and current source state. At reuse
time, fingerprint the effective inputs for that check: source revision and dirty state,
base revision, dependency content digests, test selection and collected case identities,
data/schema versions, interpreter/runtime/dependency versions, command/configuration,
and any worker, seed, platform, or environment setting that can affect its contract.
Retain the dependency-resolution version as an input too: changing the resolver cannot
silently approve results computed under its older interpretation.

Whole-tree changes and check-specific invalidation are distinct. A prose edit may
invalidate a rendered-document check while leaving a mathematical replay unaffected.
A document containing executable examples or a registry consumed by a checker is an
input; a `.md` suffix alone proves nothing. Unknown or dynamically discovered inputs,
ambiguous base ancestry, missing fingerprints, uncertain dependency reachability, or a
changed collection must conservatively select the affected full family. If family
reachability itself is uncertain, select the complete checkpoint.

## Plan Before Running and Show Coverage Afterward

Have the maintained runner emit a machine-readable plan plus a short readable summary:
check ID, requested family, resolved dependencies, and disposition with its reason.
Before execution, dispositions are “run”, “reuse candidate”, or explicitly inapplicable.
After validation, distinguish freshly passed, validly reused, failed, canceled,
incomplete, invalidated, and inapplicable results. Keep the original run and receipt
identity for every reused result. A skip is never a pass.

The final aggregate must prove that the union of fresh successful receipts and valid
reused successful receipts covers every check required by the requested checkpoint.
Reject missing checks, duplicate or conflicting identities, incompatible receipt
contracts, unsuccessful or partial original runs, stale or unavailable input evidence,
and aggregation that reports a selected subset as a complete checkpoint. Preserve all
failures and interruptions, including ones from attempted reruns; reuse must not hide
new contrary evidence.

## Keep the Final Checkpoint Complete

Cheap checks remain routine commit feedback. Justified expensive families run when
invalidated and at the project's declared final boundary. A complete final checkpoint
may compose fresh and reused evidence only when the project's explicit policy permits
that and the runner verifies the dependency contract. If the project requires a fresh
full run, retain that requirement. A forced-fresh or strict-checkpoint mode should use
the same inventory and execute every required check, giving a reference for periodic
validation of the reuse path and for uncertain changes.

Document whether required hosted contexts enforce the complete checkpoint or whether
additional advisory/local evidence must be inspected. Do not relabel a green ordinary
PR context as full validation. A change after the final checkpoint triggers the same
invalidation procedure against the final reviewed source and base, including merged or
stacked-branch changes. Scheduled and post-merge checks do not retroactively establish
pre-merge coverage.

## Acceptance Evidence for the Tooling Change

Add focused tests to the existing gate-contract suite. Exercise a prose-only change,
an executable-document change, a transitive shared-helper change, data/schema/runtime
changes, a changed base, changed test collection, and an unknown dynamic dependency.
Assert which named checks invalidate and that unknowns widen selection. Exercise a
missing, failed, canceled, stale, contradictory, or tampered receipt and prove that the
aggregate cannot claim full coverage. Retain negative controls for accidentally omitted
checks and failure propagation.

Compare the selected/reused path against forced-fresh execution on representative
changes, including known contract violations. Report selected families, fresh and
reused check counts, false reuse or missed-invalidations found, wall time, and summed
allocated work with detailed receipts. Acceptance requires preserved contracts and no
false passes in these probes before crediting reduced latency. Worker parallelism or
cache hits alone do not establish lower total cost.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
~~~~

## Focused Edits to Existing Files

Apply these snippets at the named headings; they are proposed source text, not an
instruction to rewrite the surrounding documents.

### General Testing Rules

In `packages/tbd/docs/guidelines/general-testing-rules.md`, add to Related:

```markdown
- `testing-and-ci-performance` (timing records, feedback/checkpoint placement,
  parallelism, and safe reuse of validation evidence)
```

After `Keep the Inner Loop Fast and Put Costly Evidence in Explicit Outer Loops`, add:

```markdown
For retained timing records, final-checkpoint coverage, and measured scheduling changes,
follow `testing-and-ci-performance`. Its performance workflow builds on these test-value
rules; it does not replace an independent oracle with a faster but weaker assertion.
```

### CI and Quality Gate Rules

In `packages/tbd/docs/guidelines/ci-and-gates-rules.md`, add to Related:

```markdown
- `testing-and-ci-performance` (cost attribution, explicit checkpoint coverage,
  bounded parallelism, and validation-result invalidation)
```

Under `Use Hooks for Local Feedback, Not as CI Authority`, replace:

```markdown
Hooks are the fast local pass, not the gate.
Pre-commit auto-fixes staged files; pre-push runs the full verify gate; CI repeats it so
a `--no-verify` commit cannot land unchecked.
```

with:

```markdown
Hooks provide local feedback; CI supplies the enforced evidence.
Pre-commit runs the project's fixing commands and pre-push runs its declared verify
selection. A project may separate fast feedback from a complete final checkpoint;
document and test the combined coverage through `testing-and-ci-performance`.
CI must enforce the promised checks regardless of whether a contributor used
`--no-verify` locally.
```

Rationale: the existing unconditional full-pre-push sentence conflicts with the explicit
outer tiers already allowed by General Testing Rules.
This edit reconciles the two without making deferred checks optional or prescribing a
platform-specific workflow.

### Engineering Agent Principles

At the end of principle 10 in
`packages/tbd/docs/guidelines/general-eng-agent-principles.md`, add:

```markdown
    When a test or run is long-lived, retain detailed timings and outcomes before
    calling its cost necessary. `testing-and-ci-performance` specifies the records,
    evidence-preserving cost review, and distinction between ordinary feedback and
    final checkpoints. Total elapsed time without attribution is insufficient.
```

Rationale: principle 10 already rejects ceremony; this adds the operational obligation
to measure cost without duplicating that principle.

### Golden Testing Guidelines

In `packages/tbd/docs/guidelines/golden-testing-guidelines.md`, extend Related with
`testing-and-ci-performance`.

At the end of `2. Classify Fields as Stable or Unstable`, add:

```markdown
Normalize durations in the correctness golden, but retain raw performance measurements
separately when they are used to diagnose or budget a run. Include failed and
interrupted work with its status; see `testing-and-ci-performance` for the timing
record contract. Stable golden comparison and performance analysis need different
representations of the same execution.
```

Replace the TL;DR bullet `Keep scenarios few but end-to-end; tests must run fast in CI
(<100ms each).` with:

```markdown
- Keep scenarios few but end-to-end; use the fast-CI guidance below to set and measure
  an appropriate feedback budget.
```

Replace `Golden tests should run in under 100ms per scenario:` with:

```markdown
For in-process mocked scenarios, under 100ms is a useful feedback target. Measure
process startup and setup separately, and set the project's budget from its execution
shape. Preserve costly independent evidence in an explicit checkpoint rather than
weakening it to meet a universal per-scenario number:
```

Replace that section’s closing `Why` paragraph with:

```markdown
**Why**: Fast scenarios can run on ordinary commits. Evidence requiring a slower
execution environment still needs an explicit checkpoint and cannot be replaced by a
mock when the real boundary is the behavior under test. See `general-testing-rules`
and `testing-and-ci-performance` for placement and measurement.
```

Rationale: the existing guide already captures timing and deliberately strips durations
from golden comparison; the missing distinction is retaining the raw observation for a
different purpose. The target edits avoid presenting sub-100ms as a portable correctness
rule for subprocess or external-boundary scenarios.

## Commit and PR Shortcut Consistency

Additional read-only audit at the same upstream revision found one direct conflict:
`precommit-process` step 3 requires the entire integration suite before every commit.
`code-review-and-commit` delegates to it and therefore inherits that cost.
The two PR wrappers equate completed hosted CI with readiness without requiring an
explicit final checkpoint that may include checks outside ordinary CI.
`address-pr-review` already runs affected tests per fix and then a full final
verification; preserve that split.

### Exact Focused Replacement in Pre-Commit Process

Replace the heading and first paragraph of step 3 with:

> **Run the project’s declared commit checks:**
> 
> Run the checks the project requires for an ordinary commit, including every cheap
> check and the tests affected by the change.
> Use the project’s shared validation entry point and documented selection; do not
> invent a narrower selection to save time.
> If the project does not declare separate feedback and checkpoint selections, run its
> full check suite. Before final review or merge, establish the project’s complete final
> checkpoint, including justified expensive checks that ordinary commits defer.
> Use `tbd guidelines testing-and-ci-performance` for timing evidence and safe
> invalidation of prior results.

Keep the following “YOU MUST FIX all issues found” instruction unchanged.
In step 5, change “If all checks pass, commit directly” to “If the required commit
checks pass, commit directly.”
This changes routine placement, not permission to ignore a failing check or bypass
hooks. The final checkpoint must certify the source being reviewed; reuse needs an
explicit affected-source argument under the new guide.

### Wrappers and Final Readiness

- In `code-review-and-commit`, append to step 1: “The precommit process owns the
  project’s commit selection and final-checkpoint boundary; do not repeat the full
  checkpoint on every intermediate commit unless the project requires it.”
  Keep its CI wait, failure repair, push, and bead-update requirements unchanged.
- In both `create-or-update-pr-simple` and `create-or-update-pr-with-validation-plan`,
  replace step 9’s first sentence with: “Confirm CI’s final result and whether the
  project’s complete final checkpoint certifies this source revision.
  Declare the PR ready for final review only when both requirements are satisfied;
  otherwise report the pending checks explicitly.”
  Crosslink the new guideline there.
  This does not prevent creating an early PR to obtain CI feedback; it prevents treating
  that feedback as complete final evidence.
- In `create-or-update-pr-with-validation-plan`’s Test Plan checklist, add: “Project’s
  full final checkpoint passes for the reviewed source; name the command, source
  identity, receipt, and any explicit limitation.”
  Keep unit, build, manual, and edge-case checklist entries.
- In `address-pr-review` step 7, replace its first bullet with: “Run the project’s full
  final checkpoint, including its full test suite and lint; use the documented command
  and record the source identity and result.
  Step 6’s affected-test runs provide feedback during fixes and do not replace this
  final verification.”
  Keep the CI failure/fix/restart rule unchanged.
  A link to the performance guide supplies reuse and timing detail without repeating the
  full policy here.

These are narrow process alignments, with `precommit-process` as the owner of routine
commit selection and the performance guide as the owner of measurement, final checkpoint
evidence, and invalidation.
No new shortcut or framework is needed.

Audited shortcut sources:

- [Pre-commit process](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/precommit-process.md)
- [Code review and commit](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/code-review-and-commit.md)
- [Simple PR wrapper](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/create-or-update-pr-simple.md)
- [PR with validation plan](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/create-or-update-pr-with-validation-plan.md)
- [Address PR review](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/address-pr-review.md)

## Registration and Discovery

1. Create `packages/tbd/docs/guidelines/testing-and-ci-performance.md` with the proposed
   `title`, `description`, `author`, and `category: general` frontmatter.
   `general` is already valid in `packages/tbd/src/lib/doc-categories.ts`; no category
   vocabulary change is needed.
   Put the single `**Related**:` block immediately below the H1, before the
   introduction, as the authoring shortcut specifies.
   No `globs` or `alwaysApply` field is needed for this language-neutral topic.

2. Add this exact mapping under `docs_cache.files` in `.tbd/config.yml`:

   ```yaml
   guidelines/testing-and-ci-performance.md: internal:guidelines/testing-and-ci-performance.md
   ```

3. Add `'testing-and-ci-performance'` to `CROSS_CUTTING_NAMES` in
   `packages/tbd/src/file/doc-cache.ts`. `category: general` alone does not put it in
   the cross-cutting group; this name otherwise reaches “Docs, process & tooling”.
   Keep `ALWAYS_LOAD_NAMES` unchanged.

4. Add the name to the existing language-neutral topic assertion in
   `packages/tbd/tests/guideline-groups.test.ts`. Existing tests also verify every
   explicitly grouped name has a bundled document.
   No new test framework is needed.

5. Add the guide to root `README.md` under Built-in Engineering Knowledge and make the
   four narrow crosslinks/consistency edits in the proposal.
   Do not hand-edit `packages/tbd/README.md`, which the build copies from root.

The build’s `packages/tbd/scripts/copy-docs.mjs` copies bundled docs into `dist/docs`.
The local built CLI then syncs the configured cache and regenerates skill directories.
A globally installed `tbd` tests the published bundle, so it cannot verify this
addition.

## Validation Commands

Run from an upstream tbd checkout after the source changes:

```shell
pnpm build
node packages/tbd/dist/bin.mjs docs sync
node packages/tbd/dist/bin.mjs setup --auto
node packages/tbd/dist/bin.mjs guidelines testing-and-ci-performance
node packages/tbd/dist/bin.mjs guidelines --list
pnpm --filter get-tbd exec vitest run tests/guideline-groups.test.ts tests/guideline-budget.test.ts tests/doc-categories.test.ts tests/doc-cache.test.ts tests/doc-sync.test.ts tests/docs-sync-output.test.ts tests/integration-files.test.ts
pnpm ci
```

Inspect that the built and cached files exist at
`packages/tbd/dist/docs/guidelines/testing-and-ci-performance.md` and
`.tbd/docs/guidelines/testing-and-ci-performance.md`, and that the listing puts the name
under Cross-cutting engineering topics.
Inspect generated skill-surface diffs from `setup --auto`; the integration-file tests
guard those surfaces.
The focused tests are an early check; `pnpm ci` is the repository’s existing full
formatting, lint/type, build, and unit-test command.
Follow any additional current release or PR requirements when the upstream work is
actually implemented.

## Discovery Sources

- [Guideline-authoring shortcut](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/docs/shortcuts/standard/new-guideline.md)
- [Cache and grouping implementation](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/src/file/doc-cache.ts)
- [Cache registration](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/.tbd/config.yml)
- [Category vocabulary](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/src/lib/doc-categories.ts)
- [Grouping tests](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/tests/guideline-groups.test.ts)
- [Bundling script](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/packages/tbd/scripts/copy-docs.mjs)
- [Root commands](https://github.com/jlevy/tbd/blob/c43e2d41c245f57a3c9296894ae322269fd7278a/package.json)

## Submission Scope

This updated draft adds family-selection and receipt-reuse contracts, recorder failure
and nested-isolation guards, commit/PR shortcut alignment, and verified discovery steps.
It remains a proposal awaiting user approval to file upstream.
No upstream issue or PR has been submitted.

Check that the existing guides and shortcuts route to the new policy without weakening
independent evidence, final checkpoint coverage, or failure repair.
Keep project-specific latency targets and gate names out of upstream text.
Local shortcut customizations remain untouched.
Recheck upstream open work and source drift before filing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
