---
type: is
id: is-01m4fp0v4fwzdjbggyqyypn1vy
title: Rehwaldt n68 packet retains and executed unlicensed author programs
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T06:36:15.375Z
updated_at: 2026-10-09T07:06:11.560Z
---
Round-2 review I: main's rehwaldt-n68-refinement-2026-10-07 packet retains source/verify.py.txt and independent_support_check.py.txt byte-identically from lollipoll/certified-square-packing-68 (no licence) and its receipt records jobs running those programs; its rows still read metadata-and-derived-numerical-facts-only. Decide whether to keep them in Git or only in custody, and whether execution was owner-approved.

## Notes

The issue-425 (rehwaldt-couzo-refinements-2026-10-07) packet's admission receipt also records the same three n68 jobs running verify.py and independent_support_check.py. #442 known-best-packings README now names this exception (38058813).
