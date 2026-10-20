---
type: is
id: is-01m4xq50rrk4can2qfvaejajnv
title: Build the W7 bucketed exact route (verifier code) that the held Fang replays wait on (think-pvov, think-yeq9, think-dyyu)
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T17:25:22.840Z
updated_at: 2026-10-14T17:25:22.840Z
---
The validation backlog (think-lh7d) found that no bead owns the code three held items need: think-pvov (Fang's 70 theorem certificates; 44 of them exceed the 600 s job ceiling), think-yeq9 (38 shipped composites) and think-dyyu (53 table-only composites). Those replays need a bucketed exact route (W7) so that a large certificate can be decided under the per-job wall ceiling (OR-17).

Scope: design and build it in the verifier, with controls and a reviewer, per development.md's verification routes. This is code work. It spends no CPU of its own until a held replay is approved under the owner's cap (40 CPU-h per item as of 2026-10-14).
