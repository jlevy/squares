---
type: is
id: is-01m5ppkz2jedpvbe0tpd7crt4s
title: "PR #781 (merge): follow-up review B of review A's fixes (A1 evidence entry, the test_house_adoption guard edit)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-781b-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T10:17:04.850Z
updated_at: 2026-10-24T10:34:45.294Z
started_at: 2026-10-24T10:17:12.801Z
closed_at: 2026-10-24T10:34:45.293Z
close_reason: "Review B posted https://github.com/jlevy/squares/pull/781#issuecomment-6383157716 at 8241aa881: approve (B1, B2 Low; B3, B4 suggestions); A1's fix and the guard-test edit verified; addressed with the #736 main merge by c-fix-781-1024."
resolution: null
duplicate_of: null
---

## Notes

Review B (follow-up, round 2) of #781 published by c-rev-781b-1024 at head 8241aa881, base b2ea7b09c: https://github.com/jlevy/squares/pull/781#issuecomment-6383157716. Verdict: approve. Dispositions A1-A7 all hold; A1's discharger is well formed, its four-count scope honest, the note chain 3 with the replay and 0 without; receipt re-run identical to the committed receipt and to the 14 Oct outputs. Guard edit eba2bc491 narrows one named citation at 241/T-182 and 273/T-174 without weakening the guard. #787 merge kept both sides. Findings: B1 (Low) replayed bytes bind to PIECES.md by name only (binding holds by data-line identity with the Lean packet copies; record and test it); B2 (Low) #603 draft's 'a read raises confirmation, not verification' and its '2 to 3 CPU-hours' vs the record's 1.5 to 3. Suggestions B3 (pin real atom rank in the discharge test), B4 (rewrap three folded lines). Records tier 53/53 incl. bead tree, 218.8 s; tests 21+9+111+92 passed. Not synced (brief).
