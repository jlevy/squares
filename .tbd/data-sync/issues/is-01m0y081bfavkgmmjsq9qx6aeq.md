---
type: is
id: is-01m0y081bfavkgmmjsq9qx6aeq
title: Tier packing CI into fast Linux and selected macOS lanes
kind: feature
status: closed
priority: 0
version: 12
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies:
  - type: blocks
    target: is-01m0y083cqkdjbbzfjxc5j7wpd
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
child_order_hints:
  - is-01m0ycwz9g10ckxpgghd62z2qf
created_at: 2026-08-26T03:01:31.629Z
updated_at: 2026-09-16T00:19:54.755Z
closed_at: 2026-09-16T00:19:54.754Z
close_reason: |
  Superseded. The tier split this bead specified landed on 2026-09-05/06 as five concurrent pull-request jobs (think-doar, think-m5ev); its 60 s p50 go criterion was never completed and is replaced by OR-14's 120-150 s target with a 180 s budget enforced on every pull request by packing/devtools/check_pr_wall.py (think-z121). The standing 288 s wall regression is owned by think-xfqk.
resolution: null
duplicate_of: null
---
Shorten the required packing pull-request signal while retaining complete assurance at declared integration boundaries. Acceptance: a required Linux fast lane publishes structured timing; the optimized full Linux lane remains visible and required at the integration boundary and on main; macOS runs named portability consumers on main, scheduled, manual, and explicit portability-sensitive triggers instead of duplicating the full gate on every unrelated PR; every invoked macOS check remains direct and blocking; workflow-contract tests cover triggers, commands, artifacts, and failure semantics; before/after p50 and p95 are retained.

## Notes

Second hosted sample on final docs SHA b7e1a13: run 32942841231 passed in 65s end-to-end; validate 54s, required step 38s, aggregator 5s, macOS skipped. First two samples are 46s and 65s (midpoint 55.5s), both below 75s p95 budget; continue to ten samples.

Operational policy (2026-08-26): macOS portability checks are asynchronous and nonblocking with respect to active research. Once invoked on a declared integration, main, scheduled, manual, or explicitly portability-sensitive surface, the check must report its own failure directly, but the coordinator must not idle, hold a research slice open, or delay further experiments while waiting for it. Continue independent read-only or disjoint-write work in parallel and reconcile the macOS result at the next bounded checkpoint. Implement any workflow or trigger changes within this W5 performance cycle while preserving the assurance contract.


2026-09-15 (think-xfqk, think-z121): closing as superseded. This has been in progress since 2026-08-26 against a go criterion -- a 60 s pull-request p50 over ten samples -- that was never finished and is no longer the target. The tiering it was heading toward landed on 2026-09-05/06 as five concurrent pull-request jobs in `.github/workflows/packing-validation.yml` (think-doar for the surface split, think-m5ev for the parallel jobs), so the acceptance criteria above are met by work that landed elsewhere. What replaces the criterion: the 2026-09-15 CI review measured the required pull-request wall at 288 s, the median of 21 runs, against 154 s on 2026-09-06, and the target is now OR-14's 120-150 s with a 180 s budget and a 1.2x regression rule enforced on every pull request by `packing/devtools/check_pr_wall.py`. The remaining wall work sits under think-xfqk and its lanes, not here.
