# Session186 storage disposition

This is a focused audit of this session’s own scratch.
It does not account for all storage on the Mac or external volume.
Only `trash` was used to remove eligible scratch from its original location; Trash
remains unemptied.

Two completed test fixtures were staged at the 04:48 UTC boundary:

| Original path | Allocated size | Verified Trash destination |
| --- | ---: | --- |
| `/Volumes/spud-ext1/agent-scratch/n17-six-hour-01a114fb/tmp/pytest-of-levy/pytest-19` | 499,056 KiB | `/Volumes/spud-ext1/.Trashes/502/pytest-19` |
| `/Volumes/spud-ext1/agent-scratch/n17-six-hour-01a114fb/tmp/main-merge-focused/control-snapshot0` | 300,088 KiB | `/Volumes/spud-ext1/.Trashes/502/control-snapshot0` |

Both exact directories had no open handles or inspection warnings in bounded `lsof
+D` checks. The pytest fixtures are recreated by their existing tests.
The control snapshot is recreated by `control_snapshot` and its tree/index builder; its
private Git repository had no commits or remotes.
Unique logs, JUnit, source and primary research evidence were retained separately.
`trash -v` completed successfully, and `trash -lv` verified both destinations and the
absence of both original paths.

Earlier eligible scratch from this session comprised the inactive root Ruff cache (24
KiB), the completed two-child test fixture (about 23 MiB), and three completed
phase-reconciliation, rank-filter and corner-cardinality test fixtures (about 12 MiB).
Each was checked for ownership, reproducibility and inactivity before staging.

The shared Python environment, recovery Cargo target, active caches, registered
worktrees, agent history, public C2 input cache and all unique receipts remain in place.
An additional 384 KiB synthetic-test fixture was identified at the final boundary but
was not staged. Large aggregate scans and one broad activity inspection exceeded their
ceilings; their coverage remains incomplete.

At 04:37:33 UTC, physical availability was 152,008 KiB internally and 433,088 KiB on the
external volume. A later 05:30 observation was 1,098,068 KiB and 721,512 KiB. Concurrent
writers and cleanup elsewhere prevent attributing that change to this session.
Moving files to Trash on the same volume does not free their allocated space.
No physical-space gain is claimed.

Disk exhaustion caused actual temporary-file failures and prevented the planned full
checkpoint from starting before its latest safe start.
The checkpoint remains unlaunched, with explicit certification debt.
The user was asked to review and empty Trash or restore working space; no answer had
arrived by this audit boundary.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
