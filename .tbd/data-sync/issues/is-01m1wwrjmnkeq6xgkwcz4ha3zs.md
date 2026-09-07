---
type: is
id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
title: "Review the Burns n = 17 page against the n = 17 record: coverage audit and integration items"
kind: task
status: in_progress
priority: 1
version: 7
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
created_at: 2026-09-07T02:57:06.708Z
updated_at: 2026-09-07T03:00:03.716Z
---
Requested 2026-09-07: review the n = 17 work and decide whether https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/ is fully captured, whether it is in the archive, and what to integrate. Findings so far: the post, proof note and verifier are retained byte for byte under packing/resources/web/n17-lower-bounds-2026/ (SHA-256 9033d31c..., a7ddd764..., 6d83c286...), re-fetched today and identical; the archive README is a frozen input of the resumable n = 17 machinery and must not be reworded. Burns's own 268-atom verifier replays here (Python 3.13 + NumPy, 7.4 s): atoms 268, total 169476/10000, minimum 10003/10000 at every direction, CERTIFICATE CONDITIONS VERIFIED, s(17) >= 4.4811 -- a replay the record never held (only Massaccesi's copy has an evidence entry). Gaps found: the near-record post's downloadable coordinates JSON and its five SVG figures and the two post images are not archived; the Part 1 intro post (2026-08-05) is not archived; the Squarl repository (github.com/sam-bee/squarl, MIT, head 016dff98 of 2026-08-05) is cited only inside the archived note; the 4.4811 rung is absent from n-017.md's provenance paragraph; the planned Burns-certificate positive control (BC-115, H-061, agenda-017) was never built; BC-151 deferred adding the [Burns--Massaccesi n17] resource to the n = 17--19 case files. Sub-beads carry each item.

## Notes

Assessment delivered in chat 2026-09-07. Verdicts: (1) the page is fully archived, byte for byte, and its content is attributed in the frontier (proof-strategies 22, source key [Burns--Massaccesi n17], T-015 'on Burns's architecture', INVENTORY novelty lines, both literature audits); (2) what the record lacks is a replay of Burns's own certificate, the 4.4811 rung in n-017.md's provenance, the near-record post's data file and figures, the Part 1 post, the Squarl pointer, the planned Burns positive control, and the deferred BC-151 resource edit; each is a child bead. Repo working tree untouched; only beads were written.
