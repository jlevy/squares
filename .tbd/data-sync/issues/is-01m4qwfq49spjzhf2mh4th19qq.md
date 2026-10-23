---
type: is
id: is-01m4qwfq49spjzhf2mh4th19qq
title: "Layer 6: records for the 2026-10-12 intake"
kind: task
status: closed
priority: 1
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T11:03:09.705Z
updated_at: 2026-10-23T06:12:29.100Z
started_at: 2026-10-12T11:03:18.294Z
closed_at: 2026-10-23T06:12:29.100Z
close_reason: "Tracker audit 2026-10-23 (c-audit-b-1023, think-ioqe), checked by coord-intake-1023: STALE-CLAIM + DONE. The layer 6 head 7dd8f5c0c (T-160, then T-156, registered and adopted at 154) is on main via #598 (e1f14898d, 2026-10-14)."
resolution: null
duplicate_of: null
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

84e0f4ef0 merge layer5 991853c80 (clean). ad2d99c7c tests: goldens (atlas 77/72, derived 47, poster 21 sources; escape screen +175, +264; T-155 superseded) and five slow nodes registered. 82ed5fdd2 fix: esummins certs/verify_tube.py pinned by digest (check_no_embedded_js reads its "=>" format string as JS), composite figure rigidity scopes at 175/232/264.
88cb1d6bb cherry-pick -x d31793edc (n40 stage 4 replay and review); document map conflicts resolved by union + render_document_map.
5d5a4a014 T-153 registered from scratchpad stage4/proposed-register.yaml: Guzhou0806 s(40) > 3359/500, V3/C3/S3, four evidence entries (report, kernel-replay, finite-audit, crate-axis), V-audit-n40-new-supports, versions at the 11 October pin for the two Guzhou kernels, coverage guzhou-n40-new-supports-2026-10-11; n-040 lanes to 3359/500 with T-145 as history (T-145 records-commit precedent 9b825844d); #485 s40-new-supports -> T-153; credit-attributions n=40 -> T-153 (precedent 6b1eb19d6); T-145 joins test_result_status's superseded set; all views rendered by their tools; check_results passes (155, contiguous). b3e165157 re-pin.
c4af885a2 fix: T-153's margin decimal rounds (0.00218425..., check_rung_figures); #528/#529 packet READMEs record the third route's decision. 4160adf27 re-pin. 92649a2eb tests: the announcement margins example is T-153 (T-145 is now superseded).
packing-validate --records: one failure (rung figure), fixed in c4af885a2. Touched tests (10 files, 638 nodes): 637 passed, 1 failed (the margins example), fixed in 92649a2eb.
check_frontend (workbench) fails on its animate-view contract: n = 29's 64.9387 and n = 272's 65.28896 share an angle in two slots (14, 15). n = 272's house moved in layer 4's 3e24adeb2 (T-151 at seven counts), which this layer did not touch; not this layer's own.
Announcement re-rendered with T-153 (7 lines; T-150 and T-155 below S3); gh profile reads succeeded with NO_PROXY for GitHub hosts; no finder declares an X handle, so all printed by name.

15bbc8792 rollups: 17 logs (coordinator, 8 grown, 8 new) via devtools.log_rollup, tier names in model fields, close_session --render; git grep finds no model identifier beyond what main already carries. packing-validate --records passes after them (49 steps, 236.6 s).
packing-validate --fast at 92649a2eb: 11 steps failed in 2711 s at load 14-20. Nine are wall timeouts (basedpyright 900 s, site table layout 900 s, behavioral shards A-D 900 s each, sqverify-fast cargo test 240 s, n17 bb native 240 s, n17 kernel clippy 120 s). Two exited 1: check_frontend's animate-view contract (n = 272, layer 4's 3e24adeb2, not this layer) and build_n5_identity_pair --check, which passed standalone right after ("2 endpoints, keys unchanged"), so it is load-dependent.
Layer head 15bbc8792. T-156 is reserved for #552 (coordinator's follow-up).

T-156 follow-up: d71aecaa3 merge review-552 (a2588a797, clean). 34e62125f T-156 registered (V3/C3/S3) and adopted at 154 by devtools.adopt_houses as a later pass (LATER_PASSES 12 October; T-136 kept 11 October; 154's prior state kept); custody 50 houses, 103 inputs, 32 mutations, 21.38 s; bibliography credit 'Daniel after Couzo, Levy' (lineage test needs Levy); #552 entry (result-report, no intake field) and #545 data release with full digests; evand read through 31523f8. bc4ade824 re-pin. 120436fae goldens (154 leaves the unstable list; poster 22 sources), #552 slow nodes registered, CI sweeps slice. 7dd8f5c0c rollups. --records passes; check_requests exit 0; touched tests 1358 passed, 3 failed then 2 fixed; test_render_packing_methods stale against layer 4's 28414fafc (main's copy fixes it). Pushed 7dd8f5c0c to origin claude/wizardly-meitner-wqn4x3-intake-1012 (fast-forward from 15bbc8792).
