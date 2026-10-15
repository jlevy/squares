# Fang’s Excess Theorem and Direct Certificates: Mathematical Review

**Verdict: accepted, with the theorems re-derived here from the retained material and no
blocking or major defect found.** Kevin Fang’s Theorem 1, $s(n^2 - n + 1) < n$ for every
integer $n \ge 15$, and Theorem 2, $s(n^2 - n + F(n)) < n$ with
$F(n) = 1 + \max\{p + 2q : 16p + 21q \le n - 15\}$, follow from three things, each of
which this review established without the note that holds the author’s proof: a gluing
lemma whose statement and proof are recoverable from `tools/glue.py` and the README and
are elementary; the validity of eighteen finite packings, the two squeezable rectangles
R and R′ and sixteen square bases, each decided here in exact arithmetic by a checker
written for this review; and a scaling lemma that turns the closed composite of a chain
of gluings into a strict packing of side $n - 1/20000$. The construction proves more
than the theorems state: $s(n^2 - n + F(n)) \le n - 1/20000$ for every $n \ge 15$.
Nothing mathematical rests on the unavailable note; what rests on it is only whether its
own text proves the theorems the way this review does, which cannot be said until it is
read.

The review also rebuilt all 76 inventory certificates from the retained pieces by its
own implementation of the lemma’s layout and found every one byte-identical to the file
the release ships, the six retained ones by direct comparison and the 70 pinned ones by
the SHA-256 the frozen header list and the tables record; then it decided all 76, the
six rectangles in both dimensions, the 25 square pieces and the fourteen direct
certificates strict-valid, in about three and a half CPU-minutes, with an all-pairs
control and two mutation controls.
Four findings are minor and three are notes; none changes the mathematics.
The direct certificates at 380, 381 and 382 are confirmed as the packet states them: the
retained replay receipt decides the retained certificates at their exact sides on both
routes, refuses its six controls, and the claims record’s comparisons hold.

Reviewer: an AI agent, Fable, strong tier, max reasoning, the mathematical lane of the
`think-0esw` import at stage 4, in a worktree and a session of its own.
It read the source as data and ran only code it wrote, kept in the packet under
[`review/`](../../../packing/resources/web/fang-excess-theorem-2026-10-13/review/README.md),
and this repository’s own exact checkers on the two packets.
No earlier review of these results exists; the packet README’s reading list, written by
the retaining lane, was read as the brief directed.
It registers nothing and moves no rung.
It is not a human oversight record.

## Scope and Evidence

The subject is
[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs) at
`078789a4cfd36f915f1bfbe76d742413d79b2965`, as the
[theorem packet](../../../packing/resources/web/fang-excess-theorem-2026-10-13/README.md)
and the
[direct-certificates packet](../../../packing/resources/web/fang-direct-certificates-2026-10-13/README.md)
retain it; both passed `devtools.acquire_source --check` here.
Read in full: the source’s `README.md`, `tools/glue.py`, `theorem/README.md`,
`theorem/PIECES.md`, `theorem/inventory.tsv`, `theorem/best.tsv`, the six rectangles’
`NOTES.md` and checker outputs, `CHANGELOG.md`, `ATTRIBUTION.md`, `VERIFICATION.md`,
`third_party/SOURCES.md`, `composites/REPRODUCE.md`, the direct folders’ `NOTES.md`, and
the archived paper of Arslanov, Mustafin and Shangitbayev
([`packing/resources/papers/arslanov-improved-packings-n-n-1.md`](../../../packing/resources/papers/arslanov-improved-packings-n-n-1.md)),
whose Figure 1 and inequality (3) are the ancestry of the gluing lemma.
Not read, on purpose: the source’s checkers `verify.py`, `tools/rectcheck.py` and Evan
Daniel’s `verify_cert.py`, so that the checker written here is clean-room with respect
to the code that decided the certificates at the source.
The note itself, *Packing n² − n + 1 unit squares in a square of side less than n, for
every n ≥ 15* (draft v0.6), is not in the repository and was not read.

Every program run here is kept in the packet’s `review/programs/` with the output it
printed in `review/outputs/`; the packet’s `review/README.md` says what each reads and
decides.
The repository’s own `devtools.upper_bound_reports check` and `check-claims` and
`cases.asymptotic.fang_excess_inventory --check` were run on both packets and passed.

## The Statements

Write $s(n)$ for the side of the smallest square containing $n$ unit squares with
pairwise disjoint interiors (README line 9).

- **Theorem 1** (README line 12). $s(n^2 - n + 1) < n$ for every integer $n \ge 15$.
- **Theorem 2** (README line 14). Let $n \ge 15$ and let $p, q \ge 0$ be integers with
  $16p + 21q \le n - 15$. Then $n^2 - n + 1 + p + 2q$ unit squares pack in a square of
  side less than $n$. In particular $s(n^2 - n + F(n)) < n$ with
  $F(n) = 1 + \max\{p + 2q : 16p + 21q \le n - 15\}$.

