---
type: is
id: is-01m5mzwrp4a8f1drb54we5z1tq
title: "PR #745 (merge): senior review, address, gate"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-rev-745-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5ndfyhknd8p766m3pnpgn4a
  - is-01m5nvh5ndwftscfb39m9ma4fb
hold: null
hold_until: null
created_at: 2026-10-23T18:20:41.540Z
updated_at: 2026-10-24T02:23:41.741Z
started_at: 2026-10-23T18:20:46.241Z
---

## Notes

2026-10-23 c-rev-745-1023 (senior review lane of coord-intake-1023): Review A (senior, round 1) posted as a PR comment at head cd03e8049, base cc91ee1b8: https://github.com/jlevy/squares/pull/745#issuecomment-6372288301
Verdict: not merge-ready at this head; no Blocker. High: A1 (the new slow marker in sweep_cases() evades test_the_slow_marker_is_declared_only_by_measured_nodes). Medium: A2 (no hosted full checkpoint for the four whole fine-net sweeps; deferred-slow-lane 1250 s ceiling at risk, about +950 s hosted call), A3 (T-233 records still say no replay has run). Low: A4 News T-233 wording, A5 sample misses least-bound index, A6 failed receipt unread and census view shows "-", A7 n31 dates. Suggestion A8 (state or split the n19/n20/n27 hold).
Tests at cd03e8049: census PR lane 161 passed (47.5 s); four whole sweeps pass (n31 151.5 s, n19 143.0, n20 180.4, n27 191.1); consumers 485 passed, 7 failed on contiguity only; check_results contiguity only; check_source_coverage reconciled; News draft validates in memory; check_added_blobs PASS 7.26 MB.
main moved to 7cd0a94bf (#747): branch conflicts in INVENTORY.md, VERIFIERS.md, release.py. Next: address A1 to A8, merge main after #753, deep-gate label at the final head.
