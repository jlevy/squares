# Validation Efficiency Ideas

| Idea | Evidence and next action |
| --- | --- |
| Reuse float midpoint-to-cell lookup | [Experiment VE-001](experiments/VE-001-float-oracle.md); retains independent oracle and every exact cell |
| Reuse the bridge row inventory within an invocation | [Experiment VE-002](experiments/VE-002-bridge.md); retains all scale and owner checks |
| Start exact verification before the checks queue | [VE-003](experiments/VE-003-checks-start-order.md) retained a failed setup check; [VE-004](experiments/VE-004-checks-start-order.md) repairs the common setup and preserves the same 48-check workload and acceptance rule |
| Parse the branch-cost corpus once per invocation | [VE-005](experiments/VE-005-rollup-corpus-snapshot.md) replaces branch-times-corpus reparsing with one invocation-local snapshot while retaining lazy semantic validation |
| Start loadfile units by recorded cost | [VE-006](experiments/VE-006-recorded-cost-first-loadfile.md) preserves native scheduling and freezes current-head coverage, allocation, CALL and shard-wall guards before measurement |
| Admit Gupta facts once per invocation | [VE-007](experiments/VE-007-gupta-invocation-facts.md) retains the rejected complete-roster experiment and its contrary timing evidence |
| Reuse paper navigation for independent read-only probes | [VE-008](experiments/VE-008-paper-layout-probes.md) was rejected on a one-field equality refusal; no timed samples ran |
| Share complete immutable test publications | [VE-009](experiments/VE-009-shared-test-publication.md) was withdrawn on controller critical-path and maintenance cost after both corpus oracles passed |
| Copy guarded receipts through their JSON representation | [VE-011](experiments/VE-011-guarded-receipt-copies.md) preserves exact types/order, fresh nested values and every nine-case custody guard |
| Bound nested pools and schedule exhaustive tests | Instrument and worker-cap regression first; register a measured scheduling experiment after profiling |
| Remove duplicate n=40 replay | Review equality and CLI contracts before proposing a replacement |
| Attribute negative-control time | Add incremental per-control receipts before optimizing repeated checker work |
| Improve guideline ownership and naming | Dedicated upstream performance guide with focused crosslinks; project matrix owns concrete tiers and budgets |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
