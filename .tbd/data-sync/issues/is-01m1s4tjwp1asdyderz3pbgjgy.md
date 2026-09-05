---
type: is
id: is-01m1s4tjwp1asdyderz3pbgjgy
title: "Frontier docs overstate the certified-ceiling gap: 30 cases and 0.46 versus the measured 18 and 0.4286"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T16:01:03.382Z
updated_at: 2026-09-05T16:01:03.382Z
---
Survey 2026-09-05: frontier/README.md:137-139, square-packing-case.schema.yaml:129-131 and tests/test_verified_upper_bound_contract.py:6-7 each say the certified ceiling trails the best known side for about a third of n<=100 by up to 0.46-0.47, and that every such case carries a mathematics blocker. Measured, and asserted by that same test at :230 and :234: 18 cases, worst gap 0.4286 at n=50, and n=68 and n=69 carry source-evidence blockers rather than mathematics. The schema text matters most, being the contract a consumer reads.
