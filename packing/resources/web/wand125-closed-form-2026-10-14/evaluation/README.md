# An Exact Evaluation of a(N), 14 October 2026

[`closed_form_bounds.py`](closed_form_bounds.py) is this project’s own program.
It takes the theorem of wand125’s `problems/closed-form` as given and decides, in exact
rational arithmetic, what the theorem implies at each count from 49 to 324 and how that
compares with every bound the case records hold.
It decides nothing about the measure certificate (the families and region records): that
is the work of the source’s `replay4d` and structure check.
It was written and run on 14 October 2026 by an AI agent, a Claude model in the intake
lane `wand125-cf` of the 14 October intake (bead think-tsox), with the project
interpreter (Python 3.14.7, `python3 -I`).

## What It Read

- The retained
  [`intervals.json.gz`](../square-packing/problems/closed-form/intervals.json.gz),
  decompressed and refused unless its SHA-256 is the one the packet manifest records
  (`a91b0b49…1c0c`). It reads each interval’s endpoints, whether it is open on the left,
  and the exact $\alpha_i$ and $\beta_i$ of its certified line, and nothing else.
- The front matter of `packing/frontier/n-049.md` to `n-324.md`, through
  `devtools.check_source_coverage.parse_case`: each case’s reported and verified lower
  and upper bounds, with the holders’ kinds, source keys and evidence.
- For two cross-checks only: the site table
  `site/public/data/papers/closed-form-table.csv` from a checkout at the pin, refused
  unless its SHA-256 is the manifest’s pinned-only digest, and the output of the
  source’s `a_of_n.py 49-3600 --json --digits 30` as run here
  ([`outputs/a_of_n-49-3600.json.gz`](outputs/a_of_n-49-3600.json.gz)).

Its authors had read the source’s README, SPEC.md and `a_of_n.py` before writing it, so
it is not clean-room.
It imports no code of the source.
The source and this program were both written with AI assistance from the same system
family: the source’s commit names Claude Opus 5.5 as co-author.

## What It Does

For a non-square $N \ge 49$ with $k = \lfloor\sqrt N\rfloor$ the theorem states
$s(N) \ge a(N) = k + \sup\{\delta \in (0, 1] : (k+\delta)^2 - 4S^*(\delta) < N\}$, where
$S^*(\delta)$ is the largest certified saving $\alpha_i\delta + \beta_i$ over the
intervals that contain $\delta$. The program computes $a(N)$ by two routes that share
only the parsed intervals:

- **Route A, the closed form.** For each interval it forms the root
  $2\alpha_i + \sqrt{4\alpha_i^2 + N + 4\beta_i - 4\alpha_i k}$, keeps it only where it
  exceeds $k + d_0^{(i)}$, caps it at $k + d_1^{(i)}$, and takes the largest.
  Every comparison is an exact sign determination in
  $\mathbb{Q}(\sqrt{R_1}, \sqrt{R_2})$.
- **Route B, the theorem’s inequality.** It never forms a root.
  For a number $b$, $a(N) > b$ exactly when some interval holds a $\delta > b - k$ with
  $T_i(\delta) = (k+\delta)^2 - 4(\alpha_i\delta + \beta_i) < N$. Because every $T_i$
  increases in $\delta$ for $k \ge 7$ (it checks $14 - 4\alpha_i > 0$ exactly), that is
  $T_i(\max(b - k, d_0^{(i)})) < N$ with $\max(b - k, d_0^{(i)}) < d_1^{(i)}$. An
  irrational $b$ is enclosed in rational intervals refined until the decision is forced,
  up to $2^{-24576}$.

At every count Route B confirms Route A’s value to 30 decimal places, and both routes
decide each comparison with the four case bounds; the program stops on any disagreement
or on any comparison the enclosures cannot force.
A case bound is read from its `exact_form`, parsed through a whitelisted syntax tree
(integers, `+ - * /`, `sqrt`, `floor`, with implicit multiplication before `sqrt` or
`(`). Where the reported lane is Nagamochi’s with no exact form it is read as
$\min(\lceil\sqrt n\rceil, 1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1})$. Otherwise it is
read from its decimal `value`. Each printed `value` is checked against the bound it
prints.

It also checks the facts about the intervals that the source’s corollaries use: that the
34 intervals cover $(0, 1]$ as SPEC.md §7.2 requires; that $I_1$’s line is
$\alpha_1\delta$ with $\alpha_1 > 1/2$; the least margin of a certified line over
$\delta/2$ at an endpoint with $\delta \ge 1/50$; and that $S^*(1) > 3/4$. Then, count
by count from 49 to 3600, it checks the source’s comparisons with Nagamochi’s and
Karakuş’s formulas and its values at the top of each block.
These statements are proved in the source for every $N$, so this count-by-count check is
only a diagnostic.

