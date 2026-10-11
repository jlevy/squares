---
type: is
id: is-01m4d0c2cd9rvtd1jp29pn0wf0
title: "n17: diagnose repeated sampled resource-guard process-query interruptions"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-08T05:39:25.705Z
updated_at: 2026-10-08T05:39:25.705Z
---
# Repair the sampled resource guard without weakening refusal

Session186 has two actual incomplete stops associated with the one-second global
process query: exp298 after 738.166 seconds (six of eight timed phases completed) and
exp311 after 480.468 seconds (no FULL receipt). Both must remain incomplete. No
mathematical payload or performance gain follows from their partial work.

Inspect the retained `supervise_posix` contract and process sampling implementation.
Select a bounded, source-reviewed approach that reduces host-wide enumeration cost
while preserving owned-group discovery, per-live-process current RSS accounting,
wall ceilings, fail-closed refusal on unavailable inspection, and verified cleanup.
Do not increase a timeout, omit descendants, accept an absent measurement, or silently
change the memory accounting scope. Keep any contract change separately reviewable.

Use deterministic fault controls for delayed/unavailable sampling and owned descendant
cleanup, and a prospectively registered same-object performance comparison if a gain
is claimed. Synthetic controls alone do not prove a production speedup. Preserve
original logs and journals; a future resumed scientific replay needs its own reviewed
prospective contract and identical input custody.

Evidence: Session186 performance review, exp298 and exp311 result directories,
and `packing/devtools/supervise_posix.py`. This mechanical work supports the proof
loop beside the shared-centre LP; it does not outrank mathematical progress.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
