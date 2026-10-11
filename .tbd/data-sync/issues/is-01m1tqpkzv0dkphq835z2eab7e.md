---
type: is
id: is-01m1tqpkzv0dkphq835z2eab7e
title: "A7: 'A wrong linear program will be rejected by the verifier'"
kind: chore
status: closed
priority: 3
version: 3
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:10.810Z
updated_at: 2026-10-06T08:24:28.496Z
closed_at: 2026-10-06T08:24:28.495Z
close_reason: "Done: PR 94 (merged 2026-09-06, 3e1fd715d) implements A7: 'The verifier rejects a certificate that fails the conditions, regardless of how it was generated'."
resolution: null
duplicate_of: null
---
explainer-article.md, 'Generator and Verifier'. The verifier never sees the program; it decides the certificate. Fix: 'A certificate written by a wrong program is rejected by the verifier.'
