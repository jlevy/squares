---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: daniil-ostashev
  display_name: Daniil Ostashev
  surname: Ostashev
  real_name: Daniil Ostashev
  aliases: [Ostashev, dostashev]
  links:
    - kind: github
      url: https://github.com/dostashev
      handle: dostashev
  sources:
    - id: source-intake
      archive_path: packing/resources/web/dostashev-records-2026-10-11/README.md
      locator: Retained source and credit evidence for [Ostashev records 2026-10-11], including repository account dostashev.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Ostashev records 2026-10-11] records the author credit Ostashev. credited_names maps Daniil Ostashev to Ostashev.'
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
