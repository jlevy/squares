---
type: is
id: is-01m4ks763ymj0a4hzgz6e5cep9
title: Reclaim inactive build artifacts during polynomial PR stabilization
kind: chore
status: closed
priority: 1
version: 4
delegate: codex-polynomial-resume-01a11d93
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-10T20:49:06.673Z
updated_at: 2026-10-10T21:18:08.744Z
started_at: 2026-10-10T20:49:18.531Z
closed_at: 2026-10-10T21:18:08.650Z
close_reason: Removed 15 verified inactive private source-copy leaves; preserved unique diagnostics and kept all active or uncertain artifacts.
resolution: null
duplicate_of: null
---
Audit the polynomial task, registered worktrees, and both macOS temporary roots while internal Data and spud-ext1 are near capacity. Preserve source, local commits, active tasks, runtime bundles, research and release evidence, and agent history. Verify generated artifacts against manifests and live/task ownership, stage eligible exact paths only with trash, record source and actual Trash destinations and physical free space, and keep Trash unemptied for owner review. Disk-heavy local gates remain paused until capacity is restored. Coordination: existing 30-minute cleanup audit chat remains active; avoid overlapping mutations.

## Notes

Careful permanent cleanup completed 2026-10-10T21:18:08.020313+00:00 under the user's explicit instruction to rm eligible artifacts immediately. Removed exactly 15 inactive, generated private source-copy leaves from two completed local pytest runs; no whole test parents or worktrees were removed. Eligibility checks matched indexed regular source files against retained Git content, checked no private refs/commits/unknown objects and no open handles, and preserved every unique diagnostic before removal. The 15 leaves accounted for 4,570,116,096 allocated bytes (4.26 GiB) and 4,092,782,284 apparent bytes. Four byte-identical mutant instances, totaling 58,672 bytes, were preserved and read back outside disposable scratch; these are diagnostic instances, not four scientific inputs.

The two immediate df intervals observed about 2.73 GiB more physical free space on the external volume, ending at 4,839,924 KiB (4.62 GiB) available. Concurrent writers, APFS allocation and other cleanup mean this physical change cannot be attributed wholly to this deletion batch. A later sample at 21:12:18Z was 4,799,160 KiB (4.58 GiB); the internal volume was 6,377,064 KiB (6.08 GiB) available. Do not equate allocated bytes removed with physical bytes reclaimed.

Kept both active polynomial source worktrees, the primary n17 checkout, the live preview, shared environments and dependency/link targets, all logs and unique research/release evidence, and ambiguous test artifacts. Task Cargo targets were empty. A bounded follow-up of the completed child2bd8 scratch established no further disposable leaf above 100 MiB; uncertain artifacts remain. Broad local validation is paused while the external volume is this constrained; small report checks and hosted CI can continue. This bead closes the verified cleanup batch, not a global disk audit or the polynomial qualification work.

Evidence: /Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-2026-10-10-1715/older20261009-source-copy-permanent-cleanup.json; olderbase-source-copy-permanent-cleanup.json; independent-older20261009-source-copy-eligibility.json; independent-olderbase-source-copy-eligibility.json; independent-child2bd8-bounded-scratch-followup.json. The guarded fixed-batch remover is retained as remove-verified-private-source-copies.py; its completed batches must not be rerun against missing leaves. Further cleanup requires fresh ownership, inactivity and recoverability checks.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
