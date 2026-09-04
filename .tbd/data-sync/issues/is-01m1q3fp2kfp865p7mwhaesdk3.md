---
type: is
id: is-01m1q3fp2kfp865p7mwhaesdk3
title: "kpress: add a second accent role for figures with two interactive colours"
kind: task
status: open
priority: 3
version: 3
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T20:59:08.755Z
updated_at: 2026-09-04T21:00:06.786Z
---
The doc roles are accent, link, success and danger. A figure needing two distinguishable interactive colours (one for the quantity displayed, one for the control the reader manipulates) has only accent, since success and danger carry semantics that should not be repurposed for a control. The certificate page defines `--cert-probe` itself and re-declares it under `[data-kpress-resolved-theme="dark"]`, duplicating kpress's theme mechanics in consumer code.

Proposal: a second non-semantic accent role, `--kpress-doc-accent-alt`, defined per theme alongside the others. Low priority: one extra token per theme block, and the workaround is small.
