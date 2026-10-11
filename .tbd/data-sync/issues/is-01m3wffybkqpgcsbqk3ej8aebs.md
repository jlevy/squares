---
type: is
id: is-01m3wffybkqpgcsbqk3ej8aebs
title: PDFs and generated files carry the right date
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T19:36:35.954Z
updated_at: 2026-10-01T22:34:35.504Z
closed_at: 2026-10-01T22:34:35.493Z
close_reason: "jlevy/squares#285 merged: the September 29 the owner saw is the review paper's 'Original proof' date, which is right; the stale dates beside it (the papers' revised lines, the poster dateline, PDF metadata from the build clock) each have one derived rule, printed by devtools.artifact_dates and held by tests/test_artifact_dates.py."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'can you confirm the pdf and generated files are using the appropriate date? I saw recent PRs with sept 29 on the pdf.' For every generated artifact that prints or embeds a date (the atlas posters known-best-1-100 and 1-324 in PDF, SVG and PNG; the two papers' PDFs and their 'revised' lines; the films' captions; document metadata such as PDF CreationDate and ModDate; generated Markdown views with 'as of' or 'reviewed' dates): find where the date comes from (a release constant, the data revision's commit date, the build clock, a hand-typed string), what it says today against what it should say (the date of the data it shows), and why a PR on 1 October showed 29 September. Fix each to one documented rule; test it.

## Notes

Answer: the September 29 on a PDF is the review paper's 'Original proof September 29, 2026', which is right (now held to the register's date for T-060). Stale and fixed on jlevy/squares#285: 'This review revised' (30 September, now derived: 1 October); the first paper's 'Last revised' (28 September, now 30 September, the article's last change); the poster dateline (28 September, now the date of its data); PDF CreationDate and ModDate (the build clock, now noon UTC of the artifact's date). devtools.artifact_dates prints the table; tests/test_artifact_dates.py holds each rule.