On the deficiency $c^*(k) = \max\{c : s(k^2 - c) = k\}$ the theorems read
$c^*(k) \le k - 2$ and $c^*(k) \le k - 1 - F(k)$ for every $k \ge 15$: if $k^2 - k + F$
squares fit below side $k$ then so do fewer, so $s(k^2 - c) < k$ for every
$c \ge k - F$, and the largest $c$ with $s(k^2 - c) = k$ is at most $k - F - 1$.

Theorem 1 is the case $p = q = 0$ of Theorem 2, and Theorem 2’s general case follows
from its particular case by removing squares, since $1 + p + 2q \le F(n)$ whenever
$16p + 21q \le n - 15$. So one statement carries everything: $n^2 - n + F(n)$ unit
squares pack in a square of side less than $n$, for every $n \ge 15$. The certificates
meet a stronger convention than the theorem needs: every square lies in the open box and
every pair is strictly separated along an edge normal (README lines 99–102), which
implies disjoint interiors.

## The Argument Re-derived

The proof has five parts: the gluing lemma, the scaling lemma, the pieces and their
squeezes, the chains with their counts, and the coverage of every $n \ge 15$. Each part
below says what it rests on.
None rests on the note.

### Step 1: Lemma 3, the Gluing

**Statement** (`tools/glue.py` lines 11–24, with the hypotheses of lines 115–146). Let A
be a packing of $N_A$ unit squares in the closed rectangle $[0, W_A] \times [0, H_A]$,
with integer box $a \times b$, $a = \lceil W_A \rceil > b = \lceil H_A \rceil$, and let
$d_A = \min(a - W_A, b - H_A) > 0$. Let B be a packing of $N_B$ unit squares in
$[0, W_B] \times [0, H_B]$ with box $a' \times b'$: either a square container,
$a' = b' = m = \lceil W_B \rceil$ and $d_B = m - W_B$, or a rectangle with $W_B > H_B$,
$a' > b'$ and $d_B = \min(a' - W_B, b' - H_B)$; in either case $d_B > 0$. Let
$0 < d \le \min(d_A, d_B, 1/2)$, $n = b + b'$, $c = n - a'$, and suppose $n \ge a$,
$c \ge 0$ and $c \le a - d$. Then the square $[0, n - d]^2$ holds a packing of
$n^2 - w_A - w_B$ unit squares, where $w_A = ab - N_A$ and $w_B = a'b' - N_B$ are the
pieces’ wastes.

**Proof.** Write $S = n - d$. Four closed rectangles lie in $[0, S]^2$ with pairwise
disjoint interiors:

$$
\mathcal A = [0, a - d] \times [n - b, S],\quad
\mathcal D = [a - d, S] \times [S - b, S],\quad
\mathcal C = [0, c] \times [0, n - b],\quad
\mathcal B = [c, S] \times [0, S - b].
$$

$\mathcal A$ and $\mathcal D$ meet only on the line $x = a - d$; $\mathcal A$ and
$\mathcal C$ only on $y = n - b$; $\mathcal A$ and $\mathcal B$ are separated by the
strip $S - b < y < n - b$ of width $d$; $\mathcal D$ and $\mathcal B$ meet only on
$y = S - b$; $\mathcal C$ and $\mathcal B$ only on $x = c$; and $\mathcal C$ and
$\mathcal D$, whose $y$-ranges overlap in $[S - b, n - b]$, are separated in $x$ because
$c \le a - d$, the one hypothesis that is not a convention.
All four lie in $[0, S]^2$ since $c \le a - d \le S$ (as $a \le n$ and $d > 0$). Place A
translated up so that its top edge is $y = S$, that is in
$[0, W_A] \times [S - H_A, S]$; since $W_A \le a - d$ and $H_A \le b - d$, this is
inside $\mathcal A$. Place B translated right so that its right edge is $x = S$, in
$[S - W_B, S] \times [0, H_B]$; since $W_B \le a' - d$ and $H_B \le b' - d = S - b$,
this is inside $\mathcal B$. Fill $\mathcal D$, which is $(n - a) \times b$, and
$\mathcal C$, which is $c \times (n - b)$, with axis-aligned unit squares on the integer
grid of each; both dimensions are integers.
Two squares in different regions have disjoint interiors because each lies in its closed
region and the regions’ interiors are disjoint; two squares of one piece because
translation preserves the piece’s validity; two of one block because they are grid
cells. The count is $N_A + (n - a)b + c(n - b) + N_B$, and since
$ab + (n - a)b + c(n - b) + a'b' = n^2$ (the boxes $a \times b$, $(n - a) \times b$,
$c \times (n - b)$ and $a' \times b' = (n - c) \times (n - b)$ tile $[0, n]^2$), it is
$n^2 - w_A - w_B$. $\square$

This is Arslanov, Mustafin and Shangitbayev’s Figure 1 with their inequality (3),
$\delta(S) \ge \min(\delta(A), \delta(B))$, made exact: the composite at side $n - d$ is
valid in the closed sense, with the two integer blocks touching each other and the
pieces, which is why the composite is not yet a strict certificate.
`glue.py` asserts exactly this tiling and this count (lines 147–162); the review’s
`glue_rebuild.py` implements the same layout from this description and reproduces every
shipped composite of the inventory to the byte (Step 6).

*Rests on the note:* nothing.
The lemma and its proof are complete from the retained files.

