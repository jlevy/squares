---
type: is
id: is-01m3w5qd0m087gc37ndp3dyxjs
title: "Defect entry: the deployed site dropped every record link into packing/resources and packing/campaign"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:45:54.579Z
updated_at: 2026-10-01T17:19:55.133Z
closed_at: 2026-10-01T17:19:55.127Z
close_reason: D-512 recorded and check_published_site now holds the published pages to the record links the renderer writes (5d86b9da3, 989670095); merged with jlevy/squares#274. Confirm on the deploy that result/t-060.html links final-composition.json.
resolution: null
duplicate_of: null
---
From the coherence audit, 2026-10-01 (think-ldrb): pages.yml checks out without packing/resources/*/ and packing/campaign/*/, and the renderers asked the disk whether a cited path exists, so the live overview and Results page lacked 20 link targets each, the case records 19, and result overviews their certificate, proof and source-packet rows (T-060 lacked final-composition.json and PROOF.md). check_published_site passed 783 of 783 and could not see it. Fixed in bb82ba141 (links come from the git tree, not the disk), on claude/site-polish-4. Allocate a D-number in packing/defects.yaml with the cause and the missing check; add to check_published_site a check that a result overview carries its record links (after the next deploy, the live result/t-060.html must link final-composition.json).
