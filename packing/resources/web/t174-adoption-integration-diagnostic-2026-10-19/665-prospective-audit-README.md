# Prospective #665 Preservation Diagnostic

[665-prospective-audit.py](665-prospective-audit.py) is a reviewer-owned engineering
diagnostic. It compares immutable source data and exact rational sides for the local
review at `7d47153fb579373cc69488d1e9c1c1f560ddd585`. It decides no packing feasibility,
coverage theorem, rigidity, optimum or new mathematical claim.
It is not cited by any evidence entry, derives no V/C rung, and has no verifier-registry
entry.

The program and [JSON output](665-prospective-audit.json) remain beside the
[review](665-prospective-final-review.md) for the parent to retain with the final
handoff. They have not been committed or published; durable promotion of this review
should preserve all three.
This local location is the explicit reviewer write boundary.
The final retained packet belongs in the result’s packet or `devtools` under *Every
Run’s Code Is Kept* if the parent publishes the diagnostic as project evidence.

## Inputs and Independence

The program reads the three revisions supplied at the command line through Git, using
`git show`, `git cat-file --batch` and `git rev-parse`. Inputs comprise case frontmatter
for n=1…324, the result register, adoption archives, exact house and regularized
witnesses, index/manifest/citation/drawing records, the literal adoption map and
historical custody receipt.
It compares the identity of the retained evidence/verifier registries, PingYou packet
and regularization run packet without running them.
`ast.literal_eval` reads a literal dictionary; no source module is imported or
evaluated.

The author read the task brief, project instructions, Stage 4/5 workflow, epistemic
code-retention rule, inherited source data and receipts, and the adoption/integration
source diff. Earlier same-result review documents were not read before the review’s
independent freeze. The record and brief summarize earlier acceptance, so this is not a
blind result review.
The requested authoring configuration was Codex’s strong-max review role, Astra at max
reasoning; it is a separate prompt and separate diagnostic code, not a new clean-room
geometric checker.

Imports are Python 3.14.7 standard-library `argparse`, `ast`, `fractions`, `gzip`,
`json`, `lzma`, `pathlib` and `subprocess`, plus the already-installed PyYAML parser
(`safe_load`). No project or upstream checker runs.
The primary project virtual environment is used read-only, bytecode writes are disabled,
and no new environment or toolchain is created.

## Run

The external volume was confirmed mounted with 71 GiB available.
The reviewer’s empty scratch directories were created after checking writability.
From the primary repository root:

```bash
TMPDIR=/Volumes/spud-ext1/agent-scratch/665-prospective-math-review-20261019/tmp \
CARGO_TARGET_DIR=/Volumes/spud-ext1/agent-scratch/665-prospective-math-review-20261019/cargo \
UV_CACHE_DIR=/Volumes/spud-ext1/agent-scratch/665-prospective-math-review-20261019/uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
PYTEST_ADDOPTS='-o tmp_path_retention_policy=failed -o tmp_path_retention_count=1' \
/Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  .codex/intake-resume-20261019/665-prospective-audit.py \
  --head 7d47153fb579373cc69488d1e9c1c1f560ddd585 \
  --base 3d34e828fddbe3b3a91172cc48b1ff07ba8d3b07 \
  --preintegration ab9f09e4d79d8b07d16c3ee3906fe748f147617d \
  --output .codex/intake-resume-20261019/665-prospective-audit.json
```

Sandbox escalation was required to write the reviewer-owned JSON under `.codex`. It was
granted; no source file was modified.
The final run exited 0, printed `failures: []`, and retained the complete output.
No timing from a failed or earlier run is combined with that result.

## What It Printed

- 324 cases; all lower lanes match the prospective base; no nonadopted case metadata
  changed.
- 37 upper adoptions match preintegration; all new exact sides improve the base’s exact
  verified ceiling; all displayed decimals safely round upward.
- For n=110, 172, 182, 206, 210, 240, 268, 273 and 297 the old reported lane has no
  exact form. Its verified exact side is the comparison baseline, and the output labels
  that substitution. It does not manufacture an exact old reported bound.
- 217 result IDs; all 18 #671 additions T-200–T-217 unchanged; all result scope,
  assurance, significance, attribution, reviews and evidence fields preserved.
  The four edited existing objects change adoption chronology only.
- A 38-case archive union, preserving both parents’ entries exactly.
- All 37 house and regularized witness blobs unchanged from preintegration; 324-entry
  manifest, regularized index and citation records inspected.
  The adopted citation entries differ only at n=108’s lower bound.
- 66 adopted houses; 11 regularized drawings, 25 settled as no better, n=103 regular as
  published; none of the 37 pending.
- The historical custody receipt is unchanged and misses current adoption n=29. This is
  an observation of an open gate, not a passing integrated custody check.

Initial diagnostic development exposed two reviewer assumptions, not source defects.
The first run stopped because some old reported lanes have `exact_form: null`; the
program now explicitly compares those cases with the old verified exact side.
A later run completed comparisons but could not save under the sandbox; escalation
allowed the save. The first saved run exited 1 because it incorrectly counted all IDs
added since the 194-record preintegration parent as #671 additions: there are 23 added
since that parent, T-195–T-217, including five already-main results.
The intended #671 roster is T-200–T-217, 18. All 23 had matched the base even in that
failed diagnostic.
The corrected final run uses the explicit 18-record roster and passes.
None of these earlier attempts is reported as a geometric replay or a successful gate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
