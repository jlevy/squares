---
type: is
id: is-01m4k3mbw3qs3y2t9gg810mr8f
title: "Owner decision: publish hosted data release data/squarepacker-k2-minus-c-upper-certificates-v1 (two Theorem 1.6 certificates, 2.6 and 4.5 MB)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:31:49.890Z
updated_at: 2026-10-15T19:58:18.218Z
---
OR-18: the two largest Theorem 1.6 certificates of Ryu's k2-minus-c-upper preprint (stair_k38250000.json.gz 2.58 MB, stair_k100000000.json.gz 4.49 MB; digests equal the source's SHA256SUMS) are pinned, not committed, and staged in packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml for tag data/squarepacker-k2-minus-c-upper-certificates-v1. Publishing a release is outside the session's editing grant, so it waits for the owner: from a checkout holding the two files at packing/cases/asymptotic/hosted/squarepacker-k2-minus-c-upper/, run python -m devtools.hosted_data publish --manifest hosted/squarepacker-k2-minus-c-upper-certificates.yaml (from packing/). Until then the two certificates are decided by the receipts the 2026-10-10 lane retained (think-rd8u), and tests use the retained k = 10^5 certificate.

## Notes

2026-10-15, evening intake pass (think-wnsv), lane D (think-ykg6): the sweep read "Until then ... (think-rd8u)" as a wait on think-rd8u, closed. This bead is an owner decision and waits only on the owner: on 2026-10-15 the release data/squarepacker-k2-minus-c-upper-certificates-v1 does not exist on jlevy/squares (`gh release view`: release not found), and the decision is not among those #543 lists. No pull request, issue or bead stands for the owner's word, so the line below only clears the misread wait; the hold stands.

blocked_on: none
