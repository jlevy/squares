---
type: is
id: is-01m4zaazfxmv8px64xvdvdqnc7
title: Tighten significance meters and clean News topics and filter wrapping
kind: bug
status: in_progress
priority: 1
version: 7
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m4zdrrf3qwg7ms04am4vx8x3
  - is-01m4zdsxez5kg9ffagfvqja44y
  - is-01m4zfcwxwmgks031psmvp1yjq
  - is-01m4zgcx35k7eyagqwae287emt
hold: null
hold_until: null
created_at: 2026-10-15T08:19:55.500Z
updated_at: 2026-10-15T10:05:50.052Z
started_at: 2026-10-15T08:21:27.177Z
---
User requests: reduce S-score-to-bars spacing below a word space in the shared meter; drop Documentation as a News topic and exclude pure document-maintenance announcements while retaining substantive domain news; fix multi-value News chooser wrapping so the control box follows its lines. Reuse shared compact design, preserve click/tap behavior and scientific news. Delegate CSS and editorial/schema changes separately; coordinator integrates/reviews.

## Notes

Implemented on focused codex/news-reader-refinements at 895637bc4. Shared meter gap 0.08em with centered fixed-width contents; News topics wrap as individually outlined compact controls. Documentation topic removed; PR492 maintenance item omitted from News with explicit news_exclusion while all28 historical IDs and54 coverage rows remain. Shared schema/publication audit updated. Desktop/mobile native preview source895637 issues[]; 66focused tests pass. Full prepush in progress; browser-floor environment failure repaired by linking already-locked workspace dependencies, exact floor rerun passes122Node tests. Independent Astra review clear; delivery still pending.
