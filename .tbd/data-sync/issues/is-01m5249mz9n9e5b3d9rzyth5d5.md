---
type: is
id: is-01m5249mz9n9e5b3d9rzyth5d5
title: intake_ledger start omits pending entries whose claim does not print their bounds (T-174's rationals)
kind: bug
status: in_progress
priority: 2
version: 4
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
hold: null
hold_until: null
created_at: 2026-10-16T10:32:03.817Z
updated_at: 2026-10-21T17:43:13.788Z
started_at: 2026-10-16T10:32:12.453Z
---
Found by PR #651 review A (https://github.com/jlevy/squares/pull/651#pullrequestreview-5546386141), A7 (Low). devtools.intake_ledger builds a ledger's start from check_standing.improvements, which reads a pending entry's bound from its claim text. T-174's claim does not print its rational certificates, so they are missing from the start at every count where they are the best pending bound (15 of #639's counts; 172, 263 and 297 among them, where the ledger would otherwise record #639 wrongly). #651's ledger (packing/campaign/intake-ledgers/, #639) works around this by hand, walking PR #574 again from the merged claim record; the ledger README notes and #651's owner item 5 say so. Fix either the tool (read the bound from the entry's structured certificate or claim record, not its prose) or the record (print T-174's rationals in its claim; the #622 note already earmarks the next change to T-174). Done when intake_ledger render at T-174's counts gives a start that holds T-174's rationals without a hand workaround, with a test.

## Notes

2026-10-21 coord-intake-1021b: ownership transferred to the 21 October intake coordinator (no update since the previous owner's last note; the 19 October machine-transfer handoff #684 and the owner's instruction of 21 October to resume the intake). Triage of the 21 October sweep follows.

2026-10-21 c-triage-sweep-1021b (read-only triage of the 21 October sweep): this bead waits on nothing; the sweep read "the best pending bound (15 of #639's counts ...)" as a wait on #639. Not fixed on main: devtools/intake_ledger.py is unchanged since 16 October and check_standing.improvements still reads a pending entry's bound from its claim text. The exposure has narrowed: since the adoption of 17 October (think-3mry, #665) the verified lanes at 172, 263 and 297 cite E-pingyou-574-exact-feasibility, so a ledger start built from the case lanes holds T-174's sides there without the hand workaround. The defect remains for any pending entry whose claim omits or truncates its bound, such as T-174's algebraic 70, 153 and 207, printed with an ellipsis. Price: 1 to 2 agent-hours with a test, no CPU.
blocked_on: none
