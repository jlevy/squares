---
type: is
id: is-01m1r3mq8knzrvyz0pfpck4v62
title: "Explainer template: custom formatting is plain HTML, no attribute sugar or ::: containers"
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T06:21:08.243Z
updated_at: 2026-09-05T06:25:17.890Z
closed_at: 2026-09-05T06:25:17.890Z
close_reason: Landed in eff24a5e (plain-HTML template, convention in conventions.md, zero-regression pixel comparison), 91c85b25 (Pages enabled with Actions as source; workflow states the prerequisite; subpath test) and 3fde37f5 (formatter notes describe the pinned 0.4.0 only).
resolution: null
duplicate_of: null
---
Replace {.class}, [text]{.class} and ::: containers in certificate_page.md with <div class>/<span class>/<figure>/<figcaption>, kpress class names where kpress styles the block; drop hand-written kpress-figcaption classes; preserve appearance, proven by a DOM diff and a full-height pixel comparison; state the format in conventions.md.
