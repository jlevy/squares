---
type: is
id: is-01m4f481rmqznv80b5k0s3p6q1
title: Integrate published record updates before the atlas cleanup PR
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T01:25:37.170Z
updated_at: 2026-10-09T02:20:29.009Z
started_at: 2026-10-09T01:52:34.240Z
---
Current origin/main b810432cccf7849920dda3aad76882f191464eb5 includes published PR434, which reuses T-117/T-118 as live Rehwaldt/Couzo results and preserves the withdrawn identities through dated amendments. The cleanup branch retains the older identities and fails the unchanged historical URL check. Independent review proved that transplanting only two URL rows is unsafe: live producers, evidence and selected n68/n105/n292 witnesses also changed. Preserve the current reviewed source, v0.5.0-9695fb exports and preview evidence, integrate the published source in the isolated cleanup branch, resolve conflicts without losing requested layout/legend/orientation changes, then rederive affected records/URL registry/docs, commit and re-pin data, regenerate both export families and the preview, and complete the full push/hosted gates. An earlier automatic approval review refused a local merge because the project's confirm-session merge grant lacked explicit human confirmation. A precise approval request for this local branch integration is pending; do not bypass through record transplantation, rebase or another indirect route. No GitHub PR merge is requested. Keep the older standalone preview clearly labeled by its own recorded data while working.

## Notes

Human explicitly approved the local merge of published main24fe88bc44967970d72f7d1efc9bf2a325b74f17 in this chat, replacing the older b810 request. This resolves the automatic-review confirmation block for that local integration; no GitHub PR merge is authorized. Root will save independently reviewed new information/footer/shared-legend edits from think-idan, then integrate that exact published source, including PR434 n68/n105/n292 refinements and PR439 archived asymptotic reports. Preserve requested layout, n211 horizontal reflection and source/evidence amendment history; rederive coherent current records, commit/re-pin data, regenerate both export families and the maintained preview, then finish full push and exact-head hosted gates plus PR. Current prior9695exports remain available and labeled by their own edition. Stack preflight reports branch is not locally tracked and GitHub confirms no PR currently exists.
