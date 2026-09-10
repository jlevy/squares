# Exact Threshold-Atom Orbit Admission

The threshold-atom orbit reader decides whether a retained ceiling family satisfies a
declared finite set of threshold rows.
It uses the historical A6 atom envelope and recomputes every quantity needed for the
decision.

For a seed set $S$, threshold $k$, and its distinct D4 orbit, the reader checks

$$
\sum_{gS}\ \sum_{P:\lvert P\cap gS\rvert\ge k} y_P
\;\le\;
\lvert D4.S\rvert\left\lfloor\frac{\lvert S\rvert}{k}\right\rfloor.
$$

The support size is the number of distinct points in the input seed.
The reader does not substitute the legacy three-point constant when it computes the
budget.

## Input Contract

The family is any record accepted by `CeilingCertificate.from_record` with a required
`total_weight`. Every placement weight must be nonnegative, and the declared total must
equal the exact sum of the placement weights.

The atom input is a JSON object with this shape:

```json
{
  "outer_side": "153/40",
  "square_side": "9977/10000",
  "atoms": [
    {
      "points": [["1/2", "1/3"], ["2/3", "3/4"], ["4/5", "5/6"]],
      "threshold": 2,
      "orbit_size": 8
    }
  ]
}
```

`outer_side` is required and must equal the family side.
When `square_side` is present, it must also equal the family value.
Each point must lie in the closed container, each seed must have distinct points, and
`threshold` must lie in `1..|S|`. The reader reconstructs the distinct D4 images and
refuses a mismatched `orbit_size`.

## Exact Decision

JSON decimal tokens are parsed as base-ten rationals.
The reader collects every distinct site in every reconstructed image and calls
`Placement.contains` for each site-placement pair.
Its two slab inequalities use `Fraction` throughout and include the boundary.
No float screen or tolerance enters the verdict.

The receipt records every image charge, the aggregate charge and budget, exact slack and
ratio, the worst row, and every violation.
Exit status `0` means every declared atom row is admitted, `1` means the inputs are
valid and at least one row is violated, and `2` means the input contract failed.

Run it from `packing/`:

```bash
uv run --frozen --all-extras --group dev \
  python -m devtools.admit_threshold_atom_orbits FAMILY.json ATOMS.json
```

## Separate Ceiling Obligation

Atom admission does not prove that the family is an admissible ceiling certificate.
The receipt marks K0--K3 unchecked.
Run the independent ceiling reader separately to decide placement admissibility,
containment, maximum depth, total weight against $n$, and D4 symmetry:

```bash
uv run --frozen --all-extras --group dev \
  python -m devtools.independent_ceiling_reader FAMILY.json
```

Both successful receipts are required before using an admitted family as proof evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
