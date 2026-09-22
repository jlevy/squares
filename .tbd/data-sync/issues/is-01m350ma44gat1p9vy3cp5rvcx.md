---
type: is
id: is-01m350ma44gat1p9vy3cp5rvcx
title: Stamp the explainer, the atlas SVGs and the videos with the shared version v0.4.1-xxxxxx
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-22T16:54:18.499Z
updated_at: 2026-09-22T16:54:18.499Z
---
The owner (2026-09-22): one version across the explainer, the SVGs and the video, written v<edition>-<first six characters of the last commit that changed the evidence and data> -- sqpack.release.data_version(repo), added in the commit after c9331a316. Bump the edition to v0.4.1 through PUBLICATION_HISTORY, move the explainer's credits and the atlas footer from PUBLICATION_STAMP (v0.4.0-277f8b1a, eight characters of a pinned edition commit) to the shared version, and give the video's MP4 metadata and receipt the same string. Committed artifacts that are compared byte for byte need a design that does not chase its own commit hash; built artifacts need a clone deep enough for git to name the data commit (the deploy and CI checkouts).
