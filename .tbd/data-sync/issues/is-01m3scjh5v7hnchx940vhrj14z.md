---
type: is
id: is-01m3scjh5v7hnchx940vhrj14z
title: Measure live CI wall time despite missing step timestamps
kind: bug
status: closed
priority: 1
version: 7
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-30T14:47:51.737Z
updated_at: 2026-09-30T15:23:38.499Z
closed_at: 2026-09-30T15:23:38.498Z
close_reason: Published b6c97667b and verified in hosted runs36735084578/36735084788. Solved n11 consumer and SVG/PDF/page checks pass. The live wall audit now reports its conservative265s endpoint and correctly propagates the separate suite-B budget failure; no timestamp observation defect remains. Remaining integration work is third-shard capacity think-o18s under think-fjdd and final certification think-niqx.
resolution: null
duplicate_of: null
---
At c32fd6f73, allindividualchecks andPages pass; Packing run36730867640 aggregate failed solely because jobsAPI omitted the live wall-step started_at for3reads. Add bounded specific eventual-consistency retry with refusal after exhaustion; preserve required-prerequisite and mixed-cohort safeguards and unchanged cost limits. Focus tests, publish and require full aggregate green.

## Notes

Published b6c97667b replaces unsuccessful extended API retries with an explicitly labeled process-invocation upper bound only for the identified live PR run/job/attempt. Complete cohort, timestamp ordering, matrix identities and prerequisite guards retained; historical/sample paths remain API-only and budgets unchanged. Root reviewed; 80 focused tests in 0.49s, Ruff and BasedPyright clean. Awaiting required hosted checks.
