---
type: is
id: is-01m0x2aed0jatdpht3twcfrget
title: "PR #39 review S1: remove stale live counts from golden contract prose"
kind: bug
status: closed
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0x29vkahkr6ht4zx2cahh2x
created_at: 2026-08-25T18:18:33.247Z
updated_at: 2026-08-25T18:38:29.441Z
closed_at: 2026-08-25T18:38:29.441Z
close_reason: Fixed in be35a70; focused regressions, full 32-surface validation, deep-golden replay, and both required CI jobs pass.
resolution: null
duplicate_of: null
---
Non-blocking review suggestion at explorations/packing/devtools/check_golden_basins.py:12 and :28. Replace the stale five-of-seven live count and serialized-file assertion wording with invariant prose aligned with semantic YAML comparison. PR #39 review: https://github.com/jlevy/thinking-scratchpad/pull/39#pullrequestreview-5022399787
