---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: trevor-green
  display_name: Trevor Green
  surname: Green
  real_name: Trevor Green
  aliases:
  - Green
  sources:
  - id: survey-credit
    archive_path: packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
    url: https://erich-friedman.github.io/papers/squares/squares.html
    locator: The Introduction names Trevor Green as the sender of an unpublished proof; the lower-bound section
      names Trevor Green immediately before Theorem 9, and the lower-bound table prints Green. These are credits
      in Friedman’s survey, not authorship of the survey.
  provenance:
  - field: /display_name
    sources:
    - survey-credit
  - field: /surname
    sources:
    - survey-credit
  - field: /real_name
    sources:
    - survey-credit
  - field: /aliases
    sources:
    - survey-credit
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
