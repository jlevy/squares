---
type: is
id: is-01m1qetz5309tjmjz9xtd2bmq6
title: "Markdown article: a devtool proves the pinned flowmark keeps every math span whole"
kind: task
status: closed
priority: 2
version: 2
labels:
  - tooling
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:17:32.834Z
updated_at: 2026-09-05T00:22:04.154Z
closed_at: 2026-09-05T00:22:04.136Z
close_reason: "Commit 7798a9ba: devtools/check_math_spans.py with tests; 0 of 2,032 archive spans broken under 0.4.0, and the 0.3.2 negative control reproduces the recorded 101/31/5."
resolution: null
duplicate_of: null
---
packing/devtools/check_math_spans.py formats copies with the Makefile's pinned flowmark and reports spans broken or changed, exit non-zero on any; a test for the counter; one sentence in AGENTS.md. Run on the archive transcriptions and on the article source. Delegated.
