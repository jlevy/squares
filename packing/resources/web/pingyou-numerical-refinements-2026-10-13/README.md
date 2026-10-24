# PingYou Ltd: 147 cumulative rational certificate refinements

This updates [PR 574](https://github.com/jlevy/squares/pull/574) to request review of
147 complete rational square-packing certificates.
All improve their cited pre-batch public certificate.
Of these, **96 are further strict reductions** relative to the preceding public
witnesses, including our v1 release; **51 retain identical v1 certificate bytes**. This
is not a claim of 147 newly better bounds than the now-public v1 submission.

The claims include reductions of certificate padding and tighter realizations of known
constructions. They do not assert new nominal designs, improvements over known algebraic
optima, or local or global optimality.
The [claims](claims.json) separate cumulative and further gains; the
[comparison](comparison.json) accounts for all 149 audited counts.
N105 and N146 now have further improvements and enter this cumulative request.
N261 remains omitted because the same side is already public.
N154 remains held back because
[a stronger pending report](https://github.com/jlevy/squares/issues/570) has an
unavailable linked certificate.
Earlier reports are linked in the corresponding claim rows.

The [exact N153/N302 supplement](../pingyou-exact-153-302-2026-10-13/README.md)
supersedes the rational witnesses for those two counts with attained algebraic sides.
The 147-count scope is unchanged; the other 145 entries and these v2 archives remain
available as submitted.

## Source and custody

The versioned
[v2 source release](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2)
uses tag `data/pingyou-numerical-refinements-2026-10-13-v2`. The
[v1 release](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v1)
remains available as the preceding submission.
The [HostedData manifest](../../../hosted/pingyou-numerical-refinements-2026-10-13.yaml)
binds the v2 asset locations, byte sizes and SHA-256 digests.
The filenames are retained under a distinct tag; v1 assets are not overwritten.

The portable archive contains complete final certificates, named pre-batch comparators,
preceding public comparators including v1, exact gain tables, source provenance and
verification receipts.
The native archive contains rational corner Witness/v2 encodings.
Downloaded bytes are checked at the external-data boundary; no Git history is needed to
reconstruct the geometry.
Upstream verification software retains its license in `native/upstream/`; this
submission asserts no new blanket license grant over geometry or retained source
material.

## Reproduce

Use the pinned Python 3.14 environment.
From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch --manifest hosted/pingyou-numerical-refinements-2026-10-13.yaml
```

Extract both archives beneath `attic/pingyou-numerical-refinements-2026-10-13/` at the
repository root, retaining their internal paths.
From the portable archive’s `numerical-refinements/` directory, run `python VERIFY.py`
as documented in its README. Its exact SAT and polygon checks validate the final and
comparison geometry and reject invalid containment and overlap controls.

For every requested row, run both native routes on its `native_witness` member.
For example, from `packing/`:

```sh
uv run --frozen packing-witness verify ../attic/pingyou-numerical-refinements-2026-10-13/native/witnesses/pingyou-n153-rational.yaml --json
uv run --frozen python -m devtools.check_rational_witness_independent ../attic/pingyou-numerical-refinements-2026-10-13/native/witnesses/pingyou-n153-rational.yaml
```

A valid finite claim has exactly `n` unit squares, satisfies every wall constraint, and
passes all `n(n-1)/2` pair checks.
Precision alone is not the validation criterion.
The exact half-angle conversion uses `c=(1-t*t)/(1+t*t)` and `s=2*t/(1+t*t)` to produce
cyclic corners without changing the centre or side.

## Evidence and limits

The portable exact SAT and polygon checkers accepted all 147 final certificates and all
147 pre-batch comparator certificates, covering 2,678,449 unordered pairs per checker in
each group. Deliberate outside-container and duplicate-square controls were rejected.

Both unchanged native verifier implementations accepted all 147 requested witnesses,
covering 2,678,449 unordered pairs per implementation.
Receipts for 96 changed witnesses were replayed for v2; receipts for 51 byte-identical
v1 witnesses were retained.
Native replay and conversion receipts are included in the native archive.

The SAT and polygon routes share rational source data and the standard-library fraction
type, but decide overlap by different geometric calculations.
The two native routes share Witness/v2 input and YAML loading; the independent corner
checker shares no geometry code with `sqpack.witness` or `sqpack.verify`. Conversion
receipts bind each native witness to its centre/half-angle source.

The full archive records the historical bank and the current v2 selection.
The 96 further gains and the 51 unchanged proposals are recorded separately.
Structural derivations, equal-value alternatives and failed construction families remain
research evidence; they are not additional record claims.
These contributor checks request review and do not assign the repository’s confirmation
or significance ratings.

## Credit

The requested credit for the numerical certificate refinements is **PingYou Ltd**.
Original construction authors, preceding refiners and source/tool authors retain their
roles, listed per count and in full provenance.
Padding reduction does not transfer authorship of an existing packing.
The underlying work includes Ryan Xu, Robert Barnett, Evan Daniel, Francisco Couzo,
Daniil Ostashev and the other authors named per count.
Evan Daniel’s exact-source and solver contributions are retained where applicable.

This packet requests maintainer intake under the
[result-import process](../../../campaign/result-import.md).
It reserves no result identifier, changes no accepted case record, and assigns no
confirmation score.


## Further exact certificate updates

The [algebraic supplement](../pingyou-algebraic-refinements-2026-10-13/README.md) replaces 59 of these 147 witnesses with strictly tighter exact certificates and adds the further refinement of the separately submitted N261. The cumulative PR therefore covers 148 counts. The earlier exact N153 and N302 supplement remains in place. Original attribution and the immutable v1/v2 archives are preserved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
