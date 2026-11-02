---
type: is
id: is-01m6cmvq7zytr8d7rp51r10b3n
title: "Efficiency: DATA_REVISION pin in release.py conflicts on parallel records PRs (32 merges in 20 PRs since 24 Oct)"
kind: task
status: closed
priority: 3
version: 4
delegate: bold-ritchie-l27
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-01T22:49:39.327Z
updated_at: 2026-11-02T08:23:28.143Z
started_at: 2026-11-02T07:50:22.330Z
closed_at: 2026-11-02T08:23:28.143Z
close_reason: "Measured (https://github.com/jlevy/squares/pull/883, merged b1b0c3a09): all 45 DATA_REVISION-conflicted merges since 24 Oct were data commits needing a re-pin anyway; no merge driver or layout removes that. Superseded by think-070d (owner-decided 22 Oct: footer names the deployed commit, DATA_REVISION and release_pin removed), which awaits scheduling."
resolution: null
duplicate_of: null
---
Measured by devtools.merge_conflicts in #873 (think-nrp6): after the no-public-change tuple, the DATA_REVISION pin in packing/src/sqpack/release.py is the next most frequent conflict, 32 merges in 20 PRs from 24 Oct to 1 Nov; the union driver 'parses' 9 of its sole-conflict merges but yields two pin assignments, silently wrong. Candidate fixes: derive the pin at check time from git (last data commit) instead of storing it, or store it outside release.py in a file whose merge is mechanical. Measure, pick the smallest sound fix (OR-12 efficiency block), red-first test that two data PRs merge cleanly.

## Notes

2026-11-02 bold-ritchie-l27 (lane L27, efficiency block): measured and decided; the pin stays until think-070d.

Measurement (`python -m devtools.merge_conflicts --since 2026-10-24 --data`, from packing/, origin/main 6062867b1): 230 merges in 80 PRs, 100 conflicted. DATA_REVISION conflicted in 45 merges across 29 PRs and was the only conflict in 11 (9 PRs). All 45 were data merges, as were 62 of the 230: each changed the data against both parents, so each was itself the new last data commit and needed a re-pin commit after it however the pin's line merged. In the same window, 121 non-merge commits moved the pin line.

What DATA_REVISION is for: it is the data half of PUBLICATION_EDITION (v0.9.2-1fc854), which the site footer (render_overview.colophon_lines) and the workbench stage (build_candidate) print and check_published_site holds the deployed pages to. It also stamps INFOGRAPHIC_EDITION and is build_known_best_atlas's test of whether a poster is current or trailing. It is stored because renders never read the history (release.py rule 1): the Pages overview and workbench jobs check out at depth 1, where data_revision() refuses, and OR-18 rules out a render that depends on history.

Options: (c), a mechanical merge, would save only the hand resolution in those 45 merges, since every one still needed its re-pin and that push's CI cycle. No built-in merge driver resolves the line correctly either: the right value is the merge commit, and neither side holds it. (b), storing the pin at release time only, would leave the footer naming stale data, which weakens the drift test's guarantee. (a), deriving the pin from the history at render time, breaks the shallow deploys and contradicts OR-18 and the owner's think-wdqo design ("no Git read at render time"). Under the current footer the pin has to be stored per commit, so I stopped there. The fix that removes the re-pins is think-070d (P1, open, owner-decided on 22 October): the footer names the deployed commit and its time, injected by pages.yml, and DATA_REVISION and release_pin are removed. It touches release.py, release_pin, render_overview, workbench build_candidate/build_site, check_published_site, build_known_best_atlas (identity and current check, from the live history), check_release_impact _PIN_FIELDS and measure_release_assets, about 9 test modules, and development.md, result-import.md stage 5, regularization-process.md and the workbench README.

Delivered: merge_conflicts --data, which makes the measurement re-runnable (OR-1), with a red-first fixture test, and a paragraph in development.md beside the re-pin rule.
