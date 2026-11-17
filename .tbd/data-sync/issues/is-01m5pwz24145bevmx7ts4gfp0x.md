---
type: is
id: is-01m5pwz24145bevmx7ts4gfp0x
title: "Regather upper-bounds-20261014 offline: its ledger.yaml differs from its sources at the pr574 algebraic claims"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T12:07:59.872Z
updated_at: 2026-10-24T13:10:45.752Z
---
Found addressing #789 review B, B7 (think-8kvu). intake_ledger gather --snapshot on a copy of packing/campaign/issue-intake/upper-bounds-20261014 does not reproduce its ledger.yaml: at two pingyou-pr574 counts (8.8809603715555796 and 12.8700138504070441) the ledger reads a rational 'below' from acquisition/algebraic-claims.json at a branch commit (claude/wizardly-meitner-wqn4x3-intake-1014-pr574@56cf868c), while the packet's current file gives an algebraic 'equal' root. The other 13 walks reproduce byte for byte, and packing/tests/test_intake_ledger.py holds them; this walk is excepted there under this bead. Decide whether to regather it or to record the frozen read.

## Notes

2026-10-24 coord-intake-1024, from #789 review C (C2): the 14 October regather differs at seven PR #574 counts (70, 153, 207, 227, 229, 260, 302), not two, and the whole cross_check list changes (15 entries become 8, none shared). With the pr574 file restored to 56cf868c every relation reproduces but cross_check still differs; the lanes' claims.json files are byte-identical, so that part comes from 13 later commits to intake_ledger.py. The exception stands.
