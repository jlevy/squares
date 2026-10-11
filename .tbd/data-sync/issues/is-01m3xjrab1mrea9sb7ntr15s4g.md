---
type: is
id: is-01m3xjrab1mrea9sb7ntr15s4g
title: Drop the subtitle line under the page title on the Results, Papers and Frontier pages
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:52:50.528Z
updated_at: 2026-10-02T07:09:30.201Z
closed_at: 2026-10-02T07:09:30.201Z
close_reason: "Merged in jlevy/squares#304 (c05e0202e, merge 81cb5716): the Results, Papers and Frontier subtitles are gone."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'and let's drop the h2s on the main pages, they don't add much, i.e. drop these: A survey of all reviewed results / Papers and interactive explanations for specific results / A survey of everything known for cases n = 1, …, 324'. These are the italic subtitle lines under the titles of all-results.html, papers.html and frontier.html. Remove them from the pages (and from wherever they are declared), keep the page descriptions used in the head and on social cards unless they are the same string by construction, close the space the line leaves so the title sits right above the first paragraph, and update the tests and paper-design.md that pin them.

## Notes

2026-10-02 10:10 UTC, branch claude/ladders-to-results at c05e0202e, draft PR #304: done. The subtitles of the Results, Papers and Frontier pages are gone at their templates; the Frontier renderer no longer sets the range as sans math; the hero is the title alone and stands the subtitle's space above the first paragraph by the existing rule. The page descriptions stay (own constants). The case records' page keeps its subtitle (not named by the owner). Page headings in paper-design.md and the subtitle test updated. Gates run once on the PR's final head.
