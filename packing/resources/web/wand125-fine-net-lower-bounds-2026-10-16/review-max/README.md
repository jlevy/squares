# Independent Mathematical Audit of the n = 108 Certificate

This directory retains the code and exact calculations for
[Review C](../../../../../docs/project/reviews/review-2026-10-18-n108-fine-net-mathematics-max.md)
of PR #671 at `32d47d3214ec28f2a82b89689cd8bb8f63f98e02`. Reviewer: Codex system family,
strongest tier, maximum reasoning.

## Program and Result

`n108_audit.py` uses Python’s standard library, imports no repository code, and checks:

- Exact positive rectangle data, D4 expansion with multiplicity, total mass, and net,
  core-fit, last-bin, domain, and numerical-cap premises.
- The complete direction-index inventories and summary consistency of the source and
  native retained verification logs.
  This reads their claims; it does not replay their coverage search.
- Exact captures at four native 99/100 control poses (indices 1, 100, 157, 200),
  comparing against the retained rational values.
- Exact capture at the source’s axis 197/200 control pose, whose log has an `argmin` but
  no `exact_below_threshold` field.
- Four analytic geometry controls: an enclosed rotated square, a half overlap, boundary
  contact of zero area, and preservation of mass for a stabilizer orbit.

`audit.json` is the retained stdout.
Its status is `EXACT_PREMISES_AND_FIVE_POSES_PASS`. It reports 823 positive
representatives, 6,524 expanded rectangles, total mass 10799999/100000, and two complete
201-direction receipt inventories.
All five fresh pose calculations pass.
It encloses large rational captures between adjacent multiples of $10^{-18}$; acceptance
and equality comparisons use the full fractions.

This program does **not** decide the universal capture condition or perform a native
replay. No source code, preexisting project audit tool, or verifier executable was run.

## Reproduction

Use Python 3.14.7 from the project’s environment.
From the repository root, after setting `TMPDIR`, `CARGO_TARGET_DIR`, and `UV_CACHE_DIR`
to task-specific directories on the mounted external scratch volume:

```bash
packing/.venv/bin/python3 -I \
  packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-max/n108_audit.py \
  --repo "$PWD" > "$TMPDIR/n108-review-max-audit.json"
```

Do not pass `-O`: the program refuses an interpreter with assertions disabled.
The review used the existing project interpreter at
`/Users/levy/wrk/github/squares/packing/.venv/bin/python3` against its separate
external-volume worktree.
No environment was installed or copied.
Ruff format/check and BasedPyright were also run explicitly on this file, because
`resources/` is excluded from the ordinary source-code floor.

## Read Log and Independence

Before writing the geometry and expansion routines, the reviewer read:

- The n = 108 candidate, source README and bundle metadata, acquisition declaration,
  premise receipt, source/native replay logs, and source/native controls, as data.
- `packing/sqverify_fast/README.md`, `SOUNDNESS.md` through its net and centre-domain
  arguments, and the beginning of `INDEPENDENCE.md` with its structured read log.
- Repository instructions, review and documentation guidelines, and the review
  requirements in `packing/campaign/result-import.md`.

After writing those routines, the reviewer read the maintained
`packing/sqverify_fast/src/certificate.rs` definitions and admission/domain code (lines
1–210 and 448–650), additional sections of `SOUNDNESS.md`, and excerpts of the 6 October
general declared-net soundness review and fix check.
No coverage-search or exact-oracle implementation was read.
No producer code is reused.
The program’s input adapters were corrected after those reads.
Accordingly the structured independence record should say `clean_room: false`,
`shares: []`, and record `producer-code` among its reads.

The review’s findings were written before the reviewer read an earlier review of this
same n = 108 result.
The retained review note records the subsequent comparison.
The mathematical audit code was finished before that comparison.

## Registration Handoff

The records lane, which owns the registries and document map, should register:

- The review note as the n = 108 mathematical review and the reported evidence’s
  `external_review`, with its final bounded verdict and C1 disposition.
- `n108_audit.py` as a new exact-arithmetic audit verifier, suggested ID
  `V-n108-review-max-exact`. It decides the listed premises and sampled captures, not
  the lower bound on its own.
  Retain this README as its independence record.
- An exact-premise evidence entry for the input premises, suggested ID
  `E-n108-review-max-premises`.
- A separate sampled-capture entry, suggested ID `E-n108-review-max-captures`: four of
  the 201 native control witness poses and one of the 32 source control poses.
  If expressed as one sample, that is 5 of 233 *recorded control poses*, not five of 201
  whole direction domains and not a full verification.

The independence fields are: mathematics, proof text, specification, certificate format,
producer output, and producer code read; no shared code; separate prompt and separate
code; Codex family, strongest tier, maximum reasoning; authorship overlap with the
source generator unknown.
The later prior-review comparison is disclosed in the review note; no calculation was
revised to agree with it.
These entries must not label the retained native replay as an independent full
implementation or promote a rung from this sample alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