### Step 2: The Scaling to a Strict Certificate

**Statement** (`glue.py` lines 24–34). Let $N$ closed unit squares with pairwise
disjoint interiors lie in the closed square $[0, S]^2$, and let $\lambda > 1$. Move each
square’s centre from $(x, y)$ to $(\lambda x, \lambda y)$ and keep its rotation.
Then every square lies in the open square $(0, \lambda S)^2$ with every corner at
distance at least $(\lambda - 1)/2$ from every wall, and every pair is strictly
separated along one of its four edge normals with separation at least $\lambda - 1$.

**Proof.** A unit square’s projection on any unit direction has half-width
$h = (|a \cdot u| + |a \cdot v|)/2 \ge 1/2$, since $|a \cdot u| \ge (a \cdot u)^2$ and
$(a \cdot u)^2 + (a \cdot v)^2 = 1$. For a wall, say $x = 0$: a square with centre
abscissa $x$ and half-width $h$ along the $x$-axis has $x - h \ge 0$ before scaling, so
afterwards its leftmost corner is at $\lambda x - h = \lambda(x - h) + (\lambda - 1)h
\ge (\lambda - 1)/2$; the wall $x = \lambda S$ and the two horizontal walls are the same
computation. For a pair, two closed convex polygons with disjoint interiors are weakly
separated along one of their edge normals (the separating-axis theorem), so before
scaling some edge normal $e$ of one of them has $|(q - p) \cdot e| \ge h_p + h_q$ with
$p, q$ the centres and $h_p, h_q$ the half-widths along $e$. After scaling the
separation along the same $e$, whose direction is unchanged, is
$\lambda |(q - p) \cdot e| - h_p - h_q \ge (\lambda - 1)(h_p + h_q)
\ge \lambda - 1$. $\square$

With $d_0 = 1/10000$ and $\lambda = 1 + d_0/(2(n - d_0))$, the closed composite at side
$n - d_0$ becomes a strict certificate at side $\lambda(n - d_0) = n - d_0/2 =
(20000n - 1)/20000 < n$, with least pair separation at least
$\lambda - 1 = 1/(20000n - 2)$ and least wall clearance at least half that.
Where an integer block touches another region the bounds are attained exactly, which the
inventory shows: in 56 of the 76 certificates, every one built by at least one gluing,
the least pair gap decided here is exactly $1/(20000n - 2)$ and the least wall clearance
exactly $1/(2(20000n - 2))$; in the 20 that are a bare base scaled, both are larger.
The record’s two-route replay of 932 found the same $1/619998$ and $1/1239996$.

*Rests on the note:* nothing.

### Step 3: The Pieces and the Uniform Squeeze

The theorem’s chains use eighteen pieces (`theorem/PIECES.md`, role `theorem`): the
rectangles R (`r17x16_n0257`, 257 squares, box $17 \times 16$, waste 15) and R′
(`r22x21_n0443`, 443 squares, box $22 \times 21$, waste 19), and the square bases
`n-211`, `n-241`, `n-273`, `n0308` (truncated to its first 307 squares), `n0343`,
`n0381`, `n0421`, `n0463`, `n0507`, `n0553`, `n0601`, `n0651` with excess 1, and
`n-110`, `n-132`, `n-156`, `n-182` with excess 0. Each piece has to be a valid packing
of its box shrunk by $d_0$ in both directions, which is the same as its squeeze
$\min(a - W, b - H)$ being at least $d_0$; and R and R′ have to be squeezable rectangles
with the wastes the lemma’s count uses.

Decided here, by `rectangle_check.py` on the retained files (`outputs/rectangles.out`,
`outputs/pieces.out`): all six rectangles and all 25 square pieces the inventory names
are strict-valid in the open box $[0, W] \times [0, H]$ with the header’s exact
dimensions, so in particular R’s 257 squares lie in $(17 - \delta) \times (16 - \delta)$
with $\delta = 126532561084761488992828749143827311 / 2^{127} = 0.000743691\ldots
\ge 7.436 \times 10^{-4}$, as the README’s Proposition 4 states, and R′’s 443 in
$(22 - d) \times (21 - d)$ with $d = 3212134849537150775519004506655055571 / 2^{128}
= 0.009439615\ldots \ge 0.0094$. The squeezes agree with the rounded-down values in
`PIECES.md` for all 31 pieces, and the least wall clearance and least pair gap found
here equal the figures the source’s own `verify_output.txt` prints for every rectangle,
down to the pair that attains them (R: $2.711 \times 10^{-20}$ at square 1 and
$2.769 \times 10^{-20}$ at squares 32 and 33; R′: squares 402 and 423). The least
squeeze among the theorem’s pieces is `n0308`’s $0.000690144\ldots$, then R’s; every one
exceeds $d_0 = 0.0001$ (`PIECES.md`’s last line, checked here exactly).
Among all 31 pieces the least is `n0814`’s $0.000126396\ldots$, used only by `best/`.

The square bases are also decided by the record: Daniel’s certificates at 110, 132, 156,
182, 210, 211, 241 and 273 by the two-route replay of the 2026-10-05 packet
(`E-evand-exact-optima-2026-10-05-exact-replay`), 308 by the replay behind T-135, 343 by
the same packet’s, and 381 by the direct-certificates packet’s receipt.
The rectangles had no exact check in this repository before this review, since no
maintained route reads a rectangular container; the direct packings at 421 to 651, the
bases for $n = 21$ to 26, had none either.

