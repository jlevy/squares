---
type: is
id: is-01m1r3c88cs7jq6acmpbqaavhc
title: Migrate math and custom formatting in all kpress-rendered documents to the plain-HTML format proven on the explainer
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-05T06:16:30.721Z
updated_at: 2026-10-06T08:34:48.265Z
closed_at: 2026-10-06T08:34:48.265Z
close_reason: "Done: no kpress-rendered document on origin/main uses attribute sugar or ::: containers (git grep finds none outside quoted rules), conventions.md lines 580-589 state the plain-HTML format, and the LaTeX math migration (00346a270) gave math one convention."
resolution: null
duplicate_of: null
---
PR 79 replaced the explainer template's kpress attribute sugar ({.class}, [text]{.class}) and ::: containers with plain HTML: <div class="…"> blocks with a blank line inside each tag so Markdown renders, <span class="…"> inline, <figure>/<figcaption> for figures, kpress's own class names (hero, subtitle, boxed-text, shaded-text, claim, summary, key-claims, centered-headers) where it styles the block. A full-height pixel comparison of the rendered page before and after showed zero changed pixels. The follow-up is to apply the same format, and one convention for math, to the proof card, t-018-proof.md, the verifiable-claim template and any other document that will render through kpress, and to retire the sugar everywhere. conventions.md states the format.
