---
type: is
id: is-01m2yn3txpz3vav8ys6kw7ek8d
title: Add a bounded stage-cost preflight before expensive research launches
kind: task
status: open
priority: 2
version: 1
labels:
  - pipeline
  - focus-efficiency
dependencies: []
parent_id: is-01m2ymyxppsc63e2m2jd9w24hs
created_at: 2026-09-20T05:37:37.717Z
updated_at: 2026-09-20T05:37:37.717Z
---
Session139 exp161 spent about three hours encoding Route S and never reached search. Add the smallest reusable preflight/receipt extension to the existing runner: distinguish setup/encoding, search and verification stages; record observed work, elapsed time, memory where measurable, input scale and remaining stage budgets; support an explicit encode-only preflight without silently launching search. Use a small known-answer fixture or bounded pilot and state uncertainty when extrapolating; unknown cost is not a zero estimate. Preserve checkpoints and diagnostics on stage stop, and classify a stopped stage as unresolved rather than scientific failure. Acceptance: controls show that expensive launch can be refused/deferred before consuming the whole intended search budget, stage completion is reported truthfully, and resume retains source/configuration identity. This block builds and validates the instrument only, not a new Route S search or a new scientific result. It is distinct from think-kmn2, whose older scope prices whole queues for 8h/24h launch horizons; do not revive that broader campaign or duplicate its queue model.
