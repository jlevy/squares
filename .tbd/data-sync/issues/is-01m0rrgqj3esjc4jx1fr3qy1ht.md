---
type: is
id: is-01m0rrgqj3esjc4jx1fr3qy1ht
title: "Engineering: make packing research code clear, safe, and scalable"
kind: epic
status: open
priority: 1
version: 36
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
child_order_hints:
  - is-01m0ttevapnhz0sgm9r09gweew
  - is-01m0ttf36md7yh66m1gz6h6svn
  - is-01m0ttfczkhxs9fqa6kwphy8rx
  - is-01m0rrhw3a0zqmyw095twj9bn3
  - is-01m0rrhwpct8th5qckp9w959bv
  - is-01m0rrjstb9c806nbjzzfaj1ss
  - is-01m0rrwmf90rynrj697ge7nk1k
  - is-01m0ttfnkek9mx0kv3rgqjth3r
  - is-01m0ttgtaj1j5rp28wxw84v4wr
  - is-01m0ttfx53tjv841cn2v2anyf2
  - is-01m0ttg3v5303w5k65gc8th28m
  - is-01m0ttgbpts9xfvqz0wck4781q
  - is-01m0ttgkhcyks8na3prg20kk8c
  - is-01m0tth2dgvwnagwh2975ac6k3
  - is-01m0s8tvzd11dyjk9s2fw40z16
  - is-01m0rrjt4p850rt1t2z32b5sm0
  - is-01m0rrhwd2zzyj0x0jwa8cqwtw
  - is-01m0rrjtdy1zxafc7790ssa720
  - is-01m0rrjtq99x8zbzd5hvqxrjcg
  - is-01m0rwwt8912eq5f3507d581e1
  - is-01m0vgy59tee79g1gdy13ev2jq
  - is-01m0vj13yefxcxhhew81ewfpvq
  - is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-24T02:10:15.746Z
updated_at: 2026-08-25T05:38:19.498Z
---
Umbrella for the packing engineering-maturity plan: classify code by reuse and consequence, separate shared foundations from stable research-loop tools and retained case code, establish a refactor-safety harness, standardize on Python 3.14, improve CLI and documentation quality, migrate substantial shell orchestration to Python, and optimize measured research-loop bottlenecks without burdening one-off experiments.

## Notes

Reconciliation: keep think-xzew and think-rthe under the existing efficiency review; think-ldq2 under the process review; think-lcfd and think-ugt1 under the minimal-toolkit spec; and think-krqi under unattended-readiness. The cleanup reused those acceptance contracts rather than duplicating them.

The structural tranche merged in PR #23 after rebasing through the exp-036 n=5 second-order-obstruction round and PR #22 workflow-entry/session-contract integration. The post-merge readiness review passed all 31 packing-validate steps in 113.31 seconds under Python 3.14, including 36 pytest contracts, 58 private-snapshot mutation controls, Python and Rust quality, exact and differential mathematics, replay, schemas, generated views, provenance, and campaign invariants. The focused cleanup beads, existing CI bead think-lrsk, and negative-control timeout bead think-cns0 are closed with evidence. D-226 through D-228 record and regress the clean-run CI history/cache defects and the workflow-test parser defect. Implementation commit 8f53f8e passed Linux and macOS CI; final PR receipt head 359c3a0 passed Linux in 2 minutes 37 seconds and macOS in 5 minutes 5 seconds.

Keep this epic open for the distinct numerical and measured-performance work in think-sk15, think-y91x, think-lwao, think-9qz0, think-u97a, think-uvmb, think-r33j, and the outer validation timeout follow-up think-tx0b. Those research and robustness contracts were reconciled but not absorbed or declared fixed by module movement.
