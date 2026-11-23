# n = 20: source custody and bounded corroboration for #1055

This preparation packet confirms the source bytes and several local steps in Joost de
Winter’s equal-absolute-tilt argument.
It does not accept the unrestricted lower bounds 4.95 or 4.99755, or the restricted
minimum of 5. The public record is unchanged.

The source is
[comment 7058955337](https://github.com/jlevy/squares/issues/1055#issuecomment-7058955337),
with archive `attachments/n20-proof-499755.zip` pinned to
`dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc` in
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc).
The downloaded mirror has 1,425,895 bytes and SHA-256
`475d7ef50e21ce4a83cfb4c8415c9e9852d619beeade5c4c8745c2c963d6c867`. The attachment URL
is recorded, but was not fetched separately to compare its bytes.

[The custody check](receipts/custody.json) passed all 660 archive manifest entries, all
20 embedded Mira-Cult Git blob identities, and all eight entries in the original 4.95
source manifest at `3a5130340b0882e72e9d04ad2419b0437cae99aa/lower_n20`. The archive has
661 files, including `SHA256SUMS`.
[The member inventory](acquisition/archive-members.json.gz) pins the submitted programs
without retaining them in this packet.

[The first-party check](receipts/small-angle.json) independently recomputed:

- 117 polynomial certificate identities, cancellation of all center variables,
  nonnegative multipliers, and strictly positive margins for `0 < t <= 1/24`;
- 992 one-diagonal chain/sign cases over that whole rational interval;
- the bridge counts for all 120 vacancy permutations: 92 have four bridges, 24 have
  five, and four have six;
- rational constants needed for the rank cells and forward separating normals.

Two deliberately corrupted certificates were rejected.
These computations took 5.598457 seconds.
They do not check that all feasible sign assignments and separation graphs are
represented, or that the graph-to-certificate lookup covers them.

See [the mathematical review](review.md) for the inequalities, limitations and next
checks, and [the dependency map](dependencies.json) for concrete source commands.
The source’s saved counts in `source/` remain author-reported receipts.

## Reproduce the bounded checks

Use Python 3.14 with assertions enabled.
The checkers use only the standard library, never import submitted programs, and impose
a 120-second alarm. Output paths must be new files.
From this packet directory:

```bash
"$PYTHON" programs/check_small_angle.py --output "$OUT/small-angle.json"
"$PYTHON" programs/check_custody.py "$ARCHIVE" \
  --original "$ORIGINAL_LOWER_N20" --output "$OUT/custody.json"
```

`ARCHIVE` is the pinned ZIP; `ORIGINAL_LOWER_N20` is optional and denotes the original
4.95 source directory.
Use a dedicated observe-only memory guard for a replay.
The recorded guard observed 9.2 seconds, four samples, peak process-tree footprint 0.02
GiB, normal pressure throughout and no interventions.
No submitted code, solver, compiler, or exhaustive proof replay was run in this slice.

## Attribution and retention

Research direction: Joost de Winter, TU Delft.
The submitter identifies GPT6.2 Astra as the AI author.
The marks derive from Wolfram Bentz; earlier exact geometry derives from Mira Cult at
`78bec6aacebf304d942a9225e16c2f18165778ff`.

The pinned repository’s [MIT notice](source/LICENSE) names Joost de Winter, 2026. The
ZIP itself has no license member.
The scope for the embedded Mira-Cult programs has not been established; the repository’s
MIT notice is not treated as a grant from that upstream author.
This packet retains only mathematical coefficient data, factual receipts, source
identities and attribution/notice, together with our first-party checkers and review.
The full ZIP is private audit evidence outside the portable packet.

[The manifest](acquisition/manifest.json) distinguishes retained data from pinned source
and records both source commits.
This is a direct-source corroboration after reading the submission and an earlier
reduction review, not a blind proof review.
Tracker context is `think-6ul3` for 4.95 and `think-guls` for the follow-up; neither was
modified.

## Compressed Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `acquisition/archive-members.json.gz` | receipt | `bf693f1ffe981917724e03f53ed5b236053f6223` | `ecd4093ea60f982009919478f25b32b3e56b82ded1bc59fe300dd5d87d4f339d` |
| `review-one-axis-bank/checker-receipt.json.gz` | receipt | `b72348118152f100e3adb3cb4fffd114af4eae83` | `5f8ca1a560ef390078f9938bc98ac63af1efec0cf0be43481dd60628a7598f4c` |
| `review-one-axis-bridges/bridge-verification.json.gz` | receipt | `69f62be84b71b713500296344d8a6f8c629d8ccc` | `a8b48b5cff9b0b101174e3eb513bb3ed502c05bbfb825e1f8b376fb0c017d286` |
| `review-one-axis-sign-census/sign-census.json.gz` | receipt | `ddda8efa9ec50b03d75cf444dcacc6547642dd93` | `45d16648622df9321d4ca3105bf3b2014b049e3774f3b89b3955fbd8ddd4654a` |
| `review-one-axis-sign-census/sign-census-isolated.json.gz` | receipt | `3cd64b80b74221bfbd0302d5b1ac5af3ef1033a0` | `fc75c5853c16cc99e3cbdda6661ddcfb5a0d6d2b0698c47c9f7747351ccd96fe` |
| `review-one-axis-general-paths/general-path-catalogue.json.gz` | receipt | `ed24a599b04023febdd50708c7b584fb7f326a9c` | `a60f45a70cb57d4e1a1e58bcbe01b1f9cf1c527fc80c0e931d7e856af22b33bb` |

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/equal_tilt_through_24.json.gz` | upstream | `83a746a504c71501682bc81769f3665a2d895c6e` | `009441b65a3364e5f2abc5736a07dc46632dfba32b03d880780fb7c6849e238f` |
| `review-one-axis-bank/one_axis_24.json.gz` | upstream | `69cdbf53f097cc89cb136adca3bb4bb81a71ccfc` | `451b1116cf5b6eaa78ecc8233ee4e4c931537e6dfd3bd4fba2a6d91b1922d257` |

The [independent one-axis polynomial-bank review](review-one-axis-bank/README.md) accepts
576 conditional certificates. The [independent bridge review](review-one-axis-bridges/README.md)
now excludes all 3,488 positive-cost local profiles through 15,696 normal choices.
The [independent sign and symmetry census](review-one-axis-sign-census/README.md)
now checks all 2,400 vacancy/aligned-position cases, retains 29,368 assignments and
verifies their 3,671 D4 orbits. The [general-path review](review-one-axis-general-paths/README.md)
classifies all 29,008 local profiles: 23,286 are excluded and 5,722 are not certified.
Application to global paths, separation-graph enumeration, rule extraction and
graph-to-certificate coverage remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
