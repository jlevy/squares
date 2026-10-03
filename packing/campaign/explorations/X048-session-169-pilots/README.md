# Session 169: bounded producer memory investigation

Owner: `Guzhou0806-Codex-T0`, bead `think-wn6x`, branch `guzhou/n17-p01-partner-memo`.
Base: PR #307 at `234a07f4`. This is an efficiency investigation, not a new mathematical
exclusion.

## Scope and choice

Three independent Sol 6.1 reads compared these candidates before implementation:

| Candidate | Mechanism and cheapest test | Falsifier and decision |
| --- | --- | --- |
| Adaptive south-wall continuation | Refine the eight live owners; a small adaptive run could test whether wall propagation resumes. | Existing K2/S2 ownership (`think-e17c`, `think-gygy`, `think-j6qy`) prevents this session from executing it. Deferred. |
| Producer memo lifetime | `PartnerMemo` strongly retains accepted row objects from obsolete generations. Measure the frozen slice below before changing anything. | Reject if obsolete entries are immaterial, certificate values differ, or gains fail the frozen threshold. Selected primary. |
| Residual-piece compatibility graph | Preserve each residual polygon as an atom; pair collision plus shared third-owner choices may remove combinations lost by convexification. B/16-bin accepted rows, at most 32 atoms per owner and 300 seconds, would discriminate this idea. | No extra whole-row deletion or an endpoint witness removed defeats the frozen abstraction. Future candidate only; no graph instrument or scientific claim in this slice. Generic triple no-goods already appear as idea #215. |

Not owned: F2’s backend/checker work (`think-3jp4`), C1 capture (`think-g2qn`), X1 Rust
(`think-ui2y`), Session 168 closure (`think-wcqs`), the standing verifier, PR #307
conflicts, or frontier admission.
The user authorized only our new stack layer; PR #307 must not be modified, merged, or
force-pushed.

Flag2’s retained `PASS_SAVED_STALL` has zero exclusions.
Its large historical checker cost motivates profiling but does not establish a producer
cache bottleneck, and it is not rerun here.
Producer cache eviction cannot fix standalone checker memory.

## Frozen W5 protocol

Declared before target execution on 2026-10-04. Representative input: pattern A, 16
bins, at most 12 rounds, collision enabled, envelope core, hull limit 16, no split, node
id `n17-W5-partner-memo-A`. Producer ceiling 240 seconds, saved checker 120 seconds.
No larger replacement input is authorized by an uninformative result.

First retain an unchanged baseline and a separate cProfile run.
Record wall, CPU, actual producer-process peak working set, canonical object size, rows,
steps, memo generations, and cached collision-domain entries.
Serialization is timed separately; saved checking runs in a cold process without
producer import. Profile overhead is not a performance comparison.
A completed stall is evidence about the instrument’s workload, not evidence of
infeasibility.

Only if the profile identifies material obsolete retention, evict replaced owner rows
after a complete step.
Candidate and baseline must have byte-identical canonical seed/node objects and equal
rounds, closure, and checker counts.
Adopt only with at least 10% or 32 MiB lower peak memory and no greater than 10% wall
regression; a one-run result near either boundary is inconclusive.
Relevant cache/split/tamper controls must pass.
W7/8-bin/6-round audit fixture supplies an independent correctness control if code
changes. Any candidate that changes proof grammar, exact arithmetic, scheduling, or
checker semantics is outside this W5 contract.

Commands are serial and supervised with whole-process-tree cleanup.
Each slice is at most 30 minutes.
Stop at 16 GiB process memory, below 8 GiB available system memory, or a 1 GiB
certificate; 512 MiB is a warning.
Session A ends by 08:31:41 +08:00, with at least 15 minutes reserved for finalization.
No need to consume the full budget.

## Measured result

Decision at the frozen experiment: **ADOPT the bounded cache-lifetime change**.
Ownership update: M1 independently landed the same lifetime fix in parent commit
`7f1db8a42`, followed by `601bbf110`’s streaming checker.
This layer was rebased onto `601bbf110` and its duplicate producer edit removed.
**The final PR contributes independent measurement, a diagnostic and a regression test;
M1 owns the production implementation.** The historical isolated candidate is retained
as [a small patch](receipts/isolated-candidate.patch) against `234a07f4`; it changes no
geometry, row schedule, arithmetic, certificate or checker.

