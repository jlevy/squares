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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
