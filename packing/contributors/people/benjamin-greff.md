---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: benjamin-greff
  display_name: Benjamin Greff
  surname: Greff
  real_name: Benjamin Greff
  aliases: [Greff, bengreff]
  links:
    - kind: github
      url: https://github.com/bengreff
      handle: bengreff
  sources:
    - id: source-intake
      archive_path: packing/resources/web/bengreff-s76-certificate-2026-10-14/README.md
      locator: Retained source and credit evidence for [bengreff s76 certificate 2026-10-14], including repository account bengreff.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[bengreff s76 certificate 2026-10-14] records the author credit Greff. credited_names maps Benjamin Greff to Greff.'
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
