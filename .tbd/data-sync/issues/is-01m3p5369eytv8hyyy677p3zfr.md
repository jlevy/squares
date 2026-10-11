---
type: is
id: is-01m3p5369eytv8hyyy677p3zfr
title: "Math group 2: renderers of generated documents, outputs regenerated"
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T08:39:25.742Z
updated_at: 2026-09-30T19:52:35.648Z
---

## Notes

Reviewed design: this changes files under packing/frontier/ that DATA_EXCLUDED does not exclude, so it is a data commit followed by the DATA_REVISION re-pin and atlas re-stamp.

Audit 2026-09-30: not done on either branch. claude/overview-page-impl has no renderer migration, and branch B's ledger skips generated blocks until this group.
