---
type: is
id: is-01m4f481rmqznv80b5k0s3p6q1
title: Integrate published record updates before the atlas cleanup PR
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: blocked
hold_until: null
created_at: 2026-10-09T01:25:37.170Z
updated_at: 2026-10-09T01:53:45.804Z
started_at: 2026-10-09T01:52:34.240Z
---
Current origin/main b810432cccf7849920dda3aad76882f191464eb5 includes published PR434, which reuses T-117/T-118 as live Rehwaldt/Couzo results and preserves the withdrawn identities through dated amendments. The cleanup branch retains the older identities and fails the unchanged historical URL check. Independent review proved that transplanting only two URL rows is unsafe: live producers, evidence and selected n68/n105/n292 witnesses also changed. Preserve the current reviewed source, v0.5.0-9695fb exports and preview evidence, integrate the published source in the isolated cleanup branch, resolve conflicts without losing requested layout/legend/orientation changes, then rederive affected records/URL registry/docs, commit and re-pin data, regenerate both export families and the preview, and complete the full push/hosted gates. An earlier automatic approval review refused a local merge because the project's confirm-session merge grant lacked explicit human confirmation. A precise approval request for this local branch integration is pending; do not bypass through record transplantation, rebase or another indirect route. No GitHub PR merge is requested. Keep the older standalone preview clearly labeled by its own recorded data while working.

## Notes

Claim published and current source/export work safely committed at 7900aafad. Strong review and a separate scientific footprint audit established that PR434 in main b810432cc changes selected n68/n105/n292 witnesses, exact side bounds, live evidence producers, bibliography, derivatives and URL amendment histories. Historical URL check is the sole current edit-tier failure. URL-only transplantation cannot safely fix it. Exact local merge approval question remains unanswered; only the distinct local-preview-server approval has arrived. Do not merge, rebase or copy upstream source as an indirect workaround. After explicit local approval, integrate b810432cc, rederive the three affected cases while preserving n211, commit/re-pin coherent records, regenerate both export families and preview, update expected counts and twenty-name credits, then run full publication gates and create the clean PR. No GitHub merge is authorized.
