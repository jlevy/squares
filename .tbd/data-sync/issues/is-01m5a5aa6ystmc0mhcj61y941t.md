---
type: is
id: is-01m5a5aa6ystmc0mhcj61y941t
title: Repair fine-net Mac reporter metadata and CPU availability
kind: bug
status: in_progress
priority: 1
version: 5
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m5a1wv68nj53kemkw4t6ws0p
child_order_hints:
  - is-01m5a6wae3kyd9e5vhpfcag5yj
hold: null
hold_until: null
created_at: 2026-10-19T13:23:49.597Z
updated_at: 2026-10-19T13:51:08.226Z
started_at: 2026-10-19T13:24:01.220Z
---
Engineering-only child: correct preserved build/platform and CPU availability prose for mixed and rectangle reporters; retain truthful current fine-net packet shared-components relationship and historical independently implemented packets. Add fail-before/pass-after synthetic regression tests, preserve all raw/native bytes, controls semantics and existing research records. Local commit only; parent remains open for fresh review and later publication.

## Notes

Local source head e062abfacfef60aa160ccd7b177c5b29eb31c2f8 on confirm-422 branch codex/intake-post671-followup-20261019, following initial reporter repair 5bced23963676b296b9aed9685184fd290c7df62. Senior review .codex/intake-resume-20261019/fine-net-reporting-senior-review.md at 5bced2396 fully read with accepted Oct6 check2 review T-114/FN-4 and retained E-n029-wand125-mixed-581-sqverify-fast-replay. B1 Medium FIXED in e062abfac: exact (wand125-mixed-bounds-check2-2026-10-06,mixed_n29_L581) is independent-implementation before the shared packet rule; prose explains published shipped mixed_rotated_verify.cpp records versus reported adapted-crate pre-publication run with no retained receipt. Real check2 n28_L5735 and current fine-net n68 remain shared-components; alternate n29 side remains shared and same filename in unknown packet remains unknown-historical. B2 Low FIXED in e062abfac: numeric float conversion catches OverflowError and invalid timing remains unavailable; optional-companion regression includes10**400 alongside null/bool/negative/nonfinite/string cases. Both reproduced red-before:2 failed,5 deselected,0.30s. Final focused command: primary packing/.venv/bin/python3 -m pytest tests/test_sqverify_fast_census_reporting.py tests/test_sqverify_fast_census.py -k reporting/evidence_entry/states_a_sweep_control equivalent OR expression:13 passed,139 deselected,1.19s. Per-file Ruff clean; BasedPyright with primary --pythonpath:0errors0warnings. Normal commit hooks passed3.04s. Only reporter and focused reporting tests changed in followup; tracked tree clean, pre-existing untracked .codex/n183-a1-20261019 untouched. All native source/binary/processes/receipts/science/records untouched; no evidence generation, push, PR, CI or public disposition reply. Source ownership released for root-assigned fresh review. Leave think-fjb1 and parent think-dazj open until fresh review accepted.
