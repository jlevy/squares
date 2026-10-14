# External Square-Certificate Sources Retrieved 2026-09-22

This packet retains the public source behind two September 22 lower-bound announcements
and the repositories needed to interpret their provenance.
Retention registers the claims for review; it does not accept a certificate or move a
Frontier bound.

The acquisition manifest is [`acquisition/sources.json`](acquisition/sources.json).
It pins every Git commit and tree, records branch, tag, release, license, submodule and
Git LFS scope, and points to a sorted SHA-256 list for each retained tree.
The social-source captures are
[`acquisition/x-kleddamag.txt`](acquisition/x-kleddamag.txt) and
[`acquisition/x-tokoharu.txt`](acquisition/x-tokoharu.txt); their attached images are
retained beside them.

Overbeck’s two posts announcing `s(11) > 31/8` were captured again on 13 October 2026, as
JSON from X’s syndication endpoint, the form the
[n = 11 formalization packet](../queuingtheorydotcom-n11-lean-2026-10-06/README.md)
keeps its announcements in:

| Post | Account | Created | Retrieved | Receipt |
| --- | --- | --- | --- | --- |
| 1/2, `2102358756591907112` | @kleddamag, account 1496776810767519746, displayed as “Marc Leonard Overbeck” | 2026-09-22T11:26:02Z | 2026-10-13T17:52:09Z | [`acquisition/tweet-2102358756591907112.json`](acquisition/tweet-2102358756591907112.json) |
| 2/2, `2102358760471564308`, a reply to 1/2 | the same | 2026-09-22T11:26:03Z | 2026-10-13T17:52:11Z | [`acquisition/tweet-2102358760471564308.json`](acquisition/tweet-2102358760471564308.json) |

Their text and times are those of [`social-transcripts.md`](social-transcripts.md) and
the September capture, with the “1/2” and “2/2” markers the transcript keeps, and the
second post’s link expands to `https://github.com/Kleddamag/11-squares-certified-bound`.
`acquisition/sources.json` lists both under `social_sources`, after the September
captures, with each one’s size, SHA-256 and retrieval time.

## Retained Repositories

| Source | Revision | Retention | Public claims relevant here |
| --- | --- | --- | --- |
| [`tokoharu-density/`](tokoharu-density/) | `b543990f7794b8c511cb46cf3854b7e8166c3674` | complete main tree, 62 files | `s(11) >= 3.81`, `s(26) >= 5.508`, `s(29) >= 5.71` |
| [`kleddamag-11/`](kleddamag-11/) | `6a733f339395c3514f2ab63d8c4aa64cf63c0b5a`, tag `v1.0.2` | complete release tree, 55 files | `s(11) > 31/8 = 3.875` |
| [`wand125-density/`](wand125-density/) | `096294aeb5f8b604df5890beda6cd601d05f4561` | complete default branch, 60 files | the same three density claims as Tokoharu at that revision |
| [`wand125-points/`](wand125-points/) | `1398e42f17f23fe3744bc54425a589fab1f3542c` | complete current main tree, 23 files | ten point-certificate files, including new `n = 53` and `n = 69` claims |
| [`dependencies/guzhou-n17-full/`](dependencies/guzhou-n17-full/) | `32edfd3da78bf80a309398f552b3b602b9c45d6c` | complete tree, 216 files | upstream checker lineage for Kleddamag |

The Tokoharu-pinned predecessor of wand125’s point repository is retained in full under
[`dependencies/wand125-points-tokoharu-pin/`](dependencies/wand125-points-tokoharu-pin/).
The source-distinct R038 checker and its notices are also copied into
[`dependencies/guzhou-r038/`](dependencies/guzhou-r038/) for direct offline replay.

The `wand125/square-packing-density-bounds` default branch is a fork of the Tokoharu
history and contains no later numerical certificate.
Its `add-push-driver` branch adds only `src/push.py` and `tests/test_push.py`; those
branch-only files are retained under
[`dependencies/wand125-density-add-push-driver/`](dependencies/wand125-density-add-push-driver/).
The public repository therefore does not, as retrieved, substantiate the X post’s phrase
“improved further” with a newer bound.

## Release and Repository Scope

All remote branches and tags were fetched for the five cloned repositories.
None uses a Git submodule or contains a Git LFS pointer.
Git LFS itself was unavailable, so the LFS finding comes from inspecting every tracked
file for the pointer signature and every tree for `.gitattributes` rules.

Kleddamag’s `v1.0.2` release has a ZIP and checksum sidecar.
The ZIP SHA-256 is `d134294bf377f4218619a12b19e1baadb01703c51f475a7309869d6785cab8ee`,
matching both GitHub’s asset digest and the sidecar.
Its expanded 55 files are byte-identical to the tracked tree, so the packet records the
release assets in the acquisition manifest and retains one expanded copy.

Each complete source tree was written with `git archive` from the named commit.
This excludes `.git`, replay caches and bytecode while preventing an upstream
working-tree artifact from entering the archive.
The source trees remain byte-identical and are not passed through this repository’s
Markdown formatter.

## Claim Inventory

The current wand125 point repository claims exact lower bounds at `n = 26`, `29`, `39`,
`40`, `53`, `55`, `56`, `69`, `70` and `72`. Its `n = 40` certificate is a generator
cross-check because the same value follows from `n = 39` by monotonicity.
Its own README marks `n = 26` and `n = 29` as superseded by Tokoharu.
The `n = 53` and `n = 69` certificates postdate the Tokoharu-pinned point tree and need
their own Frontier review.

The two X pages were readable without authentication in the in-app browser even though
the text web fetch returned a cache miss.
The retained text files give the exact post and reply URLs, UTC publication times from
first-party Open Graph metadata, visible text, media URLs and local media hashes.

## Review and Verification

The
[integration review](../../../../docs/project/reviews/review-2026-09-22-external-square-certificates-integration.md)
records the mathematical verdicts, verified Frontier updates, reproduced driver defect
and next technical work.
Its two detailed reviews cover the density proof and the n11 threshold proof separately.
Acquisition alone supplies provenance; complete coverage replays and discharged proof
assumptions supply the verified bounds.

The first-party receipts are retained under [`receipts/`](receipts/). The
[n11 instructions](receipts/n11/README.md) and
[point-certificate instructions](receipts/wand125-points/README.md) give reproducible
commands and scope. Density’s complete replay and exact premise audit are in
[`receipts/density/audit.json`](receipts/density/audit.json); later source-binding
controls are recorded separately.
Independent sampled geometry does not count as a second complete coverage method.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
