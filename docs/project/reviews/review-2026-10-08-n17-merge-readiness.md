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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
