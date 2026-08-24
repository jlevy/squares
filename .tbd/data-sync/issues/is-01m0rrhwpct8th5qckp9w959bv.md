---
type: is
id: is-01m0rrhwpct8th5qckp9w959bv
title: golden/basin-maps.yaml is byte-frozen, so it cannot tell 'improved' from 'broke'
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:10:53.772Z
updated_at: 2026-08-24T02:10:53.772Z
---
tools/golden_basins.py --deep compares re-quenched output to the committed file with GOLDEN.read_text() != rendered -- an exact string comparison over floats formatted to 10 decimals plus derived counts.

The file's own docstring argues the oracles are mathematics, not a captured run ('A golden captured from a previous RUN would only freeze whatever the code did that morning'). The fast path honours that. The deep path adds a byte comparison that does not, and that is the path --strict forces, i.e. the unattended handover gate.

Consequences, all of them observed on this branch:
- A mathematically-identical refactor of the quench fails the handover gate. Reviewing the failure costs a 90s regeneration plus a by-hand judgement about whether the diff is real.
- It will fail on a different CPU, a different scipy or HiGHS build, or under different compiler flags. This is also the reason -C target-cpu=native must stay off: it changes float contraction and would break both this and engine determinism.
- Because it cannot discriminate, the safe-looking response to a red deep gate is to regenerate, which is exactly how a real regression gets accepted.

Suggested split: keep byte-exact comparison for the structural and categorical fields (n, proved value, closed-form name, validity, converged flag) and compare the float fields at a declared tolerance; make a change in the basin PARTITION loud and a change in the 10th decimal quiet.
