---
type: is
id: is-01m6xtfj9k290nt68gkczqsrkh
title: "Import #924: unnir (Numaro) s(12) >= 9929/2500 = 3.9716, weighted-point certificate in Daniel's format (+1/10000 over T-095)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l57
labels:
  - result-import
  - intake
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-08T14:54:57.840Z
updated_at: 2026-11-08T20:57:20.019Z
started_at: 2026-11-08T14:56:54.967Z
---
Issue jlevy/squares#924 (unnir, Numaro; opened 2026-11-08T14:21:31Z). Certificate: github.com/unnir/s12-lower-bound-3.9716 at 064c2955670765321aaf1c0a2d5c778949daab6b, certificate/s12_lower_3.9716.txt sha256 833b76a1...2cbd; 4,996 D4-symmetric points, side 15886400/4000000, W=9985226, total 119787760/9985226 < 12. Producer checks: Daniel's verify (all 39,765 bins, min 1) and Ryu's indep_scan (96,000 intervals). Precedent T-095 (#363): replayed by Daniel's verifier, this repository's parent-core interval branch and bound (method-distinct), and indep_check; stage 4 review docs/project/reviews/review-2026-10-05-s12-v11-certificate.md. Runbook packing/campaign/result-import.md stages 1-7.

## Notes

Stage 1 triage (intake lane L57, bold-ritchie-l57, 2026-11-08):

Claim map. The source (unnir/s12-lower-bound-3.9716 at 064c2955, its only commit, 2026-11-08T14:20:03Z) makes one claim in scope: s(12) >= 9929/2500 = 3.9716 from certificate/s12_lower_3.9716.txt (sha256 833b76a1...2cbd, matches #924). Register action: a new entry, T-274 (lower-bound, n = 12), 1/10000 above T-095. n = 12's reported lower lane holds T-245's s(12) = 4 (#810, V0/C0), so this moves only the verified lane. Credit: unnir (Numaro); AI assistance "Numaro Autonomous Research (agentic autonomous autoresearch)".

Outcome (stages 2, 3 and 5, draft PR jlevy/squares#925, branch claude/bold-ritchie-xo28us-l57, head 7b4badf24):
- Packet packing/resources/web/unnir-s12-lower-bound-2026-11-08 at 064c2955; all 19 SHA256SUMS digests match; vendored Rust verify = evand 0e76d9fe verify/ byte for byte (differs from retained 226ef3f1 only by upstream cca7bf1: exit codes, doc comment); indep_scan.cpp = 7a96bec3 with one include line changed.
- Daniel's verify (overflow checks, binary 9f9dbeaf), all 39,765 bins: VERIFIED, min 9985226/9985226 at bin 39531, log identical but timings; 28,028 CPU-s.
- Native parent-core route, case s12-unnir at d1b96ff4 clean: PASS_COMPLETE, 39,765 rows, 416,547,583 boxes; 27,321 CPU-s.
- indep_scan (binary fb0d4e2d), no range args, all 96,000 bins: VERIFIED, output identical to the source log; 834 CPU-s.
- Controls: source's two (W doubled; truncated) reproduce its logs; added lowered-tight-orbit (1/W a point) and regrid D = 3999600; every checker refuses each.
- Exact audit devtools.audit_s12_unnir_certificate: 16 checks PASS; tight pose at bin 39531 captures exactly W; T-095's 1,736 points kept (dilated 39716/39715) plus 3,260 new.
- Stage 4 review (L58, c066f1f9) cherry-picked after the verdicts were recorded and mapped: accept with findings; its full sweep is E-n012-unnir-9929-2500-review-sweep. T-274 at V3/C3, S3 confirmed; n = 12 verified lower lane moved to 9929/2500.
Total ~16.5 CPU-h under the 40 CPU-h cap.

Owed after merge (stage 7, the coordinator): the acknowledgement/confirmation reply on #924 with the review's F1, F2 and three questions for the author.
