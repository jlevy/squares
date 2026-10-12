---
type: is
id: is-01m4pn087wev95haqgv9rffnj9
title: "Import Francisco Couzo: s(175) <= 13.767119024199 at 337078c, not named by #506 (no issue)"
kind: task
status: open
priority: 2
version: 4
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-11T23:33:08.475Z
updated_at: 2026-10-12T18:54:54.963Z
---
franciscouzo/square-packing 337078ca3e05153aceb099237b175cf64af5748a certificates/n175.cert (changed in f311f08, 2026-10-11T03:39:54Z), retained in the couzo-certificates-2026-10-11 packet by the #506 lane (think-om5l) and replayed there on both maintained exact routes. Smallest known at 175: below T-140 (#488) by 1.70e-6. #506 does not name it, so by result-import.md stage 1 it is an import of its own: ask the author whether it should be registered (draft in think-om5l's acknowledgement), then register from the same packet with the third route and a review.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/506 is where the ask goes; #506 has no reply yet. #528 (dostashev, 2026-10-12) now reports s(175) <= 13.764174317487, below this value. Listed on the tracker https://github.com/jlevy/squares/issues/544.

2026-10-12, layer 6 records lane (think-cq95): T-154 (#528, Daniil Ostashev) is registered at V3/C3 and adopted as the house at 175, 2.94e-03 below Couzo's 337078c certificate. By the 12 October review's RX-5 and stage 1 ("below the standing bound and asking for no work"), the certificate stays in the couzo-certificates-2026-10-11 packet, replayed and compared in its claim record and named in T-154's claim, and is not registered unless the author answers on #506 that he wants it to be. T-152's notes, the #506 request entry and the coverage note say so. This bead can close with that disposition once the #506 reply has said it.

2026-10-12, #558 review A1: the #506 final reply (https://github.com/jlevy/squares/issues/506#issuecomment-6130063939) followed main's not_registered for the unnamed 175, saying "175 is below the case's house, and its own import is queued", and asked nothing. So this bead's closing condition is not yet met: no reply has said that the certificate stays in the packet, and the author has not been asked whether he wants it registered. The follow-up on #506 waits for layer 6 (T-154's registration and adoption at 175) to be on main. It says that T-154 holds 175, 2.94e-03 below his certificate, which stays replayed in the packet and is not registered unless he wants it to be, and asks whether he does; it is recorded with an outdated statement on the final reply, which the follow-up names in corrects. The #506 request entry's notes say the same.
