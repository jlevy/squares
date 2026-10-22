---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: hiroaki-hosono
  display_name: Hiroaki Hosono
  surname: Hosono
  real_name: Hiroaki Hosono
  aliases: [Hosono, wand125, '@wand_125']
  links:
    - kind: github
      url: https://github.com/wand125
      handle: wand125
    - kind: twitter
      url: https://x.com/wand_125
      handle: wand_125
  sources:
    - id: commit-author
      archive_path: packing/resources/web/wand125-linear-n122-2026-10-10/README.md
      locator: 'Credit: “The source credits wand125; the commit is authored by Hiroaki Hosono.”'
    - id: source-manifest
      archive_path: packing/resources/web/wand125-linear-n122-2026-10-10/source-manifest.json
      locator: 'attribution.credit is “wand125 (commit author Hiroaki Hosono)”.'
    - id: github-profile
      url: https://github.com/wand125
      locator: 'The GitHub account wand125 gives its name as Hiroaki Hosono (read 2026-10-13).'
    - id: owner-confirmation
      archive_path: attribution.md
      locator: 'Decisions and Exceptions, the Hiroaki Hosono row: the owner’s instruction to credit his name and keep his GitHub and X handles.'
    - id: x-messages
      archive_path: packing/resources/web/wand125-x-update-2026-09-28/README.md
      locator: 'Opening paragraph: three messages from wand125 (X: @wand_125, GitHub: wand125) to the project owner, 28 and 29 September 2026.'
    - id: primary-byline
      archive_path: packing/resources/web/wand125-valid7-independent-check-2026-10-06/valid7-independent-check/LICENSE
      locator: 'Copyright (c) 2026 wand125.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source authors and credits print Hosono; the bibliography keys keep the handle wand125, and the notes name Hiroaki Hosono as commit author.'
  provenance:
    - field: /surname
      sources: [owner-confirmation, bibliography]
    - field: /display_name
      sources: [commit-author, github-profile, owner-confirmation]
    - field: /real_name
      sources: [commit-author, source-manifest, github-profile]
    - field: /aliases/0
      sources: [owner-confirmation, bibliography]
    - field: /aliases/1
      sources: [primary-byline, x-messages]
    - field: /aliases/2
      sources: [x-messages]
    - field: /links/0
      sources: [x-messages, github-profile]
    - field: /links/1
      sources: [x-messages, owner-confirmation]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
