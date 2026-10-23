---
type: is
id: is-01m5mz8g2y73hxc578abyx90s4
title: "Fang inventory: a Göbel column beside the recorded rows (deferred from #754 review A2)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T18:09:37.374Z
updated_at: 2026-10-23T18:09:37.374Z
---
Deferred from PR #754, review A, A2 (https://github.com/jlevy/squares/pull/754#issuecomment-6369572454), by coord-intake-1023's decision of 23 October 2026.

**The owner's answer** (think-8krd, as coord-intake-1023 recorded it): "YES, Goebel's classical constructions count as earlier reports beyond n = 324 (the baseline): a rational row above Goebel's exact side is not recorded."

**What #754 does.** `cases/asymptotic/fang_excess_inventory.read_record` stays on recorded rows: the case records and each current beyond-horizon row (`check_source_coverage.current_beyond_horizon`). The deficiency comparison measures excess over what the record holds, not over a baseline, and its docstring says so. Göbel's construction has no row, so the inventory does not read it. Since #754 marks the rows at 369 and 376 above-classical-construction, a fresh `--write` reads those two counts as having no recorded row. The frozen receipt is unchanged; `--check` rebuilds from the values frozen in it.

**Why it is deferred, not done.**
- A Göbel column would change what the comparison measures: from rows the record holds to the best sides it knows.
- The inventory's table runs k = 15 to 72, so counts to 5184. The retained Göbel program reaches 1073 (`intake_ledger.goebel_reach`).

**If taken up:** add a separate column, k^2 - m - 1 for the largest m <= k^2 below k with Göbel's construction included, beside the record's own. Do it through 1073 only, or after think-llit extends the program. Write it in a new receipt format, so the frozen receipt keeps its meaning.
