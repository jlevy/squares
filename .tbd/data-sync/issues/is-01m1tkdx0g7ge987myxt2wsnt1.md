---
type: is
id: is-01m1tkdx0g7ge987myxt2wsnt1
title: Pin the explainer's proof and verifier links to the publication commit or a release archive (F8)
kind: task
status: closed
priority: 2
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:30.831Z
updated_at: 2026-09-06T06:21:09.298Z
closed_at: 2026-09-06T06:21:09.298Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 8, confirmed: render_explainer.py:307 builds every repository link as blob/main/..., while the page stamps an edition that already names a commit (sqpack.release PUBLICATION_STAMP). The certificate digests identify the data; nothing identifies the executed verifier, the lockfile, or the exposition a reported run used. Fix: build links from the publication commit (permalinks) and/or publish a release archive with the theorem, both certificates, verify_claim.py, the thirdparty package, uv.lock and complete verification outputs, so external replays can name both the certificate bytes and the executed source. Related: PR #92's Limits section notes the edition stamp is stale and that bumping it regenerates the atlas family.
