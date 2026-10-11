---
type: is
id: is-01m3p04nvawjqqtx8cynyj2pwy
title: Resolve wand125 tools ceiling and certificate admission findings
kind: task
status: open
priority: 1
version: 14
labels: []
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
child_order_hints:
  - is-01m3q334yhrpa4nzahc9e8sw67
  - is-01m3q335am18z87zzbvvshk1c1
  - is-01m3q335pvv0mr0bgr5623m3bb
  - is-01m3q3362x0jttkppzvf27tabm
created_at: 2026-09-29T07:12:51.561Z
updated_at: 2026-10-02T20:48:16.318Z
---
W2 tools review retained: T-058 general B*UB ceiling lacks net-orientation premise and rigorous UB rounding. Admission defect executed: unchanged source scale_and_verify/certify/verify.cpp passes all201 then falsely prints s(1)>=1.5 for mass289/10. Reproducer devtools.audit_wand125_tools and receipts in wand125-tools-2026-09-29. Native checker must refuse same input. Remaining: corrected ceiling tooling and safe integration; do not send external maintainer messages without authorization.

## To finish (validation backlog, 2026-10-02)

T-058 (wand125's B*UB(n) rectangle-certificate ceiling, V0/C1): no CPU; a W2 mathematical slice. Either prove the ceiling with its missing premises discharged (net-aligned orientations of the B-scaled witness squares, certified outward upper witnesses in place of the table's rounded floats), or adopt the reviewed sufficient correction B*(1+D) from docs/project/reviews/review-2026-09-29-wand125-tools-mathematics.md, and record the statement that holds. Refutes: a certificate the reviewed checker accepts with mass below n at L >= B*UB(n) for some n <= 100, or an explicit configuration showing the dropped premise is needed. Moves the rung: an exact machine check of the corrected ceiling over n = 1..100 with certified upper witnesses, replayed here, derives V3/C3; a proof-audited statement alone reaches V3/C2. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

Reviewed source 0d33ab6. The general B*UB ceiling needs net-orientation and rigorous outward-witness premises; the review derives the sufficient factor B*(1+D). The executed rescaling control lets the upstream wrapper announce false s(1)>=1.5 with mass28.9 after all201 coverage checks pass. Integration must enforce strict mass admission, pinned source/patch/builder identities, a positive complete root census, explicit refusals under Python -O, and compiled cached-axis differential controls. Astra-max review also identified build-status loss in archived zmx2_run.sh:14 and zmx2_tests.sh:10; use actual compiler status and a fresh source-bound binary. The unchecked u32 point index at zmx2.rs:555 needs a count cap or checked conversion for unrestricted inputs. That enormous-input case was identified statically and does not invalidate retained certificates. Detailed findings: docs/project/reviews/review-2026-09-29-wand125-tools-mathematics.md. Archived source remains unchanged.

2026-09-29 upstream integration: wand125 provisional T-056/T-057 map to canonical T-058/T-059. Published Couzo/de Winter retain T-056/T-057. Historical notes and archived receipts retain their original labels; no evidence bytes or acceptance level changed.

2026-10-02: Done on claude/lane-dd-t058-ceiling (eb1d3f287, 6d27778df, 475e2a0b7): T-058 V3/C3, corrected statement; close after merge into #298. Review its check_certificate_citations change.
