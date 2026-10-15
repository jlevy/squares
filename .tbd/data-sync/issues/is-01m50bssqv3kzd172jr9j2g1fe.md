---
type: is
id: is-01m50bssqv3kzd172jr9j2g1fe
title: Scope News metadata and PR template changes to their native fast checks
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T18:04:44.154Z
updated_at: 2026-10-15T18:04:53.644Z
started_at: 2026-10-15T18:04:53.643Z
---
A News-only change selected all67prerequisites because packing/site-changelog.yaml and its schema have no Step.touches owner; the PR template also triggered every quick test through the blanket .github/config rule. Astra source audit confirmed both causes and current push receipt. Assign News YAML to its native schema/changelog/release/documentation validator and treat the exact Markdown PR template as prose rather than runtime CI configuration. Keep fail-closed behavior for unknown paths and actual workflow changes. Add meaningful selection controls. No newCIjob or timing-ceiling change. Validate in hosted CI while local external scratch is exhausted.
