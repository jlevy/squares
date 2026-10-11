---
type: is
id: is-01m44qz3phdnc1yfv76nxp6cak
title: "Import evand: the Square Packing Atlas site (evand.github.io/square-packing, incl. problems.html) and repository results since 2eb15455"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
child_order_hints:
  - is-01m44rx09j4dapps52fx9bjjda
hold: null
hold_until: null
created_at: 2026-10-05T00:38:37.009Z
updated_at: 2026-10-05T07:51:16.402Z
started_at: 2026-10-05T00:41:15.310Z
closed_at: 2026-10-05T07:19:51.156Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Retain the site pages (index, explore, compare, bounds, proofs, problems, sources) and the new s12 notes at evand/square-packing 7ff3b21 in a packet, add bibliography keys, write a mapped review of the site's claims against the register (docs/project/reviews/), map each claim: s(20) > 3 + 4 sqrt(2)/3 (2010d63, below wand125's 1959/400), Lean LebMass (LEB/CAP leaves kernel-checked), SpecChelokot, CEILINGS_17_20, open problems/conjectures. evand.github.io is blocked by egress; use the git repository (site/www is the Pages root).

## Notes

Workflow: W1 import, stages 1-3 of packing/campaign/result-import.md, plus a citation review of the site. Branch claude/ecstatic-pascal-pothtx-evand, commits 5c4626b95, 6d48ab842, 4e72c1156 (+ validation fix-ups if any).

Pin: evand/square-packing 7ff3b2113532889708a3baa4d56bc44294022e63 (2026-10-04T20:17:38Z), retrieved 2026-10-05T00:34Z, main at retrieval. evand.github.io blocked by egress; pages read from the commit (site/www = Pages root, s12/docs served under it).
Packet: packing/resources/web/evand-square-packing-2026-10-04 (acquire_source declaration; 69 retained, 2 pinned; --check PACKET_MATCHES_ITS_CONTRACT). Keys: [evand square-packing 2026-10-04], [evand square packing atlas 2026-10-04]. Coverage: evand-square-packing-2026-10-04.

Claim map (claim -> action -> id):
- s(11), s(21), s(32), s(45), s(59), s(60), s(61), s(77), s(78) as site states -> already registered -> T-060, T-052, T-051, T-053, T-066, T-062, T-063, T-067, T-064
- s(k^2-3)=k k>=6 -> already registered -> T-064; s(k^2-4)=k k>=5 -> already registered, reported -> T-081 (replay think-4uir)
- s(k^2-1), s(k^2-2) re-proofs -> already registered -> T-084, T-086, T-085
- s(12) >= 15680000/3949423 -> already registered -> T-079
- s(20) > 3+4sqrt2/3 (point cover side 2443/500, S20_LB.md, REPORT.md) -> below standing 1959/400, stays in packet -> reported evidence E-n020-evand-point-cover-4886-report cited by n-020 only
- pure-cover ceilings n=17-20 (CEILINGS_17_20.md) -> none (method limit by others, not acted on)
- Lean LebMass (689 LEB + 374 CAP leaves of ValidTilt7), ValidSplit7 -> evidence update on T-064 (next_rung, notes, artifacts); no rung moves
- SpecChelokot -> evidence update on T-086 (notes); no rung moves
- floors table n<=100 -> checked: devtools.compare_site_floors, receipt in packet: 99/100 equal verified lane, n=96 = reported T-081, all 20 'verified' marks held, 24 family-ring counts past 100 held
- Guzhou0806 R070/R071 (s(17) > 18641771/4000000, above verified) -> import of its own -> think-1qms
- Kleddamag 4.6601 -> below standing, packet note
- open problems/conjectures -> none (questions), checked in review §5
Review: docs/project/reviews/review-2026-10-05-evand-square-packing-atlas.md (mapped). Non-blocking S-1..S-7 for the author: s(211)<15 listed as target though T-057; n=77 floor credited to k2m4 route; T-043 shown V4/C3; T-060 'independently'; Nagamochi gap credited to Karakus alone; root README stale; zeromargin.roots() latent gap (not hit here).
Stage 7 draft (owner posts, no issue): none filed; reply to Daniel optional with the review's S-items.
