# Feature: A Shorter Website Development Loop

**Date:** 2026-10-10

**Author:** Codex, with delegated source analysis and Astra review

**Status:** Initial Repairs Merged; Cleanup Merged in PR #496; Review Follow-Up in
Progress

## Overview

Routine website changes reached a completed draft PR, but repeated validation and
runtime-only CI failures consumed hours.
Repair the development loop under `think-ht59`, alongside the website implementation in
PR #462.

## Goals

- Select tests because their inputs or contracts can change, rather than because a
  source string happens to contain a filesystem method name.
- Keep functional correctness failures distinct from shared-runner cost measurements.
- Remove assertions and setup that provide no independent evidence.
- Run one frozen repair batch through the handoff gate; repeat only invalidated
  evidence.

## Background and Review Findings

The delegated reviews read tbd’s engineering agent principles, general testing rules, CI
and quality gate rules, release engineering rules, general coding rules, and code review
rules. The relevant principles are independent evidence, no ceremony without a named
benefit, attributable performance measurements, and promotion of validated bytes.

| Finding | Evidence | Repair |
| --- | --- | --- |
| Unrelated tests selected | One changed website test selects 111 of 740 files: itself and 110 always-run walkers, with no import or text dependents. Quoted attack strings are classified as repository input. | Retain the conservative selector; defer syntax classification until its benefit earns the complexity. |
| Completed work fails as a hang | Head `34e5581ad` passes 408 site tests, four native HTTP cases, both floors, Workbench and 29 other checks, then fails at 399.44 s against a 330 s wall boundary. The budget record already documents 28 of 36 wall-only red pushes and up to 2.3× identical-code runner variation. | Report PR cost policy breaches separately; retain actual subprocess deadlines and explicit strict enforcement. |
| Unused fixture work | The amendment fixture renders every result page but uses only T-116 and T-110. Selecting those two retains byte-identical documents; the existing pair passes before and after, with setup 35.84 → 4.69 s. | Retain the existing selected-result renderer API. These are illustrative single-run timings, not a statistical speed claim. |
| Brittle duplicated oracle | A literal CSS selector-list assertion broke when the correct reduced-motion fix added row and segment selectors. The browser regression independently proves immediate spacing and absent transitions. | Remove the spelling assertion and retain the behavior regression. |
| Coordinator repetition | Small fixes repeatedly triggered broad local checks, reviews, pushes and another complete CI cycle. Some experiments followed aggregate time without attributing phases. | Batch independent repairs; reuse unaffected reviews; profile a phase before optimizing it. |

