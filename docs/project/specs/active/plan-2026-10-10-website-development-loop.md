# Feature: A Shorter Website Development Loop

**Date:** 2026-10-10

**Author:** Codex, with delegated source analysis and Astra review

**Status:** Implementation Reviewed; Integrated Validation Pending

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
- [ ] Review the frozen batch, run the canonical floor and required handoff checks, and
  update PR #462 and beads with the exact results.

## Testing Strategy

Keep selector investigation receipts as rejected alternatives, rather than adding new
selector machinery to this batch.
For policy, prove that completed advisory findings are reported, and functional errors,
real timeouts, explicit strict enforcement and missing trackers still fail.
Retain the existing direct and fetched result compatibility checks and the browser
reduced-motion regression.
No new benchmark suite is needed for these repairs.

## Integrated Validation Receipt

Astra approved the frozen changes.
The 118 focused policy and CLI tests passed.
The canonical push prerequisite run passed 64 checks and failed only the missing plan
registry entry; that entry was repaired and the documentation check passed.
The remaining behavioral phase timed out at its unchanged 900-second guard after 1,883
passes, 57 failures or errors, and 16 skips.
It produced no final traceback or JUnit summary.
This is incomplete validation, not an aggregate pass.
Host load reached 184.66 on 10 CPUs; targeted diagnosis and exact-head hosted CI remain
with `think-o2jd`. The draft PR preserves this limitation.

## Rollout and Follow-Up

Land the reviewable repair batch in the existing draft PR. Keep the full pre-merge
checkpoint `think-xio5` open.
`think-9k61` owns scoping pre-push prerequisites: the current entry point runs all 65,
while its existing dependency selector reaches 9 for a website-test edit.
A broad package pattern still reaches 58 for the CI-policy module.
These counts establish selection overhead, not a wall-time prediction.
A single host snapshot read load 102.13 on 10 CPUs; avoid overlapping validators that
each claim the whole host, without attributing that load to this task alone.
Profile the remaining homepage and Atlas phases before considering further matrix
consolidation; map each proposed deletion to the independent contract it replaces.
Full-checkpoint placement requires an explicit coverage and cost record, not an
arbitrary reduction in test count.

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
