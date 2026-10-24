---
type: is
id: is-01m5nstg2vqmhpdnwnyhhb0vjj
title: "PR #759 (merge): senior review of the News feed plan"
kind: task
status: closed
priority: 2
version: 6
delegate: c-rev-759-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5nvex330ynadac7263123y2
  - is-01m5nxsv4849rrgby596kc6prq
hold: null
hold_until: null
created_at: 2026-10-24T01:53:50.171Z
updated_at: 2026-10-24T04:03:29.324Z
started_at: 2026-10-24T01:53:57.856Z
closed_at: 2026-10-24T04:03:29.324Z
close_reason: "#759 merged at 1aa953fad (head f7856724b; reviews A 6378649518 and B 6379328505 with dispositions 6379056910 and 6379608495; B1 verified against corrected_rule_check.out; CI green 40059938843, 40059938857, 40059935573)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-759-1024: senior review A (round 1) of PR #759 posted as a PR comment: https://github.com/jlevy/squares/pull/759#issuecomment-6378649518
Marker: <!-- tbd:review v=1 id=A kind=senior pr=759 round=1 head=8dee3896c3e270bc6f9464926e7cbfb6f395835b base=64b316b6cc8fa31177824e20733853708b996fb5 -->

Verdict: changes requested before merge for A1 (High). No Blocker. A2-A7 (Medium) should be fixed in the same round.

High:
- A1: results are attributed per merge commit, and GitHub shares one mergeCommit across stack and chain layers: 28 commits, 89 PRs, 53 rows sharing a register diff. For example, d3860c97a is the mergeCommit of 11 PRs and registers 6 ids.

Medium:
- A2: the runbook list misses result-import.md:1357 ("S3 News stays optional"), :1372, :1148-1166 and the omission clause at :1129-1131.
- A3: fidelity:
  - :828 credits the 1.3 MB figure to "the owner's question";
  - "Approved in outline" claims an approval nobody gave;
  - two labels lose "(Recommended)";
  - Decision 4 is a coordinator default listed among the owner's decisions.
- A4: the trip check fails every PR once main crosses it, and at the trip point no S3+ merge can be recorded.
- A5: the "two weeks after think-4oj0" trigger is a time frame. The deployed news.html is 318,655 bytes over 50 cards, and the 600,000 budget is about 19 days away.
- A6: the coverage rule of SiteChangelog/v2 is unstated.
- A7: the switch measurement misses a feed-first load followed by a switch to the stories, where news-cards.js's ResizeObserver runs refresh on every card.

Low: A8-A16. Suggestions: A17 (label floor) and A18 (OR-18 standing of record_pull_requests).

Dedicated reviews: none for this documentation-only PR. Correctness review for Phase 1's implementation; performance review for Phase 2's.

Tests run at 8dee3896c, all passing: check_documentation, check_synopsis, check_pr_description, and merge-tree onto 5664ac1e8 (clean). CI: 16 pass, 41 skip, 0 fail.