*Rests on the note:* nothing.
The note’s Proposition 4 (R’s squeeze) and Proposition 5 (the $m^2 - m$ bases) are facts
about these certificates and were decided from them.

### Step 4: The Chains and Their Counts

A gluing step with a rectangle of box $a \times b$ and waste $w$ onto a square packing
of $m^2 - m + j$ squares in an $m \times m$ box gives, by Lemma 3 with $a' = b' = m$,
$n = m + b$ and $c = n - m = b$: the hypotheses hold whenever $a = b + 1$ and
$d \le 1/2$, since then $c = a - 1 \le a - d$ and $n \ge a$ as soon as $m \ge 1$; and
the count is
$n^2 - w - (m^2 - (m^2 - m + j)) = n^2 - w - m + j = n^2 - n + (b - w) + j$. So R, with
$b - w = 1$, takes $(n, j)$ to $(n + 16, j + 1)$ and R′, with $b - w = 2$, to
$(n + 21, j + 2)$. Starting from a base of excess 1 at side $r$ and applying R $p$ times
and R′ $q$ times in any order gives $n = r + 16p + 21q$ and $j = 1 + p + 2q$. The bases
at $r = 27, \ldots, 30$ are themselves one R step on the excess-0 packings of $m^2 - m$
squares at $m = 11, \ldots, 14$: $(m + 16)^2 - (m + 16)
+ 1$ squares, as the lemma’s count says.

Every step is taken at the common squeeze $d_0$, closed.
The first step’s B is a piece with $d_B \ge d_0$, every later step’s B is the previous
closed composite, whose box is $n \times n$ at side $n - d_0$ so that $d_B = d_0$
exactly, and A is R or R′ with $d_A > d_0$; so $0 < d_0 \le \min(d_A, d_B, 1/2)$ at
every step. One scaling at the end (Step 2) gives the strict certificate at side
$n - 1/20000$.

`excess_arithmetic.py` recounted every chain of `inventory.tsv` and `best.tsv` from the
pieces’ counts and boxes in `PIECES.md` and found each row’s count and side; it also
recomputed $F(n)$, the maximiser and the base $r = n - 16p - 21q$ for every row
(`outputs/excess_arithmetic.out`).

*Rests on the note:* nothing.

### Step 5: Why Every $n \ge 15$ Is Covered

For $n$ in $15..30$ the base itself has $n^2 - n + 1$ squares and $F(n) = 1$. For
$n \ge 15$ in general, let $(p, q)$ attain $\max\{p + 2q : 16p + 21q \le n - 15\}$ and
$r = n - 16p - 21q$. Then $r \ge 15$ by the constraint, and $r \le 30$, since otherwise
$(p + 1, q)$ would be admissible with a larger value.
So the base at $r$ is one of the sixteen, and the chain of Step 4 gives $n^2 - n + F(n)$
squares at side $n - 1/20000$. This is the extreme case of Theorem 2, and Theorem 1 and
the general case follow by removing squares (The Statements).
Theorem 1 also follows directly by steps of 16 from the same bases:
$(p, q) = (\lfloor (n - 15)/16 \rfloor, 0)$ leaves $r$ in $15..30$.
`excess_arithmetic.py` checked both decompositions for $n = 15..2000$.

Hence, for every $n \ge 15$, $s(n^2 - n + F(n)) \le n - 1/20000 < n$. $\square$

*Rests on the note:* nothing.
The README’s one-line outline, “inducts on n in steps of 16, starting from finitely many
certificates” (line 17), describes Theorem 1; Theorem 2’s chains also step by 21 (MR-2).

### Step 6: The Inventory Rebuilt and Decided

`glue_rebuild.py` built all 76 certificates of `theorem/` from the retained pieces by
their `chain` columns, at $d_0$, closed, then scaled once, and wrote each with the
comment line the retained files carry.
All 76 have the SHA-256 that `acquisition/inventory-headers.json` froze from the
checkout at the pin, which is the manifest’s digest of the shipped file, and the SHA-256
the tables’ own column states; the six the packet retains are equal byte for byte
(`outputs/glue_rebuild.out`). So the 70 pinned certificates are known, without their
bytes, to be exactly the Lemma 3 composites of retained pieces that their rows describe,
and their validity is a consequence of Steps 1 to 5. It was also decided directly:
`rectangle_check.py` on the 76 rebuilt files found every one strict-valid at side
$(20000n - 1)/20000$ (`outputs/inventory_rebuilt.out`, 60 CPU seconds), with the margins
of Step 2.

## The Deficiency Comparison, $k = 15..72$

