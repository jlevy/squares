---
type: is
id: is-01m1z0wvtasxnptpt2pg4qnty1
title: Restore the missing formatting hook and normalize owned checkpoint Markdown
kind: bug
status: open
priority: 1
version: 2
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1ytzagmmx58w96ksbf5j3dj
created_at: 2026-09-07T22:47:50.343Z
updated_at: 2026-09-07T22:50:08.541Z
---
Read-only audit found this checkout has no .git/hooks/pre-commit and no core.hooksPath. Pinned makeformat-check reports10 owned/research Markdown files drift; the prior commits therefore did not automatically format. Restore the documented pinned lefthook2.1.10 install, preserving otherhooks. After running main-checkout gate91336 finishes, root runs makeformat against repo root to preserve archive exclusions, reviews exactchangedpaths, commits formatting, and performs required finalpushvalidation. Do not editmain duringactivegate, toucharchive, useexplicitpathFlowmarkthatbypassesignore, or reportuncheckedformattingaspassed. All correctivework staysPR116.

## Notes

Hook portion completed high worker22:48:14–22:48:54 UTC40s: makehooks-install uses pinnedlefthook2.1.10, exit0, executablepre-commit2233bytes, sh-npasses, installedversion2.1.10.14samplehooks preserved; no activehookoverwritten ortrackededit. Root stillmust waitactualcleanmainpush91336completion, then whole-root makeformat, inspectownedpaths, commit andrunlatestpushbeforepublication. Makeformat-check earlieractualexit2fromuvcachepermission, approvedrerunactualexit1listed10ownedresearchdocs; no formattingpassclaimed. Futurehookcachedeletionmayrequirereinstall.
