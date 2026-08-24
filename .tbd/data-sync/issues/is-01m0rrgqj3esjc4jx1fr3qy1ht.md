---
type: is
id: is-01m0rrgqj3esjc4jx1fr3qy1ht
title: "Engineering: make the packing research loops fast enough to iterate"
kind: epic
status: open
priority: 1
version: 11
labels: []
dependencies: []
child_order_hints:
  - is-01m0rrhw3a0zqmyw095twj9bn3
  - is-01m0rrhwd2zzyj0x0jwa8cqwtw
  - is-01m0rrhwpct8th5qckp9w959bv
  - is-01m0rrjstb9c806nbjzzfaj1ss
  - is-01m0rrjt4p850rt1t2z32b5sm0
  - is-01m0rrjtdy1zxafc7790ssa720
  - is-01m0rrjtq99x8zbzd5hvqxrjcg
  - is-01m0rrwmf90rynrj697ge7nk1k
  - is-01m0rwwt8912eq5f3507d581e1
  - is-01m0s8tvzd11dyjk9s2fw40z16
created_at: 2026-08-24T02:10:15.746Z
updated_at: 2026-08-24T06:55:25.164Z
---
Engineering review of PR #17 (codex/packing-unattended-research-readiness) from a process, efficiency and software-correctness angle.

Measured baseline on a 10-core M-series machine, warm caches:
- ./test.sh: 170s wall, 133s user CPU -- i.e. ~0.8 of 10 cores, fully serial, 25 steps, no way to run a subset.
- sqsearch engine: 28.7M moves/s. NOT the bottleneck.
- One quench: ~2.5s and ~1,600 scipy linprog calls.
- One LP solve (99 rows x 23 cols): 1456us via scipy.optimize.linprog; 380us driving HiGHS directly. ~95% of the time is wrapper overhead, not simplex.
- Zero Python parallelism anywhere in the tree.

The research critical path named in the PR (H-021 endpoint identifiability, H-023 terminal-component identity) is a basin census, and a basin census is quench-bound. At 2.5s/quench a 10k-endpoint census is ~7 hours single-threaded; the same census at Rust-LP speed is minutes. That ratio, not the annealer, is what decides how many hypotheses can be tested per session.
