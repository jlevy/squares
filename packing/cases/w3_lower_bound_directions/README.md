# W3 Lower-Bound Direction Diagnostics

This directory retains the bounded diagnostics used by
[X-043](../../campaign/explorations/X-043-new-lower-bound-proof-directions.md),
[X-044](../../campaign/explorations/X-044-low-n-certificate-transfer.md), and
[X-045](../../campaign/explorations/X-045-n11-global-capture-and-exact-optimality.md).
They screen proof directions and source arithmetic.
They do not certify a new packing bound, replay a complete certificate, or promote a
Frontier field.

`innovation_probes.py` produced three finite diagnostics:

- `token-groups.json` tests whether a bounded family of overlapping threshold features
  has a stricter joint token capacity than the sum of its separate capacities.
- `weak-pose-graph.json` builds and checks a greedy clique partition of retained n17
  low-charge witness centres.
- `weak-pose-graph-margins.json` rechecks that partition at the source parent side and
  at the illustrative target side `463/100`.

`frontier_transfer_audit.py` produced `frontier-transfer-audit.json` and
`frontier-transfer-count-slack.json` from immutable Git objects at
`be736b0ef05ac2f256691bc3ded21873ad1f2ab1`. The receipts preserve the original command,
interpreter, runtime, exact arithmetic, and scope verbatim.
Their historical absolute paths describe the run that occurred; they are not current
reproduction instructions.

`structural_endpoint_audit.py` produced the two structural-endpoint receipts from the
same immutable source commit.
The initial receipt preserves a display defect in `FieldElement.decimal`; its exact
signs and enclosures remain valid.
The corrected receipt uses an explicitly approximate fixed-point Decimal midpoint.
The shared display defect is tracked by `think-xy0r` and is outside this research
branch.

From the repository root, reproduce the diagnostics with project Python 3.14 and fresh
output names:

```bash
packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/innovation_probes.py \
  token-groups \
  --source packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json \
  --output /private/tmp/w3-token-groups-fresh.json \
  --seconds 30

packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/innovation_probes.py \
  weak-pose-graph \
  --source packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/global-certificate.json \
  --cells packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-cells.jsonl \
  --output /private/tmp/w3-weak-pose-graph-fresh.json \
  --seconds 30 \
  --target-side 463/100

packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/frontier_transfer_audit.py \
  --repo . \
  --commit be736b0ef05ac2f256691bc3ded21873ad1f2ab1 \
  --output /private/tmp/w3-frontier-transfer-audit-fresh.json \
  --seconds 10

PYTHONPATH=packing:packing/src packing/.venv/bin/python3 \
  packing/cases/w3_lower_bound_directions/structural_endpoint_audit.py \
  --repo . \
  --commit be736b0ef05ac2f256691bc3ded21873ad1f2ab1 \
  --output /private/tmp/w3-structural-endpoint-audit-fresh.json \
  --seconds 15
```

Each tool refuses to overwrite an existing output.
Use another fresh filename for every replay.
The finite diagnostics retain their own limits: sampled centres do not cover a
continuous bad-pose region, a surviving relaxation is not a packing, and display gaps do
not replace exact endpoint comparisons.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
