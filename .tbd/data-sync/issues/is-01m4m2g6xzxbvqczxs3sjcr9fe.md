---
type: is
id: is-01m4m2g6xzxbvqczxs3sjcr9fe
title: Compare a short PDF using the web prose typography
kind: task
status: closed
priority: 2
version: 6
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-10T23:31:19.614Z
updated_at: 2026-10-11T01:05:02.645Z
started_at: 2026-10-10T23:31:20.493Z
closed_at: 2026-10-11T01:05:02.644Z
close_reason: "Created and visually verified the three-page comparison with web font sizes, complete selected content, reproducible source and reserved-footer QA. Final artifact: 91,042 bytes; full catalogue remains on the web."
resolution: null
duplicate_of: null
---
Create and visually validate one short PDF comparison of the polynomial web report,
applying the measured web font sizes and leading while retaining the existing print font
and math choices. The owner requested delegation and then asked to continue; root
selected the polynomial report from the session context.
The sample includes the introduction and coverage, complete source-identity table,
catalogue explanation and complete n=11 polynomial.
The full catalogue remains a web publication.
Use existing tools and mounted external scratch; retain the final PDF, reproducible
excerpt source and QA evidence outside disposable scratch.
/root/pdf_web_typography_comparison owns the isolated comparison files; root owns this
bead.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

## Notes

# Completed polynomial report PDF comparison

The owner asked for a delegated comparison and then asked to continue.
Root selected the polynomial report as the contextual default and stated that assumption
in the chat. The comparison uses the served complete catalogue at
http://127.0.0.1:60649/papers/exact-side-values-complete.html.

The sample is three Letter landscape pages (792 × 612 pt), containing the full opening
and coverage text, complete eight-row source-identity table, catalogue explanation and
complete degree-eight n=11 equation.
It is an excerpt of the online catalogue.

Prose and math use 13.5 pt, with prose leading of 20.25 pt, matching the measured web
18px/27px. Table containers use 12.825 pt/16.6725 pt; the source-path code retains its
existing smaller print size.
Existing print font choices and math proportions are preserved.
The catalogue’s former print prose baseline was 12 pt/16.8 pt.

Root found first-page coverage text intruding into the footer and requested a spacing
correction. The complete text now fits above the reserved footer without shrinking it.
Root visually approved the revised first page and the unchanged second and third pages.
QA checks the reserved content boundary as well as page bounds; fonts are embedded, all
three n=11 equation lines are present, and the standalone source reloads offline.
The PDF authoring marker succeeded exactly once for this operation.

Final artifact:
/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-2026-10-10-1715/pdf-web-typography/polynomial-web-size-sample.pdf.

QA and reproducible source bundle:
/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-2026-10-10-1715/pdf-web-typography/qa-receipt.json.
The same directory retains excerpt.html, measured CSS, renderer/probe code, actual PDF
font measurements and all three page previews.
The earlier preparation and continued scope are archived in the separate bead receipts.

This comparison used existing Chromium, Playwright, project Python 3.14.7 and Poppler,
with external scratch and no new environments.
The complete report stays on the web; this task makes no source, PR, live-preview or
production PDF pipeline changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
