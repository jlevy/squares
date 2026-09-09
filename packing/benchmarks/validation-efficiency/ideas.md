# Validation Efficiency Ideas

| Idea | Evidence and next action |
| --- | --- |
| Reuse float midpoint-to-cell lookup | [Experiment VE-001](experiments/VE-001-float-oracle.md); retains independent oracle and every exact cell |
| Reuse the bridge row inventory within an invocation | [Experiment VE-002](experiments/VE-002-bridge.md); retains all scale and owner checks |
| Start exact verification before the checks queue | [VE-003](experiments/VE-003-checks-start-order.md) retained a failed setup check; [VE-004](experiments/VE-004-checks-start-order.md) repairs the common setup and preserves the same 48-check workload and acceptance rule |
| Bound nested pools and schedule exhaustive tests | Instrument and worker-cap regression first; register a measured scheduling experiment after profiling |
| Remove duplicate n=40 replay | Review equality and CLI contracts before proposing a replacement |
| Attribute negative-control time | Add incremental per-control receipts before optimizing repeated checker work |
| Improve guideline ownership and naming | Dedicated upstream performance guide with focused crosslinks; project matrix owns concrete tiers and budgets |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
