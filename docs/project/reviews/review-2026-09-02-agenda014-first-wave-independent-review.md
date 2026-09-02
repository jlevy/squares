# Independent Review: Agenda 014 First Wave

**Date:** 2026-09-02

**Author:** Claude, for the project maintainers

**Status:** Complete — three passes, no caveat

This review applies agenda-014’s BC-135 independent replay gate to the three first-wave
experiment decisions in the n = 17, n = 68 and n = 50 lanes.
It records what each reviewer reproduced, which mutation fired, the accepted claim
boundary and whether BC-136 may clear an experiment’s `needs_review` flag without
changing its frozen decision.

## Frozen Review Surface

| Item | Frozen value |
| --- | --- |
| Scientific evidence revision | `1e1751085fcdf0e71f563ed6b0f282feee54d07e` |
| Packet commit | `e9c9209185ac9c073b2118d29744710f632cb862` |
| Packet SHA-256 | `c163452ac449ec61f18575e7b5236216fbc81404b7addf04de4c97caa2c87f49` |
| Review window | `2026-09-02T04:22:00Z--04:30:00Z` |

The packet set is
[review-2026-09-02-agenda014-first-wave-packets.md](review-2026-09-02-agenda014-first-wave-packets.md).
Its artifact hashes, exact commands, mutations and claim boundaries are part of this
review contract. One commit landed on the branch during the window, `377a155c`, which
changed only session-076’s record; every reviewer re-ran the evidence-path diff at the
new head and found the packet document and all evidence bytes unchanged.

## Independent Assignments

| Packet | Reviewer | Separation from the source under review | Return |
| --- | --- | --- | --- |
| n = 17 / H-057 | reviewer-a, a fresh Claude sub-agent | Authored no first-wave lane; the lanes were written by three Codex agents and the coordinator | 338 s |
| n = 68 / H-058 | reviewer-b, a fresh Claude sub-agent | Same separation | 423 s |
| n = 50 / H-059 | reviewer-c, a fresh Claude sub-agent | Same separation | 319 s |

Reviewers read frozen repository bytes, ran only the packet-named checkers, suites and
self-tests, and wrote only under pytest or operating-system temporary paths.
None edited a repository file, made a network request, ran a pair, assemble, production
or producer command, or wrote this coordinator-owned document.
The replay host was Linux under Python 3.14.7; the frozen runs were recorded on macOS
arm64, so a matching receipt is cross-platform evidence rather than a same-host repeat.

## Decision Rule

Each experiment receives one determination:

- **pass:** exact decision, replay, mutation and claim boundary reproduce;
- **bounded caveat:** the outcome reproduces, but a material frozen limitation prevents
  clearance;
- **discrepancy:** retained evidence contradicts the recorded decision or boundary; or
- **cannot-reproduce:** the exact replay cannot be completed at the frozen revision.

Only `pass` permits BC-136 to change that experiment’s `needs_review` value from `true`
to `false`, in the experiment record only.
The decision, reason, hypothesis state and frontier remain unchanged.
The coordinator recorded every reviewer return as **Artifact, Result, Guard, Next** in
session-076 before applying this rule.

## Determination Register

| Experiment | Frozen decision | Reviewer determination | Replay and guard | BC-136 permission |
| --- | --- | --- | --- | --- |
| exp-053 / H-057 | `unresolved`; review pending | **pass** | Retained serial arm, absences, 30-guard receipt and both mutations reproduced | Clear only `needs_review` |
| exp-054 / H-058 | `unresolved`; review pending | **pass** | Target-blind admission, corrected depth guard, 35 tests, twenty mutations and the byte-identical receipt reproduced | Clear only `needs_review` |
| exp-055 / H-059 | `accepted`; review pending | **pass** | Immutable result verified under both interpreters, bindings, sentinels and all mutations reproduced | Clear only `needs_review` |

## Packet A Determination: n = 17

**Artifact.** The reviewer matched the packet hash and all twelve Packet A artifact
hashes at the frozen revision and in the working tree, and confirmed that `merged.json`
binds the frozen package manifest `309ec241…d54` and the parent row hash
`9badcc57…ade6`, both unchanged from exp-052.

**Result.** Exp-053 passes.
`receipt.json` reads mode `serial`, `elapsed_ns` `524743164166`, one inline worker, and
its three fragment hashes equal the three fragment files in packet order; its merged
hash equals the computed `bd383747…33ba`. Seven focused tests passed in 1.75 s. Both
self-tests emitted 30 guards with byte-identical output whose SHA-256 is
`0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958`. No paired sample
exists: the pair receipt, arm B, pair 2 and pair 3 are absent on disk and in the index,
and exp-053 records the three-pair question as `invalid`. Every occurrence of 2.8x in
the records is the preregistered criterion, a synthetic self-test control or a
scheduling diagnostic that session-073 labels as not a paired measurement.
Arm A is described only as process cost and historical evidence.

**Guard.** `git diff --exit-code 1e175108` over the evidence paths and the two read-only
exp-052 inputs was empty before and after replay; `git status --porcelain` was empty at
the end. The two named mutation tests passed in 0.23 s: the pair contract rejected a
changed ordinal and a wrong output root, and the induced parallel failure removed the
partial candidate arm while the complete arm’s receipt bytes were unchanged.
No `pair` or `assemble` subcommand ran.

**Next.** BC-136 may clear only exp-053’s `needs_review` flag.
The decision stays `unresolved`, H-057 stays instrument-ready and undecided, BC-129
stays stopped, and a future profile still needs fresh pair roots and a host-wide quiet
lease. Packet facts the reviewer recorded: the receipt hash is the SHA-256 of the
self-test’s stdout including its trailing newline, which the packet did not state; the
canonical result path is also named as a placeholder in exp-053’s `method.record`; the
self-test’s `skips` field is a literal zero rather than a measurement; and the routing
table’s 0.444 rows per minute is an exp-052 figure, since the profiler’s own arm implies
about 0.343 rows per minute for a different per-row workload.

