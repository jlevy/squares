---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: closed
priority: 1
version: 10
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-07T06:23:10.673Z
started_at: 2026-10-03T22:35:21.360Z
closed_at: 2026-10-05T05:35:40.288Z
close_reason: "Review written (30a6c9753, docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md, in #347); the gmpy2 port (c401c81d6) and the memory fix (7f1db8a42) are integrated; the compiled backend continues as think-ui2y."
resolution: null
duplicate_of: null
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

gmpy2 port integrated c401c81d6 (owner-approved): producer 2.78x, check-saved 4.20x on W7 round 1, byte-identical; full W7 check-saved 173 s (930 s indexed before rank 3, 1,634 s reference). Lock regenerated with CI's uv 0.12.8 (revision 3, additive). Verifiers stay on CPython integers. Next F2: profile the capture producer (C1's ~155 CPU-s per update at 128 rows) vs the branch-and-bound verifier cut cache; build the larger payoff.

2026-10-03 evening. Lane M1, kernel memory. producer.produce kept every replaced row's partner-memo entry (on W7-split, about 3,300 stale of 3,821, over 400 MB), now dropped (7f1db8a42). Nodes are read a step at a time, and the term and facet memos are capped at 2^15 pairs. Peaks fell 55-83% on W7-split and SW8, with results and bytes identical. Flag 2's 931 MB node under the streamed check-saved peaked at 1,230 MB (it was about 4.3 GB sampled), same verdict, 3,375 s CPU (3,187 before, on a loaded machine). The verifier's counterpart (601bbf110) is committed but unlisted pending review. Also: the selector's resume lever (73a68676d, 11.5% on flagged classes, verdict-identical on 21 classes), and test selection parsing each file once without the cyclic GC (96d229ffe, cold scan 8.1-8.7 s to 6.0 s, which fixed a 12 s backstop trip on shard D).
