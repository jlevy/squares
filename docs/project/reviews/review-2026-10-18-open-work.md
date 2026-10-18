# Open Work Review — 18 October 2026

This pass fetched all **68 open GitHub issues and 16 open pull requests**, ran the
complete intake sweep, and reconciled the interrupted handoff with retained evidence.
The issue-by-issue disposition and raw source receipts are in the
[intake audit](review-2026-10-18-intake-audit.md).
This report distinguishes fresh source reviews from reviews of existing findings,
integration state, and contributor intake.

The comparison point is main at `804eff369193b698d497a9c06847059eb9de0470`. PR heads
below identify the reviewed snapshots, not scientific input identities.
No PR was merged, no contribution was declared mathematically accepted by this audit,
and no long certificate replay was started.

## Immediate Findings

- **#661:** the adoption writer reports the exact T-155-to-T-195 improvement beside
  T-155’s different, stale decimal display.
  The exact margin is about `1.566e-36`; subtracting the printed baseline instead gives
  about `5.434e-20`.
  [Review D](https://github.com/jlevy/squares/pull/661#pullrequestreview-5562181788)
  identifies the writer and regression test.
  Fix owners are `think-9143` and `think-0f8z`. The fix is pushed at `9783a53a2` and all
  59 adoption tests pass.
  [Independent follow-up E](https://github.com/jlevy/squares/pull/661#pullrequestreview-5562229750)
  confirms both fixes with no new findings.
  A stale data pin found by CI is repaired at `a87de0cf7`; all six targeted pin checks
  pass. The failed frontend atlas check passes locally, with browser source unchanged; a
  transient resize failure is suspected but not established.
  Fresh hosted checks determine final readiness.
  The broader display-consistency issue remains `think-gzrw`.
- **#671:** retention can overwrite and then delete an existing plain candidate while
  returning success. The manifest replacement is non-atomic.
  Release metadata, announcement expectations and page-size gates also need repair.
  [Review A](https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918)
  records six findings, owned by `think-8iky` and `think-5nvt`.
- **#665:** the adoption pass still carries a stale n236 custody attribution after its
  selected scope narrowed from 38 to 37 counts.
  Derived records, page size and live-data expectations also need reconciliation.
  Source registration of #574 is not evidence that this adoption branch is ready.
  [Review A](https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404)
  records 2 High, 2 Medium and 1 Low findings; `think-heuf` routes them to the existing
  `think-3mry` adoption lane.
- **#407:** main already has Darwin current RSS through libproc.
  The proposed Mach implementation passes native tests, but its useful SDK assurance
  should be reconciled with the implementation on main.
  This is `think-behe`.
- **#435:** the n83 coefficient link opens n87 because it uses a legacy polynomial-order
  anchor.
  [Review F](https://github.com/jlevy/squares/pull/435#pullrequestreview-5562286722)
  requires the stable n83 anchor and a producer-to-browser regression test.
  `think-5hv7` owns the correction under the existing formal-stack lane.

## All Open Pull Requests

“Green” below describes checks on the recorded head.
It does not certify a later conflict resolution, a new base, a deployment, or unfinished
scientific review.

| PR | Recorded head | Review and disposition |
| --- | --- | --- |
| [#671](https://github.com/jlevy/squares/pull/671) | `32d47d321` | Fresh senior review A: 3 High, 2 Medium, 1 Low. Required CI red. Repair retention/publication before integration; census and stage 4 remain open. |
| [#667](https://github.com/jlevy/squares/pull/667) | `a5b5f0ec2` | Fresh disposition B maps all 14 A findings to fixes or retained owners in replacement #676. Its four-file intake update is incorporated. Keep the original open until the replacement is accepted. |
| [#665](https://github.com/jlevy/squares/pull/665) | `bb85cbb59` | Fresh bounded senior source review; adoption and derived-output defects, required CI red. Retain the per-count adoption owners. |
| [#661](https://github.com/jlevy/squares/pull/661) | `a87de0cf7` | D’s numerical reporting and stale-status defects fixed; independent E confirms both. All 59 adoption tests and six pin controls pass. Later stale data pin repaired; fresh hosted checks pending. T-195 preserved. |
| [#658](https://github.com/jlevy/squares/pull/658) | `3022eb984` | Fresh follow-up C: prior source fixes hold, Low missing B disposition. Release-impact gate red. Ten focused tests pass; `think-8ido` retains correction work. |
| [#646](https://github.com/jlevy/squares/pull/646) | `f79f22cd1` | Fresh follow-up F: E fixes hold, Low stale PR description. Mergeable; release-impact gate red while frontend/Pages pass. `think-s9g3` tracks metadata follow-up. |
| [#645](https://github.com/jlevy/squares/pull/645) | `dafff1238` | Fresh follow-up F: E1–E7 fixes hold, 121 tests pass. Conflicts with main and release-impact gate red. Preserve the evidence distinctions during integration. |
| [#622](https://github.com/jlevy/squares/pull/622) | `31155575c` | Read-only contributor intake review A. Substance imported by #661. Keep `think-30n2` open through merge, deployed-side agreement and final reply. |
| [#599](https://github.com/jlevy/squares/pull/599) | `e5a046b3d` | Existing senior O and correctness P cover this exact head; new Q records the actual gate failures. Eight per-test and all four aggregate walls fail; conflicts with main. Continue `think-toaf`/`think-h96x`/`think-4syd`. |
| [#578](https://github.com/jlevy/squares/pull/578) | `e1f921bf0` | Fresh integration review A recovers the historical independent review and browser evidence. Standard CI has 31 successes; earlier full checkpoint passed. High current-main conflict and Low stale PR description remain. Keep profile population distinct from integration readiness. |
| [#574](https://github.com/jlevy/squares/pull/574) | `4c319c24a` | Read-only contributor intake review A. Current cumulative scope is 148 counts; 68 selected counts registered through #602/T-174. #665 and separate algebraic owners retain unfinished adoption. |
| [#514](https://github.com/jlevy/squares/pull/514) | `eb94b3dfd` | Fresh follow-up C confirms B1–B7 source fixes: six stamp tests and 25 Node tests pass. Current main conflicts and release gate is red. Reconcile newer result entries and generator writes when integrating. |
| [#435](https://github.com/jlevy/squares/pull/435) | `273abfa59` | Fresh F: Medium n83 link selects n87; Medium full checkpoint fails two call-wall guards. 32 ordinary checks and eleven separate full-run prerequisites pass. Clean against #403; that does not qualify the stack against main. |
| [#407](https://github.com/jlevy/squares/pull/407) | `78b8bbbd0` | Fresh senior A: native controls pass, Medium integration finding. Conflicts with main’s existing libproc implementation. |
| [#406](https://github.com/jlevy/squares/pull/406) | `8811bd763` | Fresh follow-up B confirms review A’s source fixes; 48 controls pass. Conflicts with main. Keep `think-lt52`/`think-h8d8` for integration and `think-xeav` for oversized historical files. |
| [#403](https://github.com/jlevy/squares/pull/403) | `3ee60c3e5` | Fresh J reviews the post-disposition delta and formal stack 447. Medium full-checkpoint blocker: 15 call-wall failures, despite 31 ordinary successes. Conflicts with main. Keep `think-6vrv`, `think-jygq` and exact-source owners open. |

The external forks #574 and #622 await workflow authorization.
That state is not a failed certificate test.
This review did not run contributor-supplied code or approve those workflow runs.

## Interrupted Census Handoff

The retained #671 snapshot contains all **18 registrations**, but native census and
control receipts for **n108 only**: **1 of 14** first-batch cases, **1 of 18** overall.
That receipt covers 201 verified directions and refused controls.
All 18 registrations remain **V0/C0**; the branch adds no certificate-specific stage 4
mathematics review.

The local process inspection found no census or verifier process on this Mac.
It cannot establish the state of a process on the previous remote host.
A statement that the batch “is running” therefore remains a historical handoff until its
host or retained output is recovered.
`think-f40c` retains the census/adoption work.

The adapted verifier’s source archive stays digest-only.
It has no license notice; the clean-room checker must remain independent.
No source was copied into the tree.
T-numbers are assigned in merge order: #661 keeps T-195, and later branches renumber
after integrating main.

## Other Work in Flight

The bead inventory contains **309 in-progress records** at this checkpoint.
That is a tracking state, not 309 running jobs, and this pass does not claim to have
revalidated every historical experiment.
The intake audit gives a disposition for every open GitHub issue; the following owners
cover the larger continuation lanes.

| Lane | Evidence and next action |
| --- | --- |
| New reports #666, #668–#670, #672–#675 | Eight request records and owners created; all bodies and comments retained. Follow stage 2 source custody before claiming feasibility. |
| Watched sources | New evand, Couzo and wand125 commits recorded; sq19 changes routed to the existing owner. New owners include `think-kjd7` for n42, `think-57ei` for Fang Lean, `think-ahr2` for Ryu Lean and `think-f8py` for the filled Ryu bound. |
| n19 optimality | `think-a4x3` keeps #640 and the changed sq19 source; source updates do not themselves close Lean/statement review. |
| n17 and Valid7 | #537’s new report claims 798 CPU-hours rather than 6,650, with 51 GB peak memory. Record and price that source update; no such replay was launched. Existing proof/census owners stay open. |
| Contributor profiles | #578 has 27 populated profiles; its historical census records 318 unresolved spans and 146 PDFs awaiting full inspection. `think-m7il` owns population, `think-5bao` integration. An idle chat or green old head is not an active census worker. |
| Polynomial source and web stack | #403/#435 are formally linked as stack 447. Finite geometry, exact identity, stationarity, rigidity and optimality remain separate obligations. Engineering checks do not close the held scientific rows. |
| CI efficiency | #599’s enforced quick run 38665027001 failed all four suite walls: 365.3/335, 467.4/360, 464.7/360 and 353.5/335 seconds. Individual call-wall failures also remain, including upper-bound comparison and verifier-registry controls. Use those exact tests for the next efficiency slice. |
| Publication-date correction | `think-tk0u` was still in progress after #647 merged. Verified merge `7b34cd5bb3e6c720dc5bcaa3d7361a9d666d9c29` and main’s corrected v0.7.11 date, then closed the stale bead. Existing deployment evidence was read; no new deployment test is claimed. |

Past budget approvals quoted in beads or reviews remain historical evidence.
This pass did not turn them into new authorization for CPU-hour experiments or merge
decisions.

## Validation and Review Limits

- #671: 224 focused tests passed; two targeted CI failures reproduced.
  The retained data checker and source-packet contract passed.
  A collision probe reproduced silent replacement and deletion.
  No expensive certificate replay ran.
- #661: nine focused exact-comparison tests passed; the baseline mismatch was reproduced
  with exact fractions.
  The follow-up fix has its own evidence.
- #406: all 48 blob-guard controls passed in 7.22 seconds at the pinned head.
- #407: all 11 native macOS memory controls passed in 0.98 seconds, including the
  compiled SDK oracle and release-of-mapping check.
- #665: 161 focused tests passed and seven failed, corroborating the stale adoption
  records and expectations.
  #658 passed ten focused regressions; #645 passed 121. #646’s two focused chooser tests
  pass; its broader release selection has 18 passes and two setup failures from missing
  worktree dependencies, not a clean suite.
- #514: six stamping regressions and 25 Node table tests pass.
  Browser and current rendered-page budgets were not freshly rerun in that follow-up.
- #403/#435: 11 parent extractor/storage controls, 17 child catalogue tests and eight
  child overflow/refusal controls pass.
  The maintained exporter reproduces the wrong n83 destination despite the catalogue
  tests passing. Both records retain 49 adopted V3/C3 and 89 historical native
  occurrences, with all 324 side/status/lower projections equal.
  No mathematical, native or Lean replay ran.
- Intake: online sweep, request schema, manual-source receipts and report-order ledger
  are recorded in the linked audit.
  The records tier passes 52 selected steps in 93.81 seconds; 125 request and ledger
  tests pass. The new ledger now participates in CI schema/render checks.
  Per-commit pagination completes the originally capped source-path inventory.
  Owned work is not equivalent to completed source-content or mathematical review.

Fresh reviews are published as formal comments through the repository’s
[tbd review workflow](../../../.agents/skills/tbd/SKILL.md).
They do not grant merge approval.
Remaining integration, scientific and publication gates stay with their named owners
rather than being closed by this inventory.

## Follow-up — 18 October 2026, 10:27 UTC

The original snapshot above retains its reviewed heads and findings.
Fresh GitHub reads establish these later changes:

- **#661**, still at `a87de0cf7`, has terminal green hosted validation, including
  [deferred checkpoint 39114501690](https://github.com/jlevy/squares/actions/runs/39114501690).
  Its deferred slow lane completed successfully at 09:44 UTC. Merge and deployed-side
  agreement remain separate gates.
- **#435** is now at `7c1fe653c`. The
  [F disposition](https://github.com/jlevy/squares/pull/435#issuecomment-6248506970)
  reports the stable n83 link repair and 32 passing catalogue/browser/case controls,
  including the generated-link regression that failed before the repair.
  Only mergeability has a hosted check at this new head; Packing and Pages evidence is
  missing. F2’s timing and final stack qualification remain with `think-6vrv`,
  `think-ht59` and `think-w0if`.
- **#676**, at `5fb743b3e`, has 31 successful hosted checks and 28 expected skips:
  [Packing](https://github.com/jlevy/squares/actions/runs/39114961111) and
  [Pages](https://github.com/jlevy/squares/actions/runs/39114961094). The earlier local
  push attempt remains a failed qualification: its JSON-layout defect was repaired at
  this head, but the reachable suite timed out at 900 seconds after an unidentified
  failure marker. `think-2jee` records a later isolated precision-test failure caused by
  importing workbench tools from the wrong checkout; the corrected import path passes
  that node. This does not identify the old failure marker or establish a local push
  pass. No current source defect was established by this bounded follow-up.

## Source-Custody Follow-up — 18 October 2026

Three new reports now have four complete stage 2 packets for their documented checker
entry points:

- **#668:**
  [de Winter’s three upper bounds](../../../packing/resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/README.md),
  at 227, 229 and 260. The retained MIT-licensed successor `9bf5d9be` changes only
  LICENSE and root README from the original claim pin `c95c4938`; the witnesses and
  checkers are unchanged.
  `think-qdcc` owns registration and validation.
- **#669:**
  [Daniel’s n155 packet](../../../packing/resources/web/evand-n155-explorer-2026-10-17/README.md),
  at MIT-licensed `59326b86`, retains the original and same-side display certificates
  with both standalone checkers.
  The issue and prior-packing report name Ostashev’s T-149 as the start; the regularized
  JSON instead says `by: ["Francisco Couzo"]`. Both statements remain in the packet.
  `think-n1ga` owns resolution before that field can supply attribution evidence.
- **#674:** Daniel’s
  [opening n229 packet](../../../packing/resources/web/evand-n229-dilation-2026-10-17/README.md),
  at MIT-licensed `e0338c7`, and
  [author update](../../../packing/resources/web/evand-n229-dilation-update-2026-10-18/README.md),
  at MIT-licensed `00e68df`, preserve both chronological claims and their standalone
  checker dependencies.
  The update’s `15.650161513896` is the current request; the opening `15.650163254859`
  remains in the report-order history.
  Both credit Daniel after Couzo’s #672, after de Winter’s #668. `think-5ij2` owns the
  import.

The source index and bibliography name the packets, dated by the original claims: 17
October for #668, #669 and #674’s opening, 18 October for #674’s update.
Custody checks establish retained inputs; no source checker or stage 4 replay ran in
this addendum. Separately, `think-qdcc` records a bounded source-level mathematical read
of #668 with no blocking geometry finding; exact witness/records binding and controls
remain pending. No result, bound, rung, house or drawing changed.

W1 remains open. The import runbook requires stages 1–3 for each new result on this
intake branch; these items have reached stage 2 only.
Stage 3’s final IDs and publication require an update from main and allocation in actual
merge order: #661 keeps T-195; each later PR, including #671 with its provisional
entries and this branch, takes the next available IDs only after updating from main,
then regenerates its views and data pin.
No ordering between #671 and #676 is assumed, and no ID is reserved or stated to an
author. Full push qualification, remote push and the PR update remain held for the
coordinator’s integration window and review of this interim addendum.

## Bulk Source Inventory Follow-up — 18 October 2026

A bounded read-only inventory of Couzo’s source pins `23aff0c6`, `af8cb795` and
`c6da0fc7` maps #670, #672 and #675’s 73, 46 and 79 issue-table improvements.
The issue-linked root certificates differ from same-count `best/` files at four counts
in #670 and nine in #672; a receipt for one set cannot establish the other.
#675’s broader index also credits Daniel’s 229 packing and contains two deletion-derived
witnesses; those relationships remain distinct from new discoveries.

The candidate custody scopes are approximately 9.7, 8.0 and 10.4 MB, respectively,
before compression. The import owners still need a bounded data-carrier decision under
OR-18. This remains stage 1 inventory: no bulk packet, checker run, geometric verdict or
stage 3 registration was added.
`think-f28n`, `think-2vjc` and `think-pvav` retain the imports and their exact
comparison, custody and replay-pricing obligations.

Concise post-merge reply drafts now exist in the eight answer beads for #666, #668–#670
and #672–#675 and are synced.
They quote no provisional result number or verification rung.
Each requires a fresh check against main, later issue comments and the deployed site
before posting; no issue comment was posted.

## Census Draft Follow-up — 18 October 2026

The opening
[#671 snapshot at `32d47d321`](https://github.com/jlevy/squares/blob/32d47d3214ec28f2a82b89689cd8bb8f63f98e02/packing/frontier/results.yaml)
records all 18 census entries at V0/C0. The later
[draft at `89166716`](https://github.com/jlevy/squares/blob/89166716d492ae7e4e76f61550e80849dec7edc3/packing/frontier/results.yaml)
records n108, provisionally T-211, at V3/C3 using its retained 201-direction census and
two accepted mathematical reviews; the other 17 entries remain V0/C0. These are
draft-branch records: #671 remains unmerged, with no promotion to main.
This follow-up claims no fresh native replay or independent full implementation.
The opening audit statements describe their pinned snapshot; the current draft’s IDs
remain provisional under the merge-order rule above.

## Local Qualification Follow-up — 18 October 2026

At clean `611b45437`, the records tier passed all 52 selected steps in 95.57 seconds.
The push tier passed 66 of 67 selected steps in 1,219.13 seconds, failing only the
[resident-Rust shutdown control](../../../packing/tests/test_rust_rectangle_geometry.py).
Its half-second fixture deadline yielded zero completed angles, consistent with expiry
before the first angle; the unchanged control passed in isolation in 0.59 seconds.

`think-26gw` tracks the test repair: hold the clock through startup and the completed
angle, then allow a real 0.05-second shutdown wait through the actual protocol code.
The control still requires INCONCLUSIVE, a backend timeout and one VERIFIED angle; it
also requires the worker to have terminated.
All seven focused boundary controls pass in 2.63 seconds, with Ruff and BasedPyright
clean. The production verifier and its deadlines are unchanged; no newly reported
certificate was replayed.
The resulting head requires a green push tier before publication, with terminal gate and
hosted-check evidence retained in #676 and `think-1ayi`.

## Watched-Source Freshness Follow-up — 18 October 2026

The interim online refresh read 45 watched repositories, including the newly watched
[Joost de Winter repository](https://github.com/JoostdeWinter/square-packing) retained
by the stage 2 addendum.
GitHub issue bodies, replies and comments still match the intake record.
This refresh is separate from the earlier closing sweep above and is not the final
post-publication sweep.

It found two new wand125 commits.
Both complete diffs were read:
[`08d77305`](https://github.com/wand125/square-packing/commit/08d77305c0838d521e5a5339ea5f41fd60b625b8)
changes four site metadata, sitemap and page files, and
[`6d93afc1`](https://github.com/wand125/square-packing/commit/6d93afc1e5336aa498c0a7657c0869dc648a7b92)
changes the theme index.
Their edits only rename “two unit cubes in a cube” to “two unit hypercubes in a
hypercube” in English and Japanese titles and links.
The mathematical expressions, n = 3 to 6 scope, proof text, certificates and checkers
are unchanged. A no-result watch read now records the new head; the earlier Valid7 and
n42 imports remain with `think-0ayk` and `think-kjd7`.

The original full history/tree fetches for BuddenPing, Esummins, Daniel and Couzo each
hit the 60-second cap.
The retained
[bounded HEAD refresh](../../../packing/campaign/issue-intake/intake-20261018/bounded-four-head-refresh-20261018.json)
records four successful GitHub API reads whose default-branch SHAs exactly equal the
existing `read_through` pins: `73d25427`, `eb3ae154`, `5ca0dc3a` and `c6da0fc7`. This
covers current head freshness without claiming fresh full-history or source-content
audits, imports or replays.
The original fetch timeouts remain limits of the interim sweep, and the existing import
owners retain their work.
UnitSquare and SQUISH remain the separately hand-checked sources recorded for 18
October.

## Isolated Qualification Environment — 18 October 2026

The later push attempt at `8f4f8a5ce` was cleanly stopped after 309.30 seconds (exit
130), when another worktree’s hook rebuilt editable packages in the shared Python
environment. Direct imports with this branch’s `PYTHONPATH` remained local, but a fresh
process without it resolved `sqpack` and `kpress` to #665; nested subprocesses can
replace or clear that variable.
This invalidates the qualification attempt without establishing a source failure.
Its original log and import-origin receipt are retained under `think-1ayi`.

A frozen install now gives #676 an isolated environment on external scratch through
`UV_PROJECT_ENVIRONMENT`. Fresh imports without `PYTHONPATH` resolve `sqpack`, `kpress`
and the workbench tools to this checkout; the checkout-import preflight passes, and
Ruff, BasedPyright and browser dependency paths resolve correctly.
The shared environment was not changed by this mitigation.
`think-rl4i` tracks a reusable safeguard separately; this branch changes no validation
harness code for it.
The resulting head requires fresh records and push tiers in the isolated environment.

## Census Admission Fixture Follow-up — 18 October 2026

At clean `600539c43`, the isolated records tier passed all 52 selected steps in 111.27
seconds.
Its push tier passed 66 of 67 selected steps in 741.09 seconds, failing only the
complete-row census fixture.
The retained journal records a 2-second timeout after exact rows 0 and 1 of the
requested 0, 1 and 2; the wrapper correctly returned PARTIAL_ROW_EQUALITY. The unchanged
case and adjacent subset and malformed-value controls pass in isolation (three tests in
1.95 seconds).

`think-urgl` gives only the success/admission helper a bounded 30-second budget for
startup and journal writes on loaded hosts.
The separate sleeping-checker timeout control remains at 2.0 seconds, with the
complete-row and exactness assertions and production admission rules unchanged.
All 13 focused module tests pass in 3.88 seconds; Ruff and BasedPyright are clean.
Fresh exact-head records and push tiers remain required before publication; this failed
gate is retained as a fixture timing failure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
