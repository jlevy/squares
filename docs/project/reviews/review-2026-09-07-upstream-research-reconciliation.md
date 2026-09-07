# Research Strategy and Upstream Reconciliation, September 7

This review reconciles PR110 at `ecd4a035` with main through `373beb36`, including
PR112, PR115 and PR114. PR114 landed during the final publication checks and was merged
cleanly; the earlier checkpoint used `a5e9dbfd`. The GitHub survey covers PRs closed
since September 6 UTC; the agenda survey covers Agendas017–028. Live task notes were
checked separately because a pushed branch can lag its owner’s current work.
The user-requested strategy/planning block is **BC283 / `think-dwq8`, W10**, with
upstream/documentation reconciliation under W8. It assesses established results and
selects the next coordinating entry; it launches no successor experiment and changes no
other lane’s frozen contract.
The independent mathematical reviews ran 22:20:04–22:21:17 and 22:20:12–22:21:45 UTC.
The planning slice ends at 22:45 UTC, followed by a 15-minute
documentation/validation/publication reserve.
Running validation is asynchronous evidence, not mathematical progress.
Two independent synthesis reviews, 22:30:42–22:31:51 and 22:30:51–22:31:32 UTC, accepted
the mathematical distinctions and planning scope.
Their final accepted wording limits claims to what this work certified, without
asserting that all suitable kernels are impossible.

## The Problem and the Proof Languages

Let $s(11)$ be the smallest container side that permits eleven unit squares, with
arbitrary positions and angles.
A construction gives an **upper bound**: these squares fit, so the optimum is no larger.
An impossibility proof gives a **lower bound**: every arrangement below a specified side
fails, so the optimum is no smaller.
Improving either bound would be progress; proving that one attractive picture is rigid
does not settle the other possible arrangements.

The exact Trump construction gives the upper bound $3.877083590022814\ldots$. T018
established the fractional certificate at 3.81; T022 refined its containment argument to
the weak limiting lower bound $3.810025723614703\ldots$. T022 is not a no-fit
certificate at its limiting endpoint.
Those are the current verified bounds in the
[n11 record](../../../packing/frontier/n-011.md).
The recent structural explorations did not raise that lower bound again.

**The successful fractional proof counts one square at a time.** Place nonnegative
weights inside the container so every permitted witness square captures at least one
unit of weight, while the container’s total is less than eleven.
Eleven disjoint witness squares would require at least eleven units, a contradiction.
The actual certificate uses smaller interior witnesses, exact orientation transfer and
explicit boundary conventions; a finite grid of poses alone would not prove the
continuous statement.
T018’s mass is $434547/40000=10.863675$, with a certified minimum capture of
$4001/4000$. Its
[proof card](../../../packing/cases/n11_fractional_certificate/t-018-proof-card.md)
records how those finite checks imply the packing theorem.

X016 asked whether better weights, less shrinking, or full-size area densities could
improve this counting method.
Better weights address optimization; adaptive witness cores reduce the geometric
information lost to shrinking.
Area densities avoid charging shared boundaries because boundaries have zero area.
All still need a guarantee for every allowed pose.
An unconverged optimization is neither a certificate nor evidence that no certificate
exists.

There is also an opposite calculation: weighted candidate square placements whose
combined overlap depth is at most one force any covering density to have at least their
total weight. This can prove a limitation of the counting method.
It is not itself an ordinary packing of eleven disjoint squares.
PR109’s exact support optimum eleven is a particularly useful result of this kind: the
chosen support cannot establish the desired strict obstruction beyond eleven.
Enlarging or changing that support is a different question.

**The structural approaches ask what can coexist.** Checking each square separately
forgets correlations: two individually legal poses can overlap, and an angle compatible
with one neighbor may be incompatible with another.
X017 organizes conditional geometry, complete case covers and pair interactions around
that missing information.
A proof on one case becomes global only after every possible arrangement is assigned to
a proved case. The intended target 3.84 is an aspiration for that complete argument, not
an established bound.

X018 tested two concrete ways to make this structural approach useful:

- **Residual capacity:** condition on four actual squares and bound how many others can
  coexist with them. The accepted central case leaves only four possible center regions,
  each of diameter below one.
  Every unit square contains a radius-one-half disk, so nonoverlapping squares have
  centers at least one apart.
  Each region therefore holds at most one further square; the required seven cannot fit.
  The outer bands and failed guards remain separate cases.
