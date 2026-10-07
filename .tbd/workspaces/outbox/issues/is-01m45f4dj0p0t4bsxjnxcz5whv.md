---
type: is
id: is-01m45f4dj0p0t4bsxjnxcz5whv
title: "Address PR #350 Review B (round 1): n17 branch-and-bound native kernel (wand125)"
kind: chore
status: open
priority: 2
version: 6
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m45f4fjgczmz88rp23cmq0q3
  - is-01m45f4hegh3px8scctd055260
  - is-01m45f4kg50gr27hwf79rwn4a6
  - is-01m45f4ngca78jxmqx0n5c05vq
  - is-01m45f4qcm18091q74s6ppxme0
created_at: 2026-10-05T07:23:28.191Z
updated_at: 2026-10-05T07:23:38.259Z
---
Review B (senior, round 1) on jlevy/squares#350 (wand125 / Hiroaki Hosono, optional
native kernel for the n17 sub-pattern branch and bound; leaf on #347, not in stack 357),
pinned to head 9179aab7d:
https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984. Verdict: code
sound and well tested; not ready to merge until B1 and B2 are settled and CI is green.
Findings, one child each: B1 (High) based on a feature branch but in no formal stack; B2
(Medium) body asserts a comparison the author retracted; B3 (Medium) body lacks the
repository’s PR sections and Validation predates the rebase; B4 (Low) certificate-run
claim broader than the code; B5 (Low) inconsistent fallback conditions.
CI: think-umlx (latest run 37275173288 cancelled).
The code is wand125’s; body and code fixes need the contributor or an authorized
maintainer commit. Closes when every child is closed and the dispositions reply is
posted.
