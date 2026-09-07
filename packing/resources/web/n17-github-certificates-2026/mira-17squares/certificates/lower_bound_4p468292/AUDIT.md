# Audit checklist for `s(17) > 4.468292`

## Mathematical statement

- Claimed side: `4468292/1000000 = 4.468292`.
- Witness denominator: `10000000`.
- Witness count: 16.
- Triangle count: 18.
- Every triangle edge is checked strictly shorter than one.
- Point leaves certify strict interior containment over a complete pose box.
- Triangle leaves certify that the complete center rectangle lies strictly in a
  valid triangle.
- Infeasible leaves certify that the complete pose box violates outer-square
  containment.
- The tree covers the complete root box and obeys the full-binary-tree identity.

## Deterministic byte stream

```text
raw bytes:   122626747
raw SHA-256: 2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2
xz bytes:    374096
xz SHA-256:  a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac
```

## Accepted statistics

```text
nodes       = 122626747
split       =  61313373
point       =  33762069
triangle    =    483875
infeasible  =  27067430
max_depth   =         74
```

Leaf accounting:

```text
33762069 + 483875 + 27067430 = 61313374 = 61313373 + 1.
```

## Independent implementations

- `verify_certificate.cpp`: fast exact C++ implementation.
- `verify_certificate_bigint.cpp`: independent unbounded-integer C++ implementation.
- `verify_certificate.py`: independent Python arbitrary-integer implementation.

## Recommended external audit

1. Read and independently prove the triangle-piercing lemma.
2. Check the scale conversions in one checker.
3. Run `verify_archived.sh` under a second compiler/toolchain.
4. Reimplement the checker from `PROOF.md` without consulting the existing code.
5. Run `verify_4p468292.sh` to reproduce the certificate byte-for-byte.
