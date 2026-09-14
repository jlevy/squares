---
type: is
id: is-01m2evx883khfqrmxg6fm6rqkg
title: Restore suite-tier headroom after the n11 stack lands
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
  - ci
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:28:31.106Z
updated_at: 2026-09-14T02:28:31.106Z
---
The hosted `suite` tier (ceiling 275 s, recorded 183.44 s; the 1.5× drift rule also fails at 275.16 s) measured 182–255 s at the stack heads, with about ±30% run-to-run noise on identical code (#166 attempts 246.1, 187.2, 248.9 s). main's tree alone measured 204.3 s (1.11× record). The stack adds about 151 test-seconds (~45 s wall), nearly all from three #156 files: test_read_fixed_core_calibration_profile.py (78.3 s), test_fixed_core_packet_calibration.py (30.0 s), test_fixed_core_packet.py (24.6 s). Projected after landing: about 249 s (91% of ceiling, 1.36× record). #157 adds only 2.4 s.

Work: (1) mark the measured slow refusal-control functions in test_read_fixed_core_calibration_profile.py `slow` with call-phase measurements recorded in test_the_slow_marker_is_declared_only_by_measured_nodes, as 2f8925b2 did (about 18 s wall); (2) after landing, re-record the suite mean from hosted readings of the landed selection (2026-09-09 precedent: ceiling up to about 1.5× the new record); (3) open the split of the suite across two runners (OR-14 treats a PR lane over 3 min as a defect; geometry-tier precedent).
