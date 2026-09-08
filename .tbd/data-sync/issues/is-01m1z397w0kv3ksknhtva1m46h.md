---
type: is
id: is-01m1z397w0kv3ksknhtva1m46h
title: Keep the opening Trump figure together on the first PDF page
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T23:29:33.054Z
updated_at: 2026-09-07T23:41:58.736Z
closed_at: 2026-09-07T23:41:58.736Z
close_reason: "Completed in PR #117 at 83a2e6f3. All required hosted checks and the paper build passed; the timing-only CI failure passed one unchanged-commit retry. Three agent reviews and root review accepted the work. HTML, Markdown and the 17-page PDF were rebuilt; the web preview and Preview PDF were opened. The latest upstream deployment also passed all 26 live-site checks. Separate selector issue think-oe1g remains open."
resolution: null
duplicate_of: null
---
After reconciling the upstream typography update, the Trump SVG retains its screen 24rem width while canvases already have a 3.2in print cap. The resulting unbreakable figure moved to page2, leaving a large opening-page gap. Apply a print-only figure size cap matching the canvases, then rebuild and visually inspect Figure1, the framework box, and later figures. Preserve typography, margins, captions, and screen sizing.

## Notes

Applied print-only .trump a width:min(100%,3.2in), matching the existing canvas cap. Root visually reviewed rebuilt17-page PDF: Figure1 and new caption both fit on page1; italic framework box page2; Figures5 and6 pages9 and11 retain readable math and no interactive handles. Screen/mobile sizes unchanged, confirmed by independent code review and the final Chromium layout/touch/self-check. Committed in83a2e6f3 and pushed to PR117; hosted CI pending.
