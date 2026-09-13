---
type: is
id: is-01m26ba97xs2scftryvmghp97r
title: The PDF reproduction check validates a fresh pair, not the artifact it ships
kind: task
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-10T19:04:36.861Z
updated_at: 2026-09-13T06:18:27.330Z
---
`render_explainer_pdf --check` draws two fresh renders and compares them. The PDF that is
published is neither of those: `--update` runs first and writes its own render, with a
94-byte receipt, and nothing compares that file with anything. So the check samples the
process and the artifact it ships is a third, unchecked draw.

That is exactly the gap D-490's race lands in. A render that was not finished when it was
captured would ship, and the pair taken afterwards could still agree.

The cheaper and stronger shape is to compare the second render against the file
`--update` wrote, receipt and all, rather than rendering a fresh pair: one render instead
of two in the Pages job, and the comparison then bears on the bytes that are deployed.
Two things to settle before doing it: `--check` is currently runnable without a prior
`--update` (it would have to either require the file or fall back to a pair, and say
which), and the receipt is a function of the page rather than of the render, so it has to
be added to the comparison render rather than stripped from the file.
