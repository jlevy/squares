---
type: is
id: is-01m4ajfv9newq89sh4qzq4156c
title: "W7: strict SQUISH #401 import and exact dual-checker receipts"
kind: task
status: in_progress
priority: 1
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T06:58:20.597Z
updated_at: 2026-10-07T07:16:01.204Z
started_at: 2026-10-07T06:58:30.243Z
---

## Notes

Local engineering implementation and verification complete; leave in_progress pending parent publication and CI. Added bounded strict SQUISH source parser/acquisition, exact half-angle conversion via public existing adapter helpers, dual exact deciding routes, deterministic compressed derived facts and certificates, bound verification receipts, source provenance checks, and fast/replay commands. Full bound recertification: 45.990 wall seconds with 2 workers. Full deterministic replay: 76.122 wall seconds serial; all eleven n=108,126,129,130,153,154,155,180,209,238,303 and both overlap/container controls pass expected outcomes; 177440 pair decisions per checker across positive cases. Final 40 tests passed in 2.92 seconds; Ruff and BasedPyright zero findings, fast artifact check passed. Fixed reviewed duplicate roster handling, tuple/list control replay mismatch, stale checker-input evidence binding, source provenance drift, and inconsistent verdict/clearance receipt fields, each with targeted tests. Runtime cost: final certification plus replay 2.04 wall minutes; exploratory initial cert49.061s, failed replay79.676s, canonical replay138.650s, final recert45.990s, final replay76.122s = 6.49 wall minutes total engineering geometry runs (reviewer runs additional). Source producer executable absent and never claimed reproduced. Raw upstream bytes not retained; source/fact/certificate hashes protect acquisition and checker-input trust boundaries, no Git code fingerprints. Packet packing/resources/web/squish-401-2026-10-07; witnesses packing/witnesses/squish-401-2026. Registration tests test_squish_upper_bound_packets.py; confirmation artifact tests test_squish_upper_bound_receipts.py. Reproduce from packing with uv run --frozen python -m devtools.squish_upper_bound_packets certify --workers 2, then check --replay. Remote tbd sync remains known divergent/push403; preserve local notes and all beads in outbox. Parent handles separate PRs, issue comments, final bead disposition.
