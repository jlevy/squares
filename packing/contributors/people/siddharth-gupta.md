---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: siddharth-gupta
  display_name: Siddharth Gupta
  surname: Gupta
  real_name: Siddharth Gupta
  aliases: [Gupta, SidG2k1]
  links:
    - kind: github
      url: https://github.com/SidG2k1
      handle: SidG2k1
  sources:
    - id: source-intake
      archive_path: packing/resources/web/gupta-square-packing-refinements-2026-10-08/README.md
      locator: Retained source and credit evidence for [Gupta rational refinements 2026-10-08], including repository account SidG2k1.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Gupta rational refinements 2026-10-08] records the author credit Gupta. credited_names maps Siddharth Gupta to Gupta.'
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
