---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: rio-calle
  display_name: Rio Calle
  surname: Calle
  real_name: Rio Calle
  aliases: [Calle, riocalle]
  links:
    - kind: github
      url: https://github.com/riocalle
      handle: riocalle
  sources:
    - id: source-intake
      archive_path: packing/resources/web/riocalle-n102-2026-10-12/README.md
      locator: Credit section requests the name Rio Calle; the source packet identifies the riocalle repository and retained n102 report.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Calle n102 2026-10-12] records the author credit Calle. '
  provenance:
    - field: /display_name
      sources: [source-intake]
    - field: /real_name
      sources: [source-intake]
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
