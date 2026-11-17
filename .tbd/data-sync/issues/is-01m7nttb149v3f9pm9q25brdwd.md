---
type: is
id: is-01m7nttb149v3f9pm9q25brdwd
title: "n-146.md and similar adopted case records: the generated 'The packing' section still names the Kingbird catalogue's finder (Cantrell at 146) after the house moved"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-17T22:42:37.220Z
updated_at: 2026-11-17T22:42:37.220Z
---
Review A3 of #1011. frontier/n-146.md's '## The packing' section says 'Found by David W. Cantrell in 2025, via an unrecorded method. Its side length is algebraic of degree 16', which describes the Kingbird catalogue's packing, not the case's house T-187 (Evan Daniel's from Ryan Xu's, rational), against the record's own found_by: Evan Daniel. Measured on 17 November 2026 (packing/resources/web/de-winter-s292-upper-bound-2026-11-16/measure/identity-n146-lineage.json): T-187 is not Cantrell's arrangement (no symmetry pairs them, 58 squares beyond a tenth; Cantrell's 36 tilted squares lean 18 each way, T-187's 37 one way) and pairs one to one with PingYou Ltd's refinement of Barnett's refinement of Xu's packing. The section is written by devtools.generate_frontier_case (about 31 case records carry 'via an unrecorded method'); fix the generator so an adopted case's packing section names its house's finder (or the earlier packing as history), regenerate, and check every adopted case. #1006's issue quoted the stale sentence.
