---
type: is
id: is-01m1r4229zbmgsfhw541ya0wjd
title: "One result, four documents: settle the set (card, claim, proof note, page)"
kind: epic
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
child_order_hints:
  - is-01m1r433dappnfce17zj7dncdg
  - is-01m1r433twqcce9hvbskxjks9p
  - is-01m1r43489pyqczr1m4rge6ag2
  - is-01m1r4a7ey2d5g3c6z8qws07kp
  - is-01m1r4qj9k28kw8mpdx50q520y
created_at: 2026-09-05T06:28:25.535Z
updated_at: 2026-09-05T07:05:36.539Z
---
T-018 is described by t-018-proof-card.md (hand-written, one page), t-018-proof.md (hand-written one-minute proof for 381/100 with the finite-form lemma and the project's decision routes), the two generated verifiable-claim documents (theorem, proof, verifier and certificate embedded, one per bound), and the explainer page. Owner's direction: the minimal proof card stays; the 280-character form goes; decide whether the proof note is subsumed by the claim document or the reverse. Recommendation recorded in the child beads.

## Notes

Done on PR 79 (2fa1c39a, dad5a019, 80c74f18): the card is generated from certificate.json and results.yaml; the claim documents carry the finite form of Condition 5 and how the repository decided the bytes; t-018-proof.md is a superseded pointer; the explainer HTML stays out of git and the Pages build proves the render deterministic; conventions.md names the kinds. Open here: the two standalone verifiers (think-dfoc), which waits on the owner's decision.
