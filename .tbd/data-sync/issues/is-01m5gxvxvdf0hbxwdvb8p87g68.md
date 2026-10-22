---
type: is
id: is-01m5gxvxvdf0hbxwdvb8p87g68
title: "PR #718 review B follow-ups (B1-B7): stale 229 prose, a test for adopt_houses._retained_672, 227 credit wording, n-103 commas, _walls sentence, two wordings, t-180 budget runway"
kind: task
status: in_progress
priority: 2
version: 2
delegate: coord-intake-1021b
labels:
  - records
dependencies: []
parent_id: is-01m5frzavxzvcqht1tf2edbfxp
hold: null
hold_until: null
created_at: 2026-10-22T04:28:19.181Z
updated_at: 2026-10-22T04:28:20.143Z
started_at: 2026-10-22T04:28:20.142Z
---
Review B of #718 (https://github.com/jlevy/squares/pull/718#issuecomment-6332701148, follow-up round 2 at c3ede79e2) found 7 Low items, deferred to the next records change (PR-B on claude/intake-2026-10-22, think-2vjc/think-f28n/think-pvav):
B1 results.yaml prose still describes 229 before #718: T-196 notes (:27625 'at 229 the case keeps T-199', :27611 'the case's ceiling'), T-198 notes (:27818 'houses the count'), T-199's and T-223's adoption sentences (:27938, :30585) should say T-225 replaced them on 22 October.
B2 add a unit test for adopt_houses._retained_672 plus assertions on n-229's body (check() reads front matter only).
B3 T-225's claim (results.yaml:30801-30807) and the packet README (:242-248) list 227 among 'Francisco Couzo's' packings; align with CREDITS[227] (de Winter's packing as refined in Couzo's #672 report).
B4 the doubled comma at n-103.md:239 and :418 (history text from the 11 October pass).
B5 _walls changed 'and every pair by at least' to 'and every pair clears by at least', differing from 52 recorded atoms; restore or migrate with a test.
B6 'is the house since' -> 'has been the house since' in T-227's claim and next_rung; n-227 '#672 report, reported in'.
B7 record the t-180 page budget's runway (450,000 against 402,418 at #718; ~1.5 KB per result, ~32 results) and name the bead that owns it.
blocked_on: none
