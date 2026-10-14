# wand125’s Closed-Form Lower Bound for Every Non-Square N ≥ 49

On 13 October 2026, wand125/square-packing added `problems/closed-form` and the release
`closed-form-v1`: a computer-assisted proof that $s(N) \ge a(N)$ for every non-square
$N \ge 49$, where $a(N)$ is given by one square root on each of 34 intervals of the
fractional part of the side.
No issue reports it; the 14 October watch survey found it (think-fxs7), and bead
think-tsox owns its import.
This packet retains the claim folder at the source’s head and records stages 1 and 2 of
the [import](../../../campaign/result-import.md), with the checks of stage 4 that cost
minutes. No standing bound or rating changes here.
The records lane applies the [register plan](register-plan.md).

| Item | Value |
| --- | --- |
| Source | [`problems/closed-form`](https://github.com/wand125/square-packing/tree/9a28a84bd55dc124bfa2919bb6c4fb504dda3149/problems/closed-form) |
| Pinned revision | `9a28a84bd55dc124bfa2919bb6c4fb504dda3149`, the head of `main`, committed 2026-10-14T09:27:10Z, tree `742bc1fd…` |
| First committed | `eb0fd1938fcabf9b81b638f9d6b6db7f80b8985a`, 2026-10-13T09:36:19Z; the folder is unchanged since |
| Release | `closed-form-v1`, published 2026-10-13T09:36:02Z: 34 interval archives and `SHA256SUMS`, 815,734,366 bytes, pinned by the retained `ASSET.json` and not retained |
| Retrieved | 2026-10-14T09:29:10Z |
| Certificate | 68 families of line segments and 136 region records, 187,183,108 leaves |
| Source’s checker | `replay4d` (Rust, crates `seam4d_core` and `replay4d`), 4,294 CPU-hours for one complete replay |

## The Claim

Write the container side as $a = k + \delta$ with $k = \lfloor\sqrt N\rfloor \ge 7$ and
$0 < \delta \le 1$. On each interval $I_i$ of $\delta$ the certificate proves a saving
$S_i(\delta) = \alpha_i\delta + \beta_i$ with exact rationals.
Let $S^*(\delta)$ be the largest over the intervals that contain $\delta$. The theorem
(README.md, SPEC.md §1.1) is this:

> Let $N \ge 49$ be a non-square integer and $k = \lfloor\sqrt N\rfloor$. If
> $(k + \delta)^2 - 4S^*(\delta) < N$, then $s(N) \ge k + \delta$. Consequently
> $s(N) \ge a(N) = k + \sup\{\delta \in (0, 1] : (k + \delta)^2 - 4S^*(\delta) < N\}$.

In closed form, $a(N)$ is the largest of
$\min(2\alpha_i + \sqrt{4\alpha_i^2 + N + 4\beta_i - 4\alpha_i k},\ k + d_1^{(i)})$ over
the intervals whose root exceeds $k + d_0^{(i)}$. The proof is a measure on $[0, a]^2$:
Lebesgue measure in the middle, and, for each interval, a family of axis-parallel
segments along the walls (period 1, mass $9/5$ per period) and in the corners.
It is C4-symmetric, of total mass $a^2 - 4S(\delta)$ for every $k \ge 7$, and has mass
at least 1 on every closed unit square.
A measure like that, of total mass below $N$, gives $s(N) \ge a$. The last property is
checked for every square whose centre lies in four local regions, which cover every case
after the rotation and the periodic shifts, by exact leaf tests over a grid of centres,
angles and $\delta$.

The source states four consequences:

- $a(N) = F(N) = k + 1$ at $N = (k+1)^2 - 1$ and $(k+1)^2 - 2$, and $a(N) > F(N)$ at
  every other non-square $N \ge 49$. Here $F$ is Nagamochi’s $1 + \sqrt{N - 2k + 1}$,
  capped at $k + 1$; the proof does not use his Lemma 1.
- $a(N)$ exceeds Karakuş’s $1/2 + \sqrt{N - k + 1/4}$ except at $(k+1)^2 - 1$.
- Because $S^*(1) > 3/4$, $s(n^2 - 1) = s(n^2 - 2) = s(n^2 - 3) = n$ for $n \ge 8$. The
  source says these values are not new.
- The site write-up adds a count over $N \le 3600$ against the author’s own choice of
  known bounds, beyond this record’s cases.

## Against the Record

[`evaluation/`](evaluation/README.md) computes $a(n)$ exactly at every count from 49 to
324 and compares it with the case records at `origin/main` `f73e9de13`.

| Lane at the 264 non-square counts | a(n) above | Equal | Below |
| --- | --- | --- | --- |
| Reported lower bound | 156: 104–116, 125–139, 148–164, 173–191, 201–220, 230–251, 261–284, 294–319 | 33 | 75 |
| Verified lower bound | 189: the 156, the 25 first counts of the blocks from 122, and the eight $m^2 - 4$ from 117 | 33 | 42: 50–60, 65–77, 82–96, 101–103 |
| Either upper bound | none | 33 | 231 |

The 33 equal counts are $m^2 - 1$, $m^2 - 2$ and $m^2 - 3$ for $m = 8, \dots, 18$, all
`proved` already: by Karakuş (T-084), chelokot’s Lean proof (T-086) and Evan Daniel’s
Valid7 (T-064). So the bound settles no open case and is above no upper bound.
In the reported lane, wand125’s own measure certificates and covers are stronger below
104, Daniel’s $s(m^2 - 4) = m$ (T-081) at each $m^2 - 4$, and Green’s DS7 values at the
first counts of each block from 122. At $n = 125$, T-144’s pending $11.26$ is above
$a(125) = 11.2545798369\ldots$; the
[register plan](register-plan.md#who-holds-each-value-now) names every holder.

## What Was Checked Here

All runs used the project interpreter, Python 3.14.7, on four cores that other agents
shared.

- **Custody** ([receipts/release-custody.json](receipts/release-custody.json)). The
  release API’s size and SHA-256 digest of all 35 assets equal `ASSET.json`. The 34
  archives were downloaded into scratch in 43 seconds, and `sha256sum -c SHA256SUMS`
  passed for all 34. They stay with the author.
- **The source’s structure check**
  ([receipts/structure-check/](receipts/structure-check/run.json)). The packet’s
  `problems/closed-form/` was copied to scratch and decompressed, and its 27 files were
  matched to the manifest.
  `structure/structure_all.py` then ran unchanged on the 34 archives and printed
  `ALL STRUCTURE OK`: all 680 checks of `validate_family.py` passed on the 68 families,
  in 68 seconds of wall time and 44 CPU-seconds.
  Its results equal the source’s `receipts/structure.json` exactly.
  That receipt names `validate_family.py` by SHA-256 `fdd61866…`, which is not the
  published file’s `22e55f17…`; this run is the first receipt of the published script.
  On interval 34, raising $\beta_{34}$ by $10^{-6}$ and adding $10^{-6}$ to one
  bottom-wall row were both refused.
- **An exact evaluation of $a(N)$** ([evaluation/](evaluation/README.md)). This
  project’s own program computes $a(n)$ by two routes, the closed form and the theorem’s
  inequality, and compares it exactly with every case bound.
  It also checks the facts the corollaries use and four controls.
  The source’s `a_of_n.py`, run here, printed the same 30-place value and interval at
  all 3,498 counts to 3600, and so does the site table, at nine places.

The structure check is a premise check: it decides SPEC.md §7.1 steps 1 and 2 and part
of step 5, and leaves the leaf tests to `replay4d`. The evaluation decides what the
theorem implies at each count, and nothing about the certificate.

## What Was Not Run

No record was replayed and `replay4d` was not built.
The source prices one complete replay at 4,294 CPU-hours (`receipts/replay.json`, 269
runs on two machines).
Even its smallest record takes 0.27 CPU-hours.
The build needs network access to crates.io for the locked crates and compiles GMP from
source. The archives unpack to about 18 GB. That is far above an intake’s budget, and no
owner budget is set, so the replay waits in think-tsox.
The [register plan](register-plan.md#validation-priced) prices each remaining step.

The source states its own limits.
`replay4d` shares its core with the search tools that made the records, so its replay is
the producer’s code re-run; no independent checker exists.
The full replay ran a build whose source hash differs from the published crates’, by
comments only, as the source says; the published build replayed intervals 1 and 34
again. `replay4d` drops family rows of weight $\le 0$ instead of rejecting them, which
the structure check covers.

## For the Mathematical Review

A review of the proof runs in its own lane after this one.
These are the files and lines that carry the proof, all under
`square-packing/problems/closed-form/`:

| File | Lines | What it carries |
| --- | --- | --- |
| `SPEC.md` | 7–43 | The theorem, the closed form, its maximum over intervals, the comparisons with Nagamochi and Karakuş, the $k^2 - j$ corollaries |
| `SPEC.md` | 44–63 | The measure principle by scaling (§1.2), and the total mass $a^2 - 4S(\delta)$, with the terminal line $m_v$ (§1.3) |
| `SPEC.md` | 64–117 | The global C4 arrangement, the reduction to $k \ge 7$, and the coverage of the container by four local regions (§2.1–2.3), where $k \ge 7$ is used |
| `SPEC.md` | 118–183 | Family format, saving extraction, the right-side family by inclusion of $U$, the X and Y variants (§3) |
| `SPEC.md` | 184–224 | Poses by $u = \tan(\theta/2)$, the 90-degree coverage, the four regions and the root grids (§4) |
| `SPEC.md` | 225–463 | Every leaf test (§5.1–5.12), the polynomial nonnegativity test and the B4 edge argument |
| `SPEC.md` | 464–514 | Record format, tiling by midpoint bisection, the product grid, and $u = 0$ by upper semicontinuity (§6) |
| `SPEC.md` | 515–564 | Acceptance order, interval coverage and joins at $\delta = j/5$, $2/5$, $4/5$ and $99/100$, and the pitfalls (§7, §8) |
| `SPEC.md` | 607–636, 643–687 | What each published checker covers, and the acceptance checklist |
| `README.md` | 7–132 | The claim as stated, the outline, and what the source checked |
| `intervals.json.gz` | — | The 34 intervals, certified lines and region bounds that the theorem reads |
| `structure/validate_family.py` | 41–74, 205–273, 291–366 | Family input checks, wall and corner decomposition, savings, the line check, and the $k = 7, 8, 9$ builds and windows |
| `structure/structure_all.py` | 40–74 | Family digests, the line through the endpoint savings, the region bounds |
| `checker/replay4d/src/main.rs` | 24–63, 81–172 | Tiling, the product grid and $u$-range checks, and the replay driver |
| `checker/seam4d_core/src/replay.rs` | 7–41, 132–425 | The X and Y variants, the edge side conditions, and leaf dispatch |
| `checker/seam4d_core/src/lib.rs` | 89–459, 635–722 | Pose geometry, the core and outer polygons, segment mass, family loading, and `cover`, which drops weights $\le 0$ |
| `checker/seam4d_core/src/fast.rs` | 370–432 | The CORE bound |
| `checker/seam4d_core/src/b3d.rs` | 398–500, 717–1187, 1520–2025, 2047–2526 | The gcd shortcut modulo primes, Sturm sequences and real algebraic numbers, `nonneg_open`, B3D, B3U and B3T (`certify3`), CORE1, B4U and the guarded edge chains |
| `checker/seam4d_core/src/b3d_sort.rs` | 1–188 | The comparison sort of edge values, compiled into `b3d.rs` by `#[path]` |
| `checker/replay_all.py` | 31–82 | Archive and member digests, and the comparison of counts with `intervals.json` |

Three places deserve a direct look.
In `b3d.rs`, `plain_rf()` lets the environment variable `B3_PLAIN_RF` switch the
rational-function arithmetic path.
`gcd` returns 1 when a modular gcd has degree 0 at a prime that divides neither leading
coefficient; `modp_gcd_deg` returns `None` at a prime that divides one.
And `b3d_sort.rs` is compiled into `replay4d`, but the source hash that `replay4d`
prints leaves it out (`main.rs` 64–78, SPEC.md §9.4).

## Retained Here

`problems/closed-form/` is MIT-licensed, so `devtools.acquire_source` retains all 27 of
its files byte-identical under `square-packing/`, with the root `LICENSE.md`. It wrote
them from the declaration in
[acquisition/declaration.json](acquisition/declaration.json):
[acquisition/sources.json](acquisition/sources.json) is the record, and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest of all 32 files in scope.
The root `README.md` and `INDEX.json` fall under no licence the tree states, and neither
does the site write-up (`site/src/content/papers/closed-form/en.mdx`) or its table of
$a(N)$ for $N \le 3600$ (`site/public/data/papers/closed-form-table.csv`). All four are
pinned by digest only.

| Path | What it is |
| --- | --- |
| `square-packing/problems/closed-form/README.md`, `SPEC.md`, `INTERVALS.md` | The claim, its full specification, and the interval table |
| `square-packing/problems/closed-form/intervals.json.gz` | The certified lines, region bounds and record digests of the 34 intervals |
| `square-packing/problems/closed-form/a_of_n.py` | The source’s evaluator of $a(N)$ |
| `square-packing/problems/closed-form/structure/` | The family structure check, run here |
| `square-packing/problems/closed-form/checker/` | The Rust checker, its `Cargo.lock`, and `replay_all.py`, not built |
| `square-packing/problems/closed-form/receipts/` | The source’s replay, structure, family-cleanup and published-checker receipts |
| `square-packing/problems/closed-form/ASSET.json`, `LICENSE` | The release’s digests, and the MIT notice |
| `receipts/` | This packet’s custody and structure-check receipts |
| `evaluation/` | This project’s exact evaluation, its outputs, and the source’s `a_of_n.py` output |
| `register-plan.md` | The plan for stage 3 |

## Sources and Notices

`problems/closed-form/LICENSE` is MIT, Copyright (c) 2026 wand125, and covers the
folder. `checker/seam4d_core/src/b3d_sort.rs` is a port of CPython’s list sort and keeps
the Python Software Foundation licence beside it in `CPYTHON_SORT_LICENSE`. The root
`LICENSE.md` says the repository has no single licence and that each folder keeps its
own.

The folder README credits Hiroaki Hosono (wand125) and names no method it builds on.
It cites Nagamochi (2005), Karakuş (arXiv:2609.37410), jlevy/squares#295 for the public
discussion of Nagamochi’s gap, and Evan Daniel’s Valid7, and it says: “Our proof uses
neither Nagamochi’s lemma nor Karakuş’s bound.”
The repository README credits Evan Daniel, tokoharu and jlevy/squares for code and
formats that other folders use.
The folder’s prose says nothing about AI assistance.
The commit that adds it names Claude Opus 5.5 as co-author.

## Compressed Files

The two upstream data files of more than 1,000 lines and the source program output kept
as a receipt are stored as deterministic gzip made by `gzip -9n`. The table gives the
Git blob and SHA-256 of the decompressed bytes; the upstream rows’ digests are the ones
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
`python -m devtools.retained_data check PACKET` re-derives every row.
Before running a source program on this packet, restore the upstream tree in a scratch
copy, as the structure run did.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing/problems/closed-form/intervals.json.gz` | upstream | `cc99b15b4bb3c853baf371c7bb99b8a120daca73` | `a91b0b49988bc5bf8977d1e9f61e2930e2cb1be136bd4ff3140b5ee263591c0c` |
| `square-packing/problems/closed-form/receipts/replay.json.gz` | upstream | `b32ff5159f9ca229c1e63e0e7fb26f45e53dce36` | `f86654130c3b9eb3c2ea0152673fd36ef6d74d85096fd4daddc02d44ef721c93` |
| `evaluation/outputs/a_of_n-49-3600.json.gz` | receipt | `903a1f69eeb90837dcb787f80597297b9894acbd` | `df122cee140bf7edf70e1d01d2209e7a5c543edf75862493a790a95b0d3ab92c` |

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-closed-form-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.retained_data check resources/web/wand125-closed-form-2026-10-14
uv run --frozen --all-extras --group dev python -I resources/web/wand125-closed-form-2026-10-14/evaluation/closed_form_bounds.py
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
