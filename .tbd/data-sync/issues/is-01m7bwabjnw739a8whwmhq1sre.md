---
type: is
id: is-01m7bwabjnw739a8whwmhq1sre
title: "Import #973: moh63-dev's s(k² − 5) = k for every k ≥ 7 (one periodic family, Valid11 board, Tight-Tile Lemma)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l145
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m7bxg56ccnr8yr3dr26nrtd2
  - is-01m7c65j5dk876m77ftewkck4q
hold: null
hold_until: null
created_at: 2026-11-14T01:56:26.322Z
updated_at: 2026-11-14T04:48:34.989Z
started_at: 2026-11-14T01:56:28.028Z
---

## Notes

2026-11-14 (lane L145, bold-ritchie-l145): stages 1 to 3 done and a time-boxed stage 4 replay run.
Claim map: one result, s(k^2 - 5) = k for every k >= 7 (#973 body), registered as T-298 (optimality, scope n = 44, 59, 76, 95, 116, 139, 164, 191, 220, 251, 284, 319), V0/C0, S4 drafted as a claim; evidence E-khalili-973-k2m5-family-report, E-khalili-973-valid11-report, E-khalili-973-lean-report (all reported). New counts k = 11 to 18 (reported lanes to k, verified unchanged); n = 95 already proved by T-191; k = 7, 8, 9 are T-252, T-066, T-184. T-081 and T-191 gain a sentence each. No verified bound changes.
Retained: packets moh63-dev-k2m5-family-2026-11-13 (pin 2c0b1b9, 465 of 466 files; tight_tile/cov.tar.xz pinned by digest, 8.7 MB, hosted release owed with think-0h7r) and evand-square-packing-2026-10-24 (zeromargin.py 3cb95fb7 at 659ee62). Licence MIT (README adds CC BY 4.0). AI assistance: Claude (Anthropic) per the paper's acknowledgments; builds on Evan Daniel's LP, format, checkers and Lean reduction.
Replay here, about 2.5 CPU-hours: fast verify.sh passed; zmx2 e2bb84e9 rebuilt (d68a2e35), patch is one line output-only; cert0 + 30 of 55 columns equal to the source; root 9632 whole (dump 6,850 boxes and qx2 83 boxes byte-identical; ROOT-9632-CLOSED on our outputs; the dump needs --uncert-cap 10^8, unrecorded); 26 tight-tile jobs equal (the shipped run_tt.py prints a K field the recorded outputs lack); controls all refused. Full replay and Lean build priced on think-0h7r (about 140 CPU-hours, up to 320). Stage 4 review: think-h10k (lane L144), not landed at push; the coordinator maps it.
Acknowledgement draft (post after the PR merges, by stage 7's rule): thank the authors; say the release was retained at 2c0b1b9 and registered as T-298, a reported family at V0/C0 pending the stage 4 review; what ran here (fast verify, cert0 and 30 zmx2 columns, root 9632 with both checkers, 26 tight-tile jobs, the controls), each matching their records; that the full replay (about 140 CPU-hours, up to 320) and the Lean build are priced and held for the owner; and ask the nine questions of the packet README.
