---
type: is
id: is-01m3wwadvw2y99xs6h5ryjnhtk
title: "Verification Ladders: cleaner column questions, and tighter rows"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T23:20:46.711Z
updated_at: 2026-10-01T23:59:07.193Z
closed_at: 2026-10-01T23:59:07.193Z
close_reason: "Merged as jlevy/squares#288 (merge 48e7e5aa8, commit 643448be9): ladder heads read Significance/Verification/Confirmation with their one-line questions; row space 0.75rem to 0.4rem; tests pin both."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'make sure the subheaders on S, V, C ladder chart are cleaner: Significance / How significant is the result? — Verification / How was it originally verified? — Confirmation / How has it been confirmed? — and drop some of the padding on the rows of the table, they are a bit too vertically separated'. The three column heads take exactly those questions; the row padding (--site-ladders-row-space, 0.75rem above and below since think-m2hd removed the row rules) comes down so the rungs read as one ladder; every description stays two lines and every rung one height at each width (test_site_ladders).
