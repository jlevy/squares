---
type: is
id: is-01m1tp65169btgpemts1hqrsjd
title: Release archive for the proof package on the next republish
kind: task
status: open
priority: 2
version: 1
labels:
  - review-gpt6
dependencies: []
created_at: 2026-09-06T06:23:42.629Z
updated_at: 2026-09-06T06:23:42.629Z
---
Finding 8 of the 2026-09-05 adversarial review asked for commit permalinks or a release archive. PR #92 did the permalinks (think-lci1); the archive was judged separate work: it needs a tag or release-asset step in a workflow, a digest manifest, and the complete verification outputs that nothing currently captures as artifacts. Contents: the theorem (proof card), both certificates, verify_claim.py, minimal_verify.py, the thirdparty package, packing/uv.lock, and the full outputs of each verifier run, so an external replay can name both the certificate bytes and the executed source. Ride it on the republish (see the edition bead) so the archive and the pinned links name the same commit.
