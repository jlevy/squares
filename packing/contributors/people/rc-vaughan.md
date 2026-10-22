---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: rc-vaughan
  display_name: R. C. Vaughan
  surname: Vaughan
  aliases:
  - Vaughan
  sources:
  - id: paper-byline
    archive_path: packing/resources/papers/roth-vaughan-1978-inefficiency-packing-squares.pdf
    url: https://www.sciencedirect.com/science/article/pii/0097316578900055
    locator: 'PDF page 1, printed page 170: Inefficiency in Packing Squares with Unit Squares, Journal of Combinatorial
      Theory, Series A 24 (1978), 170–186, by K. F. Roth and R. C. Vaughan. The published initials are retained.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The [squarepacker k2-minus-c 2026] and [squarepacker k2-minus-c v1.2 2026] credit fields print Ryu
      after Roth, Vaughan; their notes identify the Roth and Vaughan (1978) fundamental lemma.
  provenance:
  - field: /display_name
    sources:
    - paper-byline
    - bibliography
  - field: /surname
    sources:
    - paper-byline
    - bibliography
  - field: /aliases
    sources:
    - paper-byline
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
