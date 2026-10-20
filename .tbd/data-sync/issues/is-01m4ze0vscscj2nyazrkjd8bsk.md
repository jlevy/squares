---
type: is
id: is-01m4ze0vscscj2nyazrkjd8bsk
title: "PR 614 A10/B8: retake the 15 October prior state of nine moved counts from main"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4yz7whq6kvpef88k4dwj8z5
hold: null
hold_until: null
created_at: 2026-10-15T09:24:18.348Z
updated_at: 2026-10-15T09:46:35.036Z
started_at: 2026-10-15T09:24:24.486Z
closed_at: 2026-10-15T09:46:35.036Z
close_reason: "Fixed in 6133c4877: nine archive rows retaken from main at 19bd792d1, writer refresh rewrote the nine records, new test test_no_section_lists_its_current_house_or_a_held_certificate_as_not_selected."
resolution: null
duplicate_of: null
---
At 105, 129, 146, 156, 176, 261, 271, 272 and 303 the 15 October prior-state archive holds round 1's branch text (5e8b3fba8), so the superseded house's section lists the new house and T-174 as not selected. Retake those nine from main at 19bd792d1, rewrite through the writer, and add a test that no record's not-selected list names its current house or a held result.
