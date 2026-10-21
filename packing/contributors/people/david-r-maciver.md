---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: david-r-maciver
  display_name: David R. MacIver
  surname: MacIver
  real_name: David R. MacIver
  aliases: [MacIver, David MacIver, DRMacIver]
  links:
    - kind: github
      url: https://github.com/DRMacIver
      handle: DRMacIver
  sources:
    - id: title-page
      archive_path: packing/resources/web/maciver-square-packing-2026-09-07/maciver-2026-seventeen-unit-squares-lower-bound.raw.md
      url: https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/s17-lower-bound/paper.pdf
      locator: 'Title page: the byline “David R. MacIver” and the date 8 August 2026; the abstract states that the paper “was produced with a mix of ChatGPT and Claude Fable and has not yet been adequately human reviewed”.'
    - id: packet
      archive_path: packing/resources/web/maciver-square-packing-2026-09-07/README.md
      url: https://drmaciver.github.io/square-packing-research/
      locator: 'Opening paragraph: David R. MacIver’s Square Packing Research, three author-hosted manuscripts and Lean source at commit 9e2cd59 of DRMacIver/square-packing-research. Papers and Dates: “All three title pages name David R. MacIver.”'
    - id: github-repository
      archive_path: packing/resources/web/maciver-square-packing-2026-09-07/source-commit.json
      url: https://github.com/DRMacIver/square-packing-research/commit/9e2cd597047e040a63b7dcd103e79962cfc2d781
      locator: 'The commit response for DRMacIver/square-packing-research at 9e2cd597, dated 2026-08-10.'
    - id: fitzharding-credit
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/sq17-lean/README.md
      locator: 'Credits: “David MacIver''s earlier Lean work concerns a lower bound for seventeen squares”, linking github.com/DRMacIver/square-packing-research.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [wand125 Green DS7 Theorem 9 2026-10-02] and [Fitzharding n17 Lean 2026] credits name MacIver.'
  provenance:
    - field: /surname
      sources: [packet, bibliography]
    - field: /display_name
      sources: [title-page, packet]
    - field: /real_name
      sources: [title-page, packet]
    - field: /aliases/0
      sources: [packet, bibliography]
    - field: /aliases/1
      sources: [packet, fitzharding-credit]
    - field: /aliases/2
      sources: [github-repository, packet]
    - field: /links/0
      sources: [github-repository, packet, fitzharding-credit]
  bio_sources: [packet, title-page]
---
David R. MacIver wrote the Square Packing Research manuscripts on geometric bounds and
counting methods, with accompanying Lean source.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
