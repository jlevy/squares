---
type: is
id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
title: "Review the Burns n = 17 page against the n = 17 record: coverage audit and integration items"
kind: task
status: in_progress
priority: 1
version: 15
labels:
  - sources
  - n17
dependencies: []
child_order_hints:
  - is-01m1wwwm5cx2s645pbeb9gxxb3
  - is-01m1wwwmhad0dahswn1x5ea8a3
  - is-01m1wwwmwxxvrftyqk3facczta
  - is-01m1wwwn7zg395nwctzk392sf7
  - is-01m1wwwnma811qb4fkntj3y972
  - is-01m1wxbf2cznnh49r78dddq5d4
  - is-01m1wz2hce88j64qdj583wwhqc
  - is-01m1x082zdzp30q5qtdp3zdkzb
  - is-01m1x0ggfbap6dnadkv027h5tw
created_at: 2026-09-07T02:57:06.708Z
updated_at: 2026-09-07T04:30:02.643Z
---
Requested 2026-09-07: review the n = 17 work and decide whether https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/ is fully captured, whether it is in the archive, and what to integrate. Findings so far: the post, proof note and verifier are retained byte for byte under packing/resources/web/n17-lower-bounds-2026/ (SHA-256 9033d31c..., a7ddd764..., 6d83c286...), re-fetched today and identical; the archive README is a frozen input of the resumable n = 17 machinery and must not be reworded. Burns's own 268-atom verifier replays here (Python 3.13 + NumPy, 7.4 s): atoms 268, total 169476/10000, minimum 10003/10000 at every direction, CERTIFICATE CONDITIONS VERIFIED, s(17) >= 4.4811 -- a replay the record never held (only Massaccesi's copy has an evidence entry). Gaps found: the near-record post's downloadable coordinates JSON and its five SVG figures and the two post images are not archived; the Part 1 intro post (2026-08-05) is not archived; the Squarl repository (github.com/sam-bee/squarl, MIT, head 016dff98 of 2026-08-05) is cited only inside the archived note; the 4.4811 rung is absent from n-017.md's provenance paragraph; the planned Burns-certificate positive control (BC-115, H-061, agenda-017) was never built; BC-151 deferred adding the [Burns--Massaccesi n17] resource to the n = 17--19 case files. Sub-beads carry each item.

## Notes

2026-09-07: both passes committed and pushed on claude/n17-square-packing-review-qb86oa (33b4f38 Burns reconciliation and comprehensive review; 9afae3c three GitHub certificate repositories archived, T-019 prior-value claim corrected, credits and catalogue entries). PR #106. Open follow-ups: think-388u (decide anabologyco under Boost/Lean and Mira/Fort by the green17 interval audit), think-t5va (Burns basin reconstruction).
