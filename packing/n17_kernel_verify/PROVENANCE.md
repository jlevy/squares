# Provenance of `n17_kernel_verifier/`

## Specification

The checks, their order, their failure messages and the receipt are those of
`packing/devtools/verify_n17_kernel_certificate.py` of
[jlevy/squares](https://github.com/jlevy/squares) at commit `ef79288a4` (identical to
the file at `4148483da`, the commit the test certificates were produced with).
That file was read in full and ported function by function; the mapping is one to one
(for example `owned`, `core_strict`, `difference_facets`, `covered_by_sweep`,
`degenerate_covered`, `check_step`, `compress`, `derive_closure`).

## Independence

- No certificate generator was read: not `packing/devtools/check_n17_subpattern.py`, not
  `sqpack.hull_kernel`, and not any Rust port of the generator.
- No code is shared with the Rust generator work this verifier is meant to check, and
  the integer library differs (this crate: GMP through `rug` with an `i128` fast path;
  the generator work: `malachite`).
- The 24 cells in `cells/cover.json` were exported once from upstream’s cover tool
  (`packing/devtools/check_n17_capacity_one_cover.py`, `build_cover(UNIQUE_24)`); the
  tests check the embedded copy against the Python verifier’s frame.

## Licences

This directory is a port of this repository’s MIT-licensed code and is offered under the
same licence. Its tests read the stalled W7 certificate in place from this repository’s
campaign record (`packing/campaign/explorations/X048-session-168-pilots/
audit-verifier-rewrites/fixture-w7-bins8/`); no copy is kept here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
