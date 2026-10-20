---
type: is
id: is-01m4xjgt3r9m08w6v2yvrdc1e6
title: "#514 review B5: a malformed ?added-since= emptied the date input, which then hid its label and matched every row"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T16:04:26.360Z
updated_at: 2026-10-14T16:05:24.052Z
closed_at: 2026-10-14T16:05:24.052Z
close_reason: "fixed in fa8f8302d: a date preset that comes back empty is marked data-unmatched, shows its label and applies a filter that matches no row until the reader edits it; test_the_added_filter_shows_what_reached_the_site holds ?added-since=2026-10-6 at 0 rows with the label visible"
resolution: null
duplicate_of: null
---
Review B of #514 (review 5520287797), finding B5: a malformed ?added-since= emptied the date input, which then hid its label and matched every row
