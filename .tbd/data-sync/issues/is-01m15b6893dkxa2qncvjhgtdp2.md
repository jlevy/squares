---
type: is
id: is-01m15b6893dkxa2qncvjhgtdp2
title: Give every declared path in the record one meaning
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T23:27:28.547Z
updated_at: 2026-08-28T23:27:31.064Z
closed_at: 2026-08-28T23:27:31.063Z
close_reason: Landed in the reorg branch
resolution: null
duplicate_of: null
---
defects.yaml recorded_in, the document map, the logbook pipeline changes and DECLARED_CONSUMERS all meant 'relative to packing/'. Make them all repository-relative and resolve every checker against the repository root, rather than teaching each one a two-root fallback.

Exclude AGENTS.md and CLAUDE.md from the durable-document map: both are assembled by installers, so neither carries the guideline footer, and neither is ours to edit.
