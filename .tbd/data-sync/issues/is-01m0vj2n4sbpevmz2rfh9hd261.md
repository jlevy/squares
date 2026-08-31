---
type: is
id: is-01m0vj2n4sbpevmz2rfh9hd261
title: "PR #23 review R13: Make list honor fast and only selection"
kind: bug
status: closed
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:26.361Z
updated_at: 2026-08-25T04:44:39.286Z
started_at: 2026-08-25T04:16:15.525Z
closed_at: 2026-08-25T04:44:39.285Z
close_reason: "Completed in 69e65eb: --list now uses the same --fast and --only selection path as execution, with regression coverage."
resolution: null
duplicate_of: null
---
PR 23 review R13. File: explorations/packing/src/sqpack/cli/validate.py lines 856-863. Route list output through the same selection logic as execution and test fast, matched, and unmatched cases.
