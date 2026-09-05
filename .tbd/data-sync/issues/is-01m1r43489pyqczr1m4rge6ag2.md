---
type: is
id: is-01m1r43489pyqczr1m4rge6ag2
title: Generate the proof card from the certificate, like the claim documents
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1r4229zbmgsfhw541ya0wjd
created_at: 2026-09-05T06:29:00.297Z
updated_at: 2026-09-05T06:29:00.297Z
---
t-018-proof-card.md is hand-written and quotes eleven figures (atom count, total weight, B, the net, D, B(1+D), least cover, cell count, digest prefix, runtime). Render it from a template through devtools.render_verifiable_claim's machinery so the card, the claim documents and the page share one source of numbers; keep the card one page, in the plain-HTML format if it is ever rendered by kpress. The digest stays read from the bytes. The four card tests in test_minimal_verify.py become drift checks against the render.
