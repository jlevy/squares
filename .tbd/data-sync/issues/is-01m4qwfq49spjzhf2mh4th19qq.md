---
type: is
id: is-01m4qwfq49spjzhf2mh4th19qq
title: "Layer 6: records for the 2026-10-12 intake"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T11:03:09.705Z
updated_at: 2026-10-12T12:16:16.628Z
started_at: 2026-10-12T11:03:18.294Z
---
Records lane for layer 6 of stack #517 (tracker #544): merge intake-esummins, intake-watch-1012 and review-528-529 onto layer5; register T-154 (#528) and T-155 (#529), T-153 reserved for s(40) > 3359/500; adopt #528's houses on n-175, n-232, n-264; result-requests entries #521-#529 and tracking issues; intake-watch reads; render; announcement; rollups; validate.

## Notes

## Layer 6 records lane (2026-10-12), worktree agent-a52951eff0f5644d2, branch layer6

Base: layer5 at 73ae0cc89. Merges (--no-ff): intake-esummins 7d4cc96c1 (5c3d11b4d), intake-watch-1012 cfbd4e8c3 (6e4c0c9a6), review-528-529 18843516c (8c9002d9a), all clean; origin/main 0d6010ff9 (#531, #546) (3b6f2b2b9): conflicts in result-import.md (kept layer 5's answering rule, added #546's label exception), the document map (both sets), SYNOPSIS (re-rendered), release.py (layer's pin until re-pin).

Baseline packing-validate --records on the merged tree: 48/49, only the stale synopsis document map.

c70872704 register: T-154 (#528, Ostashev, 175/232/264, S3) and T-155 (#529, Calle, 102, S2, superseded by T-146 on arrival, published 2026-10-11). T-153 left reserved for s(40) > 3359/500: check_results reports "register ids are not contiguous" until it is inserted. T-149 + E-ostashev-501-certificate-report RX-4 sentence. T-152 notes, #506 entry and couzo coverage note: Couzo's 175 stays in its packet (RX-5). #521 evidence E-n011-kleddamag-3875-esummins-replay-report on T-037 (+ URL identity amendment). Bibliography: [Calle n102 2026-10-12] lineage credits-project, credit "Calle after Xu, Levy" (the plan's builds-on-project "Calle after Xu" fails test_a_sources_credit_and_lineage_agree); [Summins stratification series 2026-10-12] without lineage (no registered result cites it). No credited-names alias needed: case records credit Daniil Ostashev, already mapped.

8a4d26fea houses: T-154 adopted at 175 (from T-140), 232 (from T-136) and 264 (from the catalogue's packing under T-101), dated 12 October (LATER_PASSES). Credits: Daniil Ostashev's compositions of his 38-square rectangle with the pieces the issue names. Custody: 50 houses, 100 inputs, 30 mutations refused, 108.94 s in the worker (deadline 120 s; load ~15). Snapshot 211,588,195 bytes, 14.9 MB headroom. n-264's T-101 ceiling prose marked historical by hand. SCREEN_FINDINGS updated (n<=200: 2184; n<=324: 121/1497/302/5040). Survey composites trail at 175/232/264 (--check-composites passes; redraw left for the next version or the owner).
3e4e63762 ci: dostashev-records-2026-10-12 joins the sweeps slice.
03169b83d requests: #521-#527 (lane Z proposals; #524 and #527 kind other + intake: true), #532-#545 (tracking issues: kind other; intake: true on #532-#537 and #545, which carry the label; asks or queued results on their beads), #485 read_through 2026-10-12T02:19:26Z, last_reviewed 2026-10-12. check_requests --github: 0 differences. intake-watch: evand ad86d42, wand125 d4a1981 (bead think-xzob), Esummins eb3ae15. dostashev and riocalle heads are their packets' pins (git ls-remote), so no read.
c607e9186 release: DATA_REVISION -> 8a4d26fe.
packing-validate --records: 48/49; the one failure is check_results' "register ids are not contiguous" (T-153 reserved).
Announcement rendered to scratchpad layer6-announcement.md (6 lines; T-150 and T-155 below S3; no handles: GitHub profile reads 403 in this session).
