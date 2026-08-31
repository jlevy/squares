---
type: is
id: is-01m0qwzssmdpwmywmpszsaaxhb
title: Golden basin maps for the small proved cases, grounded in mathematics not in a prior run
kind: task
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4asxdaenzfkx53j4vh6qs
parent_id: is-01m0pw7redm194km37gpb3cvmf
created_at: 2026-08-23T18:09:09.427Z
updated_at: 2026-08-23T19:40:03.548Z
closed_at: 2026-08-23T19:40:03.548Z
close_reason: |
  Built as tools/golden_basins.py plus golden/basin-maps.yaml on claude/packing-overnight-strategy-queue (PR #14), wired into test.sh.

  Wider than the spec asked for: n = 1, 2, 3, 4, 5, 9, 10 rather than n = 1..5.

  The design point is that the assertions are grounded in things that were true before this code existed, not in a previous run. A golden captured from a wrong run is a wrong answer with a checksum on it, and D-030 is the live example -- a golden taken that morning would have frozen twelve interrupted descents as twelve basins. So the oracles are: the proved s(n) read from frontier/; closed-form recognition via the new sqpack/closed_form.py, whose search space is bounded so its coincidence probability is stateable (~3e-6 at 1e-11); and sqpack.verify through code the quench does not share (R1). No basin may lie below a proved optimum, which is a bug unconditionally rather than a record.

  Convergence and discovery are deliberately separated. Convergence -- given a start in the optimum's basin, does the pipeline land on it -- is a property of the tools, is deterministic, and is asserted. Discovery -- does uniform multistart find it in N draws -- is a property of the landscape, is probabilistic, and is recorded as data. The first version conflated them and failed on seed luck; that is what H-012 exists to measure, not what a gate should assert.

  It earned its place on the first run: it found D-031 at n = 3, where basin identity was splitting an angle at the pi/2 seam and storing two images of one packing as two basins. Verified against three tamper modes; two of the first tampers passed vacuously (YAML escapes the surd, a float renders 8.882e-15 not 8.9e-15) and were fixed by asserting the anchor matched exactly.

  Fast path: verify_stored() re-checks the oracles against the committed map without re-quenching, 221s -> 0.6s, which is what made it affordable in the gate. Regeneration still happens under ./test.sh --deep and is required by the handover gate.
resolution: null
duplicate_of: null
---
