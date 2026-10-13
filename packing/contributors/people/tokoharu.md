---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: tokoharu
  display_name: 'Tokoharu'
  aliases: ['tokoharu']
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/LICENSE
      locator: 'Copyright (c) 2026 tokoharu; bibliography uses Tokoharu.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /display_name
      sources: [primary-byline]
    - field: /aliases
      sources: [primary-byline, bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
