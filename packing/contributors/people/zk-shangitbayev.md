---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: zk-shangitbayev
  display_name: Z.K. Shangitbayev
  surname: Shangitbayev
  aliases:
  - Shangitbayev
  sources:
  - id: paper-byline
    archive_path: packing/resources/papers/arslanov-improved-packings-n-n-1.raw.md
    url: https://doi.org/10.37236/8586
    locator: Title-page author byline reads Z.K. Shangitbayev; the article was published November
      5, 2021.
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names explicitly maps Z.K. Shangitbayev to Shangitbayev.
  provenance:
  - field: /display_name
    sources:
    - paper-byline
    - bibliography
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