Raw validation receipts remain in external task scratch; the exact hosted
[frontend report](https://github.com/jlevy/squares/actions/runs/38070700709/job/114267324846)
is the durable CI reference.
Active effort was not separately metered, so elapsed calendar time is not reported as
labor time.

## Design

Keep the existing project validation entry point and release artifact promotion path.
The selector must remain conservative for unknown bindings, actual repository walks,
dynamic execution and suite-wide configuration changes.
An unexpectedly empty required selection or missing required dependency must still fail
visibly.

PR cost findings remain computed and annotated with their owning bead.
Completed wall measurements are not a substitute for subprocess timeout protection.
Functional failures, actual timeouts, explicit strict enforcement and main/full
checkpoint policy retain independent failure behavior.
No numerical budget increase is the proposed repair.

Temporary-root inference was rejected: it selected 110 files instead of 111 while
increasing cold selector time by about 20%. The smaller syntax classifier was also
rejected: a net reduction from 111 to 108 files did not earn roughly 140 lines of new
binding and string-use rules.
Its cold measurement overlapped other validation and establishes no runtime improvement.
The existing conservative selector remains unchanged.

The case-matrix consolidation was rejected and reverted: its cold pair changed 47.57 →
62.80 s and did not establish a gain.
Native-wrapper and worker-allocation controls also remain rejected.
Do not reopen these without a new measured hypothesis.

## Implementation Plan

- [x] Evaluate selector repairs; reject both candidates and retain the conservative
  selector.
- [x] Separate PR cost observations from completed correctness verdicts.
- [x] Reduce the two-result fixture to its actual inputs, with byte-equivalence
  evidence.
- [x] Remove the duplicate CSS selector-list assertion.
- [x] Review the frozen batch, run the canonical floor and required handoff checks, and
  update PR #462 and beads with the exact results.

## Testing Strategy

Keep selector investigation receipts as rejected alternatives, rather than adding new
selector machinery to this batch.
For policy, prove that completed advisory findings are reported, and functional errors,
real timeouts, explicit strict enforcement and missing trackers still fail.
Retain the existing direct and fetched result compatibility checks and the browser
reduced-motion regression.
No new benchmark suite is needed for these repairs.

## Initial Local Validation Receipt

Astra approved the frozen changes.
The 118 focused policy and CLI tests passed.
The canonical push prerequisite run passed 64 checks and failed only the missing plan
registry entry; that entry was repaired and the documentation check passed.
The remaining behavioral phase timed out at its unchanged 900-second guard after 1,883
passes, 57 failures or errors, and 16 skips.
It produced no final traceback or JUnit summary.
This is incomplete validation, not an aggregate pass.
Host load reached 184.66 on 10 CPUs.
The draft PR disclosed this incomplete local receipt.
Later exact-head hosted checks passed; the local run is retained as evidence of
development cost, not reclassified as a pass.

## Rollout and Follow-Up

PR #462 merged as `6038af33`. Its final Packing, Pages, and exact-tree Deferred checks
passed.
The deployment succeeded, but its publication audit passed 3,920 of 3,932 checks:
twelve GitHub source links returned HTTP 503. All twelve later returned HTTP 200 in
bounded probes. The retry passed 3,907 of 3,932 checks and failed on 25 GitHub HTTP 503
responses after 27m36s of checking.
Local paired HEAD and GET probes both returned 200; this does not establish
method-sensitive failure.
A complete local audit of the same deployed revision with the patched checker then
passed 3,932 of 3,932 checks in 511.65 seconds, with 993 unique transport requests and
no retries
([review C](https://github.com/jlevy/squares/pull/496#pullrequestreview-5481651340)
records the receipt).
After PR #496 merged as `8aba9508`, the hosted `verify-deployment` job passed in 3m45s
([run 38117038690](https://github.com/jlevy/squares/actions/runs/38117038690)).
`think-xio5` is closed.
`think-9k61` owns scoping pre-push prerequisites: the merged entry point runs all 65,
while its existing dependency selector reaches 9 for a website-test edit.
A broad package pattern still reaches 58 for the CI-policy module.
These counts establish selection overhead, not a wall-time prediction.
A single host snapshot read load 102.13 on 10 CPUs; avoid overlapping validators that
each claim the whole host, without attributing that load to this task alone.
Profile the remaining homepage and Atlas phases before considering further matrix
consolidation; map each proposed deletion to the independent contract it replaces.
Full-checkpoint placement requires an explicit coverage and cost record, not an
arbitrary reduction in test count.

## Follow-Up Cleanup Slices

The cleanup branch is `codex/website-cleanups`, based on merged `6038af33`. No
production behavior defect is established by the external-link failures.
Priority reflects verification and iteration cost.

| Priority | Work | Acceptance |
| --- | --- | --- |
| P1 | `think-2z6l`: recover publication verification | Preserve the failed receipt and obtain a complete successful audit of the deployed revision. |
| P1 | `think-hc4d`: deduplicate transport requests | Anchors share requests; queries remain distinct; failed responses and per-link diagnostics remain visible. |
| P2 | `think-9k61`: scope pre-push prerequisites | Use the complete changed-path set; retain unknown-input fallback and scientific, browser, and policy coverage. |
| P2 | `think-cpnb`: expose audit progress | Report phase wall, retries, and unique requests during execution. |
| P2 | `think-6y2j`: bound deployment verification | Enforce a 30-minute job ceiling without treating timeout as successful verification. |
| P3 | `think-srma`: measure forwarder waits | Preserve destination, query, and fragment checks while testing whether arrival needs full page load. |

The configuration-only test-placement task `think-xyub` is complete in PR #462. The
final hosted Packing and Deferred checks cover its merged implementation.
Do not reopen rejected selector experiments or infer wall savings from selection counts.

## Cleanup Implementation and Review

The cleanup branch captures changed paths once for both prerequisite and behavioral
selection. Empty or unclaimed changes retain the complete fallback; CI and full
checkpoint coverage are unchanged.
Its current ten-file change selects 59 of 65 prerequisites, followed by reachable
behavioral tests. The integrated run passed all 59 prerequisites, then its behavioral
phase timed out at the unchanged 900-second guard without a final pytest summary.
Total wall was 1,275.28 seconds.
This is incomplete validation; collect exact-head hosted coverage before closing the
cleanup.

The publication checker shares fragment-only HTTP requests while preserving each
original link verdict and distinct queries.
The retained audit has 359 repository link verdicts and 357 transport identities: this
saves two requests, not a substantial overall speedup.
Progress now reports phases, elapsed wall, requests, and retries.
Forwarders retain destination, query, and fragment assertions while waiting for
navigation commit. A controlled slow-image fixture took 2.375 seconds with a load wait
and 0.317 seconds with a commit wait.

The audit tests passed 104 checks; two browser forwarder controls passed.
Scoping controls passed 25 CLI tests.
The broader selection run passed 113 tests and failed one new test with an incorrect
expected check name; after correcting that expectation, nine affected controls passed.
Two independent Astra cross-reviews found no outstanding issues.
These focused receipts do not replace the integrated gate.

Keep `think-ht59` open for broader development cost and `think-9dhb` for controlled
browser timing enforcement.
This cleanup does not establish the nominal runtime budgets or justify removing further
independent checks. The integrated run’s `--jobs 2 --inner-jobs 2` does not impose a
two-worker host limit: the existing normal pytest lane derives nine workers from ten
CPUs minus two outer jobs plus one, with `PACK_JOBS=1`; its pool-heavy lane uses one
process with `PACK_JOBS=2`. Account for this allocation when scheduling validators
alongside other local work.

## Review Follow-Up

PR #496 merged as `8aba9508` before three later reviews were addressed: a full senior
review (E), a performance review (F) and a correctness review (G). The follow-up branch
`claude/pr496-review-fixes` (`think-jjs7`) carries their fixes.

- **Prerequisite attribution (G1, G2).** Push scoping trusted `Step.touches`, but 48
  attributed steps imported 171 files they did not claim, and `*.py` being claimed by
  the lint floor left no fallback.
  Every attributed step now claims the static import closure of what it runs; a contract
  test enforces it in 3 to 20 seconds, depending on the host and disk.
  The site renderers form one 138-file import cycle, so 17 steps claim it as a group and
  21 claim `packing/devtools/*` in all, against 6 before.
  A one-file `devtools` change now selects 21 of 65 prerequisites instead of 10; most of
  the added time is `exact verification` (118 s), which reaches the cycle through one
  function-local import (`think-2cuz`, review A4 on PR #507).
- **Bounded audit (F1, F2).** The 30-minute job ceiling killed the checker before it
  printed anything. The checker now stops itself at `--deadline-minutes 25` and prints
  what it reached. Timeouts and dropped connections are retried rather than ending the
  audit.
- **Smaller repairs.** JSON output stays one document under `--push` (E1, G4), selector
  errors name the snapshot (G3), the test doubles always receive `on_retry` (E2), the
  ceiling and deadline are pinned (E3), and the snapshot argument refusals are tested
  (E6). G5 needed no claim: the math-markup step never imports kpress.
- **Deferred under `think-ht59`.** Budgets for large narrow selections (`think-ri5z`),
  reusing the probe’s selection (`think-tqwo`), host-level handling of github.com
  throttling (`think-h7c0`), and claiming the paths that most often force the full
  fallback (`think-7qbv`).

## References

- [Validation loops](../../../../development.md#validation-tiers)
- [Website implementation plan](plan-2026-10-08-site-layout-and-navigation.md)
- `tbd guidelines general-eng-agent-principles`
- `tbd guidelines general-testing-rules`
- `tbd guidelines ci-and-gates-rules`
- `tbd guidelines release-engineering-rules`

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
