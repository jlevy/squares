---
type: is
id: is-01m5p95exr8s93wbavjwh82m0n
title: "Register claims: 30 credit sentences drop Stromquist, Nagamochi, Burns and Massaccesi from the bibliography's credit line (PR #770 review A2)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T06:21:58.072Z
updated_at: 2026-10-24T06:21:58.072Z
---
Review A2 on PR #770 (https://github.com/jlevy/squares/pull/770#issuecomment-6380669495), deferred part. attribution.md, Credit Text and Lineage: the bibliography's `credit` is the single home of a result's curated credit text, and hand-written prose "does not silently drop authors or antecedents".

30 register entries' `claim` paragraphs credit "Hosono after Tokoharu and Levy" (or "Hiroaki Hosono after Tokoharu and Levy"), while `result_credit.credit_line` for each, read from the bibliography, is "Hosono after Tokoharu, Levy, Stromquist, Nagamochi, Burns, Massaccesi": T-046, T-068, T-069, T-071, T-072, T-073, T-075, T-076, T-077, T-080, T-082, T-090, T-091, T-094, T-096, T-097, T-099, T-100, T-102, T-103, T-104, T-105, T-106, T-107, T-108, T-109, T-110, T-111, T-144, T-179 (counted on 24 October 2026 at the #770 branch after merging main c5697c2f2, by comparing each claim with credit_line). The bibliography was widened on 29 September (a1527e7f0, "name every link the sources' own attribution files name"); the claims were not. The gap predates #770; that PR corrected only the three tracking-issue bodies that copied it (#773, #778, #779).

Do: bring each claim's credit sentence to the bibliography's line (or have it cite the line rather than restate it), re-render RESULTS.md and the views, and add a check that a claim's credit sentence names every name its credit line names, so the drift cannot recur. Other claims may restate a narrower line too (T-234 and T-235 read "Hosono after Daniel" against "Hosono after Daniel, Levy, Stromquist, Nagamochi, Burns, Massaccesi"); the check should find them all. No CPU. Records only; the site's credit cells already print the bibliography's line.