| Frozen input | Baseline | Candidate | Same work |
| --- | --- | --- | --- |
| A producer process peak | 165,134,336 bytes | 130,379,776 bytes | 21.0% lower (33.14 MiB); same 42 steps and 672 rows |
| A observed producer wall / CPU | 14.567 / 14.531 s | 12.781 / 12.719 s | Observer overhead included; not an isolated speedup claim |
| A canonical node size | 14,649,116 bytes | 14,649,116 bytes | Seed and node compared byte for byte; both equal |
| A final memo / obsolete entries | 736 / 656 | 80 / 0 | Final cached domain values 45,056 / 4,096 |
| A independent saved checker | PASS_SAVED_STALL | PASS_SAVED_STALL | 42 steps, 672 rows, 52,871 events; producer never imported; zero exclusions |
| W7 correctness control | 14-step saved object | Byte-identical saved object | Same complete rounds, closure and row counts |

The separate [profile](receipts/A-profile.txt) puts most time in row geometry:
`produce_row` 14.08 s cumulative, subtraction 7.28 s and clipping 6.00 s. These nested
times must not be added.
The change addresses retained memory, not the dominant arithmetic path.
Serialization took 0.414 s before and 0.379 s after; pipeline process peaks were
192,638,976 and 161,914,880 bytes.

[The comparison receipt](receipts/comparison.json) and before/after receipts retain the
measurements. The small W7 control is saved under `objects-W7/`. The 2.7 MB compressed A
node is retained in the operator local `runs/w5-A-baseline-objects/` and
`control/p01/retained-large-objects-A/`, outside Git: publishing it exceeded the
repository mutation-snapshot size guard.
The first replay command below regenerates its canonical bytes; receipts retain existing
certificate identifiers and the direct comparison outcome.
Duplicate candidate objects are not published.
Peak memory is the actual Python process high-water mark through producer completion,
including imports and frame construction.
The observer scans the memo and has lower overhead after eviction; the wall difference
cannot all be attributed to the producer change.
This is one cold process per version, not a general speed estimate or a Flag2
extrapolation.

A separate Sol 6.1 xhigh soundness read checked the complete-step boundary, adaptive
predecessor lifetime, object-identity reuse, and observer references.
It found no defect; it did not independently rerun the experiment.
The targeted cache, adaptive split, tamper/refusal, and full blind/wall verifier tests
passed: **73 tests in 20.91 seconds**. The new regression bounds the retained
generations across a multi-round W7 production.

Replay from `packing/` with the pinned environment:

```bash
uv run --frozen --all-extras --group dev python -m devtools.profile_n17_partner_memo NEW_OUTPUT
uv run --frozen --all-extras --group dev python -m devtools.profile_n17_partner_memo PROFILE_OUTPUT --profile
uv run --frozen --all-extras --group dev python -m devtools.check_n17_subpattern --check-saved NEW_OUTPUT --max-seconds 120
```

Baseline production used unchanged `234a07f4` producer code; candidate measurements used
the retained isolated eviction patch.
The checker source was unchanged at `234e65efc`; its `dirty: false` field covers that
checker entry point, not the entire working tree.
Later parent streaming changes must not be credited to this single-variable comparison.
A fresh check on parent `601bbf110` reproduced the same seed/node bytes, 42 steps and
672 rows, with 130,387,968 bytes producer peak and 135,819,264 bytes pipeline peak.
That run confirms compatibility; it is not a new isolated optimization comparison.

## Validation status

The clean-base ledger check passed.
The full fast gate at `234a07f4` failed before useful validation: its bounded subprocess
runner explicitly refuses Windows.
This is an environment limitation, not a proof failure.
Targeted runs use a separately smoke-tested Windows Job supervisor.
The branch remains uncertified until a supported-host full gate passes.
Initial hosted validation passed the test shards but rejected this new README’s missing
document-map entry; that narrow metadata omission is fixed in this layer.
The initial main-mergeability failure names the inherited `SYNOPSIS.md` conflict.
No new scientific exclusion or full optimality result is claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
