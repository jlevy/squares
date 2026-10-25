# The Stage 4 Review of Theorem A (#797): Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Kevin Fang’s
Theorem A, $c^*(k) < 4\sqrt{2k} + 1$ for every $k \ge 6$, from issue #797
([the review](../../../../../../docs/project/reviews/review-2026-10-25-fang-theorem-a.md)).
The result has no `T-NNN`; PR #801 records it as a reported row of
`deficiency_upper_bounds`. They were written on 25 October 2026 by the review lane
`c-review-797-math` (bead `think-qmqq`): Claude, strongest tier (`tbd-strong-max`),
maximum reasoning.

**What they read.** The programs were written from the note v0.2,
`../../source/theorem-a/note/main.tex` (SHA-256
`f6f26d7b75eb30509e2117344d5e4d3e4cccdb2772bc48f1329ee719f3e01152`).
`fang_a_comparisons.py` also takes the statements of the other bounds from the register
rows PR #801 holds and from Ryu’s preprint v1.1.

- **Nothing of the source’s code.** No program reads or runs `lband.py`,
  `windowed_check.py`, `regenerate.sh` or the certificates, and their authors never
  opened them.
- **Nothing of this repository.** No program imports from it, except that
  `fang_a_squeeze_conditions.py` imports `fang_a_review.py` from this directory.

**Before writing**, their authors had read the packet README and the register row, which
summarise what the maintained `cases/asymptotic/fang_theorem_a.py` decided (its ranges,
its 60,167 pairs, the least slack and its 75 mutants).
They had not read the module itself, the stage 1 triage’s notes or any earlier review.

**The order of events, 25 October 2026 (UTC).**

| Time | Event |
| --- | --- |
| 02:20:32 | `fang_a_identities.py`, `fang_a_review.py` and `fang_a_comparisons.py` frozen, digests recorded |
| 02:20:38–02:22:52 | Every receipt but two rerun from those bytes |
| 02:23:06 | The review’s findings written (SHA-256 of that text `d0c35b5e4b7a9e2a470c0dbf343024b5d6eaf32c48dce73c098790add88f3146`) |
| After 02:23:06 | `fang_theorem_a.py` and its receipts read, then the triage’s notes and the model review |
| 02:25:24 | `fang_a_comparisons.py` revised to report the first $k$ where Daniel’s $k^{2/5}$ bound is smaller and its margin at $10^6$ (digest `ea73666051b2163de9a3f6127bb9ff69d715e5548cb1222363ec31ed182ccdaf` before, `0e3a7d56…6031` after); `outputs/comparisons.json` rerun at 02:27:08 |
| 02:33:46 | `fang_a_squeeze_conditions.py` written; run at 02:33:49 |
| 02:36:57 | `fang_a_case_bounds.py` written, for the caveat in `record-changes.md`; run at 02:37:00 |

`fang_a_identities.py` and `fang_a_review.py` are unchanged since they decided.
`outputs/program-digests.sha256` holds every program’s current SHA-256, which each
receipt also carries.

**How they ran.** CPython 3.14.7 (`packing/.venv/bin/python3`, run with `-I`), sympy
1.14.0 and mpmath 1.3.0, under `nice -n 19`, at most two processes at a time, on the
shared four-core host.
The final receipts took about 3.8 CPU-minutes.
Every run of the review, development runs included, took about 11 CPU-minutes (0.18
CPU-hours).

## What Each Program Does

| Program | Role | Receipts |
| --- | --- | --- |
| `fang_a_identities.py` | **decides** every identity and polynomial inequality the proof uses, for all $b$, $k$, $t$, symbolically (sympy), and refuses four mutated identities | `outputs/identities.json` |
| `fang_a_review.py` | **decides** the construction exactly at each $k$ of a range, the lemmas at sampled lifts and lengths, every square of chosen packings, the tie values $k = 2m^2$ and the sharpness remark; also the squeeze example and a self-test | the rest of `outputs/`, below |
| `fang_a_comparisons.py` | **decides** the comparisons of Section 7 and the abstract, and the register’s counts, in integers with tail lemmas | `outputs/comparisons.json` |
| `fang_a_squeeze_conditions.py` | decides nothing about the theorem: records which closeness conditions fail in finding M-1’s example | `outputs/squeeze-conditions.json` |
| `fang_a_case_bounds.py` | decides nothing about the theorem: reads the case records `packing/frontier/n-NNN.md` at the 15 counts the geometry run reaches and decides, exactly, that both upper bounds lie below each $k$ | `outputs/case-bounds.json` |

`fang_a_review.py`’s subcommands:

