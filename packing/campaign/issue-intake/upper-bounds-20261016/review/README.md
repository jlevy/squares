# Exact Sides for the 16 October Ledger

The ledger in this directory compares issue #639’s exact algebraic sides with the record
by prints cut at 120 places, and four of its comparisons are exact ties that no print
can decide. [`exact_sides.py`](exact_sides.py) computes both from the source’s own data
files and writes [`../exact-sides.json`](../exact-sides.json), which `sources.yaml`
transcribes: each claim’s `printed` and, at 51, 70, 153 and 207, its `record_relations`.

Run it from `packing/` with the project interpreter, `.venv/bin/python3`:

```sh
.venv/bin/python3 campaign/issue-intake/upper-bounds-20261016/review/exact_sides.py --pinned DIR [--check]
```

## What It Reads and Prints

| Input | Where |
| --- | --- |
| The 19 exact forms the packet retains | `packing/resources/web/evand-exact-cur-2026-10-16/source/search/exact/cur/data/` |
| The four it pins by digest only (204, 263, 267, 297) | `DIR`, a copy fetched from evand/square-packing at `7d1407a`; each is refused unless its SHA-256 is the packet manifest’s |
| PR #574’s algebraic witnesses at 70, 153 and 207 | `packing/resources/web/pingyou-pr574-certificates-2026-10-13/facts/alg-n-NNN.yaml.gz` |

For each count it checks that the file states its own $n$ with $n$ squares, counts the
roots of $p$ in the source’s interval by Sturm’s theorem (one at every count), narrows
that interval below $10^{-130}$ by exact bisection, and prints the root cut at 120
places. At 51, 126 and 295 it checks that the source’s closed form is that root.
The ties:

- **51:** the case record’s lanes hold $(16 + 5\sqrt2)/3$, which is a root of $p$ inside
  the interval where $p$ has one root, so the two sides are equal.
- **70, 153, 207:** T-174’s side is $c(b)$, $b$ the one root of $m$ in the witness’s
  isolating interval. $\mathrm{Res}_b(m(b), x - c(b))$ is $p$ times a rational at each,
  and an interval enclosure of $c(b)$ lies inside the interval where $p$ has one root,
  so the two sides are equal.

Each run took under a minute.
`--check` recomputes the file and compares it byte for byte.
Nothing here uses floating point, and it decides nothing about the packings: whether
each configuration fits is the source checker’s question, which the replay of think-g59l
asks.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
