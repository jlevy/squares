# Joost de Winter’s Lower Bounds of 19 November 2026 at 21d944c

This packet retains, from one pin of Joost de Winter’s watched repository
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing), the
material of three reports of raised lower bounds on $s(n)$, all credited “Joost de
Winter, Delft University of Technology, after Hiroaki Hosono”:

- [jlevy/squares#1039](https://github.com/jlevy/squares/issues/1039) (04:49:37Z on 19
  November 2026): 56 counts from 19 to 148, 49 direct and 7 by monotonicity.
- [jlevy/squares#1041](https://github.com/jlevy/squares/issues/1041) (12:05:56Z): 34
  direct bounds from 50 to 137, a follow-up to #1039.
- [jlevy/squares#1042](https://github.com/jlevy/squares/issues/1042) (18:45:38Z): 48
  bounds from 50 to 218, and its comment of 19:59:12Z at 161.

Each certificate is a nonnegative rectangle measure on the board of the claimed side, of
total mass below the count, with a computation that every admissible unit square
captures mass at least one.
The import is lane c15-lower, bead think-fv42.

## Source and Pin

| Field | Value |
| --- | --- |
| Repository | <https://github.com/JoostdeWinter/square-packing> |
| Pin | `21d944c43098e2261ab7d713cd10f02a5eb13f3d`, tree `20b6bca8ac912e1fdb0eb8674ddea8d0e54c1554` |
| Committed | 2026-11-19T18:44:48Z, “Add lower bounds for 48 counts between 50 and 218” |
| Retrieved | 2026-11-20T16:57Z, a partial clone; `git ls-remote` read the head as the pin then and at 17:12Z |
| Scope | `LICENSE`, `README.md`, `lower_bounds_2026_11_19/` (962 files) |
| Licence | MIT, Joost de Winter, by `LICENSE` at the pin |

The pin is the commit #1042 names, 50 seconds before the issue, and the head when read.
It adds `lower_bounds_2026_11_19/` and two lines of the root README.

**The attachments.** #1039 and #1041 each attach a zip, and the session proxy refused
both attachment URLs (HTTP 403), so neither was fetched from the issue.
The folder holds #1039’s attachment at `followup/mass_reserve/lower-bounds-56.zip`, and
its SHA-256, `9641ca15ac63213db22ad32854efb0bc0575d7c0beeb646fd6931f50ae183452`, is the
one #1039 states, so those are the attachment’s bytes.
#1039’s source commit, `e94e6ce65a887f80dd4821454df53c0c18a4ba97`, is not in the public
repository (`git fetch` of it is refused as “not our ref”); the zip carries its raw
commit objects in `.source/`. #1041’s attachment, `squaremath_continued_20261119.zip`
with stated SHA-256 `d8d0d6966f7ac7f9a69f24d578619ee2323a158e5c6c9c7e6be9039c401445df`,
is not in the folder as a zip.
The folder’s top level is that packet’s content as #1041 describes it (34 direct
certificates in `proof/`, `lower_bounds.csv` with #1041’s 34 exact values, the integer
checker, the source measures, `corners/`, `upper/` and `constructions/`), but nothing
here compares it with the attachment’s digest.
#1041’s bytes are therefore retained from the pin, committed 6 hours and 39 minutes
after #1041 was reported.

## What the Reports Claim

The exact values are transcribed, with the report order and the case records’ lanes, in
[`campaign/issue-intake/lower-bounds-de-winter-20261120/`](../../../campaign/issue-intake/lower-bounds-de-winter-20261120/README.md).

| Report | Where the claims are | Certificates |
| --- | --- | --- |
| #1039 | `exact_claims.csv` inside the zip | rectangle, mixed, heterogeneous-core and adaptive-core measures, some with the source’s original direction checks |
| #1041 | `lower_bounds.csv`, `proof/nNNN/` | 34 standalone certificates, kernel `octagon-gram` |
| #1042 | `CLAIM.md`, `followup/best_by_count.csv` | 43 standalone certificates in `followup/lower/`; repeated strips (`followup/repeated/`), four translated regions (`followup/envelopes/`) and corner reweighting (`followup/corner_trim/`) |
| #1042, comment at 161 | the comment’s text | `followup/repeated/161--749858-12.858-100-uniform/proof` with the four-region transfer |

Not claimed by any of them, by `CLAIM.md` and the issues: the 67 corner bounds in
`corners/`, which inherit the global coverage of Hosono’s T-180 measures; the 16
edge-strip refinements of `followup/mass_reserve/`; and the packings in `upper/` and
`followup/upper/`.

## Retained Here

Under `source/`, 346 text files, 1,315,136 bytes, at their upstream paths: the claims
and their comparisons, every manifest, `comparison.json` and `verification.json`, the
proofs (`PROOF.md`, `proof/INTEGER_CHECKER.md`), and every program (`verify.py`,
`proof/*.py`, `proof/*.cpp`, `followup/**/*.py`, `followup/envelopes/envelope.cpp`).
Data files of more than 1,000 lines are stored as deterministic gzip, listed below.

Pinned by SHA-256 only, 618 files and 56,710,055 bytes, each listed in
`acquisition/sources.json` with its reason: the #1039 zip; every gzip measure and
per-direction receipt (about 24 MB, by OR-18); the figures; the 67 corner families; and
the upper-bound witnesses.
A replay that reads them retains or hosts what it reads from this same pin.
`LICENSE` is pinned against its byte-identical copy in the
`de-winter-upper-bounds-227-229-260-2026-10-17` packet.
`acquisition/upstream-subtree.sha256` lists all 964 files of the scope.

No program of the source ran in writing this packet.

## Credit and AI Assistance

The three issues credit “Joost de Winter, Delft University of Technology, after Hiroaki
Hosono”: Hosono constructed the source measures, and the reweighted measures and the
integer checker are de Winter’s, from #1039 and T-327. #1039 says GPT6.2 Astra helped
develop the constructions, perform the computations and prepare the certificates and the
report.
#1041 says OpenAI GPT-6.2 Astra carried out the numerical search, the derivations
and the certificate construction under his direction.
#1042 says GPT6.2 Astra was the AI author for the numerical search, derivations and
certificate construction under his direction, and its comment of 20:17:20Z says “OpenAI
Codes should be ‘GPT 6.2 Astra’”, which reads as a correction of the folder’s README,
which names Codex. The folder’s `notices/` carries Hosono’s MIT notice and this
repository’s licence.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/lower_bounds_2026_11_19/corners/comparisons.json.gz` | upstream | `4c6b3c5b4d7cf946bcf48d47d3ca34d20a93212c` | `00e725b9268f53093e6db397ab9b5bd86be48ef05bf467f21108162cd1c07ccf` |
| `source/lower_bounds_2026_11_19/corners/intervals.json.gz` | upstream | `cc99b15b4bb3c853baf371c7bb99b8a120daca73` | `a91b0b49988bc5bf8977d1e9f61e2930e2cb1be136bd4ff3140b5ee263591c0c` |
| `source/lower_bounds_2026_11_19/followup/comparisons/inputs/prior56/attribution/registry_lower_intervals.json.gz` | upstream | `9065b65959173ecff197f2f34c7cc6989b081d29` | `82510c9c37e6b5d21cb614e3757575df4cd8bb72a2deb0cd812b230b7c3b2ea7` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