- **Contact release:** enlarge a family related to Trump’s configuration by dropping
  contacts, then try to exclude the enlarged family at smaller sides.
  This produced continuous exclusions over substantial angle intervals.
  It still retains particular wall assignments, axis squares and common-angle structure;
  no theorem puts every better packing into that family.

The strongest boundary-model counterexample explains why correlations matter.
Seven residual disks fit, defeating the proposed disk-capacity bound of six.
The corresponding squares cannot simply be substituted: walls constrain their
orientations, and those orientations overlap.
A weak outer model admitting seven objects need not imply seven actual squares fit.
Wall-dependent common cores retain more information than disks, but their complete
seven-core question remains unresolved.

BC282 then removed square 10 and reduced the necessary ten-square skeleton exactly.
For fixed structural parameters, all translations lie in a closed rectangle and 24 pairs
forbid explicit open intervals on each horizontal fiber.
Covering every fiber would exclude the skeleton; finding a legal translation would
exhibit a skeleton. Neither was done.
The reduction is useful, but the proposed short covering chain lacked the uniform
templates and endpoint analysis needed to fund the larger attempt.
Even an exact ten-square skeleton would only show that square 10 must enter the proof.

**The current kernel lane encodes pairs directly.** In the accepted normalization, a
kernel $K$ satisfies $K-1\succeq0$, is nonpositive on distinct compatible poses, and has
diagonal at most $B$. An actual $m$-square packing would then satisfy

$$
m^2\le\sum_{i,j}K(x_i,x_j)\le mB.
$$

