# Hyukdong Kim’s Exact Sides at 88, 126, 172, 199 and 263, Issue 804

Hyukdong Kim reports in [jlevy/squares#804](https://github.com/jlevy/squares/issues/804),
opened 2026-10-25T01:57:25Z, that the side of the best-known packing at each of 88, 126,
172, 199 and 263 is a stated root of a stated integer polynomial, irreducible over Q.
The issue attaches `squares-exact-forms.zip`, whose `exact_forms.json` gives each
polynomial, highest degree first, and the side to 100 digits.
It is a numerical determination with no exact configuration, and the issue says so.

| n | Degree | Root | The record’s holder of that side | What the record does with it |
| ---: | ---: | --- | --- | --- |
| 88 | 7 | 4th of 5 real roots | T-193 (Evan Daniel, #639), V3/C3 | Nothing new: the same polynomial and root |
| 126 | 2 | $15/2 + 3\sqrt{2}$, the larger root of $4s^2 - 60s + 153$ | T-193 | Nothing new |
| 172 | 24 | least of 4 real roots | none: 3.898e-89 below T-174 | T-244, reported (V0/C0) |
| 199 | 16 | 2nd of 2 real roots | T-193 | Nothing new |
| 263 | 17 | the only real root | none: 2.126e-94 below T-174 | T-244, reported (V0/C0) |

## Source and Credit

| Field | Value |
| --- | --- |
| Issue | [jlevy/squares#804](https://github.com/jlevy/squares/issues/804), opened 2026-10-25T01:57:25Z by HyukdongKim; no comments and never edited when read at 05:50:06Z. The author’s two later comments, of 07:22:16Z and 09:06:23Z, are kept in the [configurations packet](../hyukdongkim-t244-configurations-2026-10-25/README.md) |
| Evidence | The attachment [`squares-exact-forms.zip`](https://github.com/user-attachments/files/33917140/squares-exact-forms.zip) |
| Pin | SHA-256 `c770f9c37dee6b248543f3e661318630a0f279bc6a8c7663cb2efc53e2814ee7`, which the issue states, and 14,112 bytes; an attachment has no commit or DOI |
| Bibliography key | **[Kim exact forms 2026-10-25]** |
| Human credit | Hyukdong Kim (ORCID [0000-0001-5787-8066](https://orcid.org/0000-0001-5787-8066)), for the exact sides; the packings are their finders’, as the issue credits them from the case records |
| AI assistance | The issue says the search for open cases, the KKT and LLL pipeline, the computations and the verification script were done by Claude (Anthropic) in a chat session at the author’s direction, and that he reviewed the outputs |
| Licence | None stated, in the issue or the archive |
| Retrieved | 25 October 2026 at 05:47Z, through `gh` with `NO_PROXY` set for GitHub’s hosts |

## What the Issue Reports

- **Claim.** “The side of the current record packing at each count below is the real
  algebraic number given, as a root of the stated polynomial, which is irreducible over
  Q.” The issue compares with the register at `2ec489d1e`, which records
  `minimal_polynomial: null` at each count, and with Evan Daniel’s `EXACT_FORMS.md` at
  evand/square-packing `659ee62`, which lists each as open.
- **Method.** For each count: read the record packing from evand/square-packing’s atlas
  at `659ee62` (`site/www/data/p/best-<n>.json`); polish it to a local optimum by LP at
  fixed angles and trust-region SLP on the angles; collect the active contacts at
  tolerance $10^{-9}$, with the sign branches of each $|\cos|$ and $|\sin|$; solve the KKT
  system for every coordinate, angle, the side and the multipliers by minimum-norm
  Newton; find the polynomial by LLL at 1,500 digits; and re-solve independently at 3,000
  digits.
- **Checks.** At 3,000 digits $|P(s)|$ is about $10^{-3000}$ at all five counts and the
  KKT residuals $10^{-3001}$ to $10^{-3011}$; a start perturbed by $10^{-9}$ gives the
  same side; SymPy finds each polynomial irreducible. `verify_exact_forms.py` reruns
  the pipeline from the atlas files at a chosen precision.
- **What the checkers share.** “Everything here is one code base by one author”: the
  1,500- and 3,000-digit runs share the active-set extraction and the KKT formulation.
- **Not done.** No exact or interval certificate; no proof that the active set and sign
  branches are right; the multipliers are not unique, and in the minimum-norm solution
  the least is about $-6 \times 10^{-16}$, with nonnegativity found by NNLS at double
  precision and not certified. “These are exact values of the record sides, i.e. upper
  bounds only, not optimality claims.”
- **At 126** the issue says $15/2 + 3\sqrt{2}$ lies about $1.2 \times 10^{-22}$ below the
  verified bound $11742640687119285146522492579501/10^{30}$. Decided exactly here, the
  gap is $1.174 \times 10^{-19}$; that bound is the side times $1 + 10^{-20}$, as at 88 and
  199. The author withdrew that paragraph at 07:22:16Z, conceding the sides at 88, 126 and
  199 to Daniel’s T-193.
- **Negative searches.** No relation of degree up to 80 at 55, 130 and 179, and none up to
  70 at 110, 131, 132, 155, 156, 180 to 182, 208 to 211, 228 and 235 to 241; at 105 the
  KKT iteration did not converge, and at 154, 270 and 303 the atlas lagged the register.
  They state no bound and are not recorded.
- **Novelty.** The issue calls the method, KKT closure and then LLL, new as far as the
  author knows. Daniel’s `exactsolve.py`, which the record vendors and whose output T-098
  registers, already solves the KKT system on the load-bearing contacts at high precision
  and searches for an integer relation, so the record credits the values, not the method.

[acquisition/issue-804.json](acquisition/issue-804.json) keeps the issue as read.

## Custody

The issue and the archive state no licence. This packet follows the derived-only rule the
amundsk-n303 packet followed for #755 before its author’s CC0 dedication, and the one
Darius Muglich’s and SQUISH’s attachments followed: it keeps an exact fact derived from
the archive and the archive’s address and digests, and no byte of the archive.
`devtools.acquire_source` keeps only Git checkouts, and an attachment has none.

- [facts/exact-forms.json](facts/exact-forms.json): each count’s polynomial and the
  100-digit side the source prints, read from `exact_forms.json` as JSON data.
- [acquisition/sources.json](acquisition/sources.json): the attachment’s address, size
  and SHA-256 with `raw_asset_retained: false`; the path, size and SHA-256 of each of the
  seven members; and the five inputs the source read, pinned by Git blob, size and
  SHA-256 at evand/square-packing `659ee62`, where each was last changed at `122d0ba` on
  10 October. Those inputs are MIT-licensed upstream and pinned only.
- [acquisition/issue-804.json](acquisition/issue-804.json): the issue as read.

`exact_forms.json` has SHA-256
`531e7077b3242aa56e959031824fb435693deaf8d73f7e33016d49c9e1709202`.
The five Python files of the archive are pinned by digest and were never run or opened as
code. The acknowledgement on the issue asks whether the author will dedicate the archive
to the public domain or license it; with an answer, the files would join this packet.

## What Was Checked Here

`review/exact_forms.py` in the
[ledger for issue 804](../../../campaign/issue-intake/upper-bounds-issue804-20261025/README.md)
derives the fact from the archive (`derive`), decides each side offline (`sides`) and
measures the atlas inputs (`poses`). Its receipts are that directory’s `exact-sides.json`
and `atlas-poses.json`.

- **Irreducibility, twice.** Each polynomial is primitive and irreducible over Q by
  SymPy’s `factor_list` and again by `sqpack.field`, through
  `devtools.exact_sides.algebraic`.
- **The root.** Sturm counts give the real roots and the root each printed side names,
  narrowed by exact bisection below $10^{-130}$; each print lies within $10^{-99}$ of its
  root.
- **The order.** Decided exactly against each case’s verified upper bound and against
  Daniel’s #639 side at the count:

| n | Below the case’s verified bound by | Against Daniel’s #639 side |
| ---: | --- | --- |
| 88 | $9.882 \times 10^{-20}$ (T-127) | the same polynomial and root (T-193) |
| 126 | $1.174 \times 10^{-19}$ (T-139) | the same (T-193) |
| 172 | $3.898 \times 10^{-89}$ (T-174) | below it by $1.185 \times 10^{-62}$; Daniel’s has degree 12 |
| 199 | $1.462 \times 10^{-19}$ (T-127) | the same (T-193) |
| 263 | $2.126 \times 10^{-94}$ (T-174) | below it by $9.234 \times 10^{-63}$; Daniel’s has degree 12 |

At 172 and 263 the ledger records the sides in report order; no other open report
states a bound there below T-174. At 88, 126 and 199 the side is the one T-193 has
registered at V3/C3 since 16 October, decided there with Daniel’s exact configurations,
so #804 is a second derivation of values the record holds, by an independent numerical
route, and no entry records it, as #639’s side at 51 was not recorded.

## Pose by Pose

`poses` pairs the squares of each atlas file the source read with the record’s witness at
its count, under the box symmetry that makes the largest move least:

| n | Witness | Largest move | Squares moved beyond $10^{-6}$ | Largest turn |
| ---: | --- | --- | ---: | --- |
| 88 | `W-known-best-n088` | 0.150 | 37 | 4.76° |
| 126 | `W-known-best-n126` | 0.137 | 65 | 28.45° |
| 172 | `W-known-best-n172` | 0 | 0 | $7 \times 10^{-15}$° |
| 199 | `W-known-best-n199` | 0.611 | 94 | 4.05° |
| 263 | `W-known-best-n263` | 0 | 0 | $7 \times 10^{-15}$° |

At 172 and 263 the input is T-174’s witness to binary64 at every square, so the source
solved T-174’s packing there. At 88, 126 and 199 the atlas holds other poses at the same
side; the value is T-193’s either way. A measurement, which decides nothing.

## What Is Not Established

- **Feasibility at the stated root.** The issue supplied no exact configuration at 172
  or 263, so $s(172) \le S^*$ and $s(263) \le S^*$ are reported, not shown. What would
  show them is a configuration with every centre and half-angle tangent in a number field
  holding $S^*$, every contact an identity there and every other pair and wall separated
  exactly. On 25 October at 09:06:23Z the author attached configurations he reports to be
  of this kind; they are kept in the
  [configurations packet](../hyukdongkim-t244-configurations-2026-10-25/README.md) and
  not yet decided here. Deciding them on this repository’s two exact routes is
  think-4rzl’s.
- **Stationarity and local minimality.** The multipliers are not unique, the least is
  about $-6 \times 10^{-16}$, and no second-order condition was checked, so nothing is
  recorded about either.
- **The negative searches and the solve** were not reproduced, and none of the source’s
  code ran here.
- **Why Daniel’s #639 forms at 172 and 263 sit above these sides** is not established.

## Credit

The issue credits the packings as the case records do: Francisco Couzo’s at 172, as Evan
Daniel and PingYou Ltd improved it, and Nate Chaoweeraprasit’s (itsnaka) at 263, as
Evan Daniel and PingYou Ltd improved it (T-174). Hyukdong Kim is credited with each exact
side, after the packing’s finders. The issue reads the record from this repository’s case
records and Daniel’s atlas, so the bibliography credit is
`Kim after Couzo, Chaoweeraprasit, Daniel, PingYou Ltd, Levy`.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py derive --archive ZIP --check
uv run --frozen --all-extras --group dev python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py sides --check
uv run --frozen --all-extras --group dev python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py poses --atlas DIR --check
```

`derive` refuses an archive without the issue’s SHA-256 and the measured size, and
`poses` an input without its pinned blob and digest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
