---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: martin-gardner
  display_name: Martin Gardner
  surname: Gardner
  real_name: Martin Gardner
  aliases: [Gardner]
  sources:
    - id: stromquist-memo-iii
      archive_path: packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf
      url: https://www.walterstromquist.com/papers/squares3.pdf
      locator: 'Page 3 names Martin Gardner as the author of Scientific American columns publishing packing improvements in October and November 1979 and March and November 1980, with reference [d]; page 13, reference [d], names Mathematical Games by M. Gardner for those dates.'
  provenance:
    - field: /display_name
      sources: [stromquist-memo-iii]
    - field: /surname
      sources: [stromquist-memo-iii]
    - field: /real_name
      sources: [stromquist-memo-iii]
    - field: /aliases/0
      sources: [stromquist-memo-iii]
  bio_sources: [stromquist-memo-iii]
---
Martin Gardner reported square-packing constructions in his *Mathematical Games* columns
in *Scientific American*, as cited in Walter Stromquist’s 1984
[memorandum](https://www.walterstromquist.com/papers/squares3.pdf), pages 3 and 13.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
