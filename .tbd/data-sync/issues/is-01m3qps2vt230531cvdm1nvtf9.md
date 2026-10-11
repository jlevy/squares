---
type: is
id: is-01m3qps2vt230531cvdm1nvtf9
title: Resolve wand125 provisional claim ID collision during upstream integration
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-29T23:07:43.041Z
updated_at: 2026-09-30T15:19:25.920Z
closed_at: 2026-09-30T15:19:25.920Z
close_reason: Published and reviewed in PR246 through b6c97667b. Existing provider T-056/T-057 are preserved; wand125 canonical claims are T-058/T-059. Lazy n32/n45 implementation reports explicitly map to existing T-051/T-053 with no new packing claim IDs or V/C promotion. Source evidence and historical identifiers remain preserved; final integration timing is separately tracked under think-niqx.
resolution: null
duplicate_of: null
---
Integrated in local merge cb7bc3998: preserve published Couzo/de Winter T-056/T-057, register wand125 as T-058/T-059, retain original archived bytes with explicit historical mapping. Independent Astra-max and Sol source-preservation audits passed. Remaining closure requirement: publish the mapped source and verify final-head registry/hosted checks under think-niqx. No additional claim promotion is authorized by this mapping.
