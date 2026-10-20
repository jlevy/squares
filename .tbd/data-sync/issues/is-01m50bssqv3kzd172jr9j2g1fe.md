---
type: is
id: is-01m50bssqv3kzd172jr9j2g1fe
title: Scope News metadata and PR template changes to their native fast checks
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T18:04:44.154Z
updated_at: 2026-10-15T18:55:27.061Z
started_at: 2026-10-15T18:04:53.643Z
closed_at: 2026-10-15T18:55:27.060Z
close_reason: "Source delivery completed in PR620: reviewed head 32ffac9dd8d8756ec619e808d0d3034b58640e6d merged as 4c9af6902e517bfff7d9f50d7cd6a042a15f60ed. Exact-head ordinary Packing 38787870695 and Pages 38787870830 passed; actual JUnit confirms all 46 targeted policy/selection controls passed without skips. Final reviews O5538212826, P5538213019 and Q5538223370 have no open findings and carry unchanged earlier M/N coverage. The historical full43 aggregate remains failed on CALL timing, while its actual 241 slow-lane nodes including all five moved operations passed. Hosted policy now explicitly reports at12s and enforces45s; strict/local/enforce remain12s, and mathematical/functional/child-deadline guards remain. The bounded retrospective, safety removal, supervision, invocation-local input sharing, measured-node placement, native ownership and selection fixes are delivered; no controlled speedup or three-minute success is claimed. Post-merge publication and complete native main coverage remain OPEN and owned in think-bmix; broader measured CI program remains open in think-kxmq/think-jpto/think-h96x. Evidence retained in primary .codex/regularization-closeout-evidence-2026-10-13/."
resolution: null
duplicate_of: null
---
A News-only change selected all67prerequisites because packing/site-changelog.yaml and its schema have no Step.touches owner; the PR template also triggered every quick test through the blanket .github/config rule. Astra source audit confirmed both causes and current push receipt. Assign News YAML to its native schema/changelog/release/documentation validator and treat the exact Markdown PR template as prose rather than runtime CI configuration. Keep fail-closed behavior for unknown paths and actual workflow changes. Add meaningful selection controls. No newCIjob or timing-ceiling change. Validate in hosted CI while local external scratch is exhausted.
