---
type: is
id: is-01m1w3nwm3vpjys7r8mxy2kf06
title: Correct active-session labeling in the generated cost summary
kind: bug
status: closed
priority: 2
version: 2
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels: []
dependencies: []
parent_id: is-01m1w140k75zvvqpvj55e8k9my
created_at: 2026-09-06T19:38:44.216Z
updated_at: 2026-09-06T20:12:29.137Z
closed_at: 2026-09-06T20:12:29.136Z
close_reason: Fixed and independently checked in ad71fc68, published PR103. Label now says unmeasured without inventing resource receipts. Focused renderer regression and both selected local gate tiers pass; parent think-exlq owns hosted follow-up.
resolution: null
duplicate_of: null
---
Adding live Session088 exposed an existing close_session renderer label bug: sessions_unmeasured correctly becomes 45, but SYNOPSIS calls all 45 closed before resource_rollups existed; only 44 are grandfathered and the new one is live with no receipt yet. Keep accounting values and session status unchanged. Fix the generator label or split active-unmeasured from historical-unmeasured, add a focused active-session control, and regenerate the existing views. This is display accuracy, not authority to invent a receipt or close the session.
