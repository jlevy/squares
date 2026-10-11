---
type: is
id: is-01m33wqgta1yxt025003j21wmw
title: Correct the finder recorded for n = 1 and n = 6, and reconcile the source-key spellings
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies:
  - type: blocks
    target: is-01m33vv50vj12ze4pka71nbqd8
parent_id: is-01m33vv4hs6kbe1c349y8wsgsf
created_at: 2026-09-22T06:26:54.921Z
updated_at: 2026-10-06T08:31:53.458Z
closed_at: 2026-10-06T08:31:53.458Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): a4bdfae4c corrected n = 1 (found_by now empty, catalogue 'Trivial') and n = 6 (Kearney) and reconciled the source-key spellings; packing/resources/README.md lists [Stromquist Memo I], [Schadt n=29 repository], [Ellsworth SVG], [Kingbird n=5 SVG], [Kingbird n=29 SVG]
resolution: null
duplicate_of: null
---
Found by the citation survey (2026-09-21). n = 1 records Goebel 1979 as its finder (packing/frontier/n-001.md:22-24) where the catalogue capture says Trivial (packing/resources/web/kingbird-squares-in-squares.md:21-25); n = 6 records Friedman 1999 (n-006.md:22-24) where the capture credits Kearney and Shiu (48-53). In both the credit belongs to the next catalogue entry. Source keys are also spelled differently across files ([Schadt n=29 repository] vs [Schadt n29 2025]; [Stromquist Memo I 1984] vs [Stromquist Memo I]; [Ellsworth SVG], [Kingbird n=5 SVG] and [Kingbird n=29 SVG] missing from packing/resources/README.md). Fix at the source records, through the generator that owns them, before the citation data is generated from them.
