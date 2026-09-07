# Verification guide

## Deterministic certificate archive

```bash
bash ./verify_archived.sh
```

This command verifies the stored XZ archive and then:

1. decompresses the raw 122,626,747-byte certificate into a temporary directory;
2. verifies the decompressed SHA-256;
3. compiles and runs three exact checkers;
4. runs small corruption/rejection tests.

Expected markers:

```text
CERTIFICATE_VALID_4P468292
BIGINT_CERTIFICATE_VALID_4P468292
PYTHON_INTEGER_CERTIFICATE_VALID_4P468292
REJECTION_TESTS_PASSED_4P468292
ARCHIVED_CERTIFICATE_VERIFIED_4P468292
```

## Full deterministic reproduction

```bash
bash ./verify_4p468292.sh
```

This regenerates the complete certificate from
`generate_certificate.cpp`, checks its SHA-256, compares it byte-for-byte with
the stored archive, and then runs the three exact checkers on the
generated stream.

Expected final marker:

```text
ALL_EXACT_CHECKS_PASSED_4P468292
```

## Trusted core

The search procedure and generator do not need to be trusted. The theorem rests
on:

- the elementary geometric lemmas in `PROOF.md`;
- the 16 rational points and 18 rational triangles in `points.json`;
- the pinned certificate byte stream;
- a correct exact checker.

The fast C++ checker uses fixed-width wide integers where bounds permit and
`boost::multiprecision::int256_t` for the largest products. The second C++
checker uses unbounded `cpp_int` arithmetic throughout. The Python checker is an
independent arbitrary-integer implementation. No floating-point arithmetic,
optimizer, SAT/SMT solver, or interval library is used in leaf verification.
