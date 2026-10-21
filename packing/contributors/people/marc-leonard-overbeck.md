---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: marc-leonard-overbeck
  display_name: Marc Leonard Overbeck
  surname: Overbeck
  real_name: Marc Leonard Overbeck
  aliases: [Overbeck, Kleddamag, '@kleddamag']
  links:
    - kind: github
      url: https://github.com/Kleddamag
      handle: Kleddamag
    - kind: twitter
      url: https://x.com/kleddamag
      handle: kleddamag
  sources:
    - id: citation-cff
      url: https://github.com/Kleddamag/the-seventeenth-square-candidate/blob/653b9589d0f8a152f01adc56b1d48ba53d49abc3/CITATION.cff
      locator: 'authors gives given-names Marc Leonard, family-names Overbeck and ORCID 0009-0008-8607-8197; repository-code is github.com/Kleddamag/the-seventeenth-square-candidate.'
    - id: candidate-edition
      url: https://github.com/Kleddamag/the-seventeenth-square-candidate/blob/653b9589d0f8a152f01adc56b1d48ba53d49abc3/README.md
      locator: 'Byline and opening paragraphs: the 12 October 2026 verification edition of a candidate proof that the side of John Bidwell’s 1998 packing of seventeen squares is optimal.'
    - id: owner-confirmation
      archive_path: attribution.md
      locator: 'Decisions and Exceptions, the Marc Leonard Overbeck row: the owner’s instruction to credit his name and link his GitHub and X accounts.'
    - id: primary-byline
      archive_path: packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/AUTHORS.md
      locator: 'Human direction and AI contribution section explicitly names Kleddamag as maintainer.'
    - id: github-repository
      archive_path: packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/README.md
      locator: 'Source row: https://github.com/Kleddamag/17-squares-certified-bound.'
    - id: x-account
      archive_path: packing/resources/web/external-square-certificates-2026-09-22/acquisition/x-kleddamag.txt
      url: https://x.com/kleddamag
      locator: 'Author profile https://x.com/kleddamag; the 22 September 2026 thread announces his lower bound 3.875 for eleven squares.'
    - id: n17-bound
      archive_path: packing/resources/web/n17-kleddamag-466001-2026-09-27/README.md
      locator: 'Title and opening paragraph: the exact lower bound 4.66001 for seventeen squares, retrieved 2026-09-27.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /surname
      sources: [citation-cff, owner-confirmation]
    - field: /display_name
      sources: [citation-cff, owner-confirmation]
    - field: /real_name
      sources: [citation-cff, owner-confirmation]
    - field: /aliases/0
      sources: [citation-cff, owner-confirmation]
    - field: /aliases/1
      sources: [primary-byline, bibliography]
    - field: /aliases/2
      sources: [x-account]
    - field: /links/0
      sources: [github-repository, citation-cff]
    - field: /links/1
      sources: [x-account, owner-confirmation]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
