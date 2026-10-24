---
type: is
id: is-01m3gy5qb0vnehs3n8hk3skn6p
title: "Explainer PDF: one KaTeX glyph's baseline moves between page loads, past D-490's draw-twice containment"
kind: bug
status: in_progress
priority: 1
version: 5
delegate: ci-followups
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-27T08:02:16.543Z
updated_at: 2026-10-24T13:29:20.785Z
started_at: 2026-10-23T04:52:09.582Z
---
PR 235 pull_request run 36126482461 (attempt 1, head de282a855, records-only) failed the Pages `pdf` job at `render_explainer_pdf --check-artifact`: `849931 then 849931 bytes, normalised; length delta 0 ... first difference at byte 514532, in object 144`, inside a FlateDecode stream. The unchanged rerun (attempt 2) passed, and `pages-required` then refused the partial rerun as unmeasurable, by design. D-509 records it; it recurs D-490 (think-ptit, think-a5qp).

The retained pair (artifact 10859178879) could not be downloaded from the session: the proxy refuses the Actions blob host. From the log alone: the two 64-byte windows agree for 32 bytes, then the second stream is the first shifted two bits earlier, which is a small change to the inflated text, the size of a changed number.

Local reproduction, prepared page built at de282a855, Chromium 141.0.7390.37 (not the pinned 151 headless shell): about 80 page loads through the maintained `--check --renders N` CLI gave four between-load disagreements, and no within-load repeat at all. Inflated, every one was a single `Tm` line in one page content stream: one KaTeX_Main glyph of prepared inline math (≥ in `s(11) ≥ 191/50 = 3.82`, ∣, =, =) moved 0.21875 or 0.1875 px vertically, a different glyph and page each time, with every other object equal. Each load's own two consecutive prints agreed, so `_draw_reproduced` (D-490's containment) cannot see it.

Open: the cause of per-load placement of one glyph; whether the published artifact can be the minority state (then `--check-artifact` fails far more often); and what the check should do. Candidate repairs, none measured: have `_difference` inflate a FlateDecode stream and name the first differing decoded line (so CI says which glyph without an artifact download); or make `--update` and `--check-artifact` compare across loads rather than within one.

## Notes

2026-10-23 PR743 occurrence, unchanged head 739e283b6921d576a96c595ecd4d139c33e96c39: Certificate page run39902176281 attempt1 pdf job120246470385 failed Draw the PDF of the page. All setup and print sans coverage passed. --update drew three distinct normalized PDFs (882563, 882565, 882565 bytes), so no two of three page loads agreed and the existing publication guard refused to write. Inflated stream differences were single text placement coordinates: object175 y15252 vs15252.2188 and object168 y13373 vs13373.2188. This is concrete new evidence beyond the guard's previously assumed two-document shape. Missing math-geometry artifact was a later cascade. Job: https://github.com/jlevy/squares/actions/runs/39902176281/job/120246470385 . Log retained at /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/739e283b6-pages-pdf-failure.log .

Coordinator authorized exactly one targeted retry on unchanged head after the workflow became terminal; gh run rerun39902176281 --job120246470385 succeeded. Attempt2 job120247726122 rendered 882657 bytes with two of two page loads agreeing, then --check-artifact passed: stored artifact and one fresh render agreed, 24 pages and19 embedded fonts. The job was subsequently cancelled at04:55:43UTC when the coordinator pushed disposition-only successor4f00b6f70e41a934ccada5438d9fb02ba8508107. Thus the draw/artifact checks passed in this retry, but the job/workflow has no terminal green verdict; no source or gate contract was changed and no additional retry was attempted. Retry: https://github.com/jlevy/squares/actions/runs/39902176281/job/120247726122 . Log retained at /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/739e283b6-pages-pdf-retry.log . Coordinator has a separate read-only tier-audit lane for the user's request to move nondeterministic publication work out of routine fast checks; that policy decision does not alter frozen PR743 gates.

Follow-on first-attempt outcome: disposition-only head 4f00b6f70e41a934ccada5438d9fb02ba8508107 passed the entire PDF job 120248890432 in Certificate page run 39902903136, including Draw PDF and check-artifact; the workflow's pages-required aggregate also passed. Job: https://github.com/jlevy/squares/actions/runs/39902903136/job/120248890432 . No retry or PDF/gate source change was made on this head. This passing observation does not resolve the concrete three-distinct-load failure above or its underlying cause.

2026-10-24 coord-intake-1024: recurred on main's post-merge Pages run for #789's merge 2ec489d1e (run 40097882450, attempt 1, job 120884242250 pdf): 'no two of 3 page loads agreed' (887804, 887804 and 887805 normalised bytes; first differences at object 171 and object 88), so deploy and verify-deployment were skipped. The PR's own CI passed the pdf job at 0329f73d6; the change touched no explainer input. Failed jobs re-run once (attempt 2).
