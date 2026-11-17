# Polkovskyi’s Thirteen Certificates at b637e6c

This packet retains part of
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/b637e6cf59c23781c813e8442bfdccb5aa5f3954)
at `b637e6cf59c23781c813e8442bfdccb5aa5f3954` (committed 2026-11-16T23:31:56Z), the
repository’s head and the commit
[issue #1009](https://github.com/jlevy/squares/issues/1009) names, opened at 23:38:22Z by
Mykhailo Polkovskyi (Mishapolk).
Intake lane c-import-1009-1117 (bead think-i38n) fetched it at 01:40Z on 17 November
2026, when `git ls-remote` read the same head.

GitHub’s activity log for the repository, read here, shows how the commit was published.
At 23:27:18Z a push moved `main` from `52aa267`, the last read, to `b9b7fa7a01` (committed
23:27:09Z, parent `52aa267`), and at 23:32:03Z a force-push replaced it with `b637e6c`.
`b9b7fa7` holds the 13 certificates, the 13 Witness/v2 files, both `SHA256SUMS` lists,
the figures and the two new verifiers byte for byte as `b637e6c` does.
It differs only in `SUBMISSION_2026_11_16.md`, whose heading and prose were rewritten,
and in the two indexes, whose generated times differ and whose credit at the 13 counts
read “Mykhailo Polkovskyi after” each standing holder in `b9b7fa7` and “Mykhailo
Polkovskyi (Mishapolk)” in `b637e6c`. `b9b7fa7` is on no branch now; it was fetched by
its id. So the certificates were first committed at 23:27:09Z and first public at
23:27:18Z, 11 minutes before the issue, and the pin stays `b637e6c`, the commit the
issue names.

## Retained Here

Under `source/`, at their upstream paths:

- the 13 certificates the issue names, `certificates/0000-0999/nN.cert` for N in 147,
  156, 180, 210, 260, 262, 268, 270, 272, 292, 295, 299 and 307;
- the 13 Witness/v2 corner files of the same packings, `witnesses/2026-11-16/n-N.yaml`,
  and their `SHA256SUMS`;
- `SUBMISSION_2026_11_16.md`, and the two new verifiers `verify_area_exact.py` and
  `verify_algebraic_bounds.py`, as data: neither was run here.

Pinned by digest in `acquisition/sources.json`, not copied: the MIT `LICENSE` (against the
issue-732 packet’s copy), the `README.md` (against the issue-846 packet’s), Evan Daniel’s
`verify_bound_certificate.py` and `BOUND_VERIFIER_LICENSE.txt` (against the issue-678
packet’s), `certificates/SHA256SUMS` over the whole repository, the two indexes
`certified_bounds.json` and `upper_bounds.json`, and the 13 figures under
`figures/2026-11-16/`.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-issue1009-2026-11-16 --check
python -m devtools.upper_bound_reports mishapolk-issue1009-2026-11-16 check-claims
python -m devtools.upper_bound_reports mishapolk-issue1009-2026-11-16 check --replay
python -m devtools.upper_bound_reports mishapolk-issue1009-2026-11-16 sharp-controls --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
