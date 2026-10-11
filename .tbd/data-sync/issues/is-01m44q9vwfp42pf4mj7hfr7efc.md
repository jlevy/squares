---
type: is
id: is-01m44q9vwfp42pf4mj7hfr7efc
title: "PR #333 A1 (High): the OR-16 integrity ratchet is bypassed."
kind: task
status: closed
priority: 2
version: 3
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44q9st2e0jh0h0cztp6hnv8
hold: null
hold_until: null
created_at: 2026-10-05T00:27:00.878Z
updated_at: 2026-10-05T02:28:57.528Z
started_at: 2026-10-05T00:54:30.323Z
closed_at: 2026-10-05T02:28:57.527Z
close_reason: Review A delivered in PR333/351/352; focused controls and source/pages gates pass; inherited parent merge conflict explicitly tracked by open think-q0z7, no active executor or reserved follow-up.
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/333#pullrequestreview-5408660716

**A1 (High): the OR-16 integrity ratchet is bypassed.**
- `packing/devtools/integrity-ceremony.yaml:28-51` adds 8 allowlist entries of kind `generated-artifact`, which the file defines as "a build product no Git revision names". It also says "There is no kind for a file this repository wrote".
- All 14 SHA-256 constants pinned in the probes are hashes of receipts this PR commits to Git:
  - `probe_n17_cached_collision.py:36-37`
  - `probe_n17_enhanced_row_support.py:49-50`
  - `probe_n17_scheduled_row_support.py:30-35`
  - `probe_n17_full_core_ablation.py:60-68`
  - `probe_n17_selective_halving.py:42-44`
- `probe_n17_raw_row_support.py:77` binds `input_identity` to a digest of the whole cold-check receipt, enforced at `:406`.
- Reproduced: regenerate B, run a fresh cold check with identical seed and node SHAs, then follow the README replay. It refuses with "seed input identity differs", and works only with the committed receipt.
- **Fix:**
  - Identify committed receipts by path and revision, and compare their content.
  - Bind inputs only to the seed/node content SHAs.
  - Drop the pins, and keep allowlist entries only for residual_graph and raw_row, whose seed/node checks are legitimate.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
