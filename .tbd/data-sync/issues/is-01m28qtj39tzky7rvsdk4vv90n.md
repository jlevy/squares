---
type: is
id: is-01m28qtj39tzky7rvsdk4vv90n
title: The badges become icons on the line they qualify
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T17:21:41.992Z
updated_at: 2026-09-11T17:21:41.992Z
---
The badges sit in a row of their own, four lines below the fact they are about, each with its label spelled out: 'O optimal   = exact   R rigid'. The owner wants them as icons beside the assertion itself -- s(324) = 18 followed by the marks that say this value is optimal, exact and rigid.

That is better than it sounds, because it says WHICH line each badge qualifies. Today the row is a property of the n; on the line it becomes a property of the statement, and the two are not the same: 'optimal' and 'exact' are claims about the side that PROVED states, while 'rigid' is a claim about the packing rather than the number.

To settle while doing it: does the star (a lower bound first proved here) move onto the lower-bound line by the same argument? It already sits directly under that line, which was the owner's earlier fix, so probably yes -- and then the star-line slot goes too.

Labels: the glyphs alone are not self-explaining, so either a legend somewhere quieter, or the label appears on hover (which the video cannot use), or the labels stay and the row simply moves up beside the value. Worth deciding with the panel in front of you rather than in the abstract.

In template.html: the .badges block and buildFacts's badge loop; the marks themselves are already drawn from the atlas's own 19-unit box and need no change.
