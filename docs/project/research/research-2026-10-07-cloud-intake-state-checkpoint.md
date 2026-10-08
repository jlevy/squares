# Cloud Intake State Checkpoint

Checkpoint: 8 October 2026 UTC, continuing the 7 October intake.
Main is
[`84881f214`](https://github.com/jlevy/squares/commit/84881f214086bf5b8ce83a714c4fda6d7be7b2d1).
The original SQUISH intake is merged, published, and closed.
The nine-packing second update has separate import and confirmation PRs; their final
validation and merge remain pending.
Issue #425 has a reviewed replay protocol and retained inputs, with zero deciding checks
executed. Its complete preparation is backed up as a draft GitHub release; public
scientific publication and actual replay remain pending.

For $s(n)$, the smallest side of a square containing $n$ unit squares, a feasible
packing establishes an upper bound.
Optimality requires an independent matching lower bound.
The import layer records source claims and provenance; the confirmation layer proposes
verification of those exact configurations.
Neither layer establishes local minimality or rigidity from feasibility alone.

## Completed Work

| Work | Completed state | Durable record |
| --- | --- | --- |
| Original SQUISH intake | Import and confirmation merged. | [PR415](https://github.com/jlevy/squares/pull/415), [PR416](https://github.com/jlevy/squares/pull/416) |
| First update | Import and confirmation merged; historical packets retained. | [PR421](https://github.com/jlevy/squares/pull/421), [PR423](https://github.com/jlevy/squares/pull/423) |
| Cloud publication account | Research report and verified closure record merged. | [PR418](https://github.com/jlevy/squares/pull/418), [PR426](https://github.com/jlevy/squares/pull/426) |
| Eighteen selected imports | Published at main `2af487e7`; independent strict-TLS site check passed 1,234/1,234, case/result/geometry audit 149/149, desktop/mobile layouts 38/38. | [Publication receipt](https://github.com/jlevy/squares/pull/426) |
| Issue #401 | Final reply published; issue closed at 22:54:52 UTC. Four native tracking beads closed; tracked outboxes empty. | [Final reply](https://github.com/jlevy/squares/issues/401#issuecomment-6048513671) |

## Second SQUISH Update: Import and Confirmation

[Issue #422](https://github.com/jlevy/squares/issues/422) supplies nine configurations:
88, 108, 179, 180, 199, 207, 236, 263, and 302. The source revision is
[`e63e4e52`](https://github.com/itsnaka/squish-certs/commit/e63e4e52b1728b6671b2f263c5e02a4aa79a39d3).
Source credit, seed lineage, original packets, and the earlier independently certified
ceilings remain attached to their own geometries.
The independent lower bound $s(88) \ge 481/50$ remains unchanged.
A feasible smaller packing refutes the earlier conjectured optimum at n88; it supplies
no replacement optimality proof.

| Layer | Exact source and base | Current disposition |
| --- | --- | --- |
| [Import PR427](https://github.com/jlevy/squares/pull/427) | Head `f1d7eacafc1249b430771583edf2120b5fc17d7b`; base main `84881f214`. Source, inventory, and metadata repairs remain in history. | Complete the remaining required heavy phase after the supported capability replay; preserve failed attempts below. |
| [Confirmation PR429](https://github.com/jlevy/squares/pull/429) | Head `0d01524be4235b7f12e6a971d73ea7d576fbac0f`; base the import head `f1d7eaca`. Source, archive, and metadata revisions remain in history. | Proposed T-116 at V3/C3/S3 remains a draft registration. Reviews A–D published with zero findings; final gate, hosted CI, deployment, and merge pending. |

The import metadata names producer revision `6c615115140c10e281c50d503a3fc46ddf4d4e25`
as its required `DATA_REVISION`. The upper producer metadata names
`c5ee0723987faf0e0e0e35ccad588aca034a0dbb`.

The confirmation branch retains all 27 completed deciding jobs, each exiting zero.
The positive batch covers 190,303 square pairs per independent route; positives and
controls cover 570,909 pairs per route.
Two independent mathematical reviews accepted the scoped replay.
Native worker validation took 22.65 seconds after the base change; nine
history-preservation tests passed in 21.31 seconds.
These receipts cover their declared scope; final branch-wide acceptance remains pending.

The measured snapshot occupies 201,216,934 bytes against the unchanged 201,326,592-byte
cap, leaving 109,658 bytes.
Scientific inputs and completed replay receipts are retained on the
[confirmation branch](https://github.com/jlevy/squares/tree/0d01524be4235b7f12e6a971d73ea7d576fbac0f/packing/resources/web/squish-422-second-update-2026-10-07).
No timeout, byte ceiling, or mathematical assertion was weakened to obtain these
receipts.

### Validation History and Outstanding Reviews

| Attempt | Actual outcome | Disposition |
| --- | --- | --- |
| Initial import gate | Exit 1 after 620.24 seconds; four failed steps. Behavioral phase: 14 failed, 6,245 passed, 30 skipped, one expected failure. Heavy phase unrun. | Technical failure: repair the owning source and derived records; retain this receipt. |
| Corrected `3c` gate | Exit 130, cancelled; terminal accounting was 94 passed commands, one failed, one cancelled. Normal and heavy pytest phases did not complete. | Cancelled attempt: preserve receipt; obtain final-source evidence. |
| Final `f1` gate | Exit 1 after 983.36 seconds, below the unchanged 1,800-second ceiling. All 97 prior commands passed. Reachable phase: 801.22 seconds, below its 900-second ceiling. Ordinary pytest: 13,219 passed, one failed, 30 skipped, one expected failure in 799.37 seconds. Heavy phase unrun. | Confirmed sandbox capability failure; preserve the broad exit 1 and use the scoped replay below. Heavy phase remains required. |

The sandbox denied the profiler’s own `/proc/self/clear_refs` access.
The unchanged complete profiler module passed both tests under supported escalation in
1.65 seconds, exit 0. This capability replay supplements the failed broad gate; it does
not relabel that gate as green.
The exact selected heavy phase is pending and will run separately, without repeating the
13,219 ordinary passes.

Lower-PR reviews A–D are published.
Final-source follow-up reviews
[E](https://github.com/jlevy/squares/pull/427#pullrequestreview-5449810151),
[F](https://github.com/jlevy/squares/pull/427#pullrequestreview-5449810241),
[G](https://github.com/jlevy/squares/pull/427#pullrequestreview-5449810343) and
[H](https://github.com/jlevy/squares/pull/427#pullrequestreview-5449810455) are
published at `f1d7eaca`, with no new findings.
Upper reviews
[A](https://github.com/jlevy/squares/pull/429#pullrequestreview-5449863506),
[B](https://github.com/jlevy/squares/pull/429#pullrequestreview-5449863621),
[C](https://github.com/jlevy/squares/pull/429#pullrequestreview-5449863708),
[D](https://github.com/jlevy/squares/pull/429#pullrequestreview-5449863858) are
published at exact `0d01524b`, each with zero findings.
Upper gate and hosted CI acceptance remain separate.
Hosted lower `f1` is clean: 30 successful checks and 26 skips.
Upper `0d` has 25 successes, 26 skips, and five failures: `validate`, `suite-a`,
`suite-b`, `suite-c`, and the required aggregate in
[run 37705180742](https://github.com/jlevy/squares/actions/runs/37705180742). The upper
source owner is diagnosing those failures under `think-x2gl`; review approval does not
replace CI repair. Acceptance of a scientific replay does not close those engineering
reviews.
The authoritative remote [stack #430](https://github.com/jlevy/squares/pull/430)
has PR427 below PR429. Both issue #422 references remain nonclosing until actual
publication. The formal stack must reach clean final-source review and CI before the
coordinator merges it.

The native tracker records each initial senior finding separately under repair bead
`think-lbku`:

| Finding | Owning repair | Bead |
| --- | --- | --- |
| A1 | Include the retained packet in the sweeps sparse checkout. | `think-911t` |
| A2 | Refresh chunk partitions, census, and evidence through their producers. | `think-ez9v` |
| A3 | Recompute all nine rigidity assessments at the existing tolerances. | `think-g7fk` |
| A4 | Declare the external raw-source byte boundary. | `think-snp3` |
| A5 | Regenerate the open-frontier table. | `think-m1ck` |
| A6 | Read rational coordinates in the diagnostic structure consumer. | `think-o6up` |
| A7 | Keep first-update citation tests bound to their historical configurations. | `think-ougm` |
| A8 | Reconcile source-sensitive behavioral contracts with the reviewed new geometry. | `think-kf2k` |

This checkpoint is tracked by `think-vz6u`, under `think-msos`. The parent `think-sfpz`,
confirmation `think-kqd3`, reply `think-qc6y`, and repair `think-lbku` remain open.
Source fixes and focused checks are recorded; closure depends on final-source gate,
reviews, CI, merge, publication, and the issue reply.
Native records are retained on
[tbd-sync](https://github.com/jlevy/squares/tree/tbd-sync/.tbd/data-sync/issues).

## Issue #425: Reviewed Protocol, Replay Pending

[Issue #425](https://github.com/jlevy/squares/issues/425), tracked by `think-f3dl`,
selects the complete n105 and n292 inputs.
The frozen-v2 protocol includes ten inputs covering 1,985 squares and 7,940 corners.
Separate mathematical and input-binding reviews accepted that protocol.
Zero deciders have run; no feasibility verdict or assurance promotion is registered.

The proposed retained core exceeds the 109,658-byte current snapshot headroom; canonical
storage remains unresolved.
The complete preparation is preserved in a
[draft GitHub release](https://github.com/jlevy/squares/releases/tag/untagged-5c79f36e3406b6245cdd),
release 406258689, tag `intake-425-preparation-2026-10-07`. Draft access requires a
repository account with access; this is not a public scientific release.

The archive contains 138 files and 6,669,242 bytes, SHA256
`00d4172972c82b2b928bc8427cff24c9a0d3c952da7ec8bf617f55399b8a9d80`. Its 28,616-byte
member manifest has SHA256
`6b7ba4f5011d799975c5ccab543aa9425c35e27b36131ef07e2f6326efd681c5`. An actual GitHub
download matched the archive hash, and archive/member-manifest round-trip verification
passed. Full source acquisition, all ten inputs, runtime/schema/module code and both
distinct accepted protocol reviews are retained, with credentials and caches excluded.
Restore with authenticated
`gh release download intake-425-preparation-2026-10-07 --repo jlevy/squares`; inspect
archived upstream code as source data.
Actual replay and full receipt follow-up remain required before any assurance promotion.

The same draft release also retains
`cloud-intake-operational-records-2026-10-08.tar.gz`: 703 files, 43,897,170 bytes
expanded, 7,805,026 bytes compressed, SHA256
`5202871832454b89669c1fb4ba673e890fa73068cb5181950ef7d2961bbc16ed`. An authenticated
GitHub download matched that hash.
This point-in-time backup covers queue plans, repair/failure/review records, and
native-state receipts before later repairs; the separate 138-file #425 archive remains
immutable.

The same draft release also retains the deployed issue #401 site verification and
renderings: 108 files, including live/result/layout receipts, screenshots, and the
original failed probe assumptions beside their corrected outcomes.
The archive `deployed-401-site-verification-and-renderings.tar.gz` is 30,263,587 bytes,
SHA256 `0134d248097ca8bcff23732d2a97a71347a8b922d5aef685fec3f51136e13696`. An actual
GitHub download matched that hash.
These are historical publication records; they do not verify the pending issue #422
deployment.

## Remaining Queue and Environment

| Work | Next bounded action |
| --- | --- |
| [#428](https://github.com/jlevy/squares/issues/428) | Under `think-v42c`, review Seth Rehwaldt’s n68 refinement at [fded6866](https://github.com/lollipoll/certified-square-packing-68/commit/fded686668e29258dad2eb29d0482fa3fd51bd6b), release v1.1.0. Compare the complete rational side, whose reported improvement is about 8.7988e-20; the 18-place ceiling is larger than Daniel’s. Independently review complete inputs and receipts before scoped replay. Author-reported checks have zero project deciders or review so far. |
| [#419](https://github.com/jlevy/squares/issues/419), [#420](https://github.com/jlevy/squares/issues/420) | Review exact configurations and local-minimum definitions separately, then select small replay controls before bulk execution. |
| [#414](https://github.com/jlevy/squares/issues/414), [#368](https://github.com/jlevy/squares/issues/368) | Review the baseline, quarter-power, and cube-root dependency chain and its closed-set packing convention. |
| [#399](https://github.com/jlevy/squares/issues/399), [#375](https://github.com/jlevy/squares/issues/375) | Retain new rational certificates separately from historical exact forms and upstream wrapper repairs. |
| [#400](https://github.com/jlevy/squares/issues/400), [#405](https://github.com/jlevy/squares/issues/405), [#413](https://github.com/jlevy/squares/issues/413) | Continue existing n17 research and verifier ownership; current source claims do not complete the proof. |
| [#411](https://github.com/jlevy/squares/issues/411), [#366](https://github.com/jlevy/squares/issues/366) | Record repository aliases and bind original inputs to existing receipts. |
| [#256](https://github.com/jlevy/squares/issues/256) | Capture the packaging comment as maintenance; no new mathematical admission. |

The current instance supports authenticated GitHub pushes, PR creation and native tbd
sync, and passed the repository bootstrap.
The latest proposed startup save returned `stale_base` after the configuration base
changed; its latest instructions were not saved.
The separate four-file `squares-environment-handoff.zip` is also an asset on the draft
release. Reconcile those tested installation/startup/helper files from a new setup chat
bound to the current environment settings before saving and publishing.
Current-instance checks do not establish new-task restoration.

The final import gate’s sole failing test is
`tests/test_profile_n17_kernel_memory.py::test_the_profiler_marks_production_the_save_and_the_check`.
The supported complete-module replay passed; no full-gate success is claimed.
The selected immediate sequence is to finish the remaining required heavy phase and
PR429 validation, and obtain clean hosted CI before the formal stack merge.
Verify publication and close the native reply work after merge.
Issue #425 canonical storage and its first replay remain under their own open bead; the
remaining mathematical intake proceeds through its bounded reviews.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
