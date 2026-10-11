---
type: is
id: is-01m3vk4ch39zkksjfbtyqkvhgx
title: "n = 11 paper: figure tests bind the figures' text and guards, not only the receipt hash"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T11:20:57.116Z
updated_at: 2026-10-01T11:20:57.116Z
---
From the review of jlevy/squares#261 (2026-10-01): a changed receipt refuses every figure by hash, but six mutated figure labels left the three figure test files green, and five disabled semantic guards did too; the POSE, CHARGE, ROADMAP and ENDPOINT figures read nothing from data. Add tests that fail on a changed label or a disabled guard, and have those four figures read their numbers from the receipts.