**As a theorem.** Theorem 2 gives $c^*(k) \le k - 1 - F(k)$ and Theorem 1
$c^*(k) \le k - 2$ for every integer $k \ge 15$, on this review’s re-derivation.
The packet README’s table is right at every row: Theorem 1 is below Arslanov, Mustafin
and Shangitbayev’s $k - 1$ at every $k \ge 15$; Theorem 2 is below Ryu’s
$8\lceil\sqrt{k - 4}\rceil - 1$ at $k = 15..78$ and $86$, tied at 79 and 87, and above
it at $80..85$ and from 88 on, searched to 2,000 here as in the packet.
Since $1 + 2\lfloor (k - 15)/21 \rfloor \le F(k) \le 1 + 2(k - 15)/21$ at every $k$ (the
upper bound because $p + 2q \le (2/21)(16p + 21q)$), the bound is $(19/21)k + O(1)$,
linear, which Ryu’s $O(\sqrt k)$ beats for large $k$.

**As finitely checked cases.** For $k = 15..64$ the inventory certificates establish
$s(k^2 - k + F(k)) \le k - 1/20000$, hence $c^*(k) \le k - 1 - F(k)$, and at the 26
counts of `best/` the better $c^*(k) \le k - 1 - j$: $j = 2$ at $k = 18..23, 28, 29$;
$3$ at $34, 35$; $4$ at $39..44$ and $49..51$; $5$ at $55, 56$; $6$ at $60..64$. Six of
those certificates are machine-replayed by the record on two routes (211, 241, 273, 307,
308, 932); all 76 are decided by this review’s one independent route.
For $k = 65..72$ no certificate exists in the release; the row is the theorem’s, and the
construction would produce the certificate in seconds.
The record’s own rows equal Theorem 2’s at $k = 15, 16, 17$, are one smaller at 18 and
19 (the 308 and 344 packings, which the inventory’s `best/` also reaches), and at
$k = 20$ the inventory’s 382 is one below the record because 382 has no row on `main`
yet; the direct packet brings it.

## The Checkers and Their Trust Boundaries

The checker written here, `squares_exact.py`, parses the certificate convention of
README lines 94–102, builds each square’s unit edge vectors
$((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2))$ and its corners, and decides two things in
`Fraction` arithmetic: every corner strictly inside $(0, W) \times (0, H)$, and every
pair strictly separated along one of the four edge normals.
It trusts Python’s rational arithmetic and the separating-axis theorem, under which
strict separation along an edge normal is equivalent to disjointness of the closed
squares. Its bucketed route decides a pair by the axis test only when the centres are
within $\sqrt 2$, tested exactly as $dx^2 + dy^2 \le 2$ within a grid of cells of side
2, and treats farther pairs as disjoint, which they are: a closed unit square lies in
the closed disc of radius $\sqrt 2 / 2$ about its centre.
The all-pairs route decides every pair by the axis test.
Both routes agreed on the verdict and on the least wall clearance and least pair gap,
the latter to the exact fraction, on R, R′, the rebuilt 932 and the direct 380
(`outputs/rectangles_all_pairs.out`, `outputs/all_pairs_932_380.out`); the duplicate and
outside controls were refused on R and R′ (`outputs/controls_*.out`).

It shares no code with the source’s three checkers, which were not read, nor with the
record’s two routes, `sqpack`’s exact witness verifier and
`devtools.check_rational_witness_independent`; it shares their method, rational
half-angle representation and separating axes, which is the one method anyone uses for
this question. Where it and the record’s routes decided the same certificate (211, 241,
273, 307, 308, 932, 380, 381, 382) the least margins agree exactly.
Its authorship overlaps the source’s in system family: the source states that its
search, verifier and bundle were written with Claude (Anthropic), and this review is by
a Claude agent, prompted separately and writing in files of its own.

`glue_rebuild.py` is not clean-room: it implements the layout `tools/glue.py` describes
after reading that program, in its own code, and decides identity, not geometry.
The other programs read tables, receipts and claims records as data and decide
arithmetic or provenance.

## Defects

No blocking or major defect was found.

| Id | Grade | Location | Description | Blocking | Resolution |
| --- | --- | --- | --- | --- | --- |
| MR-1 | minor | `theorem/PIECES.md` lines 7–8, 12–20, 26–37 | The table’s `sha256` column identifies the shipped file for Daniel’s eight pieces only; for the author’s own 22 pieces the digest is neither the shipped file’s nor its comment-stripped bytes’ (`outputs/pieces_digests.out`), so the inventory’s piece list does not bind to the release by digest. The binding was established here by rebuilding the inventory from the shipped pieces | No | Record the digests of the shipped files, as each folder’s `SHA256SUMS` does, or say which copies the column names |
| MR-2 | minor | `README.md` lines 16–17 | The proof outline names only R and “steps of 16”; Theorem 2 as stated at line 14 also needs R′ and steps of 21, added on 2026-10-13 (`CHANGELOG.md` line 29, `theorem/README.md` lines 5–8) | No | One sentence |
| MR-3 | minor | `README.md` lines 146–153; `ATTRIBUTION.md`, Licence | The licence list names `nNNNN/`, `rectangles/` and `composites/` under CC0 and the code under MIT, and does not name `theorem/` | No | State the licence of `theorem/` |
| MR-4 | minor | `theorem/n015_F1.cert`, `n031_F2.cert`, `n036_F3.cert`, `n052_F4.cert`, `n057_F5.cert`; `README.md` lines 22, 152–153; `composites/REPRODUCE.md`, “Composites from de Winter’s n = 211 packing” | These five certificates contain Daniel’s exact certificate of de Winter’s unlicensed 211-square packing, its centres scaled by a rational factor, while the README says that packing is fetched and not copied and the composites built on it were left out of the release for that reason | No: a question of licence, not of mathematics | The author’s decision: say what licence the five carry, or treat them as the composites were treated |
| MR-5 | note | `theorem/README.md` line 14 | `instantiate_theorem.py`, which built the inventory, is private; the inventory reproduces only by re-implementing the chains, as done here | No | Ship it under MIT, as `tools/glue.py` is |
| MR-6 | note | `README.md` line 14 | Theorem 2’s statement with free $(p, q)$ follows from its particular case $F(n)$ by removing squares; the two-part statement reads as if the general case needed its own construction | No | Presentation |
| MR-7 | note | `README.md` lines 12–14, 30; `theorem/README.md` lines 3–5 | The construction proves the uniform bound $s(n^2 - n + F(n)) \le n - 1/20000$ for every $n \ge 15$, which the release states only for $n \le 64$ as the inventory’s side | No | A corollary the author may wish to state |

