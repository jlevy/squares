---
type: is
id: is-01m4m2g6xzxbvqczxs3sjcr9fe
title: Compare a short PDF using the web prose typography
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-10T23:31:19.614Z
updated_at: 2026-10-10T23:34:59.617Z
started_at: 2026-10-10T23:31:20.493Z
---
Create a separate two-to-three-page comparison PDF matching the actual served web prose font family, size and spacing. The user explicitly requested delegation and a visual comparison; the target document is awaiting clarification. Prepare only read-only typography/toolchain inspection until that answer arrives. Execution is delegated to /root/pdf_web_typography_comparison; root owns tracking and publication. Preserve the production HTML/Markdown-only exact-report policy and earlier closed full-catalogue typography task think-3ui5; do not reinstate report PDF assets, packaging or CI. Use the mounted external scratch volume with a small output budget and existing tools, no internal build fallback or new environments. Render and visually inspect the short PDF before delivering its absolute artifact path, page count, size and font evidence. No source, Git or PR edits belong to this comparison.

## Notes

Preparation completed with existing Chromium headless-shell, project Python 3.14.7 and
Poppler; no installs, source edits, preview changes or PDF authorship.

The actual complete polynomial catalogue uses web prose 18px with 27px leading,
equivalent to 13.5pt/20.25pt at CSS print scale.
Its publication print override is 12pt/16.8pt leading; the generic 11pt default is not
the actual catalogue baseline.
Web headings/table/math sizes were measured too.
The maintained methods route is currently 404 in this preview.
A short 2–3-page sample can preserve print layout/font/math choices while applying
measured web sizing and leading.

The target document remains required and awaiting the human’s answer (methods paper,
exact-side report or home page).
Do not author until confirmed.
This comparison does not reinstate production catalogue PDF packaging or CI. Root owns
tracking/publication; /root/pdf_web_typography_comparison owns the small external
comparison files. Frozen preparation receipt:
/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-2026-10-10-1715/pdf-web-typography-prepared.json.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