Four controls must be refused, and were.
A changed `intervals.json` is refused by its digest.
Route B refuses $a(N) + 10^{-25}$ as the value at four counts.
At $N = 118$ the program finds $a = 11$ equal to 11 and below $11 + 10^{-40}$. Lowering
every $\beta_i$ by $10^{-6}$ lowers $a(230)$.

## How to Run It

From `packing/`, with the pinned checkout of the source at `CHECKOUT`:

```sh
P=resources/web/wand125-closed-form-2026-10-14
uv run --frozen --all-extras --group dev python -I $P/evaluation/closed_form_bounds.py \
  --author-table CHECKOUT/site/public/data/papers/closed-form-table.csv \
  --author-a-of-n $P/evaluation/outputs/a_of_n-49-3600.json.gz \
  --exact $P/evaluation/outputs/exact-forms.json \
  --table $P/evaluation/outputs/counts.tsv \
  --out $P/evaluation/outputs/bounds.json
```

The two `--author-*` options are optional.
The `a_of_n` output was made from the packet’s retained `a_of_n.py`, in a scratch copy
of `problems/closed-form/` whose 27 files matched the manifest, with
`python3 -I a_of_n.py 49-3600 --json --digits 30` (5.5 s).

## What It Printed

The run at 2026-10-14T09:43:37Z took 19.5 s of wall time and 17.9 CPU-seconds on one
worker.
The four cores were shared with other agents, at a load average of 5.2. It exited
0\. Its output is [`outputs/bounds.out`](outputs/bounds.out).
The receipt [`outputs/bounds.json`](outputs/bounds.json) records the program’s SHA-256
(`1a430c09…e251`), the interval facts, the summary, the claims check, the controls, both
cross-checks and one row per count.
[`outputs/counts.tsv`](outputs/counts.tsv) is the same table as tab-separated lines,
with $a(n)$ rounded down at 15 places.
[`outputs/exact-forms.json`](outputs/exact-forms.json) gives each count’s exact $a(n)$:
either the rational $k + d_1^{(i)}$, or `2α + sqrt(R)` with $R$ a rational of up to
about a thousand characters.

| Lane at n = 49…324 (264 non-square counts) | a(n) above | Equal | Below |
| --- | --- | --- | --- |
| Reported lower bound | 156: 104–116, 125–139, 148–164, 173–191, 201–220, 230–251, 261–284, 294–319 | 33 | 75 |
| Verified lower bound | 189: 104–117, 122–140, 145–165, 170–192, 197–221, 226–252, 257–285, 290–320 | 33 | 42: 50–60, 65–77, 82–96, 101–103 |
| Verified and reported upper bound | none | 33 | 231 |

The 33 counts where the bound equals a case’s bound are $m^2 - 1$, $m^2 - 2$ and
$m^2 - 3$ for $m = 8, \dots, 18$, where $a(n) = m$. All are already proved here.
No $a(n)$ is above any upper bound.
Every printed `value` agrees with the bound it prints.

- **Interval facts.** The intervals cover $(0, 1]$. The largest $\alpha_i$ is
  1.7495351…, so every $T_i$ increases for $k \ge 7$. $\alpha_1 - 1/2 = 1.2294000…$ with
  $\beta_1 = 0$. The least endpoint margin over $\delta/2$ for $\delta \ge 1/50$ is
  0.0226439…, at $\delta = 1/50$ on $I_2$. $S^*(1) = 0.8528498…$, which is above 3/4 and
  not above 1.
- **Claims check, 49 to 3600 (3,498 non-square counts).** The bound is not above
  Nagamochi’s capped formula exactly at $m^2 - 1$ and $m^2 - 2$, and not above Karakuş’s
  exactly at $m^2 - 1$, $m = 8, \dots, 60$, as the source states.
  It equals $m$ at $m^2 - 1$, $m^2 - 2$ and $m^2 - 3$ and nowhere at $m^2 - 4$.
- **Cross-checks.** The source’s `a_of_n.py` printed the same 30-place value and
  interval at all 3,498 counts.
  The site table’s `a_N`, which is rounded down at nine places, and its interval agree
  at all 3,498 counts.

## What It Decides

Its results are registered nowhere yet.
The [register plan](../register-plan.md) proposes it as `V-closed-form-evaluation` in
`verifiers.yaml`, with role `premises`: it decides what the theorem implies at each
count and leaves the theorem to the replay and the review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
