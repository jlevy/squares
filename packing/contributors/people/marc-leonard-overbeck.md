---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: marc-leonard-overbeck
  display_name: Marc Leonard Overbeck
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
      archive_path: packing/resources/web/kleddamag-n17-candidate-2026-10-12/README.md
      url: https://github.com/Kleddamag/the-seventeenth-square-candidate/blob/653b9589d0f8a152f01adc56b1d48ba53d49abc3/CITATION.cff
      locator: 'CITATION.cff at 653b958: authors gives given-names Marc Leonard, family-names Overbeck and ORCID 0009-0008-8607-8197; repository-code is github.com/Kleddamag/the-seventeenth-square-candidate. The packet keeps no upstream bytes; its Source and Credit table, Author row, records “Marc Leonard Overbeck (GitHub Kleddamag, ORCID 0009-0008-8607-8197), as README.md and CITATION.cff name him”, and its acquisition/upstream-subtree.sha256 binds CITATION.cff at SHA-256 899e0457883915f6c52144deba9862063cc810cc1e4b5e0f5bc9cd4ad69a9971.'
    - id: candidate-edition
      archive_path: packing/resources/web/kleddamag-n17-candidate-2026-10-12/acquisition/sources.json
      url: https://github.com/Kleddamag/the-seventeenth-square-candidate/blob/653b9589d0f8a152f01adc56b1d48ba53d49abc3/README.md
      locator: 'README.md at 653b958, byline and opening paragraphs: the 12 October 2026 verification edition of a candidate proof that the side of John Bidwell’s 1998 packing of seventeen squares is optimal. The packet keeps no upstream bytes; acquisition/sources.json pins the commit, committed 2026-10-12T14:40:59Z, and its license field records that README.md and CREDITS.md say he conceived and led the project and that AI systems, Codex and Claude, produced the mathematics, engines, certificates, checkers, reviews and text under his direction.'
    - id: candidate-announcement
      archive_path: packing/resources/web/kleddamag-n17-candidate-2026-10-12/receipts/announcement/tweet-2109658579678761429.json
      url: https://x.com/kleddamag/status/2109658579678761429
      locator: 'user.screen_name is kleddamag, user.name is Marc Leonard Overbeck and user.id_str is 1496776810767519746; the post of 2026-10-12T14:52:55Z announces the candidate proof for 17 squares and links github.com/Kleddamag/the-seventeenth-square-candidate.'
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
    - field: /display_name
      sources: [citation-cff, owner-confirmation, candidate-announcement]
    - field: /real_name
      sources: [citation-cff, owner-confirmation]
    - field: /aliases/0
      sources: [citation-cff, owner-confirmation]
    - field: /aliases/1
      sources: [primary-byline, bibliography]
    - field: /aliases/2
      sources: [x-account, candidate-announcement]
    - field: /links/0
      sources: [github-repository, citation-cff]
    - field: /links/1
      sources: [x-account, owner-confirmation, candidate-announcement]
  bio_sources: [x-account, n17-bound, candidate-edition, primary-byline]
---
Marc Leonard Overbeck publishes his square-packing work as Kleddamag on GitHub and as
@kleddamag on X. In September 2026 he released exact computer-assisted lower bounds for
eleven and seventeen unit squares, raising the bound for seventeen to 4.66001. On 12
October 2026 he released the verification edition of a candidate proof that John
Bidwell’s 1998 packing of seventeen squares is optimal.
His releases state that he directed the work and that AI systems carried out the
mathematics, code and certificates.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
