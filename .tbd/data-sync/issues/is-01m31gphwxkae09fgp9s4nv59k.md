---
type: is
id: is-01m31gphwxkae09fgp9s4nv59k
title: transport_ceiling_family silently strips variant and corner_clip
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:11.484Z
updated_at: 2026-10-06T08:48:44.093Z
---
PR 207 re-review residual; pre-existing, same invariant H1 protects. transport_ceiling_family.py:45,81 reads a family with CeilingCertificate.from_record and emits family.to_record(), which (ceiling.py:288-304) writes only n / outer_side / square_side / half_tangents / placements. Run on the retained class family at --scale 1: exit 0, output contains zero occurrences of variant or corner_clip. The class hypothesis is stripped and the stripped bytes then read as the unconditional program at every reader. Nine other devtools take a family through from_record with no variant check.

## Notes

2026-10-06 bead review: think-iy6r (think-nalh, filed later the same day from the same PR 204-209 review) was closed as a duplicate of this bead. Re-checked on origin/main eb43ffe9a: still unfixed.