## Questions for the Author

1. Can the note, draft v0.6, be made available at a pinned address, so that its Lemma 3
   and its proof of Theorems 1 and 2 can be read against the derivation above?
   (The packet’s bead already asks this.)
2. Does the note state Lemma 3 with the hypothesis $c \le a - d$ and prove the final
   strictification separately, as `tools/glue.py` does, or does it keep every step
   strict at $d = \min(d_A, d_B, 1/2)$?
3. Does the note state the uniform bound $s(n^2 - n + F(n)) \le n - 1/20000$, or any
   explicit squeeze, for every $n \ge 15$ (MR-7)?
4. Which licence covers `theorem/` (MR-3), and what is intended for the five
   certificates that contain the 211-square piece (MR-4)?
5. Which copies of the pieces do the digests in `theorem/PIECES.md` name (MR-1)?
6. Will `instantiate_theorem.py` be shipped (MR-5)?

## Checks Run Here

All programs are in the packet’s `review/programs/`, run from `packing/` with the
project interpreter as `python3 -I -B`, reading the retained packets by path; the
commands are in `review/README.md` and every output is in `review/outputs/`.

| # | Check | Result |
| --- | --- | --- |
| 1 | $F(n)$, its maximiser and base, $n = 15..2000$; Theorem 1’s step of 16 | base $r$ in $15..30$ at every $n$; $F$ non-decreasing from 1 |
| 2 | Every row of `inventory.tsv` and `best.tsv`: $(F, p, q, r)$, count, side; the chain recounted from the pieces | 50 and 26 rows, all hold |
| 3 | Deficiency table $k = 15..72$ and the crossover with Ryu’s bound to 2,000 | as the packet README prints; below at $15..78$ and $86$, tied at 79 and 87 |
| 4 | The six rectangles decided in both dimensions, bucketed route | all strict-valid; squeezes R $0.000743691\ldots$, R′ $0.009439615\ldots$, the four others $0.00245$, $0.00595$, $0.01171$, $0.00278$; wastes $b - 1$, $b - 2$ for R′ |
| 5 | R and R′ with every pair decided by the axis test | same verdicts and least margins as check 4; 32,896 and 97,903 pairs |
| 6 | Duplicate-square and outside-container controls on R and R′ | all four refused, on squares 0 and 1 or on square 0 |
| 7 | The 25 square pieces (Daniel’s eight, `n0308`, `n0343`, `n0344`, the fourteen direct packings) | all strict-valid; squeezes as `PIECES.md`; least theorem-piece squeeze `n0308` $0.000690144$, all above $1/10000$ |
| 8 | The six retained inventory certificates | all strict-valid; least margins equal the record’s receipt, e.g. $1/1239996$ and $1/619998$ at 932 |
| 9 | All 76 inventory certificates rebuilt from the pieces by Lemma 3 and compared | 76 of 76 digests equal the frozen list’s and the tables’; 6 of 6 retained files equal byte for byte |
| 10 | The 76 rebuilt certificates decided | all strict-valid at $(20000n - 1)/20000$; 56 with least gap exactly $1/(20000n - 2)$ and clearance exactly half, 20 larger; 60 CPU s |
| 11 | All-pairs control on the rebuilt 932 and on the direct 380 | same least margins as the bucketed route; 433,846 and 72,010 pairs |
| 12 | The theorem packet’s receipt and claims record | 18 jobs on the retained certificates; 6 positives pass both routes, 12 controls refused; 3,697,788 pair decisions, 1,278.6 route CPU s, 1,733.9 wall s, longest 485.4 s; every claim comparison holds |
| 13 | The direct packet’s receipt and claims record | 9 jobs on the retained certificates; 3 positives pass both routes with wall clearance $2^{-65}$ and gaps $2.33, 1.79, 1.58 \times 10^{-20}$; 6 controls refused; 1,303,026 pair decisions, 652.1 CPU s, 863.3 wall s, longest 138.3 s; every claim comparison holds |
| 14 | Which files `PIECES.md`’s digests identify | 8 the shipped file, 1 (R′) its comment-stripped bytes, 22 neither |
| 15 | The repository’s own checks: `acquire_source --check`, `upper_bound_reports check` and `check-claims` on both packets, `fang_excess_inventory --check` | all pass |

