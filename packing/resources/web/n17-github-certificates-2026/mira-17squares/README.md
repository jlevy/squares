# Packing 17 unit squares in a square

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary orientations. This repository
contains an exact computer-assisted proof that

\[
\boxed{s(17)>4.468292}.
\]

The previous exact computer-assisted bound was `s(17) > 4.456575`, proved in
[Stanislav Fort's certificate repository](https://github.com/stanislavfort/17squares).

## Read the proof

- [Paper (PDF)](paper/17squares-lower-bound.pdf)
- [LaTeX source](paper/main.tex)
- [Exact certificate package](certificates/lower_bound_4p468292)
- [Proof interface and triangle lemma](certificates/lower_bound_4p468292/PROOF.md)

The proof supplies sixteen rational points in the square of side
`4468292/1000000`. A 122,626,747-node exact subdivision certificate proves that
every contained unit square, at every orientation, contains one of those points
strictly in its interior. In addition to direct point witnesses, the certificate
uses a strict triangle-piercing lemma to cover some regions independently of
orientation. Seventeen interior-disjoint squares would require seventeen
distinct points, so no such packing exists at that side length. Compactness
makes the resulting lower bound strict.

## Verify the certificate

Requirements:

- Python 3
- a C++17 compiler
- Boost headers
- `xz` and `sha256sum`

Run the full deterministic reproduction:

```bash
bash ./verify_all.sh
```

This regenerates all 122,626,747 certificate bytes, checks the raw SHA-256,
compares the result byte-for-byte with the archived XZ stream, and validates the
tree with three exact checkers. The raw certificate is larger than GitHub's
ordinary per-file limit, so the repository stores its deterministic 374,096-byte
XZ archive.

For the faster audit that checks the archive without regenerating the tree, run:

```bash
bash certificates/lower_bound_4p468292/verify_archived.sh
```

See [VERIFY.md](VERIFY.md) for hashes, expected output, and the trust boundary.

## Repository contents

```text
paper/                                  paper source and rendered PDF
certificates/lower_bound_4p468292/      points, triangles, archive, generator, checkers
verify_all.sh                           full deterministic reproduction
```

Search experiments and weaker historical certificates are intentionally omitted
from this publication repository. There is no hosted CI; verification is an
explicit local command.

## Status

The certificate has been reproduced with the included exact checkers. The result
has not undergone independent peer review.
