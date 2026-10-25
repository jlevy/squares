---
type: is
id: is-01m5rt5tsxbxfb0b3n9mrtqs01
title: "Exact configurations at 172 and 263 in Q(S*): a KKT/number-field builder (W7-style) or the author's configurations"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
deferred_until: 2026-11-08T00:00:00.000Z
created_at: 2026-10-25T05:57:44.893Z
updated_at: 2026-10-25T05:57:44.893Z
---
T-244 (issue #804, Hyukdong Kim) registers s(172) <= S*_172 and s(263) <= S*_263 as reported, V0/C0: each S* the root of an irreducible polynomial of degree 24 and 17 that #804 found by KKT closure and LLL from T-174's witnesses (atlas inputs equal to binary64). Nothing exact shows a packing at either side yet. This bead gets an exact configuration at each side, every centre and half-angle tangent in Q(S*) (or a field holding S*), so that sqpack.witness.exact_verify and a second route can decide it (T-244's unfinished confirmation, about 2 CPU-hours, up to 8, on both routes).

Two routes, in order:
1. The author's configurations. The acknowledgement on #804 (draft in think-9vai's notes, posted by the coordinator after the import PR merges) asks for them, in Daniel's n-N.minpoly.json.gz format or as the 3,000-digit KKT points with active set and sign branches. Wait 14 days from the merge for an answer (deferred to 2026-11-08).
2. Otherwise a W7-style builder here: a KKT closure with multipliers on the house's active set (sqpack.promote.system.close adds no first-order condition; the vendored exactsolve.py solves at mpmath precision only as a generator), a Newton solve at about 2,000 to 3,000 digits, and one integer relation per coordinate in Q(S*): about 516 at 172 and 790 at 263.

Price, against the 40 CPU-hour item cap: about one agent-day of tooling, plus 10 to 100 CPU-hours at 172 without python-flint (mpmath PSLQ at dimension 26 and thousands of digits), less at 263 (degree 17). The upper end is over the cap, so route 2 needs the owner's budget or python-flint in the lock (a dependency change, supply-chain review first) before it runs. A cheaper rigorous fallback, which gives no exact value, is a Krawczyk enclosure of the closed KKT system with sqpack.promote.interval_verify: s(n) <= a rational just above S*.

Done when: an exact configuration at each side is retained and decided (T-244 to C3 by its replay), or the route is declined with a reason recorded on T-244's next_rung.
