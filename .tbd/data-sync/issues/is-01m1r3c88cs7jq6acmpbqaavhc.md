---
type: is
id: is-01m1r3c88cs7jq6acmpbqaavhc
title: Migrate math and custom formatting in all kpress-rendered documents to the plain-HTML format proven on the explainer
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-05T06:16:30.721Z
updated_at: 2026-09-05T06:16:30.721Z
---
PR 79 replaced the explainer template's kpress attribute sugar ({.class}, [text]{.class}) and ::: containers with plain HTML: <div class="…"> blocks with a blank line inside each tag so Markdown renders, <span class="…"> inline, <figure>/<figcaption> for figures, kpress's own class names (hero, subtitle, boxed-text, shaded-text, claim, summary, key-claims, centered-headers) where it styles the block. A full-height pixel comparison of the rendered page before and after showed zero changed pixels. The follow-up is to apply the same format, and one convention for math, to the proof card, t-018-proof.md, the verifiable-claim template and any other document that will render through kpress, and to retire the sugar everywhere. conventions.md states the format.
