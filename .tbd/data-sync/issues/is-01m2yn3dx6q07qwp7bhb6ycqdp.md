---
type: is
id: is-01m2yn3dx6q07qwp7bhb6ycqdp
title: Make session closeout validate, render and check in one repeatable operation
kind: task
status: open
priority: 1
version: 2
labels:
  - pipeline
  - correctness
dependencies: []
parent_id: is-01m2ymyxppsc63e2m2jd9w24hs
created_at: 2026-09-20T05:37:24.388Z
updated_at: 2026-09-20T05:38:46.912Z
---
Bounded W7 closeout slice from Session142. Extend existing close_session/record-rendering entry points with a preview/check path for the complete intended update. Validate authoritative source records before requiring generated views to be current; then invoke the owning renderers in a fixed dependency order and run their drift/semantic checks. Cover terminal session and canonical gate declaration, ledger, agenda map when applicable, result/frontier views when affected, defects, synopsis status/handoff and cost views. Consume scientific-state contracts from think-7ec6 and source-derived aggregates/provenance from existing think-y9wk; do not duplicate either implementation. Do not infer scientific conclusions, invent clocks, advance assurance, or attribute an old gate to a new revision. Acceptance: a Session142-shaped closeout needs no manual status-count or gate-string repair; failed previews leave source records intact; completed application reports partial failures honestly; rerender is byte-idempotent; --check is read-only; controls cover stale-view recovery, malformed gate declaration and missing inputs. Use existing tools and preserve historical records. Generic tooling is distinct from the paused BC329-specific reconciliation think-iexs.
