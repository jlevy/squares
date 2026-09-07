# Provenance and relationship to the original result

This package is a response/improvement to the public repository
`Mira-acc/17squares`:

```text
https://github.com/Mira-acc/17squares
```

The original repository states and certifies

```text
s(17) > 4.450837
```

using a 16-point piercing set, a deterministic pose-space subdivision
certificate, and three exact checkers. This package preserves that proof idea and
certificate protocol while replacing the side length, rational point set, and
resulting certificate with the stronger `4.456575` instance.

The optimization/search history used to discover the new point set is not
needed for verification and is omitted.

## Attribution / licensing note

At the time this response package was prepared, the upstream repository did not
advertise an explicit `LICENSE` file in its top-level file listing. Several files
here intentionally follow/adapt the upstream certificate architecture so that
the result is easy for the original maintainer to review.

If publishing this package as a separate public repository rather than sending
it as a proposed upstream contribution, it is prudent to ask the upstream
maintainer what license/attribution they prefer for adapted verifier/generator
source. The new rational point data and generated certificate are identified
separately in `points.json` and `MANIFEST.sha256`.
