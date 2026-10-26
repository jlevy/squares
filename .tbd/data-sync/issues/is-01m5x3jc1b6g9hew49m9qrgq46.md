---
type: is
id: is-01m5x3jc1b6g9hew49m9qrgq46
title: Twelve site browser contracts run only after merge, so a site change can go green on its PR and red on main
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-10-26T21:58:50.667Z
updated_at: 2026-10-26T21:58:50.667Z
---
Twelve site browser contracts never run on a pull request, so a site change can go green
on its PR and red on main. That happened twice on 26 October 2026: #837 merged green and
turned `integration-suites` red on `e82acb66c`, and #839 exists only to repair the two
contracts it tripped.

## The mechanism

`integration-suites` is gated `if: github.event_name != 'pull_request'`, and it is the
job that installs Chromium and then runs the quick lane whole. On a pull request:

- the four `suite-a`..`suite-d` jobs run `_quick_lane_command`, which passes
  `--ignore` for every path in `SITE_LAYOUT_TESTS` and installs no browser;
- the `frontend` job installs Chromium and runs exactly `SITE_LAYOUT_TESTS`.

So a site browser file that is *not* listed in `SITE_LAYOUT_TESTS` falls to the shard
jobs, finds no Chromium, and skips. It is first exercised after the merge.

The twelve in that position today, all of which read the deployed chrome:

`test_site_wide_blocks.py`, `test_site_github_links.py`, `test_site_project_tallies.py`,
`test_site_text_tokens.py`, `test_site_source_actions.py`, `test_site_glyphs.py`,
`test_site_head.py`, `test_site_ladders.py`, `test_measure_news_page.py`,
`test_site_browser.py`, `test_site_atlas_follow.py`, `test_scroll_restoration.py`.

The two that went red are the first two: one read the navigation bar's own row as
`Overview, News, Results, Learn, About, GitHub`, the other read the colophon's links as
the repository, Flowmark and KPress. Both were correct shapes before #837 moved them.

## Why this is an OR-13 matter and not a slow-lane one

These are not unavoidably slow. Measured on this session's container, the twelve files
run **285 passed in 270 s** wall at `-n 4 --dist=loadfile`, with Chromium from
`/opt/pw-browsers`. Nothing in them is marked `slow` or `exhaustive_exact`; they are off
the pull-request surface because of where the browser is installed, not because of cost.
`OR-13` says every fast check runs on the pull-request surface and only the unavoidably
slow ones leave it, each on its own measurement. No measurement put these off it.

## The candidate fix, and the question it has to answer

The `frontend` job already installs Chromium on pull requests and already runs a list.
Adding these twelve to `SITE_LAYOUT_TESTS` would put them on the surface with no new job
and no new browser install, and the shard jobs would keep ignoring them.

What that has to be priced against is `OR-17`: the `frontend` job has a wall ceiling, and
270 s of new work at `-n 4` is not free. The honest options are to measure the `frontend`
job with the twelve added and raise its ceiling on that measurement, or to give the
browser surface a second concurrent job so the pull request waits on the longer of two
rather than their sum. Either way the decision is a measurement, per `OR-14`.

Worth checking while here: whether any file *in* `SITE_LAYOUT_TESTS` is slow enough that
the list is already at its ceiling, since that changes which of the two options is open.
