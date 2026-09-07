# Research and Upstream Reconciliation, September 7

This review reconciles PR110 at `ecd4a035` with main at `a5e9dbfd`, including PR112 and
PR115. The GitHub survey covers PRs closed since September 6 UTC; the agenda survey
covers Agendas017–028. Live task notes were checked separately because a pushed branch
can lag its owner’s current work.
The integration is tracked by `think-dwq8` under W8/W10.

## What Has Landed

The survey found 25 closed PRs: 23 merged and two closed without merging.
PR108 merged into PR107’s branch, then reached main through PR107. Closing a PR or a
session does not close every commitment in its agenda.

| PR | Disposition and retained contribution |
| --- | --- |
| [87](https://github.com/jlevy/squares/pull/87) | Merged: validation efficiency, behavioral lanes and budgets |
| [89](https://github.com/jlevy/squares/pull/89) | Merged: post-3.81 T+2 research checkpoint |
| [90](https://github.com/jlevy/squares/pull/90) | Merged: print cascade and layout validation |
| [91](https://github.com/jlevy/squares/pull/91) | Merged: exhaustive n20 test follows the promoted certificate |
| [92](https://github.com/jlevy/squares/pull/92) | Merged: paper typesetting and first adversarial corrections |
| [93](https://github.com/jlevy/squares/pull/93) | Merged: four PR jobs, advisory deep gate and CPU diagnostics |
| [94](https://github.com/jlevy/squares/pull/94) | Merged: second adversarial review and verifier agreement |
| [95](https://github.com/jlevy/squares/pull/95) | Merged: optional atlas/census pools and Cargo caching |
| [96](https://github.com/jlevy/squares/pull/96) | Merged: declared-bound audit attribution |
| [97](https://github.com/jlevy/squares/pull/97) | Merged: T-022, post-3.81 results and research priorities |
| [98](https://github.com/jlevy/squares/pull/98) | Merged: measured repeated-work reductions and timing receipts |
| [99](https://github.com/jlevy/squares/pull/99) | Merged: explainer editorial, typography and browser checks |
| [100](https://github.com/jlevy/squares/pull/100) | Merged: fractional-depth repairs and independent geometry oracle |
| [101](https://github.com/jlevy/squares/pull/101) | Merged: integrated research checkpoint and next allocations |
| [102](https://github.com/jlevy/squares/pull/102) | Closed unmerged: operating-rule control repair superseded by PR98 |
| [103](https://github.com/jlevy/squares/pull/103) | Closed unmerged: scan pruning and cost labels consolidated into PR101 |
| [104](https://github.com/jlevy/squares/pull/104) | Merged: displayed bound and footnote stay together |
| [105](https://github.com/jlevy/squares/pull/105) | Merged: scalar, density and restricted-angle block |
| [106](https://github.com/jlevy/squares/pull/106) | Merged: n17 source reconciliation and certificate archives |
| [107](https://github.com/jlevy/squares/pull/107) | Merged: n11 packet and parallel Agendas027–028 |
| [108](https://github.com/jlevy/squares/pull/108) | Merged into PR107 at `8be1f03c`; incorporated into main by `dd36800e` |
| [109](https://github.com/jlevy/squares/pull/109) | Merged: diagonal compatibility and fixed-support ceiling |
| [112](https://github.com/jlevy/squares/pull/112) | Merged: Stromquist memos, helper arguments and paper v0.2.3 |
| [113](https://github.com/jlevy/squares/pull/113) | Merged: bound-direction explanation and paper v0.2.2 |
| [115](https://github.com/jlevy/squares/pull/115) | Merged: attribution, explicit new bound and D-480 layout repair |

The current paper edition is DRAFT v0.2.3-14beee33. PR115 preserves the mathematical
results while distinguishing approximate construction coordinates from formal
upper-bound proofs. Publication versions are independent of the Python package version.

## Mathematical Disposition

**The n11 bracket is unchanged by this integration or by PR110’s local reductions.** The
[frontier record](../../../packing/frontier/n-011.md) owns the current bound and its
evidence. The following distinctions determine what deserves further attention.

| Work | Established result | Consequence for the next allocation |
| --- | --- | --- |
| PR105 and terminal sessions089–090 | Restricted near-axis and near-45 auxiliaries; scalar exp116 remained unconverged | Retain the lemmas. No unchanged scalar retry or global-bound claim |
| PR109 and sessions091/093–095 | Counterexamples to unchanged P12 and small-diamond shortcuts; complete localization and diagonal compatibility; exp128 independently establishes optimum eleven on the fixed support | H099 is refuted only on that support. H124/H036 remain unresolved. The fixed collision-cover representation gets no automatic retry |
| PR110, BC273/276/278–282 | Exact signed-release exclusions, scoped wall/boundary obstructions and an independently admitted seven-parameter residual skeleton | Preserve the closed remainder and exact fiber equivalence. No covered target fiber, feasible skeleton or eleven-square packing was established |
| PR112, Stromquist session096 | Corrected 1984 chronology, finite Memo I incidence control, independent local segment-helper proof and quantitative five-point piercing obstruction | Geometric replay and the remaining lemmas are a separate helper-tool lane; finite incidence does not establish missing geometric premises |
| PR106 | Corrected n17 prior-value/source attribution and preserved certificates | Retain the current n17 lower bound 4.59; the reconciliation itself is not a new bound |

The source detail is in the
[Stromquist brief](../research/research-2026-09-07-stromquist-memos-and-helper-arguments.md),
[segment-helper review](review-2026-09-07-stromquist-segment-helper.md),
[quantitative piercing review](review-2026-09-07-n6-quantitative-piercing-bound.md),
[Session095](../../../packing/campaign/agent-sessions/session-095-collision-cover-and-support-ceiling.md)
and
[BC282 admission](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-admission.md).

## Agenda Status and Parallel Work

These are recorded agenda statuses, not inferred completion from PR titles.
The [agenda map](../../../SYNOPSIS.md) is the generated inventory.

| Agendas | Recorded status | Retained result or remaining commitment |
| --- | --- | --- |
| 017 | Completed | T017–020 bounds and generator/verifier infrastructure |
| 018–019 | Paused | Preserve their conditional entries; historical BC191 selection is superseded as the portfolio’s next entry |
| 020 | Completed | Exact integer sweep replacement and independent verification; timings remain host-specific evidence |
| 021 | Completed | T021 at n20/n21 and fractional/isolation quantities; later BC213 improves the restricted wall bracket from 0.025 to 0.015 |
| 022 | Active | Session087 is terminal; other commitments remain conditional |
| 023 | Active | Several efficiency checkpoints landed; proposed caching/reuse work is not all complete |
| 024–026 | Active | Sessions089–095 have terminal dispositions; their selected continuation supersedes the original launch instructions |
| 027 | Active | X017’s broad cover/family pilots remain unlaunched; BC264 kernel work has its own live owner |
| 028 | Active | The eight-hour block and residual-design continuation are terminal; H118/H120 target work is parked behind explicit re-entry conditions |

The next decisions are separated by what they can establish:

1. **BC264/H114 remains with its existing owner, `think-mq0d`.** Live notes on September
   7 at 21:47 UTC report session097’s independently admitted kernel implication and
   cubic center-feature obstruction, followed by a fixed eleven-feature,
   sixteen-parameter family.
   The producer (`think-s8cj`) and independent reader (`think-rbmm`) completed
   source-free builds. Separate code/protocol admission and whole-child supervision
   remain prerequisites.
   No scientific source run or continuum certificate was claimed in those notes.
   These working-tree results are not part of main or this merge; the owner’s current
   record governs dispatch.
2. **Stromquist helper replay, `think-0krc`, is an independent tool/proof lane.** Encode
   exact segment clipping, component ownership and universal inequalities, then replay
   the remaining Memo I implications.
   This can make a geometric proof method reusable; it does not inherit permission to
   change a packing bound or launch a target.
3. **Local H118/H120 target work stays parked.** BC282’s six-source covering chain is
   unproved. H120 needs a justified parameter selection, independent skeleton binding and
   a complete price (`think-k54y`). H118 needs a finite joint-angle-preserving rule, its
   control and the full verification price.
   Neither is ready for another overnight target merely because a previous block ended.

The integration itself starts no new H, BC or scientific experiment and transfers no
other agent’s ownership.

## Open PRs and Integration Boundaries

At the survey snapshot, PR110, PR111 and PR114 were open and conflicted with main.
This work resolves PR110’s integration only.

| Open work | Relation to this branch | Integration requirement |
| --- | --- | --- |
| [110](https://github.com/jlevy/squares/pull/110), `codex/n11-hybrid-overnight` | Our mathematical checkpoints and measured scheduler repair | Retain both main’s new source work and our scoped results; validate the combined tree |
| [111](https://github.com/jlevy/squares/pull/111), atlas expansion to 324 | Changes corpus size, validator selection, budgets and PR/deep workflows | Review complete-versus-sampled coverage separately; do not transfer the frozen 100-case timing claim to this workload |
| [114](https://github.com/jlevy/squares/pull/114), math text face | Changes vendored kpress, fontTools/development lock and rendering tests | Resolve its kpress PR53 dependency and retain its separate browser/print obligations |

Green checks attached to an older PR head do not establish present mergeability.
Open PR status also does not establish whether an agent is currently running.

## Record Identity and Validation

Main’s Stromquist session096 and PR110’s former residual session096 used the same
receipt filename for different task roots and intervals.
Preserve the landed record and rekey only the unmerged residual record to session098
after checking remote refs **and live worktrees**. The 47 present registered worktrees
contained no 098+ allocation; `think-dwq8` reserves 098. BC264’s live session097 is
reserved even though it was absent from the remote inventory.
The atlas PR’s remote session093 and local proposed 097 both collide with source
ownership; `think-rzek` retains that separate repair and the need for a fresh
reservation. Neither collision justifies renumbering landed scientific records.

A concurrent upstream merge reached the same PR110 branch as `7a2145f4` during
validation. It independently preserved both receipts but selected097 from the remote
inventory. This integration retains that commit in history and resolves the competing
rename to098, preserving the earlier live kernel allocation.
Its additional plan reference is carried forward with098. No code or scientific result
differs between these two merge resolutions.

Preserve each cost payload byte-for-byte during rekeying, including its original before
baseline. Historical runtime archives keep their original filenames and source IDs.
Update current links and regenerate the ledger and cost views from the resolved records.
The integration/survey has its own bead and does not extend the original mathematical
clocks or relabel a prior failed check.

The incoming main code adds Stromquist finite controls and tests, rendering/print checks
and release metadata.
It does not change the validator scheduler, workflows, budgets or dependency lock.
VE004’s 22.9% local median improvement remains evidence about its frozen 48-check
workload, not a new measurement of the merged tree.
Run the records and affected pre-push floor, then a full frozen combined-tree checkpoint
concurrently with hosted CI. PR110 retains the actual source-bound outcomes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
