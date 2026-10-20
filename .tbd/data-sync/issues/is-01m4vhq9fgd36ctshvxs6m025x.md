---
type: is
id: is-01m4vhq9fgd36ctshvxs6m025x
title: Add a formalization result kind; register T-154 as a formalization (owner, 13 October)
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-13T21:12:01.263Z
updated_at: 2026-10-14T01:25:00.563Z
---
Owner, 13 October 2026, on T-154's kind: 'simplification is one thing but formalization is another', then 'let's go with formalization then'. Add a kind formalization to epistemics.md's Result Kinds (a proof-assistant proof of a result the record already holds, formalizing an existing argument or by a route of its own; it moves no bound by itself), to the results schema and every checker and renderer that enumerates kinds (check_results, check_standing, render_recent_results, the site's kind filters and labels), with tests; move T-154 to it, with its claim, headline, notes, next_rung, n-017 prose, requests entry and URL row brought into line. Lands in PR #588 before it merges, under a sub-agent review.

## Notes

2026-10-14, writer lane on claude/stoic-clarke-jhfnru (from df9767225), local commits, not pushed:
- cd901b786 kinds: formalization in epistemics.md (table row, fifth kind rule, headline and evidence rules, the second-proof standing paragraph, a dated vocabulary record citing the owner's decision of 13 October), results.schema.yaml, check_results (KINDS, SECOND_PROOF_KINDS; a formalization names its result on a shared case and cites proof-assistant-checked evidence, performed or reported; a simplification citing such evidence is refused), check_standing and render_recent_results (both second-proof kinds), audit_t007_consumers LOWER_KINDS, the all-results article, paper-design, result-import.
- 3515d3a40 register: T-154 kind formalization (headline, claim, rationale sentence, next_rung, notes), T-153's note, n-017 (note, priority note, prose, Reported Lower Bound), #565 entry, source-coverage note; site-urls.yaml result/t-154.html identity kind formalization with a dated amendment of 2026-10-14 (previous = the simplification identity); tests.
- f3d620c98 views: RESULTS.md, SYNOPSIS.md, t007-consumer-audit.json.
- 7a1aadceb release: re-pin DATA_REVISION to f3d620c9.
check_standing --list identical to df9767225 (T-154 stays "second certificate, reported").
Validation: --records 50/50 steps passed; --edit 66/66 passed; --push 64/65, the one failed step being reachable behavioral tests with 4 failures (7,705 passed) that fail identically at df9767225: two process-group reaping tests (test_fixed_core_packet, test_fixed_core_packet_calibration: "worker process group remained alive after SIGKILL") and two test_site_column_measurement tests (no Chromium on this host). Not pushed; no PR edited.
