---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: ctjlewis
  display_name: Lewis
  aliases:
  - ctjlewis
  links:
  - kind: github
    url: https://github.com/ctjlewis
    handle: ctjlewis
  - kind: twitter
    url: https://x.com/ctjlewis
    handle: ctjlewis
  sources:
  - id: formalization-acknowledgment
    archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md
    url: https://github.com/Queuingtheorydotcom/11SquaresFormalized/blob/cdc746ed907d258057c283aeb6d077cb2c27e349/ACKNOWLEDGEMENTS.md
    locator: Line 5 names @ctjlewis and links the GitHub account separately from the EvolvingPrograms organization;
      it credits verification infrastructure and replay support.
  - id: public-profile
    url: https://api.github.com/users/ctjlewis
    locator: 'Public GitHub profile checked 2026-10-21: login ctjlewis, name Lewis, type User. Its bio links EvolvingPrograms
      as an affiliation; no fuller name or surname is asserted.'
  - id: announcement-receipt
    archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/announcement/tweet-2107508501610217640.json
    url: https://x.com/ManassehA06/status/2107508501610217640
    locator: entities.user_mentions contains screen_name ctjlewis and display name Lewis followed by a flag emoji;
      the announcement thanks this account for aiding the formalization.
  - id: github-social-crosslink
    url: https://github.com/ctjlewis
    locator: 'Public GitHub profile checked 2026-10-21 directly links twitter.com/ctjlewis; the account handle matches the retained announcement receipt.'
  - id: n12-formalization-credit
    archive_path: packing/resources/web/jatloe-n12-lean-2026-10-16/Jatloe12SquaresFormalized/README.md
    url: https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/blob/d0caf4532a7ead68be1389ef87387b126fc2e0ab/README.md
    locator: 'Credits of the twelve-square formalization: “CTJLewis refactored and compiled the formalization.” SOURCE-PROVENANCE.json lists CTJLewis under credits as “Refactoring and compiling”. The label is this profile’s GitHub and X handle ctjlewis, matched ignoring case, and the proof sources are said to come from EvolvingPrograms/SquaresLean, the organization the public profile names as an affiliation.'
  provenance:
  - field: /display_name
    sources:
    - public-profile
    - announcement-receipt
  - field: /aliases
    sources:
    - formalization-acknowledgment
    - public-profile
  - field: /links
    sources:
    - formalization-acknowledgment
    - public-profile
    - github-social-crosslink
    - announcement-receipt
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
