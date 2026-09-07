# Eleven Squares: Contributed Research

Start with [the intake note](INTAKE.md) for provenance, evidence status and links to the
native exploration and agenda.
This is the research subset of the supplied bundle; the complete upload and its PDF
publishing assets remain in the local attic.
The contributor’s `updates/integrated_agenda.md` records proposed priorities.

The 40-page combined PDF contains the new 16-page enumeration addendum first, followed
by the original 24-page technical review.
Each part retains its own pagination and table of contents; PDF bookmarks identify both
parts. The combined editable text is `complete_review.md`.

## Included work

| Location | Contents |
| --- | --- |
| `complete_review.pdf` and `.md` | Both technical reports in one reading file |
| `updates/integrated_agenda.md` | Current synthesis of the research priorities and first discriminators |
| `updates/enumeration_addendum.pdf` and `.md` | Detailed review of the follow-up ideas, angle-case catalogues, quantitative transfer, mixed-size frames, parametric LPs, and stationary-value finiteness |
| `original_review/` | Original PDF and Markdown report, construction image, and certificate directory |
| `enumeration/` | New standard-library controls, a complete discrete angle-profile catalogue, results, and tests |
| `source_packet/` | All 19 files of the supplied frozen research packet; a supplemental original uploaded image is included when available |
| `evidence/` | Supplied same-code mathematical replay outputs |
| `run_checks.py` | One command to replay both sets of executable certificate/control checks |

## Executable checks

The mathematical checkers need only Python 3.10 or later and its standard library:

```sh
python run_checks.py
```

The new catalogue can be regenerated separately:

```sh
cd enumeration
python enumeration_checks.py --write .
python test_enumeration.py
```

The retained checks need no PDF publishing tools.

## Mathematical status

The original review’s seven-row certificate proves the exact value eleven for the
specified sixty-placement Trump-D4 a.e. weight-support problem.
Equality uses the supplied feasibility of the packing average.
It is not a global density certificate or a new lower bound for s(11). The original
report also supplies a normal-stationarity proof in its stated physical formulation.

The addendum’s 1,024 multiplicity profiles and 78 (then 65) bin profiles are **discrete
descriptors, not solved continuous packing cases**. Its angular transfer, case-cover
composition, robust-Farkas inequality, and finite stationary side-value statements are
proved deductions, not a completed global solver.

The original certificate and both control suites were replayed successfully.
Normal and optimized Python outputs agree.
These are same-code/same-author checks, not independent external peer review.
The historical 3.81 continuum sweep and the omitted full local-radius calculations were
not rerun here. No new global bound, proof of Trump optimality, or complete n=11
enumeration is claimed.

The user-provided source snapshot remains dated 6 September 2026 at revision
`4d305597a505ebfbe85f1851fa7148374661e622`. Historical instructions inside that packet
are preserved as sources, not executed as a task schedule.
The package is not a clone of sqpack, and does not contain omitted campaign databases,
unretained exploratory scripts, or the missing full modulus receipts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
