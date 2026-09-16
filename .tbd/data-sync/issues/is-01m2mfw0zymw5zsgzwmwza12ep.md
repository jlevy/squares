---
type: is
id: is-01m2mfw0zymw5zsgzwmwza12ep
title: "PR #181 senior review: default-deny guard accepts script-producing BoolOp and lambda"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T06:53:34.588Z
updated_at: 2026-09-16T06:58:00.903Z
closed_at: 2026-09-16T06:58:00.902Z
close_reason: "Completed at PR #181 head 8cc783ec: BoolOp alternatives are merged, local lambda returns are classified conservatively, direct lambdas fail closed, and watched negative controls pass."
resolution: null
duplicate_of: null
---
Novel reproducible bypass in packing/devtools/check_no_embedded_js.py. At lines 464-515, classify marks ast.BoolOp as opaque, so page.evaluate(PROBE or a neutral string literal) produces zero sites even though it can execute the literal. At lines 526-570, a directly called lambda is treated as an external opaque call, so page.evaluate((lambda: a neutral string literal)()) also produces zero sites. Both contradict rule 1's default-deny guarantee and recur beyond the already-closed think-c2u6 cases. Fix by merging BoolOp operand verdicts and classifying locally visible lambda returns conservatively; add negative controls using signature-free script text and watch them fail on the current implementation.
