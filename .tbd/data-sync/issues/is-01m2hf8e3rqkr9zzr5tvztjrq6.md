---
type: is
id: is-01m2hf8e3rqkr9zzr5tvztjrq6
title: "PR #155 review D06: summariser, resolved definition and rows missing; README, .gitignore and X-034 disagree"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb40g8vbnq8914rkt7p87c
created_at: 2026-09-15T02:45:09.367Z
updated_at: 2026-09-15T02:45:09.367Z
---
Review: attic/reviews/pr155/review-pr155-d46b86a5.md (PR #155 review at d46b86a5). Parent: think-xqc3.

Source: #155 R4.

Files: packing/campaign/results/annealing/README.md:24-25, :51-53; .gitignore:36-40; X-034 :44-47, :126-128, :211-212, :244-250; exp-210 :124-126; H-210 :37-39; summaries.json.

Fix: commit the summariser (packing/devtools/summarize_annealing.py, recovered from the 2026-09-12 session transcript, byte-identical output on local rows) with a fixture test; README, .gitignore, X-034, exp-210 and H-210 say the rows are unretained, regenerable by recorded command, and re-checkable by the summariser.
