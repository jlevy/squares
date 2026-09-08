---
type: is
id: is-01m21c5xaewdteevvk6hr5a6wa
title: "PR127 R3: scope the corner ratio obstruction to the tested site set"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m21badm7ednkkxzwgcjmgaam
created_at: 2026-09-08T20:43:29.998Z
updated_at: 2026-09-08T23:03:18.415Z
closed_at: 2026-09-08T23:03:18.415Z
close_reason: Corrections are committed in ef8a2e72 and cbe9fd76 and documented in docs/project/reviews/review-2026-09-08-pr127-research-readiness.md. The completed checkpoint combines actual passing cbe9fd76 fast, negative-control, slow and exhaustive receipts with four unchanged geometry passes from the failed ef8a2e72 full run. Scientific limits and unrun complements remain explicit.
resolution: null
duplicate_of: null
---
Lane A 1440-1444 and 1511-1515; agenda030 73-76; synopsis: universal lambda=1 obstruction is not proved. Every slice with wf=1 normalizes by T=4wc+7 to ratio M/T=1+(M-4wc-7)/T. Thus negative slice implies ratio<1. Conversely successful ratio has wf>0 because four disjoint admissible cores at chosen marks exclude wf=0; divide by wf. Formulations have identical exclusion power; preserve exact site-A dual=1 obstruction and the better numerical gap resolution of slice form.
