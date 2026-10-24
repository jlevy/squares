---
type: is
id: is-01m5pwz24145bevmx7ts4gfp0x
title: "Regather upper-bounds-20261014 offline: its ledger.yaml differs from its sources at the pr574 algebraic claims"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T12:07:59.872Z
updated_at: 2026-10-24T12:07:59.872Z
---
Found addressing #789 review B, B7 (think-8kvu). intake_ledger gather --snapshot on a copy of packing/campaign/issue-intake/upper-bounds-20261014 does not reproduce its ledger.yaml: at two pingyou-pr574 counts (8.8809603715555796 and 12.8700138504070441) the ledger reads a rational 'below' from acquisition/algebraic-claims.json at a branch commit (claude/wizardly-meitner-wqn4x3-intake-1014-pr574@56cf868c), while the packet's current file gives an algebraic 'equal' root. The other 13 walks reproduce byte for byte, and packing/tests/test_intake_ledger.py holds them; this walk is excepted there under this bead. Decide whether to regather it or to record the frozen read.
