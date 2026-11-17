# s(12) ≥ 9929/2500 = 3.9716

**Credit: unnir · [Numaro](https://numaro.tech).** Prepared 8 November 2026.

This packet reports a computer-checked lower bound for packing twelve unit squares, each independently rotated, with pairwise disjoint interiors, inside a square. It excludes containing squares of side **strictly less than 3.9716**. It does not establish the optimal value or provide a packing.

The [public verified n = 12 record](https://squaremath.org/cases/12.html) consulted on 8 November 2026 is 7943/2000 = 3.9715 (T-095). The proposed improvement is exactly **1/10000**. External replay and mathematical review are requested before adoption.

## Certificate and mathematical scope

[`certificate/s12_lower_3.9716.txt`](certificate/s12_lower_3.9716.txt) is a plain weighted-point certificate in Evan Daniel's format, with no clique or region extensions:

| Quantity | Exact value |
| --- | --- |
| Container side | 15886400/4000000 = 9929/2500 |
| Coordinate denominator D | 4000000 |
| Weight denominator W | 9985226 |
| Distinct positive-weight points | 4996 |
| Total weight | 119787760/9985226 ≈ 11.996499628551222 |
| Margin below 12 | 34952/9985226 |
| Minimum captured weight certified by both complete sweeps | 9985226/9985226 = 1 |
| Symmetry | Exact D4 invariance, checked by the Rust verifier |
| Certificate SHA-256 | `833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd` |

The argument is the established weighted closed-cover reduction used by Daniel and the accepted [T-095 registration](https://github.com/jlevy/squares/issues/363). Every closed unit square in the container captures weight at least one, while the total weight is strictly less than twelve. The upstream reduction handles boundary contact and yields the strict-side exclusion stated above. This is a new certificate instance, with no claim to a new mathematical technique.

The angle net is not a sample of placements. Rational endpoint rotations and a conservative shrink bound cover each continuous angle interval; an arrangement sweep checks all admissible translations of the shrunk square for that interval. See the included verifier sources for the precise predicates and the upstream [explanation](https://evand.github.io/square-packing/s12/).

## Completed checks

Raw, unedited outputs are in [`verification/logs`](verification/logs); a machine-readable summary is [`verification/summary.json`](verification/summary.json).

| Checker | Arithmetic and complete scope | Minimum | Exit | Cost on Apple M4 Max, 36 GiB |
| --- | --- | --- | --- | --- |
| Evan Daniel's Rust `verify` | i128 rational/integer geometry; release overflow checks enabled; N = 96000; 39,765 intervals covering [0°,45°] plus checked D4 symmetry | 9985226/9985226 | 0, VERIFIED | 2167.12 s reported wall, 10 threads |
| Ryu Sungjoon's C++ `indep_scan` | Checked __int128 arithmetic and conservative rounding; N = 96000, Q = 10^15; all 96,000 intervals covering [0°,90°], no symmetry assumption | 9985226/9985226 | 0, VERIFIED | Approximately 626.45 s observed wall, one thread |

These two checks ran concurrently. Timings are observations, not uncontended benchmarks. Floating-point angle/centre coordinates in the C++ output are diagnostic; the checking predicates use integer bounds. The Rust log's `bins=39766` statistics field counts one more than the 39,765 processed intervals; its ten per-thread interval counts sum to 39,765. The source loop covers k = 0 through 39764. We retain the upstream output unchanged.

**Independence limits:** both implementations use the same weighted-cover theorem, rational angle net and shrink mechanism, and consume the same certificate. They are separately written implementations, not method-distinct mathematical proofs. These runs are producer evidence, not third-party validation. No Lean replay of this certificate, independent mathematical review, or method-distinct parent-core interval replay is supplied.

## Reproduce

Requirements: Python 3, Rust/Cargo (edition 2021; original build rustc 1.95.0), and a C++20 compiler with `__int128` support (original build Apple Clang 17). The Rust crate has no external dependencies.

From this repository's root:

```sh
shasum -a 256 -c SHA256SUMS
mkdir -p build
cargo rustc --release --locked --manifest-path verifier/rust/Cargo.toml --target-dir build/verify -- -C overflow-checks=yes
clang++ -O3 -std=c++20 verifier/cpp/indep_scan.cpp -o build/indep_scan
python3 verification/replay.py --threads 10
python3 verification/replay.py --controls
```

The replay helper removes inherited `VERIFY_*` and `TIGHT_*` variables before launching the verifiers, checks the certificate digest, requires an explicit `VERIFIED` verdict and exit 0 for each full sweep, and stores fresh output in `replay-output/`. Full sweeps run sequentially in this helper. Expect roughly tens of minutes, depending on the machine.

Equivalent complete verifier invocations, with the same environment sanitization, are:

```sh
VERIFY_STATS=1 build/verify/release/verify certificate/s12_lower_3.9716.txt 12 96000 10 0
build/indep_scan certificate/s12_lower_3.9716.txt 96000 1000000000000000 12
```

Do not set `VERIFY_BINS` or append C++ range arguments to a full verification run: those restrict coverage.

## Negative controls

`python3 verification/replay.py --controls` deterministically generates two altered copies without changing the retained certificate or verifier sources:

1. Double W, keeping all coordinates and weight numerators. Both checkers find exact capture **1/2** at bin 39531 and decline acceptance. These are explicitly **single-bin diagnostics**, not complete sweeps. Rust exits 4 (partial, no verdict); C++ exits 1 with `NOT VERIFIED`.
2. Remove the last point while keeping the declared count 4996. Both parsers exit 2 with an input error.

The original control outputs and exact statuses are retained in [`verification/controls`](verification/controls). No control is presented as a proof that the original bound is optimal.

## Source provenance, credit and licensing

- Rust source, Cargo manifest and lockfile are unchanged from [evand/square-packing at 0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d](https://github.com/evand/square-packing/tree/0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d/verify). Source SHA-256: `aca2fa6f8b42d7973f299a5332d8f7ef200409a0a04fb6eb21d703ff9c8dabc0`. MIT, copyright Evan Daniel.
- C++ source is `tools/indep_scan.cpp` from [squarepacker/s12-lower-bound at 7a96bec36bc6811c3715ef581598f22ff9b7ba3a](https://github.com/squarepacker/s12-lower-bound/blob/7a96bec36bc6811c3715ef581598f22ff9b7ba3a/tools/indep_scan.cpp), with only `<bits/stdc++.h>` replaced by explicit standard-library headers for compiler portability. Checking logic is unchanged. Included source SHA-256: `74146d48aa46287514ea44fcfdab6ed66ff687ccca46f24347dd8b1cf923ac61`. MIT, copyright Ryu Sungjoon; upstream notices retained.
- The underlying lower-bound framework builds on Burns and Massaccesi and subsequent work by Levy, Evan Daniel and Ryu Sungjoon, as recorded in T-095. Credit the new certificate/bound instance to **unnir (Numaro), building on Levy, Evan Daniel and Ryu Sungjoon's work**. No ownership of their reduction or code is claimed.
- Upstream notices are in `LICENSES/`. New certificate and packet helpers/documentation are offered under the MIT license in `LICENSE`.

**AI assistance:** Numaro Autonomous Research (agentic autonomous autoresearch) assisted the work. Numerical acceptance comes from the included executable checks, not agent agreement. This packet contains the certificate and verification evidence; it makes no claim about a new discovery method.

We request an independent replay, ideally including the repository's method-distinct parent-core interval checker, mathematical review, and an n = 12 record update if confirmed.
