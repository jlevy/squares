---
type: is
id: is-01m5qw2vxfpq9swr8q3nq6cnw8
title: "Correct #795's 'seeded from previous_source' credit at 364, 450 and 874: the manifest field names the catalogue's previous record, not the seed"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: c-map-hx0e-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T21:11:50.447Z
updated_at: 2026-10-24T21:12:00.790Z
started_at: 2026-10-24T21:12:00.789Z
---
Stage 4 review think-vm3m, finding M-1, confirmed by the coordinator against fa6237e's manifest: at 303 source_provenance.seed_credit is Lavrentev while previous_source.credit is Evan Daniel (T-230); in 182 of 182 fa6237e entries with their own seed the fields name someone else. So previous_source / previous_reference.seed_credit name the record Couzo's catalogue held before at that count, not lineage. #795 (merged 2ed0ea740) credits 364 (aqibrazadev after Tymchishin), 450 (kyleluecke after Tymchishin) and 874 (kyleluecke after Couzo and Lavrentev) as 'new packings seeded from the earlier side' on that field alone, with more than fifty squares beyond 0.1 measured: the seed link is unsupported. Correct the ledger's new_packing/continues reading, the coverage notes, the packet README's #795 section (around line 489: 'the manifest's previous_source is the link at all five counts'), the requests entry and the bibliography; 378 and 405 stay credited after Lavrentev, measured refinements. The coordinator's call of 24 October ('seeded from previous_source') was the error. Ask Couzo (C1) what previous_source means and which packing each notebook started from.
