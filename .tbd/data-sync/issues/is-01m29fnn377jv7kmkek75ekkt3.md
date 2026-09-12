---
type: is
id: is-01m29fnn377jv7kmkek75ekkt3
title: The bar marks its values with vertical rules, not just arrows
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T00:18:27.044Z
updated_at: 2026-09-12T00:18:27.044Z
---
Owner's design, 2026-09-11: 'On the bar visual, we should have vertical bars that are bold and black on the lower and higher bounds. There should be vertical bars that are a little darker gray on the relevant numbers, including the integers that are near there, as well as the square root of n and the square root of n + 1.'

Two weights of vertical rule, which is what a scale wants and what the bar does not have:

- **Bold black** at the proved lower bound and the best known upper bound. A triangle points AT a value; a rule IS the value, and at the widths in play the apex is a few tenths of a unit of guesswork. The scarlet and green arrows stay -- they are what says which bound is which -- with the rule giving the position exactly.
- **A little darker grey** at the scale's reference marks: the two ends the bar already ticks, and every integer that falls inside the span. For n = 26 the span is 5.10 to 6.10, so 6 sits inside it and should be marked and labelled; for many n no integer falls inside at all, and then there is nothing to draw.

Watch the end ticks' weight while doing this. The owner has already said once that quiet end ticks read better than the black marks an earlier revision had, so 'a little darker' means a step from --quiet-rule toward the ink, not all the way to it.

The integer labels are diagram labels: sans, the bar's small size, ink rather than a bound colour, since an integer is neither bound.
