---
type: is
id: is-01m5jr2g54r568rrq3yg3dwj6w
title: Cut the results and atlas pages' DOM size
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-22T21:25:31.939Z
updated_at: 2026-10-22T21:25:31.939Z
---
After the quick fixes, the remaining non-prerendered cost is layout of a very large DOM: results 22,560 elements (13,011 spans, 742 math instances), atlas 13,726. First layout ~370-570 ms on results. Options to evaluate: content-visibility:auto on collapsed day sections, lazily rendered table rows, lighter math markup. Root/body/main :has() rules and atlas-view's root dataset writes were tested and made no measurable difference.