## Not Reached

The note was not read, so whether its text proves the theorems as above is not known.
The source’s checkers were not run and not read.
The `.cert.json` copies of the certificates were not compared with the `.cert` files
here; the direct packet’s `read_facts` holds them equal.
The 230 composites of `composites/` and the 38 shipped ones were not rebuilt or decided,
being another import’s; the rebuild program could do it with the same layout.
No local minimality, rigidity or optimality is claimed by the source or examined here.
The eleven direct certificates at 421 to 814 were decided here on one route only (check
7); the record’s two-route replay of them waits for the owner’s budget.
The gluing with a rectangular B, which `glue.py` admits and the `best/` chains `R'+R'`
use, was re-derived under Lemma 3’s general hypotheses and exercised by the rebuild at
$n = 42$ and $63$; the theorem’s own chains never need it.

## The Direct Certificates at 380, 381 and 382

This is the records-lane check the brief asked for, on the
[direct-certificates packet](../../../packing/resources/web/fang-direct-certificates-2026-10-13/README.md).

- **The replay decides the stated sides.** The retained receipt’s nine jobs take as
  input the retained `n0380.cert`, `n0381.cert` and `n0382.cert`, count, side and every
  pose, as reparsed here; `upper_bound_reports check` admits it against the same files.
  Both routes pass each positive at the certificate’s exact side, which rounds up at 15
  places to the side the source prints, 19.976775433974195, 19.976969740405508 and
  19.989479729399675, with every pair tested and the least wall clearance $2^{-65}$ and
  least pair gaps $2.33 \times 10^{-20}$, $1.79 \times 10^{-20}$ and
  $1.58 \times 10^{-20}$ that the packet README states.
  The checker written here decided the same three certificates and found the same least
  margins to the exact fraction (check 7), and it decided the other eleven strict-valid
  too.
- **The controls hold.** Both routes refuse the six controls: the duplicate-square job
  on the overlap of squares 0 and 1, the translated-square job on square 0 through the
  right wall, each with a negative margin on the mutated quantity only.
- **The claims record holds.** `check-claims` rebuilds it unchanged, and the comparisons
  recomputed here from the exact sides agree with it and with the README’s table: 380
  and 381 below the standing Couzo rows by $1.07 \times 10^{-2}$ and
  $1.57 \times 10^{-2}$; 381 below #582 by $8.66 \times 10^{-3}$; all three above
  Couzo’s #583 and #586 by the amounts the README gives; 382 below the grid by
  $1.05 \times 10^{-2}$ with no row; the other eleven the smallest the record knows,
  below the grid by $1.26 \times 10^{-4}$ (814) to $1.38 \times 10^{-2}$ (421). The 508
  side is below the 507 side, so the consequence $s(507) \le 22.994733849702143$ the
  README names is right.
  The summed statistics the README prints are the receipt’s.

Nothing in the direct packet is questioned.

## For the Records Lane

**What the retained material supports.** For the theorems: the proof is recoverable from
the public repository and was re-derived in full above, so the packet’s planned `V2`,
“proof asserted but not publicly recoverable”, understates it; `V3` as a proof audited
here is defensible once this review is mapped, and the choice between them is the
owner’s reading of what an audit requires.
On the confirming side this review is a qualifying read, `C1`, and every finite part of
the proof, the pieces and the inventory, is decided here by an independent
implementation with full coverage; if the records lane registers those runs as evidence
they confirm the finite parts at that level, and the theorem for all $n$ stays what a
read can give, since no machine replays an induction.
For the inventory’s finite bounds: `C3` at 211, 241, 273, 307, 308 and 932 from the
record’s two-route replay, which this review found sound; the other 70 are decided here
on one route, full coverage of the inventory, and are byte-identical rebuilds of the
pinned files from retained pieces, which the records lane may treat as their retention
or not under `OR-18`. For the direct certificates: `C3` at 380, 381 and 382 from the
record’s replay, independently re-implemented, with this review’s route beside it; the
other eleven decided here on one route.

**Significance.** `S4` as drafted: a bound family for every $n \ge 15$ with an explicit
construction, which improves Arslanov, Mustafin and Shangitbayev’s $k - 1$ at every $k$
and Ryu’s bound at $15 \le k \le 78$; it settles no case $n \le 324$.

**The superseded mark.** The register entry’s four in-scope finite bounds are above
their cases, so `check_standing` will mark them superseded; nothing supersedes the
theorem, which no other result implies at any $n$, and the entry’s claim should say so
in words.

**Proposed `verifiers.yaml` entries.** Written here, not added to the file; the records
lane adds them with the evidence entries it writes and the digests it computes.

