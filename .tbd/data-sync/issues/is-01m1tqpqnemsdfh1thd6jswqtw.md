---
type: is
id: is-01m1tqpqnemsdfh1thd6jswqtw
title: "C6: two verifiers, two runtimes, neither named"
kind: task
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:14.573Z
updated_at: 2026-09-06T06:50:22.432Z
---
The page's 'Verifiable Claim' section gives verify_claim.py's times ('about half a minute', 'about 3 minutes') and the proof card gives minimal_verify.py's (47.5 to 67 s); neither names the program or the machine, so they read as inconsistent. Fix on the page: '...verified by the embedded standard-library verifier in about 3 minutes on a laptop (the pinned one-file checker beside it, minimal_verify.py, in about a minute)'; on the proof card (proof_card.md template) name minimal_verify.py and the machine class. The RUNTIME placeholder already exists; add what is needed rather than typing numbers.
