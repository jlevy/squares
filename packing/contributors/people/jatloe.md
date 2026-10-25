---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: jatloe
  display_name: Jatloe
  aliases:
  - Jatloe
  - jatloe
  - '@jatloe'
  links:
  - kind: twitter
    url: https://x.com/jatloe
    handle: jatloe
  sources:
  - id: formalization-credit
    archive_path: packing/resources/web/jatloe-n12-lean-2026-10-16/Jatloe12SquaresFormalized/README.md
    url: https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/blob/d0caf4532a7ead68be1389ef87387b126fc2e0ab/README.md
    locator: 'Credits: “Jatloe provided the full mathematical proof and partial Lean formalization.” SOURCE-PROVENANCE.json repeats the credit; the source gives no other name and no account link.'
  - id: announcement-mention
    archive_path: packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/announcement/tweet-2113097037306569124.json
    url: https://x.com/ManassehA06/status/2113097037306569124
    locator: 'Manasseh Ahmed’s announcement of 22 October 2026 thanks “@jatloe for sending me a full proof of the result alongside a partial formalization”; entities.user_mentions gives screen_name jatloe, name jatloe, id_str 1339674174239944705.'
  - id: reply-mention
    archive_path: packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/announcement/tweet-2113097091580932578.json
    url: https://x.com/ManassehA06/status/2113097091580932578
    locator: 'The reply “@jatloe Lean repo:” links Queuingtheorydotcom/Jatloe12SquaresFormalized; entities.user_mentions gives the same id_str 1339674174239944705.'
  provenance:
  - field: /display_name
    sources: [formalization-credit]
  - field: /aliases
    sources: [formalization-credit, announcement-mention]
  - field: /links
    sources: [announcement-mention, reply-mention]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
