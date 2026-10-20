---
type: is
id: is-01m50wdv3taw3k5gt76mhzx8mm
title: "Record-keeping: make the record state explicitly per count whether its displayed drawing is regularized (field + gate), fix the process if it cannot"
kind: task
status: closed
priority: 1
version: 11
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
updated_at: 2026-10-16T04:17:15.040Z
started_at: 2026-10-15T23:18:47.484Z
closed_at: 2026-10-16T04:17:15.040Z
close_reason: "#636 merged 2026-10-16 (e2e018f32): per-count regularization state, lapse record, shrink-only gate"
resolution: null
duplicate_of: null
---

## Notes

Design from the audit (think-y1x3): extend default-drawings.json to all 324 counts with drawn source, state (regularized / regular-as-published / decided / exempt / pending), the seven measures, witness digest, runs decided on that witness with outcome; update_atlas writes a lapsed block instead of printing; records-tier gate fails on pending counts with a shrink-only allowlist starting at today's 20; fix case-note wording where the house is drawn. Land before any T-174 (#574) adoption: 35 counts at risk.

2026-10-15, ecstatic-edison-reg-record: built in draft PR #636 (https://github.com/jlevy/squares/pull/636), branch claude/ecstatic-edison-8en33t-regularization-record, head 48c175623.
- default-drawings.json is DefaultDrawings/v2: `entries` unchanged plus `states` for n = 1..324 (state, drawn, generator, witness {id, source, side}, the drawn picture's seven measures, decisions {generator, run, outcome}, lapsed, why) and totals.states. Today: 58 regularized, 232 regular-as-published, 10 decided-no-better, 4 exempt, 20 pending.
- Declared inputs in devtools/default_drawings.py: SETTLED (decided 102, 110, 123, 155, 179, 180, 236, 258, 263, 269; exempt 39, 55, 290, 291 under think-yk2h), each bound to the witness's source key and side (OR-16: no digest comparisons) with runs and evidence; PENDING_ALLOWED = the audit's 20 with beads think-la7h / think-kpm3 / think-3zi3. A strong view held but not drawn on the current witness is decided-no-better automatically.
- Gate: `python -m devtools.default_drawings --check-state`, step "every drawn picture is regularized, regular as published, decided or exempt" (fast + records). Fails on a pending count not allowed, an allowed count no longer pending, a record naming another witness than the index, a SETTLED entry on another witness (source, side) or for a count that no longer needs it; a stale record fails the measuring --check.
- update_atlas writes `lapsed` {generator, run, witness_sha256} onto the axis record and carries it; verify_atlas compares without it (derived()); check_atlas holds it; regularize_evand admit_views strips it from `reference`.
- Case notes for the 10 house-drawn view counts open "Drawn as published: ..." (render_case_pages no longer appends held_note). Site cut v0.7.11; papers' no-change records (source review, no renders: no Chromium here).
- Guide/policy cost fixed to 13.7 CPU-h (49,302 CPU-s); closes think-0sx2.
- Follow-ups: think-290l (register-sense "regularization" wording in notes), think-0ut1 (residue runs). Each regularization PR (la7h/kpm3/3zi3) must take its counts off PENDING_ALLOWED.
- The first push (a94449d62) failed hosted validate and suite-c on 'integrity ceremony never grows' (OR-16 digest comparisons); fixed in afdf5cc65 by binding to source key and side. Hosted validate also fails 'bead tree' on think-eiu9 and think-nhut (PR #625 review A3/A4, open under closed think-i7i0), which this branch does not touch.
- Hosted CI on 48c175623: all 31 run checks pass (packing-required run 38827509142, pages-required run 38827509343), 28 skipped by selection; the deferred regularized-views job is skipped on PRs. PR #636 stays draft; never merged by this lane.