| Subcommand | What it decides | Receipt | What it printed |
| --- | --- | --- | --- |
| `selftest` | known answers: the odd widths, the bound at an exact tie, $w = 44$ at $k = 59$; that Lemma 2’s odd-$b$ bound fails for $b = 10$; the limit count against a tiny $t - 1/b$ | `selftest.json` | 13 of 13 pass |
| `construction --kmin 6 --kmax 60000 --limit-kmax 20000` | at a close rational $t$ for every $(k, b)$: (a)–(d), $S < k$, $k - b > h$, identity (1), Lemma 2 at all four ends, Lemma 3 for both bands, $w < H(t)$, $w$, $H(t)$ and $B(k)$ below $4\sqrt{2k} + 2$; to $k = 20{,}000$ also the one-sided limit count as $t \to 1/b^+$, exactly | `construction.json` | 60,167 pairs, no failure; least $B(k) - w = 8019401/78023840599$ at $k = 19{,}705$; the far-end rounding loss above $3/2$ at 516 band ends, most 1.5664 |
| `construction --kmin 60001 --kmax 250000 --limit-kmax 0` | the same, without the limit | `construction-extension.json` | 190,180 pairs, no failure; far-end loss above $3/2$ at 542 band ends |
| `lemmas` | Lemmas 2 and 3 and (E2) at sampled close $t$ spread over each close interval, sampled lifts and lengths with every tie; the chain $w(t) < H(t)$ for $6 \le k \le 400$ and five larger $k$ | `lemmas.json` | 291,401 and 133,989 cases and 5,807 chain cases hold; one close interval per width, of width about $b^{-3}$ |
| `geometry` | every square at $k = 6$–40, 50, 59, 72, 98 and 101, both widths at ties: inside $[0, S]^2$, unit, pairwise disjoint interiors by exact separating axes, count $= N(t)$; seven mutants at $k = 6, 8, 18, 40, 101$ | `geometry.json` | 46 packings valid; 49 of 49 mutants refused |
| `sharpness --bmax 2001 --scan-bmax 61` | the remark at $k = (b^2 - b + 8)/2$: the limit waste for odd $5 \le b \le 2001$, and the waste at sampled close $t$ for $b \le 61$ | `sharpness.json` | waste $4b$ everywhere |
| `ties --mmax 1000` | $k = 2m^2$, both odd widths, at a chosen $t$ and in the limit | `ties.json` | 1,998 pairs hold; waste at most $8m$ |
| `squeeze` | $k = 43{,}218$ with $k - S$ and with $t - 1/b$ fixed, and a log scan of $k - S$ | `squeeze.json` | waste 1176 at $k - S = 10^{-7}$ (both widths); 1178 at $t - 1/b = 10^{-7}$, $b = 293$ |

`fang_a_comparisons.py` printed 22 of 22 checks holding, with these results:

- the counts 495,210, 255,215 and 249,568 against Daniel’s bound below $10^6$, the 17
  values below 89 and $|A - D| \le 2$ from 89;
- Daniel’s $k^{2/5}$ bound first smaller at 735,988, and smaller at every $k$ from
  736,595;
- the thresholds against Ryu’s Theorems 1.2, 1.3, 1.4 and 1.6 and against T-163;
- 346,919 and 346,920 for the register’s window, with a longest run of 589.

## How to Run Them

From any directory:

```bash
PY=/home/user/squares/packing/.venv/bin/python3
D=packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25
$PY -I $D/programs/fang_a_identities.py --out identities.json
$PY -I $D/programs/fang_a_review.py selftest --out selftest.json
$PY -I $D/programs/fang_a_review.py construction --kmin 6 --kmax 60000 --limit-kmax 20000 --out construction.json
$PY -I $D/programs/fang_a_review.py construction --kmin 60001 --kmax 250000 --limit-kmax 0 --out construction-extension.json
$PY -I $D/programs/fang_a_review.py lemmas --out lemmas.json
$PY -I $D/programs/fang_a_review.py geometry --out geometry.json
$PY -I $D/programs/fang_a_review.py sharpness --bmax 2001 --scan-bmax 61 --out sharpness.json
$PY -I $D/programs/fang_a_review.py ties --mmax 1000 --limit-mmax 1000 --out ties.json
$PY -I $D/programs/fang_a_review.py squeeze --out squeeze.json
$PY -I $D/programs/fang_a_comparisons.py --out comparisons.json
$PY -I $D/programs/fang_a_squeeze_conditions.py --out squeeze-conditions.json
$PY -I $D/programs/fang_a_case_bounds.py --frontier packing/frontier --out case-bounds.json
```

Each exits 0 when everything it decides holds.
Each receipt records the SHA-256 of the program that wrote it, and each `.log` file next
to a receipt holds that run’s printed output.

## Registration

Nothing here is cited by an evidence entry yet.
[`record-changes.md`](record-changes.md) drafts the `verifiers.yaml` records of the
three deciding programs, with their structured `independence`. It also drafts the
register row’s new text and a count-scoped evidence entry, with the reason that entry
needs the records lane’s decision.
`fang_a_squeeze_conditions.py` and `fang_a_case_bounds.py` decide nothing about the
theorem and are cited by no evidence entry.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
