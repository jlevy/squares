---
type: is
id: is-01m4evm6rm5ay11r282w7qe5k6
title: "n17 BB intake: require complete convex cell enclosure in standalone verifier"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
created_at: 2026-10-08T22:54:58.323Z
updated_at: 2026-10-08T22:54:58.323Z
---
The standalone BB verifier's check_header currently checks equality of the declared
polygon vertex set with the source-cell hull and positive local turns. A pentagram
ordering demonstrates that those checks do not imply complete convex enclosure.
PR404's new check_n17_bb_header wrapper correctly adds the missing prerequisite:
every original source-cell vertex must lie left/on every declared inward edge,
with duplicate vertices and zero edges refused.

Repair the standalone intake or require the same independently checked enclosure
before unrestricted full-BB acceptance. Retain the tiny pentagram control. This is
an inherited proof-boundary weakness, not introduced by PR404 and not evidence
against retained correctly ordered FULL manifests or wrapper-qualified HEADER_ONLY
receipts. H318 documents the distinction; Astra's full pinned1d review confirmed it.

Source: packing/devtools/verify_n17_bb_certificate.py check_header; new guard and
regression: packing/devtools/check_n17_bb_header.py and
packing/tests/test_check_n17_bb_header.py. No new global exclusion or admission.
