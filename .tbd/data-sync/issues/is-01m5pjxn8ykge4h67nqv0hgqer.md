---
type: is
id: is-01m5pjxn8ykge4h67nqv0hgqer
title: "Import evand and franciscouzo: s(268) <= 16.874361715870 and s(304) <= 17.926898900357 (evand/square-packing 8a8879a), and s(304) <= 17.926898903393 (franciscouzo/square-packing fa6237e, Tymchishin's packing) (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-import-l49q-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T09:12:28.189Z
updated_at: 2026-10-24T13:38:16.088Z
started_at: 2026-10-24T13:38:16.088Z
---

## Notes

2026-10-24 coord-intake-1024, from think-6r5p's triage (c-triage-watch-1024; full verdicts in that bead's notes, tools and data in scratchpad triage-watch/). Report order: 268, #763 16.874361715873825 (23:35:51Z) then evand s268_lightning 16.874361715869346 (pushed 04:53:53Z), -4.48e-12, the exact KKT minimum of the same packing (0 squares beyond 0.1 against #763's and Tymchishin's v4 parent): recorded as a refinement (T-146 precedent), S2. 304 (not claimed by #763): franciscouzo certificates/best/n304.cert first committed in fa6237e, pushed 23:38:42Z, 17.926898903393 (-2.5289e-3 vs T-186; Couzo credits Tymchishin's 'CPU Alternating Reclosure' v3), S3; then evand s304_pub 17.926898900357 (-3.04e-9, the same packing, 4.6e-4 largest move), recorded. 303: evand's s303_cdeotte 17.907238274538 is above #763's 303 and is not recorded. Evan did not post them ('franciscouzo's open #763 already held all three'). Packet pinning 8a8879a (~0.45 MB) and n304.cert at fa6237e. Price < 2 CPU-h (replay < 0.02; two reviews; adoption and regularization at 268 and 304, 10-50 CPU-min each). PR B of #763 adopts 268 after this import (or Evan's packing) so 268 is re-housed once. Author questions (Evan): does he claim the 268 and 304 certificates, with this credit; notebook versions and dates for lightningv08's 268, Deotte's 303 and kozykappa's 304. Leaderboard side-only entries (pjmathematician 303, panpanpanda 268): not reports under 'Several Reports at One Count' (the order is the time a claim reached this repository: an issue, comment, PR or watched-repository commit), so no owner question; they bear only on credit wording, which the authors are asked.
blocked_on: think-ptkk
