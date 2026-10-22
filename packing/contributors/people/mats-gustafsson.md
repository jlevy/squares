---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: mats-gustafsson
  display_name: Mats Gustafsson
  surname: Gustafsson
  real_name: Mats Gustafsson
  aliases: [Gustafsson]
  sources:
    - id: stromquist-memo-iii
      archive_path: packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf
      url: https://www.walterstromquist.com/papers/squares3.pdf
      locator: 'Page 3 names Mats Gustafsson and Magnus Thulin as discoverers of the eleven-square packing of side approximately 3.877; page 2, Table 1, credits Gustafsson & Thulin for n = 11 and refers to the November 1980 Mathematical Games column.'
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
Walter Stromquist’s 1984
[memorandum](https://www.walterstromquist.com/papers/squares3.pdf) credits Mats
Gustafsson and Magnus Thulin with an eleven-square packing of side approximately 3.877.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
