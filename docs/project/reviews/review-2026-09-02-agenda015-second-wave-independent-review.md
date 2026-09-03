# Independent Review: Agenda 015 Second Wave

**Date:** 2026-09-02

**Author:** Codex, for the project maintainers

**Status:** Reconciled BC-145 review; three passes, no caveat or discrepancy

Three fresh Max reviewers independently replayed the three immutable BC-144 packets
against evidence revision `313624cc08650bb9054e969da9cfd91ad83e2125`. Each reviewer used
only the packet’s read-only hashes, absences, safe loaders, self-tests and
temporary-data mutations.
None authored a wave lane or its BC-144 packet audit.

All three determinations are `pass`. The passes authorize two narrow review-flag
transitions in BC-146; they do not perform those transitions here and do not change a
hypothesis, instrument state, experiment decision, scientific route, lower bound or
frontier fact.

## Reconciliation

| Packet | Independent determination | Reproduced evidence | BC-146 authority |
| --- | --- | --- | --- |
| A: exp-056, n = 17 / H-052 | **pass** | 12 frozen hashes; canonical-result absence; 170-row verified agreeing chain through ordinal 169; ordinal-170 `independent_started` marker; byte-identical normal/optimized 36-guard receipt; 17 tests; four chain/interruption controls | Change only exp-056 `needs_review: true` to `false` |
| B: exp-057, n = 68 / H-058 | **pass** | 12 frozen hashes; result and `square-68.svg` absences; byte-identical normal/optimized 13-guard receipt; 62 tests; `wrong-direction`; independent source-provenance refusal | Change only exp-057 `needs_review: true` to `false` |
| C: BC-141, n = 54 / H-055 | **pass** | 14 frozen hashes; byte-identical author output; 79 tests; both exact exit mutations; canonical JSON rules; standard-library-only independent import closure; no retained result | Record the pass only; H-055 has no review-flag transition and remains `instrument_ready: false` |

No reviewer reported a mismatch, bounded caveat or cannot-reproduce condition.
The existing instrument states remain unchanged: H-052 and H-058 are
`instrument_ready: true`, while H-055 is `instrument_ready: false`. The packet file
remained byte-identical at SHA-256
`67206898214e49250f559be57694633b920eb927ebf09650e76b79eb7727f0de`; the packet commit is
`9d3ea64d6131439993d26dabea63bdbf209044ce`, and the raw reviewer receipts are retained
in session-078 at commit `c0433f3807c16f30d14147691b53a6c73b42064e`.

## Packet A: exp-056

The reviewer reproduced all twelve packet hashes and an empty executable/checkpoint/
progress/test diff from the frozen revision.
The canonical exp-056 result was absent from both the frozen tree and the worktree
before and after replay.

Status reported 170 rows, ordinals 0--169, 33 parent plus 137 child rows,
`all_agree: true`, `chain_verified: true` and `complete: false`. The last-row link was
`8947b38e0351048c3a67d914f2b8449185686d920913f5a2404898bdeca4c0b6`; progress recorded
ordinal 170 at `independent_started`, chained to that link.
Eleven of 181 directions remain uncomputed.

Normal and optimized self-tests were byte-identical at SHA-256
`9d6cbdc83ad83bf5234b872d67931b7003a038fa870ebc426133368e8e43a28e`. Both reported 36
guards, zero skips and receipt/inventory hash
`612349379b70ccddfa5bd4f5265a747caca768c5b9a9627b4057e69a5791f894`; 17 focused tests
passed. `tampered-child-chain-link`, `between-accumulator-interruption`,
`no-partial-row-promotion` and `interrupted-resume-equivalence` all fired.

This passes the retained process evidence only.
Exp-056 remains `unresolved`, stopped by the fixed 21,360-second elapsed lease, with
cost-role outcome `criterion_missed`. Clearing its review flag does not decide H-052,
move a lower bound or frontier, or authorize resuming ordinal 170 inside exp-056. Any
continuation needs a newly preregistered round.

## Packet B: exp-057

The reviewer reproduced all twelve packet hashes, an empty executable/test diff and the
declared absences of the canonical exp-057 result and `square-68.svg` before and after
replay.

Normal and optimized receipts were byte-identical at SHA-256
`790a973ee5e11e079a3c41dab578311d491eabe5dee76a120ee3a12f5702d76b`; all 13 guards fired
and 62 focused tests passed.
The `wrong-direction` control refused both a downward positive truncate-six interval and
a one-sided nearest-six interval.

The reviewer independently confirmed the recorded provenance refusal.
Frozen `_source_interval` applies an exactly-six-fractional-digit rule to SVG coordinate
tokens. The token `8.80345993651653` has fourteen fractional digits, is release text
rather than an SVG coordinate, and has no cited source rule projecting the coordinate
semantics onto it. Its literal exact-rational point interpretation survives, but it
cannot satisfy the unchanged conjunctive three-model criterion alone.

Clearing exp-057’s review flag leaves the decision `unresolved`, its guard-role outcome
`invalid`, H-058 unmeasured and BC-139 stopped.
The pass verifies the recorded refusal; it does not turn that refusal into an accepted
scientific result. It authorizes no source or network access and changes no frontier
fact. A future literal-only route still needs a new prospectively frozen hypothesis and
experiment.

## Packet C: BC-141

The reviewer reproduced all fourteen packet hashes and empty pre/post diffs for the
executable, fixture, tests, formula-audit dependency and Python environment files.
Normal and optimized author streams were byte-identical at SHA-256
`79008d0738f17102e77b4c45c54af01f0b0faf8666ab650289dbdef4f89aa3d9`; 79 tests passed in
53.17 seconds.

Both exit mutations reproduced exactly:

- `missing_structural_inventory` refused with
  `missing or unexpected synthetic source endpoint`;
- the bijective `correspondence_swap` refused with `synthetic structural-tag drift`.

The reviewer also reproduced exact-key canonical JSON, sorted compact ASCII encoding,
one terminal newline, and duplicate-key, float, exponent and non-finite refusal.
Static and runtime import-closure checks found only the standard library and the
independent verifier package itself: no author contract or runner, production verifier,
`sqpack`, SymPy, XML or lxml import occurred.
No durable `N54Result/v1` was published.

This is a pass for prospective `synthetic-structure-only` instrumentation.
It establishes no live-source fidelity, actual source-label-to-row correspondence,
source-derived precision cells, witness values, geometry, feasibility, optimality or
packing bound. H-055 has no `needs_review` transition and remains
`instrument_ready: false`.

## Access and Mutation Guard

All three reviewers were read-only and changed no repository file.
They opened no network, live source, target, witness value or geometry channel; ran no
scientific producer or record command; and published no result.
Test mutations wrote only to pytest temporary paths with bytecode and repository caches
disabled. The coordinator recorded the raw returns without reconciling them before the
fixed 12:58Z boundary.

## Next

BC-145 retains this reconciliation and runs the records, documentation and formatting
gates through its fixed 13:43Z boundary.
At that boundary, BC-146 may apply only the two explicit review-flag transitions above
and record Packet C’s pass.
Any other change requires separate evidence and authority.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
