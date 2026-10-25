# Kevin Fang’s Theorem A, Pinned 2026-10-24

Kevin Fang’s note *Packing k² − ⌈√(32k)⌉ − 1 unit squares in a square of side less than
k* proves that for every integer $k \ge 6$ the waste $w(k) = k^2 - \max\{N : s(N) < k\}$
is below $4\sqrt{2k} + 2$, so

$$c^*(k) < 4\sqrt{2k} + 1, \qquad c^*(k) \le \lceil\sqrt{32k}\,\rceil,$$

where $c^*(k) = \max\{c : s(k^2 - c) = k\} = w(k) - 1$. The packing is Sungjoon Ryu’s L,
a $(k - b)^2$ grid and two bands of $b$ rows tilted at $t = \tan(\theta/2)$ just above
$1/b$, with both ends of each band filled by axis-parallel rows (lift 0 at one end, the
whole free length at the other) and $b$ an odd integer with $|b - \sqrt{2k}| \le 1$.
Fang reported it on [jlevy/squares#797](https://github.com/jlevy/squares/issues/797)
on 24 October 2026, with the code, 36 certificates and the note in `theorem-a/` of
[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs).

Evan Daniel proved a bound of the same strength first, $c^*(k) \le
4\lceil\sqrt{2k - 7}\rceil - 1$ for every $k \ge 7$, in Lean on 18 October, with the same
idea of axis rows at the band ends of Ryu’s L
([evand-k2-minus-c-lean-2026-10-18](../evand-k2-minus-c-lean-2026-10-18/README.md)).
The note’s v0.2 credits him and calls Theorem A an independent second proof. Per $k$
neither integer bound is always the smaller, so the asymptotic register records Theorem A
as a reported row of `deficiency_upper_bounds` of its own, credited after Daniel’s row,
which the same change records. It settles no count $n \le 324$, so it has no `T-NNN`.

Its Frontier key is **[Fang Theorem A 2026-10-24]**. Bead `think-4tj5` holds the import
and the reply.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/TheSnakeFang/squarepack-certs> |
| Revision | `db1ed6220731fce432fa3b1ef3b994b5ab6c3663`, tree `9617832c6bb0480b69298dc94f2b494fa150a26c`, the head when read: “theorem-a: note v0.2 crediting Evan Daniel’s earlier bound (doi:10.5281/zenodo.23624565)” |
| Committed | 2026-10-24T19:12:51Z, pushed 19:12:52Z |
| Earlier pins of the same theorem | `b1b3f6bda13739c9eeecc1ceaefec9178294e0ca` (committed 18:47:49Z, pushed 18:48:24Z), the commit the issue and the note’s front matter name, which adds `theorem-a/`; and `31bdc2d1b9e247ccb16877c35302beda97cee24c` (18:59:07Z), the note v0.1 with its DOI. `lband.py`, `windowed_check.py`, `regenerate.sh`, `LARGE.sha256` and `certs/` have the same bytes at all three; only the note and the READMEs change |
| Zenodo | v0.1 [10.5281/zenodo.23624412](https://doi.org/10.5281/zenodo.23624412) (created 2026-10-24T18:58:43Z) and v0.2 [10.5281/zenodo.23624565](https://doi.org/10.5281/zenodo.23624565) (19:12:19Z), one concept DOI `10.5281/zenodo.23624411`, both CC BY 4.0 |
| Licence | MIT, copyright 2026 Kevin Fang (`LICENSE`), for the code; `ATTRIBUTION.md` releases `theorem-a/certs/` under CC0 1.0 and the note under CC BY 4.0; `tools/verify_cert_daniel.py` is Evan Daniel’s, MIT |
| Retrieved | 2026-10-24T20:26Z, a full clone by the stage 1 triage; the Zenodo records at 21:09Z on 24 October |
| Pinned subtree | 54 files, 4,767,904 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 48 files, 4,719,856 bytes, byte-identical under [`source/`](source/) |

## Credit and AI Assistance, as the Source States Them

The note’s acknowledgement (v0.2) reads: “The L-shaped packing, its end-region framework
and most of the bounds compared above are Sungjoon Ryu’s. The axis-layer filling of the
band ends and the bound $4\lceil\sqrt{2k-7}\,\rceil-1$ were found first by Evan Daniel,
whose certificate format and checker we also use. The Squares Project (Joshua Levy) keeps
the register in which these bounds are compared. The construction code, checkers and
certificates were written and run with Claude (Anthropic) as a coding and research agent,
directed and reviewed by the author. Two blind language-model reviews of the proof
(Claude Opus; OpenAI Codex, GPT-6 Astra) found errors that were corrected. That is not an
external mathematical review.” `ATTRIBUTION.md` says the same of `theorem-a/` and names
what Theorem A adds: “its end split, odd width and form $4\sqrt{2k} + 2$”. The record
credits it as **Fang after Ryu, Daniel**, after Daniel’s earlier row.

## What Is Retained

`devtools.acquire_source` wrote [`source/`](source/) from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin, and [acquisition/sources.json](acquisition/sources.json) is the
record.

- **Retained, 48 files:** `theorem-a/` whole: the README, `lband.py` (the construction in
  exact rationals), `windowed_check.py` (the source’s windowed driver for its two
  checkers), `regenerate.sh`, `LARGE.sha256`, the 36 certificates `certs/k006.cert` to
  `k040.cert` and `k101.cert` in Evan Daniel’s text format with their `SHA256SUMS`, and the
  note v0.2 as `note/main.pdf` and `note/main.tex`; and the root `README.md`,
  `ATTRIBUTION.md`, `CHANGELOG.md` and `VERIFICATION.md`, which state the credit, the
  licences and the source’s checks.
- **Pinned by digest, six files:** `LICENSE`, `verify.py`, `tools/verify_cert_daniel.py`,
  `tools/NOTICE-verify_cert_daniel` and `tools/rectcheck.py`, each byte-identical to a copy
  another packet retains (the acquisition record names it), and `MANIFEST.sha256`, the
  whole repository’s digest list, whose `theorem-a/` lines name the retained files.
- **The Zenodo records**, under [`zenodo/`](zenodo/), written by
  `devtools.capture_web_source zenodo RECORD --extract main.tex`: each record and its file
  listing as Zenodo served them, the archive’s member manifest, the receipt with each
  file’s stated and computed digests, and the extracted `main.tex`. v0.2’s PDF and TeX are
  byte-identical to `source/theorem-a/note/`. v0.1’s are those of `31bdc2d`, a revision
  this packet does not otherwise pin, so its PDF is kept as
  [`zenodo/zenodo-23624412/fang-2026-theorem-a.pdf`](zenodo/zenodo-23624412/fang-2026-theorem-a.pdf),
  97,397 bytes, MD5 `81c34bb50619d4fa98fa5d02f3b51e47` as the record states, SHA-256
  `a5311732b40f3e8c75685322f056cace97520c73ef32b2bc00dfec2eb494139f`.
- **Not shipped by the source:** the certificates at $k = 300$ and $600$ (89,902 and
  359,860 squares, 12 MB and 49 MB by the README). `LARGE.sha256` states their SHA-256,
  `162bcfeb…0732` and `d6cda47e…3e22`, which the record keeps as the author’s statement.
  They were not rebuilt here.

## What Was Checked Here

Three receipts under [`receipts/`](receipts/), each written by the maintained
`packing/cases/asymptotic/fang_theorem_a.py`, which was written from the note’s Sections 2
to 5 and never reads or runs `lband.py` or any other program of the source. Everything
in it is exact, in integers and fractions.

- **[`construction.json`](receipts/construction.json)**, `construction` (44 s on this
  host). For every $k$ from 6 to 60,000 and every odd $b$ with $|b - \sqrt{2k}| \le 1$,
  both where there are two, it finds a rational $t$ just above $1/b$ satisfying the note’s
  conditions (a) to (d) with $H(t) < 4\sqrt{2k} + 2$, and decides
  $w = k^2 - N < 4\sqrt{2k} + 2$, $w < H(t)$ (Lemma 3 with equation 1) and
  $B(k) < 4\sqrt{2k} + 2$: 60,167 pairs, no failure. The least $B(k) - w$ for
  $k \le 20{,}000$ is $8019401/78023840599$ at $k = 19{,}705$, as the note states. It
  decides the identities that carry $B(k)$ below the bound to every $k$, lays out every
  square of the packing at $k = 6$ to 40 and 101 (39 packings, each inside $[0, S]^2$ with
  $S < k$, no two interiors meeting, the count equal to $N$), refuses 75 mutated packings,
  checks the sharpness remark at 25 odd $b$ (waste exactly $4b$, below the bound by less
  than $16/b$, and $w < 4\sqrt{2k} + 15/8$ failing at $b = 127$), and finds each of the 36
  certificates to be this construction at its $k$, with the smaller $b$ at a tie.
- **[`certificate-replay.json`](receipts/certificate-replay.json)**, `replay` (12.8
  minutes wall at two workers, 11.7 CPU-minutes). The 36 certificates, read through the
  maintained `evand-cert` adapter after the packet’s custody check, are instances of the
  theorem: each is accepted by both maintained exact routes, `sqpack`’s predicates and the
  independent checker, over every wall and every pair whose centres are closer than
  $\sqrt 2$ (71,411 pairs), with the filter and controls of `devtools.couzo_678_replay`;
  all six controls of each (a duplicated square, a square outside, the side lowered by
  $10^{-18}$ past the least clearance, an enlarged square, a one-coordinate overlap and a
  near-contact pair moved $10^{-30}$ past contact) are refused by both, 216 of 216; and the
  sharp controls of `devtools.upper_bound_sharp_controls`, which decide all pairs, are as
  expected at the 13 certificates whose count is in the case corpus ($k \le 18$), 143 of
  143. At $k = 101$ the least pair gap is about $9.6 \cdot 10^{-15}$, below the binary64
  spacing of its coordinates. `check` reads the receipt back against the packet.
- **[`comparisons.json`](receipts/comparisons.json)**, `compare` (5 s). In integers:
  $\lceil\sqrt{32k}\rceil$ is smaller than Daniel’s $4\lceil\sqrt{2k - 7}\rceil - 1$ at
  495,210 of $7 \le k < 10^6$, ties it at 249,568 and is larger at 255,215, never by more
  than 2 from $k = 89$; it is strictly the least statement of the family at 346,919 of
  $42 \le k \le 702{,}000$ (below Daniel’s at 346,920, less $k = 10^5$, where Ryu’s
  certificate gives 1583). It is smaller than Ryu’s Theorem 1.4 at $k = 6$ and from 9, than
  his Theorem 1.3 at its best $b$ from 14, and than T-163 from 42; Ryu’s Theorem 1.2 is
  smaller at every $k \ge 1.6 \cdot 10^7$. Daniel’s unregistered
  $c^*(k) < 18.9k^{2/5} + 35.7k^{1/5} + 122$ ($k \ge 3 \cdot 10^5$) is first smaller at
  735,988 and smaller at every $k$ from 736,595, with $k^{1/5}$ bracketed between rationals
  until the comparison is decided. At every $n \le 324$ the case records already
  hold both bounds’ implications. Each comparison is decided one $k$ at a time and beyond
  by a tail lemma the receipt names.

From `packing/`, with the project interpreter:

```sh
P=resources/web/fang-theorem-a-2026-10-24/receipts
python -m cases.asymptotic.fang_theorem_a construction --out $P/construction.json
python -m cases.asymptotic.fang_theorem_a replay --workers 2
python -m cases.asymptotic.fang_theorem_a compare --out $P/comparisons.json
python -m cases.asymptotic.fang_theorem_a check [--replay K ...]
```

`tests/test_fang_theorem_a.py` runs the
construction’s checks on a bounded range with the identities as the tail, the mutation
controls, and the receipts’ checks, in the pull-request tier.

Theorem and lemma numbers here are the note’s as printed: Theorem A is its Theorem 1,
Lemma 2 fills a band end and Lemma 3 bounds a band.
This README and the register row called them Lemmas 1 and 2 until the review below
(its N-2).

## The Mathematical Review

The stage 4 review of 25 October 2026,
[review-2026-10-25-fang-theorem-a.md](../../../../docs/project/reviews/review-2026-10-25-fang-theorem-a.md),
re-derived the proof of Lemmas 2 and 3 and of Theorem A and accepted it with findings,
none blocking or major: two minor findings on the note’s Section 6 squeeze example and
the last sentence of its Section 7, and twelve notes.
Its programs, written from the note by a Claude agent prompted separately, and their
receipts are in [`review/review-2026-10-25/`](review/review-2026-10-25/README.md).
They decided every identity and inequality of Sections 2 to 5 symbolically, the bound
with both lemmas at every $k$ from 6 to 250,000, every square at 46 packings to
$k = 101$, and the note’s comparisons, including the first $k$ at which Daniel’s
unregistered $k^{2/5}$ bound is smaller, 735,988.

## Limitations

- **One AI review, not a referee.** The review is one AI reader’s re-derivation, of the
  system family the source also used. The checks above decide the construction one $k$ at
  a time to 60,000 and the identities for every $k$; that some close $t$ gives
  $H(t) < 4\sqrt{2k} + 2$ at every $k$ is the note’s continuity argument, which the
  review read.
- **No source program ran.** The source’s `lband.py --bound`, its three checkers and its
  windowed driver are retained or pinned and were not run; `VERIFICATION.md` reports them.
- **$k = 300$ and $600$ are the author’s statement**, by digest only. The optimized
  constructions of Section 6 (waste at most $4\sqrt{2k} + 1.18$ for $15 \le k \le 300$,
  9,946 squares below side 100, gains at $k = 25$, 30 and 40) are stated without
  certificates and are not registered; the acknowledgement asks the author for both.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
