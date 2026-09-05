---
type: is
id: is-01m1qf5hax9r31tsrfn30p5an1
title: "Certificate page: footnote popovers and hover states still show kpress's link blue"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-05T00:23:19.132Z
updated_at: 2026-09-05T00:26:35.330Z
closed_at: 2026-09-05T00:26:35.329Z
close_reason: Commit 6b639c00, verified on the rendered page.
resolution: null
duplicate_of: null
---
Follow-up to think-1cpm, which was closed too early: the accent token was set on .cert-page, but kpress appends footnote popovers to body, outside it, and the hover states use --color-primary-light, so links inside popovers and on hover were still blue. The link token moves to body and the hover states take the accent.
