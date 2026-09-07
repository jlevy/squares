# Provenance

This package extends two earlier exact certificate packages:

1. `Mira-acc/17squares`, which introduced the exact 16-point pose-space
   certificate architecture and proved `s(17) > 4.450837`;
2. `stanislavfort/17squares`, which optimized the point set within the same
   point-leaf architecture and proved `s(17) > 4.456575`.

The present package keeps the same exact point and infeasibility leaves, changes
the rational point set, and adds strict triangle-piercing leaves. The triangle
principle is a strict version of a classical lemma used in the square-packing
literature; the contribution here is its exact integration into the finite
certificate language and the resulting stronger instance.

The point search, certificate generator, code, and exposition were developed
with substantial assistance from OpenAI's GPT-5.6 Pro under human direction.
The model is not an author. The claim is intended to be judged solely from the
explicit data, proof interface, deterministic certificate, and exact checkers.

This package has not undergone independent peer review at the time of publication.
