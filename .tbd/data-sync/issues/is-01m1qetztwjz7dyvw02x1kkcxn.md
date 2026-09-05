---
type: is
id: is-01m1qetztwjz7dyvw02x1kkcxn
title: "kpress: a figure container so captions can be Markdown with math"
kind: task
status: open
priority: 3
version: 1
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-05T00:17:33.532Z
updated_at: 2026-09-05T00:17:33.532Z
---
Raised converting the certificate page to Markdown. Interactive figures must be raw HTML blocks, so their captions cannot use $…$ math or Markdown emphasis; a ::: figure container carrying a head (number, title, tag) and a Markdown caption around a raw HTML stage would let the page's captions be text too.
