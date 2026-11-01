---
type: is
id: is-01m692j9fhhs5b5vbyzz6crbvv
title: "Store the two-strip family's decisions receipts over 1,000 lines as deterministic gzip (#799's v2 on main, #836's v5), read and written through retained_data"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5qsa2jj6mf8cgemykzyy109
created_at: 2026-10-31T13:32:12.657Z
updated_at: 2026-10-31T13:32:12.657Z
---
Review A6 of #859. devtools.retained_data's convention keeps retained receipts of more than 1,000 lines as gzip -9n X.gz files with a Compressed Files row in the packet README, read through read_retained_bytes. 'python -m devtools.retained_data candidates' lists karimi-two-strip-2026-10-24/receipts/two-strip-decisions-v2.json (2,854 lines, on main since #808) and karimi-records-2026-10-31/receipts/two-strip-decisions-v5.json (5,339 lines, 2,128,349 bytes, #859). devtools.two_strip_checker's _read and _write read and write plain JSON, so the family has never followed the convention; nothing gates on it. Do: compress both with 'retained_data compress', add each packet's Compressed Files rows, route two_strip_checker's receipt reads and writes through retained_data, and rerun two_strip_checker check and acquire_source --check for both packets. Seconds of compute; no row or verdict changes.
