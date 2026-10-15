---
type: is
id: is-01m50wdv3taw3k5gt76mhzx8mm
title: "Record-keeping: make the record state explicitly per count whether its displayed drawing is regularized (field + gate), fix the process if it cannot"
kind: task
status: in_progress
priority: 1
version: 7
delegate: ecstatic-edison-reg-record
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m50wdvvpwz9asfq2gvaxfz5w
  - type: blocks
    target: is-01m50xqm2f4t3jb74z1sjnx5x9
  - type: blocks
    target: is-01m50xqnsqj449s8rz91s61rdn
  - type: blocks
    target: is-01m50xqqjr60wtgjhqbwayj10m
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T22:55:18.138Z
updated_at: 2026-10-15T23:18:47.484Z
started_at: 2026-10-15T23:18:47.484Z
---

## Notes

Design from the audit (think-y1x3): extend default-drawings.json to all 324 counts with drawn source, state (regularized / regular-as-published / decided / exempt / pending), the seven measures, witness digest, runs decided on that witness with outcome; update_atlas writes a lapsed block instead of printing; records-tier gate fails on pending counts with a shrink-only allowlist starting at today's 20; fix case-note wording where the house is drawn. Land before any T-174 (#574) adoption: 35 counts at risk.
