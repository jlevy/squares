---
type: is
id: is-01m3gy5qb0vnehs3n8hk3skn6p
title: "Explainer PDF: one KaTeX glyph's baseline moves between page loads, past D-490's draw-twice containment"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: ci-followups
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-27T08:02:16.543Z
updated_at: 2026-10-23T04:52:09.584Z
started_at: 2026-10-23T04:52:09.582Z
---
PR 235 pull_request run 36126482461 (attempt 1, head de282a855, records-only) failed the Pages `pdf` job at `render_explainer_pdf --check-artifact`: `849931 then 849931 bytes, normalised; length delta 0 ... first difference at byte 514532, in object 144`, inside a FlateDecode stream. The unchanged rerun (attempt 2) passed, and `pages-required` then refused the partial rerun as unmeasurable, by design. D-509 records it; it recurs D-490 (think-ptit, think-a5qp).

The retained pair (artifact 10859178879) could not be downloaded from the session: the proxy refuses the Actions blob host. From the log alone: the two 64-byte windows agree for 32 bytes, then the second stream is the first shifted two bits earlier, which is a small change to the inflated text, the size of a changed number.

Local reproduction, prepared page built at de282a855, Chromium 141.0.7390.37 (not the pinned 151 headless shell): about 80 page loads through the maintained `--check --renders N` CLI gave four between-load disagreements, and no within-load repeat at all. Inflated, every one was a single `Tm` line in one page content stream: one KaTeX_Main glyph of prepared inline math (≥ in `s(11) ≥ 191/50 = 3.82`, ∣, =, =) moved 0.21875 or 0.1875 px vertically, a different glyph and page each time, with every other object equal. Each load's own two consecutive prints agreed, so `_draw_reproduced` (D-490's containment) cannot see it.

Open: the cause of per-load placement of one glyph; whether the published artifact can be the minority state (then `--check-artifact` fails far more often); and what the check should do. Candidate repairs, none measured: have `_difference` inflate a FlateDecode stream and name the first differing decoded line (so CI says which glyph without an artifact download); or make `--update` and `--check-artifact` compare across loads rather than within one.
