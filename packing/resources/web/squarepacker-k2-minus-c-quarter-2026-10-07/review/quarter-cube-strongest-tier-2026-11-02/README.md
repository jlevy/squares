# Strongest-Tier Review of the Quarter-Power and Cube-Root Preprints: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Sungjoon Ryu’s
quarter-power and cube-root deficiency preprints of
[#414](https://github.com/jlevy/squares/issues/414), and of the lemmas of his k2-minus-c
v1.2 that they import
([the review](../../../../../../docs/project/reviews/review-2026-11-02-ryu-quarter-cube-strongest-tier.md)).
They cover both preprints and are kept in this packet, the quarter-power one, because
the cube-root preprint rests on it.

They were written on 2 November 2026 by lane L23 of the intake pass think-3guf (bead
think-yf8j). The lane is an AI reviewer of the Claude family (Anthropic) at the strong
sub-agent tier (`tbd-strong-max`) and maximum reasoning, working in a worktree of its
own at `main` `bdf52188a`. The programs import only the Python standard library.
Their authors read the three TeX sources as data and never read or ran the source’s
programs:

- `k14_constants_check.py` and the numerical tests here;
- `check_table_iv.py`, `check_table_exact.py` and `check_table_exact2.py` in the
  cube-root packet;
- the v1.2 programs.

They did not read this repository’s `cases/asymptotic/quarter_cube_constants.py` or
`cases/asymptotic/ryu_k2_minus_c_constants.py` before the programs below had run.

All programs ran with CPython 3.14.7 (`packing/.venv/bin/python3 -I`), under `nice`, one
at a time, on a shared four-core host.

## What Each Program Does

| Program | Role | What it read | Receipt |
| --- | --- | --- | --- |
| `iv.py` | the interval arithmetic: exact rationals rounded outward to the grid 2^-480, with series remainders bounded explicitly for cos, sin, tan, atan, log, π and k-th roots; `python -I iv.py` runs its self-test | nothing | printed (8 of 8) |
| `qmodel.py` | Q’s quantities as functions of the parameters: Definitions 3.1, 3.2, 3.6, the bound Ψ of (10.3), conditions (i)–(iii) of Proposition 11.2, c_∞ of (11.4) | Q’s text | used by the next two |
| `checks.py` | records each displayed value in the direction the proof needs and, separately, in its displayed rounding direction (Q, Section 12.1) | Q’s text | used by the programs below |
| `q_constants.py` | **decides** every constant and threshold of Q that a theorem uses: Sections 1–11, Table 2 and Table 3, both columns | Q’s text | `outputs/q-constants.json`: 193 of 193 proved, 57 of 57 displays tight |
| `q_supplementary.py` | **decides** Q’s supplementary tables, never executed before: Table 4 (further thresholds), Table 5 (bounds at given k) and every claim of the sensitivity record of Section 12.6, with bisection brackets decided at both ends | Q’s text | `outputs/q-supplementary.json`: 118 of 118 proved, 41 of 41 displays tight |
| `c_constants.py` | **decides** the cube-root preprint’s constants B1, L1, Lemma 2.1, all eight cases of Table 1 (conditions (i)–(iv) of Proposition 5.1), the liminf constants and the comparisons of Section 1; exhibits explicit parameters and a finite k_a for each liminf constant | C’s text | `outputs/c-constants.json`: 95 of 95 proved, 24 of 24 displays tight |
| `r_lemmas_check.py` | **decides** the finite angle check that ends the proof of [R, Lemma 4.9] (the base of Theorem A13 and of C’s Theorem 1.2) and the numbers in the proofs of [R, Lemmas 4.8–4.10, Proposition 4.5] | [R]’s text | `outputs/r-lemmas.json`: 48 of 48 proved |
| `q_quotes.py` | **decides** that Q’s quotations of [R] are [R]’s text: 19 quoted statements and 12 quoted sentences, after normalizing cross-references | both TeX files | `outputs/q-quotes.json`: 19 of 19 and 12 of 12, one emphasis dropped |
| `c_citations.py` | numbers Q’s results as amsart does and resolves each of C’s 44 citations of Q to its environment, label and title; decides only that each cited kind is the kind at that number | both TeX files | `outputs/c-citations.json`: 44 of 44 |

Every receipt but `q-quotes.json` and `c-citations.json` records the SHA-256 of every
program in `programs/` when it ran; those two record their own and their inputs’.

No evidence entry cites these programs: the two preprints’ results are recorded in
`frontier/asymptotic-waste-bounds.yaml`, which has no evidence entries, and settle no
count the result register holds.
The deciding programs are registered in `frontier/verifiers.yaml` with their
independence records.

## How to Run Them

From the packet’s `review/quarter-cube-strongest-tier-2026-11-02/` directory, with `PY`
the project interpreter run as `python -I`:

```bash
PY="../../../../../.venv/bin/python3 -I"
$PY programs/iv.py
$PY programs/q_constants.py outputs/q-constants.json
$PY programs/q_supplementary.py outputs/q-supplementary.json
$PY programs/c_constants.py outputs/c-constants.json
$PY programs/r_lemmas_check.py outputs/r-lemmas.json
$PY programs/q_quotes.py ../../source/paper/paper.tex \
  ../../../squarepacker-k2-minus-c-v12-2026-10-06/source/paper/paper.tex outputs/q-quotes.json
$PY programs/c_citations.py ../../source/paper/paper.tex \
  ../../../squarepacker-k2-minus-c-cube-root-2026-10-07/source/paper/paper.tex outputs/c-citations.json
```

The constants programs take under a second each, and `q_supplementary.py` takes 18
seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
