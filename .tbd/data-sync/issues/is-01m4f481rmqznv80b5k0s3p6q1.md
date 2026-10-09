---
type: is
id: is-01m4f481rmqznv80b5k0s3p6q1
title: Integrate published record updates before the atlas cleanup PR
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
created_at: 2026-10-09T01:25:37.170Z
updated_at: 2026-10-09T01:25:37.170Z
---
Current origin/main b810432cccf7849920dda3aad76882f191464eb5 includes published PR434, which reuses T-117/T-118 as live Rehwaldt/Couzo results and preserves the withdrawn identities through dated amendments. The cleanup branch retains the older identities and fails the unchanged historical URL check. Independent review proved that transplanting only two URL rows is unsafe: live producers, evidence and selected n68/n105/n292 witnesses also changed. Preserve the current reviewed source, v0.5.0-9695fb exports and preview evidence, integrate the published source in the isolated cleanup branch, resolve conflicts without losing requested layout/legend/orientation changes, then rederive affected records/URL registry/docs, commit and re-pin data, regenerate both export families and the preview, and complete the full push/hosted gates. An earlier automatic approval review refused a local merge because the project's confirm-session merge grant lacked explicit human confirmation. A precise approval request for this local branch integration is pending; do not bypass through record transplantation, rebase or another indirect route. No GitHub PR merge is requested. Keep the older standalone preview clearly labeled by its own recorded data while working.
