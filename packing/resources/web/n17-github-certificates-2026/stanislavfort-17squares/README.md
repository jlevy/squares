Warning: everything here has been done by GPT-5.6-Sol with high reasoning settings. I, Stanislav Fort, don't really understand it => can't vouch for its correctness. But it should be checkable by other AIs and/or knowledgeable humans.

# Packing 17 unit squares: exact lower bound `s(17) > 4.456575`

This repository is a self-contained computer-assisted certificate for

\[
\boxed{s(17)>4.456575},
\]

where `s(17)` is the least side length of a square containing 17 pairwise
interior-disjoint unit squares with arbitrary orientations.

It improves the bound `s(17) > 4.450837` in `Mira-acc/17squares` by

```text
4.456575 - 4.450837 = 0.005738.
```

The proof uses the same simple architecture as the original result: give 16
rational witness points and certify, by an exact subdivision of square-pose
space, that every unit square contained in `[0,4.456575]^2` contains at least
one witness strictly in its interior. Seventeen interior-disjoint unit squares
would then require 17 distinct witnesses, impossible with only 16 points.
Compactness makes the lower bound strict.

## Quick audit

Requirements:

- Python 3
- a C++17 compiler (`g++` by default; set `CXX=clang++` if preferred)
- Boost headers
- `sha256sum`

Run the three exact checkers on the archived certificate:

```bash
bash ./verify_archived.sh
```

Expected final marker:

```text
ARCHIVED_CERTIFICATE_VERIFIED_4P456575
```

The checkers use exact integer arithmetic. No floating-point arithmetic,
optimizer, search code, SAT/SMT solver, or interval library is in the trusted
verification path.

## Full deterministic reproduction

To regenerate the complete subdivision certificate from source, compare it
byte-for-byte with the archived certificate, and then run all three exact
checkers:

```bash
bash ./verify_4p456575.sh
```

Expected final marker:

```text
ALL_EXACT_CHECKS_PASSED_4P456575
```

The archived certificate contains **21,696,657 nodes/bytes** and has SHA-256

```text
5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550
```

Certificate statistics:

```text
nodes       = 21,696,657
split       = 10,848,328
covered     = 10,594,408
infeasible  =    253,921
max_depth   = 68
```

## What to read

- [`PROOF.md`](PROOF.md): mathematical proof interface and exact inequalities.
- [`VERIFY.md`](VERIFY.md): verification/reproduction procedure and trust boundary.
- [`AUDIT.md`](AUDIT.md): publication checklist and independently checked facts.
- [`certificates/lower_bound_4p456575/points.json`](certificates/lower_bound_4p456575/points.json): exact 16-point configuration and certificate metadata.
- [`PROVENANCE.md`](PROVENANCE.md): relation to the original repository.
- [`CHANGELOG_FROM_4p452625.md`](CHANGELOG_FROM_4p452625.md): delta from the earlier response checkpoint.

## Repository layout

```text
certificates/lower_bound_4p456575/
    points.json
    square17_lb_4p456575.cert
    generate_certificate.cpp
    lower_bound_common.hpp
    verify_certificate.cpp
    verify_certificate_bigint.cpp
    verify_certificate.py
    README.md
    Makefile
PROOF.md
VERIFY.md
AUDIT.md
PROVENANCE.md
verify_archived.sh
verify_4p456575.sh
tests/rejection_tests.sh
MANIFEST.sha256
```

## Status

The archived certificate has been accepted by three exact implementations,
including two arbitrary-precision implementations. The deterministic generator
reproduces the archived byte stream exactly under the tested GCC toolchain.
This is a computer-assisted proof package, not a claim of peer review.
