---
type: is
id: is-01m32dwb67ww7mszq1w6nf2f4c
title: transport_ceiling_family strips the class hypothesis (PR 207 residual 1)
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:09.927Z
updated_at: 2026-10-06T08:47:38.962Z
closed_at: 2026-10-06T08:47:38.962Z
close_reason: "Duplicate of think-mhhr (older): both are PR 207 residual 1, transport_ceiling_family stripping variant and corner_clip. Still unfixed on origin/main (from_record/to_record at lines 45 and 81)."
resolution: duplicate
duplicate_of: is-01m31gphwxkae09fgp9s4nv59k
---
transport_ceiling_family.py:45,81 reads a family with CeilingCertificate.from_record and emits family.to_record(), which (ceiling.py:288-304) writes only n/outer_side/square_side/half_tangents/placements. Run on the retained class family at --scale 1 the output contains zero occurrences of variant or corner_clip: the class hypothesis is stripped, and the stripped bytes then read as the unconditional program at every reader. Nine other devtools take a family through from_record with no variant check. Same invariant H1 protects, reached by a tool neither the review nor its fix enumerated. Pre-existing, not introduced by PR 207.
