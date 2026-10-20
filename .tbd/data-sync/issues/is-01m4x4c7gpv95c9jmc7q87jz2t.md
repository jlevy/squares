---
type: is
id: is-01m4x4c7gpv95c9jmc7q87jz2t
title: "#597 review A1: check_requests reasons keyed by reply date merge same-day replies' fields"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T11:57:16.182Z
updated_at: 2026-10-14T11:57:25.099Z
closed_at: 2026-10-14T11:57:25.099Z
close_reason: "fixed in e218dafb1: _moved groups by the reply's place, each reason quotes that reply's own statement, and _reply_label names a reply by date, kind or address; test_two_replies_of_one_day_are_each_quoted_for_what_it_stated fails before and passes after (#597 head 8db1905d5)"
resolution: null
duplicate_of: null
---
Review A of #597 (review 5517404240), finding A1 (Medium): _moved grouped held fields by reply date, so fields last stated by two replies of one date were quoted as one statement neither made, and --draft would quote it to an author; the date alone could not say which of a day's replies was meant.
