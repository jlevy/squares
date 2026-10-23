---
type: is
id: is-01m5kpenktnwj1zw0z2pp2m85n
title: "PR #742 A1: the #732 key's builds-on-project lineage and Levy credit are not what the source states"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-addr-742-1023
labels: []
dependencies: []
parent_id: is-01m5kpejtm3fmbx0sb888yj3t4
hold: null
hold_until: null
created_at: 2026-10-23T06:16:28.026Z
updated_at: 2026-10-23T07:42:20.750Z
started_at: 2026-10-23T06:16:57.777Z
closed_at: 2026-10-23T07:42:20.750Z
close_reason: "fixed in 5d1731b43: lineage independent, credit 'Polkovskyi after Couzo, Fang, PingYou Ltd' (chain at 931 through #715's index), header provenance in the note, Levy span removed, Fang and PingYou Ltd spans added; test_a_sources_credit_and_lineage_agree and credit tests pass (372). Reply: https://github.com/jlevy/squares/pull/742#issuecomment-6360024272"
resolution: null
duplicate_of: null
---
Medium, review A of PR #742 (https://github.com/jlevy/squares/pull/742#issuecomment-6358224906). packing/resources/bibliography.yaml:3259-3260; packing/contributors/occurrences.yaml:26096-26113. Set the lineage from what the source and the author's comment 6355486108 state, record the certificate headers' provenance, keep the suite-a credit test green honestly.
