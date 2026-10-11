---
type: is
id: is-01m4eheqhy4hjmn7khpc5wk85z
title: "PR #456 review E2: cover native math in preview font-probe Node fixtures"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4edy0gkgv91t6evhbzeyk58
hold: null
hold_until: null
created_at: 2026-10-08T19:57:13.148Z
updated_at: 2026-10-08T21:37:25.856Z
started_at: 2026-10-08T19:59:13.722Z
closed_at: 2026-10-08T21:37:25.855Z
close_reason: Fixed in e047331e5ef17d6590ebd36d7c1b8aa4e0441372. DOM stand-in implements getAttribute; four original KaTeX controls preserved and focused Node file7/7 passes. Complete local browser floor/liveness and final-head hosted validate/type floor pass. Independent Astra ReviewE5463107477 and disposition6069502067 confirm repair.
resolution: null
duplicate_of: null
---
Combined push-floor browser-floor command failed four retained preview_site/math-face.test.mjs cases because old DOM stand-ins lack getAttribute required by the native-math probe. Update stand-ins with correct null attribute semantics, preserve all KaTeX controls, add actual-token custom/system positive and wrong-face native controls. Author patch prepared outside frozen source; apply after active floor then rerun affected Node program/language floor. Retain aggregate failure; production probe/guard unchanged.
