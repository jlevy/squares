---
type: is
id: is-01m5249mz9n9e5b3d9rzyth5d5
title: intake_ledger start omits pending entries whose claim does not print their bounds (T-174's rationals)
kind: bug
status: in_progress
priority: 2
version: 2
delegate: user-eb-addr-642-651
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
hold: null
hold_until: null
created_at: 2026-10-16T10:32:03.817Z
updated_at: 2026-10-16T10:32:12.453Z
started_at: 2026-10-16T10:32:12.453Z
---
Found by PR #651 review A (https://github.com/jlevy/squares/pull/651#pullrequestreview-5546386141), A7 (Low). devtools.intake_ledger builds a ledger's start from check_standing.improvements, which reads a pending entry's bound from its claim text. T-174's claim does not print its rational certificates, so they are missing from the start at every count where they are the best pending bound (15 of #639's counts; 172, 263 and 297 among them, where the ledger would otherwise record #639 wrongly). #651's ledger (packing/campaign/intake-ledgers/, #639) works around this by hand, walking PR #574 again from the merged claim record; the ledger README notes and #651's owner item 5 say so. Fix either the tool (read the bound from the entry's structured certificate or claim record, not its prose) or the record (print T-174's rationals in its claim; the #622 note already earmarks the next change to T-174). Done when intake_ledger render at T-174's counts gives a start that holds T-174's rationals without a hand workaround, with a test.
