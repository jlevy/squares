---
type: is
id: is-01m5k8wh4tmn5xret1ksd04yah
title: Review narrow breadcrumb reflow during sans font loading
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T02:19:22.137Z
updated_at: 2026-10-23T04:17:28.943Z
started_at: 2026-10-23T03:44:43.497Z
closed_at: 2026-10-23T04:17:28.942Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Reproduced a 29.265625px T-037 article shift at 390px with Source Sans delayed. Deep narrow breadcrumb trails now give the current page its own row without changing header-track alignment. The focused delayed-font regression passed at 320, 390, 640, 641, and 1280px, including absolute article position on narrow screens. Implementation complete; no hosted CI or deployment claim.
resolution: null
duplicate_of: null
---
At390px with Source Sans intentionally delayed, result T037 title height remains stable but page-level navigation changes article vertical position by29px. Review shared breadcrumb/font fallback stability separately; result title test now measures relative geometry correctly. Followup after navigation stabilization.
