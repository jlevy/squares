---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: ryan-xu
  display_name: Ryan Xu
  surname: Xu
  real_name: Ryan Xu
  aliases: [Xu, ry-xu, '@small_LM']
  links:
    - kind: github
      url: https://github.com/ry-xu
      handle: ry-xu
    - kind: twitter
      url: https://x.com/small_LM
      handle: small_LM
    - kind: personal
      url: https://ryanxu.net
  sources:
    - id: github-profile
      url: https://github.com/ry-xu
      locator: 'The GitHub account ry-xu gives its name as Ryan Xu, its website as ryanxu.net and its X account as small_LM (read 2026-10-14).'
    - id: owner-confirmation
      archive_path: attribution.md
      locator: 'Decisions and Exceptions, the Ryan Xu row: the owner’s instruction to credit ry-xu by his real name.'
    - id: packet
      archive_path: packing/resources/web/ry-xu-new-packings-2026-10-08/README.md
      url: https://github.com/ry-xu/square_packing/tree/8dc415296f697f5140caea27c7a0193d52deb4e6
      locator: 'Opening paragraphs: the 25 packings of issue #432 from ry-xu/square_packing at 8dc4152; “Credit for the reported constructions belongs to ry-xu. The source describes an LLM-assisted search and certificate workflow.”'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source authors and credits print Xu; the [ry-xu square packing 2026] key keeps the handle. The later credits that build on his issue #432 packings name Xu, and their notes call those packings Ryan Xu’s ([Deleeuw n70 refinement 2026-10-10], [SQUISH third request 2026-10-09], [Ostashev records 2026-10-11]).'
  provenance:
    - field: /surname
      sources: [bibliography, owner-confirmation]
    - field: /display_name
      sources: [github-profile, owner-confirmation]
    - field: /real_name
      sources: [github-profile, owner-confirmation]
    - field: /aliases/0
      sources: [bibliography, owner-confirmation]
    - field: /aliases/1
      sources: [packet, github-profile]
    - field: /aliases/2
      sources: [github-profile]
    - field: /links/0
      sources: [github-profile, packet]
    - field: /links/1
      sources: [github-profile]
    - field: /links/2
      sources: [github-profile]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
