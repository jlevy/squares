---
type: is
id: is-01m4t1y0xye322ehz1p8pts800
title: "move_documents: case-only renames, and reports for bare basenames, blob/main links and AGENTS.md, CLAUDE.md and dot-directory references"
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-11-documentation-organization.md
labels: []
dependencies: []
parent_id: is-01m4s66qs6ep9c3jycyamqgmf2
created_at: 2026-10-13T07:16:50.238Z
updated_at: 2026-10-13T07:17:20.594Z
---
The rest of slice 0's mover contract in docs/project/specs/active/plan-2026-10-11-documentation-organization.md, deferred from PR #579 review B finding B2 (https://github.com/jlevy/squares/pull/579#pullrequestreview-5499824274). #579 ships devtools.move_documents with whole-list validation, atomic apply, content-based text detection, a sorted math-markup.yaml, fenced code and footnotes left alone, and reports for paths left in fenced code and in files that are not text. Remaining: (1) a two-step git mv for a case-only rename, whose target-exists check refuses it on a case-insensitive filesystem; (2) a report of what the mover should not decide alone: the bare basename mentions and absolute github.com/jlevy/squares/blob/main/ links it leaves, and the references it rewrites in AGENTS.md, CLAUDE.md and dot-directories. Waits on slices 2 to 5 of the plan (think-xz7z), its first users.
