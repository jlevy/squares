# Bead Reconciliation, Lane A — 2026-10-10

## Scope and method

This lane covers all 486 nonclosed beads and all 27 specifications assigned to lane A in
the retained `review-2026-10-10-bead-reconciliation-baseline.json` scope.
I compared that scope with fresh `tbd show --json` records and the full tracker listing
on 2026-10-10; the companion JSON retains the current version, status, and delegate
returned for every proposed mutation and records the observed parent and child counts.
For specification lifecycle decisions, I also normalized the removed
`explorations/packing/` prefix and checked IDs named in each specification body, so
stale links count as prior or current implementation.
The review proposes no `tbd` writes.
It does not infer completion from age, a closed child set, or a missing delegate in the
list snapshot.

The machine-readable companion contains one explicit disposition for every assigned ID.
Its bead counts are: **4 close**, **40 metadata update**, **246 retain**, and **196
needs evidence**. The specification counts are: **2 move_archive**, **3 move_done**, **1
move_draft**, **3 needs_evidence**, **15 retain**, **3 update_status**.

Only one bead changed status between the inventory and the fresh show: `think-1a9o`
moved from `open` to `in_progress` at version 2. It is retained as current
reconciliation work.
Before each mutation, the coordinator should fresh-read and compare the bead with the
`expected_version` and `expected_status` attached to the proposal.
This pre-update version check has a concurrency limit: `tbd update` has no
`--expected-version` guard, so a concurrent write can still race the check and update.

## Supported bead mutations

Four closures have direct completion or merged-delivery evidence:

| Bead | Disposition | Evidence |
| --- | --- | --- |
| `think-giqi` | Close policy decision | OR-18 and hosted-data handling landed in merged PRs [#347](https://github.com/jlevy/squares/pull/347) and [#349](https://github.com/jlevy/squares/pull/349); enforcement remains `think-h8d8`. |
| `think-5o8i` | Close sizing decision | Retained JSON and page caps landed in merged PR [#323](https://github.com/jlevy/squares/pull/323). |
| `think-ele8` | Close delivered audit | Audit and OR-16 landed in PR #347; `think-gzju` owns the remaining slice. |
| `think-6l39` | Close completed decision | The record names `think-os9k` as the implementation successor. |

The 40 metadata updates repair `spec_path` from removed `explorations/packing/...`
locations to an existing same-filename file.
Each update carries its fresh expected version and status.
No fuzzy path match is proposed.
The `think-23td` update also proposes `hold=paused`: its notes say Phase 1 is complete
and Phase 2 is intentionally paused pending an amended spec and independent controls.

## Retained and uncertain scope

The 246 retained beads have observable live or governing scope: an `in_progress` or
`deferred` status, a nonclosed parent or child, a declared dependency, or an existing
governing document. Seven parents with all children closed remain open because their own
records still name remaining scope: `think-4o6l`, `think-2w1a`, `think-1q3g`,
`think-d4hm`, `think-gvlg`, `think-be1s`, and `think-190a`.

The 196 `needs_evidence` entries are intentionally nonmutating.
They either point to an absent governing path without a unique same-filename
replacement, or are open leaves with no existing governing path, active child,
dependency, completion receipt, or explicit successor.
Each entry names the missing decision or receipt.
`think-fh5n` remains in this conservative group because its tested Mach alternative
overlaps active, unmerged PR #404; consolidation evidence is required before closure.
`think-00e3` needs the n17 owner’s choice between closure and taking the exact form as
its scope.
`think-geid` needs the owner review that its negative-result note names before
retirement. `think-3hw2` delivered a draft and controls, but its record disclaims
production adoption and contains no acceptance disposition.
`think-0fkt` also stays open because T-097 still names the complete producer-checker
replay as an optional next rung.
The verified result no longer waits on the replay, but the record does not say that
optional deliverable was completed or canceled.

## Specification disposition

| Action | Specifications |
| --- | --- |
| Move to archive | superseded n11 overnight three-block plan; historical BC329 three-profile run sheet that never ran |
| Move to done | deterministic SVG toolkit; site URLs/SEO/performance; n5 motion-lab spike |
| Move to draft | interval certification |
| Update status | minimal packing toolkit to Active; promotion pipeline to Active; measure verifier milestone C to Active |
| Needs evidence | gate validation speed; video delivery profiles; epistemics ladder review |
| Retain | the remaining fifteen assigned specifications |

Moves are proposals for the coordinator because inbound links must be repaired with
them. The companion JSON records the path-level reason and evidence for all 27
specifications.

## Limits

This is a repository and tracker snapshot, not an execution transcript.
It can establish recorded ownership, status, merged delivery, parent/child state, and
governing-path validity.
It cannot prove that an unrecorded duplicate execution did or did not happen, and it
cannot prove synchronization between replicas from one fresh snapshot.
Missing delegate data is treated as unknown because the list inventory may omit it; no
ownership conclusion relies on that field.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
