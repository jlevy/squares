---
type: is
id: is-01m5qw2vxfpq9swr8q3nq6cnw8
title: "Correct #795's 'seeded from previous_source' credit at 364, 450 and 874: the manifest field names the catalogue's previous record, not the seed"
kind: bug
status: closed
priority: 1
version: 5
delegate: c-map-hx0e-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T21:11:50.447Z
updated_at: 2026-10-25T04:14:53.416Z
started_at: 2026-10-24T21:12:00.789Z
closed_at: 2026-10-25T04:14:53.416Z
close_reason: "#795's credits at 364, 450 and 874 corrected to the notebook authors alone in #803 (merged 3699ce15e); previous_source is the catalogue's previous record, not the seed."
resolution: null
duplicate_of: null
---
Stage 4 review think-vm3m, finding M-1, confirmed by the coordinator against fa6237e's manifest: at 303 source_provenance.seed_credit is Lavrentev while previous_source.credit is Evan Daniel (T-230); in 182 of 182 fa6237e entries with their own seed the fields name someone else. So previous_source / previous_reference.seed_credit name the record Couzo's catalogue held before at that count, not lineage. #795 (merged 2ed0ea740) credits 364 (aqibrazadev after Tymchishin), 450 (kyleluecke after Tymchishin) and 874 (kyleluecke after Couzo and Lavrentev) as 'new packings seeded from the earlier side' on that field alone, with more than fifty squares beyond 0.1 measured: the seed link is unsupported. Correct the ledger's new_packing/continues reading, the coverage notes, the packet README's #795 section (around line 489: 'the manifest's previous_source is the link at all five counts'), the requests entry and the bibliography; 378 and 405 stay credited after Lavrentev, measured refinements. The coordinator's call of 24 October ('seeded from previous_source') was the error. Ask Couzo (C1) what previous_source means and which packing each notebook started from.

## Notes

2026-10-25 c-map-hx0e-1024: done in af0f65e05 on PR https://github.com/jlevy/squares/pull/803 (H1 of think-hx0e).
- beyond_horizon_replay._push_identity_parts: previous_source read as the catalogue's previous record (M-1 of the 24 October review of T-241 and T-242); a row one to one within 1e-3 refines (378, 405: kyleluecke after Lavrentev, unchanged); otherwise new_packing with no `continues` (364, 450, 874). The rows' own manifest provenance states no seed or lineage (checked at all five counts).
- Walk upper-bounds-couzo-964ee2b-notebooks-20261024 regenerated: release-sources (kyleluecke key), intake_ledger gather --snapshot and render --write: "a new packing" at 364, 450, 874; recorded_new_continuing 0.
- test_beyond_horizon_replay: the identity test asserts "a new packing" at the three counts and that no step names `continues` (coverage kept, assertion changed).
- Credit corrected to aqibrazadev alone at 364 and kyleluecke alone at 450 and 874 in: source-coverage notes (couzo-fa6237e, tymchishin-reclosure-v3, kyleluecke-inos, aqibrazadev-blending), the couzo-issue763 packet README's identity and credit section, #763's requests entry (notebook-rows-325-1024), and the kyleluecke and aqibrazadev bibliography notes.
- beyond_horizon_replay check, intake_ledger check and render --check pass; test_beyond_horizon_replay + test_intake_ledger 223 passed, 1 skipped.
- Which packing each notebook search started from: the posted #763 reply's question 7 asks what previous_source means (C1).



2026-10-25 c-map-hx0e-1024: after #800 (4089f9587, merged into #803 at 4b6f4bd27) the 43f666c walk supersedes 46 of #795's notebook rows (kyleluecke 11, aqibrazadev 8, among them 377 and 405) but none at 364, 450 or 874, so the three corrected rows stay current. Couzo's answer to question 7 of the confirmation reply (awaiting_author on #763) could add a link at 364, 450, 874. #803 head 9cc28fce0, CI green.
