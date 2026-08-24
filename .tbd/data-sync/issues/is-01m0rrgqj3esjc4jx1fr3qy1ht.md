---
type: is
id: is-01m0rrgqj3esjc4jx1fr3qy1ht
title: "Engineering: make packing research code clear, safe, and scalable"
kind: epic
status: open
priority: 1
version: 28
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
created_at: 2026-08-24T02:10:15.746Z
updated_at: 2026-08-24T23:25:52.377Z
---
Umbrella for the packing engineering-maturity plan: classify code by reuse and consequence, separate shared foundations from stable research-loop tools and retained case code, establish a refactor-safety harness, standardize on Python 3.14, improve CLI and documentation quality, migrate substantial shell orchestration to Python, and optimize measured research-loop bottlenecks without burdening one-off experiments.

## Notes

Reconciliation: keep think-xzew and think-rthe under the existing efficiency review; think-ldq2 under the process review; think-lcfd and think-ugt1 under the minimal-toolkit spec; and think-krqi under unattended-readiness. The cleanup reused those acceptance contracts rather than duplicating them.

The structural tranche is implemented on stacked PR #23 above PR #22 and rebased through the exp-036 n=5 second-order-obstruction round. The definitive local packing-validate run passed all 31 steps in 112.21 seconds under Python 3.14: 16 pytest contracts, 38 one-worker mutation controls, Python and Rust quality, exact and differential mathematics, replay, schemas, generated views, provenance, and campaign invariants. The focused cleanup beads, existing CI bead think-lrsk, and negative-control timeout bead think-cns0 are closed with evidence. D-205 through D-207 record and regress the first clean-run CI history/cache defects and the workflow-test parser defect.

Keep this epic open for the distinct numerical and measured-performance work in think-sk15, think-y91x, think-lwao, think-9qz0, think-u97a, think-uvmb, and think-r33j. Those research contracts were reconciled but not absorbed or declared fixed by module movement.
