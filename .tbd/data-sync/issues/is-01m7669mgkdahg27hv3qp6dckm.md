---
type: is
id: is-01m7669mgkdahg27hv3qp6dckm
title: Import de Winter's s(132) <= 11.976048383604 and s(157) <= 12.993302611344 (JoostdeWinter/square-packing a491dad/6617869, no issue; report by first commit)
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l104
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T20:55:21.870Z
updated_at: 2026-11-11T21:45:48.245Z
started_at: 2026-11-11T20:55:27.152Z
---

## Notes

Lane L104 (bold-ritchie-l104), 11 November 2026. Claim map and stage status.

Issue: jlevy/squares#958 (20:56:18Z), registration request, names JoostdeWinter/square-packing 6617869 (head, 20:52:23Z); n132/ and n157/ first committed at a491dad (20:49:44Z). Push not read (activity log refused); ledger dates by the issue with first commit kept; no other report reached 132/157 in the window.

Claims:
- s(132) <= 11.9760483836034076 (12-place print 11.976048383604): T-292, V3/C3 on the replay, S3 draft. 9.63e-03 below T-174 (Daniel, improved by PingYou Ltd). New arrangement (84 squares beyond 0.1). T-174 margin 0 (pair 87,88), RV-3 n/a. Own margin 1.248e-59.
- s(157) <= 12.9933026113432237 (12.993302611344): T-293, V3/C3 on the replay, S3 draft. 6.70e-03 below the grid 13; first below grid at 157 = 13^2-13+1 (k=13; T-220 k=14, T-163 k>=15). Grid margin 0. Own margin 1.349e-59.
- Credit: de Winter after Samanyu-dev (pinwheel at 109, Samanyu-dev/squares_in_squares 53551d7).
- L-step scan: neither bound carries; 184's L-extension from the grid at 157 lapses.

Packets: de-winter-s132-upper-bound-2026-11-11, de-winter-s157-upper-bound-2026-11-11. Ledger: campaign/issue-intake/upper-bounds-de-winter-132-157-20261111. intake-watch read through 6617869 covers 501cb8d (L103 owns #941/#942 entries).

PR: https://github.com/jlevy/squares/pull/961 (draft), head 5315ad8e5. T-291 is L100's (#954); records tier fails contiguity until #954 merges.

Next: merge L105's blind stage 4 review, map it (reviews on T-292/T-293, external_review on four atoms, verifier), then adopt 132 and 157 under the house rule with both strong generators and the flip; remove the two certificate-citation deferrals.

Open for coordinator: Samanyu-dev's 109 (10.949289581 < record 10.9497474683) is a candidate import; intake label on #958 and PR significance label not applied.
