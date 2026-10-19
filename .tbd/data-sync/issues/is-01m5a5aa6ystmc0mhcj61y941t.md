---
type: is
id: is-01m5a5aa6ystmc0mhcj61y941t
title: Repair fine-net Mac reporter metadata and CPU availability
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m5a1wv68nj53kemkw4t6ws0p
hold: null
hold_until: null
created_at: 2026-10-19T13:23:49.597Z
updated_at: 2026-10-19T13:33:14.160Z
started_at: 2026-10-19T13:24:01.220Z
---
Engineering-only child: correct preserved build/platform and CPU availability prose for mixed and rectangle reporters; retain truthful current fine-net packet shared-components relationship and historical independently implemented packets. Add fail-before/pass-after synthetic regression tests, preserve all raw/native bytes, controls semantics and existing research records. Local commit only; parent remains open for fresh review and later publication.

## Notes

Local engineering repair committed 5bced23963676b296b9aed9685184fd290c7df62 (base 8f2d7981528fd31efd3af557cd367cc9741ba66e), confirm-422 branch codex/intake-post671-followup-20261019. Three files only: reporter, existing thread-count expectations, new synthetic reporting tests. Six new regressions failed before repair (0.30s) and passed after; focused synthetic plus historical evidence-entry selection: 12 passed, 139 deselected, 1.41s. Ruff check/format clean and BasedPyright with primary Python3.14.7 interpreter 0 errors, 0 warnings for all three files. Normal commit hooks passed in 3.15s. Native bytes/source/binary/process and all raw science/records untouched. Optional CERT.execution.json is the authentic execution record, bound by certificate/candidate/binary/build; recovery outer capture exit remains unobserved while native exit0 is explicit, aggregate controls timing is kept separate from wait4 capture CPU and absent direction CPU. Current fine-net/check2 packets are shared-components; known historical packets remain independent; unknown packet relation unknown-historical. No generated evidence publication, push, PR or public reply. Source ownership released to root for fresh review; keep this child and parent think-dazj open until that review is accepted.