## Packet B Determination: n = 68

**Artifact.** The reviewer matched the packet hash and all nine Packet B artifact hashes
at the frozen revision and in the working tree.
Reading `run.py`, the entry point calls only the literal self-test, which refuses any
record path other than the registered one, runs inside a temporary output root and
injects an in-memory synthetic SVG as its opener; the network-capable opener is never
reached from the entry point and performs no I/O at construction.
In `adapter.py`, `mark_selected_path` counts the element and raises the bounded-parser
refusal on the element or depth bound before it iterates children.

**Result.** Exp-054 passes.
The focused suite reported 35 passed in 0.90 s, Ruff and BasedPyright were clean, and
the two named tests passed: the depth regression nests one level past Python’s recursion
limit and receives the bounded-parser refusal, and the whole-result verifier rejects
model-binding and proof mutations.
The literal self-test’s receipt, observed inside the suite’s own subprocess under normal
and optimized Python, is 1,112 bytes with SHA-256
`becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906` in both runs and
carries exactly twenty mutation names, from `wrong-result-path-before-open` through
`whole-verifier-before-publisher`. The record’s reason states the round opened no
network or target source and created no result, so it supplies no H-058 sample; the
three typed `serialization-refusal` outcomes are exhibited directly by the two tests
that drive the model factory with an unbound side, and both documents describe them as
premeasurement behavior.

**Guard.** The evidence-path diff was empty before and after replay, the working tree
was clean at the end, and the four instrument files rehash to their frozen values after
every run. No network request was made.
The registered command was not run by hand: the reviewer’s one attempt to do so was
refused by the session’s permission classifier before it executed, so the command ran
only inside the suite’s subprocess.
The receipt hash was obtained through a read-only pytest plugin kept outside the
repository that hashes the stdout the test already captures, since the test neither
prints nor asserts it.
The exp-054 and exp-051 result paths were absent before, between and after every run; no
tracked file is named `square-68.svg` or hashes to the declared parent digest.

**Next.** BC-136 may clear only exp-054’s `needs_review` flag.
The decision stays `unresolved`, H-058 stays instrument-ready and unmeasured, and BC-130
stays a conditional candidate until a separate preregistration binds the reported side
token’s semantics. Packet facts the reviewer recorded: the receipt hash is invariant
across the depth-guard correction, since session-074’s pre-correction phases record the
same value, so a receipt match attests the correction only together with the four
current file hashes and the 34-to-35 test count; three n = 68 SVGs are tracked under the
atlas and the web-resources archive, none of which the production package or its test
opens, so the packet’s “no n = 68 source byte” holds for the parent source only; and the
packet’s instruction to report the receipt hash is not satisfiable from the test’s own
output.

## Packet C Determination: n = 50

**Artifact.** The reviewer matched the packet hash and all thirteen Packet C artifact
hashes at the frozen revision and in the working tree, including the 5,211-byte result
`9c90a04e…654c` and the 1,574-byte exp-050 result `ab00e50d…4a02`. The result’s six
instrument bindings, its producer binding `52baeb1b…f29d` and both exp-050 bindings
equal the computed values.
The case directory holds exactly four tracked files and no fixture, source or geometry
data.

**Result.** Exp-055 passes.
The independent verifier exited 0 under normal and optimized Python with identical
390-byte stdout whose SHA-256 is
`64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc`, matching the session
record. The two focused suites reported 21 passed in 8.14 s. The four stage sentinels
each calibrate exactly once, the retained observation’s stage trace is empty, and all
twelve producer-side mutation leaves are `rejected: true`. The verifier imports only the
standard library, re-hashes every bound file on disk, enforces canonical JSON with a
duplicate-key guard, pins the claim boundary verbatim and contains no bare `assert`, so
the two-interpreter agreement is substantive.

**Guard.** The evidence-path diff was empty before and after replay and the working tree
was clean at the end.
All five named verifier mutations rejected, including `review-cleared`, in 3.76 s. The
producer `--record` command and `--selftest` were not run; no network or geometry access
occurred. The exp-050 hash was recomputed last and was unchanged.

**Next.** BC-136 may clear only exp-055’s `needs_review` flag, and only in the
experiment record: the immutable result also carries `needs_review: true`, the verifier
requires it, and the `review-cleared` mutation exists to reject its removal.
The decision stays `accepted` for the prospective protocol claim only; H-054, exp-050, n
= 50 feasibility and the frontier are untouched.
Packet facts the reviewer recorded: the packet gave no paths for the exp-055 record,
session-075 and H-059; the 0.72-second publication figure is a session attestation the
packet cannot replay; H-059’s prerequisites pre-name a “bounded caveat” for this packet,
which is stale and not the determination; and exp-055’s `dirty: true` provenance with
distinct launch and scientific revisions is reconciled by the hash bindings rather than
by a commit id.

## Coordinator Reconciliation

All three determinations are `pass`, recorded separately and reconciled against the same
packet commit. BC-136 therefore holds permission to change `needs_review` from `true` to
`false` in the exp-053, exp-054 and exp-055 experiment records, and nothing else.
This review does not apply those transitions: BC-136 is a later block that the owner’s
resume instruction left paused, and the flags stay `true` until it opens.

No frozen decision, hypothesis field, frontier entry or result changed during review.
Every packet fact the reviewers recorded is retained above for the next packet author;
none is a lane defect and none alters a determination.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
