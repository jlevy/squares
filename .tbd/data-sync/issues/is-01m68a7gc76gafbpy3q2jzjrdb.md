---
type: is
id: is-01m68a7gc76gafbpy3q2jzjrdb
title: check_requests.replies_due takes a comment read on the day of the last reply as answered, so a comment posted after that reply owes nothing (#804, 26 October)
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-31T06:26:53.447Z
updated_at: 2026-10-31T06:26:53.447Z
---
replies_due (packing/devtools/check_requests.py, about lines 779-797) compares the day of read_through with the date of the last reply: 'Reply dates are days, so a comment read on the day of the last reply is taken as answered by it.' On #804 the follow-up was posted at 2026-10-26T10:29:17Z and Hyukdong Kim commented at 11:50:22Z the same day, asking which public copy we prefer; once PR #833 read the comment in, neither check_requests --report nor the intake sweep listed a reply due (review A of #833, finding A1). The comparison should use the last reply's created_at, which the record does not hold (replies carry date only): record a time on each reply (or read it from GitHub in the reporting modes) and compare read_through with it. Found 31 October 2026 by review A of #833; #833 works around it for #804 by marking the 26 October follow-up's licence statement outdated (think-8r92). Done when a comment after the last reply on the same day makes a reply due, with a test.
