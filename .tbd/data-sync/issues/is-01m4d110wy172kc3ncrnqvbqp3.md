---
type: is
id: is-01m4d110wy172kc3ncrnqvbqp3
title: "n17: gate PR410 native verifier and establish ordinary-U full parity before adoption"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-07-n17-pr410-integration.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m4d2mbv5at5v053xsp9s68tg
created_at: 2026-10-08T05:50:52.317Z
updated_at: 2026-10-08T06:18:54.691Z
---
---
title: PR410 Integration Review for the n17 Continuation
date: 2026-10-07
status: reviewed
---
# PR410 Integration Review for the n17 Continuation

[PR410](https://github.com/jlevy/squares/pull/410) has been considered in the n17 plans,
but its Rust verifier has not been adopted or independently replayed here.
The current source still verifies the ordinary container with owned hulls capped at 16
vertices; it cannot replace the centered-container, hull-48 replay used by the numeric
parent.
Its potential value justifies a bounded ordinary-container parity pilot after the
outstanding source and evidence checks below.

This review inspected head
[`763ecd3bae4be5ccca55fdd626d3f43b38897216`](https://github.com/jlevy/squares/pull/410/commits/763ecd3bae4be5ccca55fdd626d3f43b38897216),
the PR body, comments, review state, changed-file inventory, current Rust source and
failed CI log. It did not download the 215 MB certificate bundle, build the crate,
execute its tests or replay certificates.

## What Is Already Incorporated

The
[issue coordination review](review-2026-10-07-n17-issue-coordination.md#pull-request-integration)
correctly distinguishes PR410’s kernel verifier from #400’s original BB verifier.
It proposes ordinary-U Tail A/B parity before centered support, and records the declared
two-hull owner-list custody concern.
The
[Session186 W3 strategy](../research/research-2026-10-07-n17-session-186-w3-strategy.md#global-completion-obligations-and-structural-alternatives)
retains the ordinary-container/hull-16 limitation; the
[continuation plan](../specs/active/plan-2026-10-07-n17-six-hour-continuation.md) keeps
verifier compatibility separate from #367’s producer branching and #358/#413 certificate
admission. These are appropriate distinctions at the current head.

The earlier Session185 source inventory inspected `6bc6f96`, so it does not establish
that the latest changes were reviewed.
The
[maintainer review](https://github.com/jlevy/squares/pull/410#issuecomment-6046714334)
requested corrections A1–A4. The
[contributor’s response](https://github.com/jlevy/squares/pull/410#issuecomment-6051481640)
and current source now supply:

- Three `owned_hulls_intersect` fixtures at 1, 2 and 4 threads, including wrong-kind and
  outside-point refusals.
- A direct zero-gap coverage control paired with positive gaps of `2^-40` and `1/1000`,
  and an exact area-subtraction comparison.
- A per-case table distinguishing 33 rejected mutations from the zero-gap positive
  coverage control, whose unchanged final state is refused later.
- Separate specifications for successful receipt equality, exact well-formed refusal
  text and malformed-input refusal prefixes, with pinned external fixture scripts.

These additions are visible in
[the tests](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/src/tests.rs#L867)
and
[TESTING.md](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/TESTING.md).
Their presence addresses the requested review documentation and control shapes;
execution and broader semantic adoption remain separate obligations.

## Current Source and Evidence Boundaries

| Question | Finding at `763ecd3` | Consequence |
| --- | --- | --- |
| Centered container | CLI has no centered-cap option. Seed ownership and legal walls use `cells.cap` with zero-offset ordinary semantics. | Supplying alternative cell JSON cannot reproduce fixed outer U, smaller inner V and offset `(U−V)/2`. |
| Compression | The accepted compressed hull has a literal limit of 16. | Hull-48 parent support requires an explicit reviewed extension. |
| Native replay | Root-node frame, all accepted rows for each cited partner, exact coverage, compression, final joins and streamed canonical EOF are implemented. Sampling is optional. | Omitted partners weaken the proof; they do not invalidate that optional-partner contract. A parity pilot must use full mode and retain complete counters and content identities. Conditional nodes are not this root-only input contract. |
| Closure metadata | The derived closure is recomputed; declared matching compares kind and `owner`, not the `owned_hulls_intersect` owner list. | Review or test that declared-owner custody separately; the new fixture does not settle a tampered owner-list case. |
| Receipt evidence | Seven seed/node identities and two crate build identities are listed; the full certificates and receipts are unpublished. | Fourteen current 1/8-thread receipts are contributor-reported, not locally observed equality. |

The capability findings follow the
[CLI](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/src/main.rs#L44),
[seed/wall checks](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/src/verify.rs#L271),
[compression limit](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/src/verify.rs#L983)
and
[closure join](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/src/verify.rs#L1224).

[PROVENANCE.md](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/PROVENANCE.md)
identifies the Python specification at `ef79288a4`, identical to `4148483da` for that
file, and declares generator independence and GMP/`rug` arithmetic.
TESTING binds seven certificates to `4148483da`, the exported cover and canonical
seed/node hashes. Its current build identity is `4ac56281…`, checked reportedly at 1/8
threads on macOS; the README timing table instead uses `71e7bb95…` at 1/16 threads on
Linux.
Those timings are neither current-head measurements nor estimates for our centered
parent.

## CI and the Next Integration Checks

At the inspected head,
[run37722203338](https://github.com/jlevy/squares/actions/runs/37722203338) fails suite
A and the required aggregate.
The
[suite A log](https://github.com/jlevy/squares/actions/runs/37722203338/job/113132206682)
shows three worker snapshot assertions: selected bytes are **201,534,502**, exceeding
the unchanged **201,326,592** cap by **207,910** bytes.
This is a concrete source selection failure, not a reported geometric refusal.
It needs dependency-aware repair with all real fixture and mutation consumers retained.
The observed CI failure does not validate the Rust implementation, and green Python CI
alone would not replace the native correctness checks.

The current
[validator’s n17 Rust gate](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/src/sqpack/cli/validate.py#L2623)
targets `n17bb_native`, not `n17_kernel_verify`; no new kernel-crate gate is wired into
that source. The PR changes no workflow or validator file.
The contributor’s reported 22 Rust tests therefore need a bounded native CI entry,
including formatting and fixture replay, before adoption; the existing n17 BB job is a
different implementation.

The next integration slice should:

1. Resolve the snapshot failure and add bounded native kernel-crate CI controls.
   Retain malformed, narrow-gap, threading, EOF and closure-owner controls.
2. Freeze a bounded full replay of already retained ordinary-U Tail A/B objects in
   Python and Rust on identical inputs; it does not require the unpublished bundle.
   Compare status, canonical IDs, full counters, closure and final-state agreement;
   sampling cannot substitute.
   Bind the exact exported or embedded 24-cell world independently of its design label
   and crate build digest:
   [build.rs](https://github.com/jlevy/squares/blob/763ecd3bae4be5ccca55fdd626d3f43b38897216/packing/n17_kernel_verify/build.rs)
   excludes `cover.json` from that digest, although seed identity binds its checked
   world. Bind compressed objects before and after, with external wall and memory guards;
   the Rust reader has no internal decoded-byte ceiling.
   Request the contributor’s seven-case bundle and inspectable receipts in parallel,
   with acquisition identities and exact comparison exclusions.
   Separate correctness from timing.
3. Only after ordinary parity, review centered U/V/offset, container receipt schema,
   hull-48 ownership/compression and refusals before a same-object numeric-parent pilot.
   Bind final-state U/B/world/mask/guard/source and the exact declared intersecting
   owner pair as part of that extension.
4. Measure any accepted implementation on the actual downstream call path before
   attributing a gain to the finite conditional consumers.

The [accepted performance profile](review-2026-10-07-n17-session-186-performance.md)
attributes 57.293 seconds to required-domain coverage and 10.218 seconds to collision
validation in one 108.237-second Python replay.
This makes kernel acceleration relevant; it does not establish that a Rust executable
accelerates the producer-free consumers, which also reconstruct geometry and custody
through Python APIs.
They need an explicit native interface or wrapper; PR410 also does not verify C2’s BB/v1
certificate or execute the proposed shared-centre LP. No PR410 speedup, new n17
admission or global bound is accepted by this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

## Notes

Astra final planning review: ordinary-U full TailA/B parity is ready to prepare in parallel with snapshot selection repair once reviewed native build/test setup, external storage, immutable input custody and bounded execution are ready. Neither the unpublished215MB corpus nor broad September rx6p redesign blocks that pilot. Adoption completion still requires current PR snapshot failure resolved, bounded kernel-native CI wired and passing, successful full parity and refusal/EOF/closure-owner controls. No current build, test, replay, speedup or assurance promotion is claimed.
