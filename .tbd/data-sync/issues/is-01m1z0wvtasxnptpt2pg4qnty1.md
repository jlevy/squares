---
type: is
id: is-01m1z0wvtasxnptpt2pg4qnty1
title: Restore the missing formatting hook and normalize owned checkpoint Markdown
kind: bug
status: closed
priority: 1
version: 4
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1ytzagmmx58w96ksbf5j3dj
created_at: 2026-09-07T22:47:50.343Z
updated_at: 2026-09-07T23:09:55.588Z
closed_at: 2026-09-07T23:09:55.583Z
close_reason: Documented pinned hook restoredandverified; whole-root Flowmark normalizationandcheckpassedaftergateended;8d79f9a9committedwithactualhookpass. Noarchiveorunownedsourceformatting. Remainingcertification/publication trackedseparatelythinkm2lx/9cvw.
resolution: null
duplicate_of: null
---
Read-only audit found this checkout has no .git/hooks/pre-commit and no core.hooksPath. Pinned makeformat-check reports10 owned/research Markdown files drift; the prior commits therefore did not automatically format. Restore the documented pinned lefthook2.1.10 install, preserving otherhooks. After running main-checkout gate91336 finishes, root runs makeformat against repo root to preserve archive exclusions, reviews exactchangedpaths, commits formatting, and performs required finalpushvalidation. Do not editmain duringactivegate, toucharchive, useexplicitpathFlowmarkthatbypassesignore, or reportuncheckedformattingaspassed. All correctivework staysPR116.

## Notes

Whole-root pinned Flowmark formatting nowexecuted aftermainpush91336terminalfailure; makeformat exit0 and approvedmakeformat-check exit0. Exactly10ownedresearchMarkdownfiles normalized, archive/generated exclusionspreserved. Hook2.1.10 restoredearlier40s. Rootalsoadds truthfulpost-freeze gatefailures/provenancereview andfixes explicitBC264/thinkmq0d handoff; synopsisfocusedchecknowpasses. Formattingwillbecommittedwithdraftprogress, while canonicalcertifyinggate remainsknownblocker underthink9cvw; do notclaimmergeability.
