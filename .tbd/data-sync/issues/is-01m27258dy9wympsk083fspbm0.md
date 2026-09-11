---
type: is
id: is-01m27258dy9wympsk083fspbm0
title: Publish verifiable claim documents for T-025 and T-026
kind: task
status: in_progress
priority: 1
version: 4
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m26sv4284ry42pyavjhmmzqs
child_order_hints:
  - is-01m27m4tvdxr9kxwpjxh696x57
hold: null
hold_until: null
created_at: 2026-09-11T01:43:49.436Z
updated_at: 2026-09-11T06:58:09.900Z
started_at: 2026-09-11T01:44:10.625Z
---
Write separate, self-contained verifiable-claim documents for the direct threshold certificate T-025 and the exact dilation theorem T-026. Each document must state the theorem and definitions from first principles, identify every trusted input, provide an executable verification path, distinguish exact replay from independent interval confirmation, bind retained data, and avoid implying that an endpoint certificate exists for T-026. Add links and regression checks, run the record and page gates, then obtain an adversarial Astra Max mathematical review before marking complete.

## Notes

T025 and T026 now have generated self-contained Markdown claim packets, one shared CPython 3.12+ standard-library verifier, an independent event-cell oracle, freshness and mutation tests, exact input hashes, definitive exhaustive receipts, and a mapped source-distinct Astra review. Local claim and records checks pass. Close after final pushed-head CI passes.
