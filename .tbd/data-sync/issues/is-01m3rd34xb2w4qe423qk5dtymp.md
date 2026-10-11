---
type: is
id: is-01m3rd34xb2w4qe423qk5dtymp
title: Implement a Rust exact geometry kernel against the Python reference
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
created_at: 2026-09-30T05:37:41.796Z
updated_at: 2026-09-30T07:25:35.787Z
closed_at: 2026-09-30T07:25:35.787Z
close_reason: Rust backend integrated af87f6d44 and verified-tree classification4c826f8. Astra-max math/failclosed review, Rust quality gate,32 focused Python tests and matched exact report controls pass. Hosted Packing validation36683159180 completed success at4c826f8. Optional backend remains slower; Pythondefault, no fullC++ equivalence or T060proof claim. Further performance research remains tracked3cwg.
resolution: null
duplicate_of: null
---
User explicitly identifies Python rational overhead and asks about Rust. No firstparty Rust exact-rational rectangle verifier exists; sqsearch is floating search, archived integer verifiers cover other formats. Implement a narrow standalone Rust arbitrary-precision rational polygon-clipping/area kernel with batch input and exact output, leaving reviewed Python as oracle. Choose maintained pinned bigint/rational dependencies; no handwritten bigint or unchecked fixed-width overflow. Match clipping/tangency/large-denominator/degenerate/invalid inputs and complete analytic control, benchmark identical committed external rectangle tasks. Acceptance requires exact differential equality, tbd Rust lint/review/golden tests, source-bound receipts and complete matched threshold/domain, with no partial-to-proof promotion. Kernel speed alone is not full verifier parity.

## Notes

Implemented and committed af87f6d44. Astra-max approved admitted common-core math and failclosed transport/source/binary binding. Rust fmt/clippy/test/doc/build and32 affected Python tests pass. Final retained matched receipt: n3Python0.504/Rust3.800s, externaln11fixed1000Python13.252/Rust24.085s under concurrent host load; Rust childCPU10.889s. Both normalized exact reports equal; external bounded status INCONCLUSIVE. Python remains default. Hosted fd9980b failed only unclassified new gate in verified-tree contract; fix4c826f8 passes four focused contract tests and is pushed. Await greenhosted CI to close feature; speed work remains3cwg.
