---
type: is
id: is-01m4xkf4v65pthd9zbd7a5a3qv
title: Redesign CI around a three-minute default gate and explicit deeper validation
kind: feature
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m4xkmdn3wbb62yx8wjtc5ec4
  - is-01m4y1bk4xqtpbjc6ppar1abj7
  - is-01m4y1d2r15w1pc4xpakvwaqfn
  - is-01m4y3k8x8386gz568dw7fb138
hold: null
hold_until: null
created_at: 2026-10-14T16:21:00.389Z
updated_at: 2026-10-14T21:02:52.839Z
started_at: 2026-10-14T16:21:26.412Z
---
User explicitly requests Astra analysis and a systematic fix for repeated hours of CI iterations. Target typical default PR CI around three minutes; retain expensive tests in clearly selected deeper, checkpoint or scheduled lanes without blocking every development iteration. Audit actual validation/workflow costs, require each addition to account for recurring forward cost, define affected-input selection and evidence reuse with fail-closed assurance, document clear running policy and implement reviewed slices. Current PR599 timing repairs and atlas-width delivery continue separately.
