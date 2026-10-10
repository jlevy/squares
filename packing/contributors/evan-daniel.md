---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: evan-daniel
  display_name: Evan Daniel
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
      locator: Readable write-ups and the Square Packing Atlas link in the opening paragraphs.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: credited_names maps Evan Daniel to Daniel.
  provenance:
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
  bio_sources: [intake-credit, repository-writeups]
---
Evan Daniel’s square-packing repository contains exact lower-bound certificates for unit
squares and accompanying write-ups.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
