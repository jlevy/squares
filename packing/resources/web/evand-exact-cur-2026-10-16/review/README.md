# The Replay of Evan Daniel’s Checker on #639’s Exact Forms

[`replay_verify_exact.py`](replay_verify_exact.py) is the stage 4 replay of issue #639
(bead think-g59l). It was written here and runs the source’s own checker; it decides
nothing about a packing itself.

## What It Runs and Reads

- **The checker:** `verify_exact.py`, run unchanged from the retained copy in
  [evand-exact-and-local-reports-2026-10-12](../../evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py)
  (SHA-256 `a0f38ca8…bab4`), byte-identical to `search/exact/verify_exact.py` at
  `7d1407a`. It was read in full before it was run. The driver refuses a copy with any
  other digest.
- **The inputs:** the 19 exact forms this packet retains, and the four it pins by digest
  only (204, 263, 267, 297), read from `--pinned DIR`, a copy fetched from the pinned
  commit outside the repository. Each of those four is refused unless its SHA-256 is the
  manifest’s.
- **The runs:** each in its own `python -I` child process, at most `--workers` at a time
  (2 here, under `nice -n 10`): the positive at every count, which must print `VALID.`
  with the statement the source’s `data/verify.txt` prints; and at each of the 19
  retained forms four controls, which must print `NOT VERIFIED`. The controls are a
  square moved $10^{-6}$ through the wall the file’s contact list says it touches, the
  side raised by $10^{-6}$ in the field, the side’s interval moved wholly below its root,
  and a duplicate square. `--controls-at all` would add the four pinned-only counts,
  whose controls cost nearly a positive each.
- **Irreducibility:** each polynomial is factored over the integers with SymPy’s
  `factor_list`, and its squarefreeness checked as $\gcd(p, p') = 1$. It counts as
  irreducible only when it is squarefree and its factorization is one factor, of
  multiplicity 1 and of $p$’s degree, so a perfect power $q^k$ is refused.
  The source asserts irreducibility and none of its programs checks it.

Each finished run is cached in the scratch directory, so an interrupted invocation
resumes where it stopped. A cached record is keyed by the run it records (the input’s
SHA-256, the checker’s SHA-256 and the control kind) and reused only when all three
match. The first replay, of 16 October, was interrupted once by its session’s
background-time limit and resumed under a cache keyed by count alone; PR #651’s review A
(A5, A6) led to both fixes. The refreshed receipt is from the fixed driver; its first
invocation was likewise stopped after four positives and resumed, this time from the
keyed cache.

## Running It

From `packing/`, with the project interpreter:

```sh
.venv/bin/python3 resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py \
    --pinned DIR --scratch SCRATCH --workers 2
```

It writes [`../receipts/replay-verify-exact.json`](../receipts/replay-verify-exact.json):
each run’s command, exit status, last line, wall and CPU seconds, each input’s digest,
and each polynomial’s factors (degree and multiplicity) and squarefreeness.
[`tests/test_evand_exact_cur.py`](../../../../tests/test_evand_exact_cur.py) holds the
outcome at n = 51 on every test run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
