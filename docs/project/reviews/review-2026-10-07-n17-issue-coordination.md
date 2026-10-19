---
title: n17 Issue Coordination and Certificate Intake
date: 2026-10-07
status: reviewed
---
# n17 Issue Coordination and Certificate Intake

The October 7 inventory contains 31 issues, seven directly relevant to the n17 proof
effort. Their obligations remain distinct.
The global proof in [#405](https://github.com/jlevy/squares/issues/405) remains open;
the admitted census has 60 entries, 36,768 states and 4,683 D4 orbits, including 95
unresolved distance-two orbits.
No contribution below has been newly admitted by this review.
The
[W3 route review](../research/research-2026-10-07-n17-w3-capacity-and-route-selection.md)
separates exclusions, conditional terminals and global coverage.

## Issue Dispositions

| Issue | Evidence and Remaining Obligation | Coordination |
| --- | --- | --- |
| [#413](https://github.com/jlevy/squares/issues/413) | The contributor reports 27 patterns: 17 verified and ten computed. Only rows 1–4 have reported upstream full verification; thirteen use the contributor’s faster verifier alone. | Request complete packages for rows 1–4 first, then perform full replay and ordinary admission. Keep the tracker open. |
| [#358](https://github.com/jlevy/squares/issues/358) | Two specific arity-seven BB classes have reported full standing PASS, hosted manifests and independent Rust checks. The upstream acknowledgment explicitly holds them unassessed. | Intake these two instances separately; link to #413 after exact named-cell/D4 comparison. Keep separate until class and receipt custody are joined. |
| [#367](https://github.com/jlevy/squares/issues/367) | B2/B2d changes producer branching; the same certificate format and full standing checker decide acceptance. | Review the producer separately from certificate admission. Its feasible six-cell example differs from #413 row 3, which also includes `interior-S`; there is no contradiction. |
| [#400](https://github.com/jlevy/squares/issues/400) | The original proposal accelerates BB/v1 verification. Its follow-up points to a separate kernel-verifier PR. | Keep format, checker and benchmark populations explicit; do not transfer timings or receipt compatibility between formats. |
| [#411](https://github.com/jlevy/squares/issues/411) | Repository relocation preserves old repositories and pinned downloads, with movement manifests. | Update discovery links as needed while preserving historical evidence and content identities. This is metadata maintenance. |
| [#308](https://github.com/jlevy/squares/issues/308) | Closed: the published unavoidable-set argument was independently checked and its defect recorded. | Preserve the disposition. Any new hitting-set claim needs complete closed pose coverage; this issue supplies no replacement n17 bound. |
| [#405](https://github.com/jlevy/squares/issues/405) | Overall optimality, independently reviewable proof and exposition remain outstanding. | Publish scoped progress and crosslinks here; regional certificates and relaxation witnesses do not close the global obligation. |

No duplicate closure is justified by this inventory.
Sharing a proof goal, or one pattern occurring within another, does not establish
identical remaining obligations.

The subsequent #358 metadata intake fetched both compressed manifests from
[b2-classes-20261005](https://github.com/wand125/n17-certificates/releases/tag/b2-classes-20261005)
and matched their published compressed hashes and canonical manifest identities.
The release contains 552 objects totaling 399,775,835 compressed bytes.
C1 and C2 have exact named-cell D4 masks 5177392 and 5177424; neither equals a currently
admitted class. Smaller-pattern subsumption and marginal census coverage remain
uncomputed. Complete tree replay and the shifted closed angle-chart join remain
unperformed, and retained full receipts were requested in
[the intake update](https://github.com/jlevy/squares/issues/358#issuecomment-6047235741).
No new admission follows from this metadata comparison.

The
[#413 package request](https://github.com/jlevy/squares/issues/413#issuecomment-6047161738)
starts with its four reported full-verified rows.
The
[#405 progress checkpoint](https://github.com/jlevy/squares/issues/405#issuecomment-6047179993)
consolidates the scoped exact results and unchanged global census.

## Pull Request Integration

[PR #410](https://github.com/jlevy/squares/pull/410) adds an independent Rust **kernel**
verifier, distinct from #400’s original BB verifier.
Review complete standing-receipt parity and refusal controls before adoption.
At its reviewed head, the CLI has no centered-cap option and compression is limited to
16 vertices. It cannot replay our numeric-cap/hull-48 parent as-is.
Ordinary-U Tail A/B parity would be a useful first control; centered support needs a
separate reviewed contract.
The seven reported certificates do not establish these joins.
The declared two-hull owner list also deserves a custody review.
[#408](https://github.com/jlevy/squares/pull/408) concerns H258 prerequisite replay,
[#409](https://github.com/jlevy/squares/pull/409) selected exact/dyadic interval
profiling, and [#407](https://github.com/jlevy/squares/pull/407) Darwin current-RSS
controls. Each retains its own acceptance evidence.

Merged [#412](https://github.com/jlevy/squares/pull/412) contributes the n11 paper
review. Merged [#415](https://github.com/jlevy/squares/pull/415) registers reported
SQUISH upper bounds; merged [#416](https://github.com/jlevy/squares/pull/416) adds
complete exact rational checks for eleven packings.
These merged changes belong in the integration baseline, without implying n17 proof
progress.

## Potential Metadata Join

Existing `census_n17_certified.class_mask` resolves exact cell names into the declared
cover’s D4 class; `removal` tests which retained states contain any D4 image.
These APIs could compare all 27 reported patterns with the 60 admitted classes and both
the 95-orbit subset and complete 4,683-orbit residue.
A join must retain the census identity, frame/cap, exact names and per-pattern evidence
status.
It is a potential metadata projection only: no such coverage counts were computed
here, and no pattern is admitted by matching its names.

Each intake package needs immutable certificate objects, hosting manifest, exact
frame/cap and named cells, canonical identities, complete verification receipts and
producer recipe. Declare the full closed independent-angle domain, boundary-contact
convention and any narrower flags or guards; discharge them before unconditional
admission. Begin with the four full-verified #413 packages; reconcile #358 through the
same interface.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
