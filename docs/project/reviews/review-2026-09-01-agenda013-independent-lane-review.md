# Independent Review: Agenda 013 Research Lanes

**Date:** 2026-09-01

**Author:** Codex, for the project maintainers

**Status:** Complete — five passes and one bounded caveat

This review applies agenda-013’s independent replay gate to all six first- and
second-wave decisions in the n = 17, n = 68 and n = 50 lanes.
It records what each reviewer reproduced, which mutation fired, the accepted claim
boundary and whether BC-121 may clear an experiment’s `needs_review` flag without
changing its frozen decision.

## Frozen Review Surface

| Item | Frozen value |
| --- | --- |
| Scientific evidence revision | `529b6729155458c940999cd11074f05ae9f1ce3d` |
| Packet commit | `90ced9098157546da388ebc89dabd224e6ed58b0` |
| Packet SHA-256 | `c40af931289adde7ff22e8000f5b1fc50996183c34e45090796ce256185636a0` |
| Packet checkpoint | `e2d53d6cfa06c589f534a0f332d5f8f45251ff54` |
| Review window | `2026-09-01T15:46:55Z--17:16:55Z` |

The packet set is
[review-2026-09-01-agenda013-second-wave-packets.md](review-2026-09-01-agenda013-second-wave-packets.md).
Its artifact hashes, exact commands, mutations and claim boundaries are part of this
review contract.

## Independent Assignments

| Packet | Reviewer | Separation from source under review | Return deadline |
| --- | --- | --- | --- |
| n = 17 / H-052 | `/root/tooling_leverage` | Authored the n = 68 lane, not the n = 17 source | `16:46:55Z` |
| n = 68 / H-053 | `/root/negative_queue` | Authored the n = 50 lane; did not write the n = 68 source | `16:46:55Z` |
| n = 50 / H-054 | `/root/math_frontier` | Authored the n = 17 lane, not the n = 50 source | `16:46:55Z` |

Reviewers may read frozen repository bytes, run the named checker or literal command,
and mutate only pytest or operating-system temporary data.
They may not edit a repository file, retrieve or execute a prohibited target, repair a
result, or write this coordinator-owned document.

## Decision Rule

Each experiment receives one determination:

- **pass:** exact decision, replay, mutation and claim boundary reproduce;
- **bounded caveat:** the outcome reproduces, but a material frozen limitation prevents
  clearance;
- **discrepancy:** retained evidence contradicts the recorded decision or boundary; or
- **cannot-reproduce:** the exact replay cannot be completed at the frozen revision.

Only `pass` permits BC-121 to change that experiment’s `needs_review` value from `true`
to `false`. The decision, reason, hypothesis state and frontier remain unchanged.
The coordinator records every reviewer return as **Artifact, Result, Guard, Next**
before applying this rule.

## Determination Register

| Experiment | Frozen decision | Reviewer determination | Replay and guard | BC-121 permission |
| --- | --- | --- | --- | --- |
| exp-047 / H-053 | `blocked`; review pending | **pass** | Precision boundary and premeasurement guards reproduced | Clear only `needs_review` |
| exp-048 / H-054 | `unresolved`; review pending | **pass** | Typed premeasurement E1 refusal and absent result reproduced | Clear only `needs_review` |
| exp-049 / H-052 | `unresolved`; review pending | **pass** | Frozen no-result process boundary reproduced | Clear only `needs_review` |
| exp-050 / H-054 | `unresolved`; review pending | **bounded caveat** | Reason-3 refusal reproduces, but producer runner is not result-bound | Leave `needs_review: true` |
| exp-051 / H-053 | `blocked`; review pending | **pass** | Literal refusal, self-tests and wall-sign mutation reproduced | Clear only `needs_review` |
| exp-052 / H-052 | `unresolved`; review pending | **pass** | 33-row prefix, chain, mutation and normal/`-O` agreement reproduced | Clear only `needs_review` |

## Packet A Determination: n = 17

**Artifact.** The reviewer confirmed that the packet commit is directly based on the
scientific evidence revision, the packet hash matches, all seven listed evidence paths
are unchanged and every Packet A artifact hash matches.

**Result.** Both experiments pass independently.
For exp-049, the retained record correctly limits its claim to the executed 3,920-second
process boundary: exit 130, no canonical output and no checkpoint or result.
For exp-052, the frozen loader returned 33 contiguous, agreeing rows with ordinals
0--32, last-row hash `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`,
and progress at ordinal 33 in `independent_started` chained to that row.
The recomputed fixture binding matched, and the result remains absent.

**Guard.** The six-test focused suite and named changed-row mutation passed.
A second mutation of retained row 0 was rejected as `checkpoint row hash changed`.
Normal and optimized self-tests each ran 27 guards with no skips and produced the same
receipt SHA-256, `beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60`. All
executable replay and mutation data stayed outside the repository; the frozen checkpoint
and progress hashes were unchanged.

