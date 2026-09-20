---
type: is
id: is-01m2yn3dx6q07qwp7bhb6ycqdp
title: Make session closeout validate, render and check in one repeatable operation
kind: task
status: open
priority: 1
version: 4
labels:
  - pipeline
  - correctness
dependencies: []
parent_id: is-01m2ymyxppsc63e2m2jd9w24hs
created_at: 2026-09-20T05:37:24.388Z
updated_at: 2026-09-20T07:11:55.165Z
---
Bounded W7 closeout slice from Session142. Extend existing close_session/record-rendering entry points with a preview/check path for the complete intended update. Validate authoritative source records before requiring generated views to be current; then invoke the owning renderers in a fixed dependency order and run their drift/semantic checks. Cover terminal session and canonical gate declaration, ledger, agenda map when applicable, result/frontier views when affected, defects, synopsis status/handoff and cost views. Consume scientific-state contracts from think-7ec6 and source-derived aggregates/provenance from existing think-y9wk; do not duplicate either implementation. Do not infer scientific conclusions, invent clocks, advance assurance, or attribute an old gate to a new revision. Acceptance: a Session142-shaped closeout needs no manual status-count or gate-string repair; failed previews leave source records intact; completed application reports partial failures honestly; rerender is byte-idempotent; --check is read-only; controls cover stale-view recovery, malformed gate declaration and missing inputs. Use existing tools and preserve historical records. Generic tooling is distinct from the paused BC329-specific reconciliation think-iexs. Owner clarification: make the existing New Result Publication runbook (packing/campaign/documentation-pass.md) part of closeout. For newly retained results, require README and survey reconciliation, result/frontier/inventory/headline rendering, and regeneration or checked-current disposition for both survey composite families (SVG, PDF and PNG). Consume existing result-ID/label/export checks and record editorial coverage; do not rebuild unchanged geometry automatically. Add a control for a registered result missing from publication and for a stale survey export. The immediate audit and narrow omission guard are owned by think-kq00; this bead owns their orchestration.

## Notes

Landing audit identified a bounded receipt-consumption requirement: existing checkpoint_manifest only archives bytes, check_pr_wall checks timing, and wait_for_run_artifact checks availability. Closeout must also reject incomplete or failed step unions and wrong checkout revisions. Use receipt top-level commit (not workflow dispatch headSha or environment.GITHUB_SHA), match final PR head/base via merge parents/tree, require each run selected_steps to equal its passing step receipts, and compare Linux fast plus deferred union with packing-validate --list. Check macOS portability and Pages separately. Retain controls for skipped deferred jobs, missing/duplicate steps, failed outcomes, stale source/base and mixed rerun attempts; reuse existing receipt contracts without a second validation framework.
