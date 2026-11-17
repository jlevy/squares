---
type: is
id: is-01m5qs1s5dgwrm3b9j8vnpzkn3
title: Reword the walk README's generic 'the owner decides the credit' preamble
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T20:18:49.132Z
updated_at: 2026-10-24T20:18:49.132Z
---
Review C of #795 (https://github.com/jlevy/squares/pull/795#issuecomment-6389018390), finding C2 (Low). packing/devtools/intake_ledger.py:2831-2835 renders 'the owner decides the credit' under 'Owner Decisions Needed' in every walk README (16 walks). On the 964ee2b notebook walk the five measured rows (378, 405 refinements; 364, 450, 874 seeded from previous_source by attribution.md's chain rule) all have credit decided, so the sentence reads as an open question it no longer is. Reword the generic preamble (e.g. 'the credit follows the source's stated link under attribution.md's chain rule, and the owner may rule otherwise'), re-render every walk README, and check the renderers' drift checks. Mention in the next #763 reply that 364, 450 and 874 are settled.