**Next.** BC-121 may clear only exp-049 and exp-052 `needs_review` flags.
The 33 rows establish resumability and process integrity, not the remaining 148
directions, the target precondition or either mutation decision.
H-052 remains unresolved with no frontier transition.

## Packet B Determination: n = 68

**Artifact.** The reviewer matched the packet commit and packet hash, all six Packet B
artifact hashes and the frozen bytes of every named evidence path.

**Result.** Both experiments pass independently.
For exp-047, the precision block correctly characterizes the source as binary64
midpoints with fixed tolerances and a `2e-15` padding term; the radii are heuristic and
the cells are not outward-rounded enclosures.
The premeasurement guards reproduce, and the experiment makes no H-053 geometry claim.
For exp-051, the literal registered `--record` command exits 2 at argument parsing,
because the CLI exposes self-test modes but no production adapter; the result remains
absent.

**Guard.** Both self-test modes exited 0, with proof receipt SHA-256
`ca1d0aa015a6e88caf132776597e0811251facb740efd59527035b3ada89a8b4` and runner receipt
SHA-256 `2530667ed7b2a55d4ae926eec9492fea40ff910991b005686208dfe924d8e6a0`. The focused
suite passed 38 tests, and the named wall-sign mutation was rejected with the expected
error. No target, network operation or production accumulation was used.

**Next.** BC-121 may clear only exp-047 and exp-051 `needs_review` flags.
Synthetic residue testing does not compensate for the missing production adapter.
Both experiment decisions remain `blocked`; H-053 remains scientifically unresolved and
`instrument_ready: false`, with no frontier transition.

## Packet C Determination: n = 50

**Artifact.** The reviewer matched the packet and all Packet C artifact hashes and
confirmed that the relevant paths are byte-identical to the scientific evidence
revision. The exp-048 result path remains absent; exp-050’s immutable result SHA-256
remains `ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02`.

**Result.** Exp-048 passes.
Its typed premeasurement E1 refusal stops at the first source-cell admission gate,
before instrument construction, controls, reconstruction, geometry or target execution.
The preregistered verifier does not exist at the frozen revision, and the result is
absent. Exp-050 receives a **bounded caveat**: its immutable reason-3
`attribution-unbound` refusal with zero cells reproduces, but neither the four result
bindings nor the independent verifier binds `source_semantics_runner.py`. The packet
identifies a contemporaneous runner, but the result cannot prove that those bytes
produced it or durably establish the producer’s runtime ordering.

**Guard.** The immutable verifier exited 0 with reason 3, four bindings, 171 retained n
= 19 pair facts, zero skips and `needs_review: true`. The six-test independent suite,
missing-semantics mutation and changed-result and duplicate-key controls all passed.
The literal command against the existing result refused with `result already exists`,
and its SHA-256 was unchanged.
The retained n = 19 receipt supports exact-side serialization, 171 pair checks and the
190-pair duplicate mutation; the independent verifier does not rerun `build(19)` or its
geometry.

**Next.** BC-121 may clear only exp-048’s `needs_review` flag.
Exp-050 must remain under review with its frozen unresolved decision.
H-054 remains unresolved and the instrument remains unready, with no pose, `53/7`
validation or frontier transition.
A future preregistered round must bind the producer-runner hash and inject a
pre-evaluation stage sentinel.

## Coordinator Reconciliation Guard

The coordinator checks each return against the packet and reruns only a reviewer-named
read-only command when needed to resolve a clerical ambiguity.
No source or result is changed to obtain a pass.
A lane-level summary cannot hide a different determination for one of its two
experiments. Any repair becomes future registered work.

The coordinator independently matched all 21 packet-listed artifact hashes at evidence
revision `529b6729` and confirmed all five declared result or checkpoint absences both
at that revision and in the working tree.
The combined focused suites passed 50 tests.
The n = 17 normal and optimized self-tests were byte-identical at the registered receipt
SHA-256. The n = 68 literal command again exited 2 with its result absent.
The registered n = 50 literal command exited 1 at `result already exists`, leaving the
result SHA-256 unchanged.

A preliminary coordinator check invoked the non-entry
`cases.n050_exact.source_semantics_runner` module directly; it has no command-line
action and returned 0 without output or a repository change.
It is not counted as the literal-command replay.
Reading the experiment’s exact command before the corrected replay is another concrete
instance of the W5 literal-entry-point guard.

One cross-lane reconciliation audit found and corrected a wording error that had grouped
H-053 with its two `blocked` experiments.
The corrected boundary is that both experiment decisions remain `blocked`, while H-053
remains scientifically unresolved and `instrument_ready: false`.

## Review Conclusion

BC-120 passes exp-047, exp-048, exp-049, exp-051 and exp-052 for the sole purpose of
clearing their `needs_review` fields in BC-121. Exp-050 retains a bounded caveat and
must remain `needs_review: true` because its immutable result does not bind the producer
runner. No experiment decision, hypothesis disposition, instrument-readiness value,
result, checkpoint or frontier field changes at this gate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
