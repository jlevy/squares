---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: griffin-casson
  display_name: Griffin Casson
  surname: Casson
  real_name: Griffin Casson
  aliases: [Casson, griffcass]
  links:
    - kind: github
      url: https://github.com/griffcass
      handle: griffcass
  sources:
    - id: source-intake
      archive_path: packing/resources/web/casson-square-packing-2026-09-23/README.md
      locator: Retained source and credit evidence for [griffcass square-packing 2026-09-23], including repository account griffcass.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[griffcass square-packing 2026-09-23] records the author credit Casson. credited_names maps Griffin Casson to Casson.'
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
