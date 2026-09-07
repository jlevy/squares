# Verification guide

## The checked statement

The certificate proves:

> Every unit square contained in `[0, 4468292/1000000]^2`, at any orientation,
> contains at least one of the listed sixteen rational points strictly in its
> interior.

Point leaves prove this directly. Triangle leaves prove that the complete center
rectangle lies strictly inside a triangle whose three sides are strictly shorter
than one. The triangle-piercing lemma then puts at least one triangle vertex in
the square interior, regardless of orientation.

The pigeonhole principle rules out seventeen pairwise interior-disjoint unit
squares at the displayed side length. A packing in a smaller container would
also fit there, giving `s(17) ≥ 4468292/1000000`; compactness ensures that the
least feasible side length is attained, so equality is also impossible. Hence

```text
s(17) > 4468292/1000000 = 4.468292.
```

## Full deterministic reproduction

```bash
bash ./verify_all.sh
```

This regenerates the complete tree, checks its raw SHA-256, compares it
byte-for-byte with the decompressed archive, runs all three exact checkers, and
runs malformed-certificate rejection tests.

Expected final marker:

```text
ALL_EXACT_CHECKS_PASSED_4P468292
```

## Faster archived-certificate check

```bash
bash certificates/lower_bound_4p468292/verify_archived.sh
```

This checks the archived XZ hash, decompresses it into a temporary directory,
checks the raw hash, and runs the same checkers and rejection tests without
regenerating the tree.

Expected checker markers:

```text
CERTIFICATE_VALID_4P468292
BIGINT_CERTIFICATE_VALID_4P468292
PYTHON_INTEGER_CERTIFICATE_VALID_4P468292
REJECTION_TESTS_PASSED_4P468292
ARCHIVED_CERTIFICATE_VERIFIED_4P468292
```

## Certificate hashes

```text
2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2  square17_lb_4p468292.cert
a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac  square17_lb_4p468292.cert.xz
```

## Trust boundary

The point search, certificate generator, and certificate bytes are not trusted.
Each checker treats the tree as untrusted input and recomputes every leaf claim.
The fast checker shares an arithmetic header with the generator. The Boost and
Python arbitrary-integer checkers separately implement the point, triangle, and
infeasibility tests and do not depend on bounded-integer overflow arguments.

The arbitrary-integer checkers use no floating-point arithmetic, numerical
optimizer, solver, or interval library. The remaining human argument—the square
parameterization, interval bounds, strict triangle-piercing lemma, tree-cover
induction, pigeonhole step, and compactness step—is given in the
[paper](paper/17squares-lower-bound.pdf) and the package's
[proof interface](certificates/lower_bound_4p468292/PROOF.md).
