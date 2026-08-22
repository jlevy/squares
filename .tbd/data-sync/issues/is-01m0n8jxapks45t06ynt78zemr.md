---
type: is
id: is-01m0n8jxapks45t06ynt78zemr
title: Protect the paper archive from reformatting
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n8jv4yts3mwdptj15b4gar
created_at: 2026-08-22T17:34:06.678Z
updated_at: 2026-08-22T17:39:00.753Z
closed_at: 2026-08-22T17:39:00.752Z
close_reason: "Added .flowmarkignore excluding resources/papers, resources/web (verbatim source and archival transcription) and .agents/skills, .claude/skills (generated, DO-NOT-EDIT). Verified: discovery drops from 37 files to 3."
---
The .raw.md extractions are ground truth and the cleaned paper transcriptions are archival; neither should be reflowed. Add a .flowmarkignore covering resources/ (or the appropriate subpaths) and verify flowmark honours it.
