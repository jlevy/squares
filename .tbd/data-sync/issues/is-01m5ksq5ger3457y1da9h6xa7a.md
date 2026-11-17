---
type: is
id: is-01m5ksq5ger3457y1da9h6xa7a
title: "Stage 4 mathematical review of T-233: wand125's #446 fine-net lower bounds at n = 19, 20, 26, 27"
kind: task
status: closed
priority: 1
version: 4
delegate: c-review-t233-math
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:13:32.174Z
updated_at: 2026-10-24T08:26:44.395Z
started_at: 2026-10-23T07:13:34.195Z
closed_at: 2026-10-24T08:26:44.394Z
close_reason: "T-233's stage 4 review landed on main with #745 (af9c9e850): docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md and the packet's review/review-2026-10-23/; T-233 V0/C1 pending think-tcsl."
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 c-review-t233-math (stage 4 mathematical review of T-233, read-only; no commit, push, post or sync).

Verdict: accept at n = 19, 20, 26 and 27. No blocking or major finding. Minor, for the record: F-1 credit "Hosono after Levy" (bibliography.yaml line 1579, T-233 claim line 32122) differs from the family's "Hiroaki Hosono after Tokoharu and Levy"; F-2 an external_review on the seven-count E-wand125-fine-net-lower-bounds-446-report must be scoped to n = 19, 20, 26 (or split the entry); F-3 the replay price applies one ratio to 6- and 12-thread runs and prices controls at the capture's full cost. Notes F-4 to F-9 (overlong lines; claim wording; README control filename; soundness document beside the archive predates lemma N0; UPSTREAM_COMMIT 42534d95 unresolvable, but by digest the archive is e020eb1e2 with only certificate.rs, tests/adversarial.rs, README.md and SOUNDNESS.md changed; whole-net control should refuse everywhere).

Checker (clean room, own code, CPU 579 s for the final runs, about 12 CPU-minutes with trials): exact premises at all four; the net by direct geometry (10,363 orientations); direction 0 decided completely at each count (events and argmins equal the source's); 124/124 oblique control witnesses equal to the source's fractions; exact capture at all 8,288 least-bound centres >= 1 and >= the certified bound; 32-direction sample per count, least exact capture found 1.0003078 (n = 26, r = 1349); every value >= 1 and >= the source's certified bound; 99/100 witness at all 128 sampled directions.

Rungs: V0/C1 now, once the external_review lands (section 3a of record-changes.md); V3/C3 per count after a maintained census with whole-net controls. Significance S3 confirmed; no News owed. Replay price (think-ndvg): n19 1.4-2.7, n20 2.3-4.6, n26 3.1-4.8, n27 3.7-7.0 CPU-h; 10.5-19.2 for the four.

Outputs (coordinator scratchpad, at repository paths): review-t233/docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md; review-t233/packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/review/review-2026-10-23/ (programs, outputs, README); review-t233/record-changes.md.
