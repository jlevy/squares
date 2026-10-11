---
type: is
id: is-01m3w25rbcb5xh7xn9h849amg5
title: "Coherence audit: the site, README and PR stack against current main's data"
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:43:50.623Z
updated_at: 2026-10-01T16:45:58.662Z
closed_at: 2026-10-01T16:45:58.660Z
close_reason: Audit complete; fixes merged into claude/site-polish-4 at 422ec9c12; follow-ups filed as their own beads.
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'make sure everything is coherent and up to date with the current data, including the things that have been merged upstream every time.' On the top of the design stack (claude/site-polish-3 with origin/main b82e4b30a merged): build the site and check every number and statement a reader sees against the register, the case records and what main merged since f9a3409f0 (math migration; the n = 11 paper review, #261; the W3 transfer plan with new n = 17 evidence, #265): result counts, rung counts, recent-progress text, the Papers page and homepage cards for the paper, the frontier table, the atlas stamp and DATA_REVISION, links to merged documents, stale phrases (Verification at a Glance, 'current best' chip, lineage headings, 'not a bound', V4/C5 for T-060). Fix what is stale on branch claude/site-coherence; list what needs the owner.

## Notes

Audit done on claude/site-coherence (e8fc0acfd, ten commits), merged into claude/site-polish-4 (422ec9c12). Counts all matched the data. Fixed: record links independent of the checkout (the deployed site was dropping links into packing/resources and packing/campaign); SYNOPSIS at V3/C3 for T-060 and eleven headline results; n = 11 results link the optimality paper first; README figure wording; an 'established' date label; development.md's 86 steps; the spec's as-built notes. Left for follow-up beads: old-ladder mentions in register notes and case records; the unregistered n = 17 certified upper bound; a defect entry for the dropped links; small stale facts. Live check: 783 of 783.
