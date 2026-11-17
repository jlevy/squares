---
type: is
id: is-01m7eb5wbrcnjdjkw461e24gd8
title: "Read moh63-dev/k2m5-family v1.1 (85279d2, 14 Nov): Lemma 7 sentence, crop_cover, axis_exact, zmx2 logs, controls, LICENSE, run_cov fix, answering #973's questions; record in intake-watch and #973 notes; re-price think-0h7r if the zmx2 logs change F4"
kind: task
status: closed
priority: 2
version: 4
delegate: bold-ritchie-l168
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-15T00:54:37.176Z
updated_at: 2026-11-15T03:21:44.329Z
started_at: 2026-11-15T02:35:34.862Z
closed_at: 2026-11-15T03:21:44.329Z
close_reason: "k2m5-family v1.1 (85279d2, 9ccfe82) read in #990: answers #973 Q1,2,6,8,11,12,13 fully, 4,5,7,14,15 in part; think-0h7r price unchanged."
resolution: null
duplicate_of: null
---

## Notes

2026-11-15 03:10Z bold-ritchie-l168 (lane L168): read moh63-dev/k2m5-family through 9ccfe82 (85279d2 at 00:22:20Z, "v1.1 ..."; 9ccfe82 at 02:56:10Z, the same plus the paper's DOI 10.5281/zenodo.24237740), recorded in intake-watch.yaml, #973's requests notes and the packet README (The Authors' Answers). Certificate unchanged (sol_exact_box11.txt d259fed5...12099; nothing under certificate/ changes); 457 of the packet's 466 pinned files hold their digests, nine change (LICENSE, README.md, SHA256SUMS_ALL, docs/CHECKING.md, paper/k2m5.tex/.pdf, tight_tile/README.md, run_cov.sh, verify.sh). #973's questions: answered 1, 2, 6, 8, 11, 12, 13; in part 4, 5, 7, 14, 15; no answer 3, 9, 10. New zmx2 logs equal the 30 replayed columns root for root (timings aside). Not retained; packet pin and T-298 (V0/C1) unchanged. think-0h7r's price unchanged (notes appended). Open points: verify.sh --full step 6b cds into build/square-packing/qx2, absent at evand 659ee62; the real board's ctl_rise run at cap 2000 is 169 cells/85 certified in the release vs 155/78 in L145's uncapped run (re-run here refused by the permission check); cite the paper DOI when T-298 next changes. PR #990 (draft), head e4dd1e421; also records the final replies on #984/#985 and #983's follow-up.
