---
title: N17 Merge Readiness Review — October 8, 2026
---
# N17 Merge Readiness Review — October 8, 2026

The review covers the formal [#404](https://github.com/jlevy/squares/pull/404) →
[#454](https://github.com/jlevy/squares/pull/454) →
[#461](https://github.com/jlevy/squares/pull/461) stack and supporting PRs
[#452](https://github.com/jlevy/squares/pull/452),
[#453](https://github.com/jlevy/squares/pull/453) and
[#457](https://github.com/jlevy/squares/pull/457). The work is not yet merge-ready:
current integrated-source required CI and a complete checkpoint remain outstanding.
No merge or draft promotion is authorized by this review.

## What the mathematical work establishes

The official bracket remains
`4.66044275 < s(17) <= 4.6755300936045509516342148538535054`. The latest official
movement is [PR362](https://github.com/jlevy/squares/pull/362), T-093, October 5. This
stack records local and conditional certificates, strategy tests and infrastructure; it
does not establish another lower bound or optimality.

The retained ordinary census has 60 admissions, 36,768 surviving states and 4,683
orbits, with the endpoint surviving.
The 95-orbit/744-state hard tail is a subset.
Tail A/B standing verification differs from HEADER_ONLY and incomplete C2 replay.
Projection cuts and numerical LP results support the next shared-centre investigation;
they do not themselves exclude an ordinary assignment.
The proposed first-eight targets remain unimplemented, unregistered and unrun.

Original exp315/316 method identities and raw receipts remain unchanged.
Their original source history is retained on the remote
`codex/n17-endpoint-source-custody-20261008` branch.
The annotations explain the history required after stack rebasing; they do not waive
provenance validation.

## Review coverage and dispositions

The parent review is pinned to `1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88`, with merge
base `7a8d9c16daa267c3a778554036374884194c2c36`. Two Astra mathematical/deep correctness
lanes and Sol 6.1 engineering/documentation lanes cover all 140 changed
code/configuration paths at least once.
Existing files receive complete changed-hunk review and relevant context; new files
receive full reads. This is coordinated coverage, not a claim of independent complete
rereads.

All 180 changed Markdown files received structure/footer checks.
Substantive review joins the research reports, H276–322, exp259–314, Sessions 184–186,
result READMEs, source provenance and admission/custody summaries.
The 862-file diff is mostly retained evidence.
Bulk JSON/archive lines were assessed through those maintained records; they were not
manually read or freshly replayed in full.

The formal parent reviews are
[A — senior](https://github.com/jlevy/squares/pull/404#pullrequestreview-5463921082),
[B — input and publication boundaries](https://github.com/jlevy/squares/pull/404#pullrequestreview-5463921224),
[C — performance](https://github.com/jlevy/squares/pull/404#pullrequestreview-5463921402)
and
[D — mathematical correctness](https://github.com/jlevy/squares/pull/404#pullrequestreview-5463921506).
A1 tracks missing integration/CI/checkpoint qualification.
The bounded repairs address:

- B1: refuse aliased child/report outputs before intake or publication, preserving
  existing destinations.
- B2: retain structured refusal for phase traversal, pre-validation descriptor
  adaptation, truncated child gzip and inherited Git/YAML registry failures.
  Programming errors still propagate; resource timeouts remain incomplete.
- B3: use the sanitized Git environment for source tracking as well as worker init/add,
  preserving source indexes and snapshot-mutated bytes.
- D1: annotate H315’s historical sign shorthand without changing the frozen criterion,
  original body, result or source identity.

Astra found no new mathematical soundness defect.
The existing standalone BB polygon-order weakness is separately tracked as `think-t41a`:
arbitrary full-BB intake needs complete source-cell enclosure.
The new header guard supplies that check; correctly ordered retained FULL manifests and
guarded header receipts are unaffected.

## Validation and remaining qualification

The B1/B2 repair’s ten affected synthetic test modules pass 366 controls with zero
deselections: 23.94 seconds of summed pytest wall and 26.673 seconds of summed process
wall. A later test-format correction passes its six affected controls again; those
repeats are excluded from the 366-control total.
B3 passes three focused controls in 1.20 seconds, with 87 unrelated cases deselected;
all ten shared repository-scope controls pass in 0.66 seconds.
Targeted lint/format/type checks are clean.
These results verify the bounded repairs, not a full gate or proof replay.

The latest-main source integration joins `91ca9b824` after nine conflict resolutions.
It preserves the earlier held merge and original source history.
All eight memory-profiler controls pass in 1.06 seconds; the local-certificate
end-to-end control passes in 14.03 seconds with independent exact replay and a fresh
rational ratio at least as strong as the retained bound.
The three source-index controls pass again in 3.36 seconds, with 122 unrelated cases
deselected. Both resolved test modules pass Ruff/format and BasedPyright with zero
findings.

The edit tier takes 179.75 seconds and passes 62 of 63 selected steps.
Its browser-floor failure is a missing isolated-worktree dependency link, not a source
lint failure. Reusing the existing installed dependency completes the focused browser
floor and its 56 liveness controls in a 30.97-second two-step PASS. This composes the
edit qualification; no clean full edit invocation, push gate or complete checkpoint is
claimed. Documentation, SYNOPSIS, ledger and 403 declared commands pass.

Earlier owning-layer repairs pass all 18 reconciliation controls and all 49 endpoint
controls. Their source blobs survive formal stack rebasing.
Final selected documentation/SYNOPSIS and ledger checks passed in 10.86 seconds; the
earlier failed attempts and narrower qualification remain explicit.

Supporting #452/#453/#457 pass their required Packing/Pages checks and hosted full
checkpoints [37849978427](https://github.com/jlevy/squares/actions/runs/37849978427),
[37849985359](https://github.com/jlevy/squares/actions/runs/37849985359) and
[37849991774](https://github.com/jlevy/squares/actions/runs/37849991774). Those
checkpoints used main `f0ec5b66`, before `91ca9b824`; they are not replays against the
later main tree. Windows native qualification in #453 and #457’s diagnostic cause
investigation retain their documented limits.

The generated timing register’s cohort
[37613399745](https://github.com/jlevy/squares/actions/runs/37613399745) passed.
Its exact merge source matches the recorded provenance; all 615 weights are finite and
nonnegative, no historical module key was dropped, and shard ceilings are unchanged.
Timing admission is neither proof admission nor current-head CI.

The newer automatic runs qualify the actual merge checkout trees, which match the
published heads. Pages passes on all three layers; Packing fails on each:

| PR and source head | Pages | Packing | Actual checkout |
| --- | --- | --- | --- |
| #404, `18e3a6f4f` | [PASS 37860039643](https://github.com/jlevy/squares/actions/runs/37860039643) | [FAIL 37860039766](https://github.com/jlevy/squares/actions/runs/37860039766) | `62a361c8ca69ad672ad01a1600a9c719ada00328` |
| #454, `5dc4d13bc` | [PASS 37860039795](https://github.com/jlevy/squares/actions/runs/37860039795) | [FAIL 37860039856](https://github.com/jlevy/squares/actions/runs/37860039856) | `914241ad61b588cdebb6fb277061d591751fd2ee` |
| #461, `7421e2daf` | [PASS 37860039410](https://github.com/jlevy/squares/actions/runs/37860039410) | [FAIL 37860039390](https://github.com/jlevy/squares/actions/runs/37860039390) | `d1fbbaf15201cc134361cc3b2d99cf42e98f5039` |

The checkout logs and Git tree identities establish source qualification; dynamically
updated run metadata alone does not.
These completed runs supersede earlier observations of absent or cancelled current
checks.

Packing exposes twelve combined-process control failures: ten nested path/hash controls
and two gzip EOF controls reach the process-wide purity refusal before their intended
input boundary.
The earlier 366 controls passed in separate modules; that result does not
establish combined-shard isolation.
The follow-up runs these CLI controls in clean subprocesses, preserving the production
purity checks and child-local failure sentinels.

Three worker failures need source dependencies or tracked-source indexes.
Two tiny fixtures now initialize sanitized local indexes, and a missing-index sentinel
refuses before worker Git mutation.
Explicit copyback restores the retained J-fixed certificate and B-ablation input, adding
558,148 selected bytes.
These inputs were unintentionally omitted by the historical whole-session prune; no
scientific evidence is removed to fit the cap.
Scoped Ruff, format and type checks pass, as does the no-disk missing-index control.
An initial external scratch directory preflight fails ENOSPC before launch.
After the measurement lane releases its temporary fixtures, an actual write preflight
permits a bounded combined run: all twelve repaired CLI controls, both indexed cloning
controls and the missing-index sentinel pass beside all 39 producer-module controls, 54
controls in 3.89 seconds.
This shared-process run exercises the previously contaminated import context.
No full worker snapshot is copied or qualified.

The suite-cost guard also failed with 79 unmeasured files.
Fifteen fresh, successful, unsharded and unfiltered whole-module runs pass 413 controls,
with 25.762 seconds of summed setup/call/teardown time.
Their retained reports append fifteen costs, preserving all 615 historical weights,
provenance, shard capacities and the 10% guard.
The current root partition has 64 unmeasured files; its four shares are 9.5%, 9.0%, 9.5%
and 8.8%. An attempted guard-ownership module passed 47 controls and failed two after
exhausting external space while writing CLI receipts; that failed report is retained
separately and is excluded from admission.

Root #404’s frontier rendering test also exceeds its unchanged 300ms longest-task limit
at 390px: 316ms in light mode and 303ms in dark mode.
The renderer, input assets, probes, launch configuration and locks are identical across
these three heads, but hosted artifact byte equality and identical physical scheduling
are not established.
Pages checks the frontier sequentially; the failing pytest lane uses three workers.
Failure output now exposes bounded existing long-task, readability and animation-frame
attribution. This diagnostic change preserves every assertion; no performance cause or
fix is claimed.

All 67 suite-file regression controls pass in 3.11 seconds.
Before cost admission, the records tier passes 45 of 47 steps in 25.25 seconds: the lint
tool directory is missing from PATH, and the suite-D pending measurement has expired.
The environment is corrected for subsequent checks, and the actual successful historical
suite-D reading is admitted: 101.34 seconds at four CPUs, one outer and one inner job,
one of 101 steps, from job 112765857172 in the complete green cohort 37613399745. Its
exact checkout is `33e96ced9ddf5025e47ecad8420865cf519102b8`. The later independently
passing suite-D job 113593324236 reads 190.63 seconds at one of 105 steps.
It is not pooled with the earlier shape and does not establish compliance with the
unchanged 143-second ceiling.
Current performance qualification remains open under `think-t7k5`. After these repairs
and the tool-path correction, all 47 selected records steps pass in 23.54 seconds.
The complete checkpoint and current hosted Packing qualification remain outstanding.

The worker source-copy ceiling remains 192 MiB. The one-line proposal to allow 224 MiB
is unapplied pending the human decision after automatic approval review rejected the
persistent quota increase under disk pressure.
Mathematical work, rational-bit, wall-time and RSS ceilings are unchanged.
Bulk worker copies and builds remain paused when external scratch cannot hold them.
No evidence is removed to fit the ceiling.

Complete current-source integration, required Packing/Pages CI and the full checkpoint
before declaring merge readiness.
`think-0m0x` tracks qualification and `think-iz2b` tracks integration.
Progress comments belong on [tracker #405](https://github.com/jlevy/squares/issues/405),
whose main body carries long-lived proof goals and background.

## Consolidation Addendum — October 8, 2026

The refreshed review keeps six open deliverables: the formal #404 → #454 → #461 research
stack, and standalone #452, #453 and #464. Their responsibilities are distinct;
combining the independent fixes with the research would enlarge review without closing a
mathematical dependency.
PR #410 is already merged as `e74a82190`.

| PR | Retained contribution | Current disposition |
| --- | --- | --- |
| [#404](https://github.com/jlevy/squares/pull/404) | Conditional exclusions, accepted-input context, the ordinary census and maintained research/validation tools | Current-main integration resolves the synopsis, document map, measured suite costs and budget-record conflicts. Required qualification remains open. |
| [#454](https://github.com/jlevy/squares/pull/454) | Contributor applicability, collision-safe pattern identities and route selection | Retain as the second stack layer; propagate the owning-layer integration before relying on its CI. |
| [#461](https://github.com/jlevy/squares/pull/461) | Exact endpoint relaxation calibration with explicit frame custody | Retain as the third layer. Astra reviews E/F at `d96a2c383` establish no new source finding; all 49 synthetic controls pass. Required qualification remains open. |
| [#452](https://github.com/jlevy/squares/pull/452) | Retire decoded BB node records after their selected uses | Existing exact-head senior/security/performance/correctness reviews and required CI are green. The recorded full checkpoint qualifies its stated earlier integration tree. |
| [#453](https://github.com/jlevy/squares/pull/453) | Publish native kernel receipts atomically | Existing exact-head reviews and required CI are green. Retain its documented platform qualifications and earlier full-checkpoint scope. |
| [#464](https://github.com/jlevy/squares/pull/464) | Packing/SOS source review, exact forced-face derivation and weighted-vertex screening plan | Current main is integrated; problem/domain/certificate definitions make the review standalone. Mathematical review and final required qualification are separate gates. |

[#457](https://github.com/jlevy/squares/pull/457) is closed as fully superseded by main
commit `e0792f403`. Its resolved integration is exactly main’s complete tree
`fa6c26ca328cf3e41b9bc70edc6ac8f99a60d278`: native layout-shift attribution and its
regression control are retained alongside font-arrival diagnostics.
No empty integration PR is needed.

The current main input is `3213d651b`. Conflict resolution retains both sets of document
entries and regenerates the synopsis counts from the integrated records.
The suite-cost register retains main’s newer complete hosted cohort, adds all 20 older
module keys missing from that cohort, and retains both sets of whole-module admission
provenance.
It contains 645 finite measured module costs; shard capacities and acceptance
ceilings are unchanged.
The two historical suite-D shapes are not pooled or presented as current performance
qualification.

Current failed Packing runs show a shared source-copy refusal, not a mathematical
counterexample: #404 selects 202,715,130 bytes, #461 selects 203,207,942, and #464
selects 201,968,306, above the 201,326,592-byte limit.
Fresh main’s live and committed inventories agree at 200,978,830 bytes.
A bounded follow-up audit found only 9,013 duplicate bytes, insufficient to cure the
failure, and no justified new output class to omit.
Broad schema and campaign readers prevent inferring unused input from absent
command-line mentions.
Dependency-selection engineering remains under `think-t1lk`; the earlier 192→224 MiB
proposal remains unapplied pending the explicit user decision.
Scientific inputs remain retained.

The selected mathematical entry remains the first-eight shared-centre LP. The new source
review then selects an exact weighted-vertex screen before an eligible SOS experiment; a
quadratic-ball variant requires its own preregistration and exact containment check.
Neither analytical reduction has run on a target.
Endpoint calibration, a feasible relaxation, a conditional exclusion and a global
lower-bound movement retain distinct statuses.
The bracket and latest official movement remain unchanged: PR362, T-093.

The source audit found no unique unpublished n17 commit content: custody commit
`70e7ab82` agrees with the three corresponding files in current #454. All ten untracked
execution/acquisition files in the recovery checkout match the corresponding tracked
exp311 files byte for byte.
They are already captured on #404; the held older integration index and the primary
checkout remain preserved.
`think-foe5` tracks this consolidation; existing qualification owners remain open until
their exact integrated source passes the required gates.

## Current-Main Fixture Recovery

The
[current-main Packing run](https://github.com/jlevy/squares/actions/runs/37882100437)
finds three fixture-integration failures beside three source-copy budget assertions.
Two synthetic alias repositories lack the tracked-source index now required by the
standing worker; the census missing-object control patches an interface main replaced.
The repair uses the existing sanitized fixture-index helper and the current
`require_from_manifest` dependency seam.
Every original assertion is preserved; production behavior, mathematical source and the
192 MiB cap are unchanged.

The three affected modules pass 58 controls in 102.89 seconds, with one known-cap
production-clone test deselected.
Ruff, formatting, BasedPyright and the owned diff check pass.
This is a selected fixture qualification, not a complete suite or gate.
Fresh required CI must qualify the published repair; the source-copy resource decision
and complete research checkpoint remain open.

The standalone source review now has exact-head
[A — senior](https://github.com/jlevy/squares/pull/464#pullrequestreview-5465603134) and
[B — correctness](https://github.com/jlevy/squares/pull/464#pullrequestreview-5465604337)
passes for content and mathematics, with A1 retaining its failed required-CI and full
qualification hold.
The same Astra reviewer performs two distinct passes independently of
the author. Its scoped weighted-screen result updates #454’s earlier unconditional
no-ball order-2 pilot, with that earlier sequence preserved as history.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
