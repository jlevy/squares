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

Not owned: F2's backend/checker work (`think-3jp4`), C1 capture (`think-g2qn`), X1 Rust
(`think-ui2y`), Session 168 closure (`think-wcqs`), the standing verifier, PR #307
conflicts, or frontier admission. The user authorized only our new stack layer; PR #307
must not be modified, merged, or force-pushed.

Flag2's retained `PASS_SAVED_STALL` has zero exclusions. Its large historical checker
cost motivates profiling but does not establish a producer cache bottleneck, and it is
not rerun here. Producer cache eviction cannot fix standalone checker memory.

## Frozen W5 protocol

Declared before target execution on 2026-10-04. Representative input: pattern A, 16
bins, at most 12 rounds, collision enabled, envelope core, hull limit 16, no split, node
id `n17-W5-partner-memo-A`. Producer ceiling 240 seconds, saved checker 120 seconds. No
larger replacement input is authorized by an uninformative result.

First retain an unchanged baseline and a separate cProfile run. Record wall, CPU, actual
producer-process peak working set, canonical object size, rows, steps, memo generations,
and cached collision-domain entries. Serialization is timed separately; saved checking
runs in a cold process without producer import. Profile overhead is not a performance
comparison. A completed stall is evidence about the instrument's workload, not evidence
of infeasibility.

Only if the profile identifies material obsolete retention, evict replaced owner rows
after a complete step. Candidate and baseline must have byte-identical canonical
seed/node objects and equal rounds, closure, and checker counts. Adopt only with at
least 10% or 32 MiB lower peak memory and no greater than 10% wall regression; a one-run
result near either boundary is inconclusive. Relevant cache/split/tamper controls must
pass. W7/8-bin/6-round audit fixture supplies an independent correctness control if code
changes. Any candidate that changes proof grammar, exact arithmetic, scheduling, or
checker semantics is outside this W5 contract.

Commands are serial and supervised with whole-process-tree cleanup. Each slice is at
most 30 minutes. Stop at 16 GiB process memory, below 8 GiB available system memory, or
a 1 GiB certificate; 512 MiB is a warning. Session A ends by 08:31:41 +08:00, with at
least 15 minutes reserved for finalization. No need to consume the full budget.

## Validation status

The clean-base ledger check passed. The full fast gate at `234a07f4` failed before
useful validation: its bounded subprocess runner explicitly refuses Windows. This is an
environment limitation, not a proof failure. Targeted runs use a separately smoke-tested
Windows Job supervisor. The branch remains uncertified until a supported-host full gate
passes. No target result or optimization is claimed yet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
