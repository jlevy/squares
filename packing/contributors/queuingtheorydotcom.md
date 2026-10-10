---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: queuingtheorydotcom
  display_name: 'Queuingtheorydotcom'
  aliases: ['Ahmed']
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md
      locator: 'Acknowledgements names @Queuingtheorydotcom for the underlying proof and integration; bibliography explicitly identifies its Ahmed attribution.'
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
