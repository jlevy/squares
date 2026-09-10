# A6 Fixed-Support Dual Admission

This package provides the maintained reader and receipt for the seven-row upper dual in
`lane-a6-dual-bracket-10-42.json`. It leaves that historical source receipt unchanged.

Run the reader from the repository root with the project’s Python 3.14 interpreter:

```bash
PYTHONPATH=packing packing/.venv/bin/python3 -m devtools.admit_fixed_support_dual \
  packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-dual-bracket-10-42.json \
  packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a3-family-153-40-sites-round1-exact25.json \
  --output packing/cases/n11_fractional_certificate/a6_dual_upper/receipt.json
```

The retained A3 file serializes all 280 placements used by this fixed-support program.
The reader parses those placements as exact rationals, requires the source to be exactly
D4-closed, and partitions it into 35 eight-placement orbits.
It then requires the certificate’s 35 representatives to name every source orbit exactly
once.

For each of the six point-depth rows, the reader calls `Placement.contains` on every
reconstructed placement.
For the three-of-five row, it reconstructs all eight D4 images, applies the exact
membership threshold, and derives budget `8 floor(5/3) = 8`. It rejects any difference
in the stored sparse row, multiplier, contribution, column, side, support count, budget,
`A^T u`, slack, or bound.
Float display fields do not enter a decision.

The admitted multipliers satisfy `A^T u >= cost` in all 35 columns, with minimum slack
`3/500000000`. Their budget-weighted dual objective `b^T u` is the upper bound
`2605263163/250000000`. This proves the bound for nonnegative D4-tied weights on the
reconstructed fixed support under the seven admitted inequalities.
It also bounds the stronger program that retains those inequalities and adds every exact
point-depth row on the same support.

An untied full-depth claim uses D4 averaging.
The reader checks that the support is D4-closed, every objective orbit cost equals its
eight placements so the objective is total placement mass, and the threshold row sums a
complete eight-image orbit.
The claim must also state that the stronger program retains that threshold-orbit row,
that its complete point-depth family is D4-invariant, and that averaging preserves
feasibility and total placement mass.

The declared lower value `325657893/31250000` is outside this admission.
It was only reported feasible on the selected finite rows, and the retained reader found
maximum depth `105263157/100000000 > 1`. This reader does not replay the full set of
139,521 depth rows, the 2,566 original atom rows, or K0–K3.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
