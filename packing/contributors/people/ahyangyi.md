---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: ahyangyi
  display_name: ahyangyi
  links:
    - kind: github
      url: https://github.com/ahyangyi
      handle: ahyangyi
  sources:
    - id: project-catalogue
      archive_path: packing/devtools/overview_sections.py
      locator: OTHER_PROJECTS credits the repository https://github.com/ahyangyi/17squares to the public handle ahyangyi.
  provenance:
    - field: /display_name
      sources: [project-catalogue]
    - field: /links/0
      sources: [project-catalogue]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
