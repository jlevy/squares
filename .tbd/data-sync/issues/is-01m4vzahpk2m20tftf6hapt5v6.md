---
type: is
id: is-01m4vzahpk2m20tftf6hapt5v6
title: Escape structured changelog links before rendering Markdown
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
created_at: 2026-10-14T01:09:43.762Z
updated_at: 2026-10-14T01:09:43.762Z
---
Precommit senior review reproduced structured references/publication evidence URL ending in )<script>alert(1)</script> passing validation and emitting script HTML through kpress. Fix the structured-link serialization and URL boundary; add regression tests through site Markdown and kpress. Do not weaken the authored prose rules.
