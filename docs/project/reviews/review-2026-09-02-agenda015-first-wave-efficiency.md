# Review: Agenda 015 First-Wave Efficiency

**Date:** 2026-09-02

**Author:** Codex, for the project maintainers

**Status:** Complete BC-143 W5 receipt; decision is `no-change`

This is agenda-015’s first W5 `efficiency-loop` slice.
It applies the predeclared change-admission rule at frozen evidence revision `d15e96c8`
and changes no scientific instrument, result, criterion, threshold, or route.

## Verdict

Record **`no-change`**.

The registered wave-efficiency renderer refuses the mixed-harness lane records.
Sessions 079 through 081 declare `ClaudeEfficiencyRollup` receipts, while the renderer
accepts `CodexTaskTreeDelta/v1`. It therefore cannot produce a common lane table without
a tested adapter. D-421 and `think-mlwo` retain that tooling gap.

The one implementation candidate carried into this checkpoint is BC-142’s reachable-test
root map. It selects 13 of 115 test files for the benchmark root and refuses an unknown
root, but its control proves only one expected inclusion and one exclusion.
It does not prove equality with the reachable set.
The selection count and agenda-014’s 1,302 pytest items are also different units, so
they cannot supply a before/after repayment result.

Both candidates fail required guards.
No change is admitted.

## Frozen Evidence

The checkpoint revision is `d15e96c888794c486d3f40b9693fcf4b849f3dbc`. Its exp-056
checkpoint and progress pair have SHA-256
`62765d94098632743de91f60249fc20368c34144ce4b851a7c16345c195b9b15` and
`5b15a9ad1846ee6d31c8a5ce0b5cb8952f05bee72b568c3388a5448530c581ad`. The records tier
passed 26 of 58 named steps before the commit, and PR #75 leads with the checkpoint’s
recut branch-cost block.

BC-138 stopped before network access.
BC-140 and BC-142 are terminal partials with D-418 and D-420 retaining their incomplete
guards. BC-137 remained live with 72 agreeing rows through ordinal 71. Those are lane
outcomes, not substitutes for the unavailable W5 measurements.

Hosted checks on `d15e96c8` all pass: macOS portability in 64 seconds, Linux validation
in 609 seconds, and the required aggregator in 3 seconds.
They are end-to-end job times, not a profile of either candidate.

## Registered Renderer Outcome

From `packing/`, normal and optimized Python ran the same registered command:

```text
python -m devtools.render_wave_efficiency --lanes session-079 session-080 session-081 --coordinator session-078 --format json
```

Both exit 2 and print the same refusal:

```text
refused: session-079: expected one Codex receipt named for the session, found 0 Codex receipts and none named for it
```

No timing table is retained.
Hand-transcribing the Claude receipts into the Codex schema would violate OR-1 and
discard the harness-specific completeness and overlap semantics that make the receipts
interpretable.

## Change-Admission Test

| Candidate | Profile | Frozen before/after input | Equivalence | Rollback | Positive remaining-wall repayment | Disjoint | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC-142 reachable-test map | 13/115 selected at `d15e96c8`; no commensurate baseline | checkpoint frozen; no valid before/after pair | **fail** — no exact-set oracle | pass — map-only seam | **fail** — no like-for-like timing pair | pass | no-change |
| Mixed-harness renderer adapter | D-421 refusal only | no implementation or before/after pair | **fail** — no tested common schema | absent | **fail** — no measured candidate | pass | future W7 |

Agenda-015 requires every guard to pass.
A partial control or plausible saving is not an admission receipt.

## Routing Boundary

This W5 decision changes no lane exit.
BC-143 routes from the independently reviewed wave-one evidence: BC-139 stays stopped,
BC-141 may use only BC-140’s admitted n = 54 controls and frozen-input inventory, and
BC-137 may continue only while its observed prefix grows.
H-052, H-055, and H-058 remain governed by their own frozen criteria.

## Limitations

- The refusal supplies no cross-harness agent-active, command, wait, or output rate.
- The 13/115 file selection and agenda-014’s 1,302 pytest items are not the same unit.
- The coordinator’s task-tree receipt is a live lower bound and contains no Claude lane
  intervals.
- CI durations are end-to-end hosted-job times and do not isolate the root-map change.

These limits prevent a numeric comparison.
They do not weaken `no-change`, which follows from named admission guards that fail on
the frozen evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
