# Exact N153 and N302 Certificates — PingYou Ltd

These complete algebraic witnesses tighten the N153 and N302 rational certificates
submitted in [PR 574](https://github.com/jlevy/squares/pull/574). They attain the
previously derived construction sides exactly. The comparison is against the
[immutable v2 submission](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2).

| Count | Exact enclosing side | Approximate side | Reduction from submitted rational side |
| --- | --- | --- | --- |
| 153 | `12 + (1+3t²)/(1+2t−t²)` | 12.87001385040446434446015340078059… | 2.302801065869619 × 10⁻¹⁵ |
| 302 | `33/2 + (7/2)t + t²` | 17.87027538255505966957269257339824… | 3.438801434779458 × 10⁻²¹ |

For N153, `t` is the unique root in `(7/20,9/25)` of
`t⁷−9t⁶+3t⁵−t⁴−t³+t²−3t+1`.
For N302, it is the unique root in that interval of `2t³−3t²−2t+1`.
The two occurrences of `t` refer to different roots. Decimal displays are
approximations; the defining equations and exact coordinate tables are the claims.

The [source release](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-exact-153-302-2026-10-13-v1) contains `pingyou-exact-153-302-2026-10-13.zip`
(235073 bytes, SHA-256 `cea5e95dc3c7a719582a2f58f24fd89171c9b29424c913513373092465783814`).
The [HostedData manifest](../../../hosted/pingyou-exact-153-302-2026-10-13.yaml) records its custody.
Extract the archive and enter its `pingyou-exact-153-302/` directory.

## Verify

From the extracted package root, with Python 3.12 or later:

```sh
python3 independent/verify_attainments.py
python3 n153/verify.py
python3 n153/native/check_conversion.py
python3 n302/verify.py
```

The independent checker uses only the standard library. It recomputes native
separating axes without trusting the supplied pair certificates, checks both
irreducible number fields and root intervals, all 455 unit-square frames, all
1,820 wall inequalities, and all 57,079 unordered pairs. Its exact comparisons
prove both reductions from the named predecessor sides. Invalid nonunit and
overlapping-square controls are recorded in `independent/NEGATIVE-CONTROLS.json`.

Each case also contains a native `packing.squares:Witness/v2` file, its conversion
check, and an independent upstream verification receipt. The unchanged upstream
verifier passed both cases at revision
`e96e9ea95c15c6ad3a9a547a8cb02760e721cfc4`. From an installed Squares Project
checkout's `packing/` directory:

```sh
uv run --frozen packing-witness verify /path/to/n153/native/pingyou-n153-algebraic.yaml --json
uv run --frozen packing-witness verify /path/to/n302/native/pingyou-n302-algebraic.yaml --json
```

The native format stores scalar coefficients lowest degree first. The portable
geometry stores them highest degree first. Exact conversion checks preserve the
side, centers, frames, root choice and physical square ownership.
`SHA256SUMS` binds every included file; `claims.json` binds the predecessor hashes,
geometry hashes and native witness hashes. The preceding rational certificates
remain available in v2 and are not replaced in that archive.

## Scope and Attribution

These are complete feasible upper bounds and strictly tighter certificates of
existing constructions. They establish no global lower bound or global
optimality. They supersede two entries in the 147-count submission and do not
increase that count. Maintainer review and intake remain pending.

Construction and certificate refinement: **PingYou Ltd**. Underlying N70
construction: **Ryan Xu**. Retained exact N70 source and earlier checking and
regularization: **Evan Daniel**. Prior comparator construction: **Nate
Chaoweeraprasit (SQUISH)**. The case credit records retain their distinct roles
and historical source identifiers; those identifiers are not replay dependencies.

Native schema and upstream verification software: **Joshua Levy and the Squares
Project**, https://github.com/jlevy/squares. `UPSTREAM-LICENSE.txt` contains the
upstream licensing terms. This package grants no new blanket license over
third-party geometry or source material.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