```yaml
  - id: V-fang-review-exact-checker
    program: rectangle_check.py, with its module squares_exact.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      Decides a square or rectangle certificate in Evan Daniel's text format strict-valid
      in both dimensions in Fraction arithmetic: every corner strictly inside the open
      box and every pair strictly separated along an edge normal, pairs with centres
      farther than sqrt 2 apart decided by the exact distance test within a grid of
      cells of side 2, or every pair by the axis test with --all-pairs; reports the exact
      squeeze, least wall clearance and least pair gap, and refuses the duplicate-square
      and outside-container controls.
    source:
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/rectangle_check.py
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/squares_exact.py
    independence_record: docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md
    independence:
      read: [mathematics, specification, certificate-format, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the mathematical review lane of the fang-theorem intake, Fable, strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source states that its search, verifier and bundle were written with
          Claude (Anthropic). This program was written by a Claude agent prompted
          separately, in files of its own, from the README's statement of the
          certificate convention and the separating-axis theorem; the source's
          checkers verify.py, tools/rectcheck.py and verify_cert.py were not read.
      note: >-
        The producer's stored checker outputs were read afterwards to compare the least
        margins, which agree to the printed digits on every rectangle.
    note: >-
      The mathematical review of 14 October 2026 wrote it and ran it on the six
      rectangles, the 25 square pieces, the 76 inventory certificates (six retained, 70
      rebuilt byte-identical to the pinned files) and the fourteen direct certificates,
      all strict-valid, with the all-pairs route agreeing on R, R', 932 and 380 and the
      two controls refused. Kept as run in the packet's review/, with every output.

  - id: V-fang-review-glue-rebuild
    program: glue_rebuild.py, with squares_exact.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      Rebuilds each certificate of Fang's theorem inventory from the retained pieces by
      its chain, as the Lemma 3 composite at the common squeeze 1/10000 scaled once by
      1 + d0/(2(n - d0)), and decides whether its bytes are the shipped file's by the
      SHA-256 the frozen header list and the tables record, and by the bytes where the
      file is retained.
    source:
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/glue_rebuild.py
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/squares_exact.py
    independence_record: docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md
    independence:
      read: [mathematics, producer-code, certificate-format, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the mathematical review lane of the fang-theorem intake, Fable, strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Written after reading tools/glue.py, the producer's construction, in code of
          its own that copies none of it; instantiate_theorem.py, which built the
          inventory, is private and was not read. The source states Claude assistance.
      note: >-
        It decides identity, not geometry: 76 of 76 rebuilt certificates have the
        digests of the shipped files, which binds the 70 pinned ones to the retained
        pieces and Lemma 3's layout.
    note: >-
      The mathematical review of 14 October 2026 wrote and ran it; the rebuilt files
      are not kept (OR-18) and are written again in two seconds.

  - id: V-fang-review-excess-arithmetic
    program: excess_arithmetic.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      Decides the arithmetic of Theorem 2 from its definition: F(n) and its maximiser
      with the base in 15..30 for n = 15..2000, every row of inventory.tsv and best.tsv
      with its chain recounted from the pieces' counts and boxes, and the deficiency
      comparison with Ryu's and Arslanov, Mustafin and Shangitbayev's bounds.
    source:
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/excess_arithmetic.py
    independence_record: docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md
    independence:
      read: [mathematics, specification, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the mathematical review lane of the fang-theorem intake, Fable, strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Written from the README's definition of F(n) and the tables, read as data;
          it shares nothing with cases/asymptotic/fang_excess_inventory.py either,
          which was read only after its results were in hand.
      note: Every statement it decides held.
    note: >-
      The mathematical review of 14 October 2026 wrote and ran it; output kept in the
      packet's review/outputs/.

  - id: V-fang-review-receipt-summary
    program: receipt_summary.py, with squares_exact.py; pieces_digests.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Reads an upper-bound packet's exact replay receipt and claims record and holds
      them to the retained certificates: each job's input, verdicts, least margins and
      controls, the summed statistics, and every claim comparison recomputed from the
      exact sides; pieces_digests.py says which files the PIECES.md digests identify.
    source:
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/receipt_summary.py
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/pieces_digests.py
      - packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/squares_exact.py
    independence_record: docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md
    independence:
      read: [certificate-format, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the mathematical review lane of the fang-theorem intake, Fable, strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Reads this repository's receipts and claims records and the retained
          certificates; decides no geometry. The source states Claude assistance.
      note: A premise check for the two packets' receipts.
    note: >-
      The mathematical review of 14 October 2026 wrote and ran it on the theorem and the
      direct-certificates packets; both receipts and both claims records held.
```

## Verdict

Accepted.
Theorems 1 and 2 are proved from the retained material: Lemma 3 and the scaling
lemma are elementary and were re-derived; the eighteen pieces the chains use are
strict-valid in their boxes, decided here, with every squeeze above the common
$1/10000$; the chains give $n^2 - n + F(n)$ squares at side $n - 1/20000$ for every
$n \ge 15$, and the inventory for $n = 15..64$ is exactly what that construction builds,
to the byte, and valid.
The deficiency bounds $c^*(k) \le k - 2$ and $c^*(k) \le k - 1 - F(k)$ hold for every
$k \ge 15$ as theorems, and the rows at $k = 15..64$ are also finitely checked.
The seven findings concern digests, prose, licences and a stronger statement the author
may wish to make. The limit of this verdict is that it is one AI reviewer’s derivation,
of the same system family as the author’s assistant, and that the note itself has not
been read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
