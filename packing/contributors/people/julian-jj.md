---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: julian-jj
  display_name: Julian-JJ
  links:
  - kind: github
    url: https://github.com/Julian-JJ
    handle: Julian-JJ
  sources:
  - id: formalization-acknowledgment
    archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md
    url: https://github.com/Queuingtheorydotcom/11SquaresFormalized/blob/cdc746ed907d258057c283aeb6d077cb2c27e349/ACKNOWLEDGEMENTS.md
    locator: Line 8 names @Julian-JJ, links the GitHub account, and calls the account a collaborator who worked
      on running the proof on an HPC cluster. No real name is asserted.
  provenance:
  - field: /display_name
    sources:
    - formalization-acknowledgment
  - field: /links
    sources:
    - formalization-acknowledgment
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
