---
type: is
id: is-01m5k1n0dpafhzby7d6d8p6jz5
title: Replace Downloads with dedicated Posters page
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-tracker-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:12:55.604Z
updated_at: 2026-10-23T01:35:55.646Z
started_at: 2026-10-23T00:13:01.640Z
---
Replace the generic Downloads destination with Posters containing the packing PDF posters. Remove the paper-editions table; paper PDFs remain discoverable on paper catalogue/detail pages. Use Posters consistently for menu, heading, metadata and breadcrumb. Prefer posters.html canonical route with old downloads.html and relevant fragments forwarded. Update plan, URL registry/build integration and focused tests, rebuild preview.

## Notes

Source complete: canonical posters.html uses Posters consistently in menu, heading, metadata and breadcrumb. Only the two Atlas packing poster PDF cards and retained SVG/source links remain; removed the unused paper-editions table renderer. Existing PDF/Markdown artifacts were not changed. downloads.html is a metadata-bearing compatibility forwarder; shared navigation preserves papers#pdfs -> posters#pdfs and posters#paper-editions -> papers with queries retained. Overview and Papers fallback links now use Posters. Plan current tree, route disposition and CSV reconciled (1157 rows; old Downloads retained as a forwarder). Focused Poster/content/semantic checks: four passed in85.72s; the separate new forwarder test used the wrong attribute assertion, corrected to data-moved-to and rerun passed in12.64s. Ruff check/format and diff-check clean. Coordinator owns final registry/workflow reconciliation, full preview build and integrated browser/CI publication checks; source stable, no partial write_site used.
