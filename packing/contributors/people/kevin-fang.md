---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: kevin-fang
  display_name: Kevin Fang
  surname: Fang
  real_name: Kevin Fang
  aliases: [Fang, TheSnakeFang]
  links:
    - kind: github
      url: https://github.com/TheSnakeFang
      handle: TheSnakeFang
  sources:
    - id: source-intake
      archive_path: packing/resources/web/fang-two-wedge-certificates-2026-10-10/README.md
      locator: Retained source and credit evidence for [Fang two-wedge certificates 2026-10-10], including repository account TheSnakeFang.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Fang two-wedge certificates 2026-10-10] records the author credit Fang. credited_names maps Kevin Fang to Fang.'
  provenance:
    - field: /display_name
      sources: [bibliography, source-intake]
    - field: /real_name
      sources: [bibliography, source-intake]
    - field: /surname
      sources: [bibliography]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [source-intake]
    - field: /links/0
      sources: [source-intake]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
