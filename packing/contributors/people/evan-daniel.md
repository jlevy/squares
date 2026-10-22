---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: evan-daniel
  display_name: Evan Daniel
  surname: Daniel
  real_name: Evan Daniel
  aliases: [Daniel, evand]
  links:
    - kind: github
      url: https://github.com/evand
      handle: evand
    - kind: publication
      url: https://evand.github.io/square-packing/
  sources:
    - id: repository-license
      archive_path: packing/resources/web/evand-square-packing-2026-09-26/square-packing/LICENSE
      locator: Copyright (c) 2026 Evan Daniel.
    - id: intake-credit
      archive_path: packing/resources/web/evand-square-packing-2026-09-26/README.md
      locator: Title, Provenance table, and Credit, as the source states it.
    - id: repository-writeups
      archive_path: packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/README.md
      locator: 'Readable write-ups for s(11), s(12), s(13), s(21), s(32) and s(45) and the Square Packing Atlas link in the opening paragraphs; the Results list, with each certificate’s date and Lean status.'
    - id: repository-credits
      archive_path: packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/CREDITS.md
      locator: 'Provenance of this work: “Produced by Claude (Anthropic) in a single session under human direction” and “Nothing here has been peer reviewed.”'
    - id: regularized-lists
      archive_path: packing/resources/web/evand-regularized-2026-10-10/README.md
      locator: 'Opening paragraph: display-regularized drawings of the record packings for n = 1 to 324, added in 346c6ed (2026-10-10T18:05:38Z), with exact rational certificates under search/regularize/lists/certs/.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: credited_names maps Evan Daniel to Daniel.
  provenance:
    - field: /surname
      sources: [bibliography]
    - field: /display_name
      sources: [repository-license]
    - field: /real_name
      sources: [repository-license]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [intake-credit]
    - field: /links/0
      sources: [intake-credit]
    - field: /links/1
      sources: [repository-writeups]
  bio_sources: [intake-credit, repository-writeups, repository-credits, regularized-lists]
---
Evan Daniel proves lower bounds for packings of unit squares in a square with exact
weighted covers, beginning with
[s(12) ≥ 15680/3951](https://evand.github.io/square-packing/s12/) in August 2026. In
September 2026 he added proofs of
[s(21) = 5](https://evand.github.io/square-packing/s21/),
[s(32) = 6](https://evand.github.io/square-packing/s32/) and
[s(45) = 7](https://evand.github.io/square-packing/s45/), and a proof of Wolfram Bentz’s
[s(13) = 4](https://evand.github.io/square-packing/s13/) without case analysis; the
proofs for 13 and 32 are also checked in full in Lean.
His repository’s
[credits](https://github.com/evand/square-packing/blob/6aa82ba457e9eaeaaa3af0833600f27f91a2fce3/s12/CREDITS.md)
say this work was produced by Claude (Anthropic) in a single session under human
direction and that none of it has been peer reviewed.
The repository also holds the
[Square Packing Atlas](https://evand.github.io/square-packing/), an explorer for the
record packings, and in October 2026 he added
[regularized drawings](https://github.com/evand/square-packing/tree/ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7/search/regularize)
of the record packings for 1 to 324 squares, with exact rational certificates.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
