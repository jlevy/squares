---
type: is
id: is-01m32htadd7m6f4v5tynkgew7s
title: Show rigidity only when proven; drop the unknown rigidity badge
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T17:56:57.896Z
updated_at: 2026-09-21T18:09:27.184Z
closed_at: 2026-09-21T18:09:27.183Z
close_reason: Builder no longer lists rigidity as open; the R badge remains on the proven side.
resolution: null
duplicate_of: null
---
Immediate mitigation for the rigidity defect: stop printing 'rigidity' as an OPEN '?' item. Show the rigid badge on the PROVEN side when rigidity is established, and show nothing otherwise.

Publishing '?' rigidity against a packing that is visibly rigid makes the panel look wrong to any reader who can see the picture, and the panel's whole job is to say what is known. Silence is the honest rendering of an absent fact.

Blocked-by the investigation in the paired bug only for the permanent answer; this change stands on its own and should land first so the video can be cut.
