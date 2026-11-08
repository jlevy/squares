---
type: is
id: is-01m6xtfj9k290nt68gkczqsrkh
title: "Import #924: unnir (Numaro) s(12) >= 9929/2500 = 3.9716, weighted-point certificate in Daniel's format (+1/10000 over T-095)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l57
labels:
  - result-import
  - intake
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-08T14:54:57.840Z
updated_at: 2026-11-08T15:21:57.209Z
started_at: 2026-11-08T14:56:54.967Z
---
Issue jlevy/squares#924 (unnir, Numaro; opened 2026-11-08T14:21:31Z). Certificate: github.com/unnir/s12-lower-bound-3.9716 at 064c2955670765321aaf1c0a2d5c778949daab6b, certificate/s12_lower_3.9716.txt sha256 833b76a1...2cbd; 4,996 D4-symmetric points, side 15886400/4000000, W=9985226, total 119787760/9985226 < 12. Producer checks: Daniel's verify (all 39,765 bins, min 1) and Ryu's indep_scan (96,000 intervals). Precedent T-095 (#363): replayed by Daniel's verifier, this repository's parent-core interval branch and bound (method-distinct), and indep_check; stage 4 review docs/project/reviews/review-2026-10-05-s12-v11-certificate.md. Runbook packing/campaign/result-import.md stages 1-7.

## Notes

Stage 1 triage (intake lane L57, bold-ritchie-l57, 2026-11-08):

Claim map. The source (unnir/s12-lower-bound-3.9716 at 064c2955, its only commit, 2026-11-08T14:20:03Z) makes one claim in scope: s(12) >= 9929/2500 = 3.9716 from certificate/s12_lower_3.9716.txt (sha256 833b76a1...2cbd, matches #924). Register action: a new entry, T-274 (kind lower-bound, scope n = 12), 1/10000 above T-095's verified 7943/2000. Nobody else holds 9929/2500. n = 12's reported lower lane holds T-245's s(12) = 4 (Jatloe's Lean proof, V0/C0, #810), so this improves only the verified lane, and that lane waits for the stage 4 review (verified_lane_review_problems). No other claims; the README claims no technique and no optimality. Credit: unnir (Numaro); the sources give no other name (attribution.md: a handle stands where no other name is given). AI assistance: "Numaro Autonomous Research (agentic autonomous autoresearch)".

Validation plan, priced from samples on this host (4 cores, shared with lane L58):
- Daniel's verify (vendored main.rs f7c700c8 = evand 0e76d9fe verify/; differs from the retained 226ef3f1 only by upstream cca7bf1, exit codes and a doc comment), built with overflow checks (binary 9f9dbeaf, reproducible), all 39,765 bins: 120-bin sample 81.4 CPU-s, so ~27,000 CPU-s (7.5 CPU-h).
- Native parent-core route, case s12-unnir, all 39,765 rows: 33-row sample, ~0.72 s/row, so ~29,000 CPU-s (8 CPU-h).
- Ryu's indep_scan.cpp (74146d48 = 7a96bec3 tools/indep_scan.cpp with its include line changed), all 96,000 bins: 600-bin sample 5.3 CPU-s, so ~850 CPU-s; plus full sweeps of the lowered-orbit and regrid controls, ~850 CPU-s each.
- Exact premise audit (devtools.audit_s12_unnir_certificate): seconds.
Total ~17 CPU-h, under the 40 CPU-h item cap; every heavy run nice 19, at most 2 threads.

Controls: the source's two (W doubled, last point dropped) rebuilt as its replay.py writes them, plus the orbit of the heaviest point captured at the tight pose of bin 39531 lowered by 1/W a point, and the regrid D = 3999600 (T-095's precedent).

Acknowledgement (draft, for the coordinator to post after the records merge): received the certificate at 064c2955; retained it with its vendored checkers; running Daniel's verify with overflow checks, indep_scan, and this repository's parent-core interval route over every bin and row, an exact audit of the premises and four controls; a separate stage 4 mathematical review; n = 12's verified lower lane moves only after that review accepts.
