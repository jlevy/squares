# Intake Continuation, 19 October 2026: n183 (#680)

This directory holds the intake evidence for Evan Daniel’s
[issue #680](https://github.com/jlevy/squares/issues/680), the first reported packing of
183 unit squares below side 14. The 19 October continuation (W1 bead **think-kwol**)
read the issue and the source head `3a9948c` and opened the import bead **think-xp0o**.
The continuation’s other items, its replies to other issues, the manual-source reads and
the #446 and #678 work, are carried by their own owners and are not recorded here.

| File | What it holds |
| --- | --- |
| [issue-680.json](issue-680.json) | The issue as read, body and metadata |
| [issue-680-replies.json](issue-680-replies.json) | The body of the interim reply posted on #680 on 19 October |
| [evand-source-inventory.json](evand-source-inventory.json) | The six source commits past `ddf09e3` and what each changes |
| [n183-ledger/](n183-ledger/README.md) | The report-order ledger at 183: one claim, recorded |
| [monotone-case-lanes.txt](monotone-case-lanes.txt) | Both upper lanes at each count 184–195, all exactly 14 |
| [monotone-registered-claims.txt](monotone-registered-claims.txt) | The registered upper claims in that range, from `check_standing --cases` |
| [n183-primary-replay.json](n183-primary-replay.json) | The primary-certificate replay batch: declaration, commands, timings and outcomes |
| [n183-evidence-integration.yaml](n183-evidence-integration.yaml) | The review’s and replay’s identities, source versions and M1–M4 dispositions, as handed to registration |

## The Claim and Its Comparison

The [source packet](../../../resources/web/evand-n183-subgrid-2026-10-19/README.md)
retains 17 files, 326,398 logical bytes, from
`3a9948c781be668b1547cc2bf64a0d1e614f9bca`, committed 2026-10-19T05:20:24Z. Both
certificates declare 183 squares and the exact side
`13999580178736252502081470897571/1000000000000000000000000000000`, printed upward as
`13.999580178737`. The original and the same-side display certificate are one bound.

The [report-order ledger](n183-ledger/README.md) compares this exact side with the
record frozen at `d167d4b86` and records the source publication before the issue, four
minutes later; one result is registered for both.
The ledger compares sides; it verifies no geometry and audits no public priority.
The recorded monotone upper envelope at 183 was also 14:
[both upper lanes at each count 184–195](monotone-case-lanes.txt) are exactly 14, and
the [registered upper claims in that range](monotone-registered-claims.txt) are 14 too.
For 196 or more squares, area alone requires side at least 14, so no packing of more
squares gives a sub-14 bound at 183 by deleting squares.

The source’s KKT and local-minimum diagnostics concern its separate numerical point
`S* = 13.999580178736252501941…`, not the slack rational certificate side `S'`. Its 27
candidate flat modes concern the force-bearing subsystem of 182 squares; the free
rattler’s coordinates are excluded from that calculation.
Neither is a local-optimality theorem for all 183 squares.
Francisco Couzo’s n182 donor credit and the unlogged crossover mates stay explicit
source claims.

## Validation and Registration

| Step | Bead | Outcome |
| --- | --- | --- |
| Primary certificate replay, both maintained exact routes, duplicate-square and outside-container controls | **think-1hmn** | Complete: 34.87 s process wall, 30.55 route CPU-s, 99,918 pair decisions; [batch record](n183-primary-replay.json) and the packet’s native receipt |
| Independent mathematical review, with a replay addendum | **think-glg8** | Accepted: [mapped review](../../../../docs/project/reviews/review-2026-10-19-evand-n183-subgrid.md); M1 and M2 dispositioned, M3 and M4 kept as limits |
| Registration at stage 3 and stage 4 | **think-xp0o** | T-220, `V3`/`C3`/`S3`, citing the report and the confirming replay |
| House adoption and both strong generators | **think-jh4w** | Adopted at 183 on 19 October 2026 in the same pull request; both strong generators decided the new witness |

The replay ran the maintained `devtools.upper_bound_reports` route on the original
certificate only, with expected n = 183, the exact side and every row bound before any
geometry was decided.
No upstream checker ran, and the regularized display certificate was not executed; it
proves no further bound, and neither its identity with the original packing nor a path
between them is measured.
The review accepted the finite upper bound on the retained receipt and reran no
geometry. The two maintained routes share parsing, half-angle conversion, `Fraction`,
runtime and the separating-axis theorem: two implementations, not two methods, and no
clean room.

The adoption moved both upper lanes of [n-183.md](../../../frontier/n-183.md) from the
trivial 14 × 14 grid, which stays retained as history, to the original certificate.
Its regularization runs are retained in
[`think-jh4w-2026-10-19`](../../../cases/regularized_drawings/think-jh4w-2026-10-19/selection-n183.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
