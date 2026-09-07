# Exact lower bound `s(17) > 4.468292`

This directory is a self-contained exact computer-assisted proof package for

\[
\boxed{s(17)>\frac{4\,468\,292}{1\,000\,000}=4.468292}.
\]

Here `s(17)` is the least side length of a square containing 17 pairwise
interior-disjoint unit squares with arbitrary orientations.

The package exhibits 16 rational witness points and certifies that every unit
square contained in `[0,4.468292]^2` contains at least one witness strictly in
its interior. The packing conclusion is then the pigeonhole principle.

## What is new

The immediate predecessor was the exact `4.456575` certificate in
`stanislavfort/17squares`. The present point set raises the certified side by

```text
4.468292 - 4.456575 = 0.011717.
```

In addition to the original point-witness leaves, this certificate implements a
strict form of the classical triangle-piercing lemma: if a square center lies
strictly inside a triangle whose three sides are strictly shorter than one,
then the square strictly contains a triangle vertex. Triangle leaves are
checked with integer arithmetic and are independent of the square orientation.

## Certificate transport

The raw certificate has 122,626,747 one-byte nodes, which is above GitHub's
ordinary 100 MB per-file limit. The repository therefore stores its
deterministic 374,096-byte XZ archive together with hashes for both forms.

Decompressed certificate SHA-256:

```text
2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2
```

Compressed archive SHA-256:

```text
a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac
```

Certificate statistics:

```text
nodes       = 122,626,747
split       =  61,313,373
point       =  33,762,069
triangle    =     483,875
infeasible  =  27,067,430
max_depth   =          74
```

## Verification

Run the archived certificate through all three exact checkers:

```bash
bash ./verify_archived.sh
```

Regenerate the full 122,626,747-byte tree, compare it byte-for-byte with the
archive, and rerun all checkers:

```bash
bash ./verify_4p468292.sh
```

Requirements:

- Python 3
- a C++17 compiler
- Boost headers
- `xz`, `sha256sum`, and standard POSIX shell tools

See [`PROOF.md`](PROOF.md), [`VERIFY.md`](VERIFY.md), and
[`AUDIT.md`](AUDIT.md) for the mathematical interface and trust boundary. The
immediate point-only predecessor is
[`stanislavfort/17squares`](https://github.com/stanislavfort/17squares).
