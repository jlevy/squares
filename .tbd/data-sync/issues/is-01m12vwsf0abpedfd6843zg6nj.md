---
type: is
id: is-01m12vwsf0abpedfd6843zg6nj
title: "Split the rigid field: catalogue transcription vs computed property"
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:21:40.959Z
updated_at: 2026-10-06T08:35:27.190Z
closed_at: 2026-10-06T08:35:27.190Z
close_reason: "Done: the case schema on origin/main (square-packing-case.schema.yaml) splits catalogue_rigid (enum rigid / semi-rigid / not-stated) from a first-party rigidity block with property, assurance and evidence; n-005, n-011, n-028, n-040 use it."
resolution: null
duplicate_of: null
---
packing.reported_upper_bound.rigid is doing two incompatible jobs. Survey: 3 true (n=5,28,40), 42 false, 55 null. It is non-null exactly when catalogue_pictured is true, so false means 'Kingbird pictured it and did not annotate Rigid' -- absence of evidence -- not 'has play'. No code writes it, no test checks it. The source vocabulary is also three-valued: the compared catalogue uses 'Semi-rigid'.

Proposal: rename the transcription to catalogue_rigid with an enum (rigid / semi-rigid / not-stated), and add a separate first-party field carrying an assurance level and evidence ref like every other bound in the schema. Also write back exp-013/H-026, which is an exact replayable first-order rigidity certificate for n=11 that exists today and is not reflected in the frontmatter.
