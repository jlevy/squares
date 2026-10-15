---
type: is
id: is-01m50wdv3taw3k5gt76mhzx8mm
title: "Record-keeping: make the record state explicitly per count whether its displayed drawing is regularized (field + gate), fix the process if it cannot"
kind: task
status: open
priority: 1
version: 3
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m50wdvvpwz9asfq2gvaxfz5w
parent_id: is-01m50wdrbfnwsq05w150az5z88
created_at: 2026-10-15T22:55:18.138Z
updated_at: 2026-10-15T23:18:16.992Z
---

## Notes

Design from the audit (think-y1x3): extend default-drawings.json to all 324 counts with drawn source, state (regularized / regular-as-published / decided / exempt / pending), the seven measures, witness digest, runs decided on that witness with outcome; update_atlas writes a lapsed block instead of printing; records-tier gate fails on pending counts with a shrink-only allowlist starting at today's 20; fix case-note wording where the house is drawn. Land before any T-174 (#574) adoption: 35 counts at risk.
