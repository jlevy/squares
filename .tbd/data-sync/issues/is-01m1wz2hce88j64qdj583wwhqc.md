---
type: is
id: is-01m1wz2hce88j64qdj583wwhqc
title: Review Mira-acc/17squares, stanislavfort/17squares and anabologyco-maker/square17-lower-bound against the n = 17 record
kind: task
status: closed
priority: 1
version: 4
labels:
  - n17
  - sources
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T03:37:30.254Z
updated_at: 2026-09-07T04:21:48.241Z
closed_at: 2026-09-07T04:21:48.237Z
close_reason: "Three repositories checked out to attic/ with the checkout shortcut and archived under packing/resources/web/n17-github-certificates-2026/ with a README, replay scripts and receipts: Mira 4.468292 and Fort 4.456575 (exact 16-point certificates) replayed by their pure-Python checkers, valid; anabologyco 4.5705 source-backed only (Boost and Lean absent; two Python stages pass; the repository's shrink reduction cannot reach its wall-line atoms). None displaces T-019's 4.59, but 4.5705 was public before T-019, so T-019's prior-value claim and movement figure were corrected to 0.0195 and three evidence entries were added."
resolution: null
duplicate_of: null
---
Requested 2026-09-07: check out https://github.com/Mira-acc/17squares into the attic with the tbd checkout shortcut, review what it contains (bounds, packings, certificates, code), compare against the n = 17 holdings (Bidwell 4.67553009360455 upper; T-019 4.59 lower; Burns 4.4811, Massaccesi 4.5058, Brandwijk 89/20; Burns near-record 4.677648), and say whether anything is new and worth incorporating.

## Notes

2026-09-07 second pass: three GitHub repositories cloned to attic/ and archived under packing/resources/web/n17-github-certificates-2026/ (about 7.1 MB; Fort's raw certificate and four anabologyco files over 1 MB XZ-compressed with raw SHA-256 recorded; anabologyco legacy/ omitted, retrievable at tag v0.1.1; Mira's first 4.450837 package not extracted). Replays: Fort pure-Python checker VALID (20 s); Mira pure-Python checker VALID over 122,626,747 nodes (3 min 34 s); anabologyco SHA256SUMS 76 OK, certificate-arithmetic and Bernstein-filter stages PASS, decisive Sturm/endpoint/coverage stages need Boost (install declined) and Lean 4.33. Repository's own sweep refuses anabologyco's 560 atoms at least mass 0.0245 (direction 0) because its atoms sit exactly one unit from the walls, which the shrink drops: reduction artefact, not evidence against. Correction owed: T-019's 'no public bound above 4.5058' and '+0.0842' are wrong; 4.5705 was public on 16 Aug, movement 0.0195. Three sub-agents writing the packet README, the register edits and the review addendum.
