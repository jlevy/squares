---
type: is
id: is-01m4m2g6xzxbvqczxs3sjcr9fe
title: Compare a short PDF using the web prose typography
kind: task
status: in_progress
priority: 2
version: 4
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-10T23:31:19.614Z
updated_at: 2026-10-11T00:45:41.559Z
started_at: 2026-10-10T23:31:20.493Z
---
Create a separate two-to-three-page comparison PDF matching the actual served web prose font family, size and spacing. The user explicitly requested delegation and a visual comparison; the target document is awaiting clarification. Prepare only read-only typography/toolchain inspection until that answer arrives. Execution is delegated to /root/pdf_web_typography_comparison; root owns tracking and publication. Preserve the production HTML/Markdown-only exact-report policy and earlier closed full-catalogue typography task think-3ui5; do not reinstate report PDF assets, packaging or CI. Use the mounted external scratch volume with a small output budget and existing tools, no internal build fallback or new environments. Render and visually inspect the short PDF before delivering its absolute artifact path, page count, size and font evidence. No source, Git or PR edits belong to this comparison.

## Notes

# Short polynomial report PDF comparison

The owner asked to continue after the document-choice question.
Root chose the original polynomial report as the contextual default and stated this
assumption in the chat.
The comparison agent is creating one short 2-3-page excerpt from the currently served
complete catalogue at http://127.0.0.1:60649/papers/exact-side-values-complete.html.

The sample will include existing prose, table rows and equations at the measured web
sizes: body 18px/27px leading (13.5pt/20.25pt at print scale), table 17.1px/22.23px
(12.825pt/16.6725pt), with the corresponding measured heading and math sizes.
Existing print font choices and math proportions are retained.
The full online catalogue remains the publication; this is a short comparison artifact.

/root/pdf_web_typography_comparison owns the isolated external PDF, previews and QA
receipt. Root owns this bead.
Before first PDF authoring, the agent must run the PDF skill’s operation marker
successfully once. Every final PDF page must be rendered and visually checked for
clipping, missing glyphs, table and equation layout, and clean page transitions before
delivery. No source, PR, preview or production pipeline change is part of this
comparison.

Use existing Chromium headless-shell, Playwright, project Python 3.14.7 and Poppler.
Verify mounted, writable external scratch before output; pause on ENOSPC without an
internal-disk fallback.
The volume had 3,324,368KiB available at the initial check.
Store intermediates under the task’s pdf-web-typography scratch directory and retain the
final artifact and unique QA evidence under its external evidence directory.

Earlier preparation and its pending-choice state are preserved in
pdf-comparison-continue-bead-before-claim.json.
The measured style receipt remains pdf-web-typography-prepared.json.
This bead stays in progress until the PDF and visual QA are complete.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
