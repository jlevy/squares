---
type: is
id: is-01m1r43489pyqczr1m4rge6ag2
title: Generate the proof card from the certificate, like the claim documents
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1r4229zbmgsfhw541ya0wjd
created_at: 2026-09-05T06:29:00.297Z
updated_at: 2026-09-05T07:01:03.479Z
closed_at: 2026-09-05T07:01:03.479Z
close_reason: "Done in dad5a019: render_verifiable_claim renders t-018-proof-card.md from certificate.json and results.yaml through templates/proof_card.md; every constant derived, rung/review/novelty read from the register, refuses without a recorded cell count or a review artifact on disk; the 279-character form removed in 2fa1c39a."
resolution: null
duplicate_of: null
---
t-018-proof-card.md is hand-written and quotes eleven figures (atom count, total weight, B, the net, D, B(1+D), least cover, cell count, digest prefix, runtime). Render it from a template through devtools.render_verifiable_claim's machinery so the card, the claim documents and the page share one source of numbers; keep the card one page, in the plain-HTML format if it is ever rendered by kpress. The digest stays read from the bytes. The four card tests in test_minimal_verify.py become drift checks against the render.
