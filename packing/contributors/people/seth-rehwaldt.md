---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: seth-rehwaldt
  display_name: Seth Rehwaldt
  surname: Rehwaldt
  real_name: Seth Rehwaldt
  aliases: [Rehwaldt, lollipoll]
  links:
    - kind: github
      url: https://github.com/lollipoll
      handle: lollipoll
  sources:
    - id: source-intake
      archive_path: packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/README.md
      locator: Retained source and credit evidence for [Rehwaldt Couzo refinements 2026-10-07], including repository account lollipoll.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Rehwaldt Couzo refinements 2026-10-07] records the author credit Rehwaldt. credited_names maps Seth Rehwaldt to Rehwaldt.'
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
