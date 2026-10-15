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
| Copy guarded receipts through their JSON representation | [VE-011](experiments/VE-011-guarded-receipt-copies.md) was rejected after six passing native observations missed the frozen inclusive timing screen |
| Read project attribution inputs once per test invocation | [VE-012](experiments/VE-012-tally-attribution-snapshot.md) retains complete-input equivalence and inclusive timing |
| Read each Gupta claim bound once for its two fields | [VE-013](experiments/VE-013-gupta-bound-pair.md) retains complete-input equivalence and inclusive timing |
| Inline identical hot scalar and point witness schema shapes | [VE-014](experiments/VE-014-witness-inline-shapes.md) was withdrawn after a 12.80% reduction missed the frozen 15% screen |
| Repeat Gupta timing with the retained schema | [VE-015](experiments/VE-015-gupta-retained-schema.md) repeats the unchanged criterion after withdrawal of the schema candidate used during VE-013 fixture setup |
| Bound nested pools and schedule exhaustive tests | Instrument and worker-cap regression first; register a measured scheduling experiment after profiling |
| Remove duplicate n=40 replay | Review equality and CLI contracts before proposing a replacement |
| Attribute negative-control time | Add incremental per-control receipts before optimizing repeated checker work |
| Improve guideline ownership and naming | Dedicated upstream performance guide with focused crosslinks; project matrix owns concrete tiers and budgets |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
