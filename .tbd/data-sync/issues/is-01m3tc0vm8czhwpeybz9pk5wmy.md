---
type: is
id: is-01m3tc0vm8czhwpeybz9pk5wmy
title: "Result popover: the full overview of one result, opened from its row on the homepage and on all-results.html"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:57:27.045Z
updated_at: 2026-10-01T04:50:48.103Z
closed_at: 2026-10-01T04:50:48.101Z
close_reason: "Done in 4123fed05 and 090309910 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. result_overview.result_popover_html: head, claim, the case's number line and packing drawing, the chain of results on the case, site links and GitHub main links (4,087 links to 491 paths, all resolved); written once per result as result/t-nnn.html and fetched on first open, so page weights are unchanged."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: Recent Results (homepage) and the Results tab rows are structured alike and open a popover with the full overview of the result. The overview carries visuals as the film and the workbench show them: the case's number line (verified and reported bounds, gap, the chained bound), the known-best packing drawing, and the proofs and results for the case with links to the right citations and sources. Reuse the atlas popover's film panel and case-view pieces rather than new drawings. Every item links to the relevant part of the website (case record, frontier row, papers) or to the GitHub repository on the main branch (think-eyrk's repo_links): the T-NNN entry in packing/frontier/results.yaml, its source packet and evidence, the frontier case file, and the underlying records for papers and sources (the bibliography / softschema records), with line or anchor targets where the file has them.
