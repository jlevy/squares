---
type: is
id: is-01m41ephbrdagjrq2q882d007z
title: Measure what drives the repository's growth, and what would slow it
kind: task
status: closed
priority: 2
version: 4
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:58:55.608Z
updated_at: 2026-10-03T18:51:27.789Z
closed_at: 2026-10-03T18:51:27.789Z
close_reason: "Measured (lane D, session-169): size is PDFs, gzip archives and PNG posters, not PR history; squashing or a squash-merge policy is not the lever. Four owner decisions filed as beads."
resolution: null
duplicate_of: null
---
Owner concern, 2026-10-03: the repository is growing large (about 912 MB packed). Measured for PR 305: its whole history packs to 6.40 MB over main and a single squashed commit to 5.87 MB, so squashing saves about 0.5 MB and would break session-168's certified gate ancestry and about 30 recorded commit references; the PR's bytes are its content (regularized views 2.9 MB packed, already gzip and no smaller as plain YAML; SVG drawings 1.4 MB). Measure the whole repository: packed bytes by path family over all history and for the current tree, growth by month, the largest single objects, which families redraw or rewrite often, what a default clone, a shallow clone and the Pages sparse checkout transfer; then rank the options by bytes saved and cost: slimmer SVG encoding (each square written twice with 28-digit coordinates), compact layouts, packet storage (devtools.retained_data), moving bulky archives out, a squash-merge policy for data-heavy PRs, partial-clone guidance, and whatever else the numbers show. Read-only; the owner decides.

## Notes

2026-10-03, lane D (session-169), measured read-only; scripts and outputs in the session scratchpad laneD/ (not retained; OR-1 would put a repeatable version in a devtools tool if wanted).
- Everything GitHub holds packs to 950 MB (GitHub reports 958,299 KB); main plus tags 734 MB; branch-only data 217 MB. A better repack gains 3%. Commits and trees are 8.6 MB.
- 87% of packed history is PDF (344 MB), gzip (323 MB) and PNG (155 MB), which git cannot compress. Families: resources/papers 294 MB (252 MB in one commit, ffa6d01c2, the week of 7 Sep), atlas posters PNG/PDF 200 MB (691 versions), resources/web packets 146 MB, X048 pilot certificates on PR 307's branch 116 MB, transfer/ on replay branches 57 MB, campaign/series 38 MB. About 95% arrived after 1 Sep.
- Growth: main +191 MB and all refs +389 MB in the week to 3 Oct; across refs 250 MB of it gzip certificates, receipts and transfer shards. Poster churn (about 1.6 MB a redraw, 67 redraws 29 Sep to 1 Oct) was stopped by PR #285.
- Text churn is cheap: SYNOPSIS.md 1,150 versions in 1.27 MB; all frequently rewritten text under 5 MB.
- Transfers: default clone 950 MB (also every CI job with fetch-depth 0: six jobs per PR push, about 5.7 GB); single-branch main 734 MB; blobless 512 MB; depth 1 507 MB; Pages sparse 46 MB.
- Branches: 77 ahead of main hold the 217 MB; open PRs unique over main: 307 115.5 MB, 311 21.7, 292 19.5, 305 6.7; 76 session/replay branches without a PR hold 60.6 MB (mostly transfer/), and beads cite 26 of their commits. PR refs keep every PR's objects on GitHub regardless of branch deletion.
- Side results: gzip saves working tree, not repository (1% from git's zlib); xz is 28-38% smaller than gzip on the largest archives; slimming per-n SVG drawings saves 74% of their future history but they are about 1% of the repo; squash-merging every PR since the start would have made main 15% smaller (mostly poster versions #285 already stops), and breaks recorded SHAs; rewriting history is the only way to recover the existing bytes.
Recommendation: decide PR 307's 115.5 MB before merging (it would take the repository past about 1 GB); a policy for bulk retained data (report bytes added per PR in CI; files of 1 MB or more to release assets or a data repository with their digest; xz for new archives); delete imported replay/transfer branches after checking bead citations; fetch only main and the PR head in the six full-history CI jobs. Keep #285's poster policy. Each is filed as its own bead for the owner.
