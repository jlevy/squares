---
type: is
id: is-01m0p6bznw805stvdkvz5rmp1a
title: "PR #5 review D-4: file the allOf-under-enforced softschema limitation upstream"
kind: task
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:36.987Z
updated_at: 2026-08-23T02:45:36.548Z
closed_at: 2026-08-23T02:45:36.532Z
close_reason: "FIXED. Filed as jlevy/softschema#41 with a minimal repro. Characterising it before filing sharpened the finding: the allOf conditional does not merely fail to fire, it masks the violation it was meant to catch — a document that genuinely breaks the if/then rule reports the same generic enforcement_unsupported message as a conforming one. Removing the allOf makes the identical document validate; soft and permissive validate it either way, so the fault is specific to the enforced-closure path. The workaround comments in both experiment schemas, contract.md and conventions.md now cite the issue."
---
DEFERRED: filing an issue on jlevy/softschema is an outward action on another repository and needs an explicit go-ahead. The limitation is measured and reproducible: softschema 0.6.2 rejects any allOf object composition under status: enforced with enforcement_unsupported, so a conditional invalidates every artifact rather than the offending one. Distinct from softschema#38. Minimal repro available; the workaround (cross-field rules in ledger.py) is documented in experiment.schema.yaml and should cite the issue number once filed.
