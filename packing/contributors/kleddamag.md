---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: kleddamag
  display_name: 'Kleddamag'
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/AUTHORS.md
      locator: 'Human direction and AI contribution section explicitly names Kleddamag as maintainer.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /display_name
      sources: [primary-byline]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
