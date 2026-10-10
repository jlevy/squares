---
type: is
id: is-01m4k3mbw3qs3y2t9gg810mr8f
title: "Owner decision: publish hosted data release data/squarepacker-k2-minus-c-upper-certificates-v1 (two Theorem 1.6 certificates, 2.6 and 4.5 MB)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:31:49.890Z
updated_at: 2026-10-10T14:31:49.890Z
---
OR-18: the two largest Theorem 1.6 certificates of Ryu's k2-minus-c-upper preprint (stair_k38250000.json.gz 2.58 MB, stair_k100000000.json.gz 4.49 MB; digests equal the source's SHA256SUMS) are pinned, not committed, and staged in packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml for tag data/squarepacker-k2-minus-c-upper-certificates-v1. Publishing a release is outside the session's editing grant, so it waits for the owner: from a checkout holding the two files at packing/cases/asymptotic/hosted/squarepacker-k2-minus-c-upper/, run python -m devtools.hosted_data publish --manifest hosted/squarepacker-k2-minus-c-upper-certificates.yaml (from packing/). Until then the two certificates are decided by the receipts the 2026-10-10 lane retained (think-rd8u), and tests use the retained k = 10^5 certificate.
