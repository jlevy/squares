---
type: is
id: is-01m2hh8q8m73b1zqc39tje43ce
title: "PR #160 review D87: leftovers from the page removals"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:15.891Z
updated_at: 2026-09-15T03:32:54.055Z
closed_at: 2026-09-15T03:32:54.054Z
close_reason: "Fixed on PR #160 in bf0b8ed7: stale headline and type-scale comments rewritten, _HEADLINE_DIGITS removed, will-change and the duplicate .star-line .note rule dropped, the blank array line removed; no visible change."
resolution: null
duplicate_of: null
---
Canonical defect D87 from the 2026-09-14 stack triage (Low). Source: #155 R19 (the two template items and two stray blank lines are gone in #160; the `facts_opacities.js` item is D67, lane D-tools).

Leftovers from the page removals: stale comments contradicting the still `n =`, dead CSS (`.numeral { will-change: transform }`, the overridden `.star-line .note` colour), "34 the exact line", an over-long comment line, a blank line inside an array.

Files: `packages/workbench/src/view/facts.ts` (:91-99, :125), `packages/workbench/src/application.js` (:561-566), `packages/workbench/assets/workbench.css` (:157-161, :297-309, :370, :484-493), `packages/workbench/probes/candidate/type_and_fit.js` (:42) @bb3f7c99. Related: think-4yow.
