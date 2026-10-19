---
type: is
id: is-01m5atsz0h85vk7w448nnptejj
title: "validate.py: a timeout after earlier commands' output loses its [timed out after N s] label"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-19T19:39:22.512Z
updated_at: 2026-10-19T19:39:22.512Z
---
PR #685 Review D2 (Low, predates #685). In _site_layout_tests (packing/src/sqpack/cli/validate.py ~:2143 at 075ea493b) the re-raise puts earlier commands' output ahead of 'command timed out', and the timeout classification at ~:7044 only matches at the start of the text, so a forwarder or load-budget timeout is not labelled [timed out after N s] in the failure class.