Thus $B<11$ would exclude eleven squares if the kernel conditions were proved on the
entire domain. A finite set of necessary constraints can instead rule out a chosen
feature family cheaply: if even its relaxed problem requires $B\ge11$, that family
cannot supply the certificate.
A feasible finite relaxation does not prove a valid kernel.
[PR116](https://github.com/jlevy/squares/pull/116) reports an independently reviewed
obstruction to cubic center features and a fixed richer family under H125. This makes
the next question much narrower than constructing an unrestricted hierarchy.

## What Has Landed

The final survey found 26 closed PRs: 24 merged and two closed without merging.
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
| [114](https://github.com/jlevy/squares/pull/114) | Merged at 22:50 UTC: explainer math text face, rendering controls and pinned font tooling |
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

1. **BC264/H114 remains with its existing owner, `think-mq0d`.** The September 7, 22:46
   UTC check of [PR116](https://github.com/jlevy/squares/pull/116) and its live owner
   records retains session097’s independently admitted kernel implication, cubic
   center-feature obstruction and reviewed implementation of the fixed eleven-feature,
   sixteen-parameter family.
   Session097 has stopped.
   Exp129 missed its fixed 22:20 launch cutoff because its protocol guards had not
   passed; no scientific source, target, packet or reader ran.
   H125 therefore remains untested, with its scientific allowances unspent.
   Finish checkpoint validation/publication under `think-m2lx`, then let `think-mq0d`
   assess a fresh bounded first-invocation allocation for the unchanged instrument.
   Passing record checks, a renewed operational lease and publication of the new
   admission must precede launch.
   This planning block renews no allocation.
   These separate branch results are not part of main or this merge.
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

The upstream merge transfers no other agent’s ownership.
The later planning block below adds only BC283; no scientific hypothesis or experiment
is launched.

## Planning Decision: Spend on Missing Information

BC283 makes the following portfolio decision from these results.
Its planning identity was checked against 80 remote refs, 48 present worktrees and
shared tbd state before reservation at 22:25 UTC. The earlier no-BC283 statements belong
to the completed overnight and residual-design allocations; this later user-requested
planning block is distinct.
No mathematical H-item, experiment or scientific session is created to count this review
as a result.

| Avenue | What panned out; what did not | Next decision and reconsideration condition |
| --- | --- | --- |
| Scalar/fractional optimization | T018/T022 improved the bound. Later scalar exp116 remained unconverged | Keep H107/its reviewed adapter deferred. Reconsider for a named downstream use, a changed mechanism and a newly priced complete invocation; no unchanged retry |
| Fixed-support density obstruction | Exp128 exactly settled the chosen support at eleven; earlier graph/depth work did not establish the broader obstruction | Retire that support attempt. Any expansion must name the new geometric information and a cheap necessary-row screen before full continuum verification |
| Conditional compatibility | Near-axis/near45 auxiliaries and the full diagonal band survived independent review; P12 and the weakened diamond cover were refuted; axis `no_chain` remains inconclusive | Retain the lemmas. Re-enter only with a changed representation preserving the actual distinguished square, and a complete independently checked axis discriminator |
| X018 capacity and release | Guarded 4+7 exclusion, signed-angle exclusions and exact residual-fiber reduction are accepted; resource superiority, whole seven-core capacity and complete fiber coverage are not | Keep H118/H120 targets parked. Require the matched LP survival witness or finite joint-angle rule for H118; justified parameter selection or bounded complete templates and an independent open-fiber reader for H120 |
| BC264/H114/H125 kernel work | Cubic-family obstruction and reviewed source-free builds provide a concrete next test. Exp129 never ran before its cutoff, so H125 remains untested | **Selected coordinating entry remains `think-mq0d` under its existing owner.** Finish checkpoint publication under `think-m2lx`, then assess a fresh bounded first invocation after its admission requirements pass. Preserve the expired protocol; no automatic feature increase or ownership transfer |
| Stromquist helper replay | Source chronology and independently reviewed local helper arguments are retained; the finite incidence table alone does not supply the geometry | Parallel enabling lane under `think-0krc`: make exact clipping/component ownership reusable and independently discharge remaining lemmas. Transfer to n11 only through an explicit reviewed consumer contract |

The priority judgment is that a cheap exact rejection of a defined representation is
more useful now than a larger search whose failure would be ambiguous.
Kernel work has a named family and a potentially decisive finite obstruction.
The helper lane has reusable geometric obligations.
H118/H120 retain promising mathematics, but currently lack the complete discriminator
that would make another target run informative.

This ranking does not assert that one-body methods are universally exhausted, that all
kernels will work, or that local contact families capture a global minimizer.
Those are precisely the unsupported steps the recent negative results teach us to avoid.
Preserve three different outcomes: a false auxiliary claim, a representation ruled out
on its declared domain, and an unfinished or inconclusive solver attempt.

PR116 retains H125, exp129 and session097 under existing BC264. The 22:46 UTC terminal
handoff supersedes the earlier live-run expectation: exp129 supplied no mathematical
test, and its original launch cutoff stays expired.
A newly admitted first invocation could produce an exact obstruction or an inconclusive
outcome; neither is available now.
Compare the actual result with alternatives only after it exists.
Our local re-entry beads stay deferred until their missing premises change.

## Open PRs and Integration Boundaries

At the initial survey snapshot, PR110, PR111 and PR114 were open and conflicted with
main.
PR114 subsequently landed and is incorporated here; PR110’s conflicts are resolved.
PR111’s separate integration remains with its owner.

| Open work | Relation to this branch | Integration requirement |
| --- | --- | --- |
| [110](https://github.com/jlevy/squares/pull/110), `codex/n11-hybrid-overnight` | Our mathematical checkpoints and measured scheduler repair | Retain both main’s new source work and our scoped results; validate the combined tree |
| [111](https://github.com/jlevy/squares/pull/111), atlas expansion to 324 | Changes corpus size, validator selection, budgets and PR/deep workflows | Review complete-versus-sampled coverage separately; do not transfer the frozen 100-case timing claim to this workload |
| [116](https://github.com/jlevy/squares/pull/116), kernel instrument | Separately owned BC264/H125 and stopped session097 | Finish its checkpoint publication before assessing a fresh scientific allocation |
| [117](https://github.com/jlevy/squares/pull/117), Figure5 controls; [118](https://github.com/jlevy/squares/pull/118), PDF font embedding | Separate paper/rendering follow-ups | Their owner reviews and published checks remain separate from this branch |

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
The later PR114 merge also changes the dependency lock and vendored kpress, adding
pinned font tooling and renderer controls.
It does not change the validator scheduler, workflows or budgets.
VE004’s 22.9% local median improvement remains evidence about its frozen 48-check
workload, not a new measurement of the merged tree.
Run the records and affected pre-push floor, then a full frozen combined-tree checkpoint
concurrently with hosted CI. PR110 retains the actual source-bound outcomes.
The first full local checkpoint remains bound to `dbd60231`; its timeout recoveries do
not validate the later dependency change.
The dispatched deferred checkpoint tests GitHub merge `c1b58f66`, whose Git tree equals
local PR114 integration `dcbcf2cf`. Use the updated lock and submodule for local checks
of that tree.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
