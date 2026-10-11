---
type: is
id: is-01m3v8g7z02m9h81yyjtr3hxax
title: "Case popover: the bound columns never break a word; the 'lower' label column is not a fixed narrow width"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:15:11.326Z
updated_at: 2026-10-01T09:35:52.238Z
closed_at: 2026-10-01T09:35:52.235Z
close_reason: "6ef429f03, merged into jlevy/squares#264: the case popover breaks no word, and the label column is as wide as its labels; preview_site checks every popover for split words."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the column holding 'lower' wraps the word in an ugly way as it is so narrow, on the popover from the frontier for many values such as n = 79. The layout should be cleaner and it should not be fixed; we should not generally wrap in the middle of words. In the frontier's case popover (and the atlas popover and case record that share the panel) the label column sizes to its content, long values wrap at spaces or scroll, and no site text breaks inside a word (find overflow-wrap: anywhere or word-break rules that cause it and scope them to long unbroken tokens such as hashes and URLs only).
